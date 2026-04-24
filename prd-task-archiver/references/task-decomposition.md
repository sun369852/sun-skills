# Task Decomposition

Read this file before drafting tasks.

## Decomposition Shape

Prefer vertical, deliverable slices when they reduce handoff risk. Use layer-based tasks only when the work is naturally separated by infrastructure, shared domain logic, or platform concerns.

Before writing individual tasks, analyze functional coupling and define functional blocks. A functional block is a cohesive, independently understandable product behavior slice that should usually be developed, reviewed, and validated together. It should not be a broad module or whole department area.

Use coupling signals to form blocks:

- shared user journey or screen flow
- shared domain object, state transition, or permission rule
- shared API contract, data model, migration, integration, or background job
- shared release or compatibility risk
- tasks that must be validated together to prove one product behavior works

Keep strongly coupled work in the same block. Separate weakly coupled work into different blocks so developers can own and ship it independently. If two blocks need the same contract or data foundation, create a front-loaded contract/foundation block or task instead of duplicating assumptions.

Name blocks by product behavior, not implementation layer. Prefer `Member Renewal Checkout`, `Support Renewal Workflow`, or `Billing Anchor Configuration` over broad labels like `Backend` or `Frontend`.

Keep blocks modest. If a block contains multiple independent user goals, multiple unrelated screens, or several behaviors that can be accepted separately, split it into smaller functional blocks. A good block usually has one primary product outcome and a small set of directly related tasks.

Functional blocks are the primary grouping for developer handoff. Phases and areas are secondary attributes inside a block.

Within each block, group or label tasks with phases such as:

- discovery and alignment
- data model or domain groundwork
- backend/API work
- frontend/user experience work
- integration/background jobs
- permissions, audit, observability, or configuration
- tests and QA
- migration, rollout, documentation, and release checks

## Required Task Fields

Every task should have:

- stable ID, such as `T001`
- title
- feature block
- owner area, such as `frontend`, `backend`, `fullstack`, `qa`, `devops`, `docs`, or `product`
- priority, such as `P0`, `P1`, or `P2`
- risk level, such as `low`, `medium`, or `high`
- source PRD reference
- dependencies
- deliverable
- concrete implementation notes
- acceptance check
- status, defaulting to `pending`

Use these status values unless the project already has a stronger convention:

- `pending`: ready but not started
- `blocked`: cannot proceed until a dependency, decision, or context gap is resolved
- `in_progress`: actively being worked
- `done`: completed and verified
- `skipped`: intentionally not implemented, with a reason recorded

## Granularity

Split tasks small enough that an implementation agent or engineer can pick one up without rereading the whole PRD, but not so small that the archive becomes noise. A good task usually describes a meaningful behavior or system change, not a single line edit.

As a practical granularity test, each task should usually fit into one focused implementation session or one coherent pull request. If a task spans multiple unrelated layers, migrations, permissions, UI flows, and tests, split it or create an earlier contract/alignment task that makes the later work independent.

Use these non-time-based split signals:

- split when a task has more than one primary deliverable
- split when a task crosses more than one major area unless it is intentionally a vertical fullstack slice
- split when a task requires data model changes, API changes, UI changes, migration, and tests all at once
- split when a task has more than 4 or 5 distinct acceptance checks
- split when a task depends on several undefined contracts; create the contract/alignment task first
- keep a task whole when splitting would produce tiny chores that cannot be validated independently

Avoid both extremes:

- too small: `Add one import`, `Rename one local variable`, `Move this button text`
- too broad: `Implement the billing system`, `Build the entire admin module`, `Finish all frontend and backend work`

## Dependencies and Parallelism

Make sequencing explicit:

- identify functional blocks that can be developed independently
- identify cross-block contracts or foundation tasks that must land first
- identify tasks that can run in parallel
- identify tasks blocked by open PRD questions
- identify tasks that must precede other work, such as schema changes, permission rules, or shared API contracts
- avoid assigning frontend tasks that depend on undefined backend contracts without creating a contract task first
- avoid QA tasks that cannot run until fixtures, test data, or environments exist

Use dependency IDs, not vague phrases like "after backend is done".

## Multi-Agent Execution Readiness

For later multi-agent execution, make task boundaries explicit:

- suggest the likely files, modules, routes, APIs, schemas, or docs to inspect when they are known
- call out areas the task should avoid changing
- describe the exact deliverable the worker should leave behind
- include validation commands or verification paths when they can be inferred from the project
- keep cross-task contracts visible so parallel workers do not make incompatible assumptions

## Test and Acceptance Coverage

Create dedicated tasks for verification when the PRD contains user-facing or domain-critical behavior:

- unit tests for domain rules and state transitions
- API tests for permissions, validation, idempotency, and error cases
- UI tests for major flows, empty/loading/error states, and role visibility
- migration or compatibility checks for existing data
- release smoke checks and rollback notes when relevant

Acceptance checks should be concrete and traceable to the PRD. If a requirement cannot be tested because the PRD is ambiguous, mark it as an open question or blocked task rather than guessing.
