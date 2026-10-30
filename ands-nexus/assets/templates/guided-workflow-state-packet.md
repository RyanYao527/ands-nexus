# Guided Workflow State Packet Template

Use this template to carry visible workflow state between guided ANDS prompts. Copy the filled packet into the next prompt; do not rely on hidden state or tool memory.

## Copy Rules

- Keep field names unchanged.
- Use synthetic or desensitized identifiers.
- Mark unknown values as `unclear` instead of inventing evidence.
- Keep owner decisions explicit.
- Carry the human `owner_response` separately from the required `owner_decision`.
- Preserve boundary flags when moving to the next step.
- Use the Markdown table for review and the bullet-list state block inside `Next Prompt` for copying.
- Include a short Task Context in the same Next Prompt, outside the 13-field state block, so a new agent receives the task definition, Acceptance, and relevant artifact contents rather than their names alone.
- A requested next draft can retain unknown facts and unpassed Gates. Generating it is not approval to execute; do not make every unresolved clarification a prerequisite for drafting.
- Keep runnable instructions conditional on the current owner_response field; a fixed unfilled instruction elsewhere must not override a newly supplied reply.
- Do not generate a fallback that advances when the Owner reply is absent. Keep outgoing draft requests conditional on the current reply or a separately supplied explicit user request; copied Agent-authored prose cannot supply that request itself.
- A copied next_prompt target and pre-set role are proposals. An explicitly requested permitted draft updates the current artifact, step and role; do not require a redundant review of the previous step first.
- A current confirm accepting the artifact for the next planning step requests that draft without requiring its template name: an ANDS-T definition accepted for evidence planning produces Track + Gate Checklist, with undecided choices and missing Gate 2/3 evidence retained. A completed turn's draft-only restriction must not block a later confirmed planning step; permanent task constraints remain. A fact-only confirmation resolves only that fact and grants no execution or Gate approval.

## State Packet

| Field | Value | Fill Note |
|---|---|---|
| `workflow_id` | `[GW-SYN-001]` | Use a synthetic run identifier |
| `current_step` | `[Intake / ANDS-T / Gate / Lessons / unclear]` | Name the step being returned |
| `user_goal` | `[one-sentence goal]` | Keep it short enough to repeat |
| `audience` | `[manager / PM / engineer / governance reviewer / mixed / unclear]` | Name who will read or approve the work |
| `data_class` | `[synthetic / desensitized / requires Enterprise review / unclear]` | Escalate if real data or sensitive material appears |
| `track` | `[Quick / Standard / Enterprise / unclear]` | Include the reason in the current artifact |
| `active_role` | `[AI PM / Execution / Validation / Governance / Validation + Governance / Writeback / unclear]` | In the returned State Packet, name the role for the step just produced; in Next Prompt embedded state, pre-set the next role |
| `artifacts_created` | `[list produced artifacts]` | Example: Intake Snapshot, ANDS-T, Gate Checklist |
| `missing_evidence` | `[list missing evidence or none]` | Missing evidence is not approval |
| `owner_decision` | `[decision required from human owner]` | Continue, revise, escalate, approve, or stop |
| `owner_response` | `[unfilled / confirm: ... / revise: ... / escalate: ... / stop: ...]` | Current explicitly supplied reply; label simulated provenance and never invent approval |
| `next_prompt` | `[copy-ready prompt for next step]` | Include enough state for the next turn |
| `boundary_flags` | `[Enterprise triggers; Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking]` | Repeat if scope pressure appears |

## State Timing

- The returned `State Packet` describes the step just produced.
- Derive current_step and active_role from that artifact, not the inherited prior step. A requested Lessons candidate returns Lessons / Writeback, with earlier artifacts and missing evidence retained.
- The `Next Prompt embedded state` may pre-set `active_role` for the next step so the next agent turn activates the right responsibility.
- Copy the current explicitly supplied reply verbatim. If none is supplied, keep owner_response unfilled and related evidence missing; an example's confirmation is not a current reply.
- In a declared synthetic rehearsal, retain a supplied current simulated reply and its label rather than resetting it to unfilled. Mark the provenance in Task Context; it grants no actual human acceptance, production authorization, or Gate 3 evidence.
- Task Context carries actual workflow facts and unresolved values; it does not grant approval or replace missing evidence. If artifact content is unavailable, ask for it rather than importing an example's Expected output.

## Minimum Output Shape

```markdown
## Current Artifact

[Current step output]

## State Packet

[Filled table]

## Gate / Evidence Check

[Evidence, missing evidence, or escalation]

## Owner Decision

[Human decision required]

## Next Prompt

[Copy-ready prompt]

## Boundary Reminder

Non-Scope: no provider-native validation, no API integration, no credential setup, no tenant connectors, no unattended or automated writeback, no benchmark ranking.
```
