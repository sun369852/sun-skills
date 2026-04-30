# Status File

Use `delivery-chain-status.md` whenever `product-delivery-skill-chain` is invoked, including partial-chain, resume, flexible, and mid-chain entry. Do not create this file when a downstream skill is invoked directly without this chain skill.

## Location

Choose the path conservatively:

1. Use the user's explicit status file path.
2. If resuming from an existing `delivery-chain-status.md` that matches the feature, keep using that path.
3. Otherwise save `delivery-chain-status.md` inside the chain artifact directory selected by `references/artifact-directory.md`.
4. If the chain artifact directory cannot be selected safely, ask one focused question before creating the status file.

Never silently overwrite an unrelated status file. If an existing `delivery-chain-status.md` appears to describe another feature, create `delivery-chain-status-<feature-slug>.md` or ask the user.

## Update Rule

Keep the main body current. Do not append full snapshots. Preserve concise history in `Change Log`.

Update the status file after:

- chain entry or resume
- every artifact gate decision
- every saved downstream artifact
- every blocker or user decision
- chain start contract confirmation or override
- implementation handoff
- each review-fix loop
- final pass, blocked, or stopped decision

## Template Loading

Read `references/status-template.md` only when creating a new `delivery-chain-status.md` or replacing a missing/corrupt status body. For normal status updates, resume, or interpretation, use this file only and update the existing sections in place.

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
- `confirmed`

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
