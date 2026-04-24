# Lead Import PRD

## Goal

Sales managers need to upload CSV files of leads, preview validation errors, and import valid rows into the CRM without creating duplicates.

## Users

- Sales manager: uploads and confirms imports.
- Sales representative: views assigned imported leads.
- Admin: configures duplicate matching rules.

## Scope

- Upload CSV files up to 20 MB.
- Validate required fields: company name, contact name, email, source, owner.
- Preview valid rows and invalid rows before import.
- Detect duplicates by normalized email first, then by company name plus contact name.
- Import valid rows in a background job after user confirmation.
- Show import history with status, counts, creator, created time, and downloadable error report.

## Status Lifecycle

- `uploaded`
- `validated`
- `importing`
- `completed`
- `completed_with_errors`
- `failed`

## Business Rules

- Invalid rows must not be imported.
- Duplicate rows should be skipped and included in the result report.
- A user may only assign leads to owners in their sales team.
- Import confirmation should be idempotent to avoid duplicate import jobs.

## Acceptance Criteria

- Manager can upload a CSV and see row-level validation errors.
- Manager can confirm an import and return later to see progress.
- The system prevents duplicate leads.
- Import history is filterable by status and creator.
- Error reports include row number, field, error code, and message.
