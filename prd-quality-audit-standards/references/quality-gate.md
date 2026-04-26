# Quality Gate

Run this self-review before saving the audit standards document.

## Draft Admission Gate

Before launching three clean-context review rounds, confirm that the draft:

- fully reads and cites the source PRD boundary
- includes a requirement inventory and traceability matrix
- gives every major PRD requirement at least one audit check or marks it blocked
- uses stable IDs such as `BV-*`, `IA-*`, `TE-*`, `RG-*`, `EV-*`, and `BQ-*`
- separates behavior verification from implementation audit
- includes pass/fail criteria, required evidence, execution mode, test execution requirement, and status for ready checks
- identifies high-risk checks as `Blocker` or `High`
- marks ambiguous PRD content as blocked/open question instead of inventing behavior
- avoids turning the output into a technical design, implementation plan, or PRD rewrite

If this gate fails, rewrite the draft before clean-context review. Rewrite at most two times. If it still fails, save a blocked standards document explaining why review could not proceed.

## Coverage Gate

Confirm that:

- every functional PRD requirement appears in the traceability matrix
- every acceptance criterion maps to at least one audit check
- each user role, workflow, lifecycle state, validation rule, and integration is covered or explicitly marked out of scope
- non-functional requirements are covered when the PRD defines them
- behavior verification and implementation audit checks both exist when black-box behavior alone cannot verify the PRD
- open questions and blocked checks are visible

## Specificity Gate

Each ready audit check should answer:

- What setup or data is needed?
- What action or review method is performed?
- What exact behavior passes?
- What evidence should be captured?
- What failure would block release?
- Is this automated, manual, review-only, or blocked?
- Is test execution required, conditional, static fallback, or not applicable?
- What is the retest scope if it fails?

If the check cannot answer those questions, either refine it or mark it blocked with the missing product detail.

## Risk Gate

Review whether high-risk areas have stronger pass/fail standards:

- permissions and role boundaries
- data integrity and duplicate processing
- payment, refund, billing, balance, or ledger behavior
- audit logs and compliance records
- irreversible or destructive operations
- privacy and sensitive data
- migrations and backward compatibility
- external integrations and asynchronous callbacks
- performance/reliability thresholds that affect core flows

## Artifact Gate

Before saving, ensure the document:

- names the source PRD and supporting context
- records bounded project-context inspection when a project path was provided
- distinguishes PRD-derived checks from derived quality standards
- records whether three clean-context review rounds were completed, approximated inline, or skipped with reason
- summarizes accepted, rejected, and unresolved findings from the clean-context reviews
- includes the three reviewer focus areas
- includes a machine-readable JSON/YAML appendix or links to an auxiliary machine-readable file
- includes environment prerequisites, test data requirements, test execution requirements, defect report format, retest rules, PRD change synchronization rules, and hard fail conditions
- includes a final readiness status
- does not silently invent product behavior
- can be used by a future implementation reviewer without rereading the whole PRD

Use only these artifact readiness statuses:

- `Ready`
- `Ready with assumptions`
- `Blocked`

If unresolved `Blocker` questions affect core product semantics, permissions, data integrity, irreversible actions, external integration behavior, or release-blocking pass/fail criteria, the overall artifact status must be `Blocked`. Do not write non-standard statuses such as `Ready with blocking questions`; they are ambiguous for audit agents.

## Hard Fail Gate

The standards cannot report unconditional readiness if any of these are true:

- any `Blocker` check is defined without pass/fail criteria
- any core PRD flow has no audit coverage
- high-risk permission, data, payment, ledger, privacy, or audit-log behavior lacks implementation audit coverage
- required test execution has no command, suite, static fallback, or blocker condition
- evidence requirements do not trace to audit check IDs
- failed-check defect reporting format is missing
- final conclusion rules are missing
- `Blocked` or `Not Run` states are treated as passes

If one or more gates fail, patch the document before saving. If the PRD prevents a gate from passing, mark the standards as blocked or ready with assumptions and explain why.
