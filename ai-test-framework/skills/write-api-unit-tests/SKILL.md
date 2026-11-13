# Skill: write-api-unit-tests

Backend unit tests for the active API.

**Who does what** (`testing.ownership`):

- **The implementing agent** (`code`) creates and maintains the test **project** (scaffolding), and writes the tests that prove its own test-only code (reset endpoint, seed units, personas; `skills/add-test-data-reset/SKILL.md`). It may add other unit tests while building.
- **The testing agent** (`testing`) writes the **scenario** unit tests, one per `<ticket>/S<n>` that needs the unit layer, tagged with that explicit ID, **inside the existing project only**. Test code only: never production code, never a new project, never the project file or solution wiring.
- **Missing project?** Mark the unit rows **Waiting — test project not created yet**, owner `code` (the implementing agent), add it to `handoff.md` `testing.blockers`, and carry on with the e2e layer. Do not create the project yourself.

## Which rules apply

| `development.api.active` | Test project and rules |
|---|---|
| `unity-api` | `Unity.API.Tests` (net10.0; xUnit 2.9.3, Moq 4.20.72, EF Core InMemory + Sqlite). Rule `.cursor/rules/unity-api-testing.mdc`; skill `.cursor/skills/unity-api-tests/SKILL.md`. CI runs `Unity.API.Tests` only. |
| `api-framework` | `Api.Framework.Tests` (xUnit + Moq, like Unity.API). **Approved by Neil on 08/10/2026.** The implementing agent creates the project (`testing.ownership.scaffolding: code`); the testing agent writes the scenario tests in it per this skill. Until it exists, unit rows are **Waiting — test project not created yet** with owner `code`, recorded in `testing.blockers` (no further approval needed). Command: `testing.unit.api-framework`. Required build check stays `dotnet build Api.Framework.sln --configuration Release`. |

### Unity.API conventions (from its rule and skill)

- Folders mirror the code: `Controllers/V1|V2|Shared/...`, `Mapping`, `Validation`, `Authorization`, `JsonSchemaValidation`, `Services`, `DataImport`; helpers in `Helpers/` (`TestDbFactory` for InMemory / Sqlite, `TestAuthConfig`, `TestResponseHelper`).
- Mock downstream `*RestService`; no `WebApplicationFactory` test for a normal BFF action.
- Include `CancellationToken` in Moq setups; one behaviour per `[Fact]`; name `{Action}_{Condition}_{Expected}`.
- Create-request shape tests include every property.
- Examples: `Controllers/V2/Nav/Projects/ProjectControllerDeleteTests`, `Mapping/ProjectApiMapperTests`, `Validation/OrganisationNameUniquenessCheckerTests`, `Authorization/UnityAuthorizationFilterTests` (`OnAuthorization_WhenWriteRequiredAndUserHasReadOnly_ReturnsUnauthorized`).
- Run: `dotnet test Unity.API.Tests/Unity.API.Tests.csproj --configuration Release --filter "Scenario=T-<DOMAIN>-NNN/S<n>"` (or `Ticket=…`).

### API.Framework — `Api.Framework.Tests` (approved 08/10/2026, Neil)

Created by the **implementing agent** (not the testing agent), per `api-framework-testing.mdc` → When a test project is added later. Listed here so the testing agent knows what to expect and can check it exists:

- Beside the other projects (`Api.Framework.Tests/Api.Framework.Tests.csproj`, net10.0), added to `Api.Framework.sln`, referencing `Api.Framework.Services` and `Api.Framework.Data`.
- Packages as Unity.API: xUnit, Moq, `Microsoft.NET.Test.Sdk`, EF Core InMemory.
- Folders mirror the areas (`Animals/AnimalServiceTests.cs`, `Animals/AnimalPoliciesTests.cs`, `TestData/...`); a `Helpers/TestDbFactory` like Unity.API's.
- Prefer service-level tests around `IRecordValidationApi` and area services over full HTTP tests.
- The implementing agent also updates `api-framework-testing.mdc` (it still says there is no test project) with the runner. That rule change and the project are code changes made in the normal build flow, not by this framework.
- Run (`testing.unit.api-framework`): `dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release --filter "Scenario=T-<DOMAIN>-NNN/S<n>"` (or `Ticket=…`).

**Provider caveats (API.Framework is PostgreSQL-only):**

- The model uses PostgreSQL-only features (`jsonb`, `'[]'::jsonb` defaults, filtered unique indexes such as `NOT is_deleted`). EF Core **SQLite** is unlikely to build this schema, so Unity.API's SQLite pattern does not carry over; use EF Core **InMemory** for service tests.
- InMemory does not enforce unique indexes or SQL defaults. Unit-test the service's own pre-save checks (trim, case, soft-deleted rows ignored) and the `IsUniqueViolation` mapping with a constructed exception. Prove the real index and `jsonb` behaviour with API e2e tests on `<api_framework_test>`.
- Model-metadata tests (schema `creatures`, columns, the filtered unique index) can build the real Npgsql model without opening a connection: `new LoginDbContext(new DbContextOptionsBuilder<LoginDbContext>().UseNpgsql("Host=unused").Options).Model`.
- A real-database integration test project is not part of this approval.

## What to unit test

Only what an explicitly numbered scenario (`<ticket>/S<n>`) asks for; tag every scenario test with `[Trait("Ticket", "T-<DOMAIN>-NNN")]` and `[Trait("Scenario", "T-<DOMAIN>-NNN/S<n>")]`. Scenarios in tickets without explicit IDs are Blocked (planning agent) and get no tests yet.

| Area | Assert | Example from a ticket |
|---|---|---|
| Validation rules | Each required / max length / format / date comparison / item-count rule fails with the **exact** spec message, and nothing is written | `Create_NameWhitespace_FailsWithNameIsRequired` |
| Uniqueness | Per organisation / tenant, or global when the plan says so; trimmed, case-insensitive where specified; soft-deleted rows ignored; the DB unique-violation path maps to the same message (constructed exception on API.Framework) | `Create_DuplicateNameDifferentCase_FailsWithAlreadyExists`, `Create_NameOfSoftDeleted_Succeeds` |
| Soft delete | Flag set, row kept, audit fields set, list excludes it, get / update / delete afterwards return not found | `Delete_Existing_SetsIsDeletedAndKeepsRow` |
| Permission policies | Policy registered with the right claim; **every** endpoint carries the policy (reflection over the controller's actions); other permissions do not satisfy it | `AllAnimalEndpoints_RequireAnimalsWritePolicy` |
| Mappers | Entity ↔ contract maps every property; fallbacks (for example display name → email) | `ToListItem_NoDisplayName_UsesEmail` |
| Model / seed | EF model metadata (schema, columns, indexes) and seeded permission links, without a database | `AnimalModel_MapsToCreaturesSchema`, `SeededGroupPermissions_LinksAnimalsWriteToStandard` |
| Audit | `UpdatedUtc` from a fake clock, `UpdatedBy` from the current user | `Update_SetsUpdatedUtcFromClock` |

## Mock only at backend boundaries

- **Mock:** downstream HTTP clients (`*RestService`), the clock (`TimeProvider` or the codebase's clock abstraction), the current user / claims, outbound email / notification senders.
- **Do not mock:** the service under test, its validators, schema validation, mappers, or the EF `DbContext` — use the codebase's EF Core factory (Unity.API: SQLite / InMemory; API.Framework: InMemory).
- Behaviour that only the real database has (PostgreSQL `jsonb`, filtered unique indexes) is proven by the e2e run on the real test database, not faked in a unit test.

## Quality checks

`checklists/api-unit-test-checklist.md`.
