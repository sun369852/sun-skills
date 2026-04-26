# Clean-Context Review

Use this reference before using three clean-context reviewers or inline fallback review passes.

## Review Packet

Each reviewer receives the same independent packet:

- original PRD content or path
- source-priority note and supporting context summary
- bounded project-context summary, if any
- current admitted draft audit standards
- explicit instruction that no other reviewer findings are available or should be inferred

Do not include previous reviewer outputs, merged findings, or mediation notes in any review prompt.

## Reviewer Focuses

Use three independent focuses:

- Reviewer A: PRD coverage completeness and traceability.
- Reviewer B: risk gates, permissions, data integrity, abnormal flows, security/privacy, irreversible operations, and integration failure behavior.
- Reviewer C: executability, required test commands, evidence quality, machine-readable structure, automation feasibility, blocked/not-run handling, and defect report usefulness.

The source packet stays the same for all reviewers. Only the review focus changes.

## Subagent Rules

When subagents are available and the user request authorizes subagents/reviewers/clean-context review:

- start three independent reviewer runs where practical
- use `agents/quality-audit-reviewer.md`
- include the reviewer focus in each prompt
- ask for concise findings, not a competing final document
- require PRD trace for gaps and recommendations
- ask reviewers to mark ambiguous or untestable requirements as blocked

If subagents are unavailable, perform three separated inline review passes named:

- `Clean review round 1`
- `Clean review round 2`
- `Clean review round 3`

Use only the source packet and admitted draft for each inline pass. Disclose that context isolation is approximated.

## Isolation Requirements

- no reviewer sees another reviewer's findings
- no reviewer sees merged synthesis or previous-round critique
- reviewers are not told what earlier reviewers focused on or found
- the main agent merges findings only after all three reviews complete
- if the environment cannot guarantee clean context, disclose the limitation
