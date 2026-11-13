# Skill: generate-user-journey

Derive user journeys from page specs and the feature plan. **Secondary** to full-stack UI↔DB specs — use after YAML/Excel specs exist so steps name real fields and persist targets.

## Purpose

Document how an actor moves through manage pages and wizards, including what is **read/written** to which service/table.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `plan` | Yes | Feature plan |
| `page_specs` | Yes | YAML (or Excel) specs with DB mappings |
| `primary_actor` | Yes | Role for this journey |

## Outputs

One markdown file per journey using `templates/journeys/journey.md`:

- Journey id, actor, goal, trigger
- Steps tied to **page title** + **step title** (wizards) or **action menu item** (manage)
- Data touched: Service / Table / Column (or Population Source)
- Success / failure paths

## Steps

1. Pick the happy path from manage → add/edit → save → return to list.
2. For each UI step, cite controls and their DB mapping from the spec.
3. Add alternate paths (validation failure, cancel, delete confirm — soft delete when the profile's `conventions.soft_delete` is true).
4. Note permission gates from the plan.
5. Keep journeys short; link to the Excel/YAML as source of truth for fields.

## Quality checks

- [ ] Every step references a page that exists in the specs
- [ ] Persist/read steps name Service + Table (and column where relevant)
- [ ] Validation failures match Validation Failure Message(s) in the spec
- [ ] No journey invents fields missing from the UI spec

## Priority note

If time is limited, finish **generate-ui-spec** (YAML + Excel with DB columns) before expanding journeys.
