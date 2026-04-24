# Billing Cycle Task Breakdown

## Source

- PRD: docs/prd/billing-cycle-prd.md
- Existing archive: docs/tasks/billing-cycle-tasks.md
- Generated: 2026-04-24
- Requirement mode: Existing project iteration
- Project context reviewed: package.json, docs/prd, docs/tasks

## Summary

- Goal: Allow account-specific billing cycle anchor days while preserving default monthly billing behavior and invoice history.
- Delivery strategy: Keep existing started work stable, add missing audit, support tooling, validation, regression, and release coverage as new tasks.
- Key risks / open questions: Invoice preview and webhook idempotency touch billing-critical behavior; no open PRD questions block task planning.

## Task Graph

| ID | Task | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T001 | Add account billing anchor field | backend | P0 | medium | - | done |
| T002 | Update invoice preview calculation | backend | P0 | high | T001 | in_progress |
| T003 | Add admin settings form | frontend | P1 | medium | T001 | pending |
| T004 | Add anchor-day validation and update API behavior | backend | P0 | medium | T001 | pending |
| T005 | Emit audit event when anchor day changes | backend | P0 | high | T004 | pending |
| T006 | Show billing anchor history in support tools | fullstack | P1 | medium | T005 | pending |
| T007 | Add billing-cycle regression and compatibility tests | qa | P0 | high | T002, T004, T005 | pending |
| T008 | Add release checks for billing data compatibility | devops | P1 | medium | T007 | pending |

## Ready Tasks

Tasks in this section can begin once their listed dependencies are satisfied.

### T001 - Add account billing anchor field

- Area: backend
- Priority: P0
- Risk: medium
- Source: Functional Requirements 1, 2; Compatibility Requirements
- Depends on: -
- Status: done
- Deliverable: Migration and model field
- Suggested files / areas:
  - Account model, Prisma schema, migration files
- Boundaries:
  - Do not recalculate historical invoices.
- Notes:
  - Preserve the historical status from the existing archive.
- Acceptance:
  - Existing accounts default to day 1.
- Validation:
  - Run migration validation and billing model tests when available.

### T002 - Update invoice preview calculation

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 3; Compatibility Requirements
- Depends on: T001
- Status: in_progress
- Deliverable: Billing preview logic
- Suggested files / areas:
  - Invoice preview service, billing date calculation utilities
- Boundaries:
  - Do not alter posted invoice records or historical invoice dates.
- Notes:
  - Preserve the historical status from the existing archive.
- Acceptance:
  - Preview uses the account anchor day.
  - Accounts without a custom anchor continue to preview the first-day cycle.
- Validation:
  - `npm run test` focused on billing date calculation and invoice preview behavior.

### T003 - Add admin settings form

- Area: frontend
- Priority: P1
- Risk: medium
- Source: Functional Requirement 1; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Account billing settings UI
- Suggested files / areas:
  - Account settings pages/components, admin account forms
- Boundaries:
  - Do not add non-PRD billing configuration options.
- Notes:
  - Display the configured anchor day and upcoming invoice date after update.
- Acceptance:
  - Admin can set anchor day 1 to 28.
  - Admin sees the new upcoming invoice date.
- Validation:
  - `npm run test:e2e` for the admin settings flow when an e2e suite exists.

### T004 - Add anchor-day validation and update API behavior

- Area: backend
- Priority: P0
- Risk: medium
- Source: Functional Requirement 1; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Account billing settings update endpoint or server action with 1 to 28 validation
- Suggested files / areas:
  - Account billing settings API, server actions, request validation, billing domain service
- Boundaries:
  - Do not accept anchor days outside the PRD range.
- Notes:
  - Return clear validation errors for invalid days and leave the current account anchor unchanged.
- Acceptance:
  - Days 1 through 28 are accepted.
  - Invalid days outside 1 to 28 are rejected.
- Validation:
  - `npm run test` for API/domain validation cases.

### T005 - Emit audit event when anchor day changes

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirements 4, 5
- Depends on: T004
- Status: pending
- Deliverable: Audit event recording previous anchor day, new anchor day, actor, and timestamp
- Suggested files / areas:
  - Audit event service, account billing update flow, support event schema
- Boundaries:
  - Do not emit duplicate audit records for failed validation or no-op updates.
- Notes:
  - Capture the actor from the existing authenticated admin context.
- Acceptance:
  - Changing the anchor day writes an audit event with previous anchor day, new anchor day, actor, and timestamp.
- Validation:
  - `npm run test` for successful update, invalid update, and no-op update audit behavior.

### T006 - Show billing anchor history in support tools

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Functional Requirement 4; Goals
- Depends on: T005
- Status: pending
- Deliverable: Support tooling view that exposes anchor change history
- Suggested files / areas:
  - Support account tools, audit event query/display components
- Boundaries:
  - Do not expose edit controls in support tools unless they already exist for this workflow.
- Notes:
  - Show previous anchor day, new anchor day, actor, and timestamp in a support-readable format.
- Acceptance:
  - Support tools show previous anchor day, new anchor day, actor, and timestamp for anchor changes.
- Validation:
  - Manual support-tool check or component/API tests for populated and empty history states.

### T007 - Add billing-cycle regression and compatibility tests

- Area: qa
- Priority: P0
- Risk: high
- Source: Compatibility Requirements; Acceptance Criteria
- Depends on: T002, T004, T005
- Status: pending
- Deliverable: Regression test coverage for default billing behavior, history immutability, validation, and webhook idempotency
- Suggested files / areas:
  - Vitest billing suites, Playwright admin settings flow, webhook processing tests
- Boundaries:
  - Do not rely on production data or brittle date fixtures.
- Notes:
  - Include coverage for accounts without a custom anchor, invalid anchor submissions, unchanged historical invoices, and repeated webhook delivery.
- Acceptance:
  - Regression tests cover default cycle behavior.
  - Existing invoice history remains unchanged.
  - Webhook processing remains idempotent.
- Validation:
  - `npm run test`
  - `npm run test:e2e` if the admin flow is covered by Playwright.

### T008 - Add release checks for billing data compatibility

- Area: devops
- Priority: P1
- Risk: medium
- Source: Compatibility Requirements; Acceptance Criteria
- Depends on: T007
- Status: pending
- Deliverable: Release checklist or runbook for migration verification, rollback posture, and billing smoke checks
- Suggested files / areas:
  - Release documentation, deployment checklist, billing smoke-test notes
- Boundaries:
  - Do not change product behavior in this task.
- Notes:
  - Include checks for migration default day 1, unchanged historical invoices, invoice preview correctness, and idempotent webhook replay.
- Acceptance:
  - Release checklist covers migration verification and billing compatibility smoke checks.
- Validation:
  - Dry-run the checklist against a staging or seeded environment before release.

## Blocked Tasks

- None

## Coverage Map

| PRD Requirement | Covered By | Notes |
| --- | --- | --- |
| Goal: configure billing cycle anchor day per account | T001, T003, T004 | Data model, admin UI, and update validation. |
| Goal: preserve first-day cycle unless changed | T001, T002, T007, T008 | Migration default and compatibility regression coverage. |
| Goal: show upcoming invoice dates in account settings and support tools | T002, T003, T006 | Admin UI shows upcoming invoice date; support tooling exposes audit history. |
| Functional Requirement 1: admins can set an anchor day from 1 to 28 | T003, T004 | UI and backend validation. |
| Functional Requirement 2: existing accounts default to day 1 after migration | T001, T007, T008 | Existing task preserved as done; tests and release checks verify behavior. |
| Functional Requirement 3: invoice preview uses account anchor day | T002, T007 | Existing in-progress task plus regression coverage. |
| Functional Requirement 4: support tools show previous anchor day, new anchor day, actor, timestamp | T005, T006 | Audit data capture and support display. |
| Functional Requirement 5: changing anchor day requires an audit event | T005, T007 | Backend event emission and tests. |
| Compatibility: existing monthly behavior unchanged without custom anchor | T002, T007, T008 | Preview logic, tests, and release checks. |
| Compatibility: historical invoices must not be recalculated | T001, T002, T007, T008 | Boundaries plus regression/release verification. |
| Compatibility: webhook processing remains idempotent | T007, T008 | Explicit regression and release smoke coverage. |
| Acceptance: migration sets existing accounts to day 1 | T001, T007, T008 | Preserved done task plus verification. |
| Acceptance: admin can update anchor day and see upcoming invoice date | T003, T004 | UI, update behavior, and preview display. |
| Acceptance: invalid days outside 1 to 28 are rejected | T004, T007 | Backend validation and tests. |
| Acceptance: existing invoice history remains unchanged | T007, T008 | Regression and release verification. |
| Acceptance: regression tests cover default cycle behavior | T007 | Dedicated QA task. |

## Unmapped PRD Items

- None

## Derived Technical Enablement

- T007: Dedicated regression coverage is required to verify compatibility requirements and billing-critical edge cases.
- T008: Release checks are required because the PRD changes persisted account data and billing behavior.

## Open Questions and Assumptions

- Assumption: The existing project uses the `npm run test`, `npm run test:e2e`, and `npm run lint` commands declared in package.json for validation.
- Assumption: Support tools already have an account-level surface where audit history can be displayed.
- Open questions: None blocking.

## Change Log

- 2026-04-20 Created initial task archive from PRD.
- 2026-04-24 Updated existing archive without renumbering T001-T003 or changing historical statuses; added T004-T008 to cover validation, audit events, support tooling, regression coverage, and release compatibility checks from the PRD.

## Archive Record

- Created by: PRD Task Archiver
- Archive purpose: updated implementation task breakdown from existing PRD and existing task archive
- Follow-up: Continue T002, then sequence T004 and T005 before support history, QA regression, and release checks.
