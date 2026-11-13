# Ticket: T-PAGING-004 — Entity grid setFilters with page reset and debounce

| Field | Value |
|-------|--------|
| ID | T-PAGING-004 |
| Type | UI framework (cross-cutting) |
| Feature | shared-paging |
| Priority | High |
| Owner | dev-bot |
| Specs | None; `plan.md` §5.3 |
| Journey (optional) | — |

## User story

**As** a user typing in any grid search box  
**I want** the grid to wait until I pause and then show page 1 of the results  
**So that** I see correct results without a request per keystroke

## Full-stack scope

No controls. Code: `src/framework/entity-framework/hooks/use-entity-grid-state.ts` (new `setFilters`), `grid/entity-grid-config.ts` (export `maxPageSize = 200`), `features/reference-data/reference-data-types-grid/ReferenceDataTypesGrid.tsx` (use `setFilters`), optionally `utils/normalize-paged-search-response.ts` (Q14).

## Work to do

1. Add `setFilters(patch)` to `EntityGridState`: merge the patch, set `pageIndex: 0`, keep sort and page size, debounce ~300 ms (Q5); apply only the latest response.
2. Export `maxPageSize = 200` next to `defaultPagingOptions` (unchanged `[5, 10, 20, 50, 100, 200]`) (Q11).
3. Switch `ReferenceDataTypesGrid` to `setFilters({ searchText })`; the input value still updates immediately.
4. Q14: trim `normalizePagedSearchResponse` only if no caller needs Unity.API shapes.
5. Vitest unit tests for the hook.

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-004/S<n>`); never renumber or reuse.

### Scenario: S1 — Typing waits for a pause

```gherkin
Given the Reference Data Types grid is on page 1
When I type "cou" quickly (under 300 ms between keys)
Then exactly one search request is sent, about 300 ms after the last key
And it carries searchText "cou"
```

### Scenario: S2 — Filters go back to page 1

```gherkin
Given the grid is on page 3 sorted by Display Name descending with page size 50
When I change the search text
Then the next request has pageIndex 0, the same sort and page size 50
```

### Scenario: S3 — Only the latest response is shown

```gherkin
Given a slow response for "co" and a fast one for "cou"
When both return, "co" last
Then the grid shows the results for "cou"
```

### Scenario: S4 — Page size cap is exported

```gherkin
Given the entity grid config module
When maxPageSize is imported
Then it is 200 and equals the largest default page-size option
```

## Out of scope

- Search / paging in the URL (Q8)
- New search boxes on other grids (Animals is T-PAGING-005)

## Notes

- Stable ID for DevOps upsert: `T-PAGING-004`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
