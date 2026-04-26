# Risk Gates

Use this reference as a fallback and supplement. In standards mode, audit standards hard fail conditions take priority. Apply these risk gates when no standards artifact exists or when the standards do not cover a risk introduced by the implementation.

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

## Risk Acceptance

Do not accept release risk on the user's behalf. `Pass with notes` or `Approved with Risks` is appropriate only when:

- there is no failed release-blocking gate
- the remaining risk is explicitly bounded
- the report names the missing evidence or deferred issue
- the user, project policy, or audit standards allow deferral

If a `High` or `Blocker` risk requires business or product acceptance, report it as `Fix needed` or `Blocked` until the user accepts the risk.

Implementation defects can be routed to the development skill automatically, but risk acceptance cannot. If the only way to pass is to accept a high-risk residual issue, stop and ask the user.

## Stop Conditions

Stop and ask or mark `Blocked` when:

- product behavior must be decided to judge correctness
- credentials or external systems are required to verify the core behavior
- the diff includes destructive operations not mentioned in the source artifacts
- source artifacts and implementation disagree on a critical behavior

Do not approve high-risk behavior based only on code inspection when a feasible verification path exists.
