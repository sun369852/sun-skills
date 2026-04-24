# Refund Approval Technical Design

## Context

This is an incremental change to the existing refund app. The PRD requires manager approval before high-value refunds are issued.

Current implementation:

- `src/api/refunds.ts` defines `RefundStatus` as `draft | processing | completed | failed`.
- `createRefund` immediately returns a refund with `status: "processing"`.
- `src/pages/refunds.tsx` only presents generic refund history and processing status.

The existing behavior is compatible for refunds under 100 USD, but refunds at or above 100 USD currently bypass the required approval step.

## Goals

- Enforce manager approval for refunds with `amountCents >= 10000`.
- Keep the existing immediate processing path for refunds under 100 USD.
- Add reason and evidence capture for support agents.
- Add manager approval and rejection actions with comments.
- Audit approval and rejection actions.
- Show approval status in existing refund history.

## Non-Goals

- Replacing the existing refund processor.
- Changing completed or failed refund processing semantics.
- Building a new evidence file storage service. The refund app will store references to evidence that has already been uploaded.

## Reviewer Compatibility Discussion

### FE Reviewer Notes

- The page currently has no structured list, status renderer, approval queue, action controls, or evidence display. The UI should add these in a way that preserves the existing refund history entry point.
- New statuses must not be collapsed into `processing`; otherwise agents and managers cannot distinguish `pending_approval`, `approved`, and `rejected`.
- The existing `RefundsPage` can remain the top-level route, but it should add role-aware views:
  - Support agents see create-request fields for amount, order, reason, and evidence links.
  - Managers see pending approval rows with approve/reject actions and comment entry.
  - Finance operators see history with approval status and audit metadata.
- Existing history rows need a fallback display for legacy refunds that do not have approval metadata.

### BE Reviewer Notes

- The server/API layer must enforce the 100 USD threshold. FE checks are useful for guidance but cannot be the source of truth.
- The current `createRefund` behavior immediately enters `processing`; it must branch by amount:
  - Under 100 USD: preserve immediate processor handoff.
  - At or above 100 USD: create `pending_approval` and do not invoke the processor.
- Approval/rejection and audit write should be atomic. A manager action must not update refund status without an audit event.
- Approval must be idempotent or safely reject repeated actions when a request is no longer `pending_approval`.

### Resolution

FE and BE agree to extend the existing refund model rather than create a separate approval-only domain object. Approval fields will live on the refund request, and a separate audit event collection/table will record decisions. This keeps history and finance audit screens compatible with existing refund records while adding strict server-side gating before the processor.

## Data Model

Extend `RefundStatus` to:

```ts
type RefundStatus =
  | "draft"
  | "pending_approval"
  | "approved"
  | "rejected"
  | "processing"
  | "completed"
  | "failed";
```

Extend `Refund` with:

```ts
interface Refund {
  id: string;
  orderId: string;
  customerId?: string;
  customerName?: string;
  amountCents: number;
  currency: "USD";
  status: RefundStatus;
  reason: string;
  evidenceUrls: string[];
  approvalRequired: boolean;
  approvalComment?: string;
  approvedBy?: string;
  approvedAt?: string;
  rejectedBy?: string;
  rejectedAt?: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}
```

Add audit records:

```ts
interface RefundApprovalAuditEvent {
  id: string;
  refundId: string;
  action: "submitted" | "approved" | "rejected";
  actorId: string;
  actorRole: "support_agent" | "support_manager";
  comment?: string;
  createdAt: string;
}
```

Legacy refunds without approval fields should be read as:

- `approvalRequired: false` when `amountCents < 10000`.
- `approvalRequired: true` plus `approvalComment: "Legacy refund before approval workflow"` when `amountCents >= 10000` and the refund is already `processing`, `completed`, or `failed`.

This avoids hiding historical data while making the absence of approval metadata explicit.

## API Design

### Create Refund

`POST /refunds`

Input:

```ts
{
  orderId: string;
  amountCents: number;
  reason: string;
  evidenceUrls?: string[];
}
```

Behavior:

- Validate `amountCents > 0`, `orderId`, and `reason`.
- For `amountCents < 10000`, create the refund with `status: "processing"` and invoke the existing refund processor.
- For `amountCents >= 10000`, create the refund with `status: "pending_approval"` and write a `submitted` audit event.
- Return the created refund.

### List Refunds

`GET /refunds?status=&approvalRequired=`

Returns existing history plus new approval fields. This supports the existing history page and manager queue without a breaking route change.

### List Pending Approvals

`GET /refunds/approvals/pending`

Returns only `pending_approval` refunds. Each item includes amount, customer, order, reason, evidence, createdBy, and createdAt.

### Approve Refund

`POST /refunds/:id/approve`

Input:

```ts
{
  comment?: string;
}
```

Behavior:

- Require support manager authorization.
- Require current status to be `pending_approval`.
- In one transaction, set status to `approved`, persist manager/comment metadata, and create an `approved` audit event.
- After the transaction succeeds, enqueue or invoke the existing refund processor, which moves the refund to `processing`.

### Reject Refund

`POST /refunds/:id/reject`

Input:

```ts
{
  comment: string;
}
```

Behavior:

- Require support manager authorization.
- Require current status to be `pending_approval`.
- In one transaction, set status to `rejected`, persist manager/comment metadata, and create a `rejected` audit event.
- Notify the support agent after the transaction succeeds.

## Frontend Design

Update `RefundsPage` to show three role-aware sections:

- Request creation: order ID, amount, reason, evidence URLs, and submit action.
- Pending approvals: manager-only list with amount, customer, order, reason, evidence, approve, reject, and comment controls.
- Refund history: all users can see status, approval required, decision, decision comment, and processor status.

Status display mapping:

- `draft`: Draft
- `pending_approval`: Pending approval
- `approved`: Approved
- `rejected`: Rejected
- `processing`: Processing
- `completed`: Completed
- `failed`: Failed

The UI should treat unknown statuses as visible text instead of silently mapping them to `processing`.

## Processor Integration

The existing refund processor remains responsible for `processing -> completed | failed`.

New gate:

- `createRefund` calls the processor only when approval is not required.
- `approveRefund` calls or enqueues the processor after the approval transaction commits.
- Direct processor entry points must check that either `approvalRequired === false` or `status === "approved"` before processing.

## Notifications

- On high-value submission: optional manager notification for pending approval queue.
- On rejection: notify the support agent with manager comment.
- On processor failure after approval: use the existing failed refund notification path if one exists.

## Authorization

- Support agent: create refund requests and view own/history records.
- Support manager: view pending approvals, approve, reject, and comment.
- Finance operator: view history, approval status, and audit metadata.

Authorization must be enforced by API endpoints, not only by hidden FE controls.

## Migration Plan

1. Add new status values and nullable approval fields.
2. Add audit event storage.
3. Backfill or read-map legacy records using the compatibility rules above.
4. Deploy BE support for new fields while keeping under-100 refund behavior unchanged.
5. Deploy FE status/history changes.
6. Enable manager approval actions for high-value refunds.

## Test Plan

- Unit: `createRefund` returns `processing` and invokes processor for `amountCents < 10000`.
- Unit: `createRefund` returns `pending_approval` and does not invoke processor for `amountCents >= 10000`.
- Unit: approval from `pending_approval` writes audit event and triggers processor.
- Unit: rejection from `pending_approval` writes audit event and does not trigger processor.
- Unit: approve/reject from non-pending statuses fails safely.
- API: non-manager cannot approve or reject.
- FE: pending approvals list renders amount, customer, order, reason, and evidence.
- FE: history renders all seven statuses and legacy approval fallback text.

## Risks and Open Questions

- Evidence storage ownership is not defined in the PRD. This design assumes the refund app stores evidence URLs, not binary uploads.
- The PRD names USD only. Multi-currency support should be a separate requirement.
- Notification delivery mechanism is not visible in the fixture. Implementation should use the existing project notification pattern if present.
- The fixture does not show persistence or routing infrastructure, so endpoint and storage names are conceptual and should be adapted to the real app framework.
