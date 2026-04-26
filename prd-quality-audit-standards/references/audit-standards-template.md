# Audit Standards Template

Use this structure for the saved Markdown artifact. Adapt section names when the project has a strong existing convention, but preserve the same information.

````markdown
# [Feature Name] Quality Audit Standards

## Source And Scope

- Source PRD: [path or pasted content summary]
- Supporting context: [technical design/task archive/project files, or "none"]
- Audit purpose: post-development verification contract for implementation audit agents and test audit agents
- In scope:
- Out of scope:

## Project Context Inspection

- Project path: [path or "not provided"]
- Context inspection mode: Bounded / Not available
- Inspected files:

| File | Reason Inspected | Impact On Audit Standards |
| --- | --- | --- |
| [path] | [test config/API/schema/auth/logging/etc.] | [commands, evidence, compatibility, or constraints] |

## Audit Environment Requirements

- Required services:
- Required accounts/roles:
- Required test data:
- Required secrets/sandboxes:
- Setup commands:
- Known environment limitations:

## Readiness Summary

- Status: Ready / Ready with assumptions / Blocked
- Draft admission: Admitted - Ready / Admitted - Blocked / Rejected - Rewrite
- Intended primary executor: Implementation audit agent / Test audit agent
- Requirements mapped: [count]
- Blocked or ambiguous requirements: [count]
- Release-blocking gates: [count]
- Machine-readable appendix: Included / External file / Not produced

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | [PRD item] | [Pass/fail standard] | Behavior Verification | Blocker/High/Medium/Low | Automated/Manual/Review-only/Blocked | Required/Conditional/Static fallback/N/A | [Required evidence] | Ready/Blocked |

## Behavior Verification Standards

### BV-001: [Check Name]

- PRD trace:
- Scenario/setup:
- Test data:
  - Positive cases:
  - Negative cases:
  - Boundary cases:
  - Stateful cases:
  - Cleanup requirements:
- Steps or review method:
- Pass criteria:
- Fail criteria:
- Required evidence:
- Mode: Automated / Manual / Review-only / Blocked
- Automation level: Required / Recommended / Not recommended / Blocked
- Test execution requirement: Required / Conditional / Static fallback / Not applicable
- Priority: Blocker / High / Medium / Low
- Retest scope:
- Notes:

## Implementation Audit Standards

### IA-001: [Check Name]

- PRD trace:
- Implementation area: [code/API/data/auth/logging/tests/config]
- Review method:
- Pass criteria:
- Fail criteria:
- Required evidence:
- Test coverage requirement:
- Static fallback:
- Priority: Blocker / High / Medium / Low
- Retest scope:

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | [command] | [audit check IDs] | Required/Conditional | [output/log/report] | [static verification or blocker] |

## UI, UX, And Accessibility Standards

[Use this section when relevant. Include visible states, empty/loading/error states, responsiveness, keyboard/focus behavior, and accessibility criteria.]

## API, Data, And State Standards

[Use this section when relevant. Include API contracts, validation, persistence, lifecycle transitions, idempotency, concurrency, and data integrity checks.]

## Permissions, Security, And Privacy Standards

[Use this section when relevant. Include role checks, unauthorized access, audit logs, sensitive data handling, and privacy expectations.]

## Integration And External Dependency Standards

[Use this section when relevant. Include retries, partial failure, timeout behavior, duplicate callbacks, and reconciliation evidence.]

## Observability, Performance, And Reliability Standards

[Use this section when relevant. Include logs, metrics, traces, alerts, performance thresholds, and reliability behavior. Mark thresholds blocked when the PRD does not define them.]

## Regression And Compatibility Standards

- Existing behavior to retest:
- Backward compatibility checks:
- Migration/rollback checks:
- Release/feature-flag checks:

## Required Evidence For Future Review

- Test results:
- Screenshots or recordings:
- API traces:
- Database records:
- Logs/audit events:
- Accessibility/performance reports:
- Code references:

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

- Check statuses: Pass / Fail / Blocked / Not Run / Not Applicable
- Final conclusions: Approved / Approved with Risks / Rejected / Blocked
- `Blocked` and `Not Run` are not passes.
- `Blocker` or `High` checks that are blocked or not run prevent unconditional approval unless sufficient substitute evidence exists.

## Hard Fail Conditions

- Any `Blocker` check fails.
- Any `Blocker` check is `Blocked` or `Not Run` without substitute evidence.
- A core PRD flow has no audit coverage.
- High-risk permission, data, payment, ledger, privacy, or audit-log behavior lacks implementation audit coverage.
- Required test commands are not run and no blocker is recorded.
- High-risk clean-context review findings are ignored without rejection rationale.
- Evidence cannot be traced to audit check IDs.

## Retest And Regression Rules

- Failed check retest scope:
- Related PRD area regression:
- Changed code path test requirements:
- Blocker/High fix verification:
- Retest round reporting:

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed checks as deprecated; do not reuse IDs.
- Rerun three clean-context reviews when changes affect core flows, permissions, data, integrations, irreversible operations, or risk levels.
- For small non-behavioral wording changes, run local update plus quality gate.

## Three-Round Clean-Context Review Record

- Review mode: Subagents / Inline fallback
- Reviewer A focus: PRD coverage completeness and traceability
- Reviewer B focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations
- Reviewer C focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling
- Round 1 status:
- Round 2 status:
- Round 3 status:
- Context isolation: Confirmed / Approximated / Not available

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| [Gap or risk] | Round 1 / Round 2 / Round 3 / Multiple | Accepted/Rejected/Unresolved | [PRD-traceable reason] |

## Blocked Checks And Open Questions

| Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- |

## Assumptions

- [Assumption and why it is safe/non-blocking]

## Final Quality Gate

- Ready for post-development audit: Yes/No
- Artifact readiness status: Ready / Ready with assumptions / Blocked
- Final conclusion rule ready: Yes/No
- Hard fail conditions complete: Yes/No
- Conditions before use:
- Checks that must pass before release:

## Machine-Readable Audit Checks Appendix

```json
{
  "audit_checks": [
    {
      "id": "BV-001",
      "prd_trace": "",
      "layer": "Behavior Verification",
      "category": "",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "",
      "test_data": {
        "positive_cases": [],
        "negative_cases": [],
        "boundary_cases": [],
        "stateful_cases": [],
        "cleanup_requirements": []
      },
      "steps_or_method": "",
      "pass_criteria": "",
      "fail_criteria": "",
      "required_evidence": [],
      "test_execution_requirement": "Required",
      "retest_scope": "",
      "status": "Ready"
    }
  ]
}
```
````

## Writing Guidance

- Keep each audit check independently executable.
- Use stable IDs such as `BV-001`, `IA-001`, `TE-001`, `RG-001`, `EV-001`, and `BQ-001`; keep IDs consistent when updating a document.
- Prefer "Given/When/Then" phrasing inside scenario details when it makes behavior clearer.
- Separate release-blocking gates from lower-priority review checks.
- Avoid generic checklist lines unless they are tied to a concrete PRD behavior.
- Do not require arbitrary test coverage percentages; require evidence for high-risk PRD paths instead.
