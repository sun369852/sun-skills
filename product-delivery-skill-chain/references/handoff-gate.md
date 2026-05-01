# Handoff Gate

Use this reference before routing to a downstream skill. The handoff gate validates that the upstream artifact is trustworthy enough for the next stage to consume.

The gate is not a substitute for each skill's internal quality gate. It is a lightweight pre-flight check that runs at the chain level, before the downstream skill starts its own work. It prevents propagating artifacts that are missing critical required content.

## Gate Check Rule

Run the gate check for the specific transition. If the check fails:

1. Record the gate result in `delivery-chain-status.md` with `GATE_BLOCKED` status and the specific reason.
2. Do not route to the downstream skill.
3. If the chain is in full-auto or controlled-upstream backtrack mode, automatically return to the upstream skill to fix the gap.
4. If the chain is in semi-auto or ask-each-stage mode, report the gate result and ask the user.

Gate results use three statuses:

| Status | Meaning |
| --- | --- |
| `GATE_PASS` | Upstream artifact meets minimum requirements. Route to downstream. |
| `GATE_PASS_WITH_NOTES` | Upstream artifact is usable but has non-blocking gaps. Route with notes in the envelope. |
| `GATE_BLOCKED` | Upstream artifact is missing critical content. Do not route. |

## Gate: Requirement Exploration → PRD

Validate against `handoff-contracts.md` minimum handoff requirements.

**Required presence checks (all must pass):**

| Check | What to verify |
| --- | --- |
| Confirmed goal | The downstream prompt clearly states the product objective. |
| Target users | The prompt identifies who the feature is for. |
| Main scenarios | At least one core workflow or scenario is described. |
| Scope boundaries | Non-goals or out-of-scope items are stated, or explicitly blank as "not discussed." |
| Open questions | Unresolved items are listed, or explicitly stated as "none remaining." |
| Acceptance expectations | Success criteria or acceptance expectations are recorded. |

**Fallback behavior:**

- If 3+ checks fail → `GATE_BLOCKED`. The requirement is still too vague; stay in exploration.
- If 1-2 checks fail → `GATE_PASS_WITH_NOTES`. Route to PRD but note the gaps in the invocation envelope so the PRD skill can target them.
- If no user permission to generate was given → `GATE_BLOCKED`. Do not pass until the user explicitly approved downstream generation.

## Gate: PRD → Technical Design

Validate against `handoff-contracts.md` minimum handoff.

**Required presence checks:**

| Check | What to verify |
| --- | --- |
| PRD file exists | Path resolves and file is non-empty. |
| Functional requirements | At least one functional requirement section is present with specific behavior. |
| Acceptance criteria | Acceptance criteria are explicit, not just "works as expected." |
| Business rules | States, permissions, data expectations are covered, or marked as TBD. |
| Open questions | Blocking and non-blocking open questions are marked. |

**Quality signal check:**

If the PRD was produced by `prompt-to-prd-review`, read its review record. Check whether frontend and backend review are both marked as `Approved`. If either reviewer still has blocking findings, the PRD is not safe for technical design.

**Fallback behavior:**

- PRD file missing or empty → `GATE_BLOCKED`.
- No concrete functional requirements → `GATE_BLOCKED`.
- Blocking reviewer findings exist → `GATE_BLOCKED`. Return to PRD review.
- Up to 2 minor missing items (e.g., permissions not discussed) → `GATE_PASS_WITH_NOTES`.

## Gate: PRD → Audit Standards

Same check as PRD → Technical Design. Audit standards require the same minimum PRD quality.

Additional check:

| Check | What to verify |
| --- | --- |
| Traceable requirements | PRD requirements can be extracted into individual checkable items. If the PRD is too vague to decompose, gate blocks. |

## Gate: PRD or Design → Task Archive

Validate against `handoff-contracts.md`.

**Required presence checks:**

| Check | What to verify |
| --- | --- |
| PRD available | PRD path or full content is present. |
| Technical design available | When tasks require implementation structure decisions, a technical design should exist. If missing and the work is complex, note it. |
| Dependencies known | Known dependencies, risks, and blocked questions are documented or stated as "not yet analyzed." |

**Technical design linkage:**

If a technical design exists, verify that it covers at least the API contracts, data model, or UI architecture needed to split tasks. If the design exists but is too vague to inform task boundaries, mark `GATE_PASS_WITH_NOTES` and surface the gap.

**Fallback behavior:**

- No PRD → `GATE_BLOCKED`. Design alone is not sufficient as source of truth.
- Tech design missing for complex work → `GATE_PASS_WITH_NOTES`. Flag as high risk for inaccurate task boundaries.

## Gate: Tasks → Implementation

Validate against `handoff-contracts.md` implementation handoff packet.

**Required presence checks:**

| Check | What to verify |
| --- | --- |
| Task list exists | File is present and non-empty. |
| Tasks are actionable | Each task has a clear description, verification expectation, and bounded write scope. |
| Source artifacts attached | PRD and technical design paths are available. |
| Blockers visible | Blocked tasks or known risks are documented. |

**Fallback behavior:**

- No task file → `GATE_BLOCKED`. Need task archive first.
- Tasks are vague or untestable → `GATE_PASS_WITH_NOTES`. Flag for the orchestrator to handle inline.

## Gate: Implementation → Review

Validate against `handoff-contracts.md`.

**Required presence checks:**

| Check | What to verify |
| --- | --- |
| Review scope is clear | Diff, branch, commits, or file list is identifiable. |
| Source artifacts available | PRD, technical design, task list paths are present or inferable. |
| Audit standards available | When relevant, `quality-audit-standards.md` path is provided or noted as skipped. |

**Fallback behavior:**

- No diff or scope → `GATE_BLOCKED`. Cannot review what is not defined.
- Audit standards available but not provided → `GATE_PASS_WITH_NOTES`. Note that a stronger review is possible with audit standards.
