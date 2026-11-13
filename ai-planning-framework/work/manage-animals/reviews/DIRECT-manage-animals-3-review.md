# Review: DIRECT-manage-animals-3 — Manage Animals

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (round 3 of max 3, final; re-review after the list-on-page change, decision 27, and the ticket split, decision 28) |
| Trigger | direct-handoff |
| Review scope | Plan scope (`direct_scope: plan`) — details in **Review scope** |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git (API and UI; `code.api.head_commit` / `code.ui.head_commit` are null) — files read from disk on 08/10/2026 at 18:51 (last UI change 18:40:34; no API change since round 2) |
| Linked tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-008 (from `handoff.md` `tickets`; T-ANIMAL-008 added by decision 28 at 18:56) |
| Feature(s) | `ai-planning-framework/work/manage-animals/` |
| Specs reviewed | `specs/manage-animals.yaml` (now `page_type: Paginated Grid`, `route: /examples/animals`, `search_filters: []`, pagination / empty state final after Q37 was accepted at 19:00), `specs/add-edit-animal.yaml` (unchanged); journey `journeys/j-animal-manage.md` used as context |
| Active API / UI | API.Framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` and `.cursor/skills` "Check" sections, + shared `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc`; Next.js `AGENTS.md`, `README.md` and `.cursor/rules` (framework/, style/, implementation/), **including the new `framework/nextjs-list-pages.mdc`** (alwaysApply) and the 18:40 versions of `nextjs-modal-routing.mdc` and `nextjs-design-system.mdc`; `checklists/ui-nextjs-checklist.md` (16:56 version, sections A–C; it doesn't cite the list-pages rule yet, so that rule is cited directly), `full-stack-checklist.md`, `api-checklist.md`, `security-checklist.md`, `severity.md` (all re-read for this round; unchanged since round 2) |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 08/10/2026 19:08 (Europe/London) |
| Review iteration | 3 (final; review cap is 3) |

## Verdict

**Approve with comments**

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 0 | 4 | 7 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`. Counts are open findings only: new F-18 to F-25 plus round 2's F-13, F-14 and F-15, which are still open. F-16 is resolved, and F-17 (the round 2 miss, see **Changes since last review**) was already fixed before this round.

## Summary

Hi Dev Bot, thanks for this round. Moving the list onto `/examples/animals` and swapping the row menu to a portalled `DropdownMenu` both landed well. I checked the code against the new `nextjs-list-pages.mdc` rule, and the page meets it: title and sub-text in `PageLayout`, the grid inline, Add / Edit as a primary-level `RoutedModal` that closes back to the page, `ConfirmModal` for delete, full-page fallbacks that render the list with the form on top, `/manage` redirecting, and no auto-open or landing page.

This round I also ran a live browser check as the Development default user, which I should have done in round 2. Round 2 approved the row menu from the code alone and missed that it was clipped to a thin sliver inside the grid. Neil's live check at about 18:06 caught it. I'm sorry about that; it's logged as F-17. It's fixed now: the menu was fully visible every time I opened it, in light and dark mode, at 1440×900 and 1024×600, and it flips above the trigger near the bottom of the viewport. Create, edit, duplicate-name, validation, delete, Escape stacking, the deleted-record URL and the no-permission view all behaved as the tickets describe.

There are four Minor findings and no Blockers or Majors:
- Dark mode fails contrast on the primary and secondary buttons (Actions, Cancel, Save, + Add Animal) and the modal close button. They measure 2.73:1 because `tokens.css` has no dark value for the secondary fill or for text on primary fills.
- In dark mode the error-red tag-chip "×" measures 1.69:1.
- Five shared files the feature now relies on are missing from the manifest.
- `DropdownMenu` isn't in the design-system showcase yet.

The rest are Nits. So the verdict is **Approve with comments**. This is the last review round, so it goes to Neil. Tests are still a tooling decision for Neil, not findings (see **Tests**).

## Review scope

How the scope was built: Plan scope. I started from the `implementation` manifest in `handoff.md` (recorded 18:48:20; 82 files: 18 api, 3 migrations, 61 ui; `tests: []`). Then I searched `ai-code-framework/api/API.Framework` and `ai-code-framework/ui/UI.NextJs.Framework` again for:
- page names (Manage Animals, Add \| Edit Animal)
- routes (`/examples/animals`, `/examples/animals/manage`, `v1/Animal`, `v1/schemas/animal`)
- `animals_write` / `AnimalsWrite`
- ticket IDs and derived names (`Animal*`, `animal-*`, `animals-*`)
- every import from the changed feature and framework files (that is how the five discovered files below were found)
- every consumer of the shared code changed in this round (`DropdownMenu`, `EntityGrid`, `useModalPreload`, the schema cache, auth normalisation)

I compared every file against the round 2 copy (read at 16:53) to see exactly what changed, and then ran the live browser check.

| Repo | File | Class | Reason | Tickets / spec items it implements |
|------|------|-------|--------|------------------------------------|
| api | `Api.Framework.Data/Models/Animal.cs` | api | manifest | T-ANIMAL-001; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended; `Animal.Id`, `Animal.Name`, `Animal.NormalizedName`, `Animal.DateBorn`, `Animal.Attributes`, `Animal.IsFurry`, `Animal.HasHooves`, `Animal.IsDeleted`, `Animal.CreatedUtc`, `Animal.UpdatedUtc`, `Animal.UpdatedBy` |
| api | `Api.Framework.Data/LoginDbContext.cs` | api | manifest | T-ANIMAL-001; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended; `Animal.NormalizedName`, `Animal.Attributes`, `Animal.UpdatedBy` |
| api | `Api.Framework.Data/LoginPermissions.cs` | api | manifest | T-ANIMAL-001; controls: + Add Animal, Edit Animal, Delete Animal |
| api | `Api.Framework.Services/Validation/Schemas/animalSchema.json` | api | manifest | T-ANIMAL-002, T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves; `Animal.Name`, `Animal.DateBorn`, `Animal.Attributes`, `Animal.IsFurry`, `Animal.HasHooves` |
| api | `Api.Framework.Services/Records/AnimalRecord.cs` | api | manifest | T-ANIMAL-002; controls: Name, Date Born, Attributes, Is Furry, Has Hooves |
| api | `Api.Framework.Services/Records/AnimalJsonSchemaBuilder.cs` | api | manifest | T-ANIMAL-002 |
| api | `Api.Framework.Services/FormSchemaDependenciesRegistrar.cs` | api | manifest | T-ANIMAL-002 |
| api | `Api.Framework.Services/Animals/AnimalContracts.cs` | api | manifest | T-ANIMAL-002; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended |
| api | `Api.Framework.Services/Animals/IAnimalService.cs` | api | manifest | T-ANIMAL-002 |
| api | `Api.Framework.Services/Animals/AnimalService.cs` | api | manifest | T-ANIMAL-002, T-ANIMAL-005; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended, Delete Animal; `Animal.Name`, `Animal.NormalizedName`, `Animal.DateBorn`, `Animal.Attributes`, `Animal.IsFurry`, `Animal.HasHooves`, `Animal.IsDeleted`, `Animal.CreatedUtc`, `Animal.UpdatedUtc`, `Animal.UpdatedBy` |
| api | `Api.Framework.Services/Animals/AnimalPolicies.cs` | api | manifest | T-ANIMAL-002; controls: + Add Animal, Edit Animal, Delete Animal |
| api | `Api.Framework.Services/LoginServiceCollectionExtensions.cs` | api | manifest | T-ANIMAL-002 |
| api | `Api.Framework/Program.cs` | api | manifest | T-ANIMAL-002 |
| api | `Api.Framework/Controllers/V1/Animals/AnimalController.cs` | api | manifest | T-ANIMAL-002, T-ANIMAL-005; controls: + Add Animal, Edit Animal, Delete Animal |
| api | `Api.Framework/Controllers/V1/Schemas/AnimalSchemaController.cs` | api | manifest | T-ANIMAL-002, T-ANIMAL-004 |
| api | `Api.Framework.Services/DataFramework/JsonSchemaValidation/RecordSchemaValidator.cs` | api | manifest (existing, dependency) | T-ANIMAL-002; controls: Name, Date Born, Attributes |
| api | `Api.Framework.Services/DataFramework/JsonSchemaValidation/CustomValidation/DateCompareValidator.cs` | api | manifest (existing, dependency) | T-ANIMAL-002; controls: Date Born |
| api | `Api.Framework.Services/Auth/TokenService.cs` | api | manifest (existing, dependency) | T-ANIMAL-001, T-ANIMAL-002 |
| api | `Api.Framework.Data/Migrations/20261008150221_AddAnimals.cs` | migration | manifest | T-ANIMAL-001; `Animal.Id`, `Animal.Name`, `Animal.NormalizedName`, `Animal.DateBorn`, `Animal.Attributes`, `Animal.IsFurry`, `Animal.HasHooves`, `Animal.IsDeleted`, `Animal.CreatedUtc`, `Animal.UpdatedUtc`, `Animal.UpdatedBy` |
| api | `Api.Framework.Data/Migrations/20261008150221_AddAnimals.Designer.cs` | migration | manifest | T-ANIMAL-001 |
| api | `Api.Framework.Data/Migrations/LoginDbContextModelSnapshot.cs` | migration | manifest | T-ANIMAL-001 |
| ui | `src/app/examples/animals/layout.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/app/examples/animals/page.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/app/examples/animals/@modal/default.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/app/examples/animals/@modal/(.)manage/item/page.tsx` | ui | manifest | T-ANIMAL-004 |
| ui | `src/app/examples/animals/@modal/(.)manage/item/[id]/page.tsx` | ui | manifest | T-ANIMAL-004 |
| ui | `src/app/examples/animals/manage/page.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/app/examples/animals/manage/item/page.tsx` | ui | manifest | T-ANIMAL-004 |
| ui | `src/app/examples/animals/manage/item/[id]/page.tsx` | ui | manifest | T-ANIMAL-004 |
| ui | `src/shell/components/SiteNav.tsx` | ui | manifest | T-ANIMAL-003; controls: Animals |
| ui | `src/config/api-routes.ts` | ui | manifest | T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005 |
| ui | `src/features/animals/shared/models/animal.model.ts` | ui | manifest | T-ANIMAL-003, T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended |
| ui | `src/features/animals/shared/utils/animal-routes.ts` | ui | manifest | T-ANIMAL-003, T-ANIMAL-004 |
| ui | `src/features/animals/shared/utils/animal-permissions.ts` | ui | manifest | T-ANIMAL-003, T-ANIMAL-005; controls: + Add Animal, Edit Animal, Delete Animal |
| ui | `src/features/animals/shared/utils/use-animals-access.ts` | ui | manifest | T-ANIMAL-003, T-ANIMAL-004 |
| ui | `src/features/animals/shared/components/AnimalsAccessNotice.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/shared/state/animals-update.service.ts` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/shared/routes/AnimalsModalRoutes.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-004 |
| ui | `src/features/animals/manage-animals/ManageAnimalsPage.tsx` | ui | manifest | T-ANIMAL-003 (new: list inline on the page, decision 27) |
| ui | `src/features/animals/manage-animals/ManageAnimals.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-005; controls: Delete Animal |
| ui | `src/features/animals/manage-animals/AnimalsGrid.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/manage-animals/use-animals-grid.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-005, T-ANIMAL-007; controls: + Add Animal, Edit Animal, Delete Animal |
| ui | `src/features/animals/manage-animals/columns/animals-grid-columns.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-006; controls: Name, Is Furry, Has Hooves, Date Born, Attributes, Last Amended |
| ui | `src/features/animals/manage-animals/state/animals-search.data-provider.ts` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/animal-form-modal/AnimalFormModal.tsx` | ui | manifest | T-ANIMAL-004; controls: Save, Cancel |
| ui | `src/features/animals/animal-form-modal/state/animal-entity.data-provider.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/features/animals/animal-form-modal/state/animal-ui-schema.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/features/animals/animal-form-modal/ui-schemas/animal.ui-schema.json` | ui | manifest | T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves |
| ui | `src/framework/auth/permissions.ts` | ui | manifest | T-ANIMAL-007, T-ANIMAL-003 |
| ui | `src/framework/auth/normalize-auth-state.ts` | ui | manifest | T-ANIMAL-001, T-ANIMAL-003 (new since round 2: maps API.Framework `accessToken` / nested `user.permissions` into the session) |
| ui | `src/framework/auth/providers/authorisation.data-provider.ts` | ui | manifest | T-ANIMAL-001, T-ANIMAL-003 (changed since round 2) |
| ui | `src/framework/auth/token-refresh.service.ts` | ui | manifest | T-ANIMAL-001, T-ANIMAL-003 (changed since round 2) |
| ui | `src/framework/design-system/forms/switch/Switch.tsx` | ui | manifest | T-ANIMAL-006; controls: Is Furry, Has Hooves |
| ui | `src/framework/design-system/forms/switch/Switch.module.css` | ui | manifest | T-ANIMAL-006 |
| ui | `src/framework/design-system/components/icon/Icon.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-005; controls: Edit Animal, Delete Animal |
| ui | `src/framework/design-system/index.ts` | ui | manifest | T-ANIMAL-006 |
| ui | `src/framework/json-schema-form/components/renderers/unity-json-form-renderers.tsx` | ui | manifest | T-ANIMAL-004, T-ANIMAL-006; controls: Name, Date Born, Attributes, Is Furry, Has Hooves |
| ui | `src/framework/json-schema-form/components/JsonSchemaForm.tsx` | ui | manifest | T-ANIMAL-004 |
| ui | `src/framework/json-schema-form/components/JsonSchemaForm.module.css` | ui | manifest | T-ANIMAL-004, T-ANIMAL-006 |
| ui | `src/framework/json-schema-form/validation/unity-schema-validation.ts` | ui | manifest | T-ANIMAL-004; controls: Name, Date Born, Attributes |
| ui | `src/framework/json-schema-form/hooks/use-json-schema-entity-form.ts` | ui | manifest | T-ANIMAL-004; controls: Save |
| ui | `src/framework/json-schema-form/models/unity-json-schema.model.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/framework/json-schema-form/schema/unity-schema-api.mapper.ts` | ui | manifest | T-ANIMAL-004; controls: Attributes, Date Born |
| ui | `src/framework/json-schema-form/schema/unity-schema.adapter.ts` | ui | manifest | T-ANIMAL-004; controls: Is Furry, Has Hooves, Attributes |
| ui | `src/framework/json-schema-form/schema/unity-schema-value.mapper.ts` | ui | manifest | T-ANIMAL-004; controls: Attributes |
| ui | `src/framework/json-schema-form/index.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/framework/entity-framework/utils/api-error.utils.ts` | ui | manifest | T-ANIMAL-004, T-ANIMAL-005 |
| ui | `src/framework/entity-framework/providers/abstract-entity.data-provider.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/framework/entity-framework/index.ts` | ui | manifest | T-ANIMAL-003 |
| ui | `src/framework/entity-framework/grid/grid-column.ts` | ui | manifest | T-ANIMAL-007; controls: Edit Animal, Delete Animal |
| ui | `src/framework/entity-framework/grid/entity-grid-config.ts` | ui | manifest | T-ANIMAL-007 |
| ui | `src/framework/entity-framework/grid/grid-cell-renderers.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-006; controls: Is Furry, Has Hooves, Date Born, Attributes, Last Amended |
| ui | `src/framework/entity-framework/components/entity-grid/EntityGrid.tsx` | ui | manifest | T-ANIMAL-007, T-ANIMAL-003; controls: + Add Animal, Actions |
| ui | `src/framework/entity-framework/components/entity-grid/EntityGridRowActionsMenu.tsx` | ui | manifest | T-ANIMAL-007; controls: Edit Animal, Delete Animal |
| ui | `src/framework/entity-framework/components/entity-grid/EntityGrid.module.css` | ui | manifest | T-ANIMAL-007 |
| ui | `src/framework/design-system/components/modal/Modal.tsx` | ui | manifest | T-ANIMAL-005, T-ANIMAL-007; controls: Delete Animal |
| ui | `src/framework/design-system/components/modal/ConfirmModal.tsx` | ui | manifest | T-ANIMAL-005; controls: Delete Animal |
| ui | `src/framework/design-system/components/modal/RoutedModal.tsx` | ui | manifest | T-ANIMAL-004 |
| ui | `src/framework/design-system/theme/tokens.css` | ui | manifest | T-ANIMAL-006, T-ANIMAL-007 |
| ui | `src/framework/entity-framework/components/entity-grid-auth-gate/EntityGridAuthGate.tsx` | ui | manifest (existing, dependency) | T-ANIMAL-003 |
| ui | `src/framework/auth/context/AuthProvider.tsx` | ui | manifest (existing, dependency) | T-ANIMAL-003, T-ANIMAL-007 |
| ui | `.cursor/rules/framework/nextjs-list-pages.mdc` | ui | manifest | T-ANIMAL-003 (new rule; applied in this review) |
| ui | `src/framework/design-system/components/menu/DropdownMenu.tsx` | ui | discovered (not in manifest) → F-18 | T-ANIMAL-007 (the row actions menu is now built on it: portal, flip, Escape / outside click / Tab, arrow keys); controls: Actions, Edit Animal, Delete Animal |
| ui | `src/framework/design-system/components/menu/DropdownMenu.module.css` | ui | discovered (not in manifest) → F-18 | T-ANIMAL-007 (menu styles moved here from `EntityGrid.module.css`) |
| ui | `src/framework/design-system/components/modal/use-modal-navigate.ts` | ui | discovered (not in manifest) → F-18 | T-ANIMAL-008 / T-ANIMAL-004 (`useModalPreload`, called by `ManageAnimals.tsx:27-31`) |
| ui | `src/framework/json-schema-form/services/json-schema-data.service.ts` | ui | discovered (not in manifest) → F-18 | T-ANIMAL-004 (schema cache, 5-minute TTL, `prefetchUnityJsonSchema`) |
| ui | `src/framework/api/unity-api-fetch.ts` | ui | discovered (not in manifest) → F-18 | T-ANIMAL-003 / T-ANIMAL-008 (`isUnityApiSuccess` accepts `accessToken`, needed by the sign-in normalisation so `animals_write` reaches the session) |
| ui | `src/framework/design-system/buttons/button/Button.module.css` | ui | dependency (read for context) | `primaryAction` / `secondaryAction` colours behind F-21 |
| ui | `src/framework/design-system/components/modal/ModalShell.module.css` | ui | dependency (read for context) | header and close button use `--primary-action` / `--ink-white` (F-21) |
| ui | `src/framework/design-system/components/modal/use-modal-dismiss.ts` | ui | dependency (read for context) | `dismissHref` back to `/examples/animals` (T-ANIMAL-008 S4) |
| ui | `src/features/design-system-showcase/DesignSystemShowcase.tsx` | ui | dependency (read for context) | no `DropdownMenu` section (F-20); `Switch` present |
| ui | `src/features/reference-data/**` (incl. `ManageReferenceDataItemsModal.tsx`) | ui | consumer of changed shared code (read for regressions) | now calls `useModalPreload`; grids still use text buttons (T-ANIMAL-007 S8) |
| ui | `next.config.ts` | ui | dependency (read for context) | `reactStrictMode: true` (explains 2 list requests on first load in dev) |
| api | `Api.Framework.Services/Auth/DefaultUserSeeder.cs`, `Api.Framework/Program.cs:104-107` | api | dependency (read for the browser check only) | Development default user used to sign in; values passed by env var, never printed or stored |

- Manifest: 82 files · Discovered (not in manifest): 5 (F-18) · Diff / dependency: 7 (read for context only)
- Changed since round 2: UI only.
  - 18:02–18:03: the auth normalisation (`normalize-auth-state.ts`, `authorisation.data-provider.ts`, `token-refresh.service.ts`, `unity-api-fetch.ts`).
  - 18:30–18:31: the list-on-page change (`manage-animals/*`, routes, `animal-routes.ts`, `AnimalFormModal.tsx`, `AnimalsModalRoutes.tsx`, rules). `AnimalsLanding.tsx`, `ManageAnimalsModal.tsx` and `@modal/(.)manage/page.tsx` were removed.
  - 18:40: `DropdownMenu`, `EntityGrid*`, `useModalPreload`, the schema cache, `tokens.css`, the design-system README / index and rules.
  - API.Framework is unchanged since round 2.
- Whole files reviewed: yes (plan scope)
- Not implemented (no file in scope): none
- Deferred: none. T-ANIMAL-003 S12 (server-side paging) and S13 (empty state) were drafts when this round started. Neil accepted Q37 at 19:00 (History row 24), so they are final and assessed normally below.
- Excluded: outside `review.scope_include` (only API / UI code is reviewed): planning artefacts (specs, tickets, journey, `handoff.md`) read as the reference only; `review.scope_exclude`: `bin/`, `obj/`, `node_modules/`, `.next/`, generated `tsconfig.tsbuildinfo`, and `UI.NextJs.Framework/.env.local` (never opened). Consumers of the changed shared code were checked for regressions but not re-reviewed: reference-data grids, form modals and `ManageReferenceDataItemsModal`, `SignInForm`.

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix |
|----|----------|------|-----------|---------|-----------------------|---------------|
| F-18 | Minor | Process / manifest | `ui/UI.NextJs.Framework/src/framework/design-system/components/menu/DropdownMenu.tsx:1`, `DropdownMenu.module.css:1`, `src/framework/design-system/components/modal/use-modal-navigate.ts:1`, `src/framework/json-schema-form/services/json-schema-data.service.ts:1`, `src/framework/api/unity-api-fetch.ts:1` | Manifest incomplete: five files that this change added or changed, and that the feature depends on, aren't in `implementation.ui`. They are `DropdownMenu.tsx` / `.module.css` (the T-ANIMAL-007 row menu is now built on them), `use-modal-navigate.ts` (`useModalPreload`, called by `ManageAnimals.tsx:27-31`), `json-schema-data.service.ts` (the schema cache and prefetch the Animals form uses) and `unity-api-fetch.ts` (`isUnityApiSuccess` now accepts `accessToken`, which the sign-in normalisation relies on). I found them by following imports and reviewed them in full. Nothing in them is wrong apart from F-20, F-23 and F-24. | `loops/pr-review.md` stage 1 / `skills/build-review-scope` → every discovered file gets a "manifest incomplete" Minor | Add the five paths to `implementation.ui` with change, tickets and controls |
| F-19 | Nit | Process / manifest | `ai-planning-framework/work/manage-animals/handoff.md` → `implementation` (notes / tickets on the page files) | After decision 28, the manifest still cites the old T-ANIMAL-003 S1 / S10 / S11 and lists the page files (`page.tsx`, `manage/page.tsx`, `ManageAnimalsPage.tsx`, `SiteNav.tsx`, the full-page form fallbacks) under T-ANIMAL-003 only. I've read those as T-ANIMAL-008 S1 / S2 / S3, as the decision's mapping says, so nothing is dangling. It's housekeeping only. | Decision 28 (`handoff.md` Notes, History row 23); `checklists/severity.md` → Nit (no effect on behaviour or traceability once mapped) | When the manifest is next written, tag the page files with T-ANIMAL-008 and use the new scenario IDs |
| F-20 | Minor | UI standards | `ui/UI.NextJs.Framework/src/features/design-system-showcase/DesignSystemShowcase.tsx:1` (no `DropdownMenu` section); `src/framework/design-system/README.md:49`, `index.ts:12-16` | `DropdownMenu` is a new user-visible design-system control. It's exported and documented in the README, but `DesignSystemShowcase` has no section for it, and the rule calls the showcase "the visual contract". | Next.js `.cursor/rules/style/nextjs-design-system.mdc:152-153` → "add a section (or controls) to `DesignSystemShowcase` when the control is user-visible … the showcase page is the visual contract"; `checklists/ui-nextjs-checklist.md` B | Add a small showcase section: a `DropdownMenu` with two items (one with an icon), opened from a `secondary-action` button, ideally near the bottom so the flip is visible |
| F-21 | Minor | UI standards / accessibility (live browser) | `ui/UI.NextJs.Framework/src/framework/design-system/theme/tokens.css:21-23` and `:43`; used by `buttons/button/Button.module.css:25-34`, `components/modal/ModalShell.module.css:16-17,60-61` | In dark mode the buttons on every Animals screen have too little contrast. The secondary buttons (Actions, Cancel, Sign out) keep a white fill (`--app-secondary-action-bg: var(--ink-white)` has no dark value) while their text and border follow the lightened `--primary-action` `#6aa3c9`: 2.73:1. The primary buttons (+ Add Animal, Save) and the modal header close "×" put `--ink-white` text on that same `#6aa3c9`: 2.73:1. Measured live with computed styles; see shots 14, 15, 16 and 17. Light mode passes (all ≥ 4.5:1). The tokens predate this plan, but this change puts them on the new Actions trigger and the form footer, and `tokens.css` is in the manifest. That's why this is a finding and not a pre-existing note. Neil also saw this in his 18:06 check. | Next.js `.cursor/rules/style/nextjs-css.mdc` → Dark mode ("semantic tokens that already change under that selector"); `checklists/ui-nextjs-checklist.md` B (dark mode through semantic tokens) and C (accessibility); general practice WCAG 2.1 AA 1.4.3 (4.5:1 for text) | In the `html[data-theme='dark']` block, give the secondary action its own dark values (e.g. `--app-secondary-action-bg: var(--app-surface-raised)` with `--app-secondary-action-fg: var(--app-text-primary)`). Add a foreground token for primary fills (e.g. `--app-primary-action-fg`, `var(--ink-white)` in light and `var(--ink-100)` in dark; `#18181b` on `#6aa3c9` is 6.49:1). Use it in `Button.module.css:27` and `ModalShell.module.css:17,61` |
| F-22 | Minor | UI standards / accessibility (live browser) | `ui/UI.NextJs.Framework/src/framework/json-schema-form/components/JsonSchemaForm.module.css:111`; `src/framework/design-system/theme/tokens.css:20` | In dark mode the tag-chip remove "×" (T-ANIMAL-006) is `--app-form-error-text` (`#cf1337`) on the dark chip `#3d4854`: **1.69:1** measured live (shot 16), so it's very hard to see. `--app-form-error-text` has no dark value. By the same token, field error messages and the required "*" would be about 2.09:1 on the dark modal surface (calculated, not measured live; I tested validation in light mode). | Same as F-21 (`style/nextjs-css.mdc` → Dark mode; checklist B / C; WCAG 1.4.3 / 1.4.11) | Add a dark `--app-form-error-text` that reaches 4.5:1 on `--app-surface-raised` / `--app-input-bg` (e.g. `#ff9aa8`: 4.63:1 on the chip, 6.12:1 on the surface). Or colour the chip "×" with `--app-text-primary` (7.7:1) and keep red for messages |
| F-23 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/auth/normalize-auth-state.ts:1`, `src/framework/auth/providers/authorisation.data-provider.ts:1`, `src/framework/auth/token-refresh.service.ts:1`, `src/framework/api/unity-api-fetch.ts:1` | The four auth / API files changed at 18:02–18:03 start with a UTF-8 BOM and have mixed line endings (one CRLF line, the rest LF). No other file in `src/` has a BOM. | General practice (consistency; `style/nextjs-formatting.mdc` doesn't cover BOM or EOL, so formatter-level and capped at Nit) | Re-save the four files as UTF-8 without BOM, with consistent line endings |
| F-24 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/json-schema-form/services/json-schema-data.service.ts:18,27-29`; `src/framework/auth/providers/authorisation.data-provider.ts:56-58` | The new schema cache's comment says it "also runs on sign-out / auth cleared", but it only listens for `unity-auth-cleared`, which the token-refresh failure path dispatches. A manual Sign out (`signOut()` → `clearAuthState()`) doesn't dispatch it. Today the impact is nil: schemas aren't user-specific, the 5-minute TTL bounds them, and the API still checks `animals_write` on every call. The comment just promises more than the code does. | General practice (comment accuracy; capped at Minor, and Nit as there's no behavioural effect) | Dispatch `unity-auth-cleared` (or call `clearUnityJsonSchemaCache()`) in `signOut()`, or reword the comment |
| F-25 | Nit | UI standards / spec question | `ui/UI.NextJs.Framework/src/framework/entity-framework/grid/grid-cell-renderers.tsx:6-8`; `src/framework/design-system/forms/switch/Switch.tsx:36-37`; `Switch.module.css:9-12` | The grid's Is Furry / Has Hooves switches are read-only as specified (`specs/manage-animals.yaml:64-73`; T-ANIMAL-003; T-ANIMAL-006). `renderBooleanSwitchCell` renders `<Switch readOnly>`, which maps to `disabled`, so clicks do nothing and send no request (verified live; screenshots `/workspace/manage-animals-check/switches-1-before.png` to `switches-4-after-reload.png`). The only visual cue is `opacity: 0.7` and the default cursor, so a read-only switch is barely distinguishable from an editable one (compare shot 07 with the form switches in shot 11). | General practice (affordance; capped at Nit, as the behaviour matches the spec) | Consider stronger read-only styling (e.g. no hover state and a muted track, or a check / dash glyph) or a tooltip such as "Edit the animal to change this". Whether the display should change is a spec question for Neil, not a PR fix |

Round 2 findings still open (unchanged code, so not repeated in full; see `reviews/DIRECT-manage-animals-2-review.md`):

| ID | Severity | File:line | Status this round |
|----|----------|-----------|-------------------|
| F-13 | Nit | `api/API.Framework/Api.Framework/Controllers/V1/Animals/AnimalController.cs:28` | Still open. GET-by-id still returns a bare `NotFound()`; confirmed live: the deleted-record URL shows the generic "This record could not be found. It may have been deleted." (shot 20) |
| F-14 | Nit | `ui/UI.NextJs.Framework/src/framework/design-system/forms/switch/Switch.tsx:43`, `Switch.module.css:49` | Still open (no final newline) |
| F-15 | Nit | `api/API.Framework/Api.Framework.Data/Models/Animal.cs:28` and the eight other API files listed in round 2 | Still open (no final newline; API unchanged) |

## Browser verification (live)

Run on 08/10/2026 at about 18:55–19:00 (Europe/London) against the running dev servers on Neil's PC: UI `http://localhost:3003` (Next.js dev, `reactStrictMode: true`), API.Framework on 5088 / 7088. I didn't start or restart anything.
- **Sign-in:** the Development default seeded user. The credentials came from `DefaultUserSeeder.cs` (seeded only when `IsDevelopment()`), were passed to a child process via environment variables, and were never printed, logged or written.
- **Tooling:** the existing Playwright in `ui/Unity.UI.Framework/e2e/node_modules`, Chromium, scripts in a temp folder outside the repos.
- **Data:** I only touched my own row "ZZ Test Animal 202610081756" and deleted it through the UI. A follow-up run confirmed 0 matching rows. I ignored the other worker's "ZZ Demo Animal" row.
- **Screenshots:** on the box in `/workspace/manage-animals-check/round3/` (file names below; `01-sign-in-page.png` etc.). Neil's 18:06 screenshots of the old modal version are in `/workspace/manage-animals-check/`.

| Check | Result | Evidence |
|-------|--------|----------|
| Nav and route (T-ANIMAL-008 S1) | ✓ "Animals" → `/examples/animals`. H1 "Manage Animals", sub-text "Animal catalogue", "+ Add Animal" and the grid on the page; 0 dialogs open | `02-list-page-light.png`; `ManageAnimalsPage.tsx:14-25`, `SiteNav.tsx:32-37` |
| List-pages rule | ✓ No list modal, no auto-open, no landing page. Filters: none by spec (`search_filters: []`), so not a gap | `02`; `nextjs-list-pages.mdc` |
| Old URL (T-ANIMAL-008 S6) | ✓ `/examples/animals/manage` → `/examples/animals`, 0 dialogs | `manage/page.tsx:6-8` |
| Add form over the page (S4, T-ANIMAL-003 S7) | ✓ `/manage/item`, "Add Animal", list visible behind, 1 dialog; Escape closes only the form and returns to `/examples/animals` | `03-add-form-required-markers.png`, `06-add-form-filled.png` |
| Required markers and validation | ✓ " *" on Name and Date Born, none on Attributes; switches Off. Empty Save → "Name is required" / "Date Born is required". Today → "Date Born must be before today" | `03`, `04-add-form-empty-submit-validation.png`, `05-add-form-date-today-validation.png` |
| Create | ✓ Trimmed name saved, form closed, one list refresh. Row: "ZZ Test Animal 202610081756 · 15/03/2020 · nocturnal, review-r3 · 08/10/2026 18:56 System Administrator". Headers: Name ↑, Is Furry, Has Hooves, Date Born, Attributes, Last Amended, Actions | `07-list-with-test-animal.png` |
| **Row actions menu visible (light)** | ✓ Portalled to `<body>`, `position: fixed`. Box 160×76 at (1128, 415) at 1440×900, 100% inside the viewport, no clipping ancestor; both items hit-test as the top-most element. Also fully visible on the last row and at 1024×600. With the viewport height cut to 382 it flips above the trigger (still 100% visible) | `08-row-menu-open-light.png`, `09-row-menu-last-row-light.png`, `10-row-menu-1024x600-light.png`, `21-row-menu-flip-above-light.png`; `DropdownMenu.tsx:85-101,189-193`, `DropdownMenu.module.css:6-8` |
| **Row actions menu visible (dark)** | ✓ Fully visible (160×76 at 1133, 415); menu items 9.6:1 | `15-row-menu-open-dark.png` |
| Menu keyboard | ✓ Escape closes only the menu, focus returns to "Actions", 0 dialogs | `DropdownMenu.tsx:119-124,67-69` |
| Edit (T-ANIMAL-004 S10) | ✓ Loaded values correct; name changed to "… edited" and Has Hooves on; saved; one list refresh | `11-edit-form-loaded.png`, `12-list-after-edit.png` |
| Duplicate name (T-ANIMAL-004 S4) | ✓ Lower-case padded duplicate → "An animal with this name already exists" on Name; form stays open | `13-duplicate-name-validation.png` |
| **Dark-mode legibility** | ✗ Secondary buttons (Actions, Cancel, Sign out) 2.73:1, primary buttons (+ Add Animal, Save) 2.73:1, modal close "×" 2.73:1 → **F-21**. Tag-chip "×" 1.69:1 → **F-22**. Menu items and the red Delete (5.52:1) pass | `14-list-page-dark.png`, `16-edit-form-dark.png`, `17-delete-confirm-dark.png` |
| Delete (T-ANIMAL-005) | ✓ "Delete ZZ Test Animal 202610081756 edited?", red Delete; Escape on the confirm closes only the confirm; Delete removes the row with one refresh and no error | `17`, `18-delete-confirm-light.png`, `19-list-after-delete.png` |
| Deleted-record Edit URL (T-ANIMAL-004 S12) | ✓ "This record could not be found. It may have been deleted." over the list (generic text → F-13) | `20-deleted-animal-edit-url.png` |
| Direct form URL (T-ANIMAL-008 S5) | ✓ `/manage/item` opened directly: page and grid with the form on top; Cancel → `/examples/animals`, 0 dialogs | `22-direct-add-url-fallback.png`; `manage/item/page.tsx:4-10` |
| No permission (T-ANIMAL-008 S2 / S3) | ✓ Simulated by removing `animals_write` from the client-side session only; the API still enforces the policy. No "Animals" link, no grid, "You do not have permission to manage animals.", 0 `v1/Animal` calls; same on `/manage/item` with 0 dialogs | `25-simulated-no-permission-page.png`, `26-simulated-no-permission-form-url.png` |
| Existing text-button grids (T-ANIMAL-007 S8) | ✓ Reference data grid still shows its text buttons; its items modal opens (it predates the list-pages rule) | `23-reference-data-page.png`, `24-reference-data-items-modal.png` |
| List reloads | 2 × `GET v1/Animal` on first load and on remount after the direct-URL Cancel. That matches React StrictMode's double effect in dev (`next.config.ts:4`), not a defect. After create, edit and delete there is exactly 1 refresh each, so the 2–3 reloads Neil saw on the old modal version are gone. Production build not assessed | run logs |

## Spec conformance (per control)

Spec: `specs/add-edit-animal.yaml` — Basic Form — Add \| Edit Animal (unchanged since round 2; the form code is unchanged except `dismissHref`, now `animalsListHref`, `AnimalFormModal.tsx:22,70`)

| Section / step | Control | Control type | Mandatory | Editable | Enablement | Min / max | Validation message | Status | Notes / finding |
|----------------|---------|--------------|-----------|----------|------------|-----------|--------------------|--------|-----------------|
| Animal Details | Name | Keyed Input → text `Input` (`unity-json-form-renderers.tsx:34-63`) | Yes ✓ server ✓ UI marker (live ✓) | Yes ✓ | Always ✓ | 1–100 ✓ | "Name is required" ✓ live; "An animal with this name already exists" ✓ live | Match | Trimmed on save ✓ live |
| Animal Details | Date Born | Date Picker → native date `Input` | Yes ✓ server ✓ UI marker (live ✓) | Yes ✓ | Always ✓ | N/A ✓ | "Date Born is required" ✓ live; "Date Born must be before today" ✓ live | Match | |
| Animal Details | Attributes | Tag Input → `UnityTagInputControl` (`unity-json-form-renderers.tsx:282-353`) | No ✓ | Yes ✓ | Always ✓ | 0–50 per tag, max 20 ✓ | limits ✓ (code) | Match | Dark-mode chip "×" → F-22 |
| Characteristics | Is Furry | Switch → `UnitySwitchControl` | No ✓ | Yes ✓ | Always ✓ | N/A | none ✓ | Match | Default Off ✓ live |
| Characteristics | Has Hooves | Switch → `UnitySwitchControl` | No ✓ | Yes ✓ | Always ✓ | N/A | none ✓ | Match | Default Off ✓ live; toggled and saved ✓ live |
| (form) | Save / Cancel | Buttons (`AnimalFormModal.tsx:76-90`) | — | — | Save disabled while loading / saving ✓ | — | Field errors on controls; record-level errors in the modal ✓ | Match | Closes to `/examples/animals` ✓ live; dark-mode contrast → F-21 |

Manage list: `specs/manage-animals.yaml` — Paginated Grid — Manage Animals ("Animal catalogue"), route `/examples/animals`

| Column / action | Population source / action on click | Display format / sortable | Status | Notes / finding |
|-----------------|-------------------------------------|---------------------------|--------|-----------------|
| (page) Title / sub-text | "Manage Animals" / "Animal catalogue" in `PageLayout` header (`ManageAnimalsPage.tsx:14-21`) | — | Match | live ✓ (shot 02) |
| Search filters | none (`search_filters: []`) | — | Match | Nothing rendered; correct |
| + Add Animal | Open Add \| Edit Animal in Add mode (`use-animals-grid.tsx:74-82`) | Primary action / — | Match | live ✓; shown only with `animals_write` ✓; dark contrast → F-21 |
| Name | `Animal.Name` (`animals-grid-columns.tsx:14-19`) | Char / Yes, default ascending ✓ | Match | live ✓ ("Name ↑") |
| Is Furry | `Animal.IsFurry` (`animals-grid-columns.tsx:20-25`) | Switch, read-only / Yes ✓ | Match | Read-only styling → F-25 |
| Has Hooves | `Animal.HasHooves` (`animals-grid-columns.tsx:26-32`) | Switch, read-only / Yes ✓ | Match | Read-only styling → F-25 |
| Date Born | `Animal.DateBorn` (`animals-grid-columns.tsx:33-38`) | DD/MM/YYYY ✓ / Yes ✓ | Match | live ✓ "15/03/2020" |
| Attributes | `Animal.Attributes` (`animals-grid-columns.tsx:39-44`) | Comma-separated ✓ / No ✓ | Match | live ✓ |
| Last Amended | `Animal.UpdatedUtc` & `UpdatedBy` → display name (`animals-grid-columns.tsx:45-55`) | "DD/MM/YYYY HH:MM Display name", local time ✓ / Yes ✓ | Match | live ✓ "08/10/2026 18:56 System Administrator" |
| Actions column | Last column, header "Actions", not sortable (`EntityGrid.tsx:70-80`) | — / No ✓ | Match | Row click does nothing ✓ |
| Edit Animal (icon Edit) | Edit mode (`use-animals-grid.tsx:55-61`) via `DropdownMenu` (`EntityGridRowActionsMenu.tsx:29-45`) | Menu item / — | Match | Fully visible light and dark ✓ live (F-17 fixed); Escape / focus ✓ |
| Delete Animal (icon Delete) | "Delete &lt;Name&gt;?" Cancel / Delete, soft delete, refresh (`use-animals-grid.tsx:63-72,90-106`; `ManageAnimals.tsx:41-53`) | Menu item / — | Match | live ✓ |
| Paging | Server-side; page size 20, options 5, 10, 20, 50, 100, 200 (Q37, accepted) | Paginator (`EntityGrid.tsx:184-195`; `EntityGridPaginator.tsx:40`, `entity-grid-config.ts:6`) | Match | `use-animals-grid.tsx:24-29,50`; API `AnimalService.cs:31-34` (Skip / Take, max 200). Live: "Items per page: 20", "1 – 2 of 2" |
| Empty state | "No results", "+ Add Animal" still shown (Q37, accepted) | — | Match | `EntityGrid.tsx:93-112,121-122`: the toolbar with "+ Add Animal" stays when there are no rows. Not exercised live (I don't touch other rows) |
| No-permission callout | "You do not have permission to manage animals." (`AnimalsAccessNotice.tsx`) | Warning `Callout` / — | Match | live ✓ (simulated) |

## Data mapping (per control)

No mapping code changed in this round (API unchanged; the UI list / form bindings are byte-identical to round 2 apart from line endings). Re-checked against the specs:

| Control | Spec: Service · Table.Column | UI binding | API record / DTO | Mapper | Entity / downstream model | Migration | Status |
|---------|------------------------------|------------|------------------|--------|---------------------------|-----------|--------|
| Name | Animals · `Animal.Name` (+ derived `NormalizedName`) | `#/properties/name` | `AnimalWriteRequest.Name` → `AnimalRecord.Name` | `AnimalService.cs:166-177` (trim), `:78-79`, `:129-130` | `Animal.Name`, `Animal.NormalizedName` (`Animal.cs:7,9`) | `20261008150221_AddAnimals.cs` (`name`, `normalized_name` varchar(100)) | Mapped |
| Date Born | Animals · `Animal.DateBorn` | `#/properties/dateBorn` | `AnimalWriteRequest.DateBorn` → `AnimalRecord.DateBorn` | `AnimalService.cs:80,131`; UI `unity-schema-value.mapper.ts:90-94` (date only) | `Animal.DateBorn` (`DateOnly`, `Animal.cs:11`) | `date_born` date | Mapped |
| Attributes | Animals · `Animal.Attributes` | `#/properties/attributes` | `AnimalWriteRequest.Attributes` (`[]` when missing) | `AnimalService.cs:175,276-277`; UI `unity-schema-value.mapper.ts:22-28` (`submitEmptyArrays`) | `Animal.Attributes` (jsonb, default `'[]'`, `LoginDbContext.cs:462`) | `attributes` jsonb | Mapped |
| Is Furry | Animals · `Animal.IsFurry` | `#/properties/isFurry` | `AnimalWriteRequest.IsFurry` | `AnimalService.cs:82,133` | `Animal.IsFurry` | `is_furry` boolean default false | Mapped |
| Has Hooves | Animals · `Animal.HasHooves` | `#/properties/hasHooves` | `AnimalWriteRequest.HasHooves` | `AnimalService.cs:83,134` | `Animal.HasHooves` | `has_hooves` boolean default false | Mapped |
| Last Amended (list) | Animals · `Animal.UpdatedUtc` & `UpdatedBy` → `User.DisplayName` / `User.Email` | grid column `updatedUtc` | `AnimalModel.UpdatedUtc`, `UpdatedByName` | `AnimalService.cs:205-229` | `Animal.UpdatedUtc`, `Animal.UpdatedBy` → `User` (FK restrict, `LoginDbContext.cs:472-476`) | `updated_utc`, `updated_by` + `fk_animals_users_updated_by` (principal schema `auth`) | Mapped |
| (soft delete) | Animals · `Animal.IsDeleted` | — | — | `AnimalService.cs:160-162` | `Animal.IsDeleted` | `is_deleted` boolean default false; filtered unique index `NOT is_deleted` | Mapped |

`UpdatedUtc` / `UpdatedBy` are set from `TimeProvider` and the JWT `sub` claim on create, update and soft delete (`AnimalService.cs:86-87,135-136,161-162`). The delete now goes through `AnimalEntityDataProvider.deleteById` (`use-animals-grid.tsx:95`), which hits the same `v1/Animal/{id}` DELETE.

Columns or properties in the reviewed code that are not in any linked spec:

- none. `Id`, `CreatedUtc`, `NormalizedName` and `IsDeleted` are specified by T-ANIMAL-001 (table design), not by a control.

## Acceptance criteria coverage (per scenario)

All 67 scenarios in T-ANIMAL-001 to 008 after decision 28. There is still no automated test project in API.Framework (by rule) and no test runner in UI.NextJs.Framework, so no scenario can be **Covered**. Scenarios whose code I traced and found correct are marked **Partial** with "code ✓". Where I also exercised them in the browser, the row says "live ✓" (screenshot numbers refer to `/workspace/manage-animals-check/round3/`). The old T-ANIMAL-003 S1 / S10 / S11 now appear as T-ANIMAL-008 S1 / S2 / S3. T-ANIMAL-003 S12 / S13 became final when Neil accepted Q37 at 19:00, so they are assessed normally.

| Scenario ID | Scenario | Status | Code reference(s) | Test reference(s) | Notes |
|-------------|----------|--------|-------------------|-------------------|-------|
| T-ANIMAL-001/S1 | Animal table stores all mapped columns | Partial | `Animal.cs:3-28`; `LoginDbContext.cs:455-477`; `20261008150221_AddAnimals.cs:19-46` | none | code ✓ (snake_case columns, `creatures.animals`) |
| T-ANIMAL-001/S2 | Attributes default to an empty array | Partial | `LoginDbContext.cs:462`; `Animal.cs:13` | none | code ✓ |
| T-ANIMAL-001/S3 | Normalised name is unique among non-deleted rows | Partial | `LoginDbContext.cs:467-470`; `20261008150221_AddAnimals.cs:64-70` | none | code ✓ (filtered unique index `NOT is_deleted`) |
| T-ANIMAL-001/S4 | A soft-deleted animal's name can be reused | Partial | `LoginDbContext.cs:467-470` | none | code ✓ |
| T-ANIMAL-001/S5 | Soft-deleted flag exists | Partial | `Animal.cs:19`; `LoginDbContext.cs:465` | none | code ✓ |
| T-ANIMAL-001/S6 | Table lives in the creatures schema | Partial | `LoginDbContext.cs:12,457`; `20261008150221_AddAnimals.cs:16-20`; `AnimalService.cs:15` | none | code ✓; comment now says `creatures.animals` (F-07 resolved) |
| T-ANIMAL-001/S7 | The animals permission is seeded for our users | Partial | `LoginPermissions.cs:36`; `LoginDbContext.cs:482-503`; `20261008150221_AddAnimals.cs:48-62` | none | code ✓ (Administrators and Standard groups) |
| T-ANIMAL-002/S1 | Create animal with valid fields | Partial | `AnimalService.cs:56-100`; `AnimalController.cs:31-42` | none | code ✓ |
| T-ANIMAL-002/S2 | Missing Attributes are stored as an empty array | Partial | `AnimalService.cs:170-177,276-277` | none | code ✓ |
| T-ANIMAL-002/S3 | Duplicate name is rejected | Partial | `AnimalService.cs:69-71,92-97` | none | code ✓ (409 + exact message, also on a unique-index race) |
| T-ANIMAL-002/S4 | Name of a soft-deleted animal can be reused | Partial | `AnimalService.cs:69` | none | code ✓ |
| T-ANIMAL-002/S5 | Date Born must be before today | Partial | `animalSchema.json:26-36`; `DateCompareValidator.cs` | none | code ✓ (UTC date) |
| T-ANIMAL-002/S6 | Date Born is mandatory | Partial | `animalSchema.json:4,25,35` | none | code ✓ |
| T-ANIMAL-002/S7 | Name is mandatory | Partial | `animalSchema.json:10-17`; `AnimalService.cs:166-177,261-265` | none | code ✓ (whitespace-only name → "Name is required") |
| T-ANIMAL-002/S8 | Attribute tag limits | Partial | `animalSchema.json:39-53` | none | code ✓ |
| T-ANIMAL-002/S9 | List returns non-deleted animals with Last Amended | Partial | `AnimalService.cs:28-47,205-229` | none | code ✓ (DisplayName, fallback Email) |
| T-ANIMAL-002/S10 | Soft delete and not found afterwards | Partial | `AnimalService.cs:49-54,108-111,149-165`; `AnimalController.cs:28` | none | code ✓ (GET returns 404; body → F-13) |
| T-ANIMAL-002/S11 | Users without animals_write are rejected on every endpoint | Partial | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` | none | code ✓ |
| T-ANIMAL-002/S12 | User-management permissions alone do not grant access to animals | Partial | `Program.cs:86-87`; `AnimalPolicies.cs:8-10` | none | code ✓ (no `DirectoryPolicies` on animal endpoints) |
| T-ANIMAL-002/S13 | AnimalsWrite guards every animal endpoint | Partial | `AnimalController.cs:17-58`; `AnimalSchemaController.cs:15` | none | code ✓ |
| T-ANIMAL-003/S2 | List shows non-deleted animals | Partial | `animals-search.data-provider.ts:13`; `animals-grid-columns.tsx:13-56`; `AnimalService.cs:30` | none | code ✓, live ✓ (deleted row gone; shot 19) |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user | Partial | `animals-grid-columns.tsx:45-55`; `grid-cell-renderers.tsx:25` | none | code ✓, live ✓ ("08/10/2026 18:56 System Administrator") |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | Partial | `grid-cell-renderers.tsx:25` | none | code ✓, live ✓ (18:56 BST for a save at 17:56 UTC) |
| T-ANIMAL-003/S5 | Last Amended outside summer time | Partial | `grid-cell-renderers.tsx:25` | none | code ✓ (uses the browser's own offset; not testable live in October) |
| T-ANIMAL-003/S6 | Default sort by Name ascending | Partial | `use-animals-grid.tsx:27,49`; `AnimalService.cs:234-250` | none | code ✓, live ✓ ("Name ↑") |
| T-ANIMAL-003/S7 | Add opens Basic Form | Partial | `use-animals-grid.tsx:74-82`; `app/examples/animals/@modal/(.)manage/item/page.tsx` | none | code ✓, live ✓ (shot 03) |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | Partial | `use-animals-grid.tsx:55-61`; `use-json-schema-entity-form.ts:182-198` | none | code ✓, live ✓ (shot 11) |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | Partial | `EntityGrid.tsx:44-53,70-80,146-153`; `EntityGridRowActionsMenu.tsx:27-45`; `use-animals-grid.tsx:52-73` | none | code ✓, live ✓ (menu fully visible; shots 08–10, 15, 21) |
| T-ANIMAL-003/S12 | Results are paged on the server | Partial | `use-animals-grid.tsx:24-29,50`; `EntityGrid.tsx:184-195`; `EntityGridPaginator.tsx:40,84,94`; `entity-grid-config.ts:6`; `AnimalService.cs:28-47` | none | code ✓ (20 per page, options 5–200, next page re-queries `v1/Animal` with `pageIndex`). Live: page size 20 shown; more than 20 rows not exercised |
| T-ANIMAL-003/S13 | No animals to show | Partial | `EntityGrid.tsx:93-112,121-122` | none | code ✓ ("No results"; the toolbar keeps "+ Add Animal"). Not exercised live: the DB has another user's row, which I didn't touch |
| T-ANIMAL-004/S1 | Add mode opens with defaults | Partial | `unity-schema.adapter.ts:125-136`; `animalSchema.json:59,65`; `unity-json-form-renderers.tsx:52` | none | code ✓, live ✓ (" *" on Name and Date Born only; both switches Off; shot 03) |
| T-ANIMAL-004/S2 | Create animal with required fields | Partial | `use-json-schema-entity-form.ts:219-262`; `unity-schema-value.mapper.ts:15-31`; `AnimalFormModal.tsx:32-35` | none | code ✓, live ✓ (trimmed name saved; form closed; one list refresh; shot 07) |
| T-ANIMAL-004/S3 | Name is mandatory | Partial | `unity-schema-validation.ts:214-223`; `animalSchema.json:14-17`; `unity-json-form-renderers.tsx:52` | none | code ✓, live ✓ ("Name is required"; shot 04) |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | Partial | `api-error.utils.ts:26-60`; `use-json-schema-entity-form.ts:253-257` | none | code ✓, live ✓ (lower-case padded duplicate → "An animal with this name already exists" on Name, form stays open; shot 13) |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | Partial | `AnimalService.cs:69` | none | code ✓ |
| T-ANIMAL-004/S6 | Date Born must be before today | Partial | `unity-schema-validation.ts:100-163` | none | code ✓, live ✓ (today → "Date Born must be before today"; shot 05) |
| T-ANIMAL-004/S7 | Date Born is mandatory | Partial | `unity-schema-validation.ts:214-223`; `unity-json-form-renderers.tsx:52` | none | code ✓, live ✓ ("Date Born is required"; shot 04) |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | Partial | `unity-schema-value.mapper.ts:22-28`; `AnimalService.cs:276-277` | none | code ✓, live ✓ ("nocturnal, review-r3" shown after save and reloaded in Edit; shots 07, 11) |
| T-ANIMAL-004/S9 | Attribute tag limits | Partial | `unity-schema-validation.ts:225-232`; `unity-json-form-renderers.tsx:348-350` | none | code ✓ |
| T-ANIMAL-004/S10 | Edit persists changed fields | Partial | `use-json-schema-entity-form.ts:243-247`; `AnimalService.cs:102-146` | none | code ✓, live ✓ (name and Has Hooves change saved; shot 12) |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | Partial | `animal-routes.ts:6`; `AnimalFormModal.tsx:53` | none | code ✓ (no View) |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | Partial | `AnimalService.cs:49-54`; `AnimalController.cs:28`; `use-json-schema-entity-form.ts:199-210`; `AnimalFormModal.tsx:93-94` | none | code ✓, live ✓ ("This record could not be found. It may have been deleted." over the list; shot 20; API body → F-13) |
| T-ANIMAL-005/S1 | Confirmation names the animal | Partial | `ManageAnimals.tsx:41-53` | none | code ✓, live ✓ ("Delete ZZ Test Animal … edited?", red Delete 5.52:1; shots 17, 18). Confirm now sits directly over the page at `level` primary, as the list-pages rule asks (F-16 closed) |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | Partial | `use-animals-grid.tsx:90-106`; `AnimalService.cs:149-165` | none | code ✓, live ✓ (row gone, one list refresh, no error; shot 19) |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | Partial | `ManageAnimals.tsx:50`; `use-animals-grid.tsx:118-120`; `Modal.tsx:76-88` | none | code ✓, live ✓ (Escape on the dark confirm closed only the confirm; the row stayed) |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | Partial | `AnimalService.cs:30,51,69,108,154` | none | code ✓ |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | Partial | `AnimalController.cs:57-58`; `use-animals-grid.tsx:67` | none | code ✓ |
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Partial | `unity-json-form-renderers.tsx:259-280`; `Switch.tsx:12-37` | none | code ✓, live ✓ (Has Hooves toggled in Edit and saved; shots 11, 12) |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Partial | `unity-json-form-renderers.tsx:282-353` | none | code ✓, live ✓ (two chips added; the chip "×" is hard to see in dark mode → F-22) |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Partial | `unity-json-form-renderers.tsx:348-350`; `unity-schema-validation.ts:225-232` | none | code ✓ |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Partial | `unity-json-form-renderers.tsx:263,273,287,317,330`; `Switch.tsx:36-37` | none | code ✓ |
| T-ANIMAL-006/S5 | Grid cells | Partial | `grid-cell-renderers.tsx:7-30`; `animals-grid-columns.tsx:24,31,43` | none | code ✓, live ✓ (read-only switches, DD/MM/YYYY, comma list; shots 07, 12; read-only styling → F-25) |
| T-ANIMAL-007/S1 | Row actions menu in the last column | Partial | `EntityGrid.tsx:70-80,146-153` | none | code ✓, live ✓ |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | Partial | `EntityGridRowActionsMenu.tsx:33-39`; `DropdownMenu.tsx:200-210` | none | code ✓, live ✓ (Edit and Delete hit-test and open for the right row; F-17 fixed) |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Partial | `EntityGrid.tsx:44-51`; `permissions.ts:6-13` | none | code ✓ |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Partial | `permissions.ts:10-12` | none | code ✓ |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Partial | `EntityGrid.tsx:70-80` | none | code ✓ |
| T-ANIMAL-007/S6 | Per-row visibility | Partial | `EntityGrid.tsx:52-53` | none | code ✓ |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Partial | `EntityGridRowActionsMenu.tsx:27` | none | code ✓ |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | Partial | `EntityGrid.tsx:155-171` | none | code ✓, live ✓ (reference data; shot 23) |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | Partial | `DropdownMenu.tsx:111-136` | none | code ✓, live ✓ (Escape closes only the menu, focus back on "Actions") |
| T-ANIMAL-008/S1 | Open Manage Animals from the nav (was T-ANIMAL-003 S1) | Partial | `SiteNav.tsx:32-37`; `app/examples/animals/page.tsx`; `ManageAnimalsPage.tsx:12-27` | none | code ✓, live ✓ (shot 02) |
| T-ANIMAL-008/S2 | User without animals_write cannot open Manage Animals (was T-ANIMAL-003 S10) | Partial | `ManageAnimals.tsx:16-21`; `AnimalsModalRoutes.tsx:16-20`; `AnimalsAccessNotice.tsx`; `SiteNav.tsx:32` | none | code ✓, live ✓ (simulated; 0 `v1/Animal` calls; shots 25, 26) |
| T-ANIMAL-008/S3 | User-management permissions alone do not give access (was T-ANIMAL-003 S11) | Partial | `animal-permissions.ts:6-8`; `use-animals-access.ts:13`; `Program.cs:86-87` | none | code ✓ (only `animals_write` is checked, UI and API); live as S2 |
| T-ANIMAL-008/S4 | Add \| Edit opens as a modal over the page and closes back to it | Partial | `AnimalFormModal.tsx:22,67-71`; `animal-routes.ts:2`; `@modal/(.)manage/item/page.tsx` | none | code ✓, live ✓ (Escape / Cancel → `/examples/animals`) |
| T-ANIMAL-008/S5 | Opening a form URL directly shows the page with the form on top | Partial | `manage/item/page.tsx:4-10`; `manage/item/[id]/page.tsx` | none | code ✓, live ✓ (shot 22) |
| T-ANIMAL-008/S6 | The old /manage URL redirects to the page | Partial | `manage/page.tsx:6-8` | none | code ✓, live ✓ |

## Security and data

| Spec rule / check | Status | Reference |
|-------------------|--------|-----------|
| Every animal endpoint (list, get, create, update, delete, form schema) requires `animals_write` | Enforced server-side (unchanged) | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` |
| User-management permissions alone give no access | Enforced server-side | `Program.cs:86-87`; UI `animal-permissions.ts:6-8` |
| Auth normalisation (new) | UI-only convenience: maps API.Framework's `accessToken` and nested `user.permissions` into the client session so the nav / grid gating works. It grants nothing; every call is still authorised by the API. No token values are logged | `normalize-auth-state.ts`; `authorisation.data-provider.ts`; `token-refresh.service.ts`; `unity-api-fetch.ts` |
| Schema cache (new) | Caches form schemas only (no record data), 5-minute TTL, cleared on `unity-auth-cleared`; not cleared on manual sign-out → F-24 (no data exposure) | `json-schema-data.service.ts:16-29` |
| Route prefetch (new) | Prefetches Next.js route code for row-action hrefs on hover / focus; no API data | `EntityGrid.tsx:55-68` |
| Name / Date Born / Attributes rules, uniqueness, soft delete, audit | Enforced server-side (unchanged since round 2) | see round 2 report; re-confirmed live for the name, date and uniqueness rules |
| Error messages don't leak internals | Yes | `use-animals-grid.tsx:97-100`; `use-json-schema-entity-form.ts:199-210` |
| Injection | No raw SQL; LINQ only | `AnimalService.cs` |
| Secrets / tokens | None in the reviewed code. `.env*` files not opened, created or edited; `src/config/environment.ts` unchanged; "committed" can't be checked without git. Browser check: credentials only via env vars in a child process, cleared afterwards; no cookie or token values read | — |
| PII | List shows the last amender's display name or email to `animals_write` users, as the spec requires | `AnimalService.cs:228` |
| Tenancy | Animals are global by design (spec notes) | `specs/manage-animals.yaml` notes |

## Tests

| Rule / scenario | Test | Status |
|-----------------|------|--------|
| Name mandatory / trimmed / ≤ 100 (T-ANIMAL-002/S7, T-ANIMAL-004/S3) | none | Untested |
| Name unique among non-deleted, reuse after delete (T-ANIMAL-001/S3-S4, T-ANIMAL-002/S3-S4, T-ANIMAL-004/S4-S5) | none | Untested |
| Date Born mandatory and before today (T-ANIMAL-002/S5-S6, T-ANIMAL-004/S6-S7) | none | Untested |
| Attribute limits (T-ANIMAL-002/S8, T-ANIMAL-004/S9, T-ANIMAL-006/S3) | none | Untested |
| Persistence of every column, `[]` default (T-ANIMAL-001/S1-S2, T-ANIMAL-002/S1-S2, T-ANIMAL-004/S2, S8, S10) | none | Untested |
| Soft delete and 404 afterwards (T-ANIMAL-002/S10, T-ANIMAL-005/S2, S4) | none | Untested |
| `AnimalsWrite` on every endpoint (T-ANIMAL-002/S11-S13, T-ANIMAL-005/S5) | none | Untested |
| UI scenarios T-ANIMAL-003 to -008 (including the round 1 fixes and the new page, menu portal and schema cache) | none | Untested (exercised by hand in the live browser check, see **Browser verification**) |

**Why these are not findings.** Same as rounds 1 and 2, and I've kept it consistent: `review-tests` would normally raise a Major for an untested mandatory, uniqueness or persistence rule, but API.Framework has no test project and its own rule (`api/API.Framework/.cursor/rules/api-framework-testing.mdc`) says not to create one "unless Neil asks", and UI.NextJs.Framework has no test runner (`checklists/ui-nextjs-checklist.md` C notes there is none in `package.json`). The implementing agent couldn't add tests without breaking that rule, so this is a tooling decision for the human owner (Neil), not a defect in this change, and it doesn't affect the verdict. It's a good fit for the `ai-test-framework` Neil is considering. The suggested tests from round 1 still stand.

Suggested tests (for when a test project is approved):

- `Create_NameBlankAfterTrim_ReturnsNameIsRequired` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — arrange a request with Name "   "; act `CreateAsync`; assert 400 and `validationErrors` name = "Name is required".
- `Create_DuplicateNameDifferentCase_ReturnsConflict` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — seed "Bessie"; create "  bessie "; assert 409 and "An animal with this name already exists".
- `Create_NameOfSoftDeletedAnimal_Succeeds` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — seed deleted "Bessie"; create "Bessie"; assert 201.
- `Create_DateBornToday_ReturnsBeforeTodayMessage` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — fake `TimeProvider`; DateBorn = today (UTC); assert 400 "Date Born must be before today".
- `Create_AttributesMissing_StoresEmptyArray` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — omit Attributes; assert stored `[]` and model `Attributes` empty.
- `Create_TwentyOneAttributes_ReturnsMaximumMessage` and `Create_AttributeOver50Chars_ReturnsLengthMessage` in the same class — assert the exact spec messages.
- `Delete_ExistingAnimal_SetsIsDeletedAndAudit` then `Get_DeletedAnimal_ReturnsNotFound` — assert `IsDeleted`, `UpdatedUtc` / `UpdatedBy`, then 404 (with "The animal was not found." once F-13 is done).
- `List_ExcludesDeleted_SortsByNameAndFallsBackToEmail` — seed users with and without DisplayName; assert order and `UpdatedByName`.
- `AnimalEndpoints_WithoutAnimalsWrite_Return403` — policy test per action (list, get, create, update, delete, schema) with a principal holding only `user_management_write`.
- UI (if a runner such as Vitest is added): `validateUnitySchemaData` cases for blank / whitespace Name, today's date in local time, 21 tags and a 51-character tag; `hasAnyPermission` any-of cases; `Modal` stack (Escape on a confirm over Manage Animals closes only the confirm); `DropdownMenu` Escape not reaching the modal, flip above near the viewport bottom and the menu staying inside the viewport; `useAnimalsGrid.confirmDelete` ignoring a second call while in flight and showing the API message on failure.

Checks run by the reviewer: a live browser check against the running dev servers (UI http://localhost:3003, API.Framework on 5088 / 7088), see **Browser verification**. No build, lint or automated tests run by the reviewer. The hand-off records `npm run build` passing after the list-on-page change, and no ESLint configuration (pre-existing).

## Changes since last review

Round 2 report: `reviews/DIRECT-manage-animals-2-review.md` (Approve; Blocker 0 · Major 0 · Minor 0 · Nit 4).

**Round 2 miss.** Round 2 judged the row actions menu from the code alone and approved it. In that version the menu rendered inside the grid. `EntityGrid.module.css:20` (`.tableWrap { overflow-x: auto }`, which makes the vertical overflow `auto` as well) and `:5` (`.grid { overflow: hidden }`) clipped it to a thin sliver, in light and dark mode. Neil's live check at about 18:06 found it, together with the dark-mode button contrast (now F-21) and the 2–3 list reloads of the old modal version. I should have caught the clipping; T-ANIMAL-007 S1 / S2 couldn't really be used in that state, so I've logged it as **F-17 (Major)** for the record. It was fixed at 18:40, before this round, by the portalled `DropdownMenu` (`DropdownMenu.tsx:189-193`, `DropdownMenu.module.css:6-8`). Both overflow rules are still in `EntityGrid.module.css`, but they no longer affect the menu. The live check this round confirms the fix (shots 08–10, 15, 21). From this round I'm running the live check rather than relying on the code alone for visual and interaction scenarios.

| Finding | Severity | Status | Evidence |
|---------|----------|--------|----------|
| F-13 GET bare `NotFound()` | Nit | Still open | `AnimalController.cs:28` unchanged; live: generic not-found text (shot 20) |
| F-14 Switch final newline | Nit | Still open | `Switch.tsx:43`, `Switch.module.css:49` unchanged |
| F-15 API final newlines | Nit | Still open | API unchanged since round 2 |
| F-16 Delete confirm `level` | Nit | Resolved (no longer applies) | The confirm now opens directly over the page, so the default `level` primary is what `nextjs-list-pages.mdc` and `nextjs-modal-routing.mdc` ask for (`ManageAnimals.tsx:41-53`) |
| F-17 Row actions menu clipped (missed in round 2) | Major | Resolved before this round | Portalled `DropdownMenu` (18:40); fully visible live in light and dark, flips above (shots 08–10, 15, 21) |

- Resolved: F-16, F-17
- Still open: F-13, F-14, F-15 (all Nit)
- New: F-18 (Minor), F-19 (Nit), F-20 (Minor), F-21 (Minor), F-22 (Minor), F-23 (Nit), F-24 (Nit), F-25 (Nit)
- Regressions: none found. The reference-data grids keep their text buttons, its forms and items modal still open, and `useModalPreload` there is additive. The old `AnimalsLanding`, `ManageAnimalsModal` and `@modal/(.)manage` files are gone, with nothing left importing them.

## Out of scope / pre-existing notes

These do not affect the verdict.

- **List-pages rule and reference data:** `ManageReferenceDataItemsModal` still shows a list in a modal. The rule itself says it "predates this rule", and it isn't part of this plan, so it's a candidate for a separate ticket, not a finding here.
- **Checklist:** `checklists/ui-nextjs-checklist.md` doesn't cite `nextjs-list-pages.mdc` yet. I cited the rule directly and didn't edit the checklist (as instructed).
- **Paginator icons:** the Previous / Next page icons are `#95999d` on white (2.87:1) in light and 4.03:1 in dark. They were disabled in my runs (one page), and `EntityGridPaginator` isn't in this plan. Worth a look alongside F-21.
- **Dev-only seeded password:** `DefaultUserSeeder.cs` has the Development default user's email and password as constants in source (seeded only when `IsDevelopment()`, `Program.cs:104-107`). This predates the plan; consider moving it to user secrets.
- **Line endings:** the feature and route files written at 18:30 are LF while most of the repo is CRLF. No rule covers EOL, so this is a note only (F-23 covers the mixed endings within single files).
- **Hand-off edits during review:** Plan Bot updated `handoff.md` at 18:56 (decision 28, History row 23) and 19:01 (Q37 accepted, History row 24) while it was in review. Both were planning content only, so I re-read them and reviewed against them.
- **Carried forward from round 2:** the Standard group's seeded description (`LoginDbContext.cs:158`); `Modal` doesn't restore focus on close and `ConfirmModal` auto-focuses Delete; `deleteById` doesn't encode the id; `DateCompareValidator` uses `DateTime.UtcNow`; Next.js `README.md` / design-system `README.md:17` staleness.
- **No git:** neither repo is under git, so there's no commit to pin and "secret committed" can't be checked.
- **Not assessed:** production build behaviour (the double first load is expected to be single without StrictMode's dev double effect), build / lint / automated tests by the reviewer, and the DST case for Last Amended (T-ANIMAL-003 S5) live.

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: Not applicable — direct hand-off. Logged in `reviews/review-log.md` (round 3).</sub>
