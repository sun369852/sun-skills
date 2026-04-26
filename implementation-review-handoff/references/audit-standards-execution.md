# Audit Standards Execution

Use this after `audit-standards-alignment.md` selects standards mode.

## Parsing

Read human-readable sections and any machine-readable JSON/YAML appendix. Prefer machine-readable check data for IDs, priorities, modes, required evidence, execution requirements, and statuses; confirm against prose when ambiguous.

For each check, capture ID, trace, layer/category, priority, mode, setup/test data, pass/fail criteria, required evidence, execution requirement, retest scope, and status.

If machine-readable data conflicts with prose, treat it as a `Standards gap`; ask for user decision when it affects a core or high-risk check.

## IDs And Layers

Recognize `BV-*`, `IA-*`, `TE-*`, `RG-*`, `EV-*`, and `BQ-*`.

If a third-party standard has no stable IDs, create report-local `EXT-*` IDs, cite the original checklist text/title/row, keep IDs stable within the saved report and re-review, and do not write them back unless asked.

Review behavior and implementation separately. A behavior can pass while implementation still fails an `IA-*` check, such as permission enforcement, data integrity, logging, or test coverage.

## Evidence

Evidence must trace to audit check IDs. Command output, code references, screenshots, API traces, database records, logs, and audit events should identify the related check. Missing required evidence keeps the check `Fail`, `Blocked`, or `Not Run` according to the standards.

Do not collapse evidence into a generic "tests passed" statement when the standards require specific artifacts.

## Hard Fails

Apply standards hard fail conditions before any internal decision label. Unless the standards say otherwise, release-blocking failures include:

- any `Blocker` check fails
- any `Blocker` check is `Blocked` or `Not Run` without substitute evidence
- a core PRD flow has no audit coverage
- high-risk permission, data, payment, ledger, privacy, audit-log, migration, or irreversible behavior lacks implementation audit evidence
- required test commands are not run and no blocker is recorded
- evidence cannot be traced to audit check IDs

A hard fail means the standards conclusion is `Rejected` for confirmed failure or `Blocked` for inability to verify.

## Three-Round Review Record

If standards include a three-round clean-context review record, use it as risk context:

- cite it in the final report
- verify accepted high-risk findings have checks and evidence
- treat ignored high-risk findings as hard fail candidates
- treat unresolved in-scope high-risk findings as `Blocked`

The review record does not replace implementation evidence.
