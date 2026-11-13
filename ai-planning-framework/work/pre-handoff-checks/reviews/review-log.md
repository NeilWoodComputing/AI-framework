# Review log: pre-handoff-checks

Append-only history of every review round for this feature, whichever route was used: a direct hand-off from the implementing agent or a pull request. The reviewing agent appends one **Round** block per review, at loop stage 10 of `loops/pr-review.md`, with no human request needed.

- Feature: `ai-planning-framework/work/pre-handoff-checks/`
- Pipeline state: `handoff.md`
- Full reports, one per round: `reviews/DIRECT-<branch-slug>-<n>-review.md` or `reviews/DIRECT-<feature>-<n>-review.md` with no branch (direct route) · `reviews/PR-<id>-review.md` (PR route, overwritten on each PR update)

Rules:

- Append only. Newest round at the bottom. Never edit or delete an earlier round; a correction goes in a new round's **Notes**.
- **Direct route:** the **Comments** table is required, with one row per finding, matching the full report.
- **PR route:** the round block plus **Summary** is required. The comments are in the full report (and on the PR only when publishing is on, which needs provider `azure-devops`), so the **Comments** table is optional.
- Dates in Europe/London. No tokens, connection strings or personal data from fixtures.

---

## Round 1 — 09/10/2026 10:56 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: 25 manifest entries + 1 discovered file (`e2e/README.md`), 0 not implemented (scripts in `ai-code-framework/scripts` reviewed as plan scope, approved by Neil) |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-GATE-001, T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005, T-GATE-008 (T-GATE-006 reference only; T-GATE-007 not part of this review) |
| Verdict | **Request changes** |
| Findings | Blocker 0 · Major 1 · Minor 4 · Nit 3 |
| Full report | `reviews/DIRECT-pre-handoff-checks-1-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | implementing agent, Dev Bot (changes-requested) |

### Summary

The pre-handoff gate (lint, typecheck, eol / BOM, secrets, docs-dup, unit) passed on both targets in place and on a temporary copy, with counts identical to Dev Bot's 10:47:27 recording. The self-test is 33/33, and 20 of 22 planted violations failed with a clear message and exit 1. T-GATE-008 and the DefaultUserSeeder deviation are safe, the 9 allowlist entries are narrow and justified, and the normalisation changed endings / BOM / final newline only (448 files compared). Request changes for one Major: a comment in `appsettings*.json` silently disables the secrets key walk.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-01 | `ai-code-framework/scripts/pre-handoff-checks.mjs:235` | Major | A comment in an `appsettings*.json` file (allowed by .NET) makes `JSON.parse` fail, and the fallback line scan only checks `Password=` and private keys. A credential-key value such as `Jwt.Secret` then passes the gate silently (reproduced). T-GATE-003 S2; plan §5.2 | String-aware comment / trailing-comma strip before parsing; fail with `secrets-json-unparsed` if a file still won't parse; add a fixture and a self-test assertion |
| F-02 | `ai-code-framework/scripts/pre-handoff-checks.mjs:210` | Minor | An all-caps value (`^[A-Z][A-Z0-9_]*$`) under a credential key is treated as an env-var name and skipped (reproduced with `Jwt.Secret`). Same shape as uppercase-only keys | Drop the shortcut in the JSON key walk, or require a credential suffix (`_PASSWORD`, `_SECRET`, `_KEY`, `_TOKEN`); add a fixture |
| F-03 | `ai-code-framework/scripts/pre-handoff-checks.mjs:500` | Minor | A non-expired unused allowlist entry passes silently (D13 hygiene) | Report `allowlist entries[n] unused` as a note when every check ran |
| F-04 | `ai-code-framework/api/API.Framework/Api.Framework.Services/Auth/DefaultUserSeeder.cs:30` | Minor | The "unset → create nothing, return false" behaviour has no unit test | Add `DefaultUserSeederTests` (unset, set, user exists) |
| F-08 | `ai-planning-framework/work/pre-handoff-checks/handoff.md:92` | Minor | Manifest incomplete: `ui/UI.NextJs.Framework/e2e/README.md` (changed by the 10:55 addition, History row 6) isn't listed; `recorded_at` still 10:47:04 | Add it under `implementation.ui` and refresh `recorded_at` |
| F-05 | `ai-code-framework/ui/UI.NextJs.Framework/tsconfig.json:61` | Nit | `include` has dev-server-added scratch entries `.next-devbot-warm` / `.next-test-tb` (also line 65) | Remove once those folders are deleted |
| F-06 | `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs:68` | Nit | The verify command deletes and rewrites `scripts/fixtures/pre-handoff/` in place | Generate into a temp dir or say plainly that it rewrites the fixtures |
| F-07 | `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs:107` | Nit | The self-test doesn't cover unit failure, D11, allowlist schema problems, `--feature` or `--record` (all verified by hand) | Add fixtures / assertions, starting with the F-01 / F-02 shapes |

### Changes since last round

First review.

### Notes

- D10: `code.pre_handoff_gate: pass` @ 10:47:27 recorded honestly (reproduced exactly at 10:51:37 in place). Dev Bot's Neil-approved 10:55 addition (`APIFW_TEST_` Test-only env vars, History row 6) was folded in: gate re-recorded at 10:55:12, and my in-place re-run at 10:56:25 passed with identical counts.
- Test Bot / Plan Bot: config renamed by Plan Bot at 10:56, but `ai-test-framework` docs (reset-endpoint-safety-checklist.md:17, add-test-data-reset/SKILL.md:15, :22, README.md:91) still name the unprefixed `ConnectionStrings__LoginConnection`.
- Plan Bot: the seeder deviation is recorded (History row 7); still add the seeded admin password to D1's rotation action. Later: a placeholder check for `.env.example`, and mirror-drift for `.cursor` ↔ `.claude` rules.
- Neil: rotate the dev DB password and Jwt secret, and change the existing system-admin password (old committed literal).
- Gate and self-test planted runs were made on a temporary copy only (`%TEMP%\rb-gate`, deleted afterwards). No processes were stopped and no framework docs were edited. T-GATE-007 is separate.

---

## Round 2 — 09/10/2026 11:12 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: round-1 findings F-01..F-08 plus every file changed since round 1 (diffed against `%TEMP%\gate\c2-backup`) and the new `Api.Framework.Tests/Auth/DefaultUserSeederTests.cs` |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-GATE-001, T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005, T-GATE-008 (T-GATE-007 not part of this review) |
| Verdict | **Approve with comments** |
| Findings | Blocker 0 · Major 0 · Minor 2 · Nit 2 |
| Full report | `reviews/DIRECT-pre-handoff-checks-2-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | human (approved; no Test Bot round, D16) |

### Summary

All eight round-1 findings are fixed and verified. The gate passed in place at 11:07:08, identical to Dev Bot's 11:03:25 record, and on a temporary copy. The self-test is 64/64 in a temp dir with the committed fixtures unchanged. In the planted matrix, 32 of 37 cases behaved as expected: all 24 core cases, the three round-1 misses and the tricky JSONC shapes (`//` in URLs and strings, block comments, unterminated comment). No value leaked in text or `--json` output. The five gaps are narrow secrets-heuristic shapes (F-09, F-11). F-10 is a `dev-test.mjs` tidy-up and F-12 a stale verification line.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-09 | `ai-code-framework/scripts/pre-handoff-checks.mjs:221` | Minor | A connection-string `Password=` value starting with `{ $ < %`, or a quoted value, is skipped (reproduced: `$…`, `%…` with no closing `%`, `'…'`) | Drop the prefix test (rely on the anchored `PLACEHOLDER`); parse quoted values; add fixtures |
| F-10 | `ai-code-framework/ui/UI.NextJs.Framework/scripts/dev-test.mjs:32` | Minor | The whole-file `tsconfig.json` restore on exit reverts legitimate edits made during the session; no restore on a crash or hard kill | Remove only the `<distDir>/types/**/*.ts` entry Next added, or skip when it's already included |
| F-11 | `ai-code-framework/scripts/pre-handoff-checks.mjs:211` | Nit | Whole-value `{…}` passes as a placeholder; in code, any literal containing `{letter` is skipped as "interpolation", even in plain quotes (`:309`) | Treat `{` as interpolation only in template literals / C# `$"…"` |
| F-12 | `ai-planning-framework/work/pre-handoff-checks/handoff.md:70` | Nit | `code.verification` still says the self-test is `33/33` with fixtures in place | Update to 64/64 (temp dir) |

### Changes since last round

F-01 (Major) fixed; F-02, F-03, F-04, F-08 (Minor) fixed; F-05, F-06, F-07 (Nit) fixed. F-05's follow-up is F-10. Details are in the report's **Changes since last review** table.

### Notes

- D10: `code.pre_handoff_gate: pass` @ 11:03:25 recorded honestly (reproduced exactly at 11:07:08 in place, check-only, no `--record`).
- F-04: the logger is passed in production (`Program.cs:132`, `app.Logger`, Development only).
- Neil's round-1 actions (rotation, user-secrets) still stand. The `ai-test-framework` doc note from round 1 was not re-checked.
- Planted runs and the self-test ran on a temporary copy only (`%TEMP%\rb-gate2`, deleted afterwards). No processes were stopped, no framework docs were edited, nothing was merged. T-GATE-007 is separate.
