# Product Delivery Skill Chain Evals

These evals focus on orchestration behavior rather than downstream artifact quality.

## Coverage

- `id: 1` requirement entry: vague input should route to requirement exploration and avoid premature downstream work.
- `id: 2` PRD entry: existing PRD should skip upstream discovery, plan technical design plus audit standards, then stop before coding.
- `id: 3` fast planning: draft tasks can run with technical design and audit standards only when parallel execution is authorized, then must be reconciled.
- `id: 4` resume: artifact discovery should be conservative and should not silently choose ambiguous files.
- `id: 5` task entry: implementation handoff should be prepared, but coding should wait for human confirmation.
- `id: 6` direct downstream skill: explicit non-chain usage should not create `delivery-chain-status.md`.
- `id: 7` context management: after a long interview has been saved into a PRD, the chain should continue from the PRD path and compact summary instead of carrying full conversation history.
- `id: 8` artifact directory: chain outputs should be centralized in one requested folder, with external source artifacts copied into `source/`.
- `id: 9` default artifact directory: new requests should preview a project-root `delivery/<timestamp9>-<feature-slug>/` request folder before creating it.
- `id: 10` first-time defaults: missing project defaults should trigger a concise options-based contract interview.
- `id: 11` git handoff: implementation delivery should record commit authorization without replacing the implementation orchestrator's commit rules.
- `id: 12` invocation envelope: downstream calls should carry contract policy, output paths, and source artifacts.
- `id: 13` technical-design-to-tasks: task archiving can start from technical design only when a linked PRD is available.

## Running

Use the `a-skill-creator` evaluation workflow when subagent/baseline execution is authorized:

1. Run each eval with `product-delivery-skill-chain`.
2. Run the baseline without the chain skill.
3. Grade outputs against `expectations` in `evals.json`.
4. Compare whether the chain skill improves routing, gate discipline, and status-file handling.

These evals do not require fixture files by default; they test planning and routing decisions from user prompts.
