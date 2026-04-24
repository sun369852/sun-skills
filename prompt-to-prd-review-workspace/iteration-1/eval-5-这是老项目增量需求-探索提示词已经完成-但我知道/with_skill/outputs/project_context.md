# Project Context Inspection

## Requirement Mode

Existing project iteration.

## Source Prompt

在现有发票模块增加“电子发票重发”能力。财务后台可以对已开具成功的电子发票重发邮件；重发不改变发票号码、金额、抬头和开票状态；需要记录重发操作人、时间、收件邮箱。用户端不新增入口。旧文档说发票邮件只能发送一次，但当前线上客服已经有手工重发流程。未定：是否限制每天重发次数。

## Source Priority Applied

1. Latest user instruction in this eval task.
2. Requirement-exploration prompt embedded in `eval_metadata.json`.
3. Existing docs/code, if available.
4. Reasonable assumptions, only if labeled.

## Files and Paths Inspected

- `D:\sun-skills\prompt-to-prd-review\SKILL.md`
- `D:\sun-skills\prompt-to-prd-review\references\core-workflow.md`
- `D:\sun-skills\prompt-to-prd-review\references\input-and-context.md`
- `D:\sun-skills\prompt-to-prd-review\references\prd-content.md`
- `D:\sun-skills\prompt-to-prd-review\references\review-and-iteration.md`
- `D:\sun-skills\prompt-to-prd-review\references\finalize-and-record.md`
- `D:\sun-skills\prompt-to-prd-review\agents\frontend-prd-reviewer.md`
- `D:\sun-skills\prompt-to-prd-review\agents\backend-prd-reviewer.md`
- `D:\sun-skills\prompt-to-prd-review-workspace\iteration-1\eval-5-这是老项目增量需求-探索提示词已经完成-但我知道\eval_metadata.json`
- `D:\sun-skills\prompt-to-prd-review-workspace\iteration-1\eval-5-这是老项目增量需求-探索提示词已经完成-但我知道\with_skill\outputs\`

## Search Result

No actual invoice module code, old invoice PRD, API files, frontend routes, backend services, schemas, migrations, permission definitions, or email integration files were present under the target eval-5 directory.

Workspace-level search found only prior eval artifacts and the eval metadata prompt. It did not provide a real current invoice module to validate.

`rg` could not be executed in this desktop sandbox because the bundled `rg.exe` path was denied by the OS. PowerShell `Get-ChildItem` and `Select-String` were used as fallback.

## Affected Existing Areas Inferred From The Prompt

These are inferred from the prompt, not verified against code:

| Area | Inferred Current Behavior | Required Change | Must Preserve | Risk |
| --- | --- | --- | --- | --- |
| Finance admin invoice module | Finance/admin users can view issued invoices | Add resend email action for successfully issued electronic invoices | Existing invoice identity, amount, title, and issued status | Cannot confirm current page, permissions, table/detail patterns, or terminology |
| Invoice email sending | Old docs say invoice email can only be sent once | Formalize a controlled resend action | Original invoice data and issue result | Current manual customer-service flow conflicts with old docs |
| Customer-service manual flow | Prompt says online customer service already manually resends | Finance backend feature should not break or duplicate manual handling unexpectedly | Operational traceability | Current implementation/SOP not available |
| Audit/operation log | Not confirmed | Record resend operator, resend time, recipient email | Historical resend records | Cannot confirm existing audit log format |
| User-facing invoice pages | Prompt says no new user entry | No new user-side route/button/copy | Existing user flow unchanged | Frontend must avoid surfacing action to users |

## Current-State Conflict

The source prompt contains a current-state conflict:

- Old documentation says invoice email can only be sent once.
- Current online customer service already has a manual resend flow.
- The requested feature asks to add a formal finance-admin resend ability.

This conflict should be recorded in the PRD. It is not enough to silently treat either the old documentation or the current manual flow as fully authoritative. The latest requirement appears to authorize a formal resend capability, but the exact compatibility relationship with the manual customer-service flow remains unverified because no project files or SOPs were available.

## Open Questions Classification

| Question | Type | Reason |
| --- | --- | --- |
| 是否限制每天重发次数？ | Blocking Open Question | This changes action eligibility, frontend button disabled/error states, backend rate-limit behavior, audit/failure semantics, and abuse/operational controls. A final PRD cannot define testable acceptance criteria for resend availability without this decision. |
| 旧文档“一次发送”与当前客服手工重发流程以哪个为准？ | Non-blocking if the latest prompt is accepted as authoritative; blocking if the business still requires old one-time semantics | The latest prompt explicitly requests a formal resend feature and names the manual flow as current reality, so the PRD can treat the old doc as stale only if product accepts this source-priority decision. |

