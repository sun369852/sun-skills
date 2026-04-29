# Billing Cycle PRD

## Goal

Support monthly billing cycle adjustment for enterprise accounts.

## Scope

- Admins can request changing the next billing day.
- The change affects only future invoices.
- Existing paid invoices are not recalculated.
- The system records requester, old billing day, new billing day, effective date, and approval status.

## Acceptance Criteria

- Pending cycle changes are visible in billing settings.
- Approved changes apply to the next invoice only.
- Rejected changes do not affect billing.
- Audit history is preserved.
