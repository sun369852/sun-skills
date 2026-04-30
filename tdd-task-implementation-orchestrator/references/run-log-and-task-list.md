# Run Log And Task List

## Run Log Location

Create one timestamped run log beside the task checklist:

```text
implementation-run-<yyyy-mm-dd-HHmm>.md
```

Examples:

- `docs/implementation-run-2026-04-26-1530.md`
- `specs/invite/implementation-run-2026-04-26-1530.md`

Do not overwrite prior logs. Append only when the user explicitly asks.

## Run Log Structure

Use this structure:

```markdown
# Implementation Run Log

## Execution Mode
## Scope
## Source Documents
## Task Batches
## Parallelization Decisions
## TDD Decisions
## Test Skips
## Runtime Verification
## Auto-Approved Decisions
## Failure Attempts
## Blockers
## Risk Notes
## Git / Worktrees / Commits
## Final Verification
```

`Execution Mode` must record:

- `Mode: standard | full-auto`
- confirmation rules
- max parallel workers
- whether commit/worktree operations are authorized or used

## Auto-Approved Decisions

Record automatic approvals, especially in full-auto mode:

```markdown
- Added dev dependency `x` because existing tools could not cover required integration behavior.
- Updated snapshot for component Y after verifying the change matches acceptance criteria.
```

## Task List Updates

The main agent updates the task list. Workers only recommend status.

Respect the existing format:

- Markdown checkbox: use `[ ]` / `[x]` and add nested verification or blocker notes.
- Table: update only status, verification, and notes columns.
- Existing status enum: preserve it.

If no format exists, use:

- `pending`
- `in_progress`
- `done`
- `partial`
- `blocked`
- `failed`

Do not rewrite or reorder the entire task list. Do not paste the run log into the task list. Keep a link or short note to the run log when useful.

Status meanings:

- `done`: implementation complete and required test/runtime verification passed
- `partial`: implementation complete but required verification is incomplete, skipped, or blocked
- `blocked`: cannot proceed because a required decision, artifact, dependency, credential, service, or environment is missing
- `failed`: required verification failed and needs a fix before continuing

A task with skipped required verification cannot be marked `done`. Demote it to `partial`, `blocked`, or `failed` and record the reason in the run log.
