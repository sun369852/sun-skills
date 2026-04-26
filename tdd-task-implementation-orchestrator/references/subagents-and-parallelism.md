# Subagents And Parallelism

## Worker Granularity

Assign workers by feature-area task batch, not one worker per checklist item. A worker batch should be coherent enough to verify in one clear pass.

Combine tasks when they share:

- feature area
- module or file group
- acceptance path
- verification command

Split tasks when they differ by:

- business domain
- page or API surface
- data model
- write scope
- risk profile

## Worker Packet

Each worker packet must include:

- task ids and exact checklist text
- feature-area responsibility
- allowed write scope
- files/modules to avoid
- relevant PRD and technical-design excerpts
- discovered project conventions
- TDD/verification expectations
- commands to run or command discovery instructions
- required final output format

Tell workers they are not alone in the codebase. They must not revert edits made by the user or other workers.

## Write Scope

Every worker must have an allowed write scope. A worker may not silently edit outside it. If out-of-scope edits are required, the worker must report that need. The main agent decides whether to expand scope, reassign work, or block the task, and records the decision.

Parallel workers should have disjoint write scopes whenever possible.

## Parallelism Rules

Default maximum parallel workers: 2.

The user may override this in the entry prompt, for example "最多 4 个 worker". If requested parallelism is greater than 2, the main agent must first present a parallel execution plan and wait for confirmation. The plan should include:

- worker count
- task batches
- write scopes
- expected verification commands
- conflict risks
- serial tasks excluded from parallel execution

Even if the user requests high parallelism, only safely independent tasks may run in parallel.

Run serially by default when tasks touch:

- database schema or migrations
- shared API contracts
- global state
- core type definitions
- route structure
- permissions or security model
- shared test environment that cannot isolate runs

## Worker Output

Workers must return:

```markdown
## Task IDs
## Summary
## Files Changed
## Tests Added Or Updated
## Commands Run
## Verification Result
## Checklist Recommendation
## Blockers
## Risk Notes
```

`Checklist Recommendation` must be one of `done`, `partial`, or `blocked`. The main agent makes the final status decision.
