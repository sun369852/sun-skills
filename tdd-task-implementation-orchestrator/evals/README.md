# Evaluation Notes

## Files

- `evals.json`: functional behavior eval prompts and expectations.
- `trigger-evals.json`: description trigger eval set with should-trigger and should-not-trigger cases.
- `run_trigger_eval_windows.py`: optional Windows-compatible trigger runner.

## Trigger Eval Safety

`run_trigger_eval_windows.py` calls the local `claude` CLI. That sends the skill description and eval queries to the configured model provider. Run it only when this external data transfer is acceptable.

Example:

```powershell
$env:PYTHONUTF8='1'
py .\evals\run_trigger_eval_windows.py `
  --eval-set .\evals\trigger-evals.json `
  --skill-path . `
  --model sonnet `
  --timeout 90 `
  --output ..\tdd-task-implementation-orchestrator-workspace\trigger-description\windows-trigger-eval.json
```

## Known Issue

The upstream `a-skill-creator/scripts/run_eval.py` uses `select.select()` on subprocess stdout. On Windows pipes this can fail with `WinError 10038`. Use the local sequential runner above when working on Windows.

The workspace directory `tdd-task-implementation-orchestrator-workspace/trigger-description/2026-04-26_055356/` was produced by the upstream runner and should be treated as an invalid diagnostic run if it shows all positive trigger cases failing with `WinError 10038`.

## Recorded Trigger Runs

Manual Windows runner results:

- `windows-trigger-eval.json`: invalid first run; the trigger detector was too broad and counted any mention of the temporary skill name.
- `windows-trigger-eval-after-description-update.json`: 19/20 passed. All 10 negative cases passed; 9/10 positive cases triggered.
- `windows-trigger-eval-final.json`: 17/20 passed in a later single-run sample. All 10 negative cases passed; 7/10 positive cases triggered. Treat this as variance from one run per query plus timeout sensitivity, not as a better description.
- `trigger-eval-3run.json`: 18/20 passed using 3 runs per query. Precision 100%, recall 80%, specificity 100%.
- `trigger-eval-3run-optimized.json`: 18/20 passed after a candidate description tweak. It did not improve score and worsened the two false-negative trigger rates, so the candidate was rejected.

The retained `SKILL.md` description is the conservative version associated with the 19/20 single-run result and the better 3-run false-negative trigger rates.

Formal report:

`tdd-task-implementation-orchestrator-workspace/trigger-description/description-optimization-formal-report.md`

## Functional Evals

`evals.json` currently defines behavior expectations for realistic prompts. To run full functional benchmarks, create fixture repositories or input file bundles for each eval under `evals/files/`, then update each eval's `files` array. Without fixtures, prompts that reference paths such as `docs/tasks.md` primarily test missing-file handling rather than implementation orchestration quality.
