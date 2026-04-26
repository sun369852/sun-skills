# Verification and Evidence

## Verification Strategy

Run the smallest command set that gives meaningful confidence:

- targeted unit tests for changed logic
- integration or API tests for contract changes
- frontend build/typecheck/lint for UI and TypeScript changes
- migration/schema checks for persistence changes
- end-to-end or manual browser checks for critical user flows

Do not run expensive broad suites first if a targeted check exists. Escalate to broader checks when shared contracts, public APIs, routing, auth, data models, or build configuration changed.

## Evidence to Record

For each command, record:

- command
- result: passed, failed, skipped, or not run
- relevant failure summary
- why it was selected
- related audit check IDs when a quality standards artifact exists

If verification is skipped, state the reason and residual risk. "Not run" is acceptable only when environment, time, credentials, or missing dependencies make the command impractical; it still affects the final decision. When the standards mark a command as required, skipping it without a blocker or substitute evidence prevents unconditional approval.

## Reproducing Reported Verification

If a developer or worker claims tests passed, prefer reproducing the critical checks locally. If reproduction is not possible:

- treat the claim as secondary evidence
- cite the source of the claim, such as run log or worker summary
- avoid a stronger final decision than the evidence supports

## Review-and-Fix Mode

If the user explicitly asks to fix issues found during review:

1. report the findings briefly before editing
2. fix only the confirmed defects
3. rerun the relevant failing or risk-covering checks
4. update the final decision based on post-fix evidence

Do not turn review into broad refactoring.
