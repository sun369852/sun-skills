# Clean-Context Review

## Default

Do not run a full clean-context second review for every completed task. Use it only when the risk justifies the extra cost.

## Triggers

Trigger clean-context review when:

- permissions, security, payments, audit, deletion, migrations, or public API breaking changes are involved
- multiple workers modify the same core workflow
- a fix succeeds after the 5-attempt failure fuse
- implementation visibly diverges from PRD or technical design
- the user asks for second review, clean-context review, or similar

## Review Packet

Give the reviewer:

- PRD excerpts
- technical-design excerpts
- task checklist entries
- diff summary
- verification results
- risk notes

Do not give the full conversation transcript unless required. The point is independent review.

## Outcome

The main agent integrates review findings, updates the run log, and either fixes issues, blocks the task, or records accepted residual risk.
