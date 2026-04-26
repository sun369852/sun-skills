# Large PRD Quality Audit Standards

## Linked Artifacts

- Machine-readable audit checks: [audit-checks.json](audit-checks.json)
- Clean-context review record: [clean-context-review-record.md](clean-context-review-record.md)
- Audit report template: [audit-report-template.md](audit-report-template.md)

## Source And Scope

- Source PRD: user-provided summary PRD covering Web, background jobs, external payment callbacks, data migration, and audit reports.
- Supporting context: none provided.
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents.
- In scope: behavior verification, implementation audit, test execution requirements, hard fail rules, evidence requirements, defect reporting, retest rules, and PRD change synchronization.
- Out of scope: rewriting the PRD, technical design, implementation tasks, and live execution against completed code.

## Assumptions And Blockers

- Assumption: the listed PRD surfaces are all in scope and all are release-relevant.
- Assumption: no project-specific test commands, code paths, schemas, or provider contracts are available in this run.
- Blocker: exact Web role/page/field/message matrix is missing (`BQ-001`).
- Blocker: background job schedule, retry, timeout, and failure policy are missing (`BQ-002`).
- Blocker: payment provider callback contract is missing (`BQ-003`).
- Blocker: migration source/target schema and rollback policy are missing (`BQ-004`).
- Blocker: audit report columns, filters, exports, retention, and access policy are missing (`BQ-005`).

## Project Context Inspection

- Project path: not provided.
- Context inspection mode: not available.
- Inspected files: none.
- Impact: standards are project-agnostic; future audit agent must bind test commands, paths, schemas, and provider fixtures before execution.

## Audit Environment Requirements

- Required services: Web application, API, job scheduler/queue, database, payment sandbox or callback fixture runner, reporting backend.
- Required accounts/roles: PRD-defined end user roles, admin/report viewer role, unauthorized role, service/job identity.
- Required test data: Web workflow fixtures, queued job records, signed payment callback payloads, legacy migration dataset, known audit/report event dataset.
- Required secrets/sandboxes: payment provider sandbox keys or verified signed fixtures; non-production database with snapshot/rollback support.
- Setup commands: unavailable; future audit agent must discover project commands and record them under `TE-001`.
- Known environment limitations: without project context, execution remains conditional or blocked where commands and credentials are required.

## Readiness Summary

- Status: Ready with assumptions.
- Intended primary executor: implementation audit agent or test audit agent.
- Requirements mapped: 5 major PRD areas.
- Blocked or ambiguous requirements: 5.
- Release-blocking gates: 6 (`BV-002`, `BV-003`, `BV-004`, `IA-001`, `IA-002`, `IA-003`, plus final `RG-001` gate).
- Machine-readable appendix: external file, `audit-checks.json`.
- Three-round clean-context review: completed via inline fallback; isolation approximated.

## Requirement Inventory

| Area | Requirement Surface | Audit Treatment |
| --- | --- | --- |
| Web | User-facing flows, validation, UI states, role-visible behavior | Behavior checks plus permission implementation audit |
| Background jobs | Scheduled/asynchronous processing, retry, idempotency, partial failure | Release-blocking behavior and data integrity checks |
| Payment callbacks | External provider callback validation, duplicate handling, state reconciliation | Release-blocking behavior, security, and auditability checks |
| Data migration | Legacy-to-target data movement, integrity, rollback, compatibility | Release-blocking migration rehearsal and rollback checks |
| Audit reports | Report generation, filters, permissions, source event traceability | Behavior checks plus audit event/source reconciliation |

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | Web user workflows | Verify PRD-defined Web flows, validation, states, and messages | Behavior Verification | High | Manual | Conditional | Screenshots/recordings, request IDs, record IDs | Ready |
| BV-002 | Background task processing | Verify job processing, retry, idempotency, and partial failure behavior | Behavior Verification | Blocker | Automated | Required | Job run IDs, before/after records, logs | Ready |
| BV-003 | External payment callback handling | Verify signed callbacks, invalid callbacks, duplicates, out-of-order delivery, and reconciliation | Behavior Verification | Blocker | Automated | Required | Callback fixture, HTTP response, payment and ledger records | Ready |
| BV-004 | Data migration | Verify migration rehearsal, integrity, rollback, and compatibility | Behavior Verification | Blocker | Automated | Required | Migration logs, counts, integrity checks, rollback result | Ready |
| BV-005 | Audit reports | Verify report completeness, filters, permissions, and source event traceability | Behavior Verification | High | Manual | Conditional | Report output, source event query, role evidence | Ready |
| IA-001 | Cross-surface permissions and data access | Review server-side authorization for Web/API/report/callback boundaries | Implementation Audit | Blocker | Review-only | Static fallback | Code references, permission test evidence | Ready |
| IA-002 | Payment, job, migration, and report auditability | Review durable audit logs and correlation IDs for high-risk operations | Implementation Audit | Blocker | Review-only | Static fallback | Log samples, audit records, correlation chains | Ready |
| IA-003 | Data integrity across surfaces | Review transactions, constraints, idempotency, locking, and report query integrity | Implementation Audit | Blocker | Review-only | Static fallback | Schema/code references, integrity tests | Ready |
| TE-001 | All ready audit checks | Discover and execute relevant project test commands | Test Execution | High | Blocked | Required | Command output, blocker notes | Blocked |
| RG-001 | Release approval across high-risk areas | Apply final hard fail and conclusion rules | Risk Gate | Blocker | Review-only | Not applicable | Final audit report, risk acceptance references | Ready |

## Behavior Verification Standards

### BV-001: Web User Workflows

- PRD trace: Web user workflows.
- Scenario/setup: use PRD-defined roles, pages, and seeded records.
- Steps or review method: execute each PRD-defined Web acceptance path, including valid submission, invalid input, unauthorized access, loading, empty, error, and retry states where applicable.
- Pass criteria: each Web flow reaches the expected persisted state, displays correct user feedback, prevents invalid transitions, and hides restricted data.
- Fail criteria: a core flow is missing, accepts invalid input, exposes unauthorized data, or leaves inconsistent state.
- Required evidence: screenshots or recordings, relevant request IDs, created/updated record IDs.
- Mode: Manual.
- Automation level: Recommended.
- Test execution requirement: Conditional.
- Priority: High.
- Retest scope: affected Web flow, validation path, and persistence checks.

### BV-002: Background Task Processing

- PRD trace: background task processing.
- Scenario/setup: queue/scheduler test environment with eligible and ineligible records.
- Steps or review method: trigger or simulate PRD-defined jobs and verify processing, retry, timeout/failure behavior, idempotent re-run, and cleanup.
- Pass criteria: eligible records are processed exactly once or according to PRD idempotency rules; failed work is visible and recoverable.
- Fail criteria: duplicate processing, skipped eligible records, silent failure, or irreversible inconsistent state.
- Required evidence: job run ID, before/after database records, logs with correlation IDs.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: failed job path, retry path, idempotency, and affected data integrity checks.

### BV-003: External Payment Callback Handling

- PRD trace: external payment callbacks.
- Scenario/setup: payment sandbox or signed callback fixtures.
- Steps or review method: replay valid, invalid, duplicate, stale, and out-of-order callbacks; inspect response status and resulting records.
- Pass criteria: only valid callbacks update payment state; duplicates and out-of-order events are safe; local records remain reconcilable with provider events.
- Fail criteria: unsigned callbacks are accepted, payment state is double-applied, money state is wrong, or reconciliation evidence is missing.
- Required evidence: callback payload fixture, HTTP response, payment record ID, ledger or audit record ID.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: callback verification, idempotency, state transition, and reconciliation evidence.

### BV-004: Data Migration

- PRD trace: data migration.
- Scenario/setup: representative pre-migration dataset, backup, and rollback rehearsal environment.
- Steps or review method: run migration rehearsal and compare record counts, checksums, referential integrity, rollback, and backward compatibility.
- Pass criteria: no data loss, corruption, duplicate irreversible changes, or broken compatibility.
- Fail criteria: unmapped data, failed integrity check, unsafe rollback, or incompatible old/new behavior without accepted migration plan.
- Required evidence: migration command log, before/after counts, integrity check output, rollback rehearsal result.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: full migration rehearsal, rollback, and affected Web/job/payment/report flows.

### BV-005: Audit Reports

- PRD trace: audit reports.
- Scenario/setup: known source event dataset with users, callbacks, jobs, and migration history.
- Steps or review method: generate reports and compare displayed/exported data with source events and permission rules.
- Pass criteria: report data is complete, filtered correctly, permissioned correctly, and traceable to source audit events.
- Fail criteria: report omits required events, leaks restricted data, misstates state, or cannot be reconciled.
- Required evidence: report screenshot/export, source event query, role used for access test.
- Mode: Manual.
- Automation level: Recommended.
- Test execution requirement: Conditional.
- Priority: High.
- Retest scope: report generation, permissions, filters, and underlying event capture.

## Implementation Audit Standards

### IA-001: Cross-Surface Permissions And Data Access

- PRD trace: Web, reports, callbacks, and service boundaries.
- Review method: inspect server-side authorization for routes, APIs, reports, background task scope, and callback trust boundaries.
- Pass criteria: authorization is enforced server-side and cannot be bypassed through direct API access or UI-only controls.
- Fail criteria: role checks are missing, client-only, inconsistent, or permit privilege escalation.
- Required evidence: code references, permission test results, static fallback notes.
- Test coverage requirement: automated or manual permission tests for every protected core path.
- Static fallback: inspect middleware/policies/controllers and identify uncovered paths.
- Priority: Blocker.
- Retest scope: all affected protected paths.

### IA-002: Auditability And Observability

- PRD trace: payment callbacks, background jobs, migration, and audit reports.
- Review method: inspect logs, audit events, metrics, trace IDs, and report source records.
- Pass criteria: high-risk operations produce durable evidence with actor/source, timestamp, correlation ID, before/after state where relevant, and failure reason.
- Fail criteria: critical operation lacks audit log, correlation ID, or records needed for investigation.
- Required evidence: log samples, audit event records, correlation ID chain.
- Test coverage requirement: tests or static evidence for successful and failed high-risk operations.
- Static fallback: inspect logging/audit call sites and storage schema.
- Priority: Blocker.
- Retest scope: observability for all affected high-risk paths.

### IA-003: Cross-Surface Data Integrity

- PRD trace: Web writes, jobs, payment callbacks, migration, and report sources.
- Review method: inspect schemas, constraints, transactions, idempotency keys, locking, and report queries.
- Pass criteria: critical invariants cannot be violated by duplicate callbacks, concurrent jobs, failed migrations, or report query drift.
- Fail criteria: money/data state relies on non-atomic logic, missing constraints, unsafe concurrency, or unverified report aggregations.
- Required evidence: schema/code references, concurrency or idempotency test evidence.
- Test coverage requirement: automated coverage or documented static proof for Blocker data paths.
- Static fallback: inspect transaction boundaries, constraints, unique keys, and reconciliation queries.
- Priority: Blocker.
- Retest scope: affected flow and dependent reports.

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | To be discovered from project test configuration | All Ready checks | Required | Command, timestamp, result, logs | Static verification of tests, fixtures, mocks, and assertions; blocker must name missing command/environment |
| TE-002 | Payment callback test suite or fixture replay | BV-003, IA-002, IA-003 | Required | Callback replay output and resulting records | Provider contract review plus signed fixture evidence |
| TE-003 | Migration rehearsal command | BV-004, IA-003 | Required | Migration logs, counts, checksums, rollback result | Block release unless non-production rehearsal evidence exists |
| TE-004 | Report permission and reconciliation tests | BV-005, IA-001, IA-002 | Conditional | Report output, source queries, role evidence | Static review of report queries and access policy |

## Risk Gates And Hard Fail Conditions

- Any `Blocker` check fails.
- Any `Blocker` check is `Blocked` or `Not Run` without sufficient substitute evidence.
- A core PRD flow has no audit coverage.
- Payment callback signature, idempotency, or reconciliation behavior is missing.
- Migration rehearsal shows data loss, corruption, unsafe rollback, or unaccepted incompatibility.
- Background jobs can silently fail, duplicate work, or corrupt state.
- Report access leaks restricted data or report output cannot be reconciled to source events.
- High-risk permission, data, payment, privacy, or audit-log behavior lacks implementation audit coverage.
- Required test commands are not run and no blocker is recorded.
- Evidence cannot be traced to audit check IDs.

## Required Evidence Rules

- Every evidence item must reference one or more audit check IDs.
- Failed evidence must reference a defect report ID.
- API/log/database evidence must include request parameters, query conditions, correlation IDs, or record IDs when relevant.
- Screenshots and recordings must identify role, environment, and data record under test.
- Static fallback evidence must identify inspected files and explain why execution was blocked.

## Defect Report Format

Use the template in [audit-report-template.md](audit-report-template.md). Required fields:

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

## Status And Final Conclusion Rules

- Check statuses: Pass / Fail / Blocked / Not Run / Not Applicable.
- Final conclusions: Approved / Approved with Risks / Rejected / Blocked.
- `Blocked` and `Not Run` are not passes.
- `Approved`: all `Blocker` and `High` checks pass, and remaining risks do not aggregate into release risk.
- `Approved with Risks`: no `Blocker` failure; remaining `High`/`Medium` issues have explicit acceptance or deferral rationale.
- `Rejected`: any `Blocker` check fails or a critical PRD behavior is missing.
- `Blocked`: critical `Blocker`/`High` checks cannot be verified and substitute evidence is insufficient.

## Retest And Regression Rules

- Retest the original failed check.
- Retest related checks in the same PRD area.
- Retest affected regression paths across Web, jobs, payment callbacks, migration, and reports when shared data changes.
- `Blocker` and `High` fixes require related regression execution or documented blocker with substitute evidence.
- Retest reports must reference defect IDs, audit check IDs, evidence IDs, and final status.

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed requirements and checks as deprecated; do not reuse IDs.
- Re-evaluate risk levels and hard fail conditions.
- Rerun three clean-context reviews when changes affect core flows, permissions, data integrity, integrations, irreversible operations, or risk levels.
- For small non-behavioral wording changes, run a local update plus quality gate.

## Three-Round Clean-Context Review

- Record: [clean-context-review-record.md](clean-context-review-record.md)
- Review mode: Inline fallback.
- Context isolation: Approximated.
- Round 1 focus: PRD coverage completeness and traceability.
- Round 2 focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations.
- Round 3 focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling.
- Result: completed; accepted findings were merged into these standards.

## Final Quality Gate

- Ready for post-development audit: Yes, with assumptions and blocked project-specific details.
- Final conclusion rule ready: Yes.
- Hard fail conditions complete: Yes.
- Machine-readable auxiliary file produced: Yes, [audit-checks.json](audit-checks.json).
- Conditions before use: bind the standards to the full PRD, project test commands, provider callback contract, migration schema, and report specification.
- Checks that must pass before release: all `Blocker` checks and all `High` checks unless risk acceptance is explicit and allowed by release governance.

