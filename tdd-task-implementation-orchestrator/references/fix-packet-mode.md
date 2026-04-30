# Fix Packet Mode

Use this reference when the input includes a `Developer Fix Packet` from `implementation-review-handoff` or a review-fix loop asks for bounded repairs.

## Boundary

Fix only the findings listed in the packet. Do not expand product behavior, revise PRD intent, change technical design decisions, rewrite the task plan, or perform risky operations unless the packet and user authorization explicitly allow it.

Stop and report blocked if a fix requires:

- PRD or product behavior changes
- technical design replacement
- audit standard changes
- scope expansion outside the listed findings
- credentials, destructive operations, migration risk, push, or pull request creation

## Workflow

1. Read the source artifacts, previous review report, findings, expected evidence, and constraints from the packet.
2. Map each finding to the smallest implementation area and verification command.
3. Repair only the listed findings.
4. Run the required tests or record why they cannot run.
5. Update task list and run log only when they are part of the existing implementation artifacts.
6. Return the fixed-format `Developer Fix Return` below.

## Developer Fix Return

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

If no findings were fixed, still return the same structure and mark `Ready for re-review: no` with blockers.
