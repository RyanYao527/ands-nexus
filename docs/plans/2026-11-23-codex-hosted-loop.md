# Approved Codex-hosted Loop contract

Owner approved the hosted route in the project chat on 2026-11-23, following the
five failed native isolation probes. This contract adds 0.5.0-alpha.2 on the
existing feature branch from 0bc81d8; it does not amend those failed results or
authorize a new model service, merge or release.

## Execution and interface

- The current trusted Codex hosts planning, drafting and Lessons. Each review
  request goes to a new independent reviewer with the actual sources, current
  artifact and acceptance. A fabricated self-review is not an independent check.
- The local Python/SQLite controller owns checkpoints, canonical Markdown,
  request/response receipts, approvals, budgets and scoped GitHub actions.
- `init --execution-mode codex-hosted` is the new default. `next WORKFLOW`
  returns state and, when needed, status awaiting_host with pending_request.
- A pending request carries id, request_hash, kind, stage, target, version, role,
  schema, payload, snapshot, snapshot_hashes, approved_scope, route, issued_at,
  deadline, allowance_seconds and time_base. The retained native selector is
  `restricted-native`; old workflows do not silently switch routes.
- The host saves raw response-schema JSON under the explicit workspace and
  calls `respond WORKFLOW --request ID --request-hash HASH --path RESPONSE`.
  There is no outer request envelope. The controller returns an applied receipt
  with request_id and response_sha256 plus current state; the host calls next.
- No response or receipt is plan approval or business acceptance. The human
  enters approve/accept/revise and budget extensions in an independent terminal.
  Decisions remain local_operator_cli with identity_verified=false; TTY/PTY does
  not authenticate a person and the host must not operate that decision entry.

## Bounds and recovery

- Five tasks, twenty logical host requests, 600 seconds per pending request,
  1800 seconds cumulative active budget, two task repair rounds. Pending host
  response time counts, waiting for a human decision/submission does not.
- Counters and request versions survive processes; stale, expired, stopped or
  mismatched-snapshot responses must not create accepted artifacts or actions.
- Only a valid accepted response binds its unique result bytes. Invalid attempts
  are archived and may be corrected under the same request before its original
  deadline. Identical valid/invalid replay returns the saved receipt/error with
  no new audit files, budget or deadline extension; a rejected receipt is
  structured stderr with exit 2.
- A valid revise transaction revokes and settles pending host work; an invalid
  revise leaves it unchanged. Accept/submit during awaiting_host reject without
  changing business state or the request. Finish host work, or pause and inspect
  the current state before intervening; neither path manufactures acceptance.
- Hosted stop revokes requests and blocks imports/controller actions; it cannot
  kill the trusted Codex session. Native stop retains child-process termination.
- Native mode keeps strict tool rejection and failed admission on the tested
  CLI. Hosted mode neither runs its probes nor claims native tool isolation.

## GitHub and acceptance

Owner designated the private synthetic repository
RyanYao527/ands-nexus-sandbox, assignee RyanYao527. Root may create that test
repository; real task writes wait for the actual plan/action preview and Owner
approval. The existing stable-operation and reconciliation rules continue.

Validation must separately record program tests, actual hosted generation,
independent review, operator decisions, remote GitHub outcomes and recovery.
Historical alpha.1 96-test evidence and five failed probes stay historical.
Unanswered human decisions and unrun integration paths are not passes. Do not
merge or publish this alpha as part of implementing the hosted contract.

Evidence belongs to the separate project directory
05-Validation/agent-v0.5/2026-11-23-hosted-loop. AGENT_VALIDATION.md records the
current actual result, while the earlier native implementation contract remains
unchanged as history.
