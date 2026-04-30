## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## skill create
- 保持主文档的整洁，将可拆分内容拆分，采用按需加载的形式
- 子代理内容可以抽离出来 

## Git
- git commit message使用中文

## Bash Command

**核心原则：主执行链不阻塞，长进程后台托管。**

### 基本规则
- 使用 `py` 执行 Python 脚本
- 主执行链只运行会自然退出的命令
- 长进程（dev server、watch、队列消费者等）必须后台托管

### 后台托管要求
启动脚本必须在 10-15 秒内完成：
1. 停止旧 PID
2. 启动新进程并重定向日志
3. 写入真实服务 PID
4. 快速退出

### 验证与清理
- 启动成功 ≠ 业务可用，用独立 smoke 命令验证（端口、HTTP、健康检查）
- 启动卡住时先检查 PID/端口/日志，不要重复启动
- 临时测试进程验证后清理 PID；用户服务不擅自停止
- 环境限制导致后台启动失败时说明原因，不要改回前台阻塞

## Extra
- 减少不必要的客套话、冗余修饰词，直接输出观点，建议，方案等内容
- 在编写代码时，对主要功能相关函数变量等内容带上注释，使用中文
- 非必要操作时，使用中文输出
