# Ticket: T-RENAME-001 — API.Framework: remove v1 URL versioning and flatten Controllers\V1

| Field | Value |
|-------|--------|
| ID | T-RENAME-001 |
| Type | Service API (cross-cutting) |
| Feature | system-rename |
| Priority | High |
| Owner | dev-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** a developer calling API.Framework  
**I want** routes without a v1 segment and no versioning machinery  
**So that** the API matches its only consumer and the UI no longer depends on a version prefix

## Full-stack scope

No UI controls or DB columns. Files: `Api.Framework/Program.cs`, `Api.Framework/Api.Framework.csproj`, the 14 controller files under `Api.Framework/Controllers/V1/**`, `Api.Framework.Tests/Animals/AnimalPoliciesTests.cs` (imports lines 4–5, comment line 77).

## Work to do

1. Remove `[ApiVersion("1")]` from the 14 controllers and change `[Route("v{version:apiVersion}/<x>")]` to `[Route("<x>")]`. Route segments after the prefix are unchanged.
2. Remove the `AddApiVersioning(...).AddMvc().AddApiExplorer(...)` block (`Program.cs:39-51`) and `using Asp.Versioning;` everywhere. D2: remove the `Asp.Versioning.Mvc` and `Asp.Versioning.Mvc.ApiExplorer` package references.
3. D1: move `Controllers/V1/{Area}/*` to `Controllers/{Area}/*` and change namespaces to `Api.Framework.Controllers.{Area}`; update `Program.cs:12` and `AnimalPoliciesTests.cs:4-5`. Keep CRLF, UTF-8 without BOM.
4. Swagger (D6): keep `SwaggerDoc("v1", …)` and `/swagger/v1/swagger.json`, and confirm every endpoint still appears in the document.
5. `dotnet build Api.Framework.sln --configuration Release` and `dotnet test` (Api.Framework.Tests) pass.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-001/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — Endpoints answer without v1

```gherkin
Given API.Framework is running in the Test environment
When I call GET /schemas/create-animal and POST /Authorisation/SignIn with valid input
Then each returns the same status and body shape as the old /v1/ route did
```

### Scenario: S2 — The old v1 routes are gone

```gherkin
Given API.Framework is running
When I call GET /v1/Animal
Then the response is 404 Not Found
```

### Scenario: S3 — No versioning machinery remains

```gherkin
Given the API.Framework source
When I search for "ApiVersion", "Asp.Versioning", "apiVersion}" and "x-api-version" outside bin and obj
Then there are no matches (D2: package references removed too)
```

### Scenario: S4 — Controllers are flattened

```gherkin
Given the change is made (D1: flatten)
When I list Api.Framework/Controllers
Then there is no V1 folder, the 14 controllers sit under Controllers/{Area}, and no file declares or imports a namespace containing "Controllers.V1"
```

### Scenario: S5 — Swagger lists every endpoint

```gherkin
Given API.Framework is running in Development
When I open /swagger/v1/swagger.json
Then it lists every action of the 14 controllers with paths that have no /v1 prefix
```

### Scenario: S6 — Build and unit tests pass

```gherkin
Given the changes are made
When dotnet build Api.Framework.sln --configuration Release and dotnet test run
Then both pass with no new warnings
```

Checklist (derived from scenarios):

- [ ] 14 controllers: attributes and routes changed
- [ ] `AddApiVersioning` and packages removed (D2)
- [ ] Flattened folders and namespaces, tests updated (D1)
- [ ] Swagger doc still complete (D6)

## Out of scope

- Unity → System text (T-RENAME-002)
- Consumers of the routes (T-RENAME-005 / 008 / 009)
- Unity.API (keeps its V2 routes)

## Notes

- Stable ID for DevOps upsert: `T-RENAME-001`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
- Spot-check 2026-10-09: 14 files, 1 controller each, 7 `Controllers.V1.*` namespaces. The Tests project imports were missed by the scan.
