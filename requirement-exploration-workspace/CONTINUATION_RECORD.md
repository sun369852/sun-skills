# requirement-exploration 项目续写记录

## 项目背景
- 这是一个持续优化 Claude Code skill `requirement-exploration` 的项目。
- 目标不是生成需求文档本身，而是让 skill 在“需求探索 / closeout review”场景里更稳定地判断：
  - 什么时候应该继续追问
  - 什么时候只剩 non-blocking gap，可以显式带默认边界继续
  - 什么时候存在真正 blocking gap，必须停住等待用户确认
- 主工作流标准以 `document-skills:skill-creator` 为准；`superpowers` 只在必要时辅助，不作为主流程。

## 当前稳定状态
- 当前建议默认基线：`iteration-17`
- 当前稳定 benchmark：
  - with_skill mean pass_rate: `1.0`
  - without_skill mean pass_rate: `0.63`
  - delta pass_rate: `+0.37`
- 对应文件：
  - `C:/Users/sun/.claude/skills/requirement-exploration-workspace/iteration-17/benchmark.md`
  - `C:/Users/sun/.claude/skills/requirement-exploration-workspace/iteration-17/benchmark.json`

## 已验证有效的规则边界
当前 skill 已稳定区分下面两类 late-stage 情况：

### 1. 必须阻塞的问题
若未确认会改变以下语义，应视为 blocking gap，不能代答后继续：
- 核心业务对象含义
- 记录 ownership / identity
- 状态流转语义
- 历史记录解释语义

典型通过样本：
- `certificate-module-single-blocking-gap`
- `entitlement-record-identity-migration`
- `entitlement-snapshot-history-freeze`

### 2. 可以显式默认并继续的问题
若只是普通 V1 经营/实现边界，通常仍属 non-blocking，可显式写默认边界后继续请求生成授权：
- stacking policy
- threshold calculation
- stock deduction timing
- reporting / statistics definitions
- default export scope
- 其他不会改写核心对象/身份/状态/历史解释的业务默认项

典型通过样本：
- `coupon-module-late-stage-defaults`

## 当前样本覆盖类别
目前样本大致覆盖 5 类情况：
1. early insufficient-info
2. late-stage non-blocking closeout
3. late-stage boundary review
4. late-stage single blocking gap
5. explicit generation authorization

## 当前工作方式
后续继续优化时，优先遵守这些约束：
- 以 `skill-creator` 为主流程
- 优先扩 eval / 修 grading / 看 benchmark，再决定是否改 `SKILL.md`
- 只做最小规则补丁，避免大改 prompt
- 保留 `with_skill` / `without_skill` 对照
- 新增样本要尽量“单一变量”，每个样本最好只保留 1 个真正 blocking gap
- 若 benchmark 与直读 `response.txt` 冲突，优先核对 `grading.json` 和 `GRADING_SPECS`，防止误判是规则退化，其实只是人工判分脚本陈旧

## 已知关键经验
- iteration-15 曾出现 benchmark 看起来很好，但实际上：
  - `event-registration-vague-authorization` 被遗漏出汇总
  - `coupon-module-late-stage-defaults` 的 grading 结论陈旧
- iteration-17 的最终稳定不是因为再次改规则，而是因为修正了陈旧 grading，并确认真实输出已恢复正常
- 因此后续看到“疑似回归”时，先排查：
  1. 是否样本没纳入汇总
  2. 是否 `GRADING_SPECS` 沿用了上轮 truth values
  3. 是否 benchmark 是旧产物，未按顺序重跑 run -> grade

## 后续优化的优先顺序
1. 先确认是不是评测工件问题，不要一上来就改 skill 规则
2. 若要扩覆盖，优先补“贴近现有边界、但不重复”的 late-stage 样本
3. 只有在新样本暴露出稳定失败模式时，再对 `SKILL.md` 做第二个最小补丁

## 未来继续此项目时可直接复用的标准提示词

### 模板 A：继续迭代优化
```text
我在继续优化 Claude Code skill `requirement-exploration`。

工作目录：
- skill: C:/Users/sun/.claude/skills/requirement-exploration
- workspace: C:/Users/sun/.claude/skills/requirement-exploration-workspace

当前稳定基线是 iteration-17，不要从头重做。请先阅读：
- iteration-17/benchmark.md
- iteration-17/benchmark.json
- SKILL.md
- evals/evals.json

当前已知稳定状态：
- with_skill pass_rate = 1.0
- without_skill pass_rate = 0.63
- delta = +0.37

工作要求：
- 以 `document-skills:skill-creator` 为主流程
- 只在必要时使用 `superpowers`
- 优先扩 eval / 修 grading / 跑 benchmark，再决定是否改 `SKILL.md`
- 只接受最小规则补丁，不做大改
- 如果 benchmark 和 response.txt 冲突，先检查 grading 脚本是否陈旧

请先判断：下一步最应该做的是扩样本、修评测，还是改规则；然后直接继续执行。
```

### 模板 B：发现疑似回归时
```text
我在 `requirement-exploration` 项目里发现一个疑似回归，但我不确定是 skill 真的退化，还是 benchmark / grading 旧了。

请按这个顺序排查：
1. 先读对应样本的 with_skill / without_skill `response.txt`
2. 再读 `grading.json`
3. 再读该 iteration 的 `grade_and_benchmark_*.py`
4. 最后再判断是否需要改 `SKILL.md`

要求：
- 不要一开始就改规则
- 优先修评测工件问题
- 若确认是规则问题，只做最小补丁
```

### 模板 C：只扩样本，不先改规则
```text
继续优化 `requirement-exploration`，这次目标是扩测试覆盖，不先改 `SKILL.md`。

要求：
- 复用当前稳定基线 iteration-17
- 新增 1-2 个与现有 late-stage blocking / non-blocking 边界相邻的样本
- 每个新样本尽量只有 1 个真正 blocking gap
- 保留旧对照样本，避免误伤
- 跑完 with_skill / without_skill 后，更新 grading 与 benchmark
- 只有当新样本暴露出明确失败模式时，才允许提出最小规则补丁
```

## 最简项目状态说明
如果以后只想给另一个大模型一小段背景，可以直接贴这段：

```text
我在持续优化 Claude Code skill `requirement-exploration`，目标是让它在需求探索场景里更稳定地区分：真正 blocking 的缺口、可默认继续的 non-blocking 边界、以及何时该请求显式生成授权。当前稳定基线是 iteration-17，benchmark 为 with_skill 1.0 / without_skill 0.63 / delta +0.37。这个版本已稳定覆盖 late-stage single blocking gap、late-stage non-blocking closeout、explicit generation authorization 等情况。后续工作应以 `document-skills:skill-creator` 为主流程，优先扩 eval 和修 grading，再决定是否对 `SKILL.md` 做最小规则补丁。
```
