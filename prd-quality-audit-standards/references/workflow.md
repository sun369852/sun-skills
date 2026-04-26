# Workflow

Use this reference before drafting, applying the draft admission gate, running review, or merging findings.

## Drafting Sequence

1. Locate and read the PRD.
2. Extract the verification surface using `references/prd-coverage-analysis.md`.
3. Inspect bounded project context when available using `references/context-and-output.md`.
4. Build an initial traceability matrix mapping each PRD requirement to one or more audit checks.
5. Draft the initial standards using `references/audit-standards-template.md`.
6. Apply audit check rules from `references/audit-check-rules.md`.
7. Mark blocked checks where the PRD is ambiguous or the environment is unavailable.

Do not convert unresolved product questions into fake standards. `Blocked` and `Not Run` are not passes.

## Audit Layers

Split checks into at least these layers:

- `Behavior Verification`: user/API/system behavior that proves the PRD outcome.
- `Implementation Audit`: code, data, permission, logging, observability, and test coverage checks needed to verify the implementation did not bypass critical requirements.
- `Test Execution`: commands, test suites, conditional execution rules, and static fallback verification.
- `Risk Gate`: release-blocking checks and hard fail conditions.

## Draft Admission Gate

Before clean-context review, the draft must have:

- source PRD boundary and requirement inventory
- traceability matrix
- at least one audit check per major PRD requirement or a blocked marker
- stable audit IDs
- behavior verification and implementation audit separation
- pass/fail criteria, required evidence, execution mode, test execution requirement, and status for ready checks
- high-risk checks marked `Blocker` or `High`
- ambiguous PRD content marked as blocked/open question
- no drift into PRD rewriting, technical design, or task decomposition

Use explicit draft admission outcomes:

- `Admitted - Ready`: the draft can support executable post-development audit standards without unresolved `Blocker` product semantics.
- `Admitted - Blocked`: the draft is structurally valid and worth reviewing, but core `Blocker` product semantics are unresolved. The final artifact must use overall status `Blocked`, not "Ready with blocking questions".
- `Rejected - Rewrite`: the draft is missing required structure, traceability, pass/fail criteria, evidence rules, or blocked-question handling.

If the draft is `Rejected - Rewrite`, rewrite it before clean-context review. Rewrite at most two times. If it still fails, save a blocked standards document explaining why review could not proceed.

If the draft is `Admitted - Blocked`, three clean-context review may still run to improve the blocked standards document, but the final readiness status remains `Blocked` until the blocking PRD questions are resolved. Do not use ad hoc statuses such as `Ready with blocking questions`.

## Clean-Context Review

Run three clean-context review rounds using `references/clean-context-review.md` after the draft passes the admission gate.

The reviewers inspect the same admitted draft, not separate drafts. The goal is to find gaps, overreach, weak evidence, weak testability, and unresolved risk.

## Merge Rules

Merge only after all three reviews complete:

- apply agreed findings when at least two reviewers identify the same gap
- apply single-reviewer findings when evidence is concrete and PRD-traceable
- give high-risk single-reviewer findings explicit accept/reject treatment
- reject findings that invent product behavior or contradict the PRD
- label useful non-PRD engineering checks as `derived quality standard`
- preserve unresolved reviewer disagreement in the review record

Do not embed full reviewer transcripts in the final artifact unless the user asks. Save a concise review record with focus, completion status, context isolation status, accepted findings, rejected findings, and unresolved issues.
