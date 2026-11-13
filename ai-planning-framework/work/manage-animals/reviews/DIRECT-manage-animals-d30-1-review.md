# DIRECT review — manage-animals Decision 30 cycle 1 (d30-1)

**Provisional — awaiting test review.** Code verdict only. `test_verdict` left untouched; no new Test Bot **test report** for this build (`tests/TEST-manage-animals-1-report.md` still 19:27). Test Bot at 20:28 wrote all 77 scenario tests and ran unit Animals Facts (20 pass / 2 skip); e2e/harness not run (`testing.status` still `blocked` on Test env / secrets). Do **not** use `blocked_tests_allow_approval`.

| Field | Value |
|-------|-------|
| Feature | manage-animals |
| Route | direct (`direct_scope: plan`) |
| Cycle | 1 (fresh Decision 30; **not** round 4 of the earlier cap) |
| Report | `reviews/DIRECT-manage-animals-d30-1-review.md` |
| Supersedes | `reviews/DIRECT-manage-animals-d29-1-review.md` (d29-1 Approve-with-comments is **SUPERSEDED** — do not merge on it) |
| Reviewed at | 2026-10-08T20:32:00+01:00 (Europe/London) |
| `review.code_verdict` | **Request changes** (Blocker F-31) |
| `review.test_verdict` | *(untouched; awaiting Test Bot)* |
| `review.verdict` | null (option B: provisional until test review) |
| `review.routed_to` | **code** |
| Stage / owner after this review | `changes-requested` / `dev-bot` |
| Live hosts | UI `http://localhost:3003` (Next `next dev`, PID started ~16:59); API `Api.Framework.exe` PID 28640 started **17:55:38** (Development profile on 5088/7088) — **stale vs Decision 30 + TestData scaffolding** (reset routes 404; F-13 MessageResponse not observed live) |

## Summary

Decision 30 filled-circle boolean cells are implemented and, after Neil's 20:19 knock-out follow-up, show as transparent Check/Close cut-outs (`Icon knockout="circle"`). Live fill-vs-row / fill-vs-hover contrast meets WCAG 1.4.11 (≥ 3:1) in light and dark. Accessible name / `role="img"`, non-interactive behaviour, dedicated boolean tokens, and unchanged `--system-green` / `--system-red` all check out. Test scaffolding structure is largely aligned with `ai-test-framework` (R2–R6, R9–R11, R13, R16, E1/E5/E16, persona rename, harness production guard, EntityGrid `sessionPermissions` override).

**Code verdict is Request changes** because of a **Blocker**: a real PostgreSQL password is committed in `appsettings.Test.json` and repeated in `e2e/README.md` (same value as Development `appsettings.json`, user `postgres`). That fails reset-endpoint safety **R8 / R12** (and R8a intent). Fix before any Test run that would rely on those files.

Follow-ups in this same cycle (Dev Bot 20:16:38 and 20:22:13) are included below: harness production guard, EntityGrid `sessionPermissions`, persona `animals-nodisplayname`, and knock-out glyph.

## Changes since last review (d29-1 — SUPERSEDED)

| Area | d29-1 | d30-1 |
|------|-------|-------|
| Boolean cell shape | Plain green tick / red cross coloured with `--system-green` / `--system-red` | Filled circle (`--app-boolean-true-fill` / `--app-boolean-false-fill`) with Check/Close |
| Glyph treatment (Neil 20:19) | N/A (ink glyphs) | Transparent cut-out via `Icon knockout="circle"` (evenodd); `--app-boolean-glyph` **removed** |
| Dark-mode contrast | Red cross failed WCAG 1.4.11 on dark row (2.09:1) — drove Decision 30 | Fill vs row / hover ≥ 3:1 light and dark (measured) |
| F-26 `role="img"` | Open (Minor) | **Resolved** (live `getByRole('img', { name: 'Yes' })` finds cells) |
| Test scaffolding | Blocked / not on disk | Api.Framework.Tests, e2e/playwright-bdd, TestData reset + batches + personas, component harness |
| Merge stance | Approve-with-comments (tests blocked) | **Do not merge on d29-1.** Fresh Decision 30 cycle |

## Findings (new IDs from F-31)

| ID | Severity | Area | File:line | Issue | Fix by |
|----|----------|------|-----------|-------|--------|
| **F-31** | **Blocker** | Security / test scaffolding (R8, R12, R8a; Neil: committed secrets = Blocker) | `api/API.Framework/Api.Framework/appsettings.Test.json` (LoginConnection); `ui/UI.NextJs.Framework/e2e/README.md:34` | Commits a real 8-char DB password for user `postgres`, **identical** to Development `appsettings.json`. DB name correctly targets `api_framework_test` (good), but R8 requires the connection string from env `ConnectionStrings__LoginConnection` only; R12 forbids putting the password in docs; R8a wants a DML+TRUNCATE-only runtime user, not the postgres superuser. Jwt Secret in the same file is a placeholder (OK). Production `TestData:Enabled=false` (OK). | Dev Bot: remove Password (and ideally Username) from committed `appsettings.Test.json`; document env-only override in README **without** any real secret; use a dedicated least-privilege test DB role. Rotate the exposed postgres password if it is still in use. |
| F-32 | Minor | Test scaffolding / auth helpers | `ui/UI.NextJs.Framework/e2e/helpers/authentication.ts:20-29` | Scaffolding `signInAs` still gets an API token and only sets `window.__E2E_ACCESS_TOKEN` (nothing in `src/` reads it; comment claims "real UI sign-in"). **Unused** after Test Bot's 20:28 write: scenarios use `features/common/auth.steps.ts` `signInViaUi` (real SignInForm fill + login-button + wait for redirect) — E1/E7 satisfied for the suite. Keep the helper from becoming a back door. | Dev Bot: delete `signInAs` (or rewrite it to call the same real UI path as `signInViaUi` and drop the window-token injection). |
| F-33 | Minor | Secrets in artefacts (R12) | `ui/UI.NextJs.Framework/e2e/playwright.config.ts:27` (`trace: 'retain-on-failure'`) + `helpers/test-data.ts:7-25` | Scenario resets and sign-ins use the **traced** `request` fixture. On failure the trace / HTML report records the `X-Test-Data-Key` header, persona passwords (sign-in body) and bearer tokens. `test-results/` and `playwright-report/` are git-ignored, so nothing gets committed, but artefacts get shared. `global-setup.ts` already uses an untraced context. | Use an untraced `request.newContext()` for reset / sign-in API calls (as global setup does), or turn tracing off for those calls. |
| F-34 | Minor | Dedicated test environment (E15) | `Api.Framework/Properties/launchSettings.json` (Test profile `https://localhost:7088;http://localhost:5088`); `e2e/helpers/config.ts:3,13` (defaults 3003 / 5088) | The Test API uses the **same ports** as the Development API, and the e2e defaults point at them. If the dev API is up, `npm test` hits Neil's dev API. It fails safe today (master reset → 404, verified live), but the two can't run side by side and it's easy to confuse them. | Give the Test profile distinct ports (and a Test UI port), or require `API_URL` / `BASE_URL` with no dev defaults. |
| F-35 | Minor | Unit-test proofs (R21) | `Api.Framework.Tests/TestData/TestDataGuardAndServiceTests.cs` | Missing proofs: R6 database-**name** mismatch (only "not Npgsql" is tested; `CreateNpgsqlModelOnly` could test a wrong name), R13a baseline check, and the pending-migrations refusal. | Add those tests (name mismatch is a model-only test). |
| F-36 | Nit | API / TestData | `Api.Framework/Controllers/V1/TestData/TestDataController.cs:24,38,42` | `Conflict(new { message = ex.Message })` returns raw exception text. Low risk (Test env only, key + persona required). | Return fixed client-safe messages; log the detail server-side. |
| F-37 | Nit | Formatting | `Api.Framework/Program.cs`, `TestData/ReferenceData/ReferenceDataTypesGridBatch.cs`, `Properties/launchSettings.json` (UTF-8 BOM); `grid-cell-renderers.tsx:78-79` (no blank line between functions) | BOMs on new or touched files; F-27 class. | Strip the BOMs; restore the blank line. |
| F-19 | Nit | Process / manifest | handoff `implementation.ui` form / intercepting routes | Still tagged T-ANIMAL-004 only; T-ANIMAL-008/S4–S6 not listed on those route files / `manage/page.tsx`. Unchanged from d29-1. | Add T-ANIMAL-008 scenario tags when next rewriting the manifest. |
| F-28 | Nit | Docs | `ui/.../design-system/README.md:17` | Still lists `Visibility` (not in `ICON_PATHS`); Check/Close are present but Visibility remains. | List real names only: Edit, Delete, Check, Close (and document `knockout` if desired). |
| F-29 | Nit | UI standards | `grid-cell-renderers.tsx` (`booleanCircleStyle` inline `color` / sizing) | Still inline styles (now `color: fill` for the knock-out SVG). Tokens are used; co-located CSS module preferred. | Move to `grid-cell-renderers.module.css`. |
| F-30 | Nit | UI / auth | `token-refresh.service.ts` | Double `unity-auth-cleared` on refresh failure still present (d29-1). | Remove the two redundant dispatches. |

**Blocker 1 · Major 0 · Minor 4 · Nit 7** (open: F-31…F-37 plus F-19, F-27, F-28, F-29, F-30). Severity basis: user instruction + `ai-test-framework/checklists/reset-endpoint-safety-checklist.md` R8/R12/R8a (severity.md not yet updated for option B).

## Prior findings status (d29-1)

| ID | Was | Now |
|----|-----|-----|
| F-26 | Minor — `aria-label` on role-less span | **Resolved** — `role="img"`; live AX `image`/"Yes"|"No"; `getByRole('img')` works |
| F-19 | Nit — partly done | **Still open** |
| F-27 | Nit — mixed EOL | **Still open** (plus F-37 BOM) |
| F-28 | Nit — README Visibility | **Still open** |
| F-29 | Nit — inline styles | **Still open** (shape changed; issue remains) |
| F-30 | Nit — double event | **Still open** |
| F-13…F-18, F-20…F-25 | Resolved / superseded in earlier rounds | Unchanged |

## Check 1 — Decision 30 boolean cells (incl. Neil 20:19 knock-out)

### Code

- `renderBooleanIconCell`: `role="img"`, `aria-label` / `title`, `data-boolean-value`; true/false use `<Icon knockout="circle" size="100%">` with `color: var(--app-boolean-*-fill)`; null/undefined → em dash + "Not set".
- `Icon.tsx`: new `knockout?: 'circle'` — single evenodd path (`KNOCKOUT_CIRCLE_PATH` + glyph), `data-icon-knockout="circle"`, `aria-hidden`, not focusable.
- `tokens.css`: `--app-boolean-true-fill` / `--app-boolean-false-fill` light `#609b44` / `#ef5673`, dark `#8dc374` / `#ff9aa8`; **`--app-boolean-glyph` removed**; `--system-green` `#72b453` / `--system-red` `#cf1337` unchanged.
- Animals grid uses `renderBooleanIconCell` only (no leftover switch cells).

### Live (Playwright 1.56.1 headless, own `ZZ Test Animal 202610081927 T/F` rows, deleted + GET 404)

| Measure | Light Yes | Light No | Dark Yes | Dark No | Pass? |
|---------|-----------|----------|----------|---------|-------|
| Fill hex (computed / sampled) | `#609b44` | `#ef5673` | `#8dc374` | `#ff9aa8` | ✓ |
| Fill vs row (sampled outsidePx) | **3.35** (#fff) | **3.36** | **5.61** (#2d3a4a) | **5.75** | ≥ 3:1 ✓ |
| Fill vs hover | **3.21** (#fafafa) | **3.22** | **4.52** (#3d4854) | **4.63** | ≥ 3:1 ✓ |
| Glyph treatment | Transparent hole; glyphPx ≈ row/white (not `#18181b`) | same | glyphPx ≈ `#2d3a4a` / hover | same | ✓ cut-out |
| `--app-boolean-glyph` | `(unset)` | | `(unset)` | | ✓ |
| `role` / name | `img` / Yes\|No | | | | ✓ |
| Clicks → API / dialogs / menus | 0 / 0 / 0 | | | | ✓ |
| Tab into cell (80×) | 0 landings | | | | ✓ |
| Switches in grid | 0 | | | | ✓ |
| Showcase `btn-red` / `btn-green` | `rgb(207,19,55)` / `rgb(114,180,83)` | | | | system tokens untouched ✓ |
| Callout success/error borders | system-green / system-red | | | | ✓ |

Note: for the Check cut-out, anti-aliased glyph-centre samples can read slightly off pure white (e.g. `#f7faf6`); **Decision 30 S7** is fill vs row / hover (outsidePx), which matches Plan Bot's numbers exactly. Glyph-vs-fill is no longer a separate token requirement after the knock-out change.

**Plan Bot doc lag (not a Dev Bot defect):** `tickets/T-ANIMAL-009-…` still names `--app-boolean-glyph` / `#18181b` in places. Treat as pending Plan Bot reword per Neil 20:19.

### Screenshots (best)

- `ko-02-cell-T-light-x4.png` — light Yes cut-out (white through Check)
- `ko-06-cell-T-dark-x4.png` — dark Yes cut-out (row through Check)
- `ko-07-cell-F-dark-x4.png` — dark No cut-out (row through Close)
- `19-harness-boolean-cells-light.png` — harness null/undefined + custom Furry/Not furry
- Also: `06`/`14` bool closeups (pre-knock-out run), `09-rows-dark-zoom.png`, menu / Escape / delete confirm shots under same folder

All under `/workspace/manage-animals-check/d30/`.

## Check 2 — Prior findings + regressions

- Menu not clipped (portalled, `visibleRatio=1`, items hit-testable) light and dark.
- Escape: closes menu → focus on trigger; closes Edit form → list; closes delete confirm → row remains.
- List-on-page: `/examples/animals`, H1 Manage Animals, Add on page, 0 dialogs at rest.
- CRUD: create T/F, edit load, cancel, delete, soft-deleted Edit URL shows not-found UI; API GET returned **ASP.NET ProblemDetails 404** (not the F-13 `MessageResponse` body). **Stale running API** (started 17:55) and/or ProblemDetails wrapping — code on disk has `NotFound(Missing("The animal was not found."))`. Do not restart per instructions; flag for Dev Bot when they next launch Test/Dev API.

## Check 3 — Test scaffolding (code review only; suites not re-run)

Dev Bot claims: Api.Framework.Tests **21/21** Release pass; UI + e2e `tsc` pass. Not re-executed here (per brief). Code review:

### Reset endpoint (R1–R22 highlights)

| Item | Result |
|------|--------|
| R2 Enabled + AllowedEnvironments | ✓ `TestDataRegistration.IsEnabled` |
| R3 Production + Enabled throws | ✓ unit-tested |
| R4 no TestData in base appsettings; Production Enabled false | ✓ |
| R6 RequiredDatabase name check | ✓ `TestDataGuard` |
| R7 dedicated DB name `api_framework_test` | ✓ |
| **R8 / R12 connection / secrets** | **✗ F-31** (committed password + README) |
| **R8a least-privilege user** | **✗** (postgres superuser in committed string) |
| R9 key FixedTimeEquals; missing env disables | ✓ |
| R10 JWT persona; R11 master = testdata-admin + AllowMasterReset | ✓ |
| R13 pending migrations refuse; TRUNCATE model tables; no DROP | ✓ (unit proves truncate list) |
| R14 footprint Clear | ✓ `AnimalsBatchSupport.ClearByFootprintAsync` |
| R15/15a keys `{feature}.{batch}.{state}`; SeedOrder | ✓ |
| R16 unknown key → 404 | ✓ |
| Personas `animals-tester`, **`animals-nodisplayname`** (renamed from emailonly; same GUIDs `…012` / `…112`), viewer, usermanager, testdata-admin, reference-data-tester | ✓ |
| Passwords from `E2E_*_PASSWORD` only | ✓ |
| Live probe on **running** API: `POST /v1/TestData/Reset/*` → **404** | Expected: process is Development, started before TestData wiring / not Test env |

### E2e (E1, E5, E7, E15, E16)

- **E1:** grep finds no `page.route` / `routeFromHAR` / MSW / stubbed fetch. Suite sign-in is real UI (`signInViaUi` in `auth.steps.ts`, Test Bot 20:28). Scaffolding leftover `signInAs` is unused/misleading → **F-32 (Minor)**.
- **E5** `Given the test data is "{key}"` → `resetScenario`.
- **E16** `global-setup.ts` → `resetMaster` as `testdata-admin`.
- **E7** personas from env; no password literals in TS.
- **E15:** the Test DB is separate (`api_framework_test`), but ports are shared with dev → **F-34**. Secrets → **F-31**. Trace artefacts → **F-33**.

### Api.Framework.Tests

- Covers registration, filter (key/401/persona/master), guard, truncate list, seed order, footprint clear, persona env-var naming (incl. nodisplayname).
- InMemory used for non-Postgres behaviour; Npgsql model-only for truncate/FK order (U14 OK).
- U13: no secrets in test code (env vars set in-process for filter tests).

### Component harness + production guard (Neil 20:09 / 20:16)

- `src/app/examples/test-harness/page.tsx`: `notFound()` when `NODE_ENV === 'production'`; `robots: { index: false, follow: false }`.
- **Not** linked from `SiteNav` (only `/`, reference-data, animals, sign-in).
- Live under `next dev`: `/examples/test-harness` present; boolean cells, custom Furry/Not furry, null/undefined, JsonSchemaForm JSON readouts, real `EntityGrid` grids for T-007 S3–S7.
- Production build not executed; code path is the standard Next production `NODE_ENV` guard — sufficient for this review.

### EntityGrid `sessionPermissions` (Neil / Dev Bot 20:16)

- Optional prop; `sessionPermissionsOverride ?? session?.permissions`.
- `hasAnyPermission`: empty/undefined permissions → deny when required non-empty; actions with no required stay visible (Open) — correct.
- **Only** `ComponentTestHarness` passes the prop. Product `AnimalsGrid` / reference-data grids pass `gridState` (+ headerActions) only — **does not weaken** Animals permission checks.
- Harness live: `animals_write` → Edit/Delete/Open/View report; `reports_view` → Open + View report; `none` → Open only on permissions grid; zero-visible grid loses Actions column without animals_write.

Live hygiene: all my rows (`ZZ Test Animal 202610081917`, `…1925`, `…1927` T/F) were deleted through the UI. Deleted IDs return GET 404, and 0 stamp rows remain. The `…1917` and `…1925` runs were interrupted part-way; their leftover rows were cleaned up afterwards. Another user's row (`triger`, saved 20:19 by System Administrator) was left untouched.

## Check 4 — Live process note

Do **not** restart servers. UI hot-reloaded Decision 30 + knock-out (verified). API process from 17:55 is **old**: TestData routes 404; deleted-animal GET shape may not match current controller. Dev Bot should relaunch under **Test** profile against `api_framework_test` after F-31 is fixed (human secrets / env).

## Out of scope / notes for Plan Bot

- Handoff History rows 33–37 etc. still show mojibake (`Â·`, `â†'`) introduced after 19:45 — **do not repair in this review**; Plan Bot ownership.
- `/workspace/d30` was briefly used by this agent then cleared (Plan Bot's area); work continues under `/workspace/rb-d30`.
- T-009 / plan text still reference `--app-boolean-glyph` / `#18181b` — Plan Bot reword pending (Neil 20:19).
- `api-framework-testing.mdc` change noted only.

## Hand-off

**To Dev Bot (code):** Request changes. Fix **F-31** (Blocker: committed DB password; env-only connection string; least-privilege test role). Then F-32…F-35 (Minor), F-36/F-37 and d29-1 Nits (F-19, F-27…F-30) if convenient. Hand back for Decision 30 review cycle 2.

**To Test Bot:** Tests are written (20:28) — thank you. Do not start a full e2e run until F-31 is cleared and a Test-env API + `api_framework_test` + env secrets are available. Scaffolding shape is otherwise reviewable. No test report for this build → this review stays **Provisional — awaiting test review**.

**To Plan Bot:** Reword T-009 / plan Decision 30 glyph wording for knock-out (remove `--app-boolean-glyph` / `#18181b` where stale); consider handoff mojibake cleanup.

**To Neil:** Merge decision stays blocked on code Request changes + pending tests. d29-1 must not be used for merge.
