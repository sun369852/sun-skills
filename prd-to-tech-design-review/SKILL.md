---
name: prd-to-tech-design-review
description: Use this skill when a PRD already exists and the user wants frontend and backend subagents/reviewers to collaborate, discuss the PRD, resolve implementation concerns, and generate a technical design document. Strongly prefer this skill for prompts such as 基于已有 PRD 生成技术文档, 从 PRD 出技术方案, 前端后端子代理协同评审, frontend/backend agents discuss PRD, technical design from PRD, API/data/UI design from PRD, or PRD 转技术设计. Do not use for creating the PRD itself or for direct coding implementation.
---

# PRD to Tech Design Review

## Purpose

Turn an existing PRD into a durable technical design document by coordinating frontend and backend perspectives. The output should be implementation-ready enough for later task splitting, but it is not a task list and it is not code.

The core idea is a mediated collaboration loop:

1. Read the PRD as the product source of truth.
2. Have frontend and backend perspectives analyze it independently.
3. Exchange their findings so each side can react to the other's constraints.
4. Resolve conflicts, preserve open questions, and document assumptions.
5. Save a technical design document that covers UI, API, data, behavior, validation, risks, and verification.

## Chain Invocation Override

When invoked by `product-delivery-skill-chain` with a downstream invocation envelope, follow the envelope before this skill's default subagent, parallel, output path, confirmation, or source-priority rules.

The envelope may constrain technical-design output path, frontend/backend reviewer authorization, parallel execution, PRD source priority, stop point, and chain status reporting. If the envelope conflicts with this skill's defaults, follow the envelope. If following it would prevent required design review or safe saving, stop and ask instead of silently weakening the chain contract.

## When to Use

Use this skill when:

- the user provides a PRD path or pasted PRD content and asks for a technical document
- the user asks for frontend/backend agents, reviewers, or subagents to discuss a PRD
- the user wants API contracts, data models, UI architecture, and implementation constraints derived from a PRD
- the user needs a design artifact before task decomposition or coding
- the PRD was produced by a requirement or PRD workflow and is ready for engineering analysis

Do not use this skill when:

- the user still needs requirement exploration or PRD creation
- the user asks only for implementation tasks, tickets, or milestones
- the user asks for direct code changes
- no PRD is available and the user has not provided enough product requirements to analyze

If the PRD is missing, ask one focused question for the PRD file or content. If the PRD has non-blocking ambiguity, continue and record assumptions/open questions instead of inventing product decisions.

## Inputs

Expected input can be any of:

- a PRD file path
- pasted PRD content
- a project path plus a PRD path
- an existing PRD plus an explicit output path
- a request such as "让前端后端子代理基于这个 PRD 协同生成技术文档"

If a file path is provided, read the full PRD before analysis. If a project path is also provided, inspect only the project areas needed to make the design compatible with existing architecture: routes/pages, API handlers, schemas/models, auth, state management, tests, and existing docs conventions.

## Output Path

If the user provides an output path, use it unless it would overwrite an unrelated file.

If no output path is provided, choose a conservative default:

- save beside the PRD as `<prd-directory>/technical-design.md`
- if the PRD was pasted instead of read from a file, save `technical-design/<yyyy-mm-dd>-<feature-slug>-technical-design.md` in the current workspace or project root

Never silently overwrite an existing technical design. If the target exists and the user did not ask to update it, append the current date: `technical-design-<yyyy-mm-dd>.md`. If that also exists, add a numeric suffix.

## Reference Loading

Read only what is needed:

- Always read `references/prd-analysis.md` after locating the PRD.
- Read `references/project-context-inspection.md` when the user provides a project path, the PRD is for an existing-project iteration, or compatibility with current implementation matters.
- Always read `references/collaboration-workflow.md` before using frontend/backend reviewers or doing the inline fallback.
- Always read `references/technical-doc-template.md` before drafting the final document.
- Read `references/quality-gate.md` before saving the document.

Bundled reviewer prompts:

- `agents/frontend-tech-reviewer.md`
- `agents/backend-tech-reviewer.md`
- `agents/second-pass-tech-reviewer.md`

When subagents are available and the user request calls for frontend/backend agents, read the matching reviewer prompt and use it as the basis for each subagent's instructions. Add only task-specific context: PRD content/path, project path, relevant project findings, current assumptions, open questions, and requested output path.

Use the second-pass reviewer only when the user asks for a second review, clean-context review, 二次复核, 清空上下文再看, or when the PRD is high-risk and the first review exposes unresolved conflicts or many assumptions. The second-pass reviewer should not see the first-round discussion transcript. Give it only the original PRD, necessary project-context summary, and the technical design draft.

## Workflow

1. Locate and read the PRD.
2. Load `references/prd-analysis.md` and extract scope, actors, flows, business rules, states, permissions, data needs, integrations, acceptance criteria, and unresolved product questions.
3. Decide whether existing project context is required. If yes, load `references/project-context-inspection.md` and inspect a bounded slice of the repository.
4. Load `references/collaboration-workflow.md`.
5. Run the frontend/backend collaboration:
   - With subagents: ask the frontend reviewer and backend reviewer for independent analysis, then run one exchange round where each side responds to the other's findings.
   - Without subagents: perform the same two-perspective analysis inline and clearly separate frontend, backend, and mediation notes.
6. Build a shared decision log with agreements, conflicts, resolved decisions, assumptions, and blocking questions.
7. Load `references/technical-doc-template.md` and draft the technical design.
8. If second-pass review is requested or warranted, run `agents/second-pass-tech-reviewer.md` against the PRD, project-context summary, and draft. Integrate required changes or record why they remain open.
9. Load `references/quality-gate.md`, self-review the draft, and patch gaps before saving.
10. Save the document and report the path, key decisions, unresolved questions, and any high-risk assumptions.

## Subagent Collaboration Rules

Use subagents only when the environment supports them and the current user request authorizes delegation through terms such as subagent, agent, reviewer, 协同, 前端后端复核, or equivalent wording. Keep the main agent responsible for the final document.

Good subagent prompts are narrow:

- ask each reviewer to analyze the PRD from their discipline
- ask for risks, missing details, API/data/UI expectations, and decisions needed
- ask for concise Markdown findings, not a full final document
- provide the counterpart's summary in the exchange round and ask for reactions, amendments, and conflict resolution proposals

Avoid letting both subagents independently write competing final technical documents. The final design should be mediated and consistent.

## Optional Second-Pass Review

Use a clean-context second-pass review for complex or risky designs, not for every routine PRD. It helps catch omissions that the first collaboration round may normalize.

Trigger it when:

- the user explicitly asks for second review, clean-context review, 二次复核, or 清空上下文再看
- the PRD spans multiple clients, services, or integrations
- the PRD involves payments, permissions, audit, sensitive data, migration, or irreversible operations
- the first collaboration round leaves unresolved API/data/state conflicts
- the quality gate finds low coverage, too many assumptions, or blocking questions

Second-pass input should be limited to:

- original PRD
- compact project-context summary and inspected file list, if any
- technical design draft

Do not include the first-round frontend/backend discussion transcript. The point is to reduce anchoring. The main agent remains responsible for integrating second-pass feedback into the final document.

## Final Conversation Response

After saving, report:

- saved file path
- whether frontend/backend collaboration was done through subagents or inline
- main technical decisions captured
- blocking questions or assumptions that remain
- whether the design is ready for task decomposition

Keep the response concise. The saved document is the durable artifact.

## Success Standard

This skill is successful when:

- the PRD remains the source of truth and no product behavior is invented silently
- frontend and backend concerns are both represented and reconciled
- API contracts, data model, UI/state behavior, permissions, errors, observability, and validation strategy are explicit when relevant
- open questions and assumptions are visible
- the final technical design is saved to disk
- the document can be handed to task planning or implementation agents without requiring a fresh design pass
