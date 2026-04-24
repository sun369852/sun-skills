# PRD Template Variants

Use this reference when the requirement is not a standard end-user feature. Adapt the base PRD shape; do not force irrelevant sections.

## Template Decision Flow

1. Is this a user-facing feature with both UI and backend behavior?
   - Yes: use Standard Product Feature from `prd-content.md`.
   - No: continue.
2. Is this primarily UI/UX behavior with minimal backend impact?
   - Yes: use Pure Frontend Component or Page.
   - No: continue.
3. Is this primarily backend/domain logic with minimal UI?
   - Yes: use Backend Service or Domain Capability.
   - No: continue.
4. Does this change existing data, history, records, or migration behavior without being mainly a new feature?
   - Yes: use Data Migration or Historical Data Change.
   - No: continue.
5. Is this about metrics, dashboards, exports, or reporting definitions?
   - Yes: use Reporting, BI, or Export Requirement.
   - No: continue.
6. Is this about access control, roles, sensitive data, audit, or security?
   - Yes: use Permission, Security, or Admin Control.
   - No: continue.
7. Does this involve manual operations, offline work, customer service, finance handling, review, or fulfillment?
   - Yes: use Operational Workflow.
   - No: re-examine the requirement. If it is a normal user-facing feature with UI and backend behavior, use Standard Product Feature. If it is genuinely unusual, adapt the closest template or ask the user for the primary product risk.

## Mixed Requirements

If the requirement spans multiple categories:

- use the template that matches the primary product risk
- add relevant sections from secondary templates
- do not duplicate sections just to satisfy every template

Example: backend service with significant reporting impact: use Backend Service or Domain Capability, then add metric definitions, filters, and export behavior from Reporting/BI.

## Standard Product Feature

Use the base structure from `prd-content.md`.

Best for:

- new user-facing flows
- B-side admin modules
- existing feature increments
- multi-role workflows

Emphasize:

- users and scenarios
- workflow
- permissions
- business rules
- UI states
- data/state changes
- acceptance criteria

## Pure Frontend Component or Page

Use when the change is primarily UI behavior and does not define new backend semantics.

Recommended sections:

```markdown
# [Component/Page] PRD

## 1. Background and Goal
## 2. Entry Points and User Scenarios
## 3. UI Scope and Non-Goals
## 4. Layout and Content Requirements
## 5. Interaction States
## 6. Validation and Error Handling
## 7. Permissions and Visibility
## 8. Data Dependencies
## 9. Responsive and Accessibility Expectations
## 10. Acceptance Criteria
## 11. Risks, Assumptions, and Open Questions
```

Do not invent API contracts. Record backend/data assumptions separately.

## Backend Service or Domain Capability

Use when the change is mostly domain behavior, API/service logic, jobs, integrations, or records.

Recommended sections:

```markdown
# [Backend Capability] PRD

## 1. Background and Goal
## 2. Actors, Systems, and Boundaries
## 3. Scope and Non-Goals
## 4. Domain Objects and Records
## 5. State Transitions and Business Rules
## 6. Permissions and Audit Requirements
## 7. Integrations, Jobs, and Failure Handling
## 8. Data Retention and Historical Behavior
## 9. Reporting or Export Impact
## 10. Acceptance Criteria
## 11. Risks, Assumptions, and Open Questions
```

Keep it product-semantic. Avoid turning it into API design unless the user asks.

## Data Migration or Historical Data Change

Use when the requirement changes existing records, backfills data, changes ownership, or migrates historical state.

Recommended sections:

```markdown
# [Data Migration] PRD

## 1. Background and Goal
## 2. Affected Data and User Impact
## 3. Current State and Target State
## 4. Migration Scope
## 5. Business Rules for Historical Records
## 6. Validation and Reconciliation
## 7. Rollout, Rollback, and Communication
## 8. Permissions and Audit
## 9. Risks and Open Questions
## 10. Acceptance Criteria
```

Blocking questions usually include historical truth, rollback, audit trail, and user-visible changes.

## Reporting, BI, or Export Requirement

Use when the requirement defines metrics, dashboards, exports, or statistics.

Recommended sections:

```markdown
# [Reporting/Export] PRD

## 1. Background and Decision Use
## 2. Users and Scenarios
## 3. Metric or Field Definitions
## 4. Filters, Dimensions, and Time Windows
## 5. Data Freshness and Update Timing
## 6. Permissions and Visibility
## 7. Export or Dashboard Behavior
## 8. Edge Cases and Data Quality Rules
## 9. Acceptance Criteria
## 10. Risks, Assumptions, and Open Questions
```

Metric definitions and time windows must be explicit before saving.

## Permission, Security, or Admin Control

Use when the requirement changes access, roles, approvals, audit, sensitive fields, or cross-tenant behavior.

Recommended sections:

```markdown
# [Permission/Security] PRD

## 1. Background and Risk
## 2. Actors and Roles
## 3. Scope and Non-Goals
## 4. Permission Matrix
## 5. Sensitive Data and Visibility Rules
## 6. Audit and Operation Records
## 7. Exception Handling
## 8. Compatibility With Existing Permissions
## 9. Acceptance Criteria
## 10. Risks, Assumptions, and Open Questions
```

Prefer a permission matrix over prose.

## Operational Workflow

Use when the requirement depends on manual handling, customer service, finance, review, fulfillment, or offline procedures.

Recommended sections:

```markdown
# [Operational Workflow] PRD

## 1. Background and Goal
## 2. Operators and Responsibilities
## 3. Triggering Scenarios
## 4. Workflow and Statuses
## 5. Manual Actions and Guardrails
## 6. Exception Handling and Escalation
## 7. Records, Audit, and Reporting
## 8. User-Facing Impact
## 9. Acceptance Criteria
## 10. Risks, Assumptions, and Open Questions
```

Do not hide SOP decisions inside implementation notes. If operator responsibility is unclear, ask.
