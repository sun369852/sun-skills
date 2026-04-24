# Technical Design Template

Use this structure for the saved Markdown document. Omit sections only when clearly irrelevant, and add project-specific sections when needed.

```markdown
# [Feature Name] Technical Design

## Source

- PRD: [path or description]
- Project: [path if applicable]
- Generated: [date]

## Executive Summary

[Short implementation-oriented summary.]

## PRD Scope Mapping

| PRD Requirement | Technical Coverage | Notes |
| --- | --- | --- |
| ... | ... | ... |

## Architecture Overview

[High-level components and data flow.]

## Frontend Design

### Routes and Screens
### Component Structure
### Client State and Data Fetching
### UX States and Validation
### Accessibility and Responsive Behavior

## Backend Design

### Domain Model
### Data Storage and Migrations
### Services and Business Rules
### Background Jobs and Integrations
### Security, Permissions, and Audit

## API Contract

| Method | Path | Purpose | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |

## Data Model

| Entity/Table | Fields | Relationships | Notes |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## State and Lifecycle Rules

[Status values, transitions, ownership, side effects, and invalid transitions.]

## Error Handling

[User-facing errors, API errors, retries, fallbacks, and empty states.]

## Observability and Operations

[Logs, metrics, tracing, admin tooling, alerts, data repair needs.]

## Testing Strategy

[Frontend, backend, integration, e2e, migration, security, and regression checks.]

## Collaboration Record

### Frontend Reviewer Summary
### Backend Reviewer Summary
### Second-Pass Review Summary
### Resolved Decisions
### Remaining Open Questions
### Assumptions

## Risks and Follow-Ups

[Known risks, deferred decisions, and recommended next steps.]
```

Keep tables compact but concrete. If an API request/response needs more detail than a table can hold, add fenced examples below the table.
