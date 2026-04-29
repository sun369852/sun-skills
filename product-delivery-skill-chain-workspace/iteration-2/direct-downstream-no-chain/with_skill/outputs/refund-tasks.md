# Refund Reason Task Breakdown

## Source

- PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\docs\refund-prd.md`
- Generated: 2026-04-29
- Requirement mode: Existing project iteration
- Project context reviewed: N/A

## Summary

- Goal: Allow support operators to record one structured internal refund reason when approving refunds, and expose that reason internally and in exports.
- Delivery strategy: Add the refund reason as part of the refund approval contract first, then surface it in internal detail and export flows, with focused tests around required reason, internal visibility, and unchanged refund status behavior.
- Key risks / open questions: No blocker. Assumption: the existing system already records the approving operator for refunds or can associate the current operator with the approval event.

## Functional Blocks and Coupling

| Block | Independent Product Behavior | Coupling Rationale | Primary Tasks | Dependencies / Parallelism |
| --- | --- | --- | --- | --- |
| B1 | Refund Approval Reason Capture | Shared approval workflow, validation rule, refund record data, and status compatibility risk | T001, T002, T005 | T001 before T002 and T005 |
| B2 | Internal Refund Reason Visibility | Shared internal refund detail behavior and operator/reason display | T003, T005 | T003 depends on T001 |
| B3 | Refund Reason Export | Shared export schema and internal reporting behavior | T004, T005 | T004 depends on T001; can run after export contract is known |

## Task Graph

| ID | Task | Block | Area | Priority | Risk | Depends On | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | Add refund reason to approved refund data contract | B1 | backend | P0 | medium | - | pending |
| T002 | Require one reason during refund approval | B1 | fullstack | P0 | medium | T001 | pending |
| T003 | Show reason and operator on internal refund detail | B2 | fullstack | P1 | low | T001 | pending |
| T004 | Include reason and operator in refund exports | B3 | backend | P1 | medium | T001 | pending |
| T005 | Add regression coverage for required reason and unchanged status behavior | B1/B2/B3 | qa | P0 | medium | T002, T003, T004 | pending |

## Ready Tasks

### B1 - Refund Approval Reason Capture

#### T001 - Add refund reason to approved refund data contract

- Feature block: B1 - Refund Approval Reason Capture
- Area: backend
- Priority: P0
- Risk: medium
- Source: PRD Scope; Acceptance Criteria
- Depends on: -
- Status: pending
- Deliverable: Refund approval data model/API contract supports an internal refund reason and approving operator reference.
- Suggested files / areas:
  - To be discovered: refund domain model, approval API, persistence schema, refund fixtures
- Boundaries:
  - Do not change existing refund status values or status transition behavior.
  - Do not expose the reason to customer-facing APIs or views.
- Notes:
  - Supported reasons must be limited to: duplicate payment, product issue, customer request, goodwill, other.
  - Store the reason with the approved refund record or approval event so detail and export flows can read the same source.
  - Treat operator as the approving support operator, not a free-form user-provided value.
- Acceptance:
  - Approved refund records can persist one supported reason.
  - Unsupported or missing reason cannot be accepted by the approval contract.
  - Existing refund status behavior remains unchanged.
- Validation:
  - Run existing backend tests for refund approval and status transitions.
  - Add or update contract/model tests for supported and unsupported reasons.

#### T002 - Require one reason during refund approval

- Feature block: B1 - Refund Approval Reason Capture
- Area: fullstack
- Priority: P0
- Risk: medium
- Source: PRD Scope; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Refund approval flow requires operators to choose exactly one supported reason before approval succeeds.
- Suggested files / areas:
  - To be discovered: support refund approval screen/form, approval endpoint, validation layer
- Boundaries:
  - Do not add customer-visible messaging about the internal reason.
  - Do not introduce multi-select, custom free-text reasons, or new approval states.
- Notes:
  - Use the exact PRD reason set unless the project has existing enum display conventions.
  - The `other` reason is a structured option, not a request for additional notes.
- Acceptance:
  - A support operator cannot approve a refund without selecting a reason.
  - A support operator can approve a refund with any one supported reason.
  - Approval still produces the same refund status outcome as before.
- Validation:
  - Add UI/API validation tests or equivalent integration tests for missing and valid reason.
  - Manually verify the operator flow if no automated UI harness exists.

### B2 - Internal Refund Reason Visibility

#### T003 - Show reason and operator on internal refund detail

- Feature block: B2 - Internal Refund Reason Visibility
- Area: fullstack
- Priority: P1
- Risk: low
- Source: PRD Scope; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Internal refund detail view displays refund reason and approving operator.
- Suggested files / areas:
  - To be discovered: internal support refund detail route/view, refund detail API/serializer
- Boundaries:
  - Do not show the refund reason or operator in customer-facing refund detail surfaces.
  - Do not change unrelated refund detail fields.
- Notes:
  - Keep the display internal-only and aligned with existing support/admin terminology.
  - If the detail API is shared, gate the fields by internal context or use an internal-only endpoint/serializer.
- Acceptance:
  - Internal refund detail shows the selected reason.
  - Internal refund detail shows the approving operator.
  - Customer-facing refund views do not expose the internal reason.
- Validation:
  - Add serializer/API/view tests for internal detail.
  - Add a negative check for customer-facing visibility if shared code paths exist.

### B3 - Refund Reason Export

#### T004 - Include reason and operator in refund exports

- Feature block: B3 - Refund Reason Export
- Area: backend
- Priority: P1
- Risk: medium
- Source: PRD Scope; Acceptance Criteria
- Depends on: T001
- Status: pending
- Deliverable: Refund export output includes refund reason and approving operator.
- Suggested files / areas:
  - To be discovered: refund export job/service, CSV/report column mapping, export tests
- Boundaries:
  - Do not change existing export filters, refund status behavior, or unrelated columns except where adding the new fields requires documented column additions.
  - Do not include customer-facing text beyond the internal reason label/value.
- Notes:
  - Add columns in a way that follows existing export compatibility conventions.
  - Ensure historical refunds without a reason are handled according to existing nullable/export conventions; do not invent backfill behavior unless required by the project.
- Acceptance:
  - Refund exports include reason.
  - Refund exports include operator.
  - Existing exported refund status values remain unchanged.
- Validation:
  - Add export fixture tests covering an approved refund with reason and operator.
  - Run existing refund export regression tests.

### B1/B2/B3 - End-to-End Verification

#### T005 - Add regression coverage for required reason and unchanged status behavior

- Feature block: B1/B2/B3 - End-to-End Verification
- Area: qa
- Priority: P0
- Risk: medium
- Source: PRD Acceptance Criteria
- Depends on: T002, T003, T004
- Status: pending
- Deliverable: Automated or documented verification proving all acceptance criteria are covered.
- Suggested files / areas:
  - To be discovered: refund approval tests, internal detail tests, export tests, regression checklist
- Boundaries:
  - Do not expand scope into refund policy, refund eligibility, notifications, payment gateway behavior, or customer messaging.
- Notes:
  - Focus coverage on the new reason requirement and unchanged existing status behavior.
  - If no automated suite exists for one surface, add a concise manual verification checklist.
- Acceptance:
  - Missing reason fails refund approval.
  - Supported reasons pass refund approval.
  - Internal detail shows reason and operator.
  - Export includes reason and operator.
  - Existing refund status behavior is unchanged.
- Validation:
  - Run relevant refund approval, detail, export, and status regression checks.

## Blocked Tasks

- None.

## Coverage Map

| PRD Requirement | Covered By | Notes |
| --- | --- | --- |
| Operators choose one refund reason when approving a refund. | T001, T002, T005 | Includes supported reason validation. |
| Supported reasons: duplicate payment, product issue, customer request, goodwill, other. | T001, T002, T005 | Reason set is treated as fixed structured options. |
| Reason is internal-only and not shown to customers. | T003, T005 | Requires negative customer-facing visibility check if shared surfaces exist. |
| Refund exports include reason and operator. | T004, T005 | Export adds reason and approving operator. |
| Refund approval requires a reason. | T002, T005 | Missing reason blocks approval. |
| Refund detail shows reason and operator internally. | T003, T005 | Internal detail only. |
| Existing refund status behavior is unchanged. | T001, T002, T004, T005 | Explicit boundary and regression check. |

## Unmapped PRD Items

- None.

## Derived Technical Enablement

- T001: Required to provide a durable source for the PRD-required approval validation, internal detail display, and export fields.
- T005: Required to verify PRD acceptance criteria and prevent regression in existing refund status behavior.

## Open Questions and Assumptions

- Assumption: the system can identify the approving support operator from the authenticated approval action or an existing audit trail.
- Assumption: historical approved refunds without a reason may remain blank/null in exports unless existing project policy requires a migration or backfill.
- Open question: whether export column additions must preserve exact column order for downstream consumers; this should be checked against local export conventions during implementation.

## Change Log

- 2026-04-29 Created initial task archive from PRD.

## Archive Record

- Created by: PRD Task Archiver
- Archive purpose: implementation task breakdown from existing PRD
- Follow-up: Hand this archive to implementation after confirming local refund model, approval API, internal detail, and export file conventions.
