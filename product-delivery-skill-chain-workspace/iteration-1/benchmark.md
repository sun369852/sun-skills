# Iteration 1 Benchmark

| Eval | Run | Passed | Total | Pass rate |
| --- | --- | ---: | ---: | ---: |
| requirement-entry | with_skill | 5 | 5 | 100% |
| requirement-entry | without_skill | 2 | 5 | 40% |
| prd-entry-default-stop | with_skill | 4 | 6 | 67% |
| prd-entry-default-stop | without_skill | 2 | 6 | 33% |
| fast-planning-reconcile | with_skill | 3 | 6 | 50% |
| fast-planning-reconcile | without_skill | 0 | 6 | 0% |
| resume-artifact-discovery | with_skill | 6 | 6 | 100% |
| resume-artifact-discovery | without_skill | 4 | 6 | 67% |
| tasks-entry-implementation-gate | with_skill | 4 | 5 | 80% |
| tasks-entry-implementation-gate | without_skill | 3 | 5 | 60% |
| direct-downstream-no-chain | with_skill | 4 | 4 | 100% |
| direct-downstream-no-chain | without_skill | 4 | 4 | 100% |

## Analyst Notes

- `with_skill` performed best on explicit chain behaviors: status file creation, conservative resume, fast-mode gate recording, and implementation confirmation.
- Baseline also handled many missing-file cases safely, so evals that reference nonexistent PRD/task paths have weak discrimination.
- Next iteration should add real fixture files for PRD, tasks, and status-file resume scenarios so downstream planning and reconciliation behavior can be tested beyond missing-path blocking.
