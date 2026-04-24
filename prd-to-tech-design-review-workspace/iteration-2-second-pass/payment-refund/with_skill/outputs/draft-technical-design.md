# Payment Refund Technical Design Draft

## Source

- PRD: `D:\sun-skills\prd-to-tech-design-review-workspace\fixtures\payment-refund\prd.md`
- Project: no project path provided
- Generated: 2026-04-25

## Executive Summary

Implement a role-based refund flow for customers, support agents, and finance managers. The backend owns eligibility, idempotency, approval threshold enforcement, status transitions, provider callback ordering, and audit logging. The frontend treats the server as source of truth after every mutation and exposes safe status, failure, retry, and approval states.

## PRD Scope Mapping

| PRD Requirement | Technical Coverage | Notes |
| --- | --- | --- |
| Customers can request refunds for paid orders within 30 days | Eligibility API and customer refund form | Server owns final eligibility decision |
| Refunds over 500 USD require finance approval | Backend threshold gate and finance approval queue | Threshold assumed to use refund amount in order currency unless clarified |
| Partial refunds until paid amount is reached | Transactional refundable-balance check | Requires order/refund aggregate lock |
| Idempotent refund requests | Client idempotency key plus server uniqueness constraint | Duplicate returns existing refund |
| Audit all actions | `refund_audit_logs` written with every status-changing action | Includes actor, action, before/after, reason, timestamp, correlation ID |
| Provider callbacks may race API response | Outbox/provider event handling and ordered callback processing | UI re-fetches after mutation |
| Users can see status and failure reason | Customer/support/finance detail views and safe error messages | Provider internals must be mapped to display-safe reason |

Coverage estimate: 100% of concrete functional PRD requirements mapped.

## Architecture Overview

Frontend surfaces call refund APIs. Backend validates eligibility, creates/refers to a refund request idempotently, gates high-value refunds through finance approval, submits approved refunds to the provider through an outbox/job, receives provider callbacks idempotently, and records audit logs in the same transaction as status changes.

## Frontend Design

### Routes and Screens

- Customer order detail refund entry point.
- Customer refund request form with amount, reason, remaining refundable amount, and approval notice.
- Customer refund status/history view.
- Support refund list and detail, including failure reason, audit timeline, retry action, and create-refund-for-customer flow.
- Finance approval queue and approval detail.

### Component Structure

- `RefundRequestForm`
- `RefundStatusTimeline`
- `RefundHistoryTable`
- `RefundApprovalQueue`
- `RefundApprovalPanel`
- `RefundAuditTimeline`
- `RefundRetryAction`

### Client State and Data Fetching

Use server state for refund detail, order eligibility, refund lists, approval queue, and audit timeline. Mutations use pessimistic updates. After create, approve, reject, retry, or callback-visible changes, invalidate order, refund detail, refund list, approval queue, and audit queries.

### UX States and Validation

Cover loading, empty, error, success, permission-denied, stale-status, and provider-failed states. Frontend mirrors amount, reason, and eligibility validation but never treats local validation as authoritative. It sends a stable idempotency key per logical user submission.

### Accessibility and Responsive Behavior

Approval and retry actions need keyboard-accessible confirmation flows. Status and failure reason must not rely only on color. Tables should collapse into readable detail rows on mobile.

## Backend Design

### Domain Model

- `refund_requests`: `id`, `order_id`, `customer_id`, `amount`, `currency`, `status`, `reason`, `failure_reason`, `safe_failure_message`, `created_by`, `approved_by`, `provider_refund_id`, `idempotency_key`, `provider_status_version`, timestamps.
- `refund_audit_logs`: actor, action, before_status, after_status, reason, correlation_id, request metadata, timestamp.
- `refund_provider_events`: provider event ID, raw payload, received_at, processed_at, processing result.
- `refund_attempts`: refund request ID, attempt number, provider request ID, submitted_at, completed_at, outcome.

### Data Storage and Migrations

Add unique constraints for scoped idempotency keys and provider refund IDs. Add indexes on order ID, customer ID, status, created time, and approval queue fields. Migration assumes existing orders expose paid amount, refunded amount, currency, customer ownership, and provider payment ID.

### Services and Business Rules

Creation locks the order refund aggregate and validates ownership, 30-day window, positive amount, currency, and remaining refundable amount. Refunds over 500 USD enter `pending_approval`; smaller eligible refunds can be auto-approved and submitted. Support cannot approve high-value refunds. Finance manager approve/reject actions require reason and write audit.

### Background Jobs and Integrations

Provider submission runs through an outbox/job after DB commit. Provider callbacks deduplicate by event ID and compare event ordering/status precedence before changing refund status. Failed provider refunds can be retried as attempts on the same refund request.

### Security, Permissions, and Audit

Customers can access only their own orders/refunds. Support can create and retry permitted refunds but cannot approve high-value refunds. Finance managers can approve/reject high-value refunds. Audit logs are mandatory for submit, approve, reject, provider callback, retry, cancel, and manual override.

## API Contract

| Method | Path | Purpose | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| GET | `/orders/{orderId}/refund-eligibility` | Get refundable amount and eligibility | none | refundable amount, reason, role permissions | `403`, `404` |
| POST | `/orders/{orderId}/refunds` | Create refund idempotently | amount, currency, reason, idempotencyKey | refund detail or existing refund | `403`, `409`, `422` |
| GET | `/orders/{orderId}/refunds` | List refunds | pagination, status | paged refunds | `403`, `404` |
| GET | `/refunds/{refundId}` | Get refund detail | none | refund detail, retry eligibility, audit visibility | `403`, `404` |
| POST | `/refunds/{refundId}/approve` | Finance approval | reason, version/correlation ID | updated refund | `403`, `409`, `422` |
| POST | `/refunds/{refundId}/reject` | Finance rejection | reason, version/correlation ID | updated refund | `403`, `409`, `422` |
| POST | `/refunds/{refundId}/retry` | Retry failed provider refund | reason, version/correlation ID | updated refund/attempt | `403`, `409`, `422` |
| POST | `/provider/refund-callbacks` | Provider callback | provider event payload | accepted/deduped | `401`, `409` |

## Data Model

| Entity/Table | Fields | Relationships | Notes |
| --- | --- | --- | --- |
| `refund_requests` | order, customer, amount, currency, status, idempotency key, provider ID | belongs to order/customer | central aggregate |
| `refund_attempts` | attempt number, provider request ID, status | belongs to refund request | supports safe retries |
| `refund_audit_logs` | actor, action, before/after, reason, correlation ID | belongs to refund request | immutable |
| `refund_provider_events` | event ID, payload, received/processed timestamps | references refund/provider ID | dedupes callbacks |

## State and Lifecycle Rules

Allowed transitions:

- `requested -> approved` for <= 500 USD eligible refunds.
- `requested -> pending_approval` for > 500 USD refunds.
- `pending_approval -> approved | rejected`.
- `approved -> provider_submitted`.
- `provider_submitted -> succeeded | failed`.
- `failed -> provider_submitted` for support retry.
- `requested | pending_approval -> cancelled` only if cancellation policy is confirmed.

Invalid transitions:

- `pending_approval -> provider_submitted` without finance approval.
- `succeeded -> failed`.
- `rejected -> provider_submitted`.
- Any transition that would exceed remaining refundable amount.

## Error Handling

Use stable machine-readable error codes: `REFUND_NOT_OWNER`, `REFUND_WINDOW_EXPIRED`, `REFUND_AMOUNT_EXCEEDS_REMAINING`, `REFUND_APPROVAL_REQUIRED`, `REFUND_STALE_STATUS`, `REFUND_RETRY_NOT_ALLOWED`, `REFUND_PROVIDER_DUPLICATE`, `REFUND_PROVIDER_PENDING`. Customer-facing messages must be display-safe and localized by frontend or returned by backend.

## Observability and Operations

Log correlation ID, refund ID, order ID, actor ID, provider event ID, status transitions, retry attempts, and dedupe decisions. Metrics include create count, approval latency, provider success/failure rate, callback dedupe count, stale callback count, retry success rate, and over-refund prevention conflicts.

## Testing Strategy

- Frontend: form validation, role-specific action visibility, status/failure states, duplicate submit behavior, approval queue, retry action.
- Backend: idempotency, remaining amount locking, approval threshold enforcement, permission checks, invalid transitions, audit logging.
- Integration: outbox provider submission, callback before/after sync response, duplicate callbacks, retry attempts.
- E2E: customer request, finance approval, provider success, provider failure and support retry.

## Collaboration Record

### Frontend Reviewer Summary

Frontend needs role-based screens, pessimistic mutations, server-owned eligibility, stable idempotency key handling, explicit failure and permission states, and safe status mapping.

### Backend Reviewer Summary

Backend needs transactional refund aggregate validation, approval gating, provider outbox, callback dedupe and ordering, unique provider IDs, retry attempts, and mandatory audit logs.

### Second-Pass Review Summary

Pending clean-context review.

### Resolved Decisions

- Server is source of truth after every mutation.
- Provider submission uses outbox/job after DB commit.
- Retry is modeled as attempts on one refund request, not new refund requests.
- Audit logging is mandatory in the same transaction as status-changing actions.

### Remaining Open Questions

- Is the 500 USD threshold based on individual refund amount or cumulative refunded amount?
- What is the cancellation policy for `requested` and `pending_approval` refunds?
- Who can perform manual override and which statuses can it affect?
- What currency conversion rules apply for non-USD orders?

### Assumptions

- Existing order/payment records expose enough paid/refunded/provider data.
- Existing auth can distinguish customer, support agent, and finance manager roles.
- Provider supplies event IDs and timestamps or status precedence can be derived.

## Risks and Follow-Ups

- Callback ordering can corrupt status if provider event precedence is not implemented.
- Partial refund concurrency can over-refund without aggregate locking.
- Failure messages may leak provider internals without safe message mapping.
- Manual override remains underspecified and should be treated as a blocking product/security question before implementation.
