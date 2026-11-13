# GitHub Publish Plan — Manage Animals (DRY-RUN)

**Generated:** 2026-11-13  
**Feature:** manage-animals  
**Target:** `tickets.github` → NeilWoodComputing/ai-framework-tests  
**Project:** AI testing  
**Mode:** DRY-RUN (no issues created)

---

## Summary

- **Total tickets:** 9
- **Stories (issues):** 9
- **Child tasks (sub-issues):** 0
- **Upsert strategy:** Search by stable ID label or title prefix `[T-ANIMAL-NNN]`

---

## Ticket: T-ANIMAL-001

**Action:** CREATE (no existing issue found with label `T-ANIMAL-001`)

**Title:** `[T-ANIMAL-001] Animal schema / persistence (Schema)`

**Labels:**
- `T-ANIMAL-001`
- `manage-animals`
- `schema`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** administrator  
**I want** an Animal table with the columns required by Manage Animals and Add | Edit Animal  
**So that** animal data can be persisted and listed reliably

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input / results | Animals | Animal (creatures.animals) | Name |
| (no control) | Persistence only | Animals | Animal (creatures.animals) | NormalizedName (derived from Name) |
| Date Born | Date Picker / results | Animals | Animal (creatures.animals) | DateBorn |
| Attributes | Tag Input / results | Animals | Animal (creatures.animals) | Attributes |
| Is Furry | Switch / results | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch / results | Animals | Animal (creatures.animals) | HasHooves |
| Last Amended | Results column | Animals | Animal (creatures.animals) | UpdatedUtc & UpdatedBy (→ User.DisplayName, fallback User.Email) |
| (soft delete) | Persistence | Animals | Animal (creatures.animals) | IsDeleted |

## Work to do

1. Add EF model `Api.Framework.Data/Models/Animal.cs` and `DbSet<Animal> Animals` on `LoginDbContext`...
2. Columns (global table — no tenant id)...
3. Unique index on `NormalizedName` filtered to non-deleted rows...
4. Add the EF migration in `Api.Framework.Data/Migrations`...
5. Privileges: the API applies migrations at start-up...
6. Animals permission (decisions 22, 24, 25)...

## Acceptance criteria

- [ ] S1 — Animal table stores all mapped columns
- [ ] S2 — Attributes default to an empty array
- [ ] S3 — NormalizedName is unique among non-deleted rows
- [ ] S4 — UpdatedBy FK enforces referential integrity
- [ ] S5 — animals_write permission is seeded
- [ ] S6 — Administrators and Standard groups receive animals_write
- [ ] S7 — Migration creates creatures schema and animals table

## Out of scope

- Seeding sample animal data
- Back-filling the permission to existing non-default tenant groups
- Granting the DB user schema creation privileges (assumed present)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-001-animal-schema.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Sub-issues:** None (standalone issue)

---

## Ticket: T-ANIMAL-002

**Action:** CREATE (no existing issue found with label `T-ANIMAL-002`)

**Title:** `[T-ANIMAL-002] Animals service (API service)`

**Labels:**
- `T-ANIMAL-002`
- `manage-animals`
- `api-service`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** developer  
**I want** an Animals service that wraps Animal CRUD  
**So that** Manage Animals and Add | Edit Animal can persist data through a single service

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input / results | Animals | Animal (creatures.animals) | Name |
| Date Born | Date Picker / results | Animals | Animal (creatures.animals) | DateBorn |
| Attributes | Tag Input / results | Animals | Animal (creatures.animals) | Attributes |
| Is Furry | Switch / results | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch / results | Animals | Animal (creatures.animals) | HasHooves |
| Last Amended | Results column | Animals | Animal (creatures.animals) | UpdatedUtc & UpdatedBy |

## Work to do

1. Create `Services/AnimalsService.cs`...
2. CRUD methods...
3. Authorization policy...
4. Validation...

## Acceptance criteria

- [ ] S1 — Create method validates and saves a new Animal
- [ ] S2 — Read method loads an Animal by ID
- [ ] S3 — Update method persists changes
- [ ] S4 — Soft delete sets IsDeleted
- [ ] S5 — Duplicate Name is rejected (case-insensitive)
- [ ] S6 — Authorization requires animals_write permission
- [ ] S7 — Service is registered in DI container

## Out of scope

- Bulk operations or batch imports
- Hard delete
- Audit logging beyond UpdatedBy

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-002-animals-service.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
- [specs/manage-animals.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/manage-animals.yaml)
- [excel/manage-animals.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/manage-animals.xlsx)
```

**Sub-issues:** None (standalone issue)

---

## Ticket: T-ANIMAL-004

**Action:** CREATE (no existing issue found with label `T-ANIMAL-004`)

**Title:** `[T-ANIMAL-004] Add | Edit Animal Basic Form (Form Modal)`

**Labels:**
- `T-ANIMAL-004`
- `manage-animals`
- `form-modal`
- `ui-page`
- `ai-planning-framework`

**Body:**

```markdown
## User story

**As a** administrator  
**I want** to add or edit an animal on a single Basic Form  
**So that** animal details are stored correctly and available from Manage Animals

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Keyed Input | Animals | Animal (creatures.animals) | Name |
| Date Born | Date Picker (date only) | Animals | Animal (creatures.animals) | DateBorn |
| Attributes | Tag Input (multi-value) | Animals | Animal (creatures.animals) | Attributes |
| Is Furry | Switch | Animals | Animal (creatures.animals) | IsFurry |
| Has Hooves | Switch | Animals | Animal (creatures.animals) | HasHooves |

## Work to do

1. Build the form as a routed modal over the Manage Animals page...
2. Render sections **Animal Details** and **Characteristics**...
3. Add mode defaults...
4. Validation messages...
5. Save/load through the Animals service...
6. Modes: Add and Edit only...

## Acceptance criteria

- [ ] S1 — Add mode opens with defaults
- [ ] S2 — Create animal with required fields
- [ ] S3 — Name is mandatory
- [ ] S4 — Duplicate name is rejected on Save
- [ ] S5 — Name of a deleted animal can be reused
- [ ] S6 — Date Born must be before today
- [ ] S7 — Date Born is mandatory
- [ ] S8 — Attributes persist as JSON tags
- [ ] S9 — Attribute tag limits
- [ ] S10 — Edit persists changed fields
- [ ] S11 — Only Add and Edit modes exist
- [ ] S12 — Deleted animal cannot be opened

## Out of scope

- Manage Animals grid / Actions column (T-ANIMAL-003, T-ANIMAL-007)
- Soft delete confirmation (T-ANIMAL-005)
- Building the Switch and Tag Input renderers (T-ANIMAL-006)
- View mode (dropped — decision 20)

---

**Source:** `work/manage-animals/tickets/T-ANIMAL-004-add-edit-animal-form.md`

**Specs:**
- [specs/add-edit-animal.yaml](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/specs/add-edit-animal.yaml)
- [excel/add-edit-animal.xlsx](https://github.com/NeilWoodComputing/AI-framework/blob/main/ai-planning-framework/work/manage-animals/excel/add-edit-animal.xlsx)
```

**Sub-issues:** None (standalone issue)

**Dependencies:** T-ANIMAL-002 (API + schema), T-ANIMAL-006 (Switch, Tag Input), T-ANIMAL-003 (entry points), T-ANIMAL-008 (Manage Animals page)

---

## Summary of Upsert Decisions

| Ticket ID | Action | Reason |
|-----------|--------|--------|
| T-ANIMAL-001 | CREATE | No existing issue with label `T-ANIMAL-001` or title prefix `[T-ANIMAL-001]` |
| T-ANIMAL-002 | CREATE | No existing issue with label `T-ANIMAL-002` or title prefix `[T-ANIMAL-002]` |
| T-ANIMAL-003 | CREATE | No existing issue with label `T-ANIMAL-003` or title prefix `[T-ANIMAL-003]` |
| T-ANIMAL-004 | CREATE | No existing issue with label `T-ANIMAL-004` or title prefix `[T-ANIMAL-004]` |
| T-ANIMAL-005 | CREATE | No existing issue with label `T-ANIMAL-005` or title prefix `[T-ANIMAL-005]` |
| T-ANIMAL-006 | CREATE | No existing issue with label `T-ANIMAL-006` or title prefix `[T-ANIMAL-006]` |
| T-ANIMAL-007 | CREATE | No existing issue with label `T-ANIMAL-007` or title prefix `[T-ANIMAL-007]` |
| T-ANIMAL-008 | CREATE | No existing issue with label `T-ANIMAL-008` or title prefix `[T-ANIMAL-008]` |
| T-ANIMAL-009 | CREATE | No existing issue with label `T-ANIMAL-009` or title prefix `[T-ANIMAL-009]` |

---

## Notes

- **DRY-RUN MODE:** No actual GitHub issues created
- **Project board:** Issues would be automatically added to project "AI testing"
- **Acceptance criteria:** Each issue body includes a checkable Acceptance criteria section derived from Given/When/Then scenarios
- **Labels:** All issues include `ai-planning-framework`, stable ID, feature slug, and page type labels
- **Source footer:** Each issue body includes source ticket path and links to specs/excel files in the AI-framework repository
- **Sub-issues:** None of the manage-animals tickets are explicitly typed as child tasks, so all are created as standalone issues
- **Dependencies:** Dependencies are noted in the issue body but not enforced as GitHub issue relationships (could be implemented as sub-issues or using GitHub's "blocked by" feature in future enhancements)

---

## GitHub API Operations (would be performed)

1. **Search for existing issues:**
   - Query: `repo:NeilWoodComputing/ai-framework-tests label:T-ANIMAL-001 OR "T-ANIMAL-001" in:title`
   - (Repeat for each ticket ID)

2. **Create new issues:**
   - POST `/repos/NeilWoodComputing/ai-framework-tests/issues`
   - Body: title, body (markdown), labels array

3. **Add to project:**
   - Add each created issue to project "AI testing" via GraphQL API

4. **Record in handoff.md:**
   - Each issue number would be recorded as `devops_work_item_id` in the feature's handoff.md
   - Issue URLs would be recorded in `devops.board_url`

---

**End of dry-run publish plan**
