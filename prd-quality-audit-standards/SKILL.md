---
name: prd-quality-audit-standards
description: Use this skill when a PRD already exists and the user wants a quality audit, QA review standard, test acceptance standard, testing checklist, audit criteria, or post-development verification standard derived from the PRD. Strongly prefer this skill for prompts such as 根据 PRD 生成测试标准, 质量审核子代理, 代码开发完成后审核, PRD 验收标准, QA checklist, audit test standards, acceptance test plan from PRD, or build review criteria before implementation. Do not use for writing the PRD itself, generating technical design, decomposing implementation tasks, or directly testing completed code.
---

# PRD Quality Audit Standards

## Purpose

Turn an existing PRD into a durable quality audit standards document that can be used after code development to review whether the implementation satisfies the product requirement.

The output is not a test execution report and not an implementation task list. It is a verification contract: traceable PRD coverage, acceptance tests, audit gates, required evidence, risk-focused checks, and pass/fail standards that a future reviewer or testing agent can apply once the code is complete.

Use a quality audit reviewer perspective to reduce blind spots. When subagents are available and the user asks for a subagent/reviewer/audit process, delegate an independent quality audit pass. If subagents are unavailable, perform the same review inline and label it as an inline quality audit pass.

## When to Use

Use this skill when:

- the user provides a PRD path or pasted PRD content and asks for testing standards, QA standards, quality gates, audit criteria, or acceptance checks
- the user wants a quality audit subagent to derive review standards from PRD content
- development has not started yet, but the user wants a future post-implementation test/audit standard
- the user wants PRD requirements converted into a traceability matrix and concrete pass/fail checks
- the user wants the resulting audit standard saved as a Markdown artifact
- the PRD was produced by a requirement/PRD workflow and is ready for downstream validation planning

Do not use this skill when:

- the requirement is still vague and needs discovery or PRD creation
- the user asks for frontend/backend technical design instead of QA/audit standards
- the user asks to split implementation tasks or generate tickets
- the user asks to run tests against completed code; use ordinary test/review workflow instead, optionally referencing the saved standards
- there is no PRD and not enough product requirement content to analyze

If the PRD is missing, ask one focused question for the PRD file or content. If the PRD is incomplete but still usable, continue and record assumptions, open questions, and blocked audit areas instead of inventing product behavior.

## Inputs

Expected input can be any of:

- a PRD file path
- pasted PRD content
- a PRD plus technical design, task archive, or project path for context
- an explicit output path for the audit standards document
- a request such as "让质量审核子代理基于 PRD 生成开发完成后的测试审核标准"

If a file path is provided, read the full PRD before analysis. If the user also provides a technical design or task archive, use it only as supporting context. The PRD remains the source of truth for acceptance behavior.

Project code inspection is optional and should be narrow. Inspect project context only when the user asks for compatibility with an existing codebase or the PRD depends on current routes, APIs, schemas, permissions, test framework, or release conventions.

## Output Path

If the user provides an output path, use it unless it would overwrite an unrelated file.

If no output path is provided, choose a conservative default:

1. If the PRD lives in a feature/spec folder, save beside it as `quality-audit-standards.md`.
2. If there is an existing local convention such as `docs/qa/`, `specs/<feature>/`, or `quality/`, follow it.
3. If the PRD was pasted, create `quality-audit/<yyyy-mm-dd>-<feature-slug>-quality-audit-standards.md` in the current workspace or project root.

Never silently overwrite an existing audit standards file. If the target exists and the user did not ask to update it, create a versioned filename such as `quality-audit-standards-<yyyy-mm-dd>.md`.

## Reference Loading

Read only what is needed:

- Always read `references/prd-coverage-analysis.md` after locating the PRD.
- Always read `references/audit-standards-template.md` before drafting the final artifact.
- Read `references/quality-gate.md` before saving or reporting that the standards are ready.

Bundled reviewer prompt:

- `agents/quality-audit-reviewer.md`

When subagents are available and the user request authorizes a quality audit subagent, read the reviewer prompt and use it as the basis for the subagent instructions. Add only task-specific context: PRD content/path, supporting design/task documents, bounded project findings if any, assumptions, open questions, and requested output path.

## Workflow

1. Locate and read the PRD.
2. Load `references/prd-coverage-analysis.md` and extract requirements, actors, workflows, states, permissions, data behavior, integrations, edge cases, non-functional requirements, acceptance criteria, and unresolved product questions.
3. Decide whether supporting context is needed:
   - read a technical design or task archive only if the user provides it or the PRD references implementation constraints
   - inspect project files only when existing-project compatibility affects test standards
4. Run the quality audit review:
   - With subagents: ask the quality audit reviewer for independent coverage gaps, test standards, risk gates, evidence requirements, and blocked questions.
   - Without subagents: perform the same audit inline and clearly separate "Quality audit reviewer findings" from the final synthesis.
5. Build a traceability matrix mapping each PRD requirement to one or more audit checks.
6. Load `references/audit-standards-template.md` and draft the standards document.
7. Classify checks by type: functional, UI/UX, API/data, permissions/security, state/lifecycle, error handling, integration, observability, performance, accessibility, migration/backward compatibility, regression, and release readiness.
8. For each check, define pass/fail criteria, required evidence, test data or scenario setup, and whether it is manual, automated, or review-only.
9. Mark blocked checks where the PRD is ambiguous. Do not convert unresolved product questions into fake standards.
10. Load `references/quality-gate.md`, self-review the draft, patch gaps, and save the document.

## Subagent Rules

Use a quality audit subagent when the host environment supports delegation and the user asks for subagents, reviewers, independent audit, or quality review. The main agent remains responsible for the saved artifact.

Good quality audit subagent prompts:

- ask for concise findings, not a full final document unless explicitly useful
- require traceability to PRD sections or quoted requirement labels
- ask for missing/ambiguous requirements that block testing
- ask for high-risk audit gates and evidence requirements
- ask for automation candidates and manual review areas

Avoid asking the subagent to invent product behavior, implementation details, or code tests that are not grounded in the PRD. If the subagent returns broad advice, distill it into concrete standards and preserve uncertainty.

For high-risk PRDs, consider a clean second audit pass when the user asks for it or when the PRD involves payments, permissions, sensitive data, audit logs, destructive operations, data migration, external integrations, or compliance. Give the second pass only the PRD and the draft standards, not the first audit transcript.

## Final Artifact Requirements

The saved Markdown document should include:

- source PRD path/content summary and supporting context used
- scope and non-scope of the audit standard
- PRD-to-audit traceability matrix
- functional acceptance checks with pass/fail standards
- state, data, permissions, and error-condition checks when relevant
- UI/UX and accessibility checks when relevant
- integration, migration, observability, performance, and release checks when relevant
- regression checks and risks to retest
- evidence requirements for future code review/test review
- blocked checks, assumptions, and open product questions
- final readiness gate explaining whether the standards are ready to use after implementation

## Final Conversation Response

After saving, report:

- the saved file path
- whether the quality audit pass used a subagent or inline review
- the number of PRD requirements mapped and any unmapped/blocked areas
- the highest-risk audit gates
- whether the standards are ready for post-development testing review

Keep the response concise. The saved document is the durable artifact.

## Success Standard

This skill is successful when:

- the audit standards document is saved to disk
- every identifiable PRD requirement is mapped to one or more audit checks or explicitly marked blocked/unmapped
- pass/fail criteria are concrete enough for a future reviewer to apply
- required evidence, test data, and execution mode are clear
- high-risk areas receive stronger gates instead of generic checklist items
- assumptions and open questions are visible
- the artifact can guide post-development code/testing review without requiring a fresh PRD analysis pass
