# Backtrack Policy

Use this reference to decide how the chain handles defects that trace to upstream artifacts—PRD, technical design, audit standards, or task decomposition. The backtrack policy determines whether the chain can automatically return to an earlier stage to fix the root cause, or whether it must stop and wait for a human.

The default review-fix loop covers implementation-scoped defects (review → fix packet → TDD → re-review). Backtrack extends this to upstream artifacts without requiring a fresh chain restart.

## Backtrack Modes

Configure in `delivery/_chain-defaults.md` via the startup contract:

| Mode | Behavior | When to use |
| --- | --- | --- |
| `bounded-bug` (default) | Implementation defects auto-loop through review-fix. Upstream defects stop and ask. | Semi-auto or conservative full-auto. Safe default. |
| `controlled-upstream` | Implementation + bounded upstream defects auto-trigger return to the affected stage. Max 2 levels. | Full-auto with trusted artifacts and bounded scope. |
| `stop-and-ask` | All defects, including implementation, require human confirmation before loop continuation. | Ask-each-stage or high-risk work. |

## Controlled Upstream: Allowed Triggers

Only the following defect types may trigger an automatic backtrack:

| Trigger | Backtrack target | Backtrack scope |
| --- | --- | --- |
| PRD requirement missing or ambiguous discovered during review | `prompt-to-prd-review` | The ambiguous section only. Do not restart the entire PRD. |
| Technical design conflicts with implementation reality | `prd-to-tech-design-review` | The conflicting area only. Do not reopen settled decisions. |
| Audit standards reference behavior not in PRD | `prd-quality-audit-standards` | Update the specific audit check. Do not regenerate all standards. |
| Task boundaries are wrong due to missing design info | `prd-task-archiver` | The affected task group. Do not replay all tasks. |
| Multiple root causes at different levels | Stop. Record each cause. Do not auto-backtrack. |

## Backtrack Depth Limit

- **1-level backtrack**: Return to the immediate upstream skill. E.g., review → backtrack to TDD (already handled by review-fix), or review → backtrack to task-archiver.
- **2-level backtrack**: Skip one intermediate stage. E.g., review discovers a PRD gap → backtrack directly to `prompt-to-prd-review`, bypassing task-archiver and tech-design.
- **3+ level backtrack**: Not allowed. Stop and record in chain status as `BLOCKED_BACKTRACK_LIMIT`.

After a 1-level or 2-level backtrack completes, the chain must re-run all downstream stages between the backtrack target and the current stage. The chain records these re-runs in `delivery-chain-status.md`.

## Backtrack Flow

When a downstream skill (typically `implementation-review-handoff`) determines that a defect cannot be fixed at the current level:

```text
1. Downstream skill judges: "This defect traces to upstream artifact X."
2. Instead of producing a standard fix packet, produce an upstream backtrack packet.
3. Return to product-delivery-skill-chain (the routing layer) with the packet.
4. Chain evaluates the backtrack: is it within allowed scope + depth?
5. If yes: chain updates delivery-chain-status.md, routes to the backtrack target.
6. If no: chain records BLOCKED_BACKTRACK_LIMIT, stops, reports in chain status.
7. After backtrack target completes: chain reruns all intermediate downstream stages.
8. After rerun completes: chain returns to the original stage for final review.
```

## Chain Status Recording

After each backtrack event, update `delivery-chain-status.md`:

```markdown
## Backtrack Events

| Event | Trigger | Target | Depth | Result | Affected Artifacts |
| --- | --- | --- | --- | --- | --- |
| 1 | Review: design conflict | prd-to-tech-design-review | 1 | Fixed | technical-design.md, tasks.md |
```

## Full-Auto Integration

In full-auto mode with `controlled-upstream` policy:

- The chain automatically evaluates each backtrack trigger against the allowed list.
- The chain does not ask before executing a 1-level or 2-level backtrack.
- The chain stops only when backtrack depth exceeds 2, or when a defect does not match any allowed trigger.
- All backtrack events are recorded in chain status for post-run inspection.
