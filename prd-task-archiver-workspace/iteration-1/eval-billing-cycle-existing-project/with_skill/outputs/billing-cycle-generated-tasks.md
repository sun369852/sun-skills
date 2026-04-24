# Billing Cycle Task Breakdown

## Source

- PRD: D:/sun-skills/prd-task-archiver/evals/files/sample-project/docs/prd/billing-cycle-prd.md
- Generated: 2026-04-24
- Requirement mode: Existing project iteration
- Project context reviewed: D:/sun-skills/prd-task-archiver/evals/files/sample-project/package.json; D:/sun-skills/prd-task-archiver/evals/files/sample-project/docs/tasks/billing-cycle-tasks.md

## Summary

- Goal: Allow account-specific monthly billing cycle anchor days while preserving existing first-day billing behavior and historical invoice records.
- Delivery strategy: Land the data contract and migration first, then update billing calculations, admin/support surfaces, audit behavior, and compatibility-focused verification before rollout.
- Key risks / open questions: Highest risk is changing invoice preview or renewal behavior in a way that recalculates historical invoices or breaks idempotent webhook processing. Exact route, schema, and service paths must be discovered because the sample project only exposes package metadata and docs.

## Task Graph

| ID | Task | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T001 | Confirm billing anchor data contract and touched modules | product | P0 | medium | - | pending |
| T002 | Add account billing anchor field and migration default | backend | P0 | high | T001 | pending |
| T003 | Implement anchor-day validation and admin update API | backend | P0 | medium | T002 | pending |
| T004 | Preserve monthly billing compatibility and invoice history | backend | P0 | high | T002 | pending |
| T005 | Update invoice preview to use account anchor day | backend | P0 | high | T002, T004 | pending |
| T006 | Emit audit event for anchor-day changes | backend | P0 | medium | T003 | pending |
| T007 | Add admin account settings UI for anchor day and upcoming invoice date | frontend | P1 | medium | T003, T005 | pending |
| T008 | Add support-tool change history display | fullstack | P1 | medium | T006 | pending |
| T009 | Add migration, compatibility, and webhook regression tests | qa | P0 | high | T002, T004, T005, T006 | pending |
| T010 | Add admin UI and API validation tests | qa | P1 | medium | T003, T007 | pending |
| T011 | Prepare rollout, rollback, and release smoke checklist | devops | P1 | medium | T009, T010 | pending |
| T012 | Update operational documentation for billing anchor support | docs | P2 | low | T007, T008, T011 | pending |

## Ready Tasks

Tasks in this section can begin once their listed dependencies are satisfied.

### T001 - Confirm billing anchor data contract and touched modules

- Area: product
- Priority: P0
- Risk: medium
- Source: Background; Goals; Functional Requirements 1-5; Compatibility Requirements
- Depends on: -
- Status: pending
- Deliverable: Short implementation contract naming the account field, accepted value range, API shape, affected billing preview path, admin route, support route, audit event name, and webhook compatibility touchpoints.
- Suggested files / areas:
  - D:/sun-skills/prd-task-archiver/evals/files/sample-project/package.json
  - Account model/schema, billing preview service, admin account settings route, support tools route, audit event writer, webhook processing path
- Boundaries:
  - Do not change billing semantics beyond monthly anchor day 1 to 28.
  - Do not introduce new billing frequencies or invoice recalculation behavior.
- Notes:
  - The project metadata indicates a Next.js app with Prisma, Vitest, and Playwright. Discover exact paths before implementation.
  - Keep the default anchor value named and handled consistently across model, API, UI, and tests.
- Acceptance:
  - Implementation workers can identify the account field, API contract, audit payload, and verification targets without rereading the full PRD.
- Validation:
  - Review contract against all PRD functional, compatibility, and acceptance criteria.

### T002 - Add account billing anchor field and migration default

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirements 1, 2; Acceptance Criteria "Migration sets all existing accounts to anchor day 1"
- Depends on: T001
- Status: pending
- Deliverable: Account persistence change and migration/backfill that sets every existing account to billing anchor day 1.
- Suggested files / areas:
  - Prisma schema and migrations
  - Account model accessors or repositories
  - Existing account fixtures or factories
- Boundaries:
  - Do not mutate invoices, invoice line items, or historical billing records.
  - Do not make the field nullable if the chosen contract requires a default.
- Notes:
  - Enforce valid stored values from 1 to 28, either via schema constraints where supported or application validation.
  - Include an explicit default of day 1 for newly created accounts unless the admin changes it later.
- Acceptance:
  - Existing accounts have anchor day 1 after migration.
  - Newly created accounts without a custom setting retain first-day monthly behavior.
- Validation:
  - Run `npm run test` after tests exist.
  - Verify migration applies cleanly and can be rolled back in the local migration workflow.

### T003 - Implement anchor-day validation and admin update API

- Area: backend
- Priority: P0
- Risk: medium
- Source: Functional Requirement 1; Acceptance Criteria "Invalid days outside 1 to 28 are rejected"
- Depends on: T002
- Status: pending
- Deliverable: Admin-only update endpoint or server action for changing an account billing anchor day.
- Suggested files / areas:
  - Admin account settings API route or server action
  - Account service
  - Permission middleware
- Boundaries:
  - Do not allow non-admin roles to update anchor day.
  - Do not accept days outside 1 to 28 or silently coerce invalid values.
- Notes:
  - Return validation errors that the admin UI can display.
  - Preserve current account settings behavior for unrelated fields.
- Acceptance:
  - Admin can set values 1 through 28.
  - Values below 1, above 28, missing, non-integer, or malformed are rejected without changing the stored anchor.
- Validation:
  - Run `npm run test` for API and domain validation coverage.

### T004 - Preserve monthly billing compatibility and invoice history

- Area: backend
- Priority: P0
- Risk: high
- Source: Compatibility Requirements "Existing monthly billing behavior must remain unchanged"; "Historical invoices must not be recalculated"
- Depends on: T002
- Status: pending
- Deliverable: Billing-domain compatibility update that isolates anchor-day behavior to future invoice preview/renewal calculations only.
- Suggested files / areas:
  - Billing cycle calculation service
  - Invoice history reads
  - Subscription renewal logic
  - Webhook processing logic
- Boundaries:
  - Do not rewrite historical invoice dates.
  - Do not re-run old invoice generation or backfill invoice records.
- Notes:
  - Treat day 1 as behaviorally equivalent to the pre-existing monthly first-day cycle.
  - If webhook code reads account billing data, keep event handling idempotent across repeated deliveries.
- Acceptance:
  - Accounts with anchor day 1 produce the same monthly billing dates as before.
  - Existing invoice history remains unchanged after migration and anchor updates.
- Validation:
  - Add focused regression tests in T009 and run `npm run test`.

### T005 - Update invoice preview to use account anchor day

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 3; Goal "Show upcoming invoice dates in account settings and support tools"; Acceptance Criteria "Admin can update the anchor day and see the new upcoming invoice date"
- Depends on: T002, T004
- Status: pending
- Deliverable: Invoice preview calculation that uses each account's configured anchor day for future upcoming invoice dates.
- Suggested files / areas:
  - Invoice preview service/API
  - Billing date calculation utilities
  - Account settings data loader
  - Support tools data loader
- Boundaries:
  - Do not use the anchor day to recalculate historical invoice records.
  - Do not change webhook side effects while updating preview logic.
- Notes:
  - Cover month transitions explicitly, including anchor day 28.
  - Anchor values are capped at 28, so no end-of-month overflow behavior should be invented.
- Acceptance:
  - Invoice preview returns upcoming invoice dates based on the account anchor day.
  - Accounts with default day 1 still preview the original first-day cycle.
- Validation:
  - Run `npm run test` with billing date calculation cases.

### T006 - Emit audit event for anchor-day changes

- Area: backend
- Priority: P0
- Risk: medium
- Source: Functional Requirements 4, 5
- Depends on: T003
- Status: pending
- Deliverable: Audit event emitted whenever an admin changes the billing anchor day, including previous anchor day, new anchor day, actor, and timestamp.
- Suggested files / areas:
  - Audit event service
  - Admin billing anchor update handler
  - Support history query source
- Boundaries:
  - Do not emit an audit event for rejected validation attempts unless existing audit policy requires it.
  - Do not expose unrelated account audit data in support tools.
- Notes:
  - Decide whether no-op updates from day N to day N should be rejected or ignored; record the chosen behavior in T001.
- Acceptance:
  - Successful anchor changes create one audit event with previous value, new value, actor, and timestamp.
  - Support tools can query the audit data needed by T008.
- Validation:
  - Run `npm run test` with audit-event assertions.

### T007 - Add admin account settings UI for anchor day and upcoming invoice date

- Area: frontend
- Priority: P1
- Risk: medium
- Source: Goals "Allow admins to configure"; "Show upcoming invoice dates in account settings"; Acceptance Criteria "Admin can update the anchor day and see the new upcoming invoice date"
- Depends on: T003, T005
- Status: pending
- Deliverable: Admin account settings experience for viewing and updating billing anchor day and seeing the updated upcoming invoice date.
- Suggested files / areas:
  - Admin account settings page/components
  - Form validation components
  - Account settings data loading and mutation path
- Boundaries:
  - Do not expose edit controls to non-admin roles.
  - Do not redesign unrelated account settings sections.
- Notes:
  - Use a numeric input or constrained selector for days 1 to 28.
  - Show server validation errors for invalid submissions.
- Acceptance:
  - Admin sees current anchor day and upcoming invoice date.
  - After a successful update, the UI reflects the new anchor day and new upcoming invoice date.
  - Invalid days outside 1 to 28 are rejected and communicated without persisting.
- Validation:
  - Run `npm run test:e2e` for the admin update flow after Playwright coverage is added.

### T008 - Add support-tool change history display

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Goal "Show upcoming invoice dates in account settings and support tools"; Functional Requirement 4
- Depends on: T006
- Status: pending
- Deliverable: Support tools display for billing anchor history showing previous anchor day, new anchor day, actor, and timestamp.
- Suggested files / areas:
  - Support account detail page/components
  - Support data loader/API
  - Audit event query/filter code
- Boundaries:
  - Do not allow support users to modify the anchor day unless existing permissions already allow it.
  - Do not show unrelated audit events in the billing anchor history section.
- Notes:
  - Confirm support role visibility in T001 before implementation.
  - Use existing timestamp formatting conventions if present.
- Acceptance:
  - Support tools show previous anchor day, new anchor day, actor, and timestamp for anchor-day changes.
  - Support tools show the account's upcoming invoice date based on the configured anchor.
- Validation:
  - Run `npm run test` and targeted UI/e2e checks where support tooling is covered.

### T009 - Add migration, compatibility, and webhook regression tests

- Area: qa
- Priority: P0
- Risk: high
- Source: Compatibility Requirements; Acceptance Criteria "Existing invoice history remains unchanged"; "Regression tests cover default cycle behavior"
- Depends on: T002, T004, T005, T006
- Status: pending
- Deliverable: Automated test coverage for migration defaults, first-day compatibility, historical invoice preservation, and webhook idempotency.
- Suggested files / areas:
  - Vitest billing domain tests
  - Migration/backfill tests or migration verification script
  - Webhook processing tests
  - Invoice history fixtures
- Boundaries:
  - Do not rewrite production fixtures in ways that hide compatibility regressions.
  - Do not replace existing regression tests; extend them.
- Notes:
  - Include repeated webhook delivery cases to prove idempotency is unchanged.
  - Include before/after snapshots or assertions for existing invoice history records.
  - Include default day 1 cases that match legacy first-day behavior.
- Acceptance:
  - Tests fail if existing accounts do not default to day 1.
  - Tests fail if historical invoices are recalculated or mutated.
  - Tests fail if repeated webhook processing creates duplicate side effects.
  - Tests fail if default day 1 monthly behavior changes.
- Validation:
  - Run `npm run test`.

### T010 - Add admin UI and API validation tests

- Area: qa
- Priority: P1
- Risk: medium
- Source: Functional Requirement 1; Acceptance Criteria "Invalid days outside 1 to 28 are rejected"; "Admin can update the anchor day and see the new upcoming invoice date"
- Depends on: T003, T007
- Status: pending
- Deliverable: API/component/e2e coverage for valid admin updates, invalid day rejection, and upcoming invoice date refresh.
- Suggested files / areas:
  - Vitest API or server-action tests
  - Playwright admin account settings flow
  - UI form validation tests
- Boundaries:
  - Do not depend only on client-side validation; include server-side rejection checks.
- Notes:
  - Cover lower boundary 1 and upper boundary 28.
  - Cover invalid examples such as 0, 29, negative values, decimals, and non-numeric input where applicable.
- Acceptance:
  - Admin update flow passes for valid days.
  - Invalid submissions are rejected and leave the stored value unchanged.
  - Upcoming invoice date updates after a successful change.
- Validation:
  - Run `npm run test` and `npm run test:e2e`.

### T011 - Prepare rollout, rollback, and release smoke checklist

- Area: devops
- Priority: P1
- Risk: medium
- Source: Existing project iteration compatibility requirements; Acceptance Criteria migration and regression coverage
- Depends on: T009, T010
- Status: pending
- Deliverable: Release checklist covering migration execution, smoke tests, rollback plan, and monitoring points for billing preview, invoice history, and webhooks.
- Suggested files / areas:
  - Release checklist or deployment notes
  - Migration runbook
  - Billing/support smoke-test scripts or manual checklist
- Boundaries:
  - Do not perform deployment as part of this task archive.
  - Do not change production data outside the planned migration.
- Notes:
  - Include a pre-release backup or restore point expectation if that is standard for schema changes.
  - Include post-release checks for default day 1 accounts, custom anchor accounts, support history, and repeated webhook events.
- Acceptance:
  - Release operator has clear go/no-go checks and rollback steps.
  - Checklist explicitly verifies migration default, invoice preview, unchanged invoice history, and webhook idempotency.
- Validation:
  - Dry-run the checklist in a non-production environment where available.

### T012 - Update operational documentation for billing anchor support

- Area: docs
- Priority: P2
- Risk: low
- Source: Goals; Functional Requirements 1, 4, 5
- Depends on: T007, T008, T011
- Status: pending
- Deliverable: Internal documentation for admins/support explaining valid anchor days, update behavior, audit history, and compatibility constraints.
- Suggested files / areas:
  - Internal admin/support docs
  - Release notes
  - Billing operations runbook
- Boundaries:
  - Do not document unsupported anchor days beyond 1 to 28.
  - Do not imply historical invoices will be recalculated.
- Notes:
  - Emphasize that existing accounts default to day 1 and historical invoice records remain unchanged.
- Acceptance:
  - Docs explain how admins update the anchor day and how support reviews change history.
  - Docs state that valid days are 1 to 28 and historical invoices are not recalculated.
- Validation:
  - Documentation review against PRD goals and compatibility requirements.

## Blocked Tasks

- None. Exact implementation paths are unknown from the provided sample project, but T001 makes path discovery an initial ready task rather than a blocking PRD gap.

## Coverage Map

| PRD Requirement | Covered By | Notes |
| --- | --- | --- |
| Admins can set an anchor day from 1 to 28. | T001, T003, T007, T010 | Includes backend validation and UI flow. |
| Existing accounts default to day 1 after migration. | T002, T009, T011 | Includes migration and release verification. |
| Invoice preview uses the account anchor day. | T005, T007, T008, T009, T010 | Covers backend preview plus admin/support display. |
| Support tools show previous anchor day, new anchor day, actor, and timestamp. | T006, T008 | Audit event provides the support-tool source data. |
| Changing the anchor day requires an audit event. | T006, T008, T009 | Includes audit creation and query/display path. |
| Existing monthly billing behavior remains unchanged for accounts without a custom anchor. | T004, T009, T011 | Explicit compatibility and regression coverage. |
| Historical invoices must not be recalculated. | T004, T009, T011, T012 | Explicit implementation boundary and release checks. |
| Webhook processing must remain idempotent. | T004, T009, T011 | Dedicated repeated-delivery regression coverage. |
| Migration sets all existing accounts to anchor day 1. | T002, T009, T011 | Covered in schema/backfill and release smoke checks. |
| Invalid days outside 1 to 28 are rejected. | T003, T007, T010 | Covers server-side and UI/e2e validation. |
| Regression tests cover default cycle behavior. | T009 | Dedicated default first-day cycle regression tests. |

## Unmapped PRD Items

- None.

## Derived Technical Enablement

- T001: Needed to discover exact existing-project modules and lock cross-layer contracts before parallel implementation.
- T009: Dedicated QA task is required to prove migration, compatibility, invoice-history, and webhook-idempotency constraints.
- T010: Dedicated QA task is required to prove admin validation and UI behavior.
- T011: Release and rollback planning is required because the change touches persisted account data and billing behavior.
- T012: Operational docs are needed so admin/support users understand the new setting and compatibility constraints.

## Open Questions and Assumptions

- Assumption: "Admins" are the only role allowed to change billing anchor day; support tools display history but do not necessarily edit the setting.
- Assumption: The account anchor day should default to 1 for both migrated existing accounts and new accounts created without a custom setting.
- Assumption: Updating an anchor day affects future invoice preview/renewal behavior only, never historical invoice records.
- Open question: Should a no-op update from an anchor day to the same value emit an audit event, be ignored, or return a validation message?
- Open question: Which existing audit event taxonomy/name should be used for billing anchor changes?

## Change Log

- 2026-04-24 Created generated task archive from billing cycle PRD for existing-project iteration evaluation.

## Archive Record

- Created by: PRD Task Archiver
- Archive purpose: implementation task breakdown from existing PRD
- Follow-up: Use T001 to discover exact repository paths and finalize the implementation contract, then execute tasks in dependency order with compatibility and regression tests kept on the critical path.
