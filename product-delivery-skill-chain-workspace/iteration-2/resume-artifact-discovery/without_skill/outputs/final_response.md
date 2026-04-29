我在当前目录里找到了这些最新候选文件，但不能直接继续往下执行，因为它们不是同一个需求链路。

已发现的候选：

- PRD：`D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\docs\member-renewal-prd.md`
  - 主题：会员续费，包含月包/年包、续费后更新会员到期时间、失败支付不变更权益。
- technical-design：`D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\technical-design.md`
  - 主题：账单周期变更审批，涉及 `billing_cycle_change_requests`、审批/拒绝 API。
- tasks：`D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\tasks.md`
  - 主题：账单周期变更任务，和 technical-design 匹配，但和会员续费 PRD 不匹配。
- 审核标准：未在当前给定目录中找到明显的 `audit standards` / `quality standards` / `review` 文件。

阻塞点：

- 最新 PRD 是“会员续费”，但最新 technical-design 和 tasks 是“账单周期变更”。
- 缺少与“会员续费”匹配的 technical-design、tasks 和审核标准。
- 如果继续执行，可能会把不同需求的产物错误拼接，导致后续开发方向错误。

建议下一步：

请确认要继续哪个需求：

1. 继续“会员续费”：我需要基于 `member-renewal-prd.md` 重新生成或查找对应的 technical-design、tasks 和审核标准。
2. 继续“账单周期变更”：应改用 `specs\billing\prd.md` 作为 PRD，并沿用当前 `technical-design.md` 和 `tasks.md`。

在你确认前，我不会进入实现阶段，也不会修改代码。
