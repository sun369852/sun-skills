# Billing Cycle Task Breakdown

## Source

- PRD: docs/prd/billing-cycle-prd.md
- Generated: 2026-04-20
- Updated: 2026-04-24
- Requirement mode: Existing project iteration
- Project context reviewed: package.json, docs/prd

## Task Graph

| ID | Task | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T001 | Add account billing anchor field | backend | P0 | medium | - | done |
| T002 | Update invoice preview calculation | backend | P0 | high | T001 | in_progress |
| T003 | Add admin settings form | frontend | P1 | medium | T001 | pending |
| T004 | Add anchor day validation and upcoming date display | fullstack | P1 | medium | T002, T003 | pending |
| T005 | Record audit events for anchor changes | backend | P0 | high | T001 | pending |
| T006 | Expose anchor change history in support tools | fullstack | P1 | medium | T005 | pending |
| T007 | Add billing cycle regression coverage | test | P0 | medium | T002, T004, T005 | pending |

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

### T004 - Add anchor day validation and upcoming date display

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Functional Requirement 1; Acceptance Criteria 2, 3
- Depends on: T002, T003
- Status: pending
- Deliverable: Validation and account settings upcoming invoice date
- Acceptance:
  - Invalid anchor days outside 1 to 28 are rejected.
  - Admin can see the recalculated upcoming invoice date after updating the anchor day.

### T005 - Record audit events for anchor changes

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 5
- Depends on: T001
- Status: pending
- Deliverable: Audit event emission for billing anchor changes
- Acceptance:
  - Changing the anchor day writes an audit event with actor, timestamp, previous anchor day, and new anchor day.
  - Repeated or retried processing remains idempotent for webhook-adjacent billing flows.

### T006 - Expose anchor change history in support tools

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Functional Requirement 4
- Depends on: T005
- Status: pending
- Deliverable: Support tooling view of anchor change history
- Acceptance:
  - Support tools show previous anchor day, new anchor day, actor, and timestamp.

### T007 - Add billing cycle regression coverage

- Area: test
- Priority: P0
- Risk: medium
- Source: Compatibility Requirements; Acceptance Criteria 4, 5; package.json scripts
- Depends on: T002, T004, T005
- Status: pending
- Deliverable: Vitest and/or Playwright regression tests for billing cycle behavior
- Acceptance:
  - Regression tests cover default first-day cycle behavior for accounts without a custom anchor.
  - Tests verify historical invoices are not recalculated after anchor changes.
  - Tests cover invalid anchor day rejection.

## Change Log

- 2026-04-20 Created initial task archive from PRD.
- 2026-04-24 Updated archive from PRD review, preserving existing task IDs and statuses while adding coverage for validation, support history, audit events, compatibility, and regression tests.
