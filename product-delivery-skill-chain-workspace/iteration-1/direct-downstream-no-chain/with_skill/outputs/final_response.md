无法生成 `tasks.md`：指定 PRD 文件不存在。

失败路径：

```text
D:\sun-skills\docs\refund-prd.md
```

按照 `prd-task-archiver` 的规则，缺少可读取 PRD 时不能根据文件名或周边上下文推断需求，也不能编造任务归档。请提供正确的 PRD 路径或直接粘贴完整 PRD 内容后，我再基于 PRD 拆分任务并保存 `tasks.md`。

本次没有启动代码实现，也没有创建 `delivery-chain-status.md`，因为这是直接调用下游 skill，不是链路编排模式。
