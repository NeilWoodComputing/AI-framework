# Adapter: azure-devops

Used by `skills/publish-tickets/SKILL.md` when `tickets.target: azure-devops`. Maps framework tickets into Azure DevOps (ADO) work items. **Dry-run until ADO access exists.**

## Config keys

- `tickets.azure_devops` — `organisation`, `project`, `area_path`, `iteration_path`, `work_item_types` (`story` / `task`), `default_tags`
- `secrets.azure_devops_pat_env` — env var **name** for the token; never read or print its value

Stop and report if any of these is still a `<placeholder>`.

## Field mapping

| ADO field / artefact | Source |
|----------------------|--------|
| Work item type | `tickets.azure_devops.work_item_types.story` (e.g. `User Story`) for UI page / Manage list / cross-cutting story tickets; `work_item_types.task` (e.g. `Task`) only when the markdown Type is explicitly a child implementation task under a parent story |
| Title | From ticket heading: after `Ticket: <ID> — ` (or `## User story` capability if heading missing) |
| Description | Full markdown body: User story (As a / I want / So that) + Full-stack scope table + Acceptance criteria (Given / When / Then) + Work to do |
| Area Path | `tickets.azure_devops.area_path`; placeholder `{{area_path}}` until configured |
| Iteration Path | `tickets.azure_devops.iteration_path`; placeholder `{{iteration_path}}` until configured |
| Tags | Feature name, page type, stable ID, plus `default_tags` (`ai-planning-framework`) |
| Links / attachments | Relative paths to matching `excel/*.xlsx` and `specs/*.yaml` from the ticket Specs field; attach or link both when publishing |
| Custom / discussion | Stable ID (`T-<DOMAIN>-NNN`) for upsert matching |

### Title

```text
[T-BOOK-001] Add | Edit Book (Form Modal)
```

Prefer including the stable ID in the ADO title for human searchability.

### Description body (preserve GWT)

Copy from the ticket markdown into the ADO description (HTML or Markdown per project convention):

1. **User story** — As a / I want / So that  
2. **Full-stack scope** — table of UI label ↔ Service / Target DB Table / Target DB Column (or Population Source)  
3. **Acceptance criteria** — every Given / When / Then scenario  
4. **Work to do** and **Out of scope** if present  
5. Footer: `Source: work/<feature>/tickets/<filename>` plus linked spec/excel paths

### Area / Iteration

```text
Area Path:      {{area_path}}        # e.g. <project>\<area>
Iteration Path: {{iteration_path}}   # e.g. <project>\Sprint 42
```

Do not invent Area or Iteration values. Leave placeholders or omit until the user supplies them.

### Tags

Always include:

- `ai-planning-framework`
- stable ID as a tag, e.g. `T-BOOK-001`
- feature slug or Feature field value
- optional: `FormModal`, `BasicForm`, `WizardModal`, `FullPageWizard`, `PaginatedGrid`, `EmbeddedGridModal`, `Import` from page type

### Attachments / links

- Attach or link every listed `excel/*.xlsx`
- Attach or link every listed `specs/*.yaml`
- Prefer linking repo/workspace paths if ADO attachment size is a concern; otherwise attach the xlsx

## Upsert

Search by the stable ID tag (or title prefix `[T-<DOMAIN>-NNN]`). Found → update description, links and tags. Not found → create.

## Live publish

Only when the Azure DevOps connector is connected **and** the user explicitly asks to publish. Record each ADO work item ID in the ticket Notes (optional) and in `handoff.md` (`devops_work_item_id`, `devops.board_url`).
