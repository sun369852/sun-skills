# Member Renewal PRD

## Background

The membership product currently lets support staff create annual memberships manually. Renewals are handled outside the product, which causes missed renewal windows and inconsistent audit records.

## Goals

- Let members renew an active or recently expired membership from the account portal.
- Let support staff renew on behalf of a member.
- Preserve historical membership periods for audit and reporting.
- Send renewal reminder emails at 30, 7, and 1 day before expiration.

## Non-Goals

- Do not introduce monthly memberships.
- Do not change the existing payment provider.
- Do not merge historical membership periods into one mutable record.

## Users and Roles

| Role | Capability |
| --- | --- |
| Member | Renew own active or expired-within-30-days membership |
| Support | Renew any eligible member membership and view renewal history |
| Admin | Configure reminder email schedule and view renewal reports |

## Functional Requirements

1. Members can see renewal eligibility, expiration date, next period dates, and renewal price in the account portal.
2. Members can renew only if the membership is active or expired within the last 30 days.
3. Support users can renew on behalf of eligible members and must provide an internal note.
4. A successful renewal creates a new membership period record linked to the previous period.
5. The system sends reminder emails 30, 7, and 1 day before expiration.
6. Renewal failures from the payment provider are shown with a recoverable error message.
7. Admins can view a renewal report filtered by status, renewal channel, and date range.

## Business Rules

- Renewal price comes from the existing annual plan price at checkout time.
- A member with an unpaid invoice cannot renew until the invoice is resolved.
- Renewal history must show actor, channel, timestamp, previous period, new period, and payment status.
- Reminder emails must not be sent to members who opted out of transactional reminders.

## Acceptance Criteria

- A member can complete a successful self-renewal and see the new period in history.
- A support user can renew for a member and the internal note is recorded.
- Ineligible members see the reason renewal is unavailable.
- Failed payment attempts do not create a new membership period.
- Reminder emails are scheduled only for eligible memberships.
- Renewal report filters return correct rows for status, channel, and date range.

## Open Questions

- Should expired memberships older than 30 days be directed to repurchase or support?
