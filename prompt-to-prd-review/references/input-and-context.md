# Input and Context Handling

Use this reference when inputs are multi-source, project-related, or ambiguous.

## Supported Inputs

The user may provide:

- a pasted downstream prompt
- a direct feature description that is already complete enough for PRD generation
- a file path containing the prompt
- a conversation summary plus an instruction such as "基于这个生成 PRD"
- an existing PRD draft plus a new explored requirement prompt
- an existing PRD/spec plus a simple incremental change description
- codebase/project paths, docs, screenshots, tickets, or module names
- extra user corrections after requirement exploration

If a file path is provided, read it before drafting.

This skill is not limited to materials produced by `requirement-exploration`. Use it whenever the user has enough clarified product intent to generate a PRD and the expected workflow is review-gated PRD finalization.

If the input is a direct description without requirement-exploration output, treat the direct description as the highest-priority source. If it is clear enough, proceed. If it is vague, route back to requirement clarification behavior and ask one focused blocking question.

## Direct Description Clarity Check

When input is a direct feature description, check whether it is clear enough before drafting.

Minimum threshold:

- What: the core feature or change
- Who: target users, roles, or systems
- Why: goal or problem being solved
- Scope: what is included and what is not

Proceed directly when the description includes most of:

- background and goal
- primary user scenario
- core functional requirements
- success criteria or expected outcome
- explicit scope boundaries
- important constraints or dependencies

Ask one focused question when exactly one critical item is missing:

- If users/roles are unclear: "Who are the primary users or roles for this feature?"
- If scope is unclear: "What is explicitly out of scope for the first version?"
- If success is unclear: "How will we know this feature is working correctly?"
- If core behavior is unclear: "What happens when [primary action] is triggered?"
- If constraints are unclear: "What existing rule or system must this feature preserve?"

Route back to requirement exploration when:

- multiple critical items are missing
- the user says they are unsure about the focused question
- the description is a vague idea rather than a clarified requirement
- the request would require broad discovery before a PRD could be trustworthy

Clear enough example:

> Add a "Cancel Order" button to the order detail page. Only customers who placed the order can cancel. Orders can only be cancelled within 24 hours and before shipping. When cancelled, refund the payment and send email notification. Out of scope: partial cancellation and admin cancellation.

Needs one question:

> Add order cancellation feature. Users can cancel their orders and get refunded.

Ask: "What are the time/status constraints for cancellation?"

Route to exploration:

> We need better order management.

If the input is an existing PRD plus a short change request, treat it as an existing-project or existing-document iteration:

- preserve current PRD decisions unless the new request explicitly changes them
- add a source-priority note for "existing PRD baseline" versus "new change request"
- decide whether to update the existing PRD or create an incremental PRD using `references/finalize-and-record.md`
- ask for clarification only when the change conflicts with core existing behavior or the intended file treatment is ambiguous

## Source Priority

When materials conflict, use this default priority:

1. Latest explicit user instruction in the current conversation
2. Requirement-exploration final downstream prompt
3. Direct feature description supplied for this PRD task when no requirement-exploration output exists
4. User-approved addenda or corrections
5. Existing PRD/spec/docs
6. Current code or observed product behavior
7. Reasonable assumptions, only when labeled as assumptions

If the existing PRD/docs conflict with code or observed behavior, do not silently choose one. Record a "current-state conflict" and ask the user which source should be authoritative when the decision changes product semantics. If the conflict is non-blocking, record it as an open question.

## Requirement Mode

Classify the work as:

- `new_requirement`: no existing product/code constraint is provided or implied
- `existing_project_iteration`: the requirement changes an existing product, module, workflow, repository, or deployed behavior
- `new_requirement_with_existing_dependencies`: the feature is new but relies on existing systems such as account, permission, order, payment, notification, reporting, or content modules
- `unclear`: the prompt implies existing behavior but lacks enough context to know what must be preserved

For `unclear`, ask one focused question only if the missing context would materially affect the PRD. Otherwise record the uncertainty and proceed.

## Existing Project Context Package

For existing-project iterations, gather a lightweight project context package before drafting:

- affected product areas, routes, pages, components, APIs, services, data models, jobs, permissions, integrations, and reports
- current behavior that must be preserved
- current terminology, states, role names, and business rules
- compatibility constraints, migration concerns, historical data behavior, and rollout constraints
- conflicts between requirement materials and current project reality

Use fast local inspection tools when available. Prefer `rg`, `rg --files`, package manifests, routes, controllers, schemas/models, permission logic, docs, and existing PRDs/specs.

Keep the context package compact. It should make the PRD compatible with reality, not become a technical design.

## New Feature With Existing Dependencies

Even when the feature is new, check whether it depends on existing systems. If it does, add a small compatibility note to the PRD and tell reviewers which dependencies to consider.

Examples:

- account and role system
- order, payment, refund, invoice, or subscription system
- notification, messaging, or email system
- content, inventory, workflow, approval, or reporting system
- data export, audit, compliance, or BI metrics

## Blocking vs Non-Blocking Open Questions

Classify unresolved questions:

- `Blocking Open Question`: must be answered before saving because it changes core semantics, permissions, historical records, data ownership, money movement, legal/compliance obligations, or primary success criteria
- `Non-blocking Open Question`: can be recorded in the PRD because it does not change the agreed first version
- `Post-MVP Follow-up`: explicitly out of current scope but useful to preserve for later

Do not save the PRD while blocking open questions remain unresolved.
