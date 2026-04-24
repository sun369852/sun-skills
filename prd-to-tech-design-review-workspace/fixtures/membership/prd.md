# Membership Points PRD

## Goal

Members earn points after successful orders and can view a complete points ledger.

## Scope

- Award points after an order is paid.
- Points expire after 12 months unless the campaign defines a shorter expiry.
- Admins can manually adjust points with a required reason.
- Members can view points balance and ledger entries.
- Prevent duplicate point awards for the same order.

## Business Rules

- 1 USD paid amount equals 1 point.
- Refunded order amounts reverse corresponding points.
- Manual adjustments must be audited.
- Expired points are deducted nightly.
- Ledger entries are immutable after creation.

## Acceptance Criteria

- A paid order grants points exactly once.
- A member sees current available points and historical ledger entries.
- Admin adjustment requires permission and reason.
- Expiry job records an expiry ledger entry.
