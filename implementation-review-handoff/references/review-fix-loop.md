# Review Fix Loop

Use this reference when implementation review finds defects, when a developer return is available for re-review, or when the user expects the default development-review loop.

## Default Loop

Implementation review forms a default loop with the development skill:

```text
development complete
-> implementation-review-handoff
-> developer fix packet
-> tdd-task-implementation-orchestrator or equivalent development skill
-> developer fix return
-> implementation-review-handoff re-review
```

The loop does not require the user to separately say "continue fixing" for implementation-scoped defects. The default maximum is 5 review-fix rounds.

## Auto-Route Boundary

Auto-route to the development skill when all are true:

- the problem is an implementation defect or implementation-scoped verification gap
- the fix stays inside the current implementation scope
- no PRD, technical design, audit standard, or third-party standard change is required
- no product decision, risk acceptance, credential, destructive operation, or scope expansion is required
- the active environment can delegate or otherwise hand off to the development skill

If delegation is unavailable, save or output the developer fix packet and stop with `Fix needed`.

Do not auto-route upstream problems. Ask the user when PRD, technical design, `quality-audit-standards.md`, third-party standards, product decisions, risk acceptance, or scope expansion are involved.

When routing to `tdd-task-implementation-orchestrator`, tell it to use `fix-packet-mode.md` and to return the `Developer Fix Return` format below. Do not rely on its normal implementation final report for re-review.

## Developer Fix Packet

Give the development skill a bounded repair packet, not a long undifferentiated review transcript:

```markdown
## Developer Fix Packet

- Source artifacts:
  - PRD:
  - Technical design:
  - Quality/third-party standards:
  - Task list:
  - Previous review report:
- Fix scope:
- Findings to fix:
  - Finding ID:
  - Category:
  - Severity:
  - Audit check / task / PRD trace:
  - Expected:
  - Actual:
  - Evidence:
- Files likely involved:
- Constraints:
  - Do not change:
  - Do not modify upstream artifacts:
  - Stay within implementation scope:
- Required tests/evidence after fix:
- Retest scope:
- Return format:
```

## Developer Fix Return

Ask the development skill to return:

```markdown
## Developer Fix Return

- Fix round:
- Fixed findings:
  - Finding ID:
  - What changed:
  - Files changed:
  - Evidence:
- Tests run:
  - Command:
  - Result:
  - Related finding/check:
- Not fixed:
  - Finding ID:
  - Reason:
  - Blocker:
- Scope changes:
  - Added files:
  - Unexpected changes:
  - Requires upstream decision: yes/no
- Ready for re-review: yes/no
```

## Re-Review

During re-review:

- start from the previous review report and developer fix return
- verify fixed findings and their required evidence first
- inspect related regression areas and unexpected scope changes
- rerun relevant failed or risk-covering checks
- expand review only if the fix changed new contracts, files, or risk surfaces

Do not restart a full audit from scratch unless the user requests it or the repair materially expands scope.

## Stop Conditions

Stop the loop when:

- the overall decision is `Pass`
- the decision is `Pass with notes` and notes are non-blocking
- upstream artifact changes or product decisions are needed
- scope expansion is needed
- dangerous operations, credentials, or user authorization are needed
- 5 review-fix rounds have been reached
- the development skill says the issue cannot be fixed in scope
- the verification environment cannot complete core checks

After 5 rounds, keep `Fix needed` if implementation defects remain. Use `Blocked` if the remaining issue is uncertainty, environment, or missing decision.

## Loop History

When saving a report, maintain one `Review Loop History` section rather than many scattered files:

```markdown
## Review Loop History

| Round | Review Decision | Developer Handoff | Developer Return | Re-Review Result | Stop Reason |
| --- | --- | --- | --- | --- | --- |
```
