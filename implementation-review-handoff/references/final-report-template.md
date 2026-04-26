# Final Report Template

Use this structure unless the user requested a different format. Keep the same structure even when there are no findings; only simplify the `Findings` section.

```markdown
## Findings

- [P1] Short finding title
  Audit check: BV-001 / IA-001 / TE-001 / none
  File: path/to/file.ext:123
  Evidence: what proves the issue
  Impact: why it matters
  Recommendation: the smallest useful fix

If there are no findings:

No blocking findings.

## Decision

Pass / Pass with notes / Fix needed / Blocked

- Audit mode: Standards / Basic
- Standards conclusion: Approved / Approved with Risks / Rejected / Blocked / N/A
- Basic mode note: if no standards artifact was used, say whether generating `quality-audit-standards.md` is recommended before final release.

## Audit Check Summary

Include this section when a quality audit standards artifact exists:

| Check ID | Priority | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| BV-001 | Blocker/High/Medium/Low | Pass/Fail/Blocked/Not Run/N/A/Out of Scope | command, file, log, screenshot, or defect ID | short note |

## Standards Sync And Review Record

Include this section when an audit standards artifact exists:

- PRD/standards sync: current / warning / blocked
- Sync evidence: version, timestamp, source path, hash, or weak mtime comparison
- Three-round review record: present / absent / not checked
- High-risk review findings affecting this implementation:

## Scope Reviewed

- Source of truth: ...
- Audit standards: path or not provided
- Change scope: ...
- Excluded changes: unrelated files or none
- Assumptions: ...

## Verification

- `command`: passed/failed/skipped/not run. Related check IDs: ... Short evidence.

## Coverage Notes

- Requirement/task coverage: ...
- Audit check coverage: ...
- Partial/out-of-scope work: ...
- Not reviewed: ...
- Residual risk: ...

## Developer Handoff

Include this section when the decision is `Fix needed` or implementation defects should enter the development-review loop.

- Suggested receiving skill: `tdd-task-implementation-orchestrator`
- Fix scope:
- Required changes:
- Files likely involved:
- Evidence:
- Retest scope:
- Acceptance checks to satisfy:
- Do not change:

## Re-Review Requirements

- Previous decision:
- Findings to verify:
- Required evidence from developer:
- Commands to rerun:
- Checks that must move from Fail/Blocked/Not Run to Pass:
- Regression areas:

## Developer Fix Packet

Include or link to the repair packet from `references/review-fix-loop.md` when auto-routing or handing off to development. Do not duplicate the full packet if it is saved elsewhere.

## Upstream Issues

- Category: Standards gap / Requirement-design conflict / Product decision needed / none
- Artifact:
- Issue:
- Impact:

## Upstream Return Recommendation

- Return needed: yes/no
- Target upstream artifact:
- Suggested receiving skill:
- Reason:
- Impact if not returned:

## User Decision Needed

Include this section when upstream artifacts, product decisions, risk acceptance, scope expansion, or conflicting standards block the next step.

- Decision:
- Options:
  - Return upstream for rework:
  - Accept risk and continue:
  - Narrow current review scope:
- Recommended option:
- Reason:

## Review Loop History

| Round | Review Decision | Developer Handoff | Developer Return | Re-Review Result | Stop Reason |
| --- | --- | --- | --- | --- | --- |

## Saved Report

- Path: saved path or not saved

## Machine-Readable Summary

Optional. Include this when another agent, script, or review-fix loop will consume the result.

```json
{
  "review_id": "",
  "audit_mode": "Standards",
  "decision": "Fix needed",
  "standards_conclusion": "Rejected",
  "findings": [
    {
      "id": "F-001",
      "severity": "P1",
      "audit_check_id": "BV-001",
      "category": "Implementation defect",
      "file": "path:line",
      "evidence": "",
      "recommendation": "",
      "retest_scope": ""
    }
  ]
}
```
```
