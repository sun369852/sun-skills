# Risk Gates

Apply stricter gates when the change touches:

- authentication, authorization, roles, sessions, or secrets
- payments, billing, credits, quotas, or irreversible user actions
- production data migration, deletion, import/export, or retention
- public API contracts, database schemas, event formats, or background jobs
- concurrency, retries, idempotency, caching, or distributed state
- user-facing critical paths such as signup, checkout, publishing, or admin actions

## Required Evidence for High-Risk Changes

High-risk work should usually have:

- direct requirement traceability
- targeted automated tests for core and failure paths
- compatibility or migration notes where relevant
- rollback or recovery consideration for irreversible operations
- explicit mention of any untested path

If these are absent, the final decision should usually be `Fix needed` or `Blocked`, not `Pass`.

## Stop Conditions

Stop and ask or mark `Blocked` when:

- product behavior must be decided to judge correctness
- credentials or external systems are required to verify the core behavior
- the diff includes destructive operations not mentioned in the source artifacts
- source artifacts and implementation disagree on a critical behavior

Do not approve high-risk behavior based only on code inspection when a feasible verification path exists.
