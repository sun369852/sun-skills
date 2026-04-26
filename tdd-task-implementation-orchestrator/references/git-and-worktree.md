# Git And Worktree

## Branches

The orchestrator may create a local branch for development, using the default prefix `codex/` unless the user requests another name.

Do not push unless the user explicitly asks.

## Commits

Commits are allowed, but the scope must be strict:

- commit only changes produced by this execution run
- do not include unrelated pre-existing user changes
- do not include unrelated formatting, lockfile churn, or temporary files
- prefer one commit per verified task batch or feature area
- combine very small tasks only when they belong to the same feature area
- do not combine cross-domain tasks into one commit
- do not commit failing work unless the user explicitly allows a WIP commit

Commit messages should include:

- task ids or feature area
- short implementation summary
- verification command summary

The run log can be committed with the corresponding batch.

## Worktrees

Git worktree use is optional. Consider it when:

- multiple workers run in parallel and write scopes are near each other
- a high-risk or experimental implementation needs isolation

Record:

- worktree path
- branch name
- task batch
- merge or discard result

Run verification before merging worktree output back. Do not use worktrees to bypass conflict management. Shared contract tasks still run serially.
