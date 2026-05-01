# 项目目录

## 1. 项目定位

`sun-skills` 是一组围绕产品交付流程组织的 Codex skills。它覆盖需求澄清、PRD、技术设计、审核标准、任务拆分、TDD 开发和实现审核。

本文件只做导航：帮助判断该看哪个目录、调用哪个 skill、以及哪些内容是正式入口或历史材料。具体执行细则以各 skill 目录中的 `SKILL.md` 和按需加载文档为准。

## 2. 一眼看懂

```text
D:\sun-skills
├─ AGENTS.md                         # 项目协作规则
├─ PROJECT_DIRECTORY.md              # 当前中文导航
├─ requirement-exploration\          # 1. 需求澄清
├─ prompt-to-prd-review\             # 2. 需求转 PRD
├─ prd-to-tech-design-review\        # 3. PRD 转技术设计
├─ prd-quality-audit-standards\      # 4a. PRD 转审核标准
├─ prd-task-archiver\                # 4b. PRD/设计转任务清单
├─ tdd-task-implementation-orchestrator\
│                                      # 5. 按任务执行 TDD 开发
├─ implementation-review-handoff\    # 6. 开发后验收和修复交接
├─ product-delivery-skill-chain\     # 全流程编排入口
├─ plan-design-interview\            # 深度设计访谈
├─ workspaces\                       # 各模块 workspace 运行材料归档
├─ dist\                             # .skill 打包产物
├─ delivery\                         # 交付链产物样例和状态
└─ docs\                             # 维护文档
```

## 3. 按目标找入口

| 你现在要做什么 | 看这里 |
| --- | --- |
| 需求还不清楚，需要先问清楚 | `requirement-exploration/` |
| 已有清晰需求，要生成 PRD | `prompt-to-prd-review/` |
| 已有 PRD，要技术设计 | `prd-to-tech-design-review/` |
| 已有 PRD，要验收或审核标准 | `prd-quality-audit-standards/` |
| 已有 PRD 或设计，要拆开发任务 | `prd-task-archiver/` |
| 已有 PRD、设计、任务清单，要开始实现 | `tdd-task-implementation-orchestrator/` |
| 开发完成后，要验收实现质量 | `implementation-review-handoff/` |
| 想串联完整交付流程或恢复链路状态 | `product-delivery-skill-chain/` |
| 想对方案逐层追问和澄清 | `plan-design-interview/` |

## 4. 推荐流程

```text
需求澄清
  ↓
PRD 生成和审查
  ↓
技术设计
  ↓
审核标准 + 任务拆分
  ↓
TDD 开发执行
  ↓
实现审核和修复交接
```

对应目录：

1. `requirement-exploration/`
2. `prompt-to-prd-review/`
3. `prd-to-tech-design-review/`
4. `prd-quality-audit-standards/` 和 `prd-task-archiver/`
5. `tdd-task-implementation-orchestrator/`
6. `implementation-review-handoff/`

如果用户希望从任意阶段进入、串联多个阶段、维护 `delivery-chain-status.md`，优先从 `product-delivery-skill-chain/` 进入。

## 5. 正式 Skill 目录结构

下面只列稳定入口和关键分层，不展开每个文件的完整规则。

### 5.1 需求到 PRD

```text
requirement-exploration\
├─ SKILL.md                          # 主入口：需求澄清
├─ references\
│  ├─ new-project.md                 # 新项目或新功能
│  ├─ existing-project-iteration.md  # 已有项目迭代
│  └─ late-stage-review.md           # 下游生成前收口
└─ evals\                            # 触发和场景评测

prompt-to-prd-review\
├─ SKILL.md                          # 主入口：需求转 PRD
├─ agents\
│  ├─ frontend-prd-reviewer.md       # 前端 PRD 审查
│  └─ backend-prd-reviewer.md        # 后端 PRD 审查
├─ references\
│  ├─ core-workflow.md               # 核心流程
│  ├─ input-and-context.md           # 输入和上下文
│  ├─ prd-content.md                 # PRD 内容要求
│  ├─ template-variants.md           # 模板变体
│  ├─ review-and-iteration.md        # 审查和迭代
│  ├─ finalize-and-record.md         # 落盘和记录
│  ├─ quality-metrics.md             # 质量指标
│  └─ troubleshooting.md             # 异常处理
└─ evals\                            # PRD 输出和触发评测
```

### 5.2 PRD 到设计、标准和任务

```text
prd-to-tech-design-review\
├─ SKILL.md                          # 主入口：PRD 转技术设计
├─ agents\
│  ├─ frontend-tech-reviewer.md      # 前端技术视角
│  ├─ backend-tech-reviewer.md       # 后端技术视角
│  └─ second-pass-tech-reviewer.md   # 二次审查
├─ references\
│  ├─ prd-analysis.md                # PRD 分析
│  ├─ project-context-inspection.md  # 项目上下文检索
│  ├─ collaboration-workflow.md      # 协作流程
│  ├─ technical-doc-template.md      # 技术设计模板
│  └─ quality-gate.md                # 质量门槛
└─ evals\                            # 技术设计评测

prd-quality-audit-standards\
├─ SKILL.md                          # 主入口：PRD 转审核标准
├─ agents\
│  └─ quality-audit-reviewer.md      # 审核标准审查
├─ references\
│  ├─ workflow.md                    # 生成流程
│  ├─ context-and-output.md          # 输入和输出
│  ├─ prd-coverage-analysis.md       # PRD 覆盖分析
│  ├─ audit-standards-template.md    # 审核标准模板
│  ├─ audit-check-rules.md           # 检查规则
│  ├─ clean-context-review.md        # 干净上下文审查
│  └─ quality-gate.md                # 质量门槛
└─ evals\                            # 审核标准评测

prd-task-archiver\
├─ SKILL.md                          # 主入口：PRD/设计转任务
├─ references\
│  ├─ source-prd-analysis.md         # PRD 来源分析
│  ├─ existing-project-context.md    # 已有项目上下文
│  ├─ task-decomposition.md          # 任务拆解
│  ├─ archive-template.md            # 任务归档模板
│  ├─ quality-review-and-updates.md  # 质量复核和更新
│  └─ error-handling.md              # 异常处理
└─ evals\                            # 任务拆解评测和样例
```

### 5.3 实现和审核

```text
tdd-task-implementation-orchestrator\
├─ SKILL.md                          # 主入口：TDD 开发编排
├─ agents\
│  ├─ feature-area-worker.md         # 功能区开发 worker
│  └─ fresh-failure-analyzer.md      # 失败后干净上下文分析
├─ references\
│  ├─ scope-and-inputs.md            # 范围和输入
│  ├─ execution-loop.md              # 执行循环
│  ├─ run-log-and-task-list.md       # 日志和任务清单
│  ├─ tdd-and-verification.md        # TDD 和验证
│  ├─ subagents-and-parallelism.md   # 子代理和并行
│  ├─ failure-fuse.md                # 失败熔断
│  ├─ full-auto-and-risk.md          # 全自动和风险
│  ├─ git-and-worktree.md            # Git 和 worktree
│  ├─ fix-packet-mode.md             # 修复包模式
│  ├─ clean-context-review.md        # 干净上下文复核
│  └─ completion-and-final-report.md # 完成和最终报告
├─ scripts\                          # 辅助脚本
└─ evals\                            # 触发和执行评测

implementation-review-handoff\
├─ SKILL.md                          # 主入口：实现审核和交接
├─ agents\
│  └─ implementation-reviewer.md     # 实现审核者
├─ references\
│  ├─ handoff-inputs.md              # 审核输入
│  ├─ review-workflow.md             # 审核流程
│  ├─ audit-standards-alignment.md   # 与审核标准对齐
│  ├─ audit-standards-execution.md   # 执行审核标准
│  ├─ verification-and-evidence.md   # 验证证据
│  ├─ status-and-findings.md         # 状态和发现
│  ├─ risk-gates.md                  # 风险门槛
│  ├─ review-fix-loop.md             # 审核修复循环
│  ├─ final-report.md                # 最终报告规则
│  └─ final-report-template.md       # 最终报告模板
└─ evals\                            # 审核场景评测
```

### 5.4 编排和访谈

```text
product-delivery-skill-chain\
├─ SKILL.md                          # 主入口：交付链编排
├─ references\
│  ├─ startup-contract.md            # 首次默认约定
│  ├─ routing-map.md                 # 阶段路由
│  ├─ flow-modes.md                  # 流程模式
│  ├─ handoff-contracts.md           # 交接契约
│  ├─ downstream-invocation-envelope.md
│  │                                  # 下游调用信封
│  ├─ status-file.md                 # 状态文件维护
│  ├─ artifact-directory.md          # 产物目录约定
│  └─ context-management.md          # 上下文管理
└─ evals\                            # 编排和路由评测

plan-design-interview\
└─ SKILL.md                          # 主入口：逐层设计访谈
```

## 6. 非正式入口目录

| 目录 | 怎么看 |
| --- | --- |
| `workspaces/` | 各模块 workspace 运行材料归档。评测、实验、优化和历史输出。适合追溯原因，不适合作为当前规则来源。 |
| `dist/` | `.skill` 打包结果。通常不要直接编辑，优先修改正式 skill 目录后再生成。 |
| `delivery/` | 交付链运行产物和样例。可看流程形态，不代表所有请求的固定输出路径。 |
| `docs/` | 维护文档、待办和跨 skill 补充说明。 |
| `.claude/`、`.kiro/`、`.vscode/` | 本地工具或编辑器配置。 |

## 7. 维护规则

- 改 skill 行为：优先改对应正式 skill 目录中的 `SKILL.md`、`references/`、`agents/` 或 `evals/`。
- 改导航：只更新本文件，保持“入口索引”定位，不复制长篇规则。
- 看历史原因：查 `workspaces/`、`delivery/` 或 `docs/`。
- 看当前执行准则：查正式 skill 的 `SKILL.md`，再按其中规则加载 `references/` 或 `agents/`。
