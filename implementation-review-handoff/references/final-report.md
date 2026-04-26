# Final Report

Use this structure unless the user requested a different format. Keep the same structure even when there are no findings; only simplify the `Findings` section.

## Saving Reports

Default to a conversation report. Save a durable audit report only when:

- the user explicitly asks to save one
- the existing workflow has a run log or task list where an audit record is expected
- the review is standards-based and the user needs an artifact for handoff

Choose a conservative path such as `implementation-review-report.md` beside the task list, run log, or audit standards file. If the file exists, append the current date or a numeric suffix instead of overwriting. Report the saved path in the final response.

```markdown
## Findings

- [P1] Short finding title
  Audit check: BV-001 / IA-001 / TE-001 / none
  File: path/to/file.ext:123
  Evidence: what proves the issue
  Impact: why it matters
  Recommendation: the smallest useful fix

If there are no findings:

No blocking findings.

## Decision

Pass / Pass with notes / Fix needed / Blocked

- Standards conclusion: Rejected / Blocked / Approved with Risks / Approved / N/A

## Scope Reviewed

- Source of truth: ...
- Audit standards: path or not provided
- Change scope: ...
- Assumptions: ...

## Verification

- `command`: passed/failed/skipped/not run. Related check IDs: ... Short evidence.

## Coverage Notes

- Requirement/task coverage: ...
- Audit check coverage: ...
- Not reviewed: ...
- Residual risk: ...

## Saved Report

- Path: saved path or not saved
```

Keep the report concise. The user needs to know whether to merge, fix, or provide missing context.
