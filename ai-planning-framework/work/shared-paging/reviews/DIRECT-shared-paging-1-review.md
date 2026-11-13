# Review: DIRECT-shared-paging-1 — Shared paging (Phase 1: T-PAGING-001..006)

> **Provisional code verdict: Approve with comments.** Option B: this waits for Test Bot's T-PAGING-007 run and the test review. **PostgreSQL (localhost:5432) is down**, and so are the API and UI. This round is therefore a code review plus unit tests on in-memory EF and the Npgsql model only. Nothing was checked live (see **Not verified**).

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (History row 4, Dev Bot 18:54 BST) |
| Trigger | direct-handoff (`code_to_review: direct`; `code_to_test: direct`, option B) |
| Review scope | Plan scope (`direct_scope: plan`): every manifest file (api 36, ui 12, tests 8, migrations 0). Each one was compared with Dev Bot's pre-edit originals in `%TEMP%\devbot-sp\orig` (read only) and, for the contracts, with the 11:20 pre-rename backup zip |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | Not under git. Working tree as of 18:58 BST |
| Linked tickets | T-PAGING-001 … T-PAGING-006 (Dev Bot). Reference: T-PAGING-007 (Test Bot), T-PAGING-008 (Phase 2, not started) |
| Feature(s) | `ai-planning-framework/work/shared-paging/` |
| Specs reviewed | `work/manage-animals/specs/manage-animals.yaml` › `search_filters`, `pagination` (decision 31); `plan.md` §2–§9, P1–P19 |
| Active API / UI | api-framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `.cursor/rules` + `.claude/rules` (services, controllers, ui-contract, testing), entity-list skill; UI `nextjs-entity-grid.mdc`, `nextjs-list-pages.mdc`, `style/nextjs-components.mdc`; `checklists/severity.md` |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 09/10/2026 19:05 (Europe/London) |
| Review iteration | 1 |

## Verdict

**Approve with comments** (provisional; final once the test review is done)

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 0 | 1 | 6 |

Plus one note (F-08). Severity threshold for Request changes: `major`. Nothing is routed back now. F-01 and the Nits are follow-ups for Dev Bot and Plan Bot, and none of them blocks Test Bot.

## Summary

This is a clean, well-tested piece of work.

- **One Paging area.** The 7 copied clamps and 3 hand-written sort switches are replaced by one small `Paging/` area. `PageWindow` adjusts out-of-range values and never rejects them. `SortMap<T>` is a typed, case-insensitive whitelist with an optional ascending secondary sort and a final `Id` tie-break. `ToPagedBodyAsync` always applies Skip/Take and uses async counts.
- **Contracts unchanged.** The three contracts moved with exactly the same members. The JSON shape is pinned by a literal-string test.
- **Animals search.** It filters on `NormalizedName`, with the input normalised the same way in C#. Npgsql turns it into a parameterised `LIKE` with `%` and `_` escaped (proven by a model-only SQL test).
- **ReferenceData.** The Types search the API used to ignore now works. The `Reverse()` that flipped ties is gone.
- **UI.** `setFilters` is a small, well-contained debounce with unmount cleanup, built on the existing "latest response wins" guard. The Animals search box matches decision 31 and the spec row.
- **Behaviour kept.** The manage-animals grid behaviours reviewed earlier (row menu, Escape, boolean cells, loading modal) are untouched.

The one Minor is a test-design issue: the CORS tests find `appsettings.json` by walking up to `Api.Framework.sln`. That ties into system-rename F-15.

## Review scope

| Repo | Files | Class | Reason |
|------|-------|-------|--------|
| api | `Api.Framework.Services/Paging/*` (5 new) | api | manifest (T-PAGING-001) |
| api | `Animals/AnimalContracts.cs`, `AnimalService.cs`, `IAnimalService.cs`; `Controllers/Animals/AnimalController.cs`, `Data/Models/Animal.cs` (existing) | api | manifest (T-PAGING-002) |
| api | `ReferenceData/ReferenceDataContracts.cs`, `ReferenceDataService.cs`, `ReferenceDataController.cs` | api | manifest (T-PAGING-003) |
| api | Directory / Tenant / Catalogue / ComponentShowcase services, interfaces and controllers (12 files) | api | manifest. Diffed against the originals: **`using` lines only**, plus `ListTypes` binding `ReferenceDataQuery` |
| api | 4 rule topics × 2 copies + entity-list skill × 2 | docs | manifest (T-PAGING-006) |
| api | `Api.Framework.Tests/Paging/*` (3), `Animals/AnimalServiceSearchTests.cs`, `AnimalSearchSqlTests.cs`, `ReferenceData/ReferenceDataQueryTests.cs` | tests | manifest |
| ui | `use-entity-grid-state.ts` (+ `.test.tsx`), `entity-grid-config.ts`, `index.ts`, `ReferenceDataTypesGrid.tsx`, `AnimalsGrid.tsx` (+ `.test.tsx`), `animals-search.data-provider.ts`, `ComponentTestHarness.tsx`, `nextjs-entity-grid.mdc` | ui / tests / docs | manifest. Existing deps read: `use-entity-search-state.ts`, `EntityGrid.tsx`, `search-query-params.ts`, `use-animals-grid.tsx`, `normalize-paged-search-response.ts` |
| api | `Api.Framework.Tests/Cors/SystemUiCorsTests.cs` | tests | dependency (Dev Bot's .sln note; F-01) |

Every source file changed since 16:10 BST is in the manifest. The only extra is `tsconfig.tsbuildinfo`, a typecheck cache. Nothing was discovered outside it.

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix | Fix by |
|----|----------|------|-----------|---------|-----------------------|---------------|--------|
| F-01 | Minor | Tests | `Api.Framework.Tests/Cors/SystemUiCorsTests.cs:52-62` | `ApiProjectDir()` walks up from `AppContext.BaseDirectory` to find `Api.Framework.sln`. Built to an output folder outside the source tree, 2 tests fail with an unhelpful `Assert.NotNull` failure. I confirmed it on my copy: `dotnet test -o %TEMP%\…` gave 125 pass / 2 fail (`AppSettingsJson_KeepsTheFourDefaultOrigins`, `AppSettingsTestJson_AddsTheTestUiOn3013_AndKeepsTheDefaults`); the in-tree build gave 127/127. It's a test-design flaw, not a product bug. It matters because system-rename **F-15** (the gate's unit check fails while a Test API locks `bin\Release`) is best fixed by building the tests elsewhere. Any such fix must keep the output inside the source tree (Test Bot's `-o Api.Framework.Tests\bin\tb-unit` works) until this is fixed. `Helpers/AnimalTestSupport.cs:29-30` has the same fixed-hop pattern as a fallback (pre-existing; it passed here) | `api-framework-testing` (tests must be deterministic) | Link the two appsettings files into the test project as content (`<None Include="..\Api.Framework\appsettings*.json" Link="ApiSettings\%(Filename)%(Extension)" CopyToOutputDirectory="PreserveNewest" />`) and read them from `AppContext.BaseDirectory`. Or stamp the project folder in with `AssemblyMetadata`. Either way, fail with a message naming the missing file. Then F-15 can build to any folder | Dev Bot |
| F-02 | Nit | Acceptance criteria | `tickets/T-PAGING-002-api-animals-search-and-sort.md:85` (S6) | S6 says "DateBorn descending then Id". The code (`AnimalService.cs:33-39`) gives DateBorn desc, then **Name asc**, then Id, which keeps the pre-feature `ThenBy(Name)` (plan §2 row "Animals have no filters"). The test asserts the code's order. Plan §5.1 doesn't mention SortMap's per-key secondary at all | plan §5.1; T-PAGING-002/S6 | Reword S6 to "DateBorn descending, then Name, then Id", and add the secondary sort to plan §5.1. Test Bot should assert that order on PostgreSQL | Plan Bot |
| F-03 | Nit | Spec conformance | `plan.md:26`, `:52`, P12 | The plan says no list page keeps search, page or sort in the URL, and P12 / Q8 say "not kept in the URL". The ReferenceData Types grid already did, through `useAuthenticatedEntitySearch` → `useEntitySearchByQueryState`, before this feature. Dev Bot flagged this in handoff Notes, and the new `nextjs-entity-grid.mdc:73` scopes the rule to local grids. Nothing to change in code; the plan is just inaccurate | plan §2 / §4 / P12 | Correct plan §2, and record that P12 applies to Animals (and new local grids), with the Types grid unchanged (P2) | Plan Bot |
| F-04 | Nit | UI standards / a11y | `ReferenceDataTypesGrid.tsx:66-76` | The Types search box has a placeholder ("Filter types…") but no `aria-label`. The new rule `nextjs-entity-grid.mdc:70` requires a tid, a placeholder **and** an aria-label, and names this file as a reference. Pre-existing, but the line was touched in this feature. Animals is fine (`aria-label="Search animals"`) | `nextjs-entity-grid.mdc` › Filters and search boxes | Add `aria-label="Filter types"` | Dev Bot |
| F-05 | Nit | UI behaviour | `ReferenceDataTypesGrid.tsx:59` | The box now keeps its own `useState`, set once from the URL. The Types grid is URL-synced, so browser Back/Forward or a link to another `?searchText=` changes the results but leaves the old text in the box. Before this feature the box was bound to the URL. The `setFilters` hook tests use the local search state only, so the URL-synced path is covered only by e2e (T-PAGING-007/S2) | `nextjs-entity-grid.mdc` (local state for typing) | Re-sync the local value when `searchState.searchRequest.searchText` changes and no debounce is pending (or key the input on it). Optionally add one hook test with the URL-synced state | Dev Bot |
| F-06 | Nit | Tests | `Api.Framework.Tests/Animals/AnimalSearchSqlTests.cs:15-21` | The SQL test is meaningful and needs no database (Npgsql model only, `Host=unused`). It proves trimming, upper-casing, a parameterised `normalized_name LIKE @…` and the escaped pattern `'%100\%\_%'`. `\` isn't covered, although `AnimalQuery.Search` documents that it matches literally (`AnimalContracts.cs:57`). The assertion relies on `ToQueryString()` text, which is fine for a pin | T-PAGING-002/S3; plan §5.2 | Add a `\` case (expect the pattern `'%\\%'`). Test Bot's PostgreSQL run should include a name with `\` | Dev Bot (unit), Test Bot (e2e) |
| F-07 | Nit | Tests | `AnimalServiceSearchTests.cs:89-110`, `ReferenceDataQueryTests.cs:122-135` | The "over 100 → 400" scenarios (002/S5, 003/S5) are unit-tested with `Validator.TryValidateObject` only. That proves the attribute, not that `[ApiController]` binds `search` / `searchText` and returns 400 with that key. Low risk: standard MVC, and controller binding is plain `[FromQuery]` | T-PAGING-002/S5, 003/S5 | Covered by Test Bot's e2e (T-PAGING-007). Optional: a `WebApplicationFactory` test like `AnimalPoliciesTests` | Test Bot (e2e) |
| F-08 | Note | API standards | `AnimalContracts.cs:59`, `ReferenceDataContracts.cs:17` | `[StringLength(100)]` counts the raw input, so 98 characters plus 3 spaces is a 400 even though the trimmed text is 98. The UI's `maxLength` 100 also counts spaces, so the two agree, and P10 says "above 100 → 400" | P10 | No change; noted for e2e expectations | — |

## Spec conformance (per control)

**manage-animals › search_filters** (decision 31):

| Control | Spec | Code | Status |
|---------|------|------|--------|
| Search animals: text input above the grid | Text input (search box) above the grid | `Input` in the grid toolbar (`headerActions`), right of "+ Add Animal", tid `animals-search` (`AnimalsGrid.tsx:26-41`) | Match |
| Placeholder | "Search animals…" | `'Search animals\u2026'` | Match |
| Max length | at most 100 (the input stops at 100) | `maxLength={100}` (`animalsSearchMaxLength`); API `[StringLength(100)]` | Match |
| filters_on | `Animal.Name` (matched on `Animal.NormalizedName`) | `NormalizedName.Contains(term.ToUpperInvariant())` (`AnimalContracts.cs:62-73`) | Match |
| match_rule | contains, case-insensitive, accent-sensitive, trimmed, from 1 char, whitespace = no filter, `%`/`_` literal, server-side after 300 ms, back to page 1, keeps sort and page size, "No results" with + Add Animal kept, not in the URL, soft-deleted never match | trim + `IsNullOrEmpty` → no filter; `ToUpperInvariant` (same as the column); Npgsql escaped `LIKE`; `filterDebounceMs = 300`; `pageIndex: 0` with sort and size kept; grid "No results"; `useAuthenticatedEntitySearchLocal` (no URL); `!IsDeleted` before the filter | Match |
| default | Empty (all non-deleted, Name ascending) | blank → no filter; SortMap default `name` asc | Match |
| pagination | 20, options 5–200, server-side, Name ascending | `PagingDefaults` 20/200; `defaultPagingOptions` unchanged; `maxPageSize` 200 | Match |

## JSON contract (T-PAGING-001/S5)

| Item | Before (`Directory/DirectoryContracts.cs`, pre-rename backup and Dev Bot's original) | After (`Paging/PagingContracts.cs`) | Result |
|------|------|------|--------|
| `PagedQuery` | `int PageIndex`; `int PageSize = 20`; `string? SortBy`; `string? SortDirection`; `bool IncludeDeleted` | Same; default via `PagingDefaults.PageSize` (20) | Identical |
| `PagingModel` | `int PageIndex, PageSize, TotalRows, TotalPages` | Same | Identical |
| `PagedBody<T>` | `IReadOnlyList<T> Data = []`; `int TotalCount`; `PagingModel Pagination = new()` | Same | Identical |
| Serialiser | ASP.NET web defaults (camelCase). No custom `JsonSerializerOptions`, and no `CustomSchemaIds` in Swagger, so schema ids use the short type name and are unaffected by the namespace | Unchanged | Same wire shape |
| Pinned | none | `PagedBodyTests.JsonShape_IsUnchanged`: `{"data":[…],"totalCount":1,"pagination":{"pageIndex":0,"pageSize":20,"totalRows":1,"totalPages":1}}` | Good |
| `totalPages` | `ceil(total/size)` (with a dead `size == 0` guard) | `ceil(total/size)`; size is never 0 after `PageWindow` | Same values |
| Query parameters | `pageIndex`, `pageSize`, `sortBy`, `sortDirection`, `includeDeleted` | Same, plus `search` (`GET Animal`) and `searchText` (`GET ReferenceData`) | Additive only |

**UI consumers.** `AbstractSearchDataProvider.search` → `normalizePagedSearchResponse` (unchanged, 46 lines) reads `data` / `pagination` / `totalCount`. `searchRequestToQueryParams` sends every non-blank key, so `search` reaches the API, and blank or whitespace is left out on the client too. No consumer code had to change.

## Paging and sort analysis

| Check | Result | Reference |
|-------|--------|-----------|
| Page size ≤ 0 → 20; > 200 → 200; negative index → 0 | Yes, never a 400 (P15) | `PageWindow.cs:10-14`; `PageWindowTests` (0/-1, -5, 1, 200, 201, 500) |
| Huge page index | `Skip` saturates at `int.MaxValue` instead of overflowing. The old `index * size` could go negative and throw | `PageWindow.cs:17`; `Skip_SaturatesInsteadOfOverflowing` |
| Beyond the last page | Empty `data`, correct totals (same as before) | — |
| Total count | `CountAsync` on the **filtered** source before sort/paging; in memory, `rows.Count` after the filter | `PagedQueryableExtensions.cs:34`, `:47-49`; 001/S4 test (45 rows, page 2 → 5) |
| Skip/Take always applied | Yes (no `totalRows` short-cut, unlike Unity `ToPagedList`) | `:35-39` |
| Deterministic order | Every key ends `ThenBy(Id)` ascending (desc applies to the primary only). Secondaries are ascending and run before Id | `SortMap.cs:73-95`; `Ties_AreOrderedById_OnEveryCallAndAcrossPages`, `SecondarySort_IsAscending_AndRunsBeforeTheIdTieBreak`, `InMemoryAndQueryable_GiveTheSameOrder` |
| Sort-key allowlist | Dictionary of typed expressions, `OrdinalIgnoreCase`, trimmed. Unknown, empty or whitespace → default key (P5). No reflection, no `EF.Property`, no string column names reach EF, so there's no column injection | `SortMap.cs:22`, `:97-101`; `UnknownOrEmptyKey_FallsBackToDefault` |
| Direction | `desc` (trimmed, any case) → descending; anything else ascending | `SortMap.cs:70-71`; `Direction_IsAscendingUnlessDesc` (desc, DESC, asc, "", sideways) |
| Map safety | Duplicate keys throw (`Dictionary.Add`); `ThenBy` before `Add` throws; a default not in the map throws. Static and read-only after construction, so concurrent reads are safe | `SortMap.cs:39-68` |
| Animals keys | name (default), isFurry, hasHooves, dateBorn, updatedUtc; non-name keys then Name then Id. Old lower-case keys still match (case-insensitive) | `AnimalService.cs:33-39`; F-02 |
| ReferenceData Types | in memory; text keys `OrdinalIgnoreCase` (as before); final tie-break `Id` (= type key, ordinal); `Reverse()` removed (P16) | `ReferenceDataService.cs:39-45`; 003/S3 test |
| ReferenceData Items | code / description / displayName (default), final Id; shared window (500 → 200) | `:48-53`, `:111-123`; 003/S4 test |
| Private clamps removed | Animals and ReferenceData use the shared helpers; the private `PageWindow` is gone. Phase 2 services still have their own clamps (T-PAGING-008) | — |

## Search analysis

| Check | Animals (`search`) | ReferenceData Types (`searchText`) |
|-------|--------------------|------------------------------------|
| Parameterised, no concatenation | EF `Contains(variable)` → Npgsql `a.normalized_name LIKE @p`, with the pattern built and escaped by the provider (`%`, `_`, `\` → `\`-escaped; PostgreSQL's default LIKE escape is `\`). No hand-built SQL or `EF.Functions.Like` | In memory (`string.Contains(term, OrdinalIgnoreCase)`); no SQL |
| `%` `_` `\` literal | Proven for `%` and `_` by `AnimalSearchSqlTests` (pattern `'%100\%\_%'`); `\` not pinned (F-06). In-memory tests check the results | Literal by construction; `_` and `%` tested |
| Case-insensitive | Input `ToUpperInvariant()` against `NormalizedName` (= `Name.Trim().ToUpperInvariant()` at write). Same rule both sides, same on both providers; accent-sensitive (P7) | `OrdinalIgnoreCase` on type key or display name (P17) |
| Trim / blank | `Search?.Trim()`; null, empty or whitespace → no filter (P8); the UI also leaves blank params out | Same |
| Length limit | `[StringLength(100)]` → automatic 400 (`[ApiController]`), unit-tested via `Validator` (F-07, F-08) | Same |
| Soft-deleted | `!IsDeleted` applied before the filter | n/a |
| Index use | `%x%` can't use the btree on `normalized_name`; accepted (plan §9, example scale) | n/a |
| SQL test needs a live DB? | **No.** `TestDbFactory.CreateNpgsqlModelOnly` (`Host=unused`) + `ToQueryString()`; it ran and passed with PostgreSQL down. It proves the translation, not PostgreSQL's matching (T-PAGING-007) | — |

## UI analysis

| Check | Result | Reference |
|-------|--------|-----------|
| `setFilters` | Merges patches in a ref, one timer, fires after `filterDebounceMs` (300) with `pageIndex: 0`; sort and page size come from the current request; the timer is cleared on unmount; stable callback | `use-entity-grid-state.ts:68-89` |
| Debounce tests | 004/S1 (one request after the pause, `searchText: 'cou'`), 004/S2 (page 3 / sort / size 50 → page 0, same sort and size), merge inside the window, cancel on unmount (fake timers) | `use-entity-grid-state.test.tsx` |
| Latest response wins | The existing `cancelled` flag in the search effect; 004/S3 test (slow "co" returns last, grid shows "cou") | `use-entity-search-state.ts:183-206` |
| Reset to page 1 | Search: `setFilters`. Sort: existing `setSort` (`pageIndex: 0`) | — |
| A sort or page click during the 300 ms window | The pending filter still fires afterwards and returns to page 1 with the new sort. Acceptable | — |
| Search state in the URL | Animals: local state (`useAuthenticatedEntitySearchLocal`), not in the URL (P12). Types grid: URL-synced as before (F-03, F-05) | `use-animals-grid.tsx:41` |
| Immediate typing | Local `useState`, value passed to `setFilters` | `AnimalsGrid.tsx:20`, `ReferenceDataTypesGrid.tsx:59` |
| Empty state | Grid "No results"; "+ Add Animal" stays in the toolbar (P11); unit-tested | `EntityGrid.tsx:126-127`; `AnimalsGrid.test.tsx:59-64` |
| Loading | "Loading…" only while there are no rows; the loading modal (`isEntityGridInitialLoad`) shows only before the **first** response, so typing never brings up a modal or moves focus. The toolbar (with the box) stays mounted across loading, empty and table states | `use-entity-grid-initial-load.ts`; `EntityGrid.tsx:97-129` |
| Accessibility | Animals: `aria-label="Search animals"`, `id` = tid, native text input, keyboard only. Types: no aria-label (F-04). There's no live region announcing the new result count; optional, same as before | — |
| List-page rule | Search and results stay on the routed page; no modal | `nextjs-list-pages.mdc` |
| manage-animals regressions | `EntityGrid.tsx`, `grid-cell-renderers`, `DropdownMenu`, `Modal` and the row actions are **unchanged** (diff against the originals). The row menu, Escape handling (menu stops the Modal listener), boolean icon cells and the initial loading modal are unaffected. `ComponentTestHarness` only gains a no-op `setFilters` | — |
| `maxPageSize` | Exported 200, equals the largest option (004/S4 test) | `entity-grid-config.ts:9` |

## P18: `normalizePagedSearchResponse`

Kept unchanged, which is allowed under P18 / Q14: trim only if no caller needs Unity.API shapes. It isn't dead code. `AbstractSearchDataProvider.search` calls it for every grid. The reason given for keeping the extra shapes holds: `work/add-edit-contact` (example, parked) plans a Manage Contacts grid against Unity.API Contacts. No dead-code risk; if it is ever trimmed, that's a separate change.

## Acceptance criteria coverage (per scenario)

| Scenario | Status | Test reference(s) | Notes |
|----------|--------|-------------------|-------|
| T-PAGING-001/S1 | Covered | `PageWindowTests.From_AdjustsOutOfRangeValues` | |
| 001/S2 | Covered | `SortMapTests.SortKey_IsCaseInsensitive`, `UnknownOrEmptyKey_FallsBackToDefault` | |
| 001/S3 | Covered (in-memory) | `Ties_AreOrderedById_OnEveryCallAndAcrossPages` (asc and desc) | PostgreSQL in 007 |
| 001/S4 | Covered | `PagedBodyTests.ToPagedBodyAsync_ReturnsTheWindowAndTotals`, `ToPagedBody_InMemory_…`, `ToPagingModel_ComputesTotalPages` | |
| 001/S5 | Covered | `JsonShape_IsUnchanged` + member diff above | |
| 002/S1 | Covered (in-memory) | `Search_MatchesPartOfTheName_AnyCase` | |
| 002/S2 | Covered | `BlankSearch_ReturnsEverything_ByName` (whitespace, "", null) | |
| 002/S3 | Covered | `SearchCharacters_AreLiteral` + `AnimalSearchSqlTests` | F-06 (`\`) |
| 002/S4 | Covered | `DeletedAnimals_NeverMatch` | |
| 002/S5 | Partial | `Search_LongerThan100_FailsValidation` (100 ok, 101 fails) | F-07 |
| 002/S6 | Covered (code's order) | `Search_KeepsSortAndPaging` | F-02 wording |
| 003/S1–S2 | Covered | `TypesSearch_FiltersTheList`, `TypesSearch_MatchesDisplayName` | |
| 003/S3 | Covered | `TypesDescending_KeepsTiesInIdOrder` | |
| 003/S4 | Covered (in-memory) | `Items_TiesById_AndPageSizeIsCapped` | |
| 003/S5 | Partial | `SearchText_LongerThan100_FailsValidation` | F-07 |
| 004/S1–S4 | Covered | `use-entity-grid-state.test.tsx` | URL-synced path: F-05 |
| 005/S1 | Partial | `AnimalsGrid.test.tsx` (wiring: `setFilters({ search })`) | Results: e2e 007/S1 |
| 005/S2 | Covered | `AnimalsGrid.test.tsx` ("No results" + "+ Add Animal") | |
| 005/S3 | Partial | `AnimalsGrid.test.tsx` (clearing sends `search: ''`) | e2e |
| 005/S4 | Covered via hook | 004/S2 | e2e |
| 005/S5 | Covered | `maxlength="100"` asserted | Paste in e2e |
| 006/S1 | Covered | Review: 4 topics; `.cursor` vs `.claude` bodies identical (only a leading blank line after the front matter differs); skill identical; gate docs-dup pass (59 allowlisted) | |
| 006/S2 | Covered | `api-framework-services` lists `ToPagedList`/`totalRows`, reflection, sync `Count()`/`ToList()`, 50000, descending by default, `EF.Property`, unescaped `LIKE`, `PaginatedResponse`, cursor paging | |
| 006/S3 | Covered | `nextjs-entity-grid.mdc:66-75` (`setFilters`, page 1, 300 ms, `maxPageSize` 200) | |

## Security and data

| Check | Status | Reference |
|-------|--------|-----------|
| No SQL built from user input | Enforced: parameterised; sort keys whitelisted to typed expressions | `AnimalContracts.cs:62-73`, `SortMap.cs` |
| Input limits | `[StringLength(100)]` on both new filters; page size capped at 200 (no unbounded reads) | P10, P15 |
| Auth | Unchanged: `GET ReferenceData` keeps `UserManagementRead`; Animals controller attributes untouched | controllers diff |
| Soft delete | Animals list still `!IsDeleted`; `IncludeDeleted` on `PagedQuery` is unchanged and still ignored by Animals (as before) | — |
| Migration | None needed (`NormalizedName` already exists, unique filtered index) | plan §2 |

## Tests

### Gate, self-test, unit tests (Review Bot)

| Run | Result |
|-----|--------|
| Gate on a temporary copy (`%TEMP%\rb-spg`, no `--record`), 18:59:15 | **pass**. API: eol 232, secrets 232, docs-dup 22 docs (59 allowlisted), **unit 127/127** (0 skipped). nextjs: lint 154 files, 0 errors / 2 warnings; typecheck 0; eol 236; secrets 236; docs-dup 17; **unit 35/35 (8 files)** |
| Self-test on the copy | 64 ok / 0 fail |
| Gate in place, check-only, 19:01:07 | **pass**, the same counts (secrets nextjs: 2 skipped secret files, not opened). `handoff.md` hash unchanged by the run. No API was running, so no `bin\Release` lock this time |
| `dotnet test -o %TEMP%\rb-spg-out` (copy, output outside the tree) | 125 pass / **2 fail** (CORS appsettings tests; F-01) |

**Postgres-dependent tests:** none. All 127 API tests use EF in-memory, or the Npgsql model with `Host=unused`. None was skipped, and none failed because 5432 is down.

### Not verified (PostgreSQL, the Test API and both UIs were down; nothing was started)

- PostgreSQL matching and escaping at run time (`LIKE` with `\%`, `\_`, `\\`), and `NormalizedName` matching on real rows.
- Collation-dependent order: Name, DisplayName and Code order on PostgreSQL versus the in-memory ordinal order, and tie order across pages.
- HTTP behaviour: the 400 from model binding for `search` / `searchText`; `GET Animal?search=` end to end; preflight and auth.
- Live UI: debounce timing, a single network request, focus kept while results load, "No results", and paste truncation.

All of these belong to Test Bot's T-PAGING-007, which needs Neil to start PostgreSQL first.

## Changes since last review

Iteration 1: first review.

## Out of scope / pre-existing notes

These don't affect the verdict.

- **Unity.API `ToPagedList` / Contacts:** a heads-up only (P3 / P14). It's listed as do-not-copy in the rules.
- **Phase 2 (T-PAGING-008):** not started; it waits for Phase 1 approval (P13).
- **Dev Bot's interruption** (16:25-18:48, PC offline): the files are consistent (gate pass, manifest matches the modification times), and nothing is half-written.
- **Review Bot hygiene:** the copy left out `.env*`, `secrets.json`, `e2e/.auth`, `bin`/`obj` and build output (except the gate's own fake fixtures). No secret scan with real values was run this round, and no secret value was written anywhere. No sign-in, no process or container started or stopped, no framework docs edited.
