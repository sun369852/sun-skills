---
name: product-delivery-skill-chain
description: Use this skill when the user wants to connect the local product-development skills into a flexible end-to-end chain, choose the right next skill, run a complete flow from requirement exploration to PRD, technical design, audit standards, task archive, implementation, and review, maintain delivery-chain-status.md, or continue from any intermediate artifact. Strongly prefer it for prompts such as 串联这些 skill, skill 链路, 从需求到开发验收全流程, flexible skill workflow, choose next skill, continue from PRD/tasks/technical design, or when the user asks for an orchestrated but optionally single-skill workflow. Do not use it when the user clearly asks for only one already-specific downstream skill and no routing or handoff decision is needed.
---

# Product Delivery Skill Chain

## Purpose

Act as the routing layer across the local product-development skills. The goal is to decide the current stage, choose the smallest useful next step, preserve handoff artifacts, and keep a chain status file when this orchestration skill is invoked so the user can run the full chain or enter/exit at any point.

This skill does not replace the downstream skills. It coordinates them.

## Core Rule

Default to the shortest trustworthy path.

Entry order for a new chain request:

1. Identify the current stage and trusted source artifact.
2. Check whether `delivery/_chain-defaults.md` exists.
3. If it is missing, run the first-time defaults interview in `references/startup-contract.md`; do not preview the per-request contract or create chain artifacts yet.
4. After project defaults are confirmed and saved, or when existing defaults are present, read the defaults.
5. Merge explicit overrides from the current user request.
6. Preview the per-request chain start contract.
7. Wait for user confirmation.
8. Create the request directory, `delivery-chain-status.md`, source archive, and `source-context.md`.
9. Build the downstream invocation envelope.
10. Route to the selected downstream skill with the envelope.

After a request contract already exists, resume from that contract and continue from the next requested stage without re-confirming unless the current user instruction conflicts with it.

- If the user asks for the full flow, run the stages in order and stop at each artifact gate.
- If the user provides a mature artifact, enter from that stage instead of restarting upstream work.
- If the user explicitly asks for one skill or one artifact, route there and do not force the whole chain.
- If an upstream artifact is missing or too weak for the requested downstream step, ask one blocking question or recommend the upstream skill that should run first.
- When this skill is invoked for an existing confirmed request, maintain `delivery-chain-status.md`; when a downstream skill is invoked directly without this chain skill, do not create orchestration state.
- When this skill is invoked for a confirmed request, establish one chain artifact directory and save new chain artifacts there unless the user explicitly chooses another path.
- For a new chain request, first ensure project defaults exist or are explicitly confirmed, then preview the chain start contract and wait for user confirmation before creating the request folder, status file, source archive, or downstream artifacts.

## Default Chain

1. `requirement-exploration` clarifies uncertain requirements before generation.
2. `prompt-to-prd-review` converts clarified requirements into a reviewed PRD.
3. After the PRD is approved, run planning with controlled parallelism:
   - `prd-to-tech-design-review` creates the technical design.
   - `prd-quality-audit-standards` creates pre-implementation audit standards for post-development review from the PRD.
4. After the PRD and technical design are ready, extract the delivery topology contract for required runtime surfaces.
5. `prd-task-archiver` creates the formal task archive after the technical design and delivery topology are ready by default. In fast mode, it may create a draft task archive in parallel, but it must be reconciled after the technical design and topology contract.
6. `tdd-task-implementation-orchestrator` implements ready tasks with verification. After any batch changes shared runtime infrastructure, require a runtime verification gate before expanding to downstream feature batches.
7. `implementation-review-handoff` reviews completed implementation against source artifacts and audit standards.

Shared runtime infrastructure includes authentication, authorization, global filters, interceptors, middleware, application startup config, logging config, database schema used by runtime code, shared API response format, route registration, and dependency injection boundaries. If the runtime verification gate fails, route to fix mode before continuing implementation.

## Reference Loading

Read only the reference needed for the current decision:

- Read `references/routing-map.md` when deciding which skill should run next.
- Read `references/handoff-contracts.md` when moving between stages or checking whether an artifact is strong enough for the next stage.
- Read `references/flow-modes.md` when the user asks for full-auto, partial chain, single-skill mode, resume, or flexible execution.
- Read `references/status-file.md` whenever this skill needs to choose, update, or interpret `delivery-chain-status.md`; read `references/status-template.md` only when creating a new status file or replacing a missing/corrupt status body.
- Read `references/startup-contract.md` before starting a new chain, creating project defaults, previewing per-request execution rules, or handling commit/subagent/full-auto policy.
- Read `references/downstream-invocation-envelope.md` before invoking any downstream skill from this chain.
- Read `references/delivery-topology-contract.md` after PRD and technical design are ready, before task archiving, before implementation, before startup status answers, and before final review when runtime surfaces matter.
- Read `references/context-management.md` for long chains, after any durable artifact is saved, before implementation/review loops, or whenever the conversation has accumulated substantial interview, review, log, or troubleshooting context.
- Read `references/artifact-directory.md` before choosing output paths or invoking downstream skills that will save PRD, technical design, audit standards, task archive, implementation run log, review report, or handoff packets.

Do not bulk-load all downstream skill references. Once routed, follow the selected downstream skill's own loading rules.

## Interaction Rules

- State the inferred current stage and the source artifact being trusted.
- State assumptions before routing if the prompt is ambiguous.
- Present tradeoffs when more than one route is valid.
- Ask only one blocking question when routing cannot be decided safely.
- Do not silently invent missing PRD, design, task, audit, or implementation facts.
- Preserve the user's ability to stop after any stage and use the produced artifact manually.
- Use an LLM gate at every stage. Use a human gate after PRD approval, before coding, for high-risk conflicts, and after final review unless the user explicitly authorized full-auto behavior.
- For a new request, show the current chain start contract preview only after project defaults exist or have just been confirmed and saved; do not proceed until the user confirms it.
- Downstream skills must receive the confirmed invocation envelope. Do not let a downstream skill override disabled subagents, disabled commits, implementation confirmation, or explicit output paths from the chain contract.
- Startup status must be answered from the delivery topology contract, not from ports alone. Report every MVP-required runtime surface before giving an overall started/not-started conclusion.
- After each durable artifact is saved, switch the main thread to a light context: artifact paths, key decisions, unresolved blockers, and next action. Do not keep relying on full interview history once the artifact exists.

## Success Standard

This skill succeeds when:

- the user knows which stage they are in
- the next skill is chosen with a clear reason
- upstream and downstream artifact expectations are explicit
- full-chain execution remains possible without making single-skill usage harder
- no downstream skill is invoked with insufficient source material
- `delivery-chain-status.md` explains the entry point, preconditions, stage gates, artifacts, decisions, blockers, and latest next step whenever this chain skill was used
- long-running chains stay resumable from saved artifacts and status summaries instead of depending on accumulated conversation history
- chain start contract decisions, including execution mode, subagent policy, implementation confirmation, and git handoff policy, are explicit before the chain executes
- downstream invocation envelope carries those decisions into every routed skill
