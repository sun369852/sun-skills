# Second-Pass Review

## Missing PRD Coverage

- Manual override is named in audit requirements, but the draft leaves who can perform it and which statuses it can affect as an open question.
- Finance manager audit use is under-specified.
- Failed provider retry audit details should explicitly include before/after status, retry attempt number/provider request ID, reason, actor, timestamp, and correlation ID.

## Frontend/Backend Contract Issues

- Same idempotency key with different payload needs payload fingerprinting or a clear conflict response.
- Provider callbacks before synchronous API response require durable provider attempt/request correlation.
- Refundable amount semantics must define which statuses reserve amount.
- API responses need shared status/error enums, failure reason, retry eligibility, approval eligibility, and audit visibility shapes.

## Risky Assumptions

- Provider event ordering may be unavailable.
- USD threshold and non-USD conversion are unresolved.
- Cancellation policy is unresolved despite `cancelled` being a PRD status.
- Existing order/payment compatibility is assumed.

## Contradictions

- “500 USD” conflicts with a draft assumption that threshold uses order currency.
- “100% coverage” was too strong while PRD-affecting decisions remained open.

## Required Changes

- Add idempotency payload fingerprint behavior.
- Add provider callback correlation via durable refund attempts.
- Define refundable balance reservation semantics.
- Mark currency conversion, cancellation, and manual override as blocking product/security questions.
- Expand API contract response shapes and enums.
- Replace the unqualified coverage estimate.

## Approval Status

request changes
