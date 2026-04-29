# Invoice Resend PRD

## Goal

Allow finance operators to resend an already-issued electronic invoice email without changing invoice data.

## Scope

- Finance operators can resend an email for invoices in `issued` status.
- The resend operation keeps invoice number, amount, title, tax number, and issue status unchanged.
- Operators can edit the recipient email before resending.
- The system records operator, recipient email, timestamp, and resend result.
- Users do not get a new frontend entry.

## Non-Goals

- No invoice reissue.
- No invoice cancellation.
- No user-facing resend flow.

## Business Rules

- Only `issued` invoices can be resent.
- A resend failure must not change invoice status.
- Resend history must be visible to finance operators.

## Acceptance Criteria

- Resending an issued invoice sends an email and appends resend history.
- Attempting to resend a non-issued invoice is rejected.
- Invoice immutable fields remain unchanged after resend.
- Resend failure is visible to the operator and can be retried.

## Open Questions

- Whether daily resend attempts should be limited.
