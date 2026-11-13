# Ticket: T-PAGING-005 — Manage Animals: Search animals box

| Field | Value |
|-------|--------|
| ID | T-PAGING-005 |
| Type | Paginated grid |
| Feature | shared-paging |
| Priority | High |
| Owner | dev-bot |
| Specs | `ai-planning-framework/work/manage-animals/specs/manage-animals.yaml` (search_filters); `excel/manage-animals.xlsx` |
| Journey (optional) | — |

## User story

**As** a user managing animals  
**I want** a search box above the Animals grid  
**So that** I can find an animal by name quickly

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|---|---|---|---|---|
| Search animals | Text input (search box), placeholder "Search animals…", maxLength 100 | Animals | Animal | Animal.Name (matched on Animal.NormalizedName) |

## Work to do

1. Add the search input on `/examples/animals` above the grid (header actions area, like ReferenceData), placeholder "Search animals…", `maxLength` 100, tid `animals-search`.
2. `AnimalsSearchRequest` gains `search?: string`; the box calls `setFilters({ search })` (T-PAGING-004).
3. No match shows the framework "No results"; "+ Add Animal" stays (Q7). Not kept in the URL (Q8).
4. Unit test the wiring; Test Bot covers e2e (T-PAGING-007).

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-005/S<n>`); never renumber or reuse.

### Scenario: S1 — Search narrows the grid

```gherkin
Given animals "Red Fox", "Fennec Fox" and "Badger" exist
When I type "fox" in Search animals and pause
Then the grid shows Fennec Fox and Red Fox only, sorted by Name ascending
And the results come from the Animals list via Animal.NormalizedName
```

### Scenario: S2 — No match shows No results

```gherkin
Given no animal name contains "zzz"
When I search "zzz"
Then the results area shows "No results"
And "+ Add Animal" is still available
```

### Scenario: S3 — Clearing the box restores the list

```gherkin
Given a search "fox" is applied
When I clear the box
Then all non-deleted animals are shown from page 1
```

### Scenario: S4 — Search goes back to page 1

```gherkin
Given more than 20 animals and the grid on page 2
When I search "a"
Then page 1 of the matching animals is shown with the same sort and page size
```

### Scenario: S5 — Input stops at 100 characters

```gherkin
Given the Search animals box
When I paste 120 characters
Then only the first 100 are kept
```

## Out of scope

- Searching Attributes; accent-insensitive search
- Search in the URL

## Notes

- Stable ID for DevOps upsert: `T-PAGING-005`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
- manage-animals decision 31; spec search_filters updated 2026-10-09; details accepted by Neil 2026-10-09 14:47 BST (plan.md P6–P12).
