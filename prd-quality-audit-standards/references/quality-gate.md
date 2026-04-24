# Quality Gate

Run this self-review before saving the audit standards document.

## Coverage Gate

Confirm that:

- every functional PRD requirement appears in the traceability matrix
- every acceptance criterion maps to at least one audit check
- each user role, workflow, lifecycle state, validation rule, and integration is covered or explicitly marked out of scope
- non-functional requirements are covered when the PRD defines them
- open questions and blocked checks are visible

## Specificity Gate

Each ready audit check should answer:

- What setup or data is needed?
- What action or review method is performed?
- What exact behavior passes?
- What evidence should be captured?
- What failure would block release?
- Is this automated, manual, review-only, or blocked?

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
- distinguishes PRD-derived checks from derived quality standards
- includes a final readiness status
- does not silently invent product behavior
- can be used by a future implementation reviewer without rereading the whole PRD

If one or more gates fail, patch the document before saving. If the PRD prevents a gate from passing, mark the standards as blocked or ready with assumptions and explain why.
