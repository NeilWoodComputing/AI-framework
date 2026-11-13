# Test report — manage-animals — run 2

| Field | Value |
|-------|-------|
| Run | 2 (`handoff.md` `testing.round`) · first real run · unit 2026-10-09 00:55 BST; e2e/harness final run 5 started 08:36 BST, finished 08:39 BST · test-bot |
| Test-fix round | 0 of 5 · first run, not a fix re-run. Test defects found during this run were self-fixed **before** reporting (F1–F6 below); nothing was routed back by Review Bot |
| Safety gate | `ConnectionStrings__LoginConnection` → Database=`api_framework_test`, host `localhost:5432` (checked before every reset / e2e run; no other part of the string printed) |
| Environment | Test · UI `http://localhost:3003` (`npm run dev`, Next.js 15.5.27) · API.Framework launch profile **Test** `https://localhost:7188` / `http://localhost:5188` (`API_URL=http://localhost:5188/v1`) · PostgreSQL Docker `localhost:5432` DB `api_framework_test` · Windows user env vars loaded into fresh processes (values never echoed) |
| UI → API wiring | `.env.local` (not opened) points the UI at the **dev** API `https://localhost:7088/v1` (browser probe: `POST https://localhost:7088/v1/Authorisation/SignIn` → connection refused). UI restarted with process env `NEXT_PUBLIC_UNITY_API_ROOT=https://localhost:7188/v1/` (no file edited); probe then hit `:7188` with `Access-Control-Allow-Origin: http://localhost:3003`. Grid scenarios (T-003 S2/S3/S13, T-008 S1) prove the UI reads `api_framework_test` |
| Master reset | Global setup (`global-setup.ts`) on every run; per-scenario batch reset keys (`Given the test data is …`) |
| Personas used | `testdata-admin`, `animals-tester`, `animals-nodisplayname`, `animals-viewer`, `animals-usermanager` |
| Code under test | not under git (api and ui); app code / scaffolding / config not modified by test-bot |
| Commands | Unit: `dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release` (trx `Api.Framework.Tests/TestResults/manage-animals-unit.trx`). E2e: `npx bddgen` then `npx playwright test --workers=1 --reporter=list,json,html` in `UI.NextJs.Framework/e2e` (`PLAYWRIGHT_JSON_OUTPUT_NAME=test-results/manage-animals-results.json`, `PLAYWRIGHT_HTML_OPEN=never`; HTML report `e2e/playwright-report/index.html`; traces retain-on-failure under `e2e/test-results/`). Reporter set on the CLI, so the config's cucumber HTML report was not regenerated |
| Result | **76 Pass · 0 Fail · 1 Not run (`@skip`, blocked on planning) · 0 Not automated** — overall **passed** |
| Layers | Unit: 47 tests, 45 pass, 2 Skip, 0 fail. E2e + harness: 64 tests, 64 pass, 0 fail (T-007 S8 excluded by `grep: /^(?!.*@skip)/`) |
| E5 reset-first scan | Every DB-backed scenario starts with `Given the test data is "<key>"`; `ComponentHarness.feature` has no reset (no data — exemption for Review Bot to confirm) |
| E1 front-end mock scan | No `page.route` / `route.fulfill` / mocked fetch in feature steps; API calls go through an untraced `playwrightRequest.newContext()` |

## Summary

First real run on Neil's PC against `api_framework_test`. Unit tests ran green in Release at 00:55 BST. The first e2e attempts were cut short by the PC entering Modern Standby (00:58 and 07:35 BST; Neil changed sleep settings at 08:21). Run 2 (07:35) then failed 45 of 64. 40 of those were an **environment** issue: the UI's API root pointed at the dev API on :7088, so the sign-in form showed "Unable to reach Unity API (Failed to fetch)". The other five were test defects. After restarting the UI with a process-level API-root override, runs 3 and 4 showed more test defects (selector strictness, a data leak between scenarios created by one of my scenarios, a hidden-input click, and an early form fill being lost). All were fixed in test code only. Run 5 passed 64/64. **No code defects were found.**

## Results by ticket

| Ticket | Scenarios | Pass | Fail | Not run |
|--------|-----------|------|------|---------|
| T-ANIMAL-001 | 7 | 7 | 0 | 0 |
| T-ANIMAL-002 | 13 | 13 | 0 | 0 |
| T-ANIMAL-003 | 12 | 12 | 0 | 0 |
| T-ANIMAL-004 | 12 | 12 | 0 | 0 |
| T-ANIMAL-005 | 5 | 5 | 0 | 0 |
| T-ANIMAL-006 | 5 | 5 | 0 | 0 |
| T-ANIMAL-007 | 9 | 8 | 0 | 1 |
| T-ANIMAL-008 | 6 | 6 | 0 | 0 |
| T-ANIMAL-009 | 8 | 8 | 0 | 0 |
| **Total** | **77** | **76** | **0** | **1** |

## Run history (this round)

| Run | Started (BST) | Result | Cause of failures | Classification |
|-----|---------------|--------|-------------------|----------------|
| Unit | 00:55 | 47 total · 45 pass · 2 Skip · 0 fail | — (2 Skip: controller reflection, no ProjectReference to Api.Framework web) | scaffolding gap (known) |
| e2e 1 | 00:57 | no result | PowerShell split the reporter list (my launch error), then the PC went into standby at 00:58 | env / runner |
| e2e 2 | 07:35 | 19 pass · 45 fail (22.6 min; PC in and out of standby) | 40: UI API root = dev API :7088 (not running) → sign-in "Failed to fetch". 5: test defects F1–F3 | **env** (40) · **test** (5) |
| e2e 3 | 08:23 | 41 pass · 23 fail | 14: duplicate `data-tid="animal-form-modal"` → strict-mode violations (F4). 7: "Nocturnal" created by T-004/S8 outside every batch footprint leaked into later scenarios (F5). 2: hidden Switch input clicks (F2) | **test** (23) |
| e2e 4 | 08:31 | 62 pass · 2 fail | T-004/S5, S8: Date Born fill lost after the Add modal opened (F6) | **test** (robustness; possible UX race noted for Dev Bot) |
| e2e 5 | 08:36 | **64 pass · 0 fail** (2.8 min) | — | — |

## Test fixes made (test code only, before reporting; test_fix_cycle stays 0)

| Fix | Files | Change | Scenarios |
|-----|-------|--------|-----------|
| F1 | `e2e/features/common/api.steps.ts` | List assertions read `PagedBody` JSON `data` (they only read `items` / `results`) | T-002 S1, S9 (+ T-001 S2 list step) |
| F2 | `e2e/features/animals/harness.steps.ts`, `animals.steps.ts` | The design-system Switch `<input>` is 0×0 with opacity 0: click its visible `<label for>` and assert checked. The read-only switch cell asserts the label is visible and the input attached, checked and disabled (rather than visible) | T-006 S1, T-004 S10, T-009 S6 |
| F3 | `e2e/features/animals/ComponentHarness.feature` | T-007/S4: with `animals_write` the menu correctly shows Edit Animal, Delete Animal, Open and View report; with `reports_view`, Open and View report. Expected lists made exact (the old step expected only View report) | T-007 S4 |
| F4 | `e2e/features/animals/animals.steps.ts` | `formModal()` targets `[role="dialog"][data-tid="animal-form-modal"]` for positive checks; absence checks stay on the tid | 14 form / page scenarios |
| F5 | `e2e/features/animals/AddEditAnimal.feature` | T-004/S8 creates "Bessie" (in the `animals.form` footprint) instead of "Nocturnal", which no batch reset clears | T-004 S8 → removed the leak into T-001 S2, T-002 S1/S9, T-003 S2/S6/S12/S13 |
| F6 | `e2e/features/animals/animals.steps.ts` | `fillStable()`: wait until the field is editable, then fill and verify the value, retrying for up to 10 s | T-004 S5, S8 (all name / Date Born fills) |

`tsc --noEmit` passed after each fix; `bddgen` regenerated.

## Results by scenario

| Scenario | Layer | Test | Status | Evidence |
|----------|-------|------|--------|----------|
| T-ANIMAL-001/S1 | Unit (EF model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S1")]` AnimalModelMetadataTests.cs::AnimalTable_StoresAllMappedColumns | Pass | unit pass (Release 00:55 BST). |
| T-ANIMAL-001/S2 | Unit (model default SQL) + API e2e | `[Trait("Scenario", "T-ANIMAL-001/S2")]` AnimalModelMetadataTests.cs::Attributes_DefaultSql_IsEmptyJsonArray + `@T-ANIMAL-001/S2` AnimalsApi.feature::Attributes default to an empty array via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F5 (Nocturnal leak removed at source, T-004/S8). |
| T-ANIMAL-001/S3 | Unit (index metadata) + API e2e (real PostgreSQL index) | `[Trait("Scenario", "T-ANIMAL-001/S3")]` AnimalModelMetadataTests.cs::NormalisedName_HasFilteredUniqueIndexAmongNonDeleted + `@T-ANIMAL-001/S3` AnimalsApi.feature::Duplicate normalised name is rejected by the database and the service | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-001/S4 | API e2e | `[Trait("Scenario", "T-ANIMAL-001/S4")]` AnimalServiceListDeleteTests.cs::SoftDeletedName_CanBeReused_OnCreate + `@T-ANIMAL-001/S4` AnimalsApi.feature::Soft-deleted animal name can be reused | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-001/S5 | Unit (model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S5")]` AnimalModelMetadataTests.cs::SoftDeletedFlag_Exists_WithDefaultFalse | Pass | unit pass (Release 00:55 BST). |
| T-ANIMAL-001/S6 | Unit (model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S6")]` AnimalModelMetadataTests.cs::Table_LivesInCreaturesSchema | Pass | unit pass (Release 00:55 BST). |
| T-ANIMAL-001/S7 | Unit (seed data) | `[Trait("Scenario", "T-ANIMAL-001/S7")]` AnimalModelMetadataTests.cs::AnimalsWritePermission_IsSeeded_ForStandardAndAdministrators | Pass | unit pass (Release 00:55 BST). |
| T-ANIMAL-002/S1 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S1")]` AnimalServiceCreateTests.cs::Create_ValidFields_PersistsAnimal + `@T-ANIMAL-002/S1` AnimalsApi.feature::Create animal with valid fields via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F1 (list steps read PagedBody `data`). |
| T-ANIMAL-002/S2 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S2")]` AnimalServiceCreateTests.cs::Create_MissingAttributes_StoresEmptyArray + `@T-ANIMAL-002/S2` AnimalsApi.feature::Missing Attributes are stored as an empty array via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S3 | Unit (service check + constructed unique violation) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S3")]` AnimalServiceCreateTests.cs::Create_DuplicateName_RejectedWithExactMessage + `[Trait("Scenario", "T-ANIMAL-002/S3")]` AnimalServiceCreateTests.cs::Create_DatabaseUniqueViolation_MapsToDuplicateMessage + `[Trait("Scenario", "T-ANIMAL-002/S3")]` AnimalServiceCreateTests.cs::Update_ToDuplicateName_RejectedAndOriginalUnchanged + `@T-ANIMAL-002/S3` AnimalsApi.feature::Duplicate normalised name is rejected by the database and the service | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S4 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S4")]` AnimalServiceCreateTests.cs::Create_NameOfSoftDeleted_Succeeds + `@T-ANIMAL-002/S4` AnimalsApi.feature::Soft-deleted animal name can be reused | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S5 | Unit (fake clock) + API e2e (today / tomorrow from the server date) | `[Trait("Scenario", "T-ANIMAL-002/S5")]` AnimalServiceCreateTests.cs::Create_DateBornTodayOrLater_FailsWithExactMessage + `@T-ANIMAL-002/S5` AnimalsApi.feature::Date Born must be before today via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). Finding kept: DateCompareValidator reads DateTime.UtcNow, not TimeProvider. |
| T-ANIMAL-002/S6 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S6")]` AnimalServiceCreateTests.cs::Create_DateBornMissing_FailsWithExactMessage + `@T-ANIMAL-002/S6` AnimalsApi.feature::Date Born is mandatory via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S7 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S7")]` AnimalServiceCreateTests.cs::Create_NameMissing_FailsWithExactMessage + `@T-ANIMAL-002/S7` AnimalsApi.feature::Name is mandatory via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S8 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S8")]` AnimalServiceCreateTests.cs::Create_AttributeTagLimits_FailWithExactMessages + `@T-ANIMAL-002/S8` AnimalsApi.feature::Attribute tag limits via the API | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S9 | Unit (mapper fallback) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S9")]` AnimalServiceListDeleteTests.cs::List_ReturnsNonDeleted_WithLastAmendedDisplayNameOrEmail + `@T-ANIMAL-002/S9` AnimalsApi.feature::List returns non-deleted animals with Last Amended user | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F1 (list steps read PagedBody `data`). |
| T-ANIMAL-002/S10 | Unit (row kept, audit) + API e2e (404s) | `[Trait("Scenario", "T-ANIMAL-002/S10")]` AnimalServiceListDeleteTests.cs::Delete_SoftDeletes_AndGetUpdateDeleteReturnNotFound + `@T-ANIMAL-002/S10` AnimalsApi.feature::Soft delete then not found on get update delete | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S11 | API e2e (+ unit reflection test) | `[Trait("Scenario", "T-ANIMAL-002/S11")]` AnimalPoliciesTests.cs::AnimalEndpoints_RejectUsersWithoutAnimalsWrite_ByPolicy (Skip) + `@T-ANIMAL-002/S11` AnimalsApi.feature::Users without animals_write are rejected on every endpoint | Pass | unit Skip only; e2e pass (run 5, 08:36 BST). unit AnimalEndpoints_RejectUsersWithoutAnimalsWrite_ByPolicy Skip (no ProjectReference to Api.Framework web - owner code); behaviour proven by API e2e. |
| T-ANIMAL-002/S12 | API e2e | `@T-ANIMAL-002/S12` AnimalsApi.feature::User-management permissions alone do not grant animals access | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-002/S13 | Unit (policy registration + reflection) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S13")]` AnimalPoliciesTests.cs::AnimalsWritePolicy_RequiresTheAnimalsWritePermissionClaim + `[Trait("Scenario", "T-ANIMAL-002/S13")]` AnimalPoliciesTests.cs::AllAnimalEndpoints_RequireAnimalsWritePolicy (Skip) + `@T-ANIMAL-002/S13` AnimalsApi.feature::AnimalsWrite succeeds on every animal endpoint | Pass | unit pass (Release 00:55 BST); e2e pass (run 5, 08:36 BST). unit AllAnimalEndpoints_RequireAnimalsWritePolicy Skip (no ProjectReference to Api.Framework web - owner code); behaviour proven by API e2e. |
| T-ANIMAL-003/S2 | UI e2e | `@T-ANIMAL-003/S2` ManageAnimalsGrid.feature::List shows non-deleted animals with attributes as comma-separated tags | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F5 (Nocturnal leak removed at source, T-004/S8). Proves UI -> Test API wiring (grid data from api_framework_test). |
| T-ANIMAL-003/S3 | UI e2e | `@T-ANIMAL-003/S3` ManageAnimalsGrid.feature::Last Amended shows date, time and user display name or email | Pass | e2e pass (run 5, 08:36 BST). Proves UI -> Test API wiring (grid data from api_framework_test). |
| T-ANIMAL-003/S4 | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S4` ManageAnimalsGrid.feature::Last Amended is shown in the browser's local time (BST) | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-003/S5 | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S5` ManageAnimalsGrid.feature::Last Amended outside summer time (GMT) | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-003/S6 | UI e2e | `@T-ANIMAL-003/S6` ManageAnimalsGrid.feature::Default sort by Name ascending | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F5 (Nocturnal leak removed at source, T-004/S8). |
| T-ANIMAL-003/S7 | UI e2e | `@T-ANIMAL-003/S7` ManageAnimalsGrid.feature::Add opens the animal form | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-003/S8 | UI e2e | `@T-ANIMAL-003/S8` ManageAnimalsGrid.feature::Edit opens the animal form with existing data | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-003/S9 | UI e2e (also tagged `@T-ANIMAL-007/S1`) | `@T-ANIMAL-003/S9` ManageAnimalsGrid.feature::Row actions menu in the last column; row click does nothing | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-003/S12 | UI e2e (observe the real page-2 `v1/Animal` response) | `@T-ANIMAL-003/S12` ManageAnimalsGrid.feature::Results are paged on the server | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F5 (Nocturnal leak removed at source, T-004/S8). |
| T-ANIMAL-003/S13 | UI e2e | `@T-ANIMAL-003/S13` ManageAnimalsGrid.feature::No animals to show | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F5 (Nocturnal leak removed at source, T-004/S8). Proves UI -> Test API wiring (grid data from api_framework_test). |
| T-ANIMAL-003/S14 | UI e2e (also tagged `@T-ANIMAL-009/S1`): cell computed `color` (the knock-out SVG paints in currentColor) = resolved `--app-boolean-true-fill`; `data-icon="Check"` with `data-icon-knockout="circle"` (tick is a transparent cut-out — no glyph colour asserted, Neil 20:19); `data-boolean-value="true"`, name "Yes", no `role="switch"` | `@T-ANIMAL-003/S14` ManageAnimalsGrid.feature::True shows a green circle with a tick, accessible name Yes | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-003/S15 | UI e2e (also tagged `@T-ANIMAL-009/S2`, `@T-ANIMAL-009/S3`): cell computed `color` = resolved `--app-boolean-false-fill`; `data-icon="Close"` with `data-icon-knockout="circle"` (cut-out, no glyph colour); `data-boolean-value="false"`, name "No"; observe no request on click, not focusable | `@T-ANIMAL-003/S15` ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-004/S1 | UI e2e | `@T-ANIMAL-004/S1` AddEditAnimal.feature::Add mode opens with defaults | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S2 | UI e2e + API read-back | `@T-ANIMAL-004/S2` AddEditAnimal.feature::Create animal with required fields | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-004/S3 | UI e2e | `@T-ANIMAL-004/S3` AddEditAnimal.feature::Name is mandatory | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S4 | UI e2e | `@T-ANIMAL-004/S4` AddEditAnimal.feature::Duplicate name is rejected on Save | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S5 | UI e2e | `@T-ANIMAL-004/S5` AddEditAnimal.feature::Name of a deleted animal can be reused | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F6 (fill-and-verify). |
| T-ANIMAL-004/S6 | UI e2e (browser date; time-zone sensitive) | `@T-ANIMAL-004/S6` AddEditAnimal.feature::Date Born must be before today | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S7 | UI e2e | `@T-ANIMAL-004/S7` AddEditAnimal.feature::Date Born is mandatory | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S8 | UI e2e + API read-back | `@T-ANIMAL-004/S8` AddEditAnimal.feature::Attributes persist as JSON tags | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F5 (Nocturnal -> Bessie, footprint) + F6 (fill-and-verify). |
| T-ANIMAL-004/S9 | UI e2e (also tagged `@T-ANIMAL-006/S3`) | `@T-ANIMAL-004/S9` AddEditAnimal.feature::Attribute tag limits on the form | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S10 | UI e2e + API read-back | `@T-ANIMAL-004/S10` AddEditAnimal.feature::Edit persists changed fields | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F2 (Switch via label). |
| T-ANIMAL-004/S11 | UI e2e (two personas) | `@T-ANIMAL-004/S11` AddEditAnimal.feature::Only Add and Edit modes exist | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-004/S12 | UI e2e (Edit URL from reset ids) | `@T-ANIMAL-004/S12` AddEditAnimal.feature::Deleted animal cannot be opened | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-005/S1 | UI e2e | `@T-ANIMAL-005/S1` DeleteAnimal.feature::Confirmation names the animal | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-005/S2 | UI e2e + API 404 | `@T-ANIMAL-005/S2` DeleteAnimal.feature::Soft delete removes row from the list | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-005/S3 | UI e2e (observe no DELETE) | `@T-ANIMAL-005/S3` DeleteAnimal.feature::Cancel leaves the animal unchanged | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-005/S4 | UI e2e | `@T-ANIMAL-005/S4` DeleteAnimal.feature::Deleted animal is gone everywhere but its name is free | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-005/S5 | UI e2e + API e2e (403 for both personas) | `@T-ANIMAL-005/S5` DeleteAnimal.feature::Users without animals_write cannot delete | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-006/S1 | Component (harness page `/examples/test-harness`, Playwright): `harness-json-form` Is Furry Switch starts Off, turn on → checked (and `harness-switch`) | `@T-ANIMAL-006/S1` ComponentHarness.feature::Switch renders and binds a boolean | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F2 (Switch clicked via its visible label). |
| T-ANIMAL-006/S2 | Component (harness page, Playwright): Attributes Tag Input in `harness-json-form` — add "nocturnal", "endangered & rare", remove chips | `@T-ANIMAL-006/S2` ComponentHarness.feature::Tag Input adds and removes chips | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-006/S3 | Covered by T-ANIMAL-004/S9 (both tags) | `@T-ANIMAL-006/S3` AddEditAnimal.feature::Attribute tag limits on the form | Pass | e2e pass (run 5, 08:36 BST). Covered by the T-ANIMAL-004/S9 test (carries both tags). |
| T-ANIMAL-006/S4 | Component (harness page, Playwright): `harness-switch-readonly`; tick `harness-form-readonly-toggle` → Switch cannot be toggled, chips have no add / remove controls | `@T-ANIMAL-006/S4` ComponentHarness.feature::Read-only Switch and Tag Input | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-006/S5 | UI e2e via Manage Animals (Attributes column) | `@T-ANIMAL-006/S5` ManageAnimalsGrid.feature::List shows non-deleted animals with attributes as comma-separated tags | Pass | e2e pass (run 5, 08:36 BST). Covered by the T-ANIMAL-003/S2 test (carries both tags). |
| T-ANIMAL-007/S1 | Covered by T-ANIMAL-003/S9 (both tags) | `@T-ANIMAL-007/S1` ManageAnimalsGrid.feature::Row actions menu in the last column; row click does nothing | Pass | e2e pass (run 5, 08:36 BST). Covered by the T-ANIMAL-003/S9 test (carries both tags). |
| T-ANIMAL-007/S2 | UI e2e via Manage Animals | `@T-ANIMAL-007/S2` ManageAnimalsGrid.feature::Choosing Edit Animal runs it for that row only | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-007/S3 | Component (harness page, Playwright): `harness-perm-usermgmt` → menus list only "Admin only"; no Edit / Any of / Unlock, disabled or otherwise | `@T-ANIMAL-007/S3` ComponentHarness.feature::Items are hidden without the required permission | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-007/S4 | Component (harness page, Playwright): `harness-perm-animals` (and `harness-perm-read`) → "Any of" listed in every row | `@T-ANIMAL-007/S4` ComponentHarness.feature::Any one of several permissions is enough | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F3 (exact menu lists per permission). |
| T-ANIMAL-007/S5 | Component (harness page, Playwright): `harness-perm-none` → `harness-no-actions-column`, no `harness-actions-table` | `@T-ANIMAL-007/S5` ComponentHarness.feature::No Actions column when no item is allowed | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-007/S6 | Component (harness page, Playwright): `harness-perm-animals` → "Unlock" in Beta's menu (`locked`), not Alpha's | `@T-ANIMAL-007/S6` ComponentHarness.feature::Per-row visibility hides Delete for Bessie | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-007/S7 | Component (harness page, Playwright): expects `harness-row-row-1-no-trigger` and a trigger on row 2 | `@T-ANIMAL-007/S7` ComponentHarness.feature::A row with no visible items has no trigger | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-007/S8 | UI e2e on the reference-data types grid | `@T-ANIMAL-007/S8` ReferenceDataTypesGrid.feature::Existing text-button grids are unaffected (@skip/@fixme) | Not run (`@skip @fixme`) — Blocked | Not run: @skip @fixme (config grep excludes @skip). Awaiting Plan Bot / Neil on the reference-data types baseline rows (owner Plan Bot / Neil). Round 2. |
| T-ANIMAL-007/S9 | UI e2e via Manage Animals | `@T-ANIMAL-007/S9` ManageAnimalsGrid.feature::Menu closes on Escape and outside click | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-008/S1 | UI e2e | `@T-ANIMAL-008/S1` ManageAnimalsPage.feature::Open Manage Animals from the nav | Pass | e2e pass (run 5, 08:36 BST). Proves UI -> Test API wiring (grid data from api_framework_test). |
| T-ANIMAL-008/S2 | UI e2e (direct to `/examples/animals` and a form URL; observe no `v1/Animal` request) | `@T-ANIMAL-008/S2` ManageAnimalsPage.feature::User without animals_write cannot open Manage Animals | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-008/S3 | UI e2e | `@T-ANIMAL-008/S3` ManageAnimalsPage.feature::User-management permissions alone do not show Animals | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-008/S4 | Edit Animal opens as a modal over the page and closes back to it | `@T-ANIMAL-008/S4` ManageAnimalsPage.feature::Add Animal opens as a modal over the page and closes back to it | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-008/S5 | UI e2e (direct to `/examples/animals/manage/item`) | `@T-ANIMAL-008/S5` ManageAnimalsPage.feature::Opening a form URL directly shows the page with the form on top | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F4 (form modal located by role=dialog; duplicate tid). |
| T-ANIMAL-008/S6 | UI e2e (direct to `/examples/animals/manage`) | `@T-ANIMAL-008/S6` ManageAnimalsPage.feature::The old manage URL redirects to the page | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-009/S1 | Covered by T-ANIMAL-003/S14 (both tags) | `@T-ANIMAL-009/S1` ManageAnimalsGrid.feature::True shows a green circle with a tick, accessible name Yes | Pass | e2e pass (run 5, 08:36 BST). Covered by the T-ANIMAL-003/S14 test (carries both tags). |
| T-ANIMAL-009/S2 | Covered by T-ANIMAL-003/S15 (both tags) | `@T-ANIMAL-009/S2` ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive | Pass | e2e pass (run 5, 08:36 BST). Covered by the T-ANIMAL-003/S15 test (carries both tags). |
| T-ANIMAL-009/S3 | UI e2e via Manage Animals (true and false cells) | `@T-ANIMAL-009/S3` ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive | Pass | e2e pass (run 5, 08:36 BST). Covered by the T-ANIMAL-003/S15 test (carries both tags). |
| T-ANIMAL-009/S4 | Component (harness page, Playwright): `harness-bool-true` / `-false` names "Yes" / "No"; `harness-bool-custom` named with its custom true label (defaults also via T-ANIMAL-003/S14, S15) | `@T-ANIMAL-009/S4` ComponentHarness.feature::Boolean labels are configurable with Yes/No defaults | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-009/S5 | Component (harness page, Playwright): `harness-bool-null` — "—", no circle, colour = resolved `--app-text-primary`, name "Not set", `data-boolean-value="null"` | `@T-ANIMAL-009/S5` ComponentHarness.feature::Null and undefined show em dash named Not set | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-009/S6 | Component (harness page, Playwright): `harness-bool-switch-cell` renders a read-only Switch (Manage Animals part via T-ANIMAL-003/S14 'neither cell is a Switch') | `@T-ANIMAL-009/S6` ComponentHarness.feature::Existing switch cell still available | Pass | e2e pass (run 5, 08:36 BST). First-run self-fix before reporting: F2 (read-only switch: attached/checked/disabled, label visible). |
| T-ANIMAL-009/S7 | UI e2e via Manage Animals (not the harness): light → `--app-boolean-true-fill` `#609b44` / `--app-boolean-false-fill` `#ef5673` and the Bessie / Ziggy cells' computed `color` match; dark (SiteNav `theme-toggle`, no reload) → `#8dc374` / `#ff9aa8`; contrast computed in the test: each fill ≥ 3:1 vs row `#ffffff` / hover `#fafafa` (light) and `#2d3a4a` / `#3d4854` (dark). Glyph is a transparent cut-out (`Icon knockout="circle"`), so glyph contrast is the same fill-vs-row pair; `--app-boolean-glyph` asserted **not defined** (Neil 20:19). No `#18181b` / glyph-colour assertion | `@T-ANIMAL-009/S7` ManageAnimalsGrid.feature::Circle fills meet contrast in light and dark mode | Pass | e2e pass (run 5, 08:36 BST). |
| T-ANIMAL-009/S8 | UI e2e via Manage Animals: in light and dark theme `--system-green` resolves to `#72b453` and `--system-red` to `#cf1337`, and `--app-boolean-glyph` is not defined; the no-permission callout (`animals-viewer`) never resolves to the boolean fills. "Renderer contains no hard-coded colour values" is a source property — left to code review (Review Bot) | `@T-ANIMAL-009/S8` ManageAnimalsGrid.feature::Dedicated tokens leave system buttons and callouts unchanged | Pass | e2e pass (run 5, 08:36 BST). |

## Failures

None in the final run. No code defects. The interim failures and their classification are in **Run history**.

## Blocked / not run

| Scenario | Reason | Owner |
|----------|--------|-------|
| T-ANIMAL-007/S8 | Written as `@skip @fixme`: reference-data types baseline rows not confirmed | Plan Bot / Neil |

## Notes for Dev Bot / Neil (not defects in the feature under test)

1. **Env / config:** UI `.env.local` `NEXT_PUBLIC_UNITY_API_ROOT` targets the dev API (`https://localhost:7088/v1`). Test runs need `https://localhost:7188/v1/`. This run used a process-level override on the UI that test-bot started; a `dev:test` script or test env file would make it repeatable (owner code / Neil).
2. **Duplicate data-tid (minor):** `animal-form-modal` appears on the routed `ModalShell` wrapper, the `Modal` dialog panel and the route `loading.tsx` fallback (`use-animals-grid.tsx`, `AnimalFormModal.tsx`, `@modal/(.)manage/item/**/loading.tsx`).
3. **Possible early-input race (low confidence):** in run 4, Date Born typed straight after the Add modal opened was empty at Save, while Name kept its value. It may be a form re-initialisation after the loading fallback. The tests now fill and verify, so this is not proven as a defect.
4. **Sensitive artefacts:** on sign-in failures, Playwright `error-context.md` page snapshots record the typed persona password in plain text (seen in run 2). Later runs clear `test-results/`. Consider signing in via API `storageState` or masking (owner code). Neil may want to rotate the `animals-viewer` test password.
5. **Batch footprints:** animal batch resets clear only their footprint names (Bessie / Ziggy / Daisy / paging names, by updated-by persona). Feature tests must only create those names. README could say so.
6. Known: `Api.Framework.Tests` has no ProjectReference to the Api.Framework web project (2 reflection Facts Skip); `DateCompareValidator` reads `DateTime.UtcNow`, not `TimeProvider`.

## For the reviewing agent (test review, `review-tests`)

- Tested: 76 scenarios pass (unit and/or e2e/harness). Failing: none. Not run: T-ANIMAL-007/S8 (`@skip @fixme`, planning decision). Not automated: none.
- Test code changed in this round (F1–F6, files above), all before reporting; no Review Bot routing, so `test_fix_cycle` = 0.
- Check: harness no-reset exemption; F4 dialog selector; F6 retry helper; T-002 S11/S13 rely on API e2e while the reflection Facts are skipped.
- Artefacts: `e2e/test-results/manage-animals-results.json` (run 5), `e2e/playwright-report/index.html`, unit trx `Api.Framework.Tests/TestResults/manage-animals-unit.trx`.
