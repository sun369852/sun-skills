# Analytics Dashboard PRD

## Background

Operations managers need a dashboard for weekly order, revenue, refund, and fulfillment metrics. Today they export CSV files and combine them manually.

## Goals

- Provide a dashboard with order volume, revenue, refund rate, and fulfillment SLA charts.
- Support CSV export for the currently filtered dashboard data.
- Restrict dashboard access to operations managers and admins.

## Non-Goals

- Do not build custom chart editing.
- Do not support scheduled email reports in this release.
- Do not expose customer PII in exports.

## Users and Roles

| Role | Dashboard Access | Export Access |
| --- | --- | --- |
| Admin | Yes | Yes |
| Operations Manager | Yes | Yes |
| Support | No | No |

## Functional Requirements

1. Dashboard filters include date range, region, channel, and fulfillment status.
2. Charts include order volume by day, revenue by channel, refund rate by region, and fulfillment SLA by warehouse.
3. Empty states explain when filters return no data.
4. Loading states appear while metrics are being fetched.
5. Error states include retry for transient API errors.
6. CSV export respects all active filters and omits customer PII.
7. Unauthorized roles cannot access dashboard routes or export endpoints.

## Acceptance Criteria

- Admin and Operations Manager roles can view charts and export filtered CSV data.
- Support users receive an authorization error.
- Applying filters updates all charts consistently.
- CSV export contains only aggregate rows and no customer email, phone, address, or full name.
- Empty, loading, and API error states are visible in the UI.

## Assumptions

- Source metrics tables already exist.
- Time zone handling follows the existing reporting module.
