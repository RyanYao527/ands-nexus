# Agent 0.5.0-alpha.2 validation

## Current readiness

**The Owner approved a trusted current-Codex hosted Loop for alpha.2.** The host
plans, drafts, uses a fresh independent reviewer, and writes Lessons responses;
the local controller manages requests, state, canonical files and scoped GitHub
actions. New workflows default to codex-hosted and use next/respond, without a
new model service or nested CLI probe prerequisite. This is a change of execution
route, not successful native tool isolation. The native route's five failed
probes remain failed and its strict gate remains intact.

The hosted handoff is implemented and the latest local suite passed 126 tests.
Independent targeted review and committed CI are tracked separately. Real
generated-document chains, fresh-reviewer evidence, operator decisions and
GitHub outcomes must be recorded before they can be counted as passed. No
live-chain pass, merge or release is asserted here. The stable v0.4.6 prompt-only
release remains separately available.

The branch contains durable SQLite state, plan-scope approval, versioned Markdown
files, semantic-review handoff, explicit local acceptance, human submission,
bounded repair/run budgets, pause/stop/recovery and a GitHub Issues adapter.
Decisions are local-operator declarations with `identity_verified=false`; a TTY
check is not human identity authentication. The outer Codex must not execute the
operator's decision commands. In hosted mode stop revokes pending requests and
blocks response import/controller actions; it cannot terminate the current
trusted Codex session. Default limits are twenty logical host requests, 600
seconds per request and 1800 cumulative seconds, including pending host-response
wait but excluding wait for a human decision/submission. Counts survive recovery.

Owner designated the private synthetic test repository
RyanYao527/ands-nexus-sandbox and assignee RyanYao527. The sandbox was created and
verified private; actual Issue writes still wait for the current plan/action preview
and the Owner's terminal approval. An unanswered approval remains pending.

## Hosted alpha.2 verification

Current source changes, program checks and actual hosted evidence are recorded
separately under the project evidence directory
05-Validation/agent-v0.5/2026-11-23-hosted-loop. The approved contract is
[the hosted Loop plan](docs/plans/2026-11-23-codex-hosted-loop.md). Request ID/hash,
snapshot/version binding, receipts, deadlines, stop, replay and budget recovery
require their own checks. Historical alpha.1 tests and native probes below do
not supply these results. This section will report only completed evidence.

- The latest local source passed **126 tests**: the original 96 regression
  cases and 30 hosted handoff cases. Earlier failures and fixes are retained.
- Both package scripts passed under Windows PowerShell 5.1 and PowerShell Core.
  The bundled skill quick validator also passed; no product dependency was added.
- An isolated alpha.2 source installation contained 49 matching skill files,
  no nested skill directory, and recovered initialized state in another process.
  This installation check did not call a model or GitHub.
- Live task plans and actual operator decisions remain separate acceptance work.

At the documentation checkpoint, the manifest groups and 28 skill reference
paths resolved, and both PowerShell engines passed the existing regression and
package scripts. The now-available external skill-creator quick_validate.py was
also run against this alpha.2 skill and returned "Skill is valid!" with exit 0;
no new Python dependency was added to the product. These checks are recorded in
the hosted-loop docs evidence and do not replace the later source-freeze checks,
new unit/CI results or actual hosted delivery.

## Historical alpha.1 program and package verification

- The frozen alpha.1 local source run passed **96 tests**: 28 controller tests, 38 mocked
  GitHub-boundary tests and 30 subprocess/worker tests. Its raw streams are
  retained with the project evidence; CI separately verifies the committed code.
- The first CI run passed Windows and package checks, but exposed a Linux
  timing dependency in a shared-deadline test: its child fixture emitted a
  forbidden tool event before the expected timeout. The replacement tests use
  a controlled clock, verify the second probe gets only the remaining budget,
  and fail if that budget is reset. Real subprocess timeout/cancellation tests
  remain, and the worker implementation and tool rejection policy are unchanged.
- Both Windows PowerShell 5.1 and PowerShell Core passed the existing release
  regression and package-validation scripts. External quick_validate was not
  supplied and remains explicitly skipped.
- An isolated source installation contained 48 skill files, with no nested
  skill directory. The installed CLI initialized a workflow and recovered it in
  another process. This check did not invoke a model or write to GitHub.
- A preserved two-task controller replay created actual Markdown files,
  checks and a Lessons candidate, then recovered completed state. Its model
  replies and operator decisions were scripted test doubles; it is not a live
  Agent pass or actual human acceptance.

Independent review reproduced and then verified fixes for cancellation between
GitHub lookup and mutation, orphan cleanup, interrupted-time accounting, human
repair limits and operation-wide deadlines. Windows job ownership precedes task
input; crash tests cover the assigned phase, not every possible startup instant.
Interrupted active windows are conservatively charged at recovery, bounded by
their original deadline; offline uncertainty can consume that allowance.

## Historical native restricted-worker evidence

1. Initial normal JSON generation succeeded, but an unexpected native resource
   query prevented strict tool-isolation admission.
2. Explicitly disabling that MCP server configuration did not remove native
   resource-query entries. The failed result remained failed.
3. A narrowly tested empty-metadata exception still did not satisfy the gate.
   Failed patch/image attempts also showed that JSON events alone did not
   describe every attempted tool operation.
4. A temporary copy of the CLI's bundled model catalog disabled its patch-tool
   metadata, and the image feature was explicitly disabled. Structured replies
   succeeded, but the inventory response still reported host tool names.
5. Child processes additionally removed inherited app-pipe, thread and
   permission environment variables while keeping the existing authentication
   location. The result still did not establish permission isolation.

All five top-level results remain **FAIL**. A successful schema-constrained
subprocess is not an admission pass. The final implementation restores strict
rejection of every tool event; the experimental metadata exemption is removed.
The failed fifth run is rejected by an offline replay without another model call.
The evidence establishes no successful canary read; where a failed run did not
archive a filesystem postcondition, that postcondition remains unknown rather
than being retrospectively counted as passed.

For the retained native route, host environment filtering, temporary model metadata, read-only sandbox settings,
event/error rejection and process-tree cleanup remain in place. There is no
fallback to unrestricted execution or a switch to bypass the admission gate.
No global account configuration or authentication files were rewritten.

## Remaining hosted acceptance work

- Complete the approved hosted implementation and verify its current source,
  with a fresh independent review and the new program/package/CI checks.
- Preview the actual sandbox plan and obtain the Owner's terminal approval
  before real Issue writes. Record normal and recovery outcomes separately;
  repository authorization does not substitute for scoped task approval.
- Complete real generated-document loops and two internal operator tasks before
  declaring the Agent ready for a pilot or a public v0.5 release.

Historical H/Q25 scores and the recorded Claude configuration failure are not
changed or reused as Agent acceptance. This work provides no team-adoption or
long-term productivity claim.
