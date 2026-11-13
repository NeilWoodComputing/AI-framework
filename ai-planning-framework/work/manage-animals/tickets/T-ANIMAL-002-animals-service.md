# Ticket: T-ANIMAL-002 — Animals service + v1/Animal API, validation and permissions

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-002 |
| Type | Service API |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/add-edit-animal.yaml`, `excel/add-edit-animal.xlsx`, `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Depends on | T-ANIMAL-001 |
| Decisions | `plan.md` › Decisions 1, 2, 3, 5, 7, 8, 9, 10, 11 (superseded by 22), 12, 13, 18, 20, 21, 22 / 24 (one animals permission, `animals_write`, on every endpoint), 25 (who gets it; seed in T-ANIMAL-001) |
| Open questions | None. Q35 (`animals_write` / `AnimalsWrite`): Neil accepted the suggested defaults for all remaining questions at 2026-10-08 15:44 BST. The permission wording is decided (decision 24) |

## User story

**As a** administrator  
**I want** the Animals service to list, create, read, update and soft-delete Animal records with Name uniqueness and Date Born before-today rules  
**So that** invalid or duplicate animals cannot be saved and only permitted users can change them

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input | Animals | Animal (creatures.animals) | Name (+ derived NormalizedName) |
| Date Born | Date Picker | Animals | Animal (creatures.animals) | DateBorn |
| Attributes | Tag Input (multi-value) | Animals | Animal (creatures.animals) | Attributes |
| Is Furry | Switch | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch | Animals | Animal (creatures.animals) | HasHooves |
| Last Amended | Results column | Animals | Animal (creatures.animals) | UpdatedUtc & UpdatedBy → User.DisplayName (fallback User.Email) |
| Delete Animal | Row actions menu item (decision 26) | Animals | Animal (creatures.animals) | IsDeleted |

## Work to do

1. New `Animals` area: `Api.Framework.Services/Animals/` (`IAnimalService`, `AnimalService`, `AnimalContracts`) and `Api.Framework/Controllers/V1/Animals/AnimalController` at route `v1/Animal`: list (paged, non-deleted only, default sort Name ascending, sortable by every sortable spec column; Last Amended sorts by `UpdatedUtc`), get by id, create, update, and soft delete on `DELETE`. Copy the shape of `ICatalogueItemService` / `CatalogueItemController`.
2. Authorisation with animals' **own single permission** (decision 22, superseding decision 11; amended by decision 24):
   - Permission `animals_write` ("Manage animals"; declared and seeded in `Api.Framework.Data/LoginPermissions.cs` by T-ANIMAL-001). There is **no** read permission and no read policy.
   - New `AnimalPolicies` class in `Api.Framework.Services/Animals/` copying `Api.Framework.Services/Directory/DirectoryPolicies.cs`: policy name `AnimalsWrite` and permission-name constant `WritePermission = "animals_write"`.
   - Register it in `Api.Framework/Program.cs` `AddAuthorization`, next to the directory policies: `AnimalsWrite` = `RequireClaim(TokenService.PermissionClaimType, AnimalPolicies.WritePermission)`.
   - `[Authorize(Policy = AnimalPolicies.AnimalsWrite)]` on **every** animal endpoint: list, get, create, update, delete (`AnimalController`) and `GET v1/schemas/create-animal` (`AnimalSchemaController`). Remove every `DirectoryPolicies.UserManagementRead` / `UserManagementWrite` use from the animals controllers; other controllers keep theirs.
   - Users get the claim in their next token: after the migration, signed-in users must sign in again or refresh their token before the API accepts them (T-ANIMAL-001 item 6).
3. Form schema: `Records/AnimalRecord` (extends `AbstractFormRecord`, copy `CatalogueItemRecord`) + `Validation/Schemas/animalSchema.json`, served at `GET v1/schemas/create-animal` by a new `Controllers/V1/Schemas/AnimalSchemaController`. One schema for Add and Edit (no View mode — decision 20). Schema: Name required, max 100; DateBorn required, `format: date`, `dateComparison` `compareTo: [TODAY]`, `operator: <`; Attributes array of strings, each `maxLength: 50`, `maxItems: 20`.
4. Name: trim before validating and saving; required after trim ("Name is required"); unique case-insensitive among non-deleted animals using `NormalizedName = Name.Trim().ToUpperInvariant()` ("An animal with this name already exists"). Soft-deleted animals are ignored, so their names can be reused. Map a unique-violation `DbUpdateException` (existing `IsUniqueViolation` pattern) to the same message.
5. DateBorn: required ("Date Born is required"); date only; strictly before today's **UTC** date via the existing `[TODAY]` constraint ("Date Born must be before today").
6. Attributes: serialise to/from the `jsonb` string array; any characters; each tag ≤ 50 characters, ≤ 20 tags; null or missing input is stored as `[]`.
7. Audit: set `UpdatedUtc` (from the clock) and `UpdatedBy` (signed-in user's id from the JWT `sub` claim, as `DirectoryControllers` does) on create, update and soft delete; on create `CreatedUtc` = `UpdatedUtc`. List and get return Last Amended as `UpdatedUtc` plus the `UpdatedBy` user's `DisplayName`, falling back to `Email`.
8. Soft delete: `DELETE v1/Animal/{id}` sets `IsDeleted = true` (row kept). Get, update or delete of a soft-deleted or unknown id returns 404 Not Found. No restore endpoint.

## Acceptance criteria

### Scenario: S1 — Create animal with valid fields

```gherkin
Given I am signed in with permission animals_write
And no non-deleted Animal exists with Name "Bessie" (case-insensitive)
And today's UTC date is 08/10/2026
When I create an Animal via v1/Animal with Name " Bessie ", DateBorn 2020-01-01, IsFurry true, HasHooves true, Attributes ["dairy","docile"]
Then the Animals service writes Animal.Name = "Bessie"
And Animal.NormalizedName = "BESSIE"
And Animal.DateBorn = 2020-01-01
And Animal.IsFurry = true
And Animal.HasHooves = true
And Animal.Attributes = ["dairy","docile"]
And Animal.IsDeleted = false
And Animal.UpdatedBy is my user id and Animal.UpdatedUtc is the time of the save
```

### Scenario: S2 — Missing Attributes are stored as an empty array

```gherkin
Given I am signed in with permission animals_write
When I create a valid Animal via v1/Animal with no Attributes
Then the Animals service writes Animal.Attributes = []
```

### Scenario: S3 — Duplicate name is rejected

```gherkin
Given a non-deleted Animal already exists with Name "Bessie"
When the Animals service attempts to create or update another Animal with Name " bessie " (trimmed, case-insensitive match)
Then the operation fails with message "An animal with this name already exists"
And no conflicting row is written via Animals to Animal.Name
```

### Scenario: S4 — Name of a soft-deleted animal can be reused

```gherkin
Given an Animal with Name "Bessie" has been soft-deleted
When the Animals service creates an Animal with Name "Bessie" and a valid DateBorn
Then the create succeeds
And the new row has Animal.IsDeleted = false
```

### Scenario: S5 — Date Born must be before today

```gherkin
Given today's UTC date is 08/10/2026
When the Animals service attempts to save an Animal with DateBorn 2026-10-08 or a later date
Then the operation fails with message "Date Born must be before today"
And Animal.DateBorn is not written/updated via Animals
```

### Scenario: S6 — Date Born is mandatory

```gherkin
Given I am creating an Animal via the Animals service
When DateBorn is missing
Then the operation fails with message "Date Born is required"
And no row is written via Animals to Animal
```

### Scenario: S7 — Name is mandatory

```gherkin
Given I am creating an Animal via the Animals service
When Name is blank or only whitespace
Then the operation fails with message "Name is required"
And no row is written via Animals to Animal
```

### Scenario: S8 — Attribute tag limits

```gherkin
Given I am creating or updating an Animal via the Animals service
When Attributes contains a tag longer than 50 characters
Then the operation fails with message "Each attribute tag must be 50 characters or fewer"
When Attributes contains more than 20 tags
Then the operation fails with message "A maximum of 20 attributes is allowed"
And Animal.Attributes is not written/updated via Animals
```

### Scenario: S9 — List returns non-deleted animals with Last Amended

```gherkin
Given Animals "Bessie" and "Ziggy" are not deleted and "Daisy" is soft-deleted
And "Bessie" was last saved by a user whose DisplayName is "Animals Tester"
And "Ziggy" was last saved by a user with no DisplayName and Email "animals-nodisplayname@e2e.test"
When I list animals via v1/Animal with permission animals_write
Then the results contain "Bessie" then "Ziggy" (Name ascending) and not "Daisy"
And "Bessie" has Last Amended from Animal.UpdatedUtc with user "Animals Tester"
And "Ziggy" has Last Amended user "animals-nodisplayname@e2e.test"
```

### Scenario: S10 — Soft delete and not found afterwards

```gherkin
Given a non-deleted Animal "Bessie" exists
When I call DELETE v1/Animal/{id} with permission animals_write
Then Animal.IsDeleted = true and the row remains in creatures.animals
And Animal.UpdatedUtc and Animal.UpdatedBy record the delete
And GET v1/Animal/{id} returns 404 Not Found
And PUT and DELETE for that id return 404 Not Found
```

### Scenario: S11 — Users without animals_write are rejected on every endpoint

```gherkin
Given I am signed in without permission animals_write
When I call list or get on v1/Animal
Then the request is rejected with 403 Forbidden
When I call create, update or delete on v1/Animal, or GET v1/schemas/create-animal
Then the request is rejected with 403 Forbidden
And nothing is written via Animals to Animal
```

### Scenario: S12 — User-management permissions alone do not grant access to animals

```gherkin
Given I am signed in with permissions user_management_read and user_management_write but not animals_write
When I call list or get on v1/Animal
Then the request is rejected with 403 Forbidden
When I call create, update or delete on v1/Animal, or GET v1/schemas/create-animal
Then the request is rejected with 403 Forbidden
And nothing is written via Animals to Animal
```

### Scenario: S13 — AnimalsWrite guards every animal endpoint

```gherkin
Given I am signed in with permission animals_write only
When I call list, get, create, update or delete on v1/Animal, or GET v1/schemas/create-animal, with valid input
Then each request succeeds
And Program.cs registers exactly one animals policy, AnimalsWrite, requiring the JWT "permission" claim animals_write
```

Checklist (derived from scenarios):

- [ ] Messages match the Excel/YAML validation failure messages exactly
- [ ] Data read/written via `Animals` to `Animal.<column>` as asserted in Then/And
- [ ] `AnimalsWrite` on list, get, create, update, delete and the form schema (decision 24); no read policy; no `DirectoryPolicies` left on the animals controllers
- [ ] Soft-deleted rows never returned; 404 for get/update/delete of deleted ids
- [ ] Follows API.Framework conventions (`CLAUDE.md`, `json-schema-forms.mdc`)

## Out of scope

- Manage Animals grid UI (T-ANIMAL-003)
- Basic Form chrome (T-ANIMAL-004)
- Soft-delete confirmation UI (T-ANIMAL-005)
- Restore, "include deleted" listing, filtering / search, import / export

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-002`
- Decision 21 (`creatures` schema) does not change the service or API surface; only the table's schema moves (`creatures.animals`), see T-ANIMAL-001.
- Decision 20 (View dropped) did not change this API. Decision 22 (Neil, 2026-10-08 14:47 BST) moved animals off `UserManagementRead` / `UserManagementWrite`, and decision 24 (15:17 BST) made it one permission: `AnimalsWrite` on list, get, create, update, delete and `GET v1/schemas/create-animal`. S11 (was "Read-only users cannot change animals") and S13 (was "write satisfies the read policy") were rewritten in place so the numbering is unchanged.
- How API.Framework declares, registers, seeds and assigns permissions today: `plan.md` › Target stack › Permissions. Dev Bot's current `AnimalController` / `AnimalSchemaController` still use `DirectoryPolicies`.
- The API checks "before today" against the UTC date; the UI checks the browser's local date (decision 9). The gap just after midnight during BST is accepted.
- Scenario IDs frozen 2026-10-08 from current positions (S1-S13; ticket heading IDs T-ANIMAL-002/S<n> for tests; doc-only, no wording or behaviour change).
- Test data personas (2026-10-08, wording only, no behaviour change): S9 uses role personas instead of a real person's name and email: DisplayName "Animals Tester" and, for the user with no DisplayName, Email "animals-nodisplayname@e2e.test" (testing persona naming `{feature}-{role}`; the `e2e.test` domain follows the config placeholder `testing.personas.email_domain`). Both personas need `animals_write` so they can save.
