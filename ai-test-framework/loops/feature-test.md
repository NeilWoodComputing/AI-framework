# Loop: feature test

One pass of the testing agent over one feature, **alongside the review** (`testing.mode: alongside-review`). Re-run it on every new `code_to_test` message and whenever the reviewing agent sends test defects.

```text
build → code review ∥ test run → test review → final approval → merge
                      ^^^^^^^^ this loop
```

## When it runs

| Trigger | State of the feature | What happens next |
|---|---|---|
| The implementing agent's `code_to_test` message (`handoff.code_to_test: direct`), sent at the same time as its hand-off to review | `in-review`, owner `review-bot` (unchanged; there is no testing stage) | This loop runs while the reviewing agent reviews the code. When it ends, the reviewing agent runs the **test review** (`review.triggers: test-report`) |
| The reviewing agent sends **test defects** (`testing.defect_routing.test_defects: testing`) | Still `in-review` | Fix the test code, re-run this loop from stage 4, bump `testing.round` and `testing.test_fix_cycle` (see **Test-fix rounds**) |

A re-run that follows a routed-back failure (a test-defect message, or a `code_to_test` re-hand-off after a run that ended `failed`) is a **test-fix round**. Check the cap first: if `testing.test_fix_cycle` is already `testing.max_test_fix_cycles` (5), do not run; see **Test-fix rounds**.

## Stages

### 1. Gather and pick up

- Config: `agents`, `development.*.active`, `output.work_dirs` (with `project.work_dir` and `output.work_dir`), `output.feature_layout.tests`, the `testing` block (`<placeholders>` stop the affected work).
- Feature folder (`feature_path` in `handoff.md`; with none known, the one `output.work_dirs` entry holding `<feature>/`; `AGENT-BRIEF.md` → Finding the feature folder): `tickets/`, `specs/`, `plan.md` (decisions, out of scope), `handoff.md` (stage, `implementation` manifest, `testing`).
- The active API's and UI's test rules (`skills/write-api-unit-tests/SKILL.md` → Which rules apply).
- **Pick up:** set `handoff.md` `testing.status: running`, `testing.updated_at`, `testing.updated_by: test-bot`; if this re-run follows a routed-back failure, also `testing.test_fix_cycle` +1 (`../handoff/README.md` → Testing alongside review, point 9). Nothing else in `handoff.md`.
- Gate: every input exists. A missing ticket or spec is a question for the planning agent.

### 2. Plan — `skills/plan-tests-from-tickets/SKILL.md`

- Write or update `tests/test-plan.md`: every `<ticket>/S<n>` → layer (unit / e2e / both) → test name and tag → reset scenario key.
- **Scenario IDs are explicit** (`testing.scenario_ids: explicit`): read from `### Scenario: S<n> — <title>` headings only. Never number by heading order; gaps and `(was …)` notes are fine. A ticket with no explicit `S<n>` IDs → its rows are **Blocked — scenario IDs not frozen**; message the planning agent.
- Gate: every explicitly numbered scenario has a row; no row without a scenario; no invented IDs.

### 3. Check prerequisites

- Test environment reachable: Test UI and API.Framework (`Test` / `E2E`) on the dedicated PostgreSQL database `<api_framework_test>`; never a shared dev / non-production environment.
- **Scaffolding by the implementing agent** (`testing.ownership`: `scaffolding`, `reset_endpoint`, `test_users` → `code`): `Api.Framework.Tests` exists; Playwright + playwright-bdd and the e2e folder exist at `testing.e2e.nextjs.path`; the reset endpoint works (master as `testdata-admin`, and a batch seed unit for every key in the plan); every persona in the plan is defined.
- Migrations are applied to the test database (the master reset refuses while any are pending) and every persona's password env var is set (human owner).
- Gate: anything missing → mark the affected rows **Waiting** / **Blocked** with the reason and owner: `code` (implementing agent) for scaffolding, reset endpoint, batch keys and personas; human owner for environment, database and secrets. Add each to `testing.blockers`. Do not build the missing piece yourself. Carry on with what can run. Expect the first runs to be blocked: there is no test environment yet.

### 4. Write tests

- Unit: `skills/write-api-unit-tests/SKILL.md` (in the existing test project only).
- E2E: `skills/write-e2e-tests/SKILL.md` (in the existing e2e folder only).
- Gate: `checklists/api-unit-test-checklist.md` and `checklists/e2e-checklist.md` pass, E1 (no front-end mocks) above all.

### 5. Run and report — `skills/run-tests-and-report/SKILL.md`

- Run unit tests, then e2e tests against the real stack, in this order: **master reset once** (global setup) → each scenario's **batch reset first** → its steps.
- Write `tests/TEST-<feature>-<n>-report.md` (`n` = the new `testing.round`) and append to `tests/test-log.md`.
- Gate: every plan row has a status (Pass / Fail / Blocked / Waiting / Not automated) and evidence.

### 6. Finish: update `testing`, message the reviewing agent

- Update `handoff.md` `testing` only: `status` (`passed` | `failed` | `blocked`), `round`, `test_fix_cycle` (as set at pick-up; not changed here), `plan`, `report`, `summary`, `results` keyed by `<ticket>/S<n>`, `blockers`, `updated_at`, `updated_by: test-bot`.
- **Check your edits** (`AGENT-BRIEF.md` → Shared editing rules): every file you changed (`handoff.md` `testing`, `tests/`, test code) was hash-checked before writing, is unchanged outside the edited region, still parses, is UTF-8 without a BOM and keeps its line endings. The feature folder is inside `ai-planning-framework/`, so run `py tools/check.py` from `ai-planning-framework/`. Send the message below when it ends `RESULT: PASS`. If it fails on a file you wrote (for example an encoding or line-ending problem under `tests/`), fix it and re-run first; if it fails on a file you did not write, leave it alone, record the file and its owner in `testing.blockers` and the report, and still send the message. Never run `--update-golden`: golden files are updated only by the planning agent (both points confirmed by the planning agent, 27/10/2026).
- Message **the reviewing agent only** (`agents.review.name`) with the feature path, the `handoff.md` path and the report path. That is the `test-report` trigger for the test review.
- Do **not** message the implementing agent for a normal completion, failures included: the reviewing agent routes them (`testing.defect_routing`: code defects → implementing agent, stage `changes-requested`; test defects → you, stage stays `in-review`).
- The other message: tickets without explicit scenario IDs go to the planning agent.
- A run that ends `failed` with `test_fix_cycle` at 5: say "test-fix limit reached (5)" at the top of the report; the reviewing agent escalates to the human owner instead of routing it back.
- Never change the front matter, `stage`, `owner`, `pickup`, `review`, `approvals`, `implementation` or History.

## How the reviewing agent uses the report (test review)

For reference; the reviewing agent's own rules are in `ai-review-framework` (`skills/review-tests/SKILL.md`) and `../handoff/README.md` → Testing alongside review.

| Report status | Review status | Severity guide (`checklists/severity.md`) |
|---|---|---|
| Pass (unit and / or e2e) | **Tested** | — |
| Fail | **Untested** until fixed; finding with the report's evidence, routed as a code defect or a test defect | Major when the change claims that scenario, or the rule is mandatory, uniqueness or persistence; otherwise Minor |
| Blocked / Waiting (no scaffolding, batch key, persona, environment, or scenario IDs not frozen) | Recorded as "Tests blocked: <reason>". Final approval is withheld (`testing.blocked_tests_allow_approval: false`); the stage stays `in-review` and the owner is the human owner | — |
| E2E scenario without a first-step reset | Test defect | Major (suggested) |
| Not automated (with reason), for a scenario the change claims | **Untested** | Major test defect; test verdict request-changes |
| E2E test uses a front-end mock | Test defect | Major (suggested) |

## Test-fix rounds

Fixing failing tests has its own cap (Neil, 08/10/2026 19:19 BST), separate from the 3 code-review rounds.

| Rule | Detail |
|---|---|
| One round | One failed run routed back for fixing: code defect → implementing agent, or test defect → testing agent. A run counts once, even with both kinds of defect |
| Counter | `handoff.md` `testing.test_fix_cycle` (starts at 0), kept by the testing agent: +1 when it starts the re-run that follows a routed-back failure (stage 1, with `status: running`), so it always equals the fix rounds used |
| Cap | `testing.max_test_fix_cycles` = 5. When a test review would route failures back again with the counter at 5, the **reviewing agent** escalates: `owner: human` (stage `changes-requested`), reason in `blockers` and History, asks Neil. The testing agent never starts a sixth fix re-run; if asked for one, it does not run, adds the blocker "test-fix limit reached (5)" and messages the reviewing agent and the human owner |
| Not rounds | `passed` runs, `blocked` runs, re-runs caused only by a code-review Request changes |
| Separate cap | `testing.failures_count_toward_review_cycles: false`: test-fix rounds never count toward `handoff.max_review_cycles` (3) |

## Checklist

- [ ] Picked up by setting `testing.status: running` (nothing else in `handoff.md`)
- [ ] Every explicitly numbered scenario in every linked ticket is in the test plan with a tag; tickets without explicit IDs are Blocked and raised with the planning agent
- [ ] No test asserts something the tickets, specs or decisions do not say
- [ ] Prerequisites checked; blocked rows have a reason and an owner (`code` or human owner); nothing built that the implementing agent owns
- [ ] Unit tests follow the active API's rule; boundary-only mocks
- [ ] E2E tests: real UI + real API + dedicated PostgreSQL test database; master reset once per run; every scenario resets its own batch data first; no front-end mocks
- [ ] Personas are `<feature>-<role>`; real-person names in tickets flagged to the planning agent
- [ ] Report and log written; failures carry trace / output paths
- [ ] `handoff.md` `testing` updated, including `test_fix_cycle`; nothing else in `handoff.md` touched
- [ ] Test-fix cap respected: `test_fix_cycle` +1 only when starting a fix re-run; no sixth fix re-run started
- [ ] Shared editing rules followed: hashes recorded and re-checked, targeted edits, UTF-8 without a BOM, line endings kept; `py tools/check.py` ended `RESULT: PASS` before the message, or its only failures are in files test-bot did not write, recorded as blockers with their owner; `--update-golden` never run
- [ ] Reviewing agent messaged by `name` (and only the reviewing agent, apart from scenario-ID blockers to the planning agent, and the human owner only if a sixth fix re-run was asked for)
- [ ] No production code, test-data module (reset endpoint, batches, personas), spec, ticket, config or `.env*` touched
