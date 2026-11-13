# Loop: feature-planning

End-to-end orchestration for one feature. **Primary outcome:** full-stack UI specs (YAML + Excel) with Service / Target DB Table / Target DB Column. Journeys, tickets, and stubs are secondary. Publishing to a ticket tracker (`tickets.target`) is optional and stubbed until access exists.

## When to run

A new or changed feature needs implementable page specs and a backlog slice.

## Config first

Read `../ai-framework.config.yaml` (paths relative to the `ai-framework` root) before stage 1:

- Read the project profile (`project.profile`; defaults in `projects/_template/project.yaml`) for services, naming, header labels, ticket prefixes and which framework rules are on (`rules`)
- Write every artefact under the feature folder, shown as `work/<feature>/` below: `<project.work_dir>/<feature>/` for a new feature, or the existing folder named by its `handoff.md` `feature_path` (see `AGENT-BRIEF.md` → Where features live)
- Active API / UI folder comes from `development` (used by stubs and later code work)
- Ticket target comes from `tickets`; if `tickets.enabled` is `false` or placeholders remain, stage 6 stops at a dry-run and reports

## Ordered stages

```text
1. plan-feature
        ↓
2. generate-ui-spec  →  YAML  →  excel_spec.py  →  .xlsx
        ↓
3. generate-user-journey   (optional / secondary)
        ↓
4. generate-tickets        (secondary; full-stack + Given/When/Then + stable IDs)
        ↓
5. generate-code-stubs     (optional; UI ↔ DB mappings only)
        ↓
6. publish-tickets         (optional; stubbed — no live tracker calls until connector + approval)
        ↓
7. hand-off                (planning agent → implementing agent: handoff.md + human owner's approval + devops | direct)
```

Stop after stage 2 if the Excel specs are enough for the next engineering conversation. Stop after stage 4 only when no hand-off is wanted. Otherwise finish with stage 7 (after stage 4, plus 5 / 6 when they run), so the implementing agent can pick the feature up.

## Stage details

### 1. plan-feature

- Run `skills/plan-feature/SKILL.md`
- Artefact: `work/<feature>/plan.md`
- Gate: every page has a type; entities have owning services; draft field inventory includes table/column guesses
- Gate: **R1** (`RULES.md`): a routed feature list is a `Paginated Grid` page, not a modal
- Gate: the feature slug exists in no work folder (**R8**)

### 2. generate-ui-spec (critical path)

- Run `skills/generate-ui-spec/SKILL.md`
- Artefacts:
  - `work/<feature>/specs/*.yaml`
  - `work/<feature>/excel/*.xlsx` (via generator)
- Commands:

  ```bash
  python3 generators/excel_spec.py work/<feature>/specs/<page>.yaml \
    -o work/<feature>/excel/<page>.xlsx          # header label from project.profile (or --profile <file>)
  ```

- Gate: wizard, Form Modal, Basic Form and Import Excel sheets show **Service**, **Target DB Table**, **Target DB Column**; grid sheets show **Population Source**
- Gate: each Excel sheet matches its sheet in `templates/excel/page-spec-templates.xlsx` (canonical layout; see `skills/generate-ui-spec/SKILL.md` step 10)
- Gate: every Paginated Grid spec has `route`, `pagination` (page size, options, server- / client-side, default sort), `search_filters` (`[]` if none) and `results_area.empty_state`; `Embedded Grid Modal` only for an embedded list
- Prefer copying structure from `templates/yaml/` then editing (or copy `templates/excel/page-spec-templates.xlsx` to fill a sheet by hand, then write its YAML twin)

### 3. generate-user-journey (secondary)

- Run only when specs are stable
- Artefacts: `work/<feature>/journeys/*.md` from `templates/journeys/journey.md`
- Gate: steps cite real pages/fields from specs

### 4. generate-tickets (secondary)

- Prefer grouping by table/service, then UI
- Artefacts: `work/<feature>/tickets/T-<DOMAIN>-NNN-<slug>.md` from `templates/tickets/ticket.md`
- Gate: stable ID in filename and heading; upsert same file when regenerating (do not duplicate IDs)
- Gate: each ticket names persistence targets **only** as in the specs
- Gate: **R2**: a Paginated Grid is split into a page ticket and a paginated grid ticket (unless switched off in the profile)
- Gate: every scenario heading has an explicit ID `### Scenario: S<n> — <title>` (full ID `<ticket>/S<n>`), which the testing agent tags its tests with; IDs are never renumbered or reused, and a moved scenario notes `(was <ticket>/S<n>)` (see `skills/generate-tickets/SKILL.md` → Scenario IDs)
- Gate: user stories use **As a / I want / So that**; acceptance criteria are **Given / When / Then** (And optional), naming Service / Target DB Table / Target DB Column where relevant
- Gate: Specs field lists excel + yaml paths
- Example: `templates/out/sample-user-story-add-edit-book.md`

### 5. generate-code-stubs (optional)

- Framework-agnostic interfaces + `ui-to-db.yaml`
- Artefacts: `work/<feature>/stubs/**`
- Gate: mapping file covers every control

### 6. publish-tickets (optional, stubbed)

- Run `skills/publish-tickets/SKILL.md` only when preparing or performing a tracker publish; it picks the adapter for `tickets.target` (`adapters/azure-devops.md`, `adapters/github.md`, `adapters/jira.md`)
- Target settings from `tickets` in `../ai-framework.config.yaml`; if `enabled: false`, the adapter is a stub, or `<placeholders>` remain, stop and report — do not guess
- Source of truth: **only** `work/<feature>/tickets/*.md`
- Map → the tracker's story type (or task when typed as such); description keeps Given / When / Then; attach/link `excel/` + `specs/`
- Upsert by stable ID `T-<DOMAIN>-NNN` — never duplicate
- Placeholders stay until the user supplies values
- **No live tracker calls** until a connector is available and the user explicitly asks to publish; dry-run may write `work/<feature>/devops/publish-plan.md`
- See also `AGENT-BRIEF.md`

### 7. hand-off (planning agent → implementing agent)

- Follow **Handoff (planning agent → implementing agent)** in `AGENT-BRIEF.md` and the pipeline rules in `../handoff/README.md`
- Artefact: `work/<feature>/handoff.md` from `../handoff/templates/handoff.md` — stage `planned`, owner `agents.planning.id`, tickets listed, artefact table and notes for the next owner filled
- Gate: `handoff.require_human_approval.plan_to_code` — ask the human owner and record their approval before handing off
- Route from `handoff.plan_to_code`: `devops` (publish via stage 6, record work item IDs; only when `tickets.enabled` is true) or `direct` (default)
- Then set stage `in-development`, owner `agents.code.id`, `pickup: pending`, add a History row, and message the implementing agent by name (`agents.code.name`) with `../handoff/templates/handoff-message.md`
- Gate: never hand off with a missing Service / Table / Column in the specs (**R3**, **R4**)
- Gate: `tools/check.py` ends `RESULT: PASS` (**R7**, **R9**); add the feature's specs to `tests/manifest.yaml` and create their goldens

## Agent checklist (per loop)

- [ ] `../ai-framework.config.yaml` and the project profile read; outputs under the feature folder (`project.work_dir` for new features)
- [ ] Plan names services and entities
- [ ] YAML controls include service + table + column
- [ ] Routed feature lists are `Paginated Grid` pages, not modals; each has a page ticket and a paginated grid ticket (unless switched off in `rules`)
- [ ] Excel generated and spot-checked (headers from column B, row 2)
- [ ] Journeys/tickets not started before DB mappings exist
- [ ] Tickets use Given / When / Then and stable IDs `T-<DOMAIN>-NNN`; every scenario has an explicit, never-renumbered ID heading `### Scenario: S<n> — <title>`
- [ ] No Service / Table / Column invented beyond specs
- [ ] Stubs (if any) stay framework-agnostic
- [ ] Tracker publish (if any) only from `tickets/`, upsert by ID, excel+specs linked
- [ ] `handoff.md` written; the human owner's `plan_to_code` approval recorded; the implementing agent messaged (or work items on the board)

## Working folder convention

```text
work/<feature-slug>/
  plan.md
  specs/
  excel/
  journeys/
  tickets/
  stubs/
  devops/          # optional; publish-plan.md dry-run
  handoff.md       # pipeline state (stage 7); then the implementing and reviewing agents update it
  reviews/         # written later by the reviewing agent
    review-log.md  # append-only log of every review round, both routes
  tests/           # test plan, run reports and test log, written by the testing agent
```

The folder names come from `output.feature_layout` in `../ai-framework.config.yaml`.

`work/<feature-slug>/` is the feature folder: `<project.work_dir>/<feature-slug>/` for a new feature (from `../ai-framework.config.yaml`), or the existing folder its `handoff.md` names. Create it when executing a real feature (not required for the samples in `templates/out/`).
