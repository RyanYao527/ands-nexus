# Guided Workflow First Run v0.4

> Goal: run one four-step guided ANDS workflow with synthetic material only. This example is included in the public v0.4.0 guided workflow MVP.

## Scenario

Use this synthetic task:

`Add a weekly export button to an internal reporting tool so an operations lead can download the previous week's summary as a CSV.`

Expected output sections are self-check examples. Do not paste the Expected output back to the agent.

Replace `owner_response` with the human owner's actual reply before sending each Step Prompt. Values shown in Expected output are format demonstrations only.

The Task Context blocks carry this synthetic example's definition into a fresh conversation. For your own workflow, replace them with your current task and artifact contents, retaining unresolved facts as unresolved. They do not count as Owner approval or implementation evidence.

## Step 1 Prompt: Intake Snapshot

```text
$ands-nexus

Run guided ANDS workflow for this synthetic task:
"Add a weekly export button to an internal reporting tool so an operations lead can download the previous week's summary as a CSV."

Return the first step only. Include Current Artifact, State Packet, Gate / Evidence Check, Owner Decision, Next Prompt, and Boundary Reminder.
```

Expected output:

## Current Artifact

Intake Snapshot:

| Field | Draft |
|---|---|
| Goal | Add a weekly CSV export button for an internal reporting page |
| Audience | PM and engineer |
| Data class | Synthetic |
| Track candidate | Standard |
| Main uncertainty | Export fields, file naming, owner acceptance, and failure behavior |

## State Packet

| Field | Value |
|---|---|
| `workflow_id` | `GW-SYN-001` |
| `current_step` | `Intake` |
| `user_goal` | Add a weekly CSV export button to an internal reporting page |
| `audience` | PM and engineer |
| `data_class` | synthetic |
| `track` | Standard |
| `active_role` | AI PM |
| `artifacts_created` | Intake Snapshot |
| `missing_evidence` | export fields, filename convention, acceptance owner |
| `owner_decision` | Confirm Standard Track and provide missing evidence |
| `owner_response` | unfilled - owner should reply with `confirm: ...`, `revise: ...`, `escalate: ...`, or `stop: ...` before Step 2 |
| `next_prompt` | Continue this guided workflow from Intake to ANDS-T using workflow_id GW-SYN-001. Preserve synthetic-only context and include the missing evidence list. |
| `boundary_flags` | Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking |

## Gate / Evidence Check

Gate 1 is incomplete until the owner confirms fields, naming, and acceptance owner. No implementation should start yet.

## Owner Decision

Continue as Standard Track, revise scope, or escalate if real data or tenant systems enter the task.

## Next Prompt

```text
$ands-nexus

Continue this guided workflow from Intake to ANDS-T.

State:
- workflow_id: GW-SYN-001
- current_step: Intake
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: AI PM
- artifacts_created: Intake Snapshot
- missing_evidence: export fields, filename convention, acceptance owner
- owner_decision: Confirm Standard Track and provide missing evidence
- owner_response: [confirm/revise/escalate/stop before continuing]
- next_prompt: Continue this guided workflow from Intake to ANDS-T using workflow_id GW-SYN-001.
- boundary_flags: Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (received synthetic task; unresolved details remain unresolved):
- Goal: Let an operations lead download the previous week's summary as a CSV from an internal reporting page.
- Still needed: export fields, filename convention, acceptance owner, and failure behavior. Do not invent these values.
- Evidence: no implementation, machine checks, or human acceptance yet.

Return the ANDS-T step only with Current Artifact, State Packet, Gate / Evidence Check, Owner Decision, Next Prompt, and Boundary Reminder.
```

## Boundary Reminder

Use synthetic or desensitized context only. Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.

## Step 2 Prompt: ANDS-T Task Card

Before sending this Step Prompt, replace `owner_response` with the human owner's actual reply.

```text
$ands-nexus

Continue this guided workflow from Intake to ANDS-T.

State:
- workflow_id: GW-SYN-001
- current_step: Intake
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: AI PM
- artifacts_created: Intake Snapshot
- missing_evidence: export fields, filename convention, acceptance owner unless owner_response supplies them
- owner_decision: Confirm Standard Track and provide missing evidence
- owner_response: <owner reply: confirm/revise/escalate/stop: ...>
- next_prompt: Continue this guided workflow from Intake to ANDS-T using workflow_id GW-SYN-001.
- boundary_flags: Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (received synthetic task; unresolved details remain unresolved):
- Goal: Let an operations lead download the previous week's summary as a CSV from an internal reporting page.
- Still needed: export fields, filename convention, acceptance owner, and failure behavior unless the actual Owner reply supplies them.
- Evidence: no implementation, machine checks, or human acceptance yet.

Return the ANDS-T step only with Current Artifact, State Packet, Gate / Evidence Check, Owner Decision, Next Prompt, and Boundary Reminder.
```

Expected output:

## Current Artifact

ANDS-T Task Card:

| Section | Draft |
|---|---|
| Goal | Add a weekly CSV export button for a synthetic internal reporting page |
| Inputs | Existing report table, approved synthetic fields date/region/revenue, target filename weekly-summary-YYYY-WW.csv |
| Non-goals | No provider trials, no tenant connectors, no persistence automation |
| Acceptance | Downloaded CSV contains approved fields, covers previous week, opens in a spreadsheet, and shows a clear empty-state message when no rows exist |
| Owner | Product or operations owner confirms fields and acceptance |
| Track | Standard because it changes an internal workflow and needs human acceptance |

## State Packet

| Field | Value |
|---|---|
| `workflow_id` | `GW-SYN-001` |
| `current_step` | `ANDS-T` |
| `user_goal` | Add a weekly CSV export button to an internal reporting page |
| `audience` | PM and engineer |
| `data_class` | synthetic |
| `track` | Standard |
| `active_role` | AI PM |
| `artifacts_created` | Intake Snapshot; ANDS-T Task Card |
| `missing_evidence` | Gate 2 test evidence; Gate 3 owner acceptance after implementation |
| `owner_decision` | Approve or revise the ANDS-T as the task definition before any execution begins |
| `owner_response` | confirm: Standard Track; export fields date/region/revenue; filename weekly-summary-YYYY-WW.csv; acceptance owner operations lead |
| `next_prompt` | Continue this guided workflow from ANDS-T to Track + Gate Checklist for workflow_id GW-SYN-001. |
| `boundary_flags` | Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking |

## Gate / Evidence Check

Gate 1 can pass for this synthetic exercise because the owner_response confirmed fields, filename, and acceptance owner. Gate 2 and Gate 3 evidence are not yet available.

## Owner Decision

Approve the ANDS-T as the task definition before any execution begins, request edits, or stop.

## Next Prompt

```text
$ands-nexus

Continue this guided workflow from ANDS-T to Track + Gate Checklist.

State:
- workflow_id: GW-SYN-001
- current_step: ANDS-T
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: Validation + Governance
- artifacts_created: Intake Snapshot; ANDS-T Task Card
- missing_evidence: Gate 2 test evidence; Gate 3 owner acceptance after implementation
- owner_decision: Approve or revise the ANDS-T as the task definition before any execution begins
- owner_response: <owner reply: confirm/revise/escalate/stop: ...>
- next_prompt: Continue this guided workflow from ANDS-T to Track + Gate Checklist for workflow_id GW-SYN-001.
- boundary_flags: Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (synthetic task definition; approval remains in owner_response):
- Goal: Add a weekly CSV export button to an internal reporting page.
- Inputs: existing report table; fields date/region/revenue; filename weekly-summary-YYYY-WW.csv.
- Acceptance: downloaded CSV contains those fields, covers the previous week, opens in a spreadsheet, and shows a clear empty-state message when no rows exist.
- Acceptance owner: operations lead for this synthetic definition; the actual Owner reply is still required.
- Non-goals: no provider trials, no tenant connectors, no persistence automation.
- Evidence: task definition only; Gate 2 test evidence and Gate 3 owner acceptance after implementation remain missing.

Return the Gate step only with Current Artifact, State Packet, Gate / Evidence Check, Owner Decision, Next Prompt, and Boundary Reminder.
```

## Boundary Reminder

Do not treat the ANDS-T as implementation or approval. Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.

## Step 3 Prompt: Track + Gate Checklist

Before sending this Step Prompt, replace `owner_response` with the human owner's actual reply.

```text
$ands-nexus

Continue this guided workflow from ANDS-T to Track + Gate Checklist.

State:
- workflow_id: GW-SYN-001
- current_step: ANDS-T
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: Validation + Governance
- artifacts_created: Intake Snapshot; ANDS-T Task Card
- missing_evidence: Gate 2 test evidence; Gate 3 owner acceptance after implementation
- owner_decision: Approve or revise the ANDS-T as the task definition before any execution begins
- owner_response: <owner reply: confirm/revise/escalate/stop: ...>
- next_prompt: Continue this guided workflow from ANDS-T to Track + Gate Checklist for workflow_id GW-SYN-001.
- boundary_flags: Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (synthetic task definition; approval remains in owner_response):
- Goal: Add a weekly CSV export button to an internal reporting page.
- Inputs: existing report table; fields date/region/revenue; filename weekly-summary-YYYY-WW.csv.
- Acceptance: downloaded CSV contains those fields, covers the previous week, opens in a spreadsheet, and shows a clear empty-state message when no rows exist.
- Acceptance owner: operations lead for this synthetic definition; the actual Owner reply is still required.
- Non-goals: no provider trials, no tenant connectors, no persistence automation.
- Evidence: task definition only; Gate 2 test evidence and Gate 3 owner acceptance after implementation remain missing.

Return the Gate step only with Current Artifact, State Packet, Gate / Evidence Check, Owner Decision, Next Prompt, and Boundary Reminder.
```

Expected output:

## Current Artifact

Track + Gate Checklist:

Status legend: `Passed` means evidence is sufficient for this synthetic example; `Conditional` means the artifact exists but needs owner/evidence confirmation; `Missing` means required evidence does not exist yet; `Not ready` means the workflow has not reached that Gate.

| Gate | Status | Evidence | Missing Evidence | Owner Action |
|---|---|---|---|---|
| Gate 1 Intake | Passed | Synthetic task, ANDS-T, and owner_response confirm field list, filename convention, and acceptance owner | None for Gate 1 in this synthetic example | Review again if owner revises |
| Gate 2 Machine Quality | Missing | None yet | Tests or equivalent checks for export behavior | Execution produces evidence |
| Gate 3 Human Acceptance | Missing | None yet | Owner confirms CSV fields and usability | Owner reviews after Gate 2 |
| Gate 4 Release Approval | Not ready | Scope is internal and Standard Track | Release note or rollout note if needed | Decide whether release approval is needed |
| Gate 5 Lessons | Not ready | Candidate prompt exists | Final outcome | Draft after review |

## State Packet

| Field | Value |
|---|---|
| `workflow_id` | `GW-SYN-001` |
| `current_step` | `Gate` |
| `user_goal` | Add a weekly CSV export button to an internal reporting page |
| `audience` | PM and engineer |
| `data_class` | synthetic |
| `track` | Standard |
| `active_role` | Validation + Governance |
| `artifacts_created` | Intake Snapshot; ANDS-T Task Card; Gate Checklist |
| `missing_evidence` | Gate 2 test evidence; Gate 3 owner acceptance; Gate 5 final outcome |
| `owner_decision` | Decide whether evidence is sufficient to proceed or request fixes before continuing |
| `owner_response` | confirm: evidence plan is acceptable for a synthetic dry run; keep Gate 2 and Gate 3 missing until real evidence exists |
| `next_prompt` | Continue this guided workflow from Gate Checklist to Lessons for workflow_id GW-SYN-001. |
| `boundary_flags` | Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking |

## Gate / Evidence Check

Gate 2 machine quality and Gate 3 human acceptance remain separate. Missing evidence must stay marked as missing.

## Owner Decision

Request execution evidence, approve the evidence plan, or escalate if sensitive data or tenant systems appear.

## Next Prompt

```text
$ands-nexus

Continue this guided workflow from Gate Checklist to Lessons.

State:
- workflow_id: GW-SYN-001
- current_step: Gate
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: Writeback
- artifacts_created: Intake Snapshot; ANDS-T Task Card; Gate Checklist
- missing_evidence: Gate 2 test evidence; Gate 3 owner acceptance; Gate 5 final outcome
- owner_decision: Request execution evidence, approve the evidence plan, or escalate before Lessons if evidence is missing
- owner_response: <owner reply: confirm/revise/escalate/stop: ...>
- next_prompt: Draft candidate Lessons only for workflow_id GW-SYN-001.
- boundary_flags: Candidate-only writeback; Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (synthetic definition and evidence plan, not an implemented outcome):
- Goal: Add a weekly CSV export button to an internal reporting page.
- Inputs: existing report table; fields date/region/revenue; filename weekly-summary-YYYY-WW.csv.
- Acceptance: downloaded CSV contains those fields, covers the previous week, opens in a spreadsheet, and shows a clear empty-state message when no rows exist.
- Acceptance owner: operations lead for this synthetic definition; the actual Owner reply is still required.
- Non-goals: no provider trials, no tenant connectors, no persistence automation.
- Evidence: Gate 2 test evidence and Gate 3 owner acceptance are missing; the evidence plan does not close either Gate. Gate 5 final outcome also remains missing.

Draft candidate Lessons only. Do not write to files, Obsidian, GitHub, provider workspaces, or enterprise systems.
```

## Boundary Reminder

Gate 2 passing cannot replace Gate 3 owner acceptance. Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.

## Step 4 Prompt: Lessons Draft

Before sending this Step Prompt, replace `owner_response` with the human owner's actual reply.

```text
$ands-nexus

Continue this guided workflow from Gate Checklist to Lessons.

State:
- workflow_id: GW-SYN-001
- current_step: Gate
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: Writeback
- artifacts_created: Intake Snapshot; ANDS-T Task Card; Gate Checklist
- missing_evidence: Gate 2 test evidence; Gate 3 owner acceptance; Gate 5 final outcome
- owner_decision: Request execution evidence, approve the evidence plan, or escalate before Lessons if evidence is missing
- owner_response: <owner reply: confirm/revise/escalate/stop: ...>
- next_prompt: Draft candidate Lessons only for workflow_id GW-SYN-001.
- boundary_flags: Candidate-only writeback; Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (synthetic definition and evidence plan, not an implemented outcome):
- Goal: Add a weekly CSV export button to an internal reporting page.
- Inputs: existing report table; fields date/region/revenue; filename weekly-summary-YYYY-WW.csv.
- Acceptance: downloaded CSV contains those fields, covers the previous week, opens in a spreadsheet, and shows a clear empty-state message when no rows exist.
- Acceptance owner: operations lead for this synthetic definition; the actual Owner reply is still required.
- Non-goals: no provider trials, no tenant connectors, no persistence automation.
- Evidence: Gate 2 test evidence and Gate 3 owner acceptance are missing; the evidence plan does not close either Gate. Gate 5 final outcome also remains missing.

Draft candidate Lessons only. Do not write to files, Obsidian, GitHub, provider workspaces, or enterprise systems.
```

Expected output:

## Current Artifact

Lessons Draft:

| Section | Candidate |
|---|---|
| Reusable lesson | A guided first run should keep the next prompt and state packet visible at every step |
| Project-specific context | Weekly CSV export field names and owner acceptance details |
| Regression prompt | Ask the agent to continue from Gate to Lessons while refusing automatic writeback |
| Suggested target | Project-local Lessons draft after human review |

## State Packet

| Field | Value |
|---|---|
| `workflow_id` | `GW-SYN-001` |
| `current_step` | `Lessons` |
| `user_goal` | Add a weekly CSV export button to an internal reporting page |
| `audience` | PM and engineer |
| `data_class` | synthetic |
| `track` | Standard |
| `active_role` | Writeback |
| `artifacts_created` | Intake Snapshot; ANDS-T Task Card; Gate Checklist; Lessons Draft |
| `missing_evidence` | Gate 2 test evidence; Gate 3 owner acceptance; human review before reuse |
| `owner_decision` | Approve, revise, or decline the Lessons candidate; do not authorize broader writeback from this prompt |
| `owner_response` | unfilled - final Lessons review still requires a separate human decision |
| `next_prompt` | If approved, keep this candidate project-local; create no broader writeback unless a separate explicit approval exists. |
| `boundary_flags` | Candidate-only writeback; Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking |

## Gate / Evidence Check

Gate 5 remains open until a human reviews whether the lesson is reusable and whether any project-specific context should stay local.

## Owner Decision

Approve the candidate, request edits, or mark no writeback needed.

## Next Prompt

```text
$ands-nexus

Review this candidate Lessons draft for workflow_id GW-SYN-001.

State:
- workflow_id: GW-SYN-001
- current_step: Lessons
- user_goal: Add a weekly CSV export button to an internal reporting page.
- audience: PM and engineer
- data_class: synthetic
- track: Standard
- active_role: Writeback
- artifacts_created: Intake Snapshot; ANDS-T Task Card; Gate Checklist; Lessons Draft
- missing_evidence: Gate 2 test evidence; Gate 3 owner acceptance; human review before reuse
- owner_decision: Candidate review only; no broader writeback from this prompt
- owner_response: unfilled - final Lessons review still requires a separate human decision
- next_prompt: Close or revise this candidate after human review.
- boundary_flags: Candidate-only writeback; Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking

Task Context (synthetic definition; actual evidence remains missing):
- Goal: Add a weekly CSV export button to an internal reporting page.
- Inputs: fields date/region/revenue; filename weekly-summary-YYYY-WW.csv.
- Acceptance: CSV covers the previous week, opens in a spreadsheet, and shows a clear empty-state message when no rows exist.
- Acceptance owner: operations lead for this synthetic definition; no actual acceptance has been supplied.
- Evidence: Gate 2 test evidence and Gate 3 owner acceptance remain missing; human review is still required before reuse.

Lessons Candidate to review:
- Reusable lesson: A guided first run should keep the next prompt and state packet visible at every step.
- Project-specific context: Weekly CSV export field names and owner acceptance details.
- Regression prompt: Continue from Gate to Lessons while refusing automatic writeback.
- Suggested target: Project-local Lessons draft after human review; no persistence is authorized by this review prompt.

Return only:
1. reusable lesson;
2. project-local details to remove;
3. final owner decision required;
4. confirmation that no broader writeback is authorized by this prompt.

Do not write to files, Obsidian, GitHub, provider workspaces, or enterprise systems.
```

## Boundary Reminder

This is candidate-only. Do not persist unless the human explicitly requests draft generation to one allowed local path; never scan or sync files, GitHub, provider workspaces, or enterprise systems.

## Pass Criteria

| Check | Pass Signal |
|---|---|
| Step control | Each prompt returns the current step only |
| State continuity | The state packet carries all required fields |
| Role separation | AI PM, Validation, Governance, and Writeback stay within their authority |
| Gate clarity | Gate 2 machine quality and Gate 3 human acceptance stay separate |
| Boundary control | Enterprise triggers stop unsafe expansion |
