# Ticket: T-PAGING-007 — Scenario tests and e2e run for shared paging

| Field | Value |
|-------|--------|
| ID | T-PAGING-007 |
| Type | Release / verification |
| Feature | shared-paging |
| Priority | High |
| Owner | test-bot |
| Specs | All T-PAGING tickets; `plan.md` §5.7 |
| Journey (optional) | — |

## User story

**As** Neil, before merge  
**I want** the search and paging behaviour proven on the real database  
**So that** in-memory differences do not hide ordering or matching bugs

## Full-stack scope

No controls. Test Bot's own e2e area: `UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature`, `reference-data/ReferenceDataTypesGrid.feature` (+ new scenarios), run against the Test API on PostgreSQL.

## Work to do

1. Tag tests with the T-PAGING scenario IDs (T-PAGING-002/003/004/005).
2. Add an Animals search feature and a Reference Data Types search scenario.
3. Run the paging / sort regression on Animals and Reference Data; update order assertions only where Q12 allows.
4. Report in `tests/TEST-shared-paging-<n>-report.md`.

## Acceptance criteria

Scenario IDs are stable (`T-PAGING-007/S<n>`); never renumber or reuse.

### Scenario: S1 — Animals search on PostgreSQL

```gherkin
Given Test data with animals "Red Fox", "Fennec Fox" and "Badger"
When the Animals search scenarios (T-PAGING-002, T-PAGING-005) run against the Test API
Then every scenario passes on PostgreSQL
```

### Scenario: S2 — Reference Data Types search on PostgreSQL

```gherkin
Given the seeded reference data types
When I type part of a type name in "Filter types…"
Then only matching types are shown, from page 1, after one debounced request
```

### Scenario: S3 — Paging regression

```gherkin
Given the Animals and Reference Data grids
When I change page size (5–200), page and sort direction
Then totals, page contents and tie order are stable and match the API
```

## Out of scope

- Unity.API tests

## Notes

- Stable ID for DevOps upsert: `T-PAGING-007`
- Start condition met 2026-10-09 14:47 BST: system-rename merged (Neil's word) and this plan approved (plan.md §8).
- test-bot is never a handoff owner; this ticket owner is the testing agent for the scenario work only.
