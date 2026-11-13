# Test report — manage-animals — run 1

| Field | Value |
|-------|-------|
| Run | 1 (`handoff.md` `testing.round`) · picked up 19:24 BST, finished 2026-10-08 19:27 BST · test-bot |
| Test-fix round | 0 of 5 · first run / not a fix re-run |
| Environment | **Not available.** Test · UI `<http://localhost:3003>` · API.Framework `<https://localhost:<api-port>/v1>` · PostgreSQL DB `<api_framework_test>` — all still `<placeholders>` in `testing`; no Test environment exists yet |
| Master reset | Not run: reset endpoint does not exist (owner `code`) and no Test DB (human owner) |
| Personas used | None (not created; owner `code`) |
| Code under test | not under git (api and ui); `handoff.md` `implementation.recorded_at` 2026-10-08T19:20:33+01:00 (Dev Bot, T-ANIMAL-009 + round-3 pass) |
| Commands | `dotnet build Api.Framework.sln --configuration Release` (in `ai-code-framework/api/API.Framework`, 19:24 BST) → **Build succeeded, 0 warnings, 0 errors** (run-tests-and-report step 2 fallback, since there is no test project). Unit `dotnet test Api.Framework.Tests/...` not run (project absent). E2E `npx bddgen && npx playwright test --grep "@T-ANIMAL-"` not run (no e2e folder) |
| Result | 0 Pass · 0 Fail · 0 Blocked · 75 Waiting · 0 Not automated — overall **blocked** |
| E5 reset-first scan | N/A — no e2e tests exist |
| E1 front-end mock scan | N/A — no e2e tests exist |

## Summary

First run, alongside Review Bot's code review. All 9 tickets now have frozen scenario IDs (75 scenarios); every one is planned in `tests/test-plan.md` with a layer, tag, reset key and persona. None could be written or run: Api.Framework.Tests, the Next.js e2e scaffolding, the reset endpoint / batch keys and the personas do not exist (owner `code`), and there is no Test environment or dedicated DB (human owner). The only check run was the API.Framework Release build, which passed. Result: **blocked**, 0 failures. Tests blocked: final approval is governed by `testing.blocked_tests_allow_approval: true` (flagged default; Neil decides at merge).

Breakdown of the 75 Waiting rows: 4 unit-only (need Api.Framework.Tests), 60 API / UI e2e (need e2e scaffolding, reset keys, personas, and the Test environment; some also unit), 11 component-level (need a component test runner or harness page).

## Results by scenario

| Scenario | Layer | Test | Status | Evidence |
|----------|-------|------|--------|----------|
| T-ANIMAL-001/S1 | Unit (EF model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S1")]` (planned, not written) | Waiting | Waiting — Api.Framework.Tests (code) |
| T-ANIMAL-001/S2 | Unit (model default SQL) + API e2e | `[Trait("Scenario", "T-ANIMAL-001/S2")]` + `@T-ANIMAL-001/S2` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-001/S3 | Unit (index metadata) + API e2e (real PostgreSQL index) | `[Trait("Scenario", "T-ANIMAL-001/S3")]` + `@T-ANIMAL-001/S3` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-001/S4 | API e2e | `@T-ANIMAL-001/S4` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-001/S5 | Unit (model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S5")]` (planned, not written) | Waiting | Waiting — Api.Framework.Tests (code) |
| T-ANIMAL-001/S6 | Unit (model metadata) | `[Trait("Scenario", "T-ANIMAL-001/S6")]` (planned, not written) | Waiting | Waiting — Api.Framework.Tests (code) |
| T-ANIMAL-001/S7 | Unit (seed data) | `[Trait("Scenario", "T-ANIMAL-001/S7")]` (planned, not written) | Waiting | Waiting — Api.Framework.Tests (code) |
| T-ANIMAL-002/S1 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S1")]` + `@T-ANIMAL-002/S1` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S2 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S2")]` + `@T-ANIMAL-002/S2` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S3 | Unit (service check + constructed unique violation) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S3")]` + `@T-ANIMAL-002/S3` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S4 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S4")]` + `@T-ANIMAL-002/S4` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S5 | Unit (fake clock) + API e2e (today / tomorrow from the server date) | `[Trait("Scenario", "T-ANIMAL-002/S5")]` + `@T-ANIMAL-002/S5` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S6 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S6")]` + `@T-ANIMAL-002/S6` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S7 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S7")]` + `@T-ANIMAL-002/S7` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S8 | Unit + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S8")]` + `@T-ANIMAL-002/S8` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S9 | Unit (mapper fallback) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S9")]` + `@T-ANIMAL-002/S9` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S10 | Unit (row kept, audit) + API e2e (404s) | `[Trait("Scenario", "T-ANIMAL-002/S10")]` + `@T-ANIMAL-002/S10` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S11 | API e2e (+ unit reflection test) | `@T-ANIMAL-002/S11` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S12 | API e2e | `@T-ANIMAL-002/S12` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-002/S13 | Unit (policy registration + reflection) + API e2e | `[Trait("Scenario", "T-ANIMAL-002/S13")]` + `@T-ANIMAL-002/S13` (planned, not written) | Waiting | Waiting — Api.Framework.Tests + e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S2 | UI e2e | `@T-ANIMAL-003/S2` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S3 | UI e2e | `@T-ANIMAL-003/S3` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S4 | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S4` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S5 | UI e2e, `timezoneId: 'Europe/London'` | `@T-ANIMAL-003/S5` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S6 | UI e2e | `@T-ANIMAL-003/S6` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S7 | UI e2e | `@T-ANIMAL-003/S7` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S8 | UI e2e | `@T-ANIMAL-003/S8` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S9 | UI e2e (also tagged `@T-ANIMAL-007/S1`) | `@T-ANIMAL-003/S9` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S12 | UI e2e (observe the real page-2 `v1/Animal` response) | `@T-ANIMAL-003/S12` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S13 | UI e2e | `@T-ANIMAL-003/S13` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S14 | UI e2e (also tagged `@T-ANIMAL-009/S1`) | `@T-ANIMAL-003/S14` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-003/S15 | UI e2e (also tagged `@T-ANIMAL-009/S2`; observe no request on click) | `@T-ANIMAL-003/S15` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S1 | UI e2e | `@T-ANIMAL-004/S1` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S2 | UI e2e + API read-back | `@T-ANIMAL-004/S2` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S3 | UI e2e | `@T-ANIMAL-004/S3` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S4 | UI e2e | `@T-ANIMAL-004/S4` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S5 | UI e2e | `@T-ANIMAL-004/S5` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S6 | UI e2e (browser date; time-zone sensitive) | `@T-ANIMAL-004/S6` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S7 | UI e2e | `@T-ANIMAL-004/S7` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S8 | UI e2e + API read-back | `@T-ANIMAL-004/S8` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S9 | UI e2e (also tagged `@T-ANIMAL-006/S3`) | `@T-ANIMAL-004/S9` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S10 | UI e2e + API read-back | `@T-ANIMAL-004/S10` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S11 | UI e2e (two personas) | `@T-ANIMAL-004/S11` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-004/S12 | UI e2e (Edit URL from reset ids) | `@T-ANIMAL-004/S12` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-005/S1 | UI e2e | `@T-ANIMAL-005/S1` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-005/S2 | UI e2e + API 404 | `@T-ANIMAL-005/S2` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-005/S3 | UI e2e (observe no DELETE) | `@T-ANIMAL-005/S3` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-005/S4 | UI e2e | `@T-ANIMAL-005/S4` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-005/S5 | UI e2e + API e2e (403 for both personas) | `@T-ANIMAL-005/S5` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-006/S1 | Component (needs runner / harness page) | `@T-ANIMAL-006/S1` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-006/S2 | Component (needs runner / harness page) | `@T-ANIMAL-006/S2` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-006/S3 | Covered by T-ANIMAL-004/S9 (both tags) | `@T-ANIMAL-006/S3` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-006/S4 | Component (no page renders read-only since decision 20) | `@T-ANIMAL-006/S4` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-006/S5 | UI e2e via Manage Animals (Attributes column) | `@T-ANIMAL-006/S5` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-007/S1 | Covered by T-ANIMAL-003/S9 (both tags) | `@T-ANIMAL-007/S1` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-007/S2 | UI e2e via Manage Animals | `@T-ANIMAL-007/S2` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-007/S3 | Component (no real page uses this configuration) | `@T-ANIMAL-007/S3` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-007/S4 | Component (as S3) | `@T-ANIMAL-007/S4` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-007/S5 | Component (as S3) | `@T-ANIMAL-007/S5` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-007/S6 | Component (as S3) | `@T-ANIMAL-007/S6` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-007/S7 | Component (as S3) | `@T-ANIMAL-007/S7` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-007/S8 | UI e2e on the reference-data types grid | `@T-ANIMAL-007/S8` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-007/S9 | UI e2e via Manage Animals | `@T-ANIMAL-007/S9` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-008/S1 | UI e2e | `@T-ANIMAL-008/S1` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-008/S2 | UI e2e (direct to `/examples/animals` and a form URL; observe no `v1/Animal` request) | `@T-ANIMAL-008/S2` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-008/S3 | UI e2e | `@T-ANIMAL-008/S3` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-008/S4 | UI e2e | `@T-ANIMAL-008/S4` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-008/S5 | UI e2e (direct to `/examples/animals/manage/item`) | `@T-ANIMAL-008/S5` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-008/S6 | UI e2e (direct to `/examples/animals/manage`) | `@T-ANIMAL-008/S6` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-009/S1 | Covered by T-ANIMAL-003/S14 (both tags) | `@T-ANIMAL-009/S1` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-009/S2 | Covered by T-ANIMAL-003/S15 (both tags) | `@T-ANIMAL-009/S2` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-009/S3 | UI e2e via Manage Animals (true and false cells) | `@T-ANIMAL-009/S3` (planned, not written) | Waiting | Waiting — e2e scaffolding / reset / personas (code); Blocked — Test env (human) |
| T-ANIMAL-009/S4 | Component (defaults exercised by T-ANIMAL-003/S14, S15; custom labels used by no real page) | `@T-ANIMAL-009/S4` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-009/S5 | Component (no real page renders a null boolean) | `@T-ANIMAL-009/S5` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |
| T-ANIMAL-009/S6 | Component (Manage Animals part via T-ANIMAL-003/S14 'neither cell is a Switch') | `@T-ANIMAL-009/S6` (planned, not written) | Waiting | Waiting — component runner / harness page (code) + e2e prerequisites |

## Failures

None (nothing ran).

## Blocked

| Scenario(s) | Reason | Owner |
|-------------|--------|-------|
| All unit layers (17 scenarios: T-ANIMAL-001/S1–S3, S5–S7; T-ANIMAL-002/S1–S10, S13) | Api.Framework.Tests project does not exist (not on disk, not in `Api.Framework.sln`) | `code` (implementing agent) |
| All API / UI e2e layers (60 scenarios) | No `UI.NextJs.Framework/e2e`, no Playwright / playwright-bdd, no `playwright.config.*`; `testing.e2e.nextjs.path` still a placeholder | `code` (implementing agent) |
| All e2e scenarios | Test-data reset endpoint (`v1/TestData/Reset/master`, `/{scenarioKey}`) and batch keys `animals.page.*`, `animals.grid.*`, `animals.form.*`, `animals.delete.*`, `animals.api.*`, `reference-data.types-grid.baseline` do not exist | `code` (implementing agent) |
| All e2e scenarios | Personas `testdata-admin`, `animals-tester`, `animals-tester-emailonly`, `animals-viewer`, `animals-usermanager`, `reference-data-tester` not defined | `code` (implementing agent) |
| T-ANIMAL-006/S1, S2, S4; T-ANIMAL-007/S3–S7; T-ANIMAL-009/S4–S6 | No component test runner / harness page (no real page exercises these) | `code` (implementing agent); Neil to decide if wanted |
| All e2e scenarios | No Test environment (API.Framework `Test` + Test UI), no dedicated PostgreSQL DB `<api_framework_test>`, `E2E_TEST_DATA_KEY` / persona password env vars not set; `testing` placeholders (`database.name`, `ui_base_url`, `api_base_url`, `personas.email_domain`, `personas.tenant`) unresolved | human owner (Neil) |
| — | Scenario IDs not frozen: **none** (all frozen at ~19:24 BST) | — |

## For the reviewing agent (test review, `review-tests`)

- Tested: none · Failing: none · Blocked / Waiting: all 75 (T-ANIMAL-001/S1–S7, T-ANIMAL-002/S1–S13, T-ANIMAL-003/S2–S9, S12–S15, T-ANIMAL-004/S1–S12, T-ANIMAL-005/S1–S5, T-ANIMAL-006/S1–S5, T-ANIMAL-007/S1–S9, T-ANIMAL-008/S1–S6, T-ANIMAL-009/S1–S6) · Not automated: none
- **Tests blocked** — record prominently; `testing.blocked_tests_allow_approval: true` (flagged default) applies. This run is not a test-fix round (blocked runs never count).
- No test code exists yet, so there is nothing to review for tagging, mocks or reset-first steps; the plan's tags and reset keys are ready for when scaffolding lands.
