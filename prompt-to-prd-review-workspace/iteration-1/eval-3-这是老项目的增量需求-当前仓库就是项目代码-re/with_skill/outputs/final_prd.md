# 订单售后部分退款原因标签 PRD

## 1. 背景

现有订单售后模块需要在运营审核部分退款时补充后台可见的原因标签，帮助运营、客服和管理人员在退款列表、退款详情和导出报表中识别部分退款原因。

本 PRD 基于 requirement-exploration 已产出的提示词生成，属于老项目增量需求。首版只增加部分退款原因标签的选择、展示、筛选和导出，不改变现有退款金额、退款状态、售后审批权限、支付退款、库存、通知或 C 端展示逻辑。

## 2. Existing Product Context and Compatibility

### 2.1 当前项目上下文

| Context Item | Inspection Result | PRD Impact |
| --- | --- | --- |
| Requirement mode | Existing project iteration | PRD 按现有订单售后模块增量改造处理 |
| Project path | `D:\sun-skills` | 已检查当前仓库作为项目上下文 |
| Relevant code availability | 未在仓库中发现实际订单售后、退款列表、退款详情、权限或导出代码 | PRD 不写具体路由、接口名、组件名、表名或字段名；仅定义产品行为和兼容约束 |
| Source priority | 当前用户指令 > requirement-exploration 提示词 > 当前仓库检查结果 > 明示假设 | 当代码缺失时，以提示词作为产品事实来源 |

### 2.2 受影响的现有产品区域

| Existing Area | Current Behavior to Preserve | Required Change | Must Preserve | Risk |
| --- | --- | --- | --- | --- |
| 订单售后部分退款审核 | 运营使用现有售后审核能力审核部分退款 | 审核部分退款时必须选择一个原因标签 | 现有审核权限、审核动作、退款金额和状态流转 | 未找到实际审核代码，具体入口需实现阶段按现有系统确认 |
| 退款列表 | 后台查看退款/售后记录 | 支持按原因标签筛选 | 默认列表能力、分页、排序、其他筛选条件 | 历史单无标签，筛选语义需明确 |
| 退款详情页 | 后台查看退款详情和操作信息 | 展示原因标签和操作人 | 现有详情字段、操作记录、C 端不可见边界 | 未找到现有详情页字段布局 |
| C 端退款展示 | 用户查看退款进度或状态 | 不展示原因标签和后台操作人 | C 端文案、状态、通知和隐私边界 | 前后端均需避免泄露后台字段 |
| 权限体系 | 售后审核权限控制审核行为 | 沿用现有售后审核权限；不新增角色 | 不新增角色、不新增独立权限口径 | 未找到现有权限定义 |
| 导出报表 | 后台导出退款相关数据 | 新增原因标签字段 | 现有导出范围、权限、筛选条件和字段顺序约定 | 未找到现有导出实现，字段位置需按现有报表规范落地 |
| 历史退款单 | 已存在退款单保持当前记录 | 不补录原因标签 | 历史记录真实性和审计一致性 | 历史导出/详情/筛选需允许空值 |

## 3. Goals and Non-Goals

### 3.1 Goals

- 运营审核部分退款时可以从固定原因标签中选择一个原因。
- 原因标签仅后台可见，C 端用户不展示。
- 历史退款单不补录原因标签。
- 后台退款列表支持按原因标签筛选。
- 后台退款详情页展示原因标签和操作人。
- 退款导出报表包含原因标签字段。
- 权限沿用现有售后审核权限，不新增角色。

### 3.2 Non-Goals

- 不改变现有退款金额计算、退款支付、库存回滚、优惠权益、通知或订单状态逻辑。
- 不新增 C 端展示、提醒、筛选或解释文案。
- 不新增角色、独立权限点或新的审核流程。
- 不为历史退款单补录、推断或批量生成原因标签。
- 不在首版决定“已审核通过后是否允许修改原因标签”；该事项作为开放问题记录。
- 不定义具体接口协议、数据库表结构、迁移脚本或组件实现方案。

## 4. Users and Scenarios

| User/Role | Scenario | Expected Result |
| --- | --- | --- |
| 运营人员 | 审核部分退款 | 必须选择一个原因标签后才能提交审核 |
| 运营人员 | 查看退款列表 | 可以按原因标签筛选部分退款记录 |
| 运营人员 | 查看退款详情 | 可以看到原因标签和操作人 |
| 运营人员 | 导出退款报表 | 导出文件中包含原因标签字段 |
| 售后主管/管理人员 | 复盘部分退款原因 | 可以在后台列表、详情和报表中识别原因分布 |
| C 端用户 | 查看自己的退款进度或结果 | 不看到后台原因标签和后台操作人 |
| 系统 | 处理历史退款单 | 不要求历史单补录原因标签，历史空值保持为空 |

## 5. Scope

### 5.1 In Scope

- 在后台部分退款审核动作中增加原因标签选择。
- 标签固定为：商品缺货、商品破损、运费差额、客服补偿、其他。
- 原因标签对部分退款审核为必填项。
- 后台退款列表增加原因标签筛选能力。
- 后台退款详情展示原因标签和操作人。
- 退款导出报表增加原因标签字段。
- 历史退款单保持无标签状态，不补录。
- 沿用现有售后审核权限控制选择、查看和导出行为。

### 5.2 Out of Scope

- 已审核通过后修改标签的能力。
- 标签自定义、标签增删改、标签多选、标签层级或原因备注。
- 对全额退款、仅退款、退货退款等其他退款类型强制增加原因标签，除非现有系统将其明确归类为部分退款审核。
- C 端展示或解释原因标签。
- 独立 BI 看板、原因统计图表或自动归因。

## 6. User Journey / Workflow

### 6.1 运营审核部分退款

1. 运营进入现有订单售后模块中的部分退款审核入口。
2. 系统展示现有退款审核信息，并新增原因标签选择项。
3. 运营从固定标签中选择一个：商品缺货、商品破损、运费差额、客服补偿、其他。
4. 运营提交审核。
5. 系统校验当前操作人具备现有售后审核权限，且部分退款审核已选择原因标签。
6. 校验通过后，系统按现有退款流程继续处理，同时记录原因标签、操作人和操作时间。
7. 校验失败时，不提交审核动作，并提示运营补充标签或处理权限/状态异常。

### 6.2 后台退款列表筛选

1. 运营进入现有退款列表。
2. 系统在现有筛选条件中提供原因标签筛选项。
3. 默认不按原因标签过滤，展示符合其他条件的全部记录，包括无标签历史记录。
4. 运营选择某个原因标签后，列表仅展示该标签对应的退款记录。
5. 历史无标签记录不命中任何具体原因标签筛选。

### 6.3 后台退款详情查看

1. 运营进入退款详情页。
2. 对已有原因标签的部分退款记录，系统展示原因标签和操作人。
3. 对历史无标签记录，系统展示为空值、短横线或遵循现有后台空字段展示规范。
4. C 端用户访问退款详情或退款状态时，不展示原因标签和后台操作人。

### 6.4 导出报表

1. 具备现有售后审核/导出权限的后台用户触发退款报表导出。
2. 导出结果包含原因标签字段。
3. 有标签记录输出对应标签中文值。
4. 历史无标签记录该字段为空值或遵循现有导出空值规范。
5. 导出筛选范围沿用现有退款导出规则；若导出入口支持退款列表当前筛选条件，则原因标签筛选也应被纳入导出范围。

## 7. Functional Requirements

### 7.1 原因标签字段

| Item | Requirement |
| --- | --- |
| 字段含义 | 运营审核部分退款时选择的业务原因标签 |
| 标签选项 | 商品缺货、商品破损、运费差额、客服补偿、其他 |
| 选择方式 | 单选 |
| 是否必填 | 部分退款审核必填 |
| 默认值 | 新审核记录默认未选择；历史退款单保持空值 |
| 可见范围 | 后台可见，C 端不可见 |
| 记录对象 | 与对应退款/售后记录关联 |
| 操作人 | 记录提交或确认部分退款审核的后台操作人 |

### 7.2 部分退款审核

| Requirement ID | Requirement |
| --- | --- |
| FR-01 | 当审核对象为部分退款时，审核表单必须展示原因标签选择项。 |
| FR-02 | 部分退款审核提交前必须校验已选择原因标签。 |
| FR-03 | 未选择原因标签时，系统不得提交审核动作，并提示运营选择原因标签。 |
| FR-04 | 审核提交成功后，系统记录原因标签、操作人和操作时间。 |
| FR-05 | 原因标签记录不得改变现有退款金额、退款方式、退款状态、支付退款、库存或通知逻辑。 |

### 7.3 退款列表筛选

| Requirement ID | Requirement |
| --- | --- |
| FR-06 | 退款列表应提供原因标签筛选项，筛选项包含全部固定标签。 |
| FR-07 | 默认状态不按原因标签过滤，历史无标签记录正常展示。 |
| FR-08 | 选择具体标签后，仅展示该标签对应记录。 |
| FR-09 | 历史无标签记录不命中任何具体原因标签筛选。 |
| FR-10 | 原因标签筛选应与现有列表搜索、分页、排序和其他筛选条件兼容。 |

### 7.4 退款详情

| Requirement ID | Requirement |
| --- | --- |
| FR-11 | 后台退款详情页展示原因标签。 |
| FR-12 | 后台退款详情页展示原因标签对应的操作人。 |
| FR-13 | 历史无标签记录按现有后台空字段规范展示。 |
| FR-14 | C 端退款详情、退款进度、退款通知和退款结果页不得展示原因标签或后台操作人。 |

### 7.5 导出报表

| Requirement ID | Requirement |
| --- | --- |
| FR-15 | 退款导出报表包含原因标签字段。 |
| FR-16 | 有标签记录输出固定标签中文值。 |
| FR-17 | 历史无标签记录输出为空值或现有导出空值规范。 |
| FR-18 | 若现有导出支持按当前列表筛选导出，原因标签筛选条件应同步影响导出结果。 |

### 7.6 权限

| Requirement ID | Requirement |
| --- | --- |
| FR-19 | 选择原因标签和提交部分退款审核沿用现有售后审核权限。 |
| FR-20 | 查看后台原因标签、详情操作人和导出原因标签字段沿用现有售后审核/后台退款查看/导出权限组合，不新增角色。 |
| FR-21 | 无对应后台权限的用户不得通过列表、详情、导出或接口获得原因标签。 |

## 8. Business Rules

| Rule ID | Rule |
| --- | --- |
| BR-01 | 原因标签仅适用于运营审核部分退款的场景。 |
| BR-02 | 每条适用的部分退款审核记录只能选择一个原因标签。 |
| BR-03 | 标签选项为固定枚举：商品缺货、商品破损、运费差额、客服补偿、其他。 |
| BR-04 | 新增功能上线后产生的部分退款审核记录必须有原因标签。 |
| BR-05 | 上线前已存在的历史退款单不补录原因标签。 |
| BR-06 | 历史无标签记录在列表默认状态、详情和导出中保持可见。 |
| BR-07 | 选择具体原因标签筛选时，历史无标签记录不应出现在结果中。 |
| BR-08 | 原因标签和操作人只对后台授权用户可见。 |
| BR-09 | C 端用户、C 端接口响应、C 端通知和 C 端页面不得展示或泄露原因标签和后台操作人。 |
| BR-10 | 权限沿用现有售后审核权限，不新增角色。 |
| BR-11 | 是否允许修改已审核通过的原因标签尚未决定；首版 PRD 不承诺该能力。 |

## 9. Permissions and Roles

| Role/User Type | Can Select Tag During Partial Refund Review | Can View Tag in Backend List/Detail | Can Export Tag | Can See Tag on C-End | Notes |
| --- | --- | --- | --- | --- | --- |
| 具备现有售后审核权限的运营 | Yes | Yes, if existing backend refund visibility allows | Yes, if existing export permission allows | No | 不新增角色 |
| 售后主管/后台管理人员 | Depends on existing after-sales/refund permissions | Depends on existing backend refund visibility | Depends on existing export permission | No | 沿用现有权限模型 |
| 无售后审核/退款查看权限的后台用户 | No | No | No | No | 不应通过接口或导出绕过权限 |
| C 端用户 | No | No | No | No | 不展示、不返回后台标签字段 |

## 10. Data, Records, and State Changes

### 10.1 Data Definitions

| Data Item | Description | Required | Source | Visibility |
| --- | --- | --- | --- | --- |
| 原因标签 | 部分退款原因，固定枚举之一 | 新增部分退款审核记录必填；历史记录可为空 | 运营审核时选择 | 后台授权用户 |
| 操作人 | 提交或确认部分退款审核的后台用户 | 新增有标签记录必填 | 当前后台登录用户/现有审计操作者 | 后台授权用户 |
| 操作时间 | 原因标签随审核动作记录的时间 | 新增有标签记录必填 | 审核提交成功时间 | 后台授权用户 |

### 10.2 State and Record Behavior

| Current State | Trigger | Next State | Actor | New Tag Behavior |
| --- | --- | --- | --- | --- |
| 部分退款待审核 | 运营提交审核且选择原因标签 | 沿用现有审核结果状态 | 运营 | 记录原因标签、操作人、操作时间 |
| 部分退款待审核 | 运营提交审核但未选择原因标签 | 状态不变 | 运营 | 拦截提交并提示补充 |
| 退款记录已存在且无标签 | 功能上线 | 状态不变 | 系统 | 不补录，原因标签保持空值 |
| 已审核通过 | 尝试修改原因标签 | 未定 | 运营/后台用户 | 作为开放问题记录，首版不定义可修改能力 |

### 10.3 Historical Records

- 上线前历史退款单不补录原因标签。
- 历史无标签记录在默认列表、详情和导出中仍可被查看或导出。
- 历史无标签记录不应被归入“其他”标签。
- 导出中历史无标签记录的原因标签字段为空值或遵循现有导出空值规范。

### 10.4 Audit and Reporting

- 原因标签应与对应退款/售后记录形成可追溯关系。
- 操作人应使用现有后台审计主体；如现有系统已有“审核人”字段，可复用其产品语义，但不得让 PRD 语义变成不记录操作人。
- 导出报表中的原因标签字段用于运营复盘，不代表新增 BI 指标口径。

## 11. UI States and Exception Handling

| Scenario | Expected Behavior |
| --- | --- |
| 部分退款审核页面加载中 | 沿用现有后台加载状态；原因标签区域不得阻塞其他非依赖信息展示 |
| 标签选项加载失败或配置不可用 | 不允许提交部分退款审核；提示稍后重试或联系管理员 |
| 未选择标签提交 | 拦截提交，提示选择原因标签 |
| 无售后审核权限访问审核入口 | 沿用现有无权限处理，不展示可操作标签选择 |
| 列表筛选无结果 | 显示现有空结果状态 |
| 历史无标签详情 | 原因标签和操作人按空字段规范展示，不误标为“其他” |
| 导出失败 | 沿用现有导出失败提示和重试机制 |
| 重复提交审核 | 不应产生重复原因标签记录或重复审核结果；以现有审核幂等/防重规则为准 |
| 审核并发 | 若退款状态已被其他操作改变，沿用现有状态冲突处理，不应只更新标签而绕过审核状态校验 |

## 12. Acceptance Criteria

| ID | Scenario | Given | When | Then |
| --- | --- | --- | --- | --- |
| AC-01 | 部分退款审核选择标签 | 运营具备现有售后审核权限，退款单为部分退款待审核 | 运营选择“商品缺货”并提交审核 | 审核按现有流程提交，退款记录保存“商品缺货”、操作人和操作时间 |
| AC-02 | 部分退款审核未选标签 | 运营具备现有售后审核权限，退款单为部分退款待审核 | 运营未选择原因标签并提交 | 系统拦截提交，退款状态不变，并提示选择原因标签 |
| AC-03 | 固定标签选项 | 运营打开部分退款审核页面 | 查看原因标签选择项 | 仅可选择商品缺货、商品破损、运费差额、客服补偿、其他中的一个 |
| AC-04 | 列表默认展示 | 后台退款列表存在有标签新记录和无标签历史记录 | 运营未选择原因标签筛选 | 列表展示符合其他筛选条件的有标签和无标签记录 |
| AC-05 | 列表按标签筛选 | 存在多个原因标签的退款记录和无标签历史记录 | 运营选择“客服补偿”筛选 | 列表仅展示原因标签为“客服补偿”的记录，无标签历史记录不展示 |
| AC-06 | 详情展示 | 有标签部分退款记录审核成功 | 运营打开后台退款详情 | 页面展示原因标签和操作人 |
| AC-07 | 历史详情 | 历史退款记录无原因标签 | 运营打开后台退款详情 | 原因标签按空字段规范展示，不显示为“其他” |
| AC-08 | C 端不可见 | C 端用户查看退款进度、结果或详情 | 退款记录存在原因标签 | C 端页面和响应不展示原因标签或后台操作人 |
| AC-09 | 导出字段 | 退款记录存在原因标签 | 后台用户导出退款报表 | 导出文件包含原因标签字段，且有标签记录输出对应中文标签 |
| AC-10 | 历史导出 | 导出范围包含历史无标签记录 | 后台用户导出退款报表 | 历史记录原因标签字段为空值或现有导出空值规范 |
| AC-11 | 权限沿用 | 后台用户没有现有售后审核/退款查看权限 | 访问审核、详情、列表或导出相关能力 | 系统沿用现有权限拦截，不新增角色也不暴露原因标签 |
| AC-12 | 不影响退款核心流程 | 运营审核部分退款并选择标签 | 审核提交成功 | 退款金额、退款状态、支付退款、库存、通知和 C 端展示按原有规则执行 |

## 13. Risks, Assumptions, and Open Questions

### 13.1 Assumptions

| Assumption | Impact |
| --- | --- |
| “部分退款”沿用现有系统中的退款类型或售后审核分类，不在 PRD 中重新定义。 | 实现阶段需映射到现有退款类型字段或流程判断。 |
| 操作人使用现有后台审计主体或审核人语义。 | 避免新增独立身份体系。 |
| 原因标签字段对后台授权用户可见，对 C 端完全不可见。 | 前后端都需要避免通过页面或接口泄露。 |
| 已审核通过后的标签修改能力不在首版范围内。 | 该能力待开放问题确认后再进入后续需求。 |

### 13.2 Non-Blocking Open Questions

| Question | Type | Impact | Owner/Decision Needed |
| --- | --- | --- | --- |
| 是否允许运营修改已审核通过的原因标签？ | Non-blocking Open Question | 会影响详情页操作入口、权限、审计记录、导出更新口径和历史准确性；不影响首版必填选择、展示、筛选和导出。 | 产品/业务负责人需后续确认。 |

### 13.3 Compatibility Risks

| Risk | Mitigation in PRD |
| --- | --- |
| 当前仓库未暴露实际订单售后模块代码，无法确认具体页面、接口、字段和权限命名。 | PRD 只定义产品行为，不绑定具体实现名称；实现前需按真实代码补充技术设计。 |
| 历史无标签记录可能被误归为“其他”。 | 明确历史空值不得归入“其他”。 |
| 后台字段可能意外进入 C 端接口或页面。 | 明确 C 端不可见为业务规则和验收项。 |
| 导出字段与现有报表字段顺序/空值规范不一致。 | 要求遵循现有导出规范，新增原因标签字段并定义空值行为。 |

### 13.4 Post-MVP Follow-ups

- 若业务确认允许修改已审核通过的标签，需要补充修改入口、权限、二次确认、修改原因、修改前后值审计和导出更新规则。
- 若运营需要复盘原因分布，可后续定义统计报表或 BI 指标口径。
- 若标签选项需要业务可配置，可后续定义标签管理能力。

## Review Record

- Frontend review: Approved
- Backend review: Approved
- Requirement mode: Existing project iteration
- File treatment: New PRD
- Project context reviewed: `D:\sun-skills` workspace structure, git status, recursive source/doc listing, order/refund/after-sale keyword search, prompt-to-PRD skill references, task eval metadata
- Source priority applied:
  - Latest user instruction in current task
  - Requirement-exploration downstream prompt
  - Current repository inspection result
  - Explicit assumptions recorded in this PRD
- Review summary:
  - Frontend review required clearer partial-refund form validation, list filter behavior, historical empty states, and backend-only visibility; PRD was updated accordingly.
  - Backend review required clearer lifecycle recording, operator/audit behavior, export behavior for historical records, and preservation of existing refund core flows; PRD was updated accordingly.
  - Final frontend and backend role reviews approved the revised PRD as coherent enough to save as the current product baseline.
- Decisions and conflict handling:
  - No frontend/backend conflict remained after revision.
  - Because application code was not available in the inspected workspace, exact implementation names were not invented and the limitation is recorded as a compatibility risk.
- Remaining open questions:
  - Non-blocking Open Question: 是否允许运营修改已审核通过的原因标签？
- Post-MVP follow-ups:
  - Define post-approval tag modification if approved by business.
  - Consider reason distribution reporting/BI only after the field is adopted.
  - Consider configurable reason tags only if fixed enum no longer satisfies operations.
