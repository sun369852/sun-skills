进入 `product-delivery-skill-chain` 的 Resume Mode。

我在 `D:\sun-skills` 下做了保守发现，但没有找到一组可以直接信任为“上次那个需求”的完整产物。不能继续往下执行，因为最新候选分散在不同需求和不同 workspace 中，静默拼接会把无关 PRD、技术设计、任务和审核标准混在一起。

发现的关键信号：

- 最新链路状态文件是 `D:\sun-skills\product-delivery-skill-chain-workspace\iteration-1\fast-planning-reconcile\with_skill\outputs\delivery-chain-status.md`，但它指向的 PRD `D:\sun-skills\specs\invoice\prd.md` 不存在，当前状态是 blocked。
- 最新可信 PRD 候选是 `D:\sun-skills\prd-to-tech-design-review-workspace\fixtures\payment-refund\prd.md`。
- 最新技术设计候选是 `D:\sun-skills\prd-to-tech-design-review-workspace\iteration-2-second-pass\payment-refund\with_skill\outputs\technical-design.md`，它看起来和 payment-refund PRD 同主题。
- 最新任务候选是 `D:\sun-skills\prd-task-archiver-workspace\iteration-1\eval-update-existing-archive\with_skill\outputs\billing-cycle-tasks-updated.md`，主题是 billing-cycle，和 payment-refund 不匹配。
- 最新审核标准候选是 `D:\sun-skills\prd-quality-audit-standards-workspace\iteration-2\eval-5-draft-admission\with_skill\outputs\approval-flow-quality-audit-standards.md`，主题是 approval-flow，和 payment-refund 不匹配。

可选下一步：

1. 继续 `payment-refund`：使用已发现的 PRD 和技术设计，接下来补生成审核标准与任务归档，然后在编码前停下确认。
2. 继续最新链路状态里的 `invoice`：需要你提供或创建 `D:\sun-skills\specs\invoice\prd.md`，否则不能进入规划。
3. 指定另一个需求目录或其中任一源文件，我再按该目录内的同主题产物恢复链路。

阻塞问题：你要我继续哪个需求？如果不指定，我建议选择 `payment-refund`，因为它是当前扫描中唯一同时找到 PRD 和技术设计且主题一致的候选。
