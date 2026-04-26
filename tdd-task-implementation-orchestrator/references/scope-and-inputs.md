# Scope And Inputs

## Execution-Only Boundary

This skill only executes development work from existing planning artifacts. It must not create the PRD, produce the technical design, or generate a full task breakdown.

If source artifacts are missing:

- Missing PRD or technical design: stop the affected execution and ask for the missing source or record a blocker.
- Missing task checklist: stop and ask for the task checklist.
- Vague task such as "implement user management module": mark blocked because the task is too broad to execute safely.

The orchestrator may provide a minimal clarification list that explains what is missing, but must not replace upstream planning.

## Expected Inputs

Inputs can include:

- PRD path or pasted PRD content
- task checklist path, often `tasks.md`
- technical design, architecture, API, database, UI, or testing docs
- repository path
- preferred test/build command
- requested task range, priority, max parallel workers, full-auto mode, or forbidden files/modules

If paths are not explicit, inspect the repository for likely files before asking. Search names such as `prd`, `requirements`, `technical-design`, `design`, `architecture`, `tasks`, `spec`, `plan`, `.speckit`, `.openspec`, and `docs`.

## Task Eligibility

A task may be claimed only when:

- it has a stable id or clear title
- it has acceptance criteria or enough detail to derive verification
- dependencies are complete or explicitly absent
- write scope can be bounded
- it does not require new product or architecture decisions

If any criterion fails, mark the task `blocked` with a concise reason.

## Task Execution Order

Choose task order by:

1. User-specified scope or priority.
2. Checklist dependency order.
3. Foundation tasks that unblock later work.
4. High-risk shared contracts handled in small serial steps, such as schema, API, or shared types.
5. Independent low-conflict tasks that can be parallelized.
6. Copy, style, cleanup, or low-risk polish tasks unless the user prioritized them.

## Direct Inline Work

Do not spawn workers for every task. The main agent should handle these directly:

- single-file low-risk fixes
- copy, style, config, or small type annotation changes
- exploratory reading and task classification
- tightly coupled work requiring continuous reasoning
- tiny changes where worker setup would cost more than implementation

Use workers when a task batch is independent, verifiable, bounded, and complex enough that isolated context reduces risk.
