# Final Report

Use this reference to decide whether and where to save a report. Load `references/final-report-template.md` only when writing a full report or saved artifact.

## Saving Reports

User instructions win: save or do not save when the user explicitly says so. If the user does not decide, choose based on handoff value.

Prefer saving when:

- the decision is `Fix needed` or `Blocked`
- a developer fix packet is needed
- a re-review loop is active
- third-party standards or `quality-audit-standards.md` were used
- the existing workflow has a run log or task list where an audit record is expected
- another agent, QA, reviewer, or developer will continue from the result

Prefer conversation-only output for small passing reviews without formal standards or follow-up handoff.

Choose a conservative path such as `implementation-review-report.md` beside the task list, run log, or audit standards file. If the file exists, append the current date or a numeric suffix instead of overwriting. Report the saved path in the final response.

Reports should keep these core sections even when there are no findings: findings, decision, scope reviewed, verification, coverage notes, and saved report path. Add standards, developer handoff, upstream decision, runtime surface/startup status, and loop history sections only when relevant.

Keep the report concise. The user needs to know whether to merge, fix, or provide missing context.
