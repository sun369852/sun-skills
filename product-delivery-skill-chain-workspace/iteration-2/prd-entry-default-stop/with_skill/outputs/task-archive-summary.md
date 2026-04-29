# Task Archive Summary: Member Renewal

## Source

- PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\docs\member-renewal-prd.md`
- Technical design summary: `technical-design-summary.md`
- Audit standards summary: `audit-standards-summary.md`
- Status: Reconciled draft task archive for iteration-2 eval.

## Ready Tasks

1. Model renewal packages and renewal order fields.
   - Include package type, paid amount, old end date, new end date, payment status, and payment time.
   - Preserve existing order and invoice history.

2. Implement renewal eligibility query.
   - Return current membership state, end date, renewal eligibility, and monthly/yearly package options.
   - Eligibility covers expired memberships and memberships expiring within 14 days.

3. Implement renewal order creation.
   - Allow authenticated members to create their own renewal orders.
   - Store old end date at order creation.
   - Do not mutate membership until payment success.

4. Implement payment success and failure handling.
   - On success, extend from current end date for active members.
   - On success, start from payment success time for expired members.
   - On failure, leave membership end date unchanged.
   - Make success handling idempotent.

5. Update member center renewal UI.
   - Show renewal entry only when eligible.
   - Support monthly and yearly package selection.
   - Surface payment result state using existing patterns.

6. Ensure paid-course access uses renewed membership end date.
   - Verify existing access checks read the updated membership end date.
   - Add regression coverage for active and expired renewal.

7. Update admin order report coverage.
   - Ensure operations admin can view renewal records in existing member order reports.
   - Include package, paid amount, old end date, and new end date.

8. Add verification coverage.
   - Unit tests for date calculation.
   - Service tests for payment success/failure and idempotency.
   - UI or route tests for member center renewal entry.

## Blocked / Deferred

- Reminder messaging channel is unresolved in the PRD. Do not implement email, SMS, or in-app reminder messaging until the product decision is confirmed.

## Implementation Gate

- Coding should not start until the user confirms implementation.
- Suggested next skill after confirmation: `tdd-task-implementation-orchestrator`.

