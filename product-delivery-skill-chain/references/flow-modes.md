# Flow Modes

Choose the lightest mode that matches the user's request.

## Full Chain

Use when the user asks for an end-to-end path such as "从需求到开发验收跑完整链路".

Process:

1. Identify whether the current requirement is clear enough.
2. Establish or preview the chain start contract. If this is a new request, wait for user confirmation before creating files or running downstream stages.
3. Establish the chain artifact directory and record it in `delivery-chain-status.md` after the contract is confirmed.
4. Run each stage only after its source artifact is adequate.
5. After PRD approval, run technical design and audit standards in parallel when possible.
6. Reconcile technical design and audit standards after both complete.
7. Create the formal task archive after technical design by default.
8. Ask for confirmation before moving from planning artifacts into coding unless the confirmed contract allows full-auto execution.
9. After implementation, run review and enter the bounded review-fix loop if needed.

## Partial Chain

Use when the user wants a range such as PRD to tasks, PRD to implementation, or implementation to review.

Process:

1. Start from the earliest artifact the user provided.
2. Skip upstream stages whose artifact is already trustworthy.
3. Reuse the existing request contract when resuming, or preview a new per-request contract and wait for confirmation.
4. Establish or reuse the chain artifact directory.
5. Create or update `delivery-chain-status.md` because the user invoked the chain skill.
6. Run only the requested downstream span, passing explicit output paths inside the chain artifact directory.
7. If the requested span includes implementation, pass the confirmed git handoff policy to `tdd-task-implementation-orchestrator`.

## Single-Skill Mode

Use when the user clearly asks for one artifact or names one skill.

Process:

1. Verify the required input exists.
2. Route directly to the selected skill.
3. If the user invoked this chain skill to reach that single stage, maintain `delivery-chain-status.md`.
4. If the user directly invoked the downstream skill without this chain skill, do not add orchestration artifacts unless the selected skill requires them.

## Resume Mode

Use when the user has previous outputs and wants to continue.

Process:

1. Locate the latest relevant artifact paths conservatively.
2. If there is exactly one obvious candidate, use it and state the inference.
3. If there are multiple plausible candidates, present the 2-3 best options and ask the user to choose.
4. If candidates are stale, mismatched, or unclear, ask for the source artifact.
5. Identify completed, current, and next stages.
6. Reuse the artifact directory from the matching `delivery-chain-status.md`, or establish a new chain artifact directory before saving new outputs.
7. Continue from the next missing or requested artifact.

## Flexible Mode

Use when the user wants a chain but also wants freedom to skip or branch.

Process:

1. Present the inferred next step and one reasonable alternative.
2. Explain the tradeoff briefly.
3. Continue with the next step when the choice is obvious; ask when the choice changes scope or cost.

## Fast Planning Mode

Use when the user values speed and accepts a reconciliation step.

Process:

1. After PRD approval, run technical design, audit standards, and draft task archive in parallel when tooling supports it.
2. Mark the task archive as draft and pending technical design confirmation.
3. After technical design and audit standards complete, reconcile audit checks against technical risks and reconcile draft tasks against technical decisions.
4. Save or update the formal task archive only after reconciliation.

## Parallel Execution Rules

- Check whether delegated worker/subagent tools are available and authorized before starting actual parallel execution.
- If actual parallel execution is unavailable or unauthorized, preserve the same logical plan but run stages sequentially: technical design, audit standards, then task archive.
- Record the execution mode in `delivery-chain-status.md`: `parallel`, `sequential fallback`, or `fast draft parallel`.
- Do not launch parallel workers for the same write target. Technical design, audit standards, and draft tasks must write separate artifacts.

## Planning Reconciliation

After technical design and audit standards both exist, check:

- whether technical design covers behaviors the audit standards require verifying
- whether audit standards include technical risks discovered during design, such as migrations, permissions, recovery, compatibility, and validation
- whether technical design, audit standards, and tasks use the same product behavior as the PRD

Reconciliation steps:

1. Compare draft tasks against technical design decisions, including API contracts, data migrations, validation, UI structure, permissions, integrations, and verification strategy.
2. Add or revise tasks for missing migration, compatibility, release, test, or documentation work that follows from the technical design.
3. Compare audit standards against technical risks discovered during design and add checks for migrations, permissions, recovery, compatibility, observability, and validation when relevant.
4. Resolve implementation-structure conflicts in favor of technical design.
5. Resolve product-behavior conflicts in favor of the PRD, and ask the user when the PRD is ambiguous.
6. Mark draft task artifacts as `reconciled` only after the conflicts and missing coverage are addressed.
7. Record reconciliation decisions in `delivery-chain-status.md`.

## Default Stop Points

When the user gives an entry stage but no explicit target:

- From requirements: stop after PRD is saved and approved for downstream planning.
- From PRD: stop after technical design, audit standards, and formal task archive are complete; require confirmation before coding.
- From technical design: stop after formal tasks are complete; require confirmation before coding.
- From tasks: prepare the implementation handoff and require confirmation before coding.
- From implementation-ready artifacts plus explicit implementation request: run implementation and review according to the confirmed chain start contract.
- From completed implementation: run review only.
