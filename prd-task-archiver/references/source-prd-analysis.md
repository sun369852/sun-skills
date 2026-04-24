# Source PRD Analysis

Read this file after locating the PRD. The purpose is to keep the PRD as the source of truth and avoid inventing work.

## Source Map

Extract a compact source map before drafting tasks:

- feature name and business goal
- target users, roles, permissions, and scenarios
- functional requirements
- non-goals and out-of-scope items
- business rules, state transitions, data rules, and integrations
- acceptance criteria
- risks, assumptions, and open questions

Preserve the PRD's terminology. Do not convert assumptions into confirmed facts. Do not add attractive features that the PRD did not request.

## Completeness Check

Proceed when the PRD is complete enough to support implementation planning. It can still contain open questions as long as they are visible and do not distort the core task split.

Ask one focused question or suggest returning to PRD review when:

- the source PRD is missing
- product semantics are still undecided
- role, ownership, or permission rules are too unclear to plan safely
- the main workflow or object lifecycle is ambiguous
- acceptance criteria are absent for the core behavior

When unresolved PRD questions affect only part of the work, split the archive into ready work and blocked work. Do not let one unresolved detail block unrelated tasks that can safely proceed.

## Traceability Rules

Every task should map to a PRD requirement or be labeled as derived technical enablement.

If any PRD requirement is not covered by a task, add it to `Unmapped PRD Items` with the reason.

If a task exists mainly to enable implementation rather than deliver a direct product requirement, label it as `Derived / Technical Enablement` and explain why it is necessary.
