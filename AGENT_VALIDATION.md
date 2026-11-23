# Agent 0.5.0-alpha.1 validation

## Current readiness

**The optional local controller is implemented, but automatic mode is not admitted
on the currently tested Codex CLI.** Five actual isolation probes failed. Do not
interpret unit-test or package-check success as a usable end-to-end Agent result.
The stable v0.4.6 prompt-only release remains separately available.

The branch contains durable SQLite state, plan-scope approval, versioned Markdown
files, semantic-review handoff, explicit local acceptance, human submission,
bounded repair/run budgets, pause/stop/recovery and a GitHub Issues adapter.
Decisions are local-operator declarations with `identity_verified=false`; a TTY
check is not human identity authentication. The outer Codex must not execute the
operator's decision commands.

## Program and package verification

- The latest local source run passed **96 tests**: 28 controller tests, 38 mocked
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

## Actual restricted-worker evidence

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

Host environment filtering, temporary model metadata, read-only sandbox settings,
event/error rejection and process-tree cleanup remain in place. There is no
fallback to unrestricted execution or a switch to bypass the admission gate.
No global account configuration or authentication files were rewritten.

## Remaining acceptance work

- Resolve the execution approach with the Owner: retain the current strict gate,
  use the trusted current Codex to host the Loop with the local controller, or
  authorize a separate model API execution adapter. No alternative is enabled
  merely because this draft documents it.
- Use an Owner-designated synthetic test repository for real GitHub writes;
  only authentication/repository/assignee reads and mocked writes were checked.
- Complete real generated-document loops and two internal operator tasks before
  declaring the Agent ready for a pilot or a public v0.5 release.

Historical H/Q25 scores and the recorded Claude configuration failure are not
changed or reused as Agent acceptance. This work provides no team-adoption or
long-term productivity claim.
