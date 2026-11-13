# Template: inline PR comment

Used only in loop stage 9 when `review.provider` is `azure-devops` and `review.publish.enabled` and `review.publish.post_inline_comments` are `true`. Never used for `github`, `cursor-origin` or `local-git`: PR posting is off until Azure DevOps is in use. One comment per finding, anchored at the finding's `file:line`. The text must match the finding in the report.

## Inline comment

```markdown
**[<Severity>] <short title>** · <Area> · F-<NN>

<What is wrong and why it matters, in one or two sentences.>

**Spec / rule:** `<specs/page.yaml → section → control>` | `<tickets/T-<DOMAIN>-NNN-*.md → Scenario: name>` | `<rule file → heading>`
**Suggested fix:** <Concrete change. A short code suggestion is fine.>

<sub>ai-review-framework · PR-<id> · <DD/MM/YYYY> · full report: `<feature_path>/reviews/PR-<id>-review.md`</sub>
```

## Summary comment

Used when `review.publish.post_summary_comment` is `true`. Posted once per review iteration.

```markdown
## AI review — <Approve | Approve with comments | Request changes>

Checked against <T-<DOMAIN>-NNN, …> and `specs/<page>.yaml`, with <rule sets applied>.

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| <n> | <n> | <n> | <n> |

<Two or three sentences on the main reasons for the verdict.>

Full report: `<feature_path>/reviews/PR-<id>-review.md`

<sub>ai-review-framework · iteration <n> · commit `<short-sha>` · a human reviewer still owns the merge decision</sub>
```

## Rules

- Keep the tone factual and specific. Name the control, column or scenario.
- Do not post Nits inline unless the team asks; leave them in the report.
- Never include tokens, connection strings or personal data from fixtures in a comment.
- Do not reply to or resolve human comments.
