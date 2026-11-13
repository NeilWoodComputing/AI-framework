# API checklist — Unity.API

Applies when `development.api.active` is `unity-api`. Every item cites its source under `ai-code-framework/api/Unity.API/`. Rules are the `.cursor/rules/*.mdc` files (index: `.cursor/rules/README.md`); skills are `.cursor/skills/*/SKILL.md`.

## Architecture and placement

- [ ] New UI-facing controllers are under `Unity.API/Controllers/V2`; no new UI routes under `Controllers/V1` — `unity-api-overview.mdc`
- [ ] Controller has `[Route("v{version:apiVersion}/...")]`, `[ApiVersion("2")]` and `[CandCAuthorize]` — `unity-api-overview.mdc`, `unity-api-bff-endpoint` skill
- [ ] Controller extends `BaseResponseHandlerController` and returns through `ExecuteWithResponseHandlingAsync` — `unity-api-bff-endpoint.mdc`
- [ ] New controller copies a sibling in the same V2 folder (canonical: `ProjectController.GetAll`, `ProjectController.Create`) — `unity-api-bff-endpoint.mdc`, rules `README.md`
- [ ] Records and schema JSON / builders in `Unity.Entities`; lookup **interfaces** in `Unity.ApplicationFramework`; implementations and DI in `Unity.API` — `unity-api-overview.mdc`
- [ ] No downstream REST clients referenced from `Unity.Entities`; a builder needing downstream data uses an interface on `Unity.ApplicationFramework` implemented in `Unity.API/Schemas/` — `unity-api-overview.mdc`, `unity-api-json-schema` skill
- [ ] Any NuGet namespace used in `Unity.Entities` has a matching `PackageReference` in `Unity.Entities.csproj` (same version as `Unity.API.csproj`) — `unity-api-overview.mdc`

## UI contract

- [ ] Existing route, query names and JSON property names kept where the UI already calls them — `unity-api-ui-contract.mdc`
- [ ] Responses use `PaginatedResponse`, `SingleResponseBase`, `IdResponse` or `BooleanResponse` from `Unity.Shared`; no bare arrays — `unity-api-ui-contract.mdc`
- [ ] `success: false` includes `errorMessages` — `unity-api-bff-endpoint.mdc`
- [ ] JSON is camelCase; grid column `field` and form `#/properties/...` scope match the C# property name — `unity-api-bff-endpoint.mdc`
- [ ] UI records mapped in `Unity.API/Mapping`; no downstream request / response model exposed when its property names differ from the UI model — `unity-api-ui-contract.mdc`, `unity-api-bff-endpoint.mdc`
- [ ] List and detail models the UI binds live in `Controllers/V2/TempEntityModels`; form records in `Unity.Entities/Records` — `unity-api-bff-endpoint.mdc`
- [ ] A UI `*-api-routes.ts` change is paired with the matching V2 controller — `AGENTS.md`

## Grid list endpoints

- [ ] Accept `pageIndex`, `pageSize`, `sortBy`, `sortDirection`; `sortBy` is the grid column field, rewritten to the canonical downstream name before validation — `unity-api-ui-contract.mdc`, `unity-api-entity-list` skill
- [ ] Default `sortBy` from the grid config survives validation; `sortDirection=asc` binds — `unity-api-entity-list` skill
- [ ] `data` items include `id` plus every column field; `totalCount`, `pagination.totalRows`, `pagination.totalPages` set — `unity-api-entity-list` skill

## JSON schema forms and wizards

- [ ] Schema served from `GET v2/schemas/{schema-name}` via `IJsonSchemaFileApi`; builder under `Unity.Entities/Validation/Schemas/{area}/` — `unity-api-json-schema` skill
- [ ] Validation and edit-section POSTs are separate URLs from the schema GET — `unity-api-ui-contract.mdc`
- [ ] `oneOf.const` is the stored value and `oneOf.title` the label — `unity-api-json-schema` skill
- [ ] `dataLookup` key exists in `BuildLookupData`; lookup provider registered in `Program.cs` — `unity-api-json-schema` skill
- [ ] Cross-field or service rules are `constraints` entries with a `messages` entry keyed by `type`; message text matches the spec — `unity-api-json-schema` skill
- [ ] New custom validator: subclass `AbstractCustomValidator`, enum member on `EntityCustomValidatorType` with `[AssociatedType]`, `AddScoped` in `JsonSchemaValidationDependenciesRegistrar` or `UnityEntitiesDependenciesRegistrar` — `unity-api-json-schema` skill
- [ ] `unique*` validators also register their checker interface — `unity-api-json-schema` skill
- [ ] Save validates the record, maps to the downstream request, and preserves fields the section does not own — `unity-api-json-schema` skill
- [ ] Builder registered in `UnityEntitiesDependenciesRegistrar` — `unity-api-json-schema` skill

## Local persistence

- [ ] Data is owned by this API (organisations / companies, contacts, filter favourites, …); projects and developments stay downstream — `unity-api-overview.mdc`, `unity-api-local-persistence` skill
- [ ] Entity in `Unity.Data.Models`, `DbSet` on `UnityContext` — `unity-api-migrations.mdc`
- [ ] Service in `Unity.Services`, interface in `Unity.Interfaces`, registered like its siblings (`ServiceBinding.BindUnityServices`) — `unity-api-local-persistence` skill
- [ ] Migration created with `Add-Migration {Name}` (default project `Unity.Data`) and present under `Unity.Data/Migrations` — `unity-api-migrations.mdc`, `unity-api-local-persistence` skill
- [ ] No `EnsureCreated`; no database drop outside an intentional local reset — `unity-api-migrations.mdc`

## Bulk import (if touched)

- [ ] Validate returns `ImportValidationResponse` even when rows fail; import re-validates and returns `400` with it on failure, `BooleanResponse` on success — `unity-api-bulk-import.mdc`
- [ ] Persist through `IDataImportApi<TRecord>` (e.g. `ContactDataImportApi`); no second spreadsheet parser — `unity-api-bulk-import.mdc`

## Configuration

- [ ] Downstream base URLs in `appsettings.{EnvironmentName}.json`, not `launchSettings.json` — `unity-api-ui-contract.mdc`
- [ ] Rule or skill edits: `.cursor` first, then synced to `.claude` — `CLAUDE.md`, `AGENTS.md`

## Tests and build

- [ ] Tests in `Unity.API.Tests` mirroring `Controllers/V2/...`; mappers in `Unity.API.Tests/Mapping`; schema in `JsonSchemaValidation` — `unity-api-testing.mdc`
- [ ] Downstream `*RestService` mocked; no `WebApplicationFactory` for a normal BFF action; `CancellationToken` in Moq setups — `unity-api-testing.mdc`
- [ ] Create-request shape tests include every property on the downstream model — `unity-api-testing.mdc`
- [ ] One behaviour per `[Fact]`, named `{Action}_{Condition}_{Expected}` — `unity-api-tests` skill
- [ ] `dotnet build Unity.sln --configuration Release` and `dotnet test Unity.API.Tests/Unity.API.Tests.csproj` pass — `unity-api-overview.mdc`, `unity-api-tests` skill
