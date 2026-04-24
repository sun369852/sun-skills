# requirement-exploration iteration-3 benchmark

- with_skill mean pass_rate: 0.78
- without_skill mean pass_rate: 0.44
- delta pass_rate: +0.34
- with_skill mean time_seconds: 78.24
- without_skill mean time_seconds: 62.96
- delta time_seconds: +15.28

## Notes
- 第三轮补入 late-stage cue 规则后，with_skill 在 draft-based late-stage 场景里明显改善，已经能做 gap review、readiness judgment 和显式征求下一步。
- approval-center-late-stage 仍未稳定命中目标行为；模型虽然感知到收口语境，但把收口误写成了一轮更大的补充问答。
- without_skill 在 approval-center-late-stage 上意外表现更好，说明该场景里“先总结已确认项，再只追一个阻塞点”是一个自然策略，skill 目前反而把它压偏了。
- 当前 skill 的主要剩余问题不是是否会进入收口阶段，而是收口阶段里何时允许继续追问、以及追问数量必须被强限制。
