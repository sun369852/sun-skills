# Delivery Topology Contract

Use this reference after the PRD and technical design are ready, before task archiving, implementation, startup checks, or final review.

The topology contract is the source of truth for what must exist and run. Do not infer product completeness from whatever projects or ports already exist in the repository.

## Extraction Rule

Extract every required runtime surface declared or implied by the PRD and technical design:

- name
- type: `frontend`, `miniapp`, `backend`, `database`, `worker`, or `external service`
- expected path
- start command
- port or preview target
- smoke check
- MVP required: `yes` or `no`
- source reference

If PRD and technical design disagree, keep the PRD as product source of truth and record the design conflict as a blocker or assumption.

## Readiness Gate

Do not enter implementation until every MVP-required runtime surface has either:

- a mapped implementation task, or
- an explicit blocked/skipped reason.

Do not report the product as fully runnable or fully started while any MVP-required runtime surface is missing, not started, failed, blocked, or unverified.

## Startup Answer Rule

When asked whether the project is started, validate against this topology contract instead of only checking responding ports.

Report each required surface as one of:

- `running`
- `missing project`
- `not started`
- `failed`
- `blocked`

Answer at product level only after listing required surfaces. For example: "Backend and platform admin are running; merchant-ui and shop-miniapp are missing, so the overall product is not fully started."
