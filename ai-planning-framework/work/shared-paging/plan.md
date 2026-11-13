# Plan: Shared paging (API.Framework + UI.NextJs.Framework)

> Status: **planned**, owner dev-bot, **approved** (plan_to_code, Neil 2026-10-09 14:47 BST). Start condition met (§8). Written by Plan Bot 2026-10-09 from Dev Bot's design; Neil approved the Animals search and at 14:47 BST accepted all 15 answers in §7 (decisions P5–P19 in §6).

## 1. Summary

Every paged list in API.Framework copies the same paging clamp and has its own sort switch. Several sorts have no stable tie-break, and the ReferenceData search box sends `searchText` that the API never reads. This feature moves paging into one shared `Paging/` area in Api.Framework.Services. It covers the contracts, defaults, the page window, a whitelisted sort map with a final `Id` tie-break, and `ToPagedBody` helpers. It adds typed query classes with filters and gives the Next.js entity grid one way to change filters: back to page 1, after a short debounce.

- **Phase 1:** Animals (new Name search, approved by Neil; see manage-animals decision 31) and ReferenceData (the existing search box gets the API and debounce fix only).
- **Phase 2:** Directory users and groups, Tenants, CatalogueItems and ComponentShowcases move to the shared helpers. This phase can be parked (Q9).

## 2. Evidence (Plan Bot spot-check 2026-10-09, read-only, machine copy)

| Claim (Dev Bot) | Result | Where |
|---|---|---|
| Paging contracts live in Directory | **Confirmed.** `PagedQuery` (PageIndex, PageSize = 20, SortBy, SortDirection, IncludeDeleted), `PagingModel`, `PagedBody` | `Api.Framework.Services/Directory/DirectoryContracts.cs:6/19/30` |
| The clamp is copied per service | **Confirmed: 7 `new PagedBody` sites in 6 services.** `PageSize<=0 ? 20 : Math.Min(PageSize, 200)` and `Math.Max(PageIndex, 0)` | AnimalService:35, DirectoryService:543 (generic helper for users :38 and groups :182), TenantService:48, CatalogueItemService:35, ComponentShowcaseService:39, ReferenceDataService:112 (items) and :397 (types, in-memory) |
| ReferenceData has its own window | **Confirmed.** A private `PageWindow` | `ReferenceDataService.cs:413` |
| ReferenceData search is ignored by the API | **Confirmed.** `ListTypes` and `ListItems` bind `[FromQuery] PagedQuery`, which has no `SearchText` | ReferenceDataController (`GET ReferenceData`, `GET ReferenceData/{type}`) |
| ReferenceData sorts have no tie-break | **Confirmed.** Types: in-memory sort (`CompareTypes`, ordinal ignore case), then `Reverse()` for desc, which also reverses ties. Items: `ApplyItemSort` on code / description / displayName, with no `Id` tie-break | `ReferenceDataService.cs` |
| ReferenceData UI search does not go back to page 1 | **Not confirmed; corrected.** `ReferenceDataTypesGrid.tsx:70` already sends `{ searchText, pageIndex: 0 }`. The real gaps: there is **no debounce** (a request on every keystroke) and the API ignores the text. The box is on the **Types grid only**; `ManageReferenceDataItemsModal` has no search box | `features/reference-data/reference-data-types-grid/ReferenceDataTypesGrid.tsx:64-74` |
| Animals have no filters | **Confirmed.** `public class AnimalQuery : PagedQuery;`. Sort keys isfurry / hashooves / dateborn / updatedutc, then `ThenBy(Name)`, default Name. No `Id` tie-break, but Name is unique among active rows | `Api.Framework.Services/Animals/` |
| A normalised Name column exists | **Confirmed.** `Animal.NormalizedName` = `Name.Trim().ToUpperInvariant()`: case-insensitive, **not** accent-insensitive. Max length 100. Unique index `ix_animals_normalized_name_active` (filtered `NOT is_deleted`). Spelling in code: "Normalized" | `Animal.cs:9`, `LoginDbContext.cs:460-467` |
| UI grid state | `useEntityGridState` has `onPageChanged` and `setSort` (sort resets `pageIndex: 0`) but no filter setter and no debounce. The only `debounce` in the UI is in `JsonSchemaForm` | `framework/entity-framework/hooks/use-entity-grid-state.ts` |
| Page-size options | `defaultPagingOptions = [5, 10, 20, 50, 100, 200]`; there is no exported `maxPageSize` | `framework/entity-framework/grid/entity-grid-config.ts:6` |
| Grid state in the URL | No list page puts paging, sort or search in the URL. `searchParams` are used only for ReferenceData `isEnumeration` | `src/app/examples/reference-data/...` |
| Unit tests run on EF in-memory | **Confirmed.** `UseInMemoryDatabase` at :11 (line 19 builds Npgsql options with `Host=unused`, so no live database) | `Api.Framework.Tests/Helpers/TestDbFactory.cs:11` |
| e2e coverage today | `ManageAnimalsGrid.feature` and `ReferenceDataTypesGrid.feature` exist. The ReferenceData feature has **no** search / filter scenario | `UI.NextJs.Framework/e2e/features/` |

## 3. Actors and ownership

| Who | Owns |
|---|---|
| dev-bot | All API.Framework and UI.NextJs.Framework code, and the rule files in both frameworks (T-PAGING-001…006, 008) |
| test-bot | Scenario tests, e2e runs and the regression run (T-PAGING-007) |
| review-bot | Code and test review (no ticket) |
| plan-bot | This plan, the manage-animals spec, the Excel and the decision (done in this planning step) |
| human (Neil) | Answers §7, approves plan_to_code and merge |

## 4. Scope

In scope:
- **Phase 1:** shared Paging area; Animals search and sort map; ReferenceData `SearchText` and sort maps; the UI `setFilters` with debounce; the Animals search box; rule updates; tests.
- **Phase 2 (parkable):** the remaining four services move to the shared helpers.

Out of scope:
- Unity.API, including its `ToPagedList` (heads-up only, §5.6).
- Cursor or keyset paging, and response envelope changes. JSON names stay the same.
- Accent-insensitive search.
- Full-text or trigram indexes.
- A search box on the ReferenceData Items modal.
- Search, paging or sort in the URL.
- Export or "select all".

## 5. Design (Dev Bot's design; each (Qn) points to the accepted answer in §7 / decision in §6)

### 5.1 API: `Api.Framework.Services/Paging/`

- Move `PagedQuery`, `PagingModel` and `PagedBody` here **with the same names and JSON shapes**. Only the namespace changes, and consumers update their `using`.
- `PagingDefaults`: PageSize 20, MaxPageSize 200 (Q11).
- `PageWindow`: **adjust, do not reject**. PageSize ≤ 0 becomes 20, above 200 becomes 200, and a negative PageIndex becomes 0. It replaces the copied clamp and ReferenceData's private window.
- `SortMap<T>`: a whitelist of sort keys (case-insensitive) mapped to expressions. An unknown or empty key uses the default sort (Q1). It always ends with `ThenBy(x => x.Id)`. Direction is `asc` unless `desc` is given.
- `ToPagedBodyAsync(IQueryable<T>, PagedQuery, SortMap<T>, projection)` uses async `CountAsync` and `ToListAsync`, with Skip/Take always applied. An in-memory `ToPagedBody(IEnumerable<T>, …)` serves ReferenceData Types.

### 5.2 Typed queries

- `{Entity}Query : PagedQuery` has `[StringLength]` filter properties and an `ApplyFilters(IQueryable<T>)` method.
- Text matching uses `Contains` on a **normalised** column, with the input normalised the same way in C#. The match is the same on in-memory and PostgreSQL, and `%`, `_` and `\` match literally (no hand-built `LIKE`).
- `AnimalQuery.Search`: max 100 (Q6). It is trimmed, and blank means no filter. Matching is `NormalizedName.Contains(search.Trim().ToUpperInvariant())`, case-insensitive and accent-sensitive (Q2, Q3), from 1 character (Q4). Bound as the `search` query parameter on `GET Animal`.
- `ReferenceDataQuery.SearchText`: max 100. On the Types list it matches `ReferenceDataType` or `DisplayName`, contains, case-insensitive (Q13). Items get the shared sort map and window only.
- Phase 2: `UserQuery` keeps `IncludeDeleted`, and the other lists keep their current filters.

### 5.3 UI: `UI.NextJs.Framework/src/framework/entity-framework/`

- `useEntityGridState` gets `setFilters(patch)`. It merges the patch, sets `pageIndex: 0`, keeps the sort and page size, and **debounces ~300 ms** (Q5). Only the last request's result is shown.
- `entity-grid-config.ts` exports `maxPageSize = 200`, and `defaultPagingOptions` stays `[5, 10, 20, 50, 100, 200]` (Q11).
- `ReferenceDataTypesGrid` uses `setFilters({ searchText })` instead of calling `setSearchRequest` on every keystroke.
- Optional: trim `normalizePagedSearchResponse` (46 lines) to the one response shape API.Framework returns (Q14).

### 5.4 Animals search box (manage-animals spec, decision 31)

- A text input "Search animals" above the grid on `/examples/animals`, `maxLength` 100.
- It uses `setFilters({ search })`, and a search that matches nothing shows the framework "No results" message (Q7).
- It is not kept in the URL (Q8).
- Full row: `ai-planning-framework/work/manage-animals/specs/manage-animals.yaml › search_filters`.

### 5.5 Rules (Dev Bot updates its own framework rules)

- API.Framework: `api-framework-services`, `api-framework-controllers`, `api-framework-ui-contract` and `api-framework-testing`, in **both** `.cursor/rules/*.mdc` and `.claude/rules/*.md`. Add `.claude/skills/api-framework-entity-list/SKILL.md` if it describes paging.
- UI.NextJs.Framework: `.cursor/rules/framework/nextjs-entity-grid.mdc` (the UI has no `.claude` rules).
- Content:
  - use the Paging helpers and never copy the clamp;
  - a SortMap with an Id tie-break;
  - typed queries with `[StringLength]`;
  - Contains on a normalised column;
  - `setFilters` resets to page 1 and debounces;
  - the anti-patterns in §5.6.

### 5.6 Unity.API patterns not to copy (list in the rules)

- `ToPagedList` skips Skip/Take when `totalRows` is passed in. Contacts uses this path, so **it loads every row**. This is a **heads-up for Neil only**: no ticket and no Unity.API change (Q10).
- Reflection or string-based sorting, and `EF.Property` strings.
- Synchronous `Count()` / `ToList()`.
- A default page size of 50000.
- Descending by default.
- Unescaped `LIKE` built from user input.
- `PaginatedResponse` envelopes.
- Cursor paging.

### 5.7 Tests

- **Unit (dev-bot, Api.Framework.Tests, in-memory):**
  - PageWindow edges (0, -1, 201, a negative index);
  - SortMap (case-insensitive key, unknown key falls back, Id tie-break, desc);
  - ToPagedBody totals;
  - Animals search (case, trim, blank, literal `%`/`_`, over 100 → 400);
  - ReferenceData Types search;
  - a Vitest for `setFilters` (page reset, debounce, last-response-wins).
- **e2e (test-bot, after hand-off):** Animals search, ReferenceData Types search, and a paging / sort regression on the Animals and ReferenceData grids, run against PostgreSQL.

## 6. Decisions

| # | Decision | Source |
|---|---|---|
| P1 | Manage Animals gets a Name search box (server-side) | Neil, 2026-10-09 (approved with Dev Bot's design); manage-animals decision 31 |
| P2 | ReferenceData search gets the API and debounce fix only (no new UI) | Neil, 2026-10-09 13:53 BST |
| P3 | Unity.API `ToPagedList` / Contacts is a heads-up note only | Neil, 2026-10-09 13:53 BST ("Neil's call") |
| P4 | Start only after system-rename is merged (Neil's word) | Neil, 2026-10-09 13:53 BST. **Met:** Neil treated system-rename as merged at 14:47 BST |
| P5 | An unknown or empty `sortBy` falls back to the list's default sort (no 400) (Q1) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P6 | Animals search covers Name only (not Attributes) (Q2) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P7 | Case-insensitive, accent-sensitive, using the existing `NormalizedName` (Q3) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P8 | Search starts from 1 character; trimmed; whitespace only = no filter (Q4) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P9 | Debounce 300 ms (Q5) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P10 | Maximum search length 100 (the UI stops at 100; the API returns 400 above it) (Q6) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P11 | No match shows the framework "No results"; "+ Add Animal" stays (Q7) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P12 | Search, page and sort are not kept in the URL (Q8) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P13 | Phase 2 is planned as T-PAGING-008, started only after Phase 1 is approved; parkable (Q9) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P14 | Unity.API Contacts / `ToPagedList` is a heads-up only; no ticket or Unity.API change (Q10) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P15 | Page size cap 200; the UI exports `maxPageSize = 200`; the API lowers larger values to 200 (Q11) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P16 | Row-order changes among tied rows (Id tie-break, no `Reverse()`) are accepted; Test Bot updates order assertions (Q12) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P17 | ReferenceData search is on the Types grid only: `ReferenceDataType` or `DisplayName`, contains, case-insensitive (Q13) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P18 | Trim `normalizePagedSearchResponse` only if Dev Bot confirms no caller needs Unity.API shapes (Q14) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |
| P19 | manage-animals stays merged and its handoff unchanged; the build is tracked in shared-paging (Q15) | Neil, 2026-10-09 14:47 BST (suggested answer accepted) |

## 7. Questions — all answered (Neil, 2026-10-09 14:47 BST: every suggested answer accepted; decisions P5–P19 in §6)

| # | Question | Accepted answer |
|---|---|---|
| Q1 | Unknown or empty `sortBy`: fall back to the default sort, or return 400? | **Fall back** to the list's default sort (same as today's switch defaults). The UI only sends whitelisted keys |
| Q2 | Animals search columns: Name only, or Name + Attributes? | **Name only.** Attributes are `jsonb`, so searching them needs a different query and index |
| Q3 | Case and accent sensitivity | **Case-insensitive, accent-sensitive**, using the existing `NormalizedName` (`ToUpperInvariant`). Accent-insensitive search would need the `unaccent` extension or a new column, which is out of scope |
| Q4 | Minimum search length: 1 or 2? | **1 character** (trimmed; whitespace only = no filter) |
| Q5 | Debounce | **300 ms** |
| Q6 | Maximum search length | **100**, the same as `NormalizedName`. The UI stops input at 100 and the API returns 400 above it (`[StringLength(100)]`) |
| Q7 | Text when a search matches nothing | **Keep the framework "No results"** (manage-animals Q37). "+ Add Animal" stays |
| Q8 | Put search, page and sort in the URL? | **No.** No grid does this today; it would be a separate feature |
| Q9 | Phase 2 (Directory users / groups, Tenants, CatalogueItems, ComponentShowcases): planned or parked? | **Planned** as T-PAGING-008, started only after Phase 1 is approved. Neil may park it |
| Q10 | Unity.API Contacts loads all rows (`ToPagedList` with `totalRows`) | **Heads-up only.** Listed in §5.6 and the rules; no ticket or Unity.API change unless Neil asks |
| Q11 | Page size cap 200 vs the UI options 5–200 | **Keep cap 200** (the largest option). The UI exports `maxPageSize = 200`; the API adjusts larger values to 200 rather than rejecting them |
| Q12 | Sign-off on row-order changes (the Id tie-break, plus ReferenceData Types desc no longer reversing ties) | **Accept.** Only rows with equal sort values can move. Test Bot updates any order assertions |
| Q13 | ReferenceData search: which list and columns? | **Types grid only** (the only search box): `ReferenceDataType` or `DisplayName`, contains, case-insensitive. Items get the sort map and window only (no search box exists) |
| Q14 | Trim `normalizePagedSearchResponse` to API.Framework's single shape? | **Yes, if** Dev Bot confirms that no UI caller relies on Unity.API shapes. Otherwise leave it as is |
| Q15 | manage-animals is merged: do the spec / Excel / decision 31 changes reopen it? | **No.** manage-animals stays merged and unchanged in its handoff. The build is tracked here (T-PAGING-005) |

## 8. Start condition and delivery slices

**Start condition:** after `work/system-rename` is merged on Neil's word, and after Neil approves this plan (`plan_to_code`). On 2026-10-09 at 13:56 BST system-rename was `approved`, waiting for Neil's merge decision. **Met 2026-10-09 14:47 BST:** Neil treated system-rename as merged and approved this plan; Dev Bot may start.

| Slice | Tickets | Owner |
|---|---|---|
| 1. Shared Paging area | T-PAGING-001 | dev-bot |
| 2. Animals search (API) + ReferenceData query (API) | T-PAGING-002, T-PAGING-003 | dev-bot |
| 3. UI setFilters / debounce + Animals search box | T-PAGING-004, T-PAGING-005 | dev-bot |
| 4. Rules | T-PAGING-006 | dev-bot |
| 5. Scenario tests / e2e | T-PAGING-007 | test-bot |
| 6. Phase 2 (parkable, Q9) | T-PAGING-008 | dev-bot |

## 9. Risks

- **In-memory provider vs PostgreSQL.**
  - Unit tests run on EF in-memory, and string ordering differs: ordinal in memory, collation in PostgreSQL. Order and search assertions must be proven by the Test Bot e2e run against PostgreSQL.
  - Matching on `NormalizedName` with C#-normalised input keeps search consistent across both providers.
- **Row-order changes** (Q12): the Id tie-break, and ReferenceData Types desc no longer using `Reverse()`. Existing e2e checks that assume an order may need updating.
- **Namespace move:** moving the contracts out of `Directory` changes `using` lines in every list service and test. JSON names must stay identical (covered by T-PAGING-001/S5).
- **Index use:** `Contains` (`%x%`) cannot use the btree index on `normalized_name`. That is fine at example scale; a trigram index is out of scope.
- **Request races:** debounced typing can still return responses out of order. The UI keeps only the latest response (T-PAGING-004/S3).
