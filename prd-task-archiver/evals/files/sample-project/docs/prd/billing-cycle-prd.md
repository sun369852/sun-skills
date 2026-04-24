# Billing Cycle PRD

## Background

The billing module currently assumes all subscriptions renew on the first day of each month. Enterprise customers need account-specific billing cycle anchors.

## Goals

- Allow admins to configure a billing cycle anchor day per account.
- Preserve existing subscriptions on the first-day cycle unless changed by an admin.
- Show upcoming invoice dates in account settings and support tools.

## Functional Requirements

1. Admins can set an anchor day from 1 to 28.
2. Existing accounts default to day 1 after migration.
3. Invoice preview uses the account anchor day.
4. Support tools show previous anchor day, new anchor day, actor, and timestamp.
5. Changing the anchor day requires an audit event.

## Compatibility Requirements

- Existing monthly billing behavior must remain unchanged for accounts without a custom anchor.
- Historical invoices must not be recalculated.
- Webhook processing must remain idempotent.

## Acceptance Criteria

- Migration sets all existing accounts to anchor day 1.
- Admin can update the anchor day and see the new upcoming invoice date.
- Invalid days outside 1 to 28 are rejected.
- Existing invoice history remains unchanged.
- Regression tests cover default cycle behavior.
