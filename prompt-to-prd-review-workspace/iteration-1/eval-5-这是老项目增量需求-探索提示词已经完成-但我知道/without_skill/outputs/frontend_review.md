# Frontend Review Notes

## Review Status

Not approved for final PRD landing.

## Reviewed Requirement

Add "electronic invoice email resend" capability in the finance/admin invoice module. No user-side entry should be added.

## Frontend Expectations If Approved

- Add the resend action only in the finance/admin invoice management surface.
- Show the action only for invoices that are:
  - Electronic invoices
  - Successfully issued
  - Eligible under the final resend policy
- Do not expose any new customer-facing/user-side entry.
- The resend action should make clear that invoice number, amount, title, and issued status will not change.
- The UI needs a way to confirm or display the recipient email before sending.
- If a daily resend limit is required, the UI must show disabled/blocked state and reason.
- After a successful resend, the UI should surface the latest resend time/operator/recipient if the existing admin page has an operation history area.

## Open Frontend Questions

- Where is the existing finance/admin invoice page and what component pattern does it use?
- Is the recipient email fixed to the original invoice email, editable by finance staff, or selected from known customer emails?
- What permission role can trigger resend: finance admin only, customer service, or both?
- Should resend history be shown inline, in an operation log drawer, or only in backend audit logs?
- Is a daily resend limit required, and if yes, what copy/state should the UI show when the limit is reached?

## Decision

Frontend review cannot pass because the existing project UI was not available for inspection and the resend policy remains unresolved.

