# requirement-exploration iteration-17 benchmark

- with_skill mean pass_rate: 1.0
- without_skill mean pass_rate: 0.63
- delta pass_rate: +0.37
- with_skill mean time_seconds: 42.88
- without_skill mean time_seconds: 38.55
- delta time_seconds: +4.34

## Notes
- iteration-15 的最小规则补丁命中了主回归：with_skill 在 entitlement-record-identity-migration 上不再默认代答，而是停在单个 blocking 问题上等待用户确认。
- entitlement-snapshot-history-freeze 继续保持单 blocking 问题模式，说明补丁没有把相邻历史语义样本推回到默认建议式 closeout。
- without_skill 在两条新增样本上仍倾向于给建议默认口径并继续往下，说明这轮修补保持了技能的区分度。
- event-registration-vague-authorization 已重新纳入汇总；with_skill 继续要求明确授权，without_skill 仍会把模糊表态当作放行信号。
- coupon-module-late-stage-defaults 在 iteration-17 已恢复为非阻塞收口：with_skill 会把叠加规则等项标成默认边界并继续请求显式生成授权。
