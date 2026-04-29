# Audit Standards Summary: Invoice Resend

Source PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\invoice\prd.md`

## Audit Scope

Verify that finance operators can resend an already-issued electronic invoice email without changing invoice data, and that resend attempts are traceable and retryable.

## Hard Fail Gates

- Resend is allowed for a non-`issued` invoice.
- Resend changes invoice number, amount, title, tax number, or issue status.
- A failed resend changes invoice status.
- Resend history is missing operator, recipient email, timestamp, or result.
- A user-facing resend entry is added.

## Requirement Traceability

| Audit ID | PRD Source | Check |
| --- | --- | --- |
| `INV-RS-AUD-001` | Scope: issued invoices | Only `issued` invoices can trigger resend. |
| `INV-RS-AUD-002` | Scope: immutable invoice data | Invoice number, amount, title, tax number, and status remain unchanged after success or failure. |
| `INV-RS-AUD-003` | Scope: edit recipient | Finance operator can supply recipient email for the resend attempt. |
| `INV-RS-AUD-004` | Scope: history | Resend history records operator, recipient, timestamp, and result. |
| `INV-RS-AUD-005` | Business rule: failure | Failed resend is visible and retryable without status mutation. |
| `INV-RS-AUD-006` | Non-goal: no frontend entry | No user-facing resend flow or entry is introduced. |

## Required Evidence

- Test or screenshot proving issued invoice resend success.
- Test proving non-issued invoices are rejected.
- Before/after data evidence showing immutable invoice fields unchanged.
- Data evidence for resend history after success and failure.
- Permission evidence showing finance-only access.
- UI or route evidence showing no user-facing resend entry.

## Technical Risk Checks Added During Reconciliation

- Permission gate for finance operators is explicit, even though the PRD only names finance operators.
- Email provider failure path must append failed history and surface retry state.
- Recipient email validation must happen before provider dispatch.
- Open question about daily resend limits is marked as unresolved and non-blocking; implementation must not invent a limit.

## Blocked / Open Audit Area

- Daily resend attempt limits cannot be audited until the product owner decides whether limits are required.
