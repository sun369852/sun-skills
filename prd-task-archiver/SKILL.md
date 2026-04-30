---
name: prd-task-archiver
description: Use this skill after a PRD already exists and the user wants to split it into implementation tasks, work items, milestones, or a tasks.md file and archive the result. Strongly prefer this skill whenever the user says PRD 已有, 基于 PRD 拆任务, 任务拆分, 生成 tasks.md, 落任务文件, 任务归档, 开发计划归档, implementation plan from PRD, or asks to turn an existing PRD into actionable frontend/backend/test/devops tasks saved to disk. Also use it when a technical design should become tasks and a linked PRD is available; the PRD remains the source of truth and the design is an implementation constraint. Do not use for initial requirement clarification or PRD generation.
---

# PRD Task Archiver

## Overview

Use this skill when the PRD is already available and the next job is to turn it into a durable implementation task archive.

The goal is not to rewrite the PRD or start coding. The goal is to read the PRD carefully, inspect enough project context when relevant, decompose the work into actionable tasks with dependencies and acceptance checks, then save the result to a clear Markdown file that future implementation agents or engineers can follow.

Core rule: preserve the PRD as the source of truth, make uncertainty visible, and save a task archive only after the task list is internally consistent and traceable back to PRD sections.

This skill sits after the requirement and PRD workflow. If the source PRD is missing, too vague, or still deciding product semantics, do not patch the gap by inventing tasks. Ask for the PRD or suggest returning to requirement exploration / PRD review before task archiving.

## Chain Invocation Override

When invoked by `product-delivery-skill-chain` with a downstream invocation envelope, follow the envelope before this skill's default subagent, output path, confirmation, or source-priority rules.

The envelope may constrain task archive output path, subagent/reviewer authorization, PRD and technical design source priority, stop point, and chain status reporting. If the envelope conflicts with this skill's defaults, follow the envelope. If following it would prevent required task coverage review or safe saving, stop and ask instead of silently weakening the chain contract.

## When to Use

Use this skill when:
- the user provides a PRD file path and asks for task breakdown
- the user says an existing PRD should be split into tasks, tickets, milestones, or phases
- the user wants a `tasks.md`, implementation plan, delivery plan, or development task archive generated from a PRD
- the user wants frontend, backend, QA, data, integration, migration, or release tasks derived from product requirements
- the user wants the resulting task split written to a file for archival or later execution
- the PRD was produced by `prompt-to-prd-review` and is ready for implementation planning
- the user provides a technical design and a linked PRD, and wants implementation tasks derived from the PRD while respecting the design

Do not use this skill when:
- the requirement is still vague and needs exploration first
- the user needs a PRD generated or reviewed instead of task decomposition
- the user asks for direct code implementation
- the user only wants a high-level planning opinion without a saved task artifact
- the source document is only a technical design and no linked PRD path or PRD content is available

If no PRD path or PRD content is available, ask one focused question for the PRD location or content. Do not invent requirements.

## Inputs

Expected input can be any of:
- a PRD file path
- pasted PRD content
- a project path plus a PRD path
- a technical design path plus linked PRD path or content
- an existing PRD plus an explicit output path
- a request such as "基于当前 PRD 拆任务并落盘"

If the user gives a file path, read it completely before producing tasks.

When a technical design is provided, use it as an implementation constraint for architecture, API/data contracts, migration, UI structure, and verification strategy. Do not let the technical design override PRD product behavior. If the technical design and PRD conflict on product behavior, use the PRD and surface the conflict.

Choose the output path with this priority order:

1. Use the explicit output path requested by the user.
2. If the user is updating an existing task archive, write the updated archive to that archive path unless the user asks for a separate copy.
3. If the PRD lives in a feature/spec folder, prefer a sibling `tasks.md` when that matches local convention.
4. Follow existing project conventions such as `specs/<feature>/tasks.md`, `docs/tasks/`, or `prd/tasks/`.
5. Otherwise create `tasks/<yyyy-mm-dd>-<feature-slug>-tasks.md` in the current workspace or project root.

Never overwrite an existing task archive silently. If the target file exists, either update it only when the user asked for an update, or create a versioned filename such as `<feature-slug>-tasks-v2.md`.

## Reference Loading

Read only the reference files needed for the current request:

- Read `references/error-handling.md` whenever a path is missing, unreadable, malformed, ambiguous, or points to a non-PRD source.
- Always read `references/source-prd-analysis.md` after locating the PRD.
- Read `references/existing-project-context.md` only when this is an existing project iteration or the user provides a project path/repository.
- Always read `references/task-decomposition.md` before drafting tasks.
- Always read `references/archive-template.md` before writing the final task archive.
- Read `references/quality-review-and-updates.md` before saving, and also when updating an existing task archive.

Do not bulk-load all references by default. The skill is intentionally split so routine tasks use only the smallest useful context.

## Workflow

1. Locate and read the PRD.
2. If the PRD path/content or project path cannot be used safely, load `references/error-handling.md` and resolve the blocker before drafting.
3. Load `references/source-prd-analysis.md` and extract the source boundary.
4. If a technical design is provided, read it after the PRD and extract implementation constraints without changing PRD semantics.
5. Decide whether this is a new feature or existing project iteration.
6. If existing project context matters, load `references/existing-project-context.md` and inspect only the relevant project files.
7. Load `references/task-decomposition.md`; analyze functional blocks and coupling first, then draft ready tasks, blocked tasks, dependencies, priority, risk, deliverables, validation, and coverage inside those blocks.
8. Load `references/archive-template.md` and format the Markdown archive.
9. Load `references/quality-review-and-updates.md`, self-review the archive, and patch gaps before saving.
10. Save the archive without silently overwriting unrelated existing files.

## Subagent Use

Use subagents only when the host environment supports them and the user request or environment policy authorizes delegation. Subagents are optional; the skill must still work inline.

Good subagent uses:
- project-context scout: inspect routes, APIs, schemas, tests, and local task conventions for an existing project
- task-coverage reviewer: compare the draft task archive against the PRD and identify missing, unmapped, or invented work
- frontend/backend reviewer: review task boundaries for UI/API/domain compatibility on large existing-project iterations

Consider subagents when one or more of these signals is present:
- the PRD has more than 10 functional requirements or acceptance criteria
- the existing-project iteration touches at least three major areas, such as frontend, backend, data/migration, permissions, integrations, or release
- the task archive is likely to exceed 15 tasks
- an existing task archive already has more than 10 tasks or mixed `done`, `in_progress`, and `blocked` statuses
- the PRD includes high-risk compatibility, migration, permission, payment, audit, or integration behavior

Avoid subagents for small PRDs, greenfield work with no repository context, or tasks where waiting for a delegate would cost more context than it saves.

Keep delegated prompts narrow. Ask subagents for concise findings and paths, not full rewritten task archives. The main flow owns the final archive.

If subagents are unavailable, fail, time out, or return broad rewrites instead of concise findings, continue inline. Record in the final response if an independent review was skipped or could not be completed and note any residual review risk.

## Output in Conversation

After saving, report:
- the saved file path
- the number of tasks plus major functional block and area distribution
- any blocked tasks or open PRD questions
- the highest-risk dependency or sequencing concern
- whether any PRD items were unmapped or any derived technical enablement tasks were added
- for updates, a change summary with counts of preserved, added, changed, skipped, and newly blocked tasks
- explicitly state that no code implementation was started

Keep the response concise. The task archive is the durable artifact.

## Success Standard

This skill is successful when:
- the task archive is saved to disk
- tasks are actionable, sequenced, and traceable to the PRD
- ready work, blocked work, priority, risk, deliverables, and validation are explicit
- major frontend, backend, QA, data, integration, release, and documentation work is covered when relevant
- assumptions and open questions are visible
- unmapped PRD items and derived technical enablement tasks are clearly labeled
- the output can be handed to implementation agents or engineers without requiring a fresh planning pass
