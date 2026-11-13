# Ticket: T-ANIMAL-001 — Animal schema / persistence

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-001 |
| Type | Schema |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/add-edit-animal.yaml`, `excel/add-edit-animal.xlsx`, `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Decisions | `plan.md` › Decisions 3, 5, 6, 7, 8, 10, 12, 18, 21 (DB schema `creatures`), 22 / 24 (one animals permission, `animals_write`), 25 (seed it to the Administrators and Standard groups) |
| Open questions | None. Q24 (registration / history table), Q25 (privileges), Q26 (cross-schema FK), Q27 (`AddAnimals` migration), Q34 (users outside the seeded groups) and Q35 (`animals_write`): Neil accepted the suggested defaults for all remaining questions at 2026-10-08 15:44 BST |

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

### Scenario: S3 — Normalised name is unique among non-deleted rows

```gherkin
Given a non-deleted Animal exists with NormalizedName "BESSIE"
When another non-deleted Animal row with NormalizedName "BESSIE" is inserted
Then the database rejects the insert with a unique-constraint violation on ix_animals_normalized_name_active
```

### Scenario: S4 — A soft-deleted animal's name can be reused

```gherkin
Given an Animal with NormalizedName "BESSIE" has IsDeleted = true
When a new non-deleted Animal row with NormalizedName "BESSIE" is inserted
Then the insert succeeds
And both rows remain in creatures.animals
```

### Scenario: S5 — Soft-deleted flag exists

```gherkin
Given an Animal row exists
When IsDeleted is set to true for that row
Then the row remains in storage
And list and get queries for non-deleted animals exclude it
```

### Scenario: S6 — Table lives in the creatures schema

```gherkin
Given an empty database
When the API starts and applies its migrations
Then schema creatures exists
And table creatures.animals exists with primary key pk_animals and index ix_animals_normalized_name_active
And there is no table auth.animals
And the EF migrations history is recorded in auth.__ef_migrations_history
```

### Scenario: S7 — The animals permission is seeded for our users

```gherkin
Given an empty database
When the API starts and applies its migrations
Then auth.permissions contains "animals_write" with display name "Manage animals" and category "Animals"
And it is the only permission in category "Animals" (no read permission)
And the preset Administrators group has "animals_write"
And the preset Standard group has "animals_write"
And no feature in auth.features grants the "Animals" category
When an existing Standard-group user signs in again
Then their token contains the permission claim "animals_write"
```

Checklist (derived from scenarios):

- [ ] All Target DB Columns from the specs exist on `creatures.animals`, plus `NormalizedName`, `UpdatedBy`, `Id`, `CreatedUtc`
- [ ] Schema `creatures` created by the migration (`EnsureSchema`); no animals table left in `auth`
- [ ] `attributes` is `jsonb` NOT NULL default `'[]'`; `date_born` is `date`
- [ ] Filtered unique index on `normalized_name` (`NOT is_deleted`)
- [ ] `updated_by` FK to `auth.users` (cross-schema; Q26)
- [ ] Migration added; no tenant column
- [ ] `animals_write` (only) in `LoginPermissions.All`, seeded and linked to Administrators and Standard (decision 25); no read permission

## Out of scope

- UI forms and manage grid (later tickets)
- Animals service validation rules beyond schema support (see T-ANIMAL-002)
- Tenant scoping (animals are global)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-001`
- `NormalizedName` and `UpdatedBy` are not shown on any page; they come from decisions 7 and 5 in `plan.md`.
- Decision 21 (Neil, 2026-10-08 14:35 BST): new `creatures` schema; only the schema grouping changes. Entity, property, table, column, index and API names are unchanged. See `plan.md` › Target stack › DB schema `creatures` for how API.Framework assigns schemas today.
- Code built before decision 21 still uses `auth.animals`; Dev Bot changes it after the updated plan is re-approved.
- Decision 22 (Neil, 2026-10-08 14:47 BST): animals get their own permission; decisions 24–25 (Neil, 15:17 BST): one permission `animals_write`, given to our users through the Administrators and Standard groups. The permission row lives in `Api.Framework.Data`, so its seed belongs to this ticket's migration; the policy and `[Authorize]` changes are in T-ANIMAL-002. Users see it after signing in again or refreshing their token. See `plan.md` › Target stack › Permissions.
- Scenario IDs frozen 2026-10-08 from current positions (S1-S7; ticket heading IDs T-ANIMAL-001/S<n> for tests; doc-only, no wording or behaviour change).
