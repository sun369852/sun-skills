已按 `product-delivery-skill-chain` 的 Resume Mode 做保守发现。

我找到的同一条需求链路是 `specs/billing`：

- PRD: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\prd.md`
- Technical design: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\technical-design.md`
- Tasks: `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\tasks.md`
- Audit standards: 未找到

我没有使用 `docs/member-renewal-prd.md`、`docs/refund-prd.md` 或 `specs/invoice/prd.md` 作为这次链路源头，因为它们分别是会员续费、退款原因、发票重发主题，和 `specs/billing` 下的 technical design/tasks 不一致。

当前阶段判断：

- Entry stage: resume artifact discovery
- Current stage: Audit Standards Gate
- 已有可信产物：billing PRD、technical design、tasks
- 缺失产物：审核标准
- 下一步应路由到：`prd-quality-audit-standards`

因为 billing cycle 涉及账单日期、审批、未来发票影响和审计历史，属于需要明确验收契约的业务流程，不能跳过审核标准直接进入实现。生成审核标准并与现有 technical design/tasks 做轻量 reconcile 后，再停在 Implementation Gate，等待你确认是否开始编码。

