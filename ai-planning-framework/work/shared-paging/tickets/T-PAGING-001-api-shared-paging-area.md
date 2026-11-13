# Ticket: T-PAGING-001 — Shared Paging area in Api.Framework.Services

| Field | Value |
|-------|--------|
| ID | T-PAGING-001 |
| Type | Service API (cross-cutting) |
| Feature | shared-paging |
| Priority | High |
| Owner | dev-bot |
| Specs | None (no UI controls); `plan.md` §5.1 |
| Journey (optional) | — |

## User story

**As** the implementing agent  
**I want** one shared place for paging contracts, defaults, the page window, sort maps and paged-body helpers  
**So that** no list service copies the clamp or hand-writes a sort switch, and every sort is stable

## Full-stack scope

No controls or DB columns. Code: new `Api.Framework.Services/Paging/` (`PagedQuery`, `PagingModel`, `PagedBody` moved from `Directory/DirectoryContracts.cs:6/19/30` with the same names and JSON; `PagingDefaults`; `PageWindow`; `SortMap<T>`; `ToPagedBodyAsync` / `ToPagedBody`). Consumers' `using` lines updated.

## Work to do

1. Move the three contracts to `Paging/` without changing property names, types or defaults (PageSize = 20). Update every `using`.
2. Add `PagingDefaults` (PageSize 20, MaxPageSize 200) and `PageWindow` (adjust, never reject: PageSize ≤ 0 → 20, > 200 → 200, PageIndex < 0 → 0).
3. Add `SortMap<T>`: case-insensitive key → expression whitelist, a default key, direction `asc` unless `desc`, always ending `ThenBy(Id)`. Unknown/empty key → default (Q1).
4. Add `ToPagedBodyAsync(IQueryable<T>, PagedQuery, SortMap<T>, projection)` (async CountAsync / ToListAsync, Skip/Take always applied) and an in-memory `ToPagedBody(IEnumerable<T>, …)`.
5. Unit tests in `Api.Framework.Tests` (new `Paging/` folder). Do not migrate any service here except as needed to compile (Animals / ReferenceData in T-PAGING-002/003; others in T-PAGING-008).

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-001/S<n>`); never renumber or reuse.

### Scenario: S1 — Page window adjusts out-of-range values

```gherkin
Given a PagedQuery with PageSize 0 and PageIndex -1
When PageWindow is computed
Then PageSize is 20 and PageIndex is 0
And a PageSize of 500 becomes 200 and no error is returned
```

### Scenario: S2 — Sort keys are case-insensitive and whitelisted

```gherkin
Given a SortMap with keys "name" and "dateBorn" and default "name"
When sortBy is "DATEBORN"
Then rows are ordered by DateBorn then Id
And when sortBy is "unknownColumn" or empty, rows are ordered by the default key then Id (Q1)
```

### Scenario: S3 — Ties are broken by Id

```gherkin
Given three rows with the same sort value and different Ids
When a page is requested ascending or descending on that key
Then the tied rows are always returned in Id order, on every call and across page boundaries
```

### Scenario: S4 — Paged body totals and window

```gherkin
Given 45 matching rows and PageSize 20
When PageIndex 2 is requested
Then data holds 5 rows
And pagination.totalRows is 45, pageIndex 2, pageSize 20
```

### Scenario: S5 — JSON shape is unchanged

```gherkin
Given an existing list endpoint (e.g. GET Animal) before and after the move
When its response is serialised
Then the property names and nesting of the paged body and pagination model are identical
```

## Out of scope

- Migrating Directory / Tenant / CatalogueItem / ComponentShowcase (T-PAGING-008)
- Cursor/keyset paging; response envelope changes

## Notes

- Stable ID for DevOps upsert: `T-PAGING-001`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
- Plan Bot spot-check: 7 `new PagedBody` sites in 6 services copy the clamp (plan.md §2).
