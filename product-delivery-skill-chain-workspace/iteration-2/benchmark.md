# Iteration 2 Benchmark

| Eval | Run | Passed | Total | Pass rate |
| --- | --- | ---: | ---: | ---: |
| requirement-entry | with_skill | 5 | 5 | 100% |
| requirement-entry | without_skill | 3 | 5 | 60% |
| prd-entry-default-stop | with_skill | 6 | 6 | 100% |
| prd-entry-default-stop | without_skill | 3 | 6 | 50% |
| fast-planning-reconcile | with_skill | 6 | 6 | 100% |
| fast-planning-reconcile | without_skill | 1 | 6 | 17% |
| resume-artifact-discovery | with_skill | 6 | 6 | 100% |
| resume-artifact-discovery | without_skill | 3 | 6 | 50% |
| tasks-entry-implementation-gate | with_skill | 5 | 5 | 100% |
| tasks-entry-implementation-gate | without_skill | 3 | 5 | 60% |
| direct-downstream-no-chain | with_skill | 4 | 4 | 100% |
| direct-downstream-no-chain | without_skill | 4 | 4 | 100% |

## Analyst Notes

- Fixture-backed evals made the chain value clearer: with-skill consistently produced `delivery-chain-status.md`, explicit gates, reconciliation records, or implementation handoff packets.
- Baseline was competitive on direct downstream usage and simple confirmation behavior, which is acceptable because the chain should not make single-skill usage harder.
- The strongest differentiators were fast planning reconciliation, resume mode, and task-entry implementation handoff.
- No skill source changes are required from iteration 2 results.
