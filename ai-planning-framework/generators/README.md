# Excel page-spec generator

Turns a YAML page specification into an `.xlsx` workbook laid out like the starter workbook `templates/excel/page-spec-templates.xlsx`.

## Layout source

The layout comes from the starter workbook **`templates/excel/page-spec-templates.xlsx`** (canonical; do not edit — copy it to fill in by hand). Each page type follows one sheet:

| Page type | Starter sheet |
|-----------|---------------|
| Form Modal, Basic Form | Modal Template |
| Wizard Modal, Full-Page Wizard | Wizard Template |
| Paginated Grid, Embedded Grid Modal (older YAML: `Modal`) | Grid Page Template |
| Import | Import Template |

Generated sheets match the starter’s cell positions, header blocks (labels on row 2, values on row 3 for forms / wizards), button blocks (Button Label, Button Type, Visibility, Enablement, Req'd. Permission, Click Action), merges, column widths and spacer rows. Column widths are read from the starter when it is present (built-in copies are used otherwise, with the same result). Results columns beyond G on a grid widen the starter's narrow spacer columns.

Framework-only blocks sit beside or below the starter's blocks: **Route** (grids, B5), extra filter columns **Filters On / Match Rule / Default** (L–N, right of the filter table), **Pagination** rows (Results Visibility, Page Size, Page Size Options, Paging, Default Sort, Paging Notes, Empty State) below the Actions Menu, then **Conditional Visibility** and **Notes**.

## DB mapping

For **Form Modal**, **Basic Form**, **Wizard Modal** and **Full-Page Wizard**, every control row includes **Service**, **Target DB Table** and **Target DB Column** (on by default; `include_service_db_columns: false` only for a rare UI-only sketch). **Import** template columns carry the same three. **Grids** use **Population Source** (`Table.Column`) for each results column.

## Older YAML

Older field names still generate (the schema marks them `deprecated`; see `../tests/cases/legacy-names.yaml`): `page_type: Modal` (= Embedded Grid Modal), `system_feature` and `unity_feature` (= `feature_module`), `primary_action` (= `buttons[0]`), `action` (= `click_action`), `availability` (= `availability_logic`), `page_sub_text` (= `page_sub_title`), `wizard_name` (shown as Page Title when `page_title` is absent).

## Project profile (header label)

The grid header label for `feature_module` (D2) comes from the project profile's `ui.feature_module_label`, default “Feature / Module”. The generator reads the profile from `--profile <file>`, else from `project.profile` in `../../ai-framework.config.yaml` (relative to the generator) when that file exists, else uses the default. Nothing else in the layout depends on the profile.

## Colours

The starter uses dark-grey label cells; the generator keeps the framework's pastel palette instead (see `../DECISIONS.md`). Value cells are white with bold text, as in the starter; font Aptos Narrow 11; thin black borders.

| Role | Hex | Swatch intent | Used for |
|------|-----|---------------|----------|
| **META** | `#E2EFDA` | Soft green | Page header labels; button blocks; Notes |
| **STEP** | `#FCE4D6` | Soft peach | Wizard **Step Title** rows; grid **Results Area** |
| **SECTION** | `#E2D5F1` | Soft lavender | **Section Title** rows; Conditional Visibility; Import validation title |
| **HEADER** | `#D9E2F3` | Soft blue | Control / Column Title / filter / actions menu / template-column header rows |
| **ATTR** | `#DDEBF7` | Light blue | Grid attribute labels (Population Source, Sortable?, …), Import panel labels, Pagination labels |

## Install

```bash
python -m pip install --user -r requirements.txt     # openpyxl, PyYAML, jsonschema
```

Run it wherever Python 3.10+ is available, the human owner's PC included (`py generators/excel_spec.py ...` on Windows); the agent box is the fallback.

## Validation, errors and determinism

- The spec is validated against `../schemas/page-spec.schema.json` before anything is written (**R7** in `../RULES.md`). The schema is strict: unknown or misspelt fields are errors. Each error names the field, e.g. `sections[0]: unknown field(s) ('contorls' was unexpected)` or `controls[0]: 'service' is a required property`; the exit code is 1 and no file is written.
- `--no-validate` skips validation for a rough draft; specs for hand-off must validate.
- Deprecated field names still generate and are reported as `note: deprecated field ...`.
- Characters Excel cannot store (control characters) are removed with a warning.
- Output is deterministic: the same YAML and profile give the same bytes (fixed document timestamps), so regenerated files only change when content changes.
- `tools/check.py` regenerates every sample and real spec and compares them cell-by-cell with `tests/golden/`.

## Usage

```bash
# from the ai-planning-framework folder
python3 generators/excel_spec.py work/<feature>/specs/<page>.yaml -o work/<feature>/excel/<page>.xlsx
                                  # profile from project.profile in the shared config
python3 generators/excel_spec.py templates/yaml/form-modal-sample.yaml -o templates/out/form-modal-sample.xlsx \
  --profile projects/_template/project.yaml
```

To rewrite every stored sample and project example at once, use `tools/regenerate.py` (see `../tools/README.md`).

If the machine holding the framework has no Python, run it on one that does (e.g. the agent box) and copy the `.xlsx` back.

## YAML shape

See `../schemas/page-spec.schema.json` and examples under `../templates/yaml/`.

Wizard, Form Modal and Basic Form controls, and Import template columns, should always set `service`, `target_db_table`, and `target_db_column`.
