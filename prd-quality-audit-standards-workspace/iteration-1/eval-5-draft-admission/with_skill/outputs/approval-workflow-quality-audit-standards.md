# Approval Workflow Quality Audit Standards

## Source And Scope

- Source PRD: pasted coarse PRD summary: "用户可以配置审批流，审批流支持多人审批、条件分支和审批通过后触发业务动作，但没有定义分支规则、审批顺序、失败重试、权限边界。"
- Supporting context: none. No project path, technical design, API contract, schema, or test commands provided.
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents.
- Status: Ready with blocking questions. The standards can guide audit preparation, but unconditional release approval is blocked until the missing product rules are resolved.
- In scope: approval-flow configuration, multi-person approval, conditional branches, post-approval business action triggering, permission boundary verification, failure/retry handling, evidence/reporting rules.
- Out of scope: inventing branch semantics, approval ordering semantics, retry policy, role matrix, concrete UI copy, concrete API paths, performance thresholds, or implementation design.

## Requirement Inventory

| ID | Requirement Or Gap | Type | Audit Treatment |
| --- | --- | --- | --- |
| PRD-001 | Users can configure approval flows. | Explicit functional requirement | Covered by behavior and implementation checks. |
| PRD-002 | Approval flows support multi-person approval. | Explicit functional requirement | Covered, but ordering/quorum rules are blocked. |
| PRD-003 | Approval flows support conditional branches. | Explicit functional requirement | Blocked until branch rule model, priority, and fallback behavior are defined. |
| PRD-004 | Successful approval triggers business actions. | Explicit functional requirement | Covered, with idempotency/failure behavior blocked. |
| GAP-001 | Branch rules are not defined. | Blocking ambiguity | Blocker open question. |
| GAP-002 | Approval sequence/order is not defined. | Blocking ambiguity | Blocker open question. |
| GAP-003 | Failure retry behavior is not defined. | Blocking ambiguity | High/Blocker open question depending on triggered action criticality. |
| GAP-004 | Permission boundaries are not defined. | Blocking ambiguity | Blocker open question. |

## Project Context Inspection

- Project path: not provided.
- Context inspection mode: Not available.
- Inspected files: none.
- Impact: audit commands, API routes, schema names, role names, log format, and test framework must be filled by the future audit agent from the implementation repository. Static fallback is required when executable tests cannot be run.

## Audit Environment Requirements

- Required services: application under audit, persistence layer, approval workflow engine, business action executor or sandbox adapter.
- Required accounts/roles: workflow creator, approver, non-approver, unauthorized user, system/service actor. Exact role names are blocked by `BQ-004`.
- Required test data: at least one approval flow with one approver, one flow with multiple approvers, one flow with conditional branches, one approved instance that triggers a business action, one unauthorized access attempt.
- Required secrets/sandboxes: business action sandbox or reversible test target when actions mutate business data.
- Setup commands: not defined by PRD or project context; future audit agent must record discovered commands as `TE-001`.
- Known environment limitations: no executable project context; product rules for branch/order/retry/permission are incomplete.

## Readiness Summary

- Intended primary executor: Implementation audit agent and test audit agent.
- Requirements mapped: 4 explicit PRD requirements.
- Blocked or ambiguous requirements: 4 major gaps.
- Release-blocking gates: 5.
- Machine-readable appendix: Included.
- Draft admission result: passed on first draft; no rewrite needed.

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | PRD-001 | Verify a user can create and persist an approval-flow configuration. | Behavior Verification | Blocker | Automated | Conditional | UI/API trace, persisted flow record | Ready |
| BV-002 | PRD-002 | Verify a workflow instance can require multiple approvers and records each decision. | Behavior Verification | Blocker | Automated | Conditional | approval instance, decision records | Ready with blocked sub-rules |
| BV-003 | PRD-003/GAP-001 | Verify conditional branch routing only after branch rules are defined. | Behavior Verification | Blocker | Blocked | Not applicable | blocked question resolution | Blocked |
| BV-004 | PRD-004 | Verify approval completion triggers the configured business action exactly once. | Behavior Verification | Blocker | Automated | Conditional | action invocation trace, idempotency evidence | Ready with blocked retry sub-rules |
| IA-001 | PRD-001 | Review workflow configuration persistence, validation, and versioning boundaries. | Implementation Audit | High | Review-only | Static fallback | code/schema/test references | Ready |
| IA-002 | PRD-002/GAP-002 | Review multi-approver state model and ordering/quorum enforcement. | Implementation Audit | Blocker | Review-only | Static fallback | code/schema/state transition references | Ready with blocked sub-rules |
| IA-003 | PRD-003/GAP-001 | Review branch evaluation model for deterministic precedence and fallback behavior. | Implementation Audit | Blocker | Blocked | Not applicable | blocked question resolution | Blocked |
| IA-004 | PRD-004/GAP-003 | Review business action dispatch for transaction boundary, retry, idempotency, and failure records. | Implementation Audit | Blocker | Review-only | Static fallback | code/log/schema references | Ready with blocked retry sub-rules |
| IA-005 | GAP-004 | Review authorization checks for creating, editing, viewing, approving, and triggering workflows. | Implementation Audit | Blocker | Blocked | Not applicable | permission matrix | Blocked |
| TE-001 | all | Run implementation test suites relevant to approval workflows, or record blocker and perform static fallback. | Test Execution | Blocker | Manual | Conditional | command, timestamp, result, logs | Ready |
| RG-001 | all | Reject release when any core approval path lacks executable or static evidence. | Risk Gate | Blocker | Review-only | Not applicable | final audit report | Ready |

## Behavior Verification Standards

### BV-001: Approval Flow Configuration

- PRD trace: PRD-001.
- Scenario/setup: Given a user with workflow configuration permission, when they create a valid approval flow, then the system stores and returns the configured flow.
- Test data: one minimal valid flow; one invalid flow missing approver/action; cleanup removes created flow and instances.
- Steps or review method: execute UI/API creation path, reload/requery the flow, and confirm fields persist without unintended defaults that alter approval behavior.
- Pass criteria: the flow is saved, retrievable, and includes approver, branch, and action configuration fields required by the implementation's documented contract.
- Fail criteria: flow cannot be saved; saved state differs from submitted state; invalid incomplete flow can be activated without validation.
- Required evidence: request/response or UI recording, persisted record ID, validation evidence for invalid flow.
- Mode: Automated when API or UI automation exists; manual is acceptable only with recorded evidence.
- Automation level: Required for release-critical paths unless tooling is unavailable.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: workflow create/update/read paths and validation tests.

### BV-002: Multi-Person Approval

- PRD trace: PRD-002 and GAP-002.
- Scenario/setup: Given a configured approval flow with more than one approver, when an approval instance is submitted, then each required approver can record an independent decision.
- Test data: at least two approvers and one unauthorized user.
- Pass criteria: approver decisions are stored separately, duplicate decisions are prevented or handled according to documented implementation behavior, and final completion does not occur before the required multi-person condition is satisfied.
- Fail criteria: one approver can impersonate another, decisions overwrite each other, completion occurs before required decisions, or unauthorized users can approve.
- Required evidence: approval instance ID, decision records, actor IDs, final status transition.
- Mode: Automated preferred.
- Automation level: Required for positive and unauthorized negative cases.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: approval decision, status transition, authorization, and concurrency regression.
- Notes: exact sequence, parallel/serial approval, all-of/any-of quorum, rejection semantics, and escalation are blocked by `BQ-002`.

### BV-003: Conditional Branch Routing

- PRD trace: PRD-003 and GAP-001.
- Status: Blocked.
- Blocking reason: PRD does not define branch condition fields, expression language, priority, conflict resolution, default branch, or behavior when no branch matches.
- Minimum future pass criteria after unblock: test at least one matching branch, one non-matching/default branch, one conflicting branch-priority case, and one invalid condition case.
- Required evidence after unblock: branch rule definition, input facts, selected branch, skipped branches, and persisted audit trail.
- Priority: Blocker.

### BV-004: Business Action Trigger After Approval

- PRD trace: PRD-004 and GAP-003.
- Scenario/setup: Given an approval instance that reaches approved status, when completion is committed, then the configured business action is triggered exactly once.
- Test data: approved instance, business action sandbox target, retry/duplicate completion attempt where supported.
- Pass criteria: action is invoked only after approval completion, contains the expected workflow/instance context, and duplicate completion attempts do not produce duplicate side effects.
- Fail criteria: action triggers before approval; action is missing after approval; duplicate action is produced; failure leaves no visible recoverable state.
- Required evidence: approval status record, action invocation record, correlation ID, idempotency or duplicate-prevention evidence.
- Mode: Automated when the action target can be sandboxed; manual/review-only evidence is acceptable only for non-executable external dependencies.
- Automation level: Required for action dispatch and duplicate-prevention paths.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: approval completion, action dispatch, idempotency, failure recovery.
- Notes: retry count, retry interval, dead-letter handling, and operator recovery are blocked by `BQ-003`.

## Implementation Audit Standards

### IA-001: Workflow Configuration Model

- PRD trace: PRD-001.
- Implementation area: code, API, data schema, validation, tests.
- Review method: inspect how flow definitions are represented, validated, activated, updated, and read by approval instances.
- Pass criteria: required fields are validated before activation; active instances are protected from unsafe definition mutation; tests cover valid and invalid configuration.
- Fail criteria: invalid active flows are possible; active instance behavior changes unpredictably after edits; there is no test or review evidence for configuration persistence.
- Required evidence: code references, schema references, validation tests, sample persisted records.
- Test coverage requirement: automated or static evidence for create/read/update validation paths.
- Static fallback: inspect validation code and existing test assertions when commands cannot run.
- Priority: High.
- Retest scope: configuration validation and active-instance compatibility.

### IA-002: Multi-Approver State And Ordering

- PRD trace: PRD-002 and GAP-002.
- Implementation area: state machine, decision records, authorization checks, concurrency handling.
- Review method: inspect data model and transitions for per-approver decisions, final status calculation, duplicate submission handling, and concurrent approvals.
- Pass criteria: state transitions are deterministic for the documented order/quorum model; each decision is actor-bound; concurrent decisions cannot corrupt final state.
- Fail criteria: final state can be reached with missing required decisions; decision records lack actor identity; concurrent updates can overwrite decisions.
- Required evidence: state transition code/tests, database constraints or transaction logic, concurrency test or reasoned static proof.
- Priority: Blocker.
- Retest scope: approval decision and completion state machine.

### IA-003: Conditional Branch Evaluation

- PRD trace: PRD-003 and GAP-001.
- Status: Blocked.
- Blocking reason: no branch rule contract exists.
- Required resolution before release approval: define condition syntax/data sources, evaluation time, precedence, fallback, invalid-rule handling, and audit trail.
- Priority: Blocker.

### IA-004: Business Action Dispatch, Retry, And Idempotency

- PRD trace: PRD-004 and GAP-003.
- Implementation area: event dispatch, transaction boundary, job queue, external integration, logs.
- Review method: inspect whether approval completion and action dispatch have a reliable handoff, idempotency key, retry/failure record, and observable outcome.
- Pass criteria: action dispatch is tied to an approved instance; duplicate dispatch is prevented; failed dispatch is recorded and recoverable according to documented retry policy.
- Fail criteria: action dispatch can be lost silently; duplicate side effects are possible; retry behavior is absent or unobservable for required actions.
- Required evidence: code references, queue/job records, logs with correlation ID, idempotency tests or static proof.
- Test coverage requirement: approved path and duplicate/failure path where environment allows.
- Static fallback: inspect transaction/job code and tests when external action sandbox is unavailable.
- Priority: Blocker.
- Retest scope: completion transaction, dispatch job, retry records, duplicate prevention.

### IA-005: Permission Boundaries

- PRD trace: GAP-004.
- Status: Blocked.
- Blocking reason: PRD does not define who may configure flows, view flows, edit active flows, approve, delegate, reject, override, or trigger/retry business actions.
- Required resolution before release approval: role/action permission matrix and unauthorized behavior for each protected operation.
- Priority: Blocker.

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | Project-specific approval workflow unit/integration/e2e tests, command to be discovered by future audit agent | BV-001, BV-002, BV-004, IA-001, IA-002, IA-004 | Conditional | command, timestamp, exit code, logs/report, failed test details | inspect test files, assertions, mocks, workflow code paths; record execution blocker |
| TE-002 | Static implementation review | IA-001 through IA-005 | Required | file references, reviewed methods/classes, schema references | none; absence is release-blocking for Blocker checks |
| TE-003 | Authorization negative tests after permission matrix is supplied | IA-005, BV-002 | Conditional | unauthorized request evidence, expected denial response/log | blocked until `BQ-004` is answered |

## API, Data, And State Standards

- Approval flow definitions must be persisted with enough data to reconstruct approvers, branches, and post-approval actions.
- Approval instances must preserve decision history by actor and timestamp.
- Status transitions must be deterministic and auditable.
- Business action dispatch must reference the approval instance and flow definition/version.
- Derived quality standard: idempotency evidence is required for post-approval action dispatch because duplicate side effects are a release-blocking data integrity risk.

## Permissions, Security, And Privacy Standards

- Permission checks are release-blocking, but exact pass/fail cases are blocked by missing PRD role boundaries.
- After `BQ-004` is answered, audit must verify every protected operation has an allowed-role positive case and a denied-role negative case.
- Evidence must include actor identity, operation, expected permission decision, actual result, and audit/log entry when available.

## Integration And External Dependency Standards

- Business actions must be tested against a sandbox or reversible target when they mutate business data.
- Failure, timeout, duplicate callback, and retry standards are blocked until `BQ-003` defines retry and recovery behavior.
- When execution is impossible, static evidence must show dispatch contract, idempotency key, error record, and operator recovery path if implemented.

## Observability, Performance, And Reliability Standards

- Required observable events: workflow created/updated, approval submitted, approver decision recorded, branch selected, approval completed, business action dispatched, business action failed/retried.
- Evidence must include correlation IDs or record IDs connecting approval instance to business action.
- Performance thresholds are not defined by PRD and must not be invented. Mark performance approval as blocked if release requires a threshold.

## Required Evidence For Future Review

- Test results: command, timestamp, result, failure logs, and environment notes for every executed suite.
- Screenshots or recordings: UI creation/approval paths if UI is the only verification surface.
- API traces: request parameters, actor, response, status, and correlation ID.
- Database records: workflow definition ID, approval instance ID, decision records, action dispatch records.
- Logs/audit events: branch selection, approval completion, business action dispatch/failure.
- Code references: files/methods for validation, state transitions, authorization, dispatch, retry/idempotency.

Evidence rules:

- Every evidence item must reference one or more audit check IDs.
- Failed evidence must reference a defect report ID.
- API/log/database evidence must include request parameters, query conditions, correlation IDs, or record IDs when relevant.

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
- Approved: all Blocker and High checks pass, and Medium/Low findings do not create aggregated release risk.
- Approved with Risks: no Blocker failure; remaining High/Medium issues have explicit risk acceptance or deferral rationale.
- Rejected: any Blocker check fails or a critical PRD behavior is missing.
- Blocked: critical Blocker/High checks cannot be verified and substitute evidence is insufficient.

## Hard Fail Conditions

- Any Blocker check fails.
- Any Blocker check is Blocked or Not Run without sufficient substitute evidence.
- A core approval flow has no audit coverage.
- Permission boundaries, multi-approver state, conditional branch routing, or business action dispatch lacks implementation audit coverage.
- Required test commands are not run and no blocker is recorded.
- High-risk clean-context review findings are ignored without rejection rationale.
- Evidence cannot be traced to audit check IDs.
- Business action can be triggered before approval completion or more than once for the same approval completion.

## Retest And Regression Rules

- Failed check retest scope: rerun the failed check and all checks sharing the same PRD trace.
- Related PRD area regression: configuration changes require retesting approval instance creation; approval-state fixes require retesting business action dispatch.
- Changed code path test requirements: run relevant unit/integration/e2e tests or record execution blocker and perform static fallback.
- Blocker/High fix verification: must include related regression execution or documented blocker.
- Retest round reporting: record defect ID, fixed version/commit, rerun command, result, and evidence IDs.

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed checks as deprecated; do not reuse IDs.
- Rerun three clean-context reviews when changes affect approval flow semantics, permissions, data integrity, integrations, irreversible actions, or risk levels.
- For small non-behavioral wording changes, run local update plus quality gate.

## Three-Round Clean-Context Review Record

- Review mode: Inline fallback.
- Context isolation: Approximated; no subagent tool was available, so three separated review passes were performed by focus.
- Reviewer A focus: PRD coverage completeness and traceability.
- Reviewer B focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations.
- Reviewer C focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling.
- Round 1 status: completed.
- Round 2 status: completed.
- Round 3 status: completed.

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| Conditional branch check must remain blocked rather than inventing branch precedence/default rules. | Round 1, Round 2 | Accepted | PRD explicitly lacks branch rules; Blocker questions added. |
| Permission boundary must be release-blocking. | Round 2 | Accepted | Unauthorized approval/configuration can create privilege escalation risk; IA-005 and BQ-004 marked Blocker. |
| Business action dispatch needs idempotency and failure evidence even though retry policy is missing. | Round 2, Round 3 | Accepted | Derived quality standard needed to prevent duplicate or lost side effects. |
| Test commands cannot be named without project context. | Round 3 | Accepted | TE-001 requires future command discovery and static fallback instead of fake command names. |
| Add performance threshold. | Round 3 | Rejected | PRD has no performance requirement; threshold would invent product criteria. |

## Blocked Checks And Open Questions

| ID | Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- | --- |
| BQ-001 | Conditional branches | What condition fields, expression syntax, data sources, precedence, conflict handling, and default branch behavior are required? | BV-003 and IA-003 cannot pass. | Product owner |
| BQ-002 | Multi-person approval | Is approval serial or parallel? Is completion all-of, any-of, weighted, ordered, or role-based? What happens on rejection? | BV-002 and IA-002 can verify storage/actor identity but not final semantic correctness. | Product owner |
| BQ-003 | Business action failure/retry | What retry count, interval, timeout, dead-letter, manual recovery, and duplicate-prevention behavior is required? | BV-004 and IA-004 cannot fully verify failure handling. | Product owner / engineering lead |
| BQ-004 | Permission boundaries | Which roles can create, edit, view, activate, approve, reject, delegate, override, retry, and audit workflows? | IA-005 and authorization negative tests are blocked. | Product owner / security owner |
| BQ-005 | Audit/history expectations | Which approval events must be visible to users or retained for compliance? | Observability/audit-log approval is limited to derived evidence requirements. | Product owner |

## Assumptions

- The pasted PRD summary is the only authoritative source.
- "用户" is treated as a role placeholder, not a permission grant to all authenticated users.
- Business action may mutate business data, so idempotency and dispatch evidence are treated as release-blocking derived quality standards.
- No project-specific test command is assumed without repository context.

## Final Quality Gate

- Ready for post-development audit: Yes, with blocking questions explicitly preserved.
- Final conclusion rule ready: Yes.
- Hard fail conditions complete: Yes.
- Conditions before unconditional release approval: answer `BQ-001` through `BQ-004`, execute or statically verify Blocker checks, and attach evidence to check IDs.
- Checks that must pass before release: BV-001, BV-002 with resolved ordering/quorum rules, BV-003 after branch rules are defined, BV-004 with retry/idempotency evidence, IA-001 through IA-005, TE-001/TE-002, RG-001.

## Machine-Readable Audit Checks Appendix

```json
{
  "source": {
    "type": "pasted_prd_summary",
    "summary": "Users can configure approval workflows with multi-person approval, conditional branches, and post-approval business actions; branch rules, approval order, retry behavior, and permission boundaries are undefined."
  },
  "readiness": {
    "status": "ready_with_blocking_questions",
    "draft_admission": "passed_first_draft",
    "clean_context_review": "completed_inline_fallback"
  },
  "audit_checks": [
    {
      "id": "BV-001",
      "prd_trace": "PRD-001",
      "layer": "Behavior Verification",
      "category": "approval_flow_configuration",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "User with workflow configuration permission and persistence available.",
      "test_data": {
        "positive_cases": ["valid minimal approval flow"],
        "negative_cases": ["flow missing required approver or action"],
        "boundary_cases": [],
        "stateful_cases": ["create then reload persisted flow"],
        "cleanup_requirements": ["delete created flow and instances"]
      },
      "steps_or_method": "Create approval flow through UI/API and verify persisted state.",
      "pass_criteria": "Flow is saved, retrievable, and does not silently change submitted behavior.",
      "fail_criteria": "Flow cannot be saved, invalid flow activates, or persisted state diverges.",
      "required_evidence": ["request_or_ui_trace", "persisted_flow_record", "validation_result"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "configuration create/read/update validation",
      "status": "Ready"
    },
    {
      "id": "BV-002",
      "prd_trace": "PRD-002,GAP-002",
      "layer": "Behavior Verification",
      "category": "multi_person_approval",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "Approval flow with at least two approvers.",
      "test_data": {
        "positive_cases": ["two approvers record independent decisions"],
        "negative_cases": ["unauthorized user attempts approval", "duplicate decision attempt"],
        "boundary_cases": [],
        "stateful_cases": ["instance status before and after each decision"],
        "cleanup_requirements": ["remove approval instance"]
      },
      "steps_or_method": "Submit approval instance and record decisions for each actor.",
      "pass_criteria": "Decisions are actor-bound and completion waits for required multi-person condition.",
      "fail_criteria": "Missing/overwritten decisions, impersonation, premature completion, or unauthorized approval.",
      "required_evidence": ["approval_instance_id", "decision_records", "actor_ids", "status_transition"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "decision recording, state transition, auth, concurrency",
      "status": "Ready with blocked sub-rules"
    },
    {
      "id": "BV-003",
      "prd_trace": "PRD-003,GAP-001",
      "layer": "Behavior Verification",
      "category": "conditional_branching",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Blocked until branch rule contract exists.",
      "test_data": {
        "positive_cases": [],
        "negative_cases": [],
        "boundary_cases": [],
        "stateful_cases": [],
        "cleanup_requirements": []
      },
      "steps_or_method": "Define branch rule tests after BQ-001 is answered.",
      "pass_criteria": "Blocked.",
      "fail_criteria": "Blocked.",
      "required_evidence": ["BQ-001_resolution"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "branch evaluation and routing",
      "status": "Blocked"
    },
    {
      "id": "BV-004",
      "prd_trace": "PRD-004,GAP-003",
      "layer": "Behavior Verification",
      "category": "post_approval_business_action",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "Approved instance and sandbox/reversible business action target.",
      "test_data": {
        "positive_cases": ["approved instance triggers action"],
        "negative_cases": ["duplicate completion attempt"],
        "boundary_cases": [],
        "stateful_cases": ["approval completion to dispatch record"],
        "cleanup_requirements": ["reverse or delete sandbox action effects"]
      },
      "steps_or_method": "Complete approval and verify action dispatch exactly once.",
      "pass_criteria": "Action triggers only after approval completion and is duplicate-safe.",
      "fail_criteria": "Early, missing, duplicate, or silently failed action dispatch.",
      "required_evidence": ["approval_status_record", "action_invocation_record", "correlation_id", "idempotency_evidence"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "completion, dispatch, retry, idempotency",
      "status": "Ready with blocked retry sub-rules"
    },
    {
      "id": "IA-005",
      "prd_trace": "GAP-004",
      "layer": "Implementation Audit",
      "category": "permissions",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Blocked until role/action permission matrix exists.",
      "test_data": {
        "positive_cases": [],
        "negative_cases": [],
        "boundary_cases": [],
        "stateful_cases": [],
        "cleanup_requirements": []
      },
      "steps_or_method": "Review authorization checks after BQ-004 is answered.",
      "pass_criteria": "Every protected operation has enforced allow/deny behavior matching the matrix.",
      "fail_criteria": "Unauthorized role can configure, approve, view, mutate, trigger, or retry protected workflow operations.",
      "required_evidence": ["permission_matrix", "auth_code_references", "positive_and_negative_auth_tests"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "all protected workflow operations",
      "status": "Blocked"
    },
    {
      "id": "RG-001",
      "prd_trace": "all",
      "layer": "Risk Gate",
      "category": "release_decision",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Not recommended",
      "setup": "Completed audit report with evidence references.",
      "test_data": {
        "positive_cases": [],
        "negative_cases": [],
        "boundary_cases": [],
        "stateful_cases": [],
        "cleanup_requirements": []
      },
      "steps_or_method": "Verify all Blocker/High checks are Pass or have accepted substitute evidence.",
      "pass_criteria": "No core approval behavior lacks coverage and all Blocker checks pass.",
      "fail_criteria": "Any Blocker failure, blocked core check without substitute evidence, or untraceable evidence.",
      "required_evidence": ["final_audit_report", "check_id_evidence_map"],
      "test_execution_requirement": "Not applicable",
      "retest_scope": "all failed or blocked Blocker/High checks",
      "status": "Ready"
    }
  ],
  "blocked_questions": [
    {
      "id": "BQ-001",
      "area": "conditional_branches",
      "question": "Define condition fields, expression syntax, data sources, precedence, conflict handling, and default branch behavior.",
      "priority": "Blocker"
    },
    {
      "id": "BQ-002",
      "area": "multi_person_approval",
      "question": "Define serial/parallel order, quorum/all-of/any-of rules, rejection behavior, and escalation/delegation if any.",
      "priority": "Blocker"
    },
    {
      "id": "BQ-003",
      "area": "business_action_retry",
      "question": "Define retry count, interval, timeout, dead-letter/manual recovery, and duplicate-prevention behavior.",
      "priority": "High"
    },
    {
      "id": "BQ-004",
      "area": "permissions",
      "question": "Define roles allowed to create, edit, view, activate, approve, reject, delegate, override, retry, and audit workflows.",
      "priority": "Blocker"
    }
  ]
}
```
