# Checklist — test-data reset endpoint and personas

Rules: `skills/add-test-data-reset/SKILL.md`. A failed item here is a security / data-integrity problem (proposed **Blocker** in review).

## Where and when

- [ ] R1 Lives in API.Framework only (none in Unity.API)
- [ ] R2 Registered only when `TestData:Enabled` is `true` and the environment is in `TestData:AllowedEnvironments` (`Test` / `E2E`)
- [ ] R3 Start-up fails if `Enabled` is `true` in `Production` (hard-coded)
- [ ] R4 `appsettings.json` has no `TestData` section; `appsettings.Production.json` sets `Enabled: false`
- [ ] R5 Disabled → controller removed from application parts → `404`; start-up seed does not run

## Database

- [ ] R6 Every write (start-up seed, master, batch) first checks the provider is Npgsql and the database name equals `TestData:RequiredDatabase` (`<api_framework_test>`)
- [ ] R7 The test database is dedicated to API.Framework; never a shared dev / non-production database
- [ ] R8 Connection string comes only from the user-level env var `APIFW_TEST_ConnectionStrings__LoginConnection` (JWT key `APIFW_TEST_Jwt__Secret`), read only when `ASPNETCORE_ENVIRONMENT=Test`; never read, printed or committed by agents
- [ ] R8a Runtime test user has DML + `TRUNCATE` only (no `DROP`, `CREATE`, `CREATEDB`); migrations applied with a separate owner connection; `InitialisationSettings:MigrateDatabase=false` for the runtime test API

## Access

- [ ] R9 `X-Test-Data-Key` checked with a fixed-time compare against `E2E_TEST_DATA_KEY`; missing env var disables the endpoint
- [ ] R10 Caller must also be signed in (valid JWT) as a seeded test persona; `401` / `403` otherwise
- [ ] R11 Master reset only for `testdata-admin`, and only when `TestData:AllowMasterReset` is `true`
- [ ] R12 Key, passwords and connection string never logged, returned or put in docs

## Scope

- [ ] R13 Master runs in one transaction: refuses if migrations are pending; `TRUNCATE` only the EF model's tables (`RESTART IDENTITY CASCADE`, identifiers from the model), never `auth.__ef_migrations_history`; no DDL of any kind; then every seed unit in dependency order
- [ ] R13a `baseline.migration-seed` recreates exactly the model's `HasData` rows (count checked per table)
- [ ] R14 Batch reset deletes only its declared footprint (fixed GUIDs, its natural keys written by its feature's personas); no delete without the footprint filter
- [ ] R15 Keys follow `{feature}.{batch}.{state}`; each batch owns its keys; overlapping footprints run serially
- [ ] R15a One set of seed units: every unit has a key, declared dependencies, an idempotent upsert `Seed` and a footprint-only `Clear`; batch units declare a default state; the master and granular resets use the same units
- [ ] R16 Idempotent: same key twice → same state; fixed GUIDs and values; unknown key → `404`; response returns seeded ids

## Personas

- [ ] R17 Personas named `<feature>-<role>`; roles describe permissions, not people; no real names or emails
- [ ] R18 Seeded only by the `personas.<feature>` seed units (start-up, master, batch re-assert) into the test tenant of the test database; never via migrations / `HasData`
- [ ] R19 Each persona has its own `<feature>-<role>` group with exactly its role's permissions; no new permissions created for tests
- [ ] R20 Passwords from `E2E_<FEATURE>_<ROLE>_PASSWORD`; missing variable → persona skipped, variable NAME logged

## Proof

- [ ] R21 Unit tests in `Api.Framework.Tests` prove R2, R3, R6, R9, R10, R11, R13 (truncate list), R13a, R14, R15a (order, cycles) and R16
- [ ] R22 Production pipeline / deployment check confirms `TestData:Enabled` is off
