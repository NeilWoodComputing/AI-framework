# Skill: review-spec-conformance

Check that what renders on screen matches the page spec, control by control.

## Purpose

Prove each control in the linked YAML / Excel is built as specified: label, control type, mandatory, editable, enablement, min / max, validation rules and **exact** failure messages. For grids (Paginated Grid, Embedded Grid Modal): columns, population source binding, sorting, paging, empty state, primary action and row actions.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | From `gather-pr-context` (control inventory, review scope) |
| `diff` | PR route / `direct_scope: diff` | PR or local diff |
| `files` | Yes | Full content of the UI and schema files in the review scope (direct plan scope: every file in scope), and the unchanged files they depend on |

## Where controls are defined in this stack

| Concern | API.Framework | C# API | UI (Next.js) | UI (Angular) |
|---------|---------------|-----------|---------------|--------------|
| Field list, types, `required`, `minLength` / `maxLength`, `format`, `oneOf` | Schema JSON under `Validation/Schemas`, served by `IJsonSchemaFileApi` | Schema builder / JSON under `entities validation schemas folder`, served from `GET v2/schemas/{schema-name}` | Rendered from the server schema with JSON Forms | Same |
| Layout, sections, steps, labels, read-only, rules | — | — | `src/features/<area>/<x>-form-modal/ui-schemas/*.ui-schema.json`, rendered by `src/framework/json-schema-form` | `ui-schemas/{step}.ui-schema.json`, `{feature}-wizard.config.ts` |
| Custom validation and messages | `constraints` + `messages` keyed by constraint `id` | `constraints` + `messages` on the property | Displays server messages; any client rule must use the same text | Same |
| Grid columns, sorting | The area's list model and its search endpoint | List model in `Controllers/V2/TempEntityModels`, `sortBy` handling | `src/features/<area>/<grid>/columns/` | Entity grid column config |

Read the column for `development.api.active` and the column for `development.ui.active`.

## Steps

1. For each spec file, list its controls (or columns / actions) from the context pack.
2. Find each control in code by its schema scope (`#/properties/<camelCaseName>`) and label. Read unchanged files when the control is not in the diff. On the direct plan scope, search every file in scope.
3. Compare each attribute:

   | Spec field | What to check |
   |------------|---------------|
   | `label` | Schema `title` or UI schema `label` text matches exactly (case and punctuation) |
   | Step / section `title` and order | Wizard step labels or `Group` / section titles and order match |
   | `control_type` | Keyed Input → text input; Single-select Dropdown → `oneOf` / `enum` with a select renderer (searchable if stated); Multi-select → array of `oneOf`; Switch → boolean toggle; Date → date control; List Form → array control |
   | `input_format` | Email → `format: email` or equivalent pattern; Numeric → number / integer type; Boolean → boolean |
   | `min_len_val` / `max_len_val` | `minLength` / `maxLength` (strings) or `minimum` / `maximum` (numbers); `N/A` means none required |
   | `mandatory` | Property in the schema `required` array **and** the UI shows it as required |
   | `editable` | `No` → read-only in the UI schema **and** the server does not accept a changed value (cross-check in stage 6) |
   | `enablement` | `Always`, or the JSON Forms `rule` (ENABLE / DISABLE / SHOW / HIDE) matching the stated condition |
   | `validation_rules` | Implemented by a schema keyword, a `constraints` entry, or a service check — name which |
   | `validation_failure_messages` | Message text is **identical** to the spec, wherever it is produced |
   | `conditional_visibility` | Mode or field conditions (for example `Mode = View` → all read-only, Save hidden) |

4. For grids (Paginated Grid, Embedded Grid Modal; page types in `checklists/full-stack-checklist.md`), also check:
   - Column titles and order; each column's field binds to the list-model property fed by its **Population Source**
   - `display_format` (for example `DD/MM/YYYY HH:MM [Username]`)
   - `sortable` columns: `sortBy` value accepted by the API (grid field name, not a downstream enum)
   - Default sort (`additional_functionality`)
   - Results filter matches the results-area description (for example non-deleted rows for the parent organisation)
   - Paging and the empty state
   - Primary action label, visibility, enablement and what it opens (form name and mode)
   - Row actions (actions menu items): icon, required permission, availability logic and `action_on_click` (correct modal and mode; Delete → confirmation then soft delete)
   - Paginated Grid: a routed page with search and filters on the page and no list modal, with both tickets of the split (page and grid) linked. Embedded Grid Modal: no route

   For Form Modal and Basic Form, also check section visibility, buttons and the required permission. For Wizard Modal and Full-Page Wizard, check each step's format (Standard Form or List Form), visibility, sections and per-step validation, and Back / Next / Finish only if the spec lists them. For Import, check the Download Template button, the upload panel (`.xls` / `.xlsx` only, one file at a time, removable), Cancel / Upload, and template-column validation.
5. Record a status per control: **Match**, **Mismatch** (say which attribute), **Missing** (in spec, not built), **Extra** (built, not in spec), or **Not in PR** (PR route: unchanged and already correct, or deferred by the ticket's out-of-scope list). On the direct plan scope use **Not implemented** (no file in scope implements it; a finding) or **Deferred** (the ticket's out-of-scope list defers it).
6. Raise findings using `checklists/severity.md`: missing mandatory control → Blocker; missing optional control, wrong control type, wrong mandatory / editable / enablement, wrong validation message → Major; label text difference → Minor.

## Outputs

- Spec conformance table rows for the report (one per control, column and action)
- Findings with `file:line` and spec reference (`specs/<page>.yaml` → section / step → control label)

## Quality checks

- [ ] Every control, column and action in the linked specs has a row
- [ ] Messages compared character for character and quoted in findings
- [ ] Extras (fields not in spec) are listed, not silently accepted
- [ ] Nothing is marked wrong for following the spec; suspected spec errors go to out-of-scope notes
- [ ] No labels, rules or messages invented beyond the YAML
