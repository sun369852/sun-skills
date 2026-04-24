# Reviewer Notes

## Review Method

No separate subagent tool was available in this execution environment, so frontend and backend reviews were simulated inline using the bundled reviewer prompts from `D:\sun-skills\prompt-to-prd-review\agents\frontend-prd-reviewer.md` and `D:\sun-skills\prompt-to-prd-review\agents\backend-prd-reviewer.md`.

## Source Map

| Source | Confirmed / Conflicting Facts |
| --- | --- |
| requirement-exploration final prompt | Admin invites by email; invite validity 7 days; accepted invite creates ordinary member; admin can revoke unaccepted invitation |
| Old PRD summary | Invite validity 3 days; phone invitation supported |
| Latest supplement | Email only; validity 14 days; expired invitations cannot be reactivated, only resent |

Applied priority: latest supplement > final prompt > old PRD summary.

## Frontend Review - Round 1

approval_status: changes_required

blocking_findings:
- Draft needs explicit email-only UI behavior so the old phone invitation entry does not remain implied.
- Draft needs visible states for invite list actions: pending, accepted, revoked, expired, empty, error, and permission-denied.
- Draft should clarify that "resend" on an expired invitation is not a reactivation from the user's perspective.

non_blocking_suggestions:
- Record that exact email copy is outside the PRD unless already standardized.
- Keep invitation history filtering as a follow-up or open question.

recommended_prd_changes:
- Add a frontend experience section covering email field validation, loading/success/error states, terminal-state disabled actions, and invitation-link result pages.
- Add acceptance criteria for no phone invitation field and expired invitation resend.

assumptions_to_make_explicit:
- Existing member management has an invitation list or equivalent entry point.
- Identity verification for invited email is handled by the existing account system.

affected_existing_frontend_areas:
- Member management or invitation management entry.
- Invitation creation form.
- Invitation list.
- Invitation acceptance page.

compatibility_risks:
- Existing phone invitation UI may need to be removed or hidden.

## Backend Review - Round 1

approval_status: changes_required

blocking_findings:
- Draft needs a precise invitation lifecycle with terminal states and allowed transitions.
- Draft must state whether expired invitation resend creates a new record or mutates the existing record.
- Draft should define duplicate pending invitation behavior for the same enterprise space and email, or record it as an explicit assumption.

non_blocking_suggestions:
- Add historical-record treatment for old 3-day invitations because the old PRD conflicts with the new 14-day rule.
- Add operation records for revocation and acceptance where product semantics depend on auditability.

recommended_prd_changes:
- Add state transition table.
- Add data fields for invitation owner, email, status, created/sent time, expiration time, accepted time, revoked time, and source invitation ID for resend lineage.
- Add business rules for already-member, revoked, expired, accepted, and duplicate pending cases.

assumptions_to_make_explicit:
- Historical invitations keep their original expiration unless a separate migration decision is made.
- Same enterprise space and email should not have multiple simultaneously valid pending invitations.

affected_existing_backend_areas:
- Invitation domain/service.
- Member relationship creation.
- Permission checks.
- Email notification integration.
- Existing phone invitation path, if present.

compatibility_risks:
- Reusing old invitation records for expired resend would violate the new product requirement.
- Existing 3-day expiration behavior may remain in jobs or validation if not updated.

## Applied Changes Before Final Review

- Removed phone invitation from current scope and made old phone support explicitly superseded.
- Set all new invitation validity rules to 14 days.
- Added lifecycle table and terminal-state semantics.
- Clarified that expired resend creates a new invitation and original invitation remains expired.
- Added frontend UI states and acceptance criteria.
- Added assumptions for duplicate pending invitations, identity matching, and historical invitation treatment.

## Frontend Review - Round 2

approval_status: approved

blocking_findings:
- None

non_blocking_suggestions:
- Email copy and list filtering can remain recorded as non-blocking open questions.

recommended_prd_changes:
- None

assumptions_to_make_explicit:
- Already explicit in PRD.

affected_existing_frontend_areas:
- Member management/invitation management, email invite form, invite list, invite acceptance page.

compatibility_risks:
- Phone invitation UI removal remains a known implementation compatibility item and is recorded.

## Backend Review - Round 2

approval_status: approved

blocking_findings:
- None

non_blocking_suggestions:
- None beyond recorded assumptions and follow-ups.

recommended_prd_changes:
- None

assumptions_to_make_explicit:
- Already explicit in PRD.

affected_existing_backend_areas:
- Invitation lifecycle, member creation, permissions, email notification, expiration handling, old phone invitation path.

compatibility_risks:
- Historical 3-day invitations and existing phone invitation paths require implementation attention; PRD records the product baseline clearly.

## Approval Result

Frontend review approved. Backend review approved. No blocking open questions remain. The final PRD was saved as `final_prd.md`.
