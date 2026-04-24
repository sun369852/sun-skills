# Late-Stage Review

Use this reference when the conversation is already near completion and the user signals near-readiness with cues like:
- 差不多了
- 先继续
- 你看看还缺不缺
- 如果够了就往下走
- 还有没有遗漏
- 可以开始了吗

## Default Behavior

At this stage, do not default to asking a fresh clarification question.

First do these steps instead:
1. summarize what is already confirmed
2. list what is still unresolved, risky, or assumption-heavy
3. judge whether the requirement is already complete enough to proceed
4. explicitly ask whether to start final generation

The default late-stage behavior is review first, not another discovery round.

## Gap Types

Separate remaining gaps into two types:
- blocking gap: a missing decision that would make the final downstream prompt clearly distorted, internally inconsistent, or materially misleading if left unanswered now
- non-blocking gap: a missing detail that should be surfaced, but can be carried as an explicit assumption, default boundary, or follow-up note without preventing useful final generation

Treat a gap as blocking if leaving it unresolved would change the meaning of a core business object, ownership or identity of a record, state transition semantics, or historical record semantics in the final prompt.

Treat a gap as non-blocking by default only when the uncertainty can be honestly preserved in the final prompt as a stated assumption, pending item, or default boundary without changing those core meanings.

Do not call a gap blocking just because resolving it would make the prompt nicer, more complete, or less ambiguous around a secondary edge case.

## When a Blocking Gap Exists

If a truly blocking gap remains:
- explain why it is blocking
- ask only one blocking question
- do not expand it into a checklist or multi-part follow-up round
- do not ask a second new question in the same response
- do not propose a default answer and continue; wait for the user to resolve it first

## When Only Non-Blocking Gaps Remain

If only non-blocking gaps remain:
- do not keep the conversation stuck in another discovery round
- give the review first
- state that generation can already start based on the current information
- make unresolved items explicit as assumptions, optional refinements, or follow-up confirmations
- ask whether to generate now as-is, or whether the user wants to answer the last non-blocking point first
- do not continue into generation in the same response after that review; wait for explicit authorization

## Draft-Based Late-Stage Cases

If the conversation is based on an existing PRD/spec draft and is already late-stage:
- treat the draft as something to review and stress-test first
- do not reopen a broad coverage checklist
- do not bundle several cleanup questions together
- unless there is exactly one clearly blocking gap, do the closeout review, mark remaining items as assumptions or pending confirmations, make a readiness judgment, and ask whether to generate now

## Authorization Rule

If the user gives vague approval such as “差不多吧” or “你觉得行就行”, do not treat it as generation authorization. Ask again for explicit permission.
