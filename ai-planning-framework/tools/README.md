# tools/

## check.py

One command that verifies the framework. Exit code 0 and `RESULT: PASS` mean every check passed;
warnings never fail the run.

```bash
python3 tools/check.py                  # Windows: py tools/check.py   (from ai-planning-framework/)
python3 tools/check.py -v               # list every warning
python3 tools/check.py --only schema,golden
python3 tools/check.py --update-golden  # after an INTENDED output change only; review the diff
```

Needs Python 3.10+ with `openpyxl`, `PyYAML`, `jsonschema` (`python -m pip install --user -r requirements.txt`).
Runs on the PC or the agent box; read-only except `--update-golden` (writes `tests/golden/` only, never `work/`).

| Section | Fails when |
|---------|------------|
| `schema` | a page spec (templates, examples, tests/cases, every work folder) does not validate; an expected-invalid case in `tests/manifest.yaml` passes or fails for the wrong reason. Warns on deprecated fields and specs without a golden |
| `profiles` | a `projects/*/project.yaml`, or the active profile (`project.profile`), does not validate against `schemas/project-profile.schema.json`. Warns when `framework_version` differs from `VERSION` |
| `golden` | regenerating a manifest entry differs cell-by-cell (value, font, fill, alignment, borders, merges, widths, heights, data validation) from `tests/golden/` |
| `stored` | a stored workbook named in the manifest (`templates/out/`, a feature's `excel/`) is missing or out of date (fix the samples with `regenerate.py`) |
| `layout` | a fixed starter cell (labels, header and button blocks, filter / import tables) or column width differs from `templates/excel/page-spec-templates.xlsx` |
| `starter` | the starter workbook's SHA-256 changed (it stays byte-for-byte, **R6**) |
| `encoding` | a text file has a BOM, is not UTF-8, mixes CRLF and LF, or contains mojibake / U+FFFD |
| `terms` | a project-specific term (`tests/leftover-terms.yaml`) appears outside the allowed folders |
| `slugs` | a feature slug exists in more than one work folder (**R8**), read from `../ai-framework.config.yaml` |
| `crossref` | never fails; warns when a spec's service or permission does not match its project profile |

A crashing check counts as a failure. Add every new real-feature spec to `tests/manifest.yaml`
(group `features`, `golden: <feature>/<page>.json`) and run `--update-golden --only golden` once
to create its golden.

## regenerate.py

Rewrites every stored sample workbook named in `tests/manifest.yaml` (each
entry's `output`, generated with its group's profile). The manifest is the one list of YAML →
workbook pairs, so there are no per-folder regenerate commands to keep in step.

```bash
python3 tools/regenerate.py                 # Windows: py tools/regenerate.py
python3 tools/regenerate.py --group samples # one manifest group only
```

Outputs inside a work folder are never written: regenerate a feature's `excel/` with
`generators/excel_spec.py` as part of that feature's planning. An invalid spec is skipped
(exit code 1). Run `check.py` afterwards.
