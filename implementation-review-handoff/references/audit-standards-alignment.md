# Audit Standards Alignment

Use this reference when a third-party acceptance standard, `quality-audit-standards.md`, implementation audit contract, test audit contract, or PRD-derived audit checklist exists.

## Role of the Standards

Treat the selected standards artifact as the primary review contract because it translates requirements into executable audit checks. Do not recreate the standards during implementation review. Execute, inspect, and report against them.

`quality-audit-standards.md` is normally the output of `prd-quality-audit-standards`. Third-party standards, such as customer acceptance checklists, QA standards, compliance checklists, or vendor test plans, are also valid review contracts.

Source priority:

1. newest explicit user instruction
2. user-specified third-party acceptance standard
3. `quality-audit-standards.md` or other PRD-derived audit contract
4. task checklist and implementation run log
5. technical design
6. PRD/spec

If standards conflict with newer user instructions, follow the newer instruction and record the conflict. If third-party standards conflict with PRD-derived standards and the user did not name a priority, mark a `Requirement/design conflict`, create a user decision point, and block only the affected core checks. If the conflict is outside the current implementation scope, continue and record residual risk.

## Execution Mode

When an audit standards artifact exists or the user asks for standards-based review, run in standards mode:

1. Parse the audit checks and their priorities, modes, required evidence, execution requirements, statuses, and hard fail conditions.
2. Limit execution to checks that are in the current implementation scope; mark the rest `Out of Scope` with a reason.
3. Verify each in-scope check by behavior, implementation review, command execution, or allowed fallback.
4. Attach evidence to the relevant check ID.
5. Apply hard fail conditions before assigning the final conclusion.
6. Derive the standards conclusion first, then map it to the internal skill decision.

If no audit standards artifact exists, this reference does not apply. Use basic review mode and note that a PRD-derived `quality-audit-standards.md` would provide stronger traceability and gates.

For parsing, check IDs, required evidence, hard fails, machine-readable appendices, and three-round review records, read `references/audit-standards-execution.md`.

## Status Rules

Use the standards' statuses when reporting each check:

- `Pass`
- `Fail`
- `Blocked`
- `Not Run`
- `Not Applicable`

Downstream implementation review may also use `Out of Scope` for checks that belong to the full standards surface but not to this implementation scope. `Out of Scope` is not the same as `Not Applicable`.

`Blocked` and `Not Run` are not passes. `Out of Scope` does not affect the current decision when the scope boundary is explicit. A `Blocker` or `High` check that is blocked or not run prevents unconditional approval unless the standards define sufficient substitute evidence and that evidence is present.


## Defect Report Fields

For failed checks, include as many of these fields as the available evidence supports:

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

Keep the report concise in conversation. If the user asks for a saved artifact, use these fields as the durable defect format.

## Final Conclusion Mapping

In standards mode, determine the standards conclusion first:

- `Approved`: all release-blocking checks pass and remaining lower-risk issues do not aggregate into release risk
- `Approved with Risks`: no `Blocker` failure, remaining risk is explicitly bounded and allowed by the standards or user
- `Rejected`: a confirmed release-blocking check fails or a core in-scope behavior is missing
- `Blocked`: release-blocking or high-risk checks cannot be verified and substitute evidence is insufficient

Then report both forms:

| Standards conclusion | Skill decision |
| --- | --- |
| Approved | Pass |
| Approved with Risks | Pass with notes |
| Rejected | Fix needed |
| Blocked | Blocked |

Do not report `Approved` if any release-blocking gate is failed, blocked, or not run without substitute evidence.
