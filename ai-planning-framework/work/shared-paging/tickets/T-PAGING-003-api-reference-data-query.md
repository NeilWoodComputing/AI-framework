# Ticket: T-PAGING-003 — ReferenceData: SearchText on Types, shared window and sort maps

| Field | Value |
|-------|--------|
| ID | T-PAGING-003 |
| Type | Service API |
| Feature | shared-paging |
| Priority | High |
| Owner | dev-bot |
| Specs | None (existing ReferenceData pages; no spec in ai-planning-framework); `plan.md` §5.2 |
| Journey (optional) | — |

## User story

**As** a user on the Reference Data page  
**I want** the existing "Filter types…" box to actually filter the list  
**So that** typing in it is not silently ignored

## Full-stack scope

No spec. Existing UI: `ReferenceDataTypesGrid.tsx` input tid `reference-data-search` sends `searchText`. API: `ReferenceDataController` `GET ReferenceData` (types) and `GET ReferenceData/{type}` (items) bind `PagedQuery` today; `ReferenceDataService.cs` :112 (items), :397 (types, in-memory), private `PageWindow` :413.

## Work to do

1. Add `ReferenceDataQuery : PagedQuery` with `SearchText` (`[StringLength(100)]`); bind it on `GET ReferenceData`.
2. Types: filter in memory on `ReferenceDataType` or `DisplayName`, contains, case-insensitive (Q13); sort with a `SortMap` (no `Reverse()`), final tie-break Id; page with the shared `ToPagedBody`.
3. Items: shared `PageWindow` and a `SortMap` (code, description, displayName; final Id). No search (no UI box).
4. Remove the private `PageWindow`. Unit tests for the scenarios.

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-003/S<n>`); never renumber or reuse.

### Scenario: S1 — Types search filters the list

```gherkin
Given reference data types including "Country" (display "Countries") and "Title"
When GET ReferenceData is called with searchText "COUNT"
Then only the "Country" type is returned
And pagination.totalRows is 1
```

### Scenario: S2 — Display name is searched too

```gherkin
Given a type whose DisplayName contains "Gender" but whose ReferenceDataType does not
When GET ReferenceData is called with searchText "gender"
Then that type is returned
```

### Scenario: S3 — Descending sort keeps a stable tie order

```gherkin
Given two types with the same sort value
When GET ReferenceData is called with sortDirection "desc" twice
Then both calls return the tied types in Id order
```

### Scenario: S4 — Items paging and sort are stable

```gherkin
Given items of one type with equal displayName values
When GET ReferenceData/{type} is called with sortBy "displayName" and pageSize 200
Then ties are ordered by Id
And a pageSize of 500 is adjusted to 200
```

### Scenario: S5 — Over-long searchText is rejected

```gherkin
Given a searchText of 101 characters
When GET ReferenceData is called
Then the API returns 400 with a validation message for searchText
```

## Out of scope

- A search box on the Items modal (Q13)
- Changing ReferenceData create / update

## Notes

- Stable ID for DevOps upsert: `T-PAGING-003`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
- Plan Bot spot-check: the UI already resets to page 1 (`ReferenceDataTypesGrid.tsx:70`); the gaps are the ignored searchText and no debounce.
