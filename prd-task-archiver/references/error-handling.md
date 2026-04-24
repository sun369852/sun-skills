# Error Handling

Read this file when an input path, PRD source, project path, or output path cannot be used safely.

## Missing or Unreadable PRD

If the PRD path is missing, does not exist, or cannot be read:

- do not generate a task archive
- ask one focused question for the correct PRD path or pasted PRD content
- mention the path that failed, when one was provided
- do not infer requirements from the filename or surrounding project alone

If the user supplied pasted content but it is empty or truncated, ask for the complete PRD or the missing section.

## Non-PRD or Incomplete Source

If the source document is a short idea, chat note, technical design, bug report, or implementation sketch rather than a PRD:

- do not silently convert it into a PRD
- explain that this skill needs an existing PRD or sufficiently complete PRD content
- list the most important missing PRD pieces only when helpful, such as goal, users, scope, requirements, business rules, and acceptance criteria
- suggest returning to requirement exploration or PRD review before task archiving

Proceed only when the source is complete enough to map requirements to tasks without inventing product semantics.

## Malformed PRD

If the PRD is readable but poorly structured:

- extract requirements from headings, lists, tables, and acceptance criteria when possible
- preserve uncertainty as assumptions or blocked tasks
- ask one focused question only if the missing information would change core ownership, permissions, state transitions, data history, or acceptance criteria
- avoid broad questionnaires

If the PRD contains multiple independent features:

- prefer separate task archives when the features can ship independently or touch mostly different product areas
- keep one archive when the features are tightly coupled into one delivery and share the same release risk
- if the choice changes ownership, sequencing, or release planning, ask one focused question: separate archives or one combined delivery plan

## Missing or Invalid Project Path

If the user says this is an existing-project iteration but the project path is missing or invalid:

- use the current workspace only when it is clearly the target project
- otherwise ask one focused question for the project path
- if the PRD is self-contained and project context is optional, proceed as a new-feature archive and record `Project context reviewed: N/A`
- do not claim project conventions were inspected when they were not

If project files are unavailable but the user still wants a task archive, mark file/module suggestions as `To be discovered` and list compatibility risks explicitly.

## Output Path Conflicts

If the selected output file already exists:

- update it only when the user explicitly asked to update the existing archive
- otherwise create a versioned filename such as `<feature-slug>-tasks-v2.md`
- mention the conflict and the chosen path in the final response

If the output directory cannot be created or written:

- choose the nearest safe writable project/workspace location when obvious
- otherwise ask one focused question for an output path
- do not pretend the archive was saved
