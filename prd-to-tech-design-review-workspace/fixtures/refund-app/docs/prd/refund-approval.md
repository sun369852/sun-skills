# Refund Approval PRD

## Goal

Support manager approval for high-value refund requests before refunds are issued.

## Users

- Support agent: creates refund request.
- Support manager: approves or rejects high-value refunds.
- Finance operator: audits approved refunds.

## Scope

- Refunds under 100 USD can be processed immediately.
- Refunds at or above 100 USD require manager approval.
- Support agents can add reason and evidence.
- Managers can approve or reject with comments.
- Approved requests trigger the existing refund processor.
- Rejected requests notify the support agent.

## Status Lifecycle

- `draft`
- `pending_approval`
- `approved`
- `rejected`
- `processing`
- `completed`
- `failed`

## Acceptance Criteria

- High-value refund requests cannot bypass approval.
- Managers see pending approvals with amount, customer, order, reason, and evidence.
- Approval and rejection actions are audited.
- Existing refund history shows approval status.
