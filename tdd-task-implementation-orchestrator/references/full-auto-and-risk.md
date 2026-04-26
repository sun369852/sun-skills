# Full-Auto And Risk

## Modes

Standard mode is the default. Full-auto mode is active when the user explicitly says fully managed, full-auto, no confirmation, completely entrusted, or equivalent.

In standard mode, normal engineering work can proceed automatically, but high-impact operations need confirmation.

In full-auto mode, the main agent can approve more engineering changes without interrupting the user, but must record decisions in the run log.

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

Ask the user before hard-risk operations. If a conservative implementation avoids the risk, choose that path and record the decision.

## Dependency Changes

Workers cannot directly add or upgrade dependencies. They may report the need. The main agent must check whether existing dependencies can satisfy the task, whether docs permit the change, and what verification is required.

Record dependency changes, rationale, impact scope, and verification results in the run log.
