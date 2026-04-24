# Existing Project Iteration

Use this reference when the user is adding to, revising, or extending an existing product, feature, workflow, PRD, or codebase.

## Goal

Do not explore the new requirement in isolation. Clarify how it relates to current behavior, current rules, existing feature boundaries, and known constraints so the downstream prompt does not accidentally conflict with what already exists.

## Additional Analysis Layer

Include one extra layer of requirement analysis:
- understand what already exists
- identify what current behavior, assumptions, or boundaries may be affected
- identify where the new request is compatible, overlapping, dependent, or conflicting

Do not jump into solution design, but do make hidden compatibility and impact questions explicit before final generation.

## Clarify These Areas

For existing-project iteration cases, also clarify:
- what the current product or feature already does
- which existing flows, rules, states, permissions, or integrations the new requirement touches
- whether the new requirement is additive, substitutive, or behavior-changing
- what compatibility expectations exist for current users, data, workflow, or APIs
- what downstream dependencies or adjacent modules may be impacted
- where the requirement may conflict with current logic, boundaries, or assumptions

## Coverage Check

Before concluding the requirement is complete, make sure the exploration surfaces:
- current behavior that matters to the new request
- compatibility expectations that should be preserved
- affected areas and likely impact scope
- relevant dependency touchpoints
- likely conflict points with current behavior or logic
- assumptions the downstream spec must keep visible

## Review Requirements

Before final generation, explicitly review:
- what current behavior or existing logic this requirement appears to depend on
- what existing modules, flows, roles, states, interfaces, or rules are likely affected
- any compatibility expectations that should be preserved
- any likely impact range, dependency links, or conflict points that the downstream spec should keep visible

## Common Mistakes

- treating the requirement like a greenfield feature when it is really an iteration on an existing system
- ignoring how current behavior constrains the new requirement
- failing to surface compatibility, impact, dependency, or conflict risks
- writing a downstream prompt that sounds polished but hides interaction risk with existing logic
