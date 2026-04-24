# Finalize and Record

Use this reference before choosing the output path, saving the PRD, or writing the review/version record.

## Output Path

If the user provides a path, save there after approval.

If no path is provided:

- for existing projects, look for existing directories such as `docs/`, `docs/prd/`, `specs/`, `requirements/`, `product/`, or prior PRD naming patterns
- if a matching convention exists, follow it
- otherwise save a clear Markdown file in the current workspace, such as `[feature-name]-prd.md`

Do not create surprising directory structures for old projects. Prefer the project's existing documentation style.

## New File vs Existing PRD Update

If the user gave an existing PRD and asked for an increment, update or create according to their wording.

If unclear:

- create a new incremental PRD when the new requirement is a discrete feature/change
- update the existing PRD only when the user asks to modify it or it is clearly the same feature baseline

Record whether the file is a new PRD or an update to an existing one.

## Versioning

For new PRDs, start with version `1.0` and record the creation date.

For updated PRDs, increment version based on change scope:

- minor clarifications or additions: `1.0` to `1.1`
- significant scope changes or rewritten baseline: `1.0` to `2.0`

For major rewrites, consider preserving the old version separately before saving the new baseline.

## Save Gate

Save only when:

- the current PRD draft includes all approved changes
- frontend review is approved
- backend review is approved
- no blocking open questions remain
- any non-blocking open questions are clearly recorded
- current-state conflicts are either resolved or explicitly recorded as non-blocking
- review history has enough detail to explain why the final draft was accepted

## Save Failure Handling

If file writing fails, do not lose the approved PRD content.

Possible causes:

- target path does not exist and cannot be created
- permission denied
- disk full
- file locked by another process
- filename invalid for the operating system

Resolution:

1. Report the specific error and intended path.
2. Ask the user for an alternative: retry same path, choose a different path, save to workspace root, or output the PRD in conversation as a temporary fallback.
3. Preserve the approved PRD content in memory or a safe alternate workspace file if possible.
4. Record the save attempt and resolution in the review record once a file is successfully saved.

### Partial Save

If a file is created but appears truncated or corrupted:

1. Re-read the file or check file size when possible.
2. Retry the save.
3. If the retry succeeds, overwrite the partial content with the complete PRD.
4. If retry fails, use the save failure flow above.

Do not delete an existing user file unless the user explicitly approves. If the partial file is newly created by this run, it may be overwritten by the successful retry.

### Save Success Verification

After saving:

1. Confirm the file exists at the expected path.
2. Verify it contains the title and Review Record.
3. When practical, read the beginning and ending of the file to check completeness.
4. If verification fails, treat it as a save failure.

## Review Record Template

Append this section to the saved PRD:

```markdown
## Review Record

- PRD Version: [1.0 or incremented version]
- Created/Updated: [date]
- Frontend review: Approved
- Backend review: Approved
- Requirement mode: [New requirement / New requirement with existing dependencies / Existing project iteration]
- File treatment: [New PRD / Updated existing PRD]
- Project context reviewed: [N/A or concise paths/modules/docs]
- Source priority applied:
  - [Latest user instruction / requirement prompt / existing PRD / code/docs, etc.]
- Review summary:
  - [Change 1]
  - [Change 2]
- Review history:
  - Round 1: [Frontend/backend key findings and changes]
  - Round 2: [Only if applicable]
- Decisions and conflict handling:
  - [Decision or "None"]
- Remaining open questions:
  - [Question and type, or "None"]
- Post-MVP follow-ups:
  - [Follow-up or "None"]
```

## Conversation Summary After Saving

After saving, report:

- file path
- whether frontend and backend review both approved
- main changes made during review
- project areas considered for existing-project iterations
- remaining non-blocking open questions or post-MVP follow-ups

Keep the response concise. The file is the durable artifact.
