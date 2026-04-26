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

## Substitute Evidence

When direct execution is blocked by services, credentials, seed data, or external systems, look for the strongest feasible substitute evidence:

- static inspection of tests, mocks, assertions, fixtures, and coverage of the changed path
- API handler, schema, migration, policy, or permission checks tied to the requirement
- dry-run commands, type checks, build checks, or migration validation that do not hit production systems
- logs, audit-event call sites, telemetry wiring, or documented correlation IDs
- screenshots or manual QA notes only when they identify the environment, data, user role, and checked path

Substitute evidence can reduce uncertainty, but it does not turn a required unavailable verification into a full pass unless the source standards allow that fallback.

## Reproducing Reported Verification

If a developer or worker claims tests passed, prefer reproducing the critical checks locally. If reproduction is not possible:

- treat the claim as secondary evidence
- cite the source of the claim, such as run log or worker summary
- avoid a stronger final decision than the evidence supports

## Failure Attribution

When a verification command fails, do a shallow attribution pass before deciding:

- inspect the failed test name, error message, stack, and failed file
- compare the failure path with changed files, touched files, task scope, and audit checks
- rerun the failing targeted test when cheap and useful
- compare with run logs or CI notes if available
- check for missing dependencies, environment variables, services, credentials, or test data

Classify the failure:

- `Related`: covered path is in scope; usually `Fix needed`.
- `Unrelated`: clear historical or unrelated module failure; usually at most `Pass with notes`.
- `Environment`: required infrastructure, credentials, data, or service missing; usually `Blocked` for core checks.
- `Unknown`: relation cannot be determined; usually `Blocked`, or `Fix needed` when the failure strongly suggests a regression.

## Inline Review-and-Fix Mode

The default repair path is to hand implementation defects to the development skill. If the user explicitly asks this current agent to fix issues found during review:

1. report the findings briefly before editing
2. fix only the confirmed defects
3. rerun the relevant failing or risk-covering checks
4. update the final decision based on post-fix evidence

Do not turn review into broad refactoring.
