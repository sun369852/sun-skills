# Execution Loop

## Implementation Brief

Before coding, create a compact brief:

- source document paths
- product goal and non-goals
- requested task scope
- current task states
- task dependencies
- acceptance criteria
- technical constraints
- expected test/build commands
- risky shared contracts
- assumptions and blockers

Write the brief or a summarized version into the run log.

## Batch Selection

A batch should be one feature area with strongly related tasks, not mechanically one task per worker. Combine tasks when they share a module, acceptance path, and verification command. Split tasks when they involve different business domains, pages, APIs, data models, or write scopes.

Shared schema, API contracts, permissions, global state, route structure, and core type definitions should usually be handled serially.

## Integration

When a worker completes:

1. Review the diff against the assigned write scope.
2. Check whether tests and implementation match the PRD and technical design.
3. Review risk by tier:
   - low risk: quick diff and verification check
   - medium risk: inspect core logic, edge cases, and tests
   - high risk: stricter review and possible clean-context review
4. Resolve conflicts with other work.
5. Run targeted or affected verification.
6. Decide final task status.
7. Update the task checklist and run log.

Worker "tests passed" is evidence, not final completion. The main agent makes the final call.

## Cross-Worker Conflicts

Resolve conflicts by:

1. Determining whether the conflict came from unsafe parallelization.
2. Preserving the implementation that best matches PRD, technical design, and current architecture.
3. Merging if both sides are valid and the merged result is smaller and more coherent.
4. Recording risk for API, schema, permission, or state-flow conflicts.
5. Re-running affected tests.
6. Switching future related tasks to serial execution if the conflict reveals hidden coupling.

In full-auto mode, the main agent may make conservative conflict decisions, but must record them.

## Stop Conditions

Stop the loop when:

- all requested executable tasks are done
- remaining tasks are blocked
- verification environment is unavailable and local/targeted verification cannot continue
- the user-specified time, task, or batch limit is reached
- a hard product or architecture decision is required
- a hard-risk operation requires confirmation
- the user asks to stop

Do not stop for an ordinary failing test until the failure-fuse process has been followed.
