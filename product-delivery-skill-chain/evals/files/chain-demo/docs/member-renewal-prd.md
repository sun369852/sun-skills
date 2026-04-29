# Member Renewal PRD

## Goal

Allow paid course members to renew an expiring membership and keep access to paid course content.

## Scope

- Show renewal entry in the member center when the membership expires within 14 days.
- Support monthly and yearly renewal packages.
- Extend the current membership end date after successful payment.
- If the membership is already expired, renewal starts from the successful payment time.
- Keep historical order and invoice records unchanged.

## Non-Goals

- No auto-renewal in this version.
- No coupon support in this version.
- No changes to course publishing or pricing.

## Users

- Member: renews membership to keep watching paid courses.
- Operations admin: views renewal records in existing member order reports.

## Acceptance Criteria

- Active members can renew before expiration.
- Expired members can renew and regain paid course access.
- Failed payments do not change membership end date.
- Renewal order records include package, paid amount, old end date, and new end date.
- Existing paid-course access checks use the updated membership end date.

## Open Questions

- Whether renewal reminder messaging should include email, SMS, or in-app only.
