# Failure Fuse

## Failure Signature

Track repeated failures by issue signature, not by loose wording. A signature can be:

- test name plus assertion or error class
- command plus core error message or exit behavior
- file/module plus type error class
- runtime exception root
- acceptance criterion that remains unmet

If the visible error changes but the root cause is clearly the same, continue the count. If the failure moves to a new test, module, or acceptance criterion, start a new count.

## Attempt Limit

For each issue signature:

1. Attempt a focused fix.
2. Re-run the smallest meaningful verification.
3. Increment the count only when the same signature remains unresolved.
4. Stop local repair after 5 failed attempts.

## Fresh-Context Handoff

After 5 failed attempts, do not keep patching in the same context. Create a handoff packet:

- original task packet
- current diff summary
- exact failing commands and errors
- fixes already tried
- suspected causes labeled as hypotheses
- files that must not be reverted

Use `agents/fresh-failure-analyzer.md` for a clean-context analysis pass.

## Two-Stage Handling

The fresh analyzer should first produce root-cause analysis and a repair plan. The main agent reviews the plan. If risk is low and write scope is clear, the main agent can authorize repair. If high-risk, record the risk and ask the user unless full-auto mode or the chain envelope's `High-risk operations: no-confirmation` policy allows a conservative decision. With `no-confirmation`, do not ask just to accept risk; choose a conservative repair path or block the affected task.
