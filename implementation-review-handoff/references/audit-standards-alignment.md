# Audit Standards Alignment

Use this reference when a `quality-audit-standards.md`, implementation audit contract, test audit contract, or PRD-derived audit checklist exists.

## Role of the Standards

Treat the standards artifact as the primary review contract because it already translates PRD requirements into executable audit checks. Do not recreate the standards during implementation review. Execute, inspect, and report against them.

Source priority:

1. newest explicit user instruction
2. quality audit standards artifact
3. task checklist and implementation run log
4. technical design
5. PRD/spec

If the standards conflict with newer user instructions, follow the newer instruction and record the conflict. If the standards conflict with the PRD and there is no newer instruction, mark the conflict as an open question instead of silently choosing behavior.

## Check Layers

Recognize these check ID families when present:

- `BV-*`: behavior verification
- `IA-*`: implementation audit
- `TE-*`: test execution
- `RG-*`: risk gate
- `EV-*`: evidence requirement
- `BQ-*`: blocked question

Review behavior and implementation separately. A UI/API behavior can appear correct while the implementation still fails an `IA-*` check, such as permission enforcement, data integrity, logging, or test coverage.

## Status Rules

Use the standards' statuses when reporting each check:

- `Pass`
- `Fail`
- `Blocked`
- `Not Run`
- `Not Applicable`

`Blocked` and `Not Run` are not passes. A `Blocker` or `High` check that is blocked or not run prevents unconditional approval unless the standards define sufficient substitute evidence and that evidence is present.

## Evidence Rules

Evidence should trace to audit check IDs:

- test output should name the relevant `BV-*`, `IA-*`, or `TE-*` checks
- code review evidence should include file paths and line references when available
- API/log/database evidence should include request parameters, query conditions, correlation IDs, or record IDs when relevant
- failed evidence should map to a defect report entry

If evidence exists but does not trace to an audit check ID, report a verification gap instead of treating it as complete.

## Hard Fail Handling

Treat these as release-blocking unless the standards explicitly say otherwise:

- any `Blocker` check fails
- any `Blocker` check is `Blocked` or `Not Run` without substitute evidence
- a core PRD flow has no audit coverage
- high-risk permission, data, payment, ledger, privacy, audit-log, migration, or irreversible behavior lacks implementation audit evidence
- required test commands are not run and no blocker is recorded
- evidence cannot be traced to audit check IDs

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

When standards define final conclusions, report both forms:

| Standards conclusion | Skill decision |
| --- | --- |
| Approved | Pass |
| Approved with Risks | Pass with notes |
| Rejected | Fix needed |
| Blocked | Blocked |

Do not report `Approved` if any release-blocking gate is failed, blocked, or not run without substitute evidence.
