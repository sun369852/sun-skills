# Lead Import Quality Audit Standards

## Source And Scope

- Source PRD: `specs/lead-import/prd.md` was referenced but not found under `D:\sun-skills\prd-quality-audit-standards-workspace\iteration-1\eval-2-lead-import`.
- Available PRD source: prompt summary only: CSV upload, field mapping, duplicate lead detection, import preview, background import jobs, and import history.
- Supporting context: project path was said to be provided, but the referenced eval/project directory did not exist during bounded inspection.
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents.
- In scope: verify completed implementation against the six summarized feature areas and explicitly block undefined product rules.
- Out of scope: inventing CSV schema, duplicate matching rules, role model, performance thresholds, exact UI copy, retention policy, or import error semantics not present in the available PRD summary.

## Project Context Inspection

- Project path: `D:\sun-skills\prd-quality-audit-standards-workspace\iteration-1\eval-2-lead-import` was referenced but missing.
- Context inspection mode: Not available.
- Inspected files:

| File | Reason Inspected | Impact On Audit Standards |
| --- | --- | --- |
| `D:\sun-skills\prd-quality-audit-standards-workspace\iteration-1` | Bounded lookup for the referenced eval directory | Directory was empty for this eval; project-specific commands, routes, schemas, and tests are blocked. |
| `D:\sun-skills\prd-quality-audit-standards-workspace` | Bounded lookup for any `prd.md` and `outputs` conventions | No `prd.md` found; standards use prompt summary as source boundary. |

## Audit Environment Requirements

- Required services: application runtime, database, file/object storage if used, background worker/queue if used.
- Required accounts/roles: blocked until PRD or project defines who can upload/import leads.
- Required test data: CSV files covering valid rows, invalid rows, duplicate rows, unmapped fields, and large imports; exact columns and valid values are blocked.
- Required secrets/sandboxes: blocked until project dependencies are known.
- Setup commands: blocked because package/test configuration is unavailable.
- Known environment limitations: future audit agent must locate the real PRD and project before executing commands; this document can guide audit scope but cannot name concrete test commands.

## Readiness Summary

- Status: Blocked for unconditional post-development audit because source PRD and project context are missing.
- Intended primary executor: Implementation audit agent and test audit agent.
- Requirements mapped: 6 summarized feature areas.
- Blocked or ambiguous requirements: 15 blocked questions.
- Release-blocking gates: 7.
- Machine-readable appendix: Included.

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | CSV upload | Valid CSV upload is accepted and invalid upload paths are rejected or reported according to defined rules. | Behavior Verification | Blocker | Blocked | Static fallback | Upload request/UI evidence, parser result, error evidence | Blocked |
| BV-002 | Field mapping | User can map CSV columns to lead fields before import. | Behavior Verification | Blocker | Blocked | Static fallback | Mapping UI/API evidence and saved mapping state | Blocked |
| BV-003 | Duplicate lead detection | Duplicate leads are identified before or during import. | Behavior Verification | Blocker | Blocked | Static fallback | Duplicate detection input/output evidence | Blocked |
| BV-004 | Import preview | Preview shows pending import results before commit. | Behavior Verification | High | Blocked | Static fallback | Preview screen/API response and row-level status evidence | Blocked |
| BV-005 | Background import task | Confirmed import runs as a background job and reaches terminal status. | Behavior Verification | Blocker | Blocked | Static fallback | Job record, status transition, worker log | Blocked |
| BV-006 | Import history | Completed imports are visible in import history. | Behavior Verification | High | Blocked | Static fallback | History UI/API response and persisted import record | Blocked |
| IA-001 | CSV upload/import data integrity | Implementation validates file parsing and avoids partial data corruption. | Implementation Audit | Blocker | Review-only | Static fallback | Code references, parser tests, database before/after records | Ready |
| IA-002 | Duplicate detection | Implementation uses one explicit duplicate strategy consistently. | Implementation Audit | Blocker | Blocked | Static fallback | Duplicate matching code/tests | Blocked |
| IA-003 | Background import task | Implementation persists job state and handles retry/failure visibility. | Implementation Audit | High | Blocked | Static fallback | Queue/job code, status schema, failure logs | Blocked |
| TE-001 | Unknown project tests | Future audit must run relevant automated tests once commands are known. | Test Execution | High | Blocked | Blocked | Command, timestamp, result, failure logs | Blocked |
| RG-001 | Core import flow | Upload -> mapping -> duplicate detection -> preview -> background import -> history has no missing stage. | Risk Gate | Blocker | Blocked | Static fallback | End-to-end evidence tied to all BV IDs | Blocked |

## Behavior Verification Standards

### BV-001: CSV Upload

- PRD trace: CSV upload.
- Scenario/setup: Use at least one valid CSV and invalid CSV cases once PRD defines file format limits.
- Test data:
  - Positive cases: CSV with all required lead data.
  - Negative cases: blocked until PRD defines invalid file type, malformed CSV, empty file, missing required columns, and encoding behavior.
  - Boundary cases: blocked until PRD defines file size, row count, and column count limits.
  - Stateful cases: repeat upload and abandoned upload.
  - Cleanup requirements: remove imported test leads and uploaded files where applicable.
- Steps or review method: Submit CSV through the intended UI/API; verify accepted uploads progress to mapping and rejected uploads do not create import jobs or lead records unless PRD says otherwise.
- Pass criteria: CSV upload behavior matches explicit PRD rules; accepted file can be mapped; rejected file has traceable error evidence.
- Fail criteria: invalid files create leads/jobs, accepted files cannot proceed, or upload results cannot be audited.
- Required evidence: request/screenshot, file fixture name, server response, created upload/import identifier, and any validation error.
- Mode: Blocked.
- Automation level: Blocked until PRD and project test framework are available.
- Test execution requirement: Static fallback.
- Priority: Blocker.
- Retest scope: upload validation, mapping entry point, job creation guard, and file cleanup.
- Notes: Exact file constraints are blocked.

### BV-002: Field Mapping

- PRD trace: field mapping.
- Scenario/setup: Start from an accepted CSV upload.
- Test data: CSV with headers that require mapping to lead fields; exact required lead fields are blocked.
- Steps or review method: Map columns to lead fields; submit mapping; verify mapping is used by preview/import.
- Pass criteria: selected mappings persist through preview and import; unmapped or invalid required fields are handled according to PRD.
- Fail criteria: mapping choices are ignored, impossible mappings are accepted without defined behavior, or import proceeds with missing required data contrary to PRD.
- Required evidence: mapping UI/API payload, saved mapping state, preview rows showing mapped values.
- Mode: Blocked.
- Automation level: Recommended once UI/API and field rules are known.
- Test execution requirement: Static fallback.
- Priority: Blocker.
- Retest scope: upload, mapping, preview, import persistence.
- Notes: Required fields, optional fields, transformations, and default values are blocked.

### BV-003: Duplicate Lead Detection

- PRD trace: duplicate lead detection.
- Scenario/setup: Prepare existing leads and CSV rows that should and should not match duplicates.
- Test data: blocked until PRD defines duplicate criteria.
- Steps or review method: Run preview/import with duplicate candidates and verify duplicate flags/actions.
- Pass criteria: duplicate detection follows the PRD-defined matching rule and prevents/marks/merges duplicates only as specified.
- Fail criteria: duplicate rows are silently imported when PRD forbids it, non-duplicates are incorrectly blocked, or duplicate handling is untraceable.
- Required evidence: existing lead records, CSV rows, duplicate detection output, final lead records.
- Mode: Blocked.
- Automation level: Required for core duplicate rules once defined.
- Test execution requirement: Static fallback.
- Priority: Blocker.
- Retest scope: duplicate detector, preview, import commit, import history counts.
- Notes: Matching keys and duplicate resolution behavior are blocked.

### BV-004: Import Preview

- PRD trace: import preview.
- Scenario/setup: Complete upload and mapping before commit.
- Test data: valid rows, invalid rows, and duplicates where rules are defined.
- Steps or review method: Open preview and verify displayed row statuses/counts match parser, mapping, and duplicate results.
- Pass criteria: preview presents enough information to decide whether to import; preview numbers match final import behavior.
- Fail criteria: preview omits critical invalid/duplicate state, shows counts inconsistent with import, or commits without preview when PRD requires preview.
- Required evidence: preview screenshot/API response, row status sample, summary counts.
- Mode: Blocked.
- Automation level: Recommended.
- Test execution requirement: Static fallback.
- Priority: High.
- Retest scope: mapping, duplicate detection, import commit, history summary.
- Notes: Exact preview fields and copy are blocked.

### BV-005: Background Import Task

- PRD trace: background import task.
- Scenario/setup: Confirm an import from preview.
- Test data: import fixture with enough rows to exercise asynchronous job behavior; exact size threshold is blocked.
- Steps or review method: Start import; verify job creation, non-blocking processing if applicable, terminal status, and lead persistence.
- Pass criteria: import runs through a tracked background task and reaches success/failure state with accurate results.
- Fail criteria: import loses rows, double-processes rows, hides failures, or cannot be correlated to the source upload.
- Required evidence: job ID, status transitions, worker log, created/failed row counts, final database records.
- Mode: Blocked.
- Automation level: Required for job lifecycle once test framework is known.
- Test execution requirement: Static fallback.
- Priority: Blocker.
- Retest scope: queue worker, database writes, duplicate guard, history record.
- Notes: Retry, cancellation, timeout, and partial failure rules are blocked.

### BV-006: Import History

- PRD trace: import history.
- Scenario/setup: Complete successful and failed/partial imports once failure semantics are known.
- Test data: at least one completed import and one non-success import if PRD supports failures.
- Steps or review method: Navigate to or request import history; verify records reflect upload/import outcomes.
- Pass criteria: history lists imports with accurate status, counts, timing, and accessible details as defined by PRD.
- Fail criteria: completed imports are missing, counts/statuses diverge from job records, or history exposes data to unauthorized users.
- Required evidence: history UI/API response, related job record, related lead records.
- Mode: Blocked.
- Automation level: Recommended.
- Test execution requirement: Static fallback.
- Priority: High.
- Retest scope: import job completion, history persistence, permissions.
- Notes: Retention, filters, visible fields, and role access are blocked.

## Implementation Audit Standards

### IA-001: Import Data Integrity

- PRD trace: CSV upload, mapping, preview, background import task.
- Implementation area: parser, validation, mapping application, import transaction/data access.
- Review method: Inspect implementation and tests to confirm rows are not silently dropped, duplicated, or written with wrong mapped values.
- Pass criteria: code has explicit parser/mapping validation, import writes can be traced from upload row to lead record, and partial failures do not corrupt unrelated rows.
- Fail criteria: row processing has no deterministic mapping path, no failed-row handling, or creates records before required validation/preview gates.
- Required evidence: code references, row fixture, before/after database records, test assertions.
- Test coverage requirement: automated coverage required for Blocker paths when test commands are available; otherwise static fallback must inspect tests and assertions.
- Static fallback: review parser, mapper, importer, model/schema, and tests.
- Priority: Blocker.
- Retest scope: parser, mapper, importer, duplicate detection, history counts.

### IA-002: Duplicate Detection Strategy

- PRD trace: duplicate lead detection.
- Implementation area: duplicate matching code, database queries/indexes, import decision logic.
- Review method: Verify one explicit duplicate rule is implemented and covered by tests after PRD defines it.
- Pass criteria: matching logic, query filters, and import behavior align with PRD-defined duplicate criteria.
- Fail criteria: duplicate logic is implicit, inconsistent across preview/import, or missing.
- Required evidence: duplicate rule code, tests, query/database evidence.
- Test coverage requirement: required after duplicate criteria are unblocked.
- Static fallback: blocked until PRD defines duplicate criteria.
- Priority: Blocker.
- Retest scope: duplicate detector, preview, import commit, history counts.

### IA-003: Background Job State And Failure Visibility

- PRD trace: background import task, import history.
- Implementation area: queue/worker, job table/schema, status transitions, logs.
- Review method: Inspect job lifecycle and failure path.
- Pass criteria: each import has a durable job/history record and terminal state; failures are visible to users/auditors according to PRD.
- Fail criteria: jobs can disappear, retry creates duplicate leads, or history reports success for failed imports.
- Required evidence: job schema/record, worker code, logs with correlation ID, tests.
- Test coverage requirement: required for success and failure paths when project commands are known.
- Static fallback: inspect queue worker and persistence code.
- Priority: High.
- Retest scope: worker, persistence, duplicate guard, history.

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | Blocked: project test command unavailable | All BV/IA/RG checks | Blocked | command, timestamp, result, logs | Inspect test files and implementation once project exists; record blocker if no tests exist. |
| TE-002 | End-to-end import workflow test suite, name TBD | BV-001 through BV-006, RG-001 | Conditional | E2E result, fixture names, screenshots/API traces | Static review of route/controller/UI tests. |
| TE-003 | Import unit/integration tests, name TBD | IA-001 through IA-003 | Conditional | unit/integration result and assertions | Static review of parser/mapper/worker test assertions. |

## UI, UX, And Accessibility Standards

- CSV upload, mapping, preview, progress/status, and history screens must expose the PRD-required states once those states are known.
- Keyboard/focus/accessibility criteria are blocked because the PRD summary does not mention accessibility requirements. Future audit may apply project baseline accessibility standards as derived quality standards, labeled separately.
- Error copy is blocked unless the PRD defines messages.

## API, Data, And State Standards

- Import lifecycle must preserve traceability from upload to mapping to preview to job to history.
- Exact statuses are blocked. Future audit must not substitute arbitrary statuses such as `pending`, `processing`, or `completed` unless defined by PRD or implementation contract accepted by product.
- Data retention, rollback, cancellation, and partial failure behavior are blocked.

## Permissions, Security, And Privacy Standards

- Role/permission matrix is blocked.
- Future audit must verify unauthorized users cannot upload CSVs, start imports, view import previews, or read import history once roles are defined.
- Sensitive lead data handling is blocked until PRD/project defines fields and privacy expectations.

## Integration And External Dependency Standards

- External CRM/sales integration behavior is blocked because the PRD summary does not mention external systems.
- Background queue/storage dependencies must be audited if present in project context.

## Observability, Performance, And Reliability Standards

- Logs should allow correlating upload, preview, job, and history evidence by import/job ID as a derived quality standard because the PRD includes asynchronous import history.
- Performance thresholds, maximum CSV size, timeout, retry count, and concurrency behavior are blocked.

## Regression And Compatibility Standards

- Existing behavior to retest: lead creation/search/listing affected by imported records, if present in project.
- Backward compatibility checks: blocked until existing lead schema/API are known.
- Migration/rollback checks: blocked until implementation uses schema changes.
- Release/feature-flag checks: blocked until project conventions are known.

## Required Evidence For Future Review

- Test results: command, timestamp, environment, pass/fail logs, and linked audit check IDs.
- Screenshots or recordings: upload, mapping, preview, job/progress if UI exists, history.
- API traces: request payloads excluding secrets, response bodies, status codes, import/job IDs.
- Database records: upload/import job records, lead records, duplicate candidates, history rows.
- Logs/audit events: worker logs, failure logs, correlation IDs.
- Accessibility/performance reports: only if PRD or project baseline requires them.
- Code references: parser, mapper, duplicate detector, importer, job worker, history endpoint/UI, tests.

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
- The upload -> mapping -> duplicate detection -> preview -> background import -> history flow has any missing stage.
- Duplicate detection has no PRD-defined rule and no approved product clarification before release.
- Import creates duplicate, corrupt, or unmapped lead records.
- Background jobs can fail without visible status/history evidence.
- Required test commands are not run and no blocker is recorded.
- Evidence cannot be traced to audit check IDs.

## Retest And Regression Rules

- Failed check retest scope: rerun the failed check and all checks in the same PRD area.
- Related PRD area regression: duplicate fixes retest preview/import/history; job fixes retest import persistence/history.
- Changed code path test requirements: run affected unit/integration/E2E tests, or record blocker and perform static fallback.
- Blocker/High fix verification: requires related regression execution or documented blocker.
- Retest round reporting: record defect ID, fixed build/commit, executed checks, evidence, and residual risk.

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes or when the missing PRD becomes available.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed checks as deprecated; do not reuse IDs.
- Rerun three clean-context reviews when changes affect core flows, permissions, data integrity, integrations, asynchronous jobs, or risk levels.
- For small non-behavioral wording changes, run local update plus quality gate.

## Three-Round Clean-Context Review Record

- Review mode: Inline fallback.
- Reviewer A focus: PRD coverage completeness and traceability.
- Reviewer B focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations.
- Reviewer C focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling.
- Round 1 status: Completed inline; context isolation approximated.
- Round 2 status: Completed inline; context isolation approximated.
- Round 3 status: Completed inline; context isolation approximated.
- Context isolation: Approximated because no subagent tool was available in this run.

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| Source PRD and project files are missing; document must not claim full readiness. | Round 1 / Round 3 | Accepted | User instructed to treat missing files as available PRD summary and state missing context. |
| Duplicate detection must be Blocker risk because wrong behavior can create duplicate or lost leads. | Round 2 | Accepted | PRD summary explicitly includes duplicate lead detection and import writes data. |
| Test commands cannot be invented. | Round 3 | Accepted | Project context unavailable; command execution standards remain blocked. |
| Add arbitrary CSV size/performance thresholds. | Round 2 | Rejected | PRD summary does not define thresholds. |
| Require accessibility checks as release blockers. | Round 3 | Rejected | Not PRD-derived; may be project baseline later, but blocked here. |

## Blocked Checks And Open Questions

| Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- |
| Source | Where is the actual `specs/lead-import/prd.md` and project root? | Cannot verify complete requirement coverage or commands. | Product/engineering |
| CSV upload | What file types, encodings, delimiters, size limits, and row limits are allowed? | Upload validation tests blocked. | Product |
| CSV validation | Which columns are required and what row-level validation rules apply? | Invalid-row pass/fail criteria blocked. | Product |
| Field mapping | What lead fields are required, optional, transformable, or defaulted? | Mapping tests blocked. | Product |
| Field mapping | Can mappings be saved/reused? | Persistence/history checks blocked. | Product |
| Duplicate detection | What fields define a duplicate lead? | Duplicate tests blocked. | Product |
| Duplicate handling | Are duplicates skipped, blocked, merged, updated, or imported with warning? | Import outcome criteria blocked. | Product |
| Preview | What fields, counts, row statuses, and actions must preview show? | Preview UI/API criteria blocked. | Product |
| Preview | Can user import partial valid rows when invalid/duplicate rows exist? | Partial import criteria blocked. | Product |
| Background job | What statuses, retries, cancellation, timeout, and failure semantics exist? | Job lifecycle tests blocked. | Product/engineering |
| History | What history fields, retention, filters, and detail view are required? | History acceptance tests blocked. | Product |
| Permissions | Which roles can upload, import, and view history? | Security tests blocked. | Product/security |
| Privacy | Which lead fields are sensitive and how should CSV/import data be protected? | Privacy/security audit blocked. | Product/security |
| Performance | What performance targets apply to upload, preview, and job processing? | Performance tests blocked. | Product/engineering |
| Test execution | What commands and environments run unit, integration, E2E, worker, and migration tests? | Automated audit execution blocked. | Engineering |

## Assumptions

- The prompt summary is treated as the only available PRD source because the referenced PRD file was missing.
- The feature writes lead data; therefore data integrity and duplicate handling are release-blocking risks.
- Background import implies a durable job or equivalent traceable asynchronous process; exact implementation is not prescribed.

## Final Quality Gate

- Ready for post-development audit: No, blocked until the actual PRD/project context is available.
- Final conclusion rule ready: Yes.
- Hard fail conditions complete: Yes for the available summary; must be revalidated against the real PRD.
- Conditions before use: locate PRD, inspect project test/config/API/schema/worker/history files, resolve blocked product questions, replace blocked commands with real commands.
- Checks that must pass before release: BV-001 through BV-006, IA-001 through IA-003, RG-001, and all future PRD-derived Blocker checks.

## Machine-Readable Audit Checks Appendix

```json
{
  "source_status": {
    "prd_found": false,
    "project_context_found": false,
    "source_used": "prompt summary only"
  },
  "audit_checks": [
    {
      "id": "BV-001",
      "prd_trace": "CSV upload",
      "layer": "Behavior Verification",
      "category": "csv_upload",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Blocked",
      "setup": "Valid and invalid CSV fixtures after PRD defines file rules.",
      "test_data": {
        "positive_cases": ["CSV with all required lead data"],
        "negative_cases": ["Blocked until invalid upload rules are defined"],
        "boundary_cases": ["Blocked until file size and row limits are defined"],
        "stateful_cases": ["Repeat upload", "abandoned upload"],
        "cleanup_requirements": ["Remove test leads and uploaded files where applicable"]
      },
      "steps_or_method": "Submit CSV through intended UI/API and verify progression or rejection.",
      "pass_criteria": "Accepted and rejected upload behavior matches explicit PRD rules.",
      "fail_criteria": "Invalid files create leads/jobs, accepted files cannot proceed, or upload is unauditable.",
      "required_evidence": ["file fixture", "request or screenshot", "response", "upload/import identifier"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "upload validation, mapping entry point, job creation guard, file cleanup",
      "status": "Blocked"
    },
    {
      "id": "BV-002",
      "prd_trace": "Field mapping",
      "layer": "Behavior Verification",
      "category": "field_mapping",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Recommended",
      "setup": "Accepted CSV upload.",
      "test_data": {
        "positive_cases": ["CSV headers mapped to lead fields"],
        "negative_cases": ["Blocked until required fields are defined"],
        "boundary_cases": [],
        "stateful_cases": ["Mapping used by preview and import"],
        "cleanup_requirements": ["Remove test import records"]
      },
      "steps_or_method": "Map CSV columns to lead fields and verify mapping persists through preview/import.",
      "pass_criteria": "Mappings are applied consistently.",
      "fail_criteria": "Mappings are ignored or invalid mappings proceed contrary to PRD.",
      "required_evidence": ["mapping payload", "saved mapping state", "preview rows"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "upload, mapping, preview, import persistence",
      "status": "Blocked"
    },
    {
      "id": "BV-003",
      "prd_trace": "Duplicate lead detection",
      "layer": "Behavior Verification",
      "category": "duplicate_detection",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Required",
      "setup": "Existing leads and CSV duplicate candidates after duplicate criteria are defined.",
      "test_data": {
        "positive_cases": ["Defined duplicate candidates"],
        "negative_cases": ["Defined non-duplicates"],
        "boundary_cases": ["Blocked until matching rules are defined"],
        "stateful_cases": ["Duplicate detection in preview and import commit"],
        "cleanup_requirements": ["Remove duplicate test records"]
      },
      "steps_or_method": "Run preview/import and verify duplicate flags/actions.",
      "pass_criteria": "Duplicate behavior follows PRD-defined rule.",
      "fail_criteria": "Duplicates are silently imported when forbidden or non-duplicates are incorrectly blocked.",
      "required_evidence": ["existing records", "CSV rows", "duplicate output", "final lead records"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "duplicate detector, preview, import commit, history counts",
      "status": "Blocked"
    },
    {
      "id": "BV-004",
      "prd_trace": "Import preview",
      "layer": "Behavior Verification",
      "category": "import_preview",
      "priority": "High",
      "mode": "Blocked",
      "automation_level": "Recommended",
      "setup": "Completed upload and mapping.",
      "test_data": {
        "positive_cases": ["Valid rows"],
        "negative_cases": ["Invalid rows once rules are known"],
        "boundary_cases": [],
        "stateful_cases": ["Preview before commit"],
        "cleanup_requirements": ["Remove test preview/import records"]
      },
      "steps_or_method": "Verify preview row statuses and counts before import commit.",
      "pass_criteria": "Preview information matches parser, mapping, duplicate results, and final import.",
      "fail_criteria": "Preview omits critical state or shows counts inconsistent with import.",
      "required_evidence": ["preview screenshot or response", "row status sample", "summary counts"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "mapping, duplicate detection, import commit, history summary",
      "status": "Blocked"
    },
    {
      "id": "BV-005",
      "prd_trace": "Background import task",
      "layer": "Behavior Verification",
      "category": "background_import",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Required",
      "setup": "Confirmed import from preview.",
      "test_data": {
        "positive_cases": ["Import fixture with valid rows"],
        "negative_cases": ["Failure fixture once failure semantics are known"],
        "boundary_cases": ["Blocked until async thresholds are defined"],
        "stateful_cases": ["Job status transitions"],
        "cleanup_requirements": ["Remove leads, jobs, and uploaded files"]
      },
      "steps_or_method": "Start import and verify job creation, terminal status, and lead persistence.",
      "pass_criteria": "Tracked background task reaches accurate success/failure state.",
      "fail_criteria": "Rows are lost, double-processed, or failures are hidden.",
      "required_evidence": ["job ID", "status transitions", "worker log", "created/failed row counts", "database records"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "queue worker, database writes, duplicate guard, history",
      "status": "Blocked"
    },
    {
      "id": "BV-006",
      "prd_trace": "Import history",
      "layer": "Behavior Verification",
      "category": "import_history",
      "priority": "High",
      "mode": "Blocked",
      "automation_level": "Recommended",
      "setup": "Completed import records.",
      "test_data": {
        "positive_cases": ["Completed successful import"],
        "negative_cases": ["Failed/partial import if PRD supports it"],
        "boundary_cases": [],
        "stateful_cases": ["History after job completion"],
        "cleanup_requirements": ["Remove history/test records if safe"]
      },
      "steps_or_method": "Open/request import history and compare records to job and lead data.",
      "pass_criteria": "History accurately reflects import outcomes.",
      "fail_criteria": "History omits records, shows wrong counts/statuses, or leaks unauthorized data.",
      "required_evidence": ["history screenshot or response", "job record", "lead records"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "job completion, history persistence, permissions",
      "status": "Blocked"
    },
    {
      "id": "IA-001",
      "prd_trace": "CSV upload, field mapping, import preview, background import task",
      "layer": "Implementation Audit",
      "category": "data_integrity",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Required when project tests are available",
      "setup": "Implementation source and tests.",
      "test_data": {
        "positive_cases": ["Mapped valid row"],
        "negative_cases": ["Invalid row after validation rules are known"],
        "boundary_cases": [],
        "stateful_cases": ["Row trace from upload to lead record"],
        "cleanup_requirements": []
      },
      "steps_or_method": "Inspect parser, mapping, validation, and import persistence.",
      "pass_criteria": "Rows are deterministically validated, mapped, written, and auditable.",
      "fail_criteria": "Rows are silently dropped, duplicated, or written with wrong fields.",
      "required_evidence": ["code references", "fixture", "before/after records", "test assertions"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "parser, mapper, importer, duplicate detection, history counts",
      "status": "Ready"
    },
    {
      "id": "RG-001",
      "prd_trace": "Full lead import workflow",
      "layer": "Risk Gate",
      "category": "end_to_end_integrity",
      "priority": "Blocker",
      "mode": "Blocked",
      "automation_level": "Required",
      "setup": "Complete project and PRD context.",
      "test_data": {
        "positive_cases": ["End-to-end import fixture"],
        "negative_cases": ["Invalid and duplicate rows after rules are known"],
        "boundary_cases": [],
        "stateful_cases": ["upload -> mapping -> duplicate detection -> preview -> job -> history"],
        "cleanup_requirements": ["Remove all test records"]
      },
      "steps_or_method": "Verify no stage is missing from the core import flow.",
      "pass_criteria": "All six PRD feature areas pass or have approved substitute evidence.",
      "fail_criteria": "Any core stage is missing, unauditable, or fails.",
      "required_evidence": ["evidence for BV-001 through BV-006", "job/history correlation"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "entire import workflow",
      "status": "Blocked"
    }
  ],
  "blocked_questions": [
    {"id": "BQ-001", "area": "Source", "question": "Where is the actual PRD and project root?"},
    {"id": "BQ-002", "area": "CSV upload", "question": "What file format, encoding, size, and row limits apply?"},
    {"id": "BQ-003", "area": "CSV validation", "question": "Which columns and row validations are required?"},
    {"id": "BQ-004", "area": "Field mapping", "question": "Which lead fields are required, optional, transformable, or defaulted?"},
    {"id": "BQ-005", "area": "Duplicate detection", "question": "What fields define a duplicate?"},
    {"id": "BQ-006", "area": "Duplicate handling", "question": "What should happen to duplicate rows?"},
    {"id": "BQ-007", "area": "Preview", "question": "What row statuses, counts, and actions must preview show?"},
    {"id": "BQ-008", "area": "Background job", "question": "What statuses, retries, cancellation, timeout, and failure semantics exist?"},
    {"id": "BQ-009", "area": "History", "question": "What history fields, retention, filters, and detail view are required?"},
    {"id": "BQ-010", "area": "Permissions", "question": "Which roles can upload, import, and view history?"},
    {"id": "BQ-011", "area": "Test execution", "question": "What test commands and environments should be used?"}
  ]
}
```
