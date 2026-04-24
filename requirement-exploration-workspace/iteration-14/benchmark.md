# requirement-exploration iteration-14 benchmark

- with_skill mean pass_rate: 0.93
- without_skill mean pass_rate: 0.74
- delta pass_rate: +0.19
- with_skill mean time_seconds: 32.62
- without_skill mean time_seconds: 25.11
- delta time_seconds: +7.51

## Notes
- 新增的 entitlement-record-identity-migration 暴露了新的回归：with_skill 虽然识别到账号合并会改变历史记录归属与含义，但仍直接给出默认方案并继续生成，没停在单个 blocking 问题上。
- 新增的 entitlement-snapshot-history-freeze 同样暴露了相同模式：with_skill 会把真正 blocking 的历史快照定义问题改写成默认建议，而不是先向用户追问。
- 两条新增样本说明：现有规则能解释 why-blocking，但还缺一条更强的 late-stage约束，禁止在 blocking gap 仍未确认时主动给默认方案并表示继续生成。
- event-registration-vague-authorization 仍是重要对照，后续修补必须避免把 '再次索取明确授权' 与 '追问 blocking gap' 混成一类。
- coupon-module-late-stage-defaults 仍是非阻塞对照，后续修补必须继续保证普通默认项不会被误升级。
