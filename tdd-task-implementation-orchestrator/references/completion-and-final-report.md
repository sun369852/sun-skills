# Completion And Final Report

## Final Status

Use:

- `done`: implementation complete, verification acceptable, main-agent review passed
- `partial`: some implementation complete but acceptance or verification remains incomplete
- `blocked`: cannot continue without missing decision, artifact, dependency, or environment
- `failed`: required verification failed and needs a fix before continuing

## Final Report

Keep the final response short and actionable:

```markdown
## Completed
- task batches or task ids completed

## Changed
- key files or modules

## Verification
- Build Verification
- Runtime Verification
- API Smoke
- Skipped / Blocked Verification

## Task List
- updated task list path

## Run Log
- run log path

## Commits
- commit hashes/messages if any

## Blocked / Partial
- unresolved items and required decisions
```

Do not paste the full run log unless the user asks.

Do not summarize `compile passed` as `verified` when runtime verification was required. Call out any skipped, blocked, or failed required verification separately.
