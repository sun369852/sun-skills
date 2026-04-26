# Audit Check Rules

Use this reference when creating audit checks, machine-readable output, execution statuses, hard fail rules, defect reports, retest rules, or PRD update rules.

## Stable IDs

Use stable IDs so audit reports, test files, evidence, and defects can reference standards:

- `BV-001`: Behavior Verification
- `IA-001`: Implementation Audit
- `TE-001`: Test Execution
- `RG-001`: Risk Gate
- `EV-001`: Evidence Requirement
- `BQ-001`: Blocked Question

When updating an existing standards document, preserve existing IDs when possible, append new IDs, and mark removed checks as deprecated instead of reusing IDs.

## Check Fields

Each audit check should include:

- PRD trace
- category
- priority: `Blocker`, `High`, `Medium`, or `Low`
- mode: `Automated`, `Manual`, `Review-only`, or `Blocked`
- automation level and rationale
- setup and test data
- steps or review method
- pass criteria
- fail criteria
- required evidence
- test execution requirement: `Required`, `Conditional`, `Static fallback`, or `Not applicable`
- retest scope
- status: `Ready`, `Blocked`, `Not Run`, or `Not Applicable`

Do not require arbitrary coverage percentages. Require evidence that P0/P1 or `Blocker`/`High` PRD risk paths have automated tests or a documented reason why automation is not feasible.

## Test Execution And Evidence

When project context provides test commands, standards should require the future audit agent to run relevant commands where feasible:

- `Required test execution`: must run and record command, timestamp, result, and failure log.
- `Conditional execution`: run when dependent services, secrets, accounts, or test data are available.
- `Static verification`: if execution is blocked, inspect test files, mocks, assertions, and coverage of PRD paths.
- `Blocked`: environment, credentials, dependencies, or data are missing; record blocker and unblock condition.

Every evidence item must trace to an audit check ID. Failure evidence must also trace to a defect report ID. API/log/database evidence should include request parameters, query conditions, correlation IDs, or record IDs where relevant.

## Status And Final Conclusions

Use these execution statuses:

- `Pass`
- `Fail`
- `Blocked`
- `Not Run`
- `Not Applicable`

`Blocked` and `Not Run` are not passes. `Blocker` or `High` checks that are blocked or not run prevent unconditional approval unless there is sufficient substitute evidence.

Use these final conclusions:

- `Approved`: all `Blocker` and `High` checks pass, and `Medium`/`Low` findings do not create aggregated release risk.
- `Approved with Risks`: no `Blocker` failure; remaining `High`/`Medium` issues have explicit risk acceptance or deferral rationale.
- `Rejected`: any `Blocker` check fails or a critical PRD behavior is missing.
- `Blocked`: critical `Blocker`/`High` checks cannot be verified and substitute evidence is insufficient.

For standards-generation readiness, use only `Ready`, `Ready with assumptions`, or `Blocked`. If core `Blocker` semantics are unknown, choose `Blocked`; assumptions are only acceptable when they do not decide release-blocking product behavior.

## Hard Fail Conditions

Hard fail conditions include:

- any `Blocker` check fails
- any `Blocker` check is `Blocked` or `Not Run` without substitute evidence
- a core PRD flow has no audit coverage
- high-risk permission, data, payment, ledger, privacy, or audit-log behavior lacks implementation audit coverage
- required test commands are not run and no blocker is recorded
- high-risk clean-context review findings are ignored without rejection rationale
- evidence cannot be traced to audit check IDs

## Defect Report

Define a defect report format for failed checks. Required fields:

- defect ID
- audit check ID
- PRD trace
- failure summary
- expected result
- actual result
- reproduction steps or review method
- evidence references
- affected files, APIs, logs, database records, or UI paths
- impact scope
- suggested severity
- release blocking status
- recommended fix direction
- retest scope

## Retest And Regression

For retest, require the future audit agent to verify:

- original failed check
- related checks in the same PRD area
- affected regression checks
- tests tied to changed code paths

`Blocker` and `High` fixes require related regression execution or a documented blocker.

## PRD Change Synchronization

When the source PRD changes:

- rerun PRD coverage analysis
- preserve unaffected audit check IDs
- append IDs for new checks
- mark removed requirements and checks as deprecated
- re-evaluate risk levels and hard fail conditions
- rerun three clean-context reviews when changes affect core flows, permissions, data integrity, integrations, irreversible operations, or risk levels
- for small non-behavioral wording changes, a local update plus quality gate is sufficient
