# Upstream Backtrack Packet

Use this reference when `implementation-review-handoff` determines that a defect roots in an upstream artifact (PRD, technical design, audit standards, or task archive) rather than in the implementation code.

A backtrack packet replaces the standard Developer Fix Packet when the fix cannot stay inside implementation scope. It tells the routing chain to re-enter an earlier skill, fix the root cause, then re-run the affected downstream stages.

## When to Create a Backtrack Packet

Create a backtrack packet instead of a Developer Fix Packet when:

| Condition | Packet type |
| --- | --- |
| Defect is in implementation code only | Developer Fix Packet → review-fix loop |
| Defect traces to task boundary, sequencing, or missing task | Backtrack packet → re-enter `prd-task-archiver` |
| Defect traces to technical design (wrong API, missing migration, incorrect data model) | Backtrack packet → re-enter `prd-to-tech-design-review` |
| Defect traces to audit standards (wrong check, missing coverage) | Backtrack packet → re-enter `prd-quality-audit-standards` |
| Defect traces to PRD (missing requirement, wrong behavior, ambiguous rule) | Backtrack packet → re-enter `prompt-to-prd-review` |
| Multiple root causes at different levels | Do not auto-backtrack. Record all causes and stop. |

## Packet Format

```markdown
## Upstream Backtrack Packet

- Review report path:
- Review decision:
- Review loop round:

### Root Cause
- Defect summary:
- Root cause stage: (prd / technical-design / audit-standards / task-archive)
- Root cause artifact:
- Root cause evidence:
  - Defect ID or finding ID:
  - Expected:
  - Actual:
  - Evidence (command output, file excerpt, test result):

### Suggested Fix Scope
- Artifacts to fix:
- Fix boundary — what to change:
- Fix boundary — what NOT to change:
- Downstream artifacts requiring re-run after fix:
- Verification expectation after fix:

### Constraints
- Do not restart upstream stage from scratch:
- Preserve all other upstream artifact sections:
- Do not change product behavior decided in confirmed PRD sections:
```

## Routing After Backtrack

1. `implementation-review-handoff` produces the backtrack packet.
2. Returns control to `product-delivery-skill-chain` (or directly states the backtrack request if the chain is not active).
3. The chain evaluates backtrack scope and depth against `backtrack-policy.md`.
4. If allowed: the chain routes to the backtrack target with a bounded fix brief derived from the packet.
5. After fix: the chain re-runs each affected downstream stage sequentially.
6. After re-runs: the chain routes back to `implementation-review-handoff` for final re-review.

## Integration with Review Fix Loop

When an upstream defect is found during a review-fix loop:

- Do not increment the review-fix loop counter (the loop counter tracks implementation re-reviews, not upstream corrections).
- Record the backtrack as a separate event in the Review Loop History.
- After backtrack completes, re-review starts at round 0 for the re-generated artifacts.
