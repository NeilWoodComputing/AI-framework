# Ticket: T-ANIMAL-007 — Shared, permission-aware row actions menu in the grid's last Actions column (UI.NextJs.Framework)

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-007 |
| Type | UI framework component |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` (Actions column: row actions menu with Edit Animal, Delete Animal) |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Decisions | `plan.md` › Decision 23 (Actions column at the end of the grid, reusable in UI.NextJs.Framework) as amended by 26 (Edit and Delete in a row actions **menu**; keep Dev Bot's `menu` approach — Q33 resolved); 24 (`animals_write`, the first consumer's permission) |
| Open questions | None. Q32 (menu trigger, hidden vs disabled, keyboard) and Q23 (row click): Neil accepted the suggested defaults for all remaining questions at 2026-10-08 15:44 BST. Work items 1–4 and scenarios S3, S5, S7, S9 are final |

## User story

**As a** developer building Unity pages in UI.NextJs.Framework  
**I want** the shared entity grid to show a row actions menu in an Actions column at the end of the grid, listing only the items the signed-in user is allowed to run  
**So that** Manage Animals (and future grids) get Edit / Delete menus without feature-local grid code or hand-built permission checks

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Actions (column header) | Shared grid column, last column | — (UI framework only) | — | — (no data; one row actions menu per row) |
| Edit Animal (first consumer) | Row actions menu item | Animals (through T-ANIMAL-003) | Animal (creatures.animals) | Opens Add \| Edit Animal in Edit mode |
| Delete Animal (first consumer) | Row actions menu item | Animals (through T-ANIMAL-005) | Animal (creatures.animals) | Soft delete (IsDeleted) after confirmation |

## Current code (extension point)

Read only in `src/framework/entity-framework/` (the files include Dev Bot's uncommitted changes listed in `handoff.md` › `implementation`):

- `grid/grid-column.ts`: `GridRowAction<T>` = `label`, `tid?`, `icon?` (added by Dev Bot), `execute(item)`, `prefetchHref?(item)`. No permission or per-row visibility.
- `grid/entity-grid-config.ts`: `EntityGridConfig<T>.rowActions?` and `rowActionsDisplay?: 'buttons' | 'menu'` (`menu` added by Dev Bot; `buttons` is the default).
- `components/entity-grid/EntityGrid.tsx`: when `rowActions` is not empty it appends a last column (`propertyName: '__actions'`, header "Actions", not sortable). With `menu`, each cell renders `EntityGridRowActionsMenu`; otherwise each action is a small text `Button`. No Actions column when `rowActions` is empty. No row-click handler.
- `components/entity-grid/EntityGridRowActionsMenu.tsx` (Dev Bot): an "Actions" text button (`aria-haspopup="menu"`, `aria-expanded`) opening a `role="menu"` list of `menuitem` buttons (optional icon + label); closes on Escape, on a click outside, and after an item is chosen; renders nothing when given no actions. Styles in `EntityGrid.module.css` (`rowActionsMenu*`).
- Consumers: the two reference-data grids (default `buttons`) and `src/features/animals/manage-animals/use-animals-grid.tsx` (`menu`; at planning time it built the item list conditionally from `user_management_write`; the folder was renamed from `manage-animals-modal/` when the list moved onto the page, decision 27).
- Permissions on the client: `session.permissions: string[]` (`src/framework/auth/models/auth-state.model.ts`, read with `useAuth()` from `@auth/context/AuthProvider`). No shared permission helper exists.

## Work to do

1. **Keep and formalise the `menu` display** (decision 26): `rowActionsDisplay: 'menu'` and `EntityGridRowActionsMenu.tsx` stay as the shared row actions menu, documented as a framework option. `buttons` stays the default.
2. **Permission-aware items** (`grid/grid-column.ts`), per Q32: add `requiredPermissions?: readonly string[]` to `GridRowAction` (the item is shown when the session has **any** of them; omitted = no permission needed) and an optional `isVisible?: (item) => boolean` per-row rule. Add one small exported helper (e.g. `hasAnyPermission(permissions, required)`) so pages and the grid use the same rule; the grid reads `session.permissions` through `useAuth()`. This applies to `buttons` too, so text-button grids can opt in; grids that do not set it behave as today.
3. **Rendering** (`components/entity-grid/EntityGrid.tsx`, `EntityGridRowActionsMenu.tsx`, `EntityGrid.module.css`):
   - The Actions column is always the **last** column, after every data column; header "Actions"; not sortable; no fixed width.
   - Items the user lacks permission for are **hidden**, not disabled (Q32).
   - If no item is permitted for the current user, do not render the Actions column at all.
   - Per row, also hide items whose `isVisible(row)` is false; a row with no visible items shows no menu trigger (an empty cell).
   - Items appear in configured order with their optional icon and label (Edit Animal, Delete Animal for Manage Animals).
   - Choosing an item calls `execute(row)` for that row only, closes the menu, and does not bubble to the row.
   - Keep the current trigger (an "Actions" text button) and close behaviour (Escape, click outside, after choosing). No arrow-key navigation is added (Q32).
4. **Row click** (Q23): no row-click option is added; clicking a row does nothing.
5. **Existing grids:** the reference-data grids (`buttons`, no `requiredPermissions`) render exactly as before.
6. Keep it generic: no animal-specific code in `src/framework/`. Manage Animals is wired to it in T-ANIMAL-003 (Edit Animal) and T-ANIMAL-005 (Delete Animal).

## Acceptance criteria

### Scenario: S1 — Row actions menu in the last column

```gherkin
Given a grid configured with data columns "Name" and "Last Amended" and rowActionsDisplay "menu"
And row actions "Edit Animal" (icon Edit) and "Delete Animal" (icon Delete) with no required permissions
When the grid renders two rows
Then the last column header is "Actions", after "Last Amended", and it is not sortable
And each row's Actions cell shows one "Actions" menu trigger
When I open the first row's menu
Then it lists "Edit Animal" then "Delete Animal", each with its icon
```

### Scenario: S2 — Choosing an item runs it for that row

```gherkin
Given the grid above shows rows "Bessie" and "Ziggy"
When I open the "Ziggy" row's menu and choose "Edit Animal"
Then the Edit Animal action is executed once with the "Ziggy" row
And no action is executed for "Bessie"
And the menu closes
And no row-level click handler runs
```

### Scenario: S3 — Items are hidden without the required permission

```gherkin
Given row actions "Edit Animal" and "Delete Animal" that each require permission "animals_write"
And row action "Open" with no required permission
And I am signed in without "animals_write"
When I open a row's menu
Then it lists only "Open"
And no disabled "Edit Animal" or "Delete Animal" items are shown
```

### Scenario: S4 — Any one of several permissions is enough

```gherkin
Given a row action that requires any of "reports_view" or "animals_write"
When I am signed in with "animals_write" only
Then the item is listed in every row's menu
```

### Scenario: S5 — No Actions column when no item is allowed

```gherkin
Given every row action requires permission "animals_write"
And I am signed in without "animals_write"
When the grid renders
Then the grid has no "Actions" column
And the last column is the last data column
```

### Scenario: S6 — Per-row visibility

```gherkin
Given a row action "Delete Animal" with isVisible returning false for the row named "Bessie"
When I open the menus for rows "Bessie" and "Ziggy"
Then the "Ziggy" menu lists "Delete Animal"
And the "Bessie" menu does not
```

### Scenario: S7 — A row with no visible items has no trigger

```gherkin
Given a single row action "Delete Animal" with isVisible returning false for the row named "Bessie"
When the grid renders rows "Bessie" and "Ziggy"
Then the "Bessie" row's Actions cell is empty
And the "Ziggy" row's Actions cell shows the "Actions" menu trigger
```

### Scenario: S8 — Existing text-button grids are unaffected

```gherkin
Given the seeded reference-data types EXAMPLE_STATUS and SHOWCASE_OPTION (2 active items each, from the existing migration seed; no extra reset rows)
And I am signed in as a user with user_management_read
When I open the reference-data types grid
Then it shows exactly 2 rows, EXAMPLE_STATUS then SHOWCASE_OPTION, with Active items 2 and 2
And the columns are "Type key", "Active items", "Actions", with "Actions" last and not sortable
And each row's Actions cell has exactly one "Manage" text button and no row actions menu trigger
When I click Manage on the SHOWCASE_OPTION row
Then the Manage SHOWCASE_OPTION modal opens listing Widget and Gadget
And closing it returns to the reference-data types grid
```

### Scenario: S9 — Menu closes on Escape and outside click

```gherkin
Given a row's actions menu is open
When I press Escape
Then the menu closes and no action runs
When I open it again and click outside it
Then the menu closes and no action runs
```

Checklist (derived from scenarios):

- [ ] `rowActionsDisplay: 'menu'` / `EntityGridRowActionsMenu` kept and documented as the shared row actions menu (decision 26)
- [ ] Actions column always last; header "Actions"; not sortable
- [ ] `requiredPermissions` (any-of) checked against `session.permissions`; unpermitted items hidden; column omitted when none permitted
- [ ] Optional per-row `isVisible`; rows with no visible items show no trigger
- [ ] `buttons` stays the default; reference-data grids unchanged
- [ ] No animal-specific code in `src/framework/`; `npx tsc --noEmit` and `npm run build` pass

## Out of scope

- Wiring Manage Animals' Edit Animal and Delete Animal items (T-ANIMAL-003, T-ANIMAL-005)
- An icon-only Actions column (dropped by decision 26)
- Kebab-icon trigger, arrow-key navigation, disabled items, row click (Q32 / Q23 options not chosen)
- Hiding other `SiteNav` links by permission
- API-side permission (T-ANIMAL-001 seed, T-ANIMAL-002 policy)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-007`. The file name is kept so the ID and path in `handoff.md` stay stable.
- Re-scoped 2026-10-08 after Neil's 15:17 BST answer to Q31 (decision 26): the 14:58 version described an icon-only Actions column; that design is dropped and Dev Bot's existing menu is formalised instead.
- Decision 23 (Neil, 14:47 BST): the Actions column is a reusable grid feature of UI.NextJs.Framework, not animals-only code. Like T-ANIMAL-006, it changes shared framework code.
- Scenario IDs frozen 2026-10-08 from current positions (S1-S9; ticket heading IDs T-ANIMAL-007/S<n> for tests; doc-only, no wording or behaviour change).
- S8 baseline and checks confirmed by Neil 2026-10-09 09:46
