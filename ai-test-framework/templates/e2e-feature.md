# Template — e2e batch, steps and global setup (Playwright + playwright-bdd)

Structure copied from the Angular framework (`e2e/features/common/fixtures.ts`, `helpers/selectors.ts`, `helpers/authentication.ts`, `helpers/config.ts`), with **no route mocks**, a **master reset in global setup** and a **reset first in every scenario**. Paths are relative to the UI's e2e folder. API.Framework's sign-in route and response shape are placeholders: check `AuthorisationController` before use.

## `features/{area}/{feature}/{Batch}.feature` — one batch, its own keys

```gherkin
@T-<DOMAIN>-NNN
Feature: <ticket title> — <batch name>
  # Batch "<feature>.<batch>": keys <feature>.<batch>.<state>; footprint in tests/test-plan.md
  # No Background that creates data or signs in.

  @T-<DOMAIN>-NNN/S1
  Scenario: <scenario title copied from the ticket>
    Given the test data is "<feature>.<batch>.<state>"
    And I am signed in as "<feature>-<role>"
    When <When line copied from the ticket>
    Then <Then line copied from the ticket>

  @T-<DOMAIN>-NNN/S2
  Scenario: <next scenario>
    Given the test data is "<feature>.<batch>.<other-state>"
    And I am signed in as "<feature>-<role>"
    ...
```

## `support/personas.ts` — role personas, passwords from env vars

```ts
export interface Credentials { username: string; password: string }

const emailDomain = '<e2e.test>';

/** persona('animals-tester') → animals-tester@<domain>, password from E2E_ANIMALS_TESTER_PASSWORD. */
export function persona(name: string): Credentials {
  const envVar = `E2E_${name.toUpperCase().replace(/-/g, '_')}_PASSWORD`;
  const password = process.env[envVar];
  if (!password) throw new Error(`Persona password env var ${envVar} is not set`); // never print the value
  return { username: `${name}@${emailDomain}`, password };
}
```

## `helpers/test-data.ts` — key header + signed-in persona

```ts
import { APIRequestContext, expect } from '@playwright/test';
import { getApiUrl } from './config';
import { persona } from '../support/personas';

const keyEnv = 'E2E_TEST_DATA_KEY'; // env var NAME from testing.reset_endpoint.key_env

async function tokenFor(request: APIRequestContext, name: string): Promise<string> {
  const { username, password } = persona(name);
  const response = await request.post(`${getApiUrl()}/<Authorisation/SignIn>`, {
    data: { <emailField>: username, password },
  });
  expect(response.status(), `sign in ${name}`).toBe(200);
  return (await response.json()).<token>;
}

async function reset(request: APIRequestContext, path: string, as: string) {
  const secret = process.env[keyEnv];
  if (!secret) throw new Error(`Reset key env var ${keyEnv} is not set`);
  const token = await tokenFor(request, as);
  const response = await request.post(`${getApiUrl()}/TestData/Reset/${path}`, {
    headers: { 'X-Test-Data-Key': secret, Authorization: `Bearer ${token}` },
  });
  expect(response.status(), `reset ${path}`).toBe(200);
  return response.json();
}

/** Once per run, global setup only. */
export const resetMaster = (request: APIRequestContext) => reset(request, 'master', 'testdata-admin');

/** First step of every scenario; signs in as the batch feature's tester persona. */
export async function resetScenario(request: APIRequestContext, key: string): Promise<Record<string, string>> {
  const feature = key.split('.')[0];
  return (await reset(request, key, `${feature}-tester`)).ids;
}
```

## `global-setup.ts` (referenced from `playwright.config.ts` → `globalSetup`)

```ts
import { request } from '@playwright/test';
import { resetMaster } from './helpers/test-data';

export default async function globalSetup() {
  const context = await request.newContext({ ignoreHTTPSErrors: true });
  try {
    await resetMaster(context);   // TRUNCATE all app tables, then every seed unit: HasData rows, tenant, personas, batch defaults
  } finally {
    await context.dispose();
  }
}
```

Add `"test:reset": "<node script calling resetMaster>"` to `package.json` for recovering a dirty database by hand.

## `features/common/test-data.steps.ts`

```ts
import { Given } from './fixtures';
import { resetScenario } from '../../helpers/test-data';

export const resetIds = new WeakMap<object, Record<string, string>>();

Given('the test data is {string}', async ({ page, request }, key: string) => {
  resetIds.set(page, await resetScenario(request, key));
});
```

## `features/{area}/{feature}/{batch}.steps.ts`

```ts
import { expect } from '@playwright/test';
import { When, Then } from '../../common/fixtures';

When('I save the form', async ({ page }) => {
  const saved = page.waitForResponse(r => r.url().includes('/Animal') && r.request().method() !== 'GET'); // observe, never fulfil
  await page.locator('[data-tid="save-animal"]').click();   // tid value from the spec
  await saved;
});

Then('I see the validation message {string}', async ({ page }, message: string) => {
  await expect(page.getByText(message, { exact: true })).toBeVisible();
});
```

## Forbidden in these files

`page.route`, `context.route`, `route.fulfill`, `route.abort`, `routeFromHAR`, MSW, `setupGridTestingBefore`, `setupEntityCrudMocking`, `setupAuthStatePermissionsMock`, `*.mockdata.ts` data fed to the UI, password literals, master reset calls outside global setup, scenarios without a first-step reset.
