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
