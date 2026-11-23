"""GitHub boundary tests: exercise recovery while the network is simulated."""
import importlib
import inspect
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "ands-nexus" / "scripts"
sys.path.insert(0, str(SCRIPTS))
try:
    github = importlib.import_module("nexus_runtime.github")
except ModuleNotFoundError:
    github = None


def issue(number=7, body="", assignees=(), state="open"):
    return {"id": 1000 + number, "number": number,
            "html_url": f"https://github.com/example/team/issues/{number}",
            "body": body, "title": "任务", "state": state,
            "assignees": [{"login": name} for name in assignees]}


def response(value=None, code=0, stderr=""):
    return subprocess.CompletedProcess([], code,
                                       "" if value is None else json.dumps(value), stderr)


class ConnectorAvailabilityTest(unittest.TestCase):
    def test_connector_is_implemented(self):
        self.assertIsNotNone(github, "GitHub recovery connector has not been implemented")


@unittest.skipIf(github is None, "Connector not implemented yet")
class GitHubConnectorTest(unittest.TestCase):
    def setUp(self):
        self.client = github.GitHubConnector("example/team")
        self.marker = "<!-- ands-nexus:operation=op-1 -->"

    def test_create_uses_json_stdin_and_preserves_literal_text(self):
        body = "中文 `literal` $(not-a-command) 'quote'\nnext line"
        with patch.object(github.subprocess, "run", side_effect=[
                response([[]]), response(issue(body=body + "\n\n" + self.marker))]) as run:
            result = self.client.perform("create_issue", "op-1", {"title": "标题", "body": body})
        self.assertEqual(result["number"], 7)
        self.assertEqual(result["url"], "https://github.com/example/team/issues/7")
        args, kwargs = run.call_args
        self.assertNotIn(body, args[0])
        self.assertFalse(kwargs.get("shell", False))
        self.assertEqual(json.loads(kwargs["input"])["body"], body + "\n\n" + self.marker)
        self.assertIn("--input", args[0])

    def test_repeat_create_finds_closed_issue_on_second_page(self):
        found = issue(body=self.marker, state="closed")
        with patch.object(github.subprocess, "run", return_value=response([
                [issue(number=1)], [found]])) as run:
            result = self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertEqual(result["number"], 7)
        self.assertEqual(run.call_count, 1)
        argv = run.call_args.args[0]
        self.assertIn("--paginate", argv)
        self.assertIn("--slurp", argv)
        self.assertTrue(any("state=all" in value for value in argv))

    def test_create_response_lost_is_reconciled_without_recreating(self):
        found = issue(body=self.marker)
        with patch.object(github.subprocess, "run", side_effect=[
                response([[]]), subprocess.TimeoutExpired("gh", 60),
                response([[found]])]) as run:
            result = self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertEqual(result["number"], 7)
        self.assertEqual(sum("POST" in call.args[0] for call in run.call_args_list), 1)

    def test_unresolved_create_uncertainty_does_not_retry(self):
        with patch.object(github.subprocess, "run", side_effect=[
                response([[]]), subprocess.TimeoutExpired("gh", 60), response([[]])]) as run:
            with self.assertRaises(github.GitHubError) as error:
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertTrue(error.exception.uncertain)
        self.assertEqual(run.call_count, 3)
        self.assertEqual(sum("POST" in call.args[0] for call in run.call_args_list), 1)

    def test_duplicate_markers_stop_instead_of_selecting_an_issue(self):
        with patch.object(github.subprocess, "run", return_value=response([
                [issue(1, self.marker), issue(2, self.marker)]])) as run:
            with self.assertRaises(github.GitHubError):
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertEqual(run.call_count, 1)

    def test_pull_requests_are_excluded_from_issue_reconciliation(self):
        pr = issue(1, self.marker)
        pr["pull_request"] = {"url": "not-an-issue"}
        with patch.object(github.subprocess, "run", side_effect=[response([[pr]]),
                response(issue(body=self.marker))]) as run:
            result = self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertEqual(result["number"], 7)
        self.assertEqual(run.call_count, 2)

    def test_assign_preserves_existing_assignees_and_is_repeatable(self):
        with patch.object(github.subprocess, "run", side_effect=[
                response(issue(assignees=["existing"])),
                response(issue(assignees=["existing", "alice"]))]) as run:
            result = self.client.perform("assign_issue", "op-1", {"number": 7, "assignees": ["alice"]})
        self.assertEqual(json.loads(run.call_args.kwargs["input"]), {"assignees": ["alice"]})
        self.assertEqual({item["login"] for item in result["assignees"]}, {"existing", "alice"})
        with patch.object(github.subprocess, "run", return_value=response(issue(assignees=["existing", "alice"]))) as run:
            self.client.perform("assign_issue", "op-1", {"number": 7, "assignees": ["alice"]})
        self.assertEqual(run.call_count, 1)

    def test_assignment_failure_does_not_create_another_issue(self):
        with patch.object(github.subprocess, "run", side_effect=[
                response(issue()), response(code=1, stderr="assignee forbidden (HTTP 422)")]) as run:
            with self.assertRaises(github.GitHubError) as error:
                self.client.perform("assign_issue", "op-assign", {"number": 7, "assignees": ["alice"]})
        self.assertFalse(error.exception.uncertain)
        self.assertEqual(run.call_count, 2)
        self.assertTrue(all("issues/7" in " ".join(call.args[0]) for call in run.call_args_list))

    def test_uncertain_assignment_reads_back_before_returning_success(self):
        with patch.object(github.subprocess, "run", side_effect=[
                response(issue()), subprocess.TimeoutExpired("gh", 60),
                response(issue(assignees=["alice"]))]) as run:
            result = self.client.perform("assign_issue", "op-1", {"number": 7, "assignees": ["alice"]})
        self.assertEqual(result["assignees"], [{"login": "alice"}])
        self.assertEqual(run.call_count, 3)

    def test_assignment_silent_non_application_is_not_success(self):
        with patch.object(github.subprocess, "run", side_effect=[response(issue()), response(issue()), response(issue())]):
            with self.assertRaises(github.GitHubError):
                self.client.perform("assign_issue", "op-1", {"number": 7, "assignees": ["alice"]})

    def test_comment_response_lost_is_reconciled_and_repeatable(self):
        found = {"id": 81, "html_url": "https://github.com/example/team/issues/7#issuecomment-81", "body": self.marker}
        with patch.object(github.subprocess, "run", side_effect=[
                response([[]]), response(code=1, stderr="connection reset"), response([[found]])]) as run:
            result = self.client.perform("comment_issue", "op-1", {"number": 7, "body": "done"})
        self.assertEqual(result["id"], 81)
        self.assertEqual(sum("POST" in call.args[0] for call in run.call_args_list), 1)
        with patch.object(github.subprocess, "run", return_value=response([[found]])) as run:
            self.client.perform("comment_issue", "op-1", {"number": 7, "body": "done"})
        self.assertEqual(run.call_count, 1)

    def test_close_checks_current_state_and_preserves_other_fields(self):
        with patch.object(github.subprocess, "run", side_effect=[response(issue()), response(issue(state="closed"))]) as run:
            self.client.perform("close_issue", "op-1", {"number": 7})
        self.assertEqual(json.loads(run.call_args.kwargs["input"]), {"state": "closed"})
        with patch.object(github.subprocess, "run", return_value=response(issue(state="closed"))) as run:
            self.client.perform("close_issue", "op-1", {"number": 7})
        self.assertEqual(run.call_count, 1)

    def test_timeout_after_close_is_reconciled(self):
        with patch.object(github.subprocess, "run", side_effect=[response(issue()),
                subprocess.TimeoutExpired("gh", 60), response(issue(state="closed"))]):
            result = self.client.perform("close_issue", "op-1", {"number": 7})
        self.assertEqual(result["state"], "closed")

    def test_preflight_and_assignees_use_read_only_endpoints(self):
        repo = {"full_name": "example/team", "has_issues": True, "permissions": {"push": True}}
        with patch.object(github.subprocess, "run", side_effect=[response({"login": "owner"}), response(repo), response(), response()]) as run:
            self.assertEqual(self.client.preflight()["full_name"], "example/team")
            self.assertEqual(self.client.validate_assignees(["alice", "bob"]), ["alice", "bob"])
        self.assertTrue(all("GET" in call.args[0] for call in run.call_args_list))

    def test_repo_without_issues_is_rejected(self):
        with patch.object(github.subprocess, "run", side_effect=[response({"login": "owner"}), response({"full_name": "example/team", "has_issues": False})]):
            with self.assertRaises(github.GitHubError):
                self.client.preflight()

    def test_unknown_assignee_is_not_silently_removed(self):
        with patch.object(github.subprocess, "run", return_value=response(code=1, stderr="Not Found (HTTP 404)")):
            with self.assertRaises(github.GitHubError) as error:
                self.client.validate_assignees(["unknown"])
        self.assertFalse(error.exception.uncertain)

    def test_empty_roster_needs_no_assignee_requests(self):
        with patch.object(github.subprocess, "run") as run:
            self.assertEqual(self.client.validate_assignees([]), [])
        run.assert_not_called()

    def test_uncertain_operation_recovery_is_read_only_when_not_found(self):
        recover = getattr(self.client, "reconcile", None)
        self.assertTrue(callable(recover), "Persisted uncertainty needs a read-only recovery entry")
        with patch.object(github.subprocess, "run", return_value=response([[]])) as run:
            self.assertIsNone(recover("create_issue", "op-1", {"title": "task", "body": "text"}))
        self.assertEqual(run.call_count, 1)
        self.assertIn("GET", run.call_args.args[0])

    def test_read_only_recovery_observes_assignment_and_close(self):
        recover = getattr(self.client, "reconcile", None)
        self.assertTrue(callable(recover), "Persisted uncertainty needs a read-only recovery entry")
        with patch.object(github.subprocess, "run", side_effect=[
                response(issue(assignees=["alice"])), response(issue(state="closed"))]) as run:
            self.assertEqual(recover("assign_issue", "op-a", {"number": 7, "assignees": ["alice"]})["number"], 7)
            self.assertEqual(recover("close_issue", "op-c", {"number": 7})["state"], "closed")
        self.assertTrue(all("GET" in call.args[0] for call in run.call_args_list))

    def test_auth_error_is_definite_and_does_not_leak_stderr(self):
        with patch.object(github.subprocess, "run", return_value=response(code=1, stderr="private-token-value (HTTP 401)")):
            with self.assertRaises(github.GitHubError) as error:
                self.client.read_issue(7)
        self.assertFalse(error.exception.uncertain)
        self.assertNotIn("private-token-value", str(error.exception))

    def test_foreign_remote_url_cannot_be_accepted_as_current_repo_result(self):
        foreign = issue()
        foreign["html_url"] = "https://github.com/other/repo/issues/7"
        with patch.object(github.subprocess, "run", return_value=response(foreign)):
            with self.assertRaises(github.GitHubError):
                self.client.read_issue(7)

    def test_unexpected_response_json_is_not_success(self):
        with patch.object(github.subprocess, "run", return_value=response({"message": "not-an-issue"})):
            with self.assertRaises(github.GitHubError):
                self.client.read_issue(7)

    def test_uncertain_create_reconciliation_failure_preserves_uncertainty(self):
        with patch.object(github.subprocess, "run", side_effect=[response([[]]),
                subprocess.TimeoutExpired("gh", 60), response(code=1, stderr="offline")]) as run:
            with self.assertRaises(github.GitHubError) as error:
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertTrue(error.exception.uncertain)
        self.assertEqual(sum("POST" in call.args[0] for call in run.call_args_list), 1)

    def test_comment_marker_cannot_be_injected_from_content(self):
        with patch.object(github.subprocess, "run") as run:
            with self.assertRaises(github.GitHubError):
                self.client.perform("comment_issue", "op-1", {"number": 7, "body": self.marker})
        run.assert_not_called()

    def test_malformed_remote_body_is_rejected_without_a_write(self):
        malformed = issue()
        malformed["body"] = {"unexpected": "object"}
        with patch.object(github.subprocess, "run", return_value=response([[malformed]])) as run:
            with self.assertRaises(github.GitHubError):
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertEqual(run.call_count, 1)

    def test_reconciliation_does_not_accept_a_different_issue_number(self):
        with patch.object(github.subprocess, "run", return_value=response(issue(8))):
            with self.assertRaises(github.GitHubError):
                self.client.read_issue(7)

    def test_constructor_accepts_optional_cancellation(self):
        self.assertIn("cancel", inspect.signature(github.GitHubConnector).parameters)
        client = github.GitHubConnector("example/team", cancel=lambda: True)
        with patch.object(github.subprocess, "run") as run:
            with self.assertRaisesRegex(github.GitHubError, "cancel") as failure:
                client.read_issue(7)
        self.assertFalse(failure.exception.uncertain)
        run.assert_not_called()

    def test_cancel_after_marker_get_does_not_dispatch_creation(self):
        cancelled = [False]
        self.client.cancel = lambda: cancelled[0]
        def request(argv, **kwargs):
            if "GET" in argv:
                cancelled[0] = True
                return response([[]])
            return response(issue(body=self.marker))
        with patch.object(github.subprocess, "run", side_effect=request) as run:
            with self.assertRaisesRegex(github.GitHubError, "cancel") as failure:
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertFalse(failure.exception.uncertain)
        self.assertEqual(run.call_count, 1)

    def test_cancel_after_issue_get_does_not_dispatch_assignment_or_close(self):
        for kind, payload in [("assign_issue", {"number": 7, "assignees": ["alice"]}),
                              ("close_issue", {"number": 7})]:
            with self.subTest(kind=kind):
                cancelled = [False]
                self.client.cancel = lambda: cancelled[0]
                def request(argv, **kwargs):
                    if "GET" in argv:
                        cancelled[0] = True
                        return response(issue())
                    return response(issue(assignees=["alice"], state="closed"))
                with patch.object(github.subprocess, "run", side_effect=request) as run:
                    with self.assertRaisesRegex(github.GitHubError, "cancel"):
                        self.client.perform(kind, "op-1", payload)
                self.assertEqual(run.call_count, 1)

    def test_cancel_after_uncertain_write_preserves_uncertainty(self):
        cancelled = [False]
        self.client.cancel = lambda: cancelled[0]
        def request(argv, **kwargs):
            if "POST" in argv:
                cancelled[0] = True
                raise subprocess.TimeoutExpired("gh", 60)
            return response([[]])
        with patch.object(github.subprocess, "run", side_effect=request) as run:
            with self.assertRaisesRegex(github.GitHubError, "cancel") as failure:
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertTrue(failure.exception.uncertain)
        self.assertEqual(run.call_count, 2)

    def test_create_get_and_post_share_one_timeout_deadline(self):
        clock = [100.0]
        self.client.timeout = 5
        def request(argv, **kwargs):
            if "GET" in argv:
                clock[0] += 4
                return response([[]])
            return response(issue(body=self.marker))
        with patch("time.monotonic", side_effect=lambda: clock[0]), patch.object(github.subprocess, "run", side_effect=request) as run:
            self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertEqual([call.kwargs["timeout"] for call in run.call_args_list], [5, 1])

    def test_deadline_exhausted_by_get_prevents_creation(self):
        clock = [100.0]
        self.client.timeout = 5
        def request(argv, **kwargs):
            if "GET" in argv:
                clock[0] += 6
                return response([[]])
            return response(issue(body=self.marker))
        with patch("time.monotonic", side_effect=lambda: clock[0]), patch.object(github.subprocess, "run", side_effect=request) as run:
            with self.assertRaisesRegex(github.GitHubError, "deadline") as failure:
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertFalse(failure.exception.uncertain)
        self.assertEqual(run.call_count, 1)

    def test_preflight_requests_share_one_timeout_deadline(self):
        clock = [100.0]
        self.client.timeout = 3
        def request(argv, **kwargs):
            if "user" in argv:
                clock[0] += 2.5
                return response({"login": "owner"})
            return response({"full_name": "example/team", "has_issues": True})
        with patch("time.monotonic", side_effect=lambda: clock[0]), patch.object(github.subprocess, "run", side_effect=request) as run:
            self.client.preflight()
        self.assertEqual([call.kwargs["timeout"] for call in run.call_args_list], [3, .5])

    def test_assignee_validation_requests_share_one_timeout_deadline(self):
        clock = [100.0]
        self.client.timeout = 1
        def request(argv, **kwargs):
            clock[0] += .5
            return response()
        with patch("time.monotonic", side_effect=lambda: clock[0]), patch.object(github.subprocess, "run", side_effect=request) as run:
            self.client.validate_assignees(["alice", "bob"])
        self.assertEqual([call.kwargs["timeout"] for call in run.call_args_list], [1, .5])

    def test_nested_reconciliation_keeps_original_deadline(self):
        clock = [100.0]
        self.client.timeout = 5
        requests = []
        def request(argv, **kwargs):
            requests.append(argv)
            if "POST" in argv:
                clock[0] += 2
                raise subprocess.TimeoutExpired("gh", kwargs["timeout"])
            if len(requests) == 1:
                clock[0] += 1
                return response([[]])
            return response([[issue(body=self.marker)]])
        with patch("time.monotonic", side_effect=lambda: clock[0]), patch.object(github.subprocess, "run", side_effect=request) as run:
            self.assertEqual(self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})["number"], 7)
        self.assertEqual([call.kwargs["timeout"] for call in run.call_args_list], [5, 4, 2])

    def test_deadline_after_uncertain_write_preserves_uncertainty(self):
        clock = [100.0]
        self.client.timeout = 5
        def request(argv, **kwargs):
            if "POST" in argv:
                clock[0] += 5
                raise subprocess.TimeoutExpired("gh", kwargs["timeout"])
            clock[0] += 1
            return response([[]])
        with patch("time.monotonic", side_effect=lambda: clock[0]), patch.object(github.subprocess, "run", side_effect=request) as run:
            with self.assertRaises(github.GitHubError) as failure:
                self.client.perform("create_issue", "op-1", {"title": "task", "body": "text"})
        self.assertTrue(failure.exception.uncertain)
        self.assertIn("deadline", str(failure.exception))
        self.assertEqual(run.call_count, 2)

    def test_invalid_inputs_do_not_start_gh(self):
        with patch.object(github.subprocess, "run") as run:
            for repo in ["https://github.com/example/team", "example/team/extra", "../team", "example/team?x=1"]:
                with self.assertRaises(github.GitHubError):
                    github.GitHubConnector(repo)
            for number in [True, 0, -1, "7/../../other"]:
                with self.assertRaises(github.GitHubError):
                    self.client.read_issue(number)
            for kind, operation, payload in [
                    ("delete_issue", "op-1", {"number": 7}),
                    ("create_issue", "op-1\n-->bad", {"title": "task", "body": "x"}),
                    ("create_issue", "op-1", {"title": "task", "body": "x", "repo": "other/repo"}),
                    ("assign_issue", "op-1", {"number": 7, "assignees": ["@copilot"]})]:
                with self.assertRaises(github.GitHubError):
                    self.client.perform(kind, operation, payload)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
