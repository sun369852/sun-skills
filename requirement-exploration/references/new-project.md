# New Project / Greenfield Exploration

Use this reference when the requirement is mostly about a new feature or new project, and there is no strong need to reconcile against existing product behavior or code logic.

## Goal

Clarify the product requirement enough for reliable downstream generation without drifting into technical design too early.

## Prioritize

Clarify in this order:
1. why this is needed
2. who it is for
3. what problem it solves
4. in which scenario it is used
5. what the current scope is
6. what rules, dependencies, or constraints exist
7. what must be true for this to count as successful

## Coverage Check

Before concluding the requirement is complete, check whether these areas are sufficiently covered:
- background and motivation
- goal and expected value
- target users or roles
- core usage scenarios
- key capability or feature expectations
- in-scope and out-of-scope boundaries
- business rules, dependencies, and constraints
- priority and trade-offs
- success criteria or acceptance expectations
- risks, assumptions, and unresolved items

## Draft-Based Input

If the user gives an existing PRD/spec draft, do not assume it is complete just because it is formatted. Read it as input material and identify missing decisions, weak boundaries, unsupported assumptions, and places likely to create downstream rework.

## Workflow

1. Read the user input and identify the biggest information gap.
2. Ask one focused question.
3. Continue iterative clarification until the main requirement is understandable.
4. Summarize what is already clear.
5. List unresolved items, ambiguity, and missing information.
6. Let the user supplement, correct, narrow, or expand them.
7. Reassess whether the requirement is complete enough.
8. Ask explicitly whether to start final generation.
9. Only then generate the final downstream prompt.
