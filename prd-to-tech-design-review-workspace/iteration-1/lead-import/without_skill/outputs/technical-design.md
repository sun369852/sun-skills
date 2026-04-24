# Lead Import Technical Design

## 1. Context

This design is based on `fixtures/crm/specs/lead-import/prd.md`.

The feature lets sales managers upload CSV lead files, preview row-level validation and duplicate results, confirm an import, and return later to view status, counts, and downloadable error reports. Valid rows are imported asynchronously. Invalid and duplicate rows are excluded from lead creation and included in reports.

## 2. Frontend and Backend Agent Collaboration

### Frontend agent review

- The user flow should be split into four predictable surfaces: upload, validation preview, confirmation/progress, and import history.
- Validation preview must support large files by showing counts first and paginating row-level results instead of loading every row into the browser at once.
- Confirmation must be visibly idempotent: after the manager confirms, the UI disables repeat submission and treats repeat clicks or refreshes as a status lookup for the same import.
- Error report download should be available from both import detail and import history rows when report data exists.
- Filters for status and creator belong on the import history screen, with default sorting by newest created time.

### Backend agent review

- CSV parsing, validation, duplicate detection, and import execution should be server-owned so rules are consistent and cannot be bypassed by client manipulation.
- Upload creates an import batch in `uploaded`, then validation moves it to `validated` or `failed`.
- Confirmation must use an idempotency key or a unique import job constraint so one validated batch cannot enqueue multiple import jobs.
- Duplicate matching requires normalized email first, then normalized company name plus normalized contact name.
- Owner authorization must be checked per row against the creator's sales team before the row can be considered valid.

### Joint decisions

- Use a persistent `lead_import_batches` record as the aggregate root for upload, validation, confirmation, progress, counts, creator, and report access.
- Store parsed row outcomes in `lead_import_rows`; do not rely on temporary in-memory validation output.
- Use a background worker for both validation and import when file size or row count exceeds a quick synchronous threshold. The API remains the same either way.
- Preserve the PRD status lifecycle exactly: `uploaded`, `validated`, `importing`, `completed`, `completed_with_errors`, `failed`.
- Treat invalid rows and duplicate rows as non-importable rows. Invalid rows block only those rows, not the whole batch.

## 3. Goals and Non-Goals

### Goals

- Upload CSV files up to 20 MB.
- Validate required fields: company name, contact name, email, source, owner.
- Preview valid and invalid rows before import.
- Detect duplicates by normalized email, then company name plus contact name.
- Import valid non-duplicate rows in a background job after confirmation.
- Show filterable import history with status, counts, creator, created time, and downloadable error reports.
- Make import confirmation idempotent.

### Non-Goals

- Admin UI for configuring duplicate matching rules beyond supporting the rules required by this PRD.
- Real-time collaborative editing of import batches.
- Importing non-CSV formats.
- Creating new sales-team ownership models.

## 4. User Experience Design

### Screens

1. Lead Import Upload
   - CSV file picker.
   - File constraints shown near the picker: `.csv`, max 20 MB.
   - Upload progress and server-side validation status.
   - Upload errors for unsupported format, oversize file, malformed CSV, or server failure.

2. Validation Preview
   - Summary counters: total rows, valid rows, invalid rows, duplicate rows.
   - Tabs or segmented filters: all, valid, invalid, duplicate.
   - Paginated row table with row number, company name, contact name, email, source, owner, validation state, and messages.
   - Confirm import button enabled only when the batch is `validated` and has at least one importable row.

3. Import Progress and Detail
   - Status badge mapped to lifecycle values.
   - Counts for imported, skipped duplicate, invalid, failed, and total rows.
   - Error report download when invalid, duplicate, or failed row details exist.
   - Refresh or polling while status is `importing`.

4. Import History
   - Filter controls for status and creator.
   - Table columns: file name, status, counts, creator, created time, completed time, error report action.
   - Default sort: created time descending.

### Frontend state model

- `UploadState`: `idle | uploading | uploaded | validating | failed`.
- `BatchStatus`: mirrors backend lifecycle.
- `PreviewFilter`: `all | valid | invalid | duplicate`.
- `HistoryFilters`: status list, creator id, page, page size.

### Frontend API behavior

- Use server batch status as source of truth.
- On confirm, send an idempotency key stored with the batch interaction. If the request times out, fetch batch detail before retrying.
- Poll batch detail every 2-5 seconds while status is `uploaded` or `importing`, with backoff after repeated unchanged responses.

## 5. Backend Architecture

### Components

- `LeadImportController`: HTTP upload, preview, confirmation, history, report download.
- `LeadImportService`: batch creation, state transitions, authorization checks, idempotency handling.
- `CsvLeadParser`: streaming CSV parsing with row numbers and field normalization.
- `LeadImportValidator`: required-field checks, email format checks, owner/team checks.
- `DuplicateLeadDetector`: normalized email lookup first, then company/contact lookup.
- `LeadImportWorker`: validates uploaded batches and imports confirmed batches.
- `ErrorReportGenerator`: exports CSV report with row number, field, error code, and message.

### Processing flow

1. Manager uploads CSV.
2. API validates file extension, size, and content type, stores the raw file, and creates `lead_import_batches` with status `uploaded`.
3. Validation job parses rows, normalizes fields, applies required-field and owner authorization rules, performs duplicate checks, and stores row outcomes.
4. Batch status becomes `validated` when validation completes successfully, or `failed` if the file cannot be parsed or validation infrastructure fails.
5. Manager previews row outcomes.
6. Manager confirms import with an idempotency key.
7. Backend atomically moves the batch from `validated` to `importing` and enqueues exactly one import job.
8. Import job creates leads for rows marked `valid` and not duplicate.
9. Batch finishes as `completed` when all importable rows are created and no row-level import failures occurred, `completed_with_errors` when any row-level failures exist, or `failed` when the whole import job fails before reliable per-row processing.

## 6. Data Model

### `lead_import_batches`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID | Primary key |
| `file_name` | string | Original file name |
| `file_size_bytes` | integer | Must be <= 20 MB |
| `storage_key` | string | Raw CSV object location |
| `status` | enum | PRD lifecycle |
| `creator_id` | UUID | Uploading manager |
| `idempotency_key` | string nullable | Unique per confirmed batch |
| `total_count` | integer | Parsed data row count |
| `valid_count` | integer | Importable before execution |
| `invalid_count` | integer | Validation failures |
| `duplicate_count` | integer | Duplicate skips |
| `imported_count` | integer | Successfully created leads |
| `failed_count` | integer | Row-level import failures |
| `created_at` | timestamp | Upload time |
| `validated_at` | timestamp nullable | Validation completion |
| `confirmed_at` | timestamp nullable | Import confirmation |
| `completed_at` | timestamp nullable | Final completion |
| `failure_message` | text nullable | Batch-level failure |

Constraints:

- `status in ('uploaded', 'validated', 'importing', 'completed', 'completed_with_errors', 'failed')`.
- Unique partial index on `idempotency_key` where not null.
- Optional unique partial index on `id` where `status = 'importing'` for worker enqueue protection, depending on queue technology.

### `lead_import_rows`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID | Primary key |
| `batch_id` | UUID | References `lead_import_batches.id` |
| `row_number` | integer | CSV row number, excluding header policy documented in parser |
| `company_name` | string | Raw trimmed value |
| `contact_name` | string | Raw trimmed value |
| `email` | string | Raw trimmed value |
| `source` | string | Raw trimmed value |
| `owner_id` | UUID nullable | Resolved owner |
| `normalized_email` | string nullable | Lowercase canonical email |
| `normalized_company_name` | string nullable | Trimmed, collapsed whitespace, lowercase |
| `normalized_contact_name` | string nullable | Trimmed, collapsed whitespace, lowercase |
| `status` | enum | `valid`, `invalid`, `duplicate`, `imported`, `failed` |
| `duplicate_lead_id` | UUID nullable | Existing lead if duplicate |
| `created_lead_id` | UUID nullable | Created lead after import |
| `errors_json` | JSON | Row-level errors |
| `created_at` | timestamp | Row persisted time |
| `updated_at` | timestamp | Last state change |

Indexes:

- `(batch_id, status, row_number)` for preview pagination.
- `(batch_id, row_number)` unique.
- `(normalized_email)` on leads table if not already present.
- `(normalized_company_name, normalized_contact_name)` on leads table if not already present.

### Row error shape

```json
{
  "field": "email",
  "error_code": "REQUIRED",
  "message": "Email is required"
}
```

Common error codes:

- `REQUIRED`
- `INVALID_EMAIL`
- `OWNER_NOT_IN_TEAM`
- `DUPLICATE_EMAIL`
- `DUPLICATE_COMPANY_CONTACT`
- `IMPORT_FAILED`
- `MALFORMED_ROW`

## 7. API Design

### Upload CSV

`POST /api/lead-imports`

Request:

- `multipart/form-data`
- `file`: CSV, max 20 MB

Response `201`:

```json
{
  "batch_id": "uuid",
  "status": "uploaded"
}
```

Errors:

- `400` invalid file type or malformed multipart request.
- `413` file larger than 20 MB.
- `403` user cannot import leads.

### Get batch detail

`GET /api/lead-imports/{batch_id}`

Response `200`:

```json
{
  "batch_id": "uuid",
  "file_name": "leads.csv",
  "status": "validated",
  "counts": {
    "total": 1000,
    "valid": 910,
    "invalid": 45,
    "duplicate": 45,
    "imported": 0,
    "failed": 0
  },
  "creator": {
    "id": "uuid",
    "name": "Sales Manager"
  },
  "created_at": "2026-04-24T10:00:00Z",
  "validated_at": "2026-04-24T10:01:00Z",
  "completed_at": null
}
```

### Preview rows

`GET /api/lead-imports/{batch_id}/rows?status=invalid&page=1&page_size=50`

Response `200`:

```json
{
  "items": [
    {
      "row_number": 12,
      "company_name": "Acme",
      "contact_name": "",
      "email": "buyer@example.com",
      "source": "Webinar",
      "owner": null,
      "status": "invalid",
      "errors": [
        {
          "field": "contact_name",
          "error_code": "REQUIRED",
          "message": "Contact name is required"
        }
      ]
    }
  ],
  "page": 1,
  "page_size": 50,
  "total": 45
}
```

### Confirm import

`POST /api/lead-imports/{batch_id}/confirm`

Headers:

- `Idempotency-Key: <client-generated-key>`

Response `202`:

```json
{
  "batch_id": "uuid",
  "status": "importing"
}
```

Idempotency behavior:

- If the same batch and idempotency key are repeated, return the current batch status.
- If a different idempotency key is sent after the batch is already `importing` or terminal, return the current batch status without enqueueing another job.
- If the batch is not `validated`, return `409`.

### Import history

`GET /api/lead-imports?status=completed&creator_id=uuid&page=1&page_size=25`

Response `200`:

```json
{
  "items": [
    {
      "batch_id": "uuid",
      "file_name": "leads.csv",
      "status": "completed_with_errors",
      "counts": {
        "total": 1000,
        "valid": 910,
        "invalid": 45,
        "duplicate": 45,
        "imported": 908,
        "failed": 2
      },
      "creator": {
        "id": "uuid",
        "name": "Sales Manager"
      },
      "created_at": "2026-04-24T10:00:00Z",
      "completed_at": "2026-04-24T10:05:00Z",
      "has_error_report": true
    }
  ],
  "page": 1,
  "page_size": 25,
  "total": 1
}
```

### Download error report

`GET /api/lead-imports/{batch_id}/error-report`

Response:

- `200 text/csv`
- Columns: `row_number,field,error_code,message`
- Include invalid rows, duplicate rows, and row-level import failures.

## 8. Validation and Duplicate Rules

### Required fields

Rows are invalid when any of these fields are blank after trimming:

- company name
- contact name
- email
- source
- owner

### Email normalization

- Trim whitespace.
- Lowercase domain and local part.
- Reject invalid email syntax before duplicate lookup.

### Name normalization

- Trim leading and trailing whitespace.
- Collapse repeated internal whitespace.
- Lowercase for comparison.

### Duplicate detection order

1. If normalized email matches an existing lead, mark row as `duplicate` with `DUPLICATE_EMAIL`.
2. Otherwise, if normalized company name plus normalized contact name matches an existing lead, mark row as `duplicate` with `DUPLICATE_COMPANY_CONTACT`.
3. Otherwise, row can remain `valid` if no validation errors exist.

### Duplicate handling inside the same CSV

The same matching order applies within a batch. The first valid occurrence is importable; later rows that match the first occurrence are marked duplicate and skipped. This prevents the import itself from creating duplicates.

### Owner authorization

- Resolve the owner field to an owner account before marking a row valid.
- The creator may only assign owners in the creator's sales team.
- If owner cannot be resolved or is outside the team, mark the row invalid with `OWNER_NOT_IN_TEAM`.

## 9. State Transitions

Allowed transitions:

- `uploaded -> validated`
- `uploaded -> failed`
- `validated -> importing`
- `importing -> completed`
- `importing -> completed_with_errors`
- `importing -> failed`

Disallowed transitions return `409 Conflict` from command endpoints and are ignored by workers when stale jobs are detected.

Terminal states:

- `completed`
- `completed_with_errors`
- `failed`

## 10. Security and Permissions

- Only authenticated sales managers with import permission can upload and confirm imports.
- Sales representatives can view imported leads through existing lead access rules, not through unrestricted import batch access.
- Admins can view import history as allowed by existing CRM admin policy.
- Batch detail, preview rows, and reports require access to the batch creator's team or admin permission.
- Store uploaded files outside public web roots and serve reports through authenticated endpoints.
- Virus scanning can be added to the upload pipeline if the CRM platform already requires it for user-uploaded files.

## 11. Reliability and Concurrency

- Use streaming CSV parsing to avoid loading 20 MB files fully into application memory.
- Use database transactions for status changes and count updates.
- Use row-level bulk insert for validation outcomes.
- Use unique constraints or atomic compare-and-set updates for confirmation idempotency.
- Import worker should be retryable. On retry, skip rows already linked to `created_lead_id`.
- Leads table should enforce duplicate prevention with normalized unique indexes where business rules permit. If unique indexes cannot match configurable rules exactly, use transactional duplicate checks plus conflict handling.

## 12. Observability

Log structured events:

- `lead_import.uploaded`
- `lead_import.validation_started`
- `lead_import.validation_completed`
- `lead_import.confirmed`
- `lead_import.import_started`
- `lead_import.import_completed`
- `lead_import.failed`

Metrics:

- Upload count by status.
- Validation duration.
- Import duration.
- Rows processed per import.
- Duplicate ratio.
- Row failure ratio.

Alerts:

- Validation job failure spike.
- Import job failure spike.
- Queue latency above service target.

## 13. Testing Strategy

### Unit tests

- CSV parser handles headers, blank rows, malformed rows, and row numbers.
- Required-field validation produces correct field-level errors.
- Email and name normalization are deterministic.
- Duplicate detection honors email before company/contact.
- Owner authorization rejects owners outside the creator's sales team.
- State transition guard rejects illegal transitions.
- Idempotency handler never enqueues more than one job per batch.

### Integration tests

- Upload a valid CSV, preview valid rows, confirm import, and observe `completed`.
- Upload mixed valid, invalid, and duplicate rows, confirm import, and observe `completed_with_errors`.
- Confirm endpoint repeated with the same idempotency key returns current status without duplicate jobs.
- Import history filters by status and creator.
- Error report includes `row_number`, `field`, `error_code`, and `message`.

### Frontend tests

- Upload form enforces file selection and displays server errors.
- Preview screen renders counts and paginated row errors.
- Confirm button disables during submission and after accepted confirmation.
- History filters call the correct query params.
- Progress screen updates when batch status changes.

## 14. Rollout Plan

1. Add database tables and indexes behind a migration.
2. Implement backend upload, validation, preview, confirmation, history, and report endpoints.
3. Implement workers for validation and import.
4. Build frontend upload, preview, progress, and history screens.
5. Enable internally for admins and selected sales managers.
6. Monitor job failures, duplicate ratios, and report downloads.
7. Roll out to all sales managers after operational metrics are stable.

## 15. Open Questions

- What exact CSV header names and aliases should be accepted for required fields?
- How should the owner field be resolved: email, display name, employee ID, or CRM user ID?
- Are duplicate matching rules globally configured by admins or fixed for this first release?
- Should a file with zero importable rows be confirmable, or should confirmation be disabled?
- What retention period applies to raw uploaded CSV files and generated error reports?
