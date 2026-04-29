# Tasks: Invoice Resend

Status: reconciled

Source PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\invoice\prd.md`

Technical design summary: `D:\sun-skills\product-delivery-skill-chain-workspace\iteration-2\fast-planning-reconcile\with_skill\outputs\technical-design-summary.md`

Audit standards summary: `D:\sun-skills\product-delivery-skill-chain-workspace\iteration-2\fast-planning-reconcile\with_skill\outputs\audit-standards-summary.md`

## Reconciliation Notes

- Draft API task was aligned to `POST /internal/invoices/{invoiceId}/resend-email`.
- Added explicit resend history persistence and migration work from technical design.
- Added permission and audit evidence tasks from audit standards.
- Product behavior remains PRD-aligned: no reissue, no cancellation, no invoice immutable-field mutation, no user-facing entry.
- Daily resend limits remain unresolved and are not implemented in this task archive.

## Ready Tasks

### T1. Add Resend History Persistence

- Area: backend / data
- Depends on: none
- Deliverable: append-only resend history table or collection with invoice, operator, recipient email, timestamp, result, and nullable failure reason.
- Acceptance checks:
  - Success and failure attempts can both be stored.
  - Existing invoice immutable fields are not modified by history creation.
  - Migration or schema update is reversible according to local project convention.

### T2. Add Finance Resend API

- Area: backend / API
- Depends on: T1
- Deliverable: `POST /internal/invoices/{invoiceId}/resend-email` or equivalent internal route.
- Acceptance checks:
  - Rejects non-`issued` invoices.
  - Validates recipient email.
  - Uses authenticated finance operator as `operator_id`.
  - Does not change invoice number, amount, title, tax number, or issue status.

### T3. Integrate Email Dispatch And Failure Recording

- Area: backend / integration
- Depends on: T1, T2
- Deliverable: resend path that uses the existing issued invoice email content and records result.
- Acceptance checks:
  - Successful send appends `sent` history.
  - Provider/system failure appends `failed` history with failure reason when available.
  - Failed resend returns a visible operator error and can be retried.

### T4. Add Internal Finance UI Action

- Area: frontend / internal UI
- Depends on: T2
- Deliverable: finance-only resend action for issued invoices with editable recipient email.
- Acceptance checks:
  - Action is visible only in internal finance invoice management.
  - Action is unavailable or rejected for non-`issued` invoices.
  - No user-facing resend entry is added.

### T5. Show Resend History To Finance Operators

- Area: frontend / backend
- Depends on: T1
- Deliverable: finance-operator-visible resend history list.
- Acceptance checks:
  - History shows operator, recipient email, timestamp, and result.
  - Failed attempts are visible.
  - Non-finance users cannot access the history.

### T6. Add Permission And Security Tests

- Area: test
- Depends on: T2, T4, T5
- Deliverable: automated permission coverage for resend action and history access.
- Acceptance checks:
  - Finance operator can resend eligible invoice.
  - Non-finance user is rejected.
  - User-facing routes or screens do not expose resend functionality.

### T7. Add Behavior And Regression Tests

- Area: test
- Depends on: T1, T2, T3
- Deliverable: unit/integration tests mapped to audit IDs.
- Acceptance checks:
  - Issued invoice resend sends email and appends history.
  - Non-issued invoice resend is rejected.
  - Immutable invoice fields remain unchanged after success and failure.
  - Failure path is visible and retryable.

### T8. Prepare Audit Evidence Notes

- Area: QA / documentation
- Depends on: T4, T5, T6, T7
- Deliverable: concise verification notes or run log entries for post-development review.
- Acceptance checks:
  - Evidence maps to `INV-RS-AUD-001` through `INV-RS-AUD-006`.
  - Daily resend limit remains marked as open product question.

## Blocked Tasks

None for implementation planning.

## Open Product Question

- Whether daily resend attempts should be limited. This is non-blocking for the current task archive because the PRD does not require a limit.

## Implementation Gate

Do not start coding until the user confirms implementation should begin.
