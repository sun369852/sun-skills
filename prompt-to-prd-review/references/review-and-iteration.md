# Review and Iteration

Use this reference before invoking reviewers, merging feedback, resolving conflicts, or deciding whether extra review is needed.

## Standard Reviewers

The main flow owns the PRD. Reviewers own critique, risk discovery, and approval.

Use these bundled prompts:

- `agents/frontend-prd-reviewer.md`
- `agents/backend-prd-reviewer.md`

## Reviewer Invocation Strategy

Use actual subagents when any of these are true:

- the current environment has a subagent/delegation tool available to the main flow
- this is an existing-project iteration and reviewers need to inspect code/docs from their own role perspective
- the PRD touches money, permissions, historical records, integrations, data export/reporting, or operational workflows
- the first self-review found meaningful risks that benefit from independent critique
- the user explicitly asked for frontend/backend agents, subagents, or independent reviewers

Inline simulation is acceptable only when:

- subagent tooling is unavailable in the current environment
- the skill is being executed inside a child worker that cannot create further subagents
- the user explicitly asked for a lightweight inline review
- the task is a low-risk PRD update and the user did not ask for independent agents

When using simulation, run a review quality check before accepting simulated approval:

- frontend and backend perspectives must be visibly different
- each review must mention at least one concrete PRD section, rule, state, or acceptance criterion
- each review must state whether there are blocking findings
- approval must explain why remaining open questions are non-blocking
- for existing-project iterations, simulation must mention what project context was or was not available
- if both simulated reviewers approve without any critique on a non-trivial PRD, perform one more adversarial self-check before saving

Give each reviewer:

- original source prompt and material summary
- current PRD draft
- source-priority notes when multiple materials exist
- requirement mode
- project path and compact project context package when applicable
- assumptions and open questions with blocking/non-blocking classification
- instruction that approval means "coherent enough to save as the current product baseline", not "ready to implement"

For existing-project iterations, instruct reviewers to inspect relevant current project files themselves when available. Keep the review bounded to PRD critique, not implementation planning.

## Review Checklist

Before accepting reviewer approval, confirm:

- reviewer response uses the expected approval status
- blocking findings are resolved or converted into user questions
- non-blocking suggestions are either applied, rejected with reason, or recorded
- recommended PRD changes are reflected in the current draft when accepted
- assumptions and open questions are classified
- review notes are specific enough to audit later

If a reviewer response is vague, ask that reviewer for a sharper pass instead of treating it as approval.

## Merge Feedback

After reviewer feedback:

- apply clear corrections that improve fidelity to the source prompt
- add missing rules, states, edge cases, acceptance criteria, assumptions, and compatibility notes
- keep unresolved items explicit
- reject or record scope expansion unless the user confirms it
- rerun both reviews after material PRD changes, even if only one reviewer requested the change
- maintain a review history entry for each round: reviewer, status, key findings, accepted changes, rejected changes, and reason

## Reviewer Conflicts

When frontend and backend feedback conflicts:

1. Check the source prompt and latest user instructions.
2. If the source supports a clear resolution, update the PRD and note the decision.
3. If not, create a decision record with both positions, impact, and proposed default.
4. Ask one focused user question if the conflict changes product semantics or blocks approval.
5. If non-blocking, record it as an open question and continue only if both reviewers can approve with that question preserved.

Decision record format:

```markdown
| Decision Point | Frontend View | Backend View | Chosen PRD Treatment | Reason | Remaining Risk |
| --- | --- | --- | --- | --- | --- |
```

## Open Question Gate

Do not save the PRD while any `Blocking Open Question` remains.

It is acceptable to save with `Non-blocking Open Question` or `Post-MVP Follow-up` items when:

- they are clearly labeled
- they do not change the agreed first-version behavior
- both reviewers approve with those items recorded

## Current-State Conflicts

If docs, code, and requirement materials disagree:

- name the conflict in the PRD
- avoid silently treating code or docs as the product truth
- ask the user for the authoritative source when the choice changes behavior
- let reviewers comment on compatibility risk from their perspective

## Additional Specialist Review

Frontend and backend review are the default gate. Add a specialist review only when the PRD has a clear risk that those reviewers cannot responsibly cover.

Possible specialist reviews:

- data/BI: metrics, dashboards, reporting definitions, tracking, export fields
- security/permission: sensitive data, access control, audit, abuse risk
- operations: admin workflows, manual handling, customer service, SOPs
- mobile/H5: app-specific navigation, device constraints, push/deep links
- legal/compliance: retention, consent, financial rules, regulated data

Trigger specialist review or explicitly recommend it when:

- payment, refunds, invoices, balances, credit, financial reporting, or money movement appears: recommend security/permission and data/reporting review
- personal data, sensitive identifiers, private messages, precise location, or access logs appear: recommend security/privacy review
- role permissions, admin actions, audit trails, or cross-tenant access appears: recommend security/permission review
- metrics, dashboards, exports, attribution, or statistics appear: recommend data/BI review
- manual operation, customer service, exception handling, or offline workflows appear: recommend operations review
- mobile app, H5, push, deep links, or device-specific behavior appears: recommend mobile/H5 review
- legal retention, consent, regulated domains, invoices, tax, medical, or HR data appears: recommend legal/compliance review

Do not create specialist reviewers by default for low-risk features. If the trigger is present but the need is not clearly blocking, record "specialist review recommended" in the review history or open questions.

## Complexity Assessment and Iteration Limit

Assess complexity before starting review so the iteration limit is explicit.

### Simple Requirement

Typical signals:

- single page, component, endpoint, or small workflow
- 1-2 roles
- 0-2 meaningful states
- no external integrations
- no data migration
- no payment, refund, invoice, balance, or compliance impact

Example: add a filter field to an existing list page.

### Normal Requirement

Typical signals:

- 2-4 pages/components or a contained backend capability
- 2-3 roles
- 3-5 states
- 0-1 external integration
- limited historical data impact
- no complex migration

Example: add an approval workflow to an existing feature.

### Complex Requirement

Any of these signals is enough:

- 5+ pages/components
- 4+ roles
- 6+ meaningful states
- 2+ external integrations
- data migration with historical records
- payment, refund, invoice, balance, or financial reporting
- cross-system workflow
- existing-project iteration affecting 3+ modules
- sensitive data, audit, compliance, or permission model changes

### Very Complex Requirement

If multiple complex signals are present, consider splitting the requirement into multiple PRDs, using an MVP plus increments, or adding specialist reviews before the standard review loop.

Record the complexity assessment in review notes or the final review record.

Iteration limits:

- simple requirement: 1-2 review rounds
- normal product feature: up to 2 review rounds
- complex existing-project iteration, payment/permission/data-heavy requirement, or multi-system workflow: up to 3 review rounds
- very complex requirement: consider splitting or adding specialist reviews before continuing

If the same blocking issue remains after the applicable limit, or reviewers cannot approve without a user decision, pause and ask the user for the narrow decision needed. Provide:

- the unresolved decision
- why it blocks saving
- frontend/backend impact
- a recommended option if the source materials support one

## Review History

Maintain review history during iteration. The final PRD should include a condensed version; detailed notes can live in reviewer notes when output files are being produced.

Suggested table:

```markdown
| Round | Reviewer | Status | Key Feedback | PRD Change | Remaining Issue |
| --- | --- | --- | --- | --- | --- |
```
