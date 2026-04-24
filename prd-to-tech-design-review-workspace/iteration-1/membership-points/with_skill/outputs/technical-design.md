# Membership Points Technical Design

## Source

- PRD: `D:\sun-skills\prd-to-tech-design-review-workspace\fixtures\membership\prd.md`
- Project: not inspected; the request provided only a PRD fixture and an output directory.
- Generated: 2026-04-24
- Collaboration mode: inline frontend/backend review, because separate subagent tools are not available in this environment.

## Executive Summary

Implement membership points as an immutable ledger plus a query-optimized account balance and expiring point lots. Order payment, refund reversal, manual admin adjustment, and nightly expiry all create ledger entries. Duplicate awards are prevented with source-based idempotency keys and database uniqueness constraints. Members get a balance and paginated ledger view; admins get a permission-gated adjustment form that requires a reason and writes audit metadata.

## PRD Scope Mapping

| PRD Requirement | Technical Coverage | Notes |
| --- | --- | --- |
| Award points after an order is paid | Order-paid event handler creates `earn` ledger entry, updates balance, and creates expiring point lot | Exactly-once enforced by `source_type + source_id` uniqueness |
| Points expire after 12 months unless campaign defines shorter expiry | Point lots store `expires_at`; expiry job consumes expired remaining lots and writes `expire` ledger entries | Campaign model is assumed because PRD references campaigns without defining them |
| Admins can manually adjust points with required reason | Admin API validates permission and non-empty reason, creates `manual_adjust` ledger entry, and records audit metadata | Negative adjustments cannot make available balance negative unless product later allows debt |
| Members can view balance and ledger entries | Member balance endpoint plus paginated ledger endpoint; frontend renders summary and history table | Ledger is immutable and sorted newest first by default |
| Prevent duplicate point awards for same order | Idempotent order award service with unique source key and transactional locking | Duplicate events return existing result |
| 1 USD paid amount equals 1 point | Store paid amount in cents; derive integer points with documented rounding assumption | Rounding is an open product question |
| Refunded order amounts reverse corresponding points | Refund event creates `reverse` ledger entry linked to original order and refund id | Reversal amount is capped by points previously awarded and not already reversed |
| Manual adjustments must be audited | Ledger stores actor, reason, correlation id, and before/after balance snapshot | Admin audit log can reference the ledger id |
| Expired points are deducted nightly | Scheduled job selects expired lots with remaining points and writes expiry ledger entries | Job must be idempotent per lot and expiry date |
| Ledger entries are immutable after creation | No update/delete path for ledger entries; corrections use compensating entries | Database permissions or service layer should enforce write-only semantics |

## Architecture Overview

Core components:

- Member UI reads balance and ledger history.
- Admin UI submits manual adjustments through a guarded form.
- Points API exposes member read endpoints and admin adjustment endpoint.
- Points domain service owns all ledger writes, balance updates, idempotency checks, point lot creation, and expiry consumption.
- Order/payment integration emits paid and refund events into the points service.
- Nightly expiry job scans point lots and creates expiry ledger entries.

Data flow:

1. Order is marked paid.
2. Points service calculates points from paid amount and campaign expiry.
3. Within one transaction, it inserts an immutable ledger entry, updates account balance, and creates a point lot.
4. Member UI refetches balance and ledger when the order state or points data changes.
5. Refunds, manual adjustments, and expiry follow the same ledger-first pattern with negative or positive deltas.

## Frontend Design

### Routes and Screens

- Member points page: `/account/points`
  - Balance summary: available points, next expiring points if available, last updated timestamp.
  - Ledger table: date, type, points delta, source, reason or description, expiry date when relevant.
  - Pagination and optional type/date filters if the existing table pattern supports them.
- Admin member points adjustment: `/admin/members/:memberId/points`
  - Current member balance.
  - Adjustment form with amount, reason, optional internal note, and submit confirmation for negative adjustments.
  - Recent ledger entries for context.

### Component Structure

- `PointsBalanceSummary`
- `PointsLedgerTable`
- `LedgerTypeBadge`
- `AdminPointsAdjustmentForm`
- `AdjustmentConfirmationDialog`

The UI should avoid editing ledger rows. Corrections are represented as new manual adjustment entries.

### Client State and Data Fetching

- Treat points data as server state.
- Cache balance and first ledger page separately, with invalidation after successful admin adjustment.
- For member pages, no optimistic balance mutation is required because ledger correctness is financial-like.
- For admin adjustment, disable duplicate submission while pending and refetch balance plus ledger after success.

### UX States and Validation

- Loading: skeleton or table loading state for balance and ledger.
- Empty: "No points activity yet" state for members with no entries.
- Error: retryable fetch error for member views; permission error for admin page.
- Validation:
  - Adjustment amount is required and non-zero integer.
  - Reason is required and trimmed.
  - Negative adjustment displays the available balance impact before submit.
  - Backend remains source of truth for permission, balance, and idempotency.

### Accessibility and Responsive Behavior

- Ledger table should preserve semantic table markup on desktop and compact stacked rows on small screens.
- Form fields need visible labels, inline validation messages, and keyboard-reachable confirmation controls.
- Point deltas should not rely on color alone; include plus/minus signs and labels.

## Backend Design

### Domain Model

- `MemberPointAccount`: one row per member with current available balance and version/timestamps.
- `PointLedgerEntry`: immutable event record for every points change.
- `PointLot`: tracks earned or manually-added expirable points and remaining points for expiry/reversal allocation.
- `CampaignPointRule`: optional campaign expiry override referenced by earning events.
- `PointIdempotencyKey`: optional separate table if the ledger source uniqueness cannot cover all event types.

### Data Storage and Migrations

- Use integer point amounts, positive for earning/addition and negative for reversal/deduction/expiry.
- Store money inputs as cents in source metadata to avoid floating point errors.
- Add unique index on `(member_id, source_type, source_id)` for exactly-once ledger creation where source ids are stable.
- Add indexes for `(member_id, created_at desc)`, `(member_id, expires_at)`, and expiry job lookup on point lots.
- Consider row-level lock or optimistic version on `MemberPointAccount` for concurrent events.

### Services and Business Rules

- `awardForPaidOrder(order)`:
  - Validate paid status and eligible paid amount.
  - Calculate points from paid cents.
  - Resolve expiry date: campaign shorter expiry if present, otherwise 12 months from award timestamp.
  - Insert `earn` ledger entry, point lot, and account balance update in one transaction.
  - Return existing ledger entry if duplicate source is received.
- `reverseForRefund(refund)`:
  - Find original award ledger and unreversed amount.
  - Calculate reversal points for refunded cents.
  - Cap reversal at remaining awarded points not already reversed.
  - Insert `reverse` ledger entry and reduce available balance/point lots.
- `createManualAdjustment(memberId, amount, reason, actor)`:
  - Require admin permission and reason.
  - Positive adjustment creates a point lot with standard expiry unless product decides manual points do not expire.
  - Negative adjustment consumes available lots by expiry order and fails if balance would go below zero.
- `expirePoints(runDate)`:
  - Nightly job selects lots where `expires_at <= runDate` and `remaining_points > 0`.
  - Creates one or batched `expire` ledger entries.
  - Marks consumed remaining points on lots.

### Background Jobs and Integrations

- Order paid event integration: at-least-once delivery is acceptable when idempotency is enforced.
- Refund event integration: idempotent by refund id.
- Nightly expiry job: safe to rerun for a date; should process in batches and record run metrics.

### Security, Permissions, and Audit

- Members can read only their own point balance and ledger.
- Admin adjustment requires explicit permission such as `points.adjust`.
- Manual adjustment must store actor id, reason, timestamp, request id, and before/after balance.
- Ledger metadata may include order id/refund id but should not expose sensitive payment details in member responses.

## API Contract

| Method | Path | Purpose | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/me/points/balance` | Member reads available points | None | `{ "availablePoints": 120, "nextExpiring": { "points": 40, "expiresAt": "2026-09-01" } }` | `401` unauthenticated |
| GET | `/api/me/points/ledger` | Member reads paginated ledger | Query: `cursor`, `limit`, optional `type` | `{ "items": [...], "nextCursor": "..." }` | `401`, `400` invalid query |
| GET | `/api/admin/members/{memberId}/points` | Admin reads member balance and recent ledger | Path member id | `{ "memberId": "...", "availablePoints": 120, "recentEntries": [...] }` | `403`, `404` |
| POST | `/api/admin/members/{memberId}/points/adjustments` | Admin creates manual adjustment | `{ "points": -10, "reason": "Customer support correction" }` | `{ "ledgerEntryId": "...", "availablePoints": 110 }` | `400`, `403`, `404`, `409` insufficient balance |
| POST/internal | `/internal/points/order-paid` | Award points for paid order event | `{ "orderId": "...", "memberId": "...", "paidCents": 12345, "campaignId": "..." }` | `{ "ledgerEntryId": "...", "awardedPoints": 123, "duplicate": false }` | `400`, `409` invalid order state |
| POST/internal | `/internal/points/order-refunded` | Reverse points for refund event | `{ "refundId": "...", "orderId": "...", "refundedCents": 2500 }` | `{ "ledgerEntryId": "...", "reversedPoints": 25, "duplicate": false }` | `400`, `404`, `409` no reversible award |

Ledger item response shape:

```json
{
  "id": "ple_123",
  "createdAt": "2026-04-24T10:00:00Z",
  "type": "earn",
  "points": 123,
  "balanceAfter": 123,
  "source": {
    "type": "order",
    "id": "ord_123"
  },
  "description": "Order points",
  "expiresAt": "2027-04-24T10:00:00Z"
}
```

## Data Model

| Entity/Table | Fields | Relationships | Notes |
| --- | --- | --- | --- |
| `member_point_accounts` | `member_id`, `available_points`, `version`, `created_at`, `updated_at` | One-to-one with member | Query cache for current balance |
| `point_ledger_entries` | `id`, `member_id`, `type`, `points_delta`, `balance_before`, `balance_after`, `source_type`, `source_id`, `reason`, `actor_id`, `metadata_json`, `created_at` | Many-to-one with member/account | Immutable; unique source keys for idempotency |
| `point_lots` | `id`, `member_id`, `origin_ledger_entry_id`, `earned_points`, `remaining_points`, `expires_at`, `campaign_id`, `created_at` | Created by positive entries; consumed by refund/manual negative/expiry | Enables expiry and allocation |
| `campaign_point_rules` | `campaign_id`, `expiry_days`, `starts_at`, `ends_at` | Optional relation from order/campaign | Assumed from PRD campaign expiry rule |
| `point_job_runs` | `id`, `job_type`, `run_date`, `status`, `processed_count`, `error_count`, `started_at`, `finished_at` | Operational record | Supports expiry job observability |

## State and Lifecycle Rules

- Ledger entry types: `earn`, `reverse`, `manual_adjust`, `expire`.
- Ledger entries are append-only. Any correction creates another ledger entry.
- Account balance is derived from ledger deltas but stored for efficient reads.
- Point lots are created for positive point deltas that can expire.
- Negative point deltas consume lots in earliest-expiring-first order.
- Expired points are deducted only for remaining unconsumed lot points.
- Duplicate order paid events return the original award result and do not create a new entry.
- Duplicate refund events return the original reversal result and do not create a new entry.

## Error Handling

- Member ledger fetch failure: show retryable error without hiding existing cached balance if available.
- Admin adjustment validation failure: show field-level reason and amount errors.
- Permission failure: return `403` and render permission-denied state.
- Duplicate event: return success with `duplicate: true` for internal callers.
- Insufficient balance for negative admin adjustment: return `409` with current available balance.
- Expiry job partial failure: keep processed ledger entries, record failed batch, and allow rerun through idempotent lot consumption.

## Observability and Operations

- Log every ledger mutation with correlation id, source type/id, member id, delta, actor id when present, and idempotency outcome.
- Metrics:
  - awarded points count and amount
  - refund reversal count and amount
  - manual adjustment count by actor/permission scope
  - expiry job processed lots, expired points, duration, and failures
  - duplicate event count
- Alerts:
  - expiry job missed or failed
  - high rate of duplicate paid events
  - ledger/account balance reconciliation mismatch
- Add a reconciliation job or admin report comparing account balance to sum of ledger deltas.

## Testing Strategy

- Frontend:
  - Member balance and ledger render loading, empty, populated, and error states.
  - Admin adjustment form validates required reason and non-zero integer amount.
  - Permission-denied state appears for unauthorized admin users.
- Backend unit tests:
  - Award calculation from paid cents.
  - Duplicate order paid event creates exactly one ledger entry.
  - Refund reversal caps at awarded and unreversed points.
  - Manual adjustment requires permission and reason.
  - Expiry job creates expiry ledger entries only for unconsumed expired lots.
- Integration tests:
  - Paid order event updates ledger, lot, and account balance transactionally.
  - Refund after paid order reduces balance and lot remaining points.
  - Admin adjustment audit fields are persisted.
  - Ledger API pagination is stable and scoped to the authenticated member.
- Regression checks:
  - Ledger rows cannot be updated or deleted through public service paths.
  - Concurrent duplicate events do not double award points.
  - Reconciliation detects intentionally corrupted account balance in test setup.

## Collaboration Record

### Frontend Reviewer Summary

The UI requires a member-facing points page with current balance and immutable history, plus an admin adjustment workflow with strong validation, permission handling, and clear post-submit refetch. The frontend needs compact ledger item payloads, stable pagination, type labels, and explicit error responses for unauthorized access, validation failures, and insufficient balance.

### Backend Reviewer Summary

The backend should centralize all point changes in a points domain service with transactional ledger writes, account balance updates, lot allocation, and idempotent event processing. The main correctness risks are duplicate order events, refund reversal mapping, expiry allocation, manual adjustment auditability, and keeping the immutable ledger consistent with cached balance.

### Exchange and Mediation Notes

- Frontend asked for balance and ledger to be separate read endpoints; backend accepts this because account balance is query-optimized while ledger can remain paginated.
- Backend requires no optimistic UI for point mutations; frontend accepts refetch-after-write for admin adjustments to preserve correctness.
- Frontend requested human-readable ledger descriptions; backend will provide source/type metadata and a safe display description without exposing sensitive payment details.
- Backend identified campaign expiry ambiguity; mediation records a design assumption for `campaign_point_rules` rather than inventing campaign behavior.

### Resolved Decisions

- Use immutable ledger entries for all point changes.
- Use account balance as a cached projection, backed by reconciliation.
- Use point lots to support expiry and refund/manual deduction allocation.
- Use source uniqueness and transactional locking for idempotency.
- Require permission and reason for manual adjustments.
- Treat duplicate internal events as successful idempotent responses.

### Remaining Open Questions

- Rounding policy: when paid/refunded amount is not a whole USD, should points be floored, rounded, or calculated from cents with fractional carryover?
- Campaign behavior: where is campaign membership defined, and can campaign expiry rules change after an order is paid?
- Manual positive adjustments: should they expire after 12 months, use a custom admin-selected expiry, or never expire?
- Negative balance policy: may admin adjustments create negative point balances, or must they fail when balance is insufficient?
- Time zone policy: should nightly expiry run by UTC date, store locale-specific expiry dates, or use the member/store time zone?

### Assumptions

- Points are integer values.
- Default expiry is 12 months from the ledger creation timestamp.
- Existing authentication can distinguish members and admins.
- Internal order/refund event payloads include stable ids suitable for idempotency.
- The system can add database constraints and background jobs.

## Risks and Follow-Ups

- Financial-like correctness: even though points are not money, duplicate awards and incorrect reversals can create material customer support issues.
- Campaign expiry is underspecified and should be confirmed before implementation.
- Rounding can affect customer-visible balances and must be decided before launch.
- Ledger/account reconciliation should be available before enabling admin manual adjustments at scale.
- This document is ready for later task decomposition after the open product questions are answered or accepted as assumptions.
