---
name: tdd-task-implementation-orchestrator
description: Use this skill when the user wants to start development execution from an existing PRD, task checklist, technical design, architecture document, spec, or implementation plan. This skill is specifically for coding execution, not for creating PRDs, designs, or task breakdowns. It orchestrates TDD-oriented implementation with clean-context feature-area workers, bounded task batches, task-list updates, run logs, optional git branch/worktree/local commits, safe parallelism, and a 5-attempt failure fuse before clean-context re-analysis. Trigger for prompts such as "根据 PRD 和任务清单开始开发", "执行 specs/.../tasks.md 里的开发任务", "按技术文档 TDD 实现", "实现 tasks.md", "implementation plan plus PRD/design docs to code the feature", "use agents to implement tasks", "clean context subagents", "领取下一个任务", "spec-driven TDD coding", "从 PRD/技术方案/任务列表进入开发", or requests to execute a development plan.
---

# TDD Task Implementation Orchestrator

## Purpose

Execute an already-planned software development scope from PRD, technical documentation, and task checklist artifacts. This skill does not write the PRD, produce the technical design, or decompose vague work into a full task plan. It turns ready execution artifacts into working code through bounded task batches, TDD-oriented verification, clean-context workers, run logging, and controlled integration.

The main agent is the orchestrator. It owns source discovery, task eligibility, batching, worker packets, integration review, verification strategy, task-list updates, run-log updates, and final reporting. Workers own only their assigned feature area and allowed write scope.

## Hard Boundary

Use this skill only for development execution. If the task checklist, PRD, or technical design is missing or too vague to support safe execution, stop the affected task and record it as blocked. Provide the smallest clarification needed, but do not replace upstream planning by inventing a new PRD, technical design, or full task breakdown.

## Reference Loading

Load only the references needed for the current situation:

| Situation | Read |
| --- | --- |
| Every invocation | `references/scope-and-inputs.md`, `references/execution-loop.md`, `references/run-log-and-task-list.md`, `references/completion-and-final-report.md` |
| TDD, test selection, skipped tests, unrelated failures | `references/tdd-and-verification.md` |
| Subagents, clean context, parallelism, worker packets | `references/subagents-and-parallelism.md` |
| Repeated failures or the 5-attempt fuse | `references/failure-fuse.md` |
| Git branch, worktree, staging, commit, or push questions | `references/git-and-worktree.md` |
| Full-auto mode, auto approvals, high-risk decisions | `references/full-auto-and-risk.md` |
| High-risk changes or second-pass review | `references/clean-context-review.md` |

Bundled prompts:

- `agents/feature-area-worker.md` for normal feature-area implementation workers.
- `agents/fresh-failure-analyzer.md` after the same issue reaches the 5-attempt limit.

## Use This Skill When

Use this skill when the user provides or references:

- a PRD plus task checklist
- a technical design plus implementation tasks
- a `tasks.md`, `todo.md`, issue list, OpenSpec/Speckit task output, or similar execution plan
- a request to implement multiple tasks with TDD or test-driven verification
- a request to use independent subagents, clean context, fresh workers, task claiming, or worker batches
- a request to keep updating the task list during implementation

Do not use this skill when:

- the user still needs requirement exploration, PRD writing, technical design, or task decomposition
- the user asks only for a code review
- the request is a small one-off edit where orchestration would add unnecessary overhead

For small low-risk edits, handle them directly with lightweight verification instead of forcing a worker loop.

## Core Workflow

1. Locate and read the task checklist first, then the PRD and technical docs that justify it.
2. Read required references from the table above.
3. Create a compact implementation brief: scope, source docs, task state, dependencies, acceptance criteria, test/build commands, risky shared contracts, assumptions, and blockers.
4. Create a timestamped run log beside the task checklist, such as `implementation-run-2026-04-26-1530.md`.
5. Classify execution mode: standard or full-auto; record max parallel workers and confirmation rules in the run log.
6. Select the next eligible task batch. Only executable tasks with clear verification, resolved dependencies, bounded write scope, and no required new product/architecture decision can be claimed.
7. Decide whether to handle the batch inline or assign it to a clean-context feature-area worker.
8. Apply TDD-oriented execution: tests first by default for meaningful logic; lightweight verification or documented test skip for very small, low-risk changes.
9. Integrate worker output through main-agent review. Workers recommend status; the main agent decides final status.
10. Update the task checklist and run log after each integrated batch.
11. Commit by verified task batch when git commits are authorized and appropriate. Never push unless the user explicitly asks.
12. Continue until all requested executable tasks are done, remaining tasks are blocked, verification cannot continue, a hard-risk operation requires confirmation, or the user stops the run.

## Default Execution Rules

- Default maximum parallel workers: 2.
- If the user asks for more than 2 parallel workers, present a parallel execution plan and wait for confirmation before launching.
- If the user says full-auto, fully managed, or equivalent, continue without normal confirmation prompts and record auto-approved decisions.
- Even in full-auto mode, do not perform hard-risk operations without explicit authorization: production data deletion, real external payment/message/API calls, destructive migrations, major security/permission semantic changes, public API breaking changes, or large rewrites outside the task scope.
- A task is complete only after implementation, required verification or documented verification exception, main-agent review, task-list update, and run-log update.

## Final Response

Use a short implementation-focused report:

```markdown
## Completed
## Changed
## Verification
## Task List
## Run Log
## Commits
## Blocked / Partial
```

Do not paste the full run log unless the user asks for it. Include paths to the task list, run log, and commits created during this run.
