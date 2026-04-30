# TDD And Verification

## TDD Default

Use strong TDD by default for:

- business logic
- state flows
- data processing
- API behavior
- permissions
- persistence
- cross-module behavior
- regression-prone behavior

Default sequence:

1. Write or update tests for documented behavior.
2. Run targeted tests and confirm failure for the expected reason when practical.
3. Implement the smallest production change.
4. Re-run targeted tests.
5. Strengthen tests after implementation if they miss acceptance criteria or assert implementation details.

## Lightweight Exceptions

For very small, low-risk changes with weak logical coupling, do not force full TDD. Direct implementation plus lightweight verification is acceptable. In extremely low-risk cases, no new test is required.

Examples:

- copy changes
- simple style adjustments
- small config changes
- narrow type annotation fixes
- changes already covered by existing tests

When skipping new tests or full TDD, record the reason in the run log.

## Test Command Priority

Choose verification commands by:

1. User-specified command.
2. Technical docs or task checklist command.
3. Existing project scripts such as `package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`, or CI config.
4. Main-agent inference from changed scope.
5. Environment blocker if no reliable command can be found.

Workers may recommend commands, but the main agent owns the final verification strategy.

## Runtime Verification Gate

Compile is only a syntax/build gate. For runtime-integrated changes, task completion requires startup and smoke verification.

Compile-only verification is not enough when a task changes:

- controller, route, or API endpoint
- Spring Security, auth, filter, interceptor, or middleware
- dependency injection or service bean registration
- mapper XML or ORM mapping
- application config, logging config, or startup config
- database migration used by runtime code
- frontend route guard, request client, or build config

Minimum verification for these tasks must include the relevant subset:

1. build or package command
2. application startup command
3. port, process, or health check
4. at least one public endpoint smoke when a public endpoint exists
5. at least one protected endpoint unauthorized smoke when auth is involved

After a batch changes shared runtime infrastructure, pause before expanding to downstream feature batches. Run the runtime verification gate first. If the gate fails, route the batch to fix mode before continuing.

If required runtime smoke is skipped, blocked, or fails, the affected task status must be `partial`, `blocked`, or `failed`, not `done`.

When audit standards are included in the implementation handoff, extract the TE/RG checks relevant to the current batch before coding. These checks inform required verification; they do not replace PRD, technical design, or task-list scope.

## Missing Test Account Rule

Missing seed data or test accounts may block success-path API tests only. It must not block:

- backend startup verification
- public endpoint smoke
- unauthorized protected endpoint smoke
- invalid-login smoke
- platform regression smoke

If success-path data is missing, mark only those success-path checks as blocked and still run account-independent runtime checks.

## Unrelated Failures

A task can be marked done when targeted verification passes and other failures are demonstrably unrelated. Evidence can include:

- failure in untouched modules
- pre-existing failure
- missing external service or environment dependency
- snapshot or integration issue outside the task path

Record the command, error summary, and reason for classifying the failure as unrelated. If relation is unclear, mark the task `partial` or `blocked`.

## Completion Minimum

A task is complete only when:

- implementation is done
- acceptance criteria are satisfied or exceptions are recorded
- necessary tests are added/updated or test-skip rationale is recorded
- target verification ran or inability to run is recorded
- main-agent review passes
- task checklist is updated
- run log is updated
- no unexplained failure, TODO, debug artifact, or out-of-scope edit remains
