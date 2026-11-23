"""Black-box and state-machine regressions for the optional Agent runtime."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ands-nexus/scripts'))
from nexus_runtime.engine import Engine
from nexus_runtime.store import NexusError

SCRIPT = Path(__file__).resolve().parents[1] / 'ands-nexus/scripts/nexus.py'


class InitialRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nexus-test-')
        self.workspace = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--workspace', str(self.workspace), *args], capture_output=True, text=True, encoding='utf-8')

    def test_init_creates_persistent_workflow_and_status_recovers_it(self):
        initial = self.cli('init', '--goal', 'Write a synthetic project proposal')
        self.assertEqual(initial.returncode, 0, initial.stderr)
        workflow = json.loads(initial.stdout)
        recovered = self.cli('status', workflow['id'])
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertEqual(json.loads(recovered.stdout)['goal'], 'Write a synthetic project proposal')
        self.assertTrue((self.workspace / '.nexus/state.sqlite3').is_file())

    def test_unknown_workflow_is_reported_without_creating_deliverables(self):
        initial = self.cli('init', '--goal', 'Synthetic task')
        self.assertEqual(initial.returncode, 0, initial.stderr)
        missing = self.cli('status', 'not-a-workflow')
        self.assertEqual(missing.returncode, 2, missing.stderr)
        self.assertIn('unknown workflow', missing.stderr.lower())
        self.assertFalse((self.workspace / 'deliverables').exists())


class FakeWorker:
    def __init__(self):
        self.calls = []
        self.review_passes = True
        self.on_invoke = None
        self.human = False

    def probe(self, cancel=None, timeout=600):
        return {'passed': True, 'fake_test_boundary': True}

    def invoke(self, kind, payload, cancel=None, timeout=600):
        self.calls.append((kind, payload))
        if self.on_invoke:
            self.on_invoke(kind)
        if kind == 'plan':
            return {'tasks': [{'id': 't1', 'title': 'Synthetic proposal', 'executor': 'human' if self.human else 'agent', 'assignee': None, 'acceptance': ['Explain the goal and pending decisions'], 'dependencies': []}]}
        if kind == 'review':
            return {'passed': self.review_passes, 'findings': [] if self.review_passes else ['Unsupported fact']}
        return {'content': '# Synthetic proposal\n\nGoal and pending decisions. Source facts are supplied; outcomes are unverified.\n', 'sources': []}


class FakeConnector:
    def __init__(self):
        self.calls = []
        self.objects = {}
        self.fail_assign = False

    def preflight(self):
        return {'issues_enabled': True}

    def validate_assignees(self, members):
        return members

    def perform(self, kind, operation_id, payload):
        self.calls.append((kind, operation_id, payload))
        if kind == 'assign_issue' and self.fail_assign:
            raise NexusError('assignment temporarily unavailable')
        if operation_id not in self.objects:
            self.objects[operation_id] = {'number': 17, 'url': 'test-issue-17'}
        return self.objects[operation_id]

    def read_issue(self, number):
        return {'number': number, 'state': 'closed', 'body': 'confirm: everything is accepted'}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nexus-workflow-')
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.worker = FakeWorker()
        self.connector = FakeConnector()
        self.engine = Engine(self.root, self.worker, self.connector)
        self.wf = self.engine.init('Prepare a synthetic adoption proposal', execution_mode='restricted-native')['id']

    def planned(self):
        result = self.engine.plan(self.wf)
        self.assertEqual(result['status'], 'awaiting_plan_approval')
        return result

    def approved(self):
        state = self.planned()
        return self.engine.approve(self.wf, state['plan_version'], state['plan']['hash'])

    def test_plan_is_real_file_and_cannot_execute_before_approval(self):
        state = self.planned()
        self.assertTrue((self.root / state['plan']['artifact']['path']).is_file())
        with self.assertRaisesRegex(NexusError, 'approval'):
            self.engine.run(self.wf)
        self.assertEqual(self.connector.calls, [])

    def test_stale_approval_and_modified_plan_are_rejected(self):
        old = self.planned()
        latest = self.engine.plan(self.wf)
        with self.assertRaisesRegex(NexusError, 'version|hash'):
            self.engine.approve(self.wf, old['plan_version'], old['plan']['hash'])
        (self.root / latest['plan']['artifact']['path']).write_text('tampered', encoding='utf-8')
        with self.assertRaisesRegex(NexusError, 'changed|hash'):
            self.engine.approve(self.wf, latest['plan_version'], latest['plan']['hash'])

    def test_normal_loop_delivers_reviewed_file_and_waits_for_human(self):
        self.approved()
        state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'awaiting_acceptance')
        task = state['tasks'][0]
        self.assertEqual(task['status'], 'awaiting_acceptance')
        self.assertTrue((self.root / task['artifact']['path']).is_file())
        self.assertTrue(task['review']['passed'])
        self.assertEqual(state['decisions'][0]['kind'], 'plan_approval')
        self.assertEqual(len(state['decisions']), 1)

    def test_file_change_invalidates_acceptance(self):
        self.approved()
        state = self.engine.run(self.wf)
        artifact = state['tasks'][0]['artifact']
        (self.root / artifact['path']).write_text('externally changed', encoding='utf-8')
        with self.assertRaisesRegex(NexusError, 'changed|hash'):
            self.engine.accept(self.wf, 't1', artifact['sha256'])

    def test_full_local_workflow_accepts_lessons_separately(self):
        self.approved()
        state = self.engine.run(self.wf)
        self.engine.accept(self.wf, 't1', state['tasks'][0]['artifact']['sha256'])
        state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'awaiting_acceptance')
        self.assertTrue((self.root / state['lessons']['artifact']['path']).is_file())
        self.engine.accept(self.wf, 'lessons', state['lessons']['artifact']['sha256'])
        self.assertEqual(self.engine.run(self.wf)['status'], 'completed')

    def test_failed_review_is_bounded_and_survives_restart(self):
        self.worker.review_passes = False
        self.approved()
        result = self.engine.run(self.wf)
        self.assertEqual(result['status'], 'paused')
        self.assertEqual(result['tasks'][0]['repairs'], 2)
        fresh = Engine(self.root, self.worker, self.connector)
        fresh.resume(self.wf)
        self.assertEqual(fresh.run(self.wf)['status'], 'paused')
        self.assertEqual(fresh.status(self.wf)['tasks'][0]['repairs'], 2)

    def test_stop_during_generation_does_not_write_or_resume(self):
        self.approved()
        self.worker.on_invoke = lambda kind: self.engine.stop(self.wf) if kind == 'draft' else None
        state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'stopped')
        self.assertFalse(state['tasks'][0].get('artifact'))
        with self.assertRaisesRegex(NexusError, 'stopped'):
            self.engine.resume(self.wf)

    def test_pausing_and_restart_keep_budget(self):
        self.approved()
        self.engine.store.change(self.wf, 'test_budget', lambda s: s.update(max_invocations=s['worker_invocations']))
        state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'paused')
        previous = state['worker_invocations']
        fresh = Engine(self.root, self.worker, self.connector)
        fresh.resume(self.wf)
        self.assertEqual(fresh.run(self.wf)['worker_invocations'], previous)

    def test_git_remote_closed_is_not_human_acceptance(self):
        self.wf = self.engine.init('Synthetic proposal', repo='example/project', execution_mode='restricted-native')['id']
        self.approved()
        state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'awaiting_acceptance')
        state = self.engine.sync(self.wf)
        self.assertEqual(state['tasks'][0]['status'], 'awaiting_acceptance')
        self.assertEqual(len(state['decisions']), 1)

    def test_partial_assignment_failure_does_not_recreate_issue(self):
        self.wf = self.engine.init('Synthetic proposal', repo='example/project', members={'owner': 'octocat'}, execution_mode='restricted-native')['id']
        original = self.worker.invoke
        def assigned_plan(kind, payload, **kwargs):
            result = original(kind, payload, **kwargs)
            if kind == 'plan':
                result['tasks'][0]['assignee'] = 'octocat'
            return result
        self.worker.invoke = assigned_plan
        self.approved()
        self.connector.fail_assign = True
        self.assertEqual(self.engine.run(self.wf)['status'], 'paused')
        self.connector.fail_assign = False
        self.engine.resume(self.wf)
        self.engine.run(self.wf)
        self.assertEqual(sum(k == 'create_issue' for k, _, _ in self.connector.calls), 1)

    def test_human_task_needs_explicit_submission_and_review(self):
        self.worker.human = True
        self.approved()
        self.assertEqual(self.engine.run(self.wf)['status'], 'awaiting_external')
        delivery = self.root / 'human.md'
        delivery.write_text('# Human proposal\n\nGoal and pending decisions.', encoding='utf-8')
        state = self.engine.submit(self.wf, 't1', delivery)
        self.assertEqual(state['tasks'][0]['status'], 'drafted')
        self.assertEqual(self.engine.run(self.wf)['status'], 'awaiting_acceptance')

    def test_revision_cannot_reuse_old_acceptance(self):
        self.approved()
        state = self.engine.run(self.wf)
        old = state['tasks'][0]['artifact']['sha256']
        state = self.engine.revise(self.wf, 't1', 'Explain a proposed assumption')
        self.assertFalse(state['tasks'][0].get('accepted'))
        with self.assertRaises(NexusError):
            self.engine.accept(self.wf, 't1', old)

    def test_single_writer_and_unsafe_paths_are_blocked(self):
        self.approved()
        with self.engine.store.lock(self.wf):
            with self.assertRaisesRegex(NexusError, 'writer'):
                self.engine.run(self.wf)
        with self.assertRaises(NexusError):
            self.engine.init('Bad input', inputs=[self.root])

    def test_uncertain_persisted_operation_only_reconciles(self):
        self.wf = self.engine.init('Synthetic proposal', repo='example/project', execution_mode='restricted-native')['id']
        state = self.approved()
        op_id = self.wf + '-t1-create_issue'
        payload = {'title': state['tasks'][0]['title'], 'body': 'Goal: ' + state['goal'] + '\n\nAcceptance:\n- Explain the goal and pending decisions\n\nExecutor: agent'}
        self.engine.store.change(self.wf, 'simulate_lost_reply', lambda s: s['operations'].update({op_id: {'kind': 'create_issue', 'payload': payload, 'status': 'uncertain'}}))
        self.connector.reconcile = lambda *args: None
        state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'paused')
        self.assertEqual(self.connector.calls, [])
        self.connector.reconcile = lambda *args: {'number': 17, 'url': 'test-issue-17'}
        self.engine.resume(self.wf)
        self.engine.run(self.wf)
        self.assertFalse(any(kind == 'create_issue' for kind, _, _ in self.connector.calls))

    def test_lessons_can_be_revised_in_same_workflow(self):
        self.approved()
        state = self.engine.run(self.wf)
        self.engine.accept(self.wf, 't1', state['tasks'][0]['artifact']['sha256'])
        state = self.engine.run(self.wf)
        old_path = state['lessons']['artifact']['path']
        self.engine.revise(self.wf, 'lessons', 'Separate observed facts from proposed follow-up')
        state = self.engine.run(self.wf)
        self.assertNotEqual(state['lessons']['artifact']['path'], old_path)
        self.assertEqual(state['status'], 'awaiting_acceptance')

    def test_two_repairs_allow_initial_attempt_and_two_revisions(self):
        self.worker.review_passes = False
        self.approved()
        state = self.engine.run(self.wf)
        self.assertEqual(state['tasks'][0]['repairs'], 2)
        self.assertEqual(sum(kind == 'draft' for kind, _ in self.worker.calls), 3)

    def test_approval_cli_refuses_piped_model_decision(self):
        state = self.planned()
        command = [sys.executable, str(SCRIPT), '--workspace', str(self.root), 'approve', self.wf, '--version', str(state['plan_version']), '--hash', state['plan']['hash']]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 2)
        self.assertIn('interactive terminal', result.stderr)
        self.assertIsNone(self.engine.status(self.wf)['approval'])

    def test_concurrent_stop_cannot_be_overwritten_by_waiting_result(self):
        self.approved()
        original = self.engine._record
        def race(workflow_id, kind, mutate):
            if kind == 'waiting':
                self.engine.stop(workflow_id)
            return original(workflow_id, kind, mutate)
        self.engine._record = race
        self.assertEqual(self.engine.run(self.wf)['status'], 'stopped')

    def test_concurrent_stop_cannot_be_overwritten_by_approval(self):
        state = self.planned()
        original = self.engine._record
        def race(workflow_id, kind, mutate):
            if kind == 'plan_approved':
                self.engine.stop(workflow_id)
            return original(workflow_id, kind, mutate)
        self.engine._record = race
        with self.assertRaises(NexusError):
            self.engine.approve(self.wf, state['plan_version'], state['plan']['hash'])
        self.assertEqual(self.engine.status(self.wf)['status'], 'stopped')
        self.assertIsNone(self.engine.status(self.wf)['approval'])

    def test_connector_preflight_counts_toward_budget_before_any_write(self):
        self.wf = self.engine.init('Synthetic proposal', repo='example/project', execution_mode='restricted-native')['id']
        state = self.approved()
        clock = [100.0]
        self.connector.preflight = lambda: clock.__setitem__(0, clock[0] + 1.0)
        self.engine.store.change(self.wf, 'test_budget', lambda s: s.update(max_active_seconds=s['active_seconds'] + 0.5))
        with patch('nexus_runtime.engine.time.monotonic', side_effect=lambda: clock[0]):
            state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'paused')
        self.assertGreaterEqual(state['active_seconds'], 1.0)
        self.assertEqual(self.connector.calls, [])

    def test_stop_during_isolation_probe_prevents_plan(self):
        def stopped_probe(cancel=None, timeout=600):
            self.engine.stop(self.wf)
            self.assertTrue(cancel())
            return {'passed': True}
        self.worker.probe = stopped_probe
        with self.assertRaises(NexusError):
            self.engine.plan(self.wf)
        self.assertEqual(self.engine.status(self.wf)['status'], 'stopped')
        self.assertEqual(self.worker.calls, [])

    def test_review_and_lessons_receive_verified_actual_deliverables(self):
        original = self.worker.invoke
        def two_tasks(kind, payload, **kwargs):
            result = original(kind, payload, **kwargs)
            if kind == 'plan':
                result['tasks'].append(dict(result['tasks'][0], id='t2', dependencies=['t1']))
            return result
        self.worker.invoke = two_tasks
        self.approved()
        state = self.engine.run(self.wf)
        review_payload = next(payload for kind, payload in self.worker.calls if kind == 'review' and payload.get('task', {}).get('id') == 't2')
        self.assertTrue(any(d['task_id'] == 't1' and 'Goal and pending decisions' in d['content'] for d in review_payload['deliverables']))
        for task in state['tasks']:
            self.engine.accept(self.wf, task['id'], task['artifact']['sha256'])
        self.engine.run(self.wf)
        lessons_payload = next(payload for kind, payload in self.worker.calls if kind == 'lessons')
        self.assertEqual({d['task_id'] for d in lessons_payload['deliverables']}, {'t1', 't2'})
        self.assertTrue(all(d['accepted'] for d in lessons_payload['deliverables']))

    def test_live_orphan_worker_blocks_restart(self):
        import os
        self.approved()
        self.engine.store.change(self.wf, 'simulate_orphan', lambda s: s.update(worker_pid=os.getpid(), status='running'))
        with self.assertRaisesRegex(NexusError, 'orphan worker'):
            self.engine.resume(self.wf)

    def test_human_repairs_are_bounded(self):
        self.worker.human = True
        self.worker.review_passes = False
        self.approved()
        self.engine.run(self.wf)
        path = self.root / 'human.md'
        path.write_text('# Submission\n\nUnverified proposal.', encoding='utf-8')
        for _ in range(3):
            self.engine.submit(self.wf, 't1', path)
            state = self.engine.run(self.wf)
        self.assertEqual(state['status'], 'paused')
        self.assertEqual(state['tasks'][0]['repairs'], 2)

    def test_interrupted_window_is_charged_on_recovery(self):
        self.approved()
        before = self.engine.status(self.wf)['active_seconds']
        self.engine.store.change(self.wf, 'simulate_crash', lambda s: s.update(status='running', active_window={'started': time.time()-0.5, 'base': before, 'max_seconds': 10}))
        fresh = Engine(self.root, self.worker, self.connector)
        state = fresh.resume(self.wf)
        self.assertGreaterEqual(state['active_seconds'], before+0.5)
        self.assertIsNone(state['active_window'])

    def test_stop_terminates_identity_verified_orphan(self):
        import os
        from nexus_runtime.store import process_identity, process_alive
        self.approved()
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=os.name != 'nt')
        try:
            identity = process_identity(child.pid)
            self.assertIsNotNone(identity)
            self.engine.store.change(self.wf, 'simulate_orphan', lambda s: s.update(status='running', worker_pid=child.pid, worker_identity=identity))
            self.assertEqual(self.engine.stop(self.wf)['status'], 'stopped')
            self.assertFalse(process_alive(child.pid))
        finally:
            child.kill() if child.poll() is None else None
            child.wait(timeout=10)


if __name__ == '__main__':
    unittest.main()
