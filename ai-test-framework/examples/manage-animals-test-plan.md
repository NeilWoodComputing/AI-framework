# Example — test plan for manage-animals

Built from the real artefacts in `ai-planning-framework/work/manage-animals/` (tickets T-ANIMAL-001 to -009, `specs/manage-animals.yaml`, `specs/add-edit-animal.yaml`, `plan.md`), re-read on 08/10/2026 after Plan Bot's decision 28 (page / grid split into T-ANIMAL-008 and T-ANIMAL-003) and decision 29 (boolean icon cells, T-ANIMAL-009). Active stack: `api-framework` + `nextjs`. Illustrative only; no tests were written or run.

**Scenario IDs are explicit and frozen** (`testing.scenario_ids: explicit`; frozen by Plan Bot on 2026-10-08, re-read at 19:24 BST). Every ID below is read from a ticket heading `### Scenario: S<n> — <title>`, never from heading order. Gaps (T-ANIMAL-003 has no S1, S10 or S11) and `(was …)` notes (T-ANIMAL-008 S1–S3) are as the tickets have them. All nine tickets now carry explicit IDs, so no scenario is blocked on IDs.

| Field | Value |
|-------|-------|
| Unit test project | `Api.Framework.Tests` — approved by Neil 08/10/2026; **Waiting** until the implementing agent creates it (owner `code`) |
| E2E location | `testing.e2e.nextjs.path` (placeholder `<ai-code-framework/ui/UI.NextJs.Framework/e2e>`; does not exist yet — **Waiting**, scaffolded by the implementing agent, owner `code`) |
| Reset endpoint, batches, personas | Built by the implementing agent (`testing.ownership`); none exist yet — **Waiting**, owner `code` |
| Environment | Test UI + API.Framework (`Test`) on dedicated PostgreSQL `<api_framework_test>`; master reset once per run as `testdata-admin`. Not set up yet — first runs **Blocked** (human owner) |

## Personas

Defined and seeded by the implementing agent (`testing.ownership.test_users: code`); listed here so it knows what the scenarios need.

| Persona | Permissions | Display name | Password env var | Used by batches |
|---------|-------------|--------------|------------------|-----------------|
| `testdata-admin` | none (master reset only) | Test Data Admin | `E2E_TESTDATA_ADMIN_PASSWORD` | global setup |
| `animals-tester` | `animals_write` | Animals Tester | `E2E_ANIMALS_TESTER_PASSWORD` | all animals batches (also calls their resets) |
| `animals-tester-emailonly` | `animals_write` | none (Email fallback) | `E2E_ANIMALS_TESTER_EMAILONLY_PASSWORD` | `animals.api`, `animals.grid` |
| `animals-viewer` | none | Animals Viewer | `E2E_ANIMALS_VIEWER_PASSWORD` | permission scenarios (`animals.page`, `animals.api`, `animals.form`, `animals.delete`) |
| `animals-usermanager` | `user_management_read`, `user_management_write` | Animals User Manager | `E2E_ANIMALS_USERMANAGER_PASSWORD` | "user-management permissions alone" scenarios (`animals.page`, `animals.api`, `animals.delete`) |
| `reference-data-tester` | `user_management_read` (reference data reads) | Reference Data Tester | `E2E_REFERENCE_DATA_TESTER_PASSWORD` | `reference-data.types-grid` |

## Batches and reset keys

Every scenario's first step is one of its batch's keys. Animals is a global table with a unique Name (decision 12), so the animals batches share the Names below and **run serially**.

| Batch unit (feature file) | Keys → data (fixed GUIDs; `UpdatedBy` = a persona) | Default state (master) | Depends on | Footprint |
|---|---|---|---|---|
| `animals.page` (`ManageAnimalsPage.feature`) | `animals.page.empty`: none · `animals.page.list`: Bessie (2020-01-01) by `animals-tester` | `empty` | `personas.animals` | Its GUIDs; Name BESSIE |
| `animals.grid` (`ManageAnimalsGrid.feature`) | `animals.grid.empty` · `animals.grid.list`: Bessie (IsFurry true, Attributes ["dairy","docile"], by `animals-tester`), Ziggy (Attributes [], by `animals-tester-emailonly`), Daisy deleted · `animals.grid.last-amended-times`: Bessie `UpdatedUtc` 2026-10-08T13:05:00Z, Ziggy 2026-12-01T09:30:00Z · `animals.grid.paging-25`: 25 non-deleted animals with fixed Names that sort in a known order (for example "Paging 01" … "Paging 25") · `animals.grid.booleans`: Bessie (IsFurry true, HasHooves true), Ziggy (IsFurry false, HasHooves false) | `empty` | `personas.animals` | Its GUIDs; Names BESSIE, ZIGGY, DAISY, PAGING 01–25 |
| `animals.form` (`AddEditAnimal.feature`) | `animals.form.empty` · `animals.form.bessie-exists` · `animals.form.bessie-soft-deleted` | `empty` | `personas.animals` | Its GUIDs; Name BESSIE |
| `animals.delete` (`DeleteAnimal.feature`) | `animals.delete.empty` (master only) · `animals.delete.bessie-exists` · `animals.delete.bessie-soft-deleted` | `empty` | `personas.animals` | Its GUIDs; Name BESSIE |
| `animals.api` (`AnimalsApi.feature`, API e2e) | `animals.api.empty`: none · `animals.api.bessie-exists`: Bessie (2020-01-01) · `animals.api.bessie-soft-deleted`: Bessie, deleted · `animals.api.list`: Bessie by `animals-tester`, Ziggy by `animals-tester-emailonly`, Daisy deleted | `empty` | `personas.animals` | Its GUIDs; Names BESSIE, ZIGGY, DAISY |
| `reference-data.types-grid` (`ReferenceDataTypesGrid.feature`) | `reference-data.types-grid.baseline`: re-asserts the reference-data types the grid shows, which come from the migrations' `HasData` (recreated by `baseline.migration-seed`); Clear only reverts edits to those rows | `baseline` | `personas.reference-data`, `baseline.migration-seed` | Those seeded types only (exact rows to confirm) |

### Seed-unit order (master reset)

After `TRUNCATE` of every app table, the master runs every unit once, dependencies first, ties by key:

| # | Unit | Seeds |
|---|------|-------|
| 1 | `baseline.migration-seed` | All migration `HasData` rows from the EF model (roles, permissions, permission groups, tenants, features, catalogue items, reference-data types and items) |
| 2 | `baseline.test-tenant` | `<e2e-test-tenant>` |
| 3 | `personas.animals` | `animals-tester`, `animals-tester-emailonly`, `animals-viewer`, `animals-usermanager` |
| 4 | `personas.reference-data` | `reference-data-tester` |
| 5 | `personas.testdata` | `testdata-admin` |
| 6 | `animals.api` | `empty` |
| 7 | `animals.delete` | `empty` |
| 8 | `animals.form` | `empty` |
| 9 | `animals.grid` | `empty` |
| 10 | `animals.page` | `empty` |
| 11 | `reference-data.types-grid` | `baseline` |

A scenario's granular reset (for example `animals.grid.booleans`) uses the same `animals.grid` unit: Clear its footprint, re-assert `personas.animals`, Seed `booleans`.

## Scenarios → tests (explicit IDs)

### T-ANIMAL-001 — Animal schema / persistence

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-001/S1 | Animal table stores all mapped columns | Unit (model metadata) + covered by T-ANIMAL-002/S1 | `AnimalModel_MapsAllColumns` | — | — | Waiting (project) |
| T-ANIMAL-001/S2 | Attributes default to an empty array | Unit (model default SQL) + covered by T-ANIMAL-002/S2 | `AnimalModel_AttributesDefaultIsEmptyJsonbArray` | — | — | Waiting (project) |
| T-ANIMAL-001/S3 | Normalised name is unique among non-deleted rows | Unit (index metadata) + API e2e via T-ANIMAL-002/S3 (real PostgreSQL index) | `AnimalModel_HasFilteredUniqueNormalizedNameIndex` | `animals.api.bessie-exists` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-001/S4 | A soft-deleted animal's name can be reused | Covered by T-ANIMAL-002/S4 | `@T-ANIMAL-002/S4` | `animals.api.bessie-soft-deleted` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-001/S5 | Soft-deleted flag exists | Unit (model metadata) | `AnimalModel_IsDeletedDefaultsFalse` | — | — | Waiting (project) |
| T-ANIMAL-001/S6 | Table lives in the creatures schema | Unit (model metadata) | `AnimalModel_MapsToCreaturesSchema` | — | — | Waiting (project) |
| T-ANIMAL-001/S7 | The animals permission is seeded for our users | Unit (seed data) | `SeededGroupPermissions_LinksAnimalsWriteToAdministratorsAndStandard` | — | — | Waiting (project) |

### T-ANIMAL-002 — Animals service + v1/Animal API

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-002/S1 | Create animal with valid fields | Unit + API e2e | `Create_ValidFields_WritesTrimmedNameAndAudit` / `@T-ANIMAL-002/S1` | `animals.api.empty` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S2 | Missing Attributes are stored as an empty array | Unit + API e2e | `Create_NoAttributes_StoresEmptyArray` / `@T-ANIMAL-002/S2` | `animals.api.empty` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S3 | Duplicate name is rejected | Unit (service check + constructed unique violation) + API e2e | `Create_DuplicateNameTrimmedCaseInsensitive_FailsWithAlreadyExists` / `@T-ANIMAL-002/S3` | `animals.api.bessie-exists` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S4 | Name of a soft-deleted animal can be reused | Unit + API e2e | `Create_NameOfSoftDeletedAnimal_Succeeds` / `@T-ANIMAL-002/S4` | `animals.api.bessie-soft-deleted` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S5 | Date Born must be before today | Unit (fake clock 2026-10-08) + API e2e (today's UTC date) | `Save_DateBornTodayOrLater_FailsWithBeforeToday` / `@T-ANIMAL-002/S5` | `animals.api.empty` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S6 | Date Born is mandatory | Unit + API e2e | `Create_DateBornMissing_FailsWithDateBornRequired` / `@T-ANIMAL-002/S6` | `animals.api.empty` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S7 | Name is mandatory | Unit + API e2e | `Create_NameWhitespace_FailsWithNameRequired` / `@T-ANIMAL-002/S7` | `animals.api.empty` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S8 | Attribute tag limits | Unit + API e2e | `Save_TagOver50Chars_Fails`, `Save_Over20Tags_Fails` / `@T-ANIMAL-002/S8` | `animals.api.empty` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S9 | List returns non-deleted animals with Last Amended | Unit (mapper fallback) + API e2e | `ToListItem_NoDisplayName_UsesEmail` / `@T-ANIMAL-002/S9` | `animals.api.list` | `animals-tester` (+ seeded rows by `animals-tester-emailonly`) | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) — **flagged** (see below) |
| T-ANIMAL-002/S10 | Soft delete and not found afterwards | Unit (row kept, audit) + API e2e (404s) | `Delete_Existing_SetsIsDeletedKeepsRowAndAudits` / `@T-ANIMAL-002/S10` | `animals.api.bessie-exists` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S11 | Users without animals_write are rejected on every endpoint | API e2e (+ unit reflection test, see S13) | `@T-ANIMAL-002/S11` | `animals.api.bessie-exists` | `animals-viewer` | Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S12 | User-management permissions alone do not grant access to animals | API e2e | `@T-ANIMAL-002/S12` | `animals.api.bessie-exists` | `animals-usermanager` | Planned — Waiting (scaffolding) |
| T-ANIMAL-002/S13 | AnimalsWrite guards every animal endpoint | Unit (policy registration + reflection) + API e2e | `AllAnimalEndpoints_RequireAnimalsWritePolicy` / `@T-ANIMAL-002/S13` | `animals.api.bessie-exists` | `animals-tester` | Unit Waiting (project); API e2e Planned — Waiting (scaffolding) |

### T-ANIMAL-008 — Manage Animals page

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-008/S1 | (was T-ANIMAL-003 S1) Open Manage Animals from the nav | UI e2e | `@T-ANIMAL-008/S1` | `animals.page.empty` | `animals-tester` | Planned — Waiting (scaffolding, owner `code`) |
| T-ANIMAL-008/S2 | (was T-ANIMAL-003 S10) User without animals_write cannot open Manage Animals | UI e2e (direct to `/examples/animals` and `/examples/animals/manage/item`; observe that no `v1/Animal` request is made) | `@T-ANIMAL-008/S2` | `animals.page.list` | `animals-viewer` | Planned — Waiting (scaffolding) |
| T-ANIMAL-008/S3 | (was T-ANIMAL-003 S11) User-management permissions alone do not give access to animals | UI e2e | `@T-ANIMAL-008/S3` | `animals.page.list` | `animals-usermanager` | Planned — Waiting (scaffolding) |
| T-ANIMAL-008/S4 | Add \| Edit Animal opens as a modal over the page and closes back to it | UI e2e | `@T-ANIMAL-008/S4` | `animals.page.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-008/S5 | Opening a form URL directly shows the page with the form on top | UI e2e (direct to `/examples/animals/manage/item`) | `@T-ANIMAL-008/S5` | `animals.page.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-008/S6 | The old /manage URL redirects to the page | UI e2e (direct to `/examples/animals/manage`) | `@T-ANIMAL-008/S6` | `animals.page.empty` | `animals-tester` | Planned — Waiting (scaffolding) |

### T-ANIMAL-003 — Manage Animals paginated grid

No S1, S10 or S11: they moved to T-ANIMAL-008 (S1, S2, S3).

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-003/S2 | List shows non-deleted animals | UI e2e | `@T-ANIMAL-003/S2` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user | UI e2e | `@T-ANIMAL-003/S3` | `animals.grid.list` | `animals-tester` (DisplayName) + `animals-tester-emailonly` (Email fallback) | Planned — Waiting (scaffolding) — **flagged** (see below) |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S4` | `animals.grid.last-amended-times` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S5 | Last Amended outside summer time | UI e2e, same | `@T-ANIMAL-003/S5` | `animals.grid.last-amended-times` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S6 | Default sort by Name ascending | UI e2e | `@T-ANIMAL-003/S6` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S7 | Add opens Basic Form | UI e2e | `@T-ANIMAL-003/S7` | `animals.grid.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | UI e2e | `@T-ANIMAL-003/S8` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | UI e2e (also tagged `@T-ANIMAL-007/S1`) | `@T-ANIMAL-003/S9` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S12 | Results are paged on the server (first 20 by Name; options 5, 10, 20, 50, 100, 200; next page requests the remaining 5 from `v1/Animal`) | UI e2e (observe the real page-2 `v1/Animal` response with `waitForResponse`) | `@T-ANIMAL-003/S12` | `animals.grid.paging-25` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S13 | No animals to show ("No results"; "+ Add Animal" still available) | UI e2e | `@T-ANIMAL-003/S13` | `animals.grid.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S14 | True shows a green tick with accessible name Yes | UI e2e (also tagged `@T-ANIMAL-009/S1`) | `@T-ANIMAL-003/S14` | `animals.grid.booleans` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-003/S15 | False shows a red cross with No; cells are not interactive | UI e2e (also tagged `@T-ANIMAL-009/S2`; observe that no request is sent on click) | `@T-ANIMAL-003/S15` | `animals.grid.booleans` | `animals-tester` | Planned — Waiting (scaffolding) |

### T-ANIMAL-004 — Add | Edit Animal form

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-004/S1 | Add mode opens with defaults | UI e2e | `@T-ANIMAL-004/S1` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S2 | Create animal with required fields | UI e2e + API read-back | `@T-ANIMAL-004/S2` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S3 | Name is mandatory | UI e2e | `@T-ANIMAL-004/S3` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | UI e2e | `@T-ANIMAL-004/S4` | `animals.form.bessie-exists` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | UI e2e | `@T-ANIMAL-004/S5` | `animals.form.bessie-soft-deleted` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S6 | Date Born must be before today | UI e2e (browser local date) | `@T-ANIMAL-004/S6` | `animals.form.bessie-exists` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S7 | Date Born is mandatory | UI e2e | `@T-ANIMAL-004/S7` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | UI e2e + API read-back | `@T-ANIMAL-004/S8` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S9 | Attribute tag limits | UI e2e (also tagged `@T-ANIMAL-006/S3`) | `@T-ANIMAL-004/S9` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S10 | Edit persists changed fields | UI e2e + API read-back (Last Amended shows "my display name" = the persona's) | `@T-ANIMAL-004/S10` | `animals.form.bessie-exists` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | UI e2e (two personas) | `@T-ANIMAL-004/S11` | `animals.form.bessie-exists` | `animals-tester`, `animals-viewer` | Planned — Waiting (scaffolding) |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | UI e2e (Edit URL from reset ids) | `@T-ANIMAL-004/S12` | `animals.form.bessie-soft-deleted` | `animals-tester` | Planned — Waiting (scaffolding) |

### T-ANIMAL-005 — Soft delete Animal

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-005/S1 | Confirmation names the animal | UI e2e | `@T-ANIMAL-005/S1` | `animals.delete.bessie-exists` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | UI e2e + API 404 (storage flag: T-ANIMAL-002/S10 unit) | `@T-ANIMAL-005/S2` | `animals.delete.bessie-exists` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | UI e2e (observe no DELETE) | `@T-ANIMAL-005/S3` | `animals.delete.bessie-exists` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | UI e2e | `@T-ANIMAL-005/S4` | `animals.delete.bessie-soft-deleted` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | UI e2e + API e2e (403 for both personas) | `@T-ANIMAL-005/S5` | `animals.delete.bessie-exists` | `animals-viewer`, `animals-usermanager` | Planned — Waiting (scaffolding) |

### T-ANIMAL-006 — Shared Switch and Tag Input controls

Component-level scenarios; there is no UI component test runner, so they are proved through real pages where one exercises them.

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Not automated at component level | — | — | — | Exercised by T-ANIMAL-004/S1, S10; needs a component test runner for the generic case |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Not automated at component level | — | — | — | Exercised by T-ANIMAL-004/S8; needs a component test runner for the generic case |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Covered by T-ANIMAL-004/S9 | `@T-ANIMAL-004/S9` + `@T-ANIMAL-006/S3` | `animals.form.empty` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Not automated | — | — | — | No page renders read-only since decision 20; needs a component test runner or a harness page |
| T-ANIMAL-006/S5 | String-array grid cells | UI e2e via Manage Animals (Attributes column: Bessie ["dairy","docile"] → "dairy, docile"; Ziggy [] → empty cell) | `@T-ANIMAL-006/S5` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |

### T-ANIMAL-007 — Shared row actions menu in the grid's Actions column

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-007/S1 | Row actions menu in the last column | Covered by T-ANIMAL-003/S9 | `@T-ANIMAL-003/S9` + `@T-ANIMAL-007/S1` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | UI e2e via Manage Animals ("Ziggy" → Edit shows Ziggy) | `@T-ANIMAL-007/S2` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Not automated | — | — | — | Generic grid configuration no real page uses; needs a component test runner or a harness page |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Not automated | — | — | — | As S3 |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Not automated | — | — | — | As S3 |
| T-ANIMAL-007/S6 | Per-row visibility | Not automated | — | — | — | As S3 |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Not automated | — | — | — | As S3 |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | UI e2e on the reference-data types grid | `@T-ANIMAL-007/S8` | `reference-data.types-grid.baseline` | `reference-data-tester` | Planned — Waiting (scaffolding) (seeded rows to confirm) |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | UI e2e via Manage Animals | `@T-ANIMAL-007/S9` | `animals.grid.list` | `animals-tester` | Planned — Waiting (scaffolding) |

### T-ANIMAL-009 — Shared boolean icon grid cell

Component-level scenarios. There is no UI component test runner, so they are proved through Manage Animals where a real page exercises them, and otherwise not automated with a reason. Manage Animals is the only grid that uses either boolean renderer today (checked read-only in `UI.NextJs.Framework/src`, 08/10/2026).

| Scenario | Title (from ticket) | Layer | Test / tag | First-step key | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-009/S1 | True shows a green tick named Yes | Covered by T-ANIMAL-003/S14 | `@T-ANIMAL-003/S14` + `@T-ANIMAL-009/S1` | `animals.grid.booleans` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-009/S2 | False shows a red cross named No | Covered by T-ANIMAL-003/S15 | `@T-ANIMAL-003/S15` + `@T-ANIMAL-009/S2` | `animals.grid.booleans` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-009/S3 | Cell is not interactive (true **and** false) | UI e2e via Manage Animals (click a true and a false cell; no request, nothing opens, not focusable) | `@T-ANIMAL-009/S3` | `animals.grid.booleans` | `animals-tester` | Planned — Waiting (scaffolding) |
| T-ANIMAL-009/S4 | Labels are configurable with Yes/No defaults | Not automated | — | — | — | Defaults ("Yes" / "No") are exercised by T-ANIMAL-003/S14, S15; custom labels are used by no real page. Needs a component test runner or a harness page |
| T-ANIMAL-009/S5 | Null / undefined shows em dash named Not set | Not automated | — | — | — | No real page renders a null boolean (`IsFurry` / `HasHooves` are `bool`, default false, per T-ANIMAL-001). Needs a component test runner or a harness page |
| T-ANIMAL-009/S6 | Existing switch cell still available | Not automated (Manage Animals part via T-ANIMAL-003/S14 "neither cell is a Switch") | — | — | — | No other grid calls `renderBooleanSwitchCell`; the "still exported and renders a read-only Switch" part needs a component test runner or a harness page |

## Flags for the planning agent

**Hard-coded users.** The spec's population source for Last Amended is generic ("UpdatedBy → User.DisplayName, fallback User.Email; User = auth.users"; `specs/manage-animals.yaml`), so these scenarios are tested with role personas. The ticket wording names specific users and should be genericised:

- **T-ANIMAL-003/S3:** "a user whose DisplayName is "Neil Wood"" and "followed by "Neil Wood"". Tested with `animals-tester` (DisplayName "Animals Tester"); Email fallback with `animals-tester-emailonly` (no DisplayName; Email `animals-tester-emailonly@<e2e.test>`).
- **T-ANIMAL-002/S9:** "a user whose DisplayName is "Neil Wood"" and "a user with no DisplayName and Email "ops@example.com"". Tested with `animals-tester` and `animals-tester-emailonly` in the same way. Suggested wording: "a user with a DisplayName" / "a user with no DisplayName", asserting that user's DisplayName / Email.

No other scenario names a real person (T-ANIMAL-004/S10 says "my display name"; T-ANIMAL-003/S4, S5 say "the user's display name").

## Questions this plan raises

- For the implementing agent (owner `code`): the new batch keys `animals.page.*`, `animals.grid.paging-25` and `animals.grid.booleans`, alongside the existing ones.
- A component test runner (or harness page) for T-ANIMAL-006/S1, S2, S4, T-ANIMAL-007/S3–S7 and T-ANIMAL-009/S4–S6?
- Which seeded reference-data types `reference-data.types-grid.baseline` should assert (T-ANIMAL-007/S8).
