已进入 `product-delivery-skill-chain` 的 Fast Planning Mode，但当前被源产物阻塞。

当前判断：
- 入口阶段：PRD
- 请求模式：快速规划模式
- 请求目标：从 `specs/invoice/prd.md` 生成技术设计、审核标准、任务草案，并 reconcile 成正式 `tasks.md`
- 并行意图：用户明确要求“尽量并行”，可视为授权并行规划；但本次尚未进入并行执行，因为 PRD 文件缺失
- 源产物状态：未找到 `D:\sun-skills\specs\invoice\prd.md`

我没有继续生成技术设计、审核标准或任务草案，因为这会违反链路规则：下游规划必须依赖可信 PRD，不能静默套用无关 PRD 或自行补全产品事实。

需要你补充一个阻塞信息：

请提供正确的 invoice PRD 文件路径，或把 `specs/invoice/prd.md` 放到当前工作区后再继续。

已生成状态文件草案：
- `delivery-chain-status.md`
