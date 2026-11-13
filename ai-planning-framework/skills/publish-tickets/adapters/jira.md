# Adapter: jira (stub)

Used by `skills/publish-tickets/SKILL.md` when `tickets.target: jira`. **Stub:** the outline below is the intended mapping; until it is completed and `tickets.jira` is added to the config, the skill stops at a dry-run.

## Config keys (to add when implemented)

- `tickets.jira` — `site` (e.g. `<your-site>.atlassian.net`), `project_key`, `issue_types` (`story` / `task`), optional `components`, `default_labels`
- Token: a connected Jira connector where available, else an env var **name** under `secrets` (e.g. `jira_token_env`); never read or print its value. **Not yet in the shared config:** the human owner adds `secrets.jira_token_env` when this adapter is implemented (agents do not edit `secrets`).

## Intended mapping

| Jira field | Source |
|------------|--------|
| Summary | `[T-<DOMAIN>-NNN] <title> (<page type>)` |
| Description | Ticket markdown as written (user story, Full-stack scope, Given / When / Then, Work to do / Out of scope) + `Source:` footer with spec / excel paths |
| Issue type | `issue_types.story`; `issue_types.task` (sub-task) only for an explicit child task |
| Labels | Stable ID, feature slug, page type, `ai-planning-framework`, plus `default_labels` |
| Attachments | Attach or link `excel/*.xlsx` and `specs/*.yaml` |
| Upsert | JQL search on the stable ID label; update if found, else create |
