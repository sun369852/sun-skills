# Backend Review Notes

## Review Result

Approved after PRD updates.

## Initial Concerns

1. The data model needed to store both the reason tag and the operator who selected it.
2. Historical refund records should not require backfill, so new fields must be nullable or otherwise backward compatible.
3. The export requirement needed field naming and empty-value behavior.
4. The unresolved edit-after-approval question needed a current-scope decision to avoid accidental backend mutation endpoints.
5. The permission rule needed to reuse existing after-sales audit authorization without creating a new role or permission code.

## PRD Updates Made

- Added suggested fields: `partial_refund_reason_tag`, `partial_refund_reason_operator_id`, `partial_refund_reason_operator_name`, and `partial_refund_reason_set_at`.
- Marked new fields as nullable and required only at partial refund approval time for newly approved partial refunds.
- Added export column `部分退款原因标签`; historical or non-partial records export empty.
- Clarified current version does not include post-approval modification; the question remains open for product decision.
- Added backend acceptance criteria for permission reuse, C-end API exclusion, audit-time validation, and filter behavior.

## Final Backend Position

The PRD is implementable with a backward-compatible schema migration and limited API changes. No blocker remains, assuming the actual project has existing refund audit, list, detail, and export surfaces matching the requirement.
