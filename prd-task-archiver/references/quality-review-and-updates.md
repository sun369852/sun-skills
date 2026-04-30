# Quality Review and Updates

Read this file before saving a task archive and when updating an existing one.

## Self-Review Before Saving

Before writing the archive, check:

- every major PRD requirement maps to at least one task
- every task either maps to a PRD requirement or is clearly labeled as derived technical enablement
- each task has a clear owner area, dependency list, and acceptance check
- each task has priority, risk, deliverable, and status
- open questions and assumptions are visible
- ready tasks and blocked tasks are separated when open questions affect execution
- every MVP-required runtime surface from the delivery topology contract has task coverage or an explicit blocked/skipped reason
- runtime surfaces that need a new project include scaffold/create, startup, smoke, and minimum flow tasks
- task order is feasible
- scope does not exceed the PRD
- existing-project tasks respect current project conventions discovered during inspection
- the archive path is appropriate and will not overwrite unrelated work
- the final response will explicitly state that no code implementation was started

Patch the task list before saving if the review finds gaps.

## Optional Review Subagent

When the host environment supports subagents and delegation is authorized, consider a task-coverage reviewer for large or high-risk PRDs.

Keep the prompt narrow:

```text
Review this draft task archive against the PRD.
Return concise findings only:
- PRD requirements not covered by tasks
- tasks that appear invented beyond the PRD
- missing dependencies or blocked-work markers
- missing test, migration, rollout, or documentation tasks
- tasks too broad for one focused implementation session
Do not rewrite the archive.
```

Use reviewer feedback to patch the main archive. The main flow owns the final file.

## Updating Existing Archives

When updating an existing task archive:

- read the current archive first
- preserve completed, skipped, and in-progress status unless the user explicitly asks to reset them
- add a `Change Log` entry for tasks added, changed, removed, skipped, or newly blocked
- include an update summary in the archive or final response with counts for preserved, added, changed, skipped, and newly blocked tasks
- avoid renumbering existing task IDs unless the archive is still a draft and no work has started
- keep old IDs stable so downstream implementation notes and conversations remain valid
- record why any task became blocked or skipped
- explicitly report whether existing task IDs were renumbered; normally this should be `No`

Suggested update summary shape:

```markdown
Update summary:
- Preserved existing tasks/statuses: [count and key IDs]
- Added tasks: [count and IDs]
- Changed tasks: [count and IDs]
- Skipped tasks: [count and IDs or "None"]
- Newly blocked tasks: [count and IDs or "None"]
- Renumbered existing IDs: No
```

## Common Mistakes

- generating tasks from memory instead of reading the PRD
- rewriting the PRD instead of decomposing it
- saving a vague checklist without dependencies or acceptance checks
- inventing implementation scope beyond the PRD
- hiding implementation-only tasks as product requirements instead of labeling them as derived technical enablement
- omitting QA, migration, rollout, or documentation tasks when they are needed
- omitting a required frontend, miniapp, backend, worker, database, or external service from the task archive
- ignoring existing project conventions for task files
- overwriting an existing archive without explicit user intent
- hiding open PRD questions inside normal tasks
- mixing ready and blocked work so no one can tell what can start now
- creating tasks too broad for one focused implementation session
