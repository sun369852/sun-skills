# Approval Flow Quality Audit Standards

## Source And Scope

- Source PRD: pasted brief in evaluation prompt.
- Source summary: users can configure approval flows; approval flows support multi-person approval, conditional branches, and business actions after approval. The brief does not define branch rules, approval order, failure retry, or permission boundaries.
- Supporting context: none.
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents.
- In scope: approval-flow configuration, multi-person approval, conditional branching, post-approval business action triggering, blocked semantic questions that prevent reliable release audit.
- Out of scope: writing the PRD, choosing product semantics, technical design, implementation task decomposition, live test execution.

## Project Context Inspection

- Project path: not provided.
- Context inspection mode: Not available.
- Inspected files: none.

| File | Reason Inspected | Impact On Audit Standards |
| --- | --- | --- |
| N/A | No project path or implementation context was provided. | Test commands, API routes, data schemas, and auth policy locations must be resolved by the future audit agent. |

## Audit Environment Requirements

- Required services: application under audit, approval-flow configuration UI or API, approval execution service, business-action target service.
- Required accounts/roles: flow administrator/configurator, approver, requester/initiator, unauthorized user. Exact role matrix is blocked by `BQ-004`.
- Required test data: one approval flow with multiple approvers, one flow with at least one conditional branch, one flow that triggers a business action after approval. Exact branch data is blocked by `BQ-001`.
- Required secrets/sandboxes: any external or internal target needed for post-approval business actions.
- Setup commands: project-specific commands are not available; see `TE-001`.
- Known environment limitations: no project path, no executable test command, no API/schema/auth references.

## Readiness Summary

- Status: Blocked
- Draft admission: Admitted - Blocked
- Intended primary executor: Implementation audit agent / Test audit agent
- Requirements mapped: 4
- Blocked or ambiguous requirements: 4
- Release-blocking gates: 6
- Machine-readable appendix: Included

## Draft Admission Record

- Initial draft result: Rejected - Rewrite.
- Rejection reason: the first pass could list feature areas, but any executable pass/fail standard for conditional branches, approval order, retry behavior, or permission boundary would have invented missing product semantics.
- Rewrite count used: 1 of 2.
- Rewritten draft result: Admitted - Blocked.
- Reason admitted: the artifact now has stable IDs, traceability, behavior and implementation layers, evidence rules, hard fail conditions, and explicit blocked questions.
- Reason blocked: unresolved Blocker product semantics remain for branch rules, approval order, failure retry, and permission boundaries. Per canonical readiness rules, overall status is `Blocked`, not `Ready with assumptions`.

## Requirement Inventory

| ID | Requirement | Coverage Decision |
| --- | --- | --- |
| R-001 | User can configure approval flows. | Covered, but permission scope and valid configuration constraints are blocked. |
| R-002 | Approval flows support multi-person approval. | Covered, but approval order and completion rule are blocked. |
| R-003 | Approval flows support conditional branches. | Covered as blocked because branch rule language, precedence, default path, and conflict handling are undefined. |
| R-004 | Approval passing triggers business actions. | Covered, but action timing, idempotency, failure retry, and partial failure handling are blocked. |

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | R-001 | Verify authorized users can create, edit, activate, and view approval-flow configuration only within defined permission boundaries. | Behavior Verification | Blocker | Blocked | Not applicable | `EV-001`, `BQ-004` | Blocked |
| BV-002 | R-002 | Verify multi-person approval completion follows the PRD-defined approval order and completion rule. | Behavior Verification | Blocker | Blocked | Not applicable | `EV-002`, `BQ-002` | Blocked |
| BV-003 | R-003 | Verify conditional branch routing follows defined branch predicates, precedence, fallback, and conflict behavior. | Behavior Verification | Blocker | Blocked | Not applicable | `EV-003`, `BQ-001` | Blocked |
| BV-004 | R-004 | Verify approved flows trigger the configured business action exactly according to defined timing and retry semantics. | Behavior Verification | Blocker | Blocked | Not applicable | `EV-004`, `BQ-003` | Blocked |
| IA-001 | R-001, R-004 | Review persistence and state transitions for configured flows, approval records, and triggered actions. | Implementation Audit | High | Review-only | Static fallback | `EV-005` | Ready |
| IA-002 | R-001, R-002, R-003, R-004 | Review audit logs/history for configuration changes, approvals, branch decisions, and business-action attempts. | Implementation Audit | High | Review-only | Static fallback | `EV-006` | Ready |
| IA-003 | R-001 | Review authorization enforcement for configuration and approval operations once role matrix is defined. | Implementation Audit | Blocker | Blocked | Not applicable | `EV-007`, `BQ-004` | Blocked |
| IA-004 | R-004 | Review idempotency and duplicate-action prevention for post-approval business actions once retry semantics are defined. | Implementation Audit | Blocker | Blocked | Not applicable | `EV-008`, `BQ-003` | Blocked |
| TE-001 | R-001-R-004 | Execute project-specific automated and static checks for mapped audit IDs. | Test Execution | High | Blocked | Static fallback | `EV-009` | Blocked |
| RG-001 | R-001-R-004 | Reject release if any Blocker semantic question remains unresolved or any Blocker check fails. | Risk Gate | Blocker | Review-only | Not applicable | `EV-010` | Ready |

## Behavior Verification Standards

### BV-001: Approval Flow Configuration Permissions

- PRD trace: R-001.
- Scenario/setup: an approval-flow configuration surface exists.
- Test data:
  - Positive cases: role that is allowed to configure approval flows.
  - Negative cases: role that must not configure approval flows.
  - Boundary cases: user with approval permission but no configuration permission.
  - Stateful cases: create, update, activate/deactivate, and view history if supported.
  - Cleanup requirements: remove or deactivate test flows.
- Steps or review method: blocked until the PRD defines who may configure flows and which operations each role may perform.
- Pass criteria: cannot be finalized until `BQ-004` is answered.
- Fail criteria: any user outside the defined permission boundary can create, modify, activate, delete, or inspect restricted approval flows.
- Required evidence: `EV-001` role matrix, operation list, test accounts, request/UI evidence, and access-denial evidence.
- Mode: Blocked.
- Automation level: Blocked.
- Test execution requirement: Not applicable until unblocked.
- Priority: Blocker.
- Retest scope: all configuration operations and related authorization checks.
- Notes: permission boundary is a release-blocking product semantic.

### BV-002: Multi-Person Approval Completion

- PRD trace: R-002.
- Scenario/setup: a flow has at least two approvers.
- Test data:
  - Positive cases: every required approver approves.
  - Negative cases: at least one required approver rejects or does not act.
  - Boundary cases: duplicate approver, unavailable approver, same user in multiple steps if allowed.
  - Stateful cases: pending, partially approved, approved, rejected/cancelled if defined.
  - Cleanup requirements: close or delete test approval instances.
- Steps or review method: blocked until the PRD defines approval order and completion rule.
- Pass criteria: cannot be finalized until `BQ-002` is answered.
- Fail criteria: implementation approves early, skips required approvers, ignores rejection semantics, or records inconsistent approval state compared with defined rules.
- Required evidence: `EV-002` approval timeline, approver identities, state transitions, and final outcome.
- Mode: Blocked.
- Automation level: Blocked.
- Test execution requirement: Not applicable until unblocked.
- Priority: Blocker.
- Retest scope: all multi-person approval paths, state transitions, and history records.

### BV-003: Conditional Branch Routing

- PRD trace: R-003.
- Scenario/setup: a flow has at least two conditional branches and a candidate default/fallback path.
- Test data:
  - Positive cases: inputs that match each defined branch.
  - Negative cases: inputs that match no branch.
  - Boundary cases: inputs that match multiple branches, missing field values, null/empty values.
  - Stateful cases: branch chosen at submission time versus reevaluation after data changes, if defined.
  - Cleanup requirements: remove test branch configurations and approval instances.
- Steps or review method: blocked until the PRD defines branch predicates, evaluation timing, precedence, fallback, and conflict handling.
- Pass criteria: cannot be finalized until `BQ-001` is answered.
- Fail criteria: branch selection differs from defined predicates, multiple-match behavior is inconsistent, fallback is missing when required, or branch evidence is not auditable.
- Required evidence: `EV-003` branch configuration, input payloads, selected branch, branch-decision logs or records.
- Mode: Blocked.
- Automation level: Blocked.
- Test execution requirement: Not applicable until unblocked.
- Priority: Blocker.
- Retest scope: all branch predicates, default path, conflict path, and branch-decision persistence.

### BV-004: Post-Approval Business Action Trigger

- PRD trace: R-004.
- Scenario/setup: a flow reaches the approved terminal state and has a configured business action.
- Test data:
  - Positive cases: approval completes and action target is available.
  - Negative cases: approval not complete, approval rejected, action target fails.
  - Boundary cases: duplicate approval callback/event, action timeout, repeated retry.
  - Stateful cases: action pending, succeeded, failed, retried, manually reconciled if defined.
  - Cleanup requirements: reverse or isolate test business actions in a sandbox.
- Steps or review method: blocked until the PRD defines action timing, target behavior, retry policy, idempotency, and failure handling.
- Pass criteria: cannot be finalized until `BQ-003` is answered.
- Fail criteria: action triggers before approval completion, triggers more than allowed, fails silently, retries outside policy, or leaves approval/action states inconsistent.
- Required evidence: `EV-004` approval completion record, action request/event, target result, retry logs, idempotency key or equivalent duplicate-prevention evidence.
- Mode: Blocked.
- Automation level: Blocked.
- Test execution requirement: Not applicable until unblocked.
- Priority: Blocker.
- Retest scope: approval completion path, action dispatch, retry/failure path, duplicate prevention, reconciliation evidence.

## Implementation Audit Standards

### IA-001: Approval Flow Data And State Integrity

- PRD trace: R-001, R-004.
- Implementation area: data model, state machine, persistence, migrations if present.
- Review method: inspect code and data records for flow definition, approval instance, approver decisions, branch decision, and business-action state.
- Pass criteria: implementation stores enough state to prove configuration, approval progress, selected branch, final approval outcome, and business-action result without relying only on transient memory.
- Fail criteria: approval/action state can be lost, overwritten without history, or cannot support audit evidence for `BV-001` through `BV-004`.
- Required evidence: `EV-005` schema/model references, example records, lifecycle state diagram or equivalent implementation reference.
- Test coverage requirement: automated or review evidence must cover state creation and transitions for high-risk paths once semantics are defined.
- Static fallback: inspect models, migration files, service methods, and tests.
- Priority: High.
- Retest scope: data model, state transition code, migrations, and tests tied to approval/action state.

### IA-002: Audit History And Observability

- PRD trace: R-001, R-002, R-003, R-004.
- Implementation area: logs, audit history, metrics/traces where available.
- Review method: verify that configuration changes, approver actions, branch decisions, and business-action attempts produce traceable records.
- Pass criteria: records include actor, timestamp, flow/version, approval instance, operation, outcome, and correlation ID or equivalent link across approval and action events.
- Fail criteria: future auditors cannot reconstruct who configured a flow, why a branch was selected, who approved, or whether an action was attempted/succeeded/failed.
- Required evidence: `EV-006` sample audit records/logs and field list.
- Test coverage requirement: test or static evidence for log/history creation on core events.
- Static fallback: inspect logging/audit writer calls and tests.
- Priority: High.
- Retest scope: all event writers and audit/history persistence.

### IA-003: Authorization Enforcement

- PRD trace: R-001.
- Implementation area: auth middleware, permission policy, route guards, UI guards.
- Review method: blocked until `BQ-004` defines role/operation boundaries.
- Pass criteria: cannot be finalized until permission matrix exists.
- Fail criteria: server-side authorization is missing for protected operations, or UI-only controls are the only enforcement.
- Required evidence: `EV-007` role matrix, protected routes/actions, positive and negative auth tests.
- Test coverage requirement: required after unblocking for every Blocker permission boundary.
- Static fallback: inspect route guards and policy checks.
- Priority: Blocker.
- Retest scope: all protected configuration and approval operations.

### IA-004: Business Action Idempotency And Failure Handling

- PRD trace: R-004.
- Implementation area: action dispatcher, job queue, retry handler, external/internal integration layer.
- Review method: blocked until `BQ-003` defines retry and failure semantics.
- Pass criteria: cannot be finalized until retry/idempotency requirements exist.
- Fail criteria: duplicate approvals or repeated retries can trigger duplicate irreversible business actions; failed actions cannot be observed or reconciled.
- Required evidence: `EV-008` action invocation records, idempotency strategy, retry policy implementation, failure state handling.
- Test coverage requirement: required after unblocking for duplicate event, retry, timeout, and failure paths.
- Static fallback: inspect dispatcher, queue config, idempotency keys, and tests.
- Priority: Blocker.
- Retest scope: action dispatcher, queue/retry config, idempotency tests, reconciliation behavior.

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | Project-specific unit/integration/e2e commands to be identified by future audit agent. | `BV-001`-`BV-004`, `IA-001`-`IA-004` | Static fallback until project context exists | command, timestamp, result, failure log, test files/assertions | Record blocker, inspect tests/routes/models/auth/logging statically, and do not treat as pass. |
| TE-002 | API/UI approval-flow regression suite, if present. | `BV-001`-`BV-004` | Conditional | test report and scenario-to-check mapping | If suite is absent, record missing coverage and inspect manual or static evidence. |
| TE-003 | Authorization/security tests, if present. | `BV-001`, `IA-003` | Conditional | positive/negative role test results | If role matrix is absent, keep blocked under `BQ-004`. |
| TE-004 | Business-action integration or contract tests, if present. | `BV-004`, `IA-004` | Conditional | action request/response logs and duplicate/retry evidence | If sandbox/target is unavailable, inspect contract tests and mark execution blocked. |

## API, Data, And State Standards

- The future audit agent must identify the API/UI entry points for flow configuration, approval actions, branch evaluation, and business-action dispatch.
- Approval instance state must not transition to approved until the PRD-defined multi-person completion rule is satisfied.
- Branch decision data must be persistently traceable to the input values and rule version used at evaluation time.
- Business-action state must be distinguishable from approval state, so an approved flow with failed action is not falsely reported as fully completed unless the PRD explicitly defines that outcome.

## Permissions, Security, And Privacy Standards

- Permission checks are release-blocking because the PRD says users can configure approval flows but does not define who those users are.
- Server-side authorization must be audited after `BQ-004` is resolved; UI-only hiding is insufficient.
- Evidence must show allowed and denied outcomes for each protected operation.
- Any sensitive data used in branch predicates or action payloads must be included in privacy/security review if present in the implementation.

## Integration And External Dependency Standards

- Post-approval business actions are high-risk because they may create irreversible or externally visible changes.
- The audit must verify action dispatch, target response, retry behavior, duplicate prevention, and reconciliation after `BQ-003` is resolved.
- If execution against a real target is unsafe, the audit may use sandbox, contract test, or mock evidence, but must record the substitute evidence and remaining risk.

## Observability, Performance, And Reliability Standards

- Required logs/history: configuration change, approval decision, branch evaluation, approval completion, action dispatch, action result, retry/failure.
- Performance thresholds are not defined in the PRD; do not invent latency pass/fail criteria.
- Reliability thresholds for retry count, retry interval, timeout, and dead-letter/reconciliation behavior are blocked by `BQ-003`.

## Regression And Compatibility Standards

- Existing behavior to retest: any existing approval, authorization, workflow, and business-action behavior touched by the implementation.
- Backward compatibility checks: blocked unless existing approval flows or migrations are in scope.
- Migration/rollback checks: required only if implementation introduces schema or state changes.
- Release/feature-flag checks: required if the implementation is guarded by a feature flag or staged rollout.

## Required Evidence For Future Review

- `EV-001`: permission matrix, test accounts, allowed/denied operation evidence for approval-flow configuration.
- `EV-002`: approval timeline, approver identities, state transitions, completion outcome.
- `EV-003`: branch predicates, input payloads, selected branch, branch decision record.
- `EV-004`: approval completion record, action dispatch request/event, action target result, retry/idempotency evidence.
- `EV-005`: schema/model/state transition references and example approval/action records.
- `EV-006`: audit logs/history records with actor, timestamp, flow/version, instance, operation, outcome, correlation ID.
- `EV-007`: auth policy references, route/action guard evidence, positive and negative authorization tests.
- `EV-008`: retry policy, idempotency strategy, duplicate-prevention and failure-handling evidence.
- `EV-009`: test command outputs or recorded execution blockers with static fallback evidence.
- `EV-010`: final audit conclusion linked to all Blocker and High checks.

Evidence rules:

- Every evidence item must reference one or more audit check IDs.
- Failed evidence must reference a defect report ID.
- API/log/database evidence must include request parameters, query conditions, correlation IDs, or record IDs when relevant.
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

- Check statuses: Pass / Fail / Blocked / Not Run / Not Applicable.
- Final conclusions: Approved / Approved with Risks / Rejected / Blocked.
- `Blocked` and `Not Run` are not passes.
- Any Blocker product semantic left unresolved requires final conclusion `Blocked`.
- `Approved` is allowed only when all Blocker and High checks pass and evidence traces to check IDs.
- `Approved with Risks` is not allowed when any Blocker check fails, is blocked, or is not run without sufficient substitute evidence.
- `Rejected` is required when any Blocker check fails or a critical PRD behavior is missing.

## Hard Fail Conditions

- Any `Blocker` check fails.
- Any `Blocker` check is `Blocked` or `Not Run` without substitute evidence.
- Any of `BQ-001` through `BQ-004` remains unresolved at release audit time.
- A core PRD flow has no audit coverage.
- Permission boundaries lack implementation audit coverage after they are defined.
- Business action idempotency, retry, or failure behavior lacks implementation audit coverage after it is defined.
- Required test commands are not run and no blocker is recorded.
- High-risk clean-context review findings are ignored without rejection rationale.
- Evidence cannot be traced to audit check IDs.

## Retest And Regression Rules

- Failed check retest scope: rerun the failed check and capture fresh evidence.
- Related PRD area regression: retest related checks in the same requirement area.
- Changed code path test requirements: rerun automated tests and static review tied to changed routes, services, schemas, auth policies, logging, and integration code.
- Blocker/High fix verification: require related regression execution or a documented blocker.
- Retest round reporting: record defect ID, fixed build/version, commands or static fallback, result, and remaining risk.

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed checks as deprecated; do not reuse IDs.
- Rerun three clean-context reviews when changes affect core flows, permissions, data, integrations, irreversible operations, or risk levels.
- For small non-behavioral wording changes, run local update plus quality gate.

## Three-Round Clean-Context Review Record

- Review mode: Inline fallback.
- Reviewer A focus: PRD coverage completeness and traceability.
- Reviewer B focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations.
- Reviewer C focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling.
- Round 1 status: Completed.
- Round 2 status: Completed.
- Round 3 status: Completed.
- Context isolation: Approximated.

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| Conditional branch behavior must remain blocked because predicates, precedence, fallback, conflict behavior, and evaluation timing are undefined. | Round 1 / Round 2 | Accepted | Directly traces to missing branch rules in the PRD; inventing them would create false pass/fail standards. |
| Approval order and completion rule must be Blocker, not an assumption. | Round 1 / Round 2 | Accepted | Multi-person approval cannot be audited without knowing whether approvals are parallel, sequential, unanimous, quorum-based, or role-based. |
| Post-approval business action needs idempotency, retry, timeout, and failure-state audit gates. | Round 2 / Round 3 | Accepted | Business actions can create duplicate or inconsistent outcomes; retry semantics are explicitly missing. |
| Permission boundaries must block readiness. | Round 2 | Accepted | The PRD does not define which users can configure, approve, view, or administer flows. This is a high-risk authorization gap. |
| Add project-specific test command requirements. | Round 3 | Accepted | No project path was provided, so execution remains blocked/static fallback until commands are identified. |
| Use `Ready with assumptions` for missing semantics. | Round 3 | Rejected | Skill quality gate requires `Blocked` when unresolved Blocker product semantics remain. |

## Blocked Checks And Open Questions

| ID | Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- | --- |
| BQ-001 | Conditional branches | What is the rule language, allowed fields/operators, evaluation timing, branch precedence, default/fallback behavior, and multiple-match conflict behavior? | Blocks executable branch-routing pass/fail standards for `BV-003`. | Product owner |
| BQ-002 | Multi-person approval | Are approvals sequential, parallel, unanimous, quorum-based, role-based, or mixed? What happens on reject, skip, timeout, delegation, duplicate approver, or unavailable approver? | Blocks executable approval completion standards for `BV-002`. | Product owner |
| BQ-003 | Business action trigger | When is the action triggered, what target/action types are allowed, what is the retry policy, how are failures surfaced, and how is duplicate execution prevented? | Blocks executable trigger, retry, failure, and idempotency standards for `BV-004` and `IA-004`. | Product owner / technical owner |
| BQ-004 | Permission boundary | Which roles can create, edit, activate, delete, view, approve, delegate, retry, or administer flows and action results? | Blocks executable authorization standards for `BV-001` and `IA-003`. | Product owner / security owner |

## Assumptions

- The artifact assumes the pasted prompt is the only PRD source. This is safe for audit generation because missing semantics are marked blocked rather than inferred.
- The artifact assumes post-development audit agents will have access to implementation files and test commands later. This is non-blocking for the standards structure, but execution remains blocked until project context exists.

## Final Quality Gate

- Ready for post-development audit: No.
- Artifact readiness status: Blocked.
- Final conclusion rule ready: Yes.
- Hard fail conditions complete: Yes.
- Conditions before use: resolve `BQ-001` through `BQ-004`; identify project test commands, API/UI surfaces, schemas, auth policies, logging/audit mechanisms, and integration targets.
- Checks that must pass before release: `BV-001`, `BV-002`, `BV-003`, `BV-004`, `IA-003`, `IA-004`, `RG-001`.

## Machine-Readable Audit Checks Appendix

```json
{
  "artifact_readiness_status": "Blocked",
  "draft_admission": "Admitted - Blocked",
  "requirements_mapped": 4,
  "blocked_questions": [
    {
      "id": "BQ-001",
      "area": "Conditional branches",
      "question": "Define rule language, fields/operators, evaluation timing, precedence, fallback, and conflict behavior.",
      "blocks": ["BV-003"]
    },
    {
      "id": "BQ-002",
      "area": "Multi-person approval",
      "question": "Define approval order, completion rule, rejection, timeout, delegation, duplicate approver, and unavailable approver behavior.",
      "blocks": ["BV-002"]
    },
    {
      "id": "BQ-003",
      "area": "Business action trigger",
      "question": "Define trigger timing, action target/types, retry policy, failure surfacing, and idempotency.",
      "blocks": ["BV-004", "IA-004"]
    },
    {
      "id": "BQ-004",
      "area": "Permission boundary",
      "question": "Define roles and allowed operations for configuration, approval, viewing, administration, retry, and action result handling.",
      "blocks": ["BV-001", "IA-003"]
    }
  ],
  "audit_checks": [
    {
      "id": "BV-001",
      "prd_trace": "R-001",
      "layer": "Behavior Verification",
      "category": "Approval flow configuration permissions",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Approval-flow configuration surface and role-specific accounts.",
      "test_data": {
        "positive_cases": ["Allowed configurator role"],
        "negative_cases": ["Unauthorized user"],
        "boundary_cases": ["Approver without configuration permission"],
        "stateful_cases": ["Create/update/activate/deactivate"],
        "cleanup_requirements": ["Remove or deactivate test flows"]
      },
      "steps_or_method": "Blocked until permission matrix is defined.",
      "pass_criteria": "Blocked by BQ-004.",
      "fail_criteria": "User outside defined permission boundary can configure or inspect restricted approval flows.",
      "required_evidence": ["EV-001"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "All configuration authorization paths.",
      "status": "Blocked"
    },
    {
      "id": "BV-002",
      "prd_trace": "R-002",
      "layer": "Behavior Verification",
      "category": "Multi-person approval completion",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Flow with at least two approvers.",
      "test_data": {
        "positive_cases": ["Every required approver approves"],
        "negative_cases": ["Required approver rejects or does not act"],
        "boundary_cases": ["Duplicate or unavailable approver"],
        "stateful_cases": ["Pending, partially approved, terminal outcome"],
        "cleanup_requirements": ["Close test approval instances"]
      },
      "steps_or_method": "Blocked until approval order and completion rule are defined.",
      "pass_criteria": "Blocked by BQ-002.",
      "fail_criteria": "Implementation approves early, skips required approvers, or records inconsistent state.",
      "required_evidence": ["EV-002"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "All multi-person approval paths and state transitions.",
      "status": "Blocked"
    },
    {
      "id": "BV-003",
      "prd_trace": "R-003",
      "layer": "Behavior Verification",
      "category": "Conditional branch routing",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Flow with multiple conditional branches.",
      "test_data": {
        "positive_cases": ["Input matching each branch"],
        "negative_cases": ["Input matching no branch"],
        "boundary_cases": ["Input matching multiple branches, missing/null values"],
        "stateful_cases": ["Branch chosen at defined evaluation time"],
        "cleanup_requirements": ["Remove test branches and instances"]
      },
      "steps_or_method": "Blocked until branch semantics are defined.",
      "pass_criteria": "Blocked by BQ-001.",
      "fail_criteria": "Branch selection differs from defined predicates or is not auditable.",
      "required_evidence": ["EV-003"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "All branch predicates, fallback, conflict path, and decision records.",
      "status": "Blocked"
    },
    {
      "id": "BV-004",
      "prd_trace": "R-004",
      "layer": "Behavior Verification",
      "category": "Post-approval business action trigger",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Approved flow with configured business action.",
      "test_data": {
        "positive_cases": ["Approval completes and action target is available"],
        "negative_cases": ["Approval incomplete/rejected or action target fails"],
        "boundary_cases": ["Duplicate event, timeout, repeated retry"],
        "stateful_cases": ["Pending, succeeded, failed, retried"],
        "cleanup_requirements": ["Reverse or isolate sandbox action effects"]
      },
      "steps_or_method": "Blocked until action timing, retry, failure, and idempotency semantics are defined.",
      "pass_criteria": "Blocked by BQ-003.",
      "fail_criteria": "Action triggers early, duplicates, fails silently, or leaves inconsistent state.",
      "required_evidence": ["EV-004"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "Action dispatch, retry/failure path, duplicate prevention, reconciliation evidence.",
      "status": "Blocked"
    },
    {
      "id": "IA-001",
      "prd_trace": "R-001,R-004",
      "layer": "Implementation Audit",
      "category": "Data and state integrity",
      "priority": "High",
      "mode": "Review-only",
      "automation_level": "Recommended",
      "setup": "Access to implementation files and records.",
      "test_data": {
        "positive_cases": ["Persisted flow definition and approval instance"],
        "negative_cases": ["Missing or inconsistent state"],
        "boundary_cases": ["State transition around approval completion"],
        "stateful_cases": ["Configured, pending, approved, action result"],
        "cleanup_requirements": []
      },
      "steps_or_method": "Inspect models, migrations, services, and tests for persistent flow/approval/action state.",
      "pass_criteria": "State is sufficient to audit configuration, approval progress, branch decision, and action result.",
      "fail_criteria": "State can be lost or cannot support required evidence.",
      "required_evidence": ["EV-005"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "Data model, state transition code, migrations, and related tests.",
      "status": "Ready"
    },
    {
      "id": "RG-001",
      "prd_trace": "R-001,R-002,R-003,R-004",
      "layer": "Risk Gate",
      "category": "Release blocking unresolved semantics",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Not recommended",
      "setup": "Final audit report with check statuses.",
      "test_data": {
        "positive_cases": ["All Blocker semantics resolved and checks pass"],
        "negative_cases": ["Any BQ remains unresolved or Blocker check fails"],
        "boundary_cases": ["Substitute evidence claimed for blocked behavior"],
        "stateful_cases": [],
        "cleanup_requirements": []
      },
      "steps_or_method": "Review final audit status and evidence traceability.",
      "pass_criteria": "No unresolved Blocker semantics; all Blocker and High checks pass or have acceptable non-Blocker risk handling.",
      "fail_criteria": "Any BQ remains unresolved, any Blocker check fails, or evidence is not traceable.",
      "required_evidence": ["EV-010"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "All Blocker checks and related High checks.",
      "status": "Ready"
    }
  ]
}
```
