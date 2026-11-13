# Journey: J-ANIMAL-001 — Manage the animal catalogue

| Field | Value |
|-------|--------|
| Actor | Any user with the `animals_write` permission (decisions 22, 24) — every user in the seeded Administrators and Standard groups, plus system admins (decision 25). There is no read-only actor |
| Goal | List animals, add or edit one so its details persist on the Animal table (`creatures.animals`), and soft-delete one |
| Trigger | User clicks "Animals" in the site navigation, which opens the Manage Animals page `/examples/animals` with the list on the page (decisions 14, 19, 27 in `plan.md`) |
| Primary pages | Manage Animals page (`/examples/animals`, Paginated Grid, list on the page); Add \| Edit Animal modal (Add and Edit modes only) |
| Source specs | `specs/manage-animals.yaml`, `specs/add-edit-animal.yaml` (Excel: `excel/manage-animals.xlsx`, `excel/add-edit-animal.xlsx`) |
| Tickets | T-ANIMAL-001 to T-ANIMAL-009 (Manage Animals: page T-ANIMAL-008, paginated grid T-ANIMAL-003; boolean icon cells T-ANIMAL-009; decision 28 / 29) |
| Changes 2026-10-08 | Decision 20 (14:31 BST): View dropped — no View Animal action, no View mode. Decision 21 (14:35 BST): table in the new `creatures` schema (`creatures.animals`). Decision 22 (14:47 BST): animals have their own permission. Decision 23 (14:47 BST): Actions column at the end of the grid. Decisions 24–26 (15:17 BST): single permission `animals_write` (no read-only access), given to every user via the Administrators and Standard groups; Edit and Delete in a row actions menu in the Actions column. Decision 27 (Neil standing rule): the list is on the page, not in a modal; only the form and the delete confirmation are modals Decision 28 (18:46 BST): Manage Animals is a Paginated Grid spec (one Excel) delivered as two tickets, the page (T-ANIMAL-008) and the paginated grid (T-ANIMAL-003); no behaviour change. Decision 29 (19:04 BST via Review Bot): Is Furry / Has Hooves show green tick / red cross icons (not read-only Switches), shared renderer T-ANIMAL-009 |

## Happy path

1. **Open Manage Animals** — Page: Manage Animals page (`/examples/animals`; the list is on the page, no modal)
   - UI: Results grid columns Name, Is Furry, Has Hooves (boolean icons: filled green circle + Check cut-out / red circle + Close cut-out, with Yes/No — decisions 29, 30), Date Born, Attributes, Last Amended, then the **Actions** column as the last column with a **row actions menu** per row (Edit Animal, Delete Animal — decisions 23, 26); primary action "+ Add Animal" (no View Animal)
   - Data: Service `Animals` → `Animal.Name`, `Animal.IsFurry`, `Animal.HasHooves`, `Animal.DateBorn`, `Animal.Attributes`, `Animal.UpdatedUtc & UpdatedBy` (→ `User.DisplayName`, fallback `User.Email`; `auth.users`); table `creatures.animals`; non-deleted rows only
   - Outcome: Paginated list of non-deleted animals, sorted by Name ascending; Is Furry / Has Hooves as filled green / red circles with a transparent tick / cross cut-out and accessible Yes/No (decisions 29, 30); Attributes shown as comma-separated tags; Last Amended as "DD/MM/YYYY HH:MM Display name" in the browser's local time. Clicking a row does nothing; Edit is chosen from the row actions menu (Q23)

2. **Add Animal** — Page: Add \| Edit Animal / Add mode (from "+ Add Animal")
   - UI: Section Animal Details (Name, Date Born, Attributes); section Characteristics (Is Furry, Has Hooves). Starts with Name and Date Born blank, both switches Off, no tags
   - Data: On Save, Animals → `Animal.Name` (trimmed; derived `NormalizedName`), `Animal.DateBorn` (date only), `Animal.Attributes` (JSON array of strings, `[]` if none), `Animal.IsFurry`, `Animal.HasHooves`; `UpdatedUtc` / `UpdatedBy` set to now / me
   - Outcome: Form closes; the new animal appears on Manage Animals

3. **Edit Animal** — Page: Add \| Edit Animal / Edit mode (row actions menu → Edit Animal)
   - UI: Same form, loaded with the animal's current values
   - Data: Read via Animals from `Animal`; on Save, Animals updates the changed columns on `Animal` and sets `UpdatedUtc` / `UpdatedBy`
   - Outcome: Form closes; Manage Animals shows the updated values and Last Amended

4. **Delete Animal** — Page: Manage Animals / row actions menu → Delete Animal
   - UI: Confirmation modal "Delete &lt;Name&gt;?" with Cancel / Delete
   - Data: On Delete, Animals soft-deletes the row (`Animal.IsDeleted = true`; `UpdatedUtc` / `UpdatedBy` set); the row stays in storage
   - Outcome: The animal no longer appears on Manage Animals; it cannot be opened (not found) or restored, and its name can be used again

## Alternate paths

- **Validation failure — Name:** blank Name → "Name is required"; a name that matches a non-deleted animal after trimming, ignoring case → "An animal with this name already exists". Nothing is written to `Animal`. A soft-deleted animal's name does not count.
- **Validation failure — Date Born:** empty → "Date Born is required"; today or later → "Date Born must be before today" (UI: browser local date; API: UTC date). Nothing is written to `Animal`.
- **Validation failure — Attributes:** a tag over 50 characters → "Each attribute tag must be 50 characters or fewer"; more than 20 tags → "A maximum of 20 attributes is allowed". Any characters are allowed. Nothing is written to `Animal`.
- **Cancel / close:** The form closes with no writes via Animals; cancelling the delete confirmation leaves the animal unchanged and visible.
- **No `animals_write` (decisions 24, Q36):** the "Animals" link is not shown; going to `/examples/animals` (or a form URL under it) directly shows no list and no form, and shows a warning callout "You do not have permission to manage animals." instead; every animal API call returns 403. `user_management_read` / `user_management_write` alone give no access. A user who has just been given the permission sees it after signing in again or refreshing their token.
- **Deleted animal opened directly:** a stale Edit link for a soft-deleted animal shows the not-found / error state (API returns 404).

## Done when

- [ ] Add and Edit persist Name, Date Born, Attributes, Is Furry and Has Hooves via Animals to `Animal` (`creatures.animals`)
- [ ] Manage Animals shows only non-deleted animals, with every column from its Population Source
- [ ] Is Furry / Has Hooves on the grid are boolean icons (filled green circle + tick cut-out / red circle + cross cut-out, readable in light and dark mode, with Yes/No), not Switches (decisions 29, 30)
- [ ] No View Animal action or View mode anywhere
- [ ] Delete soft-deletes after "Delete &lt;Name&gt;?" confirmation
- [ ] Edit Animal and Delete Animal are items of the row actions menu in the Actions column at the end of the grid (decisions 23, 26)
- [ ] Access is controlled by the single `animals_write` permission, not user management (decisions 22, 24); without it no nav link, no page, 403 from the API
- [ ] Persisted fields match Target DB Column / Population Source in the Excel specs
