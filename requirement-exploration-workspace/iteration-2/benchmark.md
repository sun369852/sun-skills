# requirement-exploration iteration-2 benchmark

- with_skill mean pass_rate: 0.55
- without_skill mean pass_rate: 0.33
- delta pass_rate: +0.22
- with_skill mean time_seconds: 68.14
- without_skill mean time_seconds: 68.16
- delta time_seconds: -0.02

## Notes
- 第二轮评测把重心从首轮起手行为，推进到了接近收口时的中后程行为。
- short-membership-request 仍有区分度：with_skill 更克制，baseline 更容易扩成小型 intake form。
- approval-center-late-stage 与 incomplete-prd-late-stage 都暴露出同一个真实缺口：with_skill 仍然倾向继续追问，而不是先做待确认项/风险项回顾并显式征求生成授权。
- 承接已有上下文而不重开流程，现在更像基础护栏，两边都能做到；真正缺的仍是收口切换机制。
