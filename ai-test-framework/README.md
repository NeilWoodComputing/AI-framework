# AI test framework

How the **testing agent** proves that a feature does what its tickets say. It turns each ticket's Given / When / Then scenarios into tests, runs them against the real stack on a dedicated test database, records the results in the feature's `handoff.md` `testing` section and `tests/` folder, and hands the run to the reviewing agent for the **test review**.

> **Status: wired.** `../ai-framework.config.yaml` carries this framework (`frameworks.testing`, `agents.testing`, the `testing` block, `handoff.code_to_test`, `output.feature_layout.tests`), and `../handoff/README.md` → **Testing alongside review** sets the rules. Neil chose option B on 08/10/2026 (19:07 BST): tests run **alongside the review**, followed by a review of the tests. His decisions of 08/10/2026 (17:12–17:27 BST) still apply: dedicated PostgreSQL test database, `Api.Framework.Tests` approved, reset endpoint in API.Framework only with master + per-batch resets, key **and** signed-in test persona, role-based personas, master reset = truncate + reseed.
>
> **Expect the first runs to be Blocked.** There is no test environment yet, and the scaffolding (`Api.Framework.Tests`, the e2e folder at `testing.e2e.nextjs.path`), the reset endpoint and the test personas do not exist yet. They are the implementing agent's to build (`testing.ownership`). Until they exist, the testing agent reports **Blocked** / **Waiting** rows with an owner rather than building them itself.

## Roles

The docs name roles, not agents. `agents` in `../ai-framework.config.yaml` maps each role to whoever fills it today.

| Role | Config entry | Does here |
|------|--------------|-----------|
| **The testing agent** | `agents.testing` (today: Test Bot, `test-bot`) | Plans tests from the tickets' explicit scenario IDs, writes the scenario tests (unit and e2e; test code only, in projects and folders that already exist), runs them, writes `tests/` and the `testing` section of `handoff.md`, then messages the reviewing agent (`testing.ownership.scenario_tests`, `test_runs`) |
| **The implementing agent** | `agents.code` (today: Dev Bot, `dev-bot`) | Builds the feature **and** the test scaffolding: creates `Api.Framework.Tests`, sets up Playwright + playwright-bdd and the `e2e/` folder in UI.NextJs.Framework, adds the test-data **reset endpoint** and the **test users** (personas) (`testing.ownership.scaffolding`, `reset_endpoint`, `test_users`); fixes code defects |
| **The reviewing agent** | `agents.review` (today: Review Bot, `review-bot`) | Owns the feature while it is `in-review`; reviews the code, then reviews each test run (`testing.test_review`); routes failures (`testing.defect_routing`); gives the final verdict only when both pass (`testing.final_approval_requires`) |
| **The planning agent** | `agents.planning` (today: Plan Bot, `plan-bot`) | Owns tickets and specs; freezes the explicit scenario IDs (`### Scenario: S<n> — <title>`); genericises scenarios that name real people; fixes untestable scenarios |
| **The human owner** | `agents.human` | Sets up the test environment, database and secrets; decides the flagged defaults; merges |

## Where it sits in the pipeline

```text
build → code review ∥ test run → test review → final approval → merge
```

| Step | Who | What |
|------|-----|------|
| build | Implementing agent | Code, plus test scaffolding, reset endpoint and test personas; fills `implementation` in `handoff.md`; hands off to review **and** testing at the same time (`handoff.code_to_review` + `handoff.code_to_test`) |
| code review ∥ test run | Reviewing agent ∥ testing agent | The feature stays `in-review`, owned by `review-bot`. The reviewing agent reviews the code (provisional verdict) while the testing agent writes and runs the scenario tests |
| test review | Reviewing agent | Triggered by the testing agent's message (`review.triggers: test-report`): report, results, test code quality, every scenario has a real test. A failed run goes back for fixing (code defects → implementing agent; test defects → testing agent); each such fix loop is one **test-fix round** (`handoff.md` `testing.test_fix_cycle`, max `testing.max_test_fix_cycles` = 5; at the cap the reviewing agent escalates to the human owner instead of routing) |
| final approval | Reviewing agent | Only when code review **and** test review pass (`testing.final_approval_requires: [code_review, test_review]`) |
| merge | Human owner | Agents never merge |

There is only one mode: `testing.mode: alongside-review`. There is no testing stage and no hand-off *to* testing as an owner; `test-bot` is never an `owner` in `handoff.md`.

## Config wiring

What is in `../ai-framework.config.yaml` today, and what each key means for this framework. Read the config itself for the current values; this table only explains them.

| Key | What it says |
|-----|--------------|
| `frameworks.testing` | This folder: `path`, `agent_brief`, `loop` (`loops/feature-test.md`), `checklists` |
| `agents.testing` | Test Bot, id `test-bot`; `hands_off_to: review`. The id is used only as `testing.updated_by` in `handoff.md`, never as `owner` |
| `handoff.code_to_test` | `direct`: the implementing agent messages the testing agent with the feature path at the same time as `code_to_review`. No stage change |
| `handoff.require_human_approval.code_to_test` | `false`: no approval needed to notify the testing agent |
| `output.feature_layout.tests` | `tests`: the feature's `tests/` folder, which the testing agent may write while `review-bot` owns the feature |
| `output.work_dirs`, `project.work_dir`, `output.work_dir`; `handoff.md` `feature_path` | Where features live. `feature_path` in the feature's `handoff.md` is authoritative; with none known, search each `output.work_dirs` entry in order for `<feature-slug>/` (exactly one match; `AGENT-BRIEF.md` → Finding the feature folder). New features are under `project.work_dir` (`ai-planning-framework/projects/<project>/work`), older ones under `output.work_dir` (`ai-planning-framework/work`) |
| `testing.mode` | `alongside-review` (the only mode in use) |
| `testing.test_review`, `testing.final_approval_requires` | The reviewing agent reviews every run; final approval needs `code_review` and `test_review` |
| `testing.scenario_ids` | `explicit`: tests are tagged with the ticket's explicit `<ticket>/S<n>`, never heading order |
| `testing.ownership` | `scaffolding`, `reset_endpoint`, `test_users` → `code`; `scenario_tests`, `test_runs` → `testing` |
| `testing.defect_routing` | `code_defects` → `code` (stage `changes-requested`); `test_defects` → `testing` (stage stays `in-review`) |
| `testing.max_test_fix_cycles` | `5`: test-fix rounds have their **own** cap (Neil, 08/10/2026 19:19 BST). Counted in `handoff.md` `testing.test_fix_cycle`; at the cap the reviewing agent escalates to the human owner instead of routing again (see **Test-fix rounds**) |
| `testing.failures_count_toward_review_cycles` | `false` (Neil, 19:19 BST): test-fix rounds do **not** count toward the 3 code-review rounds (`handoff.max_review_cycles`) |
| `testing.blocked_tests_allow_approval` | `false`: a blocked run does not get final approval (decided default (2), see below) |
| `testing.shared_environments_allowed`, `environment`, `database.*`, `ui_base_url`, `api_base_url` | The test environment (below); `<placeholders>` stop the run |
| `testing.reset_endpoint.*`, `testing.personas.*` | Reset routes, key header and env var, master persona; persona naming, email domain, password env var pattern |
| `testing.e2e.nextjs.*` | e2e `path` (does not exist yet; scaffolded by the implementing agent), `runner`, `command` |
| `testing.unit.*` | `dotnet test` commands for `unity-api` and `api-framework` |
| `testing.report_names` | `tests/test-plan.md`, `tests/TEST-<feature>-<n>-report.md` (`n` = `handoff.md` `testing.round`), `tests/test-log.md` |
| `testing.forbid_frontend_mocks` | `true` (hard rule 3) |
| `secrets.test_*` | Env var **names** only for the test connection string, reset key and persona passwords |

### Defaults flagged to Neil

Configurable in `testing` (`../handoff/README.md` → Testing alongside review):

1. **`failures_count_toward_review_cycles`** — **decided by Neil, 08/10/2026 19:19 BST: `false`.** Test-fix rounds have their own cap, `max_test_fix_cycles: 5`, and do not count toward the 3 code-review rounds. (Was flagged as `true`.)
2. **`blocked_tests_allow_approval: false`** — decided. If testing is `blocked` (for example no test environment yet), or a required unit command was not run, the reviewing agent does not give final approval. The stage stays `in-review` and the owner is the human owner.

> The authoritative rules are `../handoff/README.md` → Testing alongside review, point 9 (Separate test-fix cap). If anything here disagrees with it or the config, they win: stop and report the mismatch.

### Test-fix rounds

Fixing failing tests has its **own** limit, separate from the code-review rounds.

| Rule | Detail |
|------|--------|
| What one round is | Each failed test run (or test review requesting changes) that the reviewing agent routes back for a fix, whichever way: code defect → implementing agent (stage `changes-requested`), or test defect → testing agent (stage stays `in-review`). A run counts **once**, even if it has both kinds of defect |
| Counter | `handoff.md` → `testing.test_fix_cycle` (starts at 0). The testing agent keeps it, inside its carve-out: +1 when it **starts the re-run that follows a routed-back failure** (at the same time as `status: running`): the trigger is the reviewing agent's test-defect message, or a `code_to_test` re-hand-off after a run that ended `failed`. So the value is always the number of fix rounds used so far |
| Cap and escalation | `testing.max_test_fix_cycles` (5). When a test review would route failures back again and `test_fix_cycle` is already 5, **the reviewing agent** does not route them: it sets `owner: human` (stage `changes-requested`), records the reason and asks Neil how to proceed. The testing agent never starts a sixth fix re-run: if one is asked for with the counter at 5, it does not run, adds the blocker "test-fix limit reached (5)" and messages the reviewing agent and the human owner. Nobody loops again until Neil decides |
| Separate from review rounds | `testing.failures_count_toward_review_cycles: false`: test-fix rounds never count toward `handoff.max_review_cycles` (3), and code-review rounds never count toward `max_test_fix_cycles` |
| Not a round | A `passed` run; a `blocked` run (nothing to fix in code or tests); a re-run caused only by a code-review Request changes |
| Stage and owner | The reviewing agent's, including the escalation. The testing agent never changes `stage`, `owner` or History, even at the cap |

## Test environment (default, adopted 08/10/2026)

| Part | Default (placeholders in `<>`) |
|---|---|
| Database | A dedicated **PostgreSQL** database for API.Framework only, `testing.database.name` (`<api_framework_test>`), on the local PostgreSQL server. Never shared with dev, other apps or other APIs. Its schema is built by API.Framework's own EF Core migrations (`Api.Framework.Data/Migrations`, Npgsql), from the first (`20260923152501_InitialLogin`) to the latest, including their `HasData` seed. |
| API | API.Framework with `ASPNETCORE_ENVIRONMENT=Test` (`testing.environment`; or `E2E`), connection string `LoginConnection` supplied by the user-level env var `APIFW_TEST_ConnectionStrings__LoginConnection` pointing at `<api_framework_test>` and the JWT signing key by `APIFW_TEST_Jwt__Secret` (both read only when `ASPNETCORE_ENVIRONMENT=Test`; the `APIFW_TEST_` prefix is stripped, and the unprefixed names are no longer used), at `testing.api_base_url`. Its database user has DML + `TRUNCATE` rights only; `InitialisationSettings__MigrateDatabase=false` |
| Migrations | Applied to `<api_framework_test>` with a separate owner / migration connection (or by the human owner) whenever they change, then a master reset |
| UI | UI.NextJs.Framework at `testing.ui_base_url` (`<http://localhost:3003>`, its `dev` script port) with `NEXT_PUBLIC_SYSTEM_API_ROOT` pointing at the Test API root, no version segment (`npm run dev:test` sets it to `E2E_UI_API_ROOT`, default `https://localhost:7188/`) |
| Who sets it up | The human owner. Agents never open `.env*`, never read, print or change connection strings or `appsettings*` secrets |
| Never | Shared dev / non-production APIs or databases for e2e, ever (`testing.shared_environments_allowed: false`) |

Provider notes and concerns: `skills/add-test-data-reset/SKILL.md` → Database and provider.

## Hard rules

1. **Never invent requirements.** The tickets' scenarios, the specs (`specs/*.yaml`) and `plan.md` decisions are the only source of what to test. Ambiguous or untestable scenarios go back to the planning agent. A scenario that names a real person is example data: test it with a role persona where the spec's population source is generic, and flag the ticket to the planning agent.
2. **Every scenario has its own traceable test, keyed by its explicit ID** (`testing.scenario_ids: explicit`). The ID is read from the ticket heading `### Scenario: S<n> — <title>` and referenced as `T-<DOMAIN>-NNN/S<n>`. Never number scenarios by heading order. Gaps (for example S2–S9 then S12) and `(was …)` notes are normal; IDs are never renumbered. A ticket whose scenarios have no explicit `S<n>` is **Blocked — scenario IDs not frozen**: raise it with the planning agent and do not invent numbers. Each scenario maps to a test per layer it needs (unit, API e2e, UI e2e), tagged `@T-<DOMAIN>-NNN/S<n>` (e2e) or `[Trait("Scenario", "T-<DOMAIN>-NNN/S<n>")]` (xUnit). Only when one test fully proves two scenarios does it carry both tags, and the plan says so.
3. **No front-end mocks in functional e2e tests** (`testing.forbid_frontend_mocks`). The real front end, the real running API, the real test database. No `page.route` / `context.route` fulfilment or modification, no `routeFromHAR`, no MSW, no stubbed `fetch`, no faked auth or permission responses. Observing traffic is fine (`checklists/e2e-checklist.md` → E1).
4. **Every scenario resets its own data first.** The first step of every e2e scenario calls a granular reset key owned by its batch (`{feature}.{batch}.{state}`), which resets only the data that batch touches. No test relies on data or persona state left by another (E5).
5. **Master reset once per run.** A full suite run starts with one master reset (`POST TestData/Reset/master`): `TRUNCATE` every app table (schema stays as the migrations built it; no drops), then run **all** seed units in dependency order: migration `HasData` rows, test tenant, personas, each batch's default state. It is also the way to recover a dirty database. It never replaces the per-scenario reset, and both use the same seed units.
6. **The reset endpoint lives in API.Framework only**, is registered only in the Test environment, works only on the named test database, and needs **both** the secret key header **and** a signed-in test persona (master: the `testdata-admin` persona only). The implementing agent builds it; the testing agent only calls it.
7. **Role-based test personas only.** `<feature>-<role>` users (for example `animals-tester`, `animals-viewer`) seeded by the test-data mechanism into the test database only; passwords from env vars. Never real people, never migrations / `HasData`. The implementing agent defines and seeds them.
8. **Mock only at backend boundaries in unit tests.** Downstream HTTP clients, the clock, the current user, outbound senders. Never the class under test, its validators or its mappers.
9. **Follow each codebase's own test rules.** Unity.API: `Unity.API.Tests` per `.cursor/rules/unity-api-testing.mdc`. API.Framework: `Api.Framework.Tests` (xUnit + Moq), **approved by Neil on 08/10/2026**, created by the implementing agent (`skills/write-api-unit-tests/SKILL.md`).
10. **Test code only.** The testing agent never creates a test project, the e2e scaffolding, the reset endpoint or personas, and never changes production code or weakens a test to make it pass. Missing scaffolding → **Waiting** / **Blocked** with owner `code` (the implementing agent).
11. **Stay inside the carve-out.** While `review-bot` owns the feature, the testing agent writes only the `testing` section of `handoff.md` and the feature's `tests/` folder (plus test code in the existing test project / e2e folder). Never the front matter, `stage`, `owner`, `review`, `approvals`, `implementation` or History.
12. **Five test-fix rounds, then the human owner.** Keep `testing.test_fix_cycle`; never start a sixth fix loop (`testing.max_test_fix_cycles`). Test-fix rounds do not count toward the code-review cap.
13. **Secrets stay out of source.** Persona passwords, the reset key and the connection string come from env vars named in config. Never print, log or commit their values; never open `.env*`.
14. **Agents never merge, approve or complete PRs**, and never run `git init` without asking the human owner.
15. **Shared editing rules** (`AGENT-BRIEF.md` → Shared editing rules; the planning agent's proposal of 27/10/2026, adopted by test-bot). Hash-check every file before and after changing it, make targeted edits only, write UTF-8 without a BOM keeping each file's line endings, and after any change inside `ai-planning-framework/` hand off only when `py tools/check.py` (run from `ai-planning-framework/`) ends `RESULT: PASS`. In a feature folder test-bot still writes only `handoff.md` `testing` and `tests/`.

## Inputs

| Input | From |
|-------|------|
| Tickets (`tickets/T-<DOMAIN>-NNN-*.md`) — explicit scenario IDs, Given / When / Then and Work to do | The feature folder: `feature_path` in its `handoff.md` (else the one `output.work_dirs` entry holding `<feature>/`) |
| Specs (`specs/*.yaml`) — controls, mandatory, messages, mappings | same |
| `plan.md` — decisions and out-of-scope list | same |
| `handoff.md` — `implementation` manifest (`api`, `ui`, `tests`, `migrations`), stage, `testing` | same |
| Active API / UI and their rules | `development.api.active`, `development.ui.active` |

## Outputs

| File | What |
|------|------|
| `handoff.md` → `testing` | `status` (`running` on pick-up, then `passed` \| `failed` \| `blocked`), `round`, `test_fix_cycle`, `plan`, `report`, `summary`, `results` keyed by `<ticket>/S<n>`, `blockers`, `updated_at`, `updated_by: test-bot` |
| `tests/test-plan.md` | Batches, reset keys, personas, scenario → test → key → status (`templates/test-plan.md`) |
| `tests/TEST-<feature>-<n>-report.md` | One report per run, `n` = `testing.round` (`templates/test-report.md`) |
| `tests/test-log.md` | One line per run, newest last |
| E2E features and steps | In the existing e2e folder at `testing.e2e.nextjs.path` (scaffolded by the implementing agent) |
| Unit tests | In the existing `Api.Framework.Tests` / `Unity.API.Tests` project |

## Layout

```text
ai-test-framework/
  README.md                           ← this file
  AGENT-BRIEF.md                      ← short brief for the testing agent
  loops/
    feature-test.md                   ← trigger, stages, gates and checklist (alongside-review only)
  skills/
    plan-tests-from-tickets/SKILL.md  ← explicit scenario IDs → batches, keys, personas, tests
    write-api-unit-tests/SKILL.md     ← backend unit test rules per API (tests in the existing project)
    add-test-data-reset/SKILL.md      ← environment, seed units, master + batch resets, personas, safety (built by the implementing agent)
    write-e2e-tests/SKILL.md          ← Playwright + playwright-bdd against the real stack (in the existing e2e folder)
    run-tests-and-report/SKILL.md     ← run order, classify, report, update `testing`, message the reviewing agent
  checklists/
    api-unit-test-checklist.md
    e2e-checklist.md                  ← E1 no front-end mocks; E5 reset first
    reset-endpoint-safety-checklist.md
  templates/
    test-plan.md
    test-report.md
    reset-handler.md                  ← C# skeletons for the implementing agent: guards, seed units, master, batch, personas
    e2e-feature.md                    ← .feature + steps + global setup skeleton
  examples/
    manage-animals-test-plan.md       ← the real T-ANIMAL scenarios (T-ANIMAL-001 to -009) in batches
    unity-ui-e2e-reference.md         ← what to copy from Unity.UI.Framework, and where it mocks
```

## Reference implementation

Unity.UI.Framework (`D:\Users\nwood01\Documents\Candc\ui\Unity.UI.Framework\e2e`, also copied under `ai-code-framework/ui/UI.Angular.Framework/e2e`) is the reference for e2e structure: Playwright + playwright-bdd, shared fixtures, `tid` selectors, API sign-in, response waits. **It relies heavily on front-end route mocks**, which this framework forbids. See `examples/unity-ui-e2e-reference.md`.

## Still open outside this framework

Not part of the config wiring; listed so nobody assumes they are done.

- **Review framework** (`ai-review-framework`, the reviewing agent's): `skills/review-tests/SKILL.md` reading the latest `tests/TEST-<feature>-<n>-report.md` and `handoff.md` `testing`; severity for front-end mocks or a missing first-step reset (suggested **Major**) and for an unsafe reset endpoint (suggested **Blocker**).
- **Implementing agent's build work:** `Api.Framework.Tests` and the update to `.cursor/rules/api-framework-testing.mdc` (it still says no test project exists); Playwright + playwright-bdd and the e2e folder in UI.NextJs.Framework; the reset endpoint and the feature's batches and personas.
- **Human owner:** the test environment, `<api_framework_test>`, and the env vars named in `secrets`.
- **Unity.UI.Framework:** decide whether to keep its mock-based suites as UI-level tests, separate from functional e2e tests.
