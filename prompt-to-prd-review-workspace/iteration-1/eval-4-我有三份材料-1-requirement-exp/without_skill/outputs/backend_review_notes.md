# Backend Review Notes

## Review Result

Passed.

## Reviewed Scope

- Invitation creation API.
- Invitation token and expiration logic.
- Invitation acceptance.
- Invitation revocation.
- Expired invitation resend behavior.
- Compatibility with the old PRD.

## Notes

- Backend must reject phone-number invitation payloads for this version, even though the old PRD mentioned phone support.
- Invitation expiration must be calculated as 14 days after creation or successful send time, using a server-side timestamp.
- Accepted users must be added to the enterprise space as ordinary members.
- Pending invitations can be revoked by administrators. Accepted invitations must not be revoked through the invitation revocation API.
- Expired invitations must not be reactivated by changing their expiration time or status. Resend must create a new invitation record and token, while preserving the old expired record for auditability.
- Acceptance must validate that the invitation exists, is addressed to the accepting email identity, is pending, is not revoked, and has not expired.

## Required PRD Clarifications Confirmed

- Store invitation channel as email for this version.
- Use server-side authorization to ensure only administrators can invite and revoke.
- Preserve invitation status history for pending, accepted, expired, and revoked states.
- Treat duplicate active invitations to the same email and enterprise space as a product rule that should be handled explicitly.
