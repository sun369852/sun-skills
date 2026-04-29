---
name: product-delivery-skill-chain
description: Use this skill when the user wants to connect the local product-development skills into a flexible end-to-end chain, choose the right next skill, run a complete flow from requirement exploration to PRD, technical design, audit standards, task archive, implementation, and review, maintain delivery-chain-status.md, or continue from any intermediate artifact. Strongly prefer it for prompts such as 串联这些 skill, skill 链路, 从需求到开发验收全流程, flexible skill workflow, choose next skill, continue from PRD/tasks/technical design, or when the user asks for an orchestrated but optionally single-skill workflow. Do not use it when the user clearly asks for only one already-specific downstream skill and no routing or handoff decision is needed.
---

# Product Delivery Skill Chain

## Purpose

Act as the routing layer across the local product-development skills. The goal is to decide the current stage, choose the smallest useful next step, preserve handoff artifacts, and keep a chain status file when this orchestration skill is invoked so the user can run the full chain or enter/exit at any point.

This skill does not replace the downstream skills. It coordinates them.

## Core Rule

Default to the shortest trustworthy path:

- If the user asks for the full flow, run the stages in order and stop at each artifact gate.
- If the user provides a mature artifact, enter from that stage instead of restarting upstream work.
- If the user explicitly asks for one skill or one artifact, route there and do not force the whole chain.
- If an upstream artifact is missing or too weak for the requested downstream step, ask one blocking question or recommend the upstream skill that should run first.
- When this skill is invoked, create or maintain `delivery-chain-status.md`; when a downstream skill is invoked directly without this chain skill, do not create orchestration state.

## Default Chain

1. `requirement-exploration` clarifies uncertain requirements before generation.
2. `prompt-to-prd-review` converts clarified requirements into a reviewed PRD.
3. After the PRD is approved, run planning with controlled parallelism:
   - `prd-to-tech-design-review` creates the technical design.
   - `prd-quality-audit-standards` creates pre-implementation audit standards for post-development review from the PRD.
4. `prd-task-archiver` creates the formal task archive after the technical design is ready by default. In fast mode, it may create a draft task archive in parallel, but it must be reconciled after the technical design.
5. `tdd-task-implementation-orchestrator` implements ready tasks with verification.
6. `implementation-review-handoff` reviews completed implementation against source artifacts and audit standards.

## Reference Loading

Read only the reference needed for the current decision:

- Read `references/routing-map.md` when deciding which skill should run next.
- Read `references/handoff-contracts.md` when moving between stages or checking whether an artifact is strong enough for the next stage.
- Read `references/flow-modes.md` when the user asks for full-auto, partial chain, single-skill mode, resume, or flexible execution.
- Read `references/status-file.md` whenever this skill needs to create, update, or interpret `delivery-chain-status.md`.

Do not bulk-load all downstream skill references. Once routed, follow the selected downstream skill's own loading rules.

## Interaction Rules

- State the inferred current stage and the source artifact being trusted.
- State assumptions before routing if the prompt is ambiguous.
- Present tradeoffs when more than one route is valid.
- Ask only one blocking question when routing cannot be decided safely.
- Do not silently invent missing PRD, design, task, audit, or implementation facts.
- Preserve the user's ability to stop after any stage and use the produced artifact manually.
- Use an LLM gate at every stage. Use a human gate after PRD approval, before coding, for high-risk conflicts, and after final review unless the user explicitly authorized full-auto behavior.

## Success Standard

This skill succeeds when:

- the user knows which stage they are in
- the next skill is chosen with a clear reason
- upstream and downstream artifact expectations are explicit
- full-chain execution remains possible without making single-skill usage harder
- no downstream skill is invoked with insufficient source material
- `delivery-chain-status.md` explains the entry point, preconditions, stage gates, artifacts, decisions, blockers, and latest next step whenever this chain skill was used
