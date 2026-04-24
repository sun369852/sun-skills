# Payment Refund Technical Design

## Source

- PRD: `D:\sun-skills\prd-to-tech-design-review-workspace\fixtures\payment-refund\prd.md`
- Project: no project path provided
- Generated: 2026-04-25

## Executive Summary

Implement a role-based refund flow for customers, support agents, and finance managers. The backend owns eligibility, idempotency, approval threshold enforcement, status transitions, provider callback ordering, retry safety, and audit logging. The frontend treats the server as source of truth after every mutation and exposes safe status, failure, retry, approval, and permission states.

Second-pass review requested changes before finalization. The final design integrates the technical fixes and marks unresolved product/security semantics as blocking questions instead of pretending they are decided.

## PRD Scope Mapping

| PRD Requirement | Technical Coverage | Notes |
| --- | --- | --- |
| Customers can request refunds for paid orders within 30 days | Eligibility API and customer refund form | Server owns final eligibility decision |
| Refunds over 500 USD require finance approval | Backend threshold gate and finance approval queue | Blocking question for non-USD conversion |
| Partial refunds until paid amount is reached | Transactional refundable-balance reservation check | Defines which statuses reserve amount |
| Idempotent refund requests | Client idempotency key plus server payload fingerprint | Same key with different payload returns conflict |
| Audit all actions | `refund_audit_logs` written with every status-changing action | Retry and manual override audit requirements are explicit |
| Provider callbacks may race API response | Durable refund attempt/correlation ID plus callback dedupe | Handles callback before synchronous response |
| Users can see status and failure reason | Customer/support/finance detail views and safe error messages | Provider internals mapped to display-safe messages |

Coverage estimate: all concrete PRD requirements are represented, but final implementation is blocked on currency conversion, cancellation, and manual override policy decisions.

## Architecture Overview

Frontend surfaces call refund APIs. Backend validates eligibility, creates or returns a refund request idempotently, gates high-value refunds through finance approval, submits approved refunds to the provider through an outbox/job, receives provider callbacks idempotently, and records audit logs in the same transaction as status changes.

Provider submission creates a durable `refund_attempt` before calling the provider. The attempt carries an internal request/correlation ID so callbacks that arrive before the synchronous response can be attached to the correct refund.

## Frontend Design

### Routes and Screens

- Customer order detail refund entry point.
- Customer refund request form with amount, reason, remaining refundable amount, and approval notice.
- Customer refund status/history view.
- Support refund list and detail with failure reason, audit timeline, retry action, and create-refund-for-customer flow.
- Finance approval queue and approval detail with audit/history visibility.

### Client State and Data Fetching

Use server state for refund detail, order eligibility, refund lists, approval queue, and audit timeline. Mutations use pessimistic updates. After create, approve, reject, retry, or callback-visible changes, invalidate order, refund detail, refund list, approval queue, and audit queries.

### UX States and Validation

Cover loading, empty, error, success, permission-denied, stale-status, and provider-failed states. Frontend mirrors amount, reason, and eligibility validation but never treats local validation as authoritative. It sends a stable idempotency key per logical user submission and routes duplicate responses to the existing refund.

## Backend Design

### Domain Model

- `refund_requests`: `id`, `order_id`, `customer_id`, `amount`, `currency`, `status`, `reason`, `failure_reason`, `safe_failure_message`, `created_by`, `approved_by`, `idempotency_key`, `idempotency_payload_hash`, timestamps.
- `refund_attempts`: `id`, `refund_request_id`, `attempt_number`, `internal_request_id`, `provider_refund_id`, `status`, `submitted_at`, `completed_at`, `failure_reason`.
- `refund_audit_logs`: actor, action, before_status, after_status, reason, correlation_id, retry_attempt_id, request metadata, timestamp.
- `refund_provider_events`: provider event ID, provider refund ID, internal request ID when available, raw payload, received_at, processed_at, processing result.

### Data Storage and Constraints

- Unique scoped idempotency key, such as `(order_id, actor_id, idempotency_key)`.
- Store `idempotency_payload_hash`; same key and same hash returns existing refund, same key and different hash returns `REFUND_IDEMPOTENCY_CONFLICT`.
- Unique nullable `provider_refund_id`.
- Unique provider event ID.
- Index approval queue by status and created time.
- Index refund history by order, customer, status, and created time.

### Refundable Balance Semantics

Refunds in these statuses reserve refundable amount: `requested`, `pending_approval`, `approved`, `provider_submitted`, and `succeeded`.

Refunds in these statuses do not reserve amount: `rejected`, `cancelled`, and terminal provider `failed` after no active retry is pending.

Retry attempts on a `failed` refund reuse the same refund request and re-reserve the amount while the retry is `provider_submitted`. Creation and retry both run under order/refund aggregate locking to prevent over-refund.

### Services and Business Rules

Creation locks the order refund aggregate and validates ownership, 30-day window, positive amount, currency, remaining refundable amount, and idempotency hash. Refunds over the threshold enter `pending_approval`; smaller eligible refunds can be approved and submitted. Support cannot approve high-value refunds. Finance manager approve/reject actions require reason and write audit.

### Background Jobs and Integrations

Provider submission runs through an outbox/job after DB commit. Before calling the provider, the job creates a durable `refund_attempt` with `internal_request_id`. Provider callbacks deduplicate by event ID and attach by provider refund ID or internal request ID. Callback processing compares event ordering or status precedence and must never downgrade `succeeded` to `failed`.

### Security, Permissions, and Audit

Customers can access only their own orders/refunds. Support can create and retry permitted refunds but cannot approve high-value refunds. Finance managers can approve/reject high-value refunds and view approval/audit history. Audit logs are mandatory for submit, approve, reject, provider callback, retry, cancel, and manual override.

Manual override is a blocking security/product question until its role, allowed statuses, and approval/audit requirements are defined.

## API Contract

| Method | Path | Purpose | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| GET | `/orders/{orderId}/refund-eligibility` | Get refundable amount and eligibility | none | `RefundEligibility` | `403`, `404` |
| POST | `/orders/{orderId}/refunds` | Create refund idempotently | `CreateRefundRequest` | `RefundDetail` or existing refund | `403`, `409`, `422` |
| GET | `/orders/{orderId}/refunds` | List refunds | pagination, status | paged `RefundSummary` | `403`, `404` |
| GET | `/refunds/{refundId}` | Get refund detail | none | `RefundDetail` | `403`, `404` |
| POST | `/refunds/{refundId}/approve` | Finance approval | reason, version/correlation ID | `RefundDetail` | `403`, `409`, `422` |
| POST | `/refunds/{refundId}/reject` | Finance rejection | reason, version/correlation ID | `RefundDetail` | `403`, `409`, `422` |
| POST | `/refunds/{refundId}/retry` | Retry failed refund | reason, version/correlation ID | `RefundDetail` with attempt | `403`, `409`, `422` |
| POST | `/provider/refund-callbacks` | Provider callback | provider event payload | accepted/deduped | `401`, `409` |

Shared response fields:

- `RefundStatus`: `requested`, `pending_approval`, `approved`, `provider_submitted`, `succeeded`, `failed`, `rejected`, `cancelled`
- `RefundDetail`: ID, order ID, amount, currency, status, failure reason, safe failure message, retry eligibility, approval eligibility, audit visibility, current attempt, timestamps, correlation ID
- `RefundEligibility`: refundable amount, reserved amount, currency, eligible flag, ineligibility reason, permissions
- `AuditEntry`: actor, action, before/after status, reason, retry attempt ID, timestamp, correlation ID

## State and Lifecycle Rules

Allowed transitions:

- `requested -> approved` for refunds that do not require finance approval.
- `requested -> pending_approval` for refunds requiring finance approval.
- `pending_approval -> approved | rejected`.
- `approved -> provider_submitted`.
- `provider_submitted -> succeeded | failed`.
- `failed -> provider_submitted` for support retry on the same refund request.
- `requested | pending_approval -> cancelled` only after cancellation policy is confirmed.

Invalid transitions:

- `pending_approval -> provider_submitted` without finance approval.
- `succeeded -> failed`.
- `rejected -> provider_submitted`.
- Same idempotency key with different payload creating a second refund.
- Any transition that would exceed remaining refundable amount.

## Error Handling

Use stable machine-readable error codes: `REFUND_NOT_OWNER`, `REFUND_WINDOW_EXPIRED`, `REFUND_AMOUNT_EXCEEDS_REMAINING`, `REFUND_APPROVAL_REQUIRED`, `REFUND_STALE_STATUS`, `REFUND_RETRY_NOT_ALLOWED`, `REFUND_PROVIDER_DUPLICATE`, `REFUND_PROVIDER_PENDING`, `REFUND_IDEMPOTENCY_CONFLICT`, `REFUND_CALLBACK_STALE`. Customer-facing messages must be display-safe.

## Observability and Operations

Log correlation ID, refund ID, order ID, actor ID, provider event ID, attempt ID, status transitions, retry attempts, idempotency conflicts, callback dedupe decisions, and stale callbacks. Metrics include create count, approval latency, provider success/failure rate, callback dedupe count, stale callback count, retry success rate, and over-refund prevention conflicts.

## Testing Strategy

- Frontend: form validation, role-specific action visibility, status/failure states, duplicate submit behavior, approval queue, retry action.
- Backend: idempotency hash conflicts, remaining amount locking, approval threshold enforcement, permission checks, invalid transitions, audit logging.
- Integration: outbox provider submission, durable attempt correlation, callback before/after sync response, duplicate callbacks, stale callbacks, retry attempts.
- E2E: customer request, finance approval, provider success, provider failure and support retry.

## Collaboration Record

### Frontend Reviewer Summary

Frontend needs role-based screens, pessimistic mutations, server-owned eligibility, stable idempotency key handling, explicit failure and permission states, and safe status mapping.

### Backend Reviewer Summary

Backend needs transactional refund aggregate validation, approval gating, provider outbox, callback dedupe and ordering, unique provider IDs, retry attempts, and mandatory audit logs.

### Second-Pass Review Summary

Second-pass reviewer returned `request changes`. Required changes were integrated for idempotency payload conflicts, durable provider attempt correlation, refundable balance reservation semantics, expanded API response shapes, retry audit detail, and qualified coverage language.

Remaining second-pass items are recorded as blocking questions: manual override policy, cancellation policy, and USD threshold/currency conversion.

### Resolved Decisions

- Server is source of truth after every mutation.
- Provider submission uses outbox/job after DB commit.
- Durable refund attempt is created before provider call.
- Retry is modeled as attempts on one refund request, not new refund requests.
- Same idempotency key with different payload returns conflict.
- Audit logging is mandatory in the same transaction as status-changing actions.

### Remaining Open Questions

- Is the 500 USD threshold converted to USD for all currencies, or are non-USD orders out of scope?
- What is the cancellation policy for `requested` and `pending_approval` refunds?
- Who can perform manual override and which statuses can it affect?
- Does the provider guarantee event IDs plus event timestamps or monotonic versions?

### Assumptions

- Existing order/payment records expose paid amount, refunded amount, owner, currency, and provider payment identifiers.
- Existing auth can distinguish customer, support agent, and finance manager roles.
- Provider supports enough correlation to attach early callbacks to attempts; if not, provider integration design is blocked.

## Risks and Follow-Ups

- Currency conversion for threshold is a blocking product/payment decision.
- Manual override is a blocking security/product decision.
- Cancellation is a blocking lifecycle decision because `cancelled` appears in PRD statuses.
- Provider callback ordering remains high risk until provider guarantees are confirmed.

## Quality Gate Result

- PRD functional coverage: represented, with three PRD-affecting decisions marked blocking.
- API/data/status/error/testing coverage: present.
- Frontend/backend contract consistency: patched after second-pass review.
- Second-pass required changes: integrated or recorded as blocking questions.
- Ready for task decomposition: not fully ready until blocking questions are answered.
