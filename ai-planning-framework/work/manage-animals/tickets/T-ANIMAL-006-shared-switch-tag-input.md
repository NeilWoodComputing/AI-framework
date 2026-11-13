# Ticket: T-ANIMAL-006 — Shared Switch and Tag Input controls for Next.js JSON Schema forms

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-006 |
| Type | UI framework component |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/add-edit-animal.yaml`, `excel/add-edit-animal.xlsx` (controls Is Furry, Has Hooves, Attributes); `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` (Attributes / tag display; boolean icon display is T-ANIMAL-009) |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Decisions | `plan.md` → Decisions 1, 15, 20, 29 (boolean grid cells moved to T-ANIMAL-009) |

## User story

**As a** developer building Unity pages in UI.NextJs.Framework  
**I want** reusable Switch and Tag Input renderers in the shared JSON Schema form framework, plus a string-array grid cell helper  
**So that** Add | Edit Animal (and future forms) can render the spec's Switch and Tag Input (multi-value) controls without feature-local copies. *(Boolean grid cells moved to T-ANIMAL-009 per decision 29 — old → new note below.)*

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Is Furry | Switch (form only; grid boolean icons are T-ANIMAL-009) | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch (form only; grid boolean icons are T-ANIMAL-009) | Animals | Animal (creatures.animals) | HasHooves |
| Attributes | Tag Input (multi-value) (form) / comma-separated tags (grid) | Animals | Animal (creatures.animals) | Attributes |

## Work to do

1. Add a **Switch** renderer for `boolean` properties in `src/framework/json-schema-form/` (registered with a tester like the existing text / text area renderers), honouring the schema default, read-only and disabled states (generic framework support; the animal form no longer has a View mode — decision 20).
2. Add a **Tag Input** renderer for `array` of `string` properties: type a value and press Enter (or the design system's add action) to add a chip; remove chips individually; shows schema validation errors for `items.maxLength` and `maxItems`; value is always an array (`[]` when empty); read-only shows chips without add/remove.
3. Add a grid cell display helper in the shared entity grid for **string arrays** only (comma-separated, empty array = empty cell) — `formatStringArrayCell` in `src/framework/entity-framework/grid/grid-cell-renderers.tsx`. **Boolean grid cells are out of scope for this ticket** (moved to T-ANIMAL-009 `renderBooleanIconCell` per decision 29). Do not add or keep a boolean switch grid-cell requirement here; `renderBooleanSwitchCell` may remain in the framework for other grids but is not acceptance for animals.
4. Keep them generic (no animal-specific code); use `@design-system` components where they exist.

## Acceptance criteria

### Scenario: S1 — Switch renders and binds a boolean

```gherkin
Given a JSON Schema form with a boolean property "isFurry" defaulting to false
When the form renders in Add mode
Then a Switch is shown in the Off position
When I turn the Switch on
Then the form data value of "isFurry" is true
```

### Scenario: S2 — Tag Input adds and removes chips

```gherkin
Given a JSON Schema form with an array-of-strings property "attributes" with items maxLength 50 and maxItems 20
When I type "nocturnal" and press Enter, then type "endangered & rare" and press Enter
Then two chips are shown and the form data value is ["nocturnal","endangered & rare"]
When I remove the "nocturnal" chip
Then the form data value is ["endangered & rare"]
When I remove every chip
Then the form data value is []
```

### Scenario: S3 — Tag Input shows the schema limit errors

```gherkin
Given the "attributes" property above with the spec's validation messages
When I add a tag longer than 50 characters
Then I see "Each attribute tag must be 50 characters or fewer"
When I add a 21st tag
Then I see "A maximum of 20 attributes is allowed"
```

### Scenario: S4 — Read-only rendering (generic framework capability)

```gherkin
Given a JSON Schema form is rendered read-only (not used by Add | Edit Animal since decision 20)
When the form renders
Then the Switch cannot be toggled
And Tag Input chips are shown without add or remove controls
```

### Scenario: S5 — String-array grid cells

```gherkin
Given a grid column bound to an array of strings
When a row with ["dairy","docile"] renders
Then the array column shows "dairy, docile"
And a row with [] shows an empty cell
```

*(Old → new: the previous "Grid cells" scenario also required a read-only boolean Switch cell. That boolean part moved to **T-ANIMAL-009** scenarios S1–S3 / T-ANIMAL-003 S14–S15 under decision 29. This scenario keeps only the string-array half and is renamed in place.)*

Checklist (derived from scenarios):

- [ ] Renderers live in `src/framework/json-schema-form/` and are registered for any form, not just animals
- [ ] Read-only and disabled states supported (generic)
- [ ] Array value never null
- [ ] Existing renderers and forms unaffected (existing tests still pass)

## Out of scope

- Using the controls on the animal pages (T-ANIMAL-003, T-ANIMAL-004)
- Boolean icon grid cell renderer (T-ANIMAL-009; was previously the boolean half of this ticket's grid-cell work)
- Date Picker changes (Date Born uses a date-only control in T-ANIMAL-004)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-006`
- This changes shared framework code; Neil approved that on 2026-10-08 (decision 15).

- Decision 29 (Neil, 2026-10-08 19:04 BST via Review Bot): **Rescoped** — boolean read-only Switch grid cell removed from this ticket; that behaviour moves to T-ANIMAL-009 (`renderBooleanIconCell`). Old → new: scenario "Grid cells" → "String-array grid cells" (string-array half kept; boolean half → T-ANIMAL-009 S1–S3 / T-ANIMAL-003 S14–S15). Form Switch and Tag Input stay here. Neil's own change; no separate re-approval.
- Scenario IDs frozen 2026-10-08 from current positions (S1-S5; ticket heading IDs T-ANIMAL-006/S<n> for tests; doc-only, no wording or behaviour change).
