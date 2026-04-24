# Project Context

## Requirement Mode

Existing project iteration.

The source prompt says this is an incremental change to an existing order after-sales module. The requested PRD therefore treats current order refund, after-sales approval, permission, refund list/detail, and export behavior as existing product surfaces that must be preserved.

## Repository Inspection

Inspected workspace: `D:\sun-skills`

Commands/context checked:

- Top-level workspace directories.
- Git status to avoid touching unrelated work.
- Recursive file listing for common source and documentation extensions.
- Recursive search for order/refund/after-sale terms in file names and small text files.
- Prompt-to-PRD skill references and reviewer prompts.
- Existing eval metadata for this task.

## Relevant Findings

| Area | Finding | PRD Treatment |
| --- | --- | --- |
| Current repository shape | The workspace mainly contains skill definitions and eval workspaces: `prompt-to-prd-review`, `requirement-exploration`, `prd-task-archiver`, and related output directories. | Recorded as a context limitation; PRD avoids claiming exact existing routes, API names, components, or schemas. |
| Order/refund module code | No concrete order after-sales module, refund list/detail page, refund approval API, permission model, or export implementation was found in the inspected repository. Search hits were skill/eval documents rather than product source code. | PRD defines product behavior and compatibility expectations without binding to nonexistent code paths. |
| Existing behavior to preserve | Source prompt explicitly states reason tags are backend-only, historical refund orders are not backfilled, permission follows existing after-sales audit permission, and no new role is added. | These are treated as confirmed compatibility constraints. |
| Open item | Whether operators may modify the tag after approval is unresolved. | Recorded as a non-blocking open question because first-version behavior can default to no post-approval modification until decided. |

## Context Limitation

Although the task states the current repository is the project code, the available workspace does not expose the expected application code for the order after-sales module. Frontend and backend review therefore used the source prompt plus this compact inspection result as the current-project context package. This does not block saving the PRD because the unresolved repository mismatch does not change the requested first-version product semantics; it is recorded as a compatibility risk.
