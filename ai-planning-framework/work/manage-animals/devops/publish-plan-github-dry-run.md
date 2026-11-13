# GitHub Publish Plan — Manage Animals (DRY-RUN)

**Generated:** 2026-11-13  
**Feature:** manage-animals  
**Target:** `tickets.github` → NeilWoodComputing/ai-framework-tests  
**Project:** AI testing  
**Mode:** DRY-RUN (no issues created)

---

## Summary

- **Total tickets:** 9
- **Stories (issues):** 9
- **Child tasks (sub-issues):** 0
- **Upsert strategy:** Search by stable ID label or title prefix `[T-ANIMAL-NNN]`

---

## Ticket: T-ANIMAL-001

**Action:** CREATE (no existing issue found with label `T-ANIMAL-001`)

**Title:** `[T-ANIMAL-001] Animal schema / persistence (Schema)`

**Labels:**
- `T-ANIMAL-001`
- `manage-animals`
- `schema`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** administrator  
**I want** an Animal table with the columns required by Manage Animals and Add | Edit Animal  
**So that** animal data can be persisted and listed reliably

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input / results | Animals | Animal (creatures.animals) | Name |
| (no control) | Persistence only | Animals | Animal (creatures.animals) | NormalizedName (derived from Name) |
| Date Born | Date Picker / results | Animals | Animal (creatures.animals) | DateBorn |
| Attributes | Tag Input / results | Animals | Animal (creatures.animals) | Attributes |
| Is Furry | Switch / results | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch / results | Animals | Animal (creatures.animals) | HasHooves |
| Last Amended | Results column | Animals | Animal (creatures.animals) | UpdatedUtc & UpdatedBy (→ User.DisplayName, fallback User.Email) |
| (soft delete) | Persistence | Animals | Animal (creatures.animals) | IsDeleted |

## Work to do

1. Add EF model `Api.Framework.Data/Models/Animal.cs` and `DbSet<Animal> Animals` on `LoginDbContext`, mapped with `ToTable("animals", "creatures")` so it lands in the new **`creatures`** schema instead of the context default (`HasDefaultSchema("auth")`); snake_case columns by convention → `creatures.animals`, key `pk_animals` (decision 21). Use a named constant for `"creatures"` rather than a magic string. Same `LoginDbContext` (Q24); EF history table stays `auth.__ef_migrations_history`.
2. Columns (global table — no tenant id):

   | Property | Column | Type / rules |
   |----------|--------|--------------|
   | `Id` | `id` | `Guid`, primary key `pk_animals` |
   | `Name` | `name` | `string`, max 100, required (stored trimmed) |
   | `NormalizedName` | `normalized_name` | `string`, max 100, required; `Name.Trim().ToUpperInvariant()` |
   | `DateBorn` | `date_born` | `DateOnly` → PostgreSQL `date`, required |
   | `Attributes` | `attributes` | JSON string array, `jsonb`, required, default `'[]'` (same as `ReferenceDataItem.Attributes`) |
   | `IsFurry` | `is_furry` | `bool`, default false |
   | `HasHooves` | `has_hooves` | `bool`, default false |
   | `IsDeleted` | `is_deleted` | `bool`, default false |
   | `CreatedUtc` | `created_utc` | `DateTimeOffset`, required |
   | `UpdatedUtc` | `updated_utc` | `DateTimeOffset`, required (Last Amended date/time) |
   | `UpdatedBy` | `updated_by` | `Guid`, required, FK to `auth.users(id)` with restrict delete (Last Amended user) — cross-schema FK from `creatures` to `auth` (Q26) |

3. Unique index on `NormalizedName` filtered to non-deleted rows: `.IsUnique().HasFilter("NOT is_deleted").HasDatabaseName("ix_animals_normalized_name_active")` (pattern: `ReferenceDataItem`'s `.HasFilter("is_active")` index).
4. Add the EF migration in `Api.Framework.Data/Migrations` (no animal seed data; it does carry the permission seed from item 6). It must start with `migrationBuilder.EnsureSchema(name: "creatures")` (EF generates this from the mapping) and create `creatures.animals` with the index and FK above. Dev Bot's existing `20261008131327_AddAnimals` (which creates `auth.animals`) is **removed and regenerated** so it creates `creatures.animals` directly (Q27: Neil has not run the API since 14:13 BST, so no database has applied it). No move migration.
5. Privileges: the API applies migrations at start-up (`Database.Migrate()`), so its DB user needs permission to create the `creatures` schema. No `GRANT` statements in the migration; the local DB user can create schemas (Q25). Never read or change connection strings, appsettings secrets or `.env` files to check this.
6. Animals permission (decisions 22, 24, 25). Add **one** permission, `Define(25, "animals_write", "Manage animals", "Animals")`, to `LoginPermissions.All` in `Api.Framework.Data/LoginPermissions.cs` (no read permission; name per Q35; category per Q34). `LoginDbContext` already seeds `auth.permissions` from that list with `HasData`, and `SeededGroupPermissions()` already links every permission to the preset **Administrators** group; add one link so the preset **Standard** group (the default tenant's `IsDefault` group) also gets `animals_write`. The migration from item 4 then gains `InsertData` for the `permissions` row and its two `permission_group_permissions` rows. No new `LoginFeatures` entry and no back-fill for other groups or tenants (Q34). Policies and controller attributes are T-ANIMAL-002.
   - **Who this reaches (decision 25):** system admins (they get every permission); every default-tenant user in Administrators or Standard, which is every self-registered user (`LoginService`: first user → Administrators, the rest → Standard) and every directory-created user saved with no groups chosen (they get the tenant's default groups). **Not reached:** default-tenant users who are only in other groups, and users of other tenants (their "<tenant> Administrators" groups are created at runtime by `TenantService` and cannot be seeded with `HasData`); they get it when it is added to their group in group management (Q34).
   - **Token refresh:** permissions are copied into the JWT `permission` claims when a token is issued (`LoginService.LoadPermissionNamesAsync` → `TokenService`). Users who are signed in when the migration runs only get `animals_write` after they **sign in again or their token is refreshed**.

## Acceptance criteria

### Scenario: S1 — Animal table stores all mapped columns

```gherkin
Given the migration has been applied
When a new Animal row is inserted with Name "Bessie", NormalizedName "BESSIE", DateBorn 2020-01-01, Attributes ["dairy","docile"], IsFurry true, HasHooves true, UpdatedUtc and UpdatedBy set
Then the Animals service can read back Animal.Name, Animal.NormalizedName, Animal.DateBorn, Animal.Attributes, Animal.IsFurry and Animal.HasHooves
And the row is stored in table creatures.animals (schema creatures, not auth) with snake_case columns (name, normalized_name, date_born, attributes, is_furry, has_hooves, is_deleted, created_utc, updated_utc, updated_by)
And Animal.Attributes is stored as a jsonb array of strings
And Animal.DateBorn is stored as a date with no time part
And Animal.IsDeleted defaults to false
And Animal.UpdatedBy references an existing auth.users row
```

### Scenario: S2 — Attributes default to an empty array

```gherkin
Given the migration has been applied
When a new Animal row is inserted without a value for Attributes
Then Animal.Attributes is stored as []
And Animal.Attributes is never null
```

### Scenario: S3 — NormalizedName is unique among non-deleted rows

```gherkin
Given an Animal with NormalizedName "BESSIE" is not deleted
When the Animals service attempts to save another Animal with Name " Bessie " or " bessie "
Then the save fails
And the unique index ix_animals_normalized_name_active prevents the duplicate
When an Animal with NormalizedName "DAISY" has been soft-deleted
And a new Animal is saved with Name "Daisy"
Then the save succeeds
And the unique index allows the duplicate NormalizedName while one is soft-deleted
```

### Scenario: S4 — A soft-deleted animal's name can be reused

```gherkin
Given the only Animal with Name "Bessie" has been soft-deleted
When a new Animal is saved with Name "Bessie" and valid DateBorn
Then the create succeeds
And the unique check excluded the soft-deleted row
```

### Scenario: S5 — UpdatedBy FK enforces referential integrity

```gherkin
Given a valid Animal row references Animal.UpdatedBy → auth.users(id)
When the auth.users row is attempted to be deleted
Then the delete is restricted (not cascaded)
And the Animal row still references a valid user id
```

### Scenario: S6 — animals_write permission is seeded

```gherkin
Given the migration has been applied
When auth.permissions is queried
Then a row exists with permission_name "animals_write", display_name "Manage animals", category "Animals"
And the permission is stable id 25
```

### Scenario: S7 — Administrators and Standard groups receive animals_write

```gherkin
Given the migration has been applied
And the default tenant has preset groups Administrators and Standard
When permission_group_permissions is queried
Then both groups are linked to permission animals_write
And self-registered users (Administrators or Standard) get animals_write in their next token
```

## Out of scope

- Seeding sample animal data
- Back-filling the permission to existing non-default tenant groups
- Granting the DB user schema creation privileges (assumed present)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-001-animal-schema.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** None

---

## Ticket: T-ANIMAL-002

**Action:** CREATE (no existing issue found with label `T-ANIMAL-002`)

**Title:** `[T-ANIMAL-002] Animals service + v1/Animal API, validation and permissions (Service API)`

**Labels:**
- `T-ANIMAL-002`
- `manage-animals`
- `service-api`
- `ai-planning-framework`

**Body:**

```markdown
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

## Acceptance criteria (summary)

- [ ] S1 — Create animal with valid fields
- [ ] S2 — Missing Attributes are stored as an empty array
- [ ] S3 — Duplicate name is rejected
- [ ] S4 — Name of a soft-deleted animal can be reused
- [ ] S5 — Date Born must be before today
- [ ] S6 — Date Born is mandatory
- [ ] S7 — Name is mandatory
- [ ] S8 — Attribute tag limits
- [ ] S9 — List returns non-deleted animals with Last Amended
- [ ] S10 — Soft delete and not found afterwards
- [ ] S11 — Users without animals_write are rejected on every endpoint
- [ ] S12 — User-management permissions alone do not grant access to animals
- [ ] S13 — AnimalsWrite guards every animal endpoint

## Out of scope

- Manage Animals grid UI (T-ANIMAL-003)
- Basic Form chrome (T-ANIMAL-004)
- Soft-delete confirmation UI (T-ANIMAL-005)
- Restore, "include deleted" listing, filtering / search, import / export

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-002-animals-service.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** T-ANIMAL-001

---

## Ticket: T-ANIMAL-003

**Action:** CREATE (no existing issue found with label `T-ANIMAL-003`)

**Title:** `[T-ANIMAL-003] Manage Animals paginated grid + row actions menu (Paginated grid)`

**Labels:**
- `T-ANIMAL-003`
- `manage-animals`
- `paginated-grid`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** administrator  
**I want** a paged, sorted Manage Animals grid with "+ Add Animal" and a row actions menu on each row  
**So that** I can find animals and add, edit or soft-delete them

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Results column | Animals | Animal (creatures.animals) | Animal.Name |
| Is Furry | Results column (boolean icon; T-ANIMAL-009) | Animals | Animal (creatures.animals) | Animal.IsFurry |
| Has Hooves | Results column (boolean icon; T-ANIMAL-009) | Animals | Animal (creatures.animals) | Animal.HasHooves |
| Date Born | Results column (DD/MM/YYYY) | Animals | Animal (creatures.animals) | Animal.DateBorn |
| Attributes | Results column | Animals | Animal (creatures.animals) | Animal.Attributes |
| Last Amended | Results column (DD/MM/YYYY HH:MM [Display name], browser local time) | Animals | Animal (creatures.animals) | Animal.UpdatedUtc & UpdatedBy → User.DisplayName (fallback User.Email) |
| + Add Animal | Primary action (`animals_write`, like the whole page) | Animals | Animal (creatures.animals) | Opens Add \| Edit Animal in Add mode |
| Actions (row actions menu: Edit Animal, Delete Animal) | Actions column, last column of the grid (decisions 23, 26) | Animals | Animal (creatures.animals) | Edit opens Basic Form in Edit mode; Delete soft-deletes (T-ANIMAL-005) |
| Paging / sort / empty state | Grid paginator; results area | Animals | Animal (creatures.animals) | Server-side paging of `v1/Animal`; page size 20, options 5, 10, 20, 50, 100, 200 (Q37, accepted); default sort Name ascending; empty state "No results" (Q37, accepted) |

## Work to do

The page that hosts this grid (route, nav link, permission gate, no-permission message, page layout, the form modal slot) is **T-ANIMAL-008** (decision 28). Old work items 1 (route and nav link), 5 (page-level permission gate and callout) and 8 (standing rule) moved there; items 2, 3, 4, 6 and 7 stay here, renumbered below.

1. Render the paginated results **inline** in the Manage Animals page from T-ANIMAL-008, per the Excel columns (`ManageAnimals`, `AnimalsGrid`, `use-animals-grid.tsx`, `columns/animals-grid-columns.tsx`, `state/animals-search.data-provider.ts` under `src/features/animals/manage-animals/`; the reference-data grid, columns and search data provider are the pattern, but not its list modal `ManageReferenceDataItemsModal`, which predates the rule), calling `v1/Animal` through `unityApiFetch` and a new entry in `src/config/api-routes.ts`. (Was item 2.)
2. Populate the grid from the Population Sources above (non-deleted only; default sort Name ascending; Attributes not sortable). (Was item 3.)
3. Display: Is Furry / Has Hooves as **boolean icon cells** via `renderBooleanIconCell` from T-ANIMAL-009 (decision 30 / Neil 20:19: filled circle in `--app-boolean-true-fill` with `Check` as a transparent cut-out + accessible "Yes" when true; filled circle in `--app-boolean-false-fill` with `Close` as a cut-out + "No" when false; not interactive, not colour-only). **Do not** use `renderBooleanSwitchCell` for these columns (decision 29). Date Born as DD/MM/YYYY; Attributes as comma-separated tags (empty array = empty cell); Last Amended as "DD/MM/YYYY HH:MM Display name", converting `UpdatedUtc` (UTC) to the browser's local time. (Was item 4; boolean display amended by decisions 29 and 30.)
4. Paging (spec `pagination`): server-side paging of `v1/Animal` (T-ANIMAL-002); page size 20 with options 5, 10, 20, 50, 100, 200, as `use-animals-grid.tsx` and the framework's `defaultPagingOptions` already do (Q37, accepted 19:00 BST). Empty state (spec `results_area.empty_state`): the EntityGrid default "No results", with "+ Add Animal" still available (Q37, accepted 19:00 BST). New in decision 28; describes the current code, no behaviour change.
5. Actions column (decisions 23, 26): keep `rowActionsDisplay: 'menu'` with the shared, permission-aware row actions menu from T-ANIMAL-007, in the last column after Last Amended. Menu items in order: **Edit Animal** (`Icon` `Edit`, opens Add | Edit Animal in Edit mode) and **Delete Animal** (`Icon` `Delete`, opens the T-ANIMAL-005 confirmation), both with `requiredPermissions: ['animals_write']` instead of building the list conditionally. Remove the View Animal item (decision 20). (Was item 6.)
6. Wire "+ Add Animal" (grid toolbar action, `animals_write`) to Add mode. Clicking a row does nothing (Q23); Edit is chosen from the row actions menu. The form opens as a modal over the page (T-ANIMAL-008). (Was item 7.)

## Acceptance criteria

(Scenarios continue; S1, S10 and S11 moved to T-ANIMAL-008)

### Scenario: S2 — List shows non-deleted animals

```gherkin
Given I am on the Manage Animals page /examples/animals
When the results area loads
Then each visible row is a non-deleted Animal via the Animals service
And Name, Is Furry, Has Hooves, Date Born, Attributes, and Last Amended match their Animal Population Sources
And Attributes display as comma-separated tags from Animal.Attributes
And soft-deleted animals are not shown and there is no option to show them
```

### Scenario: S3 — Last Amended shows date, time and user

```gherkin
Given an Animal was last saved by a user whose DisplayName is "Animals Tester"
When Manage Animals loads
Then that row's Last Amended shows Animal.UpdatedUtc as DD/MM/YYYY HH:MM in the browser's local time, followed by "Animals Tester" from Animal.UpdatedBy
And when the saving user has no DisplayName, their Email is shown instead
```

### Scenario: S4 — Last Amended is shown in the browser's local time

```gherkin
Given an Animal has Animal.UpdatedUtc = 2026-10-08T13:05:00Z
And my browser's time zone is Europe/London (BST, UTC+1)
When Manage Animals loads
Then that row's Last Amended shows "08/10/2026 14:05" followed by the user's display name
And Animal.UpdatedUtc itself is unchanged in storage (UTC)
```

### Scenario: S5 — Last Amended outside summer time

```gherkin
Given an Animal has Animal.UpdatedUtc = 2026-12-01T09:30:00Z
And my browser's time zone is Europe/London (GMT, UTC+0)
When Manage Animals loads
Then that row's Last Amended shows "01/12/2026 09:30" followed by the user's display name
```

### Scenario: S6 — Default sort by Name ascending

```gherkin
Given multiple non-deleted Animals exist
When Manage Animals loads
Then rows are sorted by Animal.Name ascending by default
```

### Scenario: S7 — Add opens Basic Form

```gherkin
Given I have permission animals_write
And I am on Manage Animals
When I click "+ Add Animal"
Then Add | Edit Animal opens in Add mode as a modal over the page
```

### Scenario: S8 — Clicking a row does nothing

```gherkin
Given I am on Manage Animals with one or more rows
When I click a row
Then the row is not selected and no modal opens and no handler runs
And I must choose Edit Animal from the row actions menu to edit
```

### Scenario: S9 — Actions column is last

```gherkin
Given the Manage Animals grid has columns Name, Is Furry, Has Hooves, Date Born, Attributes, Last Amended
When the grid renders
Then the Actions column is shown after Last Amended as the last column
And the Actions header is not sortable
```

### Scenario: S12 — Page size options

```gherkin
Given I am on Manage Animals
When the paginator renders
Then the default page size is 20
And I can choose 5, 10, 20, 50, 100 or 200 rows per page
```

### Scenario: S13 — Empty state

```gherkin
Given no non-deleted Animals exist
When Manage Animals loads
Then the results area shows "No results"
And "+ Add Animal" is still available
```

### Scenario: S14 — Is Furry / Has Hooves show boolean icons, not switches

```gherkin
Given the grid has columns Is Furry and Has Hooves
When a row renders with Animal.IsFurry true and Animal.HasHooves false
Then Is Furry shows a filled green circle with a tick cut-out (renderBooleanIconCell)
And Has Hooves shows a filled red circle with a cross cut-out
And neither is an editable Switch
```

### Scenario: S15 — Boolean icons are not interactive

```gherkin
Given a boolean icon cell is shown in the Is Furry or Has Hooves column
When I click the cell
Then no handler runs and the cell is not focusable as a control
```

## Acceptance criteria (summary)

- [ ] S2 — List shows non-deleted animals
- [ ] S3 — Last Amended shows date, time and user
- [ ] S4 — Last Amended is shown in the browser's local time
- [ ] S5 — Last Amended outside summer time
- [ ] S6 — Default sort by Name ascending
- [ ] S7 — Add opens Basic Form
- [ ] S8 — Clicking a row does nothing
- [ ] S9 — Actions column is last
- [ ] S12 — Page size options
- [ ] S13 — Empty state
- [ ] S14 — Is Furry / Has Hooves show boolean icons, not switches
- [ ] S15 — Boolean icons are not interactive

## Out of scope

- Route, nav link, page permission gate, no-permission message, page layout (T-ANIMAL-008)
- Add | Edit Animal form (T-ANIMAL-004); delete confirmation (T-ANIMAL-005)
- Shared Switch / Tag Input / boolean icon renderers (T-ANIMAL-006, T-ANIMAL-009)
- Shared row actions menu (T-ANIMAL-007)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-003-manage-animals-grid.md`

**Specs:**
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** T-ANIMAL-002 (API), T-ANIMAL-006 (form Switch / Tag Input; string-array grid cell only after decision 29), T-ANIMAL-007 (shared permission-aware row actions menu), T-ANIMAL-009 (shared boolean icon grid cell). Hosted by T-ANIMAL-008 (the page), which depends on this ticket

---

## Ticket: T-ANIMAL-004

**Action:** CREATE (no existing issue found with label `T-ANIMAL-004`)

**Title:** `[T-ANIMAL-004] Add | Edit Animal Basic Form (Form Modal)`

**Labels:**
- `T-ANIMAL-004`
- `manage-animals`
- `form-modal`
- `ui-page`
- `ai-planning-framework`

**Body:**

```markdown
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

## Acceptance criteria (summary)

- [ ] S1 — Add mode opens with defaults
- [ ] S2 — Create animal with required fields
- [ ] S3 — Name is mandatory
- [ ] S4 — Duplicate name is rejected on Save
- [ ] S5 — Name of a deleted animal can be reused
- [ ] S6 — Date Born must be before today
- [ ] S7 — Date Born is mandatory
- [ ] S8 — Attributes persist as JSON tags
- [ ] S9 — Attribute tag limits
- [ ] S10 — Edit persists changed fields
- [ ] S11 — Only Add and Edit modes exist
- [ ] S12 — Deleted animal cannot be opened

## Out of scope

- Manage Animals grid / Actions column (T-ANIMAL-003, T-ANIMAL-007)
- Soft delete confirmation (T-ANIMAL-005)
- Building the Switch and Tag Input renderers (T-ANIMAL-006)
- View mode (dropped — decision 20)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-004-add-edit-animal-form.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
```

**Depends on:** T-ANIMAL-002 (API + schema), T-ANIMAL-006 (Switch, Tag Input), T-ANIMAL-003 (entry points: "+ Add Animal", Edit Animal in the row actions menu), T-ANIMAL-008 (the Manage Animals page that hosts the form modal; decision 28)

---

## Ticket: T-ANIMAL-005

**Action:** CREATE (no existing issue found with label `T-ANIMAL-005`)

**Title:** `[T-ANIMAL-005] Soft delete Animal with confirmation (Cross-cutting)`

**Labels:**
- `T-ANIMAL-005`
- `manage-animals`
- `cross-cutting`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** administrator  
**I want** to soft-delete an animal from Manage Animals after confirmation  
**So that** the animal no longer appears in the list but is not hard-deleted

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Delete Animal | Row actions menu item in the Actions column, after Edit Animal (`animals_write`; decision 26) | Animals | Animal (creatures.animals) | Soft delete (IsDeleted = true; UpdatedUtc & UpdatedBy set) |
| Name (list exclusion) | Results column | Animals | Animal (creatures.animals) | Animal.Name (non-deleted only) |

## Work to do

1. Delete Animal is an item of each row's **actions menu** in the Manage Animals **Actions column** (the last column; decisions 23, 26), listed after Edit Animal, with `Icon` `Delete`. It needs `animals_write` (decisions 22, 24; the whole page needs it) and opens the framework `ConfirmModal` titled "Delete &lt;Name&gt;?" with Cancel and Delete buttons.
2. On Delete, call `DELETE v1/Animal/{id}`; the Animals service sets `IsDeleted = true` (no hard delete).
3. Refresh the results list so the row no longer appears. There is no "show deleted" option and no restore.

## Acceptance criteria

### Scenario: S1 — Confirmation names the animal

```gherkin
Given I have permission animals_write
And an Animal named "Bessie" is shown on Manage Animals
When I open that row's actions menu in the Actions column and choose Delete Animal
Then a confirmation modal shows "Delete Bessie?"
And it offers Cancel and Delete buttons
```

### Scenario: S2 — Soft delete removes row from the list

```gherkin
Given the confirmation "Delete Bessie?" is open
When I click Delete
Then the Animals service soft-deletes that Animal
And the row no longer appears on Manage Animals
And the Animal row remains in storage with Animal.IsDeleted = true
```

### Scenario: S3 — Cancel leaves the animal unchanged

```gherkin
Given an Animal row is shown on Manage Animals
When I choose Delete Animal from the row's actions menu and cancel the confirmation
Then no soft-delete is performed via the Animals service
And the row remains visible on Manage Animals
```

### Scenario: S4 — Deleted animal is gone everywhere but its name is free

```gherkin
Given "Bessie" has been soft-deleted
When I open "Bessie" by its id
Then the Animals service returns not found
When I add a new animal named "Bessie" with a valid Date Born
Then the save succeeds
```

### Scenario: S5 — Users without animals_write cannot delete

```gherkin
Given I am signed in without permission animals_write
When I try to open Manage Animals
Then it does not open, so Delete Animal is never offered to me
And DELETE v1/Animal/{id} is rejected with 403 Forbidden
And the same 403 applies to a user with user_management_write but not animals_write
```

## Acceptance criteria (summary)

- [ ] S1 — Confirmation names the animal
- [ ] S2 — Soft delete removes row from the list
- [ ] S3 — Cancel leaves the animal unchanged
- [ ] S4 — Deleted animal is gone everywhere but its name is free
- [ ] S5 — Users without animals_write cannot delete

## Out of scope

- Hard delete / purge
- Restoring soft-deleted animals or an "include deleted" filter (decision 2)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-005-soft-delete.md`

**Specs:**
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** T-ANIMAL-002 (`DELETE v1/Animal/{id}`), T-ANIMAL-003 (Actions column wiring), T-ANIMAL-007 (shared Actions column)

---

## Ticket: T-ANIMAL-006

**Action:** CREATE (no existing issue found with label `T-ANIMAL-006`)

**Title:** `[T-ANIMAL-006] Shared Switch and Tag Input controls for Next.js JSON Schema forms (UI framework component)`

**Labels:**
- `T-ANIMAL-006`
- `manage-animals`
- `ui-framework-component`
- `ai-planning-framework`

**Body:**

```markdown
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

## Acceptance criteria (summary)

- [ ] S1 — Switch renders and binds a boolean
- [ ] S2 — Tag Input adds and removes chips
- [ ] S3 — Tag Input shows the schema limit errors
- [ ] S4 — Read-only rendering (generic framework capability)
- [ ] S5 — String-array grid cells

## Out of scope

- Using the controls on the animal pages (T-ANIMAL-003, T-ANIMAL-004)
- Boolean icon grid cell renderer (T-ANIMAL-009; was previously the boolean half of this ticket's grid-cell work)
- Date Picker changes (Date Born uses a date-only control in T-ANIMAL-004)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-006-shared-switch-tag-input.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** None (framework component)

---

## Ticket: T-ANIMAL-007

**Action:** CREATE (no existing issue found with label `T-ANIMAL-007`)

**Title:** `[T-ANIMAL-007] Shared, permission-aware row actions menu in the grid's last Actions column (UI framework component)`

**Labels:**
- `T-ANIMAL-007`
- `manage-animals`
- `ui-framework-component`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** developer building Unity pages in UI.NextJs.Framework  
**I want** the shared entity grid to show a row actions menu in an Actions column at the end of the grid, listing only the items the signed-in user is allowed to run  
**So that** Manage Animals (and future grids) get Edit / Delete menus without feature-local grid code or hand-built permission checks

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Actions (column header) | Shared grid column, last column | — (UI framework only) | — | — (no data; one row actions menu per row) |
| Edit Animal (first consumer) | Row actions menu item | Animals (through T-ANIMAL-003) | Animal (creatures.animals) | Opens Add \| Edit Animal in Edit mode |
| Delete Animal (first consumer) | Row actions menu item | Animals (through T-ANIMAL-005) | Animal (creatures.animals) | Soft delete (IsDeleted) after confirmation |

## Work to do

1. **Keep and formalise the `menu` display** (decision 26): `rowActionsDisplay: 'menu'` and `EntityGridRowActionsMenu.tsx` stay as the shared row actions menu, documented as a framework option. `buttons` stays the default.
2. **Permission-aware items** (`grid/grid-column.ts`), per Q32: add `requiredPermissions?: readonly string[]` to `GridRowAction` (the item is shown when the session has **any** of them; omitted = no permission needed) and an optional `isVisible?: (item) => boolean` per-row rule. Add one small exported helper (e.g. `hasAnyPermission(permissions, required)`) so pages and the grid use the same rule; the grid reads `session.permissions` through `useAuth()`. This applies to `buttons` too, so text-button grids can opt in; grids that do not set it behave as today.
3. **Rendering** (`components/entity-grid/EntityGrid.tsx`, `EntityGridRowActionsMenu.tsx`, `EntityGrid.module.css`):
   - The Actions column is always the **last** column, after every data column; header "Actions"; not sortable; no fixed width.
   - Items the user lacks permission for are **hidden**, not disabled (Q32).
   - If no item is permitted for the current user, do not render the Actions column at all.
   - Per row, also hide items whose `isVisible(row)` is false; a row with no visible items shows no menu trigger (an empty cell).
   - Items appear in configured order with their optional icon and label (Edit Animal, Delete Animal for Manage Animals).
   - Choosing an item calls `execute(row)` for that row only, closes the menu, and does not bubble to the row.
   - Keep the current trigger (an "Actions" text button) and close behaviour (Escape, click outside, after choosing). No arrow-key navigation is added (Q32).
4. **Row click** (Q23): no row-click option is added; clicking a row does nothing.
5. **Existing grids:** the reference-data grids (`buttons`, no `requiredPermissions`) render exactly as before.
6. Keep it generic: no animal-specific code in `src/framework/`. Manage Animals is wired to it in T-ANIMAL-003 (Edit Animal) and T-ANIMAL-005 (Delete Animal).

## Acceptance criteria

(Selected key scenarios; full scenarios in ticket)

### Scenario: S1 — Row actions menu in the last column

```gherkin
Given a grid configured with data columns "Name" and "Last Amended" and rowActionsDisplay "menu"
And row actions "Edit Animal" (icon Edit) and "Delete Animal" (icon Delete) with no required permissions
When the grid renders two rows
Then the last column header is "Actions", after "Last Amended", and it is not sortable
And each row's Actions cell shows one "Actions" menu trigger
When I open the first row's menu
Then it lists "Edit Animal" then "Delete Animal", each with its icon
```

### Scenario: S2 — Choosing an item runs it for that row

```gherkin
Given the grid above shows rows "Bessie" and "Ziggy"
When I open the "Ziggy" row's menu and choose "Edit Animal"
Then the Edit Animal action is executed once with the "Ziggy" row
And no action is executed for "Bessie"
And the menu closes
And no row-level click handler runs
```

### Scenario: S3 — Items are hidden without the required permission

```gherkin
Given row actions "Edit Animal" and "Delete Animal" that each require permission "animals_write"
And row action "Open" with no required permission
And I am signed in without "animals_write"
When I open a row's menu
Then it lists only "Open"
And no disabled "Edit Animal" or "Delete Animal" items are shown
```

### Scenario: S5 — No Actions column when no item is allowed

```gherkin
Given row actions all require permission "animals_write"
And I am signed in without "animals_write"
When the grid renders
Then there is no Actions column
```

## Acceptance criteria (summary)

- [ ] S1 — Row actions menu in the last column
- [ ] S2 — Choosing an item runs it for that row
- [ ] S3 — Items are hidden without the required permission
- [ ] S4 — Any one of several permissions is enough
- [ ] S5 — No Actions column when no item is allowed
- [ ] S6 — Per-row visibility with isVisible
- [ ] S7 — Empty cell when no items visible for that row
- [ ] S8 — Existing grids unchanged

## Out of scope

- Wiring the menu on Manage Animals (T-ANIMAL-003, T-ANIMAL-005)
- Arrow-key navigation in the menu
- Row click handlers

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-007-shared-grid-actions-column.md`

**Specs:**
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** None (framework component)

---

## Ticket: T-ANIMAL-008

**Action:** CREATE (no existing issue found with label `T-ANIMAL-008`)

**Title:** `[T-ANIMAL-008] Manage Animals page (route, nav link, permission gate, layout) (Page)`

**Labels:**
- `T-ANIMAL-008`
- `manage-animals`
- `page`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** administrator with animals_write  
**I want** a Manage Animals page at /examples/animals, reached from an "Animals" link in the site navigation  
**So that** I can open the animal catalogue directly, and people without access are told so instead of seeing it

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Animals (nav link) | `SiteNav` link to `/examples/animals`, shown only with `animals_write` | — (UI only) | — | — |
| Manage Animals (H1) / "Animal catalogue" (sub-text) | Page heading on route `/examples/animals` | — (UI only) | — | — |
| Search / filters | None (out of scope; spec `search_filters: []`) | — | — | — |
| Results area | Hosts the paginated grid from T-ANIMAL-003 | Animals | Animal (creatures.animals) | See T-ANIMAL-003 |
| Add \| Edit Animal | Routed form modal over this page (`@modal` slot) | Animals | Animal (creatures.animals) | See T-ANIMAL-004 |
| "You do not have permission to manage animals." | Warning callout in place of the grid | — (UI only) | — | — |

## Work to do

1. The `/examples/animals` route **is the Manage Animals page** (decision 27): `src/app/examples/animals/page.tsx` renders `ManageAnimalsPage` (`src/features/animals/manage-animals/ManageAnimalsPage.tsx`: `PageLayout` with `SiteNav`, H1 "Manage Animals", sub-text "Animal catalogue", then `ManageAnimals` inline, which renders the T-ANIMAL-003 grid). No list modal, no landing page, no auto-open, no `?manage=closed`. (Was T-ANIMAL-003 item 1.)
2. Form modal hosting: `layout.tsx` has an `@modal` slot used **only** for the Add | Edit form (`@modal/(.)manage/item`, `@modal/(.)manage/item/[id]`); the full-page fallbacks `manage/item` and `manage/item/[id]` render the list page plus the form modal; the form closes back to `/examples/animals`; the old `manage/page.tsx` URL redirects to `/examples/animals`. (Was T-ANIMAL-003 item 1.)
3. Nav link: add an "Animals" link in `src/shell/components/SiteNav.tsx` next to "Reference data", shown only when `session.permissions` contains `animals_write` (decisions 19, 24; the first permission check in `SiteNav`). (Was T-ANIMAL-003 item 1.)
4. Page permission gate with the single animals permission `animals_write` (decisions 22, 24): replace the `user_management_*` checks in `src/features/animals/shared/utils/animal-permissions.ts`. The **whole page** needs `animals_write`: without it there is no nav link, the grid is not mounted, no API call is made, and the form URLs mount no form. `AnimalsAccessNotice` (`src/features/animals/shared/components/AnimalsAccessNotice.tsx`) shows a warning `Callout` "You do not have permission to manage animals." in place of the grid (signed-out users get the `EntityGridAuthGate` sign-in prompt). There is no read-only view and no View action (decisions 20, 24). Users who have just been given `animals_write` see the page after signing in again or refreshing their token. (Was T-ANIMAL-003 item 5.)
5. Page layout and search area: no on-page search or filters (out of scope; spec `search_filters: []`). The grid's search state stays in memory, as built for modal grids (no URL query); that is not a change in this plan.
6. Standing rule (decision 27): a routed list page shows its list on the page; modals only for the Add | Edit form and the delete confirmation. Follow UI.NextJs.Framework `.cursor/rules/framework/nextjs-list-pages.mdc` and `nextjs-modal-routing.mdc` for the form. (Was T-ANIMAL-003 item 8.)

## Acceptance criteria

### Scenario: S1 (was T-ANIMAL-003 S1) — Open Manage Animals from the nav (decisions 24, 27)

```gherkin
Given I am signed in with permission animals_write
When I click "Animals" in the site navigation
Then the /examples/animals page opens with the heading "Manage Animals"
And the results grid and "+ Add Animal" are shown on the page
And no modal is open
```

### Scenario: S2 (was T-ANIMAL-003 S10) — User without animals_write cannot open Manage Animals

```gherkin
Given I am signed in without permission animals_write
When I look at the site navigation
Then the "Animals" link is not shown
When I go to /examples/animals or /examples/animals/manage/item directly
Then no animals list or form is shown and no request is made to v1/Animal
And a warning callout says "You do not have permission to manage animals."
And no animal rows, "+ Add Animal" or row actions are shown
```

### Scenario: S3 (was T-ANIMAL-003 S11) — User-management permissions alone do not give access to animals

```gherkin
Given I am signed in with permissions user_management_read and user_management_write but not animals_write
When I look at the site navigation
Then the "Animals" link is not shown
When I go to /examples/animals directly
Then no animals list is shown
```

### Scenario: S4 — Add | Edit Animal opens as a modal over the page and closes back to it (decision 27)

```gherkin
Given I have permission animals_write
And I am on the Manage Animals page /examples/animals
When I click "+ Add Animal"
Then Add | Edit Animal opens as a modal over the page
And the Manage Animals heading and grid stay on the page behind it
When I close the form without saving
Then the modal closes and I am on /examples/animals with the grid shown
```

### Scenario: S5 — Opening a form URL directly shows the page with the form on top (decision 27)

```gherkin
Given I have permission animals_write
When I go to /examples/animals/manage/item directly
Then the Manage Animals page with its grid is shown
And Add | Edit Animal is open in Add mode as a modal over it
```

### Scenario: S6 — The old /manage URL redirects to the page (decision 27)

```gherkin
Given I have permission animals_write
When I go to /examples/animals/manage
Then I am redirected to /examples/animals
And the grid is shown on the page with no modal open
```

## Acceptance criteria (summary)

- [ ] S1 — Open Manage Animals from the nav
- [ ] S2 — User without animals_write cannot open Manage Animals
- [ ] S3 — User-management permissions alone do not give access to animals
- [ ] S4 — Add | Edit Animal opens as a modal over the page and closes back to it
- [ ] S5 — Opening a form URL directly shows the page with the form on top
- [ ] S6 — The old /manage URL redirects to the page

## Out of scope

- Grid columns, population, sorting, paging, the row actions menu and the empty state (T-ANIMAL-003)
- Add | Edit Animal form fields and validation (T-ANIMAL-004); delete confirmation (T-ANIMAL-005)
- Filtering or searching the grid; import / export
- View Animal action / View mode (dropped — decision 20)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-008-manage-animals-page.md`

**Specs:**
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
```

**Depends on:** T-ANIMAL-003 (the paginated grid this page hosts), T-ANIMAL-004 (the Add \| Edit Animal form modal it hosts)

---

## Ticket: T-ANIMAL-009

**Action:** CREATE (no existing issue found with label `T-ANIMAL-009`)

**Title:** `[T-ANIMAL-009] Shared boolean icon grid cell renderer (UI framework component)`

**Labels:**
- `T-ANIMAL-009`
- `manage-animals`
- `ui-framework-component`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** developer building Unity grids in UI.NextJs.Framework  
**I want** a shared read-only boolean cell that shows a filled green circle with a tick cut-out or a filled red circle with a cross cut-out (the row colour shows through, readable in light and dark mode) with an accessible Yes/No name  
**So that** Manage Animals (and any future grid) can show booleans without looking like editable Switches

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Is Furry (grid) | Boolean icon cell (`renderBooleanIconCell`) | Animals | Animal (creatures.animals) | Animal.IsFurry |
| Has Hooves (grid) | Boolean icon cell (`renderBooleanIconCell`) | Animals | Animal (creatures.animals) | Animal.HasHooves |

## Work to do

1. In `src/framework/design-system/components/icon/Icon.tsx`, add Material icon paths for **`Check`** (tick) and **`Close`** (cross) to `ICON_PATHS` / `IconName`, same style as `Edit` / `Delete`. Do not invent other names.
2. In `src/framework/entity-framework/grid/grid-cell-renderers.tsx`, add **`renderBooleanIconCell`** next to `renderBooleanSwitchCell`. Suggested signature: `(value: boolean | null | undefined, options?: { trueLabel?: string; falseLabel?: string; nullLabel?: string; tid?: string; size?: number | string }) => ReactNode`. Defaults: `trueLabel = 'Yes'`, `falseLabel = 'No'`, `nullLabel = 'Not set'` (Q38, accepted 19:14 BST).
3. *(Amended by decision 30, Neil 19:57; cut-out amendment Neil 20:19.)* True → a **filled circle** in `var(--app-boolean-true-fill)` with Material `Check` as a **transparent cut-out** (the row / hover colour shows through the tick); false → a filled circle in `var(--app-boolean-false-fill)` with Material `Close` as a cut-out; null / undefined → em dash (`—`) only (no circle) in the theme text colour (`var(--app-text-primary)`), with accessible name from `nullLabel` (Q38, accepted 19:14 BST: default "Not set"). Build with `<Icon name="Check" | "Close" knockout="circle" />` (one evenodd SVG path: filled circle with the tick / cross punched out). Do **not** draw a separate coloured glyph on top of or behind the circle, and do **not** keep `--app-boolean-glyph`. Wrap in a non-interactive element with `aria-label` matching the label; no `onClick`, not a button/link, not in the tab order as a control (`tabIndex` unset / not focusable).
4. Keep **`renderBooleanSwitchCell`** exported and unchanged for other grids that still want a read-only switch.
5. Export `renderBooleanIconCell` from `@entity-framework` (`src/framework/entity-framework/index.ts`).
6. Suggested icon size for grid cells: smaller than the Icon default `1.8rem` (e.g. `1.6rem` or `20px`) so the cell matches other grid content — confirm with Neil only if it looks wrong; otherwise use `1.6rem`. *(Decision 30 / 20:19: `1.6rem` is the circle's diameter; the cut-out tick / cross sits inside it.)*
7. *(New, decision 30; amended Neil 20:19.)* In `src/framework/design-system/theme/tokens.css` add dedicated tokens on `:root` — `--app-boolean-true-fill: #609b44`, `--app-boolean-false-fill: #ef5673` — and dark overrides in the existing `html[data-theme='dark']` block — `--app-boolean-true-fill: #8dc374`, `--app-boolean-false-fill: #ff9aa8` (may be `var(--app-form-error-text)`). Do **not** add `--app-boolean-glyph` (Neil 20:19: the glyph is a cut-out, not a colour). Leave `--system-green` / `--system-red` and every other existing token unchanged. The renderer uses only the fill tokens (no hard-coded hex).

## Acceptance criteria

(Selected key scenarios; full scenarios in ticket)

### Scenario: S1 — True shows a green circle with a tick, named Yes

```gherkin
Given a grid column that uses renderBooleanIconCell
And a row whose bound boolean is true
When the cell renders
Then it shows a filled circle coloured var(--app-boolean-true-fill)
And the design-system Icon named Check is a transparent cut-out of that circle (Icon knockout="circle"; the row colour shows through the tick)
And the cell has an accessible name "Yes" (not colour-only)
And the cell is not a switch
```

### Scenario: S2 — False shows a red circle with a cross, named No

```gherkin
Given a grid column that uses renderBooleanIconCell
And a row whose bound boolean is false
When the cell renders
Then it shows a filled circle coloured var(--app-boolean-false-fill)
And the design-system Icon named Close is a transparent cut-out of that circle (Icon knockout="circle"; the row colour shows through the cross)
And the cell has an accessible name "No" (not colour-only)
```

### Scenario: S5 — Null / undefined shows em dash named Not set

```gherkin
Given a grid column that uses renderBooleanIconCell
And a row whose bound value is null or undefined
When the cell renders
Then it shows an em dash "—" (not a Check or Close icon, and no circle)
And the em dash uses the theme text colour var(--app-text-primary)
And the cell has an accessible name "Not set"
And it is not colour-coded as success or error
```

## Acceptance criteria (summary)

- [ ] S1 — True shows a green circle with a tick, named Yes
- [ ] S2 — False shows a red circle with a cross, named No
- [ ] S3 — Cell is not interactive
- [ ] S4 — Labels are configurable with Yes/No defaults
- [ ] S5 — Null / undefined shows em dash named Not set
- [ ] S6 — Existing switch cell still available
- [ ] S7 — Circle fills meet contrast in light and dark mode
- [ ] S8 — Dedicated tokens leave system buttons and callouts unchanged

## Out of scope

- Wiring Is Furry / Has Hooves on Manage Animals to the new renderer (T-ANIMAL-003)
- Form Switch / Tag Input controls (T-ANIMAL-006)
- Changing existing token values, including `--system-green` / `--system-red` (decision 30 only adds new boolean tokens)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-009-shared-boolean-icon-grid-cell.md`

**Specs:**
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Depends on:** Design-system `Icon` and theme tokens (adds `Check` / `Close` to `Icon` if missing; adds the decision 30 boolean tokens to `tokens.css`). Used by T-ANIMAL-003

---

## Summary of Upsert Decisions

| Ticket ID | Action | Reason |
|-----------|--------|--------|
| T-ANIMAL-001 | CREATE | No existing issue with label `T-ANIMAL-001` or title prefix `[T-ANIMAL-001]` |
| T-ANIMAL-002 | CREATE | No existing issue with label `T-ANIMAL-002` or title prefix `[T-ANIMAL-002]` |
| T-ANIMAL-003 | CREATE | No existing issue with label `T-ANIMAL-003` or title prefix `[T-ANIMAL-003]` |
| T-ANIMAL-004 | CREATE | No existing issue with label `T-ANIMAL-004` or title prefix `[T-ANIMAL-004]` |
| T-ANIMAL-005 | CREATE | No existing issue with label `T-ANIMAL-005` or title prefix `[T-ANIMAL-005]` |
| T-ANIMAL-006 | CREATE | No existing issue with label `T-ANIMAL-006` or title prefix `[T-ANIMAL-006]` |
| T-ANIMAL-007 | CREATE | No existing issue with label `T-ANIMAL-007` or title prefix `[T-ANIMAL-007]` |
| T-ANIMAL-008 | CREATE | No existing issue with label `T-ANIMAL-008` or title prefix `[T-ANIMAL-008]` |
| T-ANIMAL-009 | CREATE | No existing issue with label `T-ANIMAL-009` or title prefix `[T-ANIMAL-009]` |

---

## Notes

- **DRY-RUN MODE:** No actual GitHub issues created
- **Project board:** Issues would be automatically added to project "AI testing"
- **Acceptance criteria:** Each issue body includes:
  1. Full Given/When/Then scenarios as written in the ticket
  2. An "Acceptance criteria (summary)" section with checkable bullets
- **Labels:** All issues include `ai-planning-framework`, stable ID, feature slug, and page type labels
- **Source footer:** Each issue body includes source ticket path and links to specs/excel files in the AI-framework repository
- **Sub-issues:** None of the manage-animals tickets are explicitly typed as child tasks, so all are created as standalone issues. Dependencies are documented in the issue bodies and in the "Depends on" notes above.
- **Dependencies:** The "Depends on" fields indicate dependency relationships but do not trigger sub-issue creation, as specified in the adapter documentation

---

## GitHub API Operations (would be performed)

1. **Search for existing issues:**
   - Query: `repo:NeilWoodComputing/ai-framework-tests label:T-ANIMAL-001` OR `repo:NeilWoodComputing/ai-framework-tests "[T-ANIMAL-001]" in:title`
   - (Repeat for each ticket ID)

2. **Create new issues:**
   - POST `/repos/NeilWoodComputing/ai-framework-tests/issues`
   - Body: title, body (markdown), labels array

3. **Add to project:**
   - Add each created issue to project "AI testing" via GraphQL API

4. **Record in handoff.md:**
   - Each issue number would be recorded as `devops_work_item_id` in the feature's handoff.md
   - Issue URLs would be recorded in `devops.board_url`

---

**End of dry-run publish plan**
