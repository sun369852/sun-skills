# Billing Cycle Tasks

## Ready Tasks

### T001 Create cycle change request model
- Status: ready
- Depends on: none
- Validation: model unit tests

### T002 Add request creation API
- Status: ready
- Depends on: T001
- Validation: API integration tests

### T003 Add approval and rejection APIs
- Status: ready
- Depends on: T001
- Validation: approval/rejection integration tests

### T004 Add billing settings UI
- Status: blocked
- Depends on: T002, T003
- Blocker: final UI copy not confirmed

## Implementation Notes

- Do not change existing paid invoices.
- Keep task completion gated by tests and task-list updates.
