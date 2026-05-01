# Delivery Summary Template

Use this template when a full chain or partial chain reaches its final stop point. Generate `<chain-dir>/delivery-summary.md` as the final human-readable overview of what happened, what was produced, and what risk remains.

Do not generate this file for single-skill invocations or mid-chain stops. Only generate it when the chain is terminating at its target stop point.

## Template

```markdown
# 链路交付摘要

## 基本信息
- 链路入口:
- 目标/停止点:
- 执行模式:
- 阶段总数（含回溯）:
- 回溯次数:
- 门禁结果:

## 阶段执行概况

| 阶段 | 状态 | 主要产物 | 门禁结果 |
| --- | --- | --- | --- |
| 需求澄清 | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |
| PRD | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |
| 技术设计 | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |
| 审核标准 | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |
| 任务拆解 | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |
| 开发 | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |
| 审核 | done/skipped/backtracked | path | GATE_PASS / GATE_BLOCKED |

## 最终产物清单

| 产物 | 路径 | 状态 |
| --- | --- | --- |
| PRD | | 已生成 / 跳过 / 回溯修复 |
| 技术设计 | | 已生成 / 跳过 / 回溯修复 |
| 审核标准 | | 已生成 / 跳过 / 回溯修复 |
| 任务归档 | | 已生成 / 跳过 / 回溯修复 |
| 运行日志 | | 路径 |
| 审核报告 | | 路径 |

## 关键决策记录

- [决策 1]
- [决策 2]

## 残留风险

| 风险 | 来源 | 建议处理 |
| --- | --- | --- |
| | | |

## 回溯事件（如有）

| 事件 | 触发 | 目标 | 结果 |
| --- | --- | --- | --- |
| | | | |

## 门禁记录

| 门禁 | 结果 | 备注 |
| --- | --- | --- |
| PRD → 技术设计 | GATE_PASS / GATE_BLOCKED | |
| 任务 → 开发 | GATE_PASS / GATE_PASS_WITH_NOTES | |
```

## Generation Rule

Fill only the sections that are relevant. If no backtracking occurred, omit the backtrack events table. If no gate was blocked, omit the gate notes column.
