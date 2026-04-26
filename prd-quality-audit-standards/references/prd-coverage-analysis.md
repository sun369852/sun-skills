# PRD Coverage Analysis

Use this reference after reading the PRD. The goal is to extract the complete verification surface before drafting audit standards.

## Extract The Source Boundary

Record:

- PRD path or pasted-source description
- PRD title and feature name
- supporting documents used, if any
- project files inspected, if any
- source priority when there are multiple documents
- whether project inspection was bounded or unavailable

The PRD should remain the source of truth. If a supporting document contradicts the PRD, preserve the conflict as an open issue unless the user has already resolved priority.

## Bounded Project Context

When a project path is provided, inspect only files that can change the audit standards:

- package/test configuration and documented test commands
- route/API entry points that correspond to the PRD
- schema/model/data access files
- auth, permission, role, and policy code
- logging, audit, metrics, tracing, and observability conventions
- existing test directories and naming patterns
- release, migration, feature-flag, or seed data conventions

Record the inspected files and why each one matters. Do not scan the whole repository just to collect context.

## Requirement Inventory

Create a working inventory before writing final standards:

- actors and user roles
- primary workflows
- alternate and failure workflows
- functional requirements
- business rules
- acceptance criteria
- UI states and user-visible messages
- API/data requirements
- permissions and authorization
- lifecycle/status transitions
- validation rules
- integrations and external dependencies
- notifications, audit logs, or history records
- non-functional requirements such as performance, accessibility, reliability, privacy, security, observability, and localization
- rollout, migration, backward compatibility, and feature-flag requirements
- explicit out-of-scope items
- open questions and assumptions

## Traceability Rules

Every final audit check should trace to one of:

- an explicit PRD requirement
- an acceptance criterion
- a necessary negative/edge case implied by a PRD rule
- a compatibility or release concern the PRD explicitly mentions
- a supporting design/task detail that does not expand product scope
- a bounded project-context finding that affects how the future audit agent can execute or evidence the check

If a check is good engineering hygiene but not PRD-derived, label it as "derived quality standard" and explain why it is needed.

## Ambiguity Handling

Do not convert ambiguous PRD text into arbitrary pass/fail criteria.

Examples:

- If the PRD says "fast" but gives no threshold, define a blocked performance threshold question and, if useful, propose a candidate threshold as an assumption.
- If the PRD says "admin can manage users" but does not define roles/actions, list the missing permission matrix.
- If the PRD says "notify users" but does not define channel/timing/content, block exact notification tests and still verify that a notification event is generated if the PRD clearly requires one.

## Risk Weighting

Promote checks to release-blocking gates when failure could cause:

- data loss, corruption, duplicate processing, or irreversible changes
- unauthorized access or privilege escalation
- payment, refund, billing, or balance errors
- broken auditability or compliance evidence
- privacy/security exposure
- external integration failures that leave inconsistent state
- migration or backward compatibility damage
- inaccessible core user flows

Routine display defects and copy issues can still be important, but should not be described with the same release-blocking weight unless the PRD makes them critical.
