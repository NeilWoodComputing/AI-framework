# Changelog

Framework version is in `VERSION` (semantic: major = breaking spec / layout change, minor = new
features or stricter checks, patch = fixes). Project profiles record the major.minor they were
written for in `framework_version`. Dated reasons: `DECISIONS.md`.

## 1.2.0 — 2026-11-13

GitHub ticket publishing adapter complete. No spec or schema change.

- **GitHub adapter** (`skills/publish-tickets/adapters/github.md`): Complete field mapping for GitHub Issues, including title format `[T-<DOMAIN>-NNN] <title> (<page type>)`, body with full Given/When/Then scenarios plus Acceptance criteria summary section (checkable bullets), labels (stable ID, feature slug, page type, `ai-planning-framework`, default_labels), sub-issues only for explicit child tasks, and upsert by stable ID label or title prefix.
- **Config** (`../ai-framework.config.yaml`): Added `tickets.github` block (owner `NeilWoodComputing`, repository `ai-framework-tests`, project `AI testing`, default_labels). Set `tickets.target: github` and `tickets.enabled: true`. Updated guard comment to reflect explicit-user-approval requirement. Jira adapter remains a stub.
- **Cross-repo workflows** (`../handoff/README.md`): Documented cross-repo closing keyword `Closes NeilWoodComputing/ai-framework-tests#N` for PRs that close issues in a different repository.
- **Docs**: Updated `skills/publish-tickets/SKILL.md` (GitHub no longer marked as stub) and `README.md` to reflect GitHub as a complete adapter alongside Azure DevOps.
- **Authentication**: GitHub adapter uses a connected GitHub connector where available, otherwise the env var named by `secrets.github_token_env`.

## 1.1.4 — 2026-11-11

More coverage cases, taken from branches the template samples mention but do not pin down. No spec, schema or layout change. Existing goldens are unchanged.

- **Valid:** `flat-form.yaml` (flat controls with DB columns; the samples use sections), `grid-no-filters.yaml` (`search_filters: []` and an empty actions menu), `import-defaults.yaml` (download button, panel and Cancel / Upload left to the starter defaults).
- **Invalid:** wizard without steps, form with no body, import column missing its mapping, import with no columns, a grid that also carries form controls, an unknown page type.

## 1.1.3 — 2026-11-11

No domain folders inside the framework. No spec, schema or layout change. Feature workbook content is unchanged.

- **Active profile moved out:** `projects/candc/project.yaml` is now `../project.yaml` (beside `ai-framework.config.yaml`). `projects/` keeps only `_template/`. `tools/check.py` validates that profile wherever `project.profile` points.
- **Removed:** `examples/candc/` and `tests/golden/candc/` (the same page types as the neutral Library samples). `examples/` keeps `source-attachments/`, the filled workbooks the starter was taken from.

## 1.1.2 — 2026-11-11

Domain-neutral feature folder. No spec, schema or layout change.

- **One feature folder:** new features go to `work/<feature>/` (was `projects/<project>/work/`, which made the framework hold a project-named folder). `projects/candc/work/` removed (it was empty). `project.work_dir` and `output.work_dirs` in `ai-framework.config.yaml` and in the profiles now name `ai-planning-framework/work`.
- **Docs:** `projects/README.md`, `AGENT-BRIEF.md` and `README.md` describe the single folder.

## 1.1.1 — 2026-11-11

Tidy-up; no spec, schema or layout change. Generated workbook content is unchanged (cell-level identical).

- **Folders:** `out/` → `templates/out/` (next to the `templates/yaml/` it is generated from); `profiles/stacks/` → `skills/generate-code-stubs/stacks/` (its only reader); `profiles/` removed.
- **Removed:** `examples/source-attachments/Manage-Organisation-Contact.xlsx` (byte-identical copy of `Manage-Contacts.xlsx`), `out/README.md` (merged into `templates/README.md`), `generators/__pycache__/`, a dead branch in `tools/check.py`.
- **`tools/regenerate.py`:** rewrites the stored sample / example workbooks from `tests/manifest.yaml`, replacing the bash loops repeated in three READMEs. Stored workbooks were rewritten with it (fixed timestamps; content unchanged).
- **Docs:** README "What you get" grouped by folder; the feature-folder tree kept once (`loops/feature-planning.md`, now listing `tests/`); repeated starter-workbook text trimmed in `examples/README.md`; CandC examples use `feature_module` instead of the deprecated `system_feature`.

## 1.1.0 — 2026-10-27

Reliability tooling. Generated workbook content is unchanged (cell-level identical; manage-animals included).

- **Strict schema:** unknown or misspelt fields are errors (`additionalProperties: false`); old names are marked `deprecated` (`system_feature`, `unity_feature`, `primary_action`, `action`, `availability`); optional `spec_version`. DB mapping is required unless `include_service_db_columns: false`.
- **Generator** validates before writing, with field-named errors and `--no-validate` for drafts; deterministic output (fixed timestamps); starter read once per run; warnings instead of silent fallbacks; control characters removed with a warning; duplicated block-writing code merged.
- **`tools/check.py`**: one command for schema, profiles, golden regression, stored outputs, layout vs starter, starter hash, encoding, leftover terms, duplicate slugs and profile cross-checks.
- **Tests:** `tests/manifest.yaml`, goldens for samples, CandC examples and real features, coverage cases and expected-invalid specs.
- **Profiles:** `schemas/project-profile.schema.json`, `framework_version`.
- **Docs:** `RULES.md` (R1–R9) replaces repeated rule text; editing rules and "running the tools" in `AGENT-BRIEF.md`; `.editorconfig`; tools run wherever Python is available (PC included). `requirements.txt` adds jsonschema.

## 1.0.0 — 2026-10-27

Generic framework: project profiles (`projects/`), neutral Library samples, CandC moved to `examples/candc/`, `feature_module` header field, `publish-tickets` with tracker adapters, `DECISIONS.md`.
