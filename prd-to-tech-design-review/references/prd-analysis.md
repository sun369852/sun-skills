# PRD Analysis

Read the PRD before designing. Extract the engineering-relevant product facts without rewriting the PRD.

## Source Boundary

Identify:

- PRD title, feature name, version/date if present
- product goal and non-goals
- primary users and roles
- in-scope flows
- out-of-scope flows
- acceptance criteria
- explicit dependencies or integrations
- PRD sections that are ambiguous, outdated, or conflicting

Treat the PRD as authoritative unless the user gives newer instructions. If project code contradicts the PRD, record the contradiction instead of silently choosing one.

## Engineering Extraction

Capture:

- user journeys and screen/page needs
- domain entities and relationships
- state machines, status values, and lifecycle rules
- permissions, ownership, tenancy, audit, and compliance concerns
- validation rules and error cases
- notifications, async jobs, imports/exports, files, or third-party integrations
- analytics, logging, observability, and operational requirements
- performance, scale, security, privacy, and migration constraints

## Uncertainty Handling

Classify questions as:

- **Blocking**: cannot produce a coherent design without a user decision.
- **Design assumption**: can proceed with a reasonable technical assumption, but it must be recorded.
- **Implementation detail**: safe to defer to task planning or coding.

Ask the user only for blocking questions. For non-blocking gaps, continue and document the assumption.
