# Handoff Inputs

## Collect the Minimum Context

Prefer concrete artifacts over memory:

- source requirement: PRD, technical design, task list, issue, spec, or latest user instruction
- audit contract: `quality-audit-standards.md`, implementation audit contract, test audit contract, or PRD-derived acceptance checklist
- implementation scope: git diff, branch, commit range, changed files, run log, or worker summary
- declared verification: test output, build logs, lint output, manual QA notes, screenshots, or skipped-test rationale
- repository expectations: existing test patterns, contribution docs, CI commands, and nearby code conventions

Do not scan the whole repository by default. Start from the changed files, source docs, and tests that cover the changed behavior.

## Scope Discovery

If no scope is provided, infer it in this order:

1. explicit user-provided files, task IDs, branch, commit, or PR
2. current git diff and untracked files
3. implementation run log or task checklist updated by the development workflow
4. changed files mentioned in the conversation
5. quality audit standards and their referenced source documents, only to define the acceptance surface

Audit standards define what to verify, not what changed. Do not use a broad standards document by itself as the implementation scope unless the user explicitly says the whole standards surface is in scope.

State the inference in the review assumptions. If multiple plausible scopes exist, ask one focused question instead of reviewing the wrong work.

## Source of Truth Priority

Use the newest explicit user instruction first, then the quality audit standards artifact when present, then the task checklist, then technical design, then PRD/spec. If these conflict:

- do not resolve product meaning silently
- review implementation against the highest-priority explicit source
- list lower-priority conflicts as open questions or risks

## Audit Standards Discovery

Look for audit standards only when the user asks for standards-based review, the handoff/run log references one, or a likely standards file is near the source artifacts. Use this order:

1. explicit user-provided path
2. paths mentioned in task lists, run logs, PRD, technical design, or previous conversation
3. files beside the PRD or task list named `quality-audit-standards.md`, `audit-standards.md`, `implementation-audit-contract.md`, or `test-audit-contract.md`
4. matching files in the current project/workspace root

If the user explicitly requested standards-based review and no standards artifact can be found, ask one focused question or mark the review `Blocked`. If the user did not request standards-based review, continue with PRD, tasks, design, diff, and verification evidence.

## Handoff Readiness Check

Before deep review, confirm:

- there is a bounded change set
- there is at least one source artifact or acceptance expectation
- if standards-based review was requested, the standards artifact is available or its absence is recorded as a blocker
- the repository can be inspected locally
- required verification commands are known or can be inferred

If one item is missing but the rest are available, continue with a visible assumption. If the missing item would make the review meaningless, mark the review `Blocked`.
