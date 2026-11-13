# Ticket: T-ANIMAL-005 — Soft delete Animal with confirmation

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-005 |
| Type | Cross-cutting |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Depends on | T-ANIMAL-002 (`DELETE v1/Animal/{id}`), T-ANIMAL-003 (Actions column wiring), T-ANIMAL-007 (shared Actions column) |
| Decisions | `plan.md` › Decisions 2, 3, 11 (superseded by 22), 18, 20, 22 / 24 (single permission `animals_write`), 23 / 26 (Delete Animal in the row actions menu) |
| Open questions | None. Q32 (row actions menu details; affects how the menu looks, not the delete flow): Neil accepted the suggested defaults for all remaining questions at 2026-10-08 15:44 BST |

## User story

**As a** administrator  
**I want** to soft-delete an animal from Manage Animals after confirmation  
**So that** the animal no longer appears in the list but is not hard-deleted

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Delete Animal | Row actions menu item in the Actions column, after Edit Animal (`animals_write`; decision 26) | Animals | Animal (creatures.animals) | Soft delete (IsDeleted = true; UpdatedUtc & UpdatedBy set) |
| Name (list exclusion) | Results column | Animals | Animal (creatures.animals) | Animal.Name (non-deleted only) |

## Work to do

1. Delete Animal is an item of each row's **actions menu** in the Manage Animals **Actions column** (the last column; decisions 23, 26), listed after Edit Animal, with `Icon` `Delete`. It needs `animals_write` (decisions 22, 24; the whole page needs it) and opens the framework `ConfirmModal` titled "Delete &lt;Name&gt;?" with Cancel and Delete buttons.
2. On Delete, call `DELETE v1/Animal/{id}`; the Animals service sets `IsDeleted = true` (no hard delete).
3. Refresh the results list so the row no longer appears. There is no "show deleted" option and no restore.

## Acceptance criteria

### Scenario: S1 — Confirmation names the animal

```gherkin
Given I have permission animals_write
And an Animal named "Bessie" is shown on Manage Animals
When I open that row's actions menu in the Actions column and choose Delete Animal
Then a confirmation modal shows "Delete Bessie?"
And it offers Cancel and Delete buttons
```

### Scenario: S2 — Soft delete removes row from the list

```gherkin
Given the confirmation "Delete Bessie?" is open
When I click Delete
Then the Animals service soft-deletes that Animal
And the row no longer appears on Manage Animals
And the Animal row remains in storage with Animal.IsDeleted = true
```

### Scenario: S3 — Cancel leaves the animal unchanged

```gherkin
Given an Animal row is shown on Manage Animals
When I choose Delete Animal from the row's actions menu and cancel the confirmation
Then no soft-delete is performed via the Animals service
And the row remains visible on Manage Animals
```

### Scenario: S4 — Deleted animal is gone everywhere but its name is free

```gherkin
Given "Bessie" has been soft-deleted
When I open "Bessie" by its id
Then the Animals service returns not found
When I add a new animal named "Bessie" with a valid Date Born
Then the save succeeds
```

### Scenario: S5 — Users without animals_write cannot delete

```gherkin
Given I am signed in without permission animals_write
When I try to open Manage Animals
Then it does not open, so Delete Animal is never offered to me
And DELETE v1/Animal/{id} is rejected with 403 Forbidden
And the same 403 applies to a user with user_management_write but not animals_write
```

Checklist (derived from scenarios):

- [ ] Confirmation "Delete <Name>?" with Cancel / Delete before soft delete
- [ ] Soft delete via `Animals` sets Animal.IsDeleted; list excludes deleted rows
- [ ] Delete Animal is a row actions menu item after Edit Animal (decision 26), only for `animals_write` (decision 24)

## Out of scope

- Hard delete / purge
- Restoring soft-deleted animals or an "include deleted" filter (decision 2)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-005`
- Matches Contacts soft-delete pattern
- Decisions 22 and 23 (Neil, 2026-10-08 14:47 BST) left Delete's place open (Q31). Decision 26 (Neil, 15:17 BST) answered it: Edit and Delete are both in an actions menu on the row, in the Actions column. Decision 24: one permission `animals_write`; users without it cannot open Manage Animals at all. S5 (was "Read-only users cannot delete") was rewritten in place.
- Scenario IDs frozen 2026-10-08 from current positions (S1-S5; ticket heading IDs T-ANIMAL-005/S<n> for tests; doc-only, no wording or behaviour change).
