# Skill: publish-tickets

Map `work/<feature>/tickets/*.md` into work items in the project's ticket tracker. The tracker is chosen by `tickets.target` in the config, and each tracker has an **adapter** under `adapters/`:

| `tickets.target` | Adapter | Status |
|------------------|---------|--------|
| `azure-devops` | `adapters/azure-devops.md` | Mapping complete; dry-run until access exists |
| `github` | `adapters/github.md` | Mapping complete; dry-run until access exists |
| `jira` | `adapters/jira.md` | Stub: mapping outline only |

**Dry-run until tracker access exists**: do not call a live connector from this skill yet; prepare payloads and upsert rules so another agent can publish when access is granted. (This skill was called `publish-devops-tickets` before the framework became tracker-neutral.)

## Config first

Read `ai-framework.config.yaml` at the `ai-framework` root (`../ai-framework.config.yaml` from the planning-framework root; its paths are relative to the `ai-framework` root):

- `tickets.enabled`, `tickets.target` and the target's own block (e.g. `tickets.azure_devops`) — read the matching adapter for which keys it needs
- `tickets.id_prefix` and `tickets.upsert` — stable ID pattern and upsert rule
- the feature folder — resolve `work/<feature>/` as in `AGENT-BRIEF.md` → *Where features live*
- `secrets.*_env` — the env var **name** holding the tracker token; never read or print its value into files

**Stop and report** (dry-run at most) if `tickets.enabled` is `false`, `tickets.target` has no adapter, the adapter is a stub, or any value still contains a `<placeholder>`. Do not guess organisation, project, repository, area, iteration or board values.

## Purpose

Turn framework tickets (Given / When / Then user stories) into tracker stories or tasks without inventing fields, duplicating work, or losing links to Excel/YAML specs.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `feature` | Yes | Feature slug (feature folder `work/<feature>/`) |
| `tickets_dir` | Yes | `work/<feature>/tickets/` — only `*.md` files matching the stable ID pattern |
| `specs_dir` | Yes | `work/<feature>/specs/` — YAML page specs |
| `excel_dir` | Yes | `work/<feature>/excel/` — generated workbooks |
| target settings | No | From the target's block under `tickets` — placeholders until known (see the adapter) |

## Outputs (when a connector exists)

Every adapter maps the same ticket parts:

| Ticket part | Goes to |
|-------------|---------|
| Type (UI page / Manage list / cross-cutting story vs explicit child task) | The tracker's story type, or task type only when the markdown Type is explicitly a child implementation task |
| Heading after `Ticket: <ID> — ` | Title, prefixed with the stable ID: `[T-<DOMAIN>-NNN] <title> (<page type>)` |
| User story + Full-stack scope + Acceptance criteria (GWT) + Work to do / Out of scope | Description / body, kept as written, with footer `Source: work/<feature>/tickets/<filename>` and the spec / excel paths |
| Feature, page type, stable ID, `ai-planning-framework` | Tags / labels |
| Specs field (`excel/*.xlsx`, `specs/*.yaml`) | Attachments or links (link when attachment size is a concern) |
| Stable ID | Upsert match (tag, title prefix or custom field, per adapter) |

Until a connector is wired: write a dry-run payload list under `work/<feature>/devops/publish-plan.md` (optional; the folder keeps its name whatever the tracker) listing each ticket ID → proposed title, type, tags and attachment paths — **do not** create tracker items.

## Stable IDs (upsert, do not duplicate)

- Every ticket file **must** be named: `T-<DOMAIN>-NNN-<short-slug>.md`  
  Example: `T-BOOK-001-add-edit-book.md`
- The ID inside the file (heading and metadata) **must** match the filename prefix: `T-<DOMAIN>-NNN`
- `<DOMAIN>` is an uppercase short domain token (the project profile's `tickets.domain_tokens`, e.g. `BOOK`, `LOAN`)
- `NNN` is a zero-padded integer, unique within that domain across the feature (and prefer unique across the backlog once published)
- **Upsert rule:** before creating a work item, search by stable ID (as the adapter says). If found → **update** description, links and tags. If not found → **create**. Never create a second item for the same `T-<DOMAIN>-NNN`.

## Hard rules

1. **Create stories only from** `work/<feature>/tickets/*.md` — never invent tickets at publish time.
2. **Never invent DB columns** (or Service / Table names) that are not in the linked YAML/Excel specs. If the ticket scope disagrees with the spec, fix the ticket via `generate-tickets` first; do not “improve” mappings while publishing.
3. **Upsert by stable ID** — no duplicates.
4. **No live tracker calls** from this skill until the tracker's connector is connected and the user explicitly asks to publish.
5. Framework-agnostic wording stays as in the tickets.

## Steps (agent)

1. Read `../ai-framework.config.yaml`; pick the adapter for `tickets.target`; stop and report if publishing is disabled, the adapter is a stub or placeholders remain (dry-run only).
2. List `work/<feature>/tickets/T-*-*.md`; skip files that do not match `T-<DOMAIN>-NNN-*.md`.
3. For each file, parse ID, title, type, Specs paths, user story, scope table, GWT scenarios.
4. Resolve Specs paths under `work/<feature>/`; fail the ticket (do not publish) if a listed spec/excel is missing.
5. Cross-check Full-stack scope rows against YAML/Excel — every Service / Table / Column must appear in the spec; abort that item if not.
6. Build the payload with the adapter's field mapping.
7. If connector unavailable: append to `work/<feature>/devops/publish-plan.md` and stop.
8. If connector available **and** user approved publish: upsert by stable ID; attach/link excel + specs; record the tracker item IDs back into the ticket Notes (optional) and in `handoff.md` (`devops_work_item_id`, kept as the field name for any tracker).

## Quality checks

- [ ] Config read; adapter chosen from `tickets.target`; publishing enabled and no `<placeholders>` left (else stopped and reported)
- [ ] Only files under `tickets/` were considered
- [ ] Every payload title includes `T-<DOMAIN>-NNN`
- [ ] Description retains Given / When / Then
- [ ] excel/ and specs/ linked or attached for each item
- [ ] Tracker location values are placeholders or user-supplied — not guessed
- [ ] No Service / Table / Column invented beyond specs
- [ ] Upsert path documented; no duplicate creates for the same ID
- [ ] Live publish skipped unless connector + explicit user approval

## Related

- Adapters: `adapters/azure-devops.md`, `adapters/github.md`, `adapters/jira.md`
- Generate tickets: `skills/generate-tickets/SKILL.md`
- Ticket template: `templates/tickets/ticket.md`
- Loop stage: `loops/feature-planning.md` stage 6 (optional, stubbed)
- Agent handoff: `AGENT-BRIEF.md`
