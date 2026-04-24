# Reviewer Notes

Subagents were not available in this execution environment. I applied the bundled frontend and backend reviewer prompts as simulated role reviews.

## Draft Readiness Gate

The requirement is coherent enough to identify scope, actors, immutable invoice fields, audit expectations, and no user-side entry. However, it is not safe to save a final PRD while the daily resend limit is undecided because that decision changes both product-facing and backend domain behavior.

## Frontend PRD Review

approval_status: changes_required

blocking_findings:
- The PRD cannot define the finance-admin resend action states until the daily resend limit is decided. If a daily limit exists, the frontend needs disabled states, limit-reached copy, retry timing, and acceptance criteria. If no limit exists, the action and failure states are different.

non_blocking_suggestions:
- Record that user-side invoice pages must not add resend entry points, notifications, or new navigation.
- Record the current-state conflict between old one-time-send documentation and current customer-service manual resend flow.
- If the admin invoice table/detail page has existing operation-log patterns, the final PRD should align the resend record display with those patterns once files are available.

recommended_prd_changes:
- Add a blocking open question: "是否限制每天重发次数？"
- Add frontend behavior notes for success, sending failure, permission denied, invoice not eligible, and limit reached if the limit is later enabled.
- Add compatibility note: no new C-side user entry.

assumptions_to_make_explicit:
- The resend action is visible only in the finance/admin backend for successfully issued electronic invoices.
- Resend does not edit invoice number, amount, title, issuing status, or the original issuing record.

affected_existing_frontend_areas:
- Inferred finance/admin invoice list or invoice detail page.
- Inferred admin operation log display, if present.
- User-side invoice pages only as "must remain unchanged."

compatibility_risks:
- No actual frontend routes/components were available for inspection.
- Old documentation says one-time email sending, so existing UI may hide or hard-disable resend-like actions.

## Backend PRD Review

approval_status: changes_required

blocking_findings:
- The daily resend limit changes backend action eligibility, idempotency/rate-limit behavior, failure responses, concurrency rules, and audit semantics. A final PRD cannot be approved without deciding whether the product baseline permits unlimited trusted-role resends, daily capped resends, or another limit model.

non_blocking_suggestions:
- Record each resend as a separate operation/audit record with operator, operation time, recipient email, target invoice ID, and delivery attempt result.
- Preserve invoice identity and issued state: resend must not create a new invoice, new invoice number, amount/title mutation, or status transition.
- Record the old-documentation versus current-manual-flow conflict and avoid treating old docs as the backend source of truth without product confirmation.
- Clarify failure handling after the limit decision: email provider failure should not change invoice status and should still leave an operation attempt record.

recommended_prd_changes:
- Add immutable invoice-field business rules.
- Add audit trail and state-change section stating "no invoice state transition on resend."
- Add current-state conflict section.
- Block final saving until the daily resend limit rule is resolved.

assumptions_to_make_explicit:
- Only already successfully issued electronic invoices are eligible.
- Paper invoices, unissued invoices, failed invoices, voided/reversed invoices, or invoices without an email recipient are not eligible unless product later expands scope.
- Finance/admin permission should reuse existing invoice/finance operation permissions unless product defines a new permission.

affected_existing_backend_areas:
- Inferred invoice domain/service.
- Inferred email notification/sending integration.
- Inferred finance/admin invoice API.
- Inferred audit/operation-log persistence.
- Inferred customer-service manual resend SOP/integration.

compatibility_risks:
- No actual backend services, schemas, migrations, permissions, or email integration files were available for inspection.
- The old one-time-send rule may exist as code-level validation; the PRD needs a product decision before asking implementation to remove, bypass, or scope that restriction.

## Review Outcome

Both simulated reviewer perspectives require changes and do not approve saving the PRD as the current product baseline.

The blocking decision needed is:

> 电子发票重发是否需要每日次数限制？如果需要，限制维度是什么：按发票、按订单、按收件邮箱、按操作人、按租户/商户，还是组合维度？

Recommended default for product decision, if the business wants the narrowest first version:

> 首版限制为同一张电子发票每天最多重发 3 次；超过限制时财务后台不可继续提交，并提示已达今日重发上限；客服特殊处理仍走现有人工流程并记录原因。

This recommendation is not applied to a final PRD because the source prompt explicitly marks the limit as undecided.

