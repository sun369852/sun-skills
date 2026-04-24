# requirement-exploration iteration-12 benchmark

- with_skill mean pass_rate: 0.92
- without_skill mean pass_rate: 0.71
- delta pass_rate: +0.21
- with_skill mean time_seconds: 29.24
- without_skill mean time_seconds: 25.2
- delta time_seconds: +4.04

## Notes
- 新增的 certificate-module-single-blocking-gap 暴露出一个新的 late-stage 漏洞：with_skill 会把实际上应先拍板的身份规则边界降级成非阻塞待确认项，直接进入 authorization。
- 新增的 event-registration-vague-authorization 继续证明当前 skill 在授权边界上是有效的：with_skill 会拒绝把‘你觉得行就行’当成明确授权，而 baseline 会直接开始生成。
- content-permission-late-stage-boundaries 仍然是稳定的主判别样本：with_skill 先做 closeout review、readiness judgment 和 authorization，baseline 仍倾向直接进入生成。
- coupon-module-late-stage-defaults 继续接近饱和，pricing-plan-late-stage-authorization 也已不再提供明显区分度，因此 iteration-12 的主要价值转向扩样本查漏而不是继续追旧回归。
- 下一轮最值得做的最小修补，是把 truly blocking gap 的判断再收紧：凡是会改变核心业务对象身份、权益归属、状态语义或历史数据解释的未决规则，不应轻易降级成非阻塞假设。
