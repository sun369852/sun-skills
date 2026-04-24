# Core Workflow

Use this workflow for every prompt-to-PRD task.

## 1. Read and Preserve the Source

Read the source prompt and materials completely before drafting. Extract a compact source map:

- confirmed facts
- explicit assumptions
- unresolved or pending items
- out-of-scope boundaries
- high-risk rules that must not be silently changed
- latest user instructions that override earlier materials

Do not treat assumptions as confirmed facts. Do not add attractive product ideas just because they are common in the domain.

## 2. Decide Whether Drafting Is Safe

Proceed when the materials cover enough of:

- background and goal
- users or roles
- core scenarios
- feature scope and boundaries
- functional requirements
- business rules and state semantics
- dependencies or constraints
- acceptance expectations
- known risks, assumptions, and unresolved items

Ask one blocking clarification question only if leaving the missing item unresolved would distort core object meaning, ownership, state transition, permission semantics, historical record semantics, compatibility expectation, or primary success criteria.

If the missing item is non-blocking, carry it into the PRD as an assumption, open question, or follow-up item.

If a blocking question prevents safe drafting or saving, do not produce a final PRD. Instead produce a short blocking decision brief that includes:

- confirmed facts that are safe to preserve
- the blocking question
- why it changes product semantics
- frontend/backend impact
- a suggested default only if the source materials support one

This keeps progress visible without turning an unresolved decision into a false product baseline.

## 3. Draft, Self-Review, Then Invite Reviewers

Draft the PRD using `references/prd-content.md`.

Before inviting reviewers, self-review and patch obvious gaps:

- each major feature has an actor, trigger, expected result, and relevant failure behavior
- scope and non-goals are explicit
- business rules are not hidden inside vague prose
- unresolved items are labeled
- acceptance criteria are testable from a product perspective
- existing-project compatibility expectations are visible when applicable

The PRD is review-ready when a reviewer can answer: "Is this coherent enough to save as the current product baseline if the recorded assumptions and open questions are accepted?"

## 4. Review and Iterate

Use `references/review-and-iteration.md`.

Bring in frontend and backend reviewers in parallel when possible. If subagents are unavailable, perform simulated role reviews inline and say so clearly.

Update the PRD based on review feedback. Rerun review after material changes until both perspectives approve or a user decision is needed.

## 5. Save After Approval

Use `references/finalize-and-record.md`.

Only write the PRD file after both frontend and backend reviewers approve the current draft. The saved file is the durable artifact; the conversation response should stay concise.
