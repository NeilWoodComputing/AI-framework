# Example — Unity.UI.Framework e2e as the reference (and where it mocks)

Studied 2026-10-08 from `D:\Users\nwood01\Documents\Candc\ui\Unity.UI.Framework` (Angular). Near-identical copies: `Candc\ui\Unity.UI.Framework - Copy` and `ai-framework\ai-code-framework\ui\UI.Angular.Framework\e2e`. Read-only study; nothing in it was changed.

## Stack

| Item | Value (file) |
|---|---|
| Runner | Playwright `^1.56.1` + playwright-bdd `^8.5.0`, TypeScript 5.9 (`e2e/package.json`) |
| Scripts | `npm test` = `npx bddgen && npx playwright test`; `test:ui`, `test:visual` (`--grep @visual-regression`), `watch:pw`, `watch:bdd`, `report` |
| Config | `e2e/playwright.config.ts`: features `features/**/*.feature` minus `unity-services`; steps `features/common/*.ts`, `features/common/**/*.ts`, `features/**/*.ts`; `grep: /^(?!.*@skip)/`; retries 1 in CI; workers from `E2E_WORKERS` (CI 4, local 8); timeouts 120 s local / 240 s CI; `trace: 'retain-on-failure'`, `screenshot: 'only-on-failure'`; chromium; viewport 1280×720 |
| Reports | `list`, `cucumberReporter('html')` → `cucumber-report/index.html`, Playwright `html` |
| URLs | `BASE_URL` (default `https://localhost:4200`), `API_URL` (default `https://localhost:7104/v2`) in `e2e/helpers/config.ts` |
| CI | `azure-pipelines.yml` stage "Playwright E2E (pre-deploy gate)": serves the app on 4200, scopes tests from the git diff with `pipelines/compute-e2e-scope.ps1`, installs chromium, runs bddgen + playwright. Legacy `e2e/.github/workflows/test.yaml` (node 18, `npm test`) |
| Unit tests | Jasmine + Karma, co-located `{name}.spec.ts` (separate from e2e) |

## Copy these patterns

| Pattern | Where | Why |
|---|---|---|
| `createBdd` over an extended `test`; shared `Given/When/Then/Before/After` exported from one file | `e2e/features/common/fixtures.ts` | One import for all steps; fixtures for selectors, personas, navigation |
| Page guard on every page | `fixtures.ts` + `helpers/guard-playwright-waits.ts` | Avoids unhandled rejections in teardown |
| `tid` selectors | `helpers/selectors.ts` (`el(page, tid)` → `[data-tid-${tid}]`) | Stable selectors from the specs. **Next.js renders `data-tid="…"`**, so the selector changes |
| API sign-in, cookies on the context | `helpers/authentication.ts` (`signInAs(page, request, persona)` → `POST {api}/Authorisation/SignIn`, sets `JWT` / `rT` cookies, domain from `BASE_URL`) | Fast, real sign-in. API.Framework's sign-in and token storage differ: adapt |
| Authenticated API helpers | `helpers/api-requests.ts` (`authenticatedGet/Post/Put/Delete`, Bearer from the JWT cookie) | Assert persisted state through the real API |
| Waiting on real responses | `helpers/wait-for-response.ts` (`waitForApiResponse`, shared timeout) | Observes, does not intercept |
| Reusable steps | `features/common/forms.steps.ts`, `navigation.steps.ts`, `dialogs.steps.ts`, `form-validation.steps.ts`, `notifications.steps.ts`, `grid/*` (columns, pagination, filters, actions) | Write fewer feature-specific steps |
| Folder per feature | `features/{domain}/{feature}/{Feature}.feature` + `{feature}.steps.ts` | Mirrors the app |
| Independent scenarios, `@skip`, scoped CI runs | `.cursor/rules/testing/angular-e2e-testing.mdc` → Test organisation; `pipelines/compute-e2e-scope.ps1` | Reliable, fast pipelines |
| Real-backend features | `features/security/SignInFlow.feature`, `RememberMe.feature`, `TokenRefresh.feature`, `contact/ContactUs.feature`, `market-messenger/dip-dashboard/DipDashboard.feature` | No `@mock` tag (but see below: some of their steps still use routes) |

## Drop these — front-end mocks (forbidden here)

The suite is built around browser-side API mocking. Neil should know the scale:

- **Rules that mandate it:** `.cursor/rules/testing/angular-e2e-testing.mdc` line 126 "Prefer `page.route()` mocking over hitting live APIs for grid/list tests"; lines 98–122 (grid mocking with `setupGridTestingBefore`, `entity-crud-mocking.ts` for create / update / delete); `angular-testing-framework.mdc` lines 51–52 ("Use Playwright `page.route()` for API mocking", "Use `entity-crud-mocking.ts`"); `.cursor/skills/unity-e2e/SKILL.md` steps 4 and 6 ("Mock create, update, and delete with `e2e/helpers/entity-crud-mocking.ts`").
- **Scale:** 61 of 75 `.feature` files carry `@mock…` tags (122 distinct tags; most used `@mockDevelopmentCrud` ×45, `@mockMessageAuditReport` ×34, `@mockScheduledReports` ×30, `@mockSchedules` ×28, `@mockProjectsGrid` ×21). 42 `.ts` files call `.route(`; the heaviest is `features/scheduled-reporting/schedule-reports/scheduled-reports.steps.ts` (33 calls).
- **Mocking helpers:** `features/common/grid/grid-api-mocking.ts` (`setupGridTestingBefore`, `setupGridApiMocking`, `route.fulfill` with generated rows), `helpers/entity-crud-mocking.ts` (`setupEntityCrudMocking`), `helpers/auth-state-permissions-mock.ts` (rewrites the sign-in response's permissions via `context.route`), `helpers/http-401-interceptor-e2e.ts`, `helpers/forgot-password-api-e2e.ts`, `helpers/billing-export-e2e.ts` (all call `.route(`), mock data such as `helpers/service-plan-action-grid-mocks.ts`, plus every `*.mockdata.ts` / `*.mocks.ts` (for example `settings/organisation-management.mockdata.ts`, `market-messenger/message-audit-report/message-audit-report.mocks.ts`, `unity-services/appointments/mocks/coverage-areas.mocks.ts`).
- **Even "real" features route some calls:** `features/contact/contact.steps.ts`, `features/security/forgot-password-update.steps.ts` and `features/common/grid/grid-columns.steps.ts` call `.route(`.
- **No data reset:** mocks use fake ids (for example `e2e-development-edit-target`); there is no seed / reset endpoint, so the suite never proves persistence.

## Other things to flag

- **Hard-coded credential:** `e2e/support/personas.ts` contains a system-admin password in source. Its value is deliberately not reproduced here. Recommend moving persona credentials to env vars (as `templates/e2e-feature.md` does) and rotating that password.
- **Shared environment in CI:** the pipeline's `e2eDefaultApiUrl` points at a shared non-production dev API, not a dedicated test database, which is only safe because the tests mock. Real-backend tests need a dedicated environment and database.

## Adapting it for this framework

Keep the structure, fixtures, selectors, sign-in, response waits, reusable steps and CI scoping. Replace every grid / CRUD / permission mock with: a `Given the test data is "{key}"` reset step, real personas with real permissions, and assertions through the real API. Visual-regression and Storybook tests are a separate concern (no Storybook in UI.NextJs.Framework).
