# Skill: generate-ui-spec

Turn a feature plan into YAML page specs (and Excel via the generator) using the framework’s full-stack templates.

**Canonical layout reference:** the starter workbook `templates/excel/page-spec-templates.xlsx` (Modal, Grid Page, Import and Wizard templates). Read it before generating or reviewing a spec: every generated sheet must match its layout (cell positions, header blocks, button blocks, column order). **Do not edit it; copy it to fill in** a spec by hand. Its feature label cell (D2 on the Grid Page Template) is the framework’s `feature_module` field. See `templates/README.md`.

## Purpose

Produce implementation-ready page specifications where **every wizard / form control and Import template column maps to Service / Target DB Table / Target DB Column**, in the starter workbook’s layout. Grid pages map columns via **Population Source**.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `plan` | Yes | Output of `plan-feature` (or equivalent) |
| `page_type` | Yes | `Form Modal` \| `Basic Form` \| `Wizard Modal` \| `Full-Page Wizard` \| `Paginated Grid` \| `Embedded Grid Modal` \| `Import` (older YAML: `Modal` = Embedded Grid Modal) |
| `page_title` | Yes | Page title (Wizard Modal: the wizard's name) |
| `required_permission` | Yes when the page is gated | Permission key needed to open the page (header **Required Permission**) |
| `parent_pages` | No | Parent navigation context |
| `entities` | Yes | Tables + owning services from the plan |
| `include_service_db_columns` | No | Default **true** for wizards/forms — keep true |

## Outputs

1. One YAML file per page under a working folder (validate against `schemas/page-spec.schema.json`).
2. Excel workbook via:

   ```bash
   python3 generators/excel_spec.py work/<feature>/specs/<page>.yaml -o work/<feature>/excel/<page>.xlsx
   ```

3. Optional notes file listing TBD mappings.

A spec may also be filled by hand from a copy of `templates/excel/page-spec-templates.xlsx`; it then still needs a YAML twin so tickets and reviews can read it.

## Template choice

| Need | Page type | Starter sheet | DB mapping |
|------|-----------|---------------|------------|
| Single-body create / edit in a dialog (no steps) | `Form Modal` | Modal Template | Control rows: Service, Target DB Table, Target DB Column; flat `controls` or `sections` |
| Single-body form on its own page | `Basic Form` | Modal Template | Same three columns |
| Multi-step create / edit in a dialog | `Wizard Modal` | Wizard Template | Same three columns (first-class, not omitted) |
| Multi-step create / edit on a full page | `Full-Page Wizard` | Wizard Template | Same three columns |
| Feature list with its own route (search + results + row actions **on the page**) | `Paginated Grid` | Grid Page Template | Results: Population Source = `Table.Column`; plus `route`, `pagination`, `search_filters` |
| List embedded in another page's flow (opened from a parent record) | `Embedded Grid Modal` | Grid Page Template | Results: Population Source = `Table.Column` |
| Bulk upload from a downloadable template | `Import` | Import Template | `import.template_columns`: Service, Target DB Table, Target DB Column per template column |

### Fields every page type shares

- `required_permission` — the header’s **Required Permission**.
- `page_sub_title` (grids / Import may still use `page_sub_text`).
- `buttons` — one block per button: `label`, `type` (Primary Action / Additional Action), `visibility`, `enablement`, `required_permission`, `click_action`. Grids show them right of the header (I/J, L/M, …); forms and wizards below the controls (e.g. Cancel / Save); Import uses them for Cancel / Upload. Older YAML: `primary_action` (with `action`) still works as the first button.
- Grids: `feature_module` (header label from the profile’s `ui.feature_module_label`, default “Feature / Module”; older YAML `system_feature` still work) and `nav_tree_path`.
- Sections (forms) and steps / step sections (wizards) take `visibility` and `additional_functionality`.

### Import

Use `Import` for a bulk-upload modal (e.g. opened from a grid’s Bulk Import button). Fill `import.template_columns` (name, mandatory, format, min / max, additional validation rules, Service, Target DB Table, Target DB Column) and `import.validation_logic`. The Download Template button, the drag-and-drop panel text and functional requirements (.xls / .xlsx only, one file at a time, red X removes it) and the Cancel / Upload buttons default to the starter's text; override `import.download_button`, `import.panel` or `buttons` only when the page differs. See `templates/yaml/import-sample.yaml`.

### Paginated Grid vs Embedded Grid Modal

Apply **R1** (`RULES.md`): a routed feature list is a **Paginated Grid** page; an **Embedded Grid Modal** is only for a list genuinely embedded in another page's flow (e.g. Book Copies opened from a Book).

Both types use the Grid Page Template layout: header, button blocks, filter table, transposed results (Column Title / Population Source / Display Format / Sortable? / Additional Functionality) and the Actions Menu table (`item`, `icon`, `required_permission`, `availability_logic`, `action_on_click`). A **Paginated Grid** also records:

- `route` (required) — the list page's route; `parent_pages` names how it is reached (nav entry), not a host page.
- `search_filters` — on-page search / filter controls: the starter's columns (label, control type, input format, min / max length, mandatory, additional functionality) plus framework-only filters on, match rule and default; `[]` when the page has none.
- `pagination` — `page_size`, `page_size_options`, `paging` (`Server-side` / `Client-side`), `default_sort`; and `results_area.empty_state`.

The create / edit form spec says it opens as a modal over the list page and closes back to it. Use `templates/yaml/paginated-grid-sample.yaml`. One spec / Excel gives two tickets (**R2**).

### Form Modal / Basic Form vs Wizard Modal

Use **Form Modal** (dialog) or **Basic Form** (full page) when the create/edit surface is a **single form body** — one set of fields the user completes without Next/Back steps. Optional `sections` group related fields (Section Title, Section Visibility, Additional Functionality); they are **not** wizard steps and have no Step Format.

Use **Wizard Modal** when the dialog is **multi-step** (ordered steps the user progresses through), each with its own Step Title, Step Format (Standard Form / List Form), optional step visibility rules and optional `sections` inside the step.

All share the same control grid and **require** Service / Target DB Table / Target DB Column. Prefer Form Modal for simple Add | Edit Book-style dialogs; prefer Wizard Modal when the domain needs staged capture (member → books → dates → …).

## Steps

1. Open `templates/excel/page-spec-templates.xlsx` and choose the page type from the plan (see table above); note the starter sheet it follows.
2. For wizards: break work into steps (`Standard Form` or `List Form`).
3. For Form Modal / Basic Form: emit a flat `controls` list, or `sections` with a title + controls when groupings help readability — **do not** invent wizard steps. Add `buttons` (e.g. Cancel / Save) when the plan defines them.
4. For each control, fill UI behaviour **and**:
   - `service`
   - `target_db_table`
   - `target_db_column`
5. Use the service names, permission pattern (`permissions.pattern`), table / column naming (`database`) and reference-data notation (`database.reference_data_notation`) from the project profile; never invent a service the profile or plan does not name.
6. For List Form steps (wizards only), use **Column Label** semantics (same control schema; generator switches the header).
7. For grids: define results columns with `population_source`, `buttons`, and the actions menu (icon, required permission, availability logic, action on click). Choose `Paginated Grid` for a feature list with its own route (fill `route`, `pagination`, `search_filters`, `empty_state`) and `Embedded Grid Modal` only for an embedded list — see **Paginated Grid vs Embedded Grid Modal**. For an Import page fill `import` — see **Import**.
8. Capture conditional visibility (enablement rules) on controls and in `conditional_visibility` when cross-field or mode-based (e.g. View mode).
9. Emit YAML; run `excel_spec.py` (wherever Python is available, the PC included; see `generators/README.md`). It validates the spec first (**R7**) and writes nothing if a field is unknown, misspelt or missing; fix every reported field. Open the xlsx and confirm DB columns are present for wizards, forms and Import.
10. **Layout check (required):** compare the generated sheet with its sheet in `templates/excel/page-spec-templates.xlsx` — header labels and positions, button blocks, filter / actions / template-column tables in the same cells and order. Only the pastel fills and the framework-only blocks (Route, Pagination, extra filter columns, Conditional Visibility, Notes) may differ. When reviewing a spec someone else wrote, use the same check.

## Control row checklist (wizards, Form Modal & Basic Form)

- [ ] Control Label, Control Type, Input Format
- [ ] Min / Max Len or Val
- [ ] Enablement, Editable, Mandatory
- [ ] Validation Rules + Failure Message(s) where needed
- [ ] **Service, Target DB Table, Target DB Column** (required)

## Quality checks

- [ ] YAML validates against schema (**R7**; the generator refuses invalid specs; controls and Import template columns have service + table + column, **R3**)
- [ ] `tools/check.py` passes (add new real-feature specs to `tests/manifest.yaml` with a golden)
- [ ] Generated Excel matches its sheet in `templates/excel/page-spec-templates.xlsx` (layout check, step 10)
- [ ] Gated pages set `required_permission`; buttons and actions menu items name their Req'd. Permission where one applies
- [ ] Generated Excel shows Service / Target DB Table / Target DB Column for wizard, Form Modal, Basic Form and Import types
- [ ] Form Modal / Basic Form Excel has **no** Step Title / Step Format / Step Visibility blocks (optional Section Title rows only)
- [ ] List Form steps use list-oriented labels where appropriate
- [ ] Grid pages: every results column has Population Source
- [ ] Grid pages: a feature list with its own route is a `Paginated Grid` with `route`, `pagination` and `search_filters` (no list modal, no auto-open); `Embedded Grid Modal` only for genuinely embedded lists; forms, imports and confirms are modals
- [ ] No orphan UI field without a persistence target (use `TBD` only temporarily and list in notes)

## Reference examples

- **`templates/excel/page-spec-templates.xlsx` — canonical layout (the starter workbook; do not edit, copy to fill in)**
- `templates/yaml/form-modal-sample.yaml` (Form Modal)
- `templates/yaml/basic-form-sample.yaml` (Basic Form, full page)
- `templates/yaml/wizard-modal-sample.yaml` (Wizard Modal)
- `templates/yaml/full-page-wizard-sample.yaml` (includes a section within a step)
- `templates/yaml/paginated-grid-sample.yaml` (routed list page)
- `templates/yaml/embedded-grid-modal-sample.yaml` (Embedded Grid Modal)
- `templates/yaml/import-sample.yaml` (Import)
- Generated samples in `templates/out/` (see `templates/README.md`)
- Samples use a neutral Library domain (Books, Members, Loans); see `templates/README.md`
- Filled originals under `examples/source-attachments/` (older than the starter; follow the starter where they differ)
