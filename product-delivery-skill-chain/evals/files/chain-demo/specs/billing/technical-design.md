# Billing Cycle Technical Design

## Data

- Add `billing_cycle_change_requests`.
- Keep existing invoice records immutable.
- Store old day, new day, effective date, requester, approver, and status.

## API

- `POST /billing/cycle-change-requests`
- `POST /billing/cycle-change-requests/{id}/approve`
- `POST /billing/cycle-change-requests/{id}/reject`

## Verification

- Unit tests for effective-date calculation.
- Integration tests for approval and rejection.
- Regression tests for existing invoice generation.
