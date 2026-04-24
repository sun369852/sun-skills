# Reviewer Notes

## Source Map

### Confirmed Facts

- Feature: B 端优惠券活动配置模块，给运营使用。
- First version supports 满减券 and 折扣券.
- Configurable fields: 有效期、库存、每人领取次数、商品范围、新老用户限制。
- Claim channels: 活动页 and 站内消息.
- Expired coupons automatically become invalid.
- Full-order refunds trigger coupon qualification rollback.
- Voiding is allowed only through manual operation in the operations backend.

### Explicit Unresolved Boundaries

- 叠加规则: 未定，首版记录为待确认边界。
- 白名单发放: 未定，首版记录为待确认边界。
- 核销统计口径: 未定，首版记录为待确认边界。

### Requirement Mode

New requirement. No existing project or codebase context was supplied.

## Draft Self-Review

Before reviewer review, the draft was checked for:

- Actor, trigger, result, and failure behavior for major flows.
- Explicit first-version scope and non-goals.
- Business rules separated from narrative prose.
- Open questions labeled as non-blocking.
- Product-verifiable acceptance criteria.

## Frontend Review - Round 1

approval_status: changes_required

blocking_findings:

- The initial draft did not sufficiently specify backend list/detail surfaces, visible empty/error/permission states, and validation behavior for the operations form.
- The two user claim channels needed an explicit statement that activity page and site message share the same eligibility checks and cannot bypass per-user limits.

non_blocking_suggestions:

- Add list filtering/search/pagination expectations.
- Add user-facing feedback for common claim failures.

recommended_prd_changes:

- Add activity list requirements: fields, filters, search, sort, pagination, actions, empty and error states.
- Add form field table with required fields and validation.
- Add claim result feedback table.
- Add acceptance criteria that frontend QA can verify.

assumptions_to_make_explicit:

- Existing backend permission system can identify operations users.
- Site message is a claim entry point, not a separate issuance rule.

affected_existing_frontend_areas:

- N/A

compatibility_risks:

- None

## Backend Review - Round 1

approval_status: changes_required

blocking_findings:

- The initial draft needed clearer domain objects and state transitions for coupon activities versus user coupon qualifications.
- Refund rollback behavior needed idempotency, terminal-state handling, and rules for expired or voided coupons.
- Inventory and per-user claim limits needed concurrency and duplicate-submission rules.

non_blocking_suggestions:

- Record audit expectations for create/edit/void actions.
- Preserve event records for future redemption statistics even though first-version statistics caliber is unresolved.

recommended_prd_changes:

- Add core object table for activity/template, user coupon instance/qualification, operation logs, and system event records.
- Add activity and user coupon state transition tables.
- Add business rules for inventory, claim count, expiration, full-refund rollback, and voiding.
- Add edge cases for repeated refund notifications, duplicate claim clicks, and final-stock concurrency.

assumptions_to_make_explicit:

- Order system can emit or expose full-order refund events.
- New/old user classification exists but its exact definition still needs business confirmation.

affected_existing_backend_areas:

- N/A

compatibility_risks:

- None

## Revision Summary

- Added product-facing operations list, form validation, visible states, and claim result feedback.
- Added domain objects, state transitions, audit records, event records, idempotency, refund rollback, and inventory concurrency semantics.
- Preserved unresolved items as non-blocking open questions and post-MVP follow-ups.

## Frontend Review - Round 2

approval_status: approved

blocking_findings:

- None

non_blocking_suggestions:

- None

recommended_prd_changes:

- None

assumptions_to_make_explicit:

- None

affected_existing_frontend_areas:

- N/A

compatibility_risks:

- None

## Backend Review - Round 2

approval_status: approved

blocking_findings:

- None

non_blocking_suggestions:

- None

recommended_prd_changes:

- None

assumptions_to_make_explicit:

- None

affected_existing_backend_areas:

- N/A

compatibility_risks:

- None

## Approval Gate

- Frontend reviewer: Approved.
- Backend reviewer: Approved.
- Blocking open questions: None.
- Non-blocking open questions: recorded in final PRD.
- Save gate: Passed.
