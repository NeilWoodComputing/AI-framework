# Skill: add-test-data-reset

The test-data mechanism: **one set of composable, idempotent seed units**, ordered by dependency and registered per feature. The **master reset** clears all data and runs every unit in order; each **granular reset** clears only its batch's rows and runs that batch's units. Both seed the **role-based test personas**.

**Who does what** (`testing.ownership`):

- **The implementing agent** (`code`) builds all of it: the reset endpoint (`reset_endpoint: code`), the seed units and batches, and the test personas (`test_users: code`), plus the unit tests that prove them. It is API code that only exists in the Test environment, delivered in the normal build and listed in `handoff.md` `implementation`.
- **The testing agent** (`testing`) only **calls** it (master reset in global setup, a batch key as each scenario's first step) and **reports** what is missing. It lists the batches, keys, footprints and personas it needs in `tests/test-plan.md`; it never writes the endpoint, a seed unit or a persona.
- **Missing endpoint, batch key or persona?** The affected rows are **Waiting** or **Blocked** with owner `code` (the implementing agent), recorded in `handoff.md` `testing.blockers`. Config: `testing.reset_endpoint.*`, `testing.personas.*`.

> Decided by Neil, 08/10/2026: API.Framework only (not Unity.API); dedicated PostgreSQL test database; key **and** signed-in test persona; master + per-batch resets; role-based personas; master reset = **TRUNCATE + reseed, no schema or database drop** (17:27 BST). Nothing has been added to a codebase yet; expect the first test runs to be Blocked until the implementing agent adds it and the human owner sets up the environment.

## Database and provider

- **Database:** a dedicated PostgreSQL database for API.Framework only, `<api_framework_test>`, on the local PostgreSQL server, reached through the user-level env var `APIFW_TEST_ConnectionStrings__LoginConnection` (the API's `LoginConnection`; the JWT key is `APIFW_TEST_Jwt__Secret`), both read only when `ASPNETCORE_ENVIRONMENT=Test` (the prefix is stripped; the unprefixed names are no longer used). Set up by the human owner.
- **Schema:** built only by API.Framework's EF Core migrations (`Api.Framework.Data/Migrations`, `20260923152501_InitialLogin` → latest, currently `20261008150221_AddAnimals`). The reset never creates, alters or drops schema objects. When migrations change, they are applied to the test database first (see Database rights), then the master reset is run.
- **Database rights:** the API's runtime test user needs only `USAGE` on the `auth` and `creatures` schemas and `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` on their tables. No `DROP`, `CREATE` or `CREATEDB`. API.Framework has no identity columns or sequences today (uuid keys), so `RESTART IDENTITY` resets nothing yet; if sequences are added later, the user also needs rights on them (confirm when that happens). Applying migrations needs DDL, so it is done with a separate owner / migration connection, or by the human owner, with `InitialisationSettings:MigrateDatabase=false` for the runtime test API.
- **Provider findings (read-only, 08/10/2026):**
  - API.Framework is PostgreSQL-only: `Npgsql.EntityFrameworkCore.PostgreSQL` 10.0.3 with EF Core 10.0.9; `UseNpgsql` in `Program.cs` and in `LoginDbContextFactory`; history table **`auth.__ef_migrations_history`**. No SQL Server code or packages.
  - The migrations are PostgreSQL-specific (`uuid`, `timestamp with time zone`, `jsonb`, `'[]'::jsonb` defaults, filtered unique indexes such as `ix_animals_normalized_name_active`, schemas `auth` and `creatures`).
  - `DefaultUserSeeder` runs only in `Development`, so a Test database has **no default user**; the test personas are the only users.
  - The design-time factory (`LoginDbContextFactory`) reads `appsettings.json`, `appsettings.Development.json`, then environment variables, and with `ASPNETCORE_ENVIRONMENT=Test` also the `APIFW_TEST_`-prefixed ones. `dotnet ef database update` hits the test database **only** when `ASPNETCORE_ENVIRONMENT=Test` is set in that shell (so `APIFW_TEST_ConnectionStrings__LoginConnection` is read); otherwise it migrates whatever the dev settings point at.

## Migration seed data (`HasData`) — decision

Migrations insert seed rows from `LoginDbContext` `HasData` calls into `roles`, `permissions`, `permission_groups`, `permission_group_permissions`, `tenants`, `features`, `tenant_features`, `catalogue_items`, `reference_data_types` and `reference_data_items`. The only raw SQL in a migration (`20260923173144_ManageUsersAndGroups`) back-fills names on existing users and adds no rows.

**Decision: truncate those tables too, and recreate their rows with the `baseline.migration-seed` unit, generated from the current EF model's seed data (`IEntityType.GetSeedData`) in foreign-key order.**

- Excluding them does not work: `TRUNCATE … CASCADE` on `tenants` or `users` cascades into `permission_groups`, `user_permission_groups` and the other dependants anyway, and test edits to seeded rows (a changed group, a deleted reference-data item) would survive the reset.
- The EF model is the same source the migrations' `InsertData` was generated from, so the rows match the migrations without duplicating them by hand.
- A unit test checks that the unit inserts exactly the model's seed rows, and the master reset reports the counts per table.

## Seed units

One unit = one named, idempotent piece of data with explicit dependencies. Features register their own units; the module orders all of them by dependency (ties broken by key, so the order is fixed).

| Unit key | Depends on | Clears | Seeds |
|---|---|---|---|
| `baseline.migration-seed` | — | (only ever run after a truncate) | Every `HasData` row from the EF model, `ON CONFLICT DO NOTHING` |
| `baseline.test-tenant` | `baseline.migration-seed` | — | The test tenant `<e2e-test-tenant>` (fixed GUID) |
| `personas.testdata` | `baseline.test-tenant` | — | `testdata-admin` (upsert) |
| `personas.<feature>` | `baseline.test-tenant` | — | The feature's personas and their groups (upsert; resets password, display name, permissions) |
| `<feature>.<batch>` | `personas.<feature>` | Its footprint only | One of its states (`{feature}.{batch}.{state}`); declares a **default state** (usually `empty`) used by the master reset |

Rules: every `Seed` is an upsert by fixed keys (running it twice changes nothing); every `Clear` deletes only the unit's own rows; units never call each other directly; adding a feature means registering its persona unit and batch units, nothing else.

## Run order

| When | Call | Who |
|---|---|---|
| Migrations changed | Apply them to `<api_framework_test>` (owner connection or human owner), then the master reset | Human owner |
| API start in Test | **Start-up seed:** `baseline.test-tenant` and every `personas.*` unit (upserts; no truncate) so `testdata-admin` can sign in | API.Framework |
| Start of a full suite run (Playwright global setup) | `POST TestData/Reset/master` once, before any worker starts | Test runner as `testdata-admin` |
| Dirty database | Master reset on its own (`npm run test:reset`), nothing else running | Human owner or testing agent |
| First step of **every** scenario | `POST TestData/Reset/{feature}.{batch}.{state}` | The scenario, as a test persona |
| After a scenario (optional) | The batch's `.empty` key | The scenario; never relied on |

A partial run (one feature or scenario) may skip the master reset: the granular resets are enough by design. Run the master when in doubt.

## Master reset contract

| Item | Rule |
|---|---|
| Route | `POST TestData/Reset/master` (literal segment, wins over `{scenarioKey}`; `master` is never a batch key) |
| Does | In **one transaction**: 1) guards; 2) refuses if migrations are pending (`GetPendingMigrations()`: "apply migrations first"); 3) `TRUNCATE` every table of the EF model (all of `auth` and `creatures`, names taken from the model, quoted) `RESTART IDENTITY CASCADE` in one statement; `auth.__ef_migrations_history` is not in the model, so it is never touched; 4) runs **all** seed units in dependency order: `baseline.migration-seed` → `baseline.test-tenant` → `personas.*` → every batch's default state. Commit. |
| Never | `DROP` or `CREATE` anything; truncate tables outside the model; touch another database |
| Caller | Key header **and** signed in as `testdata-admin`. Persona ids are fixed GUIDs, so the caller's token stays valid after the reseed; refresh tokens do not survive. |
| Flags | Also needs `TestData:AllowMasterReset` = `true` (default `false`) |
| Concurrency | Only when nothing else is running against the API (global setup, before workers) |
| Response | `200` `{ "scenario": "master", "truncatedTables": <n>, "units": ["baseline.migration-seed", …], "seedRows": { "<table>": <n> } }` |

## Granular (batch) reset contract

| Item | Rule |
|---|---|
| Route | `POST TestData/Reset/{scenarioKey}` |
| Key | `{feature}.{batch}.{state}`, lowercase kebab-case: `animals.form.bessie-exists`. A **batch** is one feature file (or describe block / scenario group); it owns its keys. |
| Does | In one transaction: 1) guards; 2) checks the baseline is present (test tenant exists), else `409` "run the master reset"; 3) the batch unit's `Clear` (its footprint only); 4) `Seed` of `personas.<feature>` (re-assert); 5) `Seed` of the requested state. The same units the master runs. |
| Footprint | Each batch declares what it may touch: its fixed GUIDs, the natural keys its scenarios create (for example Names "Bessie", "Ziggy"), written by its feature's personas. Nothing outside it is touched. |
| Every scenario | Calls its key as its **first step**. No Background step creates data or signs in before it. No scenario relies on data or persona state left by another. |
| Idempotent | Same key twice → same state; fixed GUIDs and values. |
| Overlap | Batches whose footprints overlap (for example the same unique Name in a global table) run serially. |
| Caller | Key header **and** signed in as any test persona of the feature (or `testdata-admin`). |
| Response | `200` `{ "scenario": "<key>", "ids": { "bessie": "<guid>", … } }`; `404` unknown key or endpoint disabled; `401` not signed in; `403` wrong key or not a test persona; `409` baseline missing. |

## Test personas

- **Naming:** `<feature>-<role>`, where the role says what the user may do, not who they are: `animals-tester` (has `animals_write`), `animals-viewer` (signed in, no animals permission), `animals-usermanager` (`user_management_read` + `user_management_write`, no `animals_write`). The suite-level admin is `testdata-admin` (may call the master reset; holds no product permissions).
- **Defined in code** per feature (`{Area}TestPersonas.cs`, registered as the `personas.<feature>` unit): role, display name (or none, when a scenario needs the "no display name" path), exact permissions, fixed user GUID.
- **Email:** `<feature>-<role>@<e2e.test>` (reserved, non-routable domain).
- **Password:** from env var `E2E_<FEATURE>_<ROLE>_PASSWORD` (upper case, `-` → `_`): `E2E_ANIMALS_TESTER_PASSWORD`, `E2E_TESTDATA_ADMIN_PASSWORD`. The API and the test runner read the same variables; the human owner sets them. Missing variable → that persona is skipped and its scenarios fail with a clear message.
- **Seeded** only by the seed units (start-up seed, master reset, and re-asserted by each batch reset of the feature): users in the test tenant, each in its own group `<feature>-<role>` with exactly the role's permissions (existing permissions such as `animals_write`; no new permissions for tests).
- **Never:** real people's names or emails; migrations or `HasData` (that would reach production); groups shared with non-test users.

## Safety (all required)

1. **Off by default.** Registered only when `TestData:Enabled` is `true` **and** the environment is in `TestData:AllowedEnvironments` (`Test`, or `E2E`). `appsettings.json` has no `TestData` section; `appsettings.Production.json` sets `Enabled: false`.
2. **Production refuses.** Start-up fails if `TestData:Enabled` is `true` in `Production`. Hard-coded.
3. **Invisible when off.** Controller removed from the application parts, so every route returns `404`; the start-up seed does not run.
4. **Named PostgreSQL test database only.** Before any write, the provider must be Npgsql and the database name must equal `TestData:RequiredDatabase` (`<api_framework_test>`); otherwise refuse. Applies to the start-up seed, master and batch resets.
5. **Secret key.** `X-Test-Data-Key` compared with a fixed-time compare against the env var `E2E_TEST_DATA_KEY`. Missing variable → endpoint disabled. Never logged, returned or committed.
6. **Signed-in test persona.** Valid JWT whose user is a seeded test persona (in the test tenant, email in the persona domain, id in the persona registry). Master: `testdata-admin` only.
7. **Scoped.** Master: truncates only tables in the EF model (never the history table, never another database), no DDL. Batch: only its footprint. Never delete without the scope filter.
8. **Least privilege.** The runtime test user has DML + `TRUNCATE` only; schema changes go through migrations with a separate connection.
9. **Audit.** Log key, caller persona, unit list and counts; never the key, passwords or the connection string.
10. **Proven by tests** in `Api.Framework.Tests` (see `templates/reset-handler.md` §6).

## Adding a feature's test data (implementing agent only)

The testing agent does not do these steps; it reads the result and marks rows Waiting / Blocked (owner `code`) until they are done.

1. Read the test plan's batches, keys, footprints, default states and personas.
2. Add `Api.Framework.Services/TestData/{Area}/{Area}TestPersonas.cs` (the `personas.<feature>` unit) and `{Area}{Batch}Batch.cs` (one unit per batch: states, default state, footprint, dependencies).
3. Register them in the test-data registration (only called when enabled).
4. Add unit tests: footprint filter, idempotency (`Seed` twice), dependency order.
5. List the new keys and personas in `handoff.md` (`implementation.api`).

Skeletons: `templates/reset-handler.md`. Checklist: `checklists/reset-endpoint-safety-checklist.md`.
