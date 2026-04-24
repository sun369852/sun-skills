# Quality Metrics

Use these metrics for final self-check, review quality checks, and continuous improvement. They are not a rigid scoring system; they help decide whether the PRD is ready to save.

## PRD Completeness Score

Score each item 0, 1, or 2:

- Goal and scope are clear
- Users, roles, or systems are identified
- Core workflow or lifecycle is described
- Functional requirements are specific and testable
- Business rules and state semantics are explicit
- Permissions and visibility are covered
- Data, records, audit, or historical behavior is covered when relevant
- Edge cases and exception states are covered
- Acceptance criteria are concrete
- Assumptions and open questions are classified
- Existing-project compatibility is covered when relevant
- Review record and decision history are present

Interpretation:

- 20-24: strong enough to save if reviewers approve
- 16-19: likely usable, but check missing high-risk areas
- under 16: not ready unless the requirement is intentionally small

Do not save when any missing item is product-critical, even if the score is high.

## Scoring Guidelines

Use these standards for each completeness item.

### 2 Points: Excellent

- fully specified with concrete details
- no ambiguity likely to create different implementations
- testable or verifiable
- important edge cases or constraints are covered

Example: "User clicks Submit. System validates required fields and date range. On success, redirect to the dashboard with a success toast. On validation error, show inline messages and preserve form data."

### 1 Point: Acceptable

- core intent is clear
- some details are missing, but they do not change the main behavior
- mostly testable
- remaining ambiguity can be handled as non-blocking assumption or reviewer feedback

Example: "User submits the form. System validates it and shows success or error message."

### 0 Points: Insufficient

- vague or missing
- multiple interpretations are likely
- not testable
- likely to cause rework or conflicting implementation

Example: "User can submit the form."

### Not Applicable

Do not score items that are genuinely irrelevant. Mark them as N/A and explain why.

Example: "Responsive design: N/A because this is a desktop-only internal operations console and the user confirmed no mobile support."

## Quick Self-Check

Before inviting reviewers, answer:

1. Can a developer read this PRD and know what behavior to build?
2. Can QA read this PRD and write test cases?
3. Are all assumptions and open questions explicitly labeled?
4. If this is an existing project, are compatibility risks identified?
5. Would this PRD be acceptable as the current product baseline?

Use `Yes`, `Mostly`, `No`, or `N/A`.

Proceed to review when all answers are `Yes` or `N/A`, or when at most one answer is `Mostly` and no answer is `No`.

Revise before review when any answer is `No`, or when two or more answers are `Mostly`.

## Review Quality Score

For each reviewer, check:

- role-specific perspective is clear
- reviewer mentions concrete PRD sections or rules
- blocking findings are explicit
- non-blocking suggestions are separated
- recommended text changes are actionable
- approval explains why remaining uncertainty is acceptable
- existing project context is considered when applicable

If a simulated review scores poorly, rerun the review more critically before saving.

## Process Health Metrics

Track informally across evals or real use:

- review pass rate by round
- number of blocking questions found before saving
- number of reviewer comments that led to PRD changes
- number of current-state conflicts surfaced
- number of times a saved PRD needed immediate rework

Use these metrics to improve the skill. A good run is not "no findings"; a good run finds important issues before the PRD becomes the baseline.

## Save Readiness

The PRD is ready to save when:

- no blocking open questions remain
- frontend and backend review are approved
- any specialist review trigger is resolved or explicitly deferred
- review history explains material changes
- source priority and project context are recorded when relevant
- non-blocking questions are visible enough for future readers
