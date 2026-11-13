# tests/

Inputs and expected outputs for `tools/check.py`.

| Path | What it is |
|------|------------|
| `manifest.yaml` | Every spec that is regenerated and compared, its profile, golden file and stored workbook; plus specs that must fail validation |
| `golden/` | Expected workbook content as JSON (cell values and styles, merges, widths, heights, data validation). Written only by `tools/check.py --update-golden` |
| `cases/` | Coverage specs the samples do not pin down: `ui-only-sketch.yaml` (no DB columns), `legacy-names.yaml` (deprecated names), `flat-form.yaml` (flat controls with DB columns), `grid-no-filters.yaml` (empty search and actions menu), `import-defaults.yaml` (starter defaults for the download button, panel and Cancel / Upload) |
| `cases/invalid/` | Specs that **must fail** validation: typo, missing mapping, Paginated Grid without route, wizard without steps, form with no body, import column missing its mapping, import with no columns, grid that also carries form controls, unknown page type |
| `leftover-terms.yaml` | Project-specific terms that must not appear in the generic framework, with allowed folders |

Goldens for parked features are stored here (`golden/features/<feature>/`); their own folders are
never written.
