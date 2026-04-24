# Reviewer Notes

## Review Setup

- Skill used: `prompt-to-prd-review`
- Requirement mode: New requirement
- Source priority: latest user instruction for output location, then the requirement-exploration final prompt as the product source.
- Review method: simulated frontend and backend role reviews inline, using the bundled reviewer prompts from the skill. No separate subagent tool was available in this environment.
- Save gate: final PRD saved only after both perspectives approved and no blocking open questions remained.

## Round 1 Frontend Review

approval_status: changes_required

blocking_findings:
- The initial draft needed more explicit user-facing states for payment failure, payment pending, expired membership, refund in progress, and permission-denied access to paid courses.
- The affected entry points were named, but the expected behavior for existing members versus non-members was not explicit enough for frontend QA.

non_blocking_suggestions:
- Add clear copy constraints that subscription messaging must not imply trial or auto-renewal.
- Record responsive/mobile Web behavior as implementation follow-up if mobile Web is in scope later.

recommended_prd_changes:
- Add a page and interaction state table covering homepage, course detail page, subscription page, payment result page, and personal center.
- Add acceptance criteria for no trial, no auto-renewal, paid-course access gating, expired subscription gating, and refund success behavior.

assumptions_to_make_explicit:
- User must be logged in before payment.
- Specific package names, prices, and duration are not confirmed.

affected_existing_frontend_areas:
- N/A

compatibility_risks:
- None

## Round 1 Backend Review

approval_status: changes_required

blocking_findings:
- The initial draft needed clearer subscription state transitions and refund state behavior.
- Payment callback idempotency, duplicate payment handling, historical record retention, and refund result handling needed to be explicit enough for backend QA.
- The refund rule depended on "learned more than 2 lessons"; the PRD needed to state how the ambiguity is handled without inventing an unconfirmed final metric.

non_blocking_suggestions:
- Add reminder records and refund records as product data expectations.
- Clarify that refund success immediately revokes paid-course entitlement.

recommended_prd_changes:
- Add subscription states: unpaid/not subscribed, payment pending, active, expiring soon, expired, refunding, refunded.
- Add a state transition table.
- Add product data records for orders, entitlements, learning records, refund records, and reminders.
- Clarify that the exact learned-lesson definition is a non-blocking open question and recommend using the platform's existing learning completion rule if present.

assumptions_to_make_explicit:
- Entitlement starts only after confirmed payment success.
- Existing course and learning-record concepts are available.

affected_existing_backend_areas:
- N/A

compatibility_risks:
- None

## Applied Changes

- Added a source information section to separate confirmed facts, non-goals, high-risk rules, and unresolved items.
- Added detailed functional requirements for entry points, subscription page, payment, entitlement, personal center, expiry reminders, and refund.
- Added subscription state definitions and state transition rules.
- Added data and historical record expectations.
- Added UI state requirements across the main pages.
- Added exception handling for delayed payment callbacks, duplicate callbacks, login requirement, payment channel unavailability, learning-record delay, refund failure, and expiration edge cases.
- Added product-verifiable acceptance criteria.
- Added non-blocking open questions for package configuration, reminder channel/timing, learned-lesson definition, refund-in-progress entitlement, renewal stacking, and refund arrival copy.

## Round 2 Frontend Review

approval_status: approved

blocking_findings:
- None

non_blocking_suggestions:
- Once business confirms reminder channels and package configuration, update the related copy and acceptance details.

recommended_prd_changes:
- None

assumptions_to_make_explicit:
- Already explicit in the PRD.

affected_existing_frontend_areas:
- N/A

compatibility_risks:
- None

## Round 2 Backend Review

approval_status: approved

blocking_findings:
- None

non_blocking_suggestions:
- Confirm the learned-lesson calculation before implementation starts, because it affects refund eligibility logic.
- Confirm whether refunding freezes entitlement or keeps entitlement active until refund success.

recommended_prd_changes:
- None. These items are already recorded as non-blocking open questions.

assumptions_to_make_explicit:
- Already explicit in the PRD.

affected_existing_backend_areas:
- N/A

compatibility_risks:
- None

## Final Review Outcome

- Frontend review: Approved
- Backend review: Approved
- Blocking open questions: None
- Non-blocking open questions: preserved in the final PRD
- PRD saved as: `final_prd.md`
