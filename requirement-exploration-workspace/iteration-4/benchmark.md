# requirement-exploration iteration-4 benchmark

- with_skill mean pass_rate: 0.89
- without_skill mean pass_rate: 0.67
- delta pass_rate: +0.22
- with_skill mean time_seconds: 70.13
- without_skill mean time_seconds: 51.97
- delta time_seconds: +18.17

## Notes
- 第四轮的小修正修好了 approval-center-late-stage：with_skill 现在能先做 review，再征求是否按默认边界进入生成。
- 但 incomplete-prd-late-stage 从 iteration-3 的 3/3 回落到 2/3，说明“只追 1 个阻塞问题”的新规则压得有点过头，让模型更倾向继续卡最后一个问题，而不是给出“现在也可生成”的双路径收口。
- short-membership-request 在 iteration-4 已不再区分 with_skill 和 baseline，两边都表现得足够克制，说明这个 eval 更适合留作回归检查，而不是主区分项。
- 当前最合适的下一步不是继续迭代大规则，而是把 late-stage 行为拆成两条：真正阻塞才追 1 个问题；非阻塞缺口则先给双路径授权。
