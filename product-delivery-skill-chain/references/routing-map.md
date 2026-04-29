# Routing Map

Use this map to choose the next skill. Prefer the most specific downstream skill once the user's stage is clear.

## Prerequisites

This chain expects the local downstream skills named in the routing table to be available. If the selected downstream skill is not available in the current environment, tell the user which stage is blocked and either ask them to install/enable that skill or proceed manually with the same source artifact and handoff contract.

## Stage Routing

| User state or request | Route to | Required source |
| --- | --- | --- |
| Vague idea, incomplete requirement, unclear product boundary | `requirement-exploration` | User prompt |
| Clarified requirement should become a saved PRD | `prompt-to-prd-review` | Clarified requirement or strong feature brief |
| Existing PRD should become a technical design | `prd-to-tech-design-review` | PRD path or pasted PRD |
| Existing PRD should become tasks or `tasks.md` | `prd-task-archiver` | PRD path or pasted PRD |
| Existing PRD needs pre-implementation audit standards or acceptance contract for post-development review | `prd-quality-audit-standards` | PRD path or pasted PRD |
| Existing tasks/design/PRD should be implemented | `tdd-task-implementation-orchestrator` | Task list plus supporting PRD/design |
| Completed implementation should be accepted or rejected | `implementation-review-handoff` | Diff, commit range, branch, run log, or changed files plus source artifacts |

## Route Conflicts

When a request could route to multiple skills:

- PRD vs requirement exploration: if the requirement is vague, explore first; if it is mostly clear and the user asks for a PRD, use PRD review.
- Technical design vs task archive: if the user wants architecture/API/data/UI decisions, use technical design; if they want executable work items, use task archive.
- PRD to planning: after PRD approval, technical design and audit standards can run in parallel. Formal task archiving waits for technical design by default. Fast mode may produce draft tasks in parallel, then reconcile after technical design.
- Task archive vs implementation: if tasks are missing, archive first; if tasks exist and are clear, implement.
- Audit standards vs implementation review: generate audit standards before coding so review has an independent acceptance contract; use implementation review after code exists. Post-development standards updates should be supplemental and should not silently rewrite PRD intent.

## Conflict Priority

- If task archive and technical design conflict on implementation structure, revise the task archive to follow the technical design.
- If technical design, audit standards, or tasks conflict on product behavior, use the PRD as source of truth and ask the user when the PRD is ambiguous.
- If audit standards miss risks discovered in technical design, add supplemental audit checks for migration, permissions, recovery, compatibility, or validation without changing product semantics.

## Single-Skill Entry

If the user names a specific skill, artifact, or stage, route directly there unless the required source artifact is missing.

If the user invokes this chain skill and names an entry stage, start there and continue forward according to the requested target or the default stop point. Do not restart upstream stages only to make the chain look complete.

## Parallel Execution Constraint

Parallel planning means the stages are logically independent after PRD approval. Use actual subagents or delegated workers only when the host environment and user request authorize delegation or parallel agent work. Otherwise, run the stages sequentially while preserving the same dependency rules and reconcile step.

Treat authorization as present only when the user asks for agents, subagents, reviewers, parallel execution, 协同, 并行, full-auto, or an equivalent delegated workflow. If authorization or tools are missing, use this order: technical design, audit standards, then task archive.
