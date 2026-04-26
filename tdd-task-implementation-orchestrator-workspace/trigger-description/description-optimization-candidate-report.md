# Description Trigger Evaluation Report

- Skill: `tdd-task-implementation-orchestrator`
- Model: `sonnet`
- Input: `D:\sun-skills\tdd-task-implementation-orchestrator-workspace\trigger-description\trigger-eval-3run-optimized.json`
- Runs per query: `3`
- Trigger threshold: `0.5`
- Timeout seconds: `35`
- Generated: `2026-04-26T16:34:07`
- Description label: candidate with exact missed phrases, evaluated with 3 runs per query

## Summary

- Overall: `18/20` (90.0%)
- Precision: `100.0%`
- Recall: `80.0%`
- Specificity: `100.0%`
- True positives: `8`
- False negatives: `2`
- True negatives: `10`
- False positives: `0`

## Failures

- Eval 6: expected `True`, actual `False`, rate `0.00`
  Query: 请执行 specs/auth/tasks.md 里的开发任务，PRD 和架构文档同目录。权限相关任务必须补测试，小的文案任务可以轻量验证，全部记录到 implementation run log。
- Eval 10: expected `True`, actual `False`, rate `0.00`
  Query: Use the implementation plan in feature/foo/tasks.md plus the existing PRD/design docs to code the feature. Create a branch, use worktrees if useful, and commit each verified batch locally.

## Unstable Items

- Eval 5: trigger runs [False, True, True]
  Query: repo 里有 openspec/changes/add-billing/spec.md 和 tasks.md，技术设计也在 docs/billing-design.md。请从任务清单开始 TDD 开发，按任务批次提交 commit。

## Recommendation

- Consider adding narrow trigger phrases for missed positive cases, but avoid broad wording that pulls in PRD/design/task-generation requests.
