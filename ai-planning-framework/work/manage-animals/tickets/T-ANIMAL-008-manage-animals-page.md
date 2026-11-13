# Ticket: T-ANIMAL-008 — Manage Animals page (route, nav link, permission gate, layout)

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-008 |
| Type | Page (part a of the Manage Animals Paginated Grid; the grid is T-ANIMAL-003) |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/manage-animals.yaml` (page_type, page title / sub-text, `route`, `nav_tree_path`, `parent_pages`, `search_filters`, primary action visibility, notes), `excel/manage-animals.xlsx`; `specs/add-edit-animal.yaml` (opens as a modal over this page) |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Depends on | T-ANIMAL-003 (the paginated grid this page hosts), T-ANIMAL-004 (the Add \| Edit Animal form modal it hosts) |
| Decisions | `plan.md` › Decisions 14 (route), 16 (`.env` note), 19 (nav label "Animals"), 22 / 24 (single permission `animals_write` for the whole page; no read-only view), 27 (list on the page; modals only for the form and confirmation), 28 (Paginated Grid page type; page / grid ticket split) |
| Open questions | None for this ticket. Q36 (no-permission callout) was accepted at 2026-10-08 15:44 BST. Q37 (page size, options, empty state) belongs to T-ANIMAL-003 |

## User story

**As a** administrator with animals_write  
**I want** a Manage Animals page at /examples/animals, reached from an "Animals" link in the site navigation  
**So that** I can open the animal catalogue directly, and people without access are told so instead of seeing it

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Animals (nav link) | `SiteNav` link to `/examples/animals`, shown only with `animals_write` | — (UI only) | — | — |
| Manage Animals (H1) / "Animal catalogue" (sub-text) | Page heading on route `/examples/animals` | — (UI only) | — | — |
| Search / filters | None (out of scope; spec `search_filters: []`) | — | — | — |
| Results area | Hosts the paginated grid from T-ANIMAL-003 | Animals | Animal (creatures.animals) | See T-ANIMAL-003 |
| Add \| Edit Animal | Routed form modal over this page (`@modal` slot) | Animals | Animal (creatures.animals) | See T-ANIMAL-004 |
| "You do not have permission to manage animals." | Warning callout in place of the grid | — (UI only) | — | — |

## Work to do

Old T-ANIMAL-003 work items 1, 5 and 8 moved here (decision 28).

1. The `/examples/animals` route **is the Manage Animals page** (decision 27): `src/app/examples/animals/page.tsx` renders `ManageAnimalsPage` (`src/features/animals/manage-animals/ManageAnimalsPage.tsx`: `PageLayout` with `SiteNav`, H1 "Manage Animals", sub-text "Animal catalogue", then `ManageAnimals` inline, which renders the T-ANIMAL-003 grid). No list modal, no landing page, no auto-open, no `?manage=closed`. (Was T-ANIMAL-003 item 1.)
2. Form modal hosting: `layout.tsx` has an `@modal` slot used **only** for the Add | Edit form (`@modal/(.)manage/item`, `@modal/(.)manage/item/[id]`); the full-page fallbacks `manage/item` and `manage/item/[id]` render the list page plus the form modal; the form closes back to `/examples/animals`; the old `manage/page.tsx` URL redirects to `/examples/animals`. (Was T-ANIMAL-003 item 1.)
3. Nav link: add an "Animals" link in `src/shell/components/SiteNav.tsx` next to "Reference data", shown only when `session.permissions` contains `animals_write` (decisions 19, 24; the first permission check in `SiteNav`). (Was T-ANIMAL-003 item 1.)
4. Page permission gate with the single animals permission `animals_write` (decisions 22, 24): replace the `user_management_*` checks in `src/features/animals/shared/utils/animal-permissions.ts`. The **whole page** needs `animals_write`: without it there is no nav link, the grid is not mounted, no API call is made, and the form URLs mount no form. `AnimalsAccessNotice` (`src/features/animals/shared/components/AnimalsAccessNotice.tsx`) shows a warning `Callout` "You do not have permission to manage animals." in place of the grid (signed-out users get the `EntityGridAuthGate` sign-in prompt). There is no read-only view and no View action (decisions 20, 24). Users who have just been given `animals_write` see the page after signing in again or refreshing their token. (Was T-ANIMAL-003 item 5.)
5. Page layout and search area: no on-page search or filters (out of scope; spec `search_filters: []`). The grid's search state stays in memory, as built for modal grids (no URL query); that is not a change in this plan.
6. Standing rule (decision 27): a routed list page shows its list on the page; modals only for the Add | Edit form and the delete confirmation. Follow UI.NextJs.Framework `.cursor/rules/framework/nextjs-list-pages.mdc` and `nextjs-modal-routing.mdc` for the form. (Was T-ANIMAL-003 item 8.)

## Acceptance criteria

Scenario IDs are stable (decision 28). S1–S3 moved here from T-ANIMAL-003 (old S1, S10, S11) with their wording unchanged; S4–S6 are new in the split and restate decision 27 (no behaviour change).

### Scenario: S1 (was T-ANIMAL-003 S1) — Open Manage Animals from the nav (decisions 24, 27)

```gherkin
Given I am signed in with permission animals_write
When I click "Animals" in the site navigation
Then the /examples/animals page opens with the heading "Manage Animals"
And the results grid and "+ Add Animal" are shown on the page
And no modal is open
```

### Scenario: S2 (was T-ANIMAL-003 S10) — User without animals_write cannot open Manage Animals

```gherkin
Given I am signed in without permission animals_write
When I look at the site navigation
Then the "Animals" link is not shown
When I go to /examples/animals or /examples/animals/manage/item directly
Then no animals list or form is shown and no request is made to v1/Animal
And a warning callout says "You do not have permission to manage animals."
And no animal rows, "+ Add Animal" or row actions are shown
```

### Scenario: S3 (was T-ANIMAL-003 S11) — User-management permissions alone do not give access to animals

```gherkin
Given I am signed in with permissions user_management_read and user_management_write but not animals_write
When I look at the site navigation
Then the "Animals" link is not shown
When I go to /examples/animals directly
Then no animals list is shown
```

### Scenario: S4 — Add | Edit Animal opens as a modal over the page and closes back to it (decision 27)

```gherkin
Given I have permission animals_write
And I am on the Manage Animals page /examples/animals
When I click "+ Add Animal"
Then Add | Edit Animal opens as a modal over the page
And the Manage Animals heading and grid stay on the page behind it
When I close the form without saving
Then the modal closes and I am on /examples/animals with the grid shown
```

### Scenario: S5 — Opening a form URL directly shows the page with the form on top (decision 27)

```gherkin
Given I have permission animals_write
When I go to /examples/animals/manage/item directly
Then the Manage Animals page with its grid is shown
And Add | Edit Animal is open in Add mode as a modal over it
```

### Scenario: S6 — The old /manage URL redirects to the page (decision 27)

```gherkin
Given I have permission animals_write
When I go to /examples/animals/manage
Then I am redirected to /examples/animals
And the grid is shown on the page with no modal open
```

Checklist (derived from scenarios):

- [ ] `/examples/animals` is the page; heading, sub-text and the grid render on it with no modal open (decision 27)
- [ ] "Animals" nav link, the page, the grid and the form URLs all need `animals_write`; no `user_management_*` checks; no read-only view (decisions 22, 24)
- [ ] No-permission users see the callout "You do not have permission to manage animals." and no request is made to `v1/Animal` (Q36)
- [ ] The form opens as a routed modal over the page and closes back to it; direct form URLs show page + form; `/manage` redirects (decision 27)

## Out of scope

- Grid columns, population, sorting, paging, the row actions menu and the empty state (T-ANIMAL-003)
- Add | Edit Animal form fields and validation (T-ANIMAL-004); delete confirmation (T-ANIMAL-005)
- Filtering or searching the grid; import / export
- View Animal action / View mode (dropped — decision 20)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-008`
- Running locally needs `NEXT_PUBLIC_UNITY_API_ROOT` in `.env.local` pointing at API.Framework's `v1/` root. Neil sets this himself; agents do not open or edit `.env*` files or change the `environment.ts` default (decision 16).
- Spec source: `specs/manage-animals.yaml` → `excel/manage-animals.xlsx` (one Excel for the page and the grid; Page Type "Paginated Grid", Route `/examples/animals`).
- Decision 28 (Neil, 2026-10-08 18:46 BST; plan restructuring, no behaviour change, no re-approval needed): new ticket for the page half of the old T-ANIMAL-003. Scenario mapping, old → new: T-ANIMAL-003 S1 → S1; T-ANIMAL-003 S10 → S2; T-ANIMAL-003 S11 → S3; S4–S6 new. Work items: old T-ANIMAL-003 items 1, 5, 8 → items 1–4 and 6 here; item 5 (search area) new.
