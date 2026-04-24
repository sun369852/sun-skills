# Audit Standards Template

Use this structure for the saved Markdown artifact. Adapt section names when the project has a strong existing convention, but preserve the same information.

```markdown
# [Feature Name] Quality Audit Standards

## Source And Scope

- Source PRD: [path or pasted content summary]
- Supporting context: [technical design/task archive/project files, or "none"]
- Audit purpose: standards for post-development verification
- In scope:
- Out of scope:

## Readiness Summary

- Status: Ready / Ready with assumptions / Blocked
- Requirements mapped: [count]
- Blocked or ambiguous requirements: [count]
- Release-blocking gates: [count]

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Type | Mode | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| QA-001 | [PRD item] | [Pass/fail standard] | Functional | Automated/Manual/Review-only | [Required evidence] | Ready/Blocked |

## Functional Acceptance Standards

### QA-001: [Check Name]

- PRD trace:
- Scenario/setup:
- Steps or review method:
- Pass criteria:
- Fail criteria:
- Required evidence:
- Mode:
- Priority: Release-blocking / High / Medium / Low
- Notes:

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

## Blocked Checks And Open Questions

| Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- |

## Assumptions

- [Assumption and why it is safe/non-blocking]

## Final Quality Gate

- Ready for post-development audit: Yes/No
- Conditions before use:
- Checks that must pass before release:
```

## Writing Guidance

- Keep each audit check independently executable.
- Use stable IDs such as `QA-001`, `QA-002`, and keep IDs consistent when updating a document.
- Prefer "Given/When/Then" phrasing inside scenario details when it makes behavior clearer.
- Separate release-blocking gates from lower-priority review checks.
- Avoid generic checklist lines unless they are tied to a concrete PRD behavior.
