# Handoff Contracts

Use this file to check whether one stage can safely feed the next stage.

The chain-level handoff gate (`references/handoff-gate.md`) runs these checks **before** routing. If the gate passes, the downstream skill still performs its own internal quality checks—the handoff gate is a pre-flight, not a replacement.

## Requirement Exploration to PRD

Minimum handoff:

- confirmed user goal and target users
- main scenarios or workflows
- scope boundaries and explicit non-goals
- assumptions and open questions
- acceptance expectations or success criteria
- existing-project compatibility notes when relevant

If the requirement still relies on major guesses, stay in `requirement-exploration`.

Human gate: require confirmation before PRD generation if the requirement was materially ambiguous and the user has not explicitly approved the clarified scope.

## PRD to Technical Design

Minimum handoff:

- PRD path or full PRD content
- functional requirements and acceptance criteria
- business rules, states, permissions, and data expectations when relevant
- open product questions marked clearly

If product behavior is still undecided, do not hide it in the technical design. Record assumptions or return to PRD work.

Human gate: after PRD approval, confirm before entering downstream planning unless the user explicitly requested continuous chain execution. In continuous chain mode, record the confirmation or inferred authorization in `delivery-chain-status.md`.

## PRD to Audit Standards

Minimum handoff:

- PRD path or full PRD content
- functional requirements and acceptance criteria
- business rules, permissions, data expectations, and high-risk flows when relevant
- known open questions or blocked verification areas

Generate audit standards before implementation by default. For low-risk small changes, the chain may record lightweight acceptance notes instead of a full audit standards artifact, but full standards are required for permissions, data changes, migrations, payments, external integrations, complex business rules, or critical user-visible flows.

## PRD or Design to Tasks

Minimum handoff:

- PRD as source of truth
- technical design when implementation structure, API/data contracts, migrations, or UI architecture matter
- known dependencies, risks, blocked questions, and validation expectations

If the current entry artifact is a technical design, it can feed task archiving only when a linked PRD path or PRD content is also available. The PRD remains the source of truth; the technical design is an implementation constraint. If only a technical design exists and no PRD can be found, stop and ask for the PRD path or content.

If tasks would require inventing product semantics or architecture decisions, route back to PRD or technical design.

Default sequencing: create formal tasks after the technical design is ready. Fast mode may create draft tasks from the PRD in parallel with technical design, but the draft must be labeled as pending technical design confirmation and reconciled before implementation.

## Tasks to Implementation

Minimum handoff:

- actionable task list with dependencies and statuses
- source PRD and technical design paths when available
- verification expectations
- bounded write scope or clear feature area

If a task is not executable, mark it blocked instead of coding around uncertainty.

Human gate: before handing work to `tdd-task-implementation-orchestrator`, confirm coding should begin unless the user explicitly requested full-auto execution.

Implementation handoff packet:

- PRD path
- technical design path
- task archive path
- audit standards path, if available
- `delivery-chain-status.md` path
- chain artifact directory
- chain start contract path
- downstream invocation envelope
- git handoff policy, including commit, push, and pull request authorization
- confirmed assumptions
- known blockers
- coding confirmation status

Hand this packet to `tdd-task-implementation-orchestrator` once. Let that skill own batching, worker use, verification, run log updates, task status updates, and commit granularity when commits are authorized.

## Implementation to Review

Minimum handoff:

- review scope: current diff, branch, commits, or named files
- source artifacts: PRD, technical design, tasks, audit standards, or user prompt
- run log or verification notes when available
- known skipped tests, blocked areas, or accepted risks

If strict acceptance matters and no audit standards exist, mention that `prd-quality-audit-standards` can strengthen the review contract.

Review-fix loop: if `implementation-review-handoff` finds bounded implementation defects, the chain may route a fix packet back to `tdd-task-implementation-orchestrator` and re-review. Default maximum: 5 loops. Stop and ask the user for product scope changes, architecture replacement, audit standard changes, dangerous operations, or loop exhaustion.

Review-fix loop scope:

Can loop automatically when the defect is bounded to implementation:

- implementation bug inside already-approved scope
- missing error handling for a defined flow
- missing or weak tests for defined behavior
- small integration mismatch that does not change PRD, technical design, task scope, or audit standards

Stop and ask when the fix requires upstream decisions:

- PRD ambiguity or product behavior conflict discovered during review
- technical design conflicts with implementation reality and needs redesign
- audit standards require behavior not present in the PRD
- fix changes task scope, data semantics, permissions, external integrations, or risky operations

Track the loop as `current/max`, such as `2/5`, in `delivery-chain-status.md`.

## Risk-Based Confirmation

- Low-risk supplements can be recorded as assumptions, notes, or non-blocking follow-ups.
- Medium-risk uncertainty should include a recommended decision; ask the user if it changes task scope, acceptance criteria, or implementation complexity.
- High-risk product semantics require user confirmation.
- Missing files, unreadable paths, or obviously incomplete source artifacts require one blocking question.
