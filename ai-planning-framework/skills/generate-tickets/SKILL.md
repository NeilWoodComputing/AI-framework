# Skill: generate-tickets

Create implementation tickets from page specs (primary) and journeys (secondary). Bias tickets toward **full-stack** work: UI control + API/service + DB column.

User stories and acceptance criteria use **Given / When / Then** (Gherkin-style).

## Purpose

Break delivery into tickets that an engineer can implement without rediscovering field→column mapping, with testable GWT acceptance criteria. Filenames and IDs are **stable** so a later tracker publish can upsert instead of duplicating.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `page_specs` | Yes | YAML/Excel with Service / Table / Column |
| `journeys` | No | Optional context for story narrative and scenarios |
| `plan` | No | Slices / priorities |

## Outputs

One markdown file per ticket using `templates/tickets/ticket.md`.

### Stable IDs and filenames (required)

| Rule | Detail |
|------|--------|
| ID format | `T-<DOMAIN>-NNN` — e.g. `T-BOOK-001` (pattern: `tickets.id_prefix` in the config) |
| Filename | `T-<DOMAIN>-NNN-<short-slug>.md` — e.g. `T-BOOK-001-add-edit-book.md` |
| Domain | Uppercase short token from the project profile's `tickets.domain_tokens`, else from the feature/entity (BOOK, MEMBER, LOAN, …) |
| NNN | Zero-padded integer, unique within that domain for the feature |
| Heading | Must start with `# Ticket: T-<DOMAIN>-NNN — <title>` matching the filename prefix |
| Upsert | Never renumber or reuse an ID for a different story. When regenerating, **update the same file** for the same ID; do not create a parallel ticket with a new ID for the same scope. Downstream `publish-tickets` upserts tracker items by this ID. |

Suggested ticket shapes:

1. **Schema / persistence** — tables/columns for an entity
2. **Service API** — read/write for a step or resource
3. **UI step / page** — render controls bound to that API (reference Excel rows)
4. **Page** (Paginated Grid, part a) — route, nav link, permission gate, no-permission message, page layout and search / filter area; hosts the grid and the create / edit form modal
5. **Paginated grid** (Paginated Grid, part b) — columns from Population Source, sorting, paging, row actions menu, empty state
6. **Manage list** (`Embedded Grid Modal`; older specs say `Modal`) — grid columns from Population Source + actions menu, for a list opened from another page
7. **Import** (`Import`) — template download, upload panel (file type / one file / remove), row validation and the all-or-nothing write, citing each template column's Service / Target DB Table / Target DB Column
8. **Cross-cutting** — validation, uniqueness, and the profile's `conventions` (soft delete, audit columns, tenancy)

Each ticket includes:

1. **User story** — `As a` / `I want` / `So that`
2. **Full-stack scope** — UI label ↔ Service / Target DB Table / Target DB Column (or Population Source) — **only** values present in the specs
3. **Acceptance criteria** — one or more **Given / When / Then** scenarios (`And` / `But` optional)
4. **Specs** field pointing at `specs/*.yaml` and `excel/*.xlsx` paths under `work/<feature>/`

## Scenario IDs (explicit, never renumbered)

Every scenario heading carries an explicit ID: `### Scenario: S<n> — <title>` (for example `### Scenario: S3 — Name is mandatory`). The full ID is `<ticket>/S<n>` (for example `T-BOOK-002/S3`). The testing agent tags each test with that ID (for example `@T-<DOMAIN>-NNN/S<n>` in e2e tests and a scenario trait / attribute in unit tests), and the implementing agent's manifest and the reviewing agent's coverage tables use it too (`testing.scenario_ids: explicit` in the config). The heading keeps the `### Scenario:` prefix so the ticket checks and tooling that read scenarios keep working.

- **Never renumber.** IDs follow the heading, not its position: reordering, rewording or rewriting a scenario keeps its ID.
- **New scenario** → the next unused number in that ticket, even if it lands out of order.
- **Removed scenario** → its number is retired (never reused); say so in the ticket notes.
- **Moved scenario** → it gets the next unused ID in the destination ticket with `(was <old ticket>/S<n>)` in its heading. The source ticket notes the move, so `<old>/S<n>` stays traceable to its new ID. Record the old → new mapping in both tickets.
- **Older tickets without IDs** → when a ticket is next updated, freeze its current positional numbers as explicit IDs (first heading = S1, …) before changing anything else.

## Given / When / Then rules

Write acceptance criteria as Gherkin-style scenarios:

```text
### Scenario: S<n> — <short name>
  Given <precondition — mode, data, permissions, or existing DB state>
  And <optional extra precondition>
  When <user or system action>
  Then <observable UI or API outcome>
  And <persistence outcome naming Service / Target DB Table / Target DB Column where relevant>
```

Guidelines:

- Prefer concrete controls and validation messages from the Excel/YAML spec.
- For create/update stories, Then/And should name **Service**, **Target DB Table**, and **Target DB Column** for fields in scope.
- For paginated grid and manage-list stories, name **Population Source** for grid columns.
- Carry the spec's permissions into scenarios: the page's **Required Permission**, each button's and each actions-menu item's **Req'd. Permission**, and the actions menu **Availability Logic**.
- **Paginated Grid: two tickets (R2, `RULES.md`)**, a page ticket and a paginated grid ticket; the page ticket depends on the grid ticket. Scenario IDs follow **Scenario IDs** above, so scenarios can move between the two without losing traceability.
- Cover happy path plus at least one validation or enablement failure when the spec defines messages.
- Keep language framework-agnostic (no React/Angular/.NET-specific wording unless the repo already mandates a stack).
- **Do not invent** Service / Table / Column values that are not in the linked specs (**R4**).

## Steps

1. Choose `<DOMAIN>` from the plan/entity; allocate the next free `NNN` (or reuse the existing ID when updating).
2. Write `work/<feature>/tickets/T-<DOMAIN>-NNN-<short-slug>.md` from the template.
3. Group controls by `target_db_table` (and service).
4. Emit persistence tickets first where schema is new.
5. Emit UI tickets that **quote** Control Label + Target DB Column from the spec.
6. Draft the user story (`As a` / `I want` / `So that`) from the page purpose and optional journey.
7. Add **Given / When / Then** acceptance scenarios, each with an explicit ID heading `### Scenario: S<n> — <title>` (see **Scenario IDs**); include validation messages from the spec.
8. Set Specs to the concrete `specs/` and `excel/` paths for that page.
9. Link related journey ids only as optional context.
10. Order by plan slices (vertical: one page/step end-to-end beats all-UI-then-DB).

## Quality checks

- [ ] Filename and heading ID match `T-<DOMAIN>-NNN`; no duplicate IDs for different scopes
- [ ] Regenerations update the same file (upsert), not a new ID for the same work
- [ ] Every wizard / Basic Form control appears in some ticket’s scope (or is explicitly deferred)
- [ ] Tickets name Service / Table / Column **only** as in the specs — nothing invented
- [ ] Manage-list Population Sources covered
- [ ] Acceptance criteria are Given / When / Then (And optional), not bullet wish-lists alone
- [ ] Every scenario heading has an explicit ID `### Scenario: S<n> — <title>`; no existing ID was renumbered or reused; moves and removals are noted with the old → new mapping
- [ ] At least one scenario asserts persistence or read via the named Service / table / column
- [ ] Specs field lists excel + yaml paths
- [ ] No framework-specific implementation mandated (agnostic)

## Priority note

Tickets without DB mapping are incomplete for this framework — go back to `generate-ui-spec`.

## Related

- Publish to the ticket tracker (later): `skills/publish-tickets/SKILL.md` (adapter for `tickets.target`)
- Agent handoff: `AGENT-BRIEF.md`
