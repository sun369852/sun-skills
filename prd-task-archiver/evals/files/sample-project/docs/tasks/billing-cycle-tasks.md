# Billing Cycle Task Breakdown

## Source

- PRD: docs/prd/billing-cycle-prd.md
- Generated: 2026-04-20
- Requirement mode: Existing project iteration
- Project context reviewed: package.json, docs/prd

## Task Graph

| ID | Task | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T001 | Add account billing anchor field | backend | P0 | medium | - | done |
| T002 | Update invoice preview calculation | backend | P0 | high | T001 | in_progress |
| T003 | Add admin settings form | frontend | P1 | medium | T001 | pending |

## Ready Tasks

### T001 - Add account billing anchor field

- Area: backend
- Priority: P0
- Risk: medium
- Source: Functional Requirements 1, 2
- Depends on: -
- Status: done
- Deliverable: Migration and model field
- Acceptance:
  - Existing accounts default to day 1.

### T002 - Update invoice preview calculation

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 3
- Depends on: T001
- Status: in_progress
- Deliverable: Billing preview logic
- Acceptance:
  - Preview uses the account anchor day.

### T003 - Add admin settings form

- Area: frontend
- Priority: P1
- Risk: medium
- Source: Functional Requirement 1
- Depends on: T001
- Status: pending
- Deliverable: Account billing settings UI
- Acceptance:
  - Admin can set anchor day 1 to 28.

## Change Log

- 2026-04-20 Created initial task archive from PRD.
