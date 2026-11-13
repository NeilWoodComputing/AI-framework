# Skill: run-tests-and-report

Run the planned tests against the real stack, classify every scenario, write the report, update `handoff.md` `testing` and message the reviewing agent.

## Steps

1. **Confirm the environment** (`testing.*`; stop on any `<placeholder>` you need): Test UI at `testing.ui_base_url`, API.Framework at `testing.api_base_url` in environment `Test` (or `E2E`), on the dedicated PostgreSQL database `<api_framework_test>`. Never a shared dev / non-production API or database. Do not start, re-point or reconfigure anything the human owner has not set up. Never open `.env*`, never read or print the connection string.
2. **Unit tests** (where the test project exists; commands `testing.unit.*`):

   ```powershell
   dotnet test CSharp.API.Tests/CSharp.API.Tests.csproj --configuration Release --filter "Ticket=T-<DOMAIN>-NNN"
   ```

   ```powershell
   dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release --filter "Ticket=T-<DOMAIN>-NNN"
   ```

   API.Framework's test project is approved (Neil, 08/10/2026) and is the implementing agent's to create (`testing.ownership.scaffolding: code`). If it does not exist yet, mark unit rows **Waiting — test project not created yet**, owner `code`, add it to `testing.blockers`, and run `dotnet build Api.Framework.sln --configuration Release`. Do not create the project.
3. **E2E tests** from the existing e2e folder (`testing.e2e.nextjs.path`; scaffolded by the implementing agent — if it does not exist, every e2e row is **Waiting — e2e scaffolding not created yet**, owner `code`), with `BASE_URL`, `API_URL`, `E2E_TEST_DATA_KEY` and the `E2E_<FEATURE>_<ROLE>_PASSWORD` variables already set by the human owner. Run order: **master reset once** (global setup), then every scenario runs its own **batch reset first**:

   ```bash
   npx bddgen && npx playwright test --grep "@T-<DOMAIN>-"
   ```

   If the database is dirty, run the master reset on its own first (`npm run test:reset`) with nothing else running. If it refuses because migrations are pending, record a blocker for the human owner (apply them to the test database; the runtime test user cannot) in `testing.blockers` and the report.

   **Safety gate and reset coverage.** Run the safety gate once per run, before Playwright starts: it reads the env var named in `testing.database.connection_env` and passes only when the database is `api_framework_test` (print the database name and host:port only). The e2e code has no gate of its own: the master reset (global setup) and every batch reset (`Given the test data is "<key>"`) go through `e2e/helpers/test-data.ts` to `<API_URL>/TestData/Reset/<key>`, and the Test API refuses any reset unless its own connection is `TestData:RequiredDatabase` (`TestDataGuard.EnsureTestDatabase`). In the report's Safety gate and Batch resets rows, record the gate result before the master reset, the number of batch resets, the `API_URL` they used (the gated Test API) and that a search for `TestData/Reset` finds no other caller.

4. **Scan for forbidden mocks** in the e2e folder before trusting a pass: search for `route(`, `routeFromHAR`, `fulfill(`, `msw`, `setupGridTestingBefore`, `setupEntityCrudMocking`, `setupAuthStatePermissionsMock`. Any hit in a functional test fails E1 and is reported. Also check every scenario starts with `Given the test data is` (E5). **Skipped and not-run tags** (playwright-bdd 8.5.1, Playwright 1.56.1; checked in `e2e/playwright.config.ts`, `e2e/features` and `e2e/setup` on 27/10/2026): `@skip` is removed by the config's `grep: /^(?!.*@skip)/` (a CLI `--grep` intersects with it), so it is never run and appears in **no** count; `@fixme` (and `test.fixme`, `test.skip` in code) runs as Playwright status *skipped*, which is the Layers row's "skipped" count; `@only` (or `test.only`) silently narrows the run to the tagged scenarios (the config sets no `forbidOnly`); `@fail` (or `test.fail`) inverts the result, so a failing scenario counts as passed; `@retries:N`, and the config's `retries: 1` when `CI` is set, can turn a failure into a flaky pass. On 27/10/2026 none of these appear in `e2e/features` or `e2e/setup`. List every hit in the report's Layers row. The reviewing agent should flag any of them on a scenario reported as Pass, any `@only`, any `@fail`, and any `@skip` (hidden from the counts) that the plan does not record as Blocked or Waiting with an owner.
5. **Classify each plan row** by its explicit `<ticket>/S<n>`: **Pass**, **Fail** (with message, file:line, trace / screenshot path), **Blocked** / **Waiting** (reason + owner: missing scaffolding, reset endpoint, batch key or persona → `code` (implementing agent); environment, database or secret → human owner; scenario IDs not frozen → planning agent), **Not automated** (reason). A Pass may carry the sub-note **Pass (partial)** (part of the Then not covered this run; say which) or **Pass (on intent)** (meets the intent, not the literal Then; say how); both are `result: pass` in `testing.results`, with `note` explaining.
6. **Write** `tests/TEST-<feature>-<n>-report.md` from `templates/test-report.md` (`n` = the new `handoff.md` `testing.round`, one more than the last run), filling every header row (including Why this run, Safety gate, Batch resets, Layers and Password scan) and every section (Results by ticket, Results by scenario, Failures with a Classification line, Blocked, Not automated, Test Bot changes this run) and append one line to `tests/test-log.md`: `| <n> | <YYYY-MM-DD HH:mm GMT/BST> | <pass>/<fail>/<blocked> | test-fix <test_fix_cycle>/5 | <report path> |`. Times in the report and the log are Europe/London local time, labelled GMT or BST for that date (BST from the last Sunday in March to the last Sunday in October), or given with the offset, e.g. `13:46 GMT (+00:00)`.
7. **Update `handoff.md` → `testing`** (your carve-out; nothing else in the file):
   - `status`: `passed` (every automated row passed), `failed` (any Fail), or `blocked` (no Fail, but rows Blocked / Waiting that stop the run proving the feature);
   - `round`, `plan`, `report`, `summary` (`scenarios`, `passed`, `failed`, `blocked`, `waiting`, `not_automated`);
   - `test_fix_cycle`: leave it as set at pick-up. You add 1 only when you **start** a re-run that follows a routed-back failure (`loops/feature-test.md` stage 1; `../handoff/README.md` → Testing alongside review, point 9). Test-fix rounds do **not** count toward `handoff.max_review_cycles` (`testing.failures_count_toward_review_cycles: false`);
   - `results`: one entry per explicit `<ticket>/S<n>` with `layers`, `tests`, `result`, `note`;
   - `blockers`: each with what is missing and who owns it (`code` / implementing agent, human owner, or planning agent), and when it was raised;
   - `updated_at` (ISO 8601 with offset), `updated_by: test-bot`.
   Never change the front matter, `stage`, `owner`, `pickup`, `review`, `approvals`, `implementation` or History.
   Edit `handoff.md` and `tests/` under the shared editing rules (`AGENT-BRIEF.md` → Shared editing rules): record the SHA-256 when you read, confirm it just before writing, and afterwards check that the rest of the file is unchanged and the front matter still parses. Then run `py tools/check.py` from `ai-planning-framework/` (never with `--update-golden`: golden files are updated only by the planning agent). Go on to step 9 when it ends `RESULT: PASS`. If it fails on a file you wrote (for example an encoding or line-ending problem under `tests/`), fix it and re-run first; if it fails on a file you did not write, leave the file alone, add it and its owner to `testing.blockers` and the report, and still go on to step 9 (confirmed by the planning agent, 27/10/2026).
8. **Test-fix cap** (`testing.max_test_fix_cycles`, 5). If the run ended `failed` and `test_fix_cycle` is 5, put "test-fix limit reached (5) — the reviewing agent escalates to the human owner" at the top of the report and in the Test-fix round field. The reviewing agent then escalates to Neil instead of routing the failures back. If you are later asked for a sixth fix re-run anyway, do not start it: add the blocker "test-fix limit reached (5)" to `testing.blockers` and message the reviewing agent and the human owner (`agents.human.name`).
9. **Message the reviewing agent** (only it, apart from scenario-ID blockers and the step 8 safety net; `agents.review.name`, today Review Bot) by name, with the feature path (`feature_path` in `handoff.md`), the `handoff.md` path and the report path (`../handoff/templates/handoff-message.md` style). This is the `test-report` trigger for the test review. Do not message the implementing agent about failures: the reviewing agent routes code defects to it and test defects back to you (`testing.defect_routing`). Tickets without explicit scenario IDs are raised separately with the planning agent.

## Never

- Change production code, the test-data module (reset endpoint, batches, personas) or assertions to get a pass.
- Create the test project, the e2e scaffolding, the reset endpoint or personas (the implementing agent's).
- Change `stage`, `owner`, `pickup` or History in `handoff.md`, or message anyone but the reviewing agent for a finished run (except the step 8 safety net).
- Start a sixth test-fix re-run, or reset `test_fix_cycle` yourself.
- Retry a failing test until it passes and call it Pass; flaky results are reported as such.
- Paste secrets, tokens or persona passwords into reports or logs.
