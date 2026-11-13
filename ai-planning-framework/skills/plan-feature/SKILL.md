# Skill: plan-feature

Plan a development feature as a structured full-stack brief before UI specs, journeys, or tickets.

## Purpose

Turn a rough feature request into a clear plan that names **screens**, **services**, and **data stores** up front. This is an implementation-oriented plan, not a marketing brief.

## Config first

Read `../ai-framework.config.yaml` and the project profile it names (`project.profile`; defaults in `projects/_template/project.yaml`). Use the profile's `services`, `glossary`, `permissions.pattern`, `database` and `conventions` instead of guessing, and apply only the `rules` that are on.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `feature_name` | Yes | Short name (e.g. Manage Books, Edit Member) |
| `problem` | Yes | What user/job is blocked today |
| `actors` | Yes | Roles who use the feature |
| `constraints` | No | Tenancy, permissions, integrations, deadlines |
| `known_entities` | No | Tables/aggregates already known (e.g. Book, Member, …; see the profile's `services`) |
| `known_services` | No | Backend services already known |

## Outputs

Write `plan.md` (or return the same structure in chat) with:

1. **Summary** — one paragraph
2. **Actors & permissions**
3. **Pages / surfaces** — each classified as `Form Modal`, `Basic Form`, `Wizard Modal`, `Full-Page Wizard`, `Paginated Grid` (a feature list with its own route), `Embedded Grid Modal` (a list embedded in another page's flow) or `Import` (bulk upload from a template) — see the rule under Steps, with the **required permission** for each page
4. **Domain entities** — proposed tables/aggregates and owning **Service**
5. **Field inventory (draft)** — for each entity: likely columns the UI will need (feeds generate-ui-spec)
6. **Integrations** — ref data, other services (e.g. Members for a member picker)
7. **Open questions** — anything blocking a UI spec
8. **Suggested delivery slices** — vertical slices that each deliver UI + persistence, not UI-only

**Layout reference:** each page type matches a sheet of the starter workbook `templates/excel/page-spec-templates.xlsx` (Modal, Wizard, Grid Page, Import templates). Read it when classifying pages so the plan asks for the fields the spec will need (Required Permission, buttons, filters, actions menu permissions, import template columns). Do not edit it; copy it to fill in. See `templates/README.md`.

## Steps

1. Restate the feature in one sentence with the primary actor.
2. List user-visible surfaces (list/manage vs create/edit wizards). Apply **R1** (`RULES.md`): a routed feature list is one `Paginated Grid` page, not a modal; plan it with the two tickets of **R2**. Choose a feature slug that exists in no work folder (**R8**).
3. For each surface, draft the **entities touched** and **owning service**.
4. Sketch a field inventory: label → likely DB column → service. Mark unknowns with `TBD`.
5. Call out cross-cutting rules from the profile's `conventions` (uniqueness per tenant when `multi_tenant`, soft delete when `soft_delete`, `audit_columns`), plus any the feature adds.
6. Produce delivery slices that always include a persist path (API/DB), not screens alone.
7. List open questions that would change the Excel control grid or DB mapping.

## Quality checks

- [ ] Every proposed page has one of the seven page types (form modal / basic form / wizard modal / full-page wizard / paginated grid / embedded grid modal / import), each matching a sheet of `templates/excel/page-spec-templates.xlsx`
- [ ] Every gated page names its required permission
- [ ] Every feature list with its own route is planned as a `Paginated Grid` page (list on the page); modals only for create / edit forms, confirms and embedded lists
- [ ] Each Paginated Grid has a page ticket and a paginated grid ticket in the delivery slices
- [ ] Every entity has an owning **Service**
- [ ] Field inventory mentions Service + Table + Column (even if draft)
- [ ] No slice is “UI only” without a persistence note
- [ ] Open questions are concrete and answerable

## Anti-patterns

- Vague “build a form” with no table/column targets (use `Form Modal` / `Basic Form` and map every control)
- Using Wizard Modal for a single-page edit when Form Modal / Basic Form would be clearer
- Putting a routed feature list in a modal, auto-opening a list modal, or adding a landing page whose only job is to open the list
- Journeys before knowing which fields persist where
- Assuming a front-end framework (keep stack-agnostic)
