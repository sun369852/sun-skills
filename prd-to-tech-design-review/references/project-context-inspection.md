# Project Context Inspection

Use this reference only when the user provides a project path, says this is an existing-project iteration, or asks for compatibility with current implementation.

The goal is to learn conventions, constraints, and integration points. Do not perform a full codebase audit.

## Inspection Budget

Default maximum: 10 files per affected domain or service.

You may exceed this only when:

- the PRD touches multiple independently implemented domains
- routing/API/model conventions cannot be identified within 10 files
- a file points to a required schema, middleware, or API contract that would make the design unsafe to infer

For multi-service or monorepo PRDs, allocate the budget per affected service and state the allocation in the technical design. If exceeding the budget, state why in the final technical design.

## Frontend Checks

Inspect:

- routing configuration or page directory: 1-2 files
- relevant page/screen components: top 2 levels only
- component naming and composition conventions
- state management setup: 1-2 files
- API client/fetch/query utilities: 1-2 files
- form validation and error display examples
- existing loading/empty/error state patterns
- authorization/permission rendering patterns if relevant

Do not inspect unrelated UI areas just to be thorough.

## Backend Checks

Inspect:

- relevant API route/controller/service definitions: 1-3 files
- data models/schemas/migrations for related entities
- auth, permission, tenancy, or middleware setup: 1-2 files
- validation patterns and error response conventions
- background job/event/queue patterns if the PRD needs async work
- test examples for the relevant layer when easy to locate

## Documentation and Output Conventions

Inspect:

- nearby `docs/`, `specs/`, or feature folders for design-document naming
- existing technical design templates if present
- PRD sibling files that indicate where technical design should live

## What to Record

Summarize only the context that affects the design:

- existing conventions to follow
- compatibility gaps
- files inspected
- assumptions caused by missing or incomplete project context
