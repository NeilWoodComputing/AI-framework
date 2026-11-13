# Review: DIRECT-pre-handoff-checks-1 — Pre-handoff automated checks (gate)

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (round 1) |
| Trigger | direct-handoff (Dev Bot, 2026-10-09 10:48 BST) |
| Review scope | Plan scope (`direct_scope: plan`) — details in **Review scope** |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git (API.Framework, UI.NextJs.Framework and `ai-code-framework` are not git repos; working tree as of 10:56 BST, including Dev Bot's 10:55 Test-settings addition, History row 6) |
| Linked tickets | T-GATE-001, T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005, T-GATE-008 (`handoff.md` `tickets`). T-GATE-006 done by Plan Bot (reference only). T-GATE-007 is Review Bot's own ticket and is **not** part of this review |
| Feature(s) | `ai-planning-framework/work/pre-handoff-checks/` |
| Specs reviewed | None: the plan has no UI pages, controls or DB columns (`plan.md` §1). Reference: `plan.md` §2, §5, §6 (D1–D17), tickets |
| Active API / UI | api-framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `AGENTS.md` + `.cursor/rules`; UI.NextJs.Framework `AGENTS.md`, `README.md`; `checklists/security-checklist.md`, `checklists/severity.md`; general practice where no rule applies |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 09/10/2026 10:56 (Europe/London) |
| Review iteration | 1 |

## Verdict

**Request changes**

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 1 | 4 | 3 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`.

## Summary

This is a strong first round. The gate is check-only by default, needs no dependencies, never prints a value, and does what Dev Bot said. It passed on both targets when I ran it in place and on a temporary copy, with identical counts to the 10:47 recording. The self-test passes 33/33, and 20 of the 22 violations I planted were caught with a clear message and exit 1. The committed dev secrets are gone, the seeder change is safe, and the line-ending normalisation is genuinely endings / BOM / final newline only (448 files compared against Dev Bot's backup).

The one thing that stops approval is **F-01**. .NET `appsettings*.json` files may contain comments. When one does, `JSON.parse` fails and the scanner quietly falls back to a line scan that only looks for `Password=` and private keys. A `Jwt:Secret` or API key value then passes the gate (reproduced). Because this is the control meant to stop committed secrets (6 of 6 manage-animals rounds), the gap is Major. The other items are small: an all-caps value blind spot (F-02), silent unused allowlist entries (F-03), a missing seeder test (F-04), one manifest gap (F-08) and three nits.

Dev Bot made a Neil-approved addition while this review was running (History row 6, 10:55): Test-only settings now come from `APIFW_TEST_`-prefixed env vars, read only when the environment is `Test`. I folded it in. It's sound: the prefix provider is added only in `Test` (`Program.cs:16-21`, `LoginDbContextFactory.cs:33-37`), the docs name settings only, and the gate re-run in place at 10:56:25 passed with the same counts.

## Review scope

How the scope was built: plan scope. I started from the `implementation` manifest in `handoff.md` (11 API, 7 UI and 7 framework entries), then searched both targets and `ai-code-framework` for files changed since Dev Bot picked up (10:36 BST), outside the 10:44:42 normalisation window. Neil approved the plan that puts the runner in `ai-code-framework/scripts/`, outside the usual `review.scope_include`, so the scripts and the two loop docs they change are reviewed as plan scope.

| Repo | File | Class | Reason | Tickets |
|------|------|-------|--------|---------|
| api | `Api.Framework/appsettings.json` | config | manifest | T-GATE-008 |
| api | `Api.Framework.Data/LoginDbContextFactory.cs` | api | manifest | T-GATE-008 |
| api | `Api.Framework.Data/Api.Framework.Data.csproj` | config | manifest | T-GATE-008 |
| api | `Api.Framework/Api.Framework.csproj` | config | manifest | T-GATE-008 |
| api | `Api.Framework.Services/Auth/DefaultUserSeeder.cs` | api | manifest | T-GATE-008 (deviation) |
| api | `Api.Framework/Program.cs` | api | manifest | T-GATE-008 |
| api | `AGENTS.md` | docs | manifest | T-GATE-008, T-GATE-005 |
| api | `.cursor/rules/api-framework-overview.mdc`, `.claude/rules/api-framework-overview.md` | docs | manifest | T-GATE-008 |
| api | `.editorconfig`, `.gitattributes` | config | manifest | T-GATE-002 |
| api | `Api.Framework/appsettings.{Development,Production,Test}.json` | config | dependency (secrets check, key names only) | T-GATE-008 |
| ui | `eslint.config.mjs` | config | manifest | T-GATE-001 |
| ui | `package.json` (scripts) | config | manifest | T-GATE-001 |
| ui | `tsconfig.json`, `e2e/tsconfig.json` | config | manifest / dependency (D11) | T-GATE-001 |
| ui | `README.md`, `AGENTS.md` | docs | manifest | T-GATE-005 |
| ui | `.editorconfig`, `.gitattributes` | config | manifest | T-GATE-002 |
| ui | `e2e/README.md` (Local settings / Test env var names) | docs | discovered (F-08, manifest incomplete) | T-GATE-008 addition (History row 6) |
| framework | `ai-code-framework/scripts/pre-handoff-checks.mjs` | tests (tooling) | manifest | T-GATE-002..005 |
| framework | `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` | tests (tooling) | manifest | T-GATE-002..005 |
| framework | `ai-code-framework/scripts/pre-handoff-allowlist.json` | config | manifest | T-GATE-003, T-GATE-004 |
| framework | `ai-code-framework/scripts/fixtures/pre-handoff/` (36 files) | tests | manifest | T-GATE-002..005 |
| framework | `ai-code-framework/scripts/README.md` | docs | manifest | T-GATE-005 |
| framework | `ai-code-framework/loops/feature-build.md`, `ai-code-framework/AGENT-BRIEF.md` | docs | manifest (gate sections only) | T-GATE-005 |

- Manifest: 25 entries · Discovered (not in manifest): 1 (`e2e/README.md`, changed by the 10:55 addition → F-08). Every other changed file I found is listed or is one of the normalised files counted in History row 5 · Dependency: 2
- Whole files reviewed: yes for the scripts, allowlist, seeder, factory, `Program.cs`, configs and the changed doc sections; the 224 normalised files were checked byte-wise (see **Line-ending normalisation**), not reread
- Not implemented: none
- Deferred by the tickets' out-of-scope lists: markdownlint, Prettier, git hooks / CI, Unity.API / UI.Angular.Framework, credential rotation
- Excluded: `review.scope_exclude` (bin / obj, node_modules, `.next*`, `*.tsbuildinfo`). `.env*` and `secrets.json` were never opened, and they were left out of the temporary copy. T-GATE-006 (Plan Bot's handoff template / README / config) and T-GATE-007 (Review Bot's own docs) are not reviewed here

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix |
|----|----------|------|-----------|---------|-----------------------|---------------|
| F-01 | Major | Security | `ai-code-framework/scripts/pre-handoff-checks.mjs:235` | `scanJson` calls `JSON.parse`, and on failure falls back to `scanLines(..., 'json')`, which only checks `Password=` / `Pwd=` and private-key blocks. .NET `appsettings*.json` allow `//` and `/* */` comments (and trailing commas), so one comment silently turns off the credential-key walk. **Reproduced on the copy:** a comment plus `Jwt.Secret` = a dummy mixed-case value in `appsettings.Development.json` → `secrets api-framework -> pass`, exit 0. Without the comment, the same value fails correctly. Nothing in the output says the file was not parsed | T-GATE-003 S2 ("Jwt.Secret set to a non-empty value → fails"); `plan.md` §5.2 secrets rules (JSON key walk); `security-checklist.md` → Secrets and configuration; `severity.md` Major ("a rule can be bypassed") | Strip comments and trailing commas with a small string-aware pass before `JSON.parse` (no dependency needed). If a file still won't parse, fail with a `secrets-json-unparsed` finding (`file`, no value) rather than downgrading quietly, or at minimum run a line-level `"<credential key>": "<non-empty>"` check. Add an `api-bad` fixture `appsettings.json` with a comment and a credential key, plus a self-test assertion |
| F-02 | Minor | Security | `ai-code-framework/scripts/pre-handoff-checks.mjs:210`, `:227` | `credentialValue` treats any value matching `^[A-Z][A-Z0-9_]*$` as an env-var *name* and skips it. A credential written in that shape under a credential key passes: `Jwt.Secret` = `NOT_A_REAL_SECRET` → pass (reproduced). The same shape covers uppercase-only keys, such as AWS access-key IDs. Minor, not Major: this stack's real credentials (connection-string `Password=`, base64 JWT keys) are still caught, and env-var *keys* are already excluded by `CRED_NAME_EXCLUDE` (`envvar`, `var`, `env`) | T-GATE-003 work item 1 (non-empty value under a credential key); general practice (security) | Don't apply the `ENV_NAME` shortcut in the JSON key walk, or only apply it when the value also ends in a credential word (`_PASSWORD`, `_SECRET`, `_KEY`, `_TOKEN`) as in the persona env-var names. Add a fixture for both shapes |
| F-03 | Minor | Security | `ai-code-framework/scripts/pre-handoff-checks.mjs:500` | Only *expired* unused allowlist entries are reported. A non-expired entry that matches nothing passes silently (reproduced: a new unused `secret-json-credential` entry → pass, no note). A stale entry could later hide a real finding at that path / key without anyone re-checking it | D13 (Review Bot checks entries every round); general practice | Print `note allowlist entries[n] unused` (and list it in `--json`) whenever every target and check ran; consider failing on unused `secret-*` entries |
| F-04 | Minor | Tests | `ai-code-framework/api/API.Framework/Api.Framework.Services/Auth/DefaultUserSeeder.cs:30` | The new behaviour (no fallback, return `false` and create nothing when `DefaultUser:Password` is unset, existing account untouched) has no unit test. `Api.Framework.Tests` has no `DefaultUserSeeder` test | `skills/review-tests` (changed behaviour untested); general practice | Add `EnsureAsync_PasswordNotConfigured_CreatesNoUserAndReturnsFalse`, `EnsureAsync_PasswordConfigured_CreatesSystemAdmin` and `EnsureAsync_UserExists_IgnoresPassword` in `Api.Framework.Tests/Auth/DefaultUserSeederTests.cs`, using the provider the existing tests use |
| F-08 | Minor | Process | `ai-planning-framework/work/pre-handoff-checks/handoff.md:92` (`implementation`) | The 10:55 addition changed `ui/UI.NextJs.Framework/e2e/README.md` (Test env var names), but it isn't in the `implementation` manifest, and `recorded_at` is still 10:47:04 | `loops/pr-review.md` stage 1 (manifest incomplete → Minor, one per file) | Add `e2e/README.md` under `implementation.ui` (`change: modified`, `tickets: [T-GATE-008]`) and refresh `recorded_at` |
| F-05 | Nit | UI standards | `ai-code-framework/ui/UI.NextJs.Framework/tsconfig.json:61`, `:65` | `include` carries `.next-devbot-warm/types/**/*.ts` and `.next-test-tb/types/**/*.ts`, both added by dev servers for agent scratch builds. `.next-test-tb` was added at 10:46:31, after the normalisation. They're harmless, but they're noise in a manifest-listed file, and `.next-test-tb` is due to be deleted | General practice | Remove both entries once Neil deletes those folders. Keep `.next/` and `.next-test/` |
| F-06 | Nit | Tests | `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs:68` | The hand-off's verify command deletes and rewrites `scripts/fixtures/pre-handoff/` in place (`rmSync` recursive). Today it regenerates byte-identical fixtures (36/36 compared), but a reviewer's "verify" still writes files | General practice | Generate into `os.tmpdir()` (or take `--out`) and keep the committed fixtures for single runs, or say plainly in the hand-off that the self-test rewrites the fixtures |
| F-07 | Nit | Tests | `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs:107-156` | The self-test doesn't cover: a unit-test failure, D11 (e2e lint ignored, e2e secrets scanned), allowlist schema problems (value present, missing expiry), `--feature` touched targets (T-GATE-005 S6) or `--record` (S3). I verified all of these by hand (matrix below), so this is about regression protection only | T-GATE-005 S3, S6; D11 | Add fixtures / assertions, starting with the F-01 and F-02 shapes |

## Spec conformance (per control)

Not applicable. The plan has no UI pages, controls or specs (`plan.md` §1: "`specs/`, `excel/`, `journeys/` and `stubs/` are intentionally not created"). This is not a "No linked ticket" case: six tickets are linked and every scenario is traced below.

## Data mapping (per control)

Not applicable. There are no Service / Target DB Table / Target DB Column mappings and no migrations (`implementation.migrations: []`).

## Acceptance criteria coverage (per scenario)

| Scenario ID | Scenario | Status | Code reference(s) | Test / verification | Notes |
|-------------|----------|--------|-------------------|---------------------|-------|
| T-GATE-001/S1 | Lint runs without prompting | Covered | `ui/.../eslint.config.mjs`; `package.json` `lint: eslint .` | Gate in place + copy: `lint nextjs -> pass (150 files, 0 errors, 2 warnings)` | |
| T-GATE-001/S2 | A lint error fails the run | Covered | `pre-handoff-checks.mjs:354-368` | Planted rules-of-hooks error → exit 1, `lint:react-hooks/rules-of-hooks src/planted-lint.tsx:5`; fixture `nextjs-bad/bad-lint.js` | |
| T-GATE-001/S3 | Warnings follow the agreed policy | Covered | `pre-handoff-checks.mjs:364` | Baseline 2 warnings, exit 0; self-test `warn-only.js` | D3 |
| T-GATE-001/S4 | Typecheck script | Covered | `package.json` `typecheck: tsc --noEmit`; `pre-handoff-checks.mjs:369-381` | Planted TS2322 → exit 1 with file:line; clean → 0 errors | |
| T-GATE-001/S5 | Build output and e2e ignored | Covered | `eslint.config.mjs` ignores; `tsconfig.json:69` excludes `e2e` | Planted lint error under `e2e/support/` → not reported, pass | D11 |
| T-GATE-001/S6 | Clean baseline | Covered | — | 0 errors / 2 warnings, recorded in `code.verification` | |
| T-GATE-002/S1 | Each target declares its rule | Covered | both `.editorconfig` / `.gitattributes` | Read: CRLF API, LF UI, utf-8, final newline, `*.ps1/cmd/bat` CRLF; `.gitattributes` consistent | |
| T-GATE-002/S2 | Wrong line ending found | Covered | `pre-handoff-checks.mjs:161-186` | Planted CRLF `.ts` in nextjs and LF `.cs` in API → exit 1, expected / found shown | |
| T-GATE-002/S3 | Mixed, no final newline, BOM | Covered | same | Planted BOM and no-newline files → exit 1; fixture `Mixed.cs` | |
| T-GATE-002/S4 | Excluded paths skipped | Covered | `pre-handoff-checks.mjs:44-48, 86-108` | Fixture `bin/Release`, `.env.local`; planted `.env.local` → "skipped by pattern (not opened)" | |
| T-GATE-002/S5 | Normalisation changes only endings / BOM | Covered | `pre-handoff-checks.mjs:173-204` | Reviewer byte-compare of all 448 backup files (see below) | |
| T-GATE-002/S6 | Clean after normalisation | Covered | — | `eol` pass on both targets, in place and on copy | |
| T-GATE-003/S1 | Connection-string password fails | Covered | `pre-handoff-checks.mjs:249` | Planted `ConnectionStrings.Planted` → `secret-connection-string-password ... [ConnectionStrings.Planted]`, no value printed | |
| T-GATE-003/S2 | Non-empty secret key fails, empty passes | **Partial** | `pre-handoff-checks.mjs:232-257` | Plain JSON: fails correctly. With a comment in the file (F-01), or an all-caps value (F-02): passes | F-01, F-02 |
| T-GATE-003/S3 | C# fallback literal fails | Covered | `pre-handoff-checks.mjs:266-268` | Planted `PlantedFactory.cs:3` → fail, no value | |
| T-GATE-003/S4 | Env / request values pass | Covered | `pre-handoff-checks.mjs:207-228, 272-281` | Real targets: 0 false positives (the plan's 7 false-positive shapes included); fixture `api-good` | |
| T-GATE-003/S5 | Allowlisted passes; expired fails | Covered | `pre-handoff-checks.mjs:124-157, 495` | Expired docs-dup entry → `allowlist-expired` exit 1; value / missing expiry → PROBLEM exit 1 | F-03 (unused entries silent) |
| T-GATE-003/S6 | Secret files never opened | Covered | `pre-handoff-checks.mjs:47, 100` | `.env.example`, `.env.local` listed as skipped in place | |
| T-GATE-003/S7 | Working tree when not in git | Covered | `pre-handoff-checks.mjs:118-121, 480` | "not a git repo: working tree scanned" for both targets | |
| T-GATE-003/S8 | Current targets give expected result | Covered (after T-GATE-008) | — | 0 findings on both targets; appsettings key walk: `LoginConnection` / `Jwt.Secret` empty | The "before" half can no longer be re-run |
| T-GATE-004/S1 | Same paragraph in two docs fails | Covered | `pre-handoff-checks.mjs:298-340` | Planted 30-word paragraph in UI `README.md` + `AGENTS.md` → exit 1, first 10 words + both file:line | |
| T-GATE-004/S2 | Short repeats / code blocks ignored | Covered | `pre-handoff-checks.mjs:306-324` | Self-test fixture | |
| T-GATE-004/S3 | Whitespace / case still match | Covered | `pre-handoff-checks.mjs:330` | Self-test `PARA_WRAPPED` | |
| T-GATE-004/S4 | Allowlisted mirror pair passes | Covered | `pre-handoff-checks.mjs:145-147` | 9 API pairs, 53 paragraphs allowlisted | |
| T-GATE-005/S1 | All checks pass | Covered | `pre-handoff-checks.mjs:464-529` | Full gate exit 0, in place (10:51:37) and on copy (10:51:06) | |
| T-GATE-005/S2 | One failing check fails the gate | Covered | same | Every planted case → exit 1; self-test "every check still runs" | |
| T-GATE-005/S3 | Results recorded in handoff.md | Covered | `pre-handoff-checks.mjs:423-455` | `--record` on a temporary copy of `handoff.md`: only `pre-handoff:` lines and `pre_handoff_gate_at` changed, `testing` untouched, no values | |
| T-GATE-005/S4 | Failed gate blocks hand-off | Covered (docs) | `ai-code-framework/loops/feature-build.md:108, 130` | Process rule; not executable | |
| T-GATE-005/S5 | Recorded result is the last run | Covered | `feature-build.md:114`; `--record` replaces earlier `pre-handoff:` lines | Verified on the copy | |
| T-GATE-005/S6 | Only touched targets run target checks | Covered | `pre-handoff-checks.mjs:401-420, 488-489` | API-only manifest copy → nextjs ran `secrets` only | |
| T-GATE-005/S7 | Docs list the gate | Covered | `feature-build.md:36, 42, 84-115, 130, 156`; `AGENT-BRIEF.md:53` | No "no test runner" line left in either | |
| T-GATE-008/S1 | No credentials in committed config | Covered | `appsettings.json` | Key walk: `ConnectionStrings.LoginConnection`, `Jwt.Secret` empty; secrets check 0 findings | |
| T-GATE-008/S2 | Factory fails clearly without config | Covered (code) | `LoginDbContextFactory.cs:41-49` | Not re-run by me (`dotnet ef` would touch Neil's config); Dev Bot's History row 5 reports it verified | |
| T-GATE-008/S3 | Factory works with env var / user-secret | Not re-run | `LoginDbContextFactory.cs:27-37` | Needs Neil's values; Dev Bot reports it verified with dummy probe values, since removed | |
| T-GATE-008/S4 | Local setup documented without values | Covered | `API.Framework/AGENTS.md:46-61`; overview rule `.mdc:54` / `.md:52` | Names only | |

## Security and data

| Check | Status | Reference |
|-------|--------|-----------|
| No credentials in committed config (`appsettings*.json`, `launchSettings.json`) | Clean: credential keys empty in `appsettings.json` / `.Test.json`; `.Development.json` / `.Production.json` hold none | key walk (names and emptiness only); secrets check 0 findings |
| Hard-coded fallback connection string removed | Clean | `LoginDbContextFactory.cs:41-49` |
| Seeder password: no fallback | Clean: returns `false` and creates nothing when unset | `DefaultUserSeeder.cs:28-34` |
| Seeder warning does not log the value | Clean: logs the fixed system email and the setting *name* only | `Program.cs:133-136` |
| Development config does not hold the seed password | Clean: no `DefaultUser` key in any `appsettings*.json`; values come from user-secrets / env (`AGENTS.md:54`) | key walk |
| Test-only settings (10:55 addition) | Clean: `APIFW_TEST_` prefix provider added only when the environment is `Test` (`Program.cs:16-21`; factory only when `ASPNETCORE_ENVIRONMENT=Test`, `LoginDbContextFactory.cs:33-37`), so Test values can't reach Development; docs name settings only (`AGENTS.md:46-61`) | History row 6 |
| Jwt secret missing → clear failure | Clean (existing): `TokenService.cs:92-94` throws when empty or < 32 bytes | |
| Scanner never prints a value | Clean: 22 planted runs + self-test, 0 value leaks | `pre-handoff-checks.mjs:503-504` |
| Secret files never opened | Clean | `pre-handoff-checks.mjs:47, 100` |
| Scanner bypasses | **F-01** (comments in appsettings), **F-02** (all-caps values) | |
| No network calls | The script makes none. Child tools can: `dotnet test` may restore from NuGet on a cache miss, and npm may check for updates | `pre-handoff-checks.mjs:343-348` |
| Writes | Default mode writes nothing. `--record` writes `handoff.md` (guarded: re-read, `testing` unchanged). `--fix-eol` rewrites target files. The self-test rewrites `scripts/fixtures/` (F-06). Tool steps write build output only (`bin` / `obj` Release); an in-place run changed no source file and no `tsconfig.json` / `tsbuildinfo` | |

### DefaultUserSeeder deviation

- **Change:** the hard-coded admin password literal is gone. `EnsureAsync(db, initialPassword)` gets `DefaultUser:Password` from configuration (`Program.cs:131`), seeds only in Development, and only creates the account when it doesn't exist. When the password is unset it creates nothing, and `Program.cs` logs a warning naming the setting.
- **Safe:** no fallback, no value logged, nothing in committed config, and an existing account is never touched. Fixing this rather than allowlisting it was right (D1, D13: real credentials are fixed, not allowlisted).
- **Impact for Neil:** a fresh Development database now seeds no system admin unless `DefaultUser:Password` (user-secret) or `DefaultUser__Password` (env var) is set. Nothing changes for an existing database where the account already exists, **but that account's password is the old committed literal**, so it should be changed too.
- **Gap:** no unit test (F-04).
- **Note for Plan Bot:** Plan Bot recorded this deviation in `plan.md` §6 and the T-GATE-008 Notes at 10:56 (handoff History row 7). One thing left: D1's "Action for Neil" still names only the DB password and the Jwt secret. Please add the existing seeded system-admin account's password.

### Allowlist (D13)

All 9 entries are `docs-dup` only, `target: api-framework`, each naming exactly one `.cursor/rules/<x>.mdc` ↔ `.claude/rules/<x>.md` pair. Each has a reason (API.Framework `AGENTS.md:13`: "Edit the Cursor `.mdc` first, then copy"), `owner: dev-bot`, `proposed: 2026-10-09` and `expires: 2027-04-09`. Matching is narrow: a duplicate is allowlisted only when **every** location is inside that pair (`pre-handoff-checks.mjs:145-147`), so a paragraph copied into a third file still fails. All 9 entries are in use (53 paragraphs). There are no `secret-*` entries and no values. `AnimalPoliciesTests.cs`' dummy key isn't flagged, so it correctly has no entry. **Justified and narrowly scoped.**

### D10: gate result recorded honestly

At hand-off: `code.pre_handoff_gate: pass` and `pre_handoff_gate_at: 2026-10-09T10:47:27+01:00`, with 14 `code.verification` lines. My in-place run at 10:51:37 reproduced every recorded line exactly: same files, docs, allowlisted, warning and test counts, and 2 skipped secret files. No target file changed between 10:47:27 and that run. Dev Bot then changed 7 files at 10:54:13 (History row 6) and re-recorded the gate at 10:55:12, and my full in-place re-run at 10:56:25 again passed with identical counts. The `--record` format matches a run made on a temporary copy. **Recorded honestly**, and the current `pre_handoff_gate_at` (10:55:12) reflects the last change.

## Tests

### Gate and self-test runs

| Run | Where | Result |
|-----|-------|--------|
| `node ai-code-framework/scripts/pre-handoff-checks.mjs` | Temporary copy (`%TEMP%\rb-gate`, no node_modules / bin / obj / `.next*` / `.env*`; node_modules junctioned) | **pass**, exit 0, 10:51:06. eol 215 / 229, secrets 0 findings (0 skipped secret files, since `.env*` wasn't copied), docs-dup 22 docs / 53 allowlisted and 17 docs, unit 52/0/0 and 10 passed / 4 files, lint 150 files / 0 errors / 2 warnings, typecheck 0 |
| same | In place (check-only, with `next dev` ×2 and the Debug API running, none stopped) | **pass**, exit 0, 10:51:37, and again at 10:56:25 after Dev Bot's 10:55 addition (identical counts). Identical, except nextjs secrets lists 2 skipped secret files (`.env.example`, `.env.local`, never opened). `tsconfig.json` unchanged by the run, and no CRLF rewrite seen this time |
| `node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` | Temporary copy only (it rewrites `scripts/fixtures/`) | **33/33 pass**, exit 0. Regenerated fixtures are byte-identical to the in-place ones (36/36) |
| `--feature` with an API-only manifest (copy) | Copy | nextjs ran `secrets` only; pass |
| `--record` on a copy of `handoff.md` | Copy | Only `pre-handoff:` lines + `pre_handoff_gate_at` changed; `testing` untouched |

### Planted-violation matrix (copy only, one plant per run, reverted after each)

| # | Planted | Check | Exit | Message | Value printed? |
|---|---------|-------|------|---------|----------------|
| 1 | CRLF `.ts` in nextjs | eol | 1 | `eol src/planted-crlf.ts expected lf, found crlf` | n/a |
| 2 | LF `.cs` in API | eol | 1 | `eol Api.Framework/PlantedLf.cs expected crlf, found lf` | n/a |
| 3 | BOM `.cs` | eol | 1 | `eol-bom Api.Framework/PlantedBom.cs bom` | n/a |
| 4 | No final newline `.ts` | eol | 1 | `eol src/planted-nonl.ts no final newline` | n/a |
| 5 | `appsettings.Development.json` `ConnectionStrings.Planted` with `Password=NOT_A_REAL_SECRET` | secrets | 1 | `secret-connection-string-password ...appsettings.Development.json:2 [ConnectionStrings.Planted]` | No |
| 6 | `Jwt.Secret` = mixed-case dummy | secrets | 1 | `secret-json-credential ... [Jwt.Secret]` | No |
| 7 | `Jwt.Secret` = `NOT_A_REAL_SECRET` (all caps) | secrets | **0** | **missed** (F-02) | No |
| 8 | Comment in appsettings + `Jwt.Secret` mixed-case dummy | secrets | **0** | **missed** (F-01) | No |
| 9 | C# `?? "Host=...;Password=NOT_A_REAL_SECRET"` | secrets | 1 | `secret-connection-string-password Api.Framework.Data/PlantedFactory.cs:3` | No |
| 10 | `Password=` value in UI `README.md` | secrets | 1 | `secret-connection-string-password README.md:87` | No |
| 11 | Password literal in `e2e/support/planted.ts` (D11) | secrets | 1 | `secret-code-literal e2e/support/planted.ts:1 [password]` | No |
| 12 | Same 30-word paragraph in UI `README.md` + `AGENTS.md` | docs-dup | 1 | `docs-dup AGENTS.md:61, README.md:87 "Planted review paragraph: ..."` | n/a |
| 13 | TS type error | typecheck | 1 | `typecheck:TS2322 src/planted-type-error.ts:1 ...` | n/a |
| 14 | Rules-of-hooks error | lint | 1 | `lint:react-hooks/rules-of-hooks src/planted-lint.tsx:5 ...` | n/a |
| 15 | Same lint error under `e2e/` (D11) | lint | 0 | correctly ignored | n/a |
| 16 | Failing Vitest test | unit | 1 | `unit nextjs -> fail (10 passed, 1 failed, 5 files)` | n/a |
| 17 | Failing xUnit test | unit | 1 | `unit api-framework -> fail (52 passed, 1 failed)` | n/a |
| 18 | Allowlist entry expired | docs-dup | 1 | `allowlist-expired ... entries[0] ... expired 2020-01-01` | n/a |
| 19 | New allowlist entry with a `value` | secrets | 1 | `PROBLEM allowlist entries[0]: must not contain a value` | No |
| 20 | New allowlist entry without `expires` | secrets | 1 | `PROBLEM allowlist entries[0]: missing expires` | n/a |
| 21 | New unused allowlist entry | secrets | 0 | silent (F-03) | n/a |
| 22 | `.env.local` with a dummy password | secrets | 0 | correctly skipped: `skipped by pattern (not opened)` | No |

Self-test fixtures cover cases 1–6, 9, 12–14 (and private keys, a TS credential literal, mixed endings, the excluded `bin/`, secret files and expired entries). They don't cover 7, 8, 11, 15–17 or 19–21 (F-07).

### Line-ending normalisation spot-check

I compared all 448 files in `%TEMP%\gate\eol-backup-20261009104442` (216 API, 232 UI) with the current files, normalising both for line endings, BOM and final newline:

| Target | Byte-identical | Endings / BOM / final newline only | Content differs | Missing |
|--------|----------------|-----------------------------------|-----------------|---------|
| API.Framework | 165 | 50 (24 `.cs`, 19 `.md`, 1 `.mdc`, 3 `.csproj`, 2 `.json`, 1 `.sln`) | 1: `AGENTS.md` | 0 |
| UI.NextJs.Framework | 57 | 171 (82 `.ts`, 56 `.tsx`, 22 `.css`, 5 `.json`, 2 `.md`, 2 `.gitignore`, 1 `.cjs`, 1 `.mts`) | 4: `README.md`, `AGENTS.md`, `tsconfig.json`, `tsconfig.tsbuildinfo` | 0 |

Every content difference is a later, manifest-listed edit: the T-GATE-005 Verify / gate lines in both `AGENTS.md` files and the UI `README.md`, the dev-server-added `.next-test-tb` include in `tsconfig.json` (F-05), and build output (`tsbuildinfo`). Three of those files were also normalised before they were edited: API `AGENTS.md` (mixed endings in the backup), UI `README.md` (BOM) and UI `tsconfig.json` (CRLF). Adding them gives 51 API / 173 UI, which matches Dev Bot's figures and per-type counts (UI `AGENTS.md` was already LF). **No unintended content changes.**

### Suggested tests

- `EnsureAsync_PasswordNotConfigured_CreatesNoUserAndReturnsFalse`, `EnsureAsync_PasswordConfigured_CreatesSystemAdmin`, `EnsureAsync_UserExists_IgnoresPassword` in `Api.Framework.Tests/Auth/DefaultUserSeederTests.cs` (F-04)
- Self-test: `api-bad/appsettings.Commented.json` (comment + `Jwt.Secret`) must fail; an all-caps credential value must fail (F-01, F-02)
- Self-test: an unused allowlist entry must produce a note (F-03); `--feature` / `--record` / D11 cases (F-07)

Checks run: as listed above. Lint wasn't run separately because it's part of the gate.

## Changes since last review

Iteration 1: n/a.

## Out of scope / pre-existing notes

These do not affect the verdict.

- **Plan Bot:** the DefaultUserSeeder deviation is now recorded (`plan.md` §6, T-GATE-008 Notes; History row 7). Still to do: add the seeded system-admin password to D1's rotation action for Neil.
- **Plan Bot (later version):** `.env.example` is never opened, because `review.scope_exclude` covers `**/.env*`. The security checklist expects `.env.example` to hold placeholders only, so a placeholder-only check for `.env.example` could be added later.
- **Plan Bot (later version):** the docs-dup allowlist accepts each `.cursor` ↔ `.claude` mirror pair, but nothing checks that the copies stay in sync. A "mirror drift" check would complement it.
- **Neil (not an agent):** rotate the dev DB password and the Jwt secret that were committed, and change the existing system-admin account's password in the dev database (its old password was a committed literal). Set `DefaultUser:Password` only if a fresh database needs the admin seeded. Delete the scratch folders `.next-devbot-warm` / `.next-test-tb` when convenient (see F-05).
- **Plan Bot / Test Bot:** since the 10:55 addition, the Test API reads `APIFW_TEST_ConnectionStrings__LoginConnection` / `APIFW_TEST_Jwt__Secret`. Plan Bot renamed `ai-framework.config.yaml` `testing.database.connection_env` and `secrets.test_db_connection_env` at 10:56. These still name the unprefixed variable: `ai-test-framework/checklists/reset-endpoint-safety-checklist.md:17`, `ai-test-framework/skills/add-test-data-reset/SKILL.md:15`, `:22` and `ai-test-framework/README.md:91`. They're framework docs, so I haven't edited them.
- **Neil:** the unprefixed user-level variables were deleted (History row 6), so the running Development API (started 10:35) will fail on its next restart until `ConnectionStrings:LoginConnection` and `Jwt:Secret` are set as user-secrets. That's expected and clearly reported, but worth knowing.
- The `next dev` CRLF rewrite of `tsconfig.json` didn't happen during this review (LF kept), but the watch-out in `handoff.md` still stands.
- The earlier manage-animals note ("Development settings contain a database password and a JWT secret in the files themselves") is resolved by T-GATE-008.
- T-GATE-007 (Review Bot's gate-enforced rules and stale "no test runner" lines) is separate Review Bot work and wasn't done in this round. No framework docs were edited.

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: Not applicable — direct hand-off. Logged in `reviews/review-log.md` (round 1).</sub>
