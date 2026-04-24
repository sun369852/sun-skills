---
name: tdd-task-implementation-orchestrator
description: Use this skill when the user wants to start coding from a PRD, task checklist, technical design, architecture document, spec, or implementation plan. This skill orchestrates TDD-driven development with clean-context subagents, feature-area task ownership, task-list updates after completed work, independent task batching, verification gates, and a maximum of 5 repair attempts before handing the stuck issue to a fresh subagent. Trigger for prompts such as "根据 PRD 和任务清单开始开发", "按技术文档 TDD 实现", "use agents to implement tasks", "clean context subagents", "领取下一个任务", "实现 tasks.md", "spec-driven TDD coding", or "从 PRD/技术方案/任务列表进入开发". Do not use for writing the PRD, producing only a technical design, pure code review, or one-off small edits that do not need task orchestration.
---

# TDD Task Implementation Orchestrator

## Purpose

Turn product and engineering planning artifacts into working code through a controlled implementation loop:

1. Read the PRD, task checklist, technical documentation, and current codebase.
2. Identify tasks that can be implemented independently by feature area.
3. Assign one bounded task bundle at a time to a clean-context worker.
4. Drive each task with tests first, implementation second, verification third.
5. Update the task checklist after each completed bundle.
6. Rotate to a new clean-context worker for the next independent bundle.
7. Stop repeated repair loops after 5 attempts and hand the issue to a fresh analyzer/worker.

The main agent remains the orchestrator. It owns task selection, context packaging, integration decisions, verification, and the final report. Workers own only their assigned feature area and write scope.

## Use This Skill When

Use this skill when the user provides or references:

- a PRD plus a task checklist
- a technical design plus implementation tasks
- a `tasks.md`, `todo.md`, issue list, OpenSpec/Speckit task output, or similar implementation plan
- a request to implement multiple tasks with TDD
- a request to use independent subagents, clean context, fresh workers, or task claiming
- a request to keep updating the task list as work completes

Do not use this skill when:

- the user still needs requirement exploration, PRD writing, or technical design generation
- the user asks for a single small bug fix that is faster and safer inline
- the user asks only for a code review
- the task list is too vague to identify verifiable behavior; ask one focused question or create a small clarification list first

## Inputs

Expected inputs can include:

- PRD path or pasted PRD content
- task checklist path, often `tasks.md`
- technical design, architecture, API, database, UI, or testing docs
- repository path
- preferred test command, build command, or package manager
- explicit constraints such as "do not touch backend" or "only finish tasks P0-P3"

If paths are missing, inspect the repository for likely planning files before asking. Search for names such as `prd`, `requirements`, `technical-design`, `design`, `architecture`, `tasks`, `spec`, `plan`, `.speckit`, `.openspec`, and `docs`.

## Operating Principles

- Treat the PRD and technical documentation as the source of truth. If code conflicts with docs, record the conflict and choose the least surprising implementation that preserves existing behavior.
- Keep worker context intentionally small: the task bundle, relevant doc excerpts, discovered project conventions, allowed write scope, verification command, and current task-list state.
- Use feature-area workers, not generic "frontend/backend" splits unless the task naturally requires that. Good feature areas include auth flow, import pipeline, billing state, report export, notification delivery, form validation, or persistence layer.
- Prefer parallel workers only for independent tasks with disjoint write sets. If tasks share files, schemas, migrations, or public contracts, sequence them.
- Update the task checklist only after a task bundle has passing verification or a clear blocked status.
- Do not allow one failure to consume the whole session. Track repeated attempts by issue signature and trigger a fresh-context handoff after 5 failed repair loops.
- Preserve unrelated user changes. Never revert files outside the assigned scope unless the user explicitly asks.

## Required Workflow

### 1. Locate And Read Sources

Read the task checklist first, then the PRD and technical docs that justify those tasks. If the codebase has existing docs for testing, architecture, or contribution patterns, read only the relevant parts.

Create a compact implementation brief:

- product goal and non-goals
- task checklist path and current completion state
- acceptance criteria
- technical constraints and compatibility notes
- expected test/build commands
- risky shared files or contracts
- open questions and assumptions

If the brief exposes a blocking ambiguity, ask one focused question. For non-blocking ambiguity, make a conservative assumption and record it.

### 2. Normalize The Task Checklist

Parse the checklist into task records:

- id or stable label
- title
- feature area
- dependencies
- expected files or modules
- acceptance criteria
- test expectations
- status: `pending`, `in_progress`, `done`, or `blocked`

Do not rewrite the whole task file for style. Make the smallest edits needed to mark status, add notes, or add missing verification references.

### 3. Select The Next Work Batch

Choose the next batch using this priority:

1. Unblocked prerequisite tasks.
2. High-value independent tasks with clear acceptance criteria.
3. Tasks that enable later testing or integration.
4. Smaller tasks when project risk is high or context is uncertain.

A task is independent enough for a separate worker only when:

- it does not require unmerged output from another active worker
- its write scope is disjoint or low-conflict
- its tests can be run in isolation or clearly targeted
- its acceptance criteria can be verified without hidden product decisions

### 4. Prepare A Worker Packet

For each worker, provide a concise packet:

- assigned task ids and exact checklist text
- feature-area responsibility
- allowed write scope and files/modules to avoid
- PRD and technical-doc excerpts relevant to the task
- current project conventions discovered by the orchestrator
- required TDD sequence
- test/build command to run
- expected final response: changed files, tests added/updated, commands run, task status recommendation, blockers

Tell workers they are not alone in the codebase. They must not revert changes made by others and should adapt to existing edits.

Use `agents/feature-area-worker.md` as the default worker prompt. Use `agents/fresh-failure-analyzer.md` when the same issue has already failed 5 repair attempts.

### 5. Test First

Before implementation, write or assign tests that express the documented behavior:

- unit tests for business rules, parsing, validation, reducers, utilities, or service functions
- integration tests for API contracts, persistence behavior, workflows, permissions, or cross-module behavior
- UI/component tests for interactive states and user-visible behavior
- end-to-end tests only when acceptance criteria require real workflow coverage or no lower-level seam can verify the behavior

Run the targeted test command and confirm the new test fails for the expected reason when practical. If the existing test framework cannot run yet, record the blocker and still write tests in the local project style.

### 6. Implement And Verify

Implement the smallest production change that satisfies the tests and documented acceptance criteria. Then run:

- the targeted tests for the task
- any adjacent tests affected by shared contracts
- lint/typecheck/build when the touched area normally requires it or when the change is broad

After implementation, improve the tests if they only assert implementation details, miss an important acceptance criterion, or fail to cover a regression risk discovered during coding.

### 7. Handle Failures Without Loops

Track failures by issue signature, such as:

- failing test name plus error message
- build/typecheck error and file
- runtime exception and stack root
- acceptance criterion not met

For each issue signature:

1. Attempt a focused fix.
2. Re-run the smallest meaningful verification.
3. Increment the issue attempt count only when the same signature remains unresolved.
4. Stop after 5 failed attempts.

After 5 failed attempts, stop local repair and create a fresh-context handoff:

- original task packet
- current diff summary
- exact failing commands and errors
- fixes already tried
- suspected root causes, clearly labeled as hypotheses
- files that must not be reverted

Send that packet to a new clean-context analyzer/worker using `agents/fresh-failure-analyzer.md`, or perform the same clean-room analysis inline if subagents are unavailable.

### 8. Integrate Worker Results

When a worker finishes:

- review its changed files and ensure they match the assigned scope
- run or inspect the verification it reported
- resolve integration conflicts with other completed work
- avoid accepting broad rewrites that were not necessary for the task
- update the task checklist with completed, blocked, or follow-up status

Only mark a task `done` when verification passes or the user explicitly accepts a partial result. If a task is blocked, write a short blocker note with the missing decision or failing command.

### 9. Continue The Loop

After updating the checklist, start the next independent task bundle with a new clean-context worker. Do not keep extending the same worker across unrelated feature areas. The reset matters because it reduces stale assumptions and keeps each task's reasoning local.

Continue until:

- all requested tasks are done
- remaining tasks are blocked on user/product decisions
- verification cannot proceed because of missing dependencies or environment constraints
- the user asks to stop

## Task Checklist Update Format

Respect the existing checklist style. If it uses Markdown checkboxes, prefer:

```markdown
- [x] T012 Add validation tests for invite expiration
  - Verification: `npm test -- invite-expiration`
```

For blocked tasks:

```markdown
- [ ] T013 Enforce organization-level quota
  - Blocked: PRD does not define whether owners can override quota.
```

If the checklist has a status table, update only the status, verification, and notes columns.

## Subagent Guidance

Use subagents only when the active environment and system instructions permit delegation. If delegation is unavailable, simulate the same boundaries inline by working on one feature area at a time and clearing assumptions between batches.

When subagents are available:

- use one worker per independent feature-area bundle
- give each worker a disjoint write scope
- do not give workers the full conversation transcript unless it is necessary
- do not ask multiple workers to edit the same files in parallel
- prefer worker implementation tasks over read-only exploration when the assignment is bounded
- wait for a worker only when its result blocks the orchestrator's next step

## Final Response

Report:

- tasks completed and checklist path updated
- key files changed
- tests added or updated
- verification commands and results
- blocked tasks and the exact reason
- any issue that hit the 5-attempt limit and was handed to a fresh context

Keep the final summary short and implementation-focused.

