# Lead Import Technical Design

## Source

- PRD: `D:\sun-skills\prd-to-tech-design-review-workspace\fixtures\crm\specs\lead-import\prd.md`
- Project: Not inspected; no project implementation path was provided for compatibility review.
- Generated: 2026-04-24
- Collaboration mode: Inline frontend and backend reviewer simulation using the skill reviewer prompts. No external subagent runner was available in this environment.

## Executive Summary

Lead import will be implemented as a server-owned import workflow with a CSV upload step, server-side validation and duplicate detection, a review/preview step, idempotent confirmation, and a background import job. The frontend owns the upload, preview, confirmation, progress, history, and error-report download experience. The backend owns file parsing, validation, duplicate detection, team-owner authorization, idempotency, job execution, result reports, audit records, and import status transitions.

The design uses an `ImportBatch` aggregate with row-level records and errors. Validation produces a stable preview of valid, invalid, and duplicate rows before confirmation. Confirmation creates at most one import job per batch and idempotency key. Invalid rows are never imported; duplicate rows are skipped and represented in result counts and downloadable reports.

## PRD Scope Mapping

| PRD Requirement | Technical Coverage | Notes |
| --- | --- | --- |
| Upload CSV files up to 20 MB | Multipart upload endpoint, file size guard, CSV MIME/extension checks, server-side parsing | Size limit enforced before parsing and at storage boundary. |
| Validate required fields | Validation service checks company name, contact name, email, source, owner | Email normalization used for duplicate matching. |
| Preview valid and invalid rows | Review screen fetches row summaries and paginated row details by status | Duplicate rows are shown separately or as skipped rows with reasons. |
| Detect duplicates by normalized email, then company name plus contact name | Duplicate detector applies ordered matching rules with normalized fields and database indexes | Admin configuration can change rules only if allowed by product policy. Default order follows PRD. |
| Import valid rows in background after confirmation | Confirmation endpoint enqueues background job and moves batch to `importing` | Confirmation is idempotent. |
| Show import history with status, counts, creator, created time | Import history API supports status and creator filters | Counts include valid, invalid, duplicate, imported, skipped, and failed rows. |
| Downloadable error report | Report endpoint streams CSV with row number, field, error code, message | Includes validation errors, duplicates, and row-level import failures. |
| Invalid rows must not be imported | Import job reads only rows marked `valid` after validation | Revalidates status at job time to prevent stale imports. |
| Duplicate rows skipped and included in report | Duplicate rows get `duplicate` row status and report entries | Duplicates are not treated as fatal batch failures. |
| User may only assign leads to owners in their sales team | Owner authorization checked during validation and again before insert | Unauthorized owner produces row-level validation error. |
| Import confirmation idempotent | Unique job constraint on import batch plus idempotency key | Repeated confirmation returns existing job/batch state. |
| Admin configures duplicate matching rules | Admin route and API for duplicate rule configuration | Assumption: default matching remains PRD order unless Admin changes active rules. |

## Architecture Overview

Data flow:

1. Manager opens Lead Imports and uploads a CSV file.
2. Backend stores the file, creates an import batch in `uploaded`, parses rows, validates required fields and owner permissions, detects duplicates, stores row statuses/errors, and transitions the batch to `validated`.
3. Frontend shows counts, paginated valid/invalid/duplicate rows, and row-level errors.
4. Manager confirms the import. The confirm request carries an idempotency key.
5. Backend atomically transitions `validated` to `importing` and enqueues a background job, or returns the existing job if already confirmed.
6. The job imports only rows that are still valid, skips duplicate rows, records row-level failures, updates counts, writes the report, and transitions to `completed`, `completed_with_errors`, or `failed`.
7. Managers can leave and return through import history. Sales representatives see imported leads through existing CRM lead views.
8. Admins manage duplicate matching rules through an admin-only settings screen.

Core backend components:

- `ImportBatchService`: upload orchestration, status transitions, counts, audit.
- `CsvParsingService`: safe CSV parsing, header mapping, row extraction.
- `LeadImportValidationService`: required field, email format, source, owner-in-team checks.
- `DuplicateDetectionService`: normalized matching rules and duplicate references.
- `LeadImportJob`: background lead creation and result generation.
- `ErrorReportService`: report materialization and streaming.
- `DuplicateRuleService`: admin configuration for matching rules.

## Frontend Design

### Routes and Screens

| Route | Users | Purpose |
| --- | --- | --- |
| `/leads/imports` | Sales manager | Import history with status and creator filters. |
| `/leads/imports/new` | Sales manager | Upload CSV file and start validation. |
| `/leads/imports/:importId` | Sales manager | Preview counts, valid rows, invalid rows, duplicate rows, confirmation, progress, report download. |
| `/admin/lead-duplicate-rules` | Admin | Configure active duplicate matching rules. |

Sales representatives do not need a dedicated import UI. They view assigned imported leads in the existing CRM lead list/detail views.

### Component Structure

- `LeadImportHistoryPage`
- `LeadImportUploadPanel`
- `LeadImportStatusHeader`
- `LeadImportCountsSummary`
- `LeadImportRowsTable`
- `LeadImportErrorDrawer`
- `ConfirmImportDialog`
- `ErrorReportDownloadButton`
- `DuplicateRulesSettingsPage`

The row preview table should support tabs or segmented filters for `valid`, `invalid`, and `duplicate` rows. It should render row number, company name, contact name, email, source, owner, row status, and the highest-priority error or duplicate reason. A row details drawer can list all errors for a row without widening the table.

### Client State and Data Fetching

- Upload uses multipart form data and reports local file size/type errors before calling the server.
- After upload, the client navigates to the import detail route and polls the batch while status is `uploaded`, `validated` pending row hydration, or `importing`.
- Server state keys should separate batch summary from paginated rows:
  - `leadImport(id)`
  - `leadImportRows(id, status, page, pageSize)`
  - `leadImports(status, creator, page, pageSize)`
- Confirm import invalidates the batch summary, rows, history, and lead list caches.
- No optimistic lead creation is used. Import results are backend authoritative.
- If websocket or server-sent events exist in the project, they can replace polling for status updates; otherwise poll with backoff.

### UX States and Validation

- Upload disabled states: no file, file larger than 20 MB, non-CSV extension/MIME, upload in progress.
- Detail screen states:
  - `uploaded`: validation/parsing in progress, counts unavailable or partial.
  - `validated`: show preview and enable confirmation when at least one valid row exists.
  - `importing`: show progress and disable confirmation.
  - `completed`: show imported count and report link if available.
  - `completed_with_errors`: show imported/skipped/failed counts and report link.
  - `failed`: show batch failure message and report link if generated.
- Invalid rows must explain the field, error code, and message.
- Duplicate rows should show the matched rule and, when permitted, the existing lead reference.
- Confirmation dialog should state that invalid and duplicate rows will not be imported.
- Permission-denied states should distinguish lack of import permission from row-level owner assignment failures.

### Accessibility and Responsive Behavior

- File input must be keyboard accessible and expose selected file name and validation errors through accessible text.
- Tables should preserve row number and error severity at narrow widths, with secondary fields collapsed into expandable row details.
- Confirmation dialog must have focus trapping and return focus to the triggering button.
- Status changes should be announced in a non-intrusive live region when polling updates the page.
- Error report download controls must have text labels, not icon-only affordances.

## Backend Design

### Domain Model

- `ImportBatch`: one uploaded CSV import attempt owned by a creator.
- `ImportRow`: one parsed CSV row and its normalized values, validation status, duplicate status, and eventual lead reference.
- `ImportRowError`: one field-level or row-level error for preview and reports.
- `ImportJob`: background execution record for a confirmed batch.
- `DuplicateRule`: ordered matching rule configuration managed by Admin.
- `Lead`: existing CRM lead entity receiving imported rows.

### Data Storage and Migrations

Add tables or equivalent persistence:

- `lead_import_batches`
- `lead_import_rows`
- `lead_import_row_errors`
- `lead_import_jobs`
- `lead_duplicate_rules`

Indexes:

- `lead_import_batches(status, created_at)`
- `lead_import_batches(created_by, created_at)`
- `lead_import_rows(batch_id, row_status, row_number)`
- `lead_import_row_errors(batch_id, row_number)`
- `leads(normalized_email)` for duplicate matching
- `leads(normalized_company_name, normalized_contact_name)` for fallback duplicate matching
- unique `lead_import_jobs(batch_id)` or `lead_import_jobs(batch_id, idempotency_key)` depending on existing idempotency conventions

### Services and Business Rules

- Upload rejects files over 20 MB before persistence.
- CSV parsing must bound row count, column count, and field length using platform-safe limits. The PRD only specifies file size, so exact row/column limits are design assumptions to finalize during implementation.
- Required fields: `company_name`, `contact_name`, `email`, `source`, `owner`.
- Email normalization lowercases and trims email before duplicate matching.
- Company/contact normalization trims, collapses internal whitespace, and applies case-insensitive matching.
- Owner authorization validates that the target owner is in the creator manager's sales team.
- Duplicate detection order:
  1. normalized email
  2. normalized company name plus normalized contact name
- Duplicate rows are marked `duplicate` and not imported.
- Import job creates leads only from rows with row status `valid`.
- Row-level insert failures should not fail the entire batch unless the job cannot safely continue.
- Batch-level failures move the batch to `failed`; partial row failures move it to `completed_with_errors`.

### Background Jobs and Integrations

- `LeadImportJob` is queued on confirmation.
- The job should process rows in chunks to avoid long transactions and memory pressure.
- Each chunk should run in a transaction that inserts leads and records row outcomes.
- The job should be retryable for transient infrastructure failures, but lead creation must be idempotent by batch row ID to avoid duplicate leads on retry.
- Imported leads should include audit metadata linking back to the import batch and row.
- Error report generation can happen at the end of validation and again at job completion, or be generated on demand from row error tables.

### Security, Permissions, and Audit

- Sales managers can create and view their own imports, plus team imports if existing CRM permission policy allows it.
- Managers cannot assign rows to owners outside their sales team.
- Sales representatives only see resulting leads assigned to them through normal lead permissions.
- Admins alone can view/update duplicate matching rules.
- Uploaded files may contain personal data; store them in private storage, encrypt at rest if supported, and apply retention policy.
- Audit events:
  - `lead_import.uploaded`
  - `lead_import.validated`
  - `lead_import.confirmed`
  - `lead_import.completed`
  - `lead_import.failed`
  - `lead_duplicate_rules.updated`

## API Contract

| Method | Path | Purpose | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| `POST` | `/api/lead-imports` | Upload CSV and start validation | Multipart `file` | `ImportBatchSummary` | `400 invalid_file`, `413 file_too_large`, `415 unsupported_media_type`, `403 forbidden` |
| `GET` | `/api/lead-imports` | Import history | `status`, `creatorId`, pagination | paginated `ImportBatchSummary[]` | `403 forbidden` |
| `GET` | `/api/lead-imports/{id}` | Batch detail and counts | path `id` | `ImportBatchDetail` | `404 not_found`, `403 forbidden` |
| `GET` | `/api/lead-imports/{id}/rows` | Preview rows | `status`, pagination | paginated `ImportRowPreview[]` | `404 not_found`, `403 forbidden`, `400 invalid_filter` |
| `POST` | `/api/lead-imports/{id}/confirm` | Idempotently confirm import | header or body `idempotencyKey` | `ImportBatchDetail` | `409 invalid_status`, `422 no_valid_rows`, `403 forbidden` |
| `GET` | `/api/lead-imports/{id}/error-report` | Download error report CSV | path `id` | `text/csv` stream | `404 not_found`, `409 report_not_ready`, `403 forbidden` |
| `GET` | `/api/admin/lead-duplicate-rules` | Read duplicate rules | none | `DuplicateRule[]` | `403 forbidden` |
| `PUT` | `/api/admin/lead-duplicate-rules` | Update duplicate rules | ordered rule list | `DuplicateRule[]` | `400 invalid_rules`, `403 forbidden` |

Example `ImportBatchDetail`:

```json
{
  "id": "imp_123",
  "status": "validated",
  "fileName": "leads.csv",
  "createdBy": { "id": "usr_1", "name": "Avery Manager" },
  "createdAt": "2026-04-24T10:00:00Z",
  "counts": {
    "totalRows": 1200,
    "validRows": 1000,
    "invalidRows": 120,
    "duplicateRows": 80,
    "importedRows": 0,
    "failedRows": 0
  },
  "canConfirm": true,
  "reportAvailable": true
}
```

Example `ImportRowPreview`:

```json
{
  "id": "row_456",
  "rowNumber": 42,
  "status": "invalid",
  "fields": {
    "companyName": "Example Co",
    "contactName": "",
    "email": "buyer@example.com",
    "source": "Conference",
    "owner": "Sam Rep"
  },
  "errors": [
    {
      "field": "contact_name",
      "errorCode": "required",
      "message": "Contact name is required."
    }
  ]
}
```

## Data Model

| Entity/Table | Fields | Relationships | Notes |
| --- | --- | --- | --- |
| `lead_import_batches` | `id`, `file_name`, `file_size`, `file_storage_key`, `status`, counts, `created_by`, `created_at`, `updated_at`, `confirmed_at`, `completed_at`, `failure_reason` | has many rows, errors, jobs | Status is backend controlled. |
| `lead_import_rows` | `id`, `batch_id`, `row_number`, raw fields, normalized fields, `owner_id`, `row_status`, `duplicate_lead_id`, `imported_lead_id`, timestamps | belongs to batch; may reference lead | Row status examples: `valid`, `invalid`, `duplicate`, `imported`, `failed`. |
| `lead_import_row_errors` | `id`, `batch_id`, `row_id`, `row_number`, `field`, `error_code`, `message`, `severity` | belongs to row/batch | Drives preview and error report. |
| `lead_import_jobs` | `id`, `batch_id`, `idempotency_key`, `status`, `attempt_count`, `started_at`, `completed_at`, `last_error` | belongs to batch | Unique constraint prevents duplicate jobs. |
| `lead_duplicate_rules` | `id`, `rule_type`, `priority`, `enabled`, `updated_by`, `updated_at` | used by duplicate detector | Defaults to email then company/contact. |
| `leads` | existing lead fields plus normalized duplicate keys and import audit fields | may reference import batch/row | Existing CRM model extended as needed. |

## State and Lifecycle Rules

Batch statuses from the PRD:

| From | To | Trigger | Rule |
| --- | --- | --- | --- |
| none | `uploaded` | CSV accepted | File is stored and batch is created. |
| `uploaded` | `validated` | Parsing, validation, duplicate scan complete | Counts and row previews are available. |
| `validated` | `importing` | Manager confirms import | Only allowed when valid row count is greater than 0. |
| `importing` | `completed` | Job imports all valid rows without row failures | Duplicate and invalid rows remain skipped. |
| `importing` | `completed_with_errors` | Some valid rows fail during import, or skipped duplicates exist in final report | User can download report. |
| `uploaded`, `validated`, `importing` | `failed` | Batch-level parsing, validation infrastructure, or job failure | Failure reason is stored and visible. |

Invalid transitions return `409 invalid_status`. Repeated confirmation for an already confirmed batch returns the current import state when the idempotency key matches or when the batch already has a job.

## Error Handling

User-facing errors:

- File too large: "CSV files must be 20 MB or smaller."
- Unsupported file: "Upload a CSV file."
- Validation in progress timeout: "Validation is taking longer than expected. You can leave and return from import history."
- No valid rows: "There are no valid rows to import."
- Permission denied: "You do not have permission to perform this import."
- Owner outside team: row-level `owner_not_in_team`.
- Duplicate lead: row-level `duplicate_email` or `duplicate_company_contact`.
- Report not ready: "The report is still being generated."

API errors should include stable `errorCode`, human-readable `message`, and optional `details`. Row errors must include row number, field, error code, and message to satisfy the PRD report requirement.

## Observability and Operations

- Structured logs include `importBatchId`, `jobId`, `createdBy`, `status`, row counts, and duration.
- Metrics:
  - upload accepted/rejected counts
  - validation duration
  - import job duration
  - rows processed/imported/skipped/failed
  - duplicate detection rate
  - job retry count
  - report generation failures
- Alerts:
  - repeated job failures
  - validation backlog above threshold
  - report generation failures
  - import job stuck in `importing`
- Operational tooling should allow an authorized admin/operator to inspect a failed batch, re-run failed job steps when safe, and download reports.
- Retention policy for uploaded source files and generated reports is an open product/ops question.

## Testing Strategy

Frontend:

- Upload form rejects oversized and non-CSV files before submission.
- Import detail renders all status states and count combinations.
- Row preview filters valid, invalid, and duplicate rows with pagination.
- Confirmation is disabled for no valid rows and during import.
- History filters by status and creator.
- Error report button handles ready and not-ready states.
- Accessibility checks for file input, table navigation, dialog focus, and live status updates.

Backend:

- File size and media validation.
- CSV parsing with malformed rows, missing headers, blank required fields, and large allowed files.
- Required field validation and email normalization.
- Owner-in-team authorization.
- Duplicate matching by email first, then company/contact.
- Idempotent confirmation under repeated and concurrent requests.
- Import job imports only valid rows and skips invalid/duplicate rows.
- Job retry does not create duplicate leads.
- Status transitions reject invalid transitions.
- Error report includes row number, field, error code, and message.
- Admin duplicate rule authorization and validation.

Integration and e2e:

- Upload -> validation preview -> confirm -> background completion -> history -> report download.
- Duplicate rows against existing leads and within the same file.
- Manager attempting to assign a lead outside their team.
- Repeated confirm requests with same idempotency key.
- Partial import failure resulting in `completed_with_errors`.

## Collaboration Record

### Frontend Reviewer Summary

The frontend needs a clear multi-screen flow: upload, validation preview, confirmation, progress, history, and report download. It needs stable status values, row-level pagination/filtering, counts, permission-aware controls, and deterministic error payloads. The UI should not optimistically create leads because the import job and duplicate checks are backend authoritative. The preview table should separate invalid and duplicate rows so managers understand what will not be imported.

### Backend Reviewer Summary

The backend should model import as a batch aggregate with durable row records, row errors, idempotent confirmation, and a retryable background job. Duplicate detection must use normalized keys and enforce the PRD's order. Owner assignment is a security rule, not only UI validation. Batch and row states must be persisted for history, reports, retry safety, and auditability.

### Exchange Notes

- Frontend requested paginated row details by status. Backend accepts because storing row records is already required for reports.
- Backend requested no optimistic lead creation. Frontend accepts and will rely on polling or realtime updates.
- Frontend requested duplicate reason and existing lead reference. Backend can return a reference only when the viewer has permission to see the matched lead.
- Backend requested confirmation idempotency. Frontend will generate and send an idempotency key and handle existing-job responses as success.
- Both sides agree that invalid rows and duplicate rows should be previewed and excluded from import.

### Resolved Decisions

- Validation and duplicate detection are server-side and persisted before confirmation.
- Confirmation creates or returns one job per batch and idempotency key.
- Row preview API supports status filtering and pagination.
- The import job processes only `valid` rows.
- Duplicate rows are skipped and included in counts and reports.
- Admin duplicate rules default to normalized email first, then company/contact.
- Error report schema is CSV with row number, field, error code, and message.

### Remaining Open Questions

- What retention period should apply to uploaded CSV files and generated reports?
- Should managers view only their own imports or all imports created by managers in their sales team?
- Are duplicate matching rules fully configurable by Admin, or only enable/disable/reorder the PRD-defined rules?
- What exact CSV header aliases are accepted for the required fields?
- What is the maximum row count, column count, and field length within the 20 MB file limit?

### Assumptions

- Existing CRM authentication, role, team, lead, and audit systems are available.
- A background job framework and private file storage are available or will be introduced.
- `completed_with_errors` is used when any valid row fails during import and may also be used when final report contains skipped rows; product should confirm whether duplicates alone should make the final status `completed` or `completed_with_errors`.
- Duplicate detection compares against existing leads and, during validation, against earlier rows in the same uploaded file.
- Report downloads are authorized using the same visibility policy as import batch detail.

## Risks and Follow-Ups

- Duplicate rule configurability can conflict with the PRD's fixed matching order. Keep PRD defaults and require product confirmation before allowing arbitrary rule changes.
- Large CSV validation can be slow. Use async validation or bounded synchronous processing with clear progress states.
- Idempotency and retry behavior must be tested under concurrency to avoid duplicate lead creation.
- Owner authorization can become stale between validation and import. Recheck ownership/team permissions immediately before insertion.
- Personal data in uploads and reports requires retention, encryption, and access-control decisions before production rollout.
