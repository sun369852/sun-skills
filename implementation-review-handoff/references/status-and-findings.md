# Status And Findings

Use this reference when assigning check status, overall decision, finding category, or severity.

## Status Layers

Use two status layers:

- Check status: `Pass`, `Fail`, `Blocked`, `Not Run`, `Not Applicable`, or downstream-only `Out of Scope`.
- Overall decision: `Pass`, `Pass with notes`, `Fix needed`, or `Blocked`.

`Out of Scope` means the check may apply to the full feature or PRD but is outside this implementation review. `Not Applicable` means the check does not apply to this project or implementation at all. Do not use either to hide a completed task that lacks implementation.

## Finding Categories

Classify findings so the next route is clear:

- `Implementation defect`: delivered code does not satisfy an in-scope requirement or check.
- `Verification gap`: required evidence, test execution, environment, or reproduction path is missing.
- `Delivery topology gap`: an MVP-required runtime surface from the PRD, technical design, or topology contract is missing, not started, failed, blocked, or unverified.
- `Standards gap`: the audit standard is incomplete, lacks IDs, cannot be executed, or conflicts internally.
- `Requirement/design conflict`: PRD, technical design, task list, third-party standard, or PRD-derived standard disagree.
- `Product decision needed`: correctness depends on a business/product decision the reviewer cannot make.

Only implementation defects and implementation-scoped verification gaps should enter the development-review loop automatically. Upstream artifact problems require a user decision.

## Defect Report Format

If the selected audit standards define a defect report format, use that format for failed checks. Otherwise use the default finding shape from `references/final-report.md`.

Standards-derived defect reports should preserve these fields when available:

- defect ID
- audit check ID
- PRD trace
- failure summary
- expected result
- actual result
- reproduction steps or review method
- evidence references
- affected files, APIs, logs, database records, or UI paths
- impact scope
- suggested severity
- release blocking status
- recommended fix direction
- retest scope

If a conversation response needs to stay short, summarize the defect but keep the saved report or developer fix packet traceable to the standards-defined fields.

## Severity

Use this scale:

- `P0`: data loss, security break, crash on core path, production-blocking release risk
- `P1`: missed acceptance criterion, broken important workflow, failing required test, incompatible API/data contract
- `P2`: edge-case bug, incomplete verification for meaningful risk, maintainability issue likely to cause defects
- `P3`: minor cleanup, clarity issue, weak test naming, low-risk follow-up

When a quality audit standards artifact uses `Blocker`, `High`, `Medium`, or `Low`, map them to review severity as:

- `Blocker` -> `P0` unless the impact is clearly bounded to `P1`
- `High` -> `P1`
- `Medium` -> `P2`
- `Low` -> `P3`

Prefer fewer, stronger findings. A review with no findings is acceptable if the evidence supports it.
