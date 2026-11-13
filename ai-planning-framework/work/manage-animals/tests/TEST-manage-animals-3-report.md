# Test report — manage-animals — run 3

> **Update — Addendum 2 (09:56 BST):** T-ANIMAL-007/S8 unblocked (Neil confirmed the baseline at 09:46) and **passes**. All 77 scenarios pass; status **passed**. The text below the addenda records the earlier run-9 / run-10 position, when S8 was still waiting.

> **Tests blocked: T-007/S8.** One frozen scenario cannot run until Plan Bot / Neil confirm the reference-data types baseline rows. Every other scenario passes. Under `run-tests-and-report` step 7 the run status is **blocked**, not passed (Review Bot F-44).

| Field | Value |
|-------|-------|
| Run | 3 (`handoff.md` `testing.round`) · unit 2026-10-09 09:10 BST · e2e/harness result of record: run 9, started 09:19:31 BST, finished 09:22:22 BST · test-bot |
| Test-fix round | **1 of 5** (`testing.test_fix_cycle: 1`) · Review Bot test review of d30-2 = request-changes, routed to testing: F-41 (Major), F-42, F-43, F-44 (Minor), F-45, F-47 (Nit), F-46 (Minor) |
| Result | **76 Pass · 0 Fail · 1 Blocked (T-ANIMAL-007/S8) · 0 Not automated** — overall **blocked** (Tests blocked: T-007/S8; owner Plan Bot / Neil). No code defects. **Addendum 2: 77 Pass · 0 Fail · 0 Blocked — passed** (run 11) |
| Layers | Unit (Release): 52 tests, 52 pass, 0 Skip, 0 fail. E2e + harness: 66 scenarios, 66 pass, plus 6 `setup` sign-ins pass (72 total); T-007/S8 excluded by `grep: /^(?!.*@skip)/` |
| Safety gate | `ConnectionStrings__LoginConnection` → Database=`api_framework_test`, host `localhost:5432`; checked before every reset / e2e run in this round (runs 6–9 and both probes). Nothing else from the string was printed |
| Environment | Test API launch profile **Test** `https://localhost:7188` / `http://localhost:5188` (`API_URL=http://localhost:5188/v1`); UI `http://localhost:3003` via **`npm run dev:test`** (Dev Bot's new script: API root `https://localhost:7188/v1/`, build dir `.next-test`, no file edited); PostgreSQL Docker `localhost:5432`, DB `api_framework_test`; Windows user env vars loaded into fresh processes, values never echoed |
| Code under test | Dev Bot's change set written 09:08:48 BST (modal routing, `use-json-schema-entity-form`, `DateCompareValidator` → `TimeProvider`, e2e `setup` project + `helpers/authentication.ts` / `untraced-http.ts`, `dev:test`). `untraced-http.ts` was edited again at 09:12:05; no code changes after that up to run 9 (checked before launch). API and UI restarted at 09:10 BST on that code. Not under git |
| Commands | Unit: `dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release --logger "trx;LogFileName=unit-round3.trx"`. E2e: `npx bddgen` then `npx playwright test --workers=1 --reporter=list,json,html` in `UI.NextJs.Framework/e2e` (`PLAYWRIGHT_JSON_OUTPUT_NAME=test-results/manage-animals-results.json`, `PLAYWRIGHT_HTML_OPEN=never`), launched detached. The HTML report is `e2e/playwright-report/index.html`. Traces are retain-on-failure (run 9 had none) |
| Password scan (F-41) | **0 hits** for all six `E2E_*_PASSWORD` values (raw, URL-, JSON-, HTML-escaped, base64) in: `playwright-report` (including its embedded zip), `test-results`, `e2e/.auth`, `%TEMP%\tb-run` logs, unit trx. Run 8's failed-scenario `trace.zip`, `error-context.md` and screenshot: **0**. Residual for Dev Bot below (forced `--trace=on` traces the setup project) |

## Summary

This round fixes the Review Bot test review (F-41 to F-47) and re-runs everything. The main fix is F-41: passwords leaked into the HTML report because the UI sign-in typed the password with `fill()`, which becomes a step title. Scenarios no longer type a password. They restore a session from a real SignInForm sign-in done once per persona in the untraced `setup` project (Dev Bot's `usePersona`). API steps take their token from Dev Bot's untraced Node-HTTP sign-in.

The two skipped reflection Facts are implemented and pass. One of them now proves from `Program.cs` that exactly one animals policy is registered. S11 and S13 now assert what their Thens say. The status is **blocked** for T-007/S8.

Dev Bot landed a code and scaffolding change at 09:08 BST, in the middle of the round. I restarted the API and UI on it and re-ran the full suite. 76 scenarios pass on the new code. **No code defects.** The F-46 early-Date-Born check passes both before (run 6) and after (run 9) the change.

## Results by ticket

| Ticket | Scenarios | Pass | Fail | Blocked |
|--------|-----------|------|------|---------|
| T-ANIMAL-001 | 7 | 7 | 0 | 0 |
| T-ANIMAL-002 | 13 | 13 | 0 | 0 |
| T-ANIMAL-003 | 12 | 12 | 0 | 0 |
| T-ANIMAL-004 | 12 | 12 | 0 | 0 |
| T-ANIMAL-005 | 5 | 5 | 0 | 0 |
| T-ANIMAL-006 | 5 | 5 | 0 | 0 |
| T-ANIMAL-007 | 9 | 9 | 0 | 0 |
| T-ANIMAL-008 | 6 | 6 | 0 | 0 |
| T-ANIMAL-009 | 8 | 8 | 0 | 0 |
| **Total** | **77** | **77** | **0** | **0** |

## Changes per finding (test code only)

| Finding | What changed | Where | Evidence |
|---|---|---|---|
| **F-41** (Major) — passwords in reports | 1. Deleted `e2e/playwright-report`, `test-results` and `cucumber-report` first. 2. `Given I am signed in as` / `When I sign in as` now call `usePersona` (Dev Bot, `helpers/authentication.ts`). It restores the JWT cookie and the app's `unity-auth-session` sessionStorage entry from the `setup` project's real SignInForm sign-in. That project has tracing, screenshots and video off and writes `e2e/.auth/`, which is git-ignored. No scenario types a password, and nothing is mocked or faked: these are real tokens from a real sign-in. 3. API steps now get the Bearer token from `apiAccessToken` (plain Node HTTP, untraced) instead of a Playwright request context. Dev Bot notes that `request.newContext()` is traced whenever tracing is on, so a failed API scenario's trace could have held the SignIn body. 4. My interim fix (a child-process sign-in, `sign-in-session.cjs`) passed run 6, then was removed so there is one sign-in path. | `features/common/auth.steps.ts`, `features/common/api.steps.ts` | Scan: **0** hits in every area after runs 6, 8 and 9, including run 8's failed T-004/S1 trace, error-context and screenshot. `storageState`: none written by test code. Dev Bot's `.auth/` is git-ignored (`e2e/.gitignore`) and holds tokens only (0 password hits) |
| **F-42** (Minor) — empty skipped Facts | `AnimalPoliciesTests.cs` rewritten. Four Facts, all pass, no Skip. **S13 `ProgramCs_RegistersExactlyOneAnimalsPolicy_AnimalsWrite_RequiringThePermissionClaim`** runs the real `Program.cs`, captures `host.Services` on the `HostBuilt` diagnostic event, and stops before anything after `Build()` (no migration, seeding or Kestrel). It uses a dummy connection string that is never opened. It asserts exactly one animals policy, `AnimalsWrite`, with one `ClaimsAuthorizationRequirement`: `permission` = [`animals_write`]. **S13 `AllAnimalEndpoints_RequireAnimalsWritePolicy`**: the action set is AnimalController Create / Delete / Get / List / Update plus `AnimalSchemaController.GetAnimalSchema`, and each carries the AnimalsWrite policy. **S11 `AnimalEndpoints_RejectUsersWithoutAnimalsWrite_ByPolicy`**: no `[AllowAnonymous]`; the effective combined policy needs the `animals_write` claim; `IAuthorizationService` refuses a `user_management_write`-only principal and admits an `animals_write` one | `Api.Framework.Tests/Animals/AnimalPoliciesTests.cs` | Unit Release 52/52 (trx `TestResults/unit-round3.trx`) |
| **F-43** (Minor) — S11 / S13 Thens | **S13:** after the GETs, create "Ziggy" (200, id kept), update Bessie and read it back (name, Date Born 2019-06-15, attributes ["changed"], isFurry / hasHooves true), delete Ziggy (200), list = Bessie. A second `@T-ANIMAL-002/S13` scenario covers `animals-viewer`, who gets **403** on create, update and delete. **S11:** the denied POST / PUT now send a *valid* body, so the 403 is the policy and not validation. Afterwards, a read-back as `animals-tester` shows Bessie's full body equal to the snapshot taken before the denied calls, and the list = Bessie only (no new row) | `features/animals/AnimalsApi.feature`, `features/common/api.steps.ts` (4 new steps) | Runs 6 and 9 pass |
| **F-44** (Minor) — status | `testing.status: blocked`; "Tests blocked: T-007/S8" at the top of this report, in the plan and in the handoff block (summary comment, blocker, result note) | handoff, plan, report | — |
| **F-45** (Nit) — dialog locator | `formModal(page, mode)` = `getByRole('dialog', { name: 'Add Animal' / 'Edit Animal', exact })` (Modal sets `aria-label` to the title). The "open in Add / Edit mode" steps now also require a **loaded form**: dialog visible, no `animal-form-modal-loading`, and the Name field visible. So the `loading.tsx` fallback, a dialog with the same name, can no longer pass them. Absence checks stay on the bare tid | `features/animals/animals.steps.ts` | Runs 6 and 9 pass |
| **F-46** (Minor) — possible masked defect | New `@T-ANIMAL-004/S2` scenario "Date Born typed as soon as the Add form opens is kept". It types once as soon as the field is visible in the Add dialog (no loaded-form wait, no retry), waits 3 s, then asserts the value. `fillStable` stays, but now logs every retry (field id and count only) | `AddEditAnimal.feature`, `animals.steps.ts` | **Passes** before (run 6) and after (runs 8, 9) Dev Bot's 09:08 changes. 0 `fillStable` retries logged in runs 6, 8 and 9. **No code defect found** |
| **F-47** (Nit) — positional cells | `cellByHeader(page, row, header)` finds the column index from `thead th` text (sort glyph stripped) and fails clearly if the header is missing. Used for Attributes, Last Amended and Name (the row-click and row-order steps too) | `animals.steps.ts` | Runs 6 and 9 pass |

## Run history (this round)

| Run | Started (BST) | Code | Result | Notes |
|-----|---------------|------|--------|-------|
| Smoke | 09:03 | pre-09:08 | 7/7 | changed scenarios (T-002 S11/S13 ×2, T-004 S1/S2 ×2, T-001 S2) |
| Unit | 09:03 | pre-09:08 | 48/48 | the two un-skipped Facts plus one new Fact |
| e2e 6 | 09:04 | pre-09:08 | **66/66** (finished 09:07:42) | child-process sign-in; scan 0 |
| Unit | 09:10 | 09:08 | **52/52** | Dev Bot added 4 `DateCompareValidatorTests` |
| e2e 7 | 09:11 | 09:08 (mid-edit) | global setup error | `API sign-in as testdata-admin failed with HTTP 307`: Dev Bot was still editing `untraced-http.ts` (rewritten 09:12:05 with same-host 307/308 follow). Scaffolding in flux, not a test or app defect |
| e2e 8 | 09:15 | 09:08 + 09:12 | 71/72 | after switching to `usePersona` / `apiAccessToken`. 1 env failure: T-004/S1 `page.goto /examples/animals` **net::ERR_ABORTED**, the first visit to that route on a freshly started `dev:test` server (cold `.next-test` compile). Every later scenario on that page passed. Scan 0, including its trace and error-context |
| e2e 9 | 09:19 | 09:08 + 09:12 | **72/72** (66 scenarios + 6 setup) | **result of record**; no code changes since 09:12:05 (checked before launch) |
| Probe | 09:23 | same | A 12/12 (traces forced on); B 8 pass + 1 timeout failure (6 s timeout, deliberate) | Failure-path artefact check; artefacts in separate folders, then **deleted** (see the residual finding) |

## Password scan method (F-41)

`%TEMP%\tb-run\scan-secrets.ps1` runs in its own PowerShell process. It reads the six `E2E_*_PASSWORD` values from the environment and searches for the raw, URL-, JSON- and HTML-escaped and base64 forms. It opens zips recursively (trace zips and the HTML report's embedded `data:application/zip;base64` archive) and reads locked logs with shared access. It prints **counts only**: per area, per variable name, and per file path with `-ListFiles`. An in-memory positive control (plain, zip and embedded zip) must score 3 hits or the scan reports itself broken. It scored 3 on every run.

Final scan (after deleting the probe folders): playwright-report 0, test-results 0, `e2e/.auth` 0, tb-run logs 0, unit trx 0. **Total 0.**

## Residual finding for Dev Bot (owner code, scaffolding) — F-41 follow-up

- **Setup-project traces under forced tracing.** Probe A ran with `--trace=on` on the CLI. That overrides the setup project's `trace: 'off'`, so each `sign in <persona>` setup test wrote a trace. Every one held its persona's password: **2 hits per persona per probe, all six personas**. The cause is that `signInThroughUi` passes the password as an `evaluate(setInputValue, password)` argument, and traces record that argument.
- **What was clean.** All 9 scenario traces, the failed scenario's `error-context.md`, and the cucumber report probe B produced had 0 hits.
- **Default runs are clean.** The default config, which produced the reports of record, writes no setup traces: 0 hits.
- **Clean-up.** I deleted the probe artefacts straight away. `playwright-report-probe*` and `test-results-probe` are not git-ignored. No one else received them.
- **Suggested fix.** Sign in from an uninstrumented browser or a child process (as my interim `sign-in-session.cjs` did). Alternatively, keep the value out of every traced call.
- **Neil.** Rotate the persona passwords once this is fixed. Review Bot named animals-tester, animals-viewer and animals-usermanager. The probe also briefly wrote all six into local trace files, now deleted.

## Other notes (not blockers)

- e2e `README.md` line 8 still says Test Bot's features are "not present yet" (owner code, docs).
- The first navigation after a fresh `dev:test` start can abort while `.next-test` compiles (run 8). Consider a warm-up page load in the setup project (owner code, minor).
- `handoff.md` front matter does not parse as YAML because of something outside the `testing:` block: an unquoted `[id]` in a `files` entry (around line 335) and a BEL control character later in the file. The `testing:` block parses on its own. Owner: whoever owns those sections.
- Scaffolding `signInAs` (the `fill(password)` pattern Review Bot flagged) has been reworked by Dev Bot (`helpers/authentication.ts`).
- Animal batch resets clear only footprint names (Bessie / Ziggy / Daisy / paging names). The new S11 / S13 steps create only Ziggy and Daisy.

## Addendum (09:48 BST, 2026-10-09)

Dev Bot (09:27) asked for three small test-code fixes and a re-run. Same round (3), test-fix 1/5 unchanged, status **blocked** (Tests blocked: T-007/S8, still `@skip @fixme`, Plan Bot to confirm).

**Code the run and probe used:** Dev Bot's round 3 fixes landed by 09:35 BST (e2e setup, sign-in child, warm-up, global setup, authentication, personas and README all dated 09:30:01). API code unchanged since 09:10 (Test API on 5188/7188, started 09:10:22). UI on :3003 restarted 09:40:41 via `npm run dev:test` on the current code, with its own dist dir `.next-test-tb`. Test code: my edits below (09:28:25). Probe 09:41:30, unit 09:42, e2e run 10 09:42:24–09:45:24 BST, all on this code.

### Test-code changes

| Ask | Change |
|-----|--------|
| 1. `withUntracedRequest` comment | Renamed `withApiRequestContext`. The comment now says the context is NOT untraced (with tracing on, its requests can appear in the scenario trace). Only the short-lived Bearer token and animal payloads go through it. The persona password never does: sign-in happens outside Playwright in Dev Bot's untraced `apiAccessToken`, which `bearer()` already uses. `bearer()` and `withApiAs` comments updated to match. No further change needed. |
| 2. "No animal form modal is open" | New `ANY_FORM_MODAL` locator covers `animal-form-modal`, `-fallback` and `-pending`, each with `-shell` and `-loading`. Used by "no animal form modal is open", "I close the animal form modal", close-if-open, the boolean-cell observer step and "I save the animal form". `formModal` still matches only the real dialog (role + exact name **and** `data-tid="animal-form-modal"`); its comment explains why (the fallback and pending dialogs share the name). |

`tsc --noEmit` and `bddgen` are clean.

### Setup-trace leak re-probe (F-41 residual)

- **First probe (09:28) invalid:** all six setup sign-ins failed ("Unable to reach Unity API"). Cause: a parallel stack (API on 5189/7189, Playwright runs from 09:36) shared the `.next-test` build cache, so the UI bundle had `NEXT_PUBLIC_UNITY_API_ROOT` pointing at :7189. It also used the setup code from before 09:30. It produced 0 traces; its folders were deleted. The UI was restarted with a private dist dir. A dummy-credential check then showed sign-in going to :7188 (401).
- **Valid probe (09:41, on the 09:30:01 setup):** `--trace=on --workers=1`, the 6 setup sign-ins + 3 scenarios (T-ANIMAL-002/S11, T-ANIMAL-004/S1, T-ANIMAL-008/S2), 9/9 pass. **Setup traces: 0** (setup now signs in from the untraced child `sign-in-child.cjs`). Scenario trace.zip: 3. **Password scan: 0 hits** across 19 report files and 4 result files, all six personas (self-test 3/3). `test-results-probe` and `playwright-report-probe` were deleted straight after; none are left.
- **Result: the leak is fixed.** Neil can now rotate all six persona passwords (Review Bot F-41).

### Re-run

| Layer | Result |
|-------|--------|
| Unit (Release, 09:42) | 52/52 pass, 0 skip |
| e2e + harness (run 10, `--workers=1`, 09:42–09:45 BST) | 72/72 pass = 66 scenarios + 6 setup sign-ins; 0 flaky; 3.0 min |
| UI warm-up | Dev Bot's `helpers/warm-up.ts` in global setup (my own warm-up dropped): 4/4 pages 200 on first attempt |
| Totals | 76 Pass / 0 Fail / 1 Blocked (T-007/S8) of 77 — unchanged |
| Password scan (after run 10) | **0 hits**: playwright-report 1 file, test-results 2, e2e .auth 12, run logs 50, unit trx 2; self-test OK. trace.zip in test-results: 0 (all passed, retain-on-failure) |

Safety gate before the probe and before run 10: `Database=api_framework_test`.

### Side effects (for Dev Bot / Neil)

- Next dev adds `<distDir>/types/**/*.ts` to `ui/UI.NextJs.Framework/tsconfig.json` on start. It added `.next-test-tb/types/**/*.ts` twice (09:39, 09:40); I reverted it exactly both times. `next-env.d.ts` is rewritten by Next on every start and now references `.next-test-tb`. It is auto-generated, so I left it alone.
- The shared `.next-test` cache between parallel UI stacks can bake in another stack's API root. Consider a per-agent `NEXT_DIST_DIR` (owner scaffolding, minor).
- Earlier notes: README "not present yet" line fixed by Dev Bot. Cold-compile `ERR_ABORTED` addressed by the global-setup warm-up.

## Addendum 2 (09:56 BST, 2026-10-09)

Plan Bot (09:47) reported that Neil confirmed T-ANIMAL-007/S8 at 09:46. This is still round 3 and test-fix 1/5: Review Bot hasn't returned the review and nothing was routed.

**Ticket:** I re-read `tickets/T-ANIMAL-007-shared-grid-actions-column.md` (written 09:47:16; notes: "S8 baseline and checks confirmed by Neil 2026-10-09 09:46"). The S8 text matches Plan Bot's spec.

### Test-code changes

| File | Change |
|------|--------|
| `e2e/features/reference-data/ReferenceDataTypesGrid.feature` | `@fixme @skip` removed from the feature and the scenario. Scenario rewritten: reset `reference-data.types-grid.baseline` (no new reset rows), persona `reference-data-tester`, open `/examples/reference-data`, then the five checks below |
| `e2e/features/reference-data/reference-data.steps.ts` | Placeholder step replaced with real steps. Cells are found by column header, never by position |

Checks:
1. Exactly 2 rows: EXAMPLE_STATUS then SHOWCASE_OPTION, Active items 2 and 2 (data table, row order checked).
2. Headers are exactly `Type key`, `Active items`, `Actions`. Actions is last (the header and each row's Actions cell index) and its header has no `sortable` class.
3. Each row's Actions cell has exactly one button. It is `button[data-tid=manage-reference-data-type]` with text `Manage`. There is no `aria-haspopup` / `…-actions` / `…-actions-menu` trigger, no `reference-data-types-grid-row-*` element on the page and no `role=menu`.
4. Manage on SHOWCASE_OPTION: the path plus query is exactly `/examples/reference-data/manage/SHOWCASE_OPTION?isEnumeration=0`. The dialog `manage-reference-data-items-modal` has the accessible name and text `Manage SHOWCASE_OPTION`, with one Widget row and one Gadget row.
5. Close (`manage-reference-data-items-modal-close-button`): the URL is exactly `/examples/reference-data`. No items modal of any kind remains (dialog, `-fallback`, `-pending`, each with `-shell` / `-loading`), and the grid shows 2 rows.

There is no EXAMPLE_STATUS modal check, as the spec says. `tsc --noEmit` and `bddgen` are clean.

### Results

| Run | Result |
|-----|--------|
| S8 alone (09:49 BST, `--workers=1`) | 6 setup + S8: 7/7 pass first time (S8 6.2 s). No code, test or data defect |
| Full e2e, run 11 (09:49:30–09:52:29 BST, `--workers=1`) | **73/73 pass** = 67 scenarios + 6 setup sign-ins; 0 flaky, 0 skipped; 3.0 min |
| Unit | Not re-run: no API or unit-test change since the 09:42 run (52/52); API code unchanged since 09:08:48 |
| Totals | **77 Pass · 0 Fail · 0 Blocked · 0 Not automated → status passed** |
| Password scan (after run 11) | **0 hits**: playwright-report 1 file, test-results 2, e2e .auth 12, run logs 57, unit trx 2; self-test OK; trace.zip 0 |

Code under test: the same as Addendum 1 (Dev Bot 09:35 code; Test API 5188/7188 pid 30188; UI :3003 pid 42536 with `.next-test-tb`). Safety gate (`Database=api_framework_test`) ran before the S8 run and before run 11. The UI wasn't restarted, and `tsconfig.json` has no `.next-test-tb` entry.

## Results by scenario

| ID | Scenario | Result | Notes |
|----|----------|--------|-------|
| T-ANIMAL-001/S1 | Animal table stores all mapped columns | Pass | unit pass (Release 09:10 BST). |
| T-ANIMAL-001/S2 | Attributes default to an empty array | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-001/S3 | Normalised name is unique among non-deleted rows | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-001/S4 | A soft-deleted animal's name can be reused | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-001/S5 | Soft-deleted flag exists | Pass | unit pass (Release 09:10 BST). |
| T-ANIMAL-001/S6 | Table lives in the creatures schema | Pass | unit pass (Release 09:10 BST). |
| T-ANIMAL-001/S7 | The animals permission is seeded for our users | Pass | unit pass (Release 09:10 BST). |
| T-ANIMAL-002/S1 | Create animal with valid fields | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S2 | Missing Attributes are stored as an empty array | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S3 | Duplicate name is rejected | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S4 | Name of a soft-deleted animal can be reused | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S5 | Date Born must be before today | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). DateCompareValidator now uses the injected TimeProvider (Dev Bot 09:08 BST); earlier finding closed. |
| T-ANIMAL-002/S6 | Date Born is mandatory | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S7 | Name is mandatory | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S8 | Attribute tag limits | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S9 | List returns non-deleted animals with Last Amended (Bessie by "Animals Tester"; Ziggy by a user with no DisplayName, Email "animals-nodisplayname@e2e.test") | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S10 | Soft delete and not found afterwards | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S11 | Users without animals_write are rejected on every endpoint | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). F-42: reflection Fact implemented and un-skipped (no anonymous access; effective policy needs the animals_write claim; IAuthorizationService refuses user_management_write only). F-43: denied POST / PUT send a valid body, then read-back as animals-tester: Bessie unchanged (full body equal) and the list is Bessie only. |
| T-ANIMAL-002/S12 | User-management permissions alone do not grant access to animals | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-002/S13 | AnimalsWrite guards every animal endpoint | Pass | unit pass (Release 09:10 BST); e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). F-42: Program.cs host captured without starting it (HostBuilt): exactly one animals policy, AnimalsWrite, one ClaimsAuthorizationRequirement permission = [animals_write]; every animal action carries it. F-43: create, update (read back) and delete succeed as animals-tester; second scenario: animals-viewer gets 403 on create, update and delete. |
| T-ANIMAL-003/S2 | List shows non-deleted animals | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user ("Animals Tester"; Email when no DisplayName) | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S5 | Last Amended outside summer time | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S6 | Default sort by Name ascending | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S7 | Add opens Basic Form | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S12 | Results are paged on the server | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S13 | No animals to show | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S14 | True shows a green circle with a tick, accessible name Yes | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-003/S15 | False shows a red circle with a cross, No; cells are not interactive | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S1 | Add mode opens with defaults | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S2 | Create animal with required fields | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). F-46: no-retry check (Date Born typed once as soon as the Add form shows, value kept after 3 s) passes on the code before and after Dev Bot 09:08 changes (runs 6 and 9); no input loss seen, so no code defect. |
| T-ANIMAL-004/S3 | Name is mandatory | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S6 | Date Born must be before today | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S7 | Date Born is mandatory | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S9 | Attribute tag limits | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S10 | Edit persists changed fields | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-005/S1 | Confirmation names the animal | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). Covered by the T-ANIMAL-004/S9 test (carries both tags). |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-006/S5 | String-array grid cells | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). Covered by the T-ANIMAL-003/S2 test (carries both tags). |
| T-ANIMAL-007/S1 | Row actions menu in the last column | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). Covered by the T-ANIMAL-003/S9 test (carries both tags). |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-007/S6 | Per-row visibility | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | Pass | Addendum 2: e2e pass (S8 alone 09:49, then full run 11, 09:52 BST). Unblocked after Neil confirmed the baseline at 09:46. |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-008/S1 | (was T-ANIMAL-003 S1) Open Manage Animals from the nav | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-008/S2 | (was T-ANIMAL-003 S10) User without animals_write cannot open Manage Animals | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-008/S3 | (was T-ANIMAL-003 S11) User-management permissions alone do not give access to animals | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-008/S4 | Add \ | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-008/S5 | Opening a form URL directly shows the page with the form on top | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-008/S6 | The old /manage URL redirects to the page | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-009/S1 | True shows a green circle with a tick, named Yes | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). Covered by the T-ANIMAL-003/S14 test (carries both tags). |
| T-ANIMAL-009/S2 | False shows a red circle with a cross, named No | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). Covered by the T-ANIMAL-003/S15 test (carries both tags). |
| T-ANIMAL-009/S3 | Cell is not interactive | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). Covered by the T-ANIMAL-003/S15 test (carries both tags). |
| T-ANIMAL-009/S4 | Labels are configurable with Yes/No defaults | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-009/S5 | Null / undefined shows em dash named Not set | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-009/S6 | Existing switch cell still available | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-009/S7 | Circle fills meet contrast in light and dark mode | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
| T-ANIMAL-009/S8 | Dedicated tokens leave system buttons and callouts unchanged | Pass | e2e pass (run 9, 09:19 BST; re-run green in run 10, 09:45 BST). |
