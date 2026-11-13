# Test plan — system-rename

| Field | Value |
|-------|-------|
| Feature folder | `ai-planning-framework/work/system-rename/` |
| Tickets | T-RENAME-001 … T-RENAME-011 (50 explicit scenario IDs; every ticket has `### Scenario: S<n>` headings) |
| Specs | None (rename only: no pages, controls or DB columns change; `plan.md` header) |
| Active API / UI | api-framework (API.Framework) / nextjs (UI.NextJs.Framework) |
| Unit test project | Api.Framework.Tests (approved 08/10/2026) |
| E2E location | `ai-code-framework/ui/UI.NextJs.Framework/e2e` (`testing.e2e.nextjs.path`) |
| Environment | Test · dedicated PostgreSQL `api_framework_test` (localhost:5432) · Test API launch profile Test (https 7188 / http 5188, no `/v1`) · UI `npm run dev:test` on Test Bot's own port :3013 from run 2 (API root `https://localhost:7188/`; :3003 is Neil's dev UI and is never used by e2e; `BASE_URL` set for the run only) · master reset once per run (global setup) |
| Written by | test-bot · 2026-10-09 13:05 BST (updated 13:10 after run 2; 13:15 T-RENAME-004/S4 reworded to same tab by Plan Bot; 13:53 run 2: T-RENAME-011/S1 written and passed, T-RENAME-002/S2 second Then covered by unit tests) |

## Scope and approach

- **T-RENAME-008 is Test Bot's own ticket** (test framework docs and e2e steps). Test Bot changed the files itself and checks S1–S3 with scripted static checks plus the e2e run.
- The other tickets are owned by Dev Bot (001–007), Plan Bot (009), Review Bot (010) and Neil + Dev Bot + Test Bot (011). Test Bot does not change their files. It tests what can be observed at runtime with new e2e scenarios in `e2e/features/system-rename/SystemRename.feature` (tag `@system-rename`), and checks source-level Thens with a read-only script (`%TEMP%\tb-run\rename\static-checks.ps1`, counts and file:line only).
- **Regression:** the full manage-animals suite (67 scenarios + 6 setup sign-ins) runs unchanged on the renamed stack. That covers T-RENAME-011/S4 ("every scenario that passed before the rename passes").
- Layers used: **Unit** (Api.Framework.Tests, Release), **API e2e** / **UI e2e** (Playwright + playwright-bdd, real UI + real API + `api_framework_test`, no front-end mocks), **Static check** (scripted read-only search / compare; not a unit or e2e test, recorded as evidence), **Not automated** (with the reason).
- Documentation and config tickets owned by other agents (006, 009, 010) have no runtime behaviour. They are **Not automated** here and are checked in Review Bot's full review (D8).

## Personas

| Persona | Permissions | Display name | Password env var | Used by batches |
|---------|-------------|--------------|------------------|-----------------|
| `animals-tester` | animals read + write (manage-animals personas, unchanged) | as seeded | `E2E_ANIMALS_TESTER_PASSWORD` | `animals.api.empty` (rename scenarios) |
| `testdata-admin` | master reset only | — | `E2E_TESTDATA_ADMIN_PASSWORD` | master reset (global setup) |
| manage-animals personas | unchanged (see `work/manage-animals/tests/test-plan.md`) | — | `E2E_*_PASSWORD` | manage-animals regression |

No new personas. Real-person names: none.

## Batches and reset keys

| Batch unit (feature file) | Keys → data | Default state (master) | Depends on | Footprint | Serial with | Exists? |
|---------------------------|-------------|------------------------|------------|-----------|-------------|---------|
| `animals.api` (`SystemRename.feature` reuses it) | `animals.api.empty`: no animals | `empty` | `personas.animals` | none created by the rename scenarios | animals batches (workers=1) | Yes (Dev Bot, manage-animals) |

No new batch keys. The master reset reseeds the renamed HasData rows (SystemBasicFeatures, system_messenger_dashboard, "System messenger").

## Scenarios → tests

| Scenario | Title (from ticket) | Layer | Test (name / tag) | Reset key (first step) | Persona | Status |
|----------|---------------------|-------|-------------------|------------------------|---------|--------|
| T-RENAME-001/S1 | Endpoints answer without v1 | API e2e (+ regression) | `@T-RENAME-001/S1` (GET /schemas/create-animal 200 + JSON object; GET /Animal 200; token from POST /Authorisation/SignIn); every manage-animals API scenario on versionless routes | `animals.api.empty` | animals-tester | Written |
| T-RENAME-001/S2 | The old v1 routes are gone | API e2e | `@T-RENAME-001/S2` (GET /v1/Animal and /v1/schemas/create-animal → 404) | `animals.api.empty` | animals-tester | Written |
| T-RENAME-001/S3 | No versioning machinery remains | Static check | static-checks.ps1 `[T-RENAME-001/S3]` (ApiVersion, Asp.Versioning, apiVersion}, x-api-version outside bin/obj) | — | — | Written |
| T-RENAME-001/S4 | Controllers are flattened | Static check | `[T-RENAME-001/S4]` (no V1 folder; 14 controller files under Controllers/{Area}, same set as the backup; no Controllers.V1 namespace) | — | — | Written |
| T-RENAME-001/S5 | Swagger lists every endpoint | API check (scripted) | GET https://localhost:7188/swagger/v1/swagger.json on the Test API: path / operation counts, no path with /v1 | — | — | Written (note: ticket says Development; the Test env serves the same document) |
| T-RENAME-001/S6 | Build and unit tests pass | Unit | `dotnet test Api.Framework.Tests --configuration Release` (all tests); build warnings from Dev Bot's build record | — | — | Written |
| T-RENAME-002/S1 | CORS policy is SystemUi | UI e2e + static | Every UI e2e scenario calls the API cross-origin (:3003 → :7188) and passes; `@T-RENAME-005/S4` records the calls; `[T-RENAME-002/S1]` SystemUi present, UnityUi absent in Program.cs | `animals.api.empty` | animals-tester | Written |
| T-RENAME-002/S2 | Tokens use system-login | API e2e (first Then) + Unit (second Then) | `@T-RENAME-002/S2`: iss and aud of a real sign-in token = system-login. `Api.Framework.Tests/Auth/TokenIssuerTests.cs` (traits `T-RENAME-002` / `T-RENAME-002/S2`, 5 tests, F-03): a unity-login issuer and/or audience fails `TokenService.CreateValidationParameters` (what JwtBearer uses → 401); random key per run, no faked token at runtime | `animals.api.empty` (e2e) | animals-tester | Written |
| T-RENAME-002/S3 | Seeded names are renamed by a new migration | Not automated (migration) + e2e indirect | Applying the migration to a database at the previous migration is a one-off on `api_framework_test`, already done by Dev Bot (counts 7 / 25 / 14 before and after). The master reset in global setup reseeds from the renamed HasData and succeeds | master | testdata-admin | Not automated — one-off migration step; Dev Bot evidence |
| T-RENAME-002/S4 | Old migrations are untouched | Static check | `[T-RENAME-002/S4]` SHA-256 of every pre-existing migration .cs vs the 11:20 backup zip | — | — | Written |
| T-RENAME-002/S5 | No plain System type or namespace | Static check | `[T-RENAME-002/S5]`; build passes (unit run builds Release) | — | — | Written |
| T-RENAME-002/S6 | Only intended Unity mentions remain | Static check | `[T-RENAME-002/S6]` case-insensitive "unity" outside bin/obj/Migrations, every hit reviewed | — | — | Written |
| T-RENAME-003/S1 | No unity identifiers or file names remain in code | Static check | `[T-RENAME-003/S1]` src, scripts, e2e/helpers; every hit reviewed against D10 | — | — | Written |
| T-RENAME-003/S2 | Imports resolve after the file renames | UI e2e (compile) + Dev Bot record | Every page used by the e2e suite compiles in `next dev`; e2e `tsc --noEmit` passes. `npm run build` not run by Test Bot (Dev Bot: typecheck pass) | — | — | Written (partial: no `npm run build`) |
| T-RENAME-003/S3 | The UI reads the new env var names | UI e2e + static | `@T-RENAME-005/S4` (calls go to the root dev:test sets in NEXT_PUBLIC_SYSTEM_API_ROOT); `[T-RENAME-003/S3]` no NEXT_PUBLIC_UNITY in src/scripts/e2e helpers | `animals.api.empty` | animals-tester | Written |
| T-RENAME-003/S4 | Validation errors carry the system keyword | UI e2e (message) + static (keyword) | `@T-ANIMAL-004/S4` duplicate name shows the server message on the field; `keyword: 'system'` in `system-schema-validation.ts` | `animals.form.bessie-exists` | animals-tester | Written |
| T-RENAME-003/S5 | Package is renamed | Static check | `[T-RENAME-003/S5]` package.json / package-lock name fields | — | — | Written (dependency tree not diffed) |
| T-RENAME-003/S6 | Existing system names are untouched | Static check + UI e2e | `[T-RENAME-003/S6]` counts now vs the 11:20 backup (same file scope); `@T-ANIMAL-003` decision-30 token scenarios read `--system-green` / `--system-red` | — | — | Written |
| T-RENAME-004/S1 | Sign-in page says System | UI e2e | `@T-RENAME-004/S1` | `animals.api.empty` | signed out | Written |
| T-RENAME-004/S2 | Session uses the new key | UI e2e | `@T-RENAME-004/S2` (the app accepts the session restored under system-auth-session and writes nothing under unity-auth-session) | `animals.api.empty` | animals-tester | Written (the sign-in itself is the setup project's real SignInForm sign-in) |
| T-RENAME-004/S3 | Theme uses the new key with no flash | UI e2e | `@T-RENAME-004/S3` (data-theme noted when `<body>` is created, before hydration) | `animals.api.empty` | animals-tester | Written |
| T-RENAME-004/S4 | Auth events still work in the same tab (reworded by Plan Bot, ticket saved 13:12:09; cross-tab out of scope) | UI e2e | `@T-RENAME-004/S4`: signed in with the session under system-auth-session; the app's real refresh path fires system-auth-refreshed (extra, supports S5's Then); sign-out fires system-auth-cleared, removes system-auth-session and the same tab shows the signed-out state | `animals.api.empty` | animals-tester | Written |
| T-RENAME-004/S5 | Token refresh still notifies | Not automated | Needs an access token that is about to expire; a scenario cannot shorten the token lifetime without a faked token or a clock hook | — | — | Not automated — no hook to expire a real token |
| T-RENAME-004/S6 | Old storage is ignored once | UI e2e | `@T-RENAME-004/S6` | `animals.api.empty` | signed out (stale unity-* entries) | Written |
| T-RENAME-005/S1 | API URL has no v1 | API e2e (indirect) | Every API step builds its URL with `getApiUrl()` from user `API_URL=http://localhost:5188`; global setup + API scenarios pass | master | — | Written (no direct unit test of the helper: e2e helpers have no unit runner) |
| T-RENAME-005/S2 | Default API URL | Not automated | `getApiUrl()` with API_URL unset; e2e helpers have no unit runner and the run uses the user value. Read-only code check: default `http://localhost:5188` | — | — | Not automated — Dev Bot scaffolding, no helper unit runner |
| T-RENAME-005/S3 | A stale v1 API_URL is reported | Not automated | As S2; read-only code check of the guard message | — | — | Not automated — as S2 |
| T-RENAME-005/S4 | Test UI uses the new root | UI e2e | `@T-RENAME-005/S4` (E2E_UI_API_ROOT unset → GET /Animal on https://localhost:7188, nothing with /v1/ or :7104) | `animals.api.empty` | animals-tester | Written |
| T-RENAME-005/S5 | http file and docs have no v1 | Static check | `[T-RENAME-005/S5]` Api.Framework.http, UI README, e2e README | — | — | Written |
| T-RENAME-006/S1–S4 | Rules / rule copies / Unity refs / env var names in docs | Not automated | Documentation owned by Dev Bot; no runtime behaviour. Review Bot full review (D8) | — | — | Not automated — docs, review-verified |
| T-RENAME-007/S1 | Selftest passes with new names | Static check (script run) | `node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` | — | — | Written |
| T-RENAME-007/S2 | Fixtures hold no old names | Static check | `[T-RENAME-007/S2]` | — | — | Written |
| T-RENAME-007/S3 | Gate passes on both targets | Static check (script run, not recorded) | `pre-handoff-checks.mjs --target all` without `--record` (Test Bot never writes `code:`) | — | — | Written |
| T-RENAME-008/S1 | Reset routes documented without v1 | Static check | `[T-RENAME-008/S1]` | — | — | Written |
| T-RENAME-008/S2 | Animals steps observe the new routes | UI e2e | `animals.steps.ts` observers (`isAnimalApiUrl` / `isAnimalListUrl`, API-root anchored); `@T-ANIMAL-003/S12` (paging observes GET /Animal) and `@T-ANIMAL-008/S2` ("no animal API list request" at line 275 counts correctly) | per scenario | per scenario | Written |
| T-RENAME-008/S3 | Real Unity references stay | Static check | `[T-RENAME-008/S3]` Unity.API / Unity.API.Tests / Unity.UI.Framework counts now vs the 11:20 backup | — | — | Written |
| T-RENAME-009/S1–S4 | Config routes / description / planning framework / Unity entries | Not automated | Config and planning docs owned by Plan Bot (done, History row 4); no runtime behaviour beyond the e2e run reading the config routes. Review Bot full review | — | — | Not automated — config / docs, review-verified |
| T-RENAME-010/S1–S2 | Review checklists | Not automated | Review Bot's own checklists | — | — | Not automated — review-owned docs |
| T-RENAME-011/S1 | UI calls API.Framework after N1 | UI e2e + read-only check | `@T-RENAME-011/S1` on the scenario shared with `@T-RENAME-004/S2 @T-RENAME-005/S4` (signed in on the Test UI: GET /Animal on the Test API root, no /v1/, nothing to port 7104). N1 (Given): `%TEMP%\tb-run\rename\probe-ui-apiroot.cjs` loads only `/auth/sign-in` on Neil's dev UI (:3003; no sign-in, clicks or writes) and reads the API root compiled into the client JS: expect `https://localhost:7088/`, no /v1, not the 7104/v2 fallback, no `NEXT_PUBLIC_UNITY_`. `.env*` never opened | `animals.api.empty` (e2e) | animals-tester (e2e); signed out (check) | Written |
| T-RENAME-011/S2 | e2e reaches versionless routes after N3 | API e2e | global setup: warm-up + `POST {API_URL}/TestData/Reset/master` succeeds (run log) | master | testdata-admin | Written |
| T-RENAME-011/S3 | Gate passes | Static check (script run, not recorded) | as T-RENAME-007/S3; `code.pre_handoff_gate` is Dev Bot's record | — | — | Written |
| T-RENAME-011/S4 | Fresh .auth and green e2e | UI e2e | old `e2e/.auth` files deleted unread; the setup project recreates them (system-login tokens); the full suite (manage-animals + system-rename) passes | per scenario | all | Written |
| T-RENAME-011/S5 | Nothing secret was printed | Static check (scan) | `%TEMP%\tb-run\scan-secrets.ps1` (six persona passwords + `APIFW_TEST_Jwt__Secret`; counts only) over the report, results, traces, `.auth`, Test Bot logs, unit trx; this feature's tests/ folder searched for env var values | — | — | Written |

Rows for T-RENAME-006, 009 and 010 are grouped above; the report and `handoff.md` `testing.results` list every S<n> separately.

## Blocked — scenario IDs not frozen

None. Every ticket has explicit `### Scenario: S<n>` headings.

## Flags for the planning agent

- ~~T-RENAME-004/S4 cross-tab question~~ **Resolved (Plan Bot, 13:10 BST):** same tab is enough; the app never had cross-tab sign-out and the rename changes only names. S4 reworded in the ticket (saved 13:12:09).
- T-RENAME-005/S5: the UI README (line 21) and e2e README (line 33) still contain the text "/v1" in sentences that say the root has **no** /v1. The literal Then is "no matches". Recorded as Pass on intent; Review Bot / Plan Bot to confirm the wording.
- T-RENAME-003/S6: the ticket's absolute counts (IsSystemAdmin 40, …) came from a wider search scope; Test Bot compares like with like against the 11:20 backup instead.

## Not automated / questions

- 002/S3, 004/S5, 005/S2, 005/S3: see the rows above for the reason and who could unblock. (T-RENAME-002/S2's second Then is covered by unit tests from run 2.)
- T-RENAME-003/S2 `npm run build` (F-07): deferred while Neil's dev UI runs on :3003.
- T-RENAME-006, 009, 010: documentation / config, checked by Review Bot.
