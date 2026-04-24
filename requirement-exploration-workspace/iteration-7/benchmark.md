# requirement-exploration iteration-7 benchmark

- with_skill mean pass_rate: 0.83
- without_skill mean pass_rate: 0.75
- delta pass_rate: +0.08
- with_skill mean time_seconds: 28.8
- without_skill mean time_seconds: 22.72
- delta time_seconds: +6.08

## Notes
- coupon-module-late-stage-defaults 成功补到了新的区分盲点：with_skill 能 review + readiness + authorization，baseline 仍倾向先替用户拍默认口径再继续。
- incomplete-prd-late-stage 出现反向结果：with_skill 重新滑回多点补问，baseline 反而完成了 review + non-blocking + authorization，说明 draft-based late-stage 行为仍不稳定。
- approval-center-late-stage 仍有区分度，但 baseline 比上一轮更强，已经会先做简版 review，再追一个它认为阻塞的问题。
- short-membership-request 继续不具备区分度：两边首轮都足够克制，说明这个样本现在更像回归保护而不是拉开差距的主力样本。
- 本轮 with_skill 平均耗时高于 baseline，说明当前收益问题既有 late-stage 规则稳定性，也有一定的额外交互成本。
