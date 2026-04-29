无法继续执行到技术设计、审核标准和正式 `tasks.md`。

原因：任务要求从 `specs/invoice/prd.md` 开始，但本次 eval 标注 `Input files: none`，当前工作区也没有找到该 PRD 文件。没有 PRD 内容时，继续生成技术设计、审核标准或任务草案会变成编造需求。

需要补充：
- `specs/invoice/prd.md` 的实际文件内容或可访问路径

拿到 PRD 后，我会按快速模式处理：
1. 基于 PRD 生成技术设计。
2. 基于 PRD 生成开发前审核标准。
3. 基于 PRD 生成任务草案。
4. 对齐技术设计、审核标准和任务草案中的冲突。
5. 输出正式 `tasks.md`，并说明哪些任务来自 reconcile 修正。
