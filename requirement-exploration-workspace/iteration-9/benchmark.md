# requirement-exploration iteration-9 benchmark

- with_skill mean pass_rate: 1.0
- without_skill mean pass_rate: 0.92
- delta pass_rate: +0.08
- with_skill mean time_seconds: 27.0
- without_skill mean time_seconds: 29.69
- delta time_seconds: -2.69

## Notes
- 这次更硬的最小修补打中了 incomplete-prd-late-stage：with_skill 不再把 draft-based late-stage 拉回 bundled follow-up round，而是先做 review + readiness + authorization。
- 不过 baseline 在 approval-center-late-stage、coupon-module-late-stage-defaults，甚至 short-membership-request 上也明显自然收敛了，整体区分度继续被压缩。
- coupon-module-late-stage-defaults 里 with_skill 仍然更像结构化 closeout review，baseline 也开始接受默认假设直接往下写，但少了更清楚的 confirmed-versus-pending 分层。
- approval-center-late-stage 里 with_skill 继续保持 review + default boundary + authorization 的完整闭环，baseline 这轮也接近通过，说明该样本更适合做回归保护而不是高区分度样本。
- 当前主要问题已从 draft-based late-stage bundled round 转为：如何在 baseline 普遍自然改进的情况下，继续保持 with_skill 的稳定区分度。
