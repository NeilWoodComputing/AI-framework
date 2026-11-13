# Ticket: T-PAGING-006 — Paging rules in API.Framework and UI.NextJs.Framework

| Field | Value |
|-------|--------|
| ID | T-PAGING-006 |
| Type | Docs / rules |
| Feature | shared-paging |
| Priority | Medium |
| Owner | dev-bot |
| Specs | None; `plan.md` §5.5–5.6 |
| Journey (optional) | — |

## User story

**As** any agent building a list  
**I want** the framework rules to describe the shared paging way and the Unity.API anti-patterns  
**So that** new lists are built the same way and old mistakes are not copied

## Full-stack scope

No controls. Files (Dev Bot's own frameworks): API.Framework `.cursor/rules/api-framework-services.mdc`, `api-framework-controllers.mdc`, `api-framework-ui-contract.mdc`, `api-framework-testing.mdc` and their `.claude/rules/*.md` twins (plus `.claude/skills/api-framework-entity-list/SKILL.md` if it covers paging); UI.NextJs.Framework `.cursor/rules/framework/nextjs-entity-grid.mdc`.

## Work to do

1. Services: use `Paging/` helpers, `SortMap` with Id tie-break, typed `{Entity}Query` with `[StringLength]` and `ApplyFilters`, Contains on a normalised column; never copy the clamp.
2. Controllers: bind `[FromQuery] {Entity}Query`; 400 on validation; adjust (not reject) page size.
3. UI contract: query parameter names (pageIndex, pageSize, sortBy, sortDirection, search / searchText), cap 200, response shape unchanged.
4. Testing: unit tests on in-memory, order/search proven in e2e on PostgreSQL.
5. nextjs-entity-grid: `setFilters` resets to page 1 with ~300 ms debounce; `maxPageSize`.
6. List the Unity.API anti-patterns (plan.md §5.6) as "do not copy". Keep `.cursor` and `.claude` in step.

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-006/S<n>`); never renumber or reuse.

### Scenario: S1 — Rules exist in both rule sets

```gherkin
Given the four API.Framework rule topics
When the .cursor and .claude copies are compared
Then both describe the Paging helpers, SortMap tie-break and typed queries with the same content
```

### Scenario: S2 — Anti-patterns are listed

```gherkin
Given api-framework-services (both copies)
When I read the paging section
Then it lists ToPagedList skipping Skip/Take with totalRows, reflection sorting, sync Count/ToList, 50000 default, descending by default, EF.Property strings, unescaped LIKE, PaginatedResponse envelopes and cursor paging as do-not-copy
```

### Scenario: S3 — Entity grid rule covers filters

```gherkin
Given nextjs-entity-grid.mdc
When I read it
Then it says filter changes go through setFilters, reset to page 1 and debounce about 300 ms, and names maxPageSize 200
```

## Out of scope

- Changing Unity.API or its rules
- Review Bot / Test Bot framework files

## Notes

- Stable ID for DevOps upsert: `T-PAGING-006`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
