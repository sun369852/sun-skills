# Stage 4 Routing Rules

Use this reference after PRD approval to decide which stage 4 skills to run: `prd-quality-audit-standards`, `prd-task-archiver`, or both.

## Decision Table

| PRD / Feature Characteristics | Run audit-standards? | Run task-archiver? | Sequencing |
| --- | --- | --- | --- |
| Involves payments, billing, balance, or ledger | **Required** | Required | Parallel by default; formal tasks wait for tech design |
| Involves permissions, roles, or data visibility | **Required** | Required | Parallel |
| Involves data migration or backward-incompatible changes | **Required** | Required | Parallel |
| Involves external integrations or async callbacks | **Required** | Required | Parallel |
| Involves audit logs or compliance records | **Required** | Required | Parallel |
| Involves irreversible or destructive operations | **Required** | Required | Parallel |
| Multiple modules or runtime surfaces affected (frontend + backend + worker) | Recommended | **Required** | Run audit-standards in parallel with tech design; tasks after tech design |
| Single module, pure backend logic change | Recommended | **Required** | Audit-standards optional; tasks required |
| Single module, pure frontend UI change, no user data side effects | **Skip** (record lightweight acceptance notes) | **Required** | Tasks after tech design |
| Small bug fix or configuration change documented in PRD | **Skip** | **Required** | Task-archiver only |
| Internal tool / operational workflow, no external users | Recommended | **Required** | Audit-standards lightweight; tasks required |

## Routing Logic for Full-Auto Mode

In full-auto mode, the chain should:

1. Scan the PRD for risk signals: payment, permission, migration, integration, audit, irreversible operations.
2. If any signal is found → route to both audit-standards and task-archiver.
3. If no signal is found and the change is single-module → audit-standards is optional. The chain checks whether the technical design or delivery topology contract reveals hidden risks.
4. If the change is a pure UI or doc-only PRD → skip audit-standards. Record a note in delivery-chain-status.md explaining why.

## Integration with Fast Planning Mode

In fast planning mode:

- If both skills are required (risk signals present): run audit-standards and draft tasks in parallel. Reconcile tasks after tech design completes.
- If only task-archiver is needed: skip reconciliation step for audit-standards.
- After reconciliation, mark the chain status: `stage4-parallel-complete` or `stage4-task-only-complete`.

## Override Rules

- The user can explicitly request or skip audit-standards. User instruction overrides the decision table.
- If the chain envelope already specifies a route for stage 4, follow the envelope.
- When running in semi-auto mode, present the routing decision to the user with the recommendation from this table, but do not execute until confirmed.
