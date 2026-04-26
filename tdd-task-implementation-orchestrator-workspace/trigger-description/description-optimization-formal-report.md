# Description Optimization Formal Report

## Scope

Skill: `tdd-task-implementation-orchestrator`

Goal: evaluate whether the skill description triggers for development-execution prompts and avoids triggering for adjacent non-execution prompts such as PRD writing, technical design, task decomposition, code review, tiny bug fixes, translation, and learning questions.

## Eval Set

- File: `D:\sun-skills\tdd-task-implementation-orchestrator\evals\trigger-evals.json`
- Total queries: 20
- Should trigger: 10
- Should not trigger: 10
- Near-miss negatives included: PRD generation, technical design generation, task decomposition, code review, tiny bug fix, description eval generation, vague task refinement, TDD explanation, PRD translation, CI analysis.

## Method

The Windows-compatible runner was used because the upstream `a-skill-creator/scripts/run_eval.py` uses `select.select()` on subprocess stdout, which fails on Windows pipes with `WinError 10038`.

Runner:

`D:\sun-skills\tdd-task-implementation-orchestrator\evals\run_trigger_eval_windows.py`

Grader:

`D:\sun-skills\tdd-task-implementation-orchestrator\evals\grade_trigger_eval.py`

The 3-run evaluation uses:

- Model: `sonnet`
- Runs per query: 3
- Trigger threshold: 0.5
- Timeout: 35 seconds

The runner detects actual `Skill` or `Read` tool use targeting the temporary command file. It does not count ordinary text mentions of the skill name.

## Results

### Retained Description

Input:

`D:\sun-skills\tdd-task-implementation-orchestrator-workspace\trigger-description\trigger-eval-3run.json`

Report:

`D:\sun-skills\tdd-task-implementation-orchestrator-workspace\trigger-description\description-optimization-report.md`

Metrics:

- Overall: 18/20, 90.0%
- Precision: 100.0%
- Recall: 80.0%
- Specificity: 100.0%
- True positives: 8
- False negatives: 2
- True negatives: 10
- False positives: 0

Failures:

- Eval 6: Chinese prompt phrased as "execute specs/auth/tasks.md development tasks; PRD and architecture docs are in the same directory"
- Eval 10: English prompt phrased as "Use the implementation plan in feature/foo/tasks.md plus existing PRD/design docs to code the feature"

Unstable positives:

- Eval 5: 2/3 triggered
- Eval 6: 1/3 triggered
- Eval 10: 1/3 triggered

### Candidate Description

Input:

`D:\sun-skills\tdd-task-implementation-orchestrator-workspace\trigger-description\trigger-eval-3run-optimized.json`

Report:

`D:\sun-skills\tdd-task-implementation-orchestrator-workspace\trigger-description\description-optimization-candidate-report.md`

Metrics:

- Overall: 18/20, 90.0%
- Precision: 100.0%
- Recall: 80.0%
- Specificity: 100.0%
- True positives: 8
- False negatives: 2
- True negatives: 10
- False positives: 0

The candidate added more exact wording for the two missed positives. It did not improve aggregate score, and the two missed positives dropped from 1/3 trigger rate to 0/3 trigger rate. It was rejected.

## Decision

Keep the retained description.

Reasoning:

- It preserves 100% precision and 100% specificity on this eval set.
- It has the same 90% overall score as the candidate under 3-run evaluation.
- It performed better than the candidate on the two unstable false-negative cases by trigger rate.
- For this execution-only skill, false positives are more harmful than false negatives because mis-triggering on PRD/design/task-generation requests would route the user into the wrong workflow.

## Residual Risk

The two remaining false negatives are both positive execution prompts but use less direct wording than the strongest trigger examples. Further description broadening may improve recall, but it risks pulling in task-decomposition or code-review near misses.

Many runs timed out at 35 seconds after partial stream parsing. The trigger decision is still useful because the runner detects early tool-use events, but future formal evaluation could use a longer timeout to reduce uncertainty.

## Recommendation

Do not change the description further until a real project trial shows under-triggering in normal use. The current boundary is conservative and appropriate for a development-execution-only skill.
