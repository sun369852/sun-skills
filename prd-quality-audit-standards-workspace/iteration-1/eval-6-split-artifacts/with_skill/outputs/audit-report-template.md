# Audit Report Template

## Audit Metadata

- Audit report ID:
- Auditor:
- Audit date:
- Source standards: `quality-audit-standards.md`
- Machine-readable checks: `audit-checks.json`
- Implementation version/commit:
- Environment:
- Final conclusion: Approved / Approved with Risks / Rejected / Blocked

## Execution Summary

| Status | Count |
| --- | ---: |
| Pass |  |
| Fail |  |
| Blocked |  |
| Not Run |  |
| Not Applicable |  |

## Check Results

| Audit Check ID | PRD Trace | Status | Evidence References | Defect ID | Notes |
| --- | --- | --- | --- | --- | --- |
| BV-001 | Web user workflows |  |  |  |  |
| BV-002 | Background task processing |  |  |  |  |
| BV-003 | External payment callback handling |  |  |  |  |
| BV-004 | Data migration |  |  |  |  |
| BV-005 | Audit reports |  |  |  |  |
| IA-001 | Cross-surface permissions and data access |  |  |  |  |
| IA-002 | Payment, job, migration, and report auditability |  |  |  |  |
| IA-003 | Data integrity across surfaces |  |  |  |  |
| TE-001 | Test execution requirements |  |  |  |  |
| RG-001 | Release approval gate |  |  |  |  |

## Required Evidence Log

| Evidence ID | Audit Check ID | Evidence Type | Location / Reference | Timestamp | Notes |
| --- | --- | --- | --- | --- | --- |
| EV-001 |  | Test output / screenshot / API trace / DB query / log / code reference |  |  |  |

## Defect Reports

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

## Blocked Or Not Run Checks

| Audit Check ID | Reason | Required Unblock Condition | Substitute Evidence | Release Impact |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Retest Record

| Defect ID | Retested Check IDs | Regression Scope | Result | Evidence |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Final Gate Decision

- Any `Blocker` check failed: Yes / No
- Any `Blocker` check blocked or not run without substitute evidence: Yes / No
- Core PRD flow without coverage: Yes / No
- Required test execution skipped without blocker: Yes / No
- Evidence traceability complete: Yes / No
- Risk acceptance references, if any:
- Final decision rationale:

