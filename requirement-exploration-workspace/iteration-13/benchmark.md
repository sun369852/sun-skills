# requirement-exploration iteration-13 benchmark

- with_skill mean pass_rate: 1.0
- without_skill mean pass_rate: 0.71
- delta pass_rate: +0.29
- with_skill mean time_seconds: 27.86
- without_skill mean time_seconds: 26.86
- delta time_seconds: +1.01

## Notes
- 最小补丁命中了新增的 certificate-module-single-blocking-gap：with_skill 不再把会改变证书历史含义的改名重发规则降级成 non-blocking，而是停在单个阻塞问题上。
- event-registration-vague-authorization 仍然通过，说明这次修补没有破坏明确授权边界。
- content-permission-late-stage-boundaries 继续保持 late-stage closeout + 单阻塞问题模式，没有被误放大成重新开一轮 discovery。
- coupon-module-late-stage-defaults 仍按非阻塞待确认项处理，说明本轮补丁没有把一般默认项误升级为 blocking。
- 下一步若继续迭代，重点应从‘blocking gap 定义是否过宽’转向‘这条新规则在更多身份/历史语义样本上是否稳定’。
