# Troubleshooting and FAQ

Use this reference when the workflow stalls or an edge case is unclear.

## FAQ

### The input did not come from requirement-exploration. Can this skill still be used?

Yes, if the user has provided enough clarified product intent to generate a PRD and wants a review-gated PRD artifact. Treat the direct description, existing PRD update request, ticket, or docs as the source material. If it is vague, ask one focused clarification question.

### The user only asked for "生成 PRD 文件" and did not mention reviewers. Should review still happen?

Yes, when this skill triggers. Review before saving is part of this skill's workflow. Keep the conversation concise, but do not skip the frontend/backend gate.

### The user explicitly asks for a quick draft without review. Should this skill force review?

No. If the user explicitly wants a quick one-shot draft, do not force the review gate. You may offer review as a follow-up.

### The existing PRD conflicts with the new prompt. Which wins?

Use source priority from `input-and-context.md`. Usually latest user instruction and the new clarified prompt win over the old PRD. If the conflict changes product semantics and the priority is unclear, ask.

### Code and docs disagree. Which is authoritative?

Do not silently choose. Record a current-state conflict. Ask the user if the choice affects product behavior, history, permissions, money, or compliance.

### Frontend and backend reviewers disagree.

Use `review-and-iteration.md` conflict handling. Resolve only when source materials support it. Otherwise ask one focused user question or record a non-blocking open question if both reviewers can approve with it.

### Reviewers approve but the PRD still feels risky.

Do not save yet. Run a self-check using `quality-metrics.md`, consider a specialist review, or ask the narrow decision that blocks confidence.

### The PRD is for a pure backend/data/security change.

Read `template-variants.md` and adapt the structure. Still keep frontend review if there is any user-facing visibility, admin operation, permission display, or error state. If frontend truly has no surface, frontend approval can say "no frontend impact" with evidence.

### The review loop keeps going.

Use the complexity-based iteration limit. If the same blocking issue repeats, stop and ask the user for the decision instead of rewriting again.

### There is no real project code available for an existing-project iteration.

Record that limitation as a compatibility risk. Do not invent route names, component names, tables, or APIs. Reviewers can approve only if the PRD is still coherent with that limitation recorded.

## Common Fixes

- Missing reviewer notes: rerun review or add a review history entry before saving.
- Open question treated as fact: move it to assumptions/open questions and classify it.
- PRD too implementation-heavy: rewrite as product behavior and acceptance criteria.
- PRD too generic: add actors, triggers, states, failure behavior, and acceptance criteria.
- Old project context ignored: add Existing Product Context and Compatibility.
- Specialist risk ignored: add a recommendation or run the specialist review.

## Technical Failures

### Subagent Launch Fails or Times Out

Symptoms:

- subagent/delegation tool returns an error
- reviewer does not respond within a reasonable time
- agent limit prevents launching both reviewers

Resolution:

1. Retry once with the same reviewer instructions.
2. If the second attempt fails, ask the user whether to wait and retry, use inline simulated review, or pause.
3. Do not save a final PRD without review unless the user explicitly asks to bypass the review gate.
4. Record the fallback choice in review notes and the final review record.

Partial success means one reviewer succeeds and the other fails:

1. Preserve the successful reviewer result.
2. Retry the failed reviewer once.
3. If retry succeeds, proceed with both reviews.
4. If retry fails, ask whether to wait and retry, use inline simulated review for the failed reviewer, or pause.
5. Record which reviewer used subagent review and which required fallback.

### Subagent Returns Malformed Response

Symptoms:

- response does not include `approval_status`
- blocking findings and suggestions are mixed together
- response is too vague to audit
- reviewer rewrites the PRD instead of reviewing it

Resolution:

1. Ask the reviewer to reformat using the expected response format.
2. If still malformed, extract usable findings but do not treat the response as approval.
3. Retry with a shorter, stricter reviewer prompt.
4. If the response remains unusable, ask the user whether to retry or use inline simulated review.

Malformed approval is not approval.

### File Reading Fails During Existing-Project Review

Symptoms:

- reviewer cannot access project files
- relevant files are missing, huge, generated, binary, or unreadable
- search returns no matching project context

Resolution:

1. Record what was searched or attempted.
2. Continue with available docs/source context.
3. Add a compatibility risk: "Could not verify compatibility with [area/files]; manual check needed."
4. Approval is valid only with that limitation recorded.
5. Block approval only when the missing context is critical to product semantics, permissions, historical records, money, compliance, or rollout.

## Anti-Patterns to Avoid

### Assumption Inflation

Pattern: treating every uncertainty as an assumption and proceeding.

Problem: the PRD becomes a collection of guesses.

Fix: classify assumptions by risk; ask about high-risk assumptions.

### Implementation Creep

Pattern: the PRD includes detailed API contracts, database schemas, component hierarchies, or implementation plans.

Problem: product requirements get mixed with technical design.

Fix: keep the PRD product-semantic; move technical detail to a design doc unless it clarifies product behavior.

### Rubber Stamp Review

Pattern: reviewers approve without concrete findings, section references, or checklist reasoning.

Problem: review adds little value.

Fix: use the review quality check and ask for a sharper reviewer pass.

### Scope Expansion During Review

Pattern: reviewers add useful but unconfirmed "nice to have" features.

Problem: PRD grows beyond the confirmed requirement.

Fix: record suggestions as Post-MVP unless the user confirms they are in scope.

### Conflict Avoidance

Pattern: choosing one reviewer's opinion without explanation.

Problem: the PRD loses important product tradeoff context.

Fix: use the conflict resolution process and record the decision rationale.

### Premature Saving

Pattern: saving a PRD with blocking questions to "make progress."

Problem: the saved document becomes a false baseline.

Fix: enforce the save gate and ask the user for blocking decisions.
