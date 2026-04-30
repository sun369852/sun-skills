# Full-Auto And Risk

## Modes

Standard mode is the default. Full-auto mode is active when the user explicitly says fully managed, full-auto, no confirmation, completely entrusted, or equivalent.

In standard mode, normal engineering work can proceed automatically, but high-impact operations need confirmation.

In full-auto mode, the main agent can approve more engineering changes without interrupting the user, but must record decisions in the run log.

Full-auto mode changes confirmation behavior, not verification standards. Do not downgrade required verification in full-auto mode. If required verification cannot run, record the reason and demote the affected task to `partial`, `blocked`, or `failed`.

## Chain High-Risk Policy

When invoked by `product-delivery-skill-chain`, read the downstream invocation envelope before applying this reference.

- `explicit-only`: ask the user before hard-risk operations.
- `ask-with-risk-summary`: ask the user with a short risk summary before hard-risk operations.
- `no-confirmation`: do not ask the user only because an operation is high risk. Record the risk, rationale, decision, and verification or blocker in the run log.

`no-confirmation` does not bypass system, sandbox, tool, repository, or platform approval requirements. It also does not authorize unsafe execution when the implementation cannot be made trustworthy. If a hard-risk operation would require production data deletion, real external payment/message/API calls, destructive migrations, major security or permission semantic changes, public API breaking changes, or a large rewrite outside the task scope, first choose a conservative implementation path. If no conservative path exists, mark the affected task blocked and record why instead of asking the user.

## Full-Auto Can Approve

Full-auto mode may automatically approve:

- dependency additions or small version updates when necessary
- local database migration generation and local verification
- test snapshot updates after verifying acceptance criteria
- low-risk internal API contract adjustment
- formatting and lint auto-fixes
- non-destructive configuration changes

Workers still cannot approve these on their own. They must request approval from the main agent.

## Hard-Risk Operations

Even in full-auto mode, do not automatically perform:

- production data deletion
- real external payment, message, or production API calls
- destructive migrations
- major framework upgrades
- public API breaking changes
- major security or permission semantic changes
- large rewrites outside the task scope

Ask the user before hard-risk operations unless the chain envelope sets `High-risk operations: no-confirmation`. If a conservative implementation avoids the risk, choose that path and record the decision. With `no-confirmation`, do not ask just to accept the risk; choose the conservative path or block the task when safe execution is not possible.

## Dependency Changes

Workers cannot directly add or upgrade dependencies. They may report the need. The main agent must check whether existing dependencies can satisfy the task, whether docs permit the change, and what verification is required.

Record dependency changes, rationale, impact scope, and verification results in the run log.
