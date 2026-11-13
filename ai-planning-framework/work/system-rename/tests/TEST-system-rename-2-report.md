# Test report — system-rename — run 2

| Field | Value |
|-------|-------|
| Run | 2 (`handoff.md` `testing.round`) · 2026-10-09 · unit 13:51 BST · e2e `@T-RENAME-011/S1` 13:45:59–13:46:31 BST · full e2e 13:46:44–13:50:22 BST · test-bot |
| Why this run | Plan Bot (13:24): Neil finished N1, the last thing T-RENAME-011/S1 was waiting for. Run 1 status was blocked on that scenario only |
| Test-fix round | 0 of 5. Not a test-fix round: run 1 ended blocked, not failed, so nothing was routed back (`feature-test.md`, Test-fix rounds: "Not rounds … blocked runs") |
| Environment | Test · **Test Bot's own Test UI on `http://localhost:3013`** via `npm run dev:test -- --port 3013` (API root `https://localhost:7188/`, build dir `.next-test`; started 13:45:49 BST, stopped after the run). `BASE_URL=http://localhost:3013` and `E2E_NO_WEB_SERVER=1` set in the run process only, after `load-env.ps1`; the run script refuses port 3003 and checks that a UI is listening on 3013 · API.Framework launch profile **Test**, Release, pid 32536 (Dev Bot restart 13:45; https 7188 / http 5188), not restarted by Test Bot · `API_URL=http://localhost:5188` · PostgreSQL `api_framework_test` |
| Not touched | Neil's dev UI on :3003 (pid 44972) and his dev API on 5088 / 7088 (dev DB). The only contact with :3003 was the read-only page load in the T-RENAME-011/S1 check (no sign-in, no clicks, no writes). No e2e run pointed at :3003 |
| Safety gate | `APIFW_TEST_ConnectionStrings__LoginConnection` → Database=`api_framework_test`, host `localhost:5432`: **PASS** at 13:46:01 (S1 run) and 13:46:40 (full run), each before global setup's master reset. Only the database name and host:port were printed |
| Master reset | OK in global setup for both runs |
| Personas used | testdata-admin, animals-tester, animals-viewer, animals-usermanager, animals-nodisplayname, reference-data-tester (setup project, real sign-ins on the Test UI) |
| Code under test | Run 1's code plus Dev Bot's 13:45 changes: CORS origins from `Cors:AllowedOrigins` (appsettings.Test.json adds localhost:3013), F-04 (`e2e/helpers/config.ts` rejects a whitespace-only `API_URL`) and F-05 (`scripts/dev-test.mjs` rejects a blank or /v1 `E2E_UI_API_ROOT`). Dev Bot's gate passed at 13:43 (unit 68/68) |
| Commands | Unit: `dotnet test Api.Framework.Tests -c Release -o Api.Framework.Tests\bin\tb-unit --logger "trx;LogFileName=system-rename-unit-2.trx"` (output folder deleted afterwards). E2E: `%TEMP%\tb-run\rename\run-e2e-3013.ps1 [-Grep @T-RENAME-011/S1]` → safety gate → `npx bddgen` → `npx playwright test --workers=1 [--grep …] --reporter=list,json,html` in `UI.NextJs.Framework/e2e` (`test-results/system-rename-2-results.json`). Read-only UI check: `node %TEMP%\tb-run\rename\probe-ui-apiroot.cjs <baseUrl> <expectedApiOrigin>`. Static: `%TEMP%\tb-run\rename\static-checks.ps1` (read-only, re-run 13:52). Swagger and CORS preflight with `curl.exe` |
| Result | **36 Pass · 0 Fail · 0 Blocked · 0 Waiting · 14 Not automated** (50 scenarios) — overall **passed**. **No code defects, no test defects** |
| Layers | Unit (Release): **68/68** pass (5 new F-03 tests). E2E: `@T-RENAME-011/S1` **7/7** (6 setup + 1); full regression **80/80** = 6 setup + 67 manage-animals + 7 `@system-rename`; 0 skipped, 0 flaky, 0 retries |
| Password scan | **0 hits** for the six `E2E_*_PASSWORD` values and `APIFW_TEST_Jwt__Secret` (raw, URL-, JSON-, HTML-escaped, base64; self-test OK; 0 read errors) in `playwright-report` (incl. its embedded zip), `test-results`, `%TEMP%\tb-run` logs (129 files), unit trx (3). **`e2e/.auth` is no longer opened or scanned** (12 files, counted by directory listing only) |
| E5 reset-first / E1 mock scans | Unchanged from run 1 and clean: every `@system-rename` scenario starts with `Given the test data is "animals.api.empty"`; no `page.route`, `route.fulfill`, HAR, MSW or stubbed fetch. The F-08 change adds no mock |

## Summary

Neil finished N1, so I re-ran the one scenario that was waiting and then the whole suite. **T-RENAME-011/S1 passes.** It has two parts:

- **On my own Test UI** (port 3013, `dev:test`): signed in, the browser's API calls go to the Test API root with no `/v1` and none to the Unity.API v2 fallback (port 7104). I tagged the existing scenario that checks exactly this with `@T-RENAME-011/S1`. It passed on its own and in the full run.
- **On Neil's dev setup (N1), read-only:** I loaded only the sign-in page of his dev UI on :3003 and read the API root its dev server compiled into the page: `https://localhost:7088/` (his dev API), no `/v1`, not the fallback, no `NEXT_PUBLIC_UNITY_` names. No sign-in, no clicks, no API calls, nothing written. I never opened `.env.local`. The same check on my Test UI read `https://localhost:7188/`, so it reads the right thing.

My first try at this run (13:30) could not sign in on port 3013 because the API's CORS policy only allowed 3003 and 4200 (4200 is a Windows-reserved port on this PC). Dev Bot moved the origins to config at 13:45. That attempt is not the result of record; it failed in setup before any scenario ran (environment, not a defect).

Unit 68/68, e2e 80/80, scan 0 hits. Review Bot's F-03 is done (5 unit tests: an old `unity-login` token is rejected), F-08 is done and exercised by `@T-RENAME-004/S6`, and F-07 (`npm run build`) is deferred because Neil's UI is running. **Status: passed, no blockers.**

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
| T-RENAME-011 | Neil + dev-bot + test-bot | 5 | 5 | 0 | 0 | 0 |
| **Total** | | **50** | **36** | **0** | **0** | **14** |

## Results by scenario

Rows that changed in run 2: 001/S5, 001/S6, 002/S1, 002/S2, 002/S6, 003/S2, 003/S3, 005/S5, 011/S1–S5. Every e2e row ran again and passed in the run-2 full run (80/80); static rows were re-run at 13:52 with the same results as run 1 except where noted. Other evidence is from run 1 and still applies (no change to the code it checks).

| Scenario | Layer | Test | Status | Evidence |
|----------|-------|------|--------|----------|
| T-RENAME-001/S1 | API e2e | `@T-RENAME-001/S1` + manage-animals API scenarios | Pass | GET /schemas/create-animal 200 with a non-empty JSON object, GET /Animal 200, sign-in token from POST /Authorisation/SignIn (run 2, 612 ms). All 15 `AnimalsApi.feature` scenarios pass on versionless routes. The old `/v1` response cannot be compared any more; the status and the steps' body assertions are unchanged |
| T-RENAME-001/S2 | API e2e | `@T-RENAME-001/S2` | Pass | GET /v1/Animal → 404 and GET /v1/schemas/create-animal → 404, with a valid bearer token |
| T-RENAME-001/S3 | Static check | `[T-RENAME-001/S3]` | Pass | 0 hits for ApiVersion / Asp.Versioning / apiVersion} / x-api-version in source. The only line the regex matched is `.claude/rules/api-framework-controllers.md:34`, guidance that says routes have **no** version |
| T-RENAME-001/S4 | Static check | `[T-RENAME-001/S4]` | Pass | No V1 folder. 14 controller files under `Controllers/{Animals,Auth,Directory,Examples,ReferenceData,Schemas,TestData}`, the same 14 as `Controllers/V1/...` in the 11:20 backup. 0 `Controllers.V1` |
| T-RENAME-001/S5 | API check | swagger.json | Pass | Run 2 (13:52): `GET https://localhost:7188/swagger/v1/swagger.json` 200: 46 paths, 66 operations, 0 paths with /v1 (same as run 1). Served by the Test environment, not Development; the document is the same |
| T-RENAME-001/S6 | Unit | `dotnet test` Release | Pass | Run 2 (13:51): **68/68** pass, 0 skip, 0 fail (57 from run 1 + Test Bot's 5 F-03 tests + Dev Bot's 6 CORS tests). Built to a throw-away folder under `Api.Framework.Tests\bin` (deleted afterwards) because the running Test API locks `bin\Release`. Build 0 errors |
| T-RENAME-002/S1 | UI e2e + static + preflight | `@T-RENAME-005/S4`, all UI scenarios | Pass | Every UI scenario calls https://localhost:7188 from http://localhost:3013 (Test Bot's Test UI). Dev Bot (13:45) moved the SystemUi origins to `Cors:AllowedOrigins` (defaults in appsettings.json; appsettings.Test.json adds http/https localhost:3013). Preflight OPTIONS /Animal: Origin http://localhost:3013 → 204 with `Access-Control-Allow-Origin: http://localhost:3013`; an unlisted origin (3999) → 204 with no allow-origin header. `Program.cs`: SystemUi 2, UnityUi 0 |
| T-RENAME-002/S2 | API e2e + Unit | `@T-RENAME-002/S2`, `TokenIssuerTests` | Pass | First Then: a real sign-in token's `iss` and `aud` are `system-login` (e2e). **Second Then now covered (F-03):** 5 unit tests in `Api.Framework.Tests/Auth/TokenIssuerTests.cs` (trait `T-RENAME-002/S2`, 5/5): defaults are system-login; a system-login token is valid; a full unity-login token, a unity-login issuer only and a unity-login audience only all fail `TokenService.CreateValidationParameters` (the parameters Program.cs gives JwtBearer, which answers 401) and `ReadUserId` returns null. The signing key is random per run, so no key in source and no faked token at runtime |
| T-RENAME-002/S3 | Not automated | — | Not automated | Applying the migration to a database at the previous migration is a one-off. Dev Bot applied it to `api_framework_test` (features 7 / permissions 25 / tenant_features 14 before and after; 0 unity names). Indirect: master reset reseeds from the renamed HasData and succeeds in both runs |
| T-RENAME-002/S4 | Static check | `[T-RENAME-002/S4]` | Pass | 16 pre-existing migration files byte-identical (SHA-256) to the 11:20 backup; only `LoginDbContextModelSnapshot.cs` differs; none missing |
| T-RENAME-002/S5 | Static check | `[T-RENAME-002/S5]` | Pass | 0 hits for `namespace System`, `class System `, `Api.Framework.System`; Release build passes |
| T-RENAME-002/S6 | Static check | `[T-RENAME-002/S6]` | Pass | Run 2: 23 hits (15 in run 1, all reviewed then). The 8 new hits are all in Test Bot's `TokenIssuerTests.cs`, which tests that the old `unity-login` issuer / audience is rejected (intended) |
| T-RENAME-003/S1 | Static check | `[T-RENAME-003/S1]` | Pass | 0 file names with "unity". 23 text hits in comments / showcase copy / metadata, all naming the real Unity products (Unity UI, Unity.API, Unity.UI.Framework, UnityCookieService in Unity.UI.Framework), kept by D10. 0 identifiers |
| T-RENAME-003/S2 | UI e2e (compile) | full suite | Pass (partial) | Every page the suite visits compiles in `next dev`; e2e `tsc --noEmit` passed in run 1. `npm run build` (F-07) **deferred**: Neil's UI is running on :3003 and a build would share the project folder |
| T-RENAME-003/S3 | UI e2e + static | `@T-RENAME-005/S4` | Pass | The browser's API calls go to the root dev:test sets in `NEXT_PUBLIC_SYSTEM_API_ROOT` (https://localhost:7188). 0 `NEXT_PUBLIC_UNITY` in src, scripts, e2e/helpers (run 2 static check). Neil's dev UI build inlines `NEXT_PUBLIC_SYSTEM_API_ROOT` with no `NEXT_PUBLIC_UNITY_` names (T-RENAME-011/S1 read-only check) |
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
| T-RENAME-005/S5 | Static check | `[T-RENAME-005/S5]` | Pass (on intent) | `Api.Framework.http`: 0. 3 README lines contain the text "/v1", all saying there is **no** /v1 or that a /v1 value is rejected: UI README line 21, e2e README line 33 (run 1) and e2e README line 60 (new, Dev Bot F-05: `E2E_UI_API_ROOT` blank or ending in /v1 fails fast). Literal Then is "no matches"; flag kept |
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
| T-RENAME-011/S1 | UI e2e + read-only check | `@T-RENAME-011/S1` (on the scenario shared with 004/S2 and 005/S4) + `probe-ui-apiroot.cjs` | **Pass** | **Test UI sign-in (When/Then):** on Test Bot's Test UI (http://localhost:3013, `npm run dev:test`, API root https://localhost:7188/) the signed-in browser's recorded API calls include GET /Animal on the Test API root, none contain /v1/ and none go to port 7104 (the Unity.API v2 fallback). Passed alone (13:46, 7/7 with setup) and in the full run. **Given (N1) — read-only check, passed (13:30:08):** `%TEMP%\tb-run\rename\probe-ui-apiroot.cjs` loaded only `/auth/sign-in` on Neil's dev UI (:3003): no sign-in, click or typing; 0 API calls on that page, so nothing written. The API root compiled into its client JS is https://localhost:7088/ (Neil's dev API; no /v1, not the 7104/v2 fallback, `NEXT_PUBLIC_SYSTEM_API_ROOT` set), 0 `NEXT_PUBLIC_UNITY_` names, heading "System Login", no "Unity" text. Control run of the same check on the Test UI read https://localhost:7188/. `.env.local` was never opened |
| T-RENAME-011/S2 | API e2e | global setup | Pass | `POST {API_URL}/TestData/Reset/master` (API_URL without /v1) succeeds in both run-2 e2e runs |
| T-RENAME-011/S3 | Script run | gate | Pass | Dev Bot's gate after the CORS fix: pass at 13:43 (unit 68/68). Test Bot's own `--target all` run is from run 1 (13:07:56); Test Bot changed no app code since |
| T-RENAME-011/S4 | UI e2e | full suite | Pass | The setup project signed in all six personas again on the Test UI (12 `.auth` files by directory listing; not opened). Every manage-animals scenario that passed before the rename passes (67/67) |
| T-RENAME-011/S5 | Scan | `scan-secrets.ps1` | Pass | 0 hits (see the header). `e2e/.auth` is no longer opened or scanned (files counted only). This report, the plan, the log and the `testing` block name env vars only |

## Failures

None in the result of record.

### Attempt at 13:30 BST (not the result of record) — environment

- `@T-RENAME-011/S1` on the 3013 Test UI: all six setup sign-ins failed with "Unable to reach System API (Failed to fetch) … CORS". Preflight from http://localhost:3013 had no `Access-Control-Allow-Origin`: `Program.cs` hard-coded 4200 / 3003. Port 4200 (allowed) is in a Windows excluded port range here (`listen EACCES`). 3003 is Neil's dev UI. Classification: **environment**. Fixed by Dev Bot at 13:45 (`Cors:AllowedOrigins`, Test adds 3013). No Test Bot code change. Safety gate PASS (13:30:16) before that attempt's master reset on `api_framework_test`.

## Blocked / Waiting

None. The run-1 blocker (T-RENAME-011/S1 waiting on N1) is cleared.

## Not automated (14)

T-RENAME-002/S3 (one-off migration), 004/S5 (no way to expire a real token), 005/S2 and 005/S3 (no unit runner for e2e helpers; code read only), 006/S1–S4, 009/S1–S4, 010/S1–S2 (documentation / config owned by Dev Bot, Plan Bot and Review Bot, checked in Review Bot's full review). Partial coverage inside passing rows: 003/S2 (`npm run build`, F-07 deferred) and 005/S5 (literal "/v1" in README sentences that say there is no /v1). 002/S2 is no longer partial (F-03).

## Test Bot changes this run (test code and test docs only)

| File | Change |
|------|--------|
| `API.Framework/Api.Framework.Tests/Auth/TokenIssuerTests.cs` (new, CRLF, no BOM) | F-03 / T-RENAME-002/S2: 5 xUnit tests (traits `Ticket=T-RENAME-002`, `Scenario=T-RENAME-002/S2`). Random signing key per run (no key literal). First draft expected an invalid-issuer error for a full unity-login token; the handler checks audience first, so that test now expects any `SecurityTokenException`, and a separate issuer-only test expects `SecurityTokenInvalidIssuerException` |
| `UI.NextJs.Framework/e2e/features/system-rename/system-rename.steps.ts` | F-08: "no page error occurred" no longer waits a fixed 500 ms; it waits for the `load` state and for `<html data-theme>` (set only by ThemeProvider's effect, so React has hydrated and run its effects), then checks the recorded page errors |
| `UI.NextJs.Framework/e2e/features/system-rename/SystemRename.feature` | Tag `@T-RENAME-011/S1` added to the scenario tagged `@T-RENAME-004/S2 @T-RENAME-005/S4` (its steps are S1's When / Then) |
| `%TEMP%\tb-run\` scratch (outside the repos) | `start-ui-3013.ps1`, `rename\run-e2e-3013.ps1/.cmd` (BASE_URL 3013 after load-env, refuses 3003, gate first), `rename\probe-ui-apiroot.cjs` (read-only API-root check), `scan-secrets.ps1` (no longer opens `e2e/.auth`; counts files only). Unused `*-4200` copies left from the CORS attempt |

`tsconfig.json` matches the baseline (SHA-256 B5AA3FC8…) after the Test UI stopped.

## Flags / questions

- **Review Bot / Plan Bot:** T-RENAME-005/S5 literal "/v1": now 3 README sentences (Dev Bot's F-05 added e2e README line 60). Pass on intent; change the wording or the Then? (carried from run 1)
- F-07 (`npm run build`) deferred while Neil's dev UI runs; can be done when :3003 is free.

## Regression: manage-animals

67/67 pass (plus 6 setup), unchanged from run 1. Unit 68/68.

## For the reviewing agent (test review, `review-tests`)

- Tested: T-RENAME-001/S1–S6, 002/S1, S2, S4–S6, 003/S1–S6, 004/S1–S4, S6, 005/S1, S4, S5, 007/S1–S3, 008/S1–S3, 011/S1–S5
- Failing: none
- Waiting: none
- Not automated: T-RENAME-002/S3, 004/S5, 005/S2, 005/S3, 006/S1–S4, 009/S1–S4, 010/S1–S2
