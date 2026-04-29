# Technical Design Summary: Member Renewal

## Source

- PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\docs\member-renewal-prd.md`
- Status: Draft summary generated for iteration-2 eval.

## Design Assumptions

- Membership access is determined by a membership end date.
- Monthly and yearly renewal packages already have or can reuse existing package/pricing configuration.
- Payment success is delivered through the existing payment success flow or webhook.
- Reminder messaging channel is not implemented in this planning pass because the PRD keeps it as an open question.

## Core Flow

1. Member center reads the current membership end date.
2. Renewal entry appears when the member is expired or expires within 14 days.
3. Member selects a monthly or yearly renewal package.
4. System creates a renewal order with package, paid amount, old end date, and pending payment status.
5. On payment success, the system calculates the new membership end date:
   - active member: `new_end_date = current_end_date + package_duration`
   - expired member: `new_end_date = payment_success_time + package_duration`
6. Failed payments leave the membership end date unchanged.
7. Existing paid-course access checks continue to use the updated membership end date.
8. Existing order and invoice history remains unchanged.

## Data Notes

- Renewal order should persist: member id, package id/type, paid amount, old end date, new end date, payment status, payment time, created time.
- Membership update should be idempotent for repeated payment success notifications.
- Historical order and invoice rows should not be mutated; renewal should create new records or append renewal-specific order metadata.

## API / Service Notes

- Query renewal eligibility and available packages for the member center.
- Create renewal order from selected package.
- Handle payment success and failure through existing payment integration.
- Reuse existing admin member order report, adding renewal metadata only if the existing report cannot display it.

## Verification Focus

- Eligibility window: expired and expires within 14 days.
- Date extension logic for active and expired members.
- Failed payment does not mutate membership.
- Renewal order record contains required fields.
- Paid-course access reflects the new end date after successful renewal.
- Payment callback idempotency.

