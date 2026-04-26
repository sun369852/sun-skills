# Refund Approval Quality Audit Standards

## Source And Scope

- Source PRD: `D:\sun-skills\prd-to-tech-design-review-workspace\fixtures\refund-app\docs\prd\refund-approval.md`
- Supporting context: bounded inspection of refund fixture code and technical design; PRD remains authoritative.
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents.
- In scope: high-value refund approval, permissions, approval status lifecycle, refund idempotency, audit logs, notifications, history display, and third-party refund processor failure handling.
- Out of scope: rewriting the PRD, choosing implementation architecture, replacing the existing refund processor, binary evidence storage, multi-currency behavior.

## Assumptions

- The requested eval path did not exist before this run; outputs were created only under the requested `with_skill\outputs` directory.
- The available PRD is the refund approval fixture listed above. If another PRD was intended, rerun coverage analysis before using these standards.
- Third-party refund failure and refund idempotency are high-risk derived quality standards because approved refunds trigger an external processor and duplicate refunds would create payment loss, even though the PRD only names `failed` status and the existing processor.
- Notification channel, delivery SLA, retry policy, and message content are not defined by the PRD. Exact notification delivery tests are blocked; event generation and recipient correctness remain auditable.

## Project Context Inspection

| File | Reason Inspected | Impact On Audit Standards |
| --- | --- | --- |
| `docs/prd/refund-approval.md` | Source PRD | Defines required roles, approval threshold, status lifecycle, audit, and history requirements. |
| `docs/design/refund-approval-tech-design.md` | Supporting context only | Clarifies likely APIs, legacy behavior, idempotent approval/rejection expectations, processor gate, and notification ambiguity. |
| `src/api/refunds.ts` | Existing API/model surface | Current status type lacks approval states and `createRefund` immediately returns `processing`; audit must verify this is changed for high-value refunds. |
| `src/pages/refunds.tsx` | Existing UI/history entry point | Current page only shows generic history text; audit must verify role-aware approval queue and history status display. |

## Audit Environment Requirements

- Required services: application under audit, persistence layer, existing refund processor or test double, notification service or test double, audit log storage.
- Required accounts/roles: support agent, support manager, finance operator, unauthorized/non-manager user.
- Required test data: refunds at `9999` cents, `10000` cents, above `10000` cents, pending approvals, rejected approvals, approved refunds, processor failure case, duplicate approval/retry case, legacy refund records.
- Required secrets/sandboxes: third-party refund processor sandbox or deterministic mock; notification sandbox or captured event sink.
- Setup commands: not available in fixture. Future audit agent must run project test commands if present; if absent, record blocker and perform static fallback.
- Known limitations: PRD does not define notification channel/SLA/content, idempotency key shape, concurrency semantics, or third-party retry policy.

## Readiness Summary

- Status: Ready with assumptions.
- Intended primary executor: Implementation audit agent and test audit agent.
- Requirements mapped: 11.
- Blocked or ambiguous areas: 5.
- Release-blocking gates: 8.
- Machine-readable appendix: external file `audit-checks.json`.
- Ready for post-development audit use: Yes, with blocked questions treated as non-passing for unconditional release.

## Requirement Inventory

1. Refunds under 100 USD can be processed immediately.
2. Refunds at or above 100 USD require manager approval.
3. Support agents can add reason and evidence.
4. Managers can see pending approvals with amount, customer, order, reason, and evidence.
5. Managers can approve or reject with comments.
6. Approved requests trigger the existing refund processor.
7. Rejected requests notify the support agent.
8. Approval and rejection actions are audited.
9. Existing refund history shows approval status.
10. Status lifecycle includes `draft`, `pending_approval`, `approved`, `rejected`, `processing`, `completed`, `failed`.
11. High-value refund requests cannot bypass approval.

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | Under 100 USD immediate processing | Verify `< 10000` cents enters existing processing path without approval. | Behavior Verification | High | Automated | Required | API response, processor invocation record | Ready |
| BV-002 | High-value refunds require approval; cannot bypass | Verify `>= 10000` cents creates `pending_approval` and does not call processor before approval. | Behavior Verification | Blocker | Automated | Required | API trace, DB record, processor mock assertion | Ready |
| BV-003 | Agent reason and evidence | Verify creation captures reason and evidence references for audit/manager review. | Behavior Verification | High | Automated | Required | Request/response, persisted record | Ready |
| BV-004 | Manager pending queue details | Verify pending queue shows amount, customer, order, reason, and evidence. | Behavior Verification | High | Manual/Automated | Required | UI screenshot or API response | Ready |
| BV-005 | Manager approval with comment | Verify manager approval from `pending_approval` records comment, transitions state, and triggers processor. | Behavior Verification | Blocker | Automated | Required | API trace, DB state, audit event, processor record | Ready |
| BV-006 | Manager rejection with comment | Verify manager rejection from `pending_approval` records comment, does not trigger processor, and emits support-agent notification. | Behavior Verification | Blocker | Automated | Required | API trace, DB state, audit event, notification event | Ready |
| BV-007 | Status lifecycle | Verify only allowed status transitions occur and invalid transitions fail safely. | Behavior Verification | Blocker | Automated | Required | State transition test output | Ready |
| BV-008 | Refund history approval status | Verify history displays all PRD statuses and approval status. | Behavior Verification | High | Manual/Automated | Required | UI screenshot/API response | Ready |
| BV-009 | Refund idempotency | Verify repeated approval/rejection/submission retries cannot duplicate refund processing or audit decisions. | Behavior Verification | Blocker | Automated | Required | Duplicate request traces, single processor/audit record | Ready |
| BV-010 | Third-party refund failure | Verify processor failure after approval results in `failed` state without losing approval/audit history. | Behavior Verification | Blocker | Automated | Conditional | Processor failure mock, DB state, logs | Ready |
| IA-001 | API authorization | Verify API enforces role permissions independent of UI controls. | Implementation Audit | Blocker | Review-only | Static fallback | Code refs, auth tests | Ready |
| IA-002 | Audit logs | Verify approval and rejection audit writes are atomic with status changes. | Implementation Audit | Blocker | Review-only | Static fallback | Transaction/code refs, audit records | Ready |
| IA-003 | Processor gate | Verify direct processor entry points enforce approval requirement. | Implementation Audit | Blocker | Review-only | Static fallback | Code refs, tests | Ready |
| IA-004 | Notification implementation | Verify rejection notification targets support agent and is emitted after rejection commit. | Implementation Audit | High | Review-only | Static fallback | Code refs, event/log record | Ready |
| BQ-001 | Notification details | Channel, SLA, retry, and exact content are undefined. | Blocked Question | High | Blocked | Not applicable | PRD clarification | Blocked |
| BQ-002 | Idempotency contract | Idempotency key and concurrent action rules are undefined. | Blocked Question | Blocker | Blocked | Not applicable | PRD/technical clarification | Blocked |
| BQ-003 | Third-party retry/reconciliation | Retry policy and reconciliation ownership are undefined. | Blocked Question | High | Blocked | Not applicable | PRD/technical clarification | Blocked |

## Behavior Verification Standards

### BV-001: Low-Value Refund Immediate Processing

- PRD trace: "Refunds under 100 USD can be processed immediately."
- Scenario/setup: support agent submits a refund with amount `9999` cents.
- Test data: order ID, customer, reason, optional evidence.
- Steps or review method: create refund through public API/UI path; observe returned status and processor call.
- Pass criteria: refund enters `processing` or existing immediate processor handoff path; no manager approval requirement blocks the flow.
- Fail criteria: under-100 refund is forced into approval, or processor is not invoked without documented PRD-compatible reason.
- Required evidence: `BV-001` API trace, persisted refund record, processor invocation or queue record.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: High.
- Retest scope: create refund path, threshold boundary checks, processor handoff tests.

### BV-002: High-Value Refund Cannot Bypass Approval

- PRD trace: "Refunds at or above 100 USD require manager approval" and "High-value refund requests cannot bypass approval."
- Scenario/setup: support agent submits refunds at `10000` cents and above.
- Steps or review method: create high-value refund; attempt direct processor invocation if such entry point exists.
- Pass criteria: refund is `pending_approval`; processor is not invoked before manager approval; any direct bypass attempt is denied or ignored with a recorded failure.
- Fail criteria: high-value refund reaches `processing`, `completed`, or external processor before manager approval.
- Required evidence: `BV-002` request/response, DB state, processor mock showing zero pre-approval calls.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: threshold logic, API authorization, processor gate.

### BV-003: Reason And Evidence Capture

- PRD trace: "Support agents can add reason and evidence."
- Scenario/setup: support agent creates refund with reason and evidence references.
- Pass criteria: reason and evidence are accepted, persisted, and visible to manager review/history surfaces.
- Fail criteria: reason or evidence is dropped, hidden from manager review, or mutable in a way that obscures submitted evidence.
- Required evidence: `BV-003` request payload, stored record, manager queue/history display.
- Mode: Automated.
- Automation level: Required for API; recommended for UI.
- Test execution requirement: Required.
- Priority: High.
- Retest scope: create request, manager queue, history view.

### BV-004: Manager Pending Approval Queue

- PRD trace: "Managers see pending approvals with amount, customer, order, reason, and evidence."
- Scenario/setup: manager opens pending approvals with at least one pending high-value refund.
- Pass criteria: each row/item includes amount, customer, order, reason, and evidence; non-pending refunds are excluded.
- Fail criteria: required fields missing, evidence not inspectable, non-manager can access manager-only queue.
- Required evidence: `BV-004` screenshot or API response, role used, pending record ID.
- Mode: Manual or Automated.
- Automation level: Recommended.
- Test execution requirement: Required.
- Priority: High.
- Retest scope: manager queue API/UI and permission checks.

### BV-005: Approval State Transition And Processor Trigger

- PRD trace: "Managers can approve ... with comments" and "Approved requests trigger the existing refund processor."
- Scenario/setup: support manager approves a `pending_approval` refund with comment.
- Pass criteria: status transitions through approved/processor handoff as implemented; manager comment and actor metadata are persisted; audit event is written; processor is triggered exactly once after approval is durable.
- Fail criteria: approval from wrong state succeeds, comment/actor missing, audit missing, processor triggered before durable approval, or duplicate processor calls occur.
- Required evidence: `BV-005` API trace, DB status/approval fields, audit event, processor invocation.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: approval endpoint/action, audit write, processor integration.

### BV-006: Rejection State Transition And Notification

- PRD trace: "Managers can ... reject with comments" and "Rejected requests notify the support agent."
- Scenario/setup: support manager rejects a `pending_approval` refund with comment.
- Pass criteria: refund becomes `rejected`; manager comment and actor metadata are persisted; audit event is written; processor is not triggered; support-agent notification event is emitted after durable rejection.
- Fail criteria: rejection lacks comment, processor is triggered, audit missing, notification targets wrong recipient, or rejection can occur from non-pending status.
- Required evidence: `BV-006` API trace, DB record, audit event, notification event, processor non-invocation.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: rejection endpoint/action, audit write, notification path.

### BV-007: Approval Status Lifecycle

- PRD trace: status lifecycle list.
- Scenario/setup: exercise valid and invalid transitions across `draft`, `pending_approval`, `approved`, `rejected`, `processing`, `completed`, and `failed`.
- Pass criteria: implementation supports all PRD states, displays them distinctly, and prevents invalid transitions such as `rejected -> processing` or non-pending approval/rejection.
- Fail criteria: states are collapsed, missing, or invalid transitions mutate refund state.
- Required evidence: `BV-007` state transition tests and history/status display evidence.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: status model, API transition handlers, UI status rendering.

### BV-008: Refund History Approval Status

- PRD trace: "Existing refund history shows approval status."
- Scenario/setup: finance operator and support user view refund history containing all approval outcomes.
- Pass criteria: history shows approval status for pending, approved, rejected, processing, completed, and failed refunds; legacy records remain visible.
- Fail criteria: approval status hidden, ambiguous, or mapped incorrectly to generic processing state.
- Required evidence: `BV-008` screenshot/API response with record IDs and roles.
- Mode: Manual or Automated.
- Automation level: Recommended.
- Test execution requirement: Required.
- Priority: High.
- Retest scope: history API/UI and status renderer.

### BV-009: Refund Idempotency And Duplicate Action Safety

- PRD trace: derived quality standard from high-risk refund processor trigger and manager approval actions.
- Scenario/setup: repeat create/approve/reject calls and simulate concurrent manager actions.
- Pass criteria: duplicate approval/retry cannot enqueue duplicate refunds; duplicate rejection cannot emit duplicate final decisions; conflicting approve/reject attempts result in one durable terminal decision and auditable safe failure for the loser.
- Fail criteria: multiple processor calls for one approved refund, multiple terminal audit events, or final state differs from the single accepted manager action.
- Required evidence: `BV-009` duplicate request traces, correlation/idempotency identifiers if available, DB/audit counts, processor invocation count.
- Mode: Automated.
- Automation level: Required.
- Test execution requirement: Required.
- Priority: Blocker.
- Retest scope: approval/rejection handlers, persistence transaction/concurrency controls, processor enqueue logic.

### BV-010: Third-Party Refund Failure After Approval

- PRD trace: status lifecycle includes `failed`; approved requests trigger existing refund processor. Derived quality standard for external processor failure.
- Scenario/setup: approve a high-value refund and force processor failure/timeout through sandbox or mock.
- Pass criteria: refund reaches `failed` or documented failed processor state; approval and audit history remain intact; no duplicate refund is issued on retry; failure is visible in history and logs.
- Fail criteria: approval audit is lost, refund remains stuck without diagnosable state, retry duplicates refund, or user-facing history hides failure.
- Required evidence: `BV-010` processor failure trace, DB state, audit event, logs/correlation ID, history view.
- Mode: Automated when mock/sandbox exists; otherwise manual with static fallback.
- Automation level: Required when processor test double is available.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: processor integration, failure handling, history/status display, retry/idempotency.

## Implementation Audit Standards

### IA-001: Server-Side Permission Enforcement

- PRD trace: role definitions and manager approval scope.
- Implementation area: API authorization, route handlers, policy checks.
- Review method: inspect approval/rejection and pending-list endpoints/actions; verify tests cover non-manager denial.
- Pass criteria: support agent cannot approve/reject; finance operator cannot approve/reject unless separately authorized by PRD update; UI-hidden controls are not the only enforcement.
- Fail criteria: role checks missing at API/server boundary or bypassable by direct request.
- Required evidence: `IA-001` code references, auth test results, denied request trace.
- Test coverage requirement: automated negative permission tests required for Blocker approval/rejection paths.
- Static fallback: code review of server policy and route/action guards.
- Priority: Blocker.
- Retest scope: all approval mutation endpoints/actions.

### IA-002: Atomic Audit Logging

- PRD trace: "Approval and rejection actions are audited."
- Implementation area: transaction/persistence/audit event writes.
- Review method: inspect whether status update and audit event are committed atomically or have compensating failure handling.
- Pass criteria: no approved/rejected state can exist without matching audit event containing action, actor, refund ID, comment when required, and timestamp.
- Fail criteria: audit write is best-effort without recovery, missing actor/comment, or failures leave unaudited terminal state.
- Required evidence: `IA-002` code references, transaction evidence, audit records for approval and rejection.
- Test coverage requirement: tests for audit creation and audit failure behavior.
- Static fallback: inspect transaction or unit-of-work boundaries.
- Priority: Blocker.
- Retest scope: approval/rejection persistence and audit storage.

### IA-003: Processor Approval Gate

- PRD trace: approved requests trigger existing refund processor; high-value cannot bypass approval.
- Implementation area: refund processor entry points, queue producers/consumers, status checks.
- Review method: inspect direct and indirect processor invocation paths.
- Pass criteria: high-value refunds are processor-eligible only after approval; low-value path remains compatible.
- Fail criteria: any code path can process high-value refund without approved status or equivalent durable approval proof.
- Required evidence: `IA-003` code references, processor gate tests, queue/event samples.
- Test coverage requirement: automated tests for processor non-invocation before approval and exactly-once invocation after approval.
- Static fallback: trace all processor callers.
- Priority: Blocker.
- Retest scope: create path, approve path, processor workers.

### IA-004: Notification Emission

- PRD trace: "Rejected requests notify the support agent."
- Implementation area: notification service/event producer.
- Review method: inspect rejection flow and notification event.
- Pass criteria: support-agent recipient is derived from refund creator/owner; notification is emitted after rejection commit; failures are logged or retriable according to existing project pattern.
- Fail criteria: notification goes to wrong role, emits before rollback-prone transaction, or failure is silent.
- Required evidence: `IA-004` event/log record, code references, recipient ID.
- Test coverage requirement: notification event test or static fallback if service unavailable.
- Static fallback: code review plus captured event sink if tests cannot execute.
- Priority: High.
- Retest scope: rejection flow and notification integration.

### IA-005: Status Model And Data Compatibility

- PRD trace: status lifecycle and history display requirements.
- Implementation area: type/schema/model/migration/history API.
- Review method: inspect model/schema/status enum and migration/backward compatibility handling.
- Pass criteria: all seven PRD statuses are representable and exposed to history; existing under-100 refund behavior is preserved.
- Fail criteria: new states missing, legacy records break, or statuses are collapsed into `processing`.
- Required evidence: `IA-005` code refs, migration/schema evidence, history response.
- Test coverage requirement: status serialization/rendering tests.
- Static fallback: model/schema review.
- Priority: High.
- Retest scope: model, API serialization, history UI.

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | Project unit tests for refund create/approve/reject/status logic | BV-001, BV-002, BV-005, BV-006, BV-007, BV-009 | Required | command, timestamp, pass/fail log | Static inspect test files and record blocker for missing runnable command. |
| TE-002 | API/integration tests with role accounts and processor mock | BV-002, BV-005, BV-006, BV-010, IA-001, IA-003 | Required | request traces, DB records, mock call counts | Static route/policy review plus documented environment blocker. |
| TE-003 | UI/e2e tests or manual scripted review for manager queue/history | BV-004, BV-008 | Conditional | screenshots/recordings, role used, record IDs | Static component review plus API evidence. |
| TE-004 | Audit log and notification tests | BV-006, IA-002, IA-004 | Required | audit records, notification event/log, correlation IDs | Static transaction/event review plus blocker if event sink unavailable. |
| TE-005 | Processor failure/idempotency tests | BV-009, BV-010, IA-003 | Conditional | failure mock output, single invocation counts, final DB state | Static review of retry/idempotency design and mark as blocked for release if no substitute evidence. |

## API, Data, And State Standards

- Boundary amount behavior must be tested at `9999`, `10000`, and at least one value above `10000` cents.
- State transitions must be explicit and auditable for `pending_approval -> approved -> processing -> completed|failed` and `pending_approval -> rejected`.
- Non-pending approve/reject actions must fail safely without changing state, triggering processor, or writing misleading terminal audit events.
- Duplicate requests and concurrent approval/rejection attempts must produce one durable outcome for a refund.
- Processor failure must preserve approval/audit metadata and expose failure in history.

## Permissions, Security, And Privacy Standards

- API/server authorization is mandatory for pending list, approve, and reject actions.
- Support agents can create refund requests and view permitted history but cannot approve/reject.
- Support managers can view pending approvals and approve/reject with comments.
- Finance operators can view history, approval status, and audit metadata, but approval mutation access is blocked unless PRD changes.
- Evidence and customer/order details must not be exposed to unauthorized users. Privacy-specific masking rules are blocked because the PRD does not define them.

## Integration And External Dependency Standards

- Existing refund processor must not receive high-value refunds before manager approval.
- Processor invocation after approval must be exactly once per approved refund under retry/concurrency conditions.
- Processor failure must lead to diagnosable `failed` handling and retain audit trail.
- Rejection notification must target the support agent after rejection is durable.
- Manager notification for pending approvals is optional in supporting design and not required by the PRD.

## Required Evidence For Future Review

- Test results: executed commands, timestamps, environment, pass/fail output.
- API traces: request parameters, authenticated role, response status/body, correlation IDs.
- Database records: refund ID, amount, status, approval fields, audit event IDs.
- Processor evidence: queue/event/invocation count, failure simulation output.
- Notification evidence: recipient, event ID, timestamp, linked refund ID.
- UI evidence: screenshots/recordings for manager queue and refund history with record IDs.
- Code references: permission guards, transaction/audit writes, processor gate, status model.

Evidence rules:

- Every evidence item must reference one or more audit check IDs.
- Failed evidence must reference a defect report ID.
- `Blocked` and `Not Run` are not passes.

## Defect Report Format

```yaml
defect_id:
audit_check_id:
prd_trace:
failure_summary:
expected_result:
actual_result:
reproduction_steps_or_review_method:
evidence_references:
affected_files_apis_logs_or_records:
impact_scope:
suggested_severity: Blocker | High | Medium | Low
release_blocking: true | false
recommended_fix_direction:
retest_scope:
```

## Status And Final Conclusion Rules

- Check statuses: Pass, Fail, Blocked, Not Run, Not Applicable.
- Final conclusions:
  - Approved: all Blocker and High checks pass; remaining issues do not aggregate into release risk.
  - Approved with Risks: no Blocker failure; High/Medium issues have explicit risk acceptance.
  - Rejected: any Blocker check fails or a critical PRD behavior is missing.
  - Blocked: critical Blocker/High checks cannot be verified and substitute evidence is insufficient.

## Hard Fail Conditions

- Any Blocker check fails.
- Any Blocker check is Blocked or Not Run without sufficient substitute evidence.
- High-value refunds can reach processor without approval.
- API/server permission checks for approval/rejection are missing.
- Approval or rejection can occur without audit event.
- Approved refund can trigger duplicate third-party refund processing.
- Processor failure loses audit trail or produces an inconsistent hidden state.
- Evidence cannot be traced to audit check IDs.
- Required test commands are not run and no blocker is recorded.

## Retest And Regression Rules

- Retest the original failed check plus related checks in the same PRD area.
- For permission fixes, rerun all approval/rejection role-negative tests.
- For processor or idempotency fixes, rerun threshold, approval, duplicate action, and failure-path tests.
- For audit fixes, rerun approval and rejection transaction/audit tests.
- For notification fixes, rerun rejection flow and recipient verification.
- Blocker/High fixes require related regression execution or a documented blocker.

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks and mark removed checks as deprecated.
- Rerun three clean-context reviews when changes affect core flows, permissions, data integrity, integrations, irreversible operations, or risk levels.
- For small non-behavioral wording changes, run local update plus quality gate.

## Three-Round Clean-Context Review Record

- Review mode: Inline fallback; independent subagent execution was not available in this environment.
- Context isolation: Approximated. Each pass used the same PRD, bounded context summary, and admitted draft; previous findings were not used until merge.
- Round 1 status: Completed. Focus: PRD coverage completeness and traceability.
- Round 2 status: Completed. Focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations.
- Round 3 status: Completed. Focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling.

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| Add explicit threshold boundary checks at `9999` and `10000` cents. | Round 1 | Accepted | Directly traces to under/at-or-above 100 USD PRD rule. |
| Treat non-manager approval/rejection as server-side Blocker, not UI-only check. | Round 1, Round 2 | Accepted | Permission failure can cause unauthorized refunds. |
| Add invalid status transition checks for non-pending approve/reject. | Round 1, Round 2 | Accepted | PRD lifecycle requires controlled state flow. |
| Add idempotency/duplicate processing gate. | Round 2 | Accepted as derived quality standard | Payment/refund duplicate processing is high-risk and implied by processor trigger. |
| Add third-party failure handling for approved refunds. | Round 2 | Accepted as derived quality standard | PRD includes `failed` status and approved processor trigger. |
| Exact notification content/SLA cannot be pass/fail without PRD clarification. | Round 3 | Accepted as blocked question | PRD only requires support-agent notification. |
| Require specific test commands. | Round 3 | Rejected | Fixture has no package/test configuration; standards require commands if available and static fallback otherwise. |
| Require arbitrary coverage percentage. | Round 3 | Rejected | Skill rules prohibit arbitrary coverage percentages; evidence for high-risk paths is required instead. |

## Blocked Checks And Open Questions

| Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- |
| BQ-001 Notifications | What channel, content, SLA, and retry policy are required for rejection notifications? | Exact delivery/content tests cannot be unconditional. | Product owner / engineering lead |
| BQ-002 Idempotency | What idempotency key or concurrency contract should create/approve/reject expose? | Auditors can verify no duplicates but cannot enforce exact API contract. | Backend lead |
| BQ-003 Processor failure | What retry/reconciliation behavior is required after third-party failure? | Failure visibility can be tested; retry policy remains conditional. | Product owner / payment lead |
| BQ-004 Evidence | Are evidence values URLs, uploaded files, or another reference type? | Audit can verify persistence/display only against implemented contract. | Product owner |
| BQ-005 Privacy | What customer/evidence masking rules apply by role? | Unauthorized exposure can be tested, exact masking cannot. | Security / product owner |

## Final Quality Gate

- Ready for post-development audit: Yes.
- Final conclusion rule ready: Yes.
- Hard fail conditions complete: Yes.
- Conditions before use: confirm this is the intended PRD; fill actual project test commands; resolve or explicitly accept blocked questions before unconditional release approval.
- Checks that must pass before release: BV-002, BV-005, BV-006, BV-007, BV-009, BV-010 or approved substitute evidence, IA-001, IA-002, IA-003.

