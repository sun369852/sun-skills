# Backend Review Notes

## Review Status

Not approved for final PRD landing.

## Reviewed Requirement

Allow finance/admin staff to resend email for an already successfully issued electronic invoice. Resend must not change invoice number, amount, title, or invoice status. Record operator, time, and recipient email.

## Backend Expectations If Approved

- Provide a backend action for resending an already issued electronic invoice email.
- Eligibility checks must include:
  - Invoice exists
  - Invoice type is electronic
  - Invoice status is issued successfully
  - Caller has required finance/admin permission
  - Invoice has or is provided a valid recipient email
  - Daily resend policy is satisfied if a limit is adopted
- Resend must not mutate immutable invoice fields:
  - Invoice number
  - Amount
  - Title/header
  - Issued status
  - Core invoice payload
- Resend should create an audit record containing:
  - Invoice id
  - Operator id/name
  - Operation time
  - Recipient email
  - Send result
  - Failure reason if failed
- Email sending should preferably use the existing invoice email template and delivery pipeline, not duplicate invoice issuance logic.
- The operation should be observable for support and audit purposes.

## Current-State Conflict

The old documentation says invoice emails can only be sent once, while current support operations already perform manual resends. Backend review needs the product owner or system owner to confirm which behavior is authoritative before the final PRD is landed.

## Open Backend Questions

- Should the manual support resend flow be formalized as the canonical behavior, overriding the old "send once" documentation?
- Should there be a daily resend limit? If yes, is it per invoice, per order, per customer, per recipient email, or per operator?
- Is the recipient email always the original billing email, or can finance staff enter a new email?
- Should failed resend attempts be logged the same way as successful attempts?
- Does resend need asynchronous delivery with retry, or is synchronous submission to the existing email service enough?

## Decision

Backend review cannot pass until the current-state conflict and resend-limit policy are resolved and the actual invoice service/schema can be inspected.

