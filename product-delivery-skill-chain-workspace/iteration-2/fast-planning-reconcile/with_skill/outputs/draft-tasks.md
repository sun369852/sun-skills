# Draft Tasks: Invoice Resend

Status: draft, pending technical design confirmation.

Source PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\invoice\prd.md`

## Draft Task List

1. Add finance-operator resend API endpoint for issued invoices.
2. Add recipient email validation for resend requests.
3. Integrate resend endpoint with existing invoice email sending path.
4. Add append-only resend history persistence.
5. Show resend action and editable recipient email in internal finance invoice UI.
6. Show resend history to finance operators.
7. Surface resend failure and allow retry without changing invoice status.
8. Add tests for eligibility, immutability, history, permission, and failure behavior.

## Draft Assumptions

- No daily resend limit will be implemented until the open PRD question is answered.
- The resend operation reuses the existing issued invoice email content and invoice attachment/link.
- Finance operator identity is available from the existing internal auth/session context.

## Pending Reconciliation Items

- Confirm API contract and history schema from technical design.
- Add any migration/release tasks required by the selected persistence approach.
- Confirm audit evidence tasks against the audit standards.
