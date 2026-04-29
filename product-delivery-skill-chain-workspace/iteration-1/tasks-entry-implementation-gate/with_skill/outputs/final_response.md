当前阶段判断：你调用的是 `product-delivery-skill-chain`，并指定从 `specs/billing/tasks.md` 进入实现阶段。

我检查到阻塞点：`D:\sun-skills\specs\billing\` 目录不存在，因此无法读取：

- `D:\sun-skills\specs\billing\tasks.md`
- 同目录下的 PRD
- 同目录下的技术方案

按链路规则，这一步需要先通过 Task Archive Gate 和 Implementation Gate：实现前至少要有可执行任务列表，并能关联 PRD / 技术方案作为上下文。现在这些源产物都不可用，所以不能把任务交给 `tdd-task-implementation-orchestrator`，也不会开始写代码。

下一步需要你确认或提供正确路径：请给出真实的 `tasks.md` 路径，或补齐 `specs/billing/` 下的任务、PRD、技术方案文件。拿到可用产物后，我会先准备 implementation handoff packet，并在写代码前停下来让你确认。
