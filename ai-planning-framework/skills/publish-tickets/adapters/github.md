# Adapter: github

Used by `skills/publish-tickets/SKILL.md` when `tickets.target: github`. Maps framework tickets into GitHub Issues. **Dry-run until GitHub access exists.**

## Config keys

- `tickets.github` — `owner`, `repository`, optional `project` (GitHub Projects board), `default_labels`
- `secrets.github_token_env` — env var **name** for the token; never read or print its value

Token: a connected GitHub connector where available, else the env var named by `secrets.github_token_env`.

Stop and report if any of these is still a `<placeholder>`.

## Field mapping

| GitHub field / artefact | Source |
|------------------------|--------|
| Issue title | `[T-<DOMAIN>-NNN] <title> (<page type>)` from ticket heading: after `Ticket: <ID> — ` plus page type from the Type field |
| Issue body | Full markdown body: User story (As a / I want / So that) + Full-stack scope table + **Acceptance criteria** (Given / When / Then) + Work to do / Out of scope + `Source:` footer with spec / excel paths |
| Labels | Stable ID, feature slug, page type, `ai-planning-framework`, plus `default_labels` |
| Story vs task | UI page / Manage list / cross-cutting story → issue; explicit child task → sub-issue of the parent issue |
| Attachments | Links to `excel/*.xlsx` and `specs/*.yaml` in the repository (relative paths under `work/<feature>/`) |
| Upsert | Search issues by the stable ID label (or title prefix `[T-<DOMAIN>-NNN]`); update if found, else create |

### Title

```text
[T-BOOK-001] Add | Edit Book Basic Form (Form Modal)
```

The title includes:
- The stable ID in brackets: `[T-<DOMAIN>-NNN]`
- The ticket heading text after `Ticket: <ID> — `
- The page type in parentheses: `(<page type>)`. Use the specific page type from the ticket when available (e.g. `Form Modal`, `Wizard Modal`, `Paginated Grid`), otherwise use the Type field value verbatim (e.g. `Schema`, `API service`)

### Description body (preserve GWT as Acceptance criteria)

Copy from the ticket markdown into the GitHub issue description (Markdown). Keep the ticket markdown **as written**, including the full Given / When / Then scenarios:

1. **User story** — As a / I want / So that
2. **Full-stack scope** — table of UI label ↔ Service / Target DB Table / Target DB Column (or Population Source)
3. **Work to do** — the full Work to do section
4. **Acceptance criteria** — Full Given / When / Then scenarios as written in the ticket, **plus** a clearly marked checkable summary section
5. **Out of scope** if present
6. Footer: `Source: work/<feature>/tickets/<filename>` plus linked spec/excel paths

**Acceptance criteria section format:**

After the full Given/When/Then scenarios (kept as written in the ticket), add a checkable summary under an `## Acceptance criteria (summary)` heading:

```markdown
## Acceptance criteria

### Scenario: S1 — Add mode opens with defaults

```gherkin
Given I have the required permission
When I open the Add form
Then required fields are empty
And boolean fields are Off
And multi-value fields have no items
```

### Scenario: S2 — Create record with required fields

```gherkin
Given I open the Add form
And today's local date is after the minimum allowed date
When I enter Name "Example"
And I enter Date Born "01/01/2020"
And I leave optional fields empty
And I save the form
Then the form closes successfully
And the service writes the record with the entered values
...
```

(... all scenarios as written in the ticket ...)

## Acceptance criteria (summary)

- [ ] S1 — Add mode opens with defaults
- [ ] S2 — Create record with required fields
- [ ] S3 — Name is mandatory
- [ ] S4 — Duplicate name is rejected on Save
- [ ] S5 — Name can be reused after deletion
- [ ] S6 — Date must be valid
- [ ] S7 — Date is mandatory
- [ ] S8 — Tags persist as JSON
- [ ] S9 — Tag limits apply
- [ ] S10 — Edit persists changed fields
- [ ] S11 — Only Add and Edit modes exist
- [ ] S12 — Deleted record cannot be opened
```

The full Given/When/Then is **required**, not optional. The checkable summary provides a quick overview for developers and testers.

### Labels

Always include:
- `ai-planning-framework`
- stable ID as a label, e.g. `T-BOOK-001`
- feature slug from the ticket's Feature field (lowercase with hyphens, e.g. `manage-books`)
- page type label: map the Type field value to a consistent label (e.g. `UI page` → `ui-page`, `Form Modal` → `form-modal`, `Paginated Grid` → `paginated-grid`)
- Any labels specified in `tickets.github.default_labels`

Label naming convention: lowercase with hyphens (kebab-case).

### Sub-issues

When a ticket is **explicitly typed as a child implementation task** in its Type field (not merely having a Depends on field), create it as a **sub-issue** of the parent GitHub issue.

**Important:** A "Depends on" field indicates a dependency relationship but does not make a ticket a sub-issue. Most tickets have dependencies and are still standalone issues (Type: Schema, API service, UI page, etc.). Only create sub-issues when the Type field explicitly says it's a child task under a parent story.

Dependencies should be recorded in the issue body (in the Work to do or Dependencies section) with references like "Depends on #123" or by stable ID.

GitHub sub-issues require:
1. The parent issue must already exist (create parent before children)
2. Use the GitHub API's sub-issue creation endpoint or relationship
3. The Type field must explicitly indicate a child task relationship

### Attachments / links

GitHub issues don't support file attachments in the same way as Azure DevOps. Instead:
- Link every listed `excel/*.xlsx` and `specs/*.yaml` in the issue body footer
- Use relative repository paths if the specs/excel are in the same repo
- Use full GitHub URLs if cross-repo: `https://github.com/<owner>/<repo>/blob/<branch>/work/<feature>/excel/<file>.xlsx`

Example footer:

```markdown
---

**Source:** `work/<feature>/tickets/T-<DOMAIN>-NNN-<slug>.md`

**Specs:**
- [<page>.yaml](../work/<feature>/specs/<page>.yaml)
- [<page>.xlsx](../work/<feature>/excel/<page>.xlsx)
```

## Upsert

Search existing issues by the stable ID label (e.g. `T-BOOK-001`) OR title prefix `[T-<DOMAIN>-NNN]`. 

If found → update the issue:
- Update title, body, and labels
- Preserve the issue number and URL
- Do not change state (open/closed)

If not found → create a new issue with all fields.

Never create duplicate issues for the same stable ID.

## Project board

If `tickets.github.project` is configured:
- Automatically add new issues to the specified GitHub Project
- The project name is used to look up the project ID via the GitHub API
- New issues are added to the project's default column/view
- Existing project automation (e.g. "Auto-add to project") may handle this automatically

## Live publish

Only when the GitHub connector is connected **or** the env var named by `secrets.github_token_env` exists, **and** the user explicitly asks to publish. 

Record each GitHub issue number in the ticket Notes (optional) and in `handoff.md` (`devops_work_item_id`, kept as the field name for any tracker, plus `devops.board_url` with the issue URL).

## Authentication

Access priority:
1. A connected GitHub connector (MCP or Cursor-native) — use this where available
2. The env var named by `secrets.github_token_env` (read the variable name from config, never the value)
3. If neither exists, stop and report; prepare a dry-run only

Never read, print, log, or commit a token value.
