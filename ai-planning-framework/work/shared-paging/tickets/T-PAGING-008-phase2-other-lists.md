# Ticket: T-PAGING-008 — Phase 2: Directory, Tenant, CatalogueItem and ComponentShowcase lists on shared paging

| Field | Value |
|-------|--------|
| ID | T-PAGING-008 |
| Type | Service API (cross-cutting) |
| Feature | shared-paging |
| Priority | Low |
| Owner | dev-bot |
| Specs | None; `plan.md` §1, §5.2 |
| Journey (optional) | — |

## User story

**As** the implementing agent  
**I want** the remaining list services on the shared Paging helpers  
**So that** no service keeps its own clamp or unstable sort

## Full-stack scope

No controls. `DirectoryService.cs` (helper :543; users :38, groups :182), `TenantService.cs:48`, `CatalogueItemService.cs:35`, `ComponentShowcaseService.cs:39`. `UserQuery` keeps `IncludeDeleted`.

## Work to do

1. Replace each copied clamp and sort switch with `SortMap` + `ToPagedBodyAsync`; keep current sort keys and defaults.
2. Typed queries keep existing filters (`UserQuery.IncludeDeleted`); no new search unless Neil asks.
3. Unit tests per service; Test Bot regression on the affected grids.

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-008/S<n>`); never renumber or reuse.

### Scenario: S1 — Lists keep their behaviour

```gherkin
Given each of the four list endpoints
When called with the same query before and after
Then the same rows are returned, except tie order which is now by Id (Q12)
```

### Scenario: S2 — Include deleted users still works

```gherkin
Given a soft-deleted user
When the users list is called with IncludeDeleted true
Then the deleted user is returned, and with false it is not
```

### Scenario: S3 — No copied clamp remains

```gherkin
Given the API.Framework source
When I search for `Math.Min(` with 200 in list services
Then only PageWindow contains the clamp
```

## Out of scope

- New search boxes on these lists

## Notes

- Stable ID for DevOps upsert: `T-PAGING-008`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
- Parkable (Q9): start only after Phase 1 is approved.
