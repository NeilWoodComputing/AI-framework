# Review: DIRECT-system-rename-1 — Rename Unity to System and drop v1 from API.Framework routes

> **Round 2 (14:05): test verdict approve; final verdict Approve with comments.** Test Bot's run 2 passed T-RENAME-011/S1, so the earlier "Tests blocked" note is cleared. Code delta after 13:16 (CORS from config, F-02..F-06 follow-ups) reviewed: no new Minor or higher. Open: F-01 (Minor, Neil) plus Nits. Neil decides at merge; agents never merge.

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (History row 7, Dev Bot 12:51:40 BST) |
| Trigger | direct-handoff (`code_to_review: direct`; `code_to_test: direct`, D5) |
| Review scope | Plan scope (`direct_scope: plan`, D8): every manifest file (api 44, ui 51, tests 11, migrations 3), checked against the 11:20 backup zip extracted to a temporary folder |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | Not under git. Working tree as of 13:05 BST, compared with `D:\Users\nwood01\Documents\Candc\backups\ai-framework-pre-rename-20261009-1120.zip` |
| Linked tickets | T-RENAME-001 … T-RENAME-007 (Dev Bot). Reference only: T-RENAME-008 (Test Bot), T-RENAME-009 (Plan Bot, done), T-RENAME-011 (Neil / Dev Bot / Test Bot). T-RENAME-010 (Review Bot): **done 13:10** on Neil's go-ahead (13:09), three checklist lines only (see **Test review**) |
| Feature(s) | `ai-planning-framework/work/system-rename/` |
| Specs reviewed | None: no pages, controls or DB columns (`plan.md` header). Reference: `plan.md` §1–§9, D1–D16, tickets |
| Active API / UI | api-framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `AGENTS.md` + `.cursor/rules`; UI.NextJs.Framework `AGENTS.md`, `README.md`, `.cursor/rules`; `checklists/security-checklist.md`, `checklists/severity.md`; general practice where no rule applies |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 09/10/2026 13:07 code review · 13:15 test review · 14:05 test review round 2 + code delta (Europe/London) |
| Review iteration | 1 |

## Verdict

**Round 2 (14:05): Approve with comments** (final). Test review of run 2: **approve** (36 Pass · 0 Fail · 0 Waiting · 14 Not automated; T-RENAME-011/S1 passes). Code delta: CORS from `Cors:AllowedOrigins` is safe, and F-02..F-06 and F-08 are resolved. Open: Minor 1 (F-01), Nit 7 (F-07, F-10..F-15), note F-09. See **Test review (round 2)**, **Code delta (after 13:16)** and **Findings (round 2)**. The round-1 text below is kept as written.

**Round 1 (13:16):** tests were blocked on T-RENAME-011/S1 at that point (cleared in round 2). **Approve with comments** (final: code review + test review, option B / D5)

- Code review (13:07): Approve with comments.
- Test review (13:15, Test Bot run 1 + 13:15 addendum): **blocked-noted**. 35 Pass · 0 Fail · 1 Waiting (T-RENAME-011/S1, Neil) · 14 Not automated, all 14 justified (see **Test review**). No code or test defects to route.

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 0 | 3 | 6 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`. F-01..F-06 come from the code review; F-07..F-09 from the test review.

## Summary

This is a careful, well-scoped rename, and the risky parts are done right.

- **Migration.** It updates the seeded rows by id only. The 16 older migration files are byte-identical to the backup. The model snapshot changed only in the 7 seeded values, and the new Designer file matches it exactly.
- **Routes.** All 14 controllers keep their routes with only the `v{version:apiVersion}/` prefix removed, so every route is otherwise unchanged. Authorisation attributes are untouched. Swagger lists 46 paths and 66 operations, matching the 66 `[Http*]` actions in the code, with no `/v1` anywhere.
- **UI.** The UI side is a clean rename with no logic changes, apart from `getApiUrl` and the `dev-test.mjs` default.
- **Docs.** The `.cursor` and `.claude` copies match word for word.
- **Checks.** The gate passed on a temporary copy and in place, and the self-test is 64/64.

The three Minor findings are not code defects in the hand-off:

- **F-01:** the Angular example UI still points at API.Framework's `/v1` routes. This is a scope gap for Neil to decide.
- **F-02:** the rollback path for the database isn't written down.
- **F-03:** no unit test pins the issuer change.

## Review scope

| Area | Files | How reviewed |
|------|-------|--------------|
| API code | `Program.cs`, `Api.Framework.csproj`, 14 controllers (moved from `Controllers/V1`), `appsettings.json`, `appsettings.Test.json`, `JwtOptions.cs`, `LoginFeatures.cs`, `LoginPermissions.cs`, `Api.Framework.http`, `AnimalPoliciesTests.cs` | Full diff against the backup; non-route lines of each controller compared one by one |
| Migrations | `20261009114033_RenameUnityToSystem.cs` / `.Designer.cs`, `LoginDbContextModelSnapshot.cs`, 16 older files | Byte compare against the backup; the snapshot diff; Designer compared with the snapshot |
| API docs | `AGENTS.md`, `CLAUDE.md`, 6 rules × 2 copies, 3 skills × 2 copies | Word diff; `.cursor` and `.claude` compared for every rule and skill (9 rules, 8 skills) |
| UI code | 8 renamed `system-*` files, barrel, 30 other `src` files, `environment.ts`, `package.json`, `package-lock.json`, `scripts/dev-test.mjs` | Full diff; the only diff lines without "unity" / "system" in them are one comment (`animal.model.ts`) |
| UI scaffolding | `e2e/helpers/config.ts`, `e2e/helpers/authentication.ts`, `e2e/setup/sign-in-child.cjs` | Diff; `getApiUrl` exercised with 11 inputs on the temporary copy |
| Gate | `pre-handoff-checks.selftest.mjs`, 4 fixture files | Diff (values only, secrets redacted); self-test run |
| Framework docs | `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc`, `loops/feature-build.md` | Word diff |

The manifest matches the actual changes. Every changed file not in the manifest belongs to another owner:

- **Test Bot (T-RENAME-008):** `animals.steps.ts`, `auth.steps.ts`, the new `e2e/features/system-rename/*`, and 4 `ai-test-framework` files.
- **Plan Bot (T-RENAME-009):** `ai-framework.config.yaml`.
- **Unrelated "parking" change:** `handoff/README.md` and `handoff/templates/handoff.md`.

Two manifest entries are deliberately unchanged ("kept" notes): `ReferenceDataSchemaBinding.cs` (D10) and `TestDataGuardAndServiceTests.cs` (D7).

## Findings

| ID | File:line | Severity | Category | Comment | Suggested fix | Fix by |
|----|-----------|----------|----------|---------|---------------|--------|
| F-01 | `ai-code-framework/ui/UI.Angular.Framework/src/environments/environment.ts:7` (and `API.Framework/.cursor/rules/api-framework-ui-contract.mdc:8`, `.claude/rules/api-framework-ui-contract.md:6`) | Minor | Scope / consumers | The Angular example UI's local environment calls API.Framework at `http://localhost:5088/v1/` (API.Framework's Development port). With v1 removed, every call it makes will 404 once the Development API restarts on the new code. The plan treats UI.Angular as a keep-as-is real repo (§4). But the API's own UI-contract rule says API.Framework serves "UI.NextJs.Framework (and the Angular example UI) over versionless routes", and CORS still allows `localhost:4200` for it. The plan didn't list this consumer in §5.5. | Neil decides. Either update that one `apiRoot` line (drop `/v1/`, as a T-RENAME-005 follow-up), or reword the UI-contract rule in both copies so it doesn't claim the Angular example UI uses versionless routes. | Neil → Plan Bot (scope), then Dev Bot |
| F-02 | `ai-planning-framework/work/system-rename/plan.md:11`, `:196` (rollback) | Minor | Data / operations | The zip is "the only rollback", but it can't roll back the databases. Once the migration has run (`api_framework_test` now; `unity_login` on the next Development start, because `MigrateDatabase` is true there), restoring the zip gives old code that expects `UnityBasicFeatures` against System-named rows. `TenantService.cs:335` then returns 400 "The feature catalogue has not been seeded" on every tenant save. `__ef_migrations_history` also keeps a row for a migration the old code doesn't know, and the old code can't run its `Down()`. | Add a rollback order to the plan / hand-off: with the **new** code, run `dotnet ef database update 20261008150221_AddAnimals` against each migrated database, then restore the zip. | Plan Bot (plan §9) or Dev Bot (hand-off note) |
| F-03 | `Api.Framework.Services/Auth/TokenService.cs:73` (no test) | Minor | Tests / security | T-RENAME-002/S2 ("a `unity-login` token is rejected with 401") rests on a manual smoke only. No unit test covers `CreateValidationParameters` rejecting the old issuer or audience, so a future edit to `JwtOptions` or the appsettings could silently accept old tokens. | Add a small `TokenServiceTests` with a throw-away 32-byte test key. A token issued for `unity-login` fails validation with `SecurityTokenInvalidIssuerException`, and one for `system-login` passes. | Dev Bot |
| F-04 | `ai-code-framework/ui/UI.NextJs.Framework/e2e/helpers/config.ts:13` | Nit | Robustness | Exercised on the copy: unset or `""` → default; trailing `/` → trimmed; `/v1`, `/v1/` and ` …/V1 ` → a clear error that never prints the value. Good. But a whitespace-only `API_URL` returns `""` instead of the default, which later fails as "Invalid URL" rather than with a clear message. There is also no test for the guard. | Treat a blank-after-trim value like unset, and add a small test for the 5 cases. | Dev Bot |
| F-05 | `ai-code-framework/ui/UI.NextJs.Framework/scripts/dev-test.mjs:27` | Nit | Robustness | `E2E_UI_API_ROOT` goes straight into `NEXT_PUBLIC_SYSTEM_API_ROOT` with no stale-`/v1` check, unlike `getApiUrl`. It's not set today (D13), so this is just for consistency. | The same one-line check as `getApiUrl` (fail with a clear message on a trailing `/v1`). | Dev Bot |
| F-06 | `handoff.md` History row 7 / hand-off message | Nit | Docs | The hand-off gives the rollback zip as `backups\ai-framework-pre-rename-20261009-1120.zip`. It's actually at `D:\Users\nwood01\Documents\Candc\backups\…` (the `Candc` folder, not `ai-framework`). The plan has the full path right. | Use the full path in future notes. | Dev Bot |
| F-07 | `e2e/features/system-rename/SystemRename.feature` (T-RENAME-003/S2) | Nit | Tests | 003/S2's "the build passes" is covered by the gate typecheck, `tsc --noEmit` on e2e and every visited page compiling in `next dev`, but `npm run build` itself wasn't run (it would share a build folder with a running UI). | Next time no UI is running, run `npm run build` once, or build into a scratch `NEXT_DIST_DIR` and delete it afterwards. | Test Bot |
| F-08 | `e2e/features/system-rename/system-rename.steps.ts:231-233` | Nit | Tests | "no page error occurred" waits a fixed 500 ms before reading the errors. That's fine on today's timings, but it's a sleep, not a condition. | Wait for a settled signal (for example the sign-in link being visible, which the previous step already asserts) and then check the errors, with no fixed timeout. | Test Bot |
| F-09 | `system-rename.steps.ts:162-174` (T-RENAME-004/S4 refresh step) | Nit | Security (test artefacts) | On a **failing** run only, the retain-on-failure trace could hold the short-lived refresh token passed to `addCookies`, as it already can for the access token in `usePersona`. Never a password. This is the same as the F-49 acceptance in manage-animals. | No change needed. If a failed trace is ever shared, treat it as holding a live test token. | Note (Neil) |

## Spec conformance (per control)

n/a: no UI controls in this plan.

## Data mapping (per control)

n/a: no DB columns change. The data change is the seeded names; see **Migration safety** under Security and data.

## Acceptance criteria coverage (per scenario)

| Scenario | Evidence (code review / my runs) | Status |
|----------|-----------------------------------|--------|
| T-RENAME-001/S1 | Anonymous: `GET /schemas/sign-in` 200. Authenticated S1 calls not repeated (no sign-in by Review Bot); Dev Bot's smoke and Test Bot's run cover them | Met (anon) |
| 001/S2 | `/v1/Animal`, `/v1/schemas/sign-in`, `/v1/Authorisation/Me`, `/v1/ReferenceData` → 404 on the Test API | Met |
| 001/S3 | No `ApiVersion`, `Asp.Versioning`, `apiVersion}`, `x-api-version` or `MapToApiVersion` outside bin / obj. Both packages are gone, and responses carry no `api-supported-versions` header | Met |
| 001/S4 | No `Controllers/V1` folder. 14 controllers under `Controllers/{Area}`; no `Controllers.V1` namespace or import | Met |
| 001/S5 | Swagger: 46 paths / 66 operations (= 66 `[Http*]` actions), 0 with `/v1`, no version parameter; doc `v1` kept (D6); UI 200 | Met |
| 001/S6 | Release build + 57/57 tests in the gate (copy and in place) | Met |
| 002/S1 | `SystemUi` on both `AddPolicy` and `UseCors`. Preflight from `http://localhost:3003` → 204 with `Access-Control-Allow-Origin`; another origin gets no CORS headers | Met |
| 002/S2 | Issuer and audience are `system-login` in `appsettings.json`, `appsettings.Test.json` and the `JwtOptions` defaults. No override in `appsettings.Development.json` (user-secrets not opened). `ValidateIssuer` / `ValidateAudience` true. I couldn't mint an old token without the signing key; see F-03 | Met by code; test gap F-03 |
| 002/S3 | 5 `UpdateData` by id cover all 7 old values in the snapshot; no inserts or deletes, so row counts can't change | Met |
| 002/S4 | 16 / 16 byte-identical to the zip; only the snapshot differs | Met |
| 002/S5 | No `namespace …System`, `class System` or `Api.Framework.System` | Met |
| 002/S6 | Remaining API hits: `unity_login` (D7) and real Unity.API / Unity text (D10); see the hit table | Met |
| 003/S1–S6 | No `unity` identifiers or file names in `src`, `scripts` or `e2e/helpers`. Barrel renamed; keyword `'system'` (`system-schema-validation.ts:269`, nothing reads it by value). `NEXT_PUBLIC_SYSTEM_*` only. Package name in 3 places, dependency tree unchanged. Collision counts unchanged (old = new for `IsSystemAdmin`, `@design-system`, `--system-red`, `--system-green`, `system-ui`). tsc / lint / vitest pass | Met |
| 004/S1 | Anonymous `GET http://localhost:3003/auth/sign-in`: title "System UI Next", "System Login", "Sign in with your System credentials." | Met |
| 004/S2–S6 | Keys and events renamed in every dispatcher and listener, and the inline theme script matches `ThemeProvider`. Old storage: `getSession()` reads only `system-auth-session`, so an existing browser is signed out once; theme falls back to the default (intended, §5.4). Runtime behaviour is for Test Bot's run | Met by code |
| 005/S1–S3 | `getApiUrl` exercised with 11 inputs (F-04 for the blank case) | Met |
| 005/S4–S5 | `dev-test.mjs` default `https://localhost:7188/`. `.http` and READMEs have no `/v1` or `NEXT_PUBLIC_UNITY` | Met |
| 006/S1–S4 | Docs: no API.Framework `v1` / `Controllers/V1` guidance left. `.cursor` = `.claude` for all 9 rules and 8 skills. Real Unity references kept. Env vars documented as Neil-owned | Met |
| 007/S1–S3 | Self-test 64/64; fixtures hold no `unity-login` or `/v1/`; gate pass | Met |

## Security and data

### Migration safety (T-RENAME-002)

- **By id only:** 5 `UpdateData` calls keyed on `id`: features `…0201` (name) and `…0203` (name + permission_category), and permissions `…0003` (category + name), `…0004` and `…0012` (category). These are the only 7 `Unity` values in the old snapshot, so none is missed and no other row is touched.
- **Idempotent:** EF applies it once (one history row). Re-running the same UPDATEs gives the same result, and an UPDATE that matches no row changes nothing.
- **Down():** restores exactly the old values (checked against the old snapshot line by line).
- **No data loss:** only the text of 5 seeded rows changes. Ids stay the same, so tenant features, permission groups and grants keep working.
- **Snapshot:** the diff is exactly those 7 values. The new `.Designer.cs` is identical to the snapshot apart from the method name (`BuildTargetModel` / `BuildModel`). `ProductVersion` is 10.0.9.
- **`__ef_migrations_history`:** gets one new row, `20261009114033_RenameUnityToSystem`, in schema `auth`. Rolling back needs the order in F-02.
- **Existing databases:**
  - `api_framework_test`: migrated by Dev Bot. Master reset truncates every EF-model table and reseeds from the model (`TestDataService.cs:26-60`), so the reset baseline now carries the System names and matches the code. The reset first calls `EnsureSchemaCurrentAsync`, so an unmigrated Test DB is refused rather than half-seeded. Personas and test data don't use the renamed names (0 hits).
  - `unity_login` (dev): not migrated yet. `appsettings.Development.json` sets `MigrateDatabase: true`, so it migrates on the next Development start. **Until then**, the running Development API (started 10:58, Debug build, old code) still serves `/v1` routes (44 of 44 paths) and `unity-login` tokens. The restart is already Neil's T-RENAME-011 step 7.
- **Name-based lookups:** `TenantService.cs:335` finds the basic feature by `LoginFeatures.BasicName`. That's fine with the migration applied, and it is why F-02 matters on rollback.

### Auth

- **Old tokens rejected:** an old `unity-login` token gets 401, as intended per §5.2 and T-RENAME-002/S2. Issuing (`TokenService.cs:38-39`) and validating (`:79-82`) both read the same `JwtOptions`, so they can't drift. Old tokens fail on issuer and audience.
- **Cookies:** the UI stores the JWT and refresh token in cookies `JWT` / `rT` (unchanged names). The UI doesn't validate the issuer, so there's nothing to keep in step there.
- **One-time logout:**
  - A browser with old `unity-auth-session` is signed out once (the session key changed). This is intended per §5.4 / T-RENAME-004/S6.
  - The old `JWT` / `rT` cookies stay until the next sign-in overwrites them. Harmless, because `getSession()` needs the new session key.
  - If only `rT` survives, the refresh runs and issues a fresh `system-login` token, so that user stays signed in. Also fine.
- **Unchanged:** authorisation policies and attributes (diff of every controller), and the `SignIn` / `Me` / `TestData` routes.
- **Test reset route:** `TestData/Reset/master` and `/{scenarioKey}` appear in the Test Swagger. `e2e/helpers/test-data.ts` builds `${getApiUrl()}/TestData/Reset/…`, and `ai-framework.config.yaml` `master_route` / `batch_route` have no `v1`.
- **No secrets:** no value appears in any changed file. Fixture secrets are unchanged dummies. I didn't open `.env*`, `secrets.json` or user-secrets.

### getApiUrl and the stale-/v1 guard

It fails fast rather than masking misconfiguration: a trailing `/v1` (any case, with or without `/`) throws a message naming `API_URL` without printing its value.

What it doesn't cover:

- the UI app itself: `NEXT_PUBLIC_SYSTEM_API_ROOT` with `/v1/`, or unset, which falls back to the Unity.API v2 default (D14, accepted; that's why N1 must happen at the same time as the code change);
- `dev-test.mjs` (F-05);
- a blank `API_URL` (F-04).

## Tests

### Gate, self-test and unit tests

| Run | Where | Result |
|-----|-------|--------|
| Gate `--feature ai-planning-framework/work/system-rename` | Temporary copy `%TEMP%\rb-sr\gate` (13:03:48) | Pass. API: eol 218, secrets 218, docs-dup 22 (53 allowlisted), unit **57/57**. UI: lint 150 files 0 errors / 2 warnings, typecheck 0, eol 231, secrets 231, docs-dup 17, unit **10/10** |
| Self-test | Temporary copy | **64/64**, exit 0 (also with `--skip-record`); committed fixtures byte-identical afterwards |
| Gate, check-only (no `--record`) | In place (13:05:13) | Pass. Same as Dev Bot's 12:51:05 record except UI eol / secrets **231** files instead of 229: Test Bot's two new `e2e/features/system-rename/*` files arrived after 12:51. `handoff.md` unchanged by the run. The running Test API's `bin\Release` DLL was not rewritten (mtime still 12:57:37), and that API stayed up |

The e2e TypeScript check and `bddgen` (Dev Bot's verification lines) were not repeated. The e2e package's own `node_modules` wasn't in the copy, and the e2e scenarios are Test Bot's run (D5).

### Anonymous smoke (Test API, started 12:58 by `dotnet run -c Release --launch-profile Test`; not restarted)

| Call | Result |
|------|--------|
| `GET /swagger/index.html`, `/swagger/v1/swagger.json` | 200, 200 (46 paths, 66 operations, 0 `/v1`) |
| `GET /schemas/sign-in` (anonymous endpoint) | 200; no `api-supported-versions` header |
| `GET /Animal`, `/Authorisation/Me`, `/schemas/create-animal`, `/ReferenceData`, `/Tenants/GetAllDetailed` (no token) | 401 each: routes exist, auth enforced |
| `GET /Animal` with a garbage bearer token | 401 |
| `GET /v1/Animal`, `/v1/schemas/sign-in`, `/v1/Authorisation/Me`, `/v1/ReferenceData` | 404 each |
| `OPTIONS /Animal` from `http://localhost:3003` | 204 with `Access-Control-Allow-Origin: http://localhost:3003` |
| `OPTIONS /Animal` from another origin | 204 with no CORS headers |
| UI `GET http://localhost:3003/auth/sign-in` | Title "System UI Next", "System Login", intro text, inline script uses `system-theme` |
| Development API `GET https://localhost:7088/swagger/v1/swagger.json` | 44 paths, all `/v1`: still the old build (started 10:58), see Migration safety |

What I didn't do: no sign-in, no authenticated calls, no token minting (I don't have the signing key and didn't look for it), and no POST to `TestData/Reset` (destructive, and Test Bot may be mid-run).

Dev Bot's smoke (verification line 89) re-signed a token with the Test signing key to show the issuer check. No value was recorded, which is fine for a local Test key, but worth Neil knowing.

### Remaining "Unity" and "/v1" hits (active targets, excluding bin / obj / node_modules / `.next*` / Migrations / `.env*` / `.auth`)

| Where | Hit | Class |
|-------|-----|-------|
| API `TestDataGuardAndServiceTests.cs:89`, API rules `api-framework-testing` (both copies), UI `e2e/README.md:12, 16` | `unity_login` | D7 (DB name kept) |
| API `ReferenceDataSchemaBinding.cs:6`, rules `json-schema-forms` (both, ×2), `api-framework-ui-contract` (both), `api-framework-overview` (both), skills `crud-feature` / `feature-loop` / `tests` (both), `AGENTS.md:71` | Unity.API / "same idea as Unity" / don't-copy guidance | D10 (real product) |
| API `Program.cs:55, 58, 124` | Swagger doc `"v1"`, `/swagger/v1/swagger.json` | D6 |
| API rules / skills / `AGENTS.md:3, 65`; UI `README.md:21`, `AGENTS.md:40`, `nextjs-framework-overview.mdc:45`, `e2e/README.md:33` | "versionless … (no `/v1`)" | Docs guidance (intended) |
| UI `e2e/helpers/config.ts:9, 15, 17-18` | stale-`/v1` guard | Intended (T-RENAME-005) |
| UI `CompanyLoader.tsx:12`, `CompanyLoader.module.css:1`, `ModalShell.tsx:14, 92`, `ModalShell.module.css:85`, `RoutedModalLoadingFallback.tsx:16`, `PendingRoutedModalHost.tsx:13`, `use-modal-navigate.ts:11`, `ConfirmModal.tsx:24`, `use-json-schema-entity-form.ts:57`, `use-entity-form-state.ts:36`, `abstract-updated.service.ts:4`, `normalize-paged-search-response.ts:12`, `reference-data-type-summary.model.ts:4`, `system-json-schema.model.ts:65`, `normalize-auth-state.ts:16, 58`, `auth-cookies.ts:1` | comments naming the real Unity UI / Unity.API as the origin | D10 |
| UI `DesignSystemShowcase.tsx:54, 116, 172`, `layout.tsx:8` (meta description "Unity-style design system") | visible text naming the real Unity design system | D10 (the showcase lines are named in D10; the meta description follows the same rule) |
| UI `README.md:3`, `AGENTS.md:3`, `.cursor/rules/README.md:3`, `nextjs-framework-overview.mdc:8`, `nextjs-css.mdc:41`, `nextjs-modal-routing.mdc:56-65`, `design-system/README.md:3` | "mirroring Unity.UI.Framework" / "Unity UI mirror" | D10 (names what the starter mirrors) |
| UI `e2e/features/system-rename/*` (new), `animals.steps.ts`, `auth.steps.ts` | `/v1` and `unity-*` as *negative* assertions | Test Bot, T-RENAME-008 (not in this code review) |
| `ai-test-framework/examples/manage-animals-test-plan.md:74, 117` | `v1/Animal` | Historical example, kept (T-RENAME-008 step 2) |
| `ai-test-framework/skills/write-api-unit-tests/SKILL.md:20` | `Controllers/V1\|V2` | Unity.API conventions section (real repo) |
| `ai-review-framework/checklists/api-checklist.md:78`, `ui-nextjs-checklist.md:9, 10` | `Controllers/V1/{Area}`, `NEXT_PUBLIC_UNITY_API_ROOT`, `unityApiFetch` / `unity-api-fetch.ts` | **T-RENAME-010: done 13:10** on Neil's go-ahead (all three lines, including line 10, which the ticket missed) |
| `ui/UI.Angular.Framework/src/environments/environment.ts:7` | `http://localhost:5088/v1/` | **Missed consumer**: F-01 |

No missed hits in the active API or UI code.

### Suggested tests

- `TokenServiceTests`: old issuer and audience rejected, new accepted (F-03).
- A small test for `getApiUrl` (unset, blank, trailing `/`, `/v1`, `/V1/`) (F-04).

## Test review (option B): Test Bot run 1 + 13:15 addendum

Round 1: tests were blocked on T-RENAME-011/S1 (cleared in round 2, see **Test review (round 2)**). Round-1 test verdict **blocked-noted**: approval is allowed (`testing.blocked_tests_allow_approval`), and Neil decides at merge.

| Item | Result |
|------|--------|
| Report | `tests/TEST-system-rename-1-report.md` (run 1, e2e result of record run 2 13:03:55–13:07:17; addendum 13:15), `handoff.md` `testing` (status `blocked`, round 1, test-fix 0/5) |
| Counts | 50 scenarios: **35 Pass · 0 Fail · 0 Blocked · 1 Waiting · 14 Not automated**. Unit 57/57 (Release). E2E 80/80 = 6 setup + 67 manage-animals (regression, unchanged) + 7 `@system-rename`. Addendum re-run of `@T-RENAME-004/S4`: 7/7 (master reset + 6 setup + S4) |
| Waiting | T-RENAME-011/S1: Neil's N1 (`NEXT_PUBLIC_UNITY_*` → `NEXT_PUBLIC_SYSTEM_*` in `.env.local`, root without `/v1`), then a plain `npm run dev`. Agents never open `.env*`. The dev:test equivalent passes (`@T-RENAME-005/S4`) |
| Failures | None in the result of record. Run 1's T-ANIMAL-003/S4 failure was a test defect (`cellByHeader` read the headers before the grid rendered). The fix waits for the first header cell and the row first (`animals.steps.ts:18-29`), and it passed in run 2. Not a routed round, so `test_fix_cycle` stays 0, which is correct |
| Safety gate | `api_framework_test` checked before each run (12:59:07, 13:03:49, 13:12:01); only the database name and host were printed |

### Rulings

- **T-RENAME-004/S4 (cross-tab):** Plan Bot ruled at 13:10 that the same tab is enough. That's recorded in History rows 9 and 10 and in the ticket (saved 13:12:09): the heading is "Auth events still work in the same tab", the Given / When / Then are now same-tab, and the Notes say cross-tab is out of scope. I checked the scenario against the new wording.
  - Given: signed in with the session under `system-auth-session`.
  - When: sign out in that tab.
  - Then: `system-auth-cleared` fires (`the "system-auth-cleared" auth event fired`), `system-auth-session` is removed (`sessionStorage has nothing under …`), and the same tab is signed out (`/auth/sign-in`, "System Login").
  - Every Then is asserted, so this is a **full Pass**.
  - The extra refresh check uses the app's real `refreshAuthToken()` path. There is no JWT cookie, and the refresh token comes from a fresh untraced Node sign-in. The check asserts `system-auth-refreshed`, a new JWT cookie, signed-in state, the session still under `system-auth-session`, and nothing under `unity-auth-session`. That's a real check with no mocks.
- **T-RENAME-005/S5 (literal "/v1"):**
  - **Against the original wording**, "When I search for "/v1" … Then there are no matches", it was **not** a literal pass: `README.md:21` and `e2e/README.md:33` match. My ruling would have been a Plan Bot wording fix, not a test-side allowlist. An allowlist makes the test disagree with the scenario text and could hide a future real `/v1` root in those files.
  - **Plan Bot has now made exactly that fix** (History row 10, Neil 2026-10-09; ticket lines 70-73 and Note line 94). The Then now reads: "no configured API root, route, default value or code path contains "/v1" … the only "/v1" matches are prose that explicitly explains /v1 was removed … and the S3 guard".
  - Both README matches are explanatory prose ("The API root has no `/v1/` segment", "No `/v1`: a value ending in `/v1` fails fast"). `config.ts` keeps `/v1` only in the guard, and `dev-test.mjs` and `Api.Framework.http` have 0 matches. **The pass on intent stands** as a Pass against the clarified Then.

### Not automated (14): classification

The option-B rule: Not automated means Untested (Minor) unless the plan or ticket marks the scenario manual / review-only, or the review covers it. D8 makes Review Bot's full review cover every manifest file. I re-checked each scenario myself at 13:1x rather than relying on the report.

| Scenario | Class | Evidence (Review Bot) |
|----------|-------|-----------------------|
| T-RENAME-002/S3 (migration on a DB at the previous migration) | **Review-verified** (D8), justified | Code review: 5 `UpdateData` calls by id cover all 7 old seeded values. There are no inserts or deletes, so row counts can't change, and `Down()` restores them exactly. Dev Bot's apply on `api_framework_test` (features 7 / permissions 25 / tenant_features 14 before and after; 0 unity names). The master reset reseeds from the renamed HasData in every run. It's a one-off database state that e2e can't reproduce |
| T-RENAME-004/S5 (token refresh still notifies) | **Not automatable, recorded by the plan owner**, justified | History row 10 (Plan Bot, Neil 2026-10-09): "refresh is S5, not automatable" (the Given "about to expire" needs a faked token or a clock hook). The Then (`system-auth-refreshed` fires, still signed in) is now observed through the real refresh path in the extended S4. Code: `token-refresh.service.ts:46` dispatches it and `AuthProvider.tsx:46` listens |
| T-RENAME-005/S2 (default API URL) | **Review-verified by execution**, justified | I ran `getApiUrl()` from a byte copy of `e2e/helpers/config.ts` on the box: unset → `http://localhost:5188`, `""` → `http://localhost:5188` |
| T-RENAME-005/S3 (stale `/v1` reported) | **Review-verified by execution**, justified | Same run: `…/v1`, `…/v1/` and `…/V1` throw "API_URL ends with /v1 … Drop the trailing /v1 from the API_URL environment variable …". It names API_URL and never prints the value. F-04 (blank value) still stands |
| T-RENAME-006/S1 (rules describe versionless routes) | **Review-verified** (D8), justified | Every `v1` / `V1` / `apiVersion` match in API.Framework, UI and ai-code-framework rules, skills and AGENTS/README says routes have **no** version (for example `api-framework-controllers.mdc:35`, `ui-contract SKILL.md:18`). The rest are Unity.API / Angular (D10). The ui-contract rule's "(and the Angular example UI)" claim is F-01 |
| T-RENAME-006/S2 (both rule copies match) | **Review-verified**, justified | 9 of 9 rules (body after front matter) and 8 of 8 skills are identical between `.cursor` and `.claude` |
| T-RENAME-006/S3 (real Unity references kept) | **Review-verified**, justified | Unity.API / Unity.UI.Framework / UI.Angular mention counts are unchanged in every in-scope doc against the 11:20 zip, with one exception. `loops/feature-build.md:78` goes 7 → 6: the Next.js line said "call Unity.API through `unityApiFetch`" and now says "call the active API through `systemApiFetch`". That line described the Next.js UI's own fetch helper, whose identifier was renamed, so the change is required. It's in the manifest and isn't a real-repo reference. Unity.API / Angular repo docs outside the zip weren't touched |
| T-RENAME-006/S4 (env var names in docs) | **Review-verified**, justified | 0 `NEXT_PUBLIC_UNITY` in ai-code-framework docs. Neil-owned `NEXT_PUBLIC_SYSTEM_API_ROOT` / `_APP_ID` are documented at `nextjs-framework-overview.mdc:46, 48` and `UI AGENTS.md:41` |
| T-RENAME-009/S1 (config routes have no v1) | **Review-verified**, justified | `ai-framework.config.yaml` parses (PyYAML). `api_base_url: <https://localhost:<api-port>>`, `master_route: TestData/Reset/master`, `batch_route: TestData/Reset/{scenarioKey}` |
| T-RENAME-009/S2 (Next.js description) | **Review-verified**, justified | The description names `NEXT_PUBLIC_SYSTEM_API_ROOT` and no longer says "Calls Unity.API v2 via NEXT_PUBLIC_UNITY_API_ROOT". It mentions the D14 fallback |
| T-RENAME-009/S3 (planning framework unchanged) | **Review-verified**, justified | Compared with the 11:20 zip: no ai-planning-framework framework file changed. The only differences are other features' `handoff.md` state (manage-animals and pre-handoff-checks recorded as merged 12:37, add-edit-contact parked 11:20; plan-bot on Neil's instruction), the new `work/system-rename/` folder, and a stale Office lock file `out/~$basic-form-sample.xlsx` that no longer exists |
| T-RENAME-009/S4 (real Unity entries stay) | **Review-verified**, justified | The config diff against the zip is only the Next.js description and the 3 routes. The unity-api, Angular and branch-pattern entries are byte-identical |
| T-RENAME-010/S1 (API checklist layout) | **Review-verified**, justified | Done 13:10: `api-checklist.md:78` now reads `Controllers/{Area}`, `Controllers/Schemas` (the folders exist under `Api.Framework/Controllers`: Animals, Auth, Directory, Examples, ReferenceData, Schemas, TestData; no V1) |
| T-RENAME-010/S2 (no `NEXT_PUBLIC_UNITY`) | **Review-verified**, justified | 0 `NEXT_PUBLIC_UNITY` in `ui-nextjs-checklist.md`. Line 10 also now names `systemApiFetch` / `system-api-fetch.ts` (exists, `export async function systemApiFetch` at line 68) |

None of the 14 is left Untested. Partial coverage inside passing rows:
- **002/S2:** the old-token 401 rests on Dev Bot's smoke, F-03 (Minor). Test Bot could also own it as 002/S2's unit-level scenario test.
- **003/S2:** `npm run build`, F-07 (Nit).

### Test code review

| Check | Result |
|-------|--------|
| Tags | Each of the 7 scenarios carries its explicit IDs (`@T-RENAME-001/S1 @T-RENAME-002/S2`, `@T-RENAME-001/S2`, `@T-RENAME-004/S1`, `@T-RENAME-004/S2 @T-RENAME-005/S4`, `@T-RENAME-004/S3`, `@T-RENAME-004/S4`, `@T-RENAME-004/S6`), plus `@system-rename` on the feature |
| Reset first | Every scenario's first step is `Given the test data is "animals.api.empty"` |
| No front-end mocks | No `page.route` / `context.route` / `route.fulfill` / HAR / MSW / stubbed fetch. Listeners only record (`page.on('request')`, `page.on('pageerror')`, `addInitScript` event counters). Sign-ins are the setup project's real SignInForm sessions (`usePersona`) and, for the S4 refresh, a real API sign-in over untraced Node HTTP. No faked tokens |
| Real Then assertions | Token `iss` / `aud` decoded and compared exactly. Status 200 / 404 plus a non-empty JSON body. Exact heading, text and title. Storage keys present / absent. Recorded API calls are checked for the origin and path and for having no `/v1/` or port 7104 (and the list must be non-empty, so the check isn't vacuous). Theme checked at `<body>` creation (pre-hydration) and after. Events counted. Signed-out link visible and sign-out absent. Page errors are empty |
| 004/S2 strength | The scenario restores the saved session, so its own "present" check is partly circular. But the setup project only saves a session it finds under `system-auth-session` (`authentication.ts:9, 62-67`), and the extended S4 now checks the app's own write after a real refresh (nothing under `unity-auth-session`). Adequate |
| Secrets in steps | No token, password or session value is logged. The refresh step throws only `API sign-in as <name> failed with HTTP <status>`. Residual trace exposure on failure only: F-09 |
| Weak spots | F-08 (fixed 500 ms wait). Nothing else |

### Test Bot's fixes

- **F-51:** `fillStable` (`animals.steps.ts`) fills once and asserts the value within 5 s with "value not kept after one fill (… F-51 forbids a silent retry)". There is no retry loop. **Resolved.**
- **F-56:** `.next-test-tb` is gone (checked), and `tsconfig.json` is byte-identical (per the report). The pre-rename dev:test UI was replaced by a fresh one, and Neil's Development API (pid 35876) was left running. **Resolved.**
  - Note for Neil: D16 said to leave `.next-test` / `.next-test-tb` "for the next build to overwrite; no manual deletion". Deleting `.next-test-tb` (unreferenced build output, excluded from the gate) follows F-56 rather than D16. It's harmless, but recorded so the two decisions are reconciled.
- **cellByHeader** (run-1 test defect): fixed as above.
- **T-RENAME-008:** the observers match versionless `/Animal`, `/Animal/{id}` and `/schemas/create-animal` (`animals.steps.ts:50-59`), and `auth.steps.ts` names `system-auth-session`. 008/S1–S3 pass.

### Secret re-scan (Review Bot, counts only)

- **Values:** the 7 user-level values (6 `E2E_*_PASSWORD` + `APIFW_TEST_Jwt__Secret`), read in memory, in raw, URL-encoded, JSON-escaped, HTML-encoded and base64 forms. The scanner self-test found a planted URL-encoded copy, which was then deleted.
- **Scope:** **197 files + 3 entries in the HTML report's embedded zip**, including the two live logs (`api.log`, `ui.log`) read with shared access:
  - `e2e/playwright-report` (1), `e2e/test-results` (2), `e2e/.auth` (12);
  - `%TEMP%\tb-run` (113);
  - `Api.Framework.Tests/TestResults` (3);
  - `work/system-rename` (19);
  - `ai-test-framework` (17);
  - `ai-review-framework/checklists` (6);
  - `e2e/features` (17), `e2e/helpers` (7).
- **Result: 0 hits.** No value was printed.

### T-RENAME-010 (done by Review Bot, 13:10, on Neil's go-ahead)

- **`checklists/api-checklist.md:78`:** `` Layout kept: `Controllers/V1/{Area}`, `Controllers/V1/Schemas`, … `` → `` Layout kept: `Controllers/{Area}`, `Controllers/Schemas`, … ``
- **`checklists/ui-nextjs-checklist.md:9`:** `` (`NEXT_PUBLIC_UNITY_API_ROOT`) `` → `` (`NEXT_PUBLIC_SYSTEM_API_ROOT`) ``
- **`checklists/ui-nextjs-checklist.md:10`:** `` `unityApiFetch` (`src/framework/api/unity-api-fetch.ts`) `` → `` `systemApiFetch` (`src/framework/api/system-api-fetch.ts`) ``

The originals are backed up in `D:\Users\nwood01\Documents\Candc\ai-framework-edit-backup-20261009-1310\ai-review-framework\checklists\`. The edits kept UTF-8 without BOM and LF. The unified diff (2 hunks, 3 lines out, 3 lines in, nothing else) is at `/workspace/t-rename-010.diff` on Review Bot's box.

Left unchanged on purpose:
- `api-checklist.md:7-8`: the Unity.API `Controllers/V2` / `[ApiVersion("2")]` section (real repo; the ticket keeps it);
- `examples/sample-review-add-edit-contact.md:41` (historical example).


## Test review (round 2): Test Bot run 2 (13:56)

Report `tests/TEST-system-rename-2-report.md` (13:53:39) and `handoff.md` `testing` (Test Bot, 13:56). Status passed, round 2, test_fix_cycle 0. **Test verdict: approve.**

| Claim | Checked by Review Bot | Result |
|-------|-----------------------|--------|
| 36 Pass · 0 Fail · 0 Waiting · 14 Not automated (50) | `testing.summary` vs. report rows; YAML parses | Matches |
| Unit 68/68 | Gate on a copy 13:57: API unit 68/68 (57 + 5 TokenIssuerTests + 6 SystemUiCorsTests) | Confirmed |
| e2e 80/80 on Test Bot's Test UI :3013, Test API 7188, `api_framework_test` | Report, run scripts in `%TEMP%\tb-run` (read only); 3013 not listening now (stopped after the run) | Consistent |
| Secret scan 0; `e2e/.auth` no longer opened | My own counts-only re-scan (below) | Confirmed |
| 011/S1 passes, including the read-only probe of Neil's dev UI on :3003 (compiled API root `https://localhost:7088/`) | Step code + `probe-ui-apiroot.cjs` read | Confirmed (see **011/S1**) |
| F-03 done (5 tests) | `Api.Framework.Tests/Auth/TokenIssuerTests.cs` read | Confirmed: real tests |
| F-08 done | `system-rename.steps.ts` read | Confirmed |
| F-07 deferred | Neil's UI still on :3003 | Accepted (still open, Nit) |
| 005/S5: 3 README `/v1` sentences | `README.md:21`, `e2e/README.md:33`, `e2e/README.md:60` | All explain the guard or say there is no /v1; allowed by Plan Bot's clarified Then (History row 10). Pass, not just "on intent" (F-11) |
| 13:30 attempt failed on CORS; Dev Bot fixed it at 13:45 | Report lines 27, 109-111; History row 12; smoke below | Consistent; the 13:30 attempt is correctly not the result of record |

### T-RENAME-011/S1

- **Ticket:** Given "T-RENAME-003 has landed and Neil has done N1"; When "I sign in at the Test UI"; Then "the browser's API calls go to API.Framework without /v1 and none go to the Unity.API v2 fallback".
- **Test:** the `@T-RENAME-011/S1` tag is on the scenario "Session uses the new key and the Test UI calls the versionless Test API root" (shared with 004/S2 and 005/S4). It records the browser's API calls (`addInitScript` recorder) and asserts that the list is non-empty, that it includes `GET /Animal` on the Test API root, and that no call contains `/v1/` or port 7104. That is the Then. The sign-in itself happens in the setup project and the scenario restores that session, which is how the whole suite signs in; acceptable.
- **N1 Given:** evidenced by `probe-ui-apiroot.cjs`. It is HTTP-only: it opens `/auth/sign-in` on :3003, waits for "System Login", fetches same-origin JS chunks and matches the inlined `NEXT_PUBLIC_SYSTEM_API_ROOT`; it counts mutating requests (none). It reads no file and never opens `.env*`. No sign-in, no writes on Neil's UI.

### Test code (delta since run 1)

- `system-rename.steps.ts` (13:26:48): F-08 now waits for the `load` state and polls for `<html data-theme>` (no fixed timeout). 7 scenarios, 7 reset-first steps (`Given the test data is "animals.api.empty"`).
- Mock scan: no `page.route`, `route.fulfill`, HAR, MSW or stubbed fetch; only the two `addInitScript` recorders.
- `TokenIssuerTests.cs` (Test Bot, 13:27; trait `T-RENAME-002/S2`): random 48-byte signing key per run (no key literal). Defaults are `system-login`; a `system-login` token validates and `ReadUserId` works; a full `unity-login` token throws a `SecurityTokenException` and `ReadUserId` is null; issuer-only throws `SecurityTokenInvalidIssuerException`; audience-only throws `SecurityTokenInvalidAudienceException`. Real assertions against the production `TokenService`.
- Test Bot scratch (read, not changed): `start-ui-3013.ps1` runs `npm run dev:test -- --port 3013` with `BASE_URL` / `PORT` set for its own process only; `run-e2e-3013.ps1` refuses 3003, needs a listener on 3013 and runs the safety gate first; `load-env.ps1` reads user-level env vars from the registry only. `dev:test` builds into `.next-test`, so it does not share `.next` with Neil's `npm run dev`. `next-env.d.ts` was rewritten at 13:28 with identical content.

### Not automated (14)

Unchanged from run 1 and still justified, except that 005/S2 and 005/S3 can now be automated: Dev Bot's `e2e/helpers/config.test.ts` (vitest, part of the root `npm test`, 26/26 in the gate) covers unset, blank and stale-`/v1` `API_URL`. Test Bot should record them as Unit / Pass next time (F-10). This doesn't change the verdict.

### Secret re-scan (Review Bot, counts only)

208 files (including trace zips expanded to a temporary folder) under `e2e\` (excluding `.auth` and `node_modules`), `%TEMP%\tb-run`, `Api.Framework.Tests\TestResults` and `work\system-rename`. Needles: 8 user-level env values (`E2E_*` and `APIFW_TEST_Jwt__Secret`) as raw, URL, JSON, HTML and base64 variants. **0 hits.** The scanner self-tested on a planted file first, and was deleted afterwards. See **Notes (round 2)** about one stray self-test file.

## Code delta (after 13:16)

Everything with a newer modification time than my round-1 review, plus `implementation.recorded_at` 13:47 (History row 12). It is moderate and mostly follow-ups, so it's recorded here rather than in a -2 report.

| File | Change | Review |
|------|--------|--------|
| `Api.Framework/Cors/SystemUiCors.cs` (new) | Policy `SystemUi`. Origins come from `Cors:AllowedOrigins`, trimmed, with any trailing `/` dropped, de-duplicated. Throws `InvalidOperationException` naming the setting when empty. `WithOrigins(...).AllowAnyHeader().AllowAnyMethod()` | OK. No `AllowAnyOrigin`, no `SetIsOriginAllowed`, no `AllowCredentials` |
| `Program.cs` | `AddSystemUiCors(builder.Configuration)` and `app.UseCors(SystemUiCors.PolicyName)` in place of the inline policy | OK |
| `appsettings.json` | `Cors:AllowedOrigins`: http/https localhost:4200 and localhost:3003 (the same 4 origins as the old hard-coded policy) | OK |
| `appsettings.Test.json` | The same 4 plus http/https localhost:3013. The full list is needed because .NET arrays merge by index | OK; 3013 is Test only |
| `appsettings.Development.json` | No `Cors` section, so it inherits the base 4 | OK |
| (no `appsettings.Production.json`) | Production inherits the base localhost list | Same as before; see F-13 |
| `Api.Framework.Tests/Cors/SystemUiCorsTests.cs` (6) | Configured origins; `AllowAnyOrigin` false; preflight allowed vs. not; trim + dedupe; empty throws naming the setting; `appsettings.json` = 4 defaults; `appsettings.Test.json` = defaults + 3013 | Real, and they cover the config files |
| `.cursor/rules/api-framework-ui-contract.mdc` + `.claude/…md` | New "## CORS" section (identical bodies): defaults, Test adds 3013, index merge, "Do not widen CORS or add credentials unless Neil asks" | OK. Line 8 still mentions the Angular example UI (F-01 still open) |
| `e2e/helpers/config.ts` + `config.test.ts` | Blank `API_URL` throws "API_URL is set but blank…"; `/v1` still throws; unset or empty gives the default. Tests never print the value; a `v1.` subdomain is allowed | F-04 resolved |
| `scripts/api-root.mjs` + `api-root.test.mjs`; `scripts/dev-test.mjs` | `resolveTestApiRoot()` applies the same rules to `E2E_UI_API_ROOT`; `dev-test` exits 1 with the message | F-05 resolved |
| `vitest.config.mts` | `include` adds `e2e/helpers/**/*.test.ts` and `scripts/**/*.test.mjs` | OK (UI unit 10 → 26) |
| `e2e/README.md:33`, `:60-61` | Guard notes; port / CORS note | OK. `:61` leaves out 4200 (F-12) |
| `handoff.md` (Dev Bot, row 12) | F-06: zip path corrected in `code.verification` and the Summary; row 7 left as written | F-06 resolved. Process: F-14 |
| `plan.md` §9 lines 202-210 (Plan Bot, 13:56, row 13) | DB rollback order: with the new code, `dotnet ef database update 20261008150221_AddAnimals …` (the migration before `20261009114033_RenameUnityToSystem`, checked), then restore the zip; why (TenantService.cs:335, checked); don't start the new API in between; only Neil runs it; Test DB open point | F-02 resolved |
| `.env.local`, `.env.example` (13:24) | Neil's N1 / N2 | Not opened (rule) |

### CORS review

- **No wildcard, no credentials.** Only `WithOrigins` with an explicit list. Credentials are never combined with a broad origin.
- **Defaults.** Development and Test are localhost-only. 3013 is only in `appsettings.Test.json`. No origin list is committed for Production. Production falls back to the base localhost list (no change from before), and an empty list fails fast at startup.
- **Preflight.** Still correct (smoke below). `UseCors` runs before auth, so anonymous `OPTIONS` gets 204.

**Anonymous smoke, Test API https://localhost:7188 (pid 32536, started 13:43 by Dev Bot), no token, no sign-in:**

| Request | Origin | Result |
|---------|--------|--------|
| `OPTIONS /Authorisation/SignIn` (POST; content-type, authorization) | http/https localhost:3003, http/https localhost:3013, http localhost:4200 | 204; `Access-Control-Allow-Origin` = the origin; Allow-Methods POST; Allow-Headers content-type,authorization; `Vary: Origin` |
| same | `https://evil.example`, `http://localhost:3014`, `null` | 204 with **no** CORS headers (the browser blocks it) |
| `OPTIONS /Animal` | http://localhost:3013 | allowed |
| `GET /schemas/sign-in` | evil / 3013 | 200 with no ACAO / ACAO 3013 |
| any | any | No `Access-Control-Allow-Credentials` anywhere |
| Swagger | n/a | 46 paths, 0 `/v1`; `/v1/Animal` 404; `/Animal` without a token 401 |

Development API (7088 / 5088): no response. As of 14:01 nothing was listening on either port. It had been listening at about 13:59 (Visual Studio debug session; `VsDebugConsole` started 10:35 is still open, and its API child process is gone). Review Bot did not stop it. Development CORS was therefore not smoked; its configuration is the base list (code review only).

### Gate, self-test, unit

| Run | Result |
|-----|--------|
| Gate on a temporary copy, `--target all --record` (copy only), 13:57:05 | **pass**. API: eol 221, secrets 221, docs-dup 22 docs (54 allowlisted), unit 68/68. nextjs: lint 152 files, 0 errors / 2 warnings; typecheck 0; eol 234; secrets 234; docs-dup 17; unit 26 passed (6 files) |
| Self-test on the copy | 64 ok / 0 fail (after re-copying the scripts folder with its fake fixtures; my first copy excluded them) |
| Gate in place, check-only, 13:58:38 | All checks pass except **API unit**: `dotnet test` exit 1, MSB3026 "could not copy Api.Framework.Services.dll / Api.Framework.Data.dll" because the running Test API locks `bin\Release` (environment, not code; F-15). `handoff.md` hash unchanged by the run; it wrote `tsconfig.tsbuildinfo` (typecheck cache). Test API not stopped |

## Findings (round 2)

Prior findings:

| ID | Severity | Status (round 2) | Evidence |
|----|----------|------------------|----------|
| F-01 | Minor | **Open** (Neil) | Angular `environment.ts:7` unchanged; UI-contract line 8 unchanged |
| F-02 | Minor | **Resolved** | `plan.md` §9 lines 202-210 (Plan Bot, row 13) |
| F-03 | Minor | **Resolved** | `TokenIssuerTests.cs`, 5 real tests |
| F-04 | Nit | **Resolved** | `config.ts` blank guard + `config.test.ts` |
| F-05 | Nit | **Resolved** | `scripts/api-root.mjs` + test; `dev-test.mjs` |
| F-06 | Nit | **Resolved** | `code.verification` and the Summary corrected (row 7 left as written, per rule) |
| F-07 | Nit | **Open / deferred** (Test Bot) | `npm run build` waits until :3003 is free |
| F-08 | Nit | **Resolved** | load state + `data-theme` poll |
| F-09 | Nit | Note (unchanged) | n/a |

New:

| ID | File:line | Severity | Category | Comment | Suggested fix | Fix by |
|----|-----------|----------|----------|---------|---------------|--------|
| F-10 | `tests/TEST-system-rename-2-report.md:78-80` | Nit | Tests (report) | 005/S2 and S3 are still "Not automated, no helper unit runner", and 005/S1 says "no direct helper unit test". `e2e/helpers/config.test.ts` now runs in the root `npm test` (vitest) and covers unset, blank and stale-/v1 `API_URL` | Next run: record 005/S2-S3 as Unit / Pass (and add the unit test to 005/S1) | Test Bot |
| F-11 | report `:82`, `:134` | Nit | Tests (report) | 005/S5 is "Pass (on intent)" and still asks Review Bot / Plan Bot to change the wording or the Then. Plan Bot already clarified the Then (History row 10): explanatory /v1 prose and the stale-value guard are allowed. All 3 sentences qualify | Record a plain Pass and drop the open question | Test Bot |
| F-12 | `e2e/README.md:61` | Nit | Docs | "`appsettings.Test.json`: 3003 and 3013" leaves out 4200, which Test also lists (it repeats the defaults because arrays merge by index) | "4200, 3003 and 3013, http and https" | Dev Bot |
| F-13 | `Api.Framework/appsettings.json` (`Cors:AllowedOrigins`) | Nit | Security / config | The localhost defaults live in the base file, so Production (no `appsettings.Production.json`) inherits them. A deployment that overrides with fewer entries (for example only `Cors__AllowedOrigins__0`) keeps the base entries at the higher indices. Low risk (localhost only, no credentials, unchanged from before) | Optional: move the defaults into `appsettings.Development.json` (Test already lists its own), so other environments hit the existing fail-fast unless configured, or document that a deployment must set the whole array | Dev Bot (Neil decides) |
| F-14 | `handoff.md` rows 12-13, `code.verification`, `implementation.recorded_at`, `waiting_on` | Nit | Process | While the owner was `human`, Dev Bot (13:47) and Plan Bot (13:56, on Neil's 13:53 instruction) wrote `handoff.md`. Dev Bot also stopped and restarted the Test API (pid 15796 → 32536). Rule: only the owner edits (testing excepted). The changes themselves are correct and were needed to unblock 011/S1 | Neil: ratify rows 12-13, or say which agents may write post-approval follow-ups | Neil |
| F-15 | `ai-code-framework/scripts/pre-handoff-checks.mjs` (unit check, api-framework) | Nit | Tooling | The in-place unit check fails with MSB3026 whenever a Test API runs from `bin\Release` (Test Bot worked around it with `-o bin\tb-unit`) | Build the tests into a separate output folder in the unit check, or report a locked-output error as "environment" | Dev Bot (gate owner) |

Open after round 2: Blocker 0 · Major 0 · Minor 1 (F-01) · Nit 7 (F-07, F-10..F-15) + note F-09. Resolved this round: F-02..F-06, F-08.

### Notes (round 2)

- **Stray self-test file (Review Bot error, cleaned up).** I called my counts-only scanner once with a wrong argument binding. It wrote its 37-byte self-test file, which holds one test env value (the test-data admin persona password), to `UI.NextJs.Framework\test-results` at 14:01:41. My next scan flagged it and I deleted it at about 14:02. It's not a git repo. No other file changed except `tsconfig.tsbuildinfo` (from the gate typecheck). The file existed only briefly and inside Neil's profile; Neil may still want to rotate `E2E_TESTDATA_ADMIN_PASSWORD`.
- **Other activity, not by Review Bot:** files under `work/manage-animals` and `work/shared-paging` were all rewritten at 14:00:18 by someone else. Not reviewed here.
- No sign-in, no token minting, no reset POST and no `.env*` / `e2e/.auth` opened by Review Bot. No processes stopped. No framework docs edited.

## Changes since last review

Round 2 (14:05, same iteration 1; test-fix and follow-up rounds don't count): Dev Bot's CORS change and F-03..F-06 follow-ups (13:43-13:47), Test Bot's F-03 tests, F-08 and run 2 (13:27-13:56), Plan Bot's F-02 rollback order (13:56). See **Code delta (after 13:16)**.

Iteration 1: n/a. Correction from the test review: the 005/S4–S5 row above says the READMEs have no `/v1`. In fact `README.md:21` and `e2e/README.md:33` contain explanatory `/v1` prose, which the clarified S5 Then allows (see **Test review → Rulings**).

## Out of scope / pre-existing notes

These do not affect the verdict.

- **T-RENAME-010 (Review Bot): done 13:10** on Neil's go-ahead (13:09). Three line edits only, with the originals backed up to `D:\Users\nwood01\Documents\Candc\ai-framework-edit-backup-20261009-1310\`; details in **Test review**.
- **Neil (T-RENAME-011):** N1 / N2 (`.env.local` / `.env.example`) are still open. Restart the Development API so `unity_login` gets the migration and the `/v1` routes go. N3 is done per Dev Bot (`API_URL` no longer ends in `/v1`; `E2E_UI_API_ROOT` not set).
- **Test Bot (D5):** run 1 and the 13:15 addendum are reviewed in **Test review**.
- **Unrelated:** `handoff/README.md` and `handoff/templates/handoff.md` gained the "parking" rule (rule 13 and `parked*` fields) after the 11:20 backup. That isn't part of this rename, so I didn't review it here.
- Everything ran on temporary copies except the check-only in-place gate. No processes were stopped and no framework docs were edited.
