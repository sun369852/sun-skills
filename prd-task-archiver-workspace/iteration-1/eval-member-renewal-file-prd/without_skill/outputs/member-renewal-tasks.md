# Development Task Archive: Member Renewal

## Source Inputs

- PRD: `D:/sun-skills/prd-task-archiver/evals/files/sample-project/docs/prd/member-renewal-prd.md`
- Project manifest: `D:/sun-skills/prd-task-archiver/evals/files/sample-project/package.json`

## Project Context

- App stack indicated by `package.json`: Next.js, React, Prisma, Vitest, Playwright, ESLint.
- Feature scope: annual membership renewal for members and support staff, renewal history preservation, reminder emails, payment failure handling, and admin reporting.
- Explicit non-goals: monthly memberships, payment provider changes, and mutating or merging historical membership periods.

## Assumptions

- Existing membership, invoice, annual plan price, payment provider, user roles, and transactional email infrastructure already exist.
- Renewal creates a new immutable membership period linked to the previous period.
- Existing auth and role authorization patterns should be reused.
- Transactional reminder opt-out data is already available or can be read from the member profile.
- The open question about memberships expired more than 30 days should be resolved before finalizing member-facing empty states and calls to action.

## Task Plan

### 1. Domain Model and Data Access

- [ ] Audit existing Prisma schema for membership period, invoice, payment, user role, and email preference models.
- [ ] Add or update membership period fields needed to link a renewed period to its previous period.
- [ ] Add or update renewal history storage to capture actor, channel, timestamp, previous period, new period, payment status, and support internal note when applicable.
- [ ] Add indexes for renewal reporting filters: status, renewal channel, and date range.
- [ ] Create migration for schema changes.
- [ ] Add data access helpers for renewal eligibility, renewal history retrieval, and renewal report queries.

### 2. Renewal Eligibility Rules

- [ ] Implement eligibility calculation for active memberships.
- [ ] Implement eligibility calculation for memberships expired within the last 30 days.
- [ ] Block renewal when the member has an unresolved unpaid invoice.
- [ ] Return structured ineligibility reasons for account portal and support workflows.
- [ ] Ensure renewal price is read from the existing annual plan price at checkout time.
- [ ] Add unit tests for active, expired-within-30-days, expired-over-30-days, unpaid-invoice, and missing-plan-price cases.

### 3. Member Account Portal

- [ ] Add account portal UI for renewal eligibility status.
- [ ] Display expiration date, next period dates, and renewal price.
- [ ] Display clear unavailable reasons for ineligible members.
- [ ] Add self-renewal action for eligible members.
- [ ] Show recoverable payment provider errors without creating a new membership period.
- [ ] Show renewed membership period in member history after successful renewal.
- [ ] Add component and integration tests for eligible, ineligible, failed payment, and successful renewal states.

### 4. Support Renewal Workflow

- [ ] Add support-facing renewal entry point for eligible member memberships.
- [ ] Require an internal note before support users can submit a renewal.
- [ ] Submit renewal with support actor and support channel metadata.
- [ ] Record the internal note in renewal history.
- [ ] Display renewal history to support users.
- [ ] Add authorization tests to ensure only support users can renew on behalf of members.
- [ ] Add workflow tests for successful support renewal and missing-note validation.

### 5. Renewal Transaction and Payment Handling

- [ ] Create a renewal service that validates eligibility immediately before charging.
- [ ] Integrate renewal checkout with the existing payment provider.
- [ ] Create the new membership period only after payment succeeds.
- [ ] Link the new period to the previous period.
- [ ] Record payment status in renewal history.
- [ ] Ensure failed payment attempts do not create a new membership period.
- [ ] Add tests around payment success, payment failure, duplicate submission, and concurrent renewal attempts.

### 6. Reminder Email Scheduling

- [ ] Identify eligible memberships expiring in 30, 7, and 1 day.
- [ ] Exclude members who opted out of transactional reminders.
- [ ] Exclude ineligible memberships, including memberships blocked by unpaid invoices if reminder eligibility follows renewal eligibility.
- [ ] Schedule or send reminder emails using existing email infrastructure.
- [ ] Prevent duplicate reminders for the same membership period and reminder offset.
- [ ] Add tests for each reminder offset, opt-out behavior, ineligible memberships, and duplicate prevention.

### 7. Admin Configuration and Reporting

- [ ] Add admin configuration for reminder email schedule using default offsets of 30, 7, and 1 day before expiration.
- [ ] Add admin renewal report view.
- [ ] Support report filters for status, renewal channel, and date range.
- [ ] Ensure report rows include enough context to audit renewal activity.
- [ ] Add tests for report filtering by status, channel, date range, and combined filters.
- [ ] Add authorization tests to ensure report and configuration access are admin-only.

### 8. End-to-End Coverage

- [ ] Add Playwright test for successful member self-renewal and renewed period history visibility.
- [ ] Add Playwright test for ineligible member unavailable reason.
- [ ] Add Playwright test for support renewal with required internal note.
- [ ] Add Playwright test for admin report filters returning the expected rows.
- [ ] Add test fixture data for active, recently expired, expired-over-30-days, unpaid-invoice, opted-out, and renewed memberships.

### 9. Operational Readiness

- [ ] Confirm audit records preserve historical periods and never mutate old periods into a merged record.
- [ ] Confirm reminder scheduling can be safely retried.
- [ ] Confirm payment failure messaging is recoverable and actionable.
- [ ] Confirm logs or observability events exist for renewal success, renewal failure, reminder send, and report query errors.
- [ ] Run `npm run lint`, `npm run test`, and `npm run test:e2e` before release.

## Suggested Delivery Order

1. Data model, renewal history, and eligibility rules.
2. Renewal transaction service and payment success/failure behavior.
3. Member account portal renewal workflow.
4. Support renewal workflow and history display.
5. Reminder email scheduler and admin reminder configuration.
6. Admin renewal report and filters.
7. End-to-end coverage and release checks.

## Requirement Traceability

| Requirement | Covered By |
| --- | --- |
| Member renewal eligibility, expiration, next dates, price | Tasks 2, 3 |
| Active or expired-within-30-days eligibility | Tasks 2, 3, 8 |
| Support renewal with internal note | Tasks 4, 8 |
| New linked membership period | Tasks 1, 5, 9 |
| Reminder emails at 30, 7, and 1 day | Tasks 6, 7 |
| Recoverable payment failure messages | Tasks 3, 5 |
| Admin report filters | Tasks 7, 8 |
| Annual price at checkout | Tasks 2, 5 |
| Unpaid invoice renewal block | Tasks 2, 6 |
| Renewal history audit fields | Tasks 1, 4, 5, 9 |
| Transactional reminder opt-out | Tasks 6 |

## Open Product Decision

- Decide whether memberships expired more than 30 days should direct members to repurchase or to support. This affects account portal messaging and any call to action shown to ineligible members.
