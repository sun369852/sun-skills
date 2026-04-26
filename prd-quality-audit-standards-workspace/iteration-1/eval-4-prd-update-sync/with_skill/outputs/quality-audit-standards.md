# Batch Export Quality Audit Standards

## Source And Scope

- Source PRD: update summary from prompt. Existing PRD changed from "batch export supports CSV only" to "batch export supports CSV and XLSX, and export tasks must record operator and filter criteria".
- Existing standards source: existing `quality-audit-standards.md` was referenced but not present in the provided eval workspace; this update preserves the assumed existing CSV export IDs and appends new IDs for changed PRD requirements.
- Supporting context: none available.
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents.
- In scope: CSV export continuity, new XLSX export, export task persistence of operator and filter criteria, evidence and regression rules for the PRD change.
- Out of scope: defining product behavior not present in the PRD update, including exact XLSX formatting, maximum export size, retention duration, role matrix, async retry semantics, and filter schema.

## Project Context Inspection

- Project path: not provided.
- Context inspection mode: Not available.
- Inspected files:

| File | Reason Inspected | Impact On Audit Standards |
| --- | --- | --- |
| N/A | No project or PRD file was available in the eval workspace. | Test commands, concrete APIs, schemas, and UI paths remain blocked until future audit locates the implementation. |

## Audit Environment Requirements

- Required services: application runtime, database or export-task storage, file generation/storage service if exports are asynchronous.
- Required accounts/roles: at least one authorized export operator; unauthorized role checks are blocked until PRD defines permissions.
- Required test data: records covering normal export, filtered export, empty-result export, and non-ASCII values if supported by the product.
- Required secrets/sandboxes: blocked until project dependencies are known.
- Setup commands: blocked because project test configuration is unavailable.
- Known environment limitations: future audit agent must bind these standards to real PRD IDs, implementation files, and test commands before execution.

## Readiness Summary

- Status: Ready with assumptions.
- Intended primary executor: Implementation audit agent and test audit agent.
- Requirements mapped: 3 PRD update requirements.
- Blocked or ambiguous requirements: 7.
- Release-blocking gates: 4.
- Machine-readable appendix: Included.

## ID Stability And PRD Update Policy

- Preserved assumed existing IDs:
  - `BV-001`: CSV batch export behavior remains valid and must not be renumbered.
  - `IA-001`: export data/query integrity remains valid and must not be renumbered.
  - `TE-001`: existing export test execution requirement remains valid and must not be renumbered.
  - `RG-001`: core export release gate remains valid and must not be renumbered.
- Appended new IDs:
  - `BV-002`: XLSX batch export behavior.
  - `BV-003`: export task records operator.
  - `BV-004`: export task records filter criteria.
  - `IA-002`: XLSX generation implementation audit.
  - `IA-003`: export task audit metadata persistence.
  - `TE-002`: XLSX/export metadata tests.
  - `RG-002`: export auditability gate.
  - `BQ-001` through `BQ-007`: unresolved PRD details.
- Deprecated IDs: none in this PRD update. CSV support was expanded, not removed; do not deprecate or reuse CSV-related IDs.

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | Existing batch export supports CSV | CSV export still works after XLSX addition and contains the expected filtered records. | Behavior Verification | Blocker | Automated | Conditional | CSV file, export request, selected filters, result row count | Ready |
| BV-002 | Batch export now supports XLSX | XLSX export can be requested, produced, opened, and verified against source records. | Behavior Verification | Blocker | Automated | Conditional | XLSX file, export request, parsed workbook values, result row count | Ready |
| BV-003 | Export task records operator | Each export task persists the authenticated operator who initiated it. | Behavior Verification | Blocker | Automated | Conditional | task record, user/account ID, API/UI action trace | Ready |
| BV-004 | Export task records filter criteria | Each export task persists the filter criteria used to generate the export. | Behavior Verification | Blocker | Automated | Conditional | task record, filter payload/snapshot, exported row comparison | Ready |
| IA-001 | Existing export query/data integrity | Export query still uses the requested dataset and filters without data leakage or missing records. | Implementation Audit | Blocker | Review-only | Static fallback | query/code references, database before/after evidence, tests | Ready |
| IA-002 | XLSX export support | Implementation uses a deterministic XLSX writer and validates generated workbook content. | Implementation Audit | High | Review-only | Static fallback | code references, workbook parser assertions, fixture output | Ready |
| IA-003 | Operator and filter criteria recording | Export task persistence stores operator and filter snapshot atomically with task creation. | Implementation Audit | Blocker | Review-only | Static fallback | schema/model/task code, transaction evidence, tests | Ready |
| TE-001 | Existing export tests | Existing CSV/export tests must still run and pass. | Test Execution | High | Automated | Conditional | command, timestamp, result log | Blocked |
| TE-002 | New XLSX and metadata tests | New or updated tests cover XLSX generation plus operator/filter task metadata. | Test Execution | High | Automated | Conditional | command, timestamp, result log, test names | Blocked |
| RG-001 | Core export correctness | CSV and XLSX exports must match the requested dataset and filters. | Risk Gate | Blocker | Automated | Conditional | file evidence tied to BV-001/BV-002/BV-004 | Ready |
| RG-002 | Export auditability | No export task may be created without operator and filter criteria evidence. | Risk Gate | Blocker | Automated | Conditional | task records tied to BV-003/BV-004/IA-003 | Ready |

## Behavior Verification Standards

### BV-001: CSV Batch Export Regression

- PRD trace: original batch export supports CSV.
- Scenario/setup: create or select records that can be exported with and without filters.
- Test data:
  - Positive cases: CSV export with all matching records.
  - Negative cases: unauthorized or invalid export request if PRD defines permissions/validation.
  - Boundary cases: empty filtered result, non-ASCII values if supported.
  - Stateful cases: export task creation followed by file retrieval.
  - Cleanup requirements: remove generated files and test export tasks when safe.
- Steps or review method: request CSV export using known filters; download or parse the CSV; compare row count and representative field values with source data.
- Pass criteria: CSV remains available; file content matches the filtered dataset; adding XLSX does not change CSV content, filename/content type, or task lifecycle unless PRD explicitly changed them.
- Fail criteria: CSV option disappears, returns wrong records, ignores filters, leaks records outside filters, or cannot be correlated to an export task.
- Required evidence: export request, filter criteria, CSV file or parser output, source data comparison, export task ID.
- Mode: Automated.
- Automation level: Required when project tests are available.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: CSV export endpoint/UI, export query, export task creation, file retrieval.

### BV-002: XLSX Batch Export

- PRD trace: updated batch export supports XLSX.
- Scenario/setup: use the same dataset and filters as CSV regression where possible.
- Test data:
  - Positive cases: XLSX export with matching records.
  - Negative cases: unsupported format request if PRD defines format validation.
  - Boundary cases: empty filtered result, text/date/number fields if present.
  - Stateful cases: export task creation followed by XLSX file retrieval.
  - Cleanup requirements: remove generated files and test export tasks when safe.
- Steps or review method: request XLSX export; open or parse the workbook with a test parser; compare worksheet headers, row count, and representative values against source data and CSV behavior where applicable.
- Pass criteria: XLSX is selectable/requestable; generated workbook is valid; workbook values match the filtered dataset; MIME type/file extension are correct where implementation exposes them.
- Fail criteria: XLSX file is corrupt, missing rows/columns, contains unfiltered data, records formulas unexpectedly, or cannot be associated with its export task.
- Required evidence: export request, XLSX file, parsed workbook output, source data comparison, export task ID.
- Mode: Automated.
- Automation level: Required when XLSX parsing can run in tests; otherwise manual file-open evidence plus static fallback.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: XLSX format selector/API, file generation, export query, file storage/retrieval.

### BV-003: Export Task Records Operator

- PRD trace: export tasks need to record operator.
- Scenario/setup: authenticate as a known operator and create CSV and XLSX export tasks.
- Test data:
  - Positive cases: authorized user starts CSV and XLSX exports.
  - Negative cases: unauthenticated or unauthorized request if PRD/project defines access control.
  - Boundary cases: operator display name change after task creation, if identity snapshot rules exist.
  - Stateful cases: inspect task record after creation and after completion.
  - Cleanup requirements: remove test export tasks when safe.
- Steps or review method: create export task; inspect task record through API, database, admin UI, or audit log; verify operator identity is recorded and traceable to the initiating account.
- Pass criteria: task stores a stable operator identifier for every export task and does not rely only on transient request context or log lines.
- Fail criteria: operator is absent, wrong, overwritten by another actor, stored only in non-durable logs, or inconsistent between CSV and XLSX tasks.
- Required evidence: authenticated account, export request, task record with operator field, correlation ID or task ID.
- Mode: Automated.
- Automation level: Required for persistence-level tests once project commands are known.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: auth context propagation, task creation, task persistence, audit/log display.

### BV-004: Export Task Records Filter Criteria

- PRD trace: export tasks need to record filter criteria.
- Scenario/setup: create exports with at least one non-empty filter and one empty/default filter case.
- Test data:
  - Positive cases: date/status/keyword/owner filters if the product supports them.
  - Negative cases: invalid filter if PRD defines validation.
  - Boundary cases: empty filter set and multi-filter combination.
  - Stateful cases: compare stored filter snapshot after task completion.
  - Cleanup requirements: remove test export tasks when safe.
- Steps or review method: request export with filters; inspect export task record; compare stored filter criteria with request payload and exported rows.
- Pass criteria: task stores the effective filter criteria used for export, not just a display label; stored filters are sufficient to audit why the exported rows were included.
- Fail criteria: filters are absent, partially recorded, recorded after mutation, stored in an unauditable format, or do not match exported row set.
- Required evidence: request filter payload, task filter snapshot, exported file sample, source data comparison.
- Mode: Automated.
- Automation level: Required for persistence/query tests once project commands are known.
- Test execution requirement: Conditional.
- Priority: Blocker.
- Retest scope: filter parsing, effective query construction, task persistence, CSV/XLSX output.

## Implementation Audit Standards

### IA-001: Export Query And Data Integrity

- PRD trace: CSV export, XLSX export, filter criteria recording.
- Implementation area: export query builder, serializers, file generators, task creation.
- Review method: inspect code and tests to confirm CSV and XLSX share the same effective dataset/filter logic or have equivalent assertions.
- Pass criteria: export content is derived from the effective filters; CSV and XLSX outputs are consistent for the same request; no unrelated records are exported.
- Fail criteria: format-specific code paths use divergent filters, omit authorization constraints, or serialize stale/unfiltered records.
- Required evidence: code references, query/filter tests, source/export comparison.
- Test coverage requirement: automated coverage required for Blocker paths when commands are available.
- Static fallback: inspect query construction, serializers, and tests.
- Priority: Blocker.
- Retest scope: export query, CSV generator, XLSX generator, task metadata.

### IA-002: XLSX Generation Implementation

- PRD trace: batch export supports XLSX.
- Implementation area: XLSX writer, content type/extension, workbook schema, tests.
- Review method: inspect XLSX generation path and parse generated workbook in tests or review evidence.
- Pass criteria: implementation generates valid XLSX files using deterministic headers and values aligned with CSV/export contract; tests parse workbook content rather than checking file existence only.
- Fail criteria: generated file is not valid XLSX, stores incorrect data types where product requires types, or tests only assert download success.
- Required evidence: XLSX generation code, parser-based test assertions, sample workbook evidence.
- Test coverage requirement: required for successful XLSX export and representative fields.
- Static fallback: inspect generator code and manually parse/open sample file.
- Priority: High.
- Retest scope: XLSX generator, file download/storage, export content comparison.

### IA-003: Export Task Audit Metadata Persistence

- PRD trace: export task records operator and filter criteria.
- Implementation area: task schema/model, task creation transaction, auth context, filter snapshot serialization.
- Review method: inspect schema/model and task creation code; verify tests assert metadata at task creation time.
- Pass criteria: operator and effective filter criteria are persisted durably for each export task and are available for later audit/review.
- Fail criteria: metadata is optional, nullable without blocker, derived only from current user at read time, or captured after filters can change.
- Required evidence: schema/model fields, task creation code, database/API evidence, tests.
- Test coverage requirement: required for CSV and XLSX task creation.
- Static fallback: inspect schema/model/migration and task creation code.
- Priority: Blocker.
- Retest scope: task creation, auth context propagation, filter parsing/snapshot, task history display/API.

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | Existing export test command, project-specific name TBD | BV-001, IA-001, RG-001 | Blocked | command, timestamp, result, failure logs | Static review of existing export tests and assertions. |
| TE-002 | New/updated XLSX and export-task metadata test command, project-specific name TBD | BV-002, BV-003, BV-004, IA-002, IA-003, RG-002 | Blocked | command, timestamp, result, test names, logs | Static review of XLSX parsing tests, task metadata tests, and implementation code. |

## API, Data, And State Standards

- Export format selection must distinguish CSV and XLSX without breaking existing CSV behavior.
- Export task records must include durable operator identity and effective filter criteria.
- Filter criteria evidence must be a snapshot of what was used for export; if the product stores references to saved filters, the audit must verify whether resolved filter values are also retained or otherwise auditable.
- Exact task status lifecycle is blocked unless the PRD or implementation contract defines it.

## Permissions, Security, And Privacy Standards

- Operator recording is release-blocking because missing or incorrect operator metadata breaks auditability.
- Future audit must verify unauthorized users cannot create exports or view export task metadata once the role matrix is known.
- Exported file contents and stored filter criteria may contain sensitive data; exact masking/encryption/retention standards are blocked unless PRD/project defines them.

## Observability, Performance, And Reliability Standards

- Logs or traces should allow correlating export request, task record, and file generation by task ID as a derived quality standard.
- Performance thresholds, maximum export size, retry policy, and retention duration are blocked.

## Regression And Compatibility Standards

- Existing behavior to retest: CSV export, existing filter behavior, export history/task list if present.
- Backward compatibility checks: existing API clients that request CSV must not need changed parameters unless PRD explicitly says so.
- Migration/rollback checks: if task schema adds operator/filter fields, future audit must verify migration/backfill/default behavior.
- Release/feature-flag checks: blocked until project conventions are known.

## Required Evidence For Future Review

- Test results: command, timestamp, environment, pass/fail logs, and linked audit check IDs.
- Files: CSV and XLSX outputs with fixture names and row-count comparison.
- API/UI traces: format selection/request payload, filter criteria, task ID, operator account.
- Database records: export task row/document containing operator and filter criteria.
- Logs/audit events: task creation and file generation correlation ID if available.
- Code references: export controller/job, query builder, CSV generator, XLSX generator, task schema/model, tests.

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
- `Blocker` or `High` checks that are blocked or not run prevent unconditional approval unless sufficient substitute evidence exists.

## Hard Fail Conditions

- Any `Blocker` check fails.
- Any `Blocker` check is `Blocked` or `Not Run` without substitute evidence.
- CSV export regresses while adding XLSX.
- XLSX export is unavailable, corrupt, or exports records inconsistent with the effective filters.
- Export task is created without durable operator identity.
- Export task is created without durable effective filter criteria.
- Export content includes records outside the requested filters or authorization scope.
- Required test commands are not run and no blocker is recorded.
- Evidence cannot be traced to audit check IDs.

## Retest And Regression Rules

- Failed check retest scope: rerun the failed check plus all checks sharing export format, query, or task metadata code.
- Related PRD area regression: XLSX fixes retest CSV parity; metadata fixes retest CSV and XLSX task creation.
- Changed code path test requirements: run affected unit/integration/E2E tests or record blocker and perform static fallback.
- Blocker/High fix verification: requires related regression execution or documented blocker.
- Retest round reporting: record defect ID, fixed build/commit, executed checks, evidence, and residual risk.

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed checks as deprecated; do not reuse IDs.
- This PRD update affects core export behavior and audit metadata; therefore the standards should receive a fresh three-round clean-context review before being treated as final for post-development audit.
- Because this eval run had no subagent tool or actual existing standards file, the review below is an inline approximation and not a substitute for a true clean-context rerun.

## Three-Round Clean-Context Review Record

- Review mode: Inline fallback.
- Reviewer A focus: PRD coverage completeness and traceability.
- Reviewer B focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations.
- Reviewer C focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling.
- Round 1 status: Completed inline; context isolation approximated.
- Round 2 status: Completed inline; context isolation approximated.
- Round 3 status: Completed inline; context isolation approximated.
- Context isolation: Approximated because no subagent tool was available in this run.
- Need fresh three clean-context reviews: Yes. Reason: PRD change adds a new export format and new auditability data requirements; these affect core flow, data integrity, and audit-log behavior.

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| Existing CSV check IDs must remain stable and cannot be repurposed for XLSX. | Round 1 | Accepted | User explicitly required stable existing IDs and appended new IDs. |
| Operator and filter criteria are auditability requirements and should be Blocker gates. | Round 2 | Accepted | Missing metadata breaks traceability for export tasks. |
| Test commands cannot be invented without project context. | Round 3 | Accepted | Project config is unavailable; TE checks remain blocked with static fallback. |
| Define exact XLSX styling/column widths. | Round 1 | Rejected | PRD update only says XLSX support; styling is not specified. |
| Treat inline review as full clean-context review. | Round 3 | Rejected | Context isolation is only approximated; fresh true review is needed. |

## Blocked Checks And Open Questions

| ID | Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- | --- |
| BQ-001 | Source | Where is the actual updated PRD and existing `quality-audit-standards.md`? | Cannot guarantee exact original ID preservation beyond stated assumptions. | Product/QA |
| BQ-002 | XLSX | What worksheet name, column order, headers, data types, and formatting are required? | XLSX pass/fail must focus on validity/content until clarified. | Product |
| BQ-003 | Filters | What filters exist and how are effective filters normalized? | Filter snapshot assertions may miss product-specific fields. | Product/engineering |
| BQ-004 | Operator | Which operator identifier must be stored: user ID, username, display name, tenant, role, or snapshot? | Operator evidence may be incomplete. | Product/security |
| BQ-005 | Permissions | Which roles can export and inspect export task metadata? | Unauthorized access tests blocked. | Product/security |
| BQ-006 | Retention/privacy | How long are export files/tasks retained and should filters/operator metadata be masked? | Privacy and retention audit blocked. | Product/security |
| BQ-007 | Test execution | What commands run unit, integration, E2E, worker, and migration tests? | TE-001/TE-002 execution blocked. | Engineering |

## Assumptions

- `BV-001`, `IA-001`, `TE-001`, and `RG-001` represent the existing CSV/export checks because the old standards file was unavailable.
- The PRD update is additive: CSV remains supported and no requirement was removed.
- Export task recording means durable persistence, not only transient logs, because the PRD says tasks need to record operator and filter criteria.

## Final Quality Gate

- Ready for post-development audit: Yes, with assumptions and blocked project-specific execution details.
- Final conclusion rule ready: Yes.
- Hard fail conditions complete: Yes for the PRD update summary.
- Conditions before use: locate the real old standards file, confirm existing IDs, bind test commands, and run a true three-round clean-context review.
- Checks that must pass before release: BV-001 through BV-004, IA-001 through IA-003, RG-001, RG-002, and executable TE checks once project commands are known.

## Machine-Readable Audit Checks Appendix

```json
{
  "source_status": {
    "prd_update_available": true,
    "existing_standards_found": false,
    "project_context_found": false,
    "id_policy": "preserve assumed existing IDs; append new IDs; do not reuse deprecated IDs"
  },
  "fresh_clean_context_review_required": true,
  "audit_checks": [
    {
      "id": "BV-001",
      "prd_trace": "Existing CSV batch export",
      "layer": "Behavior Verification",
      "category": "csv_export_regression",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "Records available for filtered export.",
      "test_data": {
        "positive_cases": ["CSV export with matching records"],
        "negative_cases": ["Unauthorized or invalid export request if defined"],
        "boundary_cases": ["Empty filtered result"],
        "stateful_cases": ["Task creation then file retrieval"],
        "cleanup_requirements": ["Remove generated files and test tasks"]
      },
      "steps_or_method": "Request CSV export and compare parsed file with source data and filters.",
      "pass_criteria": "CSV remains available and content matches effective filters.",
      "fail_criteria": "CSV disappears, ignores filters, leaks data, or cannot be tied to a task.",
      "required_evidence": ["export request", "filter criteria", "CSV file", "source data comparison", "task ID"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "CSV endpoint/UI, export query, task creation, file retrieval",
      "status": "Ready"
    },
    {
      "id": "BV-002",
      "prd_trace": "New XLSX batch export",
      "layer": "Behavior Verification",
      "category": "xlsx_export",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "Same dataset and filters as CSV regression where possible.",
      "test_data": {
        "positive_cases": ["XLSX export with matching records"],
        "negative_cases": ["Unsupported format if validation exists"],
        "boundary_cases": ["Empty filtered result", "text/date/number fields if present"],
        "stateful_cases": ["Task creation then XLSX retrieval"],
        "cleanup_requirements": ["Remove generated files and test tasks"]
      },
      "steps_or_method": "Request XLSX export, parse workbook, and compare content with source data.",
      "pass_criteria": "Valid XLSX is generated and matches effective filters.",
      "fail_criteria": "Workbook is corrupt, missing data, or includes unfiltered records.",
      "required_evidence": ["export request", "XLSX file", "parsed workbook output", "source data comparison", "task ID"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "XLSX selector/API, generator, storage/retrieval, export query",
      "status": "Ready"
    },
    {
      "id": "BV-003",
      "prd_trace": "Export task records operator",
      "layer": "Behavior Verification",
      "category": "operator_recording",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "Authenticated operator creates CSV and XLSX export tasks.",
      "test_data": {
        "positive_cases": ["Authorized user starts CSV export", "Authorized user starts XLSX export"],
        "negative_cases": ["Unauthenticated/unauthorized request if defined"],
        "boundary_cases": ["Operator profile changes after task creation if relevant"],
        "stateful_cases": ["Inspect task after creation and completion"],
        "cleanup_requirements": ["Remove test tasks"]
      },
      "steps_or_method": "Create export task and verify durable operator field on task record.",
      "pass_criteria": "Every export task stores stable initiating operator identity.",
      "fail_criteria": "Operator is absent, wrong, transient, or inconsistent across formats.",
      "required_evidence": ["authenticated account", "export request", "task operator field", "task ID"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "auth context propagation, task creation, persistence, task history/API",
      "status": "Ready"
    },
    {
      "id": "BV-004",
      "prd_trace": "Export task records filter criteria",
      "layer": "Behavior Verification",
      "category": "filter_criteria_recording",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "Export requests with empty and non-empty filters.",
      "test_data": {
        "positive_cases": ["Single filter", "multiple filters"],
        "negative_cases": ["Invalid filter if defined"],
        "boundary_cases": ["Empty/default filter set"],
        "stateful_cases": ["Compare stored snapshot after task completion"],
        "cleanup_requirements": ["Remove test tasks"]
      },
      "steps_or_method": "Create filtered export and compare stored filter snapshot with request and exported rows.",
      "pass_criteria": "Task stores effective filter criteria sufficient for later audit.",
      "fail_criteria": "Filters are absent, partial, stale, unauditable, or inconsistent with exported rows.",
      "required_evidence": ["request filter payload", "task filter snapshot", "exported file sample", "source data comparison"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "filter parsing, query construction, task persistence, CSV/XLSX output",
      "status": "Ready"
    },
    {
      "id": "IA-002",
      "prd_trace": "New XLSX batch export",
      "layer": "Implementation Audit",
      "category": "xlsx_generation",
      "priority": "High",
      "mode": "Review-only",
      "automation_level": "Required",
      "setup": "Implementation source and generated workbook fixture.",
      "test_data": {
        "positive_cases": ["Representative workbook parse"],
        "negative_cases": ["Generator failure path if defined"],
        "boundary_cases": ["Empty workbook/result"],
        "stateful_cases": [],
        "cleanup_requirements": []
      },
      "steps_or_method": "Inspect XLSX generator and parser-based tests.",
      "pass_criteria": "Generated XLSX is valid and content assertions verify values.",
      "fail_criteria": "Tests only check file existence or generator creates invalid workbook.",
      "required_evidence": ["XLSX generator code", "parser assertions", "sample workbook evidence"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "XLSX generator, file download/storage, export content comparison",
      "status": "Ready"
    },
    {
      "id": "IA-003",
      "prd_trace": "Export task records operator and filter criteria",
      "layer": "Implementation Audit",
      "category": "task_audit_metadata",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Required",
      "setup": "Task schema/model and creation code.",
      "test_data": {
        "positive_cases": ["CSV task metadata", "XLSX task metadata"],
        "negative_cases": ["Missing auth/filter context if tests support it"],
        "boundary_cases": ["Empty filter set"],
        "stateful_cases": ["Metadata after task completion"],
        "cleanup_requirements": []
      },
      "steps_or_method": "Inspect schema/model, task creation, and persistence tests.",
      "pass_criteria": "Operator and effective filters are persisted durably at task creation.",
      "fail_criteria": "Metadata is optional, nullable without blocker, transient, or captured after mutation.",
      "required_evidence": ["schema/model fields", "task creation code", "database/API evidence", "tests"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "task creation, auth propagation, filter snapshot, task history/API",
      "status": "Ready"
    },
    {
      "id": "RG-002",
      "prd_trace": "Export task auditability",
      "layer": "Risk Gate",
      "category": "export_auditability",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "CSV and XLSX task records available.",
      "test_data": {
        "positive_cases": ["CSV task with operator/filter", "XLSX task with operator/filter"],
        "negative_cases": ["Blocked creation without durable metadata if implementation can simulate it"],
        "boundary_cases": ["Empty/default filters"],
        "stateful_cases": ["Task record after completion"],
        "cleanup_requirements": ["Remove test tasks"]
      },
      "steps_or_method": "Verify no export task exists without operator and effective filter criteria.",
      "pass_criteria": "All export tasks are auditable by operator and filter snapshot.",
      "fail_criteria": "Any export task lacks operator or filter criteria evidence.",
      "required_evidence": ["task records", "operator identity", "filter snapshot", "task IDs"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "all export task creation paths and formats",
      "status": "Ready"
    }
  ],
  "blocked_questions": [
    {"id": "BQ-001", "area": "Source", "question": "Where is the actual updated PRD and existing standards file?"},
    {"id": "BQ-002", "area": "XLSX", "question": "What worksheet name, column order, headers, data types, and formatting are required?"},
    {"id": "BQ-003", "area": "Filters", "question": "What filters exist and how are effective filters normalized?"},
    {"id": "BQ-004", "area": "Operator", "question": "Which operator identifier or snapshot must be stored?"},
    {"id": "BQ-005", "area": "Permissions", "question": "Which roles can export and inspect export task metadata?"},
    {"id": "BQ-006", "area": "Retention/privacy", "question": "How long are export files/tasks retained and should metadata be masked?"},
    {"id": "BQ-007", "area": "Test execution", "question": "What project commands run the required tests?"}
  ]
}
```
