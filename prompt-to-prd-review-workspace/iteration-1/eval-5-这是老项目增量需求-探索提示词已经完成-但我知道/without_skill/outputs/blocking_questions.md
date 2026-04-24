# Blocking Questions

The final PRD was not saved because these questions affect product semantics, audit/compliance behavior, or implementation scope.

1. Which behavior is authoritative: the old documentation saying invoice email can only be sent once, or the current online support process that already allows manual resend?

2. Should the new finance/admin resend capability impose a daily resend limit?
   - If yes: define limit count, time window, scope, and whether privileged roles can override it.
   - If no: explicitly state that MVP has no daily cap, but every attempt must be audited.

3. What recipient email policy should the resend use?
   - Original invoice recipient only
   - Editable recipient entered by finance/admin staff
   - Selectable from customer/order contact emails

4. Which roles are allowed to resend electronic invoice email?
   - Finance admin only
   - Customer service only
   - Finance admin plus customer service
   - Other scoped permission

5. Should failed resend attempts be recorded in the same audit trail as successful attempts?

## Non-Blocking Draft Direction

If the product owner confirms current manual resend is intended behavior and chooses "no daily limit for MVP", the PRD can proceed with this default:

- Only finance/admin backend gets the resend action.
- Only successfully issued electronic invoices are eligible.
- Resend never changes invoice number, amount, title, issued status, or invoice payload.
- Each resend attempt records operator, time, recipient email, result, and failure reason if any.
- User-side product has no new entry.

