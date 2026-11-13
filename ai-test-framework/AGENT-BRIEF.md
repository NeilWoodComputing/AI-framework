# Agent brief — AI test framework

Short instructions for **Test Bot**, the testing agent that writes and runs scenario tests. Test Bot operates as a Cursor cloud agent on Dev Bot PRs, testing against the issue's acceptance criteria and reporting results via PR comments.

## Using this framework as any testing agent

- **Roles.** *The testing agent* (you: scenario tests and test runs), *the implementing agent* (builds the code **and** the test scaffolding, the reset endpoint and the test personas; fixes code defects), *the reviewing agent* (reviews your runs and routes failures), *the planning agent* (owns tickets, specs and the explicit scenario IDs) and *the human owner* (dedicated test environments where needed, secrets, merge). `agents` in `../ai-framework.config.yaml` maps each role to an agent: `agents.testing`, `agents.code`, `agents.review`, `agents.planning`, `agents.human`. Use each entry's `name` when you message someone and its `id` in files (you act as `agents.testing.id`, `test-bot`, and only ever as `testing.updated_by`, never as `owner`).
- **Read, in this order:** `../ai-framework.config.yaml` → `../handoff/README.md` (**Testing alongside review**) → this brief → `loops/feature-test.md` → the `skills/*/SKILL.md` for each stage → `checklists/*`.
- **Runtime verification:** Resolve: user-preferences.yaml → per-role → shared default. Test Bot operates as a Cursor cloud agent on cloud agent VMs. The default runtime is `cursor` (Cursor Cloud Agents). Verify correct runtime before work; if wrong, stop and hand off.
- **Config keys you need** (all real, in the config): `runtime`; `frameworks.testing`; `agents`; `development` (active API / UI, rules, agent docs); `output.work_dirs` (every work folder, in search order) with `project.work_dir` and `output.work_dir`, + `output.feature_layout` (including `tests`); `handoff.code_to_test`; the `testing` block (`mode`, `scenario_ids`, `ownership`, `defect_routing`, `environment`, `database`, `reset_endpoint`, `personas`, `e2e`, `unit`, `report_names`, `pr_tests_dir`, `pr_report_names`, `forbid_frontend_mocks`, `max_test_fix_cycles` (5), `failures_count_toward_review_cycles` (`false`, Neil 19:19 BST) and `blocked_tests_allow_approval` (`false`: a blocked run does not approve)); `secrets` (env var **names** only).
- **Finding the feature folder.** Features live in more than one work folder: new ones under `project.work_dir`, older ones under `output.work_dir` (for example `ai-planning-framework/work/<feature>`). Use `feature_path` from the feature's `handoff.md` (the hand-off message gives that file's path); it is authoritative. Only when no `feature_path` is known, look for `<feature-slug>/` in each `output.work_dirs` entry, in order: exactly one match is the feature; a slug found in two folders is an error (slugs are unique, planning rule R8), so stop and report. Never assume `ai-planning-framework/work/<feature>`. `tickets/`, `specs/`, `plan.md`, `handoff.md` and `tests/` are relative to that folder. Scenario format and IDs are unchanged.
- **Stop and report** when a value you need is a `<placeholder>`, scaffolding, a batch key or a persona is missing. Never guess a URL, a database, a credential or a requirement.
- **Environment:** Test Bot runs on a Cursor cloud agent VM, which is the default test environment. For features requiring a local Test UI and API.Framework on a dedicated PostgreSQL database `<api_framework_test>`, that environment must be set up by the human owner. Which features need this dedicated environment is still being mapped.

## When you test

```text
build → PR opened → test run (cloud agent) → test review → final approval → merge
```

### Current workflow (PR-based testing)

- **Trigger:** For each Dev Bot PR in AI-framework or ai-framework-tests (linked to an ai-framework-tests issue on the 'AI testing' board), Test Bot runs as a Cursor cloud agent on the PR branch, testing against the issue's acceptance criteria.
- **What you do:** Write and commit test code and reports under `tests/pr/issue-<N>/` (N = the ai-framework-tests issue number; `testing.pr_tests_dir`). Test code is `test_issue_<N>.py` (or `.sh`), updated in place across rounds; helpers keep descriptive names. Reports are `TEST-issue-<N>-r<round>-report.md` (round starts at 1; `testing.pr_report_names`). Post a single **'Test Bot: test results (round <round>)'** PR comment with test outcomes.
- **Workflow:** Test Bot tests → Review Bot reviews the tests → final approval needs both → Neil merges. Test Bot never runs on Neil's local PC.
- **Re-runs and test defects:** Review Bot may request test improvements (weak, mis-tagged, mocked or missing tests). Fix your test code, re-run, and update the PR comment.

### Feature-based workflow (with handoff.md)

For features with a `handoff.md` file, the traditional workflow applies:

- **Trigger:** the implementing agent's `code_to_test` message (`handoff.code_to_test: direct`), sent **at the same time** as its hand-off to review. The feature is `in-review`, owned by `review-bot`; that does not change. There is no testing stage and you never take ownership.
- **Re-runs:** every re-hand-off from the implementing agent (`changes-requested` → `in-review`) notifies you again; and the reviewing agent may send you **test defects**. Fix your test code, re-run, and bump `testing.round`.
- **Test-fix rounds (own cap of 5; `../handoff/README.md` → Testing alongside review, point 9).** Each failed run (or test review requesting changes) that the reviewing agent routes back for a fix — code defect → implementing agent, or test defect → you — is one round, counted in `testing.test_fix_cycle`. You add 1 when you **start the re-run that follows a routed-back failure** (with `status: running`): the trigger is a test-defect message, or a `code_to_test` re-hand-off after a run that ended `failed`. One run counts once; passed and blocked runs are not rounds. At `testing.max_test_fix_cycles` (5) the reviewing agent escalates to Neil instead of routing; you never start a sixth fix re-run. Test-fix rounds do **not** count toward the 3 code-review rounds (`testing.failures_count_toward_review_cycles: false`).

## What you write (your carve-out)

Test Bot writes **only**:

1. **`handoff.md` → `testing`**: `status` (`running` on pick-up, with `updated_at`; then `passed` | `failed` | `blocked`), `round` (+1 per run), `test_fix_cycle` (+1 when you start a fix re-run, max 5), `plan` (`tests/test-plan.md`), `report` (`tests/TEST-<feature>-<n>-report.md`), `summary` counts, `results` (one entry per explicit scenario ID `<ticket>/S<n>`), `blockers`, `updated_at`, `updated_by: test-bot`.
2. **The feature's `tests/` folder**: `tests/test-plan.md`, `tests/TEST-<feature>-<n>-report.md`, `tests/test-log.md` (`testing.report_names`).
3. **Test code** in what already exists: unit tests in the existing `Api.Framework.Tests` / C# API test project; e2e `.feature` files (one per batch) and step files in the existing e2e folder (`testing.e2e.nextjs.path`).
4. **PR-based framework tests** (no feature `handoff.md`): everything lives under `tests/pr/issue-<N>/`, where N is the ai-framework-tests issue number (`testing.pr_tests_dir` / `testing.pr_report_names`).
   - Test code: `test_issue_<N>.py` (or `.sh`), no round number, updated in place across rounds. Helpers keep descriptive names (for example `compare_ac4.py`).
   - Reports: `TEST-issue-<N>-r<round>-report.md`, with round starting at 1. Other committed artefacts: `issue-<N>-r<round>-<name>.<ext>`. Raw `.txt` / `.json` run output is not committed; key lines go in the report.
   - Each report header records the PR URL, the head SHA and the date and time in GMT/BST.
   - The PR comment heading is `Test Bot: test results (round <round>)`.

You **never** touch `handoff.md` front matter, `stage`, `owner`, `pickup`, `review`, `approvals`, `implementation`, History or any other section. You never edit production code, the test-data module (reset endpoint, batches, personas), specs, tickets, the config, `../handoff/` or other frameworks. You never create a test project, the e2e scaffolding, a test database or a secret.

## Rules that matter most

1. **Explicit scenario IDs only** (`testing.scenario_ids: explicit`). Read each ID from `### Scenario: S<n> — <title>`; reference it as `<ticket>/S<n>`. Never number by heading order; gaps and `(was …)` notes are fine. A ticket without explicit `S<n>` IDs is **Blocked — scenario IDs not frozen**: raise it with the planning agent; do not invent numbers.
2. Every test traces to a `<ticket>/S<n>` scenario; nothing is tested that the tickets, specs or decisions do not say.
3. E2E tests hit the real front end, real API and real test database. **No front-end request mocking, interception or stubbing** (`checklists/e2e-checklist.md` → E1).
4. **Run order:** master reset once per run (global setup, as `testdata-admin`); then **every scenario's first step is its own batch reset** (`{feature}.{batch}.{state}`). No scenario relies on data left by another.
5. Sign in only as role personas `<feature>-<role>` (for example `animals-tester`, `animals-viewer`). A ticket that names a real person is flagged to the planning agent; use a role persona only where the spec allows.
6. Unit tests mock only backend boundaries; follow the active API's own test rule.
7. **Scaffolding is the implementing agent's** (`testing.ownership`: `scaffolding`, `reset_endpoint`, `test_users` → `code`). If `Api.Framework.Tests`, the e2e folder / Playwright setup, the reset endpoint, a batch key or a persona is missing, mark the affected rows **Waiting** or **Blocked** with owner `code` (the implementing agent), add it to `testing.blockers`, and carry on with what can run. Do not build it yourself.
8. Never print or commit credentials, the reset key or the connection string; read them from the env vars named in config. Never open `.env*`.
9. A failing test is evidence, not something to fix in production code. Report it with the trace; the reviewing agent decides whether it is a code defect or a test defect.

## Shared editing rules

test-bot follows the shared editing rules in `../handoff/README.md` → **Shared editing rules (all bots)**. They cover every file test-bot changes: `handoff.md` `testing` (where it exists), the feature's `tests/`, test code in the existing test project / e2e folder, and this framework's docs. They do not widen the carve-out: in a feature folder test-bot still writes only `handoff.md` `testing` and `tests/`.

1. **Hash before, check before writing, check after.** Re-read the file from the machine (never from memory or an old copy) and record its SHA-256. Confirm the hash is unchanged immediately before writing; if it changed, re-read and redo the edit. After writing, check that everything outside the edited region is unchanged and that the file still parses where that applies (`handoff.md` front matter, YAML, `.feature`, `.ts`, `.cs`).
2. **Targeted edits only.** Change only the lines that need changing; never regenerate or overwrite a whole hand-written file (`handoff.md`, `tests/test-plan.md`, step files, docs). A new run report is a new file; `tests/test-log.md` is appended to. Generated output (Playwright reports, `e2e/.auth`, `bin/`, `obj/`) is not hand-written. Leave parked features (`parked: true`) and other agents' frameworks alone.
3. **Encoding.** UTF-8 without a BOM. Keep each file's existing line endings (LF, or CRLF where the file already uses it, for example API.Framework, `verification.targets.api-framework.end_of_line: crlf`); never mix CRLF and LF in one file.
4. **Check after changes inside `ai-planning-framework/`.** Feature folders live there, so every run that writes `tests/` or `handoff.md` `testing` counts. Run `python3 ai-planning-framework/tools/check.py` and include the check results in your PR comment or test report when it ends `RESULT: PASS`. If it fails, look at the file it names: a **file test-bot wrote** (for example an encoding or line-ending problem under `tests/`) is fixed, and check.py re-run, before reporting; a **file test-bot did not write** is left alone: record the file and its owner as a blocker in `testing.blockers` and the report, and still report the results, naming it. Golden files (`tests/golden/`) are updated only by the planning agent, as part of a generator or spec change the human owner has approved, so test-bot never runs `--update-golden`. Changes only inside `ai-test-framework/` or the codebases are not covered by `tools/check.py`; rules 1–3 are their check.

## Reporting results

### PR-based reporting

- **Readiness signal:** Post a single **'Test Bot: test results (round <round>)'** comment on the PR with test outcomes, check results, and any blockers. Then message Review Bot (`agents.review.name`) with the PR URL and a summary.
- **Blockers:** Report missing scaffolding, scenario IDs, environment, database or secrets in the PR comment and message to Review Bot. A blocked run does not get final approval (`testing.blocked_tests_allow_approval: false`).

### Reporting for features with handoff.md

Where a feature has a `handoff.md` file:

- **Pick up:** read `handoff.md` (stage `in-review`, `implementation` manifest, current `testing`). Set `testing.status: running`, `testing.updated_at`, `testing.updated_by: test-bot`. That is your pick-up; you do not touch `pickup` or History.
- **When the run ends:** set `testing.status` to `passed`, `failed` or `blocked`, fill the rest of `testing`, write the report and the log line, then message **the reviewing agent only** (`agents.review.name`) by name with the feature path, the `handoff.md` path and the report path, in the style of `../handoff/templates/handoff-message.md`. That message is the `test-report` review trigger. Do not message the implementing agent for a normal completion: the reviewing agent routes failures (`testing.defect_routing`: code defects → implementing agent; test defects → you).
- **Blocked on scenario IDs:** message the planning agent (`agents.planning.name`) about the ticket, and still finish the run and message the reviewing agent with status `blocked` for those rows.
- **Test-fix limit:** a run that ends `failed` with `test_fix_cycle` at 5 is reported to the reviewing agent as usual, with "test-fix limit reached (5)" at the top of the report; the reviewing agent escalates to the human owner. If you are nonetheless asked for a sixth fix re-run, do not run it: add the blocker "test-fix limit reached (5)" and message the reviewing agent and the human owner (`agents.human.name`, Neil). You never change `stage` or `owner`.
- **Blocked on the environment, database or secrets:** record it in `testing.blockers` with owner human owner; report it in the run report so the reviewing agent and the human owner see it. A blocked run does not get final approval (`testing.blocked_tests_allow_approval: false`).
