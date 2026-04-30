# Startup Contract

Use this reference before starting a new `product-delivery-skill-chain` request, creating project defaults, previewing per-request execution rules, or handling commit/subagent/full-auto policy.

## Contract Files

- Project defaults: `delivery/_chain-defaults.md`
- Per-request contract: `<chain-dir>/chain-start-contract.md`

The project defaults store long-lived user preferences. The per-request contract is a snapshot for one requirement, based on project defaults plus explicit overrides from the current request.

## First-Time Defaults Interview

### First-Time Defaults Gate

If `delivery/_chain-defaults.md` does not exist, stop before the per-request chain starts.

- Do not show preview / 不展示预览：不要展示 `本次链路合同预览`。
- Do not synthesize project defaults from recommended values.
- Do not create the request folder, `delivery-chain-status.md`, source archive, `source-context.md`, or downstream invocation envelope.
- Ask the first-time defaults interview one question at a time, with 2-3 numbered options and one recommended option.
- Tell the user they may reply with only the option number.
- Treat recommended values as recommendations only, not confirmed defaults.
- After all answers are confirmed, save `delivery/_chain-defaults.md`, then continue to the new request preview.

问题：

1. 执行模式
   1. `semi-auto`（推荐：半自动）：PRD 后、开发前、最终验收后确认
   2. `full-auto`：除高风险或外部动作外自动推进
   3. `ask-each-stage`：每个阶段都确认
2. 子代理授权
   1. `planning-review-only`（推荐：规划/审核可用子代理，编码前确认）：规划和审核可用子代理；编码 worker 需要开发前确认
   2. `all-allowed-after-confirmation`：开发确认后，编码 worker 也可用
   3. `none`：不使用子代理
3. 并行规划
   1. `planning-parallel`（推荐：PRD 通过后规划阶段可并行）：工具允许时，技术设计和审核标准可并行
   2. `sequential`：所有阶段串行执行
4. 开发前确认
   1. `required`（推荐：开始编码前确认）：编码开始前必须询问
   2. `skip-in-full-auto`：仅在 full-auto 模式下跳过
5. 提交策略
   1. `disabled-by-default`（推荐：默认不提交）：除非本次需求明确授权，否则不创建 git commit
   2. `commit-after-verified-batch`：允许实现阶段在验证通过的任务批次后提交
   3. `ask-before-each-commit`：每次提交前询问
6. Push / PR 策略
   1. `explicit-only`（推荐：只在明确要求时执行）：只有用户明确要求时才 push 或创建 PR
   2. `ask-after-final-review`：最终审核通过后询问是否 push/建 PR
7. 审核修复循环
   1. `max-5-stop-on-scope-conflict`（推荐：最多 5 轮，遇到范围冲突停止）：限定范围内自动修复，遇到 PRD/设计/范围冲突时停止
   2. `ask-after-each-review`：每次审核后询问
   3. `review-only-no-fix`：只审核，不自动进入修复循环
8. 高风险操作
   1. `explicit-only`（推荐：必须明确确认）：高风险操作必须得到明确确认
   2. `ask-with-risk-summary`：执行前带简短风险摘要询问
   3. `no-confirmation`：完全不询问，按链路继续执行；这是高风险选择，只在用户明确选择时使用

固定默认项不单独询问：

- 产物归档策略：创建 `delivery/<timestamp9>-<feature-slug>/`；将用户提供的文件复制到 `source/`；创建 `source/source-manifest.md`；创建 `source-context.md`。
- 上下文策略：每保存一个正式产物后，主线程只保留产物路径、关键决策、阻塞项和下一步。

## New Request Preview

Enter this step only after `delivery/_chain-defaults.md` exists, or after first-time defaults were just confirmed and saved. Do not treat recommended values as saved defaults.

For every new request, read `delivery/_chain-defaults.md`, merge explicit instructions from the current user prompt, then show a contract preview. Do not create the request folder, status file, source archive, or downstream invocation envelope until the user confirms.

用户可见预览模板：

```markdown
## 本次链路合同预览
- 执行模式:
- 入口阶段:
- 目标/停止点:
- 产物目录:
- 源文件归档:
- 子代理策略:
- 并行规划:
- 开发前确认:
- 提交策略:
- Push / PR:
- 审核修复循环:
- 高风险操作:
- 上下文策略:
```

Then ask:

```text
是否按以上合同创建本次链路？如果要改，只说要改的项。
```

## Resume Rules

When resuming an existing request:

1. If `<chain-dir>/chain-start-contract.md` exists, use it and do not ask again.
2. If `delivery-chain-status.md` points to a contract path, use that contract.
3. If no per-request contract exists, read `delivery/_chain-defaults.md`, show a preview, and ask before creating the missing contract.
4. Ask only when the current user instruction conflicts with the saved contract, requests push/PR, changes implementation confirmation, or introduces high-risk work.

## Git Handoff

The chain contract records authorization. It does not decide commit granularity.

- If commits are disabled, tell `tdd-task-implementation-orchestrator` not to commit.
- If commits are authorized, tell `tdd-task-implementation-orchestrator` to apply its own verified task-batch or feature-area commit rules.
- Push and pull request creation remain unauthorized unless explicitly allowed by the current request or saved contract.
- Record created commits, push status, PR status, and git blockers in `delivery-chain-status.md`.

## Downstream Enforcement

After the request contract is confirmed, build the downstream invocation envelope from it. Every downstream skill invoked by the chain receives the envelope fields relevant to that stage.

The envelope is the bridge between the user's contract and downstream skill behavior. If the contract disables subagents, commits, push, PR, or unconfirmed implementation, downstream skills must not enable them through their own defaults.
