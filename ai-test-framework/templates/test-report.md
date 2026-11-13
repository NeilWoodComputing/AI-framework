# Test report — <feature> — run <n>

| Field | Value |
|-------|-------|
| Run | <n> (`handoff.md` `testing.round`) · <YYYY-MM-DD HH:mm GMT \| BST> · <agents.testing.id> |
| Why this run | <first `code_to_test` \| re-hand-off after <code \| test> defects \| re-run after a blocker cleared: <what cleared it>> |
| Test-fix round | <test_fix_cycle> of <testing.max_test_fix_cycles> (5) · <"first run / not a fix re-run" \| "fix re-run after <code \| test> defects" \| "limit reached — the reviewing agent escalates to the human owner"> |
| Environment | Test · UI <ui_base_url> · API.Framework <api_base_url> · PostgreSQL DB <api_framework_test> (dedicated) |
| Safety gate | Pre-run check, once per run, before global setup's master reset: <PASS \| FAIL> at <HH:mm GMT \| BST>, database `<api_framework_test>` on `<host:port>`, read from the env var named in `testing.database.connection_env` (database name and host:port only; never the connection string). It checks the variable the Test API was started from, not the running process |
| Batch resets | <n> batch resets (one `Given the test data is "<key>"` per executed scenario, see E5) + <1> master reset, all `POST <API_URL>/TestData/Reset/…` from `e2e/helpers/test-data.ts` to the gated Test API (`API_URL` <http://localhost:5188>, launch profile Test, pid <n>); <0> reset calls from anywhere else (search for `TestData/Reset`). The API also refuses every master and batch reset unless its own connection is PostgreSQL database `TestData:RequiredDatabase` (`TestDataGuard.EnsureTestDatabase`); the endpoint exists only with `TestData:Enabled`, the environment in `TestData:AllowedEnvironments` (`Test`) and `E2E_TEST_DATA_KEY` set |
| Master reset | <OK at HH:mm GMT \| BST · tables truncated n · seed units n · HasData rows n \| failed: reason (e.g. pending migrations)> |
| Personas used | <animals-tester, animals-viewer, …> |
| Code under test | <branch / head commit, or "not under git" + handoff updated_at> |
| Commands | <dotnet test …> · <npx bddgen && npx playwright test --grep …> |
| Result | <pass> Pass · <fail> Fail · <blocked> Blocked · <waiting> Waiting · <n> Not automated |
| Layers | Unit <passed>/<total> · e2e <passed>/<total> (<n> setup + <n> scenarios) · <n> skipped (Playwright status skipped: `@fixme`, `test.skip`, `test.fixme`) · <n> `@skip` scenarios filtered out by the config grep and absent from the counts (list them) · <n> flaky · <n> retries · special tags in use: <none \| `@only` / `@fail` / `@retries:N` with scenarios> |
| Password scan | <n> hits (count only; never print a value) for the env vars in `secrets.test_persona_password_env_pattern` and the Test JWT secret, in <playwright-report, test-results, logs, trx>; `e2e/.auth` is not opened |
| E5 reset-first scan | Clean \| <scenarios without a first-step reset> |
| E1 front-end mock scan | Clean \| <hits with file:line> |

Times: Europe/London local time, labelled GMT or BST for that date (BST from the last Sunday in March to the last Sunday in October), or given with the offset, e.g. `13:46 GMT (+00:00)`.

## Summary

<2–4 sentences: what was run, the headline result, what blocks the rest.>

## Results by ticket

| Ticket | Owner | Scenarios | Pass | Fail | Blocked | Waiting | Not automated |
|--------|-------|-----------|------|------|---------|---------|---------------|
| T-<DOMAIN>-NNN | <owner id> | <n> | <n> | <n> | <n> | <n> | <n> |
| **Total** | | **<n>** | **<n>** | **<n>** | **<n>** | **<n>** | **<n>** |

## Results by scenario

| Scenario | Layer | Test | Status | Evidence |
|----------|-------|------|--------|----------|
| T-<DOMAIN>-NNN/S1 | E2E | `@T-<DOMAIN>-NNN/S1` | Pass \| Fail \| Blocked \| Waiting \| Not automated | <assertion message, file:line, trace path> |

Status `Pass` may carry a sub-note: **Pass (partial)** means the test proves the scenario but one part of its Then is not covered this run (say which part and why, e.g. a deferred build); **Pass (on intent)** means the outcome meets the scenario's intent but differs from its literal Then (quote the difference and raise it in Flags). Both are recorded as `result: pass` in `handoff.md` `testing.results`, with `note` explaining. Anything less is Fail, Blocked, Waiting or Not automated.

## Failures

### <scenario> — <one line>

- Expected (from the ticket): <…>
- Actual: <…>
- Evidence: <trace / screenshot / test output path>
- Classification: <code \| test \| environment> (the testing agent's reading; an attempt that is not the result of record is labelled as such)
- Routed by: the reviewing agent (`testing.defect_routing`: code defect → implementing agent; test defect → testing agent)

## Blocked

| Scenario(s) | Reason | Owner |
|-------------|--------|-------|
| <…> | <missing scaffolding / reset endpoint / batch key / persona / environment / database / secret / scenario IDs not frozen / test-fix limit reached> | <`code` (implementing agent) \| human owner \| planning agent> |

## Not automated

| Scenario(s) | Reason | Covered elsewhere |
|-------------|--------|-------------------|
| <…> | <why it cannot be automated in this stack> | <e.g. the reviewing agent's full review, a read-only code check, or none> |

## Test Bot changes this run

Test code and test docs only.

| File | Change |
|------|--------|
| <repo-relative path> (<new \| changed>, <LF \| CRLF>, no BOM) | <what changed and which `<ticket>/S<n>` or finding it is for> |

## For the reviewing agent (test review, `review-tests`)

- Tested: <list> · Failing: <list> · Blocked: <list> · Not automated: <list>
