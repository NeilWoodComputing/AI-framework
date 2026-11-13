# Skill: write-e2e-tests

Functional end-to-end tests: the real front end in a real browser, against the real running API.Framework on the dedicated PostgreSQL test database `<api_framework_test>`.

**Who does what** (`testing.ownership`):

- **The implementing agent** (`code`) creates the **scaffolding**: the e2e folder at `testing.e2e.nextjs.path` with its own `package.json`, Playwright + playwright-bdd, `playwright.config.ts`, the global setup that runs the master reset, the shared fixtures and helpers (`helpers/*`, `support/personas.ts`, `features/common/fixtures.ts`, `features/common/test-data.steps.ts`), plus the **reset endpoint** and the **test personas** in API.Framework.
- **The testing agent** (`testing`) writes **test code only** inside that folder: one `.feature` file per batch with one scenario per explicit `<ticket>/S<n>`, its batch step files, and reusable steps under `features/common/` where the scaffolding leaves room for them. Then it runs them.
- **Missing scaffolding, reset endpoint, batch key or persona?** Mark the affected rows **Waiting** or **Blocked** with owner `code` (the implementing agent), add it to `handoff.md` `testing.blockers`, and carry on with what can run. Do not create the folder, the Playwright set-up, the endpoint or the personas yourself.

## Stack

- Playwright + playwright-bdd (Gherkin), TypeScript; the Angular framework uses `@playwright/test ^1.56.1`, `playwright-bdd ^8.5.0`.
- `npm test` = `npx bddgen && npx playwright test`; reporters `list`, `cucumberReporter('html')` → `cucumber-report/index.html`, Playwright `html`.
- `baseURL` from `BASE_URL` (Test UI), API from `API_URL` (Test API), `trace: 'retain-on-failure'`, `screenshot: 'only-on-failure'`, chromium, `grep: /^(?!.*@skip)/`, one retry in CI only.
- **Global setup** (scaffolded by the implementing agent) runs the master reset once per run (`templates/e2e-feature.md`): it truncates all app data and runs every seed unit. Command: `testing.e2e.nextjs.command`.
- Location for UI.NextJs.Framework: config key `testing.e2e.nextjs.path`, with its own `package.json`. The value is still the placeholder `<ai-code-framework/ui/UI.NextJs.Framework/e2e>` and **the folder does not exist yet**; the implementing agent scaffolds it, and the placeholder is confirmed once it does. Until then, every e2e row is **Waiting — e2e scaffolding not created yet**, owner `code`.

## Layout

Scaffolding (implementing agent) vs test code (testing agent) is marked on the right.

```text
e2e/
  playwright.config.ts          ← globalSetup: ./global-setup.ts                      [code]
  global-setup.ts               ← master reset as testdata-admin, once                [code]
  features/
    common/fixtures.ts          ← createBdd over an extended test; exports Given/When/Then/Before/After  [code]
    common/test-data.steps.ts   ← Given the test data is "{feature}.{batch}.{state}"   [code]
    common/*.steps.ts           ← reusable steps (forms, navigation, dialogs, grid, notifications)  [testing]
    {area}/{feature}/
      {Batch}.feature           ← one batch = one feature file, owns its reset keys   [testing]
      {batch}.steps.ts          ← batch-only steps                                    [testing]
  helpers/                      ← all [code]
    config.ts                   ← BASE_URL / API_URL
    selectors.ts                ← el(page, tid)
    authentication.ts           ← signInAs(page, request, persona) via API.Framework's real sign-in
    test-data.ts                ← resetMaster(), resetScenario(key, persona)
    wait-for-response.ts        ← observe real responses
  support/personas.ts           ← persona('<feature>-<role>'); passwords from env vars only  [code]
```

## Rules

1. **Scenarios come from the tickets, by explicit ID.** Copy the Given / When / Then text, values and messages; tag the feature `@T-<DOMAIN>-NNN` and each scenario `@T-<DOMAIN>-NNN/S<n>`, where `S<n>` is the ID in the ticket heading `### Scenario: S<n> — <title>` (`testing.scenario_ids: explicit`), never its position. Scenarios in a ticket without explicit IDs are Blocked (planning agent) and get no `.feature` scenario yet. Where a ticket names a real person, use the role persona the plan maps it to and keep the ticket flag.
2. **No front-end mocks (hard rule).** No `page.route`, `context.route`, `route.fulfill`, `route.abort`, `route.continue` with altered data, `routeFromHAR`, MSW, service-worker mocks, stubbed `fetch` / `XMLHttpRequest`, or faked auth / permission responses. Do not port the Angular framework's `grid-api-mocking.ts`, `entity-crud-mocking.ts`, `auth-state-permissions-mock.ts`, `http-401-interceptor-e2e.ts` or `*.mockdata.ts` / `*.mocks.ts`. Allowed: `page.waitForResponse`, `page.on('request' | 'response')`, and the `request` fixture.
3. **Reset first, every scenario (hard rule).** The first step of every scenario is `Given the test data is "{feature}.{batch}.{state}"`, using a key owned by its batch (feature file). It calls `POST {API_URL}/TestData/Reset/{key}` with the key header **and** a token for one of the feature's personas. Background sections must not create data or sign in. No scenario relies on data or persona state left by another; use the ids the reset returns.
4. **Master reset only in global setup.** Once per run, as `testdata-admin`, before workers start. Never from a scenario.
5. **Role personas.** Sign in through API.Framework's real sign-in endpoint as `<feature>-<role>` personas (`animals-tester`, `animals-viewer`, …). Passwords from `E2E_<FEATURE>_<ROLE>_PASSWORD`; emails `<feature>-<role>@<e2e.test>`. Permission scenarios use a persona that really lacks or holds the permission.
6. **Assert what the scenario says.** UI text and messages exactly; then the persisted outcome through the real API (`GET` after save). Columns the API does not expose go to the paired unit test.
7. **Selectors by `tid`.** Next.js renders `data-tid="{value}"` (`style/nextjs-components.mdc` → Test IDs), so `el(page, tid)` = `page.locator('[data-tid="' + tid + '"]')`; Angular uses `[data-tid-{tid}]`. Values must match the specs.
8. **Wait on real events.** `expect(locator).toBeVisible()` / `waitForResponse` on the real call; no fixed sleeps.
9. **Batches and parallelism.** Scenarios within a batch are independent (each resets first). Batches whose footprints overlap (for example the same unique Name in a global table) run serially: mark them serial and keep them out of parallel workers.
10. **Dates and time zones.** Dates safely in the past for "before today"; compute "today" in the browser's time zone when the scenario is about it. Browser emulation (`test.use({ timezoneId: 'Europe/London' })`) is allowed; it changes the browser, not API traffic.
11. **API e2e.** Scenarios with no UI step run in the same suite through the `request` fixture against the real API, signed in as a persona, with the same reset-first step and tags.
12. **Environment.** `BASE_URL` / `API_URL` point at the Test UI and Test API only. Never a shared dev / non-production URL.

Skeleton: `templates/e2e-feature.md`. Checklist: `checklists/e2e-checklist.md`.
