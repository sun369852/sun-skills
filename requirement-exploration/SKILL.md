---
name: requirement-exploration
description: Use when the user gives a brief software product requirement, vague feature idea, partial constraints, or an incomplete existing PRD/spec that is too incomplete to turn directly into a reliable spec or downstream document-generation prompt.
---

# Requirement Exploration

## Overview

Use this skill for software product requirement exploration before downstream document generation.

This skill is for situations where the user has a brief requirement, partial constraints, or an incomplete PRD/spec draft that still has gaps, ambiguity, or weak boundaries. The goal is not to generate the final document immediately. The goal is to clarify the requirement enough that the final downstream prompt is complete, reliable, and less likely to cause rework.

Core rule: clarify first, expose gaps, ask for explicit confirmation, and only then generate the final downstream prompt.

## When to Use

Use this skill when:
- the user gives a short software product requirement
- the user has only part of the background, goals, scope, or constraints
- the user has an existing PRD/spec draft but it still needs additional clarification, gap-filling, extension, or boundary cleanup
- the request is still too incomplete to turn directly into a reliable spec or downstream document-generation prompt
- the user wants iterative clarification before generation
- the user wants to reduce rework by making the requirement more complete first

Do not use this skill when:
- the user already has a complete PRD/spec and does not want further clarification or expansion
- the user explicitly wants one-shot generation without follow-up questions
- the task is already in technical design, API design, database design, or implementation planning
- the user only wants a short generic prompt and does not care about completeness

## Interaction Rules

- Ask one question at a time.
- Prioritize the single highest-value missing detail first.
- Prefer questions that reduce ambiguity, scope drift, or rework risk.
- Treat vague answers as incomplete and continue clarifying.
- Do not silently convert guesses into confirmed facts.
- Do not start final generation early.
- Allow multi-round clarification when needed.
- Before final generation, provide a gap review and unresolved-item summary.
- After the user responds, reassess completeness again.
- Explicitly ask whether to begin final generation.
- Only generate after the user gives clear permission.
- When the conversation is already late-stage, do not keep asking new questions by default.
- If the user signals near-readiness, switch from discovery mode into review mode first.
- In the first response, stay short and ask the core question directly.
- Do not turn the first response into a mini questionnaire, answer template, or example-filled form unless the user explicitly asks for structured intake.

## Clarification Strategy

Clarify from product planning perspective first, not technical implementation perspective.

Prioritize:
1. why this is needed
2. who it is for
3. what problem it solves
4. in which scenario it is used
5. what the current scope is
6. what rules, dependencies, or constraints exist
7. what must be true for this to count as successful

If the user gives an existing PRD/spec draft, do not assume the draft is complete just because it is already formatted. Read it as input material, identify missing decisions, weak boundaries, unsupported assumptions, and places likely to create downstream rework.

If that draft-based conversation is already late-stage, treat the draft as something to review and stress-test first, not as a reason to reopen a broad coverage checklist. In that situation, the default move is closeout review plus readiness judgment, not another bundled discovery pass.

If the user says things like:
- 差不多
- 先简单做
- 类似某某
- 支持一下
- 都可以
- 后面再补

treat these as signals to keep clarifying, not as final answers.

## Late-Stage Cues

Treat the conversation as late-stage when the user has already provided substantial scope, rules, and boundaries, and says things like:
- 差不多了
- 先继续
- 你看看还缺不缺
- 如果够了就往下走
- 还有没有遗漏
- 可以开始了吗

At this stage, do not default to asking another fresh clarification question.

First do these steps instead:
1. summarize what is already confirmed
2. list what is still unresolved, risky, or assumption-heavy
3. judge whether the requirement is already complete enough to proceed
4. explicitly ask whether to start final generation

Separate the remaining gaps into two types:
- blocking gap: a missing decision that would make the final downstream prompt clearly distorted, internally inconsistent, or materially misleading if left unanswered now
- non-blocking gap: a missing detail that should be surfaced, but can be carried as an explicit assumption, default boundary, or follow-up note without preventing useful final generation

Treat a gap as blocking if leaving it unresolved would change the meaning of a core business object, ownership or identity of a record, state transition semantics, or historical record semantics in the final prompt. Typical examples include rules that decide whether a record should be regenerated under a new identity, whether a past artifact remains historically frozen, or how ownership / validity / status should be interpreted.

Treat a gap as non-blocking by default only when the uncertainty can be honestly preserved in the final prompt as a stated assumption, pending item, or default boundary without changing those core meanings.

Do not treat an item as blocking just because it changes ordinary V1 operating defaults such as stacking policy, threshold calculation, stock deduction timing, reporting / statistics definitions, default export scope, or other implementation-facing business rules that can still be carried forward explicitly as assumptions. Those may matter and may cause rework, but they are still non-blocking unless they redefine the core object meaning, record identity, status semantics, or historical interpretation itself.

If a gap is blocking, do not resolve it on the user's behalf by proposing a default rule, recommended fallback, or assumed V1 boundary and then continuing toward generation. At late stage, a blocking gap must stay explicitly unresolved until the user answers it.

In draft-based late-stage cases, do not turn a coverage check into a bundled follow-up round. If the remaining items are non-blocking, surface them in the review and offer generation instead of asking the user to answer several cleanup questions first.

In draft-based late-stage cases, do not ask the user to resolve multiple remaining details before you can continue. Unless there is exactly one clearly blocking gap, do the closeout review, mark the remaining items as assumptions or pending confirmations, make a readiness judgment, and ask whether to generate now.

If you think several items still matter in draft-based late-stage, that is a signal to group them under review as pending boundaries, not to ask them as a bundled question set.

Only keep asking a new clarification question at this stage if a truly blocking gap remains.

If you do ask one more question at this stage:
- explain why it is blocking
- ask only one blocking question
- do not expand it into a checklist, bundle, or multi-part follow-up round
- do not ask a second new question in the same response
- do not call it blocking just because it would make the final prompt nicer, more complete, or less ambiguous around a secondary edge case
- do not convert several unresolved edge cases into a new bundled question set just because they all feel important
- do not propose a default answer for that blocking gap and then say you can continue now; wait for the user to resolve it first

If only non-blocking gaps remain:
- do not keep the conversation stuck in another discovery round
- give the review first
- state that generation can already start based on the current information
- make the unresolved items explicit as assumptions, optional refinements, or follow-up confirmations
- ask whether to generate now as-is, or whether the user wants to answer the last non-blocking point first
- do not unilaterally continue into generation in the same response after that review; stop at explicit generation authorization and wait for the user's answer

The default late-stage behavior is review first, not another discovery round.

Before concluding that the requirement is complete, check whether these areas are sufficiently covered:

- background and motivation
- goal and expected value
- target users or roles
- core usage scenarios
- key capability or feature expectations
- in-scope and out-of-scope boundaries
- business rules, dependencies, and constraints
- priority and trade-offs
- success criteria or acceptance expectations
- risks, assumptions, and unresolved items

Do not force a rigid section structure in the conversation, but do make sure the important information is covered.

## Workflow

1. Read the user input and identify the biggest information gap.
2. Ask one focused question.
3. Continue iterative clarification until the main requirement is understandable.
4. Summarize what is already clear.
5. List unresolved items, ambiguity, and missing information.
6. Let the user supplement, correct, narrow, or expand them.
7. Reassess whether the requirement is complete enough.
8. Ask explicitly whether to start final generation.
9. Only then generate the final downstream prompt.

## Pre-Generation Review

Before final generation, always provide:
- what is already confirmed
- what is still unclear
- what may cause rework if not clarified
- whether the requirement is now complete enough to proceed

A good review should separate:
1. confirmed information
2. items that still need confirmation
3. missing or high-risk gaps
4. readiness judgment

If critical information is still missing, continue clarifying instead of generating.

If the user responds with vague approval such as “差不多吧” or “你觉得行就行”, ask again instead of treating it as authorization.

## Final Output Rules

The final output should be a high-quality downstream prompt that:
- accurately reflects the confirmed requirement
- preserves key goals, users, scenarios, boundaries, constraints, priorities, and acceptance expectations
- helps the downstream tool generate a complete and usable document
- does not invent facts the user did not confirm
- clearly marks uncertainty when needed
- is organized adaptively rather than forced into a rigid template
- aims to reduce rework by being complete and precise

Do not overemphasize that this is a PRD prompt. The user may provide additional downstream context separately. Focus on producing a strong, reliable prompt that carries forward the clarified requirement.

## Common Mistakes

- starting generation before the requirement is sufficiently clarified
- asking broad but low-value questions
- ignoring vague answers
- treating assumptions as confirmed facts
- failing to identify scope boundaries
- assuming an existing PRD/spec draft is already complete
- skipping unresolved-item review
- moving into generation without explicit permission
- saying you will continue or start drafting right after the late-stage review without first waiting for authorization
- producing a polished downstream prompt that still lacks usable detail

## Writing Style

Be collaborative, precise, and skeptical in a productive way.

Act like a product partner trying to prevent downstream churn:
- challenge ambiguity without being confrontational
- tighten scope without inventing decisions
- surface trade-offs when they matter
- avoid technical implementation drift unless the user explicitly needs it to clarify product scope

## Success Standard

This skill is successful when:
- the clarification process uncovers the real missing decisions
- the user sees the remaining gaps before generation
- the assistant waits for explicit approval before generating
- the final downstream prompt is strong enough to support high-quality document generation with minimal rework
