# Downstream Invocation Envelope

Use this reference before invoking any downstream skill from `product-delivery-skill-chain`.

## Core Rule

Every downstream invocation from the chain must include the confirmed contract constraints and output paths that matter to that downstream stage. Downstream skills keep their own domain rules, but they must not override disabled subagents, disabled commits, implementation confirmation, or explicit output paths from the chain contract.

## Envelope

Use this structure in the handoff prompt or packet:

```markdown
## Downstream Invocation Envelope
- Chain contract path:
- Status file path:
- Artifact directory:
- Source archive:
- Source context:
- Delivery topology contract:
- Entry stage:
- Target / stop point:
- Subagent policy:
- Parallel policy:
- Handoff gate result:
- Backtrack policy:
- Implementation confirmation:
- High-risk operations:
- Git policy:
- Minimum verification gates:
  - Build/package:
  - Backend startup smoke:
  - Frontend build smoke:
  - Public endpoint smoke:
  - Protected endpoint unauthorized smoke:
  - Changed API smoke:
- Output paths:
  - PRD:
  - Technical design:
  - Audit standards:
  - Task archive:
  - Implementation run log:
  - Review report:
- Source artifacts:
  - PRD:
  - Technical design:
  - Delivery topology contract:
  - Task archive:
  - Audit standards:
- Constraints:
  - Do not override disabled subagents:
  - Do not override disabled commits:
  - Do not push or create PR unless authorized:
  - Do not ask about high-risk operations when policy is `no-confirmation`; record the decision and choose a conservative or blocked path if safe execution is not possible:
  - Do not report product startup or runnable status from ports alone; validate every MVP-required runtime surface in the topology contract:
  - Do not write outside output paths unless user confirms:
  - Handoff gate result (`GATE_PASS`, `GATE_PASS_WITH_NOTES`, or `GATE_BLOCKED` — if blocked, this envelope should not be sent):
  - Backtrack policy (`bounded-bug`, `controlled-upstream`, or `stop-and-ask`):
```

## Stage-Specific Notes

- `prompt-to-prd-review`: pass the PRD output path and subagent policy.
- `prd-to-tech-design-review`: pass PRD source, technical-design output path, subagent policy, and parallel policy.
- `prd-quality-audit-standards`: pass PRD source, audit-standards output path, and parallel policy.
- `prd-task-archiver`: pass PRD source, delivery topology contract, task output path, and technical design as an implementation constraint when available.
- `tdd-task-implementation-orchestrator`: pass tasks, PRD/design/audit-standards sources, delivery topology contract, implementation confirmation, high-risk operations policy, minimum verification gates, git policy, run-log path, and worker/subagent policy.
- `implementation-review-handoff`: pass review scope, source artifacts, delivery topology contract, audit standards, run log, review report path, review-fix loop policy, and high-risk operations policy.

High-risk operations policy values are `explicit-only`, `ask-with-risk-summary`, and `no-confirmation`.

Minimum verification gates are conditional on touched surface, not always mandatory. Use them to prevent compile-only completion:

- backend runtime/config/DI/mapper/migration touched: backend startup smoke
- auth/security/filter/interceptor/middleware touched: protected endpoint unauthorized smoke
- API/controller/route touched: changed API smoke and public endpoint smoke when applicable
- frontend route guard/request client/build config touched: frontend build smoke and route/client smoke when practical
- audit standards TE/RG checks exist for the batch: include the relevant checks in the implementation handoff

## Enforcement

If a downstream skill's default behavior conflicts with the envelope, follow the envelope. If the conflict would block the downstream skill from doing required work, stop and ask the user rather than silently weakening the contract.
