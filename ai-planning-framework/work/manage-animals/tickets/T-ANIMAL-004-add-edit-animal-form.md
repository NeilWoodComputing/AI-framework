# Ticket: T-ANIMAL-004 — Add | Edit Animal Basic Form

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-004 |
| Type | UI page |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/add-edit-animal.yaml`, `excel/add-edit-animal.xlsx` |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Depends on | T-ANIMAL-002 (API + schema), T-ANIMAL-006 (Switch, Tag Input), T-ANIMAL-003 (entry points: "+ Add Animal", Edit Animal in the row actions menu), T-ANIMAL-008 (the Manage Animals page that hosts the form modal; decision 28) |
| Decisions | `plan.md` › Decisions 1, 2, 3, 4, 8, 9, 10, 11 (superseded by 22), 15, 16, 20 (View dropped), 22 / 24 (single permission `animals_write`), 27 (form is a modal over the Manage Animals page), 23 / 26 (Edit Animal in the row actions menu opens Edit mode) |
| Open questions | None. Q35 (`animals_write`): Neil accepted the suggested defaults for all remaining questions at 2026-10-08 15:44 BST |

## User story

**As a** administrator  
**I want** to add or edit an animal on a single Basic Form  
**So that** animal details are stored correctly and available from Manage Animals

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input | Animals | Animal (creatures.animals) | Name |
| Date Born | Date Picker (date only) | Animals | Animal (creatures.animals) | DateBorn |
| Attributes | Tag Input (multi-value) | Animals | Animal (creatures.animals) | Attributes |
| Is Furry | Switch | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch | Animals | Animal (creatures.animals) | HasHooves |

## Work to do

1. Build the form as a routed modal over the Manage Animals page `/examples/animals` (`src/features/animals/animal-form-modal/AnimalFormModal.tsx` via `@modal/(.)manage/item[/id]`, closing back to `/examples/animals`; decision 27) (copy `src/features/reference-data/reference-data-item-form-modal/`: JSON Forms + `*.ui-schema.json` + entity data provider), loading the schema from `GET v1/schemas/create-animal`.
2. Render sections **Animal Details** (Name, Date Born, Attributes) and **Characteristics** (Is Furry, Has Hooves) per the Excel spec, using the shared Switch and Tag Input renderers from T-ANIMAL-006 and a date-only control for Date Born.
3. Add mode defaults: Name and Date Born blank; Is Furry Off; Has Hooves Off; Attributes empty.
4. Validation messages exactly as the spec: Name required / unique; Date Born required / before today (UI checks the browser's local date); Attributes ≤ 50 characters per tag, ≤ 20 tags; any characters. Show the API's "An animal with this name already exists" on save.
5. Save/load through the Animals service (`v1/Animal`) to table Animal for the columns above. Edit loads the current values; Save sends Attributes as a string array (`[]` when empty).
6. Modes: **Add and Edit only**, both need `animals_write` (decisions 22, 24). Edit mode opens from Edit Animal in the Manage Animals row actions menu (decisions 23, 26). There is no View mode (decision 20); remove any `mode=view` route or read-only rendering for this form. Users without write permission cannot open the form. Opening a soft-deleted or unknown animal shows the framework's standard not-found / error state (the API returns 404).

## Acceptance criteria

### Scenario: S1 — Add mode opens with defaults

```gherkin
Given I have permission animals_write
When I open Add Animal from Manage Animals
Then Name and Date Born are empty
And Is Furry and Has Hooves are Off
And Attributes has no tags
```

### Scenario: S2 — Create animal with required fields

```gherkin
Given I open Add Animal from Manage Animals
And today's local date is after 01/01/2020
When I enter Name "Bessie"
And I enter Date Born "01/01/2020"
And I leave Attributes empty
And I leave Is Furry and Has Hooves off
And I save the form
Then the form closes successfully
And the Animals service writes Animal.Name = "Bessie"
And the Animals service writes Animal.DateBorn = 2020-01-01 (date only)
And Animal.Attributes is stored as []
And Animal.IsFurry and Animal.HasHooves are false
And the new animal appears on Manage Animals
```

### Scenario: S3 — Name is mandatory

```gherkin
Given I open Add Animal from Manage Animals
When I clear Name and attempt to save
Then I see the validation message "Name is required"
And no row is written via the Animals service to Animal
```

### Scenario: S4 — Duplicate name is rejected on Save

```gherkin
Given a non-deleted Animal already exists with Name "Bessie"
And I open Add Animal
When I enter Name "bessie"
And I enter a valid Date Born before today
And I attempt to save
Then I see the validation message "An animal with this name already exists"
And no conflicting row is written via Animals to Animal.Name
```

### Scenario: S5 — Name of a deleted animal can be reused

```gherkin
Given the only Animal named "Bessie" has been soft-deleted
And I open Add Animal
When I enter Name "Bessie" and a valid Date Born and save
Then the form closes successfully
And the Animals service writes a new Animal with Animal.Name = "Bessie"
```

### Scenario: S6 — Date Born must be before today

```gherkin
Given I open Add Animal or Edit Animal
And Name is populated
When I set Date Born to today's local date or a future date
And I attempt to save
Then I see the validation message "Date Born must be before today"
And Animal.DateBorn is not updated via the Animals service
```

### Scenario: S7 — Date Born is mandatory

```gherkin
Given I open Add Animal
And Name is populated
When Date Born is empty and I attempt to save
Then I see the validation message "Date Born is required"
And no row is written via the Animals service to Animal
```

### Scenario: S8 — Attributes persist as JSON tags

```gherkin
Given I open Add Animal or Edit Animal
When I add attribute chips "nocturnal" and "endangered & rare"
And I save with valid Name and Date Born
Then the Animals service writes Animal.Attributes as ["nocturnal","endangered & rare"]
```

### Scenario: S9 — Attribute tag limits

```gherkin
Given I open Add Animal or Edit Animal
When I enter an attribute tag longer than 50 characters
Then I see the validation message "Each attribute tag must be 50 characters or fewer"
When I try to save with more than 20 attribute tags
Then I see the validation message "A maximum of 20 attributes is allowed"
And Animal.Attributes is not updated via the Animals service
```

### Scenario: S10 — Edit persists changed fields

```gherkin
Given an existing Animal is opened in Edit mode
When I change Is Furry to on
And I change Has Hooves to on
And I save
Then the Animals service updates Animal.IsFurry = true
And the Animals service updates Animal.HasHooves = true
And unchanged columns on Animal are left as they were
And Manage Animals shows the new Last Amended date, time and my display name
```

### Scenario: S11 — Only Add and Edit modes exist

```gherkin
Given I am signed in with permission animals_write
When I open Add | Edit Animal from Manage Animals
Then it opens in Add mode (from "+ Add Animal") or Edit mode (from Edit Animal in the row actions menu) only
And there is no View mode and no read-only rendering of the form
When I am signed in without permission animals_write
Then I cannot open the form in any mode
And no reads of the form schema or writes are made via the Animals service
```

### Scenario: S12 — Deleted animal cannot be opened

```gherkin
Given an Animal has been soft-deleted
When I open its Edit URL directly
Then the Animals service returns not found
And the form shows the not-found / error state with no fields loaded
```

Checklist (derived from scenarios):

- [ ] UI behaviour matches the Excel control rows (enablement, mandatory, validation messages, Add defaults)
- [ ] Data read/written via `Animals` to `Animal.<column>` as asserted in Then/And
- [ ] Add / Edit only for `animals_write` (decision 24); no View mode (decision 20)
- [ ] Uses the shared Switch / Tag Input renderers (no feature-local copies)

## Out of scope

- Manage Animals grid / Actions column (T-ANIMAL-003, T-ANIMAL-007)
- Soft delete confirmation (T-ANIMAL-005)
- Building the Switch and Tag Input renderers (T-ANIMAL-006)
- View mode (dropped — decision 20)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-004`
- Spec source: `specs/add-edit-animal.yaml` → `excel/add-edit-animal.xlsx`
- Opened from Manage Animals in Add or Edit mode only. Decision 20 (Neil, 2026-10-08 14:31 BST) dropped View; S11 (was "View mode is read-only") was replaced in place by "Only Add and Edit modes exist", so scenario numbering is unchanged.
- The UI validates "before today" against the browser's local date; the API uses the UTC date (decision 9).
- Running locally needs Neil's `NEXT_PUBLIC_UNITY_API_ROOT` setting in `.env.local`; agents never open or edit `.env*` files (decision 16).
- Scenario IDs frozen 2026-10-08 from current positions (S1-S12; ticket heading IDs T-ANIMAL-004/S<n> for tests; doc-only, no wording or behaviour change).
