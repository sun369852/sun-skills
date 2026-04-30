---
name: prd-quality-audit-standards
description: Use this skill when a PRD already exists and the user wants to derive a post-development audit contract or quality audit standard for implementation audit agents, test audit agents, or clean-context reviewers. Trigger for requests to generate audit-agent-readable acceptance criteria, implementation audit contract, test audit contract, PRD-to-audit traceability, layered audit checks, hard fail gates, defect report format, required evidence, machine-readable audit checks, PRD change sync rules, or three-round clean-context review records. Strongly prefer it for prompts like 根据 PRD 生成开发完成后的审核标准/测试审核契约, implementation audit contract, audit-agent-readable acceptance plan, or 三轮 clean-context review. Do not use it for writing a PRD, requirement discovery, technical design, task decomposition, code review, direct test execution, translating QA checklists, or summarizing test reports.
---

# PRD Quality Audit Standards

## Purpose

Turn an existing PRD into a durable post-development audit contract. The primary executor is an implementation audit agent or test audit agent; human QA/testers are secondary readers.

The artifact defines how a future reviewer verifies that completed code satisfies the PRD. It is not a PRD, technical design, task split, implementation plan, or live test execution report.

## Chain Invocation Override

When invoked by `product-delivery-skill-chain` with a downstream invocation envelope, follow the envelope before this skill's default reviewer, parallel, output path, confirmation, or source-priority rules.

The envelope may constrain audit-standards output path, clean-context reviewer authorization, parallel execution, PRD source priority, stop point, and chain status reporting. If the envelope conflicts with this skill's defaults, follow the envelope. If following it would prevent required audit standard generation or safe saving, stop and ask instead of silently weakening the chain contract.

## Use This Skill When

Use this skill when the user provides or references a PRD and asks for:

- quality audit standards, QA standards, acceptance checks, or testing standards
- standards for a post-development implementation audit agent or test audit agent
- three-round clean-context review of audit standards
- PRD-to-audit traceability, hard fail rules, defect reporting format, or machine-readable audit checks
- a saved `quality-audit-standards.md` or equivalent audit artifact

Do not use this skill when the user needs requirement discovery, PRD creation, technical design, task decomposition, code implementation, or direct execution of tests against completed code.

If the PRD is missing, ask one focused question for the PRD file or content. If the PRD is incomplete but usable, continue and mark ambiguous areas as blocked instead of inventing behavior.

## Progressive Loading

Read only the references needed for the current stage:

- Always read `references/prd-coverage-analysis.md` after locating the PRD.
- Read `references/context-and-output.md` when the user provides a project path, supporting technical/task documents, an output path, or asks about split artifacts.
- Always read `references/workflow.md` before drafting, applying the draft admission gate, running clean-context reviews, or merging review findings.
- Read `references/audit-check-rules.md` before creating audit check IDs, priorities, statuses, hard fail rules, defect reporting, retest rules, or machine-readable checks.
- Read `references/clean-context-review.md` before using three clean-context reviewers or inline fallback review passes.
- Always read `references/audit-standards-template.md` before writing the final artifact.
- Always read `references/quality-gate.md` before saving or reporting readiness.

Bundled reviewer prompt:

- `agents/quality-audit-reviewer.md`

When subagents are available and the user asks for subagents, reviewers, independent audit, quality review, clean-context review, or three review rounds, use the reviewer prompt with the clean-context rules in `references/clean-context-review.md`.

## Core Workflow

1. Locate and read the PRD.
2. Load `references/prd-coverage-analysis.md` and extract the verification surface.
3. Load `references/context-and-output.md` if project context, supporting documents, or output path decisions matter.
4. Load `references/workflow.md` and draft the initial audit standards.
5. Load `references/audit-check-rules.md` and ensure the draft uses the required layers, IDs, statuses, evidence rules, hard fail rules, and reporting rules.
6. Apply the draft admission gate from `references/workflow.md`. If the draft fails, rewrite it before review; stop as blocked if it still fails after the allowed rewrites.
7. Load `references/clean-context-review.md` and run three independent clean-context review rounds against the admitted draft.
8. Merge review findings using evidence-first rules from `references/workflow.md`.
9. Load `references/audit-standards-template.md` and write the final artifact.
10. Load `references/quality-gate.md`, patch gaps, save the artifact, and report readiness.

## Required Output Qualities

The final artifact should provide:

- PRD-to-audit traceability
- behavior verification and implementation audit checks
- test execution requirements and static fallback rules
- environment and test data requirements
- required evidence traceable to audit check IDs
- three-round clean-context review record
- defect report format, retest rules, PRD change synchronization rules, final conclusion rules, and hard fail conditions
- machine-readable JSON/YAML appendix or linked auxiliary file

## Final Conversation Response

After saving, report:

- saved file path
- whether subagents or inline fallback were used
- whether three clean-context review rounds completed, were skipped, or were approximated
- number of PRD requirements mapped and any unmapped/blocked areas
- highest-risk audit gates
- whether a machine-readable appendix or auxiliary file was produced
- whether the standards are ready for post-development audit use

Keep the response concise. The saved document is the durable artifact.

## Success Standard

This skill is successful when the saved standards can guide a future implementation/test audit agent without a fresh PRD analysis pass, every identifiable PRD requirement is mapped or explicitly blocked, high-risk requirements have strong gates, three clean-context reviews are recorded or limitations disclosed, and ambiguous PRD content is visible instead of silently resolved.
