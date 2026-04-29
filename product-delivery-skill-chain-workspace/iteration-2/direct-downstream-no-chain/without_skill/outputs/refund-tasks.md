# Refund Reason Task Breakdown

## Source

- PRD: D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\docs\refund-prd.md
- Generated: 2026-04-29
- Requirement mode: Existing project iteration
- Project context reviewed: N/A

## Summary

- Goal: Allow support operators to record structured internal refund reasons for approved refunds.
- Delivery strategy: Start with the refund reason domain contract, then wire approval validation, internal detail display, exports, and focused verification.
- Key risks / open questions: Project routes, schema, API names, and export implementation are not provided, so exact files must be discovered during implementation.

## Functional Blocks and Coupling

| Block | Independent Product Behavior | Coupling Rationale | Primary Tasks | Dependencies / Parallelism |
| --- | --- | --- | --- | --- |
| B1 | Refund Reason Contract | Approval, detail, and export must share the same allowed reason values and stored operator metadata. | T001 | Must land before T002-T005 |
| B2 | Refund Approval Reason Capture | Operators must choose one reason before an approved refund can be saved. | T002 | Depends on T001 |
| B3 | Internal Refund Visibility | Internal refund detail must show reason and operator without exposing the reason to customers. | T003 | Depends on T001; can run after T002 contract is stable |
| B4 | Refund Export Coverage | Refund exports must include reason and operator. | T004 | Depends on T001; can run in parallel with T003 |
| B5 | Verification and Regression | Prove required behavior works while existing refund status behavior remains unchanged. | T005 | Depends on T002-T004 |

## Task Graph

| ID | Task | Block | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | Define refund reason data contract | B1 | backend | P0 | medium | - | pending |
| T002 | Require reason during refund approval | B2 | fullstack | P0 | medium | T001 | pending |
| T003 | Show reason and operator on internal refund detail | B3 | fullstack | P1 | low | T001 | pending |
| T004 | Include reason and operator in refund exports | B4 | backend | P1 | medium | T001 | pending |
| T005 | Add refund reason verification coverage | B5 | qa | P0 | medium | T002, T003, T004 | pending |

## Ready Tasks

### B1 - Refund Reason Contract

#### T001 - Define refund reason data contract

- Feature block: B1 - Refund Reason Contract
- Area: backend
- Priority: P0
- Risk: medium
- Source: PRD Scope; Acceptance Criteria
- Depends on: -
- Status: pending
- Deliverable: Stored refund reason and operator fields backed by the supported reason list.
- Suggested files / areas:
  - To be discovered: refund domain model, persistence schema, approval API/input contract, fixtures or factories.
- Boundaries:
  - Do not change refund status values or status transition semantics.
  - Do not expose the internal reason in customer-facing responses.
- Notes:
  - Supported reasons are duplicate payment, product issue, customer request, goodwill, and other.
  - Store enough operator metadata for internal detail and export output.
- Acceptance:
  - The refund record can persist exactly one supported reason for an approved refund.
  - The approving operator can be associated with the saved refund reason.
  - Unsupported reason values are rejected or cannot be selected.
- Validation:
  - Add or update domain/API tests for allowed values and operator persistence.

### B2 - Refund Approval Reason Capture

#### T002 - Require reason during refund approval

- Feature block: B2 - Refund Approval Reason Capture
- Area: fullstack
- Priority: P0
- Risk: medium
- Source: PRD Scope; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Refund approval flow requires operators to select one reason before approval succeeds.
- Suggested files / areas:
  - To be discovered: support refund approval UI, approval API handler, validation layer, form state.
- Boundaries:
  - Do not add customer-visible refund reason messaging.
  - Do not alter existing refund status behavior except adding the required reason validation.
- Notes:
  - Present only the supported reason options from the PRD.
  - Validation should fail before or during approval if no reason is provided.
- Acceptance:
  - Approval without a reason is blocked.
  - Approval with one supported reason succeeds.
  - Existing approved/refunded status behavior remains unchanged.
- Validation:
  - Add or update UI/API tests for missing reason and valid reason approval.

### B3 - Internal Refund Visibility

#### T003 - Show reason and operator on internal refund detail

- Feature block: B3 - Internal Refund Visibility
- Area: fullstack
- Priority: P1
- Risk: low
- Source: PRD Scope; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Internal refund detail view displays the saved refund reason and approving operator.
- Suggested files / areas:
  - To be discovered: internal support refund detail route, detail API/serializer, UI component.
- Boundaries:
  - Do not add reason fields to customer-facing refund detail, notification, email, or public API output.
- Notes:
  - Confirm the detail surface is internal-only before adding the fields.
- Acceptance:
  - Internal operators can see refund reason and operator on refund detail.
  - Customer-facing refund surfaces do not show the internal reason.
- Validation:
  - Add or update internal detail tests and, where available, customer visibility regression checks.

### B4 - Refund Export Coverage

#### T004 - Include reason and operator in refund exports

- Feature block: B4 - Refund Export Coverage
- Area: backend
- Priority: P1
- Risk: medium
- Source: PRD Scope; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Refund export output includes refund reason and operator columns or fields.
- Suggested files / areas:
  - To be discovered: refund export query, CSV/report serializer, export tests.
- Boundaries:
  - Do not change unrelated export filters, ordering, or refund status behavior.
- Notes:
  - Keep export values aligned with the stored reason contract from T001.
- Acceptance:
  - Exported refund rows include the saved reason.
  - Exported refund rows include the associated operator.
- Validation:
  - Add or update export tests using a refund with a saved reason and operator.

### B5 - Verification and Regression

#### T005 - Add refund reason verification coverage

- Feature block: B5 - Verification and Regression
- Area: qa
- Priority: P0
- Risk: medium
- Source: PRD Acceptance Criteria
- Depends on: T002, T003, T004
- Status: pending
- Deliverable: Focused test coverage and manual smoke checklist for refund reason behavior.
- Suggested files / areas:
  - To be discovered: refund test suites, API tests, UI flow tests, export tests, QA checklist.
- Boundaries:
  - Do not broaden coverage to unrelated refund lifecycle changes beyond regression checks needed by the PRD.
- Notes:
  - Treat "Existing refund status behavior is unchanged" as an explicit regression check.
- Acceptance:
  - Tests cover required reason on approval.
  - Tests cover internal detail reason/operator visibility.
  - Tests cover export reason/operator fields.
  - Regression checks confirm existing refund status behavior is unchanged.
- Validation:
  - Run the project's relevant refund test suites once identified.

## Blocked Tasks

- None.

## Coverage Map

| PRD Requirement | Covered By | Notes |
| --- | --- | --- |
| Operators choose one refund reason when approving a refund. | T001, T002 | Contract plus approval validation. |
| Supported reasons: duplicate payment, product issue, customer request, goodwill, other. | T001, T002 | Allowed value contract and UI/API selection. |
| Reason is internal-only and not shown to customers. | T003, T005 | Internal detail plus customer visibility regression. |
| Refund exports include reason and operator. | T004, T005 | Export implementation and tests. |
| Refund approval requires a reason. | T002, T005 | Approval validation and tests. |
| Refund detail shows reason and operator internally. | T003, T005 | Internal detail implementation and tests. |
| Existing refund status behavior is unchanged. | T002, T004, T005 | Boundary on implementation plus regression coverage. |

## Unmapped PRD Items

- None.

## Derived Technical Enablement

- T001: Required to make approval, detail, and export behavior share a consistent saved reason/operator contract.
- T005: Required to verify the PRD acceptance criteria and refund status regression behavior.

## Open Questions and Assumptions

- Assumption: Operator identity is already available in the refund approval context.
- Assumption: The existing project has an internal refund detail surface and refund export mechanism.
- Open question: Exact schema/API/UI file locations must be discovered during implementation.

## Change Log

- 2026-04-29 Created initial task archive from PRD.

## Archive Record

- Created by: PRD Task Archiver
- Archive purpose: implementation task breakdown from existing PRD
- Follow-up: Confirm project file locations, then implement tasks in dependency order.
