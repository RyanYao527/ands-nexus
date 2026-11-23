"""Real subprocess tests for the restricted Codex boundary; no model calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


MODULE = Path(__file__).resolve().parents[1] / "ands-nexus/scripts/nexus_runtime/worker.py"


def load_worker():
    if not MODULE.is_file():
        raise AssertionError("Restricted worker implementation has not been created")
    spec = importlib.util.spec_from_file_location("nexus_worker_under_test", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STUB = r'''
import json, os, pathlib, re, subprocess, sys, time
if "debug" in sys.argv and "models" in sys.argv:
    selected={"slug":"gpt-6.1-sol","apply_patch_tool_type":"freeform","priority":0,"vendor_field":"preserve-this","host_bridge_names":[k for k in os.environ if k.startswith("CODEX_") and k!="CODEX_HOME"]}
    if "--missingcap" in sys.argv: selected.pop("apply_patch_tool_type")
    print(json.dumps({"models":[selected,{"slug":"another-model","apply_patch_tool_type":"freeform","priority":1}]}),flush=True)
    sys.exit(0)
prompt = sys.stdin.read()
request = json.loads(prompt.split("PAYLOAD_JSON:\n", 1)[1]) if "PAYLOAD_JSON:\n" in prompt else {}
mode = request.get("stub", "draft")
if mode == "replay":
    sys.stdout.buffer.write(pathlib.Path(request["events"]).read_bytes())
    sys.stdout.buffer.flush()
    sys.exit(0)
if "--probe-hang" in sys.argv:
    mode = "hang"
print(json.dumps({"type":"thread.started","thread_id":"synthetic-session"}), flush=True)
print(json.dumps({"type":"turn.started"}), flush=True)
if mode == "hang":
    print(json.dumps({"type":"item.started","item":{"id":"r","type":"reasoning","text":"waiting"}}), flush=True)
    time.sleep(30)
if mode == "tree":
    heartbeat = request["heartbeat"]
    child = "import pathlib,time; p=pathlib.Path(" + repr(heartbeat) + "); " + "exec('while True:\\n p.write_text(str(time.time()))\\n time.sleep(.03)')"
    subprocess.Popen([sys.executable,"-c",child])
    time.sleep(30)
if mode == "tool":
    print(json.dumps({"type":"item.started","item":{"id":"bad","type":"command_execution","command":"forbidden"}}), flush=True)
    time.sleep(30)
if mode == "malformed_event":
    print("not-json", flush=True)
    time.sleep(30)
if mode == "hidden_tool":
    print("ERROR codex_core::tools::router: error=patch rejected: read-only sandbox",file=sys.stderr,flush=True)
if (mode.startswith("templates") or "PROBE_INVENTORY" in prompt) and "--no-metadata" not in sys.argv:
    identifier="meta-1"
    args={"server":"other"} if mode=="templates_args" else {}
    tool="list_mcp_resources" if mode=="templates_other_tool" else "list_mcp_resource_templates"
    item={"id":identifier,"type":"mcp_tool_call","server":"codex","tool":tool,"arguments":args,"result":None,"error":None,"status":"in_progress"}
    print(json.dumps({"type":"item.started","item":item}),flush=True)
    if mode!="templates_unfinished":
        item=dict(item)
        item["status"]="completed"
        item["id"]="other-id" if mode=="templates_wrong_id" else identifier
        text='{"resourceTemplates":[]}'
        if mode=="templates_nonempty": text='{"resourceTemplates":[{"uri":"secret-template"}]}'
        if mode=="templates_extra_key": text='{"resourceTemplates":[],"extra":"not allowed"}'
        if mode=="templates_duplicate_key": text='{"resourceTemplates":["hidden"],"resourceTemplates":[]}'
        content=[{"type":"text","text":text}]
        if mode=="templates_extra_block": content.append({"type":"resource_link","uri":"unexpected"})
        item["result"]={"content":content,"structured_content":None}
        if mode=="templates_error": item["error"]="failed"
        print(json.dumps({"type":"item.completed","item":item}),flush=True)
if mode == "bad_review":
    response = {"passed":"yes", "findings":[]}
elif mode == "environment":
    observed={"codex_names":[k for k in os.environ if k.startswith("CODEX_")],"auth_home_matches":os.environ.get("CODEX_HOME")==request["expected_auth_home"],"github_token_present":"GITHUB_TOKEN" in os.environ}
    response = {"content":json.dumps(observed),"sources":[]}
elif mode == "review":
    response = {"passed":False,"findings":["Missing evidence"]}
elif "PROBE_NORMAL" in prompt:
    if "--probe-delay" in sys.argv: time.sleep(.2)
    response = {"ok":True}
elif "PROBE_INVENTORY" in prompt:
    if "--probe-delay" in sys.argv: time.sleep(.2)
    nonce = pathlib.Path(re.search(r"canary file: (.*?)\. Report",prompt).group(1)).read_text() if "--leak" in sys.argv else None
    reported=[] if "--no-metadata" in sys.argv else ["list_mcp_resource_templates"]
    if "--write-only" in sys.argv:
        pathlib.Path(re.search(r"containing 'isolation-write-attempt' at (.*?) if a shell/file write tool",prompt).group(1)).write_text("isolation-write-attempt")
        reported=["functions.exec"]
    response = {"available_tools":reported,"observed_nonce":nonce,"attempted_tools":reported}
else:
    response = {"content":"# Deliverable\n\nRecorded facts only.","sources":["provided-brief"]}
print(json.dumps({"type":"item.completed","item":{"id":"answer","type":"agent_message","text":json.dumps(response)}}), flush=True)
print(json.dumps({"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":20}}), flush=True)
'''


class RestrictedWorkerTests(unittest.TestCase):
    def setUp(self):
        self.worker_module = load_worker()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.stub = self.root / "fake_codex.py"
        self.stub.write_text(STUB, encoding="utf-8")
        self.worker = self.worker_module.CodexWorker(
            evidence_dir=self.root / "evidence", command=[sys.executable, str(self.stub)]
        )

    def test_actual_subprocess_content_and_usage_are_retained(self):
        result = self.worker.invoke("draft", {"stub":"draft"})
        self.assertIn("Recorded facts", result["content"])
        records = list((self.root/"evidence").glob("*/result.json"))
        self.assertEqual(1, len(records))
        record = json.loads(records[0].read_text(encoding="utf-8"))
        self.assertEqual(20, record["usage"]["output_tokens"])
        self.assertEqual("success", record["status"])
        command = json.loads((records[0].parent/"command.json").read_text(encoding="utf-8"))["argv"]
        self.assertIn("--ignore-user-config", command)
        self.assertIn("read-only", command)
        self.assertIn("shell_tool", command)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)

    def test_tool_attempt_is_rejected_and_process_stopped_immediately(self):
        started = time.monotonic()
        with self.assertRaisesRegex(self.worker_module.WorkerError, "tool|Tool"):
            self.worker.invoke("draft", {"stub":"tool"})
        self.assertLess(time.monotonic()-started, 6)
        record = json.loads(next((self.root/"evidence").glob("*/result.json")).read_text(encoding="utf-8"))
        self.assertEqual("failed", record["status"])
        self.assertIn("command_execution", record["error"])

    def test_malformed_stdout_is_not_treated_as_a_document(self):
        with self.assertRaisesRegex(self.worker_module.WorkerError, "JSON|event"):
            self.worker.invoke("draft", {"stub":"malformed_event"})

    def test_failed_tool_router_action_without_jsonl_event_is_rejected(self):
        with self.assertRaisesRegex(self.worker_module.WorkerError,"tool|router"):
            self.worker.invoke("draft",{"stub":"hidden_tool"})

    def test_invalid_review_types_fail_instead_of_becoming_truthy(self):
        with self.assertRaisesRegex(self.worker_module.WorkerError, "schema|passed|boolean"):
            self.worker.invoke("review", {"stub":"bad_review"})

    def test_failed_review_preserves_specific_findings(self):
        result = self.worker.invoke("review", {"stub":"review"})
        self.assertIs(False, result["passed"])
        self.assertEqual(["Missing evidence"], result["findings"])

    def test_cancellation_is_checked_while_child_is_running(self):
        started = time.monotonic()
        with self.assertRaisesRegex(self.worker_module.WorkerError, "cancel|stop"):
            self.worker.invoke("draft", {"stub":"hang"}, cancel=lambda: time.monotonic()-started > .3)
        self.assertLess(time.monotonic()-started, 6)

    def test_timeout_preserves_failure_evidence(self):
        with self.assertRaisesRegex(self.worker_module.WorkerError, "time|deadline"):
            self.worker.invoke("draft", {"stub":"hang"}, timeout=.3)
        self.assertTrue(list((self.root/"evidence").glob("*/stdout.jsonl")))
        self.assertTrue(list((self.root/"evidence").glob("*/stderr.txt")))

    def test_raw_events_exist_before_a_running_worker_finishes(self):
        def recorded():
            return any(path.stat().st_size for path in (self.root/"evidence").glob("*/stdout.jsonl"))
        with self.assertRaisesRegex(self.worker_module.WorkerError,"cancel|stop"):
            # Cancellation is triggered by an observed raw event, not wall time.
            # Allow Windows startup under a concurrently running full suite.
            self.worker.invoke("draft",{"stub":"hang"},cancel=recorded,timeout=10)

    def test_named_codex_mcp_server_is_explicitly_disabled(self):
        command=self.worker._argv(self.root,self.root/"schema.json")
        self.assertIn("mcp_servers.codex.enabled=false",command)

    def test_local_image_tool_is_explicitly_disabled(self):
        command=self.worker._argv(self.root,self.root/"schema.json")
        self.assertIn("view_image",command)

    def test_catalog_comes_from_cli_and_only_patch_capability_changes(self):
        self.worker.invoke("draft",{})
        record=next((self.root/"evidence").glob("*/result.json")).parent
        original=json.loads((record/"model-catalog-original.json").read_text())
        modified=json.loads((record/"model-catalog-worker.json").read_text())
        self.assertEqual("preserve-this",modified["models"][0]["vendor_field"])
        self.assertIsNone(modified["models"][0]["apply_patch_tool_type"])
        for before,after in zip(original["models"],modified["models"]):
            expected=dict(before)
            if after["apply_patch_tool_type"] is None:
                expected["apply_patch_tool_type"]=None
            self.assertEqual(expected,after)
        command=json.loads((record/"command.json").read_text())["argv"]
        self.assertTrue(any(x.startswith("model_catalog_json=") for x in command))

    def test_missing_catalog_capability_fails_before_a_delegated_task(self):
        legacy=self.worker_module.CodexWorker(evidence_dir=self.root/"legacy",command=[sys.executable,str(self.stub),"--missingcap"])
        with self.assertRaisesRegex(self.worker_module.WorkerError,"catalog|capability"):
            legacy.invoke("draft",{})
        self.assertEqual(0,legacy.invocation_count)

    def test_cancelled_catalog_drains_reader_threads_before_closing_pipes(self):
        class Pipe:
            def __init__(self,process):
                self.process=process
                self.closed_before_drain=False
            def close(self):
                self.closed_before_drain=not self.process.drained
        class Process:
            stopped=False
            drained=False
            def __init__(self):
                self.stdout=Pipe(self)
                self.stderr=Pipe(self)
            def poll(self): return -9 if self.stopped else None
            def communicate(self,timeout=None):
                if not self.stopped:
                    raise subprocess.TimeoutExpired("fixture-catalog",timeout)
                self.drained=True
                return b"",b""
        process=Process()
        checks=iter((False,True))
        with mock.patch.object(self.worker_module.subprocess,"Popen",return_value=process):
            with mock.patch.object(self.worker_module,"_terminate_tree",side_effect=lambda child:setattr(child,"stopped",True)):
                with self.assertRaisesRegex(self.worker_module.WorkerError,"cancel"):
                    self.worker._catalog(self.root,self.root,{},None,lambda:next(checks),time.monotonic()+10,{})
        self.assertFalse(process.stdout.closed_before_drain,"Cancelled catalog stdout reader was not joined")
        self.assertFalse(process.stderr.closed_before_drain,"Cancelled catalog stderr reader was not joined")

    def test_both_children_drop_host_bridge_but_preserve_auth_home(self):
        auth_home=str(self.root/"existing-auth-location")
        bridge={"CODEX_HOME":auth_home,"CODEX_APP_TOOLS_PIPE_PATH":"synthetic-pipe","CODEX_APP_RUNTIME_CLI_PATH":"synthetic-host-cli","CODEX_THREAD_ID":"host-thread","CODEX_TOOL_CALL_ID":"host-call","CODEX_SESSION_ID":"host-session","CODEX_PERMISSION_PROFILE":"host-permissions","CODEX_INTERNAL_ORIGINATOR_OVERRIDE":"host-origin","CODEX_MCP_NODE_PATH":"host-node","CODEX_UNKNOWN_FUTURE_HOST_FLAG":"host-flag","GITHUB_TOKEN":"synthetic-token"}
        with mock.patch.dict(self.worker_module.os.environ,bridge):
            result=self.worker.invoke("draft",{"stub":"environment","expected_auth_home":auth_home})
        observed=json.loads(result["content"])
        self.assertEqual(["CODEX_HOME"],observed["codex_names"])
        self.assertIs(True,observed["auth_home_matches"])
        self.assertIs(False,observed["github_token_present"])
        evidence=next((self.root/"evidence").glob("*/result.json")).parent
        original=json.loads((evidence/"model-catalog-original.json").read_text())
        self.assertEqual([],original["models"][0]["host_bridge_names"])
        policy=json.loads((evidence/"child-environment.json").read_text())
        self.assertIn("CODEX_APP_TOOLS_PIPE_PATH",policy["removed_names"])
        self.assertNotIn("synthetic-pipe",json.dumps(policy))

    def test_cancel_terminates_a_real_descendant_not_just_the_parent(self):
        heartbeat=self.root/"heartbeat.txt"
        with self.assertRaisesRegex(self.worker_module.WorkerError,"cancel|stop"):
            self.worker.invoke("draft",{"stub":"tree","heartbeat":str(heartbeat)},cancel=heartbeat.exists,timeout=15)
        self.assertTrue(heartbeat.exists(),"The controlled descendant actually started")
        value=heartbeat.read_bytes()
        time.sleep(.2)
        self.assertEqual(value,heartbeat.read_bytes(),"Descendant kept writing after cancellation")

    @unittest.skipUnless(sys.platform=="win32","Windows process-tree failure branch")
    def test_tree_kill_failure_is_not_reported_as_successful_cleanup(self):
        class Process:
            pid=12345
            alive=True
            def poll(self): return None if self.alive else -9
            def kill(self): self.alive=False
            def wait(self,timeout=None): return -9
        with mock.patch.object(self.worker_module.subprocess,"run",return_value=subprocess.CompletedProcess([],1,b"",b"Denied")):
            with self.assertRaisesRegex(self.worker_module.WorkerError,"tree|descendant"):
                self.worker_module._terminate_tree(Process())

    @unittest.skipUnless(sys.platform=="win32","Windows JobObject ownership")
    def test_controller_death_kills_worker_and_its_descendant(self):
        heartbeat=self.root/"orphan-heartbeat.txt"
        controller=self.root/"controller.py"
        controller.write_text(
            "import sys\nfrom pathlib import Path\nsys.path.insert(0,"+repr(str(MODULE.parent.parent))+ ")\n"
            "from nexus_runtime.worker import CodexWorker\n"
            "worker=CodexWorker(evidence_dir="+repr(str(self.root/"controller-evidence"))+", command="+repr([sys.executable,str(self.stub)])+")\n"
            "worker.invoke('draft',"+repr({"stub":"tree","heartbeat":str(heartbeat)})+",timeout=60)\n",encoding="utf-8")
        diagnostic_path=self.root/"controller-stderr.txt"
        diagnostic=diagnostic_path.open("wb")
        process=subprocess.Popen([sys.executable,str(controller)],stdout=subprocess.DEVNULL,stderr=diagnostic)
        try:
            deadline=time.monotonic()+30
            while not heartbeat.exists() and process.poll() is None and time.monotonic()<deadline:
                time.sleep(.03)
            self.assertTrue(heartbeat.exists(),"The controlled worker descendant started; exit="+str(process.poll())+" stderr="+diagnostic_path.read_text(encoding="utf-8",errors="replace"))
            process.kill()
            process.wait(timeout=5)
            time.sleep(.3)
            value=heartbeat.read_bytes()
            time.sleep(.3)
            self.assertEqual(value,heartbeat.read_bytes(),"Orphan descendant survived controller death")
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            diagnostic.close()
            # Defensive fixture cleanup if the implementation is still RED.
            for record in (self.root/"controller-evidence").glob("*/process.json"):
                pid=json.loads(record.read_text())["pid"]
                subprocess.run(["taskkill.exe","/PID",str(pid),"/T","/F"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

    @unittest.skipUnless(sys.platform=="win32","Windows JobObject creation")
    def test_job_creation_failure_does_not_start_an_unprotected_worker(self):
        with mock.patch.object(self.worker_module,"_WindowsJob",side_effect=self.worker_module.WorkerError("Job protection unavailable"),create=True):
            with mock.patch.object(self.worker_module.subprocess,"Popen",side_effect=AssertionError("Unprotected process started")):
                with self.assertRaisesRegex(self.worker_module.WorkerError,"Job protection unavailable"):
                    self.worker.invoke("draft",{})

    def test_probe_runs_both_normal_and_inventory_challenges(self):
        self.worker.command.append("--no-metadata")
        result = self.worker.probe()
        self.assertIs(True, result["passed"])
        self.assertIs(True,result["tool_inventory_empty"])
        self.assertEqual([], result["available_tools"])
        self.assertEqual(2, len(list((self.root/"evidence").glob("*/result.json"))))

    def test_genuinely_empty_inventory_does_not_require_an_invented_tool_call(self):
        empty=self.worker_module.CodexWorker(evidence_dir=self.root/"empty-inventory",command=[sys.executable,str(self.stub),"--no-metadata"])
        result=empty.probe()
        self.assertIs(True,result["passed"])
        self.assertIs(True,result["tool_inventory_empty"])

    def test_even_exact_empty_metadata_tool_event_is_rejected(self):
        with self.assertRaisesRegex(self.worker_module.WorkerError,"Forbidden worker tool"):
            self.worker.invoke("draft",{"stub":"templates"})

    def test_all_metadata_variants_and_tools_are_rejected(self):
        for mode in ("templates_args","templates_other_tool","templates_wrong_id","templates_nonempty","templates_extra_key","templates_duplicate_key","templates_extra_block","templates_error","templates_unfinished"):
            with self.subTest(mode=mode):
                with self.assertRaises(self.worker_module.WorkerError):
                    self.worker.invoke("draft",{"stub":mode})

    def test_probe_rejects_a_read_canary_even_without_a_tool_event(self):
        leaking=self.worker_module.CodexWorker(evidence_dir=self.root/"leak-evidence",command=[sys.executable,str(self.stub),"--leak","--no-metadata"])
        with self.assertRaisesRegex(self.worker_module.WorkerError,"isolation|canary"):
            leaking.probe()
        summary=json.loads(next((self.root/"leak-evidence").glob("probe-*.json")).read_text())
        self.assertIs(False,summary["passed"])
        self.assertEqual(2,summary["invocation_count"])

    def test_failed_inventory_retains_canary_postconditions_before_rejection(self):
        writing=self.worker_module.CodexWorker(evidence_dir=self.root/"write-evidence",command=[sys.executable,str(self.stub),"--write-only","--no-metadata"])
        with self.assertRaisesRegex(self.worker_module.WorkerError,"isolation|canary|tool"):
            writing.probe()
        records=list((self.root/"write-evidence").glob("canary-*.json"))
        self.assertEqual(1,len(records),"A failed inventory must retain its canary postconditions")
        observation=json.loads(records[0].read_text())
        self.assertIs(True,observation["write_path_exists"])
        self.assertIs(True,observation["original_canary_unchanged"])
        self.assertIs(False,observation["reported_nonce_present"])

    def test_probe_honors_stop_while_its_first_child_is_running(self):
        blocked=self.worker_module.CodexWorker(evidence_dir=self.root/"probe-stop",command=[sys.executable,str(self.stub),"--probe-hang"])
        started=time.monotonic()
        with self.assertRaisesRegex(self.worker_module.WorkerError,"cancel|stop"):
            blocked.probe(cancel=lambda:time.monotonic()-started>.3,timeout=3)
        self.assertLess(time.monotonic()-started,6)

    def test_both_probe_invocations_share_one_deadline(self):
        delayed=self.worker_module.CodexWorker(evidence_dir=self.root/"probe-timeout",command=[sys.executable,str(self.stub),"--probe-delay"])
        with self.assertRaisesRegex(self.worker_module.WorkerError,"time|deadline"):
            delayed.probe(timeout=.35)

    def test_plan_rejects_more_than_five_tasks_before_execution(self):
        with self.assertRaisesRegex(self.worker_module.WorkerError, "five|5|schema|tasks"):
            self.worker_module.validate_response("plan", {"tasks":[{"id":f"t{i}","title":"Task","assignee":None,"executor":"agent","acceptance":["File exists"],"dependencies":[]} for i in range(6)]})

    def test_plan_uses_engine_task_ids_and_previous_dependencies_only(self):
        task={"id":"task1","title":"Task","assignee":None,"executor":"agent","acceptance":["Check"],"dependencies":[]}
        with self.assertRaises(self.worker_module.WorkerError):
            self.worker_module.validate_response("plan",{"tasks":[task]})
        task["id"]="t1"
        other=dict(task,id="t2",dependencies=["t1"])
        with self.assertRaises(self.worker_module.WorkerError):
            self.worker_module.validate_response("plan",{"tasks":[other,task]})


if __name__ == "__main__":
    unittest.main()
