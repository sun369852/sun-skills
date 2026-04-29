已读取这些输入文件：

- `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\prd.md`
- `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\technical-design.md`
- `D:\sun-skills\product-delivery-skill-chain\evals\files\chain-demo\specs\billing\tasks.md`

当前可以从 `tasks.md` 进入实现前准备，但我不会直接开始写代码，因为你明确要求“先别全自动，开始写代码前让我确认”。

可执行任务：

- T001 Create cycle change request model
- T002 Add request creation API
- T003 Add approval and rejection APIs

暂不执行：

- T004 Add billing settings UI，因为任务中标记为 blocked，阻塞原因是 final UI copy not confirmed。

实现前确认点：

- 实现范围只覆盖后端模型、创建 API、审批/拒绝 API。
- 不修改已有已支付发票，保持 invoice records immutable。
- 验证应覆盖 model unit tests、API integration tests、approval/rejection integration tests，以及现有 invoice generation 回归测试。
- UI 任务等文案确认后再处理。

请确认是否开始执行 T001-T003。确认后我再进入代码实现。
