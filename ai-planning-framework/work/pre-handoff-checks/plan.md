# Plan: Pre-handoff automated checks (gate)

| Field | Value |
|-------|-------|
| Feature | pre-handoff-checks |
| Type | Framework / tooling (cross-framework) |
| Status | **Approved** for hand-off to Dev Bot (Neil, 2026-10-09 10:32 BST; all Q1–Q17 answered with the suggested defaults, see §6) |
| Requested | 2026-10-09, relayed by Dev Bot from Neil |
| Planned by | plan-bot, 2026-10-09 |
| UI spec / Excel / journeys | **None.** No UI pages, controls or DB columns; this is build tooling and framework docs. `specs/`, `excel/`, `journeys/` and `stubs/` are intentionally not created |

## 1. Summary

Add an automated **pre-handoff gate** to the implementing agent's loop (`ai-code-framework/loops/feature-build.md`, stage 5, before stage 6 optimise / stage 7 self-review) that runs mechanical checks — lint + type-check, line endings / encoding, a secrets scan of committed config, and (if cheap) a duplicate-paragraph check on README / docs — and records the results in `handoff.md` `code.verification`. A failed gate blocks moving to `in-review`. Review Bot then treats these points as gate-enforced instead of re-raising them each round.

## 2. Problem and evidence

Mechanical findings keep recurring in manage-animals code reviews (6 rounds: `reviews/DIRECT-manage-animals-{1,2,3,d29-1,d30-1,d30-2}-review.md`), as relayed by Dev Bot from Neil:

| Finding | Rounds with it | Note |
|---------|----------------|------|
| Secrets in committed config | 6 / 6 | e.g. d30-1 Blocker F-31 (Test DB password committed) |
| Line endings / final newline | 3 / 6 | mixed CRLF / LF in the same target |
| Duplicated README / doc text | 5 / 6 | repeated paragraphs across README, AGENT docs and rules |

A keyword count of the six reports is consistent with this (secret/password mentions in every report; line-ending terms in 4; "duplicat" in 5). Exact per-round counts are Dev Bot's figures, not re-derived.

### Current state (read-only investigation, 2026-10-09)

**Loop and docs**

- `feature-build.md` stage 5 *tests*: API `dotnet build Api.Framework.sln --configuration Release`; UI `npx tsc --noEmit`, "run `npm run lint` and `npm run build` when configured; record that the UI has no test runner when `package.json` has none". Gate: build / tsc pass (3 attempts, then blocker). Writes `code.build`, `code.tests`, `code.verification` (the commands). Stage 6 says "Re-run stage 5 after changes"; gate "no new warnings you introduced".
- `AGENT-BRIEF.md` Definition of done (line 52): "Builds (API: `dotnet build` …; UI: `npx tsc --noEmit`, and `npm run lint` / `npm run build` when configured)". No lint / secrets / line-ending item.
- Handoff template `code:` block **already has** `build`, `tests` and `verification: []` ("commands run"). No structured gate result.
- `ai-framework.config.yaml`: nothing about lint, verification or a gate. It does have `review.scope_exclude` (bin / obj / node_modules / `.next` / `.env*` / `secrets.json` / keys) which the scanner can reuse.

**UI.NextJs.Framework**

- Next.js **15.5.27** installed (`package.json` `^15.1.3`), TypeScript 5.9.3, ESLint 9.39.5, `eslint-config-next` 15.5.27, `@eslint/eslintrc` 3.3.7 (transitive), `@next/eslint-plugin-next` 15.5.27, `eslint-plugin-react-hooks` 5.2.0. **No** `typescript-eslint`, markdownlint or Prettier.
- Scripts: `dev`, `dev:turbo`, `dev:test`, `build`, `start`, **`lint: next lint`**, **`test: vitest run`**.
- **No ESLint config file** (`eslint.config.*` / `.eslintrc*` absent), so `next lint` prompts for setup. `next lint` is deprecated from Next 15.5 in favour of the ESLint CLI.
- **Vitest exists** (Dev Bot is right): vitest 5.0.3, `vitest.config.mts` (jsdom, `src/**/*.test.{ts,tsx}`), 4 test files (`RoutedModal`, `PendingRoutedModalHost`, `JsonSchemaForm`, `use-json-schema-entity-form`). Playwright lives in the separate `e2e/` package (Test Bot).
- `tsconfig.json` strict, `noEmit`, includes `.next*/types`.

**Line endings (text files, excluding build output / node_modules / secrets)**

| Target | Type | CRLF | LF | Mixed | BOM |
|--------|------|------|----|-------|-----|
| API.Framework | `.cs` | 148 | 6 | 0 | 15 |
| | `.csproj` / `.sln` / `.json` | 21 | 0 | 0 | 2 |
| | `.md` / `.mdc` | 19 | 18 | 3 | 2 |
| UI.NextJs.Framework | `.ts` / `.tsx` | 138 | 30 | 0 | 0 |
| | `.css` / `.mts` / `.cjs` | 24 | 0 | 0 | 0 |
| | `.md` / `.mdc` / `.feature` / `.mjs` | 2 | 23 | 0 | 1 |
| | `.json` | 5 | 1 | 1 | 0 |

- Neither target has `.editorconfig` or `.gitattributes`. Precedents: Unity.API `.gitattributes` = `* text=auto`; UI.Angular.Framework `.editorconfig` = `charset = utf-8`, `insert_final_newline = true`.
- Neil's git: global `core.autocrlf = true`.

**Git**

- **Neither API.Framework nor UI.NextJs.Framework is a git repository** (no `.git`; `git rev-parse` fails; `ai-code-framework` itself is not a repo). Unity.API and UI.Angular.Framework are. So "committed config" today means "files on disk in the target", and `.gitattributes` has no effect until a repo exists.

**Tools on Neil's machine**: Node 22.16.0, npm 11.5.2, .NET SDK 10.0.301, git, Windows PowerShell 5. **No Python** (only the Windows Store stub), no `pwsh`, no gitleaks.

**Secrets currently present** (file + key names only; no values recorded here)

| File | Key / location | Finding |
|------|----------------|---------|
| `api/API.Framework/Api.Framework/appsettings.json` | `ConnectionStrings.LoginConnection` | Connection string with a non-empty `Password=` |
| same | `Jwt.Secret` | Non-empty |
| `api/API.Framework/Api.Framework.Data/LoginDbContextFactory.cs` (line 29) | design-time fallback after `GetConnectionString(...) ??` | Hard-coded connection string literal with a non-empty `Password=` |
| `api/API.Framework/Api.Framework/appsettings.Test.json` | `ConnectionStrings.LoginConnection`, `Jwt.Secret` | **Empty** (clean; fixed after d30-1 F-31) |
| `appsettings.Development.json`, `appsettings.Production.json`, `Properties/launchSettings.json` | — | No secret-like non-empty values |
| `api/API.Framework/Api.Framework.Tests/Animals/AnimalPoliciesTests.cs` (line 157) | test signing key literal | Dummy, explicitly named "not a secret" → allowlist candidate |
| `Jwt.Issuer`, `Jwt.Audience` (appsettings.json, appsettings.Test.json) | — | Non-empty but **not secrets** (naive "jwt" patterns would flag them) |
| `AuthController.cs:56`, `PersonasUnit.cs:45`, `e2e/setup/auth.setup.ts:63`, `e2e/setup/sign-in-child.cjs:41`, `e2e/support/personas.ts:36`, `TokenService.cs:94`, `e2e/README.md:35` | `Password =` / "secret" text | **Not secrets** — values come from request models / `Environment.GetEnvironmentVariable` / `process.env`, or are prose. Show the false-positive patterns the scanner must not fail on |

The two real ones (`appsettings.json` and the `LoginDbContextFactory` fallback) are Neil's separate pending decision, so a strict gate would fail on its first run. Decided: fix first (D1, T-GATE-008); Neil rotates the exposed dev DB password and Jwt secret.

**Review Bot framework (stale lines, quoted)**

- `ai-review-framework/skills/review-tests/SKILL.md:22` — "| UI.NextJs.Framework | No test runner configured - `package.json` scripts are `dev`, `build`, `start`, `lint`. Report the gap; do not fail the PR for it alone. `npm run lint` and `npm run build` are the available checks. |"
- `ai-review-framework/skills/review-tests/SKILL.md:43` — severity rule ending "… A UI codebase with no test run…" (line read truncated; Review Bot to confirm the full wording) — built on the same assumption
- `ai-review-framework/checklists/ui-nextjs-checklist.md:47` — "- [ ] `npm run lint` and `npm run build` pass where they can run (no test runner is configured in `package.json`)"
- `ai-review-framework/examples/sample-review-add-edit-contact.md:84, 106, 122` — "no UI test runner" (illustrative sample; Review Bot decides whether to touch it)
- Related rules that would become gate-backed: `skills/review-code-standards/SKILL.md:40` ("Do not repeat what a formatter or linter enforces … **Nit** at most"), `checklists/severity.md:18` (linter points capped at Nit), `skills/review-security-and-data/SKILL.md:26` and `:42` (secrets scan), `checklists/security-checklist.md:33` (Secrets and configuration).

## 3. Actors and ownership

| Actor | Role here |
|-------|-----------|
| Neil (human owner) | Answered D1–D17 and approved `plan_to_code` (2026-10-09 10:32 BST); decides on the existing dev secrets (rotation / local config), merges |
| Dev Bot (implementing agent) | Owns `ai-code-framework` (feature-build loop, AGENT-BRIEF, both targets, the scripts). Builds T-GATE-001..005 and T-GATE-008 |
| Plan Bot | Owns the shared handoff template / README and the `verification` entry in `ai-framework.config.yaml` (T-GATE-006), as with earlier `testing:` config changes |
| Review Bot | Owns `ai-review-framework`; updates its own skills / checklists (T-GATE-007, cross-framework ticket). Plan Bot does not edit those files |
| Test Bot | Not affected, except that the gate must not touch `e2e/` scenario code it owns (D11) |

## 4. Scope

**In scope (v1)**

- Targets: `api-framework` (`ai-code-framework/api/API.Framework`) and `nextjs` (`ai-code-framework/ui/UI.NextJs.Framework`) — the active `development.api` / `development.ui` entries.
- Checks: (a) ESLint config + `lint` / `typecheck` scripts for Next.js, run with `tsc --noEmit`; (b) `.editorconfig` + `.gitattributes` in both targets, a line-ending / final-newline / BOM check, and a one-off normalisation; (c) a secrets scan of `appsettings*.json`, `launchSettings.json`, `*.cs` connection-string fallbacks and docs; (d) a duplicate-paragraph check on README / docs (D8).
- One runner command that runs every check for the targets touched and prints a pass / fail summary.
- Framework docs: feature-build stage 5 gate, AGENT-BRIEF checklist item, handoff template / README (`code.verification` + gate result), config `verification:` block.
- Review Bot: treat gate-enforced points as such; fix the stale "no test runner" lines.

**Out of scope (v1)**

- Unity.API and UI.Angular.Framework (they have their own loops; config can add them later).
- Creating git repositories for API.Framework / UI.NextJs.Framework.
- Prettier / auto-formatting the code base; changing C# analyzers / `TreatWarningsAsErrors`.
- CI pipelines or git hooks (no repos yet).
- Rotating credentials (Neil).
- Scenario tests / e2e (Test Bot).

## 5. Design (proposed; open points are questions in §7)

### 5.1 Runner

- `ai-code-framework/scripts/pre-handoff-checks.mjs` (Node 22, no new dependencies; D4) with `--target api-framework|nextjs|all` and `--json`.
- Runs, per target touched by the feature (from the `implementation` manifest; secrets scan always runs on both):
  - **nextjs**: `npm run lint` (ESLint CLI), `npm run typecheck` (`tsc --noEmit`); `npm test` (vitest, existing unit tests; D6)
  - **api-framework**: `dotnet build Api.Framework.sln --configuration Release` stays in stage 5 as today; `dotnet test` on `Api.Framework.Tests` (existing unit tests; D6)
  - **both**: line-ending / final newline / BOM check against `.editorconfig`; secrets scan; duplicate-paragraph check (D8)
- Exit code 0 = pass, 1 = fail; prints one line per check: `<check> <target> -> pass|fail (<counts>)`. Never prints a secret value — only `file:line`, key path and the rule id.
- Excludes `review.scope_exclude` paths (build output, node_modules, `.next*`, `.env*`, `secrets.json`, keys) and never opens `.env*` / `secrets.json`.

### 5.2 Checks

| Id | Check | Fails when | Notes |
|----|-------|------------|-------|
| `lint` | ESLint flat config `eslint.config.mjs` (D2) | any ESLint **error** (warnings per D3) | Replace `next lint` with `eslint .` (deprecated in 15.5) |
| `typecheck` | `tsc --noEmit` | any error | Already in stage 5; moves into the runner |
| `eol` | Line endings, final newline, charset/BOM per `.editorconfig` | any file not matching its target's rule | Direct file check, works without git (D5, D12) |
| `secrets` | Pattern scan + JSON key walk + allowlist | any non-empty secret value not on the allowlist | Rules below |
| `docs-dup` | Repeated paragraphs (≥ N words) across README / docs in a target | an exact duplicate paragraph outside an allowlist | D8; full markdownlint later |
| `unit` | `npm test`, `dotnet test` (existing tests) | any failure | Existing unit tests only (D6) |

**Secrets rules (draft)**

- JSON (`appsettings*.json`, `launchSettings.json`, other committed `*.json` config): walk keys; fail on a non-empty string under a key matching `password|pwd|secret|token|apikey|api_key|signingkey|privatekey|clientsecret|connectionstring` **with a credential part**, or any value containing `Password=` / `Pwd=` with a non-empty value. `Jwt.Issuer` / `Jwt.Audience` are not secrets.
- Code (`*.cs`, `*.ts`, `*.tsx`, `*.js`, `*.mjs`, `*.cjs`): a string **literal** containing `Password=…` / `Pwd=…` (non-empty), private key blocks, or a literal assigned to a key/secret/password name. Values read from `Environment.GetEnvironmentVariable`, `process.env`, configuration or request models pass.
- Docs (`*.md`, `*.mdc`): `Password=` / `Pwd=` with a non-empty value, private key blocks. Prose that mentions "secret" passes.
- **Allowlist**: `ai-code-framework/scripts/pre-handoff-allowlist.json` — entries `{ "path", "rule", "key" or "line_hint", "reason", "owner", "expires" }`, no values; reviewed by Review Bot; an expired entry fails (D1, D13).

### 5.3 Line endings

- `.editorconfig` in each target root (`root = true`), `charset`, `insert_final_newline = true`, `trim_trailing_whitespace = true` (not for `*.md`), `end_of_line` per D5.
- `.gitattributes` in each target (`* text=auto` + explicit `eol=` per type to match `.editorconfig`, binaries marked `binary`). Effective once the target is a git repo.
- One-off normalisation of existing files to the chosen endings (no other change), run when no feature is in development (D12).

### 5.4 Pipeline integration

- **feature-build.md stage 5** becomes *tests + pre-handoff checks*: run the runner after build; failures that survive 3 attempts are blockers (same rule as build). Stage 6 already re-runs stage 5, so the **last** run before stage 8 is the one recorded.
- **Stage 8 gate**: do not hand off unless the latest gate result is `pass` (or every failure is allowlisted).
- **handoff.md**: keep `code.verification` as the list of commands with results (e.g. `"pre-handoff: lint nextjs -> pass (0 errors, 4 warnings)"`), and add `code.pre_handoff_gate: null | pass | fail` + `code.pre_handoff_gate_at` (D9).
- **AGENT-BRIEF.md** Definition of done: new item "Pre-handoff checks pass (`node ../scripts/pre-handoff-checks.mjs`); results in `code.verification`, `code.pre_handoff_gate: pass`".
- **handoff/README.md**: stage rule "a failed or missing gate blocks `in-development → in-review`".
- **ai-framework.config.yaml**: new `verification:` block (draft below).
- **Review Bot**: on pickup, if `code.pre_handoff_gate` is not `pass`, return the hand-off without a review round (D10); points the gate enforces are not re-raised unless the gate missed them (then raise once and note the gate gap).

Config block (accepted defaults; applied by T-GATE-006; nothing secret):

```yaml
verification:
  # Pre-handoff gate (feature-build stage 5). Draft: pre-handoff-checks plan, 2026-10-09.
  runner: node ai-code-framework/scripts/pre-handoff-checks.mjs
  allowlist: ai-code-framework/scripts/pre-handoff-allowlist.json
  fail_on_warnings: false            # D3
  blocks_handoff: true               # failed gate blocks in-development -> in-review
  targets:
    api-framework:
      path: ai-code-framework/api/API.Framework
      checks: [eol, secrets, docs-dup, unit]    # unit = dotnet test Api.Framework.Tests (D6)
    nextjs:
      path: ai-code-framework/ui/UI.NextJs.Framework
      checks: [lint, typecheck, eol, secrets, docs-dup, unit]   # unit = npm test (vitest) (D6)
  not_in_git: scan-working-tree      # D14
```

## 6. Decisions

All from Neil, 2026-10-09 10:32 BST: every suggested default in §7 accepted, and the plan approved for hand-off to Dev Bot.

1. D1 (Q1) Existing dev secrets are **fixed first** (T-GATE-008, before the gate blocks): committed values emptied, dev values in .NET user-secrets / env vars, factory fails clearly when unset. **Action for Neil (not an agent):** rotate the exposed dev DB password and Jwt secret.
2. D2 (Q2) ESLint: flat `eslint.config.mjs` with `FlatCompat` → `next/core-web-vitals` + `next/typescript`, ignoring `.next*`, `node_modules`, `e2e/`; `"lint": "eslint ."`, `"typecheck": "tsc --noEmit"`.
3. D3 (Q3) Warnings do not fail v1: errors fail, warnings are counted and recorded; stage 6 "no new warnings you introduced" still applies.
4. D4 (Q4) Runner and scanner are a dependency-free Node `.mjs` script (no PowerShell 5 script, no gitleaks).
5. D5 (Q5) Line endings: API.Framework CRLF; UI.NextJs.Framework LF; `*.ps1` / `*.cmd` / `*.bat` CRLF in both.
6. D6 (Q6) The gate runs the existing unit tests (`dotnet test` on Api.Framework.Tests, `npm test` / vitest); e2e / harness and scenario tests stay with Test Bot.
7. D7 (Q7) UTF-8 without BOM in both targets; BOMs removed in the normalisation pass; `.sln` allowlisted if Visual Studio re-adds its BOM.
8. D8 (Q8) Docs check now, cheap part only: exact duplicate paragraphs (≥ 25 words) within a target; full markdownlint later.
9. D9 (Q9) Results recorded as lines in `code.verification` plus `code.pre_handoff_gate: pass | fail` and `code.pre_handoff_gate_at`.
10. D10 (Q10) A hand-off with the gate missing or failed is returned by Review Bot without a review round (no `review.cycle` increment), with a History row.
11. D11 (Q11) Test Bot's `e2e/` package: secrets scan yes; lint / typecheck no.
12. D12 (Q12) Existing files are normalised once (endings / BOM only) in T-GATE-002, while no feature is in development.
13. D13 (Q13) Allowlist entries: Dev Bot proposes with reason and expiry; real credentials need Neil's OK; Review Bot checks new entries every round.
14. D14 (Q14) Where a target is not in git, the gate scans the working tree minus `review.scope_exclude` and records "not a git repo: working tree scanned".
15. D15 (Q15) Runner and allowlist live in `ai-code-framework/scripts/` (shared by both targets).
16. D16 (Q16) These framework tickets need no Test Bot round; Review Bot verifies by running the gate on the real targets and on fixture files with seeded violations.
17. D17 (Q17) Line-ending and lint checks cover the whole target after normalisation; if T-GATE-001 cannot reach a clean lint baseline, fall back to touched files + a recorded baseline.

Defaults Plan Bot picked inside tickets (Neil may override): T-GATE-008 uses .NET user-secrets for dev, with env var names `ConnectionStrings__LoginConnection` and `Jwt__Secret`; T-GATE-007: Review Bot updates its sample review and report template wording.

**Amendment to D1 / T-GATE-008 (2026-10-09, found during the build; Neil approved):**

- `DefaultUserSeeder`'s hard-coded admin password was not in the §2 secrets table, but the secrets scan flags it (literal assigned to a password name). It moved to the `DefaultUser:Password` setting; seeding is skipped when the setting is unset. Recorded as a deviation for review.
- Test environment only: the Test API settings use **user-level** env vars `APIFW_TEST_ConnectionStrings__LoginConnection` and `APIFW_TEST_Jwt__Secret`, read by `Program.cs` / `LoginDbContextFactory` only when the environment is Test (Neil approved). Development keeps the user-secrets / `ConnectionStrings__LoginConnection` / `Jwt__Secret` default above. `ai-framework.config.yaml` `testing.database.connection_env` and `secrets.test_db_connection_env` now name `APIFW_TEST_ConnectionStrings__LoginConnection`. Names only; no values anywhere.

Recorded facts that shape the plan:

1. Vitest is configured in UI.NextJs.Framework (`npm test` = `vitest run`, 4 test files), so the Review Bot "no test runner" lines are stale (verified 2026-10-09).
2. Neither target is a git repo; the gate must work on the working tree.
3. No Python on Neil's machine; Node 22 and .NET 10 are available.
4. No UI spec / Excel / journeys: no pages or DB columns are involved.

## 7. Open questions — all answered (Neil, 2026-10-09 10:32 BST: suggested defaults accepted; decisions D1–D17 in §6)

| # | Question | Answer (accepted default) |
|---|----------|-------------------|
| Q1 | Existing dev secrets (`appsettings.json` `ConnectionStrings.LoginConnection` + `Jwt.Secret`; `LoginDbContextFactory` fallback connection string): allowlist them so the gate passes now, or fix them first? | **Fix first** (T-GATE-008, before the gate is switched on): move local dev values to `dotnet user-secrets` / env vars, leave the committed values empty, make the factory fall back to an env var and fail clearly when none is set. **Action for Neil (not an agent):** rotate the exposed dev DB password and Jwt secret. |
| Q2 | ESLint ruleset? | Flat `eslint.config.mjs` using `FlatCompat` with `next/core-web-vitals` + `next/typescript` (the create-next-app 15 default; uses packages already installed), ignoring `.next*`, `node_modules`, `e2e/`. Replace `"lint": "next lint"` with `"lint": "eslint ."` and add `"typecheck": "tsc --noEmit"` |
| Q3 | Fail on warnings? (ESLint and build) | **No** for v1: errors fail, warnings are counted and recorded; stage 6's "no new warnings you introduced" still applies. Revisit (`--max-warnings 0`) once the baseline is clean |
| Q4 | Scanner / runner implementation: PowerShell 5 script, Node script, or gitleaks? | **Node script** (`.mjs`, no dependencies): Node 22 is already required by the UI, runs the same for every agent, easier to test than PS5; gitleaks needs a download and approval and is built around git history, which these targets lack |
| Q5 | Line endings per target? | **API.Framework: CRLF** (148/154 `.cs` already CRLF; Visual Studio / .NET default). **UI.NextJs.Framework: LF** for code and docs (Next.js / ESLint ecosystem default; `.feature`, `.mdc`, `.mjs` already LF). `*.ps1` / `*.cmd` / `*.bat` CRLF everywhere (PowerShell 5) |
| Q6 | Should the gate also run the existing unit tests (`dotnet test` on Api.Framework.Tests, `npm test` / vitest)? | **Yes, existing unit tests only** (fast, no environment): a red unit test should never reach review. e2e / harness and new scenario tests stay with Test Bot |
| Q7 | Encoding: UTF-8 without BOM everywhere? (15 `.cs` and a few `.md` / `.sln` files have a BOM today) | **UTF-8 without BOM** in both targets (`charset = utf-8`), BOMs removed in the normalisation pass; `.sln` keeps its BOM if Visual Studio re-adds it (allowlisted) |
| Q8 | Markdown duplicate / lint check: now or later? | **Now, the cheap part only**: exact duplicate paragraphs (≥ 25 words) within a target's README / docs, in the same Node script. Full markdownlint (new devDependency + rules) **later** |
| Q9 | How to record the result: only lines in `code.verification`, or also a structured field? | Both: lines in `code.verification` **plus** `code.pre_handoff_gate: pass|fail` and `code.pre_handoff_gate_at` in the template, so Review Bot can check one field |
| Q10 | What does Review Bot do if a hand-off arrives with the gate missing or failed? | Return it to Dev Bot without starting a review round (no `review.cycle` increment), with a one-line note in History |
| Q11 | Does the gate lint / scan Test Bot's `e2e/` package? | **Secrets scan: yes** (credentials there matter). **Lint / typecheck: no** in v1 (separate package and tsconfig, owned by Test Bot) |
| Q12 | Renormalise existing files now? | **Yes, once**, as its own step in T-GATE-002 when no feature is in development (under Q5: about 170 UI files CRLF → LF — 138 `.ts`/`.tsx`, 24 `.css`/`.mts`/`.cjs`, a few `.json`/`.md`; about 6 `.cs` plus ~21 `.md`/`.mdc` in API.Framework → CRLF; BOM removals per Q7). Churn note: no git diff noise today (no repos), but every touched file changes on disk, so concurrent agents must not be editing; with git later, it would be a single "normalise line endings" commit |
| Q13 | Who may add allowlist entries? | Dev Bot proposes with a reason and expiry; an entry needs Neil's OK for real credentials; Review Bot checks new entries each round |
| Q14 | How does the gate behave where a target is not in git? | Scan the **working tree** (minus `scope_exclude`) instead of committed files; `.gitattributes` is still written for later. Record "not a git repo: working tree scanned" in `code.verification` |
| Q15 | Where do the runner and allowlist live? | `ai-code-framework/scripts/` (shared by both targets; outside each target so it is not part of either future repo) |
| Q16 | Do these framework tickets go through Test Bot (option B), or is Review Bot running the gate on fixtures enough? | **Review Bot only**: acceptance is checked by running the runner on the real targets and on small fixture files (seeded violations); no Test Bot round. Test Bot is told the gate exists |
| Q17 | Should the line-ending and lint checks apply to the whole target or only to files the feature touched? | **Whole target** after the one-off normalisation (cheap and keeps it clean); lint on the whole target too. If the baseline cannot be made clean in T-GATE-001, fall back to touched files + recorded baseline |

## 8. Delivery slices and tickets

| Ticket | Title | Owner | Depends on |
|--------|-------|-------|------------|
| T-GATE-001 | ESLint flat config and lint / typecheck scripts (UI.NextJs.Framework) | dev-bot | D2, D3 |
| T-GATE-002 | `.editorconfig` / `.gitattributes` and one-off line-ending normalisation (both targets) | dev-bot | D5, D7, D12 |
| T-GATE-003 | Secrets scan and allowlist | dev-bot | D1, D4, D13, D14, D15 |
| T-GATE-004 | Duplicate-paragraph docs check | dev-bot | D8 |
| T-GATE-005 | Pre-handoff runner and feature-build stage 5 gate + AGENT-BRIEF item | dev-bot | 001–004, D6, D9, D11, D17 |
| T-GATE-006 | Handoff template / README `code.verification` + gate field, config `verification:` block | plan-bot — **done 2026-10-09** | D9, D10 |
| T-GATE-007 | Review Bot: gate-enforced rules and stale "no test runner" lines (cross-framework) | review-bot | 005, 006, D10 |
| T-GATE-008 | Remove committed dev secrets from API.Framework | dev-bot (+ Neil: rotation and local values) | D1 |

T-GATE-006 was done by Plan Bot at approval time (2026-10-09), ahead of the order below, so the fields and config exist when Dev Bot starts.

Order: 008 → 001, 002, 003, 004 (parallel) → 005 → 006 → 007. The gate is switched on (stage 8 blocks) only when 005 and 006 are done and the first full run passes.

## 9. Risks

- First lint run on existing code may report many errors (no config has ever run) — T-GATE-001 fixes errors or falls back per D17.
- False positives in the secrets scan (seen above) — tests in T-GATE-003 cover them.
- Normalisation while another agent edits a file would lose or garble edits (seen with `handoff.md` on 2026-10-08) — D12 runs it only when idle.
- `.gitattributes` is inert until the targets are git repos.
