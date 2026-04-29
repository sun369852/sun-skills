已基于 `product-delivery-skill-chain/evals/files/chain-demo/specs/invoice/prd.md` 完成快速规划。由于本次 eval 只要求保存 `final_response.md`，以下把技术设计、审核标准、任务草案和整理后的正式 `tasks.md` 内容集中在本响应中。

## Assumptions

- 现有系统已经有发票查询、发票详情、邮件发送能力和财务操作员权限体系。
- “用户无新前端入口”理解为普通用户端不新增入口；财务操作员后台可以在现有发票详情或操作区增加重发能力。
- 每日重发次数限制仍是 open question，当前任务不实现限制，只预留后续规则入口。

## Technical Design

### Entry Point

- 在财务后台的发票详情或发票列表操作区增加“重发邮件”操作。
- 仅当发票状态为 `issued` 时展示或允许执行。
- 操作员可输入或修改收件邮箱后提交。

### API

- `POST /admin/invoices/{invoiceId}/resend-email`
- Request:

```json
{
  "recipientEmail": "finance-target@example.com"
}
```

- Success response:

```json
{
  "success": true,
  "historyId": "resend_history_id",
  "sentAt": "2026-04-29T10:00:00Z"
}
```

- Failure response:

```json
{
  "success": false,
  "errorCode": "EMAIL_SEND_FAILED",
  "message": "Invoice email resend failed."
}
```

### Backend Flow

1. 校验当前操作员有财务发票操作权限。
2. 查询发票并校验状态必须为 `issued`。
3. 校验 `recipientEmail` 格式。
4. 调用既有邮件发送能力，使用原发票数据生成邮件。
5. 无论发送成功或失败，都追加重发历史，记录操作员、收件邮箱、时间、结果和失败原因。
6. 不修改发票号、金额、抬头、税号、开票状态等不可变字段。

### Data Changes

新增或复用发票操作日志表；推荐单独增加发票重发历史表：

```text
invoice_resend_history
- id
- invoice_id
- operator_id
- recipient_email
- result: success / failed
- failure_reason
- created_at
```

### UI

- 财务后台展示发票重发历史。
- 非 `issued` 发票不允许重发，按钮禁用或接口拒绝。
- 发送失败时向操作员展示错误，并允许再次提交。

## Audit Standards

- 只有 `issued` 状态发票可以重发。
- 非 `issued` 发票调用重发接口必须被拒绝。
- 重发成功后必须追加历史记录，包含操作员、收件邮箱、时间和结果。
- 重发失败不得改变发票状态，也必须让操作员看到失败结果。
- 重发操作不得修改发票号、金额、抬头、税号、开票状态。
- 财务操作员可以看到重发历史。
- 普通用户端不得新增重发入口。
- 邮箱格式错误应被拦截，不触发发送。
- 每日重发次数限制是未决问题，不应在本轮默认实现。

## Draft Tasks

- Add resend email API for issued invoices.
- Add recipient email validation.
- Add resend history persistence.
- Reuse existing invoice email sender.
- Add finance operator UI action.
- Show resend history in finance UI.
- Add tests for issued, non-issued, failure, immutable invoice fields.

## Reconciliation

- 技术设计要求无论成功失败都记录历史，因此任务中补充“失败历史记录”。
- 审核标准要求普通用户端不新增入口，因此任务中限定 UI 只改财务后台。
- PRD 未确认每日限制，因此正式任务只记录 open question，不实现限流。
- 发票不可变字段是核心验收项，因此正式任务中加入回归测试。

## Formal tasks.md

```markdown
# Invoice Resend Tasks

## Open Questions

- Whether daily resend attempts should be limited.

## Tasks

### T1. Add invoice resend history storage

- Create or extend storage for invoice resend history.
- Record invoice id, operator id, recipient email, timestamp, resend result, and failure reason.
- Do not store changes to invoice number, amount, title, tax number, or issue status.

### T2. Add resend email backend API

- Add `POST /admin/invoices/{invoiceId}/resend-email`.
- Require finance operator permission.
- Accept editable `recipientEmail`.
- Reject invalid email format.
- Reject invoices whose status is not `issued`.

### T3. Integrate existing invoice email sending

- Reuse existing issued invoice data and email template.
- Send the invoice email to the provided recipient email.
- Keep invoice number, amount, title, tax number, and issue status unchanged.

### T4. Record resend result for success and failure

- Append resend history when sending succeeds.
- Append resend history when sending fails.
- Preserve invoice status on failure.
- Return an operator-visible failure message when sending fails.

### T5. Add finance operator UI action

- Add resend action only in finance operator invoice management UI.
- Do not add any user-facing resend entry.
- Allow operator to edit recipient email before submitting.
- Disable or block resend for non-issued invoices.

### T6. Show resend history to finance operators

- Display resend timestamp, operator, recipient email, result, and failure reason when available.
- Make the history visible from invoice detail or the existing finance invoice workflow.

### T7. Add automated tests

- Test successful resend for an `issued` invoice sends email and records history.
- Test non-issued invoice resend is rejected.
- Test resend failure does not change invoice status.
- Test invoice number, amount, title, tax number, and issue status remain unchanged.
- Test invalid recipient email is rejected.
- Test resend history is visible to finance operators.
- Test no user-facing resend entry is added.
```
