# Review: DIRECT-pre-handoff-checks-2 — Pre-handoff automated checks (gate)

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (round 2, History row 11) |
| Trigger | direct-handoff (Dev Bot, 2026-10-09 11:04 BST) |
| Review scope | Plan scope (`direct_scope: plan`): the round-1 findings F-01..F-08 and every file changed since round 1 (diffed against Dev Bot's backups in `%TEMP%\gate\c2-backup`), plus the new `DefaultUserSeederTests.cs` |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git (working tree as of 11:07 BST) |
| Linked tickets | T-GATE-001, T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005, T-GATE-008. T-GATE-007 is Review Bot's own ticket and is **not** part of this review |
| Feature(s) | `ai-planning-framework/work/pre-handoff-checks/` |
| Specs reviewed | None (no UI pages, controls or DB columns). Reference: `plan.md` §2, §5, §6 (D1–D17), tickets |
| Active API / UI | api-framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `AGENTS.md` + `.cursor/rules`; UI.NextJs.Framework `AGENTS.md`, `README.md`; `checklists/security-checklist.md`, `checklists/severity.md`; general practice where no rule applies |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 09/10/2026 11:12 (Europe/London) |
| Review iteration | 2 |

## Verdict

**Approve with comments**

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 0 | 2 | 2 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`. No Test Bot round for this feature (D16), so this is the final verdict: stage `approved`, owner human.

## Summary

All eight round-1 findings are fixed and I verified each one with evidence. The Major (F-01, comments in `appsettings*.json`) is properly fixed. The comment strip understands strings, so `//` inside a URL or a quoted value is left alone. JSON that still can't be parsed now fails the gate (`secrets-json-unparsed`) instead of passing quietly. All three round-1 misses are now caught, and so are the new tricky shapes.

The gate passed in place at 11:07:08 with exactly the counts Dev Bot recorded at 11:03:25. It also passed on a temporary copy. The self-test passes 64/64, works in its own temp folder and left the committed fixtures byte-identical. The planted matrix now has 37 cases. All 24 core cases and all 3 round-1 misses behave as expected, no run printed a planted value, and the copy was restored after each case.

The remaining findings are narrower gaps in the secrets heuristics, plus one tidy-up in `dev-test.mjs`. None of them stops approval:

- **F-09:** a connection-string password is skipped if it starts with `$`, `{`, `<` or `%`, or if it is quoted.
- **F-11:** values containing `{…}` are skipped.
- **F-10:** `dev-test.mjs` puts back the whole of `tsconfig.json` on exit, so it can undo a legitimate edit made during the session.
- **F-12:** the stale self-test line in `code.verification`.

## Review scope

| Item | How reviewed |
|------|--------------|
| `ai-code-framework/scripts/pre-handoff-checks.mjs` | Diff against `c2-backup`: only the F-01 / F-02 / F-03 changes (+66 / −8). Secrets section (lines 206–316) and the allowlist / unused logic (124–153, 530–556) read in full |
| `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` | Read in full (288 lines); diff against `c2-backup` (+140 / −11) |
| `ai-code-framework/api/API.Framework/Api.Framework.Services/Auth/DefaultUserSeeder.cs` | Diff against `c2-backup`: optional `ILogger` parameter, one warning on the unset path |
| `ai-code-framework/api/API.Framework/Api.Framework/Program.cs` | Diff against `c2-backup`: line 132 passes `app.Logger` (Development + MigrateDatabase path only) |
| `ai-code-framework/api/API.Framework/Api.Framework.Tests/Auth/DefaultUserSeederTests.cs` | New: read (107 lines, 5 test cases) |
| `ai-code-framework/ui/UI.NextJs.Framework/scripts/dev-test.mjs` | Read in full (56 lines); diff against `c2-backup` |
| `ai-code-framework/ui/UI.NextJs.Framework/tsconfig.json`, `e2e/README.md` | Diff against `c2-backup` |
| `handoff.md` | `code.verification`, `pre_handoff_gate*`, `implementation` manifest, History rows 10–11 |

No unrelated changes in any backed-up file. `.env*` and `secrets.json` were not opened or copied.

## Findings

| ID | File:line | Severity | Category | Comment | Suggested fix |
|----|-----------|----------|----------|---------|---------------|
| F-09 | `ai-code-framework/scripts/pre-handoff-checks.mjs:221` (and `:212`) | Minor | Security | `connPasswordValues` skips any `Password=` / `Pwd=` value that **starts with** `{`, `$`, `<` or `%` (`!/^[{$<%]/.test(v)`, not anchored to a whole placeholder). `CONN_PWD`'s value group `[^;"'\`\s]*` also stops at a quote, so a quoted value (`Password='…'`, valid in Npgsql / SqlClient) reads as empty. Reproduced on the copy: `Password=$uper…` (T7), `Password=%abc…` with no closing `%` (T8) and `Password='…'` inside a C# literal (T9) all pass. Real passwords often start with a symbol. | Drop the prefix test and rely on the anchored `PLACEHOLDER`. Accept a quoted value (`'[^']*'` / `"[^"]*"`) and test its inside. Add T7–T9 as fixtures. |
| F-10 | `ai-code-framework/ui/UI.NextJs.Framework/scripts/dev-test.mjs:32-36` | Minor | Correctness | On exit, `restoreTsconfig()` writes back the whole snapshot taken at start whenever the file differs. A legitimate `tsconfig.json` edit made while `dev:test` is running (e.g. by Dev Bot during a long session) is silently reverted. With the default `.next-test` build dir, Next adds nothing (it's already included), so the restore is pure risk in that case. A crash or a hard kill (`taskkill /F`) skips the restore. That part is acceptable, because self-test line 253 then catches a stray scratch include. Ctrl+C / SIGTERM is forwarded to the child, and the restore runs on the child's `exit` (node is spawned directly, with no shell in between), so the normal path works. | Remove only the entry Next added (`<distDir>/types/**/*.ts`) when it wasn't in the snapshot, instead of rewriting the whole file. Or skip the restore when `distDir` is already in `include`. |
| F-11 | `ai-code-framework/scripts/pre-handoff-checks.mjs:211`, `:309` | Nit | Security | Two ways a value containing braces passes. First, `PLACEHOLDER` accepts any whole value wrapped as `{…}`, `<…>`, `%…%`, `$(…)` or `env:…`, so `"Secret": "{AnyValue}"` passes (T10). That's the documented convention, but it's the one remaining way a real value can pass. Second, in code, `/\$\{|\{[A-Za-z_]/` skips any literal that contains `{letter` anywhere (`token = "ab{cd…"`, T12), even in plain `"…"` / `'…'` strings where it can't be interpolation. Values containing `xxx`, `***` or `changeme` *inside* the value are flagged correctly (T4–T6), so the anchored placeholder list can't be abused that way. | Code rule: treat `{` as interpolation only in template literals (`` ` ``) or C# `$"…"`. JSON: optionally limit `{…}` to `{UPPER_NAME}`-style references. |
| F-12 | `ai-planning-framework/work/pre-handoff-checks/handoff.md:70` | Nit | Docs | `code.verification` still says `selftest.mjs -> pass (33/33; fixtures in …)`. `--record` only replaces the `pre-handoff:` lines, and the self-test is now 64/64 in a temp folder. | Update the line by hand, or have `--record` refresh it. |

## Spec conformance (per control)

n/a: no UI controls in this plan.

## Data mapping (per control)

n/a: no DB columns in this plan.

## Acceptance criteria coverage (per scenario)

The round-1 acceptance table still holds. Round 2 strengthened two scenarios:

- T-GATE-003 S2 (secrets in config): JSON with comments or trailing commas is now covered (planted #8, T1–T3, T11).
- D13 (allowlist hygiene): unused entries are now reported (#22 fails, #23 warns).

## Security and data

- No value is printed or written anywhere. In all 37 planted runs, I searched the text output and the `--json` output for the planted dummy, and it never appeared. Unparsed JSON reports only a line number, not the parser message (`pre-handoff-checks.mjs:261-264`). Allowlist entries carrying `value` still fail (#24).
- **Can the placeholder list be abused?** Not by containing a token: `PLACEHOLDER` is anchored (`^(…)$`). `abcxxx123def`, `ab***cd…` and `changeme-…` are flagged (T4–T6). Only whole-value wrappers pass (F-11), and connection-string values with a leading symbol or quotes pass (F-09).
- **F-04 in production:** `Program.cs:132` calls `DefaultUserSeeder.EnsureAsync(context, builder.Configuration[DefaultUserSeeder.PasswordSetting], app.Logger)`. This runs only under `IsDevelopment()` inside the MigrateDatabase block, which is the only production caller (searched all `.cs` outside bin / obj: Program.cs plus the 4 test calls). The warning names the setting and the env var, never a value.
- Seeder tests (in-memory EF, no real DB): unset (null / empty / whitespace; 3 cases) → no user, `false`, exactly one Warning that mentions the setting; password set → system admin with role and permission group, no log; user exists → hash unchanged with or without a password.

## Tests

### Gate and self-test runs

| Run | Where | Result |
|-----|-------|--------|
| Full gate | temp copy `%TEMP%\rb-gate2` (11:06:24) | pass: API eol 216 / secrets 216 (0 skipped) / docs-dup 22 docs, 53 allowlisted / unit 57; UI lint 150 files 0 errors 2 warnings / typecheck 0 / eol 229 / secrets 229 (0 skipped; `.env*` not copied) / docs-dup 17 / unit 10 |
| Self-test | temp copy (its `FRAMEWORK_ROOT` = the copy) | 64/64 pass, exit 0. It wrote to `%TEMP%\pre-handoff-selftest-*` and removed it afterwards; the committed `scripts/fixtures/pre-handoff` hashes were unchanged |
| Full gate, check-only | in place (11:07:08) | pass, **identical** to the 11:03:25 record, line for line (including `2 skipped secret files`: `.env.example`, `.env.local`, skipped by pattern, not opened). `handoff.md` hash unchanged by the run (no `--record`). `tsconfig.tsbuildinfo` not rewritten (mtime still 11:03:03) |

The self-test was not run in place. Reading it confirms it now uses a temp dir, but its `--record` case does a full real-target run, and the copy run already proves the fixtures stay untouched.

### Planted-violation matrix (copy only, one plant per run, reverted after each)

| # | Plant | Expect | Result |
|---|-------|--------|--------|
| 1 | API `.cs` with LF endings | fail `eol` | ✅ fail |
| 2 | API `.cs` with BOM | fail `eol-bom` | ✅ fail |
| 3 | UI `.ts` with CRLF | fail `eol` | ✅ fail |
| 4 | UI `.ts` with BOM | fail `eol-bom` | ✅ fail |
| 5 | UI `.ps1` with LF (D5: always CRLF) | fail `eol` | ✅ fail |
| 6 | appsettings connection string `Password=NOT_A_REAL_SECRET` | fail `secret-connection-string-password` | ✅ fail |
| 7 | **ALL-CAPS `Jwt.Secret`** (round-1 miss, F-02) | fail `secret-json-credential` | ✅ fail |
| 8 | **appsettings with `//` and `/* */` comments + trailing commas, `Jwt.Secret`** (round-1 miss, F-01) | fail `secret-json-credential` | ✅ fail |
| 9 | UI `.ts` `apiToken = "…"` | fail `secret-code-literal` | ✅ fail |
| 10 | UI `e2e/support` `password: '…'` (D11) | fail `secret-code-literal` | ✅ fail |
| 11 | C# connection-string literal | fail `secret-connection-string-password` | ✅ fail |
| 12 | Doc line `Password=…` | fail `secret-connection-string-password` | ✅ fail |
| 13 | Private-key header in a doc | fail `secret-private-key` | ✅ fail |
| 14 | API duplicate 37-word paragraph (`docs/`) | fail `docs-dup` | ✅ fail |
| 15 | UI duplicate paragraph (`docs/`) | fail `docs-dup` | ✅ fail |
| 16 | UI TS type error | fail `typecheck` | ✅ fail |
| 17 | UI lint error (`@ts-ignore`, `require`) | fail `lint` | ✅ fail |
| 18 | UI failing vitest | fail `unit-failed` | ✅ fail |
| 19 | API failing xUnit test | fail `unit-failed` | ✅ fail |
| 20 | Expired allowlist entry (used) | fail `allowlist-expired` | ✅ fail |
| 21 | New allowlist entry without `reason` | fail (schema) | ✅ fail |
| 22 | **Unused `secret-*` allowlist entry** (round-1 miss, F-03) | fail `matched nothing` | ✅ fail |
| 23 | Unused `docs-dup` allowlist entry | pass + warning | ✅ pass, warning shown |
| 24 | Allowlist entry carrying `value` | fail (schema) | ✅ fail |
| T1 | Block comment holding `"http://…//a"`, a string holding `// … /* … */`, then `Jwt.Secret` | fail | ✅ fail |
| T2 | URL value `https://…//x` then `Jwt.Secret` on the same line | fail | ✅ fail |
| T3 | Escaped quote + `//` in a string, then `ApiKey` | fail | ✅ fail |
| T4 | Secret containing `xxx` (`abcxxx123def`) | fail | ✅ fail |
| T5 | Secret containing `***` | fail | ✅ fail |
| T6 | Secret containing `changeme` | fail | ✅ fail |
| T7 | Connection string `Password=$uper…` | fail | ❌ **pass** (F-09) |
| T8 | Connection string `Password=%abc…` (no closing `%`) | fail | ❌ **pass** (F-09) |
| T9 | C# connection string `Password='…'` (quoted) | fail | ❌ **pass** (F-09) |
| T10 | `Jwt.Secret` wrapped `{…}` | fail | ❌ pass (F-11, documented placeholder) |
| T11 | Unterminated block comment in JSON | fail `secrets-json-unparsed` | ✅ fail |
| T12 | Code literal `token = "ab{cd…"` | fail | ❌ pass (F-11) |
| N1 | True negatives: `${JWT_SECRET}`, `xxx`, `***`, `<client-secret>`, `env:DB_PWD`, `Password=%DB_PWD%`, `Password=<password>`, comments + trailing commas | pass | ✅ pass (no false positive) |

Summary: 37 cases, 32 as expected, 5 gaps (F-09 ×3, F-11 ×2). In every run, the text and `--json` exit codes matched and no value leaked. On my first attempt, #14 / #15 planted the paragraph in non-doc `.md` files, which `isDoc` deliberately ignores (README / AGENTS / CLAUDE / `docs/` / rules only). Re-planted under `docs/`, both fail as expected. That was a harness error, not a gate fault.

### Suggested tests

- Fixtures for T7–T9 (F-09) and T12 (F-11) once fixed.
- A `dev-test.mjs` restore test, or a note on the behaviour, once F-10 is decided.

## Changes since last review

| Round-1 ID | Severity | Status | Evidence |
|------------|----------|--------|----------|
| F-01 | Major | **Fixed** | String-aware `stripJsonc` (`:235-255`) keeps line numbers. Unparseable JSON fails `secrets-json-unparsed` and still runs the line rules. Caught: #8, T1, T2, T3, T11; N1 has no false positive |
| F-02 | Minor | **Fixed** | Anchored `PLACEHOLDER` (`:211`), and bare ALL_CAPS values are no longer skipped. Caught: #7, T4–T6. Remaining gap: wrappers (F-11) |
| F-03 | Minor | **Fixed** | `:544-556`: an unused secret-* entry fails, any other unused entry warns, and entries are judged only when the check ran on every target the entry applies to. Caught: #22 (fail), #23 (warn) |
| F-04 | Minor | **Fixed** | `DefaultUserSeederTests.cs` has 5 cases (Theory ×3 + 2 Facts) and is included in the API's 57. The logger is passed in production (`Program.cs:132`, `app.Logger`) |
| F-05 | Nit | **Fixed**, follow-up F-10 | The scratch `.next-*` includes are gone from `tsconfig.json`. `dev-test.mjs` restores on the child's exit. Ctrl+C / SIGTERM are forwarded. A crash or hard kill doesn't restore, but self-test line 253 catches the result. Whole-file restore → F-10 |
| F-06 | Nit | **Fixed** | The self-test uses `mkdtempSync(os.tmpdir())`. The committed fixtures are compared, not rewritten (`--write-fixtures` only). Hashes were unchanged after the run |
| F-07 | Nit | **Fixed** | 64 assertions covering unit failure, the D11 e2e rules, allowlist schema, unused entries, `--feature`, and `--record` (a partial run is refused; a full run records into a temp handoff) |
| F-08 | Minor | **Fixed** | The manifest lists `e2e/README.md`, `scripts/dev-test.mjs` and `Api.Framework.Tests/Auth/DefaultUserSeederTests.cs` (handoff lines 160–173). `recorded_at` is 11:03:19 |

## Out of scope / pre-existing notes

These do not affect the verdict.

- **Neil (not an agent):** the round-1 actions still stand. Rotate the dev DB password and Jwt secret, change the system-admin password, and set Development user-secrets.
- **Plan Bot / Test Bot:** not re-checked this round: the `ai-test-framework` docs that named the unprefixed `ConnectionStrings__LoginConnection` (round-1 note), and adding the seeded admin password to D1's rotation list.
- **Self-test, line 253:** it checks the *live* UI `tsconfig.json`. If someone runs `next dev` with another build dir in the working tree, the self-test fails until that include is removed. That's intended as a guard, but worth knowing.
- The running `dev:test` (started 09:40) still runs the old `dev-test.mjs`, so the restore applies only from its next start. No processes were stopped.
- All planted runs and the self-test ran on a temporary copy only (`%TEMP%\rb-gate2`, deleted afterwards; the `node_modules` junction was removed first). No framework docs were edited. T-GATE-007 is separate.
