# Full-stack checklist

Use for every control and grid column in the linked specs, by page type (below). The spec YAML is the expectation; never add expectations it does not contain.

## Page types

The planning agent's page types; layout reference: `ai-planning-framework/templates/excel/page-spec-templates.xlsx`. Check only what the spec for the page lists.

| Page type | What it is | Check |
|-----------|------------|-------|
| **Paginated Grid** (was "manage list") | A routed list page: search and filters on the page, no list modal | Results grid (**Per grid column**), paging, empty state, default sort, row actions (**Per grid action**), and both tickets of the split (page and grid) |
| **Embedded Grid Modal** (was the list "Modal") | A list inside a modal or a parent page; no route | The same grid and row-action checks as Paginated Grid |
| **Form Modal** | A create / edit dialog | The control table (**Per control**), section visibility, buttons and required permission |
| **Basic Form** | A full routed page | The same control checks as Form Modal |
| **Wizard Modal** | Steps, each with a format (Standard Form or List Form), visibility and sections | Each step's controls (**Per control**) and per-step validation; Back / Next / Finish only if the spec lists them |
| **Full-Page Wizard** | The same as Wizard Modal, as a routed page | As Wizard Modal |
| **Import** | Bulk upload from a template | Download Template button; upload panel (`.xls` / `.xlsx` only, one file at a time, removable); Cancel / Upload buttons; template-column validation with Service / Target DB Table / Target DB Column mapping |

## Per control (Form Modal, Basic Form, Wizard Modal and Full-Page Wizard steps)

- [ ] **Rendered** — control appears in the right step or section, in spec order
- [ ] **Label** — matches the spec exactly
- [ ] **Control type** and **input format** — match the spec (Keyed Input, Single-select Dropdown, Switch, Date, List Form, …)
- [ ] **Mandatory** — in the server schema `required` and shown as required in the UI
- [ ] **Editable / enablement** — read-only and enable / show rules match; read-only fields are not writable through the API
- [ ] **Min / max** — schema `minLength` / `maxLength` or `minimum` / `maximum` match; DB column at least as long
- [ ] **Validation** — each rule implemented (schema keyword, `constraints` entry or service check) on the server
- [ ] **Messages** — failure messages identical to the spec
- [ ] **UI binding** — `#/properties/<camelCaseField>` matches the C# property name (JSON is camelCase)
- [ ] **API record / DTO** — the property exists on the record or list model for the active API (where that type lives: that API's checklist)
- [ ] **Mapper** — where this API maps a UI record to a stored model, the field is mapped both ways and fields the section does not own are preserved
- [ ] **Service** — the write goes through the spec's Service
- [ ] **Table.Column** — the stored property maps to the spec's **Target DB Table**.**Target DB Column**
- [ ] **Type / nullability** — the stored type and nullability fit the control and the mandatory flag
- [ ] **Migration** — a new or changed local column has a migration where that API's checklist says migrations live; the snapshot is updated; no data loss
- [ ] **Read back** — edit and view modes load the stored value into the same control

## Per grid column (Paginated Grid, Embedded Grid Modal)

- [ ] Column title and order match
- [ ] Grid column `field` matches the list-model property name
- [ ] List-model property is filled from the **Population Source** (`Table.Column`)
- [ ] Display format matches (for example `DD/MM/YYYY HH:MM [Username]`)
- [ ] Sortable columns accepted as `sortBy` by the API; default sort applied
- [ ] Results filter matches the results-area description (for example non-deleted rows for the parent record)

## Per grid action (Paginated Grid, Embedded Grid Modal)

- [ ] Primary action label, visibility, enablement and target (form name and mode)
- [ ] Each row action: label, icon, required permission, availability logic and action on click (correct form and mode)
- [ ] Delete → confirmation, then soft delete when the spec says so

## Across the change (PR diff or direct-route scope)

- [ ] Nothing persisted that is not in a spec (extra columns, properties or migrations listed)
- [ ] UI route change paired with the matching API controller change
- [ ] Every Given / When / Then scenario traced (see `skills/review-acceptance-criteria`)
