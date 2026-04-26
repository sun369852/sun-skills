# Review Workflow

## Pass 1: Requirement Coverage

Map delivered changes to the source of truth:

- PRD-derived audit checks such as `BV-*`, `IA-*`, `TE-*`, `RG-*`, `EV-*`, and `BQ-*` when a quality standards artifact exists
- each completed task or acceptance criterion
- expected user-visible behavior
- API, data, permission, validation, and state changes
- required edge cases and error states
- explicit non-goals or out-of-scope areas

Flag any requirement or audit check with no implementation evidence, no test evidence, missing required evidence, or contradictory behavior.

## Pass 2: Diff and Architecture Review

Inspect changed files with the repository's existing style and boundaries in mind:

- behavior correctness and regression risk
- contract compatibility between frontend/backend/API/data layers
- state handling, validation, error handling, loading/empty states, and permission checks
- data migration, persistence, idempotency, concurrency, and rollback concerns when relevant
- test coverage relative to risk
- unnecessary scope expansion or speculative abstractions

Keep findings concrete. If a concern is only a preference, leave it out unless it affects maintainability or future correctness.

## Pass 3: Task and Documentation Consistency

When task lists, run logs, or status documents exist, check whether they match reality:

- completed tasks have implementation and verification evidence
- audit check statuses match actual evidence; `Blocked` and `Not Run` are not treated as passes
- blocked/partial tasks are not marked complete
- run log records commands, failures, retries, and skipped checks
- docs or comments were updated only when behavior changed enough to require it

Do not rewrite task state during review-only work unless the user explicitly asks.

## Task Status Updates

Default to read-only task status handling:

- do not silently change completed, blocked, or partial task states
- if task status does not match implementation evidence, report the mismatch as a finding or coverage note
- if the user asks to save an audit record, append the review conclusion or recommended status instead of rewriting the development history
- in review-and-fix mode, update task status only when the user explicitly asks for it; otherwise report the post-fix recommendation

Use suggested statuses such as `accepted`, `fix-needed`, or `blocked` in the report, but do not mutate task files without authorization.

## Severity

Use this scale:

- `P0`: data loss, security break, crash on core path, production-blocking release risk
- `P1`: missed acceptance criterion, broken important workflow, failing required test, incompatible API/data contract
- `P2`: edge-case bug, incomplete verification for meaningful risk, maintainability issue likely to cause defects
- `P3`: minor cleanup, clarity issue, weak test naming, low-risk follow-up

When a quality audit standards artifact uses `Blocker`, `High`, `Medium`, or `Low`, map them to review severity as:

- `Blocker` -> `P0` unless the impact is clearly bounded to `P1`
- `High` -> `P1`
- `Medium` -> `P2`
- `Low` -> `P3`

Prefer fewer, stronger findings. A review with no findings is acceptable if the evidence supports it.

## Clean-Context Review

Use a clean-context reviewer only when explicitly requested or when the user asks for independent reviewers/subagents. Give the reviewer:

- source artifacts or compact summaries
- changed files or diff scope
- verification commands and known results
- exact output requested: findings only, severity-ranked, no fixes

The main agent integrates reviewer output, checks it against local evidence, and owns the final decision.
