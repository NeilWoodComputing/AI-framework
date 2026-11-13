# AI planning framework

Markdown **skills** and an orchestration **loop** for planning full-stack development work the way the starter Excel page specs do it: **what appears on screen** and **where it lives in the database** (Service, Target DB Table, Target DB Column).

Journeys and tickets are supported but secondary. Generated application code is **framework-agnostic** (interfaces and mappings only).

Shared settings (active API/UI folder, output folder, ticket target, active project) live one level up in `../ai-framework.config.yaml` — agents read it first, then the active **project profile** (`project.profile`, beside the config, outside this framework). The framework itself is project-neutral; see `projects/README.md`.

## What you get

| Path | Role |
|------|------|
| `AGENT-BRIEF.md` | Short handoff for any agent (read first) |
| `RULES.md` | The framework rules R1–R9, stated once and referred to by ID |
| `DECISIONS.md` | Dated record of the decisions behind the framework's defaults |
| `VERSION`, `CHANGELOG.md` | Framework version (profiles record `framework_version`) and what changed |
| `loops/feature-planning.md` | End-to-end order: plan → UI specs/Excel → journeys → tickets → stubs → publish (optional) → hand-off |
| `skills/` | Agent-readable procedures (inputs, steps, quality checks). `publish-tickets/adapters/` holds one file per tracker; `generate-code-stubs/stacks/` holds optional stack naming hints |
| `templates/` | The starter workbook `excel/page-spec-templates.xlsx` (**canonical layout; do not edit, copy it to fill in**), neutral Library sample specs `yaml/` and their generated workbooks `out/`, and ticket / journey / stub templates. See `templates/README.md` |
| `schemas/` | JSON Schemas for page specs (`page-spec.schema.json`) and project profiles (`project-profile.schema.json`) |
| `generators/excel_spec.py` | YAML → `.xlsx` in the starter workbook’s layout (see `generators/README.md`) |
| `tools/` | `check.py` verifies the framework; `regenerate.py` rewrites the stored sample workbooks (see `tools/README.md`) |
| `tests/` | Manifest, golden outputs, coverage cases and expected-invalid specs used by `tools/check.py` |
| `projects/` | Framework defaults only (`_template/project.yaml`). The active profile lives outside this framework; see `projects/README.md` |
| `examples/` | The filled workbooks the starter was taken from (`source-attachments/`; see `examples/README.md`) |
| `work/` | The feature folder: every feature (new and existing) lives in `work/<feature>/`. Existing features predate project profiles and were left in place so their paths stay valid |
| `.editorconfig`, `requirements.txt` | UTF-8 / LF / final newline for editors; Python dependencies |

## Full-stack bias (important)

For **Full-Page Wizard**, **Wizard Modal**, **Form Modal** and **Basic Form**, every control, and every **Import** template column, carries (**R3** in `RULES.md`):

- **Service** — owning backend capability  
- **Target DB Table** — table or aggregate  
- **Target DB Column** — column/field (or filter expression)

The Excel generator includes those columns **by default**. Manage/list pages use **Population Source** (`Table.Column`) as the equivalent mapping for grid columns.

## Quick start

```bash
python -m pip install --user -r requirements.txt
python3 generators/excel_spec.py work/<feature>/specs/<page>.yaml -o work/<feature>/excel/<page>.xlsx
python3 tools/regenerate.py     # rewrite every stored sample / example workbook from tests/manifest.yaml
```

The generator and checks need Python 3.10+ with openpyxl, PyYAML and jsonschema. Run them wherever Python is available, the human owner's PC included (`py` in place of `python3` on Windows); the agent box is the fallback. The generator validates each spec first and writes nothing when it is invalid (`--no-validate` for drafts).

**Verify everything with one command** (exit code 0 = pass):

```bash
python3 tools/check.py        # Windows: py tools/check.py
```

It validates every spec and profile, regenerates the samples, project examples and real feature specs and compares them cell-by-cell with `tests/golden/`, checks the layout against the starter, the starter's hash, encoding (BOM / line endings / mojibake), leftover project terms and duplicate feature slugs, and warns where specs disagree with the project profile. See `tools/README.md`.

**Filling a spec by hand:** copy `templates/excel/page-spec-templates.xlsx` (do not edit the original), keep the sheet for your page type, and fill it in. Its feature label cell (Grid Page Template D2) is the framework’s `feature_module` field; the starter is kept unchanged.

See `generators/README.md` for CLI details.

## Suggested workflow

1. **Plan** — follow `skills/plan-feature/SKILL.md` (pages, services, draft fields).
2. **UI specs** — follow `skills/generate-ui-spec/SKILL.md`; write YAML; run the generator; open the xlsx and check DB columns.
3. **Journeys** (optional) — `skills/generate-user-journey/SKILL.md`.
4. **Tickets** (optional) — `skills/generate-tickets/SKILL.md` (Given/When/Then; stable IDs `T-<DOMAIN>-NNN`; still name Service/Table/Column from specs only).
5. **Stubs** (optional) — `skills/generate-code-stubs/SKILL.md` (UI ↔ DB mapping files only).
6. **Publish tickets** (optional) — `skills/publish-tickets/SKILL.md` when tracker access exists; adapters for Azure DevOps, GitHub (complete), and Jira (stub). See `AGENT-BRIEF.md`.
7. **Hand off** — write `handoff.md` in the feature folder and pass the feature to the implementing agent; see `AGENT-BRIEF.md` → Handoff and `../handoff/README.md`.

Or run the lot via `loops/feature-planning.md`.

## Page types

Each page type follows one sheet of the starter workbook `templates/excel/page-spec-templates.xlsx`:

| Page type | Starter sheet | What it is |
|-----------|---------------|------------|
| **Form Modal** | Modal Template | Single-body create / edit dialog: optional Section Title rows, control grid + DB columns, button blocks (e.g. Cancel / Save). See `form-modal-sample.yaml` (Add \| Edit Book) |
| **Basic Form** | Modal Template | The same layout for a single-body form on its own page. See `basic-form-sample.yaml` (Member Details) |
| **Wizard Modal** | Wizard Template | Multi-step dialog: Step Title rows (Standard Form / List Form), optional sections within a step, control grid + DB columns. See `wizard-modal-sample.yaml` (New Loan) |
| **Full-Page Wizard** | Wizard Template | The same layout for a multi-step page. See `full-page-wizard-sample.yaml` (Library Setup) |
| **Paginated Grid** | Grid Page Template | A feature list with its own route: header, button blocks, filter table, results (Population Source), actions menu (Icon, Req’d. Permission, Availability Logic, Action(s) on Click), plus framework-only `route`, `pagination` and `empty_state`. Search and results sit on the page; no list modal, auto-open or landing page. One spec / Excel, two tickets: the page and the paginated grid. See `paginated-grid-sample.yaml` (Manage Books) |
| **Embedded Grid Modal** | Grid Page Template | The same layout for a list genuinely embedded in another page's flow (see `embedded-grid-modal-sample.yaml`: Book Copies, opened from a Book). Older YAML may say `Modal`, which means the same |
| **Import** | Import Template | Bulk upload: Download Template button, drag-and-drop panel, Cancel / Upload, and the template-column validation table with Service / Target DB Table / Target DB Column. See `import-sample.yaml` (Import Books) |

Prefer Form Modal / Basic Form over a wizard when the surface is one form body. Modals are otherwise only for create / edit forms (Form Modal, Wizard Modal), imports and confirmations (**R1** in `RULES.md`).

## Layout conventions (Excel)

- **The starter workbook `templates/excel/page-spec-templates.xlsx` is the canonical layout.** The generator matches its cell positions, header blocks, button blocks, merges, column widths and spacer rows; agents read it when generating or reviewing specs.
- Fills use the framework’s pastel palette (see `DECISIONS.md`) instead of the starter’s dark-grey label cells; value cells are white and bold, as in the starter. See `generators/README.md`.
- Forms and wizards: header labels on row 2 with values on row 3 (Page Type, Page Title, Page Sub-Title, Required Permission, Parent Page(s)); first Section / Step Title row on row 5; control header row; button blocks below the controls.
- Grids: Page Type / Feature / Module (label from the profile’s `ui.feature_module_label`) / Nav Tree Path on row 2, Page Title + Required Permission on row 3, Page Sub-title on row 4; button blocks at I/J, L/M, …; filter table on row 9; transposed Results Area (Column Title / Population Source / Display Format / Sortable? / Additional Functionality across columns C+); Actions Menu table.
- Framework-only blocks (Route, Pagination, extra filter columns, Conditional Visibility, Notes) sit beside or below the starter’s blocks.

## Language

Skills, loop, and this README use British English (organise, favour, artefact) for narrative text; code identifiers stay as in the domain examples. Generated specs and tickets follow the profile's `language.spelling` (default `en-GB`).

## Non-goals

- No git remote required — files on disk only.
- No commitment to a UI or ORM framework.
- Not a colour clone of the starter: layout matches it, but fills stay pastel (see `DECISIONS.md`).
- No project-specific names in the framework itself: they belong in the active profile (`project.profile` in the shared config) and in `work/`.
