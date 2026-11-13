# Test report — system-rename — run 1

> **Addendum (13:15 BST) — T-RENAME-004/S4 now a full Pass.** Plan Bot ruled at 13:10 that same tab is enough (the app never had cross-tab sign-out; the rename only changes names) and reworded S4 in the ticket (file saved 13:12:09): *signed in with the session under "system-auth-session" → sign out in that tab → "system-auth-cleared" fires, "system-auth-session" is removed and the same tab shows the signed-out state*. The existing scenario already asserted all of that. I extended it to also drive the app's real refresh path (no JWT cookie, a fresh refresh token from an untraced Node sign-in → `getSession()` → `refreshAuthToken()`) and assert `system-auth-refreshed` fires, the app stays signed in with a new JWT cookie, and the session stays under `system-auth-session` (nothing under `unity-auth-session`). The refresh check is extra to the reworded S4; it observes S5's Then, but S5's Given (a token *about to expire*) is not reproduced, so S5 stays Not automated. Re-run of just that scenario (safety gate `api_framework_test` PASS 13:12:01; master reset + 6 setup + `@T-RENAME-004/S4`): **7/7 pass**, 13:12–13:12 BST. Password scan 0 hits; gate eol / secrets / docs-dup nextjs pass; `tsconfig.json` unchanged. New counts: **35 Pass · 0 Fail · 1 Waiting · 14 Not automated** (unchanged totals; 004/S4 no longer partial). Status stays **blocked** on T-RENAME-011/S1 (Neil's N1). Residual: on a failing run only, the retain-on-failure trace of that scenario could hold the short-lived refresh token passed to `addCookies` (as it can the access token in `usePersona`); never a password.

> **Tests waiting: T-RENAME-011/S1** (Neil's N1: rename the `NEXT_PUBLIC_UNITY_*` names in `.env.local`, then a plain `npm run dev`). Every automated scenario passes. Under `run-tests-and-report` step 7 (and Review Bot's F-44 reading) the run status is **blocked**, not passed. `testing.blocked_tests_allow_approval` applies.

| Field | Value |
|-------|-------|
| Run | 1 (`handoff.md` `testing.round`) · unit 2026-10-09 12:57–12:58 BST · e2e result of record: run 2, started 13:03:55 BST, finished 13:07:17 BST (run 1 12:59–13:03 had one test-defect failure, fixed) · test-bot |
| Test-fix round | 0 of 5 · first run on `code_to_test` (Dev Bot, 12:51 BST); run 1's failure was a Test Bot test defect fixed before reporting, not a routed-back failure |
| Environment | Test · UI `http://localhost:3003` via `npm run dev:test` (API root `https://localhost:7188/`, build dir `.next-test`; started 12:58 BST as a fresh process) · API.Framework launch profile **Test**, Release (`https://localhost:7188` / `http://localhost:5188`, "Hosting environment: Test", started 12:58 BST as a fresh process) · `API_URL=http://localhost:5188` (no `/v1`) · PostgreSQL DB `api_framework_test` (dedicated) |
| Safety gate | `APIFW_TEST_ConnectionStrings__LoginConnection` → Database=`api_framework_test`, host `localhost:5432`: **PASS** at 12:52, 12:59:07 (before run 1) and 13:03:49 (before run 2). Only the database name and host:port were printed |
| Master reset | OK in global setup for both runs (`resetMaster()` after Dev Bot's warm-up; it throws on failure, and every scenario reset afterwards succeeded) |
| Personas used | testdata-admin (master reset), animals-tester, animals-viewer, animals-usermanager, animals-nodisplayname, reference-data-tester (setup project; the six `.auth` sign-ins were regenerated) |
| Code under test | Dev Bot hand-off 2026-10-09 12:51:40 BST (`code_to_test: direct`). Not under git. Newest app / scaffolding file times: UI `src` 12:44:54, `e2e/helpers` 12:44:04, `e2e/setup` 12:43:54, `scripts` 12:44:04, API.Framework 12:44:54, so nothing changed after the hand-off |
| Commands | Unit: `dotnet test Api.Framework.Tests --configuration Release --logger "trx;LogFileName=system-rename-unit.trx"`. E2E: `npx bddgen` then `npx playwright test --workers=1 --reporter=list,json,html` in `UI.NextJs.Framework/e2e` (`PLAYWRIGHT_JSON_OUTPUT_NAME=test-results/system-rename-results.json`), launched detached after the safety gate, log `%TEMP%\tb-run\rename\e2e.log`. Static: `%TEMP%\tb-run\rename\static-checks.ps1` (read-only). Swagger and CORS preflight with `curl.exe`. Gate: `pre-handoff-checks.selftest.mjs`; `pre-handoff-checks.mjs --target all --checks lint,typecheck,eol,secrets,docs-dup` (no `--record`; unit already run above) |
| Result | **35 Pass · 0 Fail · 0 Blocked · 1 Waiting · 14 Not automated** (50 scenarios) — overall **blocked** (Tests waiting: T-RENAME-011/S1, owner Neil). **No code defects** |
| Layers | Unit (Release): 57 tests, 57 pass, 0 skip, 0 fail. E2E: **80 / 80 pass** in run 2 = 6 `setup` sign-ins + 67 manage-animals scenarios (regression) + 7 new `@system-rename` scenarios. 0 skipped, 0 flaky |
| Password scan | **0 hits** for the six `E2E_*_PASSWORD` values and `APIFW_TEST_Jwt__Secret` (raw, URL-, JSON-, HTML-escaped, base64; scanner self-test OK) in `playwright-report` (incl. its embedded zip), `test-results`, `e2e/.auth` (12 files), `%TEMP%\tb-run` logs (93 files, incl. run 1's failure copies), unit trx |
| E5 reset-first scan | Clean: every new `@system-rename` scenario starts with `Given the test data is "animals.api.empty"`; manage-animals scenarios unchanged |
| E1 front-end mock scan | Clean: no `page.route`, `context.route`, `route.fulfill`, `routeFromHAR`, MSW or stubbed fetch in the new steps. The rename steps use `page.on('request')`, `page.on('pageerror')`, `addInitScript` listeners (record only) and real sign-ins |

## Summary

This is the first test run for the system rename, alongside Review Bot's code review. I did my own ticket, T-RENAME-008. The animals network observers now match `/Animal` and `/schemas/create-animal` on the API root without `/v1`. The `auth.steps.ts` comment names `system-auth-session`. The test framework README, the reset skill, the reset safety checklist and the reset-handler template now show versionless routes and the `APIFW_TEST_`-prefixed env var names. I also folded in Review Bot's F-51 (`fillStable` no longer retries silently) and F-56 (no `.next-test-tb`, old processes replaced by fresh ones).

I added 7 e2e scenarios (`e2e/features/system-rename/SystemRename.feature`) for the runtime parts of T-RENAME-001, 002, 004 and 005, and a read-only static check script for the source-level Thens. Unit tests pass 57/57. The full e2e suite passes 80/80, so the **manage-animals regression is unchanged** (67/67 e2e; unit 57/57, up from 52 because of Dev Bot's 5 new regression tests). Run 1 had one failure, a race in my `cellByHeader` helper (test defect), which I fixed before run 2. **No code defects.**

## Results by ticket

| Ticket | Owner | Scenarios | Pass | Fail | Waiting | Not automated |
|--------|-------|-----------|------|------|---------|---------------|
| T-RENAME-001 | dev-bot | 6 | 6 | 0 | 0 | 0 |
| T-RENAME-002 | dev-bot | 6 | 5 | 0 | 0 | 1 |
| T-RENAME-003 | dev-bot | 6 | 6 | 0 | 0 | 0 |
| T-RENAME-004 | dev-bot | 6 | 5 | 0 | 0 | 1 |
| T-RENAME-005 | dev-bot | 5 | 3 | 0 | 0 | 2 |
| T-RENAME-006 | dev-bot | 4 | 0 | 0 | 0 | 4 |
| T-RENAME-007 | dev-bot | 3 | 3 | 0 | 0 | 0 |
| T-RENAME-008 | test-bot | 3 | 3 | 0 | 0 | 0 |
| T-RENAME-009 | plan-bot | 4 | 0 | 0 | 0 | 4 |
| T-RENAME-010 | review-bot | 2 | 0 | 0 | 0 | 2 |
| T-RENAME-011 | Neil + dev-bot + test-bot | 5 | 4 | 0 | 1 | 0 |
| **Total** | | **50** | **35** | **0** | **1** | **14** |

## Results by scenario

| Scenario | Layer | Test | Status | Evidence |
|----------|-------|------|--------|----------|
| T-RENAME-001/S1 | API e2e | `@T-RENAME-001/S1` + manage-animals API scenarios | Pass | GET /schemas/create-animal 200 with a non-empty JSON object, GET /Animal 200, sign-in token from POST /Authorisation/SignIn (run 2, 612 ms). All 15 `AnimalsApi.feature` scenarios pass on versionless routes. The old `/v1` response cannot be compared any more; the status and the steps' body assertions are unchanged |
| T-RENAME-001/S2 | API e2e | `@T-RENAME-001/S2` | Pass | GET /v1/Animal → 404 and GET /v1/schemas/create-animal → 404, with a valid bearer token |
| T-RENAME-001/S3 | Static check | `[T-RENAME-001/S3]` | Pass | 0 hits for ApiVersion / Asp.Versioning / apiVersion} / x-api-version in source. The only line the regex matched is `.claude/rules/api-framework-controllers.md:34`, guidance that says routes have **no** version |
| T-RENAME-001/S4 | Static check | `[T-RENAME-001/S4]` | Pass | No V1 folder. 14 controller files under `Controllers/{Animals,Auth,Directory,Examples,ReferenceData,Schemas,TestData}`, the same 14 as `Controllers/V1/...` in the 11:20 backup. 0 `Controllers.V1` |
| T-RENAME-001/S5 | API check | swagger.json | Pass | `GET https://localhost:7188/swagger/v1/swagger.json` 200: 46 paths, 66 operations, 0 paths with /v1 (matches Dev Bot's smoke). Served by the Test environment, not Development; the document is the same |
| T-RENAME-001/S6 | Unit | `dotnet test` Release | Pass | 57/57 pass, 0 skip. Build in the same run: 0 errors; 3 xUnit1031 warnings in `AnimalPoliciesTests.cs`, all pre-existing (Dev Bot's record lists the same) |
| T-RENAME-002/S1 | UI e2e + static + preflight | `@T-RENAME-005/S4`, all UI scenarios | Pass | Every UI scenario calls https://localhost:7188 from http://localhost:3003. Preflight OPTIONS /Animal with Origin http://localhost:3003 → 204, `Access-Control-Allow-Origin: http://localhost:3003`. `Program.cs`: SystemUi 2, UnityUi 0 |
| T-RENAME-002/S2 | API e2e | `@T-RENAME-002/S2` | Pass (first Then) | A real token's `iss` and `aud` are `system-login`. **Second Then not automated:** "a unity-login token is rejected with 401" needs a token signed with the Test JWT key, and Test Bot does not mint or fake tokens. Dev Bot's smoke covers it (unity-login token 401) |
| T-RENAME-002/S3 | Not automated | — | Not automated | Applying the migration to a database at the previous migration is a one-off. Dev Bot applied it to `api_framework_test` (features 7 / permissions 25 / tenant_features 14 before and after; 0 unity names). Indirect: master reset reseeds from the renamed HasData and succeeds in both runs |
| T-RENAME-002/S4 | Static check | `[T-RENAME-002/S4]` | Pass | 16 pre-existing migration files byte-identical (SHA-256) to the 11:20 backup; only `LoginDbContextModelSnapshot.cs` differs; none missing |
| T-RENAME-002/S5 | Static check | `[T-RENAME-002/S5]` | Pass | 0 hits for `namespace System`, `class System `, `Api.Framework.System`; Release build passes |
| T-RENAME-002/S6 | Static check | `[T-RENAME-002/S6]` | Pass | 15 hits for "unity" outside bin/obj/Migrations, all reviewed: real Unity.API / Unity UI text (D10) in `.claude` / `.cursor` rules and skills, `AGENTS.md`, one XML comment ("Unity's schema builder"), and `unity_login` (D7) in a test |
| T-RENAME-003/S1 | Static check | `[T-RENAME-003/S1]` | Pass | 0 file names with "unity". 23 text hits in comments / showcase copy / metadata, all naming the real Unity products (Unity UI, Unity.API, Unity.UI.Framework, UnityCookieService in Unity.UI.Framework), kept by D10. 0 identifiers |
| T-RENAME-003/S2 | UI e2e (compile) | full suite | Pass (partial) | Every page the suite visits compiles in `next dev`; e2e `tsc --noEmit` 0 errors; gate typecheck nextjs pass. `npm run build` not run by Test Bot (it would share the running UI's folder); Dev Bot's record has typecheck pass |
| T-RENAME-003/S3 | UI e2e + static | `@T-RENAME-005/S4` | Pass | The browser's API calls go to the root dev:test sets in `NEXT_PUBLIC_SYSTEM_API_ROOT` (https://localhost:7188). 0 `NEXT_PUBLIC_UNITY` in src, scripts, e2e/helpers |
| T-RENAME-003/S4 | UI e2e + static | `@T-ANIMAL-004/S4` | Pass | Duplicate name shows "An animal with this name already exists" on the field (as before). `system-schema-validation.ts:269` sets `keyword: 'system'` |
| T-RENAME-003/S5 | Static check | `[T-RENAME-003/S5]` | Pass | package.json name, package-lock name and lock root package name are all `system-ui-next`. Dependency tree not diffed |
| T-RENAME-003/S6 | Static check + UI e2e | `[T-RENAME-003/S6]`, `@T-ANIMAL-009/S7` | Pass | Like-for-like counts vs the 11:20 backup, same file scope: isSystemAdmin 9 / 9, @design-system 39 / 39, --system-red 8 / 8, --system-green 7 / 7, system-ui 2 / 2 (the ticket's absolute numbers came from a wider scope). Decision-30 token scenarios read `--system-green` / `--system-red` and pass |
| T-RENAME-004/S1 | UI e2e | `@T-RENAME-004/S1` | Pass | Heading "System Login", text "Sign in with your System credentials.", title "System UI Next" |
| T-RENAME-004/S2 | UI e2e | `@T-RENAME-004/S2` | Pass | The app accepts the session restored under `system-auth-session` (sign-out shown, grid loads) and nothing is written under `unity-auth-session`. The sign-in is the setup project's real SignInForm sign-in (no password typed in the scenario, F-41) |
| T-RENAME-004/S3 | UI e2e | `@T-RENAME-004/S3` | Pass | After choosing dark and reloading: `data-theme` is `dark` when `<body>` is created (before hydration), localStorage `system-theme` = `dark`, `unity-theme` absent |
| T-RENAME-004/S4 | UI e2e | `@T-RENAME-004/S4` | Pass | Reworded S4 (same tab; Plan Bot 13:10, see addendum). Session under `system-auth-session`; real refresh fires `system-auth-refreshed` (extra); sign-out fires `system-auth-cleared`, the tab goes to /auth/sign-in ("System Login") and `system-auth-session` is removed. Re-run 13:12: pass |
| T-RENAME-004/S5 | Not automated | — | Not automated | Needs an access token about to expire; a scenario cannot shorten a real token's lifetime without a faked token or a clock hook |
| T-RENAME-004/S6 | UI e2e | `@T-RENAME-004/S6` | Pass | With stale `unity-auth-session` and `unity-theme=dark`: shown as signed out with a sign-in link, theme `light` (default), no page error |
| T-RENAME-005/S1 | API e2e (indirect) | global setup + API steps | Pass | Every API call uses `getApiUrl()` with user `API_URL=http://localhost:5188`; the master reset and all API scenarios pass. No direct helper unit test (e2e helpers have no unit runner) |
| T-RENAME-005/S2 | Not automated | — | Not automated | `getApiUrl()` with API_URL unset; no helper unit runner and the run uses the user value. Read-only code check: default `http://localhost:5188` |
| T-RENAME-005/S3 | Not automated | — | Not automated | As S2. Read-only code check: the guard throws a message naming API_URL and telling the user to drop /v1, with no value printed |
| T-RENAME-005/S4 | UI e2e | `@T-RENAME-005/S4` | Pass | `E2E_UI_API_ROOT` not set (user level and process). Recorded calls include GET /Animal on https://localhost:7188; none with /v1/ or port 7104 |
| T-RENAME-005/S5 | Static check | `[T-RENAME-005/S5]` | Pass (on intent) | `Api.Framework.http`: 0. UI README line 21 and e2e README line 33 still contain the text "/v1" in sentences saying the root has **no** /v1. Literal Then is "no matches"; flagged below |
| T-RENAME-006/S1 | Not automated | — | Not automated | Dev Bot's rules / skills docs; Review Bot full review (D8) |
| T-RENAME-006/S2 | Not automated | — | Not automated | As S1 |
| T-RENAME-006/S3 | Not automated | — | Not automated | As S1 |
| T-RENAME-006/S4 | Not automated | — | Not automated | As S1 |
| T-RENAME-007/S1 | Script run | selftest | Pass | `pre-handoff-checks.selftest.mjs`: 64 ok, "self-test passed" |
| T-RENAME-007/S2 | Static check | `[T-RENAME-007/S2]` | Pass | 0 hits for unity-login and /v1/ in `ai-code-framework/scripts` (fixtures + selftest) |
| T-RENAME-007/S3 | Script run | gate `--target all` | Pass | 13:07:56: eol / secrets / docs-dup api-framework pass; lint (0 errors, 2 pre-existing warnings) / typecheck / eol / secrets / docs-dup nextjs pass. Unit check covered by the separate unit run (57/57). Not recorded: `code.pre_handoff_gate` is Dev Bot's (pass at 12:51:05) |
| T-RENAME-008/S1 | Static check | `[T-RENAME-008/S1]` | Pass | 0 "v1/TestData" in README + reset skill; `POST TestData/Reset/master` (3 lines) and `POST TestData/Reset/{scenarioKey}` present |
| T-RENAME-008/S2 | UI e2e | `@T-ANIMAL-003/S12`, `@T-ANIMAL-008/S2`, `@T-ANIMAL-005/S3` | Pass | Paging observes the real GET /Animal page-2 response (pageIndex=1), so the new matcher does match; "no animal API list request" (now line 307, was 275) counts 0 on the guarded pages; the cancel-delete observer sees no mutation |
| T-RENAME-008/S3 | Static check | `[T-RENAME-008/S3]` | Pass | Mentions in ai-test-framework now vs the 11:20 backup: Unity.API 21 / 21, Unity.API.Tests 11 / 11, Unity.UI.Framework 11 / 11 |
| T-RENAME-009/S1 | Not automated | — | Not automated | Plan Bot's config (done, History row 4); Review Bot full review. The e2e run itself uses versionless routes |
| T-RENAME-009/S2 | Not automated | — | Not automated | As S1 |
| T-RENAME-009/S3 | Not automated | — | Not automated | As S1 |
| T-RENAME-009/S4 | Not automated | — | Not automated | As S1 |
| T-RENAME-010/S1 | Not automated | — | Not automated | Review Bot's own checklists |
| T-RENAME-010/S2 | Not automated | — | Not automated | As S1 |
| T-RENAME-011/S1 | — | — | **Waiting** | Neil's N1 (`.env.local`) and a plain `npm run dev`. Agents never open `.env*`. Under dev:test the equivalent is covered by `@T-RENAME-005/S4` |
| T-RENAME-011/S2 | API e2e | global setup | Pass | `POST {API_URL}/TestData/Reset/master` (API_URL without /v1) succeeds in both runs |
| T-RENAME-011/S3 | Script run | gate `--target all` | Pass | As T-RENAME-007/S3; `code.pre_handoff_gate: pass` (Dev Bot, 12:51:05) |
| T-RENAME-011/S4 | UI e2e | full suite | Pass | Old `e2e/.auth` files (12) deleted without opening; the setup project recreated 12 at 13:04 with system-login tokens. Every manage-animals scenario that passed before the rename passes (67/67) |
| T-RENAME-011/S5 | Scan | `scan-secrets.ps1` | Pass | 0 hits (see the header). This report, the plan, the log and the `testing` block name env vars only |

## Failures

None in the result of record (run 2).

### Run 1 (12:59–13:03 BST) — T-ANIMAL-003/S4 "Last Amended is shown in the browser's local time" — test defect, fixed

- Expected (from the ticket): Bessie's Last Amended starts with "08/10/2026 14:05".
- Actual: `column "Last Amended" in headers []` at `animals.steps.ts:23` (`cellByHeader`). The error-context snapshot taken just afterwards shows the grid with the right value ("08/10/2026 14:05 Animals Tester"). `allInnerTexts()` does not wait, so the helper read the headers before the grid had rendered.
- Classification: **test defect** (Test Bot, F-47 helper from round 3 of manage-animals). Not a code defect, not env.
- Fix: `cellByHeader` now waits for the first header cell and the row to be visible before reading the headers. Run 2: passes (and every other `cellByHeader` user passes).
- Evidence: `%TEMP%\tb-run\rename\e2e-run1.log`, `%TEMP%\tb-run\rename\run1-failure\error-context.md` and `test-failed-1.png` (scan: 0 hits).

## Blocked / Waiting

| Scenario(s) | Reason | Owner |
|-------------|--------|-------|
| T-RENAME-011/S1 | Needs N1 (`NEXT_PUBLIC_UNITY_API_ROOT` / `_APP_ID` → `NEXT_PUBLIC_SYSTEM_*` in `.env.local`, root without /v1) and a plain `npm run dev` | human owner (Neil) |

## Not automated (14)

T-RENAME-002/S3 (one-off migration), 004/S5 (no way to expire a real token), 005/S2 and 005/S3 (no unit runner for e2e helpers; code read only), 006/S1–S4, 009/S1–S4, 010/S1–S2 (documentation / config owned by Dev Bot, Plan Bot and Review Bot, checked in Review Bot's full review). Partial coverage inside passing rows: 002/S2 (unity-login 401), 003/S2 (`npm run build`), 005/S5 (literal "/v1" in two README sentences). 004/S4 is no longer partial (addendum).

## Test Bot changes this run (test code and test docs only)

| File | Change |
|------|--------|
| `UI.NextJs.Framework/e2e/features/animals/animals.steps.ts` | T-RENAME-008: the `/v1` observer regexes (old lines 42, 44, 275) replaced by `isAnimalApiUrl` / `isAnimalListUrl`, which match `/Animal`, `/Animal/{id}` and `/schemas/create-animal` on any origin except the UI's, case-sensitive. F-51: `fillStable` fills once and fails with "value not kept after one fill" instead of retrying. Run-1 fix: `cellByHeader` waits for the header and the row |
| `UI.NextJs.Framework/e2e/features/common/auth.steps.ts` | T-RENAME-008: comment names `system-auth-session` |
| `UI.NextJs.Framework/e2e/features/system-rename/SystemRename.feature` (new) | 7 scenarios for T-RENAME-001/S1, S2, 002/S2, 004/S1–S4, S6, 005/S4 |
| `UI.NextJs.Framework/e2e/features/system-rename/system-rename.steps.ts` (new) | Steps for the above; real UI + API, no mocks, never logs a token or session value |
| `ai-test-framework/README.md` | Line 91: `APIFW_TEST_ConnectionStrings__LoginConnection` + `APIFW_TEST_Jwt__Secret`, read only when `ASPNETCORE_ENVIRONMENT=Test`. Line 93: `NEXT_PUBLIC_SYSTEM_API_ROOT` (dev:test default `https://localhost:7188/`). Line 105: `POST TestData/Reset/master` |
| `ai-test-framework/skills/add-test-data-reset/SKILL.md` | Lines 15 and 22: prefixed env var names, Test-only; `dotnet ef database update` hits the test DB only with `ASPNETCORE_ENVIRONMENT=Test`. Lines 54, 56, 65, 77: routes without `v1/` |
| `ai-test-framework/checklists/reset-endpoint-safety-checklist.md` | R8 (line 17): prefixed env var names, Test-only |
| `ai-test-framework/templates/reset-handler.md` | Line 3: `Controllers/{Area}/...`, no versioning attributes; controller skeleton `[Route("TestData")]` |
| `%TEMP%\tb-run\scan-secrets.ps1`, `load-env.ps1`, `start-api.ps1`, `start-ui-devtest.ps1` (Test Bot's scratch, outside the repos) | Scan adds `APIFW_TEST_Jwt__Secret`. load-env uses the prefixed names and drops stale `ConnectionStrings__LoginConnection`, `Jwt__Secret`, `NEXT_PUBLIC_UNITY_*`, `NEXT_DIST_DIR`, `E2E_UI_API_ROOT`. API starts in Release (Neil's dev API locks bin\Debug). UI starts with the default `.next-test` and API root. `start-ui-test.ps1` (old `NEXT_PUBLIC_UNITY_API_ROOT`) deleted |

Kept on purpose (T-RENAME-008 step 2): `examples/manage-animals-test-plan.md` (historical copy), `examples/unity-ui-e2e-reference.md` and every Unity.API / Unity.API.Tests / Unity.UI.Framework mention; `skills/write-api-unit-tests/SKILL.md:20` `Controllers/V1|V2|Shared` describes Unity.API, not API.Framework.

Environment (F-56): pids 42536 and 30188 were not running. The pre-rename `dev:test` UI on :3003 (pid 3036 and its npm / dev-test parents, started 10:57) was stopped and replaced. `.next-test-tb` deleted (nothing referenced it; `tsconfig.json` never listed it). `tsconfig.json` byte-identical before and after (SHA-256 checked after both runs and the gate). Neil's Development API (pid 35876, 5088/7088, started 10:58, pre-rename) was **left running**: it is his to restart (T-RENAME-011).

## Scaffolding and code notes (no defects)

- Dev Bot's e2e helpers (`authentication.ts`, `config.ts`, `sign-in-child.cjs`, `warm-up.ts`, `test-data.ts`) use the new names; no old session key, `/v1` or Unity string found. `config.ts` keeps `/v1` only in the stale-value guard (intended).
- `src/app/layout.tsx:8` metadata description still says "Unity-style design system". It describes the real Unity design system (D10) and is not user-visible text from T-RENAME-004, so not a defect; mentioned for Review Bot.
- `e2e/README.md:12,16` name `unity_login`, the real dev database (D7).

## Flags / questions

- ~~**Plan Bot:** T-RENAME-004/S4 cross-tab~~ **Resolved 13:10:** same tab only; S4 reworded (addendum).
- **Review Bot / Plan Bot:** T-RENAME-005/S5 literal "/v1" in two README sentences that say there is no /v1. Pass on intent; change the wording or the Then?

## Regression: manage-animals

The manage-animals e2e scenarios ran unchanged in the same suite: **67/67 pass** (plus 6 setup), the same as its round 3 addendum 2 (77/77 with the unit tests). Unit: 57/57 (52 manage-animals-era tests plus Dev Bot's 5 F-46 / TimeProvider regressions). The manage-animals report and `handoff.md` are not changed by this run; the only shared test-code changes are the versionless observers, F-51 and the `cellByHeader` wait.

## For the reviewing agent (test review, `review-tests`)

- Tested: T-RENAME-001/S1–S6, 002/S1, S2 (first Then), S4–S6, 003/S1–S6, 004/S1–S4, S6, 005/S1, S4, S5, 007/S1–S3, 008/S1–S3, 011/S2–S5
- Failing: none
- Waiting: T-RENAME-011/S1 (Neil, N1)
- Not automated: T-RENAME-002/S3, 004/S5, 005/S2, 005/S3, 006/S1–S4, 009/S1–S4, 010/S1–S2
