# Artifact Directory

Use this reference to keep chain artifacts in one request folder instead of scattering them across downstream skill defaults.

## Core Rule

When `product-delivery-skill-chain` is invoked for a new request, preview the chain start contract first. After the user confirms it, establish a single chain artifact directory before saving new durable artifacts. By default, all chain artifact directories live under a project-root `delivery/` folder. Pass explicit output paths to downstream skills so their outputs land in the selected request folder.

Direct downstream skill usage keeps the downstream skill's own path rules and does not need a chain artifact directory.

## Directory Selection

Choose the chain artifact directory with this priority:

1. Use the user's explicit output directory.
2. If resuming from an existing `delivery-chain-status.md`, use its directory.
3. If the user provides an existing feature/spec folder that already contains related artifacts, use that folder.
4. If starting from existing files outside `delivery/`, create a new request folder under project-root `delivery/` after contract confirmation, then copy those files into `source/`.
5. If starting from scratch, create `delivery/<timestamp9>-<feature-slug>/` under the current workspace or project root after the feature slug is clear.
6. If no safe feature slug can be inferred, ask one focused question for the requirement name before creating the directory.

Never silently mix unrelated features in the same artifact directory. If a candidate directory already has a `delivery-chain-status.md` for another feature, create a new sibling directory or ask the user.

## Request Folder Name

Default request folder format:

```text
delivery/<timestamp9>-<feature-slug>/
```

Use:

- `timestamp9`: the last 9 digits of the current Unix timestamp in seconds, left-padded with zeroes if needed
- `feature-slug`: a short lowercase kebab-case requirement name inferred from the PRD title, user wording, or confirmed feature name

Examples:

- `delivery/769338420-member-renewal/`
- `delivery/769338421-invoice-resend/`

If the user supplies a Chinese requirement name, translate or summarize it into a stable English slug unless the project already uses Chinese folder names.

## Standard Filenames

Use stable filenames unless the user requests otherwise:

- `delivery-chain-status.md`
- `chain-start-contract.md`
- `source-context.md`
- `prd.md`
- `technical-design.md`
- `quality-audit-standards.md`
- `tasks.md`
- `implementation-handoff-packet.md`
- `implementation-run-<yyyy-mm-dd-HHmm>.md`
- `implementation-review-report.md`
- `review-fix-packet-<n>.md`

If updating an existing artifact, preserve its path only when it belongs to the current chain artifact directory or the user explicitly asks to update it in place.

## Existing External Artifacts

If the chain starts from an artifact outside the chosen chain directory:

- Do not move or modify the original.
- Copy a snapshot into `<chain-dir>/source/` after the user confirms the chain start contract.
- Create `<chain-dir>/source/source-manifest.md` with original path, copied path, role, and copy time.
- Create `<chain-dir>/source-context.md` that combines current user context, inferred artifact relationships, entry stage, missing inputs, and assumptions.
- Record copied source files and original source paths in `delivery-chain-status.md`.
- Save new downstream artifacts in the chain artifact directory.

If source-of-truth ambiguity matters, state that the original file remains the source until the chain produces or confirms the standardized artifact inside the request folder.

## Downstream Output Paths

When invoking downstream skills from the chain, pass explicit paths:

- `prompt-to-prd-review` -> `<chain-dir>/prd.md`
- `prd-to-tech-design-review` -> `<chain-dir>/technical-design.md`
- `prd-quality-audit-standards` -> `<chain-dir>/quality-audit-standards.md`
- `prd-task-archiver` -> `<chain-dir>/tasks.md`
- `tdd-task-implementation-orchestrator` -> run log beside `<chain-dir>/tasks.md`, preferably `<chain-dir>/implementation-run-<yyyy-mm-dd-HHmm>.md`
- `implementation-review-handoff` -> `<chain-dir>/implementation-review-report.md` when a saved report is requested or useful

Record every chosen output path in `delivery-chain-status.md` before or immediately after invoking the downstream skill.

## Subdirectories

Keep the default flat folder for normal features. Use subdirectories only when the artifact set becomes large:

- `source/` for copied external inputs
- `reviews/` for multiple review reports or clean-context review outputs
- `runs/` for many implementation run logs

Avoid deep folder structures unless the user asks or the chain produces many versions.
