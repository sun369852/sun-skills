---
name: requirement-exploration
description: "Use for requirement clarification before spec/PRD/prompt generation: brief or vague product requirements, incomplete PRD/spec drafts, in-progress requirement discussions, existing-product requirement iteration, and late-stage closeout review before generation. Do not use for technical design, codebase exploration, pure rewriting, or explicit one-shot generation requests."
---

# Requirement Exploration

## Overview

Use this skill before downstream spec or prompt generation when the requirement is still incomplete, ambiguous, assumption-heavy, or weakly bounded.

This includes both:
- new-project / new-feature exploration
- requirement iteration on an existing product, workflow, or codebase

The goal is not to generate immediately. The goal is to clarify enough that the downstream prompt is reliable, complete, and less likely to cause rework.

Core rule: clarify first, expose gaps, ask for explicit confirmation, and only then generate the final downstream prompt.

## When to Use

Use this skill when:
- the user gives a short software product requirement
- the user has only part of the background, goals, scope, or constraints
- the user has an existing PRD/spec draft that still needs clarification, extension, or boundary cleanup
- the user is iterating on an existing product, system, workflow, or codebase and the new requirement may interact with current behavior or logic
- the conversation is already near the end and needs a closeout review before final generation
- the request is too incomplete to turn directly into a reliable spec or downstream prompt

Do not use this skill when:
- the user already has a complete spec and does not want further clarification
- the user explicitly wants one-shot generation without follow-up questions
- the task is already in technical design or implementation planning

## Routing Rules

Read only the reference file that matches the situation.

- If this is a new project or greenfield feature with little existing-context pressure, read `references/new-project.md`.
- If this is an iteration on an existing product, feature, workflow, or codebase, read `references/existing-project-iteration.md`.
- If the conversation is already late-stage, or the user says things like “差不多了”, “你看看还缺不缺”, “如果够了就往下走”, “可以开始了吗”, also read `references/late-stage-review.md`.

If more than one situation applies, prefer this order:
1. `references/late-stage-review.md`
2. `references/existing-project-iteration.md`
3. `references/new-project.md`

Do not read all references by default. Load only what is needed.

## Universal Interaction Rules

- Ask one question at a time.
- Prioritize the highest-value missing detail.
- Prefer questions that reduce ambiguity, scope drift, compatibility risk, or rework risk.
- Treat vague answers as incomplete.
- Do not silently convert guesses into confirmed facts.
- Do not start final generation early.
- Before final generation, provide a review of what is confirmed, what is unresolved, and whether the requirement is complete enough to proceed.
- Explicitly ask whether to begin final generation.
- Only generate after the user gives clear permission.
- If the user gives vague approval such as “差不多吧” or “你觉得行就行”, ask again instead of treating it as authorization.
- In the first response, stay short and ask the core question directly.
- Do not turn the first response into a broad questionnaire unless the user explicitly asks for structured intake.

## Output Expectations

Before generation, the review should make visible:
- confirmed information
- unresolved items
- high-risk gaps or assumptions
- readiness judgment

If this is an existing-project iteration, also keep visible:
- compatibility expectations
- affected areas / impact scope
- relevant dependencies and touchpoints
- known or suspected conflict points with current logic or behavior

## Final Output Rules

The final downstream prompt should:
- accurately reflect confirmed information
- preserve goals, users, scenarios, boundaries, constraints, priorities, and acceptance expectations
- avoid inventing facts
- clearly mark uncertainty when needed
- carry forward compatibility, impact, dependency, and conflict context when relevant
- reduce downstream rework by being precise and decision-aware

## Common Mistakes

- generating too early
- asking broad but low-value questions
- treating assumptions as facts
- restarting discovery from scratch when the conversation is already late-stage
- treating an existing-project iteration as isolated from current behavior or logic
- failing to surface compatibility, impact, dependency, or conflict risks before generation
- moving into generation without explicit permission
