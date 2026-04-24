# Member Renewal Task Breakdown

## Source

- PRD: `D:/sun-skills/prd-task-archiver/evals/files/sample-project/docs/prd/member-renewal-prd.md`
- Generated: 2026-04-24
- Requirement mode: Existing project iteration
- Project context reviewed:
  - `D:/sun-skills/prd-task-archiver/evals/files/sample-project/package.json`

## Summary

- Goal: Enable eligible member and support-assisted annual membership renewals while preserving auditable membership history and sending renewal reminders.
- Delivery strategy: Establish the domain/data contract first, then implement renewal APIs and payments, followed by member/support/admin UI, reminder jobs, reports, and verification.
- Key risks / open questions:
  - Highest sequencing risk: payment success must be atomic with creation of the new membership period so failed attempts never create audit records.
  - Open PRD question: expired memberships older than 30 days may need a distinct repurchase or support path.

## Task Graph

| ID | Task | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T001 | Define renewal domain contract and eligibility matrix | fullstack | P0 | medium | - | pending |
| T002 | Add membership period history data model and migration | backend | P0 | high | T001 | pending |
| T003 | Implement renewal eligibility and pricing service | backend | P0 | high | T001, T002 | pending |
| T004 | Implement self-service renewal API with payment failure handling | backend | P0 | high | T003 | pending |
| T005 | Implement support-assisted renewal API and internal note capture | backend | P0 | high | T003 | pending |
| T006 | Build member account renewal experience | frontend | P0 | medium | T004 | pending |
| T007 | Build support renewal and history experience | fullstack | P1 | medium | T005 | pending |
| T008 | Implement reminder scheduling and opt-out filtering | backend | P0 | high | T003 | pending |
| T009 | Build admin reminder schedule configuration | fullstack | P1 | medium | T008 | pending |
| T010 | Build admin renewal report filters | fullstack | P1 | medium | T002, T004, T005 | pending |
| T011 | Add automated test coverage for renewal rules and flows | qa | P0 | medium | T004, T005, T008, T010 | pending |
| T012 | Prepare rollout, migration verification, and support documentation | docs | P1 | medium | T002, T011 | pending |
| T013 | Decide handling for memberships expired more than 30 days | product | P1 | medium | Open PRD question | blocked |

## Ready Tasks

Tasks in this section can begin once their listed dependencies are satisfied.

### T001 - Define renewal domain contract and eligibility matrix

- Area: fullstack
- Priority: P0
- Risk: medium
- Source: Functional Requirements 1-4, Business Rules, Users and Roles
- Depends on: -
- Status: pending
- Deliverable: A documented renewal contract covering eligible states, actor roles, channels, audit fields, payment outcomes, and API/UI data needs.
- Suggested files / areas:
  - Existing membership domain modules, API route conventions, and Prisma schema locations to be discovered in the real project.
  - `package.json` confirms a Next/React, Prisma, Vitest, and Playwright stack.
- Boundaries:
  - Do not introduce monthly memberships.
  - Do not change the existing payment provider.
  - Do not collapse historical periods into one mutable record.
- Notes:
  - Define active and expired-within-30-days eligibility, unpaid invoice blocking, renewal channel values, and required history fields.
  - Make the payment provider interaction contract explicit enough for backend and frontend work to proceed in parallel.
- Acceptance:
  - The contract maps every role capability and business rule from the PRD to a concrete state, field, endpoint, or UI requirement.
- Validation:
  - Peer review the contract against the PRD before implementation tasks begin.

### T002 - Add membership period history data model and migration

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 4; Business Rules; Non-Goals
- Depends on: T001
- Status: pending
- Deliverable: Prisma schema changes and migration for immutable membership period records linked to previous periods, plus audit/history fields.
- Suggested files / areas:
  - Prisma schema and migration directories to be discovered.
  - Existing membership and invoice models.
- Boundaries:
  - Do not merge historical membership periods into a single mutable membership record.
  - Do not backfill or rewrite unrelated member data beyond what is necessary for period history compatibility.
- Notes:
  - Store previous period, new period, actor, channel, timestamp, payment status, and support internal note where applicable.
  - Include migration/backfill checks for existing annual memberships so current support-created memberships remain readable.
- Acceptance:
  - A successful renewal can create a new period linked to the previous period, and renewal history can display all required fields.
- Validation:
  - Run `npm run lint` and relevant migration/schema validation in the real project.

### T003 - Implement renewal eligibility and pricing service

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirements 1-3; Business Rules
- Depends on: T001, T002
- Status: pending
- Deliverable: Shared service for renewal eligibility, ineligibility reasons, next period dates, renewal price, unpaid invoice blocking, and actor/channel validation.
- Suggested files / areas:
  - Membership services, invoice services, annual plan pricing lookup, and role/permission helpers to be discovered.
- Boundaries:
  - Do not create a new pricing source.
  - Do not add monthly plan logic.
- Notes:
  - Price must come from the existing annual plan price at checkout time.
  - Ineligible members need machine-readable reasons for UI display and API error responses.
- Acceptance:
  - Active and expired-within-30-days memberships are eligible unless blocked by unpaid invoices; older expirations are not treated as renewable.
- Validation:
  - Add or prepare Vitest unit cases for eligibility windows, unpaid invoices, actor role rules, and pricing lookup.

### T004 - Implement self-service renewal API with payment failure handling

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirements 2, 4, 6; Acceptance Criteria
- Depends on: T003
- Status: pending
- Deliverable: Member-facing renewal endpoint/action that charges through the existing payment provider and creates the next membership period only after confirmed success.
- Suggested files / areas:
  - Next API routes or server actions, existing payment integration, membership services, and error handling utilities.
- Boundaries:
  - Do not replace or reconfigure the payment provider.
  - Do not create a membership period for failed payment attempts.
- Notes:
  - Return recoverable payment errors suitable for account portal display.
  - Consider idempotency protections so repeated submissions do not create duplicate periods.
- Acceptance:
  - A member can complete a successful self-renewal and see the new period in history; failed payment attempts leave membership history unchanged.
- Validation:
  - Vitest API/service tests for success, provider failure, unpaid invoice, ineligible status, and duplicate submission handling.

### T005 - Implement support-assisted renewal API and internal note capture

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 3; Acceptance Criteria
- Depends on: T003
- Status: pending
- Deliverable: Support-facing renewal endpoint/action that renews eligible member memberships and requires an internal note.
- Suggested files / areas:
  - Support/admin routes, permission middleware, membership services, audit/history persistence.
- Boundaries:
  - Do not allow support renewals without eligibility validation.
  - Do not expose internal notes to members unless the existing product already does so.
- Notes:
  - Store actor, support channel, timestamp, internal note, previous period, new period, and payment status in history.
- Acceptance:
  - A support user can renew for an eligible member, and the required internal note is recorded in renewal history.
- Validation:
  - API/service tests for support permission, missing note, ineligible member, payment failure, and successful renewal.

### T006 - Build member account renewal experience

- Area: frontend
- Priority: P0
- Risk: medium
- Source: Functional Requirements 1, 2, 6; Acceptance Criteria
- Depends on: T004
- Status: pending
- Deliverable: Account portal UI showing eligibility, expiration date, next period dates, renewal price, ineligibility reasons, recoverable payment errors, and updated renewal history.
- Suggested files / areas:
  - Account portal pages/components and member membership history components to be discovered.
- Boundaries:
  - Do not add monthly membership options.
  - Do not expose support-only internal notes.
- Notes:
  - Include loading, success, ineligible, and recoverable payment failure states.
  - Use backend-provided eligibility and pricing rather than duplicating business rules in the UI.
- Acceptance:
  - Eligible members can renew from the portal; ineligible members see the reason renewal is unavailable; successful renewal displays the new period in history.
- Validation:
  - Playwright coverage for successful self-renewal, ineligible state, and payment failure message.

### T007 - Build support renewal and history experience

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Users and Roles; Functional Requirement 3; Business Rules
- Depends on: T005
- Status: pending
- Deliverable: Support UI for renewing eligible member memberships on behalf of members and viewing renewal history.
- Suggested files / areas:
  - Support member detail pages, support permissions, renewal form components, and history tables to be discovered.
- Boundaries:
  - Do not grant support users admin-only reporting or reminder configuration access.
- Notes:
  - The renewal form must require an internal note before submission.
  - History should show actor, channel, timestamp, previous period, new period, and payment status.
- Acceptance:
  - Support can renew any eligible membership and confirm the internal note appears in support-visible history.
- Validation:
  - Playwright or integration coverage for support renewal success, missing note validation, and history rendering.

### T008 - Implement reminder scheduling and opt-out filtering

- Area: backend
- Priority: P0
- Risk: high
- Source: Functional Requirement 5; Business Rules; Acceptance Criteria
- Depends on: T003
- Status: pending
- Deliverable: Reminder job/scheduler logic that sends renewal reminders 30, 7, and 1 day before expiration only to eligible, non-opted-out memberships.
- Suggested files / areas:
  - Existing email service, scheduled job infrastructure, membership eligibility service, and transactional reminder preference storage.
- Boundaries:
  - Do not create marketing email flows.
  - Do not send reminders to members opted out of transactional reminders.
- Notes:
  - Ensure eligibility is evaluated at send/schedule time so unpaid invoices or status changes are respected.
  - Record enough job output for operational review if the project has logging conventions.
- Acceptance:
  - Reminder emails are scheduled only for eligible memberships at 30, 7, and 1 days before expiration, excluding opted-out members.
- Validation:
  - Vitest coverage for reminder dates, eligibility filtering, opt-out filtering, and no-send cases.

### T009 - Build admin reminder schedule configuration

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Users and Roles
- Depends on: T008
- Status: pending
- Deliverable: Admin-only configuration UI/API for the reminder email schedule.
- Suggested files / areas:
  - Admin settings routes, permission middleware, schedule configuration persistence, and reminder job configuration.
- Boundaries:
  - Do not expose reminder configuration to members or support users.
  - Do not add reminder channels beyond email.
- Notes:
  - The PRD states the default schedule is 30, 7, and 1 day; preserve those defaults unless admin configuration changes them.
- Acceptance:
  - Admin users can view and configure the reminder schedule, and the reminder scheduler uses the saved configuration.
- Validation:
  - Permission tests and UI/API tests for admin access and non-admin denial.

### T010 - Build admin renewal report filters

- Area: fullstack
- Priority: P1
- Risk: medium
- Source: Functional Requirement 7; Acceptance Criteria
- Depends on: T002, T004, T005
- Status: pending
- Deliverable: Admin renewal report filtered by status, renewal channel, and date range.
- Suggested files / areas:
  - Admin reporting pages, report APIs, membership period history queries, and filter components to be discovered.
- Boundaries:
  - Do not add analytics dimensions beyond status, channel, and date range unless already present in the existing reporting framework.
- Notes:
  - Report rows should be sourced from immutable renewal history/period data so member and support renewals are included consistently.
- Acceptance:
  - Renewal report filters return correct rows for status, renewal channel, and date range.
- Validation:
  - Unit/integration tests for report query filters and Playwright coverage for applying filters in the admin UI.

### T011 - Add automated test coverage for renewal rules and flows

- Area: qa
- Priority: P0
- Risk: medium
- Source: Acceptance Criteria; all Functional Requirements
- Depends on: T004, T005, T008, T010
- Status: pending
- Deliverable: Focused Vitest and Playwright test suites covering domain rules, API behavior, major UI flows, reminder scheduling, and report filters.
- Suggested files / areas:
  - `npm run test`
  - `npm run test:e2e`
  - Existing test fixtures and factories to be discovered.
- Boundaries:
  - Do not rely on real payment provider calls in automated tests.
- Notes:
  - Include fixture coverage for active, expired-within-30-days, expired-older-than-30-days, unpaid invoice, opted-out reminder preference, successful payment, and failed payment.
- Acceptance:
  - Tests verify every PRD acceptance criterion and fail when a failed payment creates a period, reminders include opted-out members, or report filters return incorrect rows.
- Validation:
  - Run `npm run test`, `npm run test:e2e`, and `npm run lint` in the real project environment.

### T012 - Prepare rollout, migration verification, and support documentation

- Area: docs
- Priority: P1
- Risk: medium
- Source: Background; Goals; Business Rules; Acceptance Criteria
- Depends on: T002, T011
- Status: pending
- Deliverable: Release checklist covering migration verification, existing membership compatibility, payment failure monitoring, reminder job smoke checks, and support/admin operating notes.
- Suggested files / areas:
  - Release docs, runbooks, support documentation, and migration verification scripts to be discovered.
- Boundaries:
  - Do not document unsupported monthly memberships or payment provider changes.
- Notes:
  - Include rollback considerations for migrations, reminder jobs, and payment integration behavior.
  - Include support guidance for ineligible members and the unresolved older-than-30-days path once T013 is decided.
- Acceptance:
  - Release owner can verify existing membership history remains readable, renewal jobs behave as expected, and support/admin users know the new workflow.
- Validation:
  - Manual release checklist review plus successful test/lint run records.

## Blocked Tasks

### T013 - Decide handling for memberships expired more than 30 days

- Area: product
- Priority: P1
- Risk: medium
- Source: Open Questions
- Depends on: Open PRD question
- Status: blocked
- Blocker: The PRD asks whether expired memberships older than 30 days should be directed to repurchase or support.
- Deliverable: Product decision and copy/API behavior for members whose memberships expired more than 30 days ago.
- Acceptance:
  - The account portal and support documentation have a confirmed behavior for memberships outside the renewal window.

## Coverage Map

| PRD Requirement | Covered By | Notes |
| --- | --- | --- |
| Members see renewal eligibility, expiration date, next period dates, and renewal price | T001, T003, T006 | Backend supplies authoritative values; UI displays them. |
| Members can renew only if active or expired within last 30 days | T001, T003, T004, T006, T011 | Eligibility service and API enforce the rule. |
| Support users can renew on behalf of eligible members and must provide an internal note | T001, T003, T005, T007, T011 | Includes permission and note validation. |
| Successful renewal creates a new membership period linked to previous period | T002, T004, T005, T011 | Migration and renewal APIs preserve history. |
| Reminder emails at 30, 7, and 1 days before expiration | T008, T009, T011 | Admin configuration task preserves defaults and connects scheduler. |
| Payment provider failures are shown with recoverable error messages | T004, T006, T011 | Failed payments must not create periods. |
| Admins can view renewal report filtered by status, channel, and date range | T010, T011 | Report uses renewal history data. |
| Annual price comes from existing annual plan price at checkout | T001, T003, T004, T011 | No new pricing source. |
| Unpaid invoice blocks renewal | T001, T003, T004, T011 | Eligibility and API enforcement. |
| Renewal history shows actor, channel, timestamp, previous period, new period, and payment status | T002, T006, T007, T010 | Data model plus member/support/admin views. |
| Reminder emails must not be sent to opted-out members | T008, T011 | Scheduler filters opted-out transactional reminders. |
| Non-goals: no monthly memberships, no payment provider change, no mutable merged period | T001, T002, T003, T004, T012 | Boundaries repeated in relevant implementation tasks. |
| Acceptance criteria for self-renewal, support renewal, ineligibility, failed payment, reminders, reports | T004, T005, T006, T007, T008, T010, T011 | T011 consolidates automated verification. |

## Unmapped PRD Items

- None. The open question about expired memberships older than 30 days is mapped to blocked task T013.

## Derived Technical Enablement

- T001: Needed to align domain, API, UI, payment, and audit contracts before parallel implementation.
- T002: Needed to satisfy audit/history preservation and prevent mutable period merging.
- T011: Needed to verify PRD acceptance criteria across domain, API, UI, scheduler, and reporting behavior.
- T012: Needed because this change touches production data migrations, payment behavior, reminder jobs, and support/admin workflows.

## Open Questions and Assumptions

- Open question: Should expired memberships older than 30 days be directed to repurchase or support?
- Assumption: The existing annual plan price, payment provider integration, role/permission system, and transactional reminder preference storage already exist because the PRD says not to change the payment provider and references current annual memberships.
- Assumption: The real project follows the manifest stack in `package.json`: Next/React, Prisma, Vitest, Playwright, and ESLint.
- Assumption: Admin reminder schedule configuration should preserve 30, 7, and 1 day defaults unless explicitly changed by an admin.

## Change Log

- 2026-04-24 Created initial task archive from PRD.

## Archive Record

- Created by: PRD Task Archiver
- Archive purpose: implementation task breakdown from existing PRD
- Follow-up: Resolve T013, then begin implementation with T001 before parallelizing backend, frontend, reminder, report, and QA work.
