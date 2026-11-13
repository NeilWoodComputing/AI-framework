# DIRECT review — manage-animals Decision 30 cycle 2 (d30-2)

**Provisional — awaiting test review.** Code verdict only. `test_verdict` left untouched; no new Test Bot **test report** for this build (`tests/TEST-manage-animals-1-report.md` still 19:27). Do **not** use `blocked_tests_allow_approval` while Test Bot will run.

| Field | Value |
|-------|-------|
| Feature | manage-animals |
| Route | direct (`direct_scope: plan`) |
| Cycle | **2** (Decision 30 re-review after d30-1 Request changes) |
| Report | `reviews/DIRECT-manage-animals-d30-2-review.md` (does **not** overwrite d30-1) |
| Prior | `reviews/DIRECT-manage-animals-d30-1-review.md` (Request changes — Blocker F-31). d29-1 remains **SUPERSEDED** |
| Reviewed at | 2026-10-08T20:50:00+01:00 (Europe/London) |
| `review.code_verdict` | **Approve with comments** (no Blocker/Major; Minor F-38; Nits F-39, F-40) |
| `review.test_verdict` | *(untouched; awaiting Test Bot)* |
| `review.verdict` | null (option B: provisional until test review) |
| `review.routed_to` | **test** |
| Stage / owner after this review | `in-review` / `review-bot` (option B: feature stays in-review; awaiting Test Bot report → Review Bot test review) |
| Live hosts | UI `http://localhost:3003` (next dev); API `Api.Framework.exe` PID 33000 started **20:26:54** on **5088/7088** (Development). **5188/7188 not listening** — Test launch profile not running. Live UI checks used Dev API (7088). |

## Summary

Re-reviewed Decision 30 knock-out boolean cells, instant-modal/CompanyLoader, and the d30-1 fix set (F-31…F-37 + open nits) against disk and a live headless check.

**All d30-1 findings are Resolved** (F-31 Blocker scrubbed; F-32…F-37 and F-19 / F-27…F-30 closed). Knock-out cells still pass WCAG 1.4.11 (≥ 3:1 fill vs row/hover light and dark). Instant Add/Edit pending shell paints in ~10–16 ms with CompanyLoader and tid `animal-form-modal-pending`. Unit `Api.Framework.Tests` **45 pass / 2 skip**; UI + e2e `tsc --noEmit` pass (temp copy / no write to Neil’s tree).

**Code verdict: Approve with comments.** One new **Minor** (F-38): browser Back during the pending shell leaves an orphaned modal over the previous history page. Two Nits: README duplicate paragraph inside the env table (F-39); csproj mixed EOL (F-40). Cancel / Esc on pending clear correctly with no late modal. Residual note (not re-opened): e2e API scenario steps still sign in via the traced Playwright `request` fixture (F-33 scope was resets + scaffolding sign-in — those are fixed).

## Changes since last review (d30-1)

| Area | d30-1 | d30-2 |
|------|-------|-------|
| F-31 Test DB password | **Blocker** — committed in `appsettings.Test.json` + README | **Resolved** — `LoginConnection: ""`; README env-only + least-privilege docs; `Password=` absent from Test/e2e sources (only Dev `appsettings.json` + design-time factory) |
| F-32 `signInAs` | Window-token back door | **Resolved** — real SignInForm path; no `__E2E_ACCESS_TOKEN` |
| F-33 traced reset | Traced `request` for reset/sign-in | **Resolved** for resets (`withUntracedRequest`); API feature steps still use traced fixture (residual note) |
| F-34 ports | Shared 5088/7088 | **Resolved** — Test profile **5188/7188**; e2e default `API_URL` 5188 (not listening live — Dev still on 5088/7088) |
| F-35 unit proofs | Gaps | **Resolved** — R6 name mismatch, R13 pending migrations, R13a baseline |
| F-36 Conflict messages | Raw `ex.Message` | **Resolved** — fixed client strings + server log |
| F-37 / F-27 BOM/EOL | BOM on Program/launchSettings; mixed EOL | **Resolved** on cited files (migrations still have historical BOMs; new csproj line → F-40) |
| F-28 / F-29 / F-30 | Open nits | **Resolved** — README Icon list + knockout; CSS module; redundant `unity-auth-cleared` removed |
| F-19 manifest | manage/page + form routes missing T-008/S4–S6 | **Resolved** — `manage/page.tsx` and `AnimalFormModal` tagged; intercepting routes remain T-004 (form) |
| Instant modal | Present | Live-verified pending host + loading.tsx + `schemaLoading \|\| !formVm` |
| Plan Bot T-009 wording | Pending | Closed by Plan Bot History **43** (not re-opened) |

## Findings (new IDs from F-38)

| ID | Severity | Area | File:line | Issue | Fix by |
|----|----------|------|-----------|-------|--------|
| F-38 | Minor | Instant modal / navigation | `PendingRoutedModalHost.tsx` + `pending-routed-modal.ts` (clear only on Cancel/Esc/`RoutedModal` mount — by design not on pathname) | Live: browser **Back** while `animal-form-modal-pending` is up navigates to `/` (Design system) but leaves the pending “Add Animal” shell + loader open (orphaned dialog). Cancel and Esc on pending clear with no late modal after 5+ s. | Dev Bot: clear pending on history pop / when `pathname` leaves the open-from list **and** no matching intercept is imminent; or dismiss pending whenever `fromPathname` is no longer in the history stack. |
| F-39 | Nit | Docs | `ui/UI.NextJs.Framework/e2e/README.md` (~L23 and ~L34) | The `LoginConnection` empty / fail-closed paragraph is duplicated, and one copy sits **inside** the env-var table (between header and rows), breaking Markdown table render. | Remove the in-table copy; keep one paragraph after the table. |
| F-40 | Nit | Formatting (F-27 class) | `api/API.Framework/Api.Framework.Tests/Api.Framework.Tests.csproj` | New `ProjectReference` line is LF in a CRLF file (1 LF / 34 CRLF). | Normalise EOL. |

**Blocker 0 · Major 0 · Minor 1 · Nit 2** (new: F-38; F-39, F-40). Residual F-33 note only (not counted as open).

## Prior findings status (d30-1 → d30-2)

| ID | Was (d30-1) | Now |
|----|-------------|-----|
| F-31 | Blocker — committed Test DB password | **Resolved** |
| F-32 | Minor — scaffolding `signInAs` token injection | **Resolved** |
| F-33 | Minor — traced reset/sign-in | **Resolved** (resets); residual: API `api.steps.ts` still uses traced `request` for bearer sign-in |
| F-34 | Minor — shared ports | **Resolved** (code); live Test ports not up |
| F-35 | Minor — unit proofs | **Resolved** (45/2 verified) |
| F-36 | Nit — Conflict messages | **Resolved** |
| F-37 | Nit — BOM / blank line | **Resolved** |
| F-19 | Nit — manifest tags | **Resolved** |
| F-27 | Nit — mixed EOL | **Resolved** (touched sources) |
| F-28 | Nit — README Visibility | **Resolved** |
| F-29 | Nit — inline styles | **Resolved** (`grid-cell-renderers.module.css`) |
| F-30 | Nit — double `unity-auth-cleared` | **Resolved** |
| F-26 | Resolved in d30-1 | Unchanged |
| F-13…F-18, F-20…F-25 | Resolved / superseded | Unchanged |

## Check 1 — Prior findings (evidence)

### F-31 (Blocker) — scrubbed

- `appsettings.Test.json`: `"LoginConnection": ""`; `TestData.RequiredDatabase` = `api_framework_test`; Production `TestData.Enabled` = false.
- `Program.cs`: empty/whitespace connection string throws with Test env-var guidance.
- `e2e/README.md`: env-only `ConnectionStrings__LoginConnection`; least-privilege role steps; **no** password literals; defaults document 5188/7188.
- Source scan `Password=` (excl. bin/obj/node_modules/reports): only Development `appsettings.json` + `LoginDbContextFactory.cs` (design-time).

### F-32 — `signInAs` is real UI

`authentication.ts`: fills `email-address` / `password`, clicks `login-button`, waits for leave `/auth/sign-in`. No `__E2E_ACCESS_TOKEN`. `signInViaApi` remains for API helpers only.

### F-33 — untraced resets

`test-data.ts`: `withUntracedRequest` wraps master + scenario resets (and the admin sign-in used for the key). `global-setup` / `reset-master` call the new signatures. **Residual:** `features/common/api.steps.ts` still uses the traced fixture for API scenario sign-ins.

### F-34 — ports

`launchSettings.json` Test profile: `https://localhost:7188;http://localhost:5188`. `e2e/helpers/config.ts` default `http://localhost:5188/v1`. Live: only 5088/7088 listening (Dev API from 20:26:54).

### F-35 — unit proofs

Added: `EnsureTestDatabase_DatabaseNameMismatch_Throws`, named-DB pass, `ResetMaster_PendingMigrations_RefusesBeforeTruncate`, `ResetBatch_BaselineMissing_ThrowsConflict_R13a` (+ `StubGuard` / `RecordingUnit`). **Verified:** `dotnet test Api.Framework.Tests -c Release` on a temp copy → **Passed: 45, Skipped: 2**.

### F-36…F-30, F-19 — as claimed

Client-safe Conflict messages + logging; Icon README (Edit/Delete/Check/Close + knockout); CSS module for boolean cells (no `--app-boolean-glyph`); token-refresh no longer double-dispatches; manage/page + AnimalFormModal carry T-ANIMAL-008/S4–S6.

## Check 2 — Decision 30 knock-out (live)

Own rows `ZZ Test Animal 202610081946 T/F` (ids `bc5ea994-…` / `08f593bf-…`), deleted + GET **404**, 0 stamp rows left.

| Measure | Light Yes | Light No | Dark Yes | Dark No | Pass? |
|---------|-----------|----------|----------|---------|-------|
| Fill (sampled) | `#609b44` | `#ef5673` | `#8dc374` | `#ff9aa8` | ✓ |
| Glyph vs fill (cut-out = row through hole) | **3.31** | **3.36** | **5.47** | **5.75** | ≥ 3:1 ✓ |
| Hover glyph vs fill | **3.17** | **3.22** | **4.41** | **4.63** | ≥ 3:1 ✓ |
| DOM | CSS module classes; `knockout=circle`; 1 path; `fill-rule=evenodd`; `role=img` Yes/No | | | | ✓ |
| `--app-boolean-glyph` | `(unset)` light + dark | | | | ✓ |
| Switches / knockout SVGs in grid | 0 / 6 | | | | ✓ |
| Cell click → API / dialogs | 0 / 0 | | | | ✓ |

## Check 3 — Instant modal loader (live)

| Check | Result |
|-------|--------|
| Add click → first paint | **11 ms**, `which=pending`, loader true (`animal-form-modal-pending`) |
| Slowed RSC (2.5 s) @400 ms | Pending dialog title “Add Animal”, CompanyLoader, Cancel present; URL still list |
| Hand-over | Pending clears; real `animal-form-modal` loads; `#name` visible |
| Pending Cancel | Clears in <300 ms; **no** late dialog after 5.3 s |
| Pending Esc | Same — clear, no late modal |
| **Pending browser Back** | URL → `/`; **orphaned** pending shell remains → **F-38** |
| Edit (slowed) | Pending “Edit Animal” → form with correct name |
| Dark pending | Shell + loader observed |

`loading.tsx` (add + edit intercept) use `RoutedModalLoadingFallback tid="animal-form-modal"`. Root layout mounts `PendingRoutedModalHost` (tid `${pending.tid}-pending`). Animals + reference-data grids pass pending options into `modalNavigate.open`.

## Check 4 — Scaffolding / harness / EntityGrid

| Item | Result |
|------|--------|
| Reset still Test-only + key + persona | Unchanged guards; F-36 messages safe |
| Harness `/examples/test-harness` (next dev) | Title “Component test harness”; `robots=noindex, nofollow`; `sessionPermissions` local (`animals_write`); **not** in SiteNav |
| Production guard | `notFound()` when `NODE_ENV === 'production'` (code; not re-built) |
| EntityGrid `sessionPermissions` | Optional override; **only** `ComponentTestHarness` passes it |
| UI / e2e tsc | Pass (`--incremental false`; `tsbuildinfo` mtime unchanged) |

## Screenshots

Under `/workspace/manage-animals-check/d30-2/` (and PC `%TEMP%\pw-rb-d30-2\shots`):

- `01-add-pending-shell-light.png` / `11-…-dark.png` — pending Add + CompanyLoader
- `02-add-form-loaded-light.png` / `05-edit-form-loaded-light.png`
- `03-pending-back-state.png` — **F-38** orphan over Design system
- `04-edit-pending-shell-light.png`
- `06`–`10` knock-out rows light/dark/hover
- `12`/`13` grid body dark/light
- `14-harness-dev-light.png`

## Out of scope / notes

- Test API on 5188/7188 not running — agents did not start it. Neil still supplies least-privilege role, `ConnectionStrings__LoginConnection`, `E2E_*` secrets, and password rotation for any previously exposed postgres password.
- `testing:` carve-out untouched.
- Plan Bot T-009 glyph reword (History 43) accepted; no ticket text re-opened.
- Handoff History mojibake in older rows left alone.

## Hand-off

**To Test Bot:** Code verdict is **Approve with comments** (provisional). Run / test-review when Neil’s Test env (5188/7188 + `api_framework_test` + secrets) is ready. Do not treat this as final merge approval. Stage stays `in-review` / owner `review-bot` (option B); `review.routed_to: test`; `test_verdict` still null.

**To Dev Bot:** Optional follow-ups **F-38** (browser Back clears pending), Nits F-39 / F-40. Residual: untraced context for API scenario sign-ins if traces are shared. Not blocking this cycle.

**To Plan Bot:** No doc action required for T-009 (History 43 done).

**To Neil:** Merge still waits on Test Bot (option B). Code side is clear of Blockers. Start Test API on 5188/7188 when ready; rotate any password that was in the scrubbed commit if still live.

---

## Test review — test round 2 (2026-10-09T09:05:00+01:00, Europe/London)

**Trigger:** Test Bot round 2 (`tests/TEST-manage-animals-2-report.md`, Fri 08:51; `testing.status: passed`, round 2, `test_fix_cycle: 0`). Code verdict (above) is unchanged: **Approve with comments** (F-38 Minor, F-39 / F-40 Nit open).

| Field | Value |
|-------|-------|
| `review.test_verdict` | **request-changes** (test defects) |
| `review.verdict` | null (final approval needs code_verdict **and** test_verdict) |
| `review.routed_to` | **testing** (Test Bot); human for the password rotation |
| Stage / owner | `in-review` / `review-bot` (unchanged; README "Testing alongside review" 7) |
| Test-fix cycle | This test review routes back → **test-fix round 1 of 5** once Test Bot starts the re-run (Test Bot adds the +1). Does **not** count toward `review.cycle` |
| Results reviewed | 76 Pass · 0 Fail · 1 Blocked (T-ANIMAL-007/S8, `@skip @fixme`, owner Plan Bot / Neil) · unit 45 pass / 2 Skip · e2e + harness 64/64 (run 5) |

### Summary

The run is genuine. Every frozen ID has a tagged test, with no front-end mocks. Every data scenario resets its own batch first, global setup does the master reset, personas are role-based, and the tests target only `api_framework_test` on 5188/7188. I found no code defects.

Two things block test approval:

1. **Security (F-41, Major).** The run-5 HTML report (`e2e/playwright-report/index.html`, all tests **passing**) stores three persona passwords in plain text: 42 matches, all on the password-field `Fill` step titles of the UI sign-in step. This happens on every run, pass or fail.
2. **Test gaps (F-42 / F-43, Minor).** T-ANIMAL-002/S13's Then "Program.cs registers exactly one animals policy …" has no working test. Its two reflection Facts are empty and skipped for a reason that no longer applies: the ProjectReference was added in d30-2. The S13 e2e covers only the GET endpoints, and S11 does not check "nothing is written".

### Answers to Test Bot's questions

- **(a) Harness has no reset, so no data: confirmed.**
  - `ComponentTestHarness.tsx` builds the `EntityGrid` state from local rows. It has no data provider, no `apiRoutes` and no fetch.
  - `JsonSchemaForm` takes an inline schema.
  - The scenarios never sign in.
  - Live probe (unsigned, :3003, harness controls exercised): **0** requests left the UI origin and **0** `/v1/` calls. The exemption from the reset rule is valid for `ComponentHarness.feature` only.
- **(b) The F4 dialog selector is acceptable but could be stronger (Nit F-45).**
  - `[role="dialog"][data-tid="animal-form-modal"]` is attribute-based, not positional. Absence checks stay on the bare tid, which is stricter. Good.
  - However, the route `loading.tsx` fallback is also a `role=dialog` with the same tid and the same "Add Animal" / "Edit Animal" heading. So "open in Add / Edit mode" can pass while the form is still loading, and during the fallback-to-form hand-over strict mode could see two matches.
  - Prefer `page.getByRole('dialog', { name: 'Add Animal' })`, and assert a loaded-form signal (for example the `name` field visible, or no `animal-form-modal-loading`) in the "open" steps.
- **(c) F6 `fillStable` does not hide Then failures, but it may mask a UX defect (Minor F-46).**
  - The helper waits for the field to be editable, fills, checks the value and retries for up to 10 s. Every Then still asserts the saved outcome, so a failed save or validation still fails.
  - It does hide what Test Bot saw in run 4: Date Born typed right after the Add modal opened was lost, while Name was kept. That fits the new behaviour where the form stays mounted while loading (`schemaLoading || !formVm`) and then re-initialises.
  - I could not reproduce it live: the UI on :3003 now points at the Test API (7188), the Development default user is not in `api_framework_test`, and I am not authorised to use persona credentials. It remains a possible code defect.
  - Fix: keep `fillStable` for robustness, but add one explicit no-retry check (fill once when the form becomes visible, wait, then assert the value is kept) or log every retry. Test Bot should tell Dev Bot if it fails.
- **(d) T-002 S11 / S13: partly genuine.** The skip is a finding for the **testing agent**.
  - The S11 behaviour is genuinely covered: 403 for `animals-viewer` on list, get, create, update, delete and the form schema. S12 does the same for `animals-usermanager`.
  - S11's last Then, "nothing is written", is not asserted (F-43).
  - The S13 e2e calls only GET list, GET by id and GET schema. Create, update and delete success under `animals_write` are not in the S13 test (create and delete pass elsewhere in the suite; update success only through the UI, T-004/S10).
  - S13's Then "Program.cs registers exactly one animals policy, AnimalsWrite, requiring the permission claim" has **no** test. The passing Fact only checks constants, and the two reflection Facts have empty bodies with `Skip` text saying the ProjectReference is missing.
  - That reason is now false: `Api.Framework.Tests.csproj` has referenced `..\Api.Framework\Api.Framework.csproj` since d30-2 (Dev Bot's F-35 work). The scaffolding gap is closed, so implementing and un-skipping them is Test Bot's job (F-42).

### Is one blocked scenario enough to make `testing.status` blocked?

**Yes.** `ai-test-framework/skills/run-tests-and-report/SKILL.md` step 7 defines the run status as:

- `passed`: every automated row passed;
- `failed`: any Fail;
- `blocked`: no Fail, but Blocked / Waiting rows that stop the run proving the feature.

T-ANIMAL-007/S8 ("existing text-button grids are unaffected") is a frozen scenario of this feature. It is Blocked, its owner is Plan Bot / Neil, and it is not run. Round 2 should therefore be **`blocked`**, not `passed`. The handoff `testing.summary` already says `blocked: 1`, which contradicts `status: passed`.

Consequences, from `handoff/README.md` "Testing alongside review" point 7 and default (2), the template `review.test_verdict` values, and `testing.blocked_tests_allow_approval: true`:

- A blocked row does not by itself stop approval. Once the test defects are fixed, the reviewing agent can record `test_verdict: blocked-noted` (or `approve` if S8 is unblocked and passes), and the final verdict can be approve-with-comments.
- If it is `blocked-noted`, **"Tests blocked: T-ANIMAL-007/S8"** must be recorded prominently in the report, `handoff.md` and the approval message. Neil decides at merge.
- A blocked run is **not** a test-fix round (point 9).

Test Bot should correct `status` and the report's Result line on the next run (F-44).

### Findings (test review; continue from F-41)

| ID | Severity | Area | File / artefact | Issue | Fix by |
|----|----------|------|-----------------|-------|--------|
| F-41 | **Major** | Security: secrets in artefacts (R12; general practice) | `ui/UI.NextJs.Framework/e2e/playwright-report/index.html` (run 5, Fri 08:39; embedded report zip, 5 JSON entries). Source: `e2e/features/common/auth.steps.ts` `signInViaUi` → `page.locator('[data-tid="password"]').fill(password)`. Same pattern in scaffolding `e2e/helpers/authentication.ts` `signInAs` | Playwright records `Fill "<value>"` as the step title, so every UI sign-in writes the persona password in plain text into the HTML report, **even on passing runs**. Counts: `E2E_ANIMALS_TESTER_PASSWORD` 37, `E2E_ANIMALS_VIEWER_PASSWORD` 4, `E2E_ANIMALS_USERMANAGER_PASSWORD` 1 (all on password `Fill` titles). On failure, traces and `error-context.md` add more copies (seen in run 2). The report is git-ignored, but it is an artefact handed to reviewers and Neil. | **Testing agent:** sign in without the value reaching a step title or trace. For example, do one real UI sign-in per persona in an untraced setup step and reuse its `storageState` (real auth, not faked), or enter the password through a call whose value is not reported, wrapped in an untraced / boxed step. Then re-scan the HTML report, traces and `error-context` (expect 0). **Implementing agent:** apply the same to scaffolding `signInAs` (or delete it; it is unused) and add a sign-in setup project to `playwright.config.ts` if that is the chosen route. **Human (Neil):** rotate the animals-tester, animals-viewer and animals-usermanager test passwords once the fix is in, and delete the current `playwright-report/` (I did not delete anything). |
| F-42 | Minor | Test completeness (T-ANIMAL-002/S13 Then; S11) | `Api.Framework.Tests/Animals/AnimalPoliciesTests.cs:24-42` | `AllAnimalEndpoints_RequireAnimalsWritePolicy` and `AnimalEndpoints_RejectUsersWithoutAnimalsWrite_ByPolicy` have empty bodies and `Skip` because of a missing ProjectReference that now exists (`Api.Framework.Tests.csproj:31`). Nothing tests S13's "Program.cs registers exactly one animals policy, AnimalsWrite, requiring claim animals_write". | **Testing agent:** implement both Facts (reflect `[Authorize(Policy = "AnimalsWrite")]` on every AnimalController / AnimalSchemaController action, no `[AllowAnonymous]`; assert exactly one animals policy and its claim requirement, for example from the built service provider's `AuthorizationOptions`) and remove the `Skip`. |
| F-43 | Minor | Assertions vs Then (T-ANIMAL-002/S11, S13) | `e2e/features/animals/AnimalsApi.feature` (S11, S13) | S13 e2e only asserts GET list, GET by id and GET schema; the scenario's "create, update or delete … with valid input → each succeeds" is missing. S11 lacks "nothing is written via Animals" (no read-back after the forbidden POST / PUT / DELETE). | **Testing agent:** add create, update and delete success with valid input to S13, and in S11 read back as `animals-tester` (Bessie unchanged, no new row). |
| F-44 | Minor | Process: test status | handoff `testing.status: passed` (`summary.blocked: 1`); report Result line | Under `run-tests-and-report` step 7, one Blocked frozen scenario (T-007/S8) makes the run `blocked`, not `passed`. | **Testing agent:** set `status: blocked` (with the blocker and owner Plan Bot / Neil) on the next write and in the report. |
| F-45 | Nit | Selector strength (F4) | `e2e/features/animals/animals.steps.ts:51-86` | Attribute selector `[role="dialog"][data-tid="animal-form-modal"]` also matches the `loading.tsx` fallback dialog (same tid and heading), so "open in Add / Edit mode" can pass before the form loads, and the hand-over could trip strict mode. | **Testing agent:** `getByRole('dialog', { name })`, plus a loaded-form check in the "open" steps. |
| F-46 | Minor | Possible masked defect (F6) | `e2e/features/animals/animals.steps.ts:428-435` `fillStable` | Retrying the fill for up to 10 s hides the run-4 "early Date Born input lost" behaviour. Not reproduced by Review Bot (no persona access; the Dev user is not in the Test DB). | **Testing agent:** add one explicit no-retry early-fill check (or log retries); if it fails, report it as a code defect. **Implementing agent:** look at whether form re-initialisation after `schemaLoading` / `formVm` wipes user input. |
| F-47 | Nit | Positional selectors | `e2e/features/animals/animals.steps.ts:172-186` (`td` `nth(4)` / `nth(5)`) | Grid cell checks use column indexes rather than a header or cell tid. They break silently if columns are reordered. | **Testing agent:** locate cells by column header / `data-tid`. |

**Test review: Major 1 · Minor 4 · Nit 2.** No code defects. T-ANIMAL-007/S8 is Blocked (owner Plan Bot / Neil), which is not a defect.

### Standard checks

| Check | Result |
|-------|--------|
| Every frozen ID has a result and a real test; tags are explicit IDs | ✓ 77/77 listed. 73 distinct `@T-ANIMAL-NNN/Sn` tags across 65 e2e scenarios (64 run + T-007/S8 skipped), plus unit-only T-001 S1, S5, S6, S7 (`[Trait("Scenario", …)]`). No positional naming. Shared tests carry both IDs (e.g. `@T-ANIMAL-003/S14 @T-ANIMAL-009/S1`). Gaps in the S13 Then (F-42 / F-43) |
| No front-end mocks | ✓ No `page.route`, `routeFromHAR`, `route.fulfill`, MSW, `addInitScript`, stubbed fetch, cookie or localStorage injection or token faking in `features/`, `helpers/`, `support/` or `global-setup.ts`. Sign-in goes through the real SignInForm |
| Reset first; master reset in global setup | ✓ All 53 non-harness scenarios (incl. skipped T-007/S8) start with `Given the test data is "<key>"` (step 1). `global-setup.ts` → `resetMaster()` (testdata-admin, untraced). Harness exemption confirmed (a) |
| Assertions check the Then outcomes | ✓ Mostly (exact messages, API read-back, 404 / 403, computed colours and contrast, no-request observers); exceptions F-42 / F-43 |
| Role-based personas; no secrets in test code | ✓ testdata-admin, animals-tester, animals-nodisplayname, animals-viewer, animals-usermanager, reference-data-tester. Passwords only from `E2E_<NAME>_PASSWORD`; no literals (grep). Artefact leak → F-41 |
| Only `api_framework_test` and 5188/7188 | ✓ `config.ts` default `http://localhost:5188/v1`. No 5088 / 7088 / dev DB references in test code (only a comment). Report safety gate: Database `api_framework_test`. Live: :3003 calls go to **7188**. Note: the UI's `.env.local` still points at the dev API; Test Bot used a process override (an env / config item, owner code / Neil) |
| Traced-context fix in `features/common/api.steps.ts` | ✓ In place: `withUntracedRequest` + `withApiAs` wrap every API sign-in and call (fresh `request.newContext`, disposed). The reset key value appears **0** times in artefacts (only the header *name* appears in reset step metadata) |
| Unit artefact | trx Fri 00:55: 0 secret matches |

### Security scan (counts and paths only; no values printed)

The script loaded the values from Windows env (names: 6 persona passwords, `E2E_TEST_DATA_KEY`, `ConnectionStrings__LoginConnection` + its password part), searched raw, URL-escaped and JSON-escaped forms, opened every zip and the HTML report's embedded base64 zip, and also matched JWT / `Bearer eyJ` / connection-string patterns.

| Location | Files | Result |
|----------|-------|--------|
| `e2e/test-results/` | 2 (run 5 JSON + `.last-run`) | 0 secrets, 0 tokens. **0** `error-context.md`, **0** trace zips (all passed) |
| `e2e/playwright-report/index.html` (+ embedded zip, 7 entries) | 1 | **HIT:** 5 entries contain persona passwords (tester 37, viewer 4, usermanager 1); reset key 0; JWT / Bearer 0; connection string 0 |
| `e2e/cucumber-report/index.html` (Fri 00:56) | 1 | 0 |
| `e2e/blob-report/` | absent | — |
| `Api.Framework.Tests/TestResults/manage-animals-unit.trx` | 1 | 0 |
| Stray `error-context.md` / `trace.zip` elsewhere under `e2e/` | 0 | — |
| `%TEMP%\playwright-artifacts-*` | 287 dirs (Jan–8 Oct), 1 file of 24 bytes | No content |
| `.gitignore` | `playwright-report/`, `test-results/`, `cucumber-report/` ignored | Not committed (not under git anyway) |

**Earlier exposure (run 2 `error-context.md`, animals-viewer password):** it has been wiped from disk; 0 copies remain in `test-results/`. Under R12 and general practice, though, a secret written to a shareable artefact counts as exposed even after deletion. And the current report re-exposes animals-viewer, animals-tester and animals-usermanager. **Recommend rotating all three persona passwords after F-41 is fixed** (test DB only; Neil sets the env values), deleting the current `playwright-report/`, and re-scanning after the next run.

### Hand-off (test review)

- **To Test Bot:** test review is **request-changes**, routed to testing (stage stays `in-review`; this is test-fix round 1 of 5 when you start the re-run). Fix F-41 (no passwords in reports, traces or error-context; re-scan to 0), F-42 (implement and un-skip the S11 / S13 reflection Facts, since the ProjectReference exists), F-43 (S13 create / update / delete success; S11 nothing-written read-back), F-44 (`status: blocked` while T-007/S8 is skipped), and optionally F-45 / F-46 / F-47. Then re-run and report round 3.
- **To Dev Bot:** no code defects from the tests. Open code items from d30-2: F-38 (Minor), F-39 / F-40 (Nit). Related to F-41: scaffolding `signInAs` has the same `fill(password)` pattern (unused; delete or fix), and a sign-in setup project in `playwright.config.ts` may be needed. Related to F-46: check for input loss on form re-initialisation. Env: give the UI a repeatable Test API root (for example a `dev:test` script) instead of the dev `.env.local`.
- **To Neil:** not approved yet (code approve-with-comments; tests request-changes). Please rotate the animals-tester, animals-viewer and animals-usermanager test passwords after the F-41 fix, and delete `e2e/playwright-report/`. T-ANIMAL-007/S8 still needs a Plan Bot / Neil decision on the reference-data baseline rows. Until then the next round will be **Tests blocked: T-007/S8**; approval is allowed by default (2), but recorded prominently.

## Test review — test round 3 (2026-10-09T09:58:00+01:00, Europe/London)

**Trigger:** Test Bot round 3 = test-fix round 1 of 5 (`tests/TEST-manage-animals-3-report.md`: main body 09:26, Addendum 09:48, Addendum 2 09:56 BST). Also covers Dev Bot's code and scaffolding deltas of 09:08 and 09:35 BST.

| Field | Value |
|-------|-------|
| `review.test_verdict` | **approve** (T-ANIMAL-007/S8 unblocked and passing, so this is not blocked-noted) |
| `review.code_verdict` | **approve-with-comments** (d30-2, plus the code delta reviewed here; only Nits are open) |
| `review.verdict` (final) | **approve-with-comments** (`testing.final_approval_requires: [code_review, test_review]` both met) |
| Stage / owner / routed_to | `approved` / `human` (pickup pending) / `human`. No fixes are required; Neil makes the merge decision |
| Results reviewed | **77 Pass · 0 Fail · 0 Blocked · 0 Not automated** (`testing.status: passed`, round 3, `test_fix_cycle: 1`). Unit 52/52, 0 Skip (09:42; no API change since 09:08:48). E2e run 11 (09:49–09:52 BST): 73/73 = 67 scenarios + 6 setup sign-ins, 0 flaky, 0 skipped |
| Test-fix cycle | 1 of 5 used. It does not count toward `review.cycle`, which stays 2 |

### Summary

Every round-2 test finding (F-41 to F-47) is fixed. F-46 turned out to be a real **code** defect, which Dev Bot fixed with regression tests. The persona-password leak (F-41, Major) is closed in a structural way: the setup sign-in now runs in a separate, untraced Node process, and no scenario types a password. My own scan of the current artefacts finds 0 persona passwords, 0 reset-key copies and 0 tokens outside `e2e/.auth/`.

T-ANIMAL-007/S8 was rewritten by Plan Bot after Neil approved the baseline (09:46, History 49). It is now automated against that text and passes. Only Nits remain open (F-50, F-51, F-52, F-55, F-56), plus out-of-scope note F-53.

### Prior findings status

| ID | Severity | Status | Evidence |
|----|----------|--------|----------|
| F-38 | Minor (code) | **Resolved** | `PendingRoutedModalHost.tsx` clears on `popstate` and when the pathname leaves both the opener page and the modal href. Covered by Vitest `PendingRoutedModalHost.test.tsx` |
| F-39 | Nit (code/docs) | **Resolved** | The `e2e/README.md` `appsettings.Test.json` paragraph appears once, outside the env table |
| F-40 | Nit (code) | **Resolved** | `Api.Framework.Tests.csproj` is all CRLF (34 lines, 0 LF-only) |
| F-41 | Major (security) | **Resolved** | Scenarios sign in with `usePersona` (restores a saved real session; no typing). The setup sign-in runs in `e2e/setup/sign-in-child.cjs`, which is plain Playwright library code outside the test runner. API sign-in and the reset go through plain Node HTTP (`helpers/untraced-http.ts`). Test Bot's `--trace=on` probe (09:41) and my scan of the 09:52 artefacts both found 0. Neil still has to rotate the exposed passwords (see Hand-off) |
| F-42 | Minor | **Resolved** | `AnimalPoliciesTests.cs`: 4 Facts, 0 Skip. Program.cs runs only up to `Build()` (HostBuilt observer, dummy unreachable connection, MigrateDatabase=false, TestData off). The tests assert exactly one animals policy, every endpoint guarded, no `[AllowAnonymous]`, and IAuthorizationService denies a user without the permission and admits one with it |
| F-43 | Minor | **Resolved** | S13 does create, update with read-back, and delete (200) as `animals-tester`, plus a second S13 scenario for 403s. S11 denied calls send valid bodies, then a read-back shows Bessie's body equal to the snapshot and the list is Bessie only |
| F-44 | Minor | **Resolved** | The status was `blocked` while S8 waited (run 10). It is now `passed` with `blockers: []` after S8 passed |
| F-45 | Nit | **Resolved** (code and test) | Code: `tid` is only on the real dialog panel. The shell is `-shell`, the pending modal `-pending`, the `loading.tsx` fallback `-fallback`. Test: `formModal` needs the role, the accessible name **and** `data-tid="animal-form-modal"`, and the "open" steps wait for `-loading` to go and Name to show |
| F-46 | Minor | **Resolved: code defect, fixed by Dev Bot** | `use-json-schema-entity-form.ts` drops a load that finishes after a newer one started. `JsonSchemaForm.tsx` adds JsonForms middleware that keeps the form's own data when the parent passes back an older data object. Regression tests: `JsonSchemaForm.test.tsx` (3) and `use-json-schema-entity-form.test.tsx` (2); Dev Bot reports 4 fail on the old code. The e2e no-retry early Date Born check passes. Residual edge, not a defect: a parent that deliberately re-passes an earlier data object would be ignored (no caller does) |
| F-47 | Nit | **Resolved** | `cellByHeader` (animals and reference-data steps) finds cells by header text, not by position |

### New findings (round 3; continue from F-48)

| ID | Severity | Area | File | Issue | Fix by | Status |
|----|----------|------|------|-------|--------|--------|
| F-48 | Minor | Test assertion | `e2e/features/animals/animals.steps.ts` | After the F-45 tid change, the "no form modal open" checks on the bare tid no longer covered the pending and fallback modals | Testing agent | **Resolved** (Addendum): `anyFormModal` covers all 9 tids, used by all 5 absence checks |
| F-49 | Nit | Security note | `features/common/api.steps.ts`; `helpers/authentication.ts` `usePersona` | The "untraced" comment was wrong: Playwright request contexts are traced. A failed scenario's trace can hold the short-lived Test-DB access token (Bearer header, `addCookies`) | Testing agent | **Resolved / accepted**: renamed `withApiRequestContext`, comment corrected. `e2e/README.md` documents the residual and says to delete the reports before sharing |
| F-50 | Nit | Test isolation | `e2e/playwright.config.ts` (webServer `reuseExistingServer: true`, :3003); `helpers/warm-up.ts` | `npm run dev` and `npm run dev:test` both default to :3003, so e2e can silently reuse a dev UI that talks to the dev API. The new warm-up only waits for 200s and doesn't check the UI's API root. It probably fails safe (Test-issued tokens are rejected by a dev API with a different signing secret), but that can't be checked from config | Implementing agent (config) or testing agent (global-setup probe) | **Open** |
| F-51 | Nit | Test strictness | `animals.steps.ts` `fillStable` | Now that F-46 is a fixed code defect, a `toPass` retry hides any regression and only logs a warning. Fail when it needs more than one attempt, or drop the retry (keep the no-retry scenario) | Testing agent | **Open** |
| F-52 | Nit | Rule file formatting | `ui/UI.NextJs.Framework/.cursor/rules/framework/nextjs-modal-routing.mdc` | No blank line before `## Fast first open (preload)` | Implementing agent | **Open** |
| F-53 | Note | Out of scope (pre-existing) | `package.json` `lint` | There's no ESLint config, so `next lint` / ESLint 9 can't run. This predates the feature | Human / backlog | **Out-of-scope note** |
| F-54 | Minor | Handoff integrity | `handoff.md` | YAML front matter didn't parse (unquoted `[id]` path in the `implementation.ui` manifest), and there was a BEL character in History 46 (a PowerShell `` `a `` escape) | Implementing agent | **Resolved**: both paths quoted, BEL gone. The front matter parses (re-checked 09:58) |
| F-55 | Nit | Least privilege | `e2e/setup/auth.setup.ts` `childEnv()` | The sign-in child process inherits the whole runner environment (all persona passwords and the reset key), although it needs one variable | Implementing agent | **Open** |
| F-56 | Nit | Housekeeping | `UI.NextJs.Framework/.next-test-tb` | Test Bot ran the UI with `NEXT_DIST_DIR=.next-test-tb`. `.gitignore` ignores `.next-test` only, so this build folder isn't ignored | Testing agent (delete it or use the default `.next-test`) | **Open** |

**Round 3: Major 0 · Minor 0 open · Nit 5 open (F-50, F-51, F-52, F-55, F-56) · 1 out-of-scope note (F-53).**

### sign-in-child.cjs review (F-41)

- **How the password arrives:** `auth.setup.ts` starts the child with `execFile(process.execPath, [script, persona, baseUrl, username, passwordEnvVarNAME, statePath, sessionPath])`. The password is never on the command line, so it isn't visible in process listings. The child reads `process.env[passwordEnvVar]` itself.
- **What is stripped first:** before starting the child, the parent removes every env var starting with `PW_`, `PWTEST`, `PWDEBUG` or `PLAYWRIGHT_` (except `PLAYWRIGHT_BROWSERS_PATH`), plus `DEBUG`, `DEBUG_FILE` and `NODE_OPTIONS`. So neither Playwright nor Node debug logging can print call arguments.
- **What it outputs:** one JSON status line on stdout. On failure the message is the stage plus the first line of the error, cut at 300 characters, with the password replaced by `***`; the parent masks it again. The child's stderr is never passed on, and a crash reports only the error name. The setup project opens no page in the test runner, so nothing can be traced, screenshotted or snapshotted. `setup.use({trace:'off',…})` stays as an extra safeguard.
- **What it saves:** `context.storageState({ path })` writes `e2e/.auth/<persona>.json` (cookies, including the access and refresh tokens). The sessionStorage session goes to `<persona>.session.json`. `.auth/` is listed in `e2e/.gitignore` and sits outside the report folders. `usePersona` leaves the refresh cookie out of scenario browsers.
- **Residual Nits:** F-55. Also, on Windows, a child killed by the 240-second timeout could leave its Chromium running, and the `.auth` files have default permissions (they live under the user profile). Neither is a finding.

### T-ANIMAL-007/S8 (rewritten per Plan Bot, History 49) against the test

| Ticket Then | Test | OK |
|---|---|---|
| Tag and first-step batch reset | `@T-ANIMAL-007/S8`; `@fixme @skip` removed from the feature and the scenario. Step 1 is `Given the test data is "reference-data.types-grid.baseline"` | ✓ |
| User with user_management_read | `reference-data-tester` (`ReferenceDataPersonasUnit`: `user_management_read` only) | ✓ |
| Exactly 2 rows, EXAMPLE_STATUS then SHOWCASE_OPTION, Active items 2 / 2 | Data table: row count `toHaveCount(2)`; each cell found by header, checked in order | ✓ |
| Columns "Type key", "Active items", "Actions"; Actions last and not sortable | Header count 3, exact text list. The last header is Actions, and each row's Actions cell is the last `td`. The last header has no `sortable` class (the only sort marker EntityGrid renders; it has no `aria-sort`) | ✓ |
| One "Manage" text button per row, no menu trigger | One `button` per Actions cell, which is `manage-reference-data-type` with text Manage. No `aria-haspopup` / `-actions` / `-actions-menu` in the cell, no `reference-data-types-grid-row-*`, no `role=menu` | ✓ |
| Manage on SHOWCASE_OPTION opens "Manage SHOWCASE_OPTION" listing Widget and Gadget | URL is exactly `/examples/reference-data/manage/SHOWCASE_OPTION?isEnumeration=0`. The dialog with role, name and `data-tid="manage-reference-data-items-modal"` contains the title and one Widget row and one Gadget row | ✓ |
| Closing returns to the grid | Close button, URL exactly `/examples/reference-data`, no items-modal tid of any kind (dialog, fallback or pending, with shell and loading), grid shows 2 rows | ✓ |

**Data:**
- **Master reset:** `TestDataService.ResetMasterAsync` truncates every model table, then re-runs every unit, including `baseline.migration-seed`. That re-inserts all `HasData` rows: types EXAMPLE_STATUS and SHOWCASE_OPTION, items Active and Archived, and Widget and Gadget (`20260923192649_AddReferenceData.cs:65-78`). So the master reset keeps the seeded reference-data rows.
- **The S8 batch:** `ReferenceDataTypesGridBatch` deliberately has a no-op `ClearAsync` and re-runs the migration seed. It is additive: it re-adds missing seed rows but doesn't undo edits or remove extra rows. That's acceptable because no scenario writes reference data.
- **Scenario wording:** the scenario was changed after freezing, but the ID stays the same, the change is Neil-approved, and Plan Bot owns it. That is not a finding.

### Code delta review (Dev Bot 09:08 and 09:35 BST)

- **Modal tids** (`ModalShell` `shellTid`, `RoutedModal`, `PendingRoutedModalHost`, `RoutedModalLoadingFallback`): there is one element per tid. Only the animals modals use these components; the reference-data modals are unaffected. Covered by Vitest `RoutedModal.test.tsx`.
- **F-46 fix:** see the table above. It is sound.
- **`DateCompareValidator`:** `[TODAY]` now comes from the injected `TimeProvider`, registered with `TryAddSingleton(TimeProvider.System)` in `JsonSchemaValidationDependenciesRegistrar`. `DateCompareValidatorTests` pins the clock in both directions, so they can only pass if the injected clock is used.
- **`npm run dev:test`** (`scripts/dev-test.mjs`): it sets `NEXT_PUBLIC_UNITY_API_ROOT` (default `https://localhost:7188/v1/`) and `NEXT_DIST_DIR=.next-test` only in its own process and edits no `.env*` file. `next.config.ts` uses `distDir: process.env.NEXT_DIST_DIR || '.next'`, so `npm run dev` and `next build` are unchanged. `.next-test` is ignored, and `tsconfig` includes `.next-test/types`. The shared :3003 port is F-50.
- **Warm-up** (`helpers/warm-up.ts`, global setup): it waits for 4 routes to answer 200 (`E2E_SKIP_WARMUP` / `E2E_WARMUP_TIMEOUT_MS`). It helps with first-compile aborts but does not address F-50.
- **Claimed results:** dotnet 52/52, tsc clean, Vitest 10/10, Playwright 73/73, consistent with Test Bot's runs. Lint wasn't run (F-53).

### Rule change for Neil (affects future features)

`ui/UI.NextJs.Framework/.cursor/rules/framework/nextjs-modal-routing.mdc` (Dev Bot, 09:08):

1. **The `loading.tsx` fallback** renders as `${tid}-fallback`. The tree comment and step 2 were updated to say so.
2. **New rule, "One element per tid":** `tid` goes on the real `RoutedModal` dialog panel only. The others are `${tid}-shell`, `${tid}-pending` (shell `${tid}-pending-shell`), `${tid}-fallback` and `${tid}-loading`. Tests wait for `tid` and for `${tid}-loading` to be gone before typing.
3. **New rule:** browser Back / Forward clears the pending shell.
4. **New rule:** early typing is kept, using the load-generation guard plus `JsonSchemaForm` ignoring older parent data.

These rules are consistent with `nextjs-list-pages.mdc`, which is unchanged: modals for forms only, `dismissHref` back to the list. Future features' tests and modal code should follow the new tid scheme. Formatting Nit F-52.

### Standard checks (round 3)

| Check | Result |
|-------|--------|
| Every frozen ID has a result and a real, ID-tagged test | ✓ 77/77 results, all passed. Tags are explicit (`@T-ANIMAL-xxx/Sn`, xUnit `Trait("Scenario", …)`), not positional |
| No front-end mocks | ✓ No `page.route`, `routeFromHAR`, MSW or stubbed fetch. `usePersona` restores a **real** session from a real SignInForm sign-in (cookie and sessionStorage), not a faked token. Accepted |
| Reset first; master reset in global setup | ✓ Every data scenario starts with its batch reset, including S8 now. `global-setup.ts` does warm-up, then `resetMaster()` (untraced Node HTTP). Harness exemption unchanged |
| Assertions check the Then outcomes | ✓ Including S11 / S13 (F-43), F-42 and S8 above |
| Role personas; no secrets in test code | ✓ Six role personas. Passwords only from `E2E_<NAME>_PASSWORD`, read by name |
| Only `api_framework_test` and 5188/7188 | ✓ `config.ts` defaults to 5188. The UI is `dev:test` → 7188. The report's safety gate is `Database=api_framework_test` before every run. Caveat F-50 (reusing a server on :3003) |

### Security scan (round 3, after run 11; counts and paths only, no values printed)

The scan loaded 7 values from Windows env by name (6 `E2E_*_PASSWORD`, `E2E_TEST_DATA_KEY`). It searched raw and URL-escaped forms, matched JWTs and `Password=`/`Pwd=` patterns, opened every zip and the HTML report's embedded base64 zips. Run at 09:57 BST.

| Location | Files (newest) | Result |
|----------|----------------|--------|
| `e2e/test-results/` | 2 (09:52) | 0 secrets, 0 JWT, 0 trace or error-context files |
| `e2e/playwright-report/index.html` | 1 (09:52) | 0 secrets, 0 JWT, no embedded trace zips. 3 `password=` pattern hits are Playwright's bundled zip-library code (`o.password=null` etc.), not credentials |
| `e2e/.auth/` | 12 (09:49) | 0 passwords, 0 reset key. 1 access token per persona `.json` (expected; git-ignored via `e2e/.gitignore` `.auth/`; not in any report) |
| `e2e/.features-gen/` | 7 | 0 |
| `Api.Framework.Tests/TestResults/` | 2 (09:42) | 0 |
| `e2e/cucumber-report/`, `ui/test-results/`, `ui/playwright-report/` | absent | — |

**Totals: 24 files; persona password and reset-key hits 0; JWT outside `.auth` 0; trace files 0.** F-41 is confirmed closed in the artefacts.

### Hand-off (test review round 3)

- **To Neil:** **final approve-with-comments**. Code approve-with-comments, tests approve, 77/77 pass, stage `approved`, owner you. Please:
  1. Rotate the animals-tester, animals-viewer and animals-usermanager test passwords. They were exposed in round-2 reports (animals-viewer also in run 2). Update the Windows env vars, then re-run the setup project to refresh `e2e/.auth/`.
  2. Rotate any previously committed Postgres password or JWT secret from F-31, if not done yet, and create the least-privilege test role (README).
  3. Delete leftover artefacts before sharing anything: `e2e/.auth/` when it's not needed, `UI.NextJs.Framework/.next-test-tb` (F-56) and Test Bot's `%TEMP%\tb-run` logs. The current `playwright-report/` and `test-results/` are clean.
  4. Note the modal-routing rule change above (it applies to future features).
  5. Optionally, schedule the Nits F-50, F-51, F-52, F-55, F-56 and the ESLint config gap (F-53).
  
  Merge is your decision.
- **To Dev Bot:** approved with comments. Open Nits for a follow-up (none block): F-50 (give `dev:test` its own port, or have global setup check the UI's API root), F-52 (rule file blank line), F-55 (pass only the one password var to `sign-in-child.cjs`). F-38, F-39, F-40, F-46 and F-54 are resolved. Thanks for the F-46 fix and its regression tests.
- **To Test Bot:** test review **approve** (round 3, test-fix 1 of 5). All F-41 to F-48 are resolved and S8 matches Plan Bot's rewritten scenario. Open Nits: F-51 (`fillStable` should fail if it needs more than one attempt), F-56 (delete `.next-test-tb` or use `.next-test`). No re-run needed.
- **To Plan Bot:** the S8 rewrite (History 49) is implemented and passes: exact rows, headers, one Manage button, modal and close. No plan action needed. Optionally, record that the S8 reset batch is additive (it doesn't remove extra reference-data rows).
