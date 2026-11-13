# API checklist — C# API

Applies when `development.api.active` is `csharp-api`. Every item cites its source under the active C# API project's rules and skills. Rules are the `.cursor/rules/*.mdc` files (index: `.cursor/rules/README.md`); skills are `.cursor/skills/*/SKILL.md`.

## Architecture and placement

- [ ] New UI-facing controllers are under `Controllers/V2`; no new UI routes under `Controllers/V1` — `csharp-api-overview.mdc`
- [ ] Controller has `[Route("v{version:apiVersion}/...")]`, `[ApiVersion("2")]` and appropriate authorization — `csharp-api-overview.mdc`, `csharp-api-bff-endpoint` skill
- [ ] Controller extends `BaseResponseHandlerController` and returns through `ExecuteWithResponseHandlingAsync` — `csharp-api-bff-endpoint.mdc`
- [ ] New controller copies a sibling in the same V2 folder (canonical: `ProjectController.GetAll`, `ProjectController.Create`) — `csharp-api-bff-endpoint.mdc`, rules `README.md`
- [ ] Records and schema JSON / builders in appropriate entities project; lookup **interfaces** in application framework; implementations and DI in API project — `csharp-api-overview.mdc`
- [ ] No downstream REST clients referenced from entities project; a builder needing downstream data uses an interface implemented in the API's schemas folder — `csharp-api-overview.mdc`, `csharp-api-json-schema` skill
- [ ] Any NuGet namespace used in entities project has a matching `PackageReference` in its csproj (same version as the API csproj) — `csharp-api-overview.mdc`

## UI contract

- [ ] Existing route, query names and JSON property names kept where the UI already calls them — `csharp-api-ui-contract.mdc`
- [ ] Responses use standard response wrappers (`PaginatedResponse`, `SingleResponseBase`, `IdResponse` or `BooleanResponse`); no bare arrays — `csharp-api-ui-contract.mdc`
- [ ] `success: false` includes `errorMessages` — `csharp-api-bff-endpoint.mdc`
- [ ] JSON is camelCase; grid column `field` and form `#/properties/...` scope match the C# property name — `csharp-api-bff-endpoint.mdc`
- [ ] UI records mapped in API's mapping folder; no downstream request / response model exposed when its property names differ from the UI model — `csharp-api-ui-contract.mdc`, `csharp-api-bff-endpoint.mdc`
- [ ] List and detail models the UI binds live in `Controllers/V2/TempEntityModels`; form records in entities records folder — `csharp-api-bff-endpoint.mdc`
- [ ] A UI `*-api-routes.ts` change is paired with the matching V2 controller — `AGENTS.md`

## Grid list endpoints

- [ ] Accept `pageIndex`, `pageSize`, `sortBy`, `sortDirection`; `sortBy` is the grid column field, rewritten to the canonical downstream name before validation — `csharp-api-ui-contract.mdc`, `csharp-api-entity-list` skill
- [ ] Default `sortBy` from the grid config survives validation; `sortDirection=asc` binds — `csharp-api-entity-list` skill
- [ ] `data` items include `id` plus every column field; `totalCount`, `pagination.totalRows`, `pagination.totalPages` set — `csharp-api-entity-list` skill

## JSON schema forms and wizards

- [ ] Schema served from `GET v2/schemas/{schema-name}` via `IJsonSchemaFileApi`; builder under entities validation schemas folder — `csharp-api-json-schema` skill
- [ ] Validation and edit-section POSTs are separate URLs from the schema GET — `csharp-api-ui-contract.mdc`
- [ ] `oneOf.const` is the stored value and `oneOf.title` the label — `csharp-api-json-schema` skill
- [ ] `dataLookup` key exists in `BuildLookupData`; lookup provider registered in `Program.cs` — `csharp-api-json-schema` skill
- [ ] Cross-field or service rules are `constraints` entries with a `messages` entry keyed by `type`; message text matches the spec — `csharp-api-json-schema` skill
- [ ] New custom validator: subclass `AbstractCustomValidator`, enum member with `[AssociatedType]`, registered in dependencies registrar — `csharp-api-json-schema` skill
- [ ] `unique*` validators also register their checker interface — `csharp-api-json-schema` skill
- [ ] Save validates the record, maps to the downstream request, and preserves fields the section does not own — `csharp-api-json-schema` skill
- [ ] Builder registered in entities dependencies registrar — `csharp-api-json-schema` skill

## Local persistence

- [ ] Data is owned by this API (organisations / companies, contacts, filter favourites, …); projects and developments stay downstream — `csharp-api-overview.mdc`, `csharp-api-local-persistence` skill
- [ ] Entity in data models, `DbSet` on DbContext — `csharp-api-migrations.mdc`
- [ ] Service in services folder, interface in interfaces folder, registered like its siblings — `csharp-api-local-persistence` skill
- [ ] Migration created with `Add-Migration {Name}` and present under migrations folder — `csharp-api-migrations.mdc`, `csharp-api-local-persistence` skill
- [ ] No `EnsureCreated`; no database drop outside an intentional local reset — `csharp-api-migrations.mdc`

## Bulk import (if touched)

- [ ] Validate returns `ImportValidationResponse` even when rows fail; import re-validates and returns `400` with it on failure, `BooleanResponse` on success — `csharp-api-bulk-import.mdc`
- [ ] Persist through `IDataImportApi<TRecord>` (e.g. `ContactDataImportApi`); no second spreadsheet parser — `csharp-api-bulk-import.mdc`

## Configuration

- [ ] Downstream base URLs in `appsettings.{EnvironmentName}.json`, not `launchSettings.json` — `csharp-api-ui-contract.mdc`
- [ ] Rule or skill edits: `.cursor` first, then synced to `.claude` — `CLAUDE.md`, `AGENTS.md`

## Tests and build

- [ ] Tests in API test project mirroring `Controllers/V2/...`; mappers in test project's mapping folder; schema in `JsonSchemaValidation` — `csharp-api-testing.mdc`
- [ ] Downstream `*RestService` mocked; no `WebApplicationFactory` for a normal BFF action; `CancellationToken` in Moq setups — `csharp-api-testing.mdc`
- [ ] Create-request shape tests include every property on the downstream model — `csharp-api-testing.mdc`
- [ ] One behaviour per `[Fact]`, named `{Action}_{Condition}_{Expected}` — `csharp-api-tests` skill
- [ ] `dotnet build` and `dotnet test` pass on the solution — `csharp-api-overview.mdc`, `csharp-api-tests` skill
