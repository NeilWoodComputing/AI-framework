# Ticket: T-ANIMAL-003 — Manage Animals paginated grid + row actions menu

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-003 |
| Type | Paginated grid (part b of the Manage Animals Paginated Grid; the page is T-ANIMAL-008) |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Depends on | T-ANIMAL-002 (API), T-ANIMAL-006 (form Switch / Tag Input; string-array grid cell only after decision 29), T-ANIMAL-007 (shared permission-aware row actions menu), T-ANIMAL-009 (shared boolean icon grid cell). Hosted by T-ANIMAL-008 (the page), which depends on this ticket |
| Decisions | `plan.md` › Decisions 2, 5, 11 (superseded by 22), 14, 15, 16, 17, 19, 20 (View dropped), 22 / 24 (single permission `animals_write` for the whole page), 23 / 26 (row actions menu in the Actions column at the end of the grid), 27 (list on the page, not in a modal), 28 (Paginated Grid page type; page / grid ticket split), 29 (boolean tick/cross grid cells; T-ANIMAL-009), 30 (boolean cells as filled circles with a transparent tick / cross cut-out, light and dark; amended Neil 20:19) |
| Open questions | None. Q38 accepted by Neil 19:14 BST (em dash + "Not set") on T-ANIMAL-009 S5; this ticket's S14/S15 cover true/false only. Q23, Q32, Q35, Q36 accepted 15:44 BST; Q37 accepted 19:00 BST (S12/S13 final) |

## User story

**As a** administrator  
**I want** a paged, sorted Manage Animals grid with "+ Add Animal" and a row actions menu on each row  
**So that** I can find animals and add, edit or soft-delete them

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Name | Results column | Animals | Animal (creatures.animals) | Animal.Name |
| Is Furry | Results column (boolean icon; T-ANIMAL-009) | Animals | Animal (creatures.animals) | Animal.IsFurry |
| Has Hooves | Results column (boolean icon; T-ANIMAL-009) | Animals | Animal (creatures.animals) | Animal.HasHooves |
| Date Born | Results column (DD/MM/YYYY) | Animals | Animal (creatures.animals) | Animal.DateBorn |
| Attributes | Results column | Animals | Animal (creatures.animals) | Animal.Attributes |
| Last Amended | Results column (DD/MM/YYYY HH:MM [Display name], browser local time) | Animals | Animal (creatures.animals) | Animal.UpdatedUtc & UpdatedBy → User.DisplayName (fallback User.Email) |
| + Add Animal | Primary action (`animals_write`, like the whole page) | Animals | Animal (creatures.animals) | Opens Add \| Edit Animal in Add mode |
| Actions (row actions menu: Edit Animal, Delete Animal) | Actions column, last column of the grid (decisions 23, 26) | Animals | Animal (creatures.animals) | Edit opens Basic Form in Edit mode; Delete soft-deletes (T-ANIMAL-005) |
| Paging / sort / empty state | Grid paginator; results area | Animals | Animal (creatures.animals) | Server-side paging of `v1/Animal`; page size 20, options 5, 10, 20, 50, 100, 200 (Q37, accepted); default sort Name ascending; empty state "No results" (Q37, accepted) |

## Work to do

The page that hosts this grid (route, nav link, permission gate, no-permission message, page layout, the form modal slot) is **T-ANIMAL-008** (decision 28). Old work items 1 (route and nav link), 5 (page-level permission gate and callout) and 8 (standing rule) moved there; items 2, 3, 4, 6 and 7 stay here, renumbered below.

1. Render the paginated results **inline** in the Manage Animals page from T-ANIMAL-008, per the Excel columns (`ManageAnimals`, `AnimalsGrid`, `use-animals-grid.tsx`, `columns/animals-grid-columns.tsx`, `state/animals-search.data-provider.ts` under `src/features/animals/manage-animals/`; the reference-data grid, columns and search data provider are the pattern, but not its list modal `ManageReferenceDataItemsModal`, which predates the rule), calling `v1/Animal` through `unityApiFetch` and a new entry in `src/config/api-routes.ts`. (Was item 2.)
2. Populate the grid from the Population Sources above (non-deleted only; default sort Name ascending; Attributes not sortable). (Was item 3.)
3. Display: Is Furry / Has Hooves as **boolean icon cells** via `renderBooleanIconCell` from T-ANIMAL-009 (decision 30 / Neil 20:19: filled circle in `--app-boolean-true-fill` with `Check` as a transparent cut-out + accessible "Yes" when true; filled circle in `--app-boolean-false-fill` with `Close` as a cut-out + "No" when false; not interactive, not colour-only). **Do not** use `renderBooleanSwitchCell` for these columns (decision 29). Date Born as DD/MM/YYYY; Attributes as comma-separated tags (empty array = empty cell); Last Amended as "DD/MM/YYYY HH:MM Display name", converting `UpdatedUtc` (UTC) to the browser's local time. (Was item 4; boolean display amended by decisions 29 and 30.)
4. Paging (spec `pagination`): server-side paging of `v1/Animal` (T-ANIMAL-002); page size 20 with options 5, 10, 20, 50, 100, 200, as `use-animals-grid.tsx` and the framework's `defaultPagingOptions` already do (Q37, accepted 19:00 BST). Empty state (spec `results_area.empty_state`): the EntityGrid default "No results", with "+ Add Animal" still available (Q37, accepted 19:00 BST). New in decision 28; describes the current code, no behaviour change.
5. Actions column (decisions 23, 26): keep `rowActionsDisplay: 'menu'` with the shared, permission-aware row actions menu from T-ANIMAL-007, in the last column after Last Amended. Menu items in order: **Edit Animal** (`Icon` `Edit`, opens Add | Edit Animal in Edit mode) and **Delete Animal** (`Icon` `Delete`, opens the T-ANIMAL-005 confirmation), both with `requiredPermissions: ['animals_write']` instead of building the list conditionally. Remove the View Animal item (decision 20). (Was item 6.)
6. Wire "+ Add Animal" (grid toolbar action, `animals_write`) to Add mode. Clicking a row does nothing (Q23); Edit is chosen from the row actions menu. The form opens as a modal over the page (T-ANIMAL-008). (Was item 7.)

## Acceptance criteria

Scenario IDs are stable (decision 28). **S1, S10 and S11 moved to T-ANIMAL-008** (the page ticket) as T-ANIMAL-008 S1, S2 and S3; S2–S9 stay here with their numbers; S12 and S13 are new scenarios for paging and the empty state (final since Neil accepted Q37 at 19:00 BST). S14 and S15 are new for decision 29 (boolean icons); no old → new remap.

### Scenario: S2 — List shows non-deleted animals

```gherkin
Given I am on the Manage Animals page /examples/animals
When the results area loads
Then each visible row is a non-deleted Animal via the Animals service
And Name, Is Furry, Has Hooves, Date Born, Attributes, and Last Amended match their Animal Population Sources
And Attributes display as comma-separated tags from Animal.Attributes
And soft-deleted animals are not shown and there is no option to show them
```

### Scenario: S3 — Last Amended shows date, time and user

```gherkin
Given an Animal was last saved by a user whose DisplayName is "Animals Tester"
When Manage Animals loads
Then that row's Last Amended shows Animal.UpdatedUtc as DD/MM/YYYY HH:MM in the browser's local time, followed by "Animals Tester" from Animal.UpdatedBy
And when the saving user has no DisplayName, their Email is shown instead
```

### Scenario: S4 — Last Amended is shown in the browser's local time

```gherkin
Given an Animal has Animal.UpdatedUtc = 2026-10-08T13:05:00Z
And my browser's time zone is Europe/London (BST, UTC+1)
When Manage Animals loads
Then that row's Last Amended shows "08/10/2026 14:05" followed by the user's display name
And Animal.UpdatedUtc itself is unchanged in storage (UTC)
```

### Scenario: S5 — Last Amended outside summer time

```gherkin
Given an Animal has Animal.UpdatedUtc = 2026-12-01T09:30:00Z
And my browser's time zone is Europe/London (GMT, UTC+0)
When Manage Animals loads
Then that row's Last Amended shows "01/12/2026 09:30" followed by the user's display name
```

### Scenario: S6 — Default sort by Name ascending

```gherkin
Given multiple non-deleted Animals exist
When Manage Animals loads
Then rows are sorted by Animal.Name ascending by default
```

### Scenario: S7 — Add opens Basic Form

```gherkin
Given I have permission animals_write
And Manage Animals is open
When I click "+ Add Animal"
Then Add | Edit Animal opens in Add mode
```

### Scenario: S8 — Edit opens Basic Form with existing data

```gherkin
Given I have permission animals_write
And an Animal row is shown on Manage Animals
When I open that row's actions menu in the Actions column and choose Edit Animal
Then Add | Edit Animal opens in Edit mode
And fields are loaded via the Animals service from Animal for that row
```

### Scenario: S9 — Row actions menu in the last column; row click does nothing

```gherkin
Given I have permission animals_write
And Animal rows are shown on Manage Animals
Then the last column of the grid is "Actions", after Last Amended, and it is not sortable
And every row's Actions cell has an "Actions" menu trigger
When I open a row's actions menu
Then it lists Edit Animal then Delete Animal, each with its icon, and no View Animal
When I click a row outside its Actions cell
Then nothing opens and no form is shown
```

### Scenario: S12 — Results are paged on the server

```gherkin
Given 25 non-deleted Animals exist
And I have permission animals_write
When Manage Animals loads
Then the grid shows the first 20 rows sorted by Animal.Name ascending
And the page size options are 5, 10, 20, 50, 100 and 200
When I go to the next page
Then the remaining 5 rows are requested from v1/Animal via the Animals service and shown
```

### Scenario: S13 — No animals to show

```gherkin
Given no non-deleted Animals exist
And I have permission animals_write
When Manage Animals loads
Then the results area shows the message "No results"
And "+ Add Animal" is still available
```

### Scenario: S14 — True shows a green circle with a tick, accessible name Yes

```gherkin
Given I have permission animals_write
And an Animal exists with Animal.IsFurry true and Animal.HasHooves true
When Manage Animals loads
Then that row's Is Furry cell shows a filled circle coloured var(--app-boolean-true-fill) with the design-system Icon named Check as a transparent cut-out (Icon knockout="circle"; the row colour shows through the tick), and accessible name "Yes"
And that row's Has Hooves cell shows the same green circle with Check cut-out and accessible name "Yes"
And neither cell is a Switch
```

### Scenario: S15 — False shows a red circle with a cross, No; cells are not interactive

```gherkin
Given I have permission animals_write
And an Animal exists with Animal.IsFurry false and Animal.HasHooves false
When Manage Animals loads
Then that row's Is Furry and Has Hooves cells each show a filled circle coloured var(--app-boolean-false-fill) with the design-system Icon named Close as a transparent cut-out (Icon knockout="circle"; the row colour shows through the cross), and accessible name "No"
When I click either cell
Then no request is sent and no form or menu opens
And neither cell is focusable as a control
And meaning is not colour-only (accessible name present)
```

Checklist (derived from scenarios):

- [ ] UI behaviour matches the Excel manage-list rows (columns, actions, primary action, availability)
- [ ] Is Furry / Has Hooves use `renderBooleanIconCell` (T-ANIMAL-009): green circle + Check cut-out / Yes, red circle + Close cut-out / No, light and dark fills from the decision 30 tokens; not Switch; not interactive; not colour-only (decisions 29, 30 / Neil 20:19)
- [ ] No View Animal action or View mode anywhere (decision 20)
- [ ] Edit Animal and Delete Animal are items of the shared row actions menu in the last Actions column (decisions 23, 26; T-ANIMAL-007)
- [ ] "+ Add Animal" and the menu items need `animals_write`; no `user_management_*` checks (decisions 22, 24; the page gate is T-ANIMAL-008)
- [ ] Server-side paging, page size and options, and the empty state match the spec `pagination` / `empty_state` (Q37, accepted)
- [ ] Data read via `Animals` from `Animal.<column>` as asserted in Then/And
- [ ] Grid renders inline in the T-ANIMAL-008 page, never in a list modal (`nextjs-list-pages.mdc`, decision 27)

## Out of scope

- The page itself: route, "Animals" nav link, page-level permission gate and no-permission callout, page layout, form modal slot and `/manage` redirect (T-ANIMAL-008)
- Basic Form field validation (see T-ANIMAL-004)
- Soft-delete confirmation details (see T-ANIMAL-005)
- Shared Switch / Tag Input form controls and string-array grid cell (T-ANIMAL-006)
- Shared boolean icon grid cell renderer itself (T-ANIMAL-009)
- Filtering or searching the grid; import / export
- View Animal action / View mode (dropped — decision 20)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-003`
- Running locally (see T-ANIMAL-008) needs `NEXT_PUBLIC_UNITY_API_ROOT` in `.env.local` pointing at API.Framework's `v1/` root. Neil sets this himself; agents do not open or edit `.env*` files or change the `environment.ts` default (decision 16).
- Last Amended display: stored UTC, shown in the browser's local time (decision 17). Nav link label "Animals" (decision 19) is in T-ANIMAL-008.
- Spec source: `specs/manage-animals.yaml` → `excel/manage-animals.xlsx`
- Decisions 22 and 23 (Neil, 2026-10-08 14:47 BST): own animals permissions; Actions column at the end of the grid, built in the shared grid (T-ANIMAL-007).
- Decisions 24 and 26 (Neil, 15:17 BST): one permission `animals_write` for the whole page (no read-only view); Edit and Delete in a row actions menu. S8 now uses the menu; S9 (Actions column), S10 (was "Read-only user sees the grid") and S11 (user-management permissions only) were rewritten in place, so S1–S11 keep their numbers. Dev Bot's current code already uses `rowActionsDisplay: 'menu'` but still checks `user_management_write` and has a View item.
- Decision 20 (Neil, 2026-10-08 14:31 BST): View dropped. Scenario numbering is unchanged: S9 (was "View opens read-only form") and S10 (was "Read-only user sees View only") were replaced in place by the draft scenarios for Q23 and Q22. Final wording follows Neil's answers to Q22 / Q23 in `plan.md`. **15:44 BST:** Neil accepted the suggested defaults (Q23, Q32, Q36); S9 and S10 are final.
- Decision 27 (Neil standing rule, 2026-10-08; conformance update at 18:35 BST, no re-approval needed): the list is the page. S1 now checks the list is on the page with no modal open; S2 starts on the page; S10 / S11 say "no list is shown" and use a form URL instead of the old `/manage` URL (which now redirects). Work items 1, 2, 5 and 8 follow Dev Bot's current code.
- Decision 28 (Neil, 2026-10-08 18:46 BST; plan restructuring, no behaviour change, no re-approval needed): the spec is now `page_type: Paginated Grid` (one Excel) and the work is split into a page ticket (T-ANIMAL-008) and this paginated grid ticket. This ticket keeps its ID and filename so existing references (manifest, T-ANIMAL-005, T-ANIMAL-007) stay valid. Scenario mapping, old → new: S1 → T-ANIMAL-008 S1; S2–S9 → T-ANIMAL-003 S2–S9 (unchanged); S10 → T-ANIMAL-008 S2; S11 → T-ANIMAL-008 S3; new T-ANIMAL-003 S12 (paging) and S13 (empty state) are drafts pending Q37; new T-ANIMAL-008 S4–S6 restate decision 27. Work items: old 2, 3, 4, 6, 7 → new 1, 2, 3, 5, 6; new item 4 (paging, empty state); old 1, 5, 8 → T-ANIMAL-008.
- Q37 (Neil, 2026-10-08 19:00 BST): suggested default accepted (page size 20; options 5, 10, 20, 50, 100, 200; server-side paging; "No results" with "+ Add Animal" still shown). S12 and S13 are final and the draft markers were removed; no behaviour change.

- Decision 29 (Neil, 2026-10-08 19:04 BST via Review Bot): Is Furry / Has Hooves use boolean icon cells, not read-only Switches. New scenarios **S14** and **S15** (no old ID remap — these are new). Work item 3 amended with a note. Dependency on T-ANIMAL-006's boolean grid cell removed; depends on **T-ANIMAL-009** instead. Neil's own change; no separate re-approval.
- Decision 30 (Neil, 2026-10-08: 19:52 / 19:53 BST requests, 19:57 BST approval; amended 20:19 BST): the boolean cells are a filled circle (`--app-boolean-true-fill` / `--app-boolean-false-fill`, light and dark values in T-ANIMAL-009) with `Check` / `Close` as a transparent cut-out (`Icon knockout="circle"`). S14 and S15 reworded in place with the same IDs (shape and colour only; accessible names and non-interactive behaviour unchanged); work item 3 and the checklist amended. Neil 20:19: `--app-boolean-glyph` removed.
- Test data personas (2026-10-08, wording only, no behaviour change): S3 uses the role persona DisplayName "Animals Tester" instead of a real person's name (testing persona naming `{feature}-{role}`).
