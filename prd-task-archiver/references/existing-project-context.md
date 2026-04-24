# Existing Project Context

Read this file only when the PRD is for an existing product, workflow, repository, or deployed behavior.

## Context to Gather

Gather a lightweight context package before splitting tasks:

- repository structure and package manifests
- routes/pages/components likely affected
- APIs/controllers/services likely affected
- models/schemas/migrations/jobs/integrations likely affected
- existing tests and fixture patterns
- docs or previous task files that show local task format
- current role names, states, permission rules, and domain terminology
- migration, compatibility, and data-history constraints

Use fast local inspection tools such as `rg`, `rg --files`, manifests, route definitions, schema files, and existing docs. Keep inspection focused; the output is a task archive, not a full technical design.

If the project path is unclear and the task split would be misleading without it, ask one focused question for the project path. If the PRD is greenfield or self-contained, proceed without code inspection.

If the PRD conflicts with the existing project in a material way, do not silently reconcile it. Examples include mismatched role names, incompatible state transitions, renamed domain objects, missing routes/APIs the PRD assumes exist, or data-history rules that contradict current persistence. Capture the conflict as an open question or blocked task, and add a front-loaded alignment task for compatibility semantics or migration strategy.

## Subagent Pattern

When the host environment supports subagents and delegation is authorized, consider a project-context scout for large existing-project iterations.

Keep the prompt narrow:

```text
Inspect the existing project only to support a PRD-to-task breakdown.
Return concise findings:
- likely frontend areas
- likely backend/API/model areas
- relevant tests/fixtures
- migration or compatibility risks
- existing task or docs conventions
- paths worth citing in tasks
Do not implement code. Do not rewrite the PRD or task archive.
```

Use the scout's findings as context, not as confirmed product requirements.

## Compatibility Focus

For existing projects, make sure the task archive includes work for:

- preserving existing user journeys and entry points
- compatibility with current role and permission semantics
- migration or backfill tasks when data shape changes
- regression tests for current behavior that must remain unchanged
- rollout and rollback checks when the change touches production data, integrations, or permissions
