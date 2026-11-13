# Test plan — manage-animals

| Field | Value |
|-------|-------|
| Feature folder | `ai-planning-framework/work/manage-animals/` |
| Tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-008, T-ANIMAL-009 |
| Specs | `specs/manage-animals.yaml`, `specs/add-edit-animal.yaml` |
| Active API / UI | api-framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Unit test project | `Api.Framework.Tests` (`ai-code-framework/api/API.Framework/Api.Framework.Tests`) — **on disk** and in `Api.Framework.sln` (4th project), checked read-only 2026-10-08 20:06 BST. Dev Bot reports 21/21 scaffold tests green (Release); not re-run by Test Bot |
| E2E location | `testing.e2e.nextjs.path` = `ai-code-framework/ui/UI.NextJs.Framework/e2e` (config placeholder replaced) — **on disk**: `playwright.config.ts`, `global-setup.ts`, `package.json` (Playwright + playwright-bdd), `helpers/`, `support/personas.ts`, `features/common/` (fixtures, reset step), `scripts/reset-master.ts`, `README.md`. No `.feature` files yet (Test Bot writes them) |
| Component harness | `testing.component.nextjs.path` = `ai-code-framework/ui/UI.NextJs.Framework/src/app/examples/test-harness` (`page.tsx` → `src/features/test-harness/ComponentTestHarness.tsx`) — **on disk**. Route `/examples/test-harness`, exercised by Playwright + playwright-bdd in the e2e stack (not Vitest). Neil chose the harness at 20:04 BST; Dev Bot built it |
| Reset endpoint, batches, personas | **On disk** (Dev Bot, History rows 38 / 40): `Api.Framework/Controllers/V1/TestData/TestDataController.cs` (`v1/TestData`), batch classes under `Api.Framework.Services/TestData/`, personas in `Api.Framework.Services/TestData/Personas/AnimalsPersonasUnit.cs`. Not exercised yet (needs the Test environment) |
| Environment | See **Target environment (local run)** below. `api_framework_test` created + migrated (Dev Bot / Neil, 9 Oct ~00:50); safety gate passed every run (Database=`api_framework_test`, `localhost:5432`) |
| Scenario IDs | Explicit (`testing.scenario_ids: explicit`), read from `### Scenario: S<n> - <title>` headings, **re-read 2026-10-08 20:06 BST** (ticket files T-002, T-003, T-009 last written 20:00:24 BST; others 19:23:53 or earlier). Dev Bot's Decision 30 hand-off was still finishing at the re-read, so tickets may still move. **77 scenarios** (was 75; T-ANIMAL-009 S7 and S8 added) |
| Written by | test-bot · 2026-10-09 09:26 BST · **round 3 = test-fix round 1 of 5** (Review Bot test review F-41–F-47): unit 52/52 pass; e2e + harness 66/66 pass (run 9) + 6 setup sign-ins; 76 Pass, T-007/S8 not run · **Addendum 2 (09:56 BST): T-007/S8 unblocked (Neil 09:46) and passes; e2e 67/67 + 6 setup (run 11); all 77 Pass; status passed** · report `tests/TEST-manage-animals-3-report.md` |

## Target environment (local run)

Neil (19:52 BST, via Review Bot): run the whole suite locally on his PC.

| Item | Value | Status |
|---|---|---|
| UI | Next.js UI.NextJs.Framework on `http://localhost:3003` (`BASE_URL` default). `.env.local` still points at the dev API (:7088); Test runs use **`npm run dev:test`** (Dev Bot, 9 Oct 09:08: process env `NEXT_PUBLIC_UNITY_API_ROOT=https://localhost:7188/v1/`, build dir `.next-test`, no file edited) | Running (restarted by test-bot 9 Oct 09:10 BST with `npm run dev:test`) |
| API | API.Framework, launch profile **Test** (`ASPNETCORE_ENVIRONMENT=Test`), `http://localhost:5188` / `https://localhost:7188`, routes under `/v1` (`API_URL=http://localhost:5188/v1`) | Running (restarted by test-bot 9 Oct 09:10 BST on Dev Bot's 09:08 code, user env) |
| Database | PostgreSQL in Docker on `localhost:5432`, **separate test database `api_framework_test`** on the same server, migrations applied to it only | Ready (8 migrations); safety gate confirmed before every run |
| Safety | The master reset **TRUNCATEs every table**. Never run Test / reset against the dev database (`unity_login`, Development settings). `TestData:RequiredDatabase` = `api_framework_test`; the reset endpoint refuses any other database | Rule for every run |
| Secrets (env var names only; agents never open `.env*`) | `E2E_TEST_DATA_KEY`, `E2E_TESTDATA_ADMIN_PASSWORD`, `E2E_ANIMALS_TESTER_PASSWORD`, `E2E_ANIMALS_NODISPLAYNAME_PASSWORD` (see Personas), `E2E_ANIMALS_VIEWER_PASSWORD`, `E2E_ANIMALS_USERMANAGER_PASSWORD`, `E2E_REFERENCE_DATA_TESTER_PASSWORD` | Set as Windows user env vars (~00:50 BST 9 Oct); loaded into fresh processes without echoing values |
| Persona email domain / tenant | `e2e.test` (`support/personas.ts` default, `E2E_PERSONA_EMAIL_DOMAIN` override). Config `testing.personas.email_domain` / `tenant` are still `<placeholders>` (config not edited by Test Bot) | Neil to confirm |

Before every run Test Bot re-checks the safety gate (database name and host only); nothing runs against an unconfirmed database.

## Personas

Seeded by the implementing agent (`testing.ownership.test_users: code`). Emails `<persona>@e2e.test`; password env var `E2E_{PERSONA}_PASSWORD` (`support/personas.ts`).

| Persona | Permissions | Display name | Password env var | Used by batches | Seeded? |
|---------|-------------|--------------|------------------|-----------------|---------|
| `testdata-admin` | none (master reset only) | Test Data Admin | `E2E_TESTDATA_ADMIN_PASSWORD` | global setup | Yes |
| `animals-tester` | `animals_write` | **Animals Tester** (T-ANIMAL-002/S9, T-ANIMAL-003/S3) | `E2E_ANIMALS_TESTER_PASSWORD` | all animals batches (also calls their resets) | Yes |
| `animals-nodisplayname` | `animals_write` | none — Email `animals-nodisplayname@e2e.test` shown as fallback (T-ANIMAL-002/S9, T-ANIMAL-003/S3) | `E2E_ANIMALS_NODISPLAYNAME_PASSWORD` | `animals.api`, `animals.grid` | **Yes** (Dev Bot renamed/replaced emailonly; verified 20:15 BST) |
| ~~`animals-tester-emailonly`~~ | — | — | — | superseded by `animals-nodisplayname` | Replaced |
| `animals-viewer` | none | Animals Viewer | `E2E_ANIMALS_VIEWER_PASSWORD` | `animals.api`, `animals.form`, `animals.delete`, `animals.page`, `animals.grid` (T-ANIMAL-009/S8 callout) | Yes |
| `animals-usermanager` | `user_management_read`, `user_management_write` | Animals User Manager | `E2E_ANIMALS_USERMANAGER_PASSWORD` | `animals.api`, `animals.delete`, `animals.page` | Yes |
| `reference-data-tester` | `user_management_read` (reference data reads) | Reference Data Tester | `E2E_REFERENCE_DATA_TESTER_PASSWORD` | `reference-data.types-grid` | Yes |

## Batches and reset keys

Every e2e scenario's first step is one of its batch's keys. Animals is a global table with a unique Name (decision 12), so the animals batches share Names and **run serially**. All keys below are listed as implemented in `e2e/README.md` (Dev Bot); not yet exercised.

| Batch unit (feature file) | Keys (`{feature}.{batch}.{state}`) → data | Default state (master) | Depends on | Footprint | Serial with | Exists? |
|---|---|---|---|---|---|---|
| `animals.page` (`ManageAnimalsPage.feature`) | `animals.page.empty`: none · `animals.page.list`: Bessie (2020-01-01) by `animals-tester` | `empty` | `personas.animals` | Its GUIDs; Name BESSIE | all animals batches | Yes (not exercised) |
| `animals.grid` (`ManageAnimalsGrid.feature`) | `animals.grid.empty` · `animals.grid.list`: Bessie (IsFurry true, Attributes ["dairy","docile"], by `animals-tester`), Ziggy (Attributes [], by `animals-nodisplayname`), Daisy deleted · `animals.grid.last-amended-times`: Bessie `UpdatedUtc` 2026-10-08T13:05:00Z, Ziggy 2026-12-01T09:30:00Z · `animals.grid.paging-25`: 25 non-deleted animals "Paging 01"…"Paging 25" · `animals.grid.booleans`: Bessie (IsFurry true, HasHooves true), Ziggy (false, false) | `empty` | `personas.animals` | Its GUIDs; Names BESSIE, ZIGGY, DAISY, PAGING 01–25 | all animals batches | Yes (not exercised) |
| `animals.form` (`AddEditAnimal.feature`) | `animals.form.empty` · `animals.form.bessie-exists` · `animals.form.bessie-soft-deleted` | `empty` | `personas.animals` | Its GUIDs; Name BESSIE (+ Names created by S2/S5/S8) | all animals batches | Yes (not exercised) |
| `animals.delete` (`DeleteAnimal.feature`) | `animals.delete.empty` (master only) · `animals.delete.bessie-exists` · `animals.delete.bessie-soft-deleted` | `empty` | `personas.animals` | Its GUIDs; Name BESSIE | all animals batches | Yes (not exercised) |
| `animals.api` (`AnimalsApi.feature`, API e2e) | `animals.api.empty` · `animals.api.bessie-exists`: Bessie (2020-01-01) · `animals.api.bessie-soft-deleted`: Bessie, deleted · `animals.api.list`: Bessie by `animals-tester`, Ziggy by `animals-nodisplayname`, Daisy deleted | `empty` | `personas.animals` | Its GUIDs; Names BESSIE, ZIGGY, DAISY | all animals batches | Yes (not exercised) |
| `reference-data.types-grid` (`ReferenceDataTypesGrid.feature`) | `reference-data.types-grid.baseline`: re-asserts the migration-seeded reference-data types (exact rows still open with Plan Bot) | `baseline` | `personas.reference-data`, `baseline.migration-seed` | Seeded types only | none | Yes (not exercised) |
| `components.harness` (`ComponentHarness.feature`, harness page) | none — the harness page holds its data in local React state, no database rows | — | — | none | none (can run in parallel) | n/a. Exempt from the reset-first rule because it touches no data (for Review Bot to confirm) |

Seed-unit order for the master reset is as in `ai-test-framework/examples/manage-animals-test-plan.md` → Seed-unit order.

## Scenarios → tests

All 77 scenario IDs have test code on disk. **Round 3 (2026-10-09, test-fix round 1 of 5):** unit Release 52/52 pass (09:10 BST, includes the two un-skipped T-002 S11/S13 reflection Facts and one new S13 Fact); e2e + harness 66/66 pass + 6 setup sign-ins (run 9, 09:19 BST). 76 scenarios Pass; T-ANIMAL-007/S8 then not run (`@skip @fixme`, Plan Bot / Neil). **Addendum 2 (09:56 BST):** Neil confirmed the S8 baseline at 09:46; `@skip @fixme` removed; e2e + harness 67/67 + 6 setup (run 11, 09:52 BST); **all 77 Pass, status passed**. Status legend:

- *Pass (round 3)*: every layer listed for the scenario passed in round 3 (unit Release 09:10 BST and/or e2e/harness run 9).
- *Not run — `@skip`*: written but excluded by the config grep; blocked on a planning decision.
- *Covered by*: the scenario's test is another scenario's test carrying both tags.


### T-ANIMAL-001 — Animal schema / persistence

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-001/S1 | Animal table stores all mapped columns | Unit (EF model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S1")]` AnimalModelMetadataTests.cs::AnimalTable_StoresAllMappedColumns | — (unit) | — | **Pass** (round 3) |
| T-ANIMAL-001/S2 | Attributes default to an empty array | Unit (model default SQL) + API e2e | `[Trait("Scenario", "T-ANIMAL-001/S2")]` AnimalModelMetadataTests.cs::Attributes_DefaultSql_IsEmptyJsonArray + `@T-ANIMAL-001/S2` AnimalsApi.feature::Attributes default to an empty array via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-001/S3 | Normalised name is unique among non-deleted rows | Unit (index metadata) + API e2e (real PostgreSQL index) | `[Trait("Scenario", "T-ANIMAL-001/S3")]` AnimalModelMetadataTests.cs::NormalisedName_HasFilteredUniqueIndexAmongNonDeleted + `@T-ANIMAL-001/S3` AnimalsApi.feature::Duplicate normalised name is rejected by the database and the service | `animals.api.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-001/S4 | A soft-deleted animal's name can be reused | API e2e | `[Trait("Scenario", "T-ANIMAL-001/S4")]` AnimalServiceListDeleteTests.cs::SoftDeletedName_CanBeReused_OnCreate + `@T-ANIMAL-001/S4` AnimalsApi.feature::Soft-deleted animal name can be reused | `animals.api.bessie-soft-deleted` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-001/S5 | Soft-deleted flag exists | Unit (model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S5")]` AnimalModelMetadataTests.cs::SoftDeletedFlag_Exists_WithDefaultFalse | — (unit) | — | **Pass** (round 3) |
| T-ANIMAL-001/S6 | Table lives in the creatures schema | Unit (model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S6")]` AnimalModelMetadataTests.cs::Table_LivesInCreaturesSchema | — (unit) | — | **Pass** (round 3) |
| T-ANIMAL-001/S7 | The animals permission is seeded for our users | Unit (seed data) | `[Trait("Scenario", "T-ANIMAL-001/S7")]` AnimalModelMetadataTests.cs::AnimalsWritePermission_IsSeeded_ForStandardAndAdministrators | — (unit) | — | **Pass** (round 3) |


### T-ANIMAL-002 — Animals service + v1/Animal API, validation and permissions

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-002/S1 | Create animal with valid fields | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S1")]` AnimalServiceCreateTests.cs::Create_ValidFields_PersistsAnimal + `@T-ANIMAL-002/S1` AnimalsApi.feature::Create animal with valid fields via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S2 | Missing Attributes are stored as an empty array | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S2")]` AnimalServiceCreateTests.cs::Create_MissingAttributes_StoresEmptyArray + `@T-ANIMAL-002/S2` AnimalsApi.feature::Missing Attributes are stored as an empty array via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S3 | Duplicate name is rejected | Unit (service check + constructed unique violation) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S3")]` AnimalServiceCreateTests.cs::Create_DuplicateName_RejectedWithExactMessage + `[Trait("Scenario", "T-ANIMAL-002/S3")]` AnimalServiceCreateTests.cs::Create_DatabaseUniqueViolation_MapsToDuplicateMessage + `[Trait("Scenario", "T-ANIMAL-002/S3")]` AnimalServiceCreateTests.cs::Update_ToDuplicateName_RejectedAndOriginalUnchanged + `@T-ANIMAL-002/S3` AnimalsApi.feature::Duplicate normalised name is rejected by the database and the service | `animals.api.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S4 | Name of a soft-deleted animal can be reused | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S4")]` AnimalServiceCreateTests.cs::Create_NameOfSoftDeleted_Succeeds + `@T-ANIMAL-002/S4` AnimalsApi.feature::Soft-deleted animal name can be reused | `animals.api.bessie-soft-deleted` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S5 | Date Born must be before today | Unit (fake clock) + API e2e (today / tomorrow from the server date) | `[Trait("Scenario", "T-ANIMAL-002/S5")]` AnimalServiceCreateTests.cs::Create_DateBornTodayOrLater_FailsWithExactMessage + `@T-ANIMAL-002/S5` AnimalsApi.feature::Date Born must be before today via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S6 | Date Born is mandatory | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S6")]` AnimalServiceCreateTests.cs::Create_DateBornMissing_FailsWithExactMessage + `@T-ANIMAL-002/S6` AnimalsApi.feature::Date Born is mandatory via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S7 | Name is mandatory | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S7")]` AnimalServiceCreateTests.cs::Create_NameMissing_FailsWithExactMessage + `@T-ANIMAL-002/S7` AnimalsApi.feature::Name is mandatory via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S8 | Attribute tag limits | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S8")]` AnimalServiceCreateTests.cs::Create_AttributeTagLimits_FailWithExactMessages + `@T-ANIMAL-002/S8` AnimalsApi.feature::Attribute tag limits via the API | `animals.api.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S9 | List returns non-deleted animals with Last Amended (Bessie by "Animals Tester"; Ziggy by a user with no DisplayName, Email "animals-nodisplayname@e2e.test") | Unit (mapper fallback) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S9")]` AnimalServiceListDeleteTests.cs::List_ReturnsNonDeleted_WithLastAmendedDisplayNameOrEmail + `@T-ANIMAL-002/S9` AnimalsApi.feature::List returns non-deleted animals with Last Amended user | `animals.api.list` | `animals-tester` + `animals-nodisplayname` (both `animals_write`) | **Pass** (round 3) |
| T-ANIMAL-002/S10 | Soft delete and not found afterwards | Unit (row kept, audit) + API e2e (404s) | `[Trait("Scenario", "T-ANIMAL-002/S10")]` AnimalServiceListDeleteTests.cs::Delete_SoftDeletes_AndGetUpdateDeleteReturnNotFound + `@T-ANIMAL-002/S10` AnimalsApi.feature::Soft delete then not found on get update delete | `animals.api.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-002/S11 | Users without animals_write are rejected on every endpoint | API e2e (+ unit reflection test) | `[Trait("Scenario", "T-ANIMAL-002/S11")]` AnimalPoliciesTests.cs::AnimalEndpoints_RejectUsersWithoutAnimalsWrite_ByPolicy + `@T-ANIMAL-002/S11` AnimalsApi.feature::Users without animals_write are rejected on every endpoint (denied writes with a valid body, then read-back as `animals-tester`: Bessie unchanged, no new row) | `animals.api.bessie-exists` | `animals-viewer`, `animals-tester` (read-back) | **Pass** (round 3) |
| T-ANIMAL-002/S12 | User-management permissions alone do not grant access to animals | API e2e | `@T-ANIMAL-002/S12` AnimalsApi.feature::User-management permissions alone do not grant animals access | `animals.api.bessie-exists` | `animals-usermanager` | **Pass** (round 3) |
| T-ANIMAL-002/S13 | AnimalsWrite guards every animal endpoint | Unit (policy registration + reflection) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S13")]` AnimalPoliciesTests.cs::AnimalsWritePolicy_RequiresTheAnimalsWritePermissionClaim + `[Trait("Scenario", "T-ANIMAL-002/S13")]` AnimalPoliciesTests.cs::AllAnimalEndpoints_RequireAnimalsWritePolicy + `[Trait("Scenario", "T-ANIMAL-002/S13")]` AnimalPoliciesTests.cs::ProgramCs_RegistersExactlyOneAnimalsPolicy_AnimalsWrite_RequiringThePermissionClaim + `@T-ANIMAL-002/S13` AnimalsApi.feature::AnimalsWrite succeeds on every animal endpoint (GETs + create / update with read-back / delete) + `@T-ANIMAL-002/S13` AnimalsApi.feature::Without AnimalsWrite create update and delete are forbidden | `animals.api.bessie-exists` | `animals-tester`, `animals-viewer` (403) | **Pass** (round 3) |


### T-ANIMAL-003 — Manage Animals paginated grid + row actions menu

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-003/S2 | List shows non-deleted animals | UI e2e | `@T-ANIMAL-003/S2` ManageAnimalsGrid.feature::List shows non-deleted animals with attributes as comma-separated tags | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user ("Animals Tester"; Email when no DisplayName) | UI e2e | `@T-ANIMAL-003/S3` ManageAnimalsGrid.feature::Last Amended shows date, time and user display name or email | `animals.grid.list` | `animals-tester` + `animals-nodisplayname` (both `animals_write`) | **Pass** (round 3) |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S4` ManageAnimalsGrid.feature::Last Amended is shown in the browser's local time (BST) | `animals.grid.last-amended-times` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S5 | Last Amended outside summer time | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S5` ManageAnimalsGrid.feature::Last Amended outside summer time (GMT) | `animals.grid.last-amended-times` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S6 | Default sort by Name ascending | UI e2e | `@T-ANIMAL-003/S6` ManageAnimalsGrid.feature::Default sort by Name ascending | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S7 | Add opens Basic Form | UI e2e | `@T-ANIMAL-003/S7` ManageAnimalsGrid.feature::Add opens the animal form | `animals.grid.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | UI e2e | `@T-ANIMAL-003/S8` ManageAnimalsGrid.feature::Edit opens the animal form with existing data | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | UI e2e (also tagged `@T-ANIMAL-007/S1`) | `@T-ANIMAL-003/S9` ManageAnimalsGrid.feature::Row actions menu in the last column; row click does nothing | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S12 | Results are paged on the server | UI e2e (observe the real page-2 `v1/Animal` response) | `@T-ANIMAL-003/S12` ManageAnimalsGrid.feature::Results are paged on the server | `animals.grid.paging-25` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S13 | No animals to show | UI e2e | `@T-ANIMAL-003/S13` ManageAnimalsGrid.feature::No animals to show | `animals.grid.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S14 | True shows a green circle with a tick, accessible name Yes | UI e2e (also tagged `@T-ANIMAL-009/S1`): cell computed `color` (the knock-out SVG paints in currentColor) = resolved `--app-boolean-true-fill`; `data-icon="Check"` with `data-icon-knockout="circle"` (tick is a transparent cut-out — no glyph colour asserted, Neil 20:19); `data-boolean-value="true"`, name "Yes", no `role="switch"` | `@T-ANIMAL-003/S14` ManageAnimalsGrid.feature::True shows a green circle with a tick, accessible name Yes | `animals.grid.booleans` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-003/S15 | False shows a red circle with a cross, No; cells are not interactive | UI e2e (also tagged `@T-ANIMAL-009/S2`, `@T-ANIMAL-009/S3`): cell computed `color` = resolved `--app-boolean-false-fill`; `data-icon="Close"` with `data-icon-knockout="circle"` (cut-out, no glyph colour); `data-boolean-value="false"`, name "No"; observe no request on click, not focusable | `@T-ANIMAL-003/S15` ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive | `animals.grid.booleans` | `animals-tester` | **Pass** (round 3) |


### T-ANIMAL-004 — Add | Edit Animal Basic Form

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-004/S1 | Add mode opens with defaults | UI e2e | `@T-ANIMAL-004/S1` AddEditAnimal.feature::Add mode opens with defaults | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S2 | Create animal with required fields | UI e2e + API read-back | `@T-ANIMAL-004/S2` AddEditAnimal.feature::Create animal with required fields + `@T-ANIMAL-004/S2` AddEditAnimal.feature::Date Born typed as soon as the Add form opens is kept (F-46 no-retry check) | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S3 | Name is mandatory | UI e2e | `@T-ANIMAL-004/S3` AddEditAnimal.feature::Name is mandatory | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | UI e2e | `@T-ANIMAL-004/S4` AddEditAnimal.feature::Duplicate name is rejected on Save | `animals.form.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | UI e2e | `@T-ANIMAL-004/S5` AddEditAnimal.feature::Name of a deleted animal can be reused | `animals.form.bessie-soft-deleted` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S6 | Date Born must be before today | UI e2e (browser date; time-zone sensitive) | `@T-ANIMAL-004/S6` AddEditAnimal.feature::Date Born must be before today | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S7 | Date Born is mandatory | UI e2e | `@T-ANIMAL-004/S7` AddEditAnimal.feature::Date Born is mandatory | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | UI e2e + API read-back | `@T-ANIMAL-004/S8` AddEditAnimal.feature::Attributes persist as JSON tags | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S9 | Attribute tag limits | UI e2e (also tagged `@T-ANIMAL-006/S3`) | `@T-ANIMAL-004/S9` AddEditAnimal.feature::Attribute tag limits on the form | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S10 | Edit persists changed fields | UI e2e + API read-back | `@T-ANIMAL-004/S10` AddEditAnimal.feature::Edit persists changed fields | `animals.form.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | UI e2e (two personas) | `@T-ANIMAL-004/S11` AddEditAnimal.feature::Only Add and Edit modes exist | `animals.form.bessie-exists` | `animals-tester` + `animals-viewer` | **Pass** (round 3) |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | UI e2e (Edit URL from reset ids) | `@T-ANIMAL-004/S12` AddEditAnimal.feature::Deleted animal cannot be opened | `animals.form.bessie-soft-deleted` | `animals-tester` | **Pass** (round 3) |


### T-ANIMAL-005 — Soft delete Animal with confirmation

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-005/S1 | Confirmation names the animal | UI e2e | `@T-ANIMAL-005/S1` DeleteAnimal.feature::Confirmation names the animal | `animals.delete.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | UI e2e + API 404 | `@T-ANIMAL-005/S2` DeleteAnimal.feature::Soft delete removes row from the list | `animals.delete.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | UI e2e (observe no DELETE) | `@T-ANIMAL-005/S3` DeleteAnimal.feature::Cancel leaves the animal unchanged | `animals.delete.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | UI e2e | `@T-ANIMAL-005/S4` DeleteAnimal.feature::Deleted animal is gone everywhere but its name is free | `animals.delete.bessie-exists` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | UI e2e + API e2e (403 for both personas) | `@T-ANIMAL-005/S5` DeleteAnimal.feature::Users without animals_write cannot delete | `animals.delete.bessie-exists` | `animals-viewer` + `animals-usermanager` | **Pass** (round 3) |


### T-ANIMAL-006 — Shared Switch and Tag Input controls for Next.js JSON Schema forms

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Component (harness page `/examples/test-harness`, Playwright): `harness-json-form` Is Furry Switch starts Off, turn on → checked (and `harness-switch`) | `@T-ANIMAL-006/S1` ComponentHarness.feature::Switch renders and binds a boolean | — (harness, no data) | `animals-tester` if the route needs sign-in | **Pass** (round 3) |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Component (harness page, Playwright): Attributes Tag Input in `harness-json-form` — add "nocturnal", "endangered & rare", remove chips | `@T-ANIMAL-006/S2` ComponentHarness.feature::Tag Input adds and removes chips | — (harness, no data) | as S1 | **Pass** (round 3) |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Covered by T-ANIMAL-004/S9 (both tags) | `@T-ANIMAL-006/S3` AddEditAnimal.feature::Attribute tag limits on the form | `animals.form.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Component (harness page, Playwright): `harness-switch-readonly`; tick `harness-form-readonly-toggle` → Switch cannot be toggled, chips have no add / remove controls | `@T-ANIMAL-006/S4` ComponentHarness.feature::Read-only Switch and Tag Input | — (harness, no data) | as S1 | **Pass** (round 3) |
| T-ANIMAL-006/S5 | String-array grid cells | UI e2e via Manage Animals (Attributes column) | `@T-ANIMAL-006/S5` ManageAnimalsGrid.feature::List shows non-deleted animals with attributes as comma-separated tags | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |


### T-ANIMAL-007 — Shared, permission-aware row actions menu (UI.NextJs.Framework)

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-007/S1 | Row actions menu in the last column | Covered by T-ANIMAL-003/S9 (both tags) | `@T-ANIMAL-007/S1` ManageAnimalsGrid.feature::Row actions menu in the last column; row click does nothing | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | UI e2e via Manage Animals | `@T-ANIMAL-007/S2` ManageAnimalsGrid.feature::Choosing Edit Animal runs it for that row only | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Component (harness page, Playwright): `harness-perm-usermgmt` → menus list only "Admin only"; no Edit / Any of / Unlock, disabled or otherwise | `@T-ANIMAL-007/S3` ComponentHarness.feature::Items are hidden without the required permission | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Component (harness page, Playwright): `harness-perm-animals` (and `harness-perm-read`) → "Any of" listed in every row | `@T-ANIMAL-007/S4` ComponentHarness.feature::Any one of several permissions is enough | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Component (harness page, Playwright): `harness-perm-none` → `harness-no-actions-column`, no `harness-actions-table` | `@T-ANIMAL-007/S5` ComponentHarness.feature::No Actions column when no item is allowed | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-007/S6 | Per-row visibility | Component (harness page, Playwright): `harness-perm-animals` → "Unlock" in Beta's menu (`locked`), not Alpha's | `@T-ANIMAL-007/S6` ComponentHarness.feature::Per-row visibility hides Delete for Bessie | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Component (harness page, Playwright): expects `harness-row-row-1-no-trigger` and a trigger on row 2 | `@T-ANIMAL-007/S7` ComponentHarness.feature::A row with no visible items has no trigger | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | UI e2e on the reference-data types grid: exactly EXAMPLE_STATUS then SHOWCASE_OPTION (Active items 2, 2); headers Type key / Active items / Actions (last, not sortable); one Manage button per row, no menu trigger; Manage SHOWCASE_OPTION → `/examples/reference-data/manage/SHOWCASE_OPTION?isEnumeration=0`, modal lists Widget and Gadget; close returns to the grid. Cells by header | `@T-ANIMAL-007/S8` ReferenceDataTypesGrid.feature::Existing text-button grids are unaffected | `reference-data.types-grid.baseline` | `reference-data-tester` | **Pass** (round 3 Addendum 2, run 11) |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | UI e2e via Manage Animals | `@T-ANIMAL-007/S9` ManageAnimalsGrid.feature::Menu closes on Escape and outside click | `animals.grid.list` | `animals-tester` | **Pass** (round 3) |


### T-ANIMAL-008 — Manage Animals page (route, nav link, permission gate, layout)

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-008/S1 | (was T-ANIMAL-003 S1) Open Manage Animals from the nav | UI e2e | `@T-ANIMAL-008/S1` ManageAnimalsPage.feature::Open Manage Animals from the nav | `animals.page.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-008/S2 | (was T-ANIMAL-003 S10) User without animals_write cannot open Manage Animals | UI e2e (direct to `/examples/animals` and a form URL; observe no `v1/Animal` request) | `@T-ANIMAL-008/S2` ManageAnimalsPage.feature::User without animals_write cannot open Manage Animals | `animals.page.list` | `animals-viewer` | **Pass** (round 3) |
| T-ANIMAL-008/S3 | (was T-ANIMAL-003 S11) User-management permissions alone do not give access to animals | UI e2e | `@T-ANIMAL-008/S3` ManageAnimalsPage.feature::User-management permissions alone do not show Animals | `animals.page.list` | `animals-usermanager` | **Pass** (round 3) |
| T-ANIMAL-008/S4 | Add \ | Edit Animal opens as a modal over the page and closes back to it | `@T-ANIMAL-008/S4` ManageAnimalsPage.feature::Add Animal opens as a modal over the page and closes back to it | `@T-ANIMAL-008/S4` | `animals.page.empty` | **Pass** (round 3) |
| T-ANIMAL-008/S5 | Opening a form URL directly shows the page with the form on top | UI e2e (direct to `/examples/animals/manage/item`) | `@T-ANIMAL-008/S5` ManageAnimalsPage.feature::Opening a form URL directly shows the page with the form on top | `animals.page.empty` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-008/S6 | The old /manage URL redirects to the page | UI e2e (direct to `/examples/animals/manage`) | `@T-ANIMAL-008/S6` ManageAnimalsPage.feature::The old manage URL redirects to the page | `animals.page.empty` | `animals-tester` | **Pass** (round 3) |


### T-ANIMAL-009 — Shared boolean icon grid cell renderer (UI.NextJs.Framework)

| Scenario | Title (from ticket) | Layer | Test (tag) | Reset key (first step) | Persona | Status |
|---|---|---|---|---|---|---|
| T-ANIMAL-009/S1 | True shows a green circle with a tick, named Yes | Covered by T-ANIMAL-003/S14 (both tags) | `@T-ANIMAL-009/S1` ManageAnimalsGrid.feature::True shows a green circle with a tick, accessible name Yes | `animals.grid.booleans` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-009/S2 | False shows a red circle with a cross, named No | Covered by T-ANIMAL-003/S15 (both tags) | `@T-ANIMAL-009/S2` ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive | `animals.grid.booleans` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-009/S3 | Cell is not interactive | UI e2e via Manage Animals (true and false cells) | `@T-ANIMAL-009/S3` ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive | `animals.grid.booleans` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-009/S4 | Labels are configurable with Yes/No defaults | Component (harness page, Playwright): `harness-bool-true` / `-false` names "Yes" / "No"; `harness-bool-custom` named with its custom true label (defaults also via T-ANIMAL-003/S14, S15) | `@T-ANIMAL-009/S4` ComponentHarness.feature::Boolean labels are configurable with Yes/No defaults | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-009/S5 | Null / undefined shows em dash named Not set | Component (harness page, Playwright): `harness-bool-null` — "—", no circle, colour = resolved `--app-text-primary`, name "Not set", `data-boolean-value="null"` | `@T-ANIMAL-009/S5` ComponentHarness.feature::Null and undefined show em dash named Not set | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-009/S6 | Existing switch cell still available | Component (harness page, Playwright): `harness-bool-switch-cell` renders a read-only Switch (Manage Animals part via T-ANIMAL-003/S14 'neither cell is a Switch') | `@T-ANIMAL-009/S6` ComponentHarness.feature::Existing switch cell still available | — (harness, no data) | as T-006/S1 | **Pass** (round 3) |
| T-ANIMAL-009/S7 | Circle fills meet contrast in light and dark mode | UI e2e via Manage Animals (not the harness): light → `--app-boolean-true-fill` `#609b44` / `--app-boolean-false-fill` `#ef5673` and the Bessie / Ziggy cells' computed `color` match; dark (SiteNav `theme-toggle`, no reload) → `#8dc374` / `#ff9aa8`; contrast computed in the test: each fill ≥ 3:1 vs row `#ffffff` / hover `#fafafa` (light) and `#2d3a4a` / `#3d4854` (dark). Glyph is a transparent cut-out (`Icon knockout="circle"`), so glyph contrast is the same fill-vs-row pair; `--app-boolean-glyph` asserted **not defined** (Neil 20:19). No `#18181b` / glyph-colour assertion | `@T-ANIMAL-009/S7` ManageAnimalsGrid.feature::Circle fills meet contrast in light and dark mode | `animals.grid.booleans` | `animals-tester` | **Pass** (round 3) |
| T-ANIMAL-009/S8 | Dedicated tokens leave system buttons and callouts unchanged | UI e2e via Manage Animals: in light and dark theme `--system-green` resolves to `#72b453` and `--system-red` to `#cf1337`, and `--app-boolean-glyph` is not defined; the no-permission callout (`animals-viewer`) never resolves to the boolean fills. "Renderer contains no hard-coded colour values" is a source property — left to code review (Review Bot) | `@T-ANIMAL-009/S8` ManageAnimalsGrid.feature::Dedicated tokens leave system buttons and callouts unchanged | `animals.grid.booleans` | `animals-tester` (+ `animals-viewer` for the callout) | **Pass** (round 3) |


## Scenario IDs — re-read 2026-10-08 20:06 BST (tests written 20:28 BST)

Every ticket has explicit `### Scenario: S<n> - <title>` headings: T-001 S1–S7 (7), T-002 S1–S13 (13), T-003 S2–S9 + S12–S15 (12), T-004 S1–S12 (12), T-005 S1–S5 (5), T-006 S1–S5 (5), T-007 S1–S9 (9), T-008 S1–S6 (6), T-009 S1–S8 (8). Total **77**.

Changes since the 19:27 BST plan (ticket files are the source):

- **T-ANIMAL-009** (Decision 30): S1 and S2 reworded (filled circle in `--app-boolean-true-fill` / `--app-boolean-false-fill` with Check / Close as a transparent cut-out, `Icon knockout="circle"`; `--app-boolean-glyph` removed — Neil 20:19, tickets T-003 / T-009 re-read 20:29 BST); S5 adds "no circle, theme text colour `--app-text-primary`"; S3, S4, S6 unchanged; **S7** and **S8** new.
- **T-ANIMAL-003**: S14 and S15 reworded in place (green / red circle with tick / cross; same IDs, same accessible names and non-interactive checks). S3 now names the DisplayName "Animals Tester"; the no-DisplayName case still reads generically ("their Email is shown instead") and does not name `animals-nodisplayname@e2e.test`.
- **T-ANIMAL-002**: S9 now uses "Animals Tester" and "animals-nodisplayname@e2e.test"; the ticket note says both personas need `animals_write`.
- Other tickets unchanged (files last written 19:23:53 BST or earlier).

## Flags for the planning agent

- *Resolved (Plan Bot, 20:00 BST, History row 36):* T-ANIMAL-003/S3 and T-ANIMAL-002/S9 no longer name a real person; they use role personas. No scenario names a real person.

## Not automated / questions

- **Resolved:** `animals-nodisplayname` seeded (Dev Bot); harness gaps for T-007 S3–S7 / T-009 S4–S5 / T-006 form JSON filled (Dev Bot 20:15 BST). Tests bind to README data-tids.
- **Resolved — T-007/S8:** Neil confirmed the reference-data types baseline at 09:46 (Plan Bot 09:47): the migration-seeded EXAMPLE_STATUS and SHOWCASE_OPTION, 2 active items each. `@skip` / `@fixme` removed and the scenario passes (Addendum 2), so nothing is blocked.
- **Round 3 sign-in (F-41):** scenarios sign in with `usePersona` (helpers/authentication.ts) from the `setup` project's real SignInForm sign-ins (`e2e/.auth/`, git-ignored); API steps take the token from the untraced `apiAccessToken`. No scenario types a password. Residual (owner code): forcing `--trace=on` on the CLI also traces the setup project, and those traces hold the passwords.
- **Resolved (round 3, F-42):** the ProjectReference exists (Dev Bot d30-2); the T-002 S11/S13 reflection Facts are implemented and pass, plus a new S13 Fact that reads Program.cs's real registrations (host captured at HostBuilt, nothing started).
- **Resolved (Dev Bot):** e2e now pins `@playwright/test` / `playwright` 1.56.1 with `playwright-bdd` 8.5.1; `npx bddgen` works (64 runnable scenarios).
- **Resolved (Dev Bot 09:08 BST):** `DateCompareValidator` now takes the injected `TimeProvider` (Dev Bot added `DateCompareValidatorTests`).
- **Resolved (9 Oct):** Test environment ready (`api_framework_test`, Test API :5188/:7188, UI :3003, secrets as user env vars). Run notes for Dev Bot / Neil: (a) UI `.env.local` API root is the dev API (:7088) — Test runs need a process override or a test env file; (b) `data-tid="animal-form-modal"` is duplicated (ModalShell wrapper + dialog panel + loading fallback); (c) possible early-input loss after the Add modal opens (run 4, Date Born) — tests now fill-and-verify; (d) Playwright `error-context.md` snapshots record typed persona passwords on sign-in failures; (e) animal batch resets clear only footprint names — tests use footprint names (Bessie / Ziggy / Daisy / paging).
- **Decided (closed):** component harness — Neil chose it at 20:04 BST; Dev Bot built `/examples/test-harness`. `ComponentHarness.feature` has no reset step (no data; exemption for Review Bot to confirm).
- **Coverage notes:** T-ANIMAL-001/S7 second half (re-signed-in Standard user's token carries `animals_write`) is implied by API e2e T-002/S13 for `animals-tester`, not asserted on the raw JWT. T-ANIMAL-004/S2, S8, S10 verify persisted values through the Manage Animals grid after save (no separate API read-back). T-ANIMAL-009/S8 "renderer contains no hard-coded colour values" is a source property → Review Bot.
