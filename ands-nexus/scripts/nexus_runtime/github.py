"""Small GitHub Issues adapter with remote reconciliation before retrying writes.

The caller owns durable operation IDs and approvals. This adapter never creates
an operation ID, treats an Issue state as human acceptance, or deletes objects.
"""
from __future__ import annotations

from contextlib import contextmanager
from functools import wraps
import json
import math
import os
import re
import subprocess
import time
from typing import Any, Callable
from urllib.parse import urlunsplit


class GitHubError(Exception):
    """A failed operation; uncertain means a remote write may have happened."""

    def __init__(self, message: str, uncertain: bool = False):
        super().__init__(message)
        self.uncertain = uncertain


_LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
_REPO = re.compile(r"[A-Za-z0-9_.-]{1,100}\Z")
_OPERATION = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
_MARKER_PREFIX = "<!-- ands-nexus:operation="


def _scoped(method):
    """Nested public operations share the outer request budget."""
    @wraps(method)
    def invoke(self, *args, **kwargs):
        with self._scope():
            return method(self, *args, **kwargs)
    return invoke


class GitHubConnector:
    """Use the existing gh login for one explicitly configured github.com repo."""

    def __init__(self, repo: str, gh_path: str = "gh", timeout: float = 60,
                 cancel: Callable[[], bool] | None = None):
        parts = repo.split("/") if isinstance(repo, str) else []
        if (len(parts) != 2 or not _LOGIN.fullmatch(parts[0])
                or not _REPO.fullmatch(parts[1]) or parts[1] in {".", ".."}):
            raise GitHubError("Expected one explicit GitHub repository as owner/repo")
        if not isinstance(gh_path, str) or not gh_path or "\x00" in gh_path:
            raise GitHubError("Invalid gh executable")
        if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
                or not math.isfinite(timeout) or timeout <= 0):
            raise GitHubError("GitHub timeout must be a positive finite number")
        if cancel is not None and not callable(cancel):
            raise GitHubError("GitHub cancellation must be a callable or None")
        self.repo = repo
        self.gh_path = gh_path
        self.timeout = timeout
        self.cancel = cancel
        self._base = "repos/" + repo
        self._request_budget = None

    @contextmanager
    def _scope(self):
        if self._request_budget is not None:
            yield self._request_budget
            return
        if (isinstance(self.timeout, bool) or not isinstance(self.timeout, (int, float))
                or not math.isfinite(self.timeout) or self.timeout <= 0):
            raise GitHubError("GitHub timeout must be a positive finite number")
        budget = {"deadline": time.monotonic() + self.timeout, "write_dispatched": False}
        self._request_budget = budget
        try:
            yield budget
        finally:
            self._request_budget = None

    @staticmethod
    def _number(number: Any) -> int:
        if isinstance(number, bool) or not isinstance(number, int) or number <= 0:
            raise GitHubError("Issue number must be a positive integer")
        return number

    @staticmethod
    def _assignees(assignees: Any) -> list[str]:
        if not isinstance(assignees, list) or not assignees:
            raise GitHubError("Expected a non-empty list of explicit GitHub usernames")
        if any(not isinstance(login, str) or not _LOGIN.fullmatch(login) for login in assignees):
            raise GitHubError("Invalid GitHub assignee; special routing values are not supported")
        if len({login.casefold() for login in assignees}) != len(assignees):
            raise GitHubError("Duplicate GitHub assignee")
        return assignees

    @staticmethod
    def _text(value: Any, name: str, *, nonempty: bool = False) -> str:
        if not isinstance(value, str) or "\x00" in value or (nonempty and not value.strip()):
            raise GitHubError("Invalid " + name)
        return value

    @_scoped
    def _api(self, method: str, endpoint: str, payload: dict | None = None,
             *, paginate: bool = False) -> Any:
        mutation = method != "GET"
        command = [self.gh_path, "api", endpoint, "--hostname", "github.com",
                   "--method", method, "--header", "Accept: application/vnd.github+json"]
        if paginate:
            command.extend(["--paginate", "--slurp"])
        raw_input = None
        if payload is not None:
            command.extend(["--input", "-"])
            raw_input = json.dumps(payload, ensure_ascii=False)
        env = os.environ.copy()
        env["GH_PROMPT_DISABLED"] = "1"
        budget = self._request_budget
        previous_write = budget["write_dispatched"]
        # Check immediately before each actual request, not just when the
        # controller entered perform(). A preceding GET may observe a stop.
        if self.cancel is not None:
            try:
                cancelled = self.cancel()
            except Exception:
                raise GitHubError("Unable to verify cancellation status; request blocked", previous_write) from None
            if cancelled:
                raise GitHubError("GitHub operation cancelled before request dispatch", previous_write)
        remaining = budget["deadline"] - time.monotonic()
        if remaining <= 0:
            raise GitHubError("GitHub operation deadline exhausted before request dispatch", previous_write)
        if mutation:
            budget["write_dispatched"] = True
        try:
            completed = subprocess.run(command, input=raw_input, capture_output=True,
                                       text=True, encoding="utf-8", timeout=remaining,
                                       shell=False, env=env)
        except subprocess.TimeoutExpired:
            raise GitHubError("GitHub request timed out; reconcile before retrying", budget["write_dispatched"]) from None
        except OSError:
            budget["write_dispatched"] = previous_write
            raise GitHubError("Unable to start the configured gh executable", previous_write) from None
        if completed.returncode:
            # gh stderr can include private request content or credentials. Do
            # not expose it in logs or user-facing exceptions.
            status_match = re.search(r"\bHTTP[ /](\d{3})\b", completed.stderr or "")
            status = int(status_match.group(1)) if status_match else None
            known_rejection = status is not None and 400 <= status < 500 and status != 408
            if mutation and known_rejection:
                budget["write_dispatched"] = previous_write
            detail = ", HTTP " + str(status) if status else ""
            raise GitHubError(f"GitHub request failed (exit {completed.returncode}{detail})",
                              budget["write_dispatched"])
        if not completed.stdout.strip():
            return None
        try:
            return json.loads(completed.stdout)
        except (ValueError, TypeError):
            raise GitHubError("GitHub returned an invalid JSON response", budget["write_dispatched"]) from None

    def _issue(self, data: Any) -> dict:
        if not isinstance(data, dict) or "pull_request" in data:
            raise GitHubError("GitHub response is not an Issue")
        number = self._number(data.get("number"))
        expected = urlunsplit(("https", "github.com", f"/{self.repo}/issues/{number}", "", ""))
        if not isinstance(data.get("html_url"), str) or data["html_url"].casefold() != expected.casefold():
            raise GitHubError("GitHub Issue response does not belong to the configured repository")
        if not isinstance(data.get("id"), int) or isinstance(data["id"], bool) or data["id"] <= 0:
            raise GitHubError("GitHub Issue response has no remote ID")
        if data.get("state") not in {"open", "closed"} or not isinstance(data.get("assignees"), list):
            raise GitHubError("GitHub Issue response has invalid state or assignees")
        if any(not isinstance(item, dict) or not isinstance(item.get("login"), str)
               for item in data["assignees"]):
            raise GitHubError("GitHub Issue response has invalid assignees")
        return dict(data, url=data["html_url"])

    def _comment(self, data: Any, number: int) -> dict:
        if (not isinstance(data, dict) or isinstance(data.get("id"), bool)
                or not isinstance(data.get("id"), int) or data["id"] <= 0):
            raise GitHubError("GitHub comment response has no remote ID")
        expected = urlunsplit(("https", "github.com", f"/{self.repo}/issues/{number}", "",
                               f"issuecomment-{data['id']}"))
        if not isinstance(data.get("html_url"), str) or data["html_url"].casefold() != expected.casefold():
            raise GitHubError("GitHub comment response does not belong to the configured Issue")
        return dict(data, number=number, url=data["html_url"])

    def _list(self, endpoint: str) -> list[dict]:
        pages = self._api("GET", endpoint, paginate=True)
        if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
            raise GitHubError("GitHub returned an invalid paginated response")
        records = [record for page in pages for record in page]
        if any(not isinstance(record, dict) for record in records):
            raise GitHubError("GitHub returned invalid paginated records")
        return records

    def _find(self, endpoint: str, marker: str, number: int | None = None) -> dict | None:
        records = self._list(endpoint)
        if any(item.get("body") is not None and not isinstance(item["body"], str) for item in records):
            raise GitHubError("GitHub returned an invalid object body; no new write was attempted")
        found = [item for item in records
                 if "pull_request" not in item and marker in (item.get("body") or "")]
        if len(found) > 1:
            raise GitHubError("Multiple remote objects have the same operation marker; manual review required", True)
        if not found:
            return None
        return self._issue(found[0]) if number is None else self._comment(found[0], number)

    @_scoped
    def preflight(self) -> dict:
        """Read-only authentication and repository capability check."""
        user = self._api("GET", "user")
        if not isinstance(user, dict) or not isinstance(user.get("login"), str) or not _LOGIN.fullmatch(user["login"]):
            raise GitHubError("Unable to identify the authenticated GitHub user")
        repo = self._api("GET", self._base)
        if (not isinstance(repo, dict) or not isinstance(repo.get("full_name"), str)
                or repo["full_name"].casefold() != self.repo.casefold()):
            raise GitHubError("Repository lookup did not match the configured repository")
        if repo.get("has_issues") is not True:
            raise GitHubError("Issues are not enabled for the configured repository")
        return {"full_name": repo["full_name"], "has_issues": True,
                "authenticated_user": user["login"], "permissions": repo.get("permissions", {})}

    @_scoped
    def validate_assignees(self, assignees: list[str]) -> list[str]:
        """Check every explicit username; never silently replace a teammate."""
        if isinstance(assignees, list) and not assignees:
            return []
        names = self._assignees(assignees)
        for login in names:
            self._api("GET", self._base + "/assignees/" + login)
        return list(names)

    @_scoped
    def read_issue(self, number: int) -> dict:
        number = self._number(number)
        data = self._issue(self._api("GET", f"{self._base}/issues/{number}"))
        if data["number"] != number:
            raise GitHubError("GitHub returned a different Issue number")
        return data

    @_scoped
    def perform(self, kind: str, operation_id: str, payload: dict) -> dict:
        """Execute exactly one approved operation, reconciling uncertain writes.

        An uncertain failure is returned to the durable parent scheduler. This
        function never performs a second create/assign/comment/close blindly.
        """
        marker = self._validate_operation(kind, operation_id, payload)
        if kind in {"create_issue", "comment_issue"}:
            body = payload["body"] + "\n\n" + marker
        if kind == "create_issue":
            endpoint = self._base + "/issues"
            finder = lambda: self._find(endpoint + "?state=all&per_page=100", marker)
            found = finder()
            if found:
                return found
            return self._write("POST", endpoint, {"title": payload["title"], "body": body}, finder, self._issue)
        number = payload["number"]
        endpoint = f"{self._base}/issues/{number}"
        if kind == "comment_issue":
            finder = lambda: self._find(endpoint + "/comments?per_page=100", marker, number)
            found = finder()
            if found:
                return found
            return self._write("POST", endpoint + "/comments", {"body": body}, finder,
                               lambda value: self._comment(value, number))
        if kind == "assign_issue":
            names = payload["assignees"]
            desired = {name.casefold() for name in names}

            def satisfied():
                return self.reconcile(kind, operation_id, payload)

            found = satisfied()
            if found:
                return found

            def validate_assignment(value):
                value = self._issue(value)
                actual = {item["login"].casefold() for item in value["assignees"]}
                if value["number"] != number or not desired <= actual:
                    raise GitHubError("GitHub did not confirm all requested assignees", True)
                return value

            return self._write("POST", endpoint + "/assignees", {"assignees": names}, satisfied, validate_assignment)

        def closed():
            return self.reconcile(kind, operation_id, payload)

        found = closed()
        if found:
            return found

        def validate_closed(value):
            value = self._issue(value)
            if value["number"] != number or value["state"] != "closed":
                raise GitHubError("GitHub did not confirm the Issue was closed", True)
            return value

        return self._write("PATCH", endpoint, {"state": "closed"}, closed, validate_closed)

    def _validate_operation(self, kind, operation_id, payload):
        expected_keys = {"create_issue": {"title", "body"},
                         "assign_issue": {"number", "assignees"},
                         "comment_issue": {"number", "body"},
                         "close_issue": {"number"}}
        if not isinstance(kind, str) or kind not in expected_keys:
            raise GitHubError("Unsupported GitHub operation")
        if not isinstance(operation_id, str) or not _OPERATION.fullmatch(operation_id):
            raise GitHubError("Invalid stable GitHub operation ID")
        if not isinstance(payload, dict) or set(payload) != expected_keys[kind]:
            raise GitHubError("Unexpected or missing GitHub operation fields")
        marker = _MARKER_PREFIX + operation_id + " -->"
        if kind in {"create_issue", "comment_issue"}:
            body = self._text(payload["body"], "Issue body")
            if _MARKER_PREFIX in body:
                raise GitHubError("Operation markers are reserved for the connector")
            if len(body + "\n\n" + marker) > 65536:
                raise GitHubError("Issue body exceeds GitHub's supported size")
        if kind == "create_issue":
            title = self._text(payload["title"], "Issue title", nonempty=True)
            if len(title) > 256 or "\n" in title or "\r" in title:
                raise GitHubError("Invalid Issue title length or line break")
        else:
            self._number(payload["number"])
        if kind == "assign_issue":
            self._assignees(payload["assignees"])
        return marker

    @_scoped
    def reconcile(self, kind: str, operation_id: str, payload: dict) -> dict | None:
        """Only read remote state for an operation already persisted as uncertain.

        None means the outcome is still unknown, not permission to retry a
        creation. The caller must retain its uncertain state or seek a human
        decision. No mutation is made by this method.
        """
        marker = self._validate_operation(kind, operation_id, payload)
        if kind == "create_issue":
            return self._find(self._base + "/issues?state=all&per_page=100", marker)
        number = payload["number"]
        endpoint = f"{self._base}/issues/{number}"
        if kind == "comment_issue":
            return self._find(endpoint + "/comments?per_page=100", marker, number)
        current = self.read_issue(number)
        if kind == "assign_issue":
            desired = {name.casefold() for name in payload["assignees"]}
            actual = {item["login"].casefold() for item in current["assignees"]}
            return current if desired <= actual else None
        return current if current["state"] == "closed" else None

    def _write(self, method, endpoint, payload, reconcile, validate):
        try:
            value = self._api(method, endpoint, payload)
            try:
                return validate(value)
            except GitHubError:
                raise GitHubError("GitHub write response could not be verified", True) from None
        except GitHubError as failure:
            if not failure.uncertain:
                raise
            try:
                found = reconcile()
            except GitHubError as recovery_error:
                raise GitHubError("GitHub write outcome is uncertain; " + str(recovery_error), True) from None
            if found:
                return found
            raise failure from None
