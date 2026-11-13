---
# handoff.md: pipeline state for ONE feature. Rules: handoff/README.md
# Copy to <output.work_dir>/<feature>/handoff.md. Only the current `owner` edits
# this file, except the `testing` section, which the testing agent (test-bot) may
# write while review-bot owns the feature (handoff/README.md -> Testing alongside review). On every transition, update this front matter AND append a row to
# History. Paths are relative to this feature folder unless they start with ai-.
handoff_version: 1
example: false                # true = illustrative only; never picked up
feature: pre-handoff-checks
feature_path: ai-planning-framework/work/pre-handoff-checks   # output.work_dir/<feature>
stage: merged                      # planned | in-development | in-review | changes-requested | approved | merged
owner: human                      # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config; test-bot is never an owner)
pickup: pending               # pending (handed over, not started) | accepted (owner is working it)
waiting_on: "Nothing for agents: MERGED 2026-10-09 12:37 BST (Neil's word to Dev Bot; no git). Neil's open to-dos remain (not blocking, D1): rotate the exposed dev DB password, the Jwt secret and the seeded system-admin password (DefaultUser:Password); set Development user-secrets. Optional follow-ups for Dev Bot: F-09/F-10 (Minor), F-11/F-12 (Nit). T-GATE-007 (Review Bot) separate"
updated_at: 2026-10-09T12:38:49+01:00
updated_by: plan-bot

routes:                       # the route actually used (from handoff in the config)
  plan_to_code: direct        # devops | direct   (set by the planning agent at hand-off)
  code_to_review: direct      # pr | direct       (set by the implementing agent at hand-off)
  code_to_test: null          # direct            (set by the implementing agent at the same hand-off; the testing agent runs alongside the review). null: no Test Bot round for this feature (D16)
  review_feedback: direct     # direct

tickets:                      # every T-<DOMAIN>-NNN in tickets/; id must match the filename
  - id: T-GATE-001
    file: tickets/T-GATE-001-eslint-config-lint-typecheck.md
    devops_work_item_id: null
  - id: T-GATE-002
    file: tickets/T-GATE-002-editorconfig-gitattributes-line-endings.md
    devops_work_item_id: null
  - id: T-GATE-003
    file: tickets/T-GATE-003-secrets-scan-allowlist.md
    devops_work_item_id: null
  - id: T-GATE-004
    file: tickets/T-GATE-004-docs-duplicate-paragraph-check.md
    devops_work_item_id: null
  - id: T-GATE-005
    file: tickets/T-GATE-005-runner-feature-build-gate.md
    devops_work_item_id: null
  - id: T-GATE-006
    file: tickets/T-GATE-006-handoff-template-config-verification.md
    devops_work_item_id: null
  - id: T-GATE-007
    file: tickets/T-GATE-007-review-bot-gate-enforced-rules.md
    devops_work_item_id: null
  - id: T-GATE-008
    file: tickets/T-GATE-008-remove-committed-dev-secrets.md
    devops_work_item_id: null

devops:                       # only when plan_to_code = devops
  board_url: null
  published_at: null

code:                         # set by the implementing agent; repos from development.api/ui active paths
  api:
    repo: ai-code-framework/api/API.Framework       # development.api.active: api-framework (not a git repo)
    branch: null              # handoff.branch_pattern; same name in every repo touched. Required for the PR route
                              # and direct_scope: diff; optional for direct_scope: plan (null if not a git repo)
    base_branch: null         # PR target / diff base (review.target_branch unless stated); not used by direct_scope: plan
    head_commit: null         # commit handed to review, when the repo is under git
  ui:
    repo: ai-code-framework/ui/UI.NextJs.Framework  # development.ui.active: nextjs (not a git repo)
    branch: null
    base_branch: null
    head_commit: null
  build: pass                 # pass | fail
  tests: pass                 # pass | fail  (existing tests and checks the implementing agent ran; scenario test results are in `testing`)
  verification:            # commands run, e.g. "dotnet test ... --filter ..."
    - "dotnet build Api.Framework.sln --configuration Release -> pass (0 errors)"
    - "node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs -> pass (33/33; fixtures in ai-code-framework/scripts/fixtures/pre-handoff)"
    - "pre-handoff: eol api-framework -> pass (216 files, 0 findings)"
    - "pre-handoff: secrets api-framework -> pass (216 files, 0 skipped secret files, 0 findings)"
    - "pre-handoff: docs-dup api-framework -> pass (22 docs, 0 findings, 53 allowlisted)"
    - "pre-handoff: unit api-framework -> pass (57 passed, 0 failed, 0 skipped, 0 findings)"
    - "pre-handoff: lint nextjs -> pass (150 files, 0 errors, 2 warnings, 0 findings)"
    - "pre-handoff: typecheck nextjs -> pass (0 errors, 0 findings)"
    - "pre-handoff: eol nextjs -> pass (229 files, 0 findings)"
    - "pre-handoff: secrets nextjs -> pass (229 files, 2 skipped secret files, 0 findings)"
    - "pre-handoff: docs-dup nextjs -> pass (17 docs, 0 findings)"
    - "pre-handoff: unit nextjs -> pass (10 passed, 0 failed, 4 files, 0 findings)"
    - "pre-handoff: api-framework: not a git repo: working tree scanned"
    - "pre-handoff: nextjs: not a git repo: working tree scanned"
  pre_handoff_gate: pass      # pass | fail   last pre-handoff run (config `verification`; handoff/README.md rule 12)
  pre_handoff_gate_at: 2026-10-09T11:03:25+01:00   # ISO 8601 with offset of that run

implementation:               # MANIFEST of what the implementing agent built; the reviewing agent's starting point for direct_scope: plan
  # Filled by the implementing agent at self-review / hand-off. Hand-off is BLOCKED while every list is empty.
  # One entry per file that implements the plan: files created or changed for the feature, plus
  # existing files the feature relies on to render a control or persist a mapping (change: existing).
  # `path` is repo-relative under code.api.repo (api, migrations) or code.ui.repo (ui); tests say which.
  # Never list build output, node_modules, bin/obj, generated files or secret / .env files.
  recorded_at: 2026-10-09T11:03:19+01:00   # ISO 8601 with offset
  # Framework tooling (no specs / controls / DB columns). tests[] holds the gate tooling outside both repos (repo: framework, ai- paths).
  # Also changed, line endings / BOM only (T-GATE-002 normalisation): 51 API.Framework files, 173 UI.NextJs.Framework files (counts in History).
  api:
    - path: "Api.Framework/appsettings.json"
      change: modified
      tickets: [T-GATE-008]
      note: "ConnectionStrings.LoginConnection and Jwt.Secret emptied"
    - path: "Api.Framework.Data/LoginDbContextFactory.cs"
      change: modified
      tickets: [T-GATE-008]
      note: "hard-coded fallback removed; user-secrets + env; throws naming ConnectionStrings:LoginConnection"
    - path: "Api.Framework.Data/Api.Framework.Data.csproj"
      change: modified
      tickets: [T-GATE-008]
      note: "Microsoft.Extensions.Configuration.UserSecrets 10.0.12"
    - path: "Api.Framework/Api.Framework.csproj"
      change: modified
      tickets: [T-GATE-008]
      note: "UserSecretsId (dotnet user-secrets init); no values set"
    - path: "Api.Framework.Services/Auth/DefaultUserSeeder.cs"
      change: modified
      tickets: [T-GATE-008]
      note: "seed password literal removed; DefaultUser:Password from config; when unset: creates nothing, returns false, logs a warning (ILogger parameter, review F-04)"
    - path: "Api.Framework/Program.cs"
      change: modified
      tickets: [T-GATE-008]
      note: "seeder password from config, passes app.Logger (seeder logs the warning); clearer missing-connection-string message"
    - path: "AGENTS.md"
      change: modified
      tickets: [T-GATE-008, T-GATE-005]
      note: "Local settings (secrets) section, names only; Verify adds dotnet test + gate"
    - path: ".cursor/rules/api-framework-overview.mdc"
      change: modified
      tickets: [T-GATE-008]
    - path: ".claude/rules/api-framework-overview.md"
      change: modified
      tickets: [T-GATE-008]
    - path: ".editorconfig"
      change: added
      tickets: [T-GATE-002]
    - path: ".gitattributes"
      change: added
      tickets: [T-GATE-002]
  ui:
    - path: "eslint.config.mjs"
      change: added
      tickets: [T-GATE-001]
    - path: "package.json"
      change: modified
      tickets: [T-GATE-001]
      note: "lint: eslint . ; typecheck: tsc --noEmit"
    - path: "tsconfig.json"
      change: modified
      tickets: [T-GATE-001]
      note: "exclude e2e (D11); scratch .next-devbot-warm / .next-test-tb includes removed, keeps .next/ and .next-test/ (review F-05)"
    - path: "README.md"
      change: modified
      tickets: [T-GATE-005]
    - path: "AGENTS.md"
      change: modified
      tickets: [T-GATE-005]
    - path: ".editorconfig"
      change: added
      tickets: [T-GATE-002]
    - path: ".gitattributes"
      change: added
      tickets: [T-GATE-002]
    - path: "e2e/README.md"
      change: modified
      tickets: [T-GATE-008]
      note: "APIFW_TEST_ setting names; build-dir row notes the tsconfig restore"
    - path: "scripts/dev-test.mjs"
      change: modified
      tickets: [T-GATE-001]
      note: "puts tsconfig.json back byte for byte on exit when next dev added a build-dir include (review F-05)"
  tests:                      # test SCAFFOLDING the implementing agent owns: Api.Framework.Tests project, Playwright / e2e setup, test-data fixtures. Scenario tests are recorded by the testing agent in testing.results
    - path: "Api.Framework.Tests/Auth/DefaultUserSeederTests.cs"
      repo: api
      change: added
      tickets: [T-GATE-008]
      note: "unset password (null / empty / whitespace) -> no user, false, warning; password set -> system admin; user exists -> unchanged (review F-04)"
    - path: "ai-code-framework/scripts/pre-handoff-checks.mjs"
      repo: framework
      change: added
      tickets: [T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005]
    - path: "ai-code-framework/scripts/pre-handoff-allowlist.json"
      repo: framework
      change: added
      tickets: [T-GATE-003, T-GATE-004]
      note: "9 docs-dup mirror-pair entries; no secret entries"
    - path: "ai-code-framework/scripts/pre-handoff-checks.selftest.mjs"
      repo: framework
      change: added
      tickets: [T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005]
    - path: "ai-code-framework/scripts/fixtures/pre-handoff/"
      repo: framework
      change: added
      tickets: [T-GATE-002, T-GATE-003, T-GATE-004, T-GATE-005]
      note: "planted-violation fixtures for Review Bot (written by the self-test with --write-fixtures; a normal self-test run works on a temp copy and compares)"
    - path: "ai-code-framework/scripts/README.md"
      repo: framework
      change: added
      tickets: [T-GATE-005]
    - path: "ai-code-framework/loops/feature-build.md"
      repo: framework
      change: modified
      tickets: [T-GATE-005]
    - path: "ai-code-framework/AGENT-BRIEF.md"
      repo: framework
      change: modified
      tickets: [T-GATE-005]
  migrations: []
  # Entry shape (copy into the lists above):
  #  - path: Unity.API/Controllers/V2/<Name>Controller.cs
  #    repo: api               # api | ui  (tests only; api / migrations are always api, ui is ui)
  #    change: added           # added | modified | existing
  #    tickets: [T-<DOMAIN>-NNN]
  #    spec_pages: [<page>]    # specs/<page>.yaml
  #    controls: [<label>]     # spec control labels, manage-list columns or actions
  #    db: [<Service>:<Table>.<Column>]   # spec Service / Target DB Table / Target DB Column (or Population Source)
  #    scenarios: [T-<DOMAIN>-NNN/S1]     # mainly for tests

pull_requests: []             # when code_to_review = pr; one entry per repo
#  - repo: ai-code-framework/api/Unity.API
#    id: 1234
#    url: https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/1234
#    source_branch: feat/T-CONTACT-001/add-edit-contact
#    target_branch: <review.target_branch>

review:
  cycle: 2                    # +1 each time a code-review round ends with a final verdict or a change request (max handoff.max_review_cycles).
                              # Test-fix rounds do NOT count here (testing.failures_count_toward_review_cycles: false); see testing.test_fix_cycle
  report: reviews/DIRECT-pre-handoff-checks-2-review.md   # latest full report: reviews/PR-<id>-review.md | reviews/DIRECT-<branch-slug>-<n>-review.md
  log: reviews/review-log.md  # reviews/review-log.md (review.log_file); every code review and test review, both routes
  code_verdict: approve-with-comments   # PROVISIONAL code-review verdict until the test review: approve | approve-with-comments | request-changes
  test_verdict: null          # no Test Bot round for this feature (D16). test review (testing.test_review): approve | request-changes | blocked-noted (testing blocked, approval allowed by default (2))
  verdict: approve-with-comments    # FINAL: approve | approve-with-comments only when testing.final_approval_requires are all met; request-changes otherwise
  routed_to: null               # who fixes the latest findings: code | testing | both (testing.defect_routing)
  reviewed_commits: {}        # repo -> commit reviewed

testing:                      # CARVE-OUT: written ONLY by the testing agent (test-bot), also while review-bot owns the feature.
  # Everything else in this file stays the owner's. Rules: handoff/README.md -> Testing alongside review.
  status: pending             # pending | running | passed | failed | blocked   (running = the testing agent has picked the run up)
  round: 0                    # +1 per test run; n in tests/TEST-<feature>-<n>-report.md
  test_fix_cycle: 0           # test-fix rounds used / max testing.max_test_fix_cycles (5); separate from review.cycle. +1 when the testing agent
                              # starts the re-run after a failure was routed back (code or test defect); at max, the next one escalates to the human owner
  plan: null                  # tests/test-plan.md
  report: null                # latest run: tests/TEST-<feature>-<n>-report.md
  summary:                    # counts from the latest report
    scenarios: 0
    passed: 0
    failed: 0
    blocked: 0
    waiting: 0
    not_automated: 0
  results: []                 # one entry per scenario, keyed by the ticket's explicit ID (testing.scenario_ids: explicit)
  #  - scenario: T-<DOMAIN>-NNN/S1
  #    layers: [unit, api-e2e, ui-e2e]
  #    tests: ["<repo-relative path>::<test name or @T-<DOMAIN>-NNN/S1 tag>"]
  #    result: pass           # pass | fail | blocked | waiting | not-automated
  #    note: null             # failure message + trace / screenshot path, or why blocked / not automated
  blockers: []                # - "<what> (needs: implementing agent | human owner; raised <ISO time>)"
  updated_at: null            # ISO 8601 with offset
  updated_by: null            # test-bot

approvals:                    # required = handoff.require_human_approval at the time of the gate
  plan_to_code:
    required: true
    approved_by: human        # Neil Wood, 2026-10-09 10:32 BST: accepted all 17 suggested answers (D1-D17) and approved hand-off to Dev Bot
    approved_at: 2026-10-09T10:32:00+01:00
  code_to_review:
    required: false
    approved_by: null
    approved_at: null
  merge:
    required: true            # always; agents never merge
    approved_by: human        # Neil, told Dev Bot directly 2026-10-09 12:37 BST: treat as merged (no git; Neil's instruction is the merge). Recorded by plan-bot
    approved_at: 2026-10-09T12:37:00+01:00

blockers: []                  # - "<what> (raised by <agent>, <ISO time>)". 2026-10-09T10:34:24+01:00 plan-bot: WAITING ON NEIL cleared (Q1-Q17 answered, plan_to_code approved 10:32)
---

# Handoff: Pre-handoff automated checks (gate)

> **Now:** `merged` (2026-10-09 12:37 BST, Neil's word to Dev Bot; no git) · owner `human`. Earlier: `changes-requested` · owner `dev-bot` · pickup `pending` · review round 1: **Request changes** (1 Major, 4 Minor, 3 Nit; `reviews/DIRECT-pre-handoff-checks-1-review.md`) · pre-handoff gate `pass` (2026-10-09 10:55 BST)
> **Next:** Dev Bot fixes F-01 (secrets scan skips the credential-key walk when an appsettings file has comments) and F-02..F-08, re-runs the gate with `--record` and hands back to Review Bot. Review Bot does T-GATE-007 separately. Neil rotates the exposed dev DB password, Jwt secret and seeded system-admin password

## Summary

A pre-handoff gate in `ai-code-framework/loops/feature-build.md` stage 5: ESLint + `tsc --noEmit` for UI.NextJs.Framework, `.editorconfig` / `.gitattributes` and a line-ending / BOM check for both targets, a secrets scan of committed config / code / docs with an allowlist, and a duplicate-paragraph docs check. Results go in `code.verification` (+ `code.pre_handoff_gate`); a failed gate blocks `in-review`. Review Bot treats these points as gate-enforced. No UI pages: no specs, Excel or journeys.

## Artefacts

| Artefact | Path |
|----------|------|
| Plan | `plan.md` |
| Page specs / Excel / journeys / stubs | None (no UI pages or DB columns) |
| Tickets | `tickets/T-GATE-001..008-*.md` |
| Review log | `reviews/review-log.md` |
| Latest review | `reviews/DIRECT-pre-handoff-checks-1-review.md` (round 1, Request changes) |

## Notes for the next owner

- Owners: Dev Bot T-GATE-001..005 and 008 (`ai-code-framework`); Plan Bot T-GATE-006 (handoff template / README, config); Review Bot T-GATE-007 (its own `ai-review-framework`, cross-framework ticket).
- Decisions D1–D17 in `plan.md` §6 (Neil 10:32: all suggested defaults). T-GATE-008 (fix first) and T-GATE-004 (docs check now) are in scope.
- **Action for Neil (not an agent):** rotate the exposed dev DB password and Jwt secret, then set local values (user-secrets / `ConnectionStrings__LoginConnection`, `Jwt__Secret`; default names, Neil may override).
- T-GATE-006 done by plan-bot: template `code.pre_handoff_gate` / `pre_handoff_gate_at`, README rule 12, config `verification:` block.
- Neither target is a git repo; the gate scans the working tree (D14).
- No secret values are recorded anywhere in this feature folder (file + key names only).
- Dev Bot hand-off (2026-10-09 10:47): verify with `node ai-code-framework/scripts/pre-handoff-checks.mjs` (both targets) and `node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` (regenerates and checks `ai-code-framework/scripts/fixtures/pre-handoff/`: api-bad / nextjs-bad must fail, api-good / nextjs-good must pass). Single fixture runs: `ai-code-framework/scripts/README.md`.
- **Neil (not an agent):** rotate the dev DB password and Jwt secret that were committed, then set them for Development with `dotnet user-secrets set "ConnectionStrings:LoginConnection" ...` and `dotnet user-secrets set "Jwt:Secret" ...` (`--project Api.Framework`), or env vars `ConnectionStrings__LoginConnection` / `Jwt__Secret`. If the system admin account must be seeded again, also `DefaultUser:Password` (its old password was a committed literal too). Test values are now user-level `APIFW_TEST_ConnectionStrings__LoginConnection` / `APIFW_TEST_Jwt__Secret`, read only in Test (History row 6); Development needs the user-secrets above before it starts.
- Deviation for review: DefaultUserSeeder's hard-coded password was not in the plan's secrets table but the scan rule (literal assigned to a password name) flags it, so it moved to `DefaultUser:Password` instead of being allowlisted (D1/D13: real credentials are fixed, not allowlisted). Not migrated to user-secrets by Dev Bot: ticket 008 says agents never read or write the values.
- Allowlist: 9 `docs-dup` entries, one per `.cursor/rules/*.mdc` ↔ `.claude/rules/*.md` mirror pair in API.Framework (expires 2027-04-09); no secrets entries. The `AnimalPoliciesTests.cs` dummy key is not flagged by the rules, so it has no entry.
- Gate watch-outs: a running `next dev` rewrites `tsconfig.json` (adds its distDir types with CRLF) and can make `eol nextjs` fail; re-run `--fix-eol --target nextjs` only when no one else is editing. Lint warning baseline: 2 (`animal-ui-schema.ts` unused `_schema` / `_editing`).

## History

Append one row per transition or pickup. Newest last. Never edit earlier rows. The owner writes History; the testing agent does not (its runs are in `tests/test-log.md`, and the reviewing agent records each test review here).

| # | When | Stage | Owner | Route / gate | By | Note |
|---|------|-------|-------|--------------|----|------|
| 1 | 2026-10-09T10:30:22+01:00 | — → planned | — → plan-bot | — (draft, not approved) | plan-bot | Draft plan + tickets T-GATE-001..008 from Neil's request relayed by Dev Bot (2026-10-09). Read-only investigation done. Waiting on Neil for Q1–Q17 and plan_to_code approval; nothing handed off, no messages sent |
| 2 | 2026-10-09T10:34:24+01:00 | planned | plan-bot → dev-bot | plan_to_code · direct (approved) | plan-bot | Neil 2026-10-09 10:32 BST accepted all 17 suggested answers (D1–D17) and approved plan_to_code (approvals.plan_to_code recorded). Plan / tickets updated: questions → decisions, T-GATE-004 and T-GATE-008 unconditional; in-ticket defaults (user-secrets + ConnectionStrings__LoginConnection / Jwt__Secret; Review Bot updates sample + template wording) marked "Neil may override". WAITING ON NEIL blocker cleared. Owner dev-bot, pickup pending; no message sent by plan-bot |
| 3 | 2026-10-09T10:34:24+01:00 | planned | dev-bot | T-GATE-006 done (plan-bot, no gate) | plan-bot | T-GATE-006 (plan-bot owned) done: handoff/templates/handoff.md code.verification comment + pre_handoff_gate / pre_handoff_gate_at; handoff/README.md in-review transition rows + rule 12 (missing / failed gate blocks in-review; Review Bot returns without a round); ai-framework.config.yaml verification: block (YAML validated on the box, other sections unchanged). Existing feature handoff files untouched. Front matter unchanged by this row |
| 4 | 2026-10-09T10:36:21+01:00 | planned → in-development | dev-bot | plan_to_code · direct (approved 10:32) | dev-bot | Picked up (pickup: accepted). Plan Bot handed over with owner dev-bot / pickup pending and approvals.plan_to_code recorded but left stage `planned`; set `in-development` on acceptance. Order: T-GATE-008 → 001–004 → 005. Read config, AGENT-BRIEF, feature-build, handoff README (rule 12), plan D1–D17, tickets 001–008 |
| 5 | 2026-10-09T10:47:48+01:00 | in-development → in-review | dev-bot → review-bot | code_to_review · direct; no Test Bot round (D16); pre-handoff gate pass (10:47:27) | dev-bot | T-GATE-008: appsettings.json ConnectionStrings.LoginConnection + Jwt.Secret emptied; LoginDbContextFactory fallback removed (user-secrets + env, throws naming ConnectionStrings:LoginConnection); UserSecretsId added to Api.Framework (no values written: ticket 008 says agents never read or write the values); DefaultUserSeeder password literal moved to DefaultUser:Password (skips seeding when unset); Program.cs messages; AGENTS.md Local settings (names only). Verified: Release build; dev API in Development fails clearly with nothing set, starts with env vars and with user-secrets (dummy probe values, removed); Test profile starts with the user env vars; dotnet ef design time fails clearly without config, works with the env var. T-GATE-001: eslint.config.mjs (FlatCompat next/core-web-vitals + next/typescript), lint: eslint ., typecheck: tsc --noEmit; root tsconfig excludes e2e (D11); baseline 0 errors / 2 warnings, no source fixes needed. T-GATE-002: .editorconfig + .gitattributes in both targets; D12 checked (manage-animals approved/human, add-edit-contact example) then normalised endings/BOM/final newline only: API.Framework 51 files (20 .md, 1 .mdc, 3 .csproj, 24 .cs, 1 .sln, 2 .json), UI.NextJs.Framework 173 files (82 .ts, 56 .tsx, 22 .css, 6 .json, 3 .md, 2 .gitignore, 1 .cjs, 1 .mts); independent byte check against a %TEMP% backup: content otherwise identical. T-GATE-003/004/005: ai-code-framework/scripts/pre-handoff-checks.mjs (+ allowlist, self-test, fixtures, README); feature-build stage 5/6/8 + checklist, AGENT-BRIEF DoD. Self-test 33/33; fixtures fail as planted. Full gate on both targets: pass (code.verification) |
| 6 | 2026-10-09T10:55:30+01:00 | in-review (unchanged) | review-bot (unchanged) | addition approved by Neil; gate pass (10:55:12) | dev-bot | Test settings scoped to Test: Program.cs and LoginDbContextFactory add env vars with prefix APIFW_TEST_ only when the environment is Test. Neil's user-level ConnectionStrings__LoginConnection / Jwt__Secret moved to APIFW_TEST_ConnectionStrings__LoginConnection / APIFW_TEST_Jwt__Secret (values not printed) and the unprefixed vars deleted; E2E_*, BASE_URL, API_URL unchanged. Docs: API AGENTS.md Local settings, api-framework-overview (.mdc/.md), e2e/README.md, scripts/README.md. Fresh-process checks: Test starts, swagger 200, DB reached (design-time resolves api_framework_test); Development without user-secrets fails with the missing-setting message (expected until Neil sets user-secrets). code.verification re-recorded. No stage / owner change |
| 7 | 2026-10-09T10:56:49+01:00 | in-review (unchanged) | review-bot (unchanged) | plan doc + config note (no gate) | plan-bot | D1 / T-GATE-008 amendment recorded in plan.md §6 and T-GATE-008 Notes: DefaultUserSeeder admin password → `DefaultUser:Password` setting (deviation found by the scan); Test-only user-level env vars `APIFW_TEST_ConnectionStrings__LoginConnection` / `APIFW_TEST_Jwt__Secret` (Neil approved). ai-framework.config.yaml: testing.database.connection_env and secrets.test_db_connection_env renamed to the APIFW_TEST_ name (Test-only comment, Jwt name noted); verification banner updated (runner + allowlist exist; flags --target/--feature/--record/--json). Names only. Front matter unchanged |
| 8 | 2026-10-09T10:49:30+01:00 | in-review | review-bot | pickup accepted · code_to_review direct; gate pass checked (D10) | review-bot | Picked up Dev Bot's 10:48 hand-off (pickup: accepted; row written with the result because the file was edited concurrently by dev-bot and plan-bot during the review). `code.pre_handoff_gate: pass` present, so a review round starts (D10). Read-only on code and docs. Gate and self-test planted-violation runs on a temporary copy only |
| 9 | 2026-10-09T10:57:46+01:00 | in-review → changes-requested | review-bot → dev-bot | review round 1 · Request changes (1 Major, 4 Minor, 3 Nit) | review-bot | Report `reviews/DIRECT-pre-handoff-checks-1-review.md`, log `reviews/review-log.md` round 1. Gate in place pass (10:51:37, and 10:56:25 after History row 6) and on a temporary copy pass (10:51:06); self-test 33/33 (copy); 22 planted violations: 20 failed with exit 1, 2 missed (F-01: comment in appsettings disables the credential-key walk, Major; F-02: all-caps values, Minor). D10 gate result recorded honestly. Normalisation spot-check: 448 backup files, endings / BOM / final newline only (51 API / 173 UI confirmed). DefaultUserSeeder deviation safe (no fallback, no value logged, nothing in committed config); test missing (F-04). Allowlist: 9 docs-dup mirror pairs, narrow, justified, expiring 2027-04-09. Dev Bot's 10:55 APIFW_TEST_ addition folded in (sound; e2e/README.md missing from manifest, F-08). review.cycle 0 → 1. No secret values recorded; nothing merged |
| 10 | 2026-10-09T10:59:24+01:00 | changes-requested | dev-bot | review_feedback · direct (round 1) | dev-bot | Picked up (pickup: accepted) to fix F-01 (Major), F-02, F-03, F-04, F-08 (Minor) and F-05, F-06, F-07 (Nit) from reviews/DIRECT-pre-handoff-checks-1-review.md |
| 11 | 2026-10-09T11:04:28+01:00 | changes-requested → in-review | dev-bot → review-bot | code_to_review · direct (round 2); no Test Bot round (D16); pre-handoff gate pass (11:03:25) | dev-bot | Review round 1 fixed: F-01 JSONC comments / trailing commas stripped (string-aware) before the key walk, still-unparseable JSON fails `secrets-json-unparsed`; F-02 only explicit references (${NAME}, %NAME%, $(NAME), env:NAME) pass, ALL_CAPS values under credential keys are reported; F-03 unused unexpired allowlist entries reported (secret-* fails, others warn); F-04 Api.Framework.Tests/Auth/DefaultUserSeederTests.cs (5 tests; seeder now logs the warning via an ILogger parameter); F-05 scratch .next-* tsconfig includes removed, dev-test.mjs restores tsconfig.json on exit; F-06 self-test runs on a temp copy and only compares the committed fixtures (--write-fixtures to rewrite); F-07 self-test covers unit failure, D11 e2e rules, allowlist schema, --feature, --record (64 assertions, pass); F-08 manifest adds e2e/README.md, scripts/dev-test.mjs and the seeder tests, recorded_at refreshed. Gate: API 57 tests, UI 10 tests, lint 0 errors / 2 warnings, typecheck 0, eol / secrets 0 findings, docs-dup 53 allowlisted. |
| 12 | 2026-10-09T11:13:30+01:00 | in-review → approved | review-bot → human | review round 2 · Approve with comments (0 Major, 2 Minor, 2 Nit); no Test Bot round (D16) | review-bot | Report `reviews/DIRECT-pre-handoff-checks-2-review.md`, log `reviews/review-log.md` round 2. Round-1 F-01..F-08 all fixed and verified. Gate in place pass (11:07:08, identical to the 11:03:25 record; check-only, no --record) and on a temporary copy pass (11:06:24); self-test 64/64 (copy; temp dir, committed fixtures unchanged). Planted matrix 37 cases: 32 as expected (24 core + 3 round-1 misses + JSONC tricky shapes), 5 gaps: F-09 connection-string Password= with leading { $ < % or quoted value skipped (Minor), F-11 {…}-wrapped / {letter values skipped (Nit). F-10 dev-test.mjs whole-file tsconfig restore can revert concurrent edits (Minor); F-12 code.verification self-test line stale 33/33 (Nit). F-04 logger passed in production (Program.cs:132 app.Logger). No values printed; review.cycle 1 → 2; nothing merged |
| 13 | 2026-10-09T12:38:49+01:00 | approved → merged | human | merge (human gate; Neil's instruction, no git) | plan-bot | merged — recorded by plan-bot on Neil's word to Dev Bot 2026-10-09 12:37 BST (no git; Neil's instruction is the merge). approvals.merge recorded (human, 12:37). Neil's D1 to-dos stay open: rotate the exposed dev DB password, Jwt secret and DefaultUser:Password (seeded system-admin); set Development user-secrets |
