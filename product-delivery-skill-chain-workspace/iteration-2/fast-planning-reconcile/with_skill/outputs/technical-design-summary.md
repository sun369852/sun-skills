# Technical Design Summary: Invoice Resend

Source PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\invoice\prd.md`

## Scope

Add an internal finance-operator resend action for already-issued electronic invoices. The action sends the existing invoice email to a chosen recipient and records a resend history entry. It must not reissue, cancel, mutate invoice identity fields, or create a user-facing entry.

## Key Decisions

- Entry point: finance operator invoice detail or internal invoice management action.
- Eligibility: only invoices with status `issued` can be resent.
- Mutable input: recipient email for the resend attempt only.
- Immutable invoice fields: invoice number, amount, title, tax number, and issue status.
- Persistence: append-only resend history with operator, recipient email, timestamp, result, and failure reason when available.
- Failure behavior: email delivery failure returns a visible operator error and does not change invoice status.

## API Design

### Resend Invoice Email

`POST /internal/invoices/{invoiceId}/resend-email`

Request:

```json
{
  "recipientEmail": "finance-target@example.com"
}
```

Response success:

```json
{
  "invoiceId": "inv_123",
  "status": "issued",
  "resendResult": "sent",
  "historyId": "hist_456"
}
```

Response rejected:

```json
{
  "error": "INVOICE_NOT_ISSUED",
  "message": "Only issued invoices can be resent."
}
```

## Data Model

Add an append-only resend history table or collection:

| Field | Purpose |
| --- | --- |
| `id` | History record identifier |
| `invoice_id` | Source invoice |
| `operator_id` | Finance operator who triggered resend |
| `recipient_email` | Recipient used for this attempt |
| `attempted_at` | Server timestamp |
| `result` | `sent` or `failed` |
| `failure_reason` | Nullable provider/system failure detail |

No invoice core field should be updated by resend except optional non-business metadata such as `updated_at` only if existing persistence conventions require it. Prefer avoiding invoice-row mutation entirely.

## Validation And Permissions

- Require finance-operator permission for the action and resend history view.
- Validate recipient email format before calling the mail provider.
- Re-check invoice status server-side immediately before sending.
- Treat the PRD open question about daily resend limits as non-blocking; no limit is applied unless the product owner confirms one.

## UI Behavior

- No user-facing entry is added.
- Finance operators can trigger resend from existing internal invoice management.
- The operator can edit recipient email before confirming.
- Resend history is visible to finance operators.
- Failed resend attempts display an actionable retry state without changing invoice status.

## Risks

- Duplicate resend attempts may be made because the PRD does not define rate limits.
- Email provider transient failure must be distinguishable from validation rejection.
- Audit/history visibility is required even for failed attempts.

## Verification

- Unit tests for issued/non-issued eligibility, immutable invoice fields, and email validation.
- Integration tests for successful send, failed send, retry, and resend history append.
- Permission tests for finance operator access and non-operator rejection.
