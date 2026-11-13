# Templates

Starting points for every artefact the planning framework produces.

| Folder / file | What it is |
|---------------|------------|
| `excel/page-spec-templates.xlsx` | **The starter workbook** — the canonical page-spec layout (see below) |
| `yaml/` | Sample page-spec YAML in a neutral Library domain (Books, Members, Loans), one per page type; copy one and edit it, then run `generators/excel_spec.py` |
| `out/` | Workbooks generated from `yaml/` (see **Generated samples** below), plus a sample user story |
| `tickets/ticket.md` | Ticket template (`T-<DOMAIN>-NNN`, Given / When / Then scenarios) |
| `journeys/journey.md` | User journey template |
| `stubs/ui-to-db.yaml` | UI ↔ DB mapping stub template |

Project-specific values (service names, permission pattern, DB naming, header labels) come from the active project profile (`project.profile` in the shared config), not from these templates.

## The starter workbook (`excel/page-spec-templates.xlsx`)

The original blank templates, stored **byte-for-byte unchanged**. The original filled examples (`../examples/source-attachments/`) were built from it.

**Do not edit; copy it to fill in.** The generator reads its column widths, so editing it changes every generated workbook.

It has four blank sheets:

| Sheet | Page types that use its layout | YAML example |
|-------|-------------------------------|--------------|
| Modal Template | Form Modal, Basic Form | `yaml/form-modal-sample.yaml`, `yaml/basic-form-sample.yaml` |
| Wizard Template | Wizard Modal, Full-Page Wizard | `yaml/wizard-modal-sample.yaml`, `yaml/full-page-wizard-sample.yaml` |
| Grid Page Template | Paginated Grid, Embedded Grid Modal | `yaml/paginated-grid-sample.yaml`, `yaml/embedded-grid-modal-sample.yaml` |
| Import Template | Import | `yaml/import-sample.yaml` |

Use it in three ways:

1. **Canonical layout reference.** Agents read it when generating or reviewing specs (`skills/generate-ui-spec/SKILL.md`, `skills/plan-feature/SKILL.md`). Generated sheets match its cell positions, header and button blocks, merges, column widths and spacer rows.
2. **Blank starter for hand-filled specs.** Copy it (for example to `work/<feature>/excel/<page>.xlsx`), delete the sheets you do not need, rename the one you keep, and fill it in. Add or remove control / column rows as needed.
3. **Example.** Compare it with the generated samples below and the filled originals in `../examples/README.md`.

Things to know:

- **The feature label cell (Grid Page Template D2) = `feature_module`.** The starter keeps its original label text. YAML uses `feature_module` (older YAML: `system_feature`), and generated grids use the profile's `ui.feature_module_label` (default “Feature / Module”).
- **Its “Modal” sheet is a form dialog** (sections, control grid, Cancel / Save). In the framework that is `Form Modal` (or `Basic Form` on a full page); a list embedded in a dialog is `Embedded Grid Modal`.
- The Wizard Template’s section row says “SectionTitle”; generated sheets say “Section Title”.
- The starter uses dark-grey label cells. Generated sheets keep the framework’s pastel fills (see `../DECISIONS.md`); the layout is the same.

## Generated samples (`out/`)

Generated from `yaml/` with `--profile projects/_template/project.yaml`, so grid headers say “Feature / Module”.

| File | Page type (starter sheet) |
|------|---------------------------|
| `out/form-modal-sample.xlsx` | Form Modal (Add \| Edit Book): sections, DB columns, Cancel / Save (Modal Template) |
| `out/basic-form-sample.xlsx` | Basic Form (Member Details): same layout on a full page (Modal Template) |
| `out/wizard-modal-sample.xlsx` | Wizard Modal (New Loan) with DB columns and a List Form step (Wizard Template) |
| `out/full-page-wizard-sample.xlsx` | Full-Page Wizard (Library Setup), with a section inside a step (Wizard Template) |
| `out/paginated-grid-sample.xlsx` | Paginated Grid (Manage Books): two buttons, filter table, actions menu, pagination (Grid Page Template) |
| `out/embedded-grid-modal-sample.xlsx` | Embedded Grid Modal (Book Copies) with Population Source (Grid Page Template) |
| `out/import-sample.xlsx` | Import (Import Books): download button, upload panel, template-column validation (Import Template) |
| `out/sample-user-story-add-edit-book.md` | User story for the Add \| Edit Book sample: As a / I want / So that + Given / When / Then |

Regenerate every sample and project example (from the ai-planning-framework folder) with `py tools/regenerate.py` (`python3` elsewhere); see `../tools/README.md`.
