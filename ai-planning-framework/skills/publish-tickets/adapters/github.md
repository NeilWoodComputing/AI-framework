# Adapter: github (stub)

Used by `skills/publish-tickets/SKILL.md` when `tickets.target: github`. **Stub:** the outline below is the intended mapping; until it is completed and `tickets.github` is added to the config, the skill stops at a dry-run.

## Config keys (to add when implemented)

- `tickets.github` — `owner`, `repository`, optional `project` (GitHub Projects board), `default_labels`
- Token: a connected GitHub connector where available, else the env var named by `secrets.github_token_env` (never read or print its value)

## Intended mapping

| GitHub field | Source |
|--------------|--------|
| Issue title | `[T-<DOMAIN>-NNN] <title> (<page type>)` |
| Issue body | Ticket markdown as written (user story, Full-stack scope, Given / When / Then, Work to do / Out of scope) + `Source:` footer with spec / excel paths |
| Labels | Stable ID, feature slug, page type, `ai-planning-framework`, plus `default_labels` |
| Story vs task | Story → issue; explicit child task → sub-issue or task-list item of the parent issue |
| Attachments | Links to `excel/*.xlsx` and `specs/*.yaml` in the repository |
| Upsert | Search issues by the stable ID label (or title prefix); update if found, else create |
