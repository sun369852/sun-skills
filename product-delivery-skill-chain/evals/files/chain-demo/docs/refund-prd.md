# Refund PRD

## Goal

Allow support operators to record structured refund reasons for approved refunds.

## Scope

- Operators choose one refund reason when approving a refund.
- Supported reasons: duplicate payment, product issue, customer request, goodwill, other.
- Reason is internal-only and not shown to customers.
- Refund exports include reason and operator.

## Acceptance Criteria

- Refund approval requires a reason.
- Refund detail shows reason and operator internally.
- Export includes reason.
- Existing refund status behavior is unchanged.
