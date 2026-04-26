# 会员积分 Quality Audit Standards

## Source And Scope

- Source PRD: 用户消息摘要，会员积分 PRD 已包含消费发放积分、退款冲正、积分过期、管理员调整、会员积分流水。
- Supporting context: 未提供技术设计、任务归档、项目代码或测试命令。
- Audit purpose: 代码开发完成后，供实现审核代理或测试审核代理验证实现是否满足 PRD。
- In scope:
  - 消费后发放积分。
  - 退款后冲正已发放积分。
  - 积分过期处理。
  - 管理员调整会员积分。
  - 会员积分流水查询与记录。
  - 积分余额、流水一致性、权限、审计证据、回归与缺陷复测规则。
- Out of scope:
  - 重新编写 PRD。
  - 技术方案、数据库设计、接口设计或开发任务拆分。
  - 未在 PRD 摘要中出现的营销活动、会员等级、兑换、冻结、转赠、跨系统清结算。

## Project Context Inspection

- Project path: not provided
- Context inspection mode: Not available
- Inspected files:

| File | Reason Inspected | Impact On Audit Standards |
| --- | --- | --- |
| N/A | 未提供项目代码路径 | 测试命令、接口路径、数据库表名、权限实现方式均标为待实现审核时确认 |

## Audit Environment Requirements

- Required services: 会员系统、订单/消费记录服务、退款服务、积分服务、后台管理系统、数据库或账本存储、日志/审计系统。
- Required accounts/roles: 普通会员账号、无权限会员账号、积分管理员账号、非积分管理员后台账号、系统任务账号。
- Required test data:
  - 至少 1 个无历史积分会员。
  - 至少 1 个已有可用积分会员。
  - 至少 1 笔可发放积分的已完成消费订单。
  - 至少 1 笔可全额退款订单和 1 笔可部分退款订单；若 PRD 不支持部分退款，标记为 BQ-002。
  - 至少 1 批即将过期积分和 1 批未过期积分。
  - 至少 1 条管理员增加积分和 1 条管理员扣减积分测试数据。
- Required secrets/sandboxes: 订单/退款沙箱凭证、后台管理员测试账号、可查询数据库或账本记录的只读权限、日志检索权限。
- Setup commands: 未提供项目命令。未来审核代理必须先确认并记录项目实际测试命令；无法执行时按 TE-002 静态回退。
- Known environment limitations: 当前标准基于 PRD 摘要生成，具体积分比例、过期周期、接口名称、UI 文案、性能阈值未定义。

## Readiness Summary

- Status: Ready with assumptions
- Intended primary executor: Implementation audit agent / Test audit agent
- Requirements mapped: 5
- Blocked or ambiguous requirements: 8
- Release-blocking gates: 7
- Machine-readable appendix: Included

## Requirement Inventory

| Requirement ID | PRD Requirement | Notes |
| --- | --- | --- |
| PRD-001 | 消费发放积分 | 高风险余额/账本行为；积分发放规则细节缺失 |
| PRD-002 | 退款冲正 | 高风险退款与余额一致性行为；全额/部分/重复退款细节缺失 |
| PRD-003 | 积分过期 | 高风险定时/批处理/余额一致性行为；过期周期和时区缺失 |
| PRD-004 | 管理员调整 | 高风险权限和手工改账行为；审批、原因、上下限缺失 |
| PRD-005 | 会员积分流水 | 核心审计证据；字段、排序、筛选、可见范围缺失 |

## Traceability Matrix

| ID | PRD Requirement | Audit Check | Layer | Priority | Mode | Test Execution | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BV-001 | PRD-001 消费发放积分 | 消费完成后按 PRD 规则增加会员可用积分并生成流水 | Behavior Verification | Blocker | Automated | Required | 测试输出、订单号、会员ID、余额前后值、流水ID | Ready |
| BV-002 | PRD-002 退款冲正 | 退款成功后冲正对应消费发放积分并生成冲正流水 | Behavior Verification | Blocker | Automated | Required | 退款单号、原订单号、余额前后值、冲正流水ID | Ready |
| BV-003 | PRD-003 积分过期 | 到期积分被扣减且未过期积分不受影响 | Behavior Verification | Blocker | Automated | Conditional | 任务执行记录、积分批次、余额前后值、过期流水ID | Ready |
| BV-004 | PRD-004 管理员调整 | 有权限管理员可增减积分，会员余额和流水同步变化 | Behavior Verification | High | Automated | Required | 管理员ID、调整原因、余额前后值、调整流水ID | Ready |
| BV-005 | PRD-005 会员积分流水 | 会员可查看自己的积分流水，流水覆盖所有积分变动类型 | Behavior Verification | High | Automated | Required | 页面/API响应、流水记录、类型/金额/时间字段 | Ready |
| IA-001 | PRD-001/002/003/004/005 | 积分余额与流水/账本一致，不允许无流水改余额 | Implementation Audit | Blocker | Review-only | Static fallback | 代码引用、数据库记录、账本一致性查询 | Ready |
| IA-002 | PRD-004 | 管理员调整权限边界正确，非授权角色不可调整 | Implementation Audit | Blocker | Review-only | Static fallback | 权限配置、拒绝访问测试、审计日志 | Ready |
| IA-003 | PRD-002 | 退款冲正具备幂等保护，重复退款事件不重复扣积分 | Implementation Audit | Blocker | Review-only | Static fallback | 幂等键/唯一约束/重复事件测试证据 | Ready |
| TE-001 | All | 执行项目相关自动化测试并记录结果 | Test Execution | Blocker | Automated | Required | 命令、时间戳、退出码、失败日志 | Ready |
| RG-001 | All | 任何核心余额、流水或权限 Blocker 失败均拒绝发布 | Risk Gate | Blocker | Review-only | Not applicable | 审核结论与缺陷引用 | Ready |
| BQ-001 | PRD-001 | 积分发放比例、舍入、上限、订单状态触发点未提供 | Blocked Question | High | Blocked | Not applicable | PRD补充或产品确认 | Blocked |
| BQ-002 | PRD-002 | 部分退款、重复退款、退款撤销的冲正规则未提供 | Blocked Question | High | Blocked | Not applicable | PRD补充或产品确认 | Blocked |
| BQ-003 | PRD-003 | 过期周期、时区、过期执行时间、通知要求未提供 | Blocked Question | High | Blocked | Not applicable | PRD补充或产品确认 | Blocked |
| BQ-004 | PRD-004 | 管理员调整是否需要审批、上下限、原因枚举未提供 | Blocked Question | High | Blocked | Not applicable | PRD补充或产品确认 | Blocked |
| BQ-005 | PRD-005 | 流水字段、排序、筛选、导出、分页要求未提供 | Blocked Question | Medium | Blocked | Not applicable | PRD补充或产品确认 | Blocked |

## Behavior Verification Standards

### BV-001: 消费发放积分

- PRD trace: PRD-001 消费发放积分。
- Scenario/setup: Given 会员完成一笔符合积分发放条件的消费订单；When 订单达到 PRD 定义的发放触发状态；Then 会员可用积分增加，并产生消费发放流水。
- Test data:
  - Positive cases: 符合发放条件的订单。
  - Negative cases: 未支付、已取消或不符合发放条件的订单；具体状态以 PRD/实现配置为准。
  - Boundary cases: 金额为发放阈值边界、积分计算产生小数、订单金额为 0；若 PRD 未定义，记录 BQ-001。
  - Stateful cases: 同一订单重复触发发放事件。
  - Cleanup requirements: 回滚或隔离测试会员、订单、流水。
- Steps or review method: 创建或定位消费订单，触发发放流程，查询会员余额和积分流水。
- Pass criteria: 余额增加值等于 PRD 规则计算结果；流水类型为消费发放；同一订单不重复发放；流水与余额变更可互相追踪。
- Fail criteria: 未发放、重复发放、金额错误、无流水、流水无法追踪订单、余额与流水不一致。
- Required evidence: EV-001 测试命令输出；EV-002 订单号和会员ID；EV-003 余额前后值；EV-004 发放流水记录。
- Mode: Automated
- Automation level: Required
- Test execution requirement: Required
- Priority: Blocker
- Retest scope: 消费发放测试、积分余额一致性、流水查询、重复事件回归。

### BV-002: 退款冲正积分

- PRD trace: PRD-002 退款冲正。
- Scenario/setup: Given 已完成积分发放的订单；When 退款成功；Then 系统冲正原发放积分并记录退款冲正流水。
- Test data:
  - Positive cases: 全额退款。
  - Negative cases: 退款失败、退款申请中、重复退款通知。
  - Boundary cases: 部分退款、积分余额不足以冲正、退款金额小于最小积分单位；未定义时记录 BQ-002。
  - Stateful cases: 同一退款单重复回调或重复处理。
  - Cleanup requirements: 隔离订单、退款单、积分流水。
- Steps or review method: 对已发放积分订单执行退款，等待冲正处理，查询余额和流水。
- Pass criteria: 冲正积分等于 PRD 退款规则；余额和流水一致；重复退款事件不重复扣减；冲正流水关联原订单和退款单。
- Fail criteria: 退款成功但未冲正、重复扣减、扣减金额错误、无冲正流水、冲正后余额/流水不一致。
- Required evidence: EV-005 原订单号、退款单号、退款状态；EV-006 冲正前后余额；EV-007 冲正流水；EV-008 重复事件处理证据。
- Mode: Automated
- Automation level: Required
- Test execution requirement: Required
- Priority: Blocker
- Retest scope: 退款流程、消费发放幂等、余额一致性、流水查询。

### BV-003: 积分过期

- PRD trace: PRD-003 积分过期。
- Scenario/setup: Given 会员存在已到期积分和未到期积分；When 过期任务或过期判定执行；Then 仅到期积分被扣减并生成过期流水。
- Test data:
  - Positive cases: 已超过有效期的积分批次。
  - Negative cases: 未到期积分批次。
  - Boundary cases: 到期日当天、跨时区、任务重复执行、余额不足；未定义时记录 BQ-003。
  - Stateful cases: 多批积分不同到期日。
  - Cleanup requirements: 隔离系统时间或使用可控测试批次。
- Steps or review method: 准备到期/未到期积分，触发过期任务或时间推进，查询余额和流水。
- Pass criteria: 只扣减到期积分；过期流水类型、金额、时间可审计；重复执行不重复扣减；未到期积分保留。
- Fail criteria: 过期未扣、提前扣、重复扣、无流水、时区导致错误过期。
- Required evidence: EV-009 积分批次和到期时间；EV-010 任务执行记录；EV-011 余额前后值；EV-012 过期流水。
- Mode: Automated
- Automation level: Required where time control exists; otherwise Recommended with static fallback.
- Test execution requirement: Conditional
- Priority: Blocker
- Retest scope: 过期任务、余额一致性、流水查询、重复任务回归。

### BV-004: 管理员调整积分

- PRD trace: PRD-004 管理员调整。
- Scenario/setup: Given 有权限积分管理员；When 提交积分增加或扣减调整；Then 会员余额变化并生成管理员调整流水。
- Test data:
  - Positive cases: 管理员增加积分、管理员扣减积分。
  - Negative cases: 非授权后台账号、普通会员、缺少调整原因。
  - Boundary cases: 扣减超过可用余额、超出单次调整上限、负数或 0；未定义时记录 BQ-004。
  - Stateful cases: 连续多次调整同一会员。
  - Cleanup requirements: 使用测试管理员和测试会员。
- Steps or review method: 使用有权限和无权限账号分别调用后台调整能力，查询余额、流水和审计日志。
- Pass criteria: 授权管理员调整成功；非授权角色被拒绝；调整原因和操作者记录在流水/审计日志中；余额和流水一致。
- Fail criteria: 未授权可调整、授权调整无流水、无原因仍成功且 PRD 要求原因、余额可被调成非法状态。
- Required evidence: EV-013 管理员ID和角色；EV-014 调整请求；EV-015 余额前后值；EV-016 调整流水和审计日志。
- Mode: Automated
- Automation level: Required for API; Manual acceptable only for纯后台页面且无接口测试能力。
- Test execution requirement: Required
- Priority: High
- Retest scope: 权限、后台调整、余额一致性、流水查询。

### BV-005: 会员积分流水

- PRD trace: PRD-005 会员积分流水。
- Scenario/setup: Given 会员发生消费发放、退款冲正、积分过期、管理员调整；When 会员查看积分流水；Then 可看到属于自己的完整流水。
- Test data:
  - Positive cases: 四类积分变动流水。
  - Negative cases: 会员访问其他会员流水。
  - Boundary cases: 多页数据、同时间多条流水、筛选条件；未定义时记录 BQ-005。
  - Stateful cases: 余额与流水累计校验。
  - Cleanup requirements: 隔离测试会员流水。
- Steps or review method: 创建覆盖所有变动类型的流水，调用会员端页面/API 查询。
- Pass criteria: 流水只展示当前会员数据；包含类型、积分变动值、发生时间、关联业务标识等 PRD 要求字段；排序和分页符合 PRD；流水累计与余额一致。
- Fail criteria: 漏展示某类流水、越权查看他人流水、字段缺失、排序错误、流水累计与余额不一致。
- Required evidence: EV-017 会员端响应/截图；EV-018 四类流水记录；EV-019 越权访问拒绝证据；EV-020 余额-流水一致性计算。
- Mode: Automated
- Automation level: Required for API; Recommended for UI.
- Test execution requirement: Required
- Priority: High
- Retest scope: 流水列表、权限隔离、余额一致性、分页/排序。

## Implementation Audit Standards

### IA-001: 余额与流水一致性

- PRD trace: PRD-001 至 PRD-005。
- Implementation area: data/accounting/audit log/tests。
- Review method: 检查积分余额更新是否与流水写入处于一致事务或具备补偿机制；抽样核对测试数据的余额与流水累计。
- Pass criteria: 所有积分变动都有流水；余额不能绕过流水直接改变；失败重试不会造成余额和流水不一致。
- Fail criteria: 存在无流水改余额路径；余额和流水非原子且无补偿；测试数据对账失败。
- Required evidence: EV-021 相关代码引用；EV-022 数据库/账本一致性查询；EV-023 失败重试或事务证据。
- Test coverage requirement: Blocker/High 积分变动路径必须有自动化测试或书面不可自动化原因。
- Static fallback: 审阅模型、事务、仓储层、服务层、测试断言。
- Priority: Blocker
- Retest scope: 所有积分变动路径和对账查询。

### IA-002: 管理员权限与审计

- PRD trace: PRD-004 管理员调整。
- Implementation area: auth/policy/admin API/audit log。
- Review method: 检查后台权限策略、路由守卫、服务层权限校验和审计日志写入。
- Pass criteria: 非授权角色在 UI/API/服务层均不能调整；成功调整记录操作者、目标会员、原因、变更值、时间。
- Fail criteria: 仅前端限制无后端校验；普通后台账号可调整；缺少审计记录。
- Required evidence: EV-024 权限配置和代码引用；EV-025 拒绝访问测试；EV-026 审计日志样例。
- Test coverage requirement: 授权成功和未授权拒绝均需测试。
- Static fallback: 审阅权限中间件、后台路由、服务方法。
- Priority: Blocker
- Retest scope: 管理员调整、后台权限、审计日志。

### IA-003: 幂等与重复处理

- PRD trace: PRD-001 消费发放、PRD-002 退款冲正、PRD-003 积分过期。
- Implementation area: event handlers/jobs/database constraints。
- Review method: 检查订单发放、退款冲正、过期任务是否使用业务唯一键或状态机防止重复处理。
- Pass criteria: 同一订单、退款单、过期批次重复触发不会重复增减积分；日志能说明重复事件被跳过或归并。
- Fail criteria: 重复回调或重复任务造成重复积分变化。
- Required evidence: EV-027 幂等键/唯一约束/状态机代码；EV-028 重复事件测试结果；EV-029 重复处理日志。
- Test coverage requirement: 每个异步或可重复触发路径至少一个重复处理测试。
- Static fallback: 审阅唯一索引、事务边界、状态流转代码。
- Priority: Blocker
- Retest scope: 发放、退款、过期任务及相关流水。

### IA-004: 流水查询数据隔离

- PRD trace: PRD-005 会员积分流水。
- Implementation area: member API/query filters/authorization。
- Review method: 检查流水查询是否始终按当前登录会员或授权主体过滤，且不信任客户端传入会员ID。
- Pass criteria: 普通会员只能看到自己的流水；管理员查询能力如存在，必须受后台权限控制。
- Fail criteria: 通过修改会员ID可查看他人流水；查询接口缺少授权约束。
- Required evidence: EV-030 查询代码引用；EV-031 越权访问测试；EV-032 API响应样例。
- Test coverage requirement: 至少覆盖本人查询和他人查询拒绝。
- Static fallback: 审阅查询条件和鉴权上下文。
- Priority: High
- Retest scope: 会员流水 API/UI 和权限回归。

## Test Execution Requirements

| ID | Command/Suite | Required For | Execution Class | Expected Evidence | Fallback If Blocked |
| --- | --- | --- | --- | --- | --- |
| TE-001 | 项目实际单元/集成/API/E2E 测试命令，待未来审核代理确认 | BV-001 至 BV-005，IA-001 至 IA-004 | Required | 命令、时间戳、退出码、完整失败日志、测试报告路径 | 若命令不存在，记录 Blocked，并执行 TE-002 |
| TE-002 | 静态测试覆盖审查 | BV-001 至 BV-005，IA-001 至 IA-004 | Static fallback | 测试文件路径、断言摘要、mock/fixture说明、未覆盖风险 | 若代码不可读，最终结论不得为 Approved |
| TE-003 | 数据一致性抽样查询 | IA-001，BV-001 至 BV-005 | Conditional | 查询条件、会员ID、流水ID、余额计算过程 | 若无数据库权限，记录 Blocked 和所需权限 |
| TE-004 | 权限/越权测试 | BV-004，BV-005，IA-002，IA-004 | Required | 授权与未授权请求、响应码、日志 | 无测试账号时记录 Blocked |

## API, Data, And State Standards

- 所有积分变动必须能追踪到业务来源：订单、退款单、过期任务批次或管理员调整单。
- 积分余额和流水累计必须可对账；若系统采用分批次有效期账本，审核需同时校验批次余额。
- 积分变动不得因重复事件、重试或并发请求产生重复入账/扣账。
- 退款冲正不得冲正超过原消费发放积分，除非 PRD 明确允许其他规则。
- 积分过期不得影响未到期积分；过期任务重复执行不得重复扣减。
- 管理员调整必须记录操作者和原因；若 PRD 未要求原因，仍作为 derived quality standard，原因是手工改账需要审计证据。

## Permissions, Security, And Privacy Standards

- 普通会员只能查看自己的积分余额和流水。
- 后台积分调整必须进行服务端权限校验。
- 管理员调整、退款冲正和过期任务应具备审计日志或等价追踪证据。
- 会员流水中不得暴露其他会员的个人信息、订单信息或内部审计字段。
- 权限失败、参数篡改、跨会员访问应返回拒绝结果，且不得产生积分变动。

## Observability, Performance, And Reliability Standards

- 消费发放、退款冲正、过期任务、管理员调整均应产生日志或审计事件，包含业务ID、会员ID、变动值、结果和错误原因。
- 过期任务和退款冲正失败应可重试或可人工定位，不能静默丢失。
- 性能阈值 PRD 未提供，不能设定硬性响应时间；记录 BQ-006。
- 批量过期规模、任务窗口、告警规则 PRD 未提供；记录 BQ-007。

## Regression And Compatibility Standards

- Existing behavior to retest: 会员登录、订单完成、退款成功、后台登录、会员积分展示。
- Backward compatibility checks: 既有积分余额和历史流水不得在上线后丢失或被错误重算。
- Migration/rollback checks: 若实现引入新流水类型、字段或批次表，需验证迁移前后余额一致；PRD 未提供迁移要求，记录 BQ-008。
- Release/feature-flag checks: 若灰度发布，需验证新旧逻辑不会对同一订单重复发放或冲正。

## Required Evidence For Future Review

- Test results: TE-001 至 TE-004 的命令、时间戳、退出码、报告路径。
- Screenshots or recordings: 后台管理员调整、会员流水页面如存在 UI。
- API traces: 消费发放、退款冲正、积分流水查询、管理员调整请求和响应。
- Database records: 会员余额、积分流水、积分批次、业务关联ID。
- Logs/audit events: 发放、冲正、过期、调整、权限拒绝、重复事件跳过。
- Accessibility/performance reports: 仅当 PRD 或项目规范要求 UI 可访问性/性能时必需。
- Code references: 余额写入、流水写入、权限校验、幂等控制、过期任务。

Evidence rules:

- Every evidence item must reference one or more audit check IDs.
- Failed evidence must reference a defect report ID.
- API/log/database evidence must include request parameters, query conditions, correlation IDs, or record IDs when relevant.

## Defect Report Format

```yaml
defect_id:
audit_check_id:
prd_trace:
failure_summary:
expected_result:
actual_result:
reproduction_steps_or_review_method:
evidence_references:
affected_files_apis_logs_or_records:
impact_scope:
suggested_severity: Blocker | High | Medium | Low
release_blocking: true | false
recommended_fix_direction:
retest_scope:
```

## Status And Final Conclusion Rules

- Check statuses: Pass / Fail / Blocked / Not Run / Not Applicable
- Final conclusions:
  - Approved: 所有 Blocker 和 High 检查通过，Medium/Low 问题无聚合发布风险。
  - Approved with Risks: 无 Blocker 失败；剩余 High/Medium 问题已有明确风险接受或延期理由。
  - Rejected: 任一 Blocker 失败，或任一核心 PRD 行为缺失。
  - Blocked: 关键 Blocker/High 检查无法验证且替代证据不足。
- `Blocked` and `Not Run` are not passes.
- `Blocker` or `High` checks that are blocked or not run prevent unconditional approval unless sufficient substitute evidence exists.

## Hard Fail Conditions

- Any `Blocker` check fails.
- Any `Blocker` check is `Blocked` or `Not Run` without substitute evidence.
- 消费发放、退款冲正、积分过期、管理员调整、会员积分流水任一核心流无审核覆盖。
- 积分余额、流水、退款冲正、管理员权限或审计日志缺少实现审核覆盖。
- Required test commands are not run and no blocker is recorded.
- High-risk clean-context review findings are ignored without rejection rationale.
- Evidence cannot be traced to audit check IDs.
- 余额可被无流水修改，或流水可被无权限访问。
- 重复退款、重复订单事件或重复过期任务导致重复积分变动。

## Retest And Regression Rules

- Failed check retest scope: 复测原失败检查，并记录新证据 ID。
- Related PRD area regression: 同一积分变动类型的余额、流水、权限、幂等检查必须同步回归。
- Changed code path test requirements: 修改服务层、任务、权限或数据模型时，必须执行相关自动化测试或静态回退。
- Blocker/High fix verification: 必须有相关回归执行结果；无法执行时结论为 Blocked 或 Approved with Risks，不能 Approved。
- Retest round reporting: 每轮复测记录缺陷ID、修复版本、执行人、命令、结果、剩余风险。

## PRD Change Synchronization

- Rerun PRD coverage analysis after PRD changes.
- Preserve unaffected audit check IDs.
- Append IDs for new checks.
- Mark removed checks as deprecated; do not reuse IDs.
- Rerun three clean-context reviews when changes affect core flows, permissions, data, integrations, irreversible operations, or risk levels.
- For small non-behavioral wording changes, run local update plus quality gate.

## Three-Round Clean-Context Review Record

- Review mode: Inline fallback
- Subagent availability: 当前环境未提供可调用的独立质量审核子代理；使用同一来源包进行三轮分离内联复核。
- Reviewer A focus: PRD coverage completeness and traceability
- Reviewer B focus: risk, permissions, data integrity, abnormal flows, security/privacy, integrations
- Reviewer C focus: executability, test commands, evidence, automation feasibility, blocked/not-run handling
- Round 1 status: Completed
- Round 2 status: Completed
- Round 3 status: Completed
- Context isolation: Approximated

| Finding | Raised By | Decision | Rationale |
| --- | --- | --- | --- |
| PRD 摘要不足以确定积分比例、触发状态、舍入和上限 | Round 1 | Accepted | 已加入 BQ-001，并避免把计算规则写成硬性标准 |
| 退款冲正必须覆盖重复退款/重复回调幂等 | Round 2 | Accepted | 退款影响余额且可能重复触发，已加入 BV-002、IA-003、RG-001 |
| 管理员调整不能只测成功路径，必须测未授权拒绝和审计证据 | Round 2 | Accepted | 已加入 BV-004、IA-002、TE-004 |
| 流水查询必须覆盖跨会员数据隔离 | Round 2 / Round 3 | Accepted | 已加入 BV-005、IA-004 |
| 缺少项目测试命令时不能伪造命令 | Round 3 | Accepted | 已将 TE-001 设为未来审核确认实际命令，TE-002 为静态回退 |
| 性能阈值可直接设为 2 秒 | Round 3 | Rejected | PRD 摘要未提供性能阈值；已标为 BQ-006 |
| 过期积分应提前通知会员 | Round 1 | Rejected | PRD 摘要仅说明积分过期，未说明通知；列为 BQ-003 而非标准 |

## Blocked Checks And Open Questions

| Area | Blocking Question | Impact On Testing | Suggested Owner |
| --- | --- | --- | --- |
| BQ-001 消费发放 | 积分发放比例、触发订单状态、舍入、上限、排除商品/订单类型是什么？ | 无法验证积分计算精确值 | Product |
| BQ-002 退款冲正 | 部分退款、重复退款、退款撤销、余额不足冲正规则是什么？ | 无法完整覆盖异常退款路径 | Product |
| BQ-003 积分过期 | 有效期、时区、执行时间、是否通知会员是什么？ | 无法验证边界日和通知行为 | Product |
| BQ-004 管理员调整 | 是否需要审批、原因必填、单次/每日上限、可否调为负数？ | 无法判定后台调整边界 | Product / Risk |
| BQ-005 会员流水 | 必填字段、排序、筛选、分页、导出要求是什么？ | 无法验证 UI/API 完整展示 | Product |
| BQ-006 性能 | 会员流水查询、发放、退款、过期任务性能阈值是什么？ | 不能做硬性性能验收 | Product / Engineering |
| BQ-007 批处理可靠性 | 过期任务批量规模、失败重试、告警规则是什么？ | 不能完整验证任务可靠性 | Engineering |
| BQ-008 迁移 | 是否存在历史积分数据迁移和兼容要求？ | 不能验证上线前后历史数据一致性 | Engineering |

## Assumptions

- 会员积分余额属于高风险账本类数据，因此余额、流水、退款冲正、管理员调整相关失败默认提升为 Blocker 或 High。
- “会员积分流水”至少需要覆盖 PRD 摘要中的四类积分变动；这是由已列功能自然推出的审计要求。
- 未提供项目测试命令，因此不生成具体命令；未来审核代理必须从项目上下文补齐。
- 管理员调整需要审计记录被标为 derived quality standard，因为手工改账没有审计证据会破坏后续质量审核。

## Final Quality Gate

- Ready for post-development audit: Yes, with assumptions and blocked questions
- Final conclusion rule ready: Yes
- Hard fail conditions complete: Yes
- Conditions before use:
  - 未来审核代理需读取完整 PRD，并用完整 PRD 修正 BQ-001 至 BQ-008。
  - 未来审核代理需读取项目测试配置并补充 TE-001 的实际命令。
  - 若完整 PRD 与本摘要冲突，以完整 PRD 为准并重新运行三轮复核。
- Checks that must pass before release:
  - BV-001、BV-002、BV-003、IA-001、IA-002、IA-003、RG-001。

## Machine-Readable Audit Checks Appendix

```json
{
  "source": {
    "prd": "用户消息摘要：消费发放积分、退款冲正、积分过期、管理员调整、会员积分流水",
    "supporting_context": "none",
    "project_context": "not provided"
  },
  "audit_checks": [
    {
      "id": "BV-001",
      "prd_trace": "PRD-001 消费发放积分",
      "layer": "Behavior Verification",
      "category": "points_earn",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "符合积分发放条件的消费订单和测试会员",
      "test_data": {
        "positive_cases": ["符合发放条件的已完成订单"],
        "negative_cases": ["未支付、已取消或不符合发放条件的订单"],
        "boundary_cases": ["阈值金额", "小数积分", "重复订单事件"],
        "stateful_cases": ["同一订单重复触发"],
        "cleanup_requirements": ["隔离或回滚测试订单、会员、流水"]
      },
      "steps_or_method": "触发订单积分发放，查询余额和流水",
      "pass_criteria": "余额按PRD规则增加，生成可追踪消费发放流水，重复事件不重复发放",
      "fail_criteria": "未发放、重复发放、金额错误、无流水或余额流水不一致",
      "required_evidence": ["EV-001", "EV-002", "EV-003", "EV-004"],
      "test_execution_requirement": "Required",
      "retest_scope": "消费发放、余额一致性、流水查询、重复事件",
      "status": "Ready"
    },
    {
      "id": "BV-002",
      "prd_trace": "PRD-002 退款冲正",
      "layer": "Behavior Verification",
      "category": "refund_reversal",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required",
      "setup": "已完成积分发放的订单和成功退款单",
      "test_data": {
        "positive_cases": ["全额退款"],
        "negative_cases": ["退款失败", "重复退款通知"],
        "boundary_cases": ["部分退款", "余额不足冲正"],
        "stateful_cases": ["同一退款单重复处理"],
        "cleanup_requirements": ["隔离订单、退款单、流水"]
      },
      "steps_or_method": "执行退款并查询冲正结果",
      "pass_criteria": "按PRD规则冲正积分，生成关联原订单和退款单的流水，重复事件不重复扣减",
      "fail_criteria": "未冲正、重复扣减、金额错误、无流水或余额流水不一致",
      "required_evidence": ["EV-005", "EV-006", "EV-007", "EV-008"],
      "test_execution_requirement": "Required",
      "retest_scope": "退款、幂等、余额一致性、流水查询",
      "status": "Ready"
    },
    {
      "id": "BV-003",
      "prd_trace": "PRD-003 积分过期",
      "layer": "Behavior Verification",
      "category": "points_expiration",
      "priority": "Blocker",
      "mode": "Automated",
      "automation_level": "Required where time control exists",
      "setup": "已到期和未到期积分批次",
      "test_data": {
        "positive_cases": ["已超过有效期积分"],
        "negative_cases": ["未到期积分"],
        "boundary_cases": ["到期日当天", "跨时区", "任务重复执行"],
        "stateful_cases": ["多批次不同到期日"],
        "cleanup_requirements": ["隔离时间或批次数据"]
      },
      "steps_or_method": "触发过期任务并查询余额、流水",
      "pass_criteria": "仅到期积分扣减，生成过期流水，重复执行不重复扣减",
      "fail_criteria": "过期未扣、提前扣、重复扣、无流水",
      "required_evidence": ["EV-009", "EV-010", "EV-011", "EV-012"],
      "test_execution_requirement": "Conditional",
      "retest_scope": "过期任务、余额一致性、流水查询",
      "status": "Ready"
    },
    {
      "id": "BV-004",
      "prd_trace": "PRD-004 管理员调整",
      "layer": "Behavior Verification",
      "category": "admin_adjustment",
      "priority": "High",
      "mode": "Automated",
      "automation_level": "Required for API",
      "setup": "有权限管理员、无权限账号、测试会员",
      "test_data": {
        "positive_cases": ["管理员增加积分", "管理员扣减积分"],
        "negative_cases": ["非授权账号调整", "缺少原因"],
        "boundary_cases": ["扣减超过余额", "超出调整上限", "0或负数"],
        "stateful_cases": ["连续多次调整"],
        "cleanup_requirements": ["隔离管理员和会员数据"]
      },
      "steps_or_method": "使用授权和未授权账号执行调整并查询余额、流水、审计日志",
      "pass_criteria": "授权调整成功，未授权拒绝，余额流水一致并记录操作者与原因",
      "fail_criteria": "未授权可调整、无流水、无审计、余额非法",
      "required_evidence": ["EV-013", "EV-014", "EV-015", "EV-016"],
      "test_execution_requirement": "Required",
      "retest_scope": "权限、管理员调整、余额一致性、流水查询",
      "status": "Ready"
    },
    {
      "id": "BV-005",
      "prd_trace": "PRD-005 会员积分流水",
      "layer": "Behavior Verification",
      "category": "points_ledger",
      "priority": "High",
      "mode": "Automated",
      "automation_level": "Required for API",
      "setup": "包含四类积分变动的测试会员",
      "test_data": {
        "positive_cases": ["消费发放", "退款冲正", "积分过期", "管理员调整"],
        "negative_cases": ["访问其他会员流水"],
        "boundary_cases": ["多页数据", "同时间多条流水"],
        "stateful_cases": ["流水累计与余额校验"],
        "cleanup_requirements": ["隔离测试会员流水"]
      },
      "steps_or_method": "查询会员积分流水并执行越权访问测试",
      "pass_criteria": "仅展示当前会员流水，覆盖所有变动类型，字段符合PRD，累计与余额一致",
      "fail_criteria": "漏流水、越权、字段缺失、排序错误、余额流水不一致",
      "required_evidence": ["EV-017", "EV-018", "EV-019", "EV-020"],
      "test_execution_requirement": "Required",
      "retest_scope": "流水列表、权限隔离、余额一致性",
      "status": "Ready"
    },
    {
      "id": "IA-001",
      "prd_trace": "PRD-001..PRD-005",
      "layer": "Implementation Audit",
      "category": "ledger_consistency",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Recommended",
      "setup": "代码和数据库只读访问",
      "test_data": {
        "positive_cases": ["各类积分变动样本"],
        "negative_cases": ["失败重试样本"],
        "boundary_cases": ["并发或重复处理"],
        "stateful_cases": ["余额与流水累计对账"],
        "cleanup_requirements": []
      },
      "steps_or_method": "审阅余额写入与流水写入事务/补偿机制并抽样对账",
      "pass_criteria": "所有积分变动有流水且余额流水一致",
      "fail_criteria": "存在无流水改余额路径或对账失败",
      "required_evidence": ["EV-021", "EV-022", "EV-023"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "所有积分变动路径",
      "status": "Ready"
    },
    {
      "id": "IA-002",
      "prd_trace": "PRD-004 管理员调整",
      "layer": "Implementation Audit",
      "category": "admin_permission",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Required where auth tests exist",
      "setup": "后台权限配置和测试账号",
      "test_data": {
        "positive_cases": ["授权管理员"],
        "negative_cases": ["非授权后台账号", "普通会员"],
        "boundary_cases": ["绕过前端直接调用API"],
        "stateful_cases": ["调整后审计日志"],
        "cleanup_requirements": []
      },
      "steps_or_method": "审阅权限策略并执行授权/未授权测试",
      "pass_criteria": "服务端权限校验完整且审计记录完整",
      "fail_criteria": "仅前端限制、未授权可调整或缺少审计",
      "required_evidence": ["EV-024", "EV-025", "EV-026"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "管理员调整权限和审计",
      "status": "Ready"
    },
    {
      "id": "IA-003",
      "prd_trace": "PRD-001/002/003",
      "layer": "Implementation Audit",
      "category": "idempotency",
      "priority": "Blocker",
      "mode": "Review-only",
      "automation_level": "Required for event paths",
      "setup": "事件处理、任务和数据库约束访问",
      "test_data": {
        "positive_cases": ["首次处理订单/退款/过期批次"],
        "negative_cases": ["重复事件"],
        "boundary_cases": ["并发重复"],
        "stateful_cases": ["重复处理日志"],
        "cleanup_requirements": []
      },
      "steps_or_method": "审阅幂等键、唯一约束、状态机并执行重复事件测试",
      "pass_criteria": "重复触发不会重复增减积分",
      "fail_criteria": "重复事件导致重复积分变动",
      "required_evidence": ["EV-027", "EV-028", "EV-029"],
      "test_execution_requirement": "Static fallback",
      "retest_scope": "发放、退款、过期任务",
      "status": "Ready"
    }
  ],
  "blocked_questions": [
    "BQ-001",
    "BQ-002",
    "BQ-003",
    "BQ-004",
    "BQ-005",
    "BQ-006",
    "BQ-007",
    "BQ-008"
  ],
  "hard_fail_checks": [
    "BV-001",
    "BV-002",
    "BV-003",
    "IA-001",
    "IA-002",
    "IA-003",
    "RG-001"
  ],
  "clean_context_review": {
    "mode": "Inline fallback",
    "rounds_completed": 3,
    "context_isolation": "Approximated"
  }
}
```
