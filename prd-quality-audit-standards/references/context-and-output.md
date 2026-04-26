# Context And Output

Use this reference when the user provides a project path, supporting documents, an output path, or asks whether to split files.

## Inputs

Expected input can be any of:

- PRD file path
- pasted PRD content
- PRD plus technical design, task archive, or project path
- explicit output path for the audit standards document
- request such as "基于 PRD 生成质量审核标准，并做三轮干净上下文复核"

The PRD remains the source of truth. Technical design and task archives can clarify implementation constraints, but they do not expand product scope unless the user explicitly says they are authoritative.

## Bounded Project Inspection

Project inspection is optional when no project path is available. When a project path is available, inspect only files that affect the audit contract:

- package/test configuration and documented test commands
- route/API entry points corresponding to the PRD
- schema/model/data access files
- auth, permission, role, and policy code
- logging, audit, metrics, tracing, and observability conventions
- existing test directories and naming patterns
- release, migration, feature-flag, or seed data conventions

Record inspected files and how they affect the standards. Do not perform a full-repository scan.

If no project path is available, generate project-agnostic standards and mark project-specific execution details as needing later resolution.

## Output Path

If the user provides an output path, use it unless it would overwrite an unrelated file.

If no output path is provided:

1. If the PRD lives in a feature/spec folder, save beside it as `quality-audit-standards.md`.
2. If there is an existing convention such as `docs/qa/`, `specs/<feature>/`, or `quality/`, follow it.
3. If the PRD was pasted, create `quality-audit/<yyyy-mm-dd>-<feature-slug>-quality-audit-standards.md` in the current workspace or project root.

Never silently overwrite an unrelated audit standards file. If the target exists and the user did not ask to update it, create a versioned filename such as `quality-audit-standards-<yyyy-mm-dd>.md`.

## Single File Vs Split Files

Default to one Markdown artifact with a machine-readable JSON or YAML appendix.

For complex PRDs or explicit user requests, split into:

- `quality-audit-standards.md`
- `audit-checks.json`
- `clean-context-review-record.md`
- `audit-report-template.md`

When splitting files, the main Markdown artifact must link all auxiliary files.
