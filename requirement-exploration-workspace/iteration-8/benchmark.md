# requirement-exploration iteration-8 benchmark

- with_skill mean pass_rate: 0.83
- without_skill mean pass_rate: 0.67
- delta pass_rate: +0.17
- with_skill mean time_seconds: 27.13
- without_skill mean time_seconds: 29.17
- delta time_seconds: -2.04

## Notes
- 这次最小修补没有打中 incomplete-prd-late-stage：with_skill 仍然把 draft-based late-stage 场景重新拉回 bundled follow-up round。
- coupon-module-late-stage-defaults 仍然保持区分度：with_skill 是 review + readiness + authorization，baseline 还是先替用户拍默认口径。
- approval-center-late-stage 也依旧有效，但 baseline 已经会先做 closeout review，再追一个它认为更关键的剩余问题。
- short-membership-request 再次显示为回归保护样本：with_skill 保持短促，baseline 又轻微回到了模板化回答。
- 当前主要瓶颈不是覆盖不到 late-stage，而是 draft-based late-stage 仍缺少更硬的反 bundled-round 约束。
