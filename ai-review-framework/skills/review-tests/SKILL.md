# Skill: review-tests

Check that the PR's tests cover the spec's validation rules and the tickets' Given / When / Then scenarios, and suggest the ones that are missing.

## Purpose

A scenario is only really delivered when a test would catch it breaking. This stage lists what is tested, what is not, and proposes concrete tests in the codebase's own conventions.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | Validation rules from specs, scenario list, active API / UI |
| `diff` + `files` | Yes | Review scope from `gather-pr-context`: PR diff + files, or on the direct route the plan-scope files read whole (or local diff): test projects and folders (manifest `tests` entries on the plan scope) |
| `stage_4_results` | Yes | GWT coverage rows (to keep statuses consistent) |

## Where tests live

| Codebase | Location and conventions (source) |
|----------|-----------------------------------|
| Unity.API | `Unity.API.Tests` (CI runs only this project). Controllers mirror `Unity.API.Tests/Controllers/V2/...`; mappers in `Unity.API.Tests/Mapping`; schema binding and constraints in `JsonSchemaValidation`; import in `DataImport`. xUnit + Moq; mock downstream `*RestService`; no `WebApplicationFactory` for a normal BFF action; include `CancellationToken` in Moq setups; one behaviour per `[Fact]`; name `{Action}_{Condition}_{Expected}`; create-request shape tests include every property. (`.cursor/rules/unity-api-testing.mdc`, `.cursor/skills/unity-api-tests/SKILL.md`) |
| API.Framework | `ai-code-framework/api/API.Framework/Api.Framework.Tests`, run with `testing.unit.api-framework` (`dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release`). Conventions: `ai-code-framework/api/API.Framework/CLAUDE.md` and its `.cursor/rules` |
| UI.NextJs.Framework | `package.json` scripts: `lint` (`eslint .`), `typecheck` (`tsc --noEmit`), `test` (`vitest run`) and `build` (`next build`). Unit tests run with `npm test`. E2E scenarios live in `e2e/` (Playwright + playwright-bdd, `testing.e2e.nextjs`) and are written and run by the testing agent. |
| UI.Angular.Framework | Unit tests per `.cursor/rules/testing/angular-tests.mdc`, `angular-testing-framework.mdc`, `angular-testing-best-practices.mdc`; E2E with Playwright + Cucumber per `angular-e2e-testing.mdc` (Given / When / Then scenarios map directly to Cucumber features). |

## Steps

1. List every spec validation rule (mandatory, min / max, format, custom rule, uniqueness) and every scenario `<ticket>/S<n>`.
2. For each, find a test that asserts it. Record test class / method or spec file and line.
3. Check test quality on what exists: asserts the outcome named in the Then (status code and envelope, exact message text, persisted column values), not only that no exception was thrown.
4. For gaps, suggest a test: name, file location, arrange / act / assert in one line each. For Unity.API use `{Action}_{Condition}_{Expected}`, for example `Create_NameMissing_ReturnsNameIsRequired`.
5. **Required run.** Run the unit suite for the active API and the unit suite for the active UI, and record each command under **Checks run**. Run only the active API's command from `testing.unit`, not the other API's. This is not optional, and a result of "not run" is never a pass. Lint, typecheck and build stay on the UI checklist; they are not this gate. Project-local tools only, never a root `npx` (`AGENT-BRIEF.md` **Running checks safely**). Never change code or tests to make them pass.

   ```powershell
   # testing.unit.unity-api, from the Unity.API project
   dotnet test Unity.API.Tests/Unity.API.Tests.csproj --configuration Release
   # testing.unit.api-framework, from ai-code-framework/api/API.Framework
   dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release
   ```

   ```bash
   # nextjs, from ai-code-framework/ui/UI.NextJs.Framework
   npm test
   ```

   What the result means:

   - **pass** — the suite executed. Scenario tests the testing agent has not written yet are still listed Untested below; this run does not clear them.
   - **fail** — Major finding, area Tests. The code verdict is Request changes and goes to the implementing agent.
   - **test project missing** (the active API test project, or the active UI's test script, is not on disk) — Major finding. Scaffolding belongs to the implementing agent.
   - **tool or machine cannot start the command** — record `not run - <reason>`. That is not a code defect. Final approval is withheld (stage 11): stage stays `in-review`, owner `agents.human.id`.

6. Raise findings using `checklists/severity.md` for tests that already exist in the change: no test for a mandatory, uniqueness or persistence rule the change claims to deliver → Major; any other missing test at this stage → Minor; test naming / structure → Nit. A Minor here does not mean the scenario is accepted. The test review below refuses approval until every scenario the change claims has a real test that was executed and asserts the Then. A UI checklist with no unit command is recorded as `not run - no UI unit command` and withholds final approval in the same way as a tool that cannot start.

## Test review (`test-report` trigger)

Runs when the testing agent reports a finished run (option B: `testing.mode: alongside-review`, `testing.test_review: true`). Ready when `handoff.md` `testing.status` is `passed`, `failed` or `blocked` and `testing.report` and `testing.round` point at the new report. Read-only: never edit `handoff.md` `testing:` or `tests/`.

1. **Find the files.** Report: `testing.report`, else `<feature_path>/tests/TEST-<feature>-<n>-report.md` (`n` = `testing.round`). Plan: `tests/test-plan.md`. Log: `tests/test-log.md`.
2. **Explicit IDs.** Every explicit scenario (`### Scenario: S<n>` in the ticket) has a real test tagged with its explicit ID: `@T-<DOMAIN>-NNN/S<n>` (e2e) or `[Trait("Scenario", "T-<DOMAIN>-NNN/S<n>")]` (xUnit), never an ID taken from heading order. A test carries two scenario tags only if it fully proves both.
3. **Assertions** check the scenario's Then.
4. **Skipped and not-run tags** (the testing agent's `skills/run-tests-and-report/SKILL.md` step 4; the report's Layers row). `@skip` is filtered out by the config grep and never counted, so the Layers row must list those scenarios by name; `@fixme`, `test.skip` and `test.fixme` run as Playwright status skipped and count as skipped. Flag any of these on a scenario reported as Pass; any `@only` (or `test.only`, which silently narrows the run) or `@fail` (or `test.fail`, which inverts the result); any `@retries:N`, or the config's `retries: 1` when `CI` is set, that hides a flaky test; and any `@skip` the plan does not record as Blocked or Waiting with an owner. Nothing weakened to get a pass.
5. **E1 and E5.** No front-end mocks (E1), and every e2e scenario starts with its batch reset (E5). A failure on either is a test defect, suggested **Major**.
6. **Unit tests** mock only backend boundaries.
7. **Not automated and Blocked / Waiting rows** each have a reason and an owner. Flaky tests are reported as flaky, not retried until they pass.
8. **Safety gate and batch resets** (the report's Safety gate and Batch resets rows). The safety gate is a pre-run check, once per run, before global setup's master reset, not before every reset: its result and time, database `api_framework_test` and host:port (never the connection string). Per-reset protection is evidenced by the Batch resets row: the number of batch resets (one `Given the test data is "<key>"` per executed scenario) plus the master reset, the `API_URL` and launch profile (Test) they used, 0 reset calls from anywhere else (search for `TestData/Reset`), and the API's own `TestDataGuard.EnsureTestDatabase` check against `TestData:RequiredDatabase` (`api_framework_test`). Check both rows are present and consistent with each other.
9. **Secrets.** No secrets or passwords in reports, traces or logs: check the report's password-scan count only, and never open `e2e/.auth`.
10. **Counts agree** across the report header, **Results by ticket**, `testing.summary`, `testing.results` and the `tests/test-log.md` row, including the per-scenario notes. Times in the report and the log row are Europe/London local time, labelled GMT or BST for that date, or given with the offset (for example `13:46 GMT (+00:00)`).
11. **Test-fix rounds.** `testing.test_fix_cycle` (max `testing.max_test_fix_cycles`, 5; separate from `review.cycle`) matches the fix rounds routed back so far. At 5 with failures still to route back, escalate to the human owner instead (`../handoff/README.md` Testing alongside review, point 9).
12. **Pass (partial) and Pass (on intent)** notes are read, and the part not covered or the difference from the literal Then is quoted in the report's **Test review**.
13. **Adequate tests, then the verdict.** Every explicit scenario the change claims (not Deferred, and not on the ticket's out-of-scope list) needs a test tagged with its explicit ID that asserts the Then, and that test needs a Pass in this run. Missing, Weak, Not automated, or not executed is a test defect at Major: `review.test_verdict` is `request-changes`, the stage stays `in-review`, and it is routed to the testing agent. Do not use Approve with comments to accept that gap.
14. **Verdict and routing.** Record `review.test_verdict` (`approve`, `request-changes`, or `blocked-noted`) separately from `review.code_verdict`. `testing.status: blocked` is `blocked-noted` with "Tests blocked: <reason>" in the report. It does not approve: `testing.blocked_tests_allow_approval` is `false`, so `review.verdict` stays unset, the stage stays `in-review`, and the owner is `agents.human.id`. Route failures by cause (`testing.defect_routing`): code defects to the implementing agent (stage `changes-requested`), test defects to the testing agent (stage stays `in-review`). Final approval needs both verdicts (`testing.final_approval_requires: [code_review, test_review]`) and a test run that is not blocked. Fill the report's **Test review** section and append a round to the review log.

## Outputs

- Tests section of the report: table of rule / scenario → test reference → status (**Tested** / **Weak** / **Untested**), plus the Execution table (each required unit command and its result)
- Suggested tests list
- Test / build run results, always, including a `not run` reason
- Test review (`test-report` trigger): `review.test_verdict` and the report's **Test review** section

## Quality checks

- [ ] Every validation rule and scenario has a test status
- [ ] The active API and UI unit commands were run, or the report says `not run` with a reason and final approval is withheld
- [ ] A failed unit run or a missing test project is a Major finding for the implementing agent
- [ ] Suggested tests follow the codebase's naming and location
- [ ] Statuses agree with stage 4 coverage
- [ ] Test review: every claimed scenario was executed and asserts the Then, or the test verdict is request-changes
- [ ] A blocked run does not set a final approval
