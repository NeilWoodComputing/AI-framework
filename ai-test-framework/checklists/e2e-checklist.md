# Checklist — functional e2e tests

Rules: `skills/write-e2e-tests/SKILL.md`.

## Hard rules

- [ ] **E1 No front-end mocks.** The test drives the real front end against the real running API and the real test database. No `page.route` / `context.route` handlers that fulfil, abort or alter requests; no `routeFromHAR`; no MSW or service-worker mocks; no stubbed `fetch` / XHR; no faked sign-in, permission or token responses; no `*.mockdata.ts` / `*.mocks.ts` feeding the UI. (Observing with `waitForResponse` is fine.) **Any breach fails the run.**
- [ ] **E5 Reset first, every scenario.** The first step of every scenario is `Given the test data is "{feature}.{batch}.{state}"` with a key owned by this batch. No Background step creates data or signs in before it. No scenario relies on data or persona state left by another scenario, batch or run.
- [ ] **E15 Dedicated test environment.** Runs against the Test API on `<api_framework_test>`; never a shared dev / non-production API or database.

## Traceability

- [ ] E2 Feature tagged `@T-<DOMAIN>-NNN`; each scenario tagged `@T-<DOMAIN>-NNN/S<n>`
- [ ] E3 Scenario text, values and messages match the ticket; real people's names replaced by role personas only where the spec allows, and the ticket flagged to the planning agent
- [ ] E4 Every e2e row in `tests/test-plan.md` has exactly one scenario, and vice versa

## Data and identity

- [ ] E6 Ids come from the reset response; none typed into the test
- [ ] E7 Personas are `<feature>-<role>`; they sign in through the real sign-in endpoint; passwords from `E2E_<FEATURE>_<ROLE>_PASSWORD`; no password literals anywhere
- [ ] E8 Permission scenarios use a persona that really lacks / holds the permission (for example `animals-viewer`, `animals-tester`)
- [ ] E9 Batches with overlapping footprints are serialised
- [ ] E16 The suite's global setup runs the master reset once as `testdata-admin` before any worker; scenarios never call the master reset

## Robustness

- [ ] E10 Selectors use `tid` (`data-tid="…"` on Next.js); values match the specs
- [ ] E11 Waits are on real UI state or real responses; no fixed sleeps
- [ ] E12 Relative dates and time zones handled as the scenario and decisions say
- [ ] E13 Trace and screenshot on failure enabled; reports written
- [ ] E14 Shared steps reused from `features/common/` before writing new ones
