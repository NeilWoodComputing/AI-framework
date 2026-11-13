# Ticket: T-PAGING-002 — Animals list: Name search and shared sort map

| Field | Value |
|-------|--------|
| ID | T-PAGING-002 |
| Type | Service API |
| Feature | shared-paging |
| Priority | High |
| Owner | dev-bot |
| Specs | `ai-planning-framework/work/manage-animals/specs/manage-animals.yaml` (search_filters, pagination); `plan.md` §5.2 |
| Journey (optional) | — |

## User story

**As** a user managing animals  
**I want** to find animals by part of their name  
**So that** I do not page through the whole catalogue

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|---|---|---|---|---|
| Search animals | Text input (search box) | Animals | Animal | Animal.Name (matched on Animal.NormalizedName) |
| Name, Is Furry, Has Hooves, Date Born, Last Amended | Sortable grid columns | Animals | Animal | Animal.Name / IsFurry / HasHooves / DateBorn / UpdatedUtc |

## Work to do

1. `AnimalQuery : PagedQuery` gains `Search` with `[StringLength(100)]` (Q6) and `ApplyFilters`: trimmed; blank = no filter; else `NormalizedName.Contains(search.Trim().ToUpperInvariant())` (Q2, Q3, Q4).
2. `GET Animal` binds the `search` query parameter. Non-deleted rows only, as today.
3. Replace AnimalService's sort switch (keys name, isfurry, hashooves, dateborn, updatedutc) with a `SortMap<Animal>` (default name asc, final ThenBy Id) and `ToPagedBodyAsync`.
4. Unit tests (in-memory) for every scenario below.

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-002/S<n>`); never renumber or reuse.

### Scenario: S1 — Search matches part of the name, any case

```gherkin
Given non-deleted animals "Red Fox", "Fennec Fox" and "Badger"
When GET Animal is called with search "fOx"
Then data holds "Fennec Fox" and "Red Fox" in Name order
And pagination.totalRows is 2
```

### Scenario: S2 — Blank search returns everything

```gherkin
Given the same animals
When GET Animal is called with search "   " or without search
Then all non-deleted animals are returned, sorted by Name ascending
```

### Scenario: S3 — Search characters are literal

```gherkin
Given an animal named "100% Owl" and one named "Owl"
When GET Animal is called with search "%"
Then only "100% Owl" is returned
And search "_" returns only names containing an underscore
```

### Scenario: S4 — Deleted animals never match

```gherkin
Given a soft-deleted animal "Grey Fox" (Animal.IsDeleted = true)
When GET Animal is called with search "fox"
Then "Grey Fox" is not returned
```

### Scenario: S5 — Over-long search is rejected

```gherkin
Given a search of 101 characters
When GET Animal is called
Then the API returns 400 with a validation message for search
And no rows are returned
```

### Scenario: S6 — Search keeps sort and paging

```gherkin
Given 25 animals whose names contain "a"
When GET Animal is called with search "a", sortBy "dateBorn", sortDirection "desc", pageSize 20, pageIndex 1
Then data holds the last 5 matches ordered by DateBorn descending then Id
And pagination.totalRows is 25
```

## Out of scope

- Searching Attributes (Q2)
- Accent-insensitive matching (Q3)
- Any change to create / update / delete

## Notes

- Stable ID for DevOps upsert: `T-PAGING-002`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
- Neil approved the Animals search (manage-animals decision 31). Search details accepted by Neil 2026-10-09 14:47 BST (plan.md P6–P8, P10).
