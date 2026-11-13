# Review log: system-rename

Append-only history of every review round for this feature, whichever route was used: a direct hand-off from the implementing agent or a pull request. The reviewing agent appends one **Round** block per review, at loop stage 10 of `loops/pr-review.md`, with no human request needed.

- Feature: `ai-planning-framework/work/system-rename/`
- Pipeline state: `handoff.md`
- Full reports, one per round: `reviews/DIRECT-<branch-slug>-<n>-review.md` or `reviews/DIRECT-<feature>-<n>-review.md` with no branch (direct route) · `reviews/PR-<id>-review.md` (PR route, overwritten on each PR update)

Rules:

- Append only. Newest round at the bottom. Never edit or delete an earlier round; a correction goes in a new round's **Notes**.
- **Direct route:** the **Comments** table is required, with one row per finding, matching the full report.
- **PR route:** the round block plus **Summary** is required. The comments are in the full report (and on the PR only when publishing is on, which needs provider `azure-devops`), so the **Comments** table is optional.
- Dates in Europe/London. No tokens, connection strings or personal data from fixtures.

---

## Round 1 — 09/10/2026 13:07 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: 109 manifest entries (api 44, ui 51, tests 11, migrations 3) + 1 discovered consumer (`ui/UI.Angular.Framework/src/environments/environment.ts`), 0 not implemented; compared with the 11:20 backup zip |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-RENAME-001..007 (T-RENAME-008 Test Bot, 009 Plan Bot, 011 Neil: reference only; T-RENAME-010 not done, awaiting Neil) |
| Verdict | **Approve with comments** (provisional code verdict; final after Test Bot's run and the test review, D5) |
| Findings | Blocker 0 · Major 0 · Minor 3 · Nit 3 |
| Full report | `reviews/DIRECT-system-rename-1-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | stays with Review Bot (in-review) pending Test Bot's e2e run (code_to_test, option B) |

### Summary

The Unity → System rename and the v1 removal are clean.

- **Migration:** updates 5 seeded rows by id only, with a correct `Down()`. The 16 older migration files are byte-identical to the zip, and the snapshot and Designer are consistent.
- **Routes and auth:** all 14 controllers keep their routes minus the version prefix, with authorisation unchanged. Swagger lists 46 paths / 66 operations with no `/v1`.
- **UI:** a pure rename, plus a fail-fast stale-`/v1` guard. The `.cursor` and `.claude` docs match.
- **Checks:** the gate passed on a copy and in place (API 57/57, UI 10/10) and the self-test is 64/64. Anonymous smoke: `/v1` → 404, plain routes 200 / 401, CORS `SystemUi` OK.

The Minor findings are a missed Angular consumer (F-01), an undocumented database rollback order (F-02) and no unit test for the issuer change (F-03).

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-01 | `ai-code-framework/ui/UI.Angular.Framework/src/environments/environment.ts:7` | Minor | The Angular example UI calls API.Framework at `http://localhost:5088/v1/`, so it will 404 once the Development API runs the new code. The UI-contract rule (both copies) says that UI uses versionless routes. Not covered by the plan (§4 keeps UI.Angular as-is) | Neil decides: drop `/v1/` there (Dev Bot), or reword the rule (both copies) |
| F-02 | `ai-planning-framework/work/system-rename/plan.md:11`, `:196` | Minor | The zip can't roll back migrated databases. Old code against System-named rows breaks tenant saves (`TenantService.cs:335`) and leaves an unknown `__ef_migrations_history` row | Document: with the new code, `dotnet ef database update 20261008150221_AddAnimals` per migrated DB, then restore the zip |
| F-03 | `Api.Framework.Services/Auth/TokenService.cs:73` | Minor | No unit test that a `unity-login` token is rejected (T-RENAME-002/S2 rests on a manual smoke) | `TokenServiceTests` with a throw-away test key: old issuer rejected, new accepted |
| F-04 | `ai-code-framework/ui/UI.NextJs.Framework/e2e/helpers/config.ts:13` | Nit | Whitespace-only `API_URL` returns `""` (later "Invalid URL"); no test for the guard | Treat blank as unset; add a test |
| F-05 | `ai-code-framework/ui/UI.NextJs.Framework/scripts/dev-test.mjs:27` | Nit | `E2E_UI_API_ROOT` has no stale-`/v1` check, unlike `getApiUrl` | Same one-line check |
| F-06 | `handoff.md` History row 7 | Nit | The rollback zip path in the hand-off is relative and points under `ai-framework`; it's in `Candc\backups` | Use the full path |

### Changes since last round

First review.

### Notes

- D10 gate: `code.pre_handoff_gate: pass` @ 12:51:05 recorded honestly. Reproduced in place (check-only) at 13:05:13, with UI file counts 231 instead of 229 because Test Bot added 2 e2e files after 12:51.
- The Development API (started 10:58) still runs the old build (44 of 44 Swagger paths are `/v1`). `unity_login` migrates on its next start (`MigrateDatabase: true`), which is Neil's T-RENAME-011 step 7.
- T-RENAME-010 was not done (it edits ai-review-framework checklists; no go-ahead from Neil). It needs `api-checklist.md:78` and `ui-nextjs-checklist.md:9`, plus line 10 (`unityApiFetch` / `unity-api-fetch.ts`), which the ticket misses.
- No sign-in, token minting or reset POST by Review Bot. Anonymous HTTP only. No `.env*`, `secrets.json` or user-secrets opened. No processes stopped.

---

## Round 1 — test review — 09/10/2026 13:15 (Europe/London)

**Tests blocked: T-RENAME-011/S1.**

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | test-report (Test Bot run 1, 13:07, + addendum 13:15) |
| Branch / PR | no branch (direct) |
| Scope | `tests/TEST-system-rename-1-report.md`, `handoff.md` `testing`, `e2e/features/system-rename/*` (7 scenarios), Test Bot's changes to `animals.steps.ts` / `auth.steps.ts`, the 14 Not-automated scenarios re-checked by Review Bot |
| Repos @ commit | not under git |
| Tickets | T-RENAME-001..011 |
| Verdict | Test **blocked-noted** · final **Approve with comments** (code review + test review). Stage `approved`, owner `human` |
| Findings | Blocker 0 · Major 0 · Minor 3 · Nit 6 (test review adds F-07..F-09, all Nit) |
| Full report | `reviews/DIRECT-system-rename-1-review.md` (section **Test review**) |
| Posted to PR | n/a (direct) |
| Handed to | Neil (merge decision; N1 for T-RENAME-011/S1) |

### Summary

- **Counts:** 35 Pass · 0 Fail · 1 Waiting (T-RENAME-011/S1, Neil's N1) · 14 Not automated. Unit 57/57; e2e 80/80, and the 13:15 S4 re-run 7/7. Manage-animals regression 67/67.
- **Not automated:** all 14 are justified.
  - 002/S3, 005/S2–S3, 006/S1–S4, 009/S1–S4 and 010/S1–S2 are review-verified (D8), and I re-checked them at 13:1x.
  - 004/S5 is recorded as not automatable by Plan Bot (History row 10), and the extended S4 now observes its Then.
- **Rulings:** 004/S4 is same-tab per Plan Bot (rows 9 and 10, ticket saved 13:12:09), now a full Pass. For 005/S5, the original wording needed a Plan Bot wording fix (not an allowlist). That fix is recorded (row 10, ticket lines 70-73), so the pass stands.
- **Test code:** tags, reset-first, no mocks and real Then assertions all OK. F-51 and F-56 are resolved.
- **Secret scan:** 197 files + 3 embedded-zip entries, 0 hits.
- **T-RENAME-010:** done 13:10 on Neil's go-ahead.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-07 | `SystemRename.feature` (T-RENAME-003/S2) | Nit | `npm run build` not run; typecheck and dev compile cover it | Run once when no UI is running, or use a scratch `NEXT_DIST_DIR` |
| F-08 | `system-rename.steps.ts:231-233` | Nit | Fixed 500 ms wait before checking page errors | Wait on a settled signal instead |
| F-09 | `system-rename.steps.ts:162-174` | Nit | A failed run's trace could hold a short-lived refresh token (no password); same as F-49 | Note only |

### Changes since last round

The code review was provisional; this round makes it final. T-RENAME-010 is done (13:10). Correction: the code-review coverage row for 005/S5 said the READMEs have no `/v1`. They have explanatory prose, which the clarified Then allows.

### Notes

- F-56 deleted `.next-test-tb`, but D16 said "no manual deletion". It's harmless; recorded for Neil to reconcile.
- No sign-in, token minting or reset POST by Review Bot. No `.env*` opened. No processes stopped.

## Round 1 — test review round 2 + code delta — 09/10/2026 14:05 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | test-report (Test Bot run 2, 13:56) + code delta since 13:16 (History rows 12-13) |
| Branch / PR | no branch (direct) |
| Scope | `tests/TEST-system-rename-2-report.md`, `handoff.md` `testing`, `system-rename.steps.ts` (F-08), `TokenIssuerTests.cs` (F-03), Dev Bot's CORS change (`SystemUiCors.cs`, `Program.cs`, appsettings, `SystemUiCorsTests.cs`, UI-contract CORS section), F-04 / F-05 files, `e2e/README.md`, `plan.md` §9 (F-02), Test Bot's 3013 scripts (read only) |
| Repos @ commit | not under git |
| Tickets | T-RENAME-001..011 |
| Verdict | Test **approve** · final **Approve with comments**. Stage `approved`, owner `human` (unchanged); review.cycle stays 1 |
| Findings | Open: Blocker 0 · Major 0 · Minor 1 (F-01) · Nit 7 (F-07, F-10..F-15) + note F-09. Resolved: F-02..F-06, F-08 |
| Full report | `reviews/DIRECT-system-rename-1-review.md` (sections **Test review (round 2)**, **Code delta (after 13:16)**, **Findings (round 2)**) |
| Posted to PR | n/a (direct) |
| Handed to | Neil (merge decision, F-01, F-14) |

### Summary

- **Counts:** 36 Pass · 0 Fail · 0 Waiting · 14 Not automated. Unit 68/68; e2e 80/80 on Test Bot's Test UI :3013 against 7188 / `api_framework_test`.
- **011/S1:** passes. The Then is asserted: recorded calls include `GET /Animal` on the Test root, and none contain `/v1/` or go to 7104. The N1 probe of :3003 is HTTP-only and opens no `.env*`.
- **F-03:** 5 real `TokenIssuerTests`. **F-08:** done.
- **CORS:** explicit origins from `Cors:AllowedOrigins`. No wildcard, no credentials. 3013 is Test only. Fail-fast when empty.
  - Preflight from 3003, 3013 and 4200 → 204 with ACAO.
  - From evil.example, 3014 and `null` → no CORS headers.
- **Gate:**
  - copy pass (unit 68/68, nextjs unit 26);
  - self-test 64/64;
  - in place, check-only: all pass except API unit (the running Test API locks `bin\Release`; environment).
- **Secret re-scan (counts only):** 208 files, 0 hits.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-10 | TEST-…-2-report.md:78-80 | Nit | 005/S2-S3 still "Not automated"; `config.test.ts` now covers them | Record as Unit / Pass |
| F-11 | TEST-…-2-report.md:82, :134 | Nit | 005/S5 "on intent" + open question already answered by row 10 | Plain Pass |
| F-12 | e2e/README.md:61 | Nit | Test origin list omits 4200 | Add 4200 |
| F-13 | appsettings.json Cors | Nit | Production inherits localhost defaults; partial index overrides keep base entries | Defaults to Development, or document the full-array override |
| F-14 | handoff.md rows 12-13 | Nit | Dev Bot / Plan Bot wrote handoff while owner was human; Dev Bot restarted the Test API | Neil ratifies |
| F-15 | pre-handoff-checks.mjs unit check | Nit | In-place unit check fails while the Test API runs from bin\Release | Separate test output folder |

### Changes since last round

Test verdict blocked-noted → approve. The "Tests blocked" banner was removed. Resolved: F-02 (plan §9), F-03, F-04, F-05, F-06, F-08. F-01 open (Neil); F-07 deferred.

### Notes

- Development API 7088/5088: not listening as of 14:01 (its VS debug session ended around 13:59). Not stopped by Review Bot; Neil to restart.
- Review Bot error: a scanner self-test file holding one test env value was written to `UI.NextJs.Framework\test-results` at 14:01:41 and deleted about a minute later. Neil may rotate `E2E_TESTDATA_ADMIN_PASSWORD`.
- No sign-in, no token minting, no reset POST, no `.env*` / `e2e/.auth` opened. No processes stopped.
