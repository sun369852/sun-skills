---
name: implementation-review-handoff
description: Use this skill when development work is complete or mostly complete and the user wants a structured review, acceptance check, handoff audit, post-implementation verification, release-readiness assessment, or a default development-review loop. Trigger for prompts such as "开发完成了帮我审核", "承接开发完成的工作", "review the implemented tasks", "验收实现结果", "检查这次改动是否符合 PRD/tasks/technical design", "按 quality-audit-standards 审核实现", "按第三方验收标准审核", "handoff from implementation", "code review after agent implementation", or requests to verify completed coding work against PRD, technical design, task list, quality audit standards, third-party acceptance standards, tests, git diff, run log, or acceptance criteria. Do not use for writing PRDs, generating technical designs, task decomposition, or doing the original implementation.
---

# Implementation Review Handoff

## Purpose

Take over after implementation and decide whether the delivered work is acceptable. This skill reviews the actual change set against the source requirements, third-party acceptance standards, quality audit standards, task list, technical design, implementation run log, tests, and repository conventions. It produces actionable findings, traceable verification evidence, and a clear pass/fix-needed/block decision.

The skill is intentionally downstream of development. Do not restart planning or silently patch code inline. If implementation defects are found, create a developer fix packet and continue the default development-review loop through the development skill when the environment supports it. Escalate to the user for upstream artifact problems, product decisions, risk acceptance, scope expansion, dangerous operations, or loop exhaustion. When a chain envelope sets `High-risk operations: no-confirmation`, do not ask only for risk acceptance; mark the review `Fix needed` or `Blocked` and record the unaccepted risk instead.

## Chain Invocation Override

When invoked by `product-delivery-skill-chain` with a downstream invocation envelope, follow the envelope before this skill's default reviewer, review-fix loop, output path, confirmation, or source-priority rules.

The envelope may constrain review report path, reviewer/subagent authorization, review-fix loop policy, high-risk operations policy, audit standards priority, source artifact priority, reviewed scope, and stop point. If the envelope conflicts with this skill's defaults, follow the envelope. If following it would prevent a trustworthy review or safe repair handoff, stop and ask instead of silently weakening the chain contract.

## Assumptions to State

Before reviewing, state the working assumptions:

- what artifact is the source of truth, such as PRD, technical design, tasks, issue, or user prompt
- whether a third-party standard, `quality-audit-standards.md`, or equivalent audit contract exists and should be the primary acceptance standard
- what implementation scope is being reviewed, such as current git diff, branch, commit range, or named files
- whether a development-review loop is already in progress, and which round this is
- what verification commands are safe and available to run

If the source of truth or change scope is missing and cannot be inferred from local context, ask one focused blocking question. If it can be inferred from a task list, run log, branch, or git diff, proceed and record the inference.

## Reference Loading

Read only what the current review needs:

| Situation | Read |
| --- | --- |
| Every invocation | `references/handoff-inputs.md`, `references/review-workflow.md`, `references/status-and-findings.md`, `references/final-report.md` |
| A quality audit standards artifact exists or the user references audit standards | `references/audit-standards-alignment.md`, then `references/audit-standards-execution.md` |
| Verification, tests, build, lint, reproducibility | `references/verification-and-evidence.md` |
| Findings require implementation repair, re-review, or loop recording | `references/review-fix-loop.md` |
| Release readiness, risky changes, user-facing behavior, migrations, auth, payments, data loss | `references/risk-gates.md` |
| User asks for subagents/reviewers or clean-context review | `agents/implementation-reviewer.md` |

Audit standards discovery lives in `references/handoff-inputs.md`. Use standards mode when a third-party standard, `quality-audit-standards.md`, or equivalent audit contract is present or requested. In standards mode, execute the contract strictly: audit check IDs, hard fail gates, evidence requirements, defect format, and standards conclusion come first. If no standards artifact exists, use basic review mode against PRD/tasks/design/diff and tell the user that generating `quality-audit-standards.md` first would make the audit stronger. `quality-audit-standards.md` is normally produced by `prd-quality-audit-standards`, but third-party acceptance standards can override it when the user says so.

## Use This Skill When

Use this skill when:

- implementation has been completed by the current agent, another agent, a developer, or a previous run
- this skill is acting as the downstream executor for `quality-audit-standards.md` produced by `prd-quality-audit-standards`
- the user wants acceptance review before marking tasks done, merging, releasing, or handing off
- there is a PRD, technical design, task checklist, OpenSpec/Speckit tasks, run log, commit range, or git diff to validate
- there is a `quality-audit-standards.md`, implementation audit contract, test audit contract, or PRD-derived audit checklist to execute against completed code
- the user asks for bugs, regressions, missed acceptance criteria, missing tests, or release risk
- the user asks a reviewer or subagent to inspect completed work
- implementation defects should be routed back into a development-review loop and re-reviewed after repair

Do not use this skill when:

- the user is asking to implement planned work from scratch
- the user needs requirement exploration, PRD creation, technical design, or task splitting
- the user needs to generate `quality-audit-standards.md` from a PRD
- the request is a normal code review of an unrelated diff without acceptance or handoff context
- the user only wants a quick explanation of code behavior

For a small one-file change, keep the review lightweight: inspect the diff, run the most relevant check, and report findings without creating extra artifacts.

## Core Workflow

1. Identify the source of truth and review scope.
2. Read `references/handoff-inputs.md`, discover applicable audit standards, choose standards mode or basic review mode, and collect only the artifacts needed to compare expected behavior with delivered behavior.
3. If an audit standards artifact exists, read `references/audit-standards-alignment.md` and execute the audit checks as the primary review contract unless newer user instructions override it.
4. Read `references/review-workflow.md` and inspect the implementation from requirements outward: acceptance criteria, behavior, data/contracts, UI/API surface, error states, tests, and maintainability.
5. If verification is required or useful, read `references/verification-and-evidence.md`, choose the smallest meaningful command set, and run it.
6. If the change is high-risk, read `references/risk-gates.md` before deciding pass/fix-needed/block.
7. If implementation defects are found, read `references/review-fix-loop.md` and prepare the developer fix packet. Auto-route to the development skill when supported; otherwise save or output the packet for handoff.
8. If upstream artifacts are deficient, prepare a user decision point instead of auto-returning upstream.
9. Use a clean-context reviewer only when the user explicitly asks for subagents/reviewers, independent review, 二次复核, or clean-context review. The main agent remains responsible for the final conclusion.
10. Produce the final report using `references/final-report.md`; load `references/final-report-template.md` only when writing a full report or saved artifact.

## Review Rules

- Findings lead the response. Order by severity and include file/line references when available.
- A finding must describe a concrete defect, missed requirement, regression risk, or verification gap. Avoid style preferences unless they create real maintenance or behavior risk.
- Findings and evidence should trace to audit check IDs, third-party standard IDs, generated `EXT-*` IDs, task IDs, PRD sections, or code locations.
- Separate confirmed issues from open questions and assumptions.
- Treat failing tests, missing required tests, skipped verification, and unverifiable acceptance criteria as first-class review outcomes.
- Do not patch code inline by default. Route implementation defects to the development skill through a bounded fix packet; only patch inline when the user explicitly asks the current agent to review-and-fix.
- Do not mark work accepted if a blocking requirement is unverified, a critical test fails, or the diff does not match the source of truth.

## Decision Labels

Use one final decision:

- `Pass`: no blocking findings; verification is adequate for the risk.
- `Pass with notes`: no blocking findings, but there are minor risks, cleanup suggestions, or limited verification.
- `Fix needed`: there are concrete defects or missed acceptance criteria, but they are bounded and fixable.
- `Blocked`: the review cannot reach a trustworthy conclusion because source artifacts, scope, environment, or required credentials are missing.

In standards mode, determine the standards-aligned conclusion first, then map it to the internal decision for the development-review loop:

- `Approved` maps to `Pass`
- `Approved with Risks` maps to `Pass with notes`
- `Rejected` maps to `Fix needed`
- `Blocked` maps to `Blocked`

Default max development-review loops: 5. Use `references/review-fix-loop.md` for repair handoff, re-review, loop history, and stop conditions.

## Success Standard

This skill succeeds when:

- the reviewed scope is explicit
- requirements and delivered behavior are compared directly
- PRD-derived audit checks are honored when available, including stable IDs, hard fail gates, and evidence traceability
- findings are actionable and severity-ranked
- verification evidence is recorded, including commands run and failures
- high-risk changes receive stricter gates
- the final decision is clear enough for the user to merge, send back for fixes, or unblock missing context
- implementation defects can be handed to the development skill without re-explaining the review context
