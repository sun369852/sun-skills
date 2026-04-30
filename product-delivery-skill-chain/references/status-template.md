# Status Template

Use this template only when creating a new `delivery-chain-status.md` or replacing a missing/corrupt status body.

```markdown
# Delivery Chain Status

## Current State
- Chain mode:
- Chain artifact directory:
- Chain start contract:
- Entry stage:
- Current stage:
- Target / stop point:
- Next skill:
- Human confirmation required:
- Review-fix loop: 0/5
- Overall status:
- Context source of truth:

## Entry Preconditions
- Requested entry stage:
- Requested target / stop point:
- Source artifact:
- Source artifact status:
- Skipped upstream stages:
- Reason skipped:
- Entry assumptions:
- Entry blockers:

## Artifacts
- Chain start contract:
- Source manifest:
- Source context:
- PRD:
- Technical design:
- Task archive:
- Audit standards:
- Implementation run log:
- Review report:

## Source Archive
- Original PRD:
- Copied PRD:
- Original technical design:
- Copied technical design:
- Original task archive:
- Copied task archive:
- Original audit standards:
- Copied audit standards:

## Runtime Surface Status

| Surface | Required | Path | Status | Start Command | Smoke Check | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | yes/no | TBD | missing/not started/running/failed/blocked | TBD | TBD | TBD |

## Stage Gates

### Chain Startup Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### Requirement Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### PRD Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### Technical Design Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### Audit Standards Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### Task Archive Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### Implementation Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

### Review Gate
- Status:
- Input:
- Output:
- Decision:
- Human confirmation:
- Notes:

## Chain Contract
- Project defaults:
- Request contract:
- Contract confirmed:
- Execution mode:
- Subagent policy:
- Parallel planning:
- Implementation confirmation:
- Review-fix loop:
- High-risk operations:
- Context policy:

## Git Handoff
- Commit policy:
- Commit authorization:
- Commit strategy owner: tdd-task-implementation-orchestrator
- Created commits:
- Push authorization:
- Pull request authorization:
- Git blockers:

## Decisions

## Blockers

## Context Summary
- Current stage:
- Trusted artifact paths:
- Key decisions:
- Open blockers:
- Next action:
- Context to discard:

## Change Log
```
