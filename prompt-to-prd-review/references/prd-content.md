# PRD Content Guide

Use this reference before drafting or revising the PRD.

If the requirement shape is not a normal end-user feature, read `references/template-variants.md` and adapt the base structure instead of forcing every section to look the same.

## Base Structure

Adapt section names to the product, but include these contents unless clearly irrelevant:

```markdown
# [Feature Name] PRD

## 1. Background
## 2. Goals and Non-Goals
## 3. Users and Scenarios
## 4. Scope
## 5. User Journey / Workflow
## 6. Functional Requirements
## 7. Business Rules
## 8. Permissions and Roles
## 9. Data, Records, and State Changes
## 10. Edge Cases and Exception Handling
## 11. Acceptance Criteria
## 12. Risks, Assumptions, and Open Questions
```

For existing-project iterations or new features with existing dependencies, add:

```markdown
## Existing Product Context and Compatibility
```

Use this section to record affected current flows, current constraints, behaviors that must remain unchanged, compatibility risks, and current-state conflicts.

## Content Rules

- Keep the PRD product-oriented.
- Include implementation details only when they clarify product behavior.
- Use tables for role permissions, state transitions, acceptance criteria, field definitions, existing-versus-new behavior, and compatibility checks.
- Preserve unresolved items explicitly instead of inventing answers.
- Separate confirmed scope, assumptions, open questions, and post-MVP follow-ups.
- If reviewer feedback adds scope beyond the source requirement, record it as a suggestion unless the user confirms it.

## Useful Tables

Role permissions:

```markdown
| Role | Can View | Can Create | Can Edit | Can Approve | Notes |
| --- | --- | --- | --- | --- | --- |
```

State transitions:

```markdown
| Current State | Trigger | Next State | Actor | Notes |
| --- | --- | --- | --- | --- |
```

Acceptance criteria:

```markdown
| ID | Scenario | Given | When | Then |
| --- | --- | --- | --- | --- |
```

Compatibility:

```markdown
| Existing Area | Current Behavior | Required Change | Must Preserve | Risk |
| --- | --- | --- | --- | --- |
```

Open questions:

```markdown
| Question | Type | Impact | Owner/Decision Needed |
| --- | --- | --- | --- |
```
