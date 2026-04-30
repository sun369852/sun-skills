# Context Management

Use this reference to keep the main thread light during long product delivery chains.

## Core Rule

After a durable artifact is saved, treat the artifact as the source of truth. The main thread should retain only:

- current stage
- trusted source artifact paths
- key decisions
- unresolved blockers
- next action
- review or verification summary

Do not keep carrying full interview transcripts, reviewer discussions, implementation logs, or long error output once they have been summarized into the status file or a saved artifact.

## Phase Boundaries

Apply a context reset at these boundaries:

1. Requirement exploration completed and PRD work begins.
2. PRD saved and downstream planning begins.
3. Technical design saved.
4. Audit standards saved.
5. Task archive saved.
6. Implementation handoff packet created.
7. Implementation run log updated after each batch.
8. Review report or review-fix packet saved.

At each boundary:

- update `delivery-chain-status.md`
- report artifact paths, not full artifact content
- carry forward only non-blocking assumptions and blocking questions
- reload the artifact from disk if exact detail is needed later

## Subagent and Reviewer Use

When the user authorizes agents, subagents, reviewers, parallel execution, 协同, 并行, or full-auto:

- delegate frontend/backend review, implementation workers, audit reviewers, and repeated failure analysis as early as the downstream skill allows
- keep the main thread responsible for routing, integration, conflict resolution, and final decisions
- ask subagents for concise findings and artifact paths, not full rewritten transcripts
- do not paste long subagent outputs back into the main thread; summarize decisions and record paths

If delegation is not authorized, continue inline but still enforce artifact-based context boundaries.

## Log Handling

For long logs, test failures, or stack traces:

- read the log once
- summarize the actionable signal in 3-5 bullets
- record the log path and summary in `delivery-chain-status.md` or the run log
- avoid repeatedly pasting the same raw log into later prompts

If the same failure recurs, track it by failure signature rather than by repeating full output.

## Status Summary Template

Use this compact summary when continuing after a boundary:

```markdown
Current stage:
Source artifacts:
Completed artifacts:
Key decisions:
Open blockers:
Next action:
Context source of truth:
```

## Anti-Patterns

- continuing to reason from a long interview after the PRD has been saved
- passing full PRD text to every later stage when a path and short decision summary would work
- carrying complete frontend/backend review discussions after the technical design has incorporated them
- repeatedly reading or pasting the same error log
- using the main thread as the storage layer instead of `delivery-chain-status.md` and durable artifacts
