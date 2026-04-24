# Collaboration Workflow

The frontend and backend perspectives should improve each other. The main agent mediates so the final technical design is coherent.

## Round 1: Independent Review

Frontend reviewer focuses on:

- pages, routes, components, layout regions, forms, tables, filters, modals, and navigation
- client state, server state, cache invalidation, optimistic updates, loading/empty/error states
- user interactions, validation, accessibility, responsive behavior, and internationalization
- API needs from the UI point of view
- frontend risks and PRD gaps

Backend reviewer focuses on:

- domain model, data storage, migrations, indexes, transactions, and consistency
- API endpoints, request/response contracts, authz/authn, rate limits, idempotency
- jobs, events, integrations, file handling, notifications, and retries
- security, privacy, audit, observability, and operational concerns
- backend risks and PRD gaps

## Shared Issue Board

After round 1, merge the findings into:

- agreements
- frontend needs from backend
- backend constraints for frontend
- conflicts or mismatched assumptions
- missing PRD details
- suggested decisions

## Round 2: Exchange

Give each reviewer the counterpart's summary. Ask for:

- corrections to their own assumptions
- acceptance or rejection of counterpart requests
- compromise proposals
- contract details needed to unblock the final design
- newly discovered risks

One exchange round is usually enough. Add another round only when the reviewers disagree on an important API, data, state, or UX decision.

## Failure Recovery

Use this short decision order before adding extra review rounds:

1. Format issue: salvage concrete findings and ask one focused follow-up.
2. Missed requirement: add it to the shared issue board and ask a targeted question.
3. Implementation preference conflict: use existing project conventions.
4. API, data, or state conflict: choose the explicit and testable contract.
5. Product semantics conflict: ask the user if blocking; otherwise record an assumption.

If a reviewer returns an unusable format:

- salvage concrete findings from the response
- ask one focused follow-up for the missing sections if subagents are still available
- if follow-up is not possible, complete that perspective inline and record the fallback in the collaboration record

If a reviewer misses an obvious PRD requirement:

- add the missed requirement to the shared issue board
- ask the reviewer to respond to that specific gap, or handle it inline if the workflow would otherwise stall

If frontend and backend reviewers disagree:

- first classify the conflict as product semantics, API contract, data ownership, state lifecycle, performance, security, or implementation preference
- resolve implementation-preference conflicts using existing project conventions
- resolve API/data/state conflicts by choosing the option that makes contracts explicit and testable
- do not resolve product-semantics conflicts by guessing; ask the user if it blocks the design, otherwise record an assumption

If the conflict cannot be resolved after one exchange round:

- preserve both positions in the technical design
- name the recommended decision and why
- mark the unresolved part as a blocking question or design assumption
- keep the rest of the technical design moving

## Mediation

The main agent resolves routine technical tradeoffs using project conventions and the PRD. For product semantics, do not guess. Either ask a blocking question or record a clear assumption.

Prefer decisions that:

- reduce ambiguity between UI and API contracts
- keep data ownership and lifecycle rules explicit
- fit existing project architecture
- make validation and error behavior testable
- preserve future task decomposition clarity
