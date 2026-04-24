# Analytics Dashboard Task Archive

Source PRD: `D:/sun-skills/prd-task-archiver/evals/files/standalone-prds/analytics-dashboard-prd.md`

## Frontend Tasks

1. Build the analytics dashboard route and page shell for authorized users.
   - Scope: Admin and Operations Manager roles.
   - Exclude: Support role access.
   - Traceability: Goals; Users and Roles; Functional Requirement 7; Acceptance Criteria 1-2.

2. Implement dashboard filters for date range, region, channel, and fulfillment status.
   - Filters must update the dashboard query state.
   - Filter changes must refresh all charts from the same active filter set.
   - Traceability: Functional Requirement 1; Acceptance Criteria 3.

3. Render the required dashboard charts.
   - Order volume by day.
   - Revenue by channel.
   - Refund rate by region.
   - Fulfillment SLA by warehouse.
   - Traceability: Goals; Functional Requirement 2; Acceptance Criteria 1.

4. Add empty states for no-result filter combinations.
   - Empty states should explain that active filters returned no data.
   - Traceability: Functional Requirement 3; Acceptance Criteria 5.

5. Add loading states while metrics are being fetched.
   - Loading states should be visible for initial load and filter changes.
   - Traceability: Functional Requirement 4; Acceptance Criteria 5.

6. Add API error states with retry behavior.
   - Retry should refetch metrics for the currently active filters.
   - Traceability: Functional Requirement 5; Acceptance Criteria 5.

7. Add CSV export UI for authorized users.
   - Export action must use all active filters.
   - Export action should be unavailable or blocked for unauthorized roles.
   - Traceability: Goal 2; Functional Requirement 6-7; Acceptance Criteria 1-2.

## Backend Tasks

1. Add an authorization guard for analytics dashboard routes and APIs.
   - Allow Admin and Operations Manager.
   - Deny Support and other unauthorized roles.
   - Traceability: Goal 3; Users and Roles; Functional Requirement 7; Acceptance Criteria 1-2.

2. Implement a metrics query endpoint for dashboard data.
   - Accept date range, region, channel, and fulfillment status filters.
   - Use existing source metrics tables.
   - Follow the existing reporting module timezone behavior.
   - Traceability: Functional Requirement 1-2; Assumptions.

3. Return aggregate data series for all required charts.
   - Order volume grouped by day.
   - Revenue grouped by channel.
   - Refund rate grouped by region.
   - Fulfillment SLA grouped by warehouse.
   - Traceability: Functional Requirement 2; Acceptance Criteria 1 and 3.

4. Implement transient API error handling semantics.
   - Return errors in a shape the UI can display with retry.
   - Preserve authorization errors as distinct authorization failures.
   - Traceability: Functional Requirement 5 and 7; Acceptance Criteria 2 and 5.

5. Implement a filtered CSV export endpoint.
   - Respect date range, region, channel, and fulfillment status filters.
   - Include only aggregate rows.
   - Omit customer email, phone, address, full name, and other PII.
   - Traceability: Goal 2; Non-Goals; Functional Requirement 6; Acceptance Criteria 4.

6. Add backend route protection for export access.
   - Allow Admin and Operations Manager.
   - Deny Support and other unauthorized roles.
   - Traceability: Users and Roles; Functional Requirement 7; Acceptance Criteria 1-2.

## Testing Tasks

1. Add role-based access tests.
   - Verify Admin can view dashboard and export CSV.
   - Verify Operations Manager can view dashboard and export CSV.
   - Verify Support receives an authorization error for dashboard and export access.
   - Traceability: Users and Roles; Acceptance Criteria 1-2.

2. Add filter behavior tests.
   - Verify applying date range, region, channel, and fulfillment status filters updates all charts consistently.
   - Verify export requests include the same active filters.
   - Traceability: Functional Requirement 1; Acceptance Criteria 3.

3. Add chart data tests.
   - Verify order volume by day is returned and rendered.
   - Verify revenue by channel is returned and rendered.
   - Verify refund rate by region is returned and rendered.
   - Verify fulfillment SLA by warehouse is returned and rendered.
   - Traceability: Functional Requirement 2; Acceptance Criteria 1.

4. Add UI state tests.
   - Verify loading states appear during metrics fetches.
   - Verify empty states appear when filters return no data.
   - Verify transient API errors show retry.
   - Verify retry refetches metrics for the active filters.
   - Traceability: Functional Requirement 3-5; Acceptance Criteria 5.

5. Add CSV export safety tests.
   - Verify CSV contains only aggregate rows.
   - Verify CSV omits customer email, phone, address, and full name.
   - Verify CSV respects active dashboard filters.
   - Traceability: Non-Goals; Functional Requirement 6; Acceptance Criteria 4.

6. Add timezone regression tests around reporting boundaries.
   - Use the existing reporting module timezone behavior as the expected behavior.
   - Traceability: Assumptions.

## Release Tasks

1. Confirm source metrics tables are available in the target environment.
   - Traceability: Assumptions.

2. Confirm role mappings for Admin, Operations Manager, and Support are configured in production.
   - Traceability: Users and Roles; Functional Requirement 7.

3. Review CSV export fields before release.
   - Confirm no customer PII fields are included.
   - Confirm export contains only aggregate rows.
   - Traceability: Non-Goals; Acceptance Criteria 4.

4. Validate dashboard behavior in a staging environment.
   - Check charts, filters, loading states, empty states, error retry, authorization, and CSV export.
   - Traceability: Functional Requirements; Acceptance Criteria.

5. Prepare release notes.
   - Mention new operations analytics dashboard.
   - Mention filtered aggregate CSV export.
   - Mention access limited to Admin and Operations Manager roles.

6. Monitor post-release dashboard and export errors.
   - Watch metrics API failures, export failures, and authorization denials.
   - Use findings to catch transient API or permissions issues quickly.
