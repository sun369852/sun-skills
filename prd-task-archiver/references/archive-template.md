# Archive Template

Read this file before writing the final Markdown task archive.

Use this structure unless the project already has a stronger local convention:

```markdown
# [Feature Name] Task Breakdown

## Source

- PRD: [path or title]
- Generated: [date/time if available]
- Requirement mode: [New feature / Existing project iteration]
- Project context reviewed: [paths/modules or N/A]

## Summary

- Goal: [one sentence]
- Delivery strategy: [short explanation]
- Key risks / open questions: [short list or None]

## Functional Blocks and Coupling

| Block | Independent Product Behavior | Coupling Rationale | Primary Tasks | Dependencies / Parallelism |
| --- | --- | --- | --- | --- |
| B1 | ... | Shared journey/domain/API/risk | T001, T002 | Can start after ... |

## Component Coverage Matrix

| Runtime Surface | MVP Required | Expected Path | Task Coverage | Startup / Smoke Coverage | Status / Reason |
| --- | --- | --- | --- | --- | --- |
| ... | yes/no | ... | T001, T002 or blocked/skipped reason | T00x or check path | implementation-ready/blocked/skipped |

## Task Graph

| ID | Task | Block | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | ... | B1 | backend | P1 | medium | - | pending |

## Ready Tasks

Tasks in this section can begin once their listed dependencies are satisfied.
When the archive has more than one functional block, group ready tasks by block.

### B1 - [Functional Block Name]

#### T001 - [Task Title]

- Feature block: [B1 - block name]
- Area: [frontend/backend/fullstack/qa/devops/docs/product]
- Priority: [P0/P1/P2]
- Risk: [low/medium/high]
- Source: [PRD section or requirement]
- Depends on: [IDs or "-"]
- Status: pending
- Deliverable: [file, endpoint, UI flow, test suite, checklist, document, or other concrete output]
- Suggested files / areas:
  - [paths, modules, or "To be discovered"]
- Boundaries:
  - [what this task should not change]
- Notes:
  - [implementation guidance]
- Acceptance:
  - [concrete check]
- Validation:
  - [test command, manual check, or verification path when known]

## Blocked Tasks

Use this section only when tasks are blocked by unresolved PRD questions, external decisions, unavailable project context, or prerequisite work.
Group blocked tasks by functional block when that makes ownership clearer.

### B? - [Functional Block Name]

#### T999 - [Blocked Task Title]

- Feature block: [B? - block name]
- Area: [frontend/backend/fullstack/qa/devops/docs/product]
- Priority: [P0/P1/P2]
- Risk: [low/medium/high]
- Source: [PRD section or requirement]
- Depends on: [IDs, decision, or context needed]
- Status: blocked
- Blocker: [specific missing decision or prerequisite]
- Deliverable: [concrete output once unblocked]
- Acceptance:
  - [concrete check once unblocked]

## Coverage Map

| PRD Requirement | Covered By | Notes |
| --- | --- | --- |
| ... | T001, T004 | ... |

## Unmapped PRD Items

- [PRD item not covered by tasks, with reason, or "None"]

## Derived Technical Enablement

- [Task ID and reason it is necessary even though it is not a direct product requirement, or "None"]

## Open Questions and Assumptions

- [question or assumption]

## Change Log

- [date] Created initial task archive from PRD.

## Archive Record

- Created by: PRD Task Archiver
- Archive purpose: implementation task breakdown from existing PRD
- Follow-up: [what should happen next]
```

When the user requests a different format, follow that format while preserving traceability, dependencies, acceptance checks, and archive metadata.

When updating an existing task archive, preserve its history. Add a `Change Log` entry describing tasks added, changed, removed, skipped, or newly blocked, and why those changes were made. Also include an update summary with preserved, added, changed, skipped, newly blocked, and renumbered-ID counts when the update is non-trivial.
