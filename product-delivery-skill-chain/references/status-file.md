# Status File

Use `delivery-chain-status.md` whenever `product-delivery-skill-chain` is invoked, including partial-chain, resume, flexible, and mid-chain entry. Do not create this file when a downstream skill is invoked directly without this chain skill.

## Location

Choose the path conservatively:

1. Use the user's explicit status file path.
2. If resuming from an existing `delivery-chain-status.md` that matches the feature, keep using that path.
3. If a PRD path exists, save beside the PRD.
4. If starting from technical design, task archive, audit standards, run log, or review report without a PRD path, save in the common parent directory when clear.
5. If there is no clear artifact directory, save in the current workspace.
6. For a new requirement from scratch, create the status file in the current workspace if the PRD output directory is not known yet. Keep using that path unless the user asks to move it.

Never silently overwrite an unrelated status file. If an existing `delivery-chain-status.md` appears to describe another feature, create `delivery-chain-status-<feature-slug>.md` or ask the user.

## Update Rule

Keep the main body current. Do not append full snapshots. Preserve concise history in `Change Log`.

Update the status file after:

- chain entry or resume
- every artifact gate decision
- every saved downstream artifact
- every blocker or user decision
- implementation handoff
- each review-fix loop
- final pass, blocked, or stopped decision

## Template

```markdown
# Delivery Chain Status

## Current State
- Chain mode:
- Entry stage:
- Current stage:
- Target / stop point:
- Next skill:
- Human confirmation required:
- Review-fix loop: 0/5
- Overall status:

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
- PRD:
- Technical design:
- Task archive:
- Audit standards:
- Implementation run log:
- Review report:

## Stage Gates

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

## Decisions

## Blockers

## Change Log
```

## Status Values

Use simple stable values:

- `not_started`
- `in_progress`
- `approved`
- `needs_changes`
- `blocked`
- `skipped`
- `draft`
- `reconciled`
- `pass`
- `pass_with_notes`
- `fix_needed`

## Preconditions

The file must make the entry point explicit. If the chain starts from the middle, record why upstream stages were skipped and whether the source artifact was confirmed by the user or inferred by the LLM.

Example:

```markdown
## Entry Preconditions
- Requested entry stage: PRD
- Source artifact: docs/checkout-prd.md
- Source artifact status: confirmed by user
- Skipped upstream stages: requirement exploration
- Reason skipped: user explicitly requested starting from existing PRD
- Entry assumptions: PRD open questions are non-blocking for technical design
- Entry blockers: none
```
