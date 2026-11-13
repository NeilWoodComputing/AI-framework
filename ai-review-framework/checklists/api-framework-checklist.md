# API checklist — API.Framework

Applies when `development.api.active` is `api-framework`. Use `ai-code-framework/api/API.Framework/CLAUDE.md`, `AGENTS.md`, its `.cursor/rules`, and the shared `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc`.

Paths below are relative to `ai-code-framework/api/API.Framework/`.

### Forms and schemas

- [ ] Forms served through `IJsonSchemaFileApi.GetFormSchemaAsync<TRecord>()`, wizard steps through `GetWizardStepSchemaAsync<TRecord>(step)`; schema files under `Validation/Schemas`
- [ ] Single form record extends `AbstractFormRecord` (`CatalogueItemRecord`); wizard record extends `JsonSchemaWizardRecord` (`ComponentShowcaseRecord`)
- [ ] Controllers do not read schema files or return a `JSchema` round-trip as the form document
- [ ] Layout kept: `Controllers/{Area}`, `Controllers/Schemas`, `Records`, `Validation/Schemas`, `DataFramework/JsonSchemaValidation`, `DataFramework/DataImport`; EF models in `Api.Framework.Data`
- [ ] Custom rules are a `constraints` array with `messages` keyed by constraint `id`; reusable validators registered as `ICustomValidator`; database checks stay in the area service
- [ ] Add and Edit share one schema file and one schema GET (default `GET schemas/create-{entity}`); create and update both call `ValidateData` on the same `{Entity}Record` - `AGENTS.md`:43, `CLAUDE.md`:17
- [ ] On submit the record is re-validated with `IRecordValidationApi`; database-only checks (uniqueness and the like) run in the area service; field errors return as `validationErrors` (`propertyId` + `errors`) - `AGENTS.md`:44-45, `CLAUDE.md`:19
- [ ] New schema JSON is picked up by the `Validation\Schemas\*.json` content glob; services and schemas registered (`AddLoginServices`, `AddFormSchemas`); permissions / policies registered; routes and `validationErrors` match the paired Next.js feature - `.cursor/rules/api-framework-testing.mdc`:56-59
- [ ] The schema policy allows every user who can open the form: the same policy on the schema endpoint and the data endpoints - `.cursor/rules/api-framework-controllers.mdc`:59
- [ ] No Unity.API BFF patterns copied in (`Controllers/V2`, `*RestService`, `PaginatedResponse`, `[CandCAuthorize]`) - `AGENTS.md`:72

### Security and permissions

- [ ] Class-level `[Authorize]` plus `[Authorize(Policy = {Area}Policies.X)]` on every endpoint of the area, schema endpoints included (a controller whose actions all share one policy may put it on the class); `[AllowAnonymous]` only for sign-in, register, token and password-reset endpoints and the sign-in schema - `.cursor/rules/api-framework-controllers.mdc`:37, `.cursor/rules/api-framework-auth-permissions.mdc`:26
- [ ] Policies registered in `Program.cs` `AddAuthorization` with `policy.RequireClaim(TokenService.PermissionClaimType, ...)` (the `permission` claim); a read policy accepts the read and the write permission - `.cursor/rules/api-framework-auth-permissions.mdc`:9, :24
- [ ] A new permission is appended to `LoginPermissions.All` with the next unused number (never renumbered or reused), group links are seeded in `LoginDbContext.SeededGroupPermissions()` (other groups only when the plan says so), `{Area}Policies.cs` is added, and the migration inserts the permission rows - `.cursor/rules/api-framework-auth-permissions.mdc`:21-25
- [ ] A new domain area has its own permission, not `user_management_*`; tenant features (`LoginFeatures`, `TenantFeature`) are not used as permissions - `.cursor/rules/api-framework-auth-permissions.mdc`:32-33
- [ ] The API policy protects every endpoint even where the UI hides it by permission; a missing or expired token on a mutating action returns `401` with `MessageResponse` - `.cursor/rules/api-framework-ui-contract.mdc`:66
- [ ] `Jwt` settings, the secret, token lifetimes and `RequireHttpsMetadata` unchanged unless the human owner asked - `.cursor/rules/api-framework-auth-permissions.mdc`:34

### Data and migrations

- [ ] Entity in `Models/{Entity}.cs`, a `DbSet<{Entity}>` on `LoginDbContext` and a `modelBuilder.Entity<{Entity}>(...)` block in `OnModelCreating` - `.cursor/rules/api-framework-data-migrations.mdc`:21
- [ ] Default schema `auth`; a domain area has its own schema constant passed to `ToTable`; the schema for a new table is a plan decision (asked of the human owner, not defaulted into `auth`); the history table stays `auth.__ef_migrations_history` - `.cursor/rules/api-framework-data-migrations.mdc`:13-16
- [ ] Tables plural snake_case; keys and indexes named explicitly (`pk_{table}`, `ix_{table}_{columns}`, `fk_{table}_{principal}_{column}`) - `.cursor/rules/api-framework-data-migrations.mdc`:22
- [ ] Keys are `Guid Id`; audit columns `CreatedUtc` / `UpdatedUtc` (`DateTimeOffset`), plus `UpdatedBy` (`Guid`, FK to `users`, `DeleteBehavior.Restrict`) when the UI shows "last amended by" - `.cursor/rules/api-framework-data-migrations.mdc`:23
- [ ] Soft delete is `IsDeleted`; a uniqueness rule that ignores deleted rows uses a `Normalized{Field}` column with a filtered unique index (`.IsUnique().HasFilter("NOT is_deleted")`) - `.cursor/rules/api-framework-data-migrations.mdc`:24
- [ ] Dates without time are `DateOnly` with `HasColumnType("date")`; simple string lists are `jsonb` with `HasDefaultValueSql("'[]'::jsonb")`; `HasMaxLength` matches the schema `maxLength` - `.cursor/rules/api-framework-data-migrations.mdc`:25-26
- [ ] `HasData` uses fixed GUIDs and fixed timestamps; never `DateTime.Now`, `Guid.NewGuid()` or other runtime values - `.cursor/rules/api-framework-data-migrations.mdc`:30
- [ ] Migration added with `dotnet ef migrations add {Name} --project Api.Framework.Data --startup-project Api.Framework` (or `Add-Migration`); `*.Designer.cs` and `LoginDbContextModelSnapshot.cs` not hand-edited; an applied migration is never edited or removed; no `EnsureCreated`, `database update` against a shared database or database drop unless the human owner asked - `.cursor/rules/api-framework-data-migrations.mdc`:36-44

### Configuration and secrets

- [ ] Committed config holds no credentials: `ConnectionStrings:LoginConnection` and `Jwt:Secret` stay empty in `appsettings.json` and `appsettings.Test.json`; `LoginDbContextFactory` has no fallback - `AGENTS.md`:49, `.cursor/rules/api-framework-overview.mdc`:54
- [ ] Values come only from user-secrets on `Api.Framework` (Development) or the `APIFW_TEST_` env vars (Test only); no unprefixed `ConnectionStrings__LoginConnection` / `Jwt__Secret` env vars - `AGENTS.md`:51-62
- [ ] Connection strings, JWT secrets and CORS origins (`Cors:AllowedOrigins`) unchanged unless the human owner asked; no credential value in a committed file; no `.env*` file created or edited - `AGENTS.md`:66, :73, `.cursor/rules/api-framework-ui-contract.mdc`:70, `.cursor/rules/api-framework-overview.mdc`:54
- [ ] No `git init` without the human owner asking; no agent-specific folder - `AGENTS.md`:70-71

### Tests and build

- [ ] `Api.Framework.Tests` (`Api.Framework.Tests/Api.Framework.Tests.csproj`, net10.0, in `Api.Framework.sln`) is the implementing agent's scaffolding; scenario tests are the testing agent's, inside that project only - `.cursor/rules/api-framework-testing.mdc`:9-15
- [ ] xUnit, Moq, Microsoft.NET.Test.Sdk and EF Core InMemory; folders mirror areas; service-level tests preferred (InMemory does not enforce PostgreSQL unique indexes or jsonb) - `.cursor/rules/api-framework-testing.mdc`:16-18
- [ ] From the `API.Framework` folder: `dotnet build Api.Framework.sln --configuration Release` and `dotnet test Api.Framework.Tests/Api.Framework.Tests.csproj --configuration Release` pass (one scenario: `--filter "Scenario=T-<DOMAIN>-NNN/S<n>"`); full gate `node ../../scripts/pre-handoff-checks.mjs --target api-framework` - `.cursor/rules/api-framework-testing.mdc`:22-33, `AGENTS.md`:75-81
- [ ] Test-data module is Test-environment only: `POST TestData/Reset/master` and `POST TestData/Reset/{scenarioKey}`, guarded by `TestData:Enabled` + environment `Test`, database `api_framework_test`, `X-Test-Data-Key` and a signed-in persona; Production forces `TestData:Enabled=false`; never pointed at `unity_login` - `.cursor/rules/api-framework-testing.mdc`:35-40
- [ ] Paging and search have unit tests on EF in-memory (`Paging/`, each list's search and sort); row order and search matching are proven by the e2e run on PostgreSQL, not unit tests alone - `.cursor/rules/api-framework-testing.mdc`:49-52
