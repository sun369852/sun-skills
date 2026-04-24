# Quality Gate

Before saving the technical design, check the draft against this list.

## Required Checks

- Every major PRD requirement appears in the scope mapping or is explicitly marked out of scope.
- At least 80% of concrete PRD functional requirements are mapped to technical coverage. If coverage is below 80%, do not save it as final. First patch the draft if possible; otherwise save it with a `DRAFT-` filename prefix and add a top-level warning block that lists missing coverage and blocking questions.
- Frontend and backend designs agree on API names, payload shape, status values, validation rules, and error behavior.
- Each API used by the frontend has request, response, and error behavior described, even if the exact schema is deferred.
- Every lifecycle status mentioned in the PRD has allowed transitions and invalid transitions recorded.
- Assumptions are labeled as assumptions, not hidden as facts.
- Blocking product questions are separated from technical follow-ups.
- Existing project conventions are respected when project context was available.
- Security, permissions, privacy, and audit concerns are covered when user data or privileged actions are involved.
- Testing strategy covers both user flows and backend business rules.
- If second-pass review was requested or triggered, required changes are integrated or explicitly recorded as open risks/questions.
- The document is specific enough for task decomposition.

## Minimum Coverage Targets

Use these as practical thresholds, not bureaucracy:

- PRD functional requirement mapping: 80% or higher
- user-facing flows: all primary flows covered
- frontend/backend contract points: all listed or explicitly deferred
- high-risk items: all have mitigation, owner, or open question
- blocking questions: no more than 3 unresolved before asking the user

## Common Failure Modes

- Writing a generic architecture essay that is not traceable to the PRD.
- Letting frontend and backend sections contradict each other.
- Inventing product policy where the PRD is silent.
- Omitting unhappy paths, empty states, or permission failures.
- Producing tasks instead of design decisions.
- Saving a document without recording unresolved questions.

Patch the document before saving when any required check fails.
