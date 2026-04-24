# Payment Refund PRD

## Goal

Customers and support staff need a safe refund flow for paid orders. Refunds must be idempotent, auditable, and compatible with payment provider failures.

## Users

- Customer: requests a refund for eligible orders.
- Support agent: creates or reviews refund requests.
- Finance manager: approves high-value refunds and audits refund history.

## Scope

- Customers can request refunds for paid orders within 30 days.
- Refunds over 500 USD require finance manager approval.
- Partial refunds are supported until the total refunded amount reaches the paid amount.
- Refund requests must be idempotent to prevent duplicate provider refunds.
- Every approve, reject, submit, provider callback, and manual override action must be audited.
- Payment provider callbacks may arrive before or after the synchronous API response.
- Users can see refund status and failure reason.

## Status Lifecycle

- `requested`
- `pending_approval`
- `approved`
- `provider_submitted`
- `succeeded`
- `failed`
- `rejected`
- `cancelled`

## Business Rules

- Refund amount must not exceed remaining refundable amount.
- Customers cannot refund orders they do not own.
- Support agents can create refunds for customers but cannot approve high-value refunds.
- Finance managers can approve or reject high-value refunds.
- Provider refund IDs must be unique.
- Duplicate client submissions must return the existing refund request.
- Failed provider refunds can be retried by support staff.

## Acceptance Criteria

- Duplicate refund submissions do not create duplicate provider refunds.
- High-value refunds cannot bypass approval.
- Audit log includes actor, action, before/after status, reason, timestamp, and correlation ID.
- Customer and support views show accurate status and failure reasons.
- Provider callback ordering does not corrupt refund status.
