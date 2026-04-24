# Billing Cycle Task Archive

## Source

- PRD: `docs/prd/billing-cycle-prd.md`
- Project: `sample-membership-app`
- Stack signals: Next.js, React, Prisma, Vitest, Playwright
- Iteration type: Existing-project iteration

## Implementation Tasks

### 1. Data Model and Migration

- [ ] Add an account-level billing cycle anchor day field to the Prisma schema.
- [ ] Constrain the stored anchor day to valid values from 1 through 28.
- [ ] Create a migration that backfills every existing account with anchor day `1`.
- [ ] Verify the migration is additive or otherwise compatible with existing account records.
- [ ] Ensure rollback or remediation notes are available if migration validation fails in staging.
- [ ] Confirm historical invoices are not modified, re-linked, or recalculated by the migration.

### 2. Billing Domain Logic

- [ ] Update subscription renewal and invoice preview logic to resolve the billing date from the account anchor day.
- [ ] Preserve current first-day monthly billing behavior for accounts with anchor day `1`.
- [ ] Treat missing or legacy account anchor values as day `1` until all environments are migrated.
- [ ] Reject invalid anchor values outside `1` through `28` at the service/domain layer.
- [ ] Add date calculation coverage for month boundaries, shorter months, and timezone-sensitive invoice preview display.
- [ ] Confirm webhook processing remains idempotent when billing cycle data is present or updated.

### 3. Admin Configuration Experience

- [ ] Add or update the admin account settings UI to edit the billing cycle anchor day.
- [ ] Limit UI input options to days `1` through `28`.
- [ ] Show the upcoming invoice date after the anchor day is saved.
- [ ] Surface validation errors for invalid, missing, or unauthorized update attempts.
- [ ] Ensure accounts that have never been changed display the default anchor day `1`.

### 4. API and Authorization

- [ ] Add or update the account billing settings endpoint/action used by admins.
- [ ] Enforce admin-only permission checks before changing an account anchor day.
- [ ] Validate request payloads server-side before persisting changes.
- [ ] Return the new upcoming invoice date in the response or ensure the UI can refresh it reliably.
- [ ] Avoid changing public or customer-facing API behavior unless explicitly required.

### 5. Audit and Support Tools

- [ ] Emit an audit event whenever an admin changes an account billing cycle anchor day.
- [ ] Include previous anchor day, new anchor day, actor, account identifier, and timestamp in the audit event.
- [ ] Update support tooling to display billing cycle anchor change history.
- [ ] Confirm support tools show previous value, new value, actor, and timestamp in a readable order.
- [ ] Ensure repeated saves with no actual value change either do not emit misleading audit events or are explicitly recorded as no-op updates.

### 6. Compatibility and Regression Protection

- [ ] Confirm existing monthly billing behavior is unchanged for all accounts defaulted to day `1`.
- [ ] Confirm existing invoice history remains unchanged after migration and after anchor updates.
- [ ] Confirm invoice preview changes do not alter already-issued invoices.
- [ ] Confirm webhook idempotency tests still pass with account anchor day data present.
- [ ] Confirm existing account settings, billing, and support workflows continue to load migrated accounts.
- [ ] Check any billing exports, reports, or internal consumers that assume renewal on the first day of the month.

## Test Tasks

### Unit and Integration Tests

- [ ] Add Vitest coverage for valid anchor days `1`, `15`, and `28`.
- [ ] Add Vitest coverage rejecting `0`, `29`, negative values, non-numeric values, and missing values where required.
- [ ] Add billing date calculation tests for default day `1` to prove existing behavior remains unchanged.
- [ ] Add invoice preview tests proving account-specific anchor days affect upcoming invoice dates.
- [ ] Add migration test or migration verification script proving existing accounts receive anchor day `1`.
- [ ] Add tests proving historical invoices are not recalculated when an anchor day changes.
- [ ] Add tests proving webhook processing remains idempotent with unchanged, changed, and default anchor values.
- [ ] Add audit event tests proving previous value, new value, actor, and timestamp are captured.

### End-to-End Tests

- [ ] Add Playwright coverage for an admin updating an account anchor day and seeing the updated upcoming invoice date.
- [ ] Add Playwright coverage for invalid day input being rejected.
- [ ] Add Playwright or integration coverage for support tooling displaying anchor change history.
- [ ] Add regression coverage for an existing migrated account retaining first-day billing behavior.

### Verification Commands

- [ ] Run `npm run lint`.
- [ ] Run `npm run test`.
- [ ] Run `npm run test:e2e` for billing/admin/support affected flows.
- [ ] Run Prisma migration generation and application checks in a disposable or staging-like database.

## Release and Migration Tasks

- [ ] Apply the migration in a staging environment and verify all existing accounts have anchor day `1`.
- [ ] Compare pre- and post-migration invoice history counts and key invoice fields to confirm no historical recalculation.
- [ ] Verify invoice preview behavior in staging for default and customized anchor days.
- [ ] Verify admin audit logs and support tools in staging with at least one anchor day change.
- [ ] Prepare a release note for support/admin users explaining configurable billing cycle anchors.
- [ ] Monitor billing webhooks and invoice preview errors after release.

## Acceptance Mapping

- Migration sets all existing accounts to anchor day `1`: covered by Data Model and Migration, migration tests, and staging verification.
- Admin can update anchor day and see new upcoming invoice date: covered by Admin Configuration Experience, API tasks, and Playwright tests.
- Invalid days outside `1` to `28` are rejected: covered by validation, UI limits, unit tests, and e2e tests.
- Existing invoice history remains unchanged: covered by compatibility tasks, migration verification, and historical invoice tests.
- Regression tests cover default cycle behavior: covered by unit, integration, and e2e regression tasks for day `1`.

## Risks and Notes

- Billing date logic is compatibility-sensitive because the current product assumes renewal on the first day of each month.
- Migration must be carefully verified because every existing account receives a new persisted billing value.
- Historical invoice immutability is a hard requirement; implementation should separate preview/future schedule logic from issued invoice records.
- Webhook idempotency must be explicitly tested because billing state changes can accidentally introduce duplicate processing or changed replay behavior.
