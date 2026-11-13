# Review: DIRECT-manage-animals-d29-1 — Manage Animals (Decision 29, cycle 1)

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (**Decision 29 fresh review cycle, cycle 1**; not round 4 of the earlier cap. Dev Bot's hand-off at 19:20:33, History row 29) |
| Trigger | direct-handoff |
| Review scope | Plan scope (`direct_scope: plan`) — details in **Review scope** |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git (API and UI; `code.api.head_commit` / `code.ui.head_commit` are null) — files read from disk on 08/10/2026 at about 19:22 (last code change 19:19:58; nothing changed afterwards up to 19:36) |
| Linked tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-008, T-ANIMAL-009 (from `handoff.md` `tickets`; scenario IDs frozen as explicit `S<n>` at 19:24, History row 31) |
| Feature(s) | `ai-planning-framework/work/manage-animals/` |
| Specs reviewed | `specs/manage-animals.yaml` (Is Furry / Has Hooves `display_format`: Boolean icon, decision 29; re-saved without BOM at 19:25, History row 32), `specs/add-edit-animal.yaml` (unchanged); journey `journeys/j-animal-manage.md` as context |
| Active API / UI | API.Framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` (incl. the 19:19 `api-framework-testing.mdc`) + shared `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc`; Next.js `AGENTS.md`, `README.md` and `.cursor/rules` (framework/, style/, implementation/), incl. `framework/nextjs-list-pages.mdc` and `style/nextjs-design-system.mdc`; `checklists/ui-nextjs-checklist.md`, `full-stack-checklist.md`, `api-checklist.md`, `security-checklist.md`, `severity.md`; `handoff/README.md` → Testing alongside review (19:23 version) and `ai-framework.config.yaml` → `testing` |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 08/10/2026 19:45 (Europe/London) |
| Review iteration | Decision 29 cycle 1 (`review.cycle` 0 → 1; the round 1–3 reports stay as they are) |

## Verdict

**Tests blocked: no test environment and no test scaffolding yet, so 0 of 75 scenarios could be tested (Test Bot run 1: 0 pass · 0 fail · 75 waiting). Final verdict: Approve with comments — allowed by `testing.blocked_tests_allow_approval: true`, a flagged default that Neil hasn't settled yet; Neil decides at merge.**

| Part | Verdict |
|------|---------|
| Code review (`review.code_verdict`) | **Approve with comments** |
| Test review (`review.test_verdict`) | **blocked-noted** (see **Test review**) |
| Final (`review.verdict`) | **Approve with comments**, with **Tests blocked** |

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 0 | 1 | 5 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`. Counts are open findings only: new F-26 to F-30, plus F-19 (round 3, only partly done). F-13 to F-18 and F-20 to F-25 are resolved; F-25 is superseded by T-ANIMAL-009.

The code verdict isn't labelled "Provisional" any more. The test review has happened: testing is `blocked`, and `testing.blocked_tests_allow_approval: true` is really set (`ai-framework.config.yaml:415`, under "DEFAULTS FLAGGED TO NEIL (not settled)"). So the final verdict is approval with "Tests blocked" recorded, as `handoff/README.md` → Testing alongside review, default (2) says.

## Summary

Hi Dev Bot, thanks for this pass. T-ANIMAL-009 is a clean piece of work. `renderBooleanIconCell` sits next to `renderBooleanSwitchCell`, which is unchanged. It takes the Yes / No / Not set defaults and the options from the ticket. It uses `--system-green` / `--system-red` through `currentColor`, with no hex. The new Material `Check` / `Close` paths match the existing icons, and the Animals grid has swapped both columns over.

I checked it live in light and dark mode with two rows of my own, one all-true and one all-false:
- the tick and the cross render at 16 px;
- each cell is exposed to assistive technology as "Yes" / "No";
- there are 0 switches left in the grid;
- clicking a boolean cell sends no request;
- Tab never stops on one.

All the round 3 fixes check out in code. Where I could see them live, they check out there too:
- Dark mode now passes on every button I measured: secondary 9.6:1, primary and modal "×" 6.49:1, chip "×" 4.63:1, error text 5.75:1. Light mode is unchanged.
- The showcase has a `DropdownMenu` section.
- Sign out fires `unity-auth-cleared` exactly once.
- The BOMs are gone.
- The manifest now lists all the shared files.
- F-13 is fixed in code. It doesn't show live yet only because the running API process started at 17:55, before the 19:19 change.

There's one Minor finding: the accessible name sits on a `span` with no role. `aria-label` on a generic element isn't allowed by ARIA 1.2. Chromium reads it anyway, but other screen readers may not, so `role="img"` would make it robust (F-26). The rest are Nits: mixed line endings, a stale README icon list, an inline style, and a double event dispatch.

One thing for Plan Bot / Neil, not a PR finding: with the tokens the ticket prescribes, the green tick on white is 2.51:1 and the red cross on the dark surface is 2.09:1. Both are below the 3:1 that WCAG asks of meaningful icons (see **Out of scope**).

**Tests blocked:** Test Bot planned all 75 frozen scenarios but couldn't write or run any:
- Api.Framework.Tests, the e2e scaffolding, the reset endpoint and the personas don't exist yet (owner: you, Dev Bot);
- there's no Test environment or test DB (owner: Neil).

The flagged default allows approval, so this goes to Neil with "Tests blocked".

## Review scope

How the scope was built: plan scope. I started from the `implementation` manifest in `handoff.md` (recorded 19:20:33; 91 files: 18 api, 3 migrations, 70 ui; `tests: []`). That's round 3's 82, plus the five F-18 files, plus four more: `DesignSystemShowcase.tsx`, `Button.module.css`, `ModalShell.module.css` and `unity-cookie.service.ts`. Then I searched `ai-code-framework/api/API.Framework` and `ai-code-framework/ui/UI.NextJs.Framework` again for:
- page names, routes (`/examples/animals`, `v1/Animal`, `v1/schemas/animal`) and `animals_write`;
- ticket IDs and derived names;
- `renderBooleanIconCell`, `renderBooleanSwitchCell`, `BooleanIconCellOptions`, `Icon name="Check"` / `"Close"`;
- `--app-primary-action-fg`, `--app-secondary-action-*`, `--app-form-error-text`;
- `unity-auth-cleared`.

I compared every file against the round 3 copy (read at 18:51) to see exactly what changed. 26 files changed: 16 UI, 9 API and one API rule doc. Then I ran the live browser check.

| Repo | File | Class | Reason | Tickets / controls (from the manifest) | Changed since round 3 |
|------|------|-------|--------|------------------------------------------|-----------------------|
| api | `Api.Framework.Data/Models/Animal.cs` | api | manifest (added) | T-ANIMAL-001; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended | yes |
| api | `Api.Framework.Data/LoginDbContext.cs` | api | manifest (modified) | T-ANIMAL-001; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended | — |
| api | `Api.Framework.Data/LoginPermissions.cs` | api | manifest (modified) | T-ANIMAL-001; controls: + Add Animal, Edit Animal, Delete Animal | — |
| api | `Api.Framework.Services/Validation/Schemas/animalSchema.json` | api | manifest (added) | T-ANIMAL-002, T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves | yes |
| api | `Api.Framework.Services/Records/AnimalRecord.cs` | api | manifest (added) | T-ANIMAL-002; controls: Name, Date Born, Attributes, Is Furry, Has Hooves | yes |
| api | `Api.Framework.Services/Records/AnimalJsonSchemaBuilder.cs` | api | manifest (added) | T-ANIMAL-002 | yes |
| api | `Api.Framework.Services/FormSchemaDependenciesRegistrar.cs` | api | manifest (modified) | T-ANIMAL-002 | — |
| api | `Api.Framework.Services/Animals/AnimalContracts.cs` | api | manifest (added) | T-ANIMAL-002; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended | yes |
| api | `Api.Framework.Services/Animals/IAnimalService.cs` | api | manifest (added) | T-ANIMAL-002 | yes |
| api | `Api.Framework.Services/Animals/AnimalService.cs` | api | manifest (added) | T-ANIMAL-002, T-ANIMAL-005; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended, Delete Animal | yes |
| api | `Api.Framework.Services/Animals/AnimalPolicies.cs` | api | manifest (added) | T-ANIMAL-002; controls: + Add Animal, Edit Animal, Delete Animal | — |
| api | `Api.Framework.Services/LoginServiceCollectionExtensions.cs` | api | manifest (modified) | T-ANIMAL-002 | — |
| api | `Api.Framework/Program.cs` | api | manifest (modified) | T-ANIMAL-002 | — |
| api | `Api.Framework/Controllers/V1/Animals/AnimalController.cs` | api | manifest (added) | T-ANIMAL-002, T-ANIMAL-005; controls: + Add Animal, Edit Animal, Delete Animal | yes |
| api | `Api.Framework/Controllers/V1/Schemas/AnimalSchemaController.cs` | api | manifest (added) | T-ANIMAL-002, T-ANIMAL-004 | yes |
| api | `Api.Framework.Services/DataFramework/JsonSchemaValidation/RecordSchemaValidator.cs` | api | manifest (existing) | T-ANIMAL-002; controls: Name, Date Born, Attributes | — |
| api | `Api.Framework.Services/DataFramework/JsonSchemaValidation/CustomValidation/DateCompareValidator.cs` | api | manifest (existing) | T-ANIMAL-002; controls: Date Born | — |
| api | `Api.Framework.Services/Auth/TokenService.cs` | api | manifest (existing) | T-ANIMAL-001, T-ANIMAL-002 | — |
| ui | `src/app/examples/animals/layout.tsx` | ui | manifest (added) | T-ANIMAL-008, T-ANIMAL-003 | — |
| ui | `src/app/examples/animals/page.tsx` | ui | manifest (added) | T-ANIMAL-008, T-ANIMAL-003 | — |
| ui | `src/app/examples/animals/@modal/default.tsx` | ui | manifest (added) | T-ANIMAL-003 | — |
| ui | `src/app/examples/animals/@modal/(.)manage/item/page.tsx` | ui | manifest (added) | T-ANIMAL-004 | — |
| ui | `src/app/examples/animals/@modal/(.)manage/item/[id]/page.tsx` | ui | manifest (added) | T-ANIMAL-004 | — |
| ui | `src/app/examples/animals/manage/page.tsx` | ui | manifest (added) | T-ANIMAL-008, T-ANIMAL-003 | — |
| ui | `src/app/examples/animals/manage/item/page.tsx` | ui | manifest (added) | T-ANIMAL-004 | — |
| ui | `src/app/examples/animals/manage/item/[id]/page.tsx` | ui | manifest (added) | T-ANIMAL-004 | — |
| ui | `src/shell/components/SiteNav.tsx` | ui | manifest (modified) | T-ANIMAL-008, T-ANIMAL-003; controls: Animals | — |
| ui | `src/config/api-routes.ts` | ui | manifest (modified) | T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005 | — |
| ui | `src/features/animals/shared/models/animal.model.ts` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended | — |
| ui | `src/features/animals/shared/utils/animal-routes.ts` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-004 | — |
| ui | `src/features/animals/shared/utils/animal-permissions.ts` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-005; controls: + Add Animal, Edit Animal, Delete Animal | — |
| ui | `src/features/animals/shared/utils/use-animals-access.ts` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-004 | — |
| ui | `src/features/animals/shared/components/AnimalsAccessNotice.tsx` | ui | manifest (added) | T-ANIMAL-008, T-ANIMAL-003 | — |
| ui | `src/features/animals/shared/state/animals-update.service.ts` | ui | manifest (added) | T-ANIMAL-003 | — |
| ui | `src/features/animals/shared/routes/AnimalsModalRoutes.tsx` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-004 | — |
| ui | `src/features/animals/manage-animals/ManageAnimalsPage.tsx` | ui | manifest (added) | T-ANIMAL-008, T-ANIMAL-003 | — |
| ui | `src/features/animals/manage-animals/ManageAnimals.tsx` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-005; controls: Delete Animal | — |
| ui | `src/features/animals/manage-animals/AnimalsGrid.tsx` | ui | manifest (added) | T-ANIMAL-003 | — |
| ui | `src/features/animals/manage-animals/use-animals-grid.tsx` | ui | manifest (added) | T-ANIMAL-003, T-ANIMAL-005, T-ANIMAL-007; controls: + Add Animal, Edit Animal, Delete Animal | — |
| ui | `src/features/animals/manage-animals/columns/animals-grid-columns.tsx` | ui | manifest (modified) | T-ANIMAL-003, T-ANIMAL-009; controls: Name, Is Furry, Has Hooves, Date Born, Attributes, Last Amended | yes |
| ui | `src/features/animals/manage-animals/state/animals-search.data-provider.ts` | ui | manifest (added) | T-ANIMAL-003 | — |
| ui | `src/features/animals/animal-form-modal/AnimalFormModal.tsx` | ui | manifest (added) | T-ANIMAL-004; controls: Save, Cancel | — |
| ui | `src/features/animals/animal-form-modal/state/animal-entity.data-provider.ts` | ui | manifest (added) | T-ANIMAL-004 | — |
| ui | `src/features/animals/animal-form-modal/state/animal-ui-schema.ts` | ui | manifest (added) | T-ANIMAL-004 | — |
| ui | `src/features/animals/animal-form-modal/ui-schemas/animal.ui-schema.json` | ui | manifest (added) | T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves | — |
| ui | `src/framework/auth/permissions.ts` | ui | manifest (added) | T-ANIMAL-007, T-ANIMAL-003 | — |
| ui | `src/framework/auth/normalize-auth-state.ts` | ui | manifest (added) | T-ANIMAL-001, T-ANIMAL-003 | yes |
| ui | `src/framework/auth/providers/authorisation.data-provider.ts` | ui | manifest (modified) | T-ANIMAL-001, T-ANIMAL-003 | yes |
| ui | `src/framework/auth/token-refresh.service.ts` | ui | manifest (modified) | T-ANIMAL-001, T-ANIMAL-003 | yes |
| ui | `src/framework/design-system/forms/switch/Switch.tsx` | ui | manifest (modified) | T-ANIMAL-006; controls: Is Furry, Has Hooves | yes |
| ui | `src/framework/design-system/forms/switch/Switch.module.css` | ui | manifest (modified) | T-ANIMAL-006 | yes |
| ui | `src/framework/design-system/components/icon/Icon.tsx` | ui | manifest (modified) | T-ANIMAL-009, T-ANIMAL-007; controls: Is Furry, Has Hooves, Edit Animal, Delete Animal | yes |
| ui | `src/framework/design-system/index.ts` | ui | manifest (modified) | T-ANIMAL-006 | — |
| ui | `src/framework/json-schema-form/components/renderers/unity-json-form-renderers.tsx` | ui | manifest (modified) | T-ANIMAL-004, T-ANIMAL-006; controls: Name, Date Born, Attributes, Is Furry, Has Hooves | — |
| ui | `src/framework/json-schema-form/components/JsonSchemaForm.tsx` | ui | manifest (modified) | T-ANIMAL-004 | — |
| ui | `src/framework/json-schema-form/components/JsonSchemaForm.module.css` | ui | manifest (modified) | T-ANIMAL-004, T-ANIMAL-006 | — |
| ui | `src/framework/json-schema-form/validation/unity-schema-validation.ts` | ui | manifest (added) | T-ANIMAL-004; controls: Name, Date Born, Attributes | — |
| ui | `src/framework/json-schema-form/hooks/use-json-schema-entity-form.ts` | ui | manifest (modified) | T-ANIMAL-004; controls: Save | — |
| ui | `src/framework/json-schema-form/models/unity-json-schema.model.ts` | ui | manifest (modified) | T-ANIMAL-004 | — |
| ui | `src/framework/json-schema-form/schema/unity-schema-api.mapper.ts` | ui | manifest (modified) | T-ANIMAL-004; controls: Attributes, Date Born | — |
| ui | `src/framework/json-schema-form/schema/unity-schema.adapter.ts` | ui | manifest (modified) | T-ANIMAL-004; controls: Is Furry, Has Hooves, Attributes | — |
| ui | `src/framework/json-schema-form/schema/unity-schema-value.mapper.ts` | ui | manifest (modified) | T-ANIMAL-004; controls: Attributes | — |
| ui | `src/framework/json-schema-form/index.ts` | ui | manifest (modified) | T-ANIMAL-004 | — |
| ui | `src/framework/entity-framework/utils/api-error.utils.ts` | ui | manifest (modified) | T-ANIMAL-004, T-ANIMAL-005 | — |
| ui | `src/framework/entity-framework/providers/abstract-entity.data-provider.ts` | ui | manifest (modified) | T-ANIMAL-004 | — |
| ui | `src/framework/entity-framework/index.ts` | ui | manifest (modified) | T-ANIMAL-009, T-ANIMAL-003; controls: Is Furry, Has Hooves | yes |
| ui | `src/framework/entity-framework/grid/grid-column.ts` | ui | manifest (modified) | T-ANIMAL-007; controls: Edit Animal, Delete Animal | — |
| ui | `src/framework/entity-framework/grid/entity-grid-config.ts` | ui | manifest (modified) | T-ANIMAL-007 | — |
| ui | `src/framework/entity-framework/grid/grid-cell-renderers.tsx` | ui | manifest (modified) | T-ANIMAL-009, T-ANIMAL-003, T-ANIMAL-006; controls: Is Furry, Has Hooves, Date Born, Attributes | yes |
| ui | `src/framework/entity-framework/components/entity-grid/EntityGrid.tsx` | ui | manifest (modified) | T-ANIMAL-007, T-ANIMAL-003; controls: + Add Animal, Actions | — |
| ui | `src/framework/entity-framework/components/entity-grid/EntityGridRowActionsMenu.tsx` | ui | manifest (added) | T-ANIMAL-007; controls: Edit Animal, Delete Animal | — |
| ui | `src/framework/entity-framework/components/entity-grid/EntityGrid.module.css` | ui | manifest (modified) | T-ANIMAL-007 | — |
| ui | `src/framework/design-system/components/modal/Modal.tsx` | ui | manifest (modified) | T-ANIMAL-005, T-ANIMAL-007; controls: Delete Animal | — |
| ui | `src/framework/design-system/components/modal/ConfirmModal.tsx` | ui | manifest (modified) | T-ANIMAL-005; controls: Delete Animal | — |
| ui | `src/framework/design-system/components/modal/RoutedModal.tsx` | ui | manifest (modified) | T-ANIMAL-004 | — |
| ui | `src/framework/design-system/theme/tokens.css` | ui | manifest (modified) | T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-004, T-ANIMAL-009; controls: + Add Animal, Actions, Is Furry, Has Hooves, Attributes | yes |
| ui | `src/framework/entity-framework/components/entity-grid-auth-gate/EntityGridAuthGate.tsx` | ui | manifest (existing) | T-ANIMAL-003 | — |
| ui | `src/framework/auth/context/AuthProvider.tsx` | ui | manifest (existing) | T-ANIMAL-003, T-ANIMAL-007 | — |
| ui | `.cursor/rules/framework/nextjs-list-pages.mdc` | ui | manifest (added) | T-ANIMAL-008, T-ANIMAL-003 | — |
| ui | `src/framework/design-system/components/menu/DropdownMenu.tsx` | ui | manifest (added) | T-ANIMAL-007; controls: Actions, Edit Animal, Delete Animal | — |
| ui | `src/framework/design-system/components/menu/DropdownMenu.module.css` | ui | manifest (added) | T-ANIMAL-007; controls: Actions | — |
| ui | `src/framework/design-system/components/modal/use-modal-navigate.ts` | ui | manifest (modified) | T-ANIMAL-004, T-ANIMAL-008 | — |
| ui | `src/framework/json-schema-form/services/json-schema-data.service.ts` | ui | manifest (modified) | T-ANIMAL-004 | yes |
| ui | `src/framework/api/unity-api-fetch.ts` | ui | manifest (modified) | T-ANIMAL-001, T-ANIMAL-003, T-ANIMAL-008 | yes |
| ui | `src/features/design-system-showcase/DesignSystemShowcase.tsx` | ui | manifest (modified) | T-ANIMAL-007; controls: Actions | yes |
| ui | `src/framework/design-system/buttons/button/Button.module.css` | ui | manifest (modified) | T-ANIMAL-004, T-ANIMAL-007; controls: + Add Animal, Actions | yes |
| ui | `src/framework/design-system/components/modal/ModalShell.module.css` | ui | manifest (modified) | T-ANIMAL-004 | yes |
| ui | `src/framework/auth/storage/unity-cookie.service.ts` | ui | manifest (modified) | T-ANIMAL-001, T-ANIMAL-004 | yes |
| api | `Api.Framework.Data/Migrations/20261008150221_AddAnimals.cs` | migration | manifest (added) | T-ANIMAL-001 | — |
| api | `Api.Framework.Data/Migrations/20261008150221_AddAnimals.Designer.cs` | migration | manifest (added) | T-ANIMAL-001 | — |
| api | `Api.Framework.Data/Migrations/LoginDbContextModelSnapshot.cs` | migration | manifest (modified) | T-ANIMAL-001 | — |
| api | `.cursor/rules/api-framework-testing.mdc` | config (rule doc) | diff (changed 19:19:58, not in manifest) | Not plan code: a framework rule doc. Read for context only (see **Out of scope**) | yes |
| ui | `src/framework/design-system/README.md` | ui (doc) | dependency (read for context) | Icon names list not updated for `Check` / `Close` → F-28 | — |
| ui | `src/framework/auth/context/AuthProvider.tsx`, `src/framework/json-schema-form/services/json-schema-data.service.ts` | ui | consumers of `unity-auth-cleared` (read for F-24 / F-30) | `setSession(null)` and `clearUnityJsonSchemaCache()`; both are safe to run twice | — |
| ui | `src/features/reference-data/**`, other `EntityGrid` callers | ui | consumers of changed shared code (read for regressions) | Nobody else calls `renderBooleanSwitchCell` or `renderBooleanIconCell`; button / modal token changes are global and were checked on the Animals screens | — |
| api | `Api.Framework.Services/Auth/DefaultUserSeeder.cs` | api | dependency (read for the browser check only) | Development default user used to sign in. Values passed by env var only, never printed or stored; the box copy was deleted | — |

- Manifest: 91 files · Discovered (not in manifest): 0 · Diff / dependency: 1 rule doc + 4 context entries
- Changed since round 3 (all at 19:19–19:20):
  - T-ANIMAL-009: `grid-cell-renderers.tsx`, `Icon.tsx`, `entity-framework/index.ts`, `animals-grid-columns.tsx`.
  - F-21 / F-22: `tokens.css`, `Button.module.css`, `ModalShell.module.css`.
  - F-20: `DesignSystemShowcase.tsx`.
  - F-23 / F-24: the four auth / API files, `unity-cookie.service.ts`, `json-schema-data.service.ts`.
  - F-14: `Switch.tsx` / `.module.css`.
  - F-13 / F-15: the nine API files.
- Whole files reviewed: yes (plan scope)
- Not implemented (no file in scope): none
- Deferred: none
- Excluded:
  - Outside `review.scope_include`: planning artefacts (specs, tickets, journey, `handoff.md`) and the feature's `tests/` folder were used as the reference only. The test plan and report are reviewed in **Test review**, not as code.
  - `review.scope_exclude`: `bin/`, `obj/`, `node_modules/`, `.next/`, `appsettings*.json` (not copied to the box), `.env*` (never opened).

## Findings

"Fix by" says who should make the change. None of these block the merge. They're worth doing before it, or in the next pass.

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix | Fix by |
|----|----------|------|-----------|---------|-----------------------|---------------|--------|
| F-26 | Minor | UI standards / accessibility | `ui/UI.NextJs.Framework/src/framework/entity-framework/grid/grid-cell-renderers.tsx:35,43,50` | The accessible name ("Yes" / "No" / "Not set") is an `aria-label` on a plain `<span>` with no role. In ARIA 1.2 a `span` has role `generic`, and naming a generic element is prohibited, so assistive technology is allowed to ignore the label. Live, Chromium does expose it (AX node `generic` named "Yes", and the grid cell is read as `cell "Yes"`). But that's browser-specific: Firefox / Safari with NVDA, JAWS or VoiceOver may announce nothing for the cell. The name is the whole point of S1 / S2 / S5 ("accessible name … not colour-only"). Playwright's `getByRole('img', { name: 'Yes' })` finds 0 elements, so Test Bot's planned e2e asserts will also be fiddlier than they need to be. The ticket's "(e.g. `span`)" allows any non-interactive element, so this is an implementation choice, not a spec issue. | T-ANIMAL-009 S1, S2, S5 and work item 3; `checklists/ui-nextjs-checklist.md` C (accessibility); general practice WAI-ARIA 1.2 §5.2.8.6 "naming prohibited" for `generic`, WCAG 2.1 4.1.2 (capped at Minor) | Add `role="img"` to the three spans (keep `aria-label`; the SVG is already `aria-hidden`). Alternatively, render the label as visually hidden text next to the icon. Either way it stays non-focusable, with no handler | Implementing agent (Dev Bot) |
| F-19 | Nit | Process / manifest | `ai-planning-framework/work/manage-animals/handoff.md` → `implementation.ui` (`src/app/examples/animals/manage/item/page.tsx`, `manage/item/[id]/page.tsx`, `@modal/(.)manage/item/*`) | Partly resolved from round 3. The remap is done: no T-ANIMAL-003/S1, S10 or S11 left, the page files are tagged T-ANIMAL-008, and no `scenarios` entry points at a missing ID. But the full-page form fallbacks and the intercepting form routes are still tagged T-ANIMAL-004 only. T-ANIMAL-008/S4, S5 and S6 aren't referenced by any manifest `scenarios` list. Housekeeping only: I traced all three anyway | Round 3 F-19; `checklists/severity.md` → Nit | When the manifest is next written, add T-ANIMAL-008 (S4 / S5) to those four route files and S6 to `manage/page.tsx` | Implementing agent (Dev Bot) |
| F-27 | Nit | UI / API standards (formatting) | API: `Api.Framework/Controllers/V1/Animals/AnimalController.cs:75`, `Controllers/V1/Schemas/AnimalSchemaController.cs:27`, `Api.Framework.Data/Models/Animal.cs:28`, `Api.Framework.Services/Animals/AnimalContracts.cs`, `AnimalService.cs`, `IAnimalService.cs`, `Records/AnimalJsonSchemaBuilder.cs`, `Records/AnimalRecord.cs`, `Validation/Schemas/animalSchema.json` (last line each). UI: `src/framework/design-system/forms/switch/Switch.tsx`, `Switch.module.css` (last line); `buttons/button/Button.module.css:25-27`; `src/framework/entity-framework/index.ts:32-34`; `src/features/design-system-showcase/DesignSystemShowcase.tsx:249-250` | The round 3 newline / BOM fixes added new mixed line endings. The 11 files that got a final newline are CRLF, but the new last line ends in LF only. The lines edited in `Button.module.css` and `index.ts` are LF inside otherwise-CRLF files. The new showcase section is followed by a double blank line. Same class of issue as round 3's F-23; no effect on behaviour | General practice (consistency; no rule covers EOL, so formatter-level, capped at Nit) | Normalise each touched file to one line ending (CRLF to match the repo, or LF if Neil prefers), and drop the extra blank line. An `.editorconfig` / `.gitattributes` would stop it recurring | Implementing agent (Dev Bot) |
| F-28 | Nit | UI standards (docs) | `ui/UI.NextJs.Framework/src/framework/design-system/README.md:17` | The `Icon` row still lists "Visibility, Edit, Delete". `Check` and `Close` were added to `ICON_PATHS` (`Icon.tsx:7-8`), and `Visibility` isn't in the component | `style/nextjs-design-system.mdc:152` (document in the design-system README) | List the real names: `Edit`, `Delete`, `Check`, `Close` | Implementing agent (Dev Bot) |
| F-29 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/entity-framework/grid/grid-cell-renderers.tsx:35,43` | Colour and layout are inline styles (`style={{ color: 'var(--system-green)', display: 'inline-flex' }}`). They use tokens, which is the important part, but the framework puts component styling in co-located CSS modules. A class would also make the contrast fix in **Out of scope** a one-line token change | `style/nextjs-design-system.mdc:140-141` (co-locate `{Name}.module.css`; colours from tokens); general practice (capped at Nit) | Move to a small `grid-cell-renderers.module.css` with `.booleanTrue` / `.booleanFalse` classes | Implementing agent (Dev Bot) |
| F-30 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/auth/token-refresh.service.ts:32-33,50-51` | `clearAuthState()` now dispatches `unity-auth-cleared` itself (`unity-cookie.service.ts:104-106`, the F-24 fix), but the two token-refresh failure paths still dispatch it again straight afterwards, so it fires twice there. Harmless today: both listeners are idempotent (`AuthProvider.tsx:42-44` `setSession(null)`, `json-schema-data.service.ts:28`). Any future listener with side effects would run twice. A manual Sign out fires it once (verified live) | General practice (single source of the event; capped at Nit) | Remove the two explicit `window.dispatchEvent(new Event('unity-auth-cleared'))` lines in `token-refresh.service.ts` | Implementing agent (Dev Bot) |

### Round 3 findings (F-13 to F-25): status

| ID | Severity (r3) | Status | Evidence |
|----|---------------|--------|----------|
| F-13 | Nit | **Resolved in code; not live-verified** | `AnimalController.cs:28` → `NotFound(Missing("The animal was not found."))`, the same pattern as `DirectoryControllers.cs:48,111`. Live `GET v1/Animal/{id}` for my deleted row still returned ASP.NET ProblemDetails: the API process started at 17:55:38 and the change landed at 19:19, and Dev Bot didn't restart it. I didn't restart anything (out of my remit). Neil: a restart of API.Framework will show it |
| F-14 | Nit | Resolved | `Switch.tsx` / `Switch.module.css` now end with a newline (the new last line is LF in a CRLF file → F-27) |
| F-15 | Nit | Resolved | All nine API files end with a newline (same EOL caveat → F-27) |
| F-16 | Nit | Resolved (round 3) | — |
| F-17 | Major | Resolved (before round 3) | Menu still portalled and 100% visible, light and dark (shots 05, 11) |
| F-18 | Minor | Resolved | All five files are in `implementation.ui`, with tickets and controls, plus `DesignSystemShowcase.tsx`, `Button.module.css`, `ModalShell.module.css` and `unity-cookie.service.ts`. Imports from the changed files found nothing else missing (0 discovered) |
| F-19 | Nit | **Partly resolved → still open** (see above) | Old IDs gone; page files tagged T-ANIMAL-008; T-ANIMAL-008/S4–S6 and the form fallbacks not tagged |
| F-20 | Minor | Resolved | `DesignSystemShowcase.tsx:217-248` "Dropdown menu" section (trigger `secondary-action`, items Edit with icon and Delete). Live: menu portalled, 100% visible, items hit-test (shot 15) |
| F-21 | Minor | Resolved | `tokens.css:21,55-58` adds `--app-primary-action-fg` (white / `var(--ink-100)`) and dark secondary bg / border / fg; used at `Button.module.css:27` and `ModalShell.module.css:17,61`. **Measured live (dark):** Sign out, Actions, Cancel 9.6:1; + Add Animal, Save 6.49:1; modal header "×" 6.49:1; Delete 5.52:1. Light unchanged: + Add Animal 5.66:1, Actions 5.66:1 (shots 06, 12, 14) |
| F-22 | Minor | Resolved | `tokens.css:53` dark `--app-form-error-text: #ff9aa8`. **Measured live (dark):** chip "×" 4.63:1 on `#3d4854`; "Name is required" 5.75:1 on `#2d3a4a`; required " *" now `#ff9aa8` (shots 12, 13) |
| F-23 | Nit | Resolved | The four auth / API files have no BOM and are LF throughout. No BOM anywhere in the changed `src/` files |
| F-24 | Nit | Resolved | `unity-cookie.service.ts:100-107` `clearAuthState()` dispatches `unity-auth-cleared`, and the comment at `json-schema-data.service.ts:18` is now accurate. Live: Sign out fired the event exactly once. Leftover double dispatch on token-refresh failure → F-30 |
| F-25 | Nit | **Superseded by T-ANIMAL-009** | Read-only switches replaced by tick / cross icons (decision 29). Live: 0 switches in the grid |

## Browser verification (live)

Run on 08/10/2026 at about 19:31–19:33 (Europe/London) against the dev servers already running on Neil's PC: UI `http://localhost:3003` (Next.js dev) and API.Framework on 5088 / 7088 (process started 17:55:38). I didn't start or restart anything.
- **Sign-in:** the Development default seeded user. The credentials came from API.Framework's dev seeder and were passed to a child process by environment variable only. They were never printed, logged, screenshotted or written; the run log was scanned afterwards and contains none.
- **Tooling:** headless Chromium via the existing Playwright 1.56.1 in `ui/Unity.UI.Framework/e2e/node_modules`. Scripts ran from a temp folder outside the repos, which has since been deleted.
- **Data:** I only touched my own two rows, both created through the Add form:
  - "ZZ Test Animal 202610081831 T": Is Furry and Has Hooves on, tags "d29, tick".
  - "ZZ Test Animal 202610081831 F": both off, no tags.

  Both were deleted through the UI. `GET v1/Animal/{id}` returned 404 for each (follow-up run), and 0 rows with the stamp remain. Another user's existing row ("triger") was left untouched.
- **Screenshots:** on the box in `/workspace/manage-animals-check/d29/` (`01-…png` to `17-…png`, plus `run-log.txt`). The best four are:
  - `17-icon-cells-zoom-light-vs-dark.png` (both icons, light over dark, zoomed);
  - `03-row-T-light-zoom.png`;
  - `09-row-F-dark-zoom.png`;
  - `12-edit-form-dark.png`.

| Check | Result | Evidence |
|-------|--------|----------|
| **T-009 / T-003 S14: true** | ✓ `<span aria-label="Yes">` containing an SVG with `data-icon="Check"`, `aria-hidden="true"`, `focusable="false"`, 16×16 px (1.6rem); computed colour rgb(114, 180, 83) = `--system-green` | shots 02, 03, 07, 08, 17 |
| **T-009 / T-003 S15: false** | ✓ Same structure with `Close`, rgb(207, 19, 55) = `--system-red`, `aria-label="No"` | shots 04, 09, 10, 17 |
| No switch left in the grid | ✓ 0 `role="switch"` / Switch elements anywhere in the grid (3 Check, 3 Close across the 3 rows) | run log |
| Accessible name | ✓ in Chromium. AX tree: `generic` "Yes" / "No" (not ignored); aria snapshot `cell "Yes"`, `cell "Yes"` for row T. `getByLabel('Yes')` = 3. ✗ `getByRole('img', { name: 'Yes' })` = 0 (no role) → **F-26** | run log |
| Not interactive (T-009 S3) | ✓ 4 clicks (T and F, both columns) → 0 new API requests, 0 dialogs, 0 menus, URL unchanged. Tab ×120 never landed inside a boolean cell; no `tabIndex`, no `onclick` | run log |
| Null → em dash (T-009 S5) | Not live: Animal booleans are non-null, so no page renders one. Traced in code (`grid-cell-renderers.tsx:49-53`) | — |
| **Icon contrast (non-text, WCAG 1.4.11, 3:1)** | Light: tick **2.51:1** (2.40 on row hover) ✗, cross 5.52:1 (5.29) ✓. Dark: tick 4.61:1 (3.71) ✓, cross **2.09:1** (1.69) ✗. Spec-mandated tokens → **Out of scope** note, not a PR finding | shots 03, 04, 08, 09, 10 |
| **F-21 dark buttons** | ✓ Sign out / Actions / Cancel 9.6:1; + Add Animal / Save 6.49:1; modal header "×" 6.49:1; Delete 5.52:1. Light: + Add Animal 5.66, Actions 5.66 | shots 06, 12, 14 |
| **F-22 dark errors** | ✓ chip "×" 4.63:1; "Name is required" 5.75:1; required " *" `#ff9aa8` | shots 12, 13 |
| List-pages rule (T-008 S1) | ✓ `/examples/animals`: H1 "Manage Animals", "+ Add Animal" on the page (not in a dialog), 0 dialogs open | shots 01, 06 |
| Row actions menu not clipped | ✓ Light and dark: portalled to `<body>`, 160×76, visibleRatio 1, both items hit-test as top-most; same on the last row | shots 05, 11 |
| Escape layering | ✓ Menu: Escape closes only the menu, focus back on "Actions". Edit form: Escape closes only the form → `/examples/animals`. Delete confirm (dark): Escape closes only the confirm, row still there | run log |
| Edit loads values (T-004) | ✓ Row T: name, Is Furry on, Has Hooves on; grid visible behind; 1 dialog | shot 12 |
| Delete (T-005) | ✓ "Delete ZZ Test Animal 202610081831 …?" with red Delete; both rows deleted through the UI, one refresh each | shot 14 |
| Deleted-record Edit URL (T-004 S12) | ✓ "This record could not be found. It may have been deleted." over the list. The API body is still ProblemDetails (F-13 needs an API restart) | shot 16 |
| Showcase dropdown (F-20) | ✓ "Dropdown menu" section present; menu portalled, visibleRatio 1, items hit-test | shot 15 |
| Sign out (F-24) | ✓ `unity-auth-cleared` fired exactly once; redirected to `/auth/sign-in` | run log |
| Not re-run this cycle | Simulated no-permission (T-008 S2 / S3), direct form URL (T-008 S5), `/manage` redirect (T-008 S6), duplicate name and the Date Born rules. That code is unchanged since round 3, where all passed live | round 3 report |
| Paginator icons | 2.87:1 light / 4.03:1 dark (unchanged, pre-existing; see **Out of scope**) | run log |

## Spec conformance (per control)

Spec: `specs/add-edit-animal.yaml` — Basic Form — Add \| Edit Animal (unchanged; the form code is unchanged since round 3 apart from global button / modal / error tokens)

| Section / step | Control | Control type | Mandatory | Editable | Enablement | Min / max | Validation message | Status | Notes / finding |
|----------------|---------|--------------|-----------|----------|------------|-----------|--------------------|--------|-----------------|
| Animal Details | Name | Keyed Input → text `Input` (`unity-json-form-renderers.tsx:34-63`) | Yes ✓ server ✓ UI marker ✓ | Yes ✓ | Always ✓ | 1–100 ✓ | "Name is required" ✓ live (dark, 5.75:1); "An animal with this name already exists" ✓ (r3 live) | Match | Trimmed on save ✓ |
| Animal Details | Date Born | Date Picker → native date `Input` | Yes ✓ server ✓ UI marker ✓ | Yes ✓ | Always ✓ | N/A ✓ | "Date Born is required" / "Date Born must be before today" ✓ (r3 live) | Match | |
| Animal Details | Attributes | Tag Input → `UnityTagInputControl` (`unity-json-form-renderers.tsx:282-353`) | No ✓ | Yes ✓ | Always ✓ | 0–50 per tag, max 20 ✓ | limits ✓ (code) | Match | Dark chip "×" 4.63:1 (F-22 resolved) |
| Characteristics | Is Furry | Switch → `UnitySwitchControl` | No ✓ | Yes ✓ | Always ✓ | N/A | none ✓ | Match | Set On and saved ✓ live |
| Characteristics | Has Hooves | Switch → `UnitySwitchControl` | No ✓ | Yes ✓ | Always ✓ | N/A | none ✓ | Match | Set On and saved ✓ live |
| (form) | Save / Cancel | Buttons (`AnimalFormModal.tsx:76-90`) | — | — | Save disabled while loading / saving ✓ | — | Field errors on controls ✓ | Match | Dark contrast 6.49 / 9.6:1 (F-21 resolved) |

Manage list: `specs/manage-animals.yaml` — Paginated Grid — Manage Animals ("Animal catalogue"), route `/examples/animals`

| Column / action | Population source / action on click | Display format / sortable | Status | Notes / finding |
|-----------------|-------------------------------------|---------------------------|--------|-----------------|
| (page) Title / sub-text | "Manage Animals" / "Animal catalogue" (`ManageAnimalsPage.tsx:14-21`) | — | Match | live ✓ (shot 01) |
| Search filters | none (`search_filters: []`) | — | Match | |
| + Add Animal | Add mode (`use-animals-grid.tsx:74-82`) | Primary action / — | Match | live ✓; dark 6.49:1 |
| Name | `Animal.Name` (`animals-grid-columns.tsx:14-19`) | Char / Yes, default ascending ✓ | Match | live ✓ "Name ↑" |
| **Is Furry** | `Animal.IsFurry` (`animals-grid-columns.tsx:20-26`) | **Boolean icon** (green tick / red cross, Yes / No) via `renderBooleanIconCell` ✓ / Yes ✓ | Match | live ✓; F-26 (name on a role-less span); contrast → Out of scope |
| **Has Hooves** | `Animal.HasHooves` (`animals-grid-columns.tsx:27-33`) | **Boolean icon** ✓ / Yes ✓ | Match | live ✓; as above |
| Date Born | `Animal.DateBorn` (`animals-grid-columns.tsx:34-39`) | DD/MM/YYYY ✓ / Yes ✓ | Match | live ✓ "20/05/2019" |
| Attributes | `Animal.Attributes` (`animals-grid-columns.tsx:40-45`) | Comma-separated ✓ / No ✓ | Match | live ✓ "d29, tick" |
| Last Amended | `Animal.UpdatedUtc` & `UpdatedBy` → display name (`animals-grid-columns.tsx:46-56`) | "DD/MM/YYYY HH:MM Display name", local ✓ / Yes ✓ | Match | live ✓ "08/10/2026 19:31 System Administrator" |
| Actions column | Last column, "Actions", not sortable (`EntityGrid.tsx:70-80`) | — / No ✓ | Match | Row click does nothing ✓ |
| Edit Animal / Delete Animal | `DropdownMenu` items (`EntityGridRowActionsMenu.tsx:29-45`; `use-animals-grid.tsx:55-72`) | Menu items | Match | live ✓ light / dark |
| Paging / empty state | Server-side, 20 per page, options 5–200; "No results" with "+ Add Animal" (Q37) | Paginator | Match | unchanged since round 3 |
| No-permission callout | "You do not have permission to manage animals." | Warning `Callout` | Match | unchanged (r3 live, simulated) |

## Data mapping (per control)

No mapping code changed in this cycle. The API files only gained a final newline. `AnimalController.cs:28` changed the 404 body only, and the grid change affects display only. Re-checked against the specs:

| Control | Spec: Service · Table.Column | UI binding | API record / DTO | Mapper | Entity / downstream model | Migration | Status |
|---------|------------------------------|------------|------------------|--------|---------------------------|-----------|--------|
| Name | Animals · `Animal.Name` (+ `NormalizedName`) | `#/properties/name` | `AnimalWriteRequest.Name` → `AnimalRecord.Name` | `AnimalService.cs:166-177`, `:78-79`, `:129-130` | `Animal.Name`, `Animal.NormalizedName` | `20261008150221_AddAnimals.cs` | Mapped |
| Date Born | Animals · `Animal.DateBorn` | `#/properties/dateBorn` | `AnimalWriteRequest.DateBorn` | `AnimalService.cs:80,131`; UI `unity-schema-value.mapper.ts:90-94` | `Animal.DateBorn` (`DateOnly`) | `date_born` date | Mapped |
| Attributes | Animals · `Animal.Attributes` | `#/properties/attributes` | `AnimalWriteRequest.Attributes` (`[]` when missing) | `AnimalService.cs:175,276-277`; UI `unity-schema-value.mapper.ts:22-28` | `Animal.Attributes` (jsonb, default `'[]'`) | `attributes` jsonb | Mapped |
| Is Furry | Animals · `Animal.IsFurry` | form `#/properties/isFurry`; grid `item.isFurry` → `renderBooleanIconCell` | `AnimalWriteRequest.IsFurry` / `AnimalModel.IsFurry` | `AnimalService.cs:82,133` | `Animal.IsFurry` | `is_furry` boolean default false | Mapped |
| Has Hooves | Animals · `Animal.HasHooves` | form `#/properties/hasHooves`; grid `item.hasHooves` → `renderBooleanIconCell` | `AnimalWriteRequest.HasHooves` / `AnimalModel.HasHooves` | `AnimalService.cs:83,134` | `Animal.HasHooves` | `has_hooves` boolean default false | Mapped |
| Last Amended (list) | Animals · `Animal.UpdatedUtc` & `UpdatedBy` → `User.DisplayName` / `Email` | grid `updatedUtc`, `updatedByName` | `AnimalModel.UpdatedUtc`, `UpdatedByName` | `AnimalService.cs:205-229` | `Animal.UpdatedUtc`, `Animal.UpdatedBy` → `User` | `updated_utc`, `updated_by` + FK | Mapped |
| (soft delete) | Animals · `Animal.IsDeleted` | — | — | `AnimalService.cs:160-162` | `Animal.IsDeleted` | `is_deleted`, filtered unique index | Mapped |

Columns or properties in the reviewed code that are not in any linked spec:

- none

## Acceptance criteria coverage (per scenario)

All **75** frozen scenarios (explicit `S<n>` IDs, History row 31):
- T-ANIMAL-001/S1–S7, T-ANIMAL-002/S1–S13, T-ANIMAL-003/S2–S9 and S12–S15, T-ANIMAL-004/S1–S12, T-ANIMAL-005/S1–S5;
- T-ANIMAL-006/S1–S5 (S5 is now "String-array grid cells");
- T-ANIMAL-007/S1–S9, T-ANIMAL-008/S1–S6, T-ANIMAL-009/S1–S6.

The T-ANIMAL-003 gaps (no S1, S10, S11) are deliberate: those scenarios moved to T-ANIMAL-008/S1–S3 and their numbers are never reused.

No scenario has a real test yet (see **Test review**), so none can be **Covered**. Scenarios whose code I traced and found correct are **Partial**, marked "code ✓". "**d29** live ✓" means exercised in this cycle's browser check (shot numbers refer to `/workspace/manage-animals-check/d29/`). "live ✓ (r3)" means exercised in round 3 on unchanged code (`/workspace/manage-animals-check/round3/`). The test reference is Test Bot's planned tag from `tests/test-plan.md`; all are Waiting in `tests/TEST-manage-animals-1-report.md`.

| Scenario ID | Scenario | Status | Code reference(s) | Test reference(s) (TEST-manage-animals-1) | Notes |
|-------------|----------|--------|-------------------|-------------------------------------------|-------|
| T-ANIMAL-001/S1 | Animal table stores all mapped columns | Partial | `Animal.cs:3-28`; `LoginDbContext.cs:455-477`; `20261008150221_AddAnimals.cs:19-46` | `[Trait("Scenario", "T-ANIMAL-001/S1")]` planned, not written — Waiting | code ✓ (snake_case columns, `creatures.animals`) (unchanged since round 3) |
| T-ANIMAL-001/S2 | Attributes default to an empty array | Partial | `LoginDbContext.cs:462`; `Animal.cs:13` | `[Trait("Scenario", "T-ANIMAL-001/S2")]` + `@T-ANIMAL-001/S2` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-001/S3 | Normalised name is unique among non-deleted rows | Partial | `LoginDbContext.cs:467-470`; `20261008150221_AddAnimals.cs:64-70` | `[Trait("Scenario", "T-ANIMAL-001/S3")]` + `@T-ANIMAL-001/S3` planned, not written — Waiting | code ✓ (filtered unique index `NOT is_deleted`) (unchanged since round 3) |
| T-ANIMAL-001/S4 | A soft-deleted animal's name can be reused | Partial | `LoginDbContext.cs:467-470` | `@T-ANIMAL-001/S4` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-001/S5 | Soft-deleted flag exists | Partial | `Animal.cs:19`; `LoginDbContext.cs:465` | `[Trait("Scenario", "T-ANIMAL-001/S5")]` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-001/S6 | Table lives in the creatures schema | Partial | `LoginDbContext.cs:12,457`; `20261008150221_AddAnimals.cs:16-20`; `AnimalService.cs:15` | `[Trait("Scenario", "T-ANIMAL-001/S6")]` planned, not written — Waiting | code ✓; comment now says `creatures.animals` (F-07 resolved) (unchanged since round 3) |
| T-ANIMAL-001/S7 | The animals permission is seeded for our users | Partial | `LoginPermissions.cs:36`; `LoginDbContext.cs:482-503`; `20261008150221_AddAnimals.cs:48-62` | `[Trait("Scenario", "T-ANIMAL-001/S7")]` planned, not written — Waiting | code ✓ (Administrators and Standard groups) (unchanged since round 3) |
| T-ANIMAL-002/S1 | Create animal with valid fields | Partial | `AnimalService.cs:56-100`; `AnimalController.cs:31-42` | `[Trait("Scenario", "T-ANIMAL-002/S1")]` + `@T-ANIMAL-002/S1` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** both test rows created through the Add form → `POST v1/Animal` 200 |
| T-ANIMAL-002/S2 | Missing Attributes are stored as an empty array | Partial | `AnimalService.cs:170-177,276-277` | `[Trait("Scenario", "T-ANIMAL-002/S2")]` + `@T-ANIMAL-002/S2` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-002/S3 | Duplicate name is rejected | Partial | `AnimalService.cs:69-71,92-97` | `[Trait("Scenario", "T-ANIMAL-002/S3")]` + `@T-ANIMAL-002/S3` planned, not written — Waiting | code ✓ (409 + exact message, also on a unique-index race) (unchanged since round 3) |
| T-ANIMAL-002/S4 | Name of a soft-deleted animal can be reused | Partial | `AnimalService.cs:69` | `[Trait("Scenario", "T-ANIMAL-002/S4")]` + `@T-ANIMAL-002/S4` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-002/S5 | Date Born must be before today | Partial | `animalSchema.json:26-36`; `DateCompareValidator.cs` | `[Trait("Scenario", "T-ANIMAL-002/S5")]` + `@T-ANIMAL-002/S5` planned, not written — Waiting | code ✓ (UTC date) (unchanged since round 3) |
| T-ANIMAL-002/S6 | Date Born is mandatory | Partial | `animalSchema.json:4,25,35` | `[Trait("Scenario", "T-ANIMAL-002/S6")]` + `@T-ANIMAL-002/S6` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-002/S7 | Name is mandatory | Partial | `animalSchema.json:10-17`; `AnimalService.cs:166-177,261-265` | `[Trait("Scenario", "T-ANIMAL-002/S7")]` + `@T-ANIMAL-002/S7` planned, not written — Waiting | code ✓ (whitespace-only name → "Name is required") (unchanged since round 3) |
| T-ANIMAL-002/S8 | Attribute tag limits | Partial | `animalSchema.json:39-53` | `[Trait("Scenario", "T-ANIMAL-002/S8")]` + `@T-ANIMAL-002/S8` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-002/S9 | List returns non-deleted animals with Last Amended | Partial | `AnimalService.cs:28-47,205-229` | `[Trait("Scenario", "T-ANIMAL-002/S9")]` + `@T-ANIMAL-002/S9` planned, not written — Waiting | code ✓ (DisplayName, fallback Email) (unchanged since round 3) |
| T-ANIMAL-002/S10 | Soft delete and not found afterwards | Partial | `AnimalService.cs:49-54,108-111,149-165`; `AnimalController.cs:28` | `[Trait("Scenario", "T-ANIMAL-002/S10")]` + `@T-ANIMAL-002/S10` planned, not written — Waiting | code ✓; GET now returns `NotFound(Missing("The animal was not found."))` (F-13 resolved in code). **d29:** soft delete through the UI, then `GET v1/Animal/{id}` 404 for both rows. The 404 body is still ProblemDetails because the running API process predates the change (see F-13 note) |
| T-ANIMAL-002/S11 | Users without animals_write are rejected on every endpoint | Partial | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` | `@T-ANIMAL-002/S11` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-002/S12 | User-management permissions alone do not grant access to animals | Partial | `Program.cs:86-87`; `AnimalPolicies.cs:8-10` | `@T-ANIMAL-002/S12` planned, not written — Waiting | code ✓ (no `DirectoryPolicies` on animal endpoints) (unchanged since round 3) |
| T-ANIMAL-002/S13 | AnimalsWrite guards every animal endpoint | Partial | `AnimalController.cs:17-58`; `AnimalSchemaController.cs:15` | `[Trait("Scenario", "T-ANIMAL-002/S13")]` + `@T-ANIMAL-002/S13` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-003/S2 | List shows non-deleted animals | Partial | `animals-search.data-provider.ts:13`; `animals-grid-columns.tsx:13-57`; `AnimalService.cs:30` | `@T-ANIMAL-003/S2` planned, not written — Waiting | code ✓, live ✓ (r3) (deleted row gone; r3 shot 19) |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user | Partial | `animals-grid-columns.tsx:46-56`; `grid-cell-renderers.tsx:70-75` | `@T-ANIMAL-003/S3` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** "08/10/2026 19:31 System Administrator" |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | Partial | `grid-cell-renderers.tsx:70-75` | `@T-ANIMAL-003/S4` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** 19:31 BST shown for a save at 18:31 UTC |
| T-ANIMAL-003/S5 | Last Amended outside summer time | Partial | `grid-cell-renderers.tsx:70-75` | `@T-ANIMAL-003/S5` planned, not written — Waiting | code ✓ (uses the browser's own offset; not testable live in October) |
| T-ANIMAL-003/S6 | Default sort by Name ascending | Partial | `use-animals-grid.tsx:27,49`; `AnimalService.cs:234-250` | `@T-ANIMAL-003/S6` planned, not written — Waiting | code ✓, live ✓ (r3) ("Name ↑") |
| T-ANIMAL-003/S7 | Add opens Basic Form | Partial | `use-animals-grid.tsx:74-82`; `app/examples/animals/@modal/(.)manage/item/page.tsx` | `@T-ANIMAL-003/S7` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** Add form used to create both test rows |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | Partial | `use-animals-grid.tsx:55-61`; `use-json-schema-entity-form.ts:182-198` | `@T-ANIMAL-003/S8` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** Edit on row T loaded name, Is Furry on, Has Hooves on (shot 12) |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | Partial | `EntityGrid.tsx:44-53,70-80,146-153`; `EntityGridRowActionsMenu.tsx:27-45`; `use-animals-grid.tsx:52-73` | `@T-ANIMAL-003/S9` planned, not written — Waiting | code ✓; **d29 live ✓:** menu portalled, 100% visible, both items hit-test, light and dark (shots 05, 11); row click does nothing |
| T-ANIMAL-003/S12 | Results are paged on the server | Partial | `use-animals-grid.tsx:24-29,50`; `EntityGrid.tsx:184-195`; `EntityGridPaginator.tsx:40,84,94`; `entity-grid-config.ts:6`; `AnimalService.cs:28-47` | `@T-ANIMAL-003/S12` planned, not written — Waiting | code ✓ (20 per page, options 5–200, next page re-queries `v1/Animal` with `pageIndex`). Live: page size 20 shown; more than 20 rows not exercised (unchanged since round 3) |
| T-ANIMAL-003/S13 | No animals to show | Partial | `EntityGrid.tsx:93-112,121-122` | `@T-ANIMAL-003/S13` planned, not written — Waiting | code ✓ ("No results"; the toolbar keeps "+ Add Animal"). Not exercised live: the DB has another user's row, which I didn't touch |
| T-ANIMAL-003/S14 | True shows a green tick with accessible name Yes | Partial | `animals-grid-columns.tsx:20-26`; `grid-cell-renderers.tsx:23-39`; `Icon.tsx:7` | `@T-ANIMAL-003/S14` planned, not written — Waiting | code ✓; **d29 live ✓:** Check icon, `color: var(--system-green)` (rgb 114,180,83), cell exposed as "Yes", 0 switches in the grid (shots 03, 08, 17). Name sits on a role-less `span` → **F-26**. Green on white is 2.51:1 → Out of scope note (spec-mandated token) |
| T-ANIMAL-003/S15 | False shows a red cross with No; cells are not interactive | Partial | `animals-grid-columns.tsx:27-33`; `grid-cell-renderers.tsx:41-47` | `@T-ANIMAL-003/S15` planned, not written — Waiting | code ✓; **d29 live ✓:** Close icon, `var(--system-red)`, cell exposed as "No" (shots 04, 09, 10). 4 clicks on boolean cells → 0 API requests, no dialog / menu, URL unchanged; Tab ×120 never lands in a boolean cell. Red on the dark surface is 2.09:1 → Out of scope note |
| T-ANIMAL-004/S1 | Add mode opens with defaults | Partial | `unity-schema.adapter.ts:125-136`; `animalSchema.json:59,65`; `unity-json-form-renderers.tsx:52` | `@T-ANIMAL-004/S1` planned, not written — Waiting | code ✓, live ✓ (r3) (" *" on Name and Date Born only; both switches Off; r3 shot 03) |
| T-ANIMAL-004/S2 | Create animal with required fields | Partial | `use-json-schema-entity-form.ts:219-262`; `unity-schema-value.mapper.ts:15-31`; `AnimalFormModal.tsx:32-35` | `@T-ANIMAL-004/S2` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** both rows saved (trimmed names, tags "d29, tick"); form closed; one list refresh each |
| T-ANIMAL-004/S3 | Name is mandatory | Partial | `unity-schema-validation.ts:214-223`; `animalSchema.json:14-17`; `unity-json-form-renderers.tsx:52` | `@T-ANIMAL-004/S3` planned, not written — Waiting | code ✓; live ✓ (r3); **d29 dark:** "Name is required" in `#ff9aa8`, 5.75:1 (shot 13) |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | Partial | `api-error.utils.ts:26-60`; `use-json-schema-entity-form.ts:253-257` | `@T-ANIMAL-004/S4` planned, not written — Waiting | code ✓, live ✓ (r3) (lower-case padded duplicate → "An animal with this name already exists" on Name, form stays open; r3 shot 13) |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | Partial | `AnimalService.cs:69` | `@T-ANIMAL-004/S5` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-004/S6 | Date Born must be before today | Partial | `unity-schema-validation.ts:100-163` | `@T-ANIMAL-004/S6` planned, not written — Waiting | code ✓, live ✓ (r3) (today → "Date Born must be before today"; r3 shot 05) |
| T-ANIMAL-004/S7 | Date Born is mandatory | Partial | `unity-schema-validation.ts:214-223`; `unity-json-form-renderers.tsx:52` | `@T-ANIMAL-004/S7` planned, not written — Waiting | code ✓, live ✓ (r3) ("Date Born is required"; r3 shot 04) |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | Partial | `unity-schema-value.mapper.ts:22-28`; `AnimalService.cs:276-277` | `@T-ANIMAL-004/S8` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** "d29, tick" shown in the grid and reloaded in Edit |
| T-ANIMAL-004/S9 | Attribute tag limits | Partial | `unity-schema-validation.ts:225-232`; `unity-json-form-renderers.tsx:348-350` | `@T-ANIMAL-004/S9` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-004/S10 | Edit persists changed fields | Partial | `use-json-schema-entity-form.ts:243-247`; `AnimalService.cs:102-146` | `@T-ANIMAL-004/S10` planned, not written — Waiting | code ✓, live ✓ (r3) (name and Has Hooves change saved; r3 shot 12) |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | Partial | `animal-routes.ts:6`; `AnimalFormModal.tsx:53` | `@T-ANIMAL-004/S11` planned, not written — Waiting | code ✓ (no View) (unchanged since round 3) |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | Partial | `AnimalService.cs:49-54`; `AnimalController.cs:28`; `use-json-schema-entity-form.ts:199-210`; `AnimalFormModal.tsx:93-94` | `@T-ANIMAL-004/S12` planned, not written — Waiting | code ✓; **d29 live ✓:** deleted row F's Edit URL shows "This record could not be found. It may have been deleted." over the list (shot 16). API message "The animal was not found." in code (F-13); not visible live until the API is restarted |
| T-ANIMAL-005/S1 | Confirmation names the animal | Partial | `ManageAnimals.tsx:41-53` | `@T-ANIMAL-005/S1` planned, not written — Waiting | code ✓; **d29 live ✓:** "Delete ZZ Test Animal 202610081831 …?" with red Delete (5.52:1) in dark (shot 14) |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | Partial | `use-animals-grid.tsx:90-106`; `AnimalService.cs:149-165` | `@T-ANIMAL-005/S2` planned, not written — Waiting | code ✓; **d29 live ✓:** both rows deleted through the UI, one list refresh each, 0 matching rows afterwards |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | Partial | `ManageAnimals.tsx:50`; `use-animals-grid.tsx:118-120`; `Modal.tsx:76-88` | `@T-ANIMAL-005/S3` planned, not written — Waiting | code ✓; **d29 live ✓:** Escape on the dark confirm closes only the confirm; the row stays |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | Partial | `AnimalService.cs:30,51,69,108,154` | `@T-ANIMAL-005/S4` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | Partial | `AnimalController.cs:57-58`; `use-animals-grid.tsx:67` | `@T-ANIMAL-005/S5` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Partial | `unity-json-form-renderers.tsx:259-280`; `Switch.tsx:12-37` | `@T-ANIMAL-006/S1` planned, not written — Waiting | code ✓; live ✓ (r3); **d29:** both form switches set On for row T and saved |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Partial | `unity-json-form-renderers.tsx:282-353` | `@T-ANIMAL-006/S2` planned, not written — Waiting | code ✓; live ✓ (r3); **d29 dark:** chip "×" now `#ff9aa8`, 4.63:1 (F-22 resolved) |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Partial | `unity-json-form-renderers.tsx:348-350`; `unity-schema-validation.ts:225-232` | `@T-ANIMAL-006/S3` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Partial | `unity-json-form-renderers.tsx:263,273,287,317,330`; `Switch.tsx:36-37` | `@T-ANIMAL-006/S4` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-006/S5 | String-array grid cells | Partial | `grid-cell-renderers.tsx:56-59`; `animals-grid-columns.tsx:40-45` | `@T-ANIMAL-006/S5` planned, not written — Waiting | code ✓ (rescoped by decision 29: string-array cells only); **d29 live ✓:** "d29, tick"; empty array → empty cell (row F) |
| T-ANIMAL-007/S1 | Row actions menu in the last column | Partial | `EntityGrid.tsx:70-80,146-153` | `@T-ANIMAL-007/S1` planned, not written — Waiting | code ✓; **d29 live ✓** (shots 05, 11) |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | Partial | `EntityGridRowActionsMenu.tsx:33-39`; `DropdownMenu.tsx:200-210` | `@T-ANIMAL-007/S2` planned, not written — Waiting | code ✓; **d29 live ✓:** Edit and Delete hit-test and open for the right row |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Partial | `EntityGrid.tsx:44-51`; `permissions.ts:6-13` | `@T-ANIMAL-007/S3` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Partial | `permissions.ts:10-12` | `@T-ANIMAL-007/S4` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Partial | `EntityGrid.tsx:70-80` | `@T-ANIMAL-007/S5` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-007/S6 | Per-row visibility | Partial | `EntityGrid.tsx:52-53` | `@T-ANIMAL-007/S6` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Partial | `EntityGridRowActionsMenu.tsx:27` | `@T-ANIMAL-007/S7` planned, not written — Waiting | code ✓ (unchanged since round 3) |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | Partial | `EntityGrid.tsx:155-171` | `@T-ANIMAL-007/S8` planned, not written — Waiting | code ✓, live ✓ (r3) (reference data; r3 shot 23) |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | Partial | `DropdownMenu.tsx:111-136` | `@T-ANIMAL-007/S9` planned, not written — Waiting | code ✓; **d29 live ✓:** Escape closes only the menu, focus back on "Actions", 0 dialogs |
| T-ANIMAL-008/S1 | Open Manage Animals from the nav (decisions 24, 27) | Partial | `SiteNav.tsx:32-37`; `app/examples/animals/page.tsx`; `ManageAnimalsPage.tsx:12-27` | `@T-ANIMAL-008/S1` planned, not written — Waiting | code ✓; **d29 live ✓:** H1 "Manage Animals", "+ Add Animal" on the page, 0 dialogs (shots 01, 06) |
| T-ANIMAL-008/S2 | User without animals_write cannot open Manage Animals | Partial | `ManageAnimals.tsx:16-21`; `AnimalsModalRoutes.tsx:16-20`; `AnimalsAccessNotice.tsx`; `SiteNav.tsx:32` | `@T-ANIMAL-008/S2` planned, not written — Waiting | code ✓, live ✓ (r3) (simulated; 0 `v1/Animal` calls; r3 shots 25, 26) |
| T-ANIMAL-008/S3 | User-management permissions alone do not give access to animals | Partial | `animal-permissions.ts:6-8`; `use-animals-access.ts:13`; `Program.cs:86-87` | `@T-ANIMAL-008/S3` planned, not written — Waiting | code ✓ (only `animals_write` is checked, UI and API); live as S2 |
| T-ANIMAL-008/S4 | Add | Edit Animal opens as a modal over the page and closes back to it (decision 27) | Partial | `AnimalFormModal.tsx:22,67-71`; `animal-routes.ts:2`; `@modal/(.)manage/item/page.tsx` | UI e2e planned, not written — Waiting | code ✓; **d29 live ✓:** Escape on the Edit form → `/examples/animals`, 0 dialogs |
| T-ANIMAL-008/S5 | Opening a form URL directly shows the page with the form on top (decision 27) | Partial | `manage/item/page.tsx:4-10`; `manage/item/[id]/page.tsx` | `@T-ANIMAL-008/S5` planned, not written — Waiting | code ✓, live ✓ (r3) (r3 shot 22) |
| T-ANIMAL-008/S6 | The old /manage URL redirects to the page (decision 27) | Partial | `manage/page.tsx:6-8` | `@T-ANIMAL-008/S6` planned, not written — Waiting | code ✓, live ✓ (r3) |
| T-ANIMAL-009/S1 | True shows a green tick named Yes | Partial | `grid-cell-renderers.tsx:23-39`; `Icon.tsx:7`; `entity-framework/index.ts:33-34` | `@T-ANIMAL-009/S1` planned, not written — Waiting | code ✓; **d29 live ✓** via Manage Animals (as T-ANIMAL-003/S14). Accessible name on a role-less `span` → **F-26**; contrast → Out of scope note |
| T-ANIMAL-009/S2 | False shows a red cross named No | Partial | `grid-cell-renderers.tsx:41-47`; `Icon.tsx:8` | `@T-ANIMAL-009/S2` planned, not written — Waiting | code ✓; **d29 live ✓** via Manage Animals (as T-ANIMAL-003/S15). F-26 applies too |
| T-ANIMAL-009/S3 | Cell is not interactive | Partial | `grid-cell-renderers.tsx:33-53` (no handler, no `tabIndex`, no role); `Icon.tsx` (`aria-hidden`, `focusable="false"`) | `@T-ANIMAL-009/S3` planned, not written — Waiting | code ✓; **d29 live ✓:** 0 requests on click, never focused by Tab, not a button / link / switch |
| T-ANIMAL-009/S4 | Labels are configurable with Yes/No defaults | Partial | `grid-cell-renderers.tsx:11-17,27-29` | `@T-ANIMAL-009/S4` planned, not written — Waiting | code ✓ (defaults Yes / No / Not set; options override each). Custom labels not exercised: no page uses them |
| T-ANIMAL-009/S5 | Null / undefined shows em dash named Not set | Partial | `grid-cell-renderers.tsx:49-53` | `@T-ANIMAL-009/S5` planned, not written — Waiting | code ✓ (em dash, `aria-label` "Not set", no colour). Not live: no page renders a null boolean (Animal booleans are non-null) |
| T-ANIMAL-009/S6 | Existing switch cell still available | Partial | `grid-cell-renderers.tsx:6-9`; `entity-framework/index.ts` | `@T-ANIMAL-009/S6` planned, not written — Waiting | code ✓ (`renderBooleanSwitchCell` unchanged and still exported); **d29 live ✓:** 0 switches in the Manage Animals grid |

## Security and data

| Spec rule / check | Status | Reference |
|-------------------|--------|-----------|
| Every animal endpoint requires `animals_write` | Enforced server-side (unchanged) | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` |
| User-management permissions alone give no access | Enforced server-side (unchanged) | `Program.cs:86-87`; UI `animal-permissions.ts:6-8` |
| GET of a missing / deleted animal | 404 with `MessageResponse` "The animal was not found." (F-13); no record data leaked | `AnimalController.cs:28,73-74` |
| Boolean icon cell | Display only: no handler, not focusable, no data beyond the row's own boolean | `grid-cell-renderers.tsx:23-54` |
| Auth events | `clearAuthState()` now dispatches `unity-auth-cleared`, so the schema cache is cleared on manual Sign out too; no token values logged | `unity-cookie.service.ts:100-107`; `json-schema-data.service.ts:18,28` |
| Injection | No raw SQL; LINQ only (unchanged) | `AnimalService.cs` |
| Secrets / tokens | None in the reviewed code. `.env*` not opened. "Committed" can't be checked without git. Browser check: credentials only via env vars in a child process; no cookie or token values read | — |
| PII / tenancy | Unchanged since round 3 (last amender's display name to `animals_write` users; animals global by design) | `AnimalService.cs:228`; spec notes |

## Tests

### Test review

**Tests blocked.** `review.test_verdict: blocked-noted`. Test Bot's run 1 (picked up 19:24, finished 19:27:45 BST; `testing.status: blocked`, `round: 1`, `test_fix_cycle: 0`). Sources:
- `tests/TEST-manage-animals-1-report.md`: 0 Pass · 0 Fail · 0 Blocked · **75 Waiting** · 0 Not automated;
- `tests/test-plan.md`;
- `tests/test-log.md`: "1 | 2026-10-08 19:27 | 0/0/75 | test-fix 0/5";
- the `testing` section of `handoff.md`.

What I checked:

| Check | Result |
|-------|--------|
| Every frozen scenario ID has a status | ✓ All 75 IDs appear exactly once in the report's results table, in the plan's scenario tables and in `testing.results`, each with status Waiting. None are missing and none are extra (T-ANIMAL-001/S1–S7, 002/S1–S13, 003/S2–S9 + S12–S15, 004/S1–S12, 005/S1–S5, 006/S1–S5, 007/S1–S9, 008/S1–S6, 009/S1–S6). Tags use the explicit IDs (`[Trait("Scenario", "T-…/S<n>")]` / `@T-…/S<n>`) |
| Every scenario has a real test | ✗ none written. That's expected while scaffolding and environment are missing. It's not a test defect: the testing agent can't write tests without them |
| Test code (tagging, no front-end mocks, reset-first, Given / When / Then asserts) | Nothing to review: no test code exists yet. The plan gives each e2e scenario a reset key as its first step and a persona, which is the right shape |
| Build | Test Bot ran `dotnet build Api.Framework.sln --configuration Release` at 19:24: succeeded, 0 warnings, 0 errors |
| Counts as a test-fix round? | No. A `blocked` run is never a round (`handoff/README.md` → Testing alongside review, point 9), so `test_fix_cycle` stays 0, and test-fix rounds never touch `review.cycle` (`failures_count_toward_review_cycles: false`) |

Why it's blocked, and who unblocks it:

| Blocker | Scenarios affected | Owner |
|---------|--------------------|-------|
| `Api.Framework.Tests` project doesn't exist (not on disk, not in `Api.Framework.sln`) | All unit layers (17 scenarios) | **code** (implementing agent, Dev Bot) |
| Next.js e2e scaffolding missing: no `UI.NextJs.Framework/e2e`, no Playwright / playwright-bdd, no `playwright.config.*` | All API / UI e2e layers (60 scenarios) | **code** (Dev Bot) |
| Test-data reset endpoint (`v1/TestData/Reset/master`, `/{scenarioKey}`) and batch keys (`animals.page/grid/form/delete/api.*`, `reference-data.types-grid.baseline`) missing | All e2e | **code** (Dev Bot) |
| Personas `testdata-admin`, `animals-tester`, `animals-tester-emailonly`, `animals-viewer`, `animals-usermanager`, `reference-data-tester` not defined | All e2e | **code** (Dev Bot) |
| No component test runner / harness page | T-ANIMAL-006/S1, S2, S4; T-ANIMAL-007/S3–S7; T-ANIMAL-009/S4–S6 (11) | **code** (Dev Bot); Neil to decide if wanted |
| No Test environment (API.Framework `Test` + Test UI), no dedicated PostgreSQL DB `<api_framework_test>`, `E2E_TEST_DATA_KEY` / persona passwords not set, `testing` placeholders unresolved (`database.name`, `ui_base_url`, `api_base_url`, `personas.email_domain`, `personas.tenant`) | All e2e | **human** (Neil) |

**Approval rule.** I read `ai-framework.config.yaml` myself: `testing.blocked_tests_allow_approval: true` (line 415, listed under "DEFAULTS FLAGGED TO NEIL (not settled)"), with `final_approval_requires: [code_review, test_review]`. The code review is Approve with comments and the test review is blocked-noted, so the final verdict is **Approve with comments with "Tests blocked"**. Neil decides at merge. If he'd rather not approve with tests blocked, the feature should go back to `in-review` and wait for the scaffolding and the environment.

Advice for Test Bot, when the scaffolding lands (not findings):
- For T-ANIMAL-003/S14–S15 and T-ANIMAL-009/S1–S2, assert the accessible name with `getByRole('img', { name: 'Yes' })` once F-26 adds `role="img"`. Until then only `getByLabel` works.
- Assert the icon via `data-icon="Check"` / `"Close"` and the colour via the computed `color` matching the token.
- For S3, assert "no request and no focus", as I did live.
- The plan's two flags for Plan Bot (T-ANIMAL-002/S9 and T-ANIMAL-003/S3 name a real person) are sensible; I've left them with Plan Bot.

### Tests by rule (code review)

| Rule / scenario | Test | Status |
|-----------------|------|--------|
| All 75 scenarios (T-ANIMAL-001 to 009) | planned in `tests/test-plan.md`; none written | Untested (Tests blocked; see above) |

Why there's no test finding in the code review: the scaffolding is the implementing agent's job under `handoff/README.md` → Testing alongside review, point 2. But the test plan that lists it only appeared at 19:27, after Dev Bot's 19:20 hand-off, and Dev Bot's updated `api-framework-testing.mdc` says the project is created "when Neil asks or a feature test plan needs those files". It's tracked as a test blocker owned by code (above), not as a code finding against this hand-off. The round 1–3 suggested tests still stand as input for Test Bot.

Checks run by the reviewer: the live browser check (see **Browser verification**). No build, lint or automated tests were run by the reviewer. Test Bot's Release build at 19:24 passed. The hand-off records no ESLint configuration (pre-existing).

## Changes since last review

Last review: round 3, `reviews/DIRECT-manage-animals-3-review.md` (Approve with comments; Blocker 0 · Major 0 · Minor 4 · Nit 7), which covered the code up to decision 28. This report starts the fresh Decision 29 cycle, and the round 1–3 reports are untouched.

What changed since round 3:
- **New ticket T-ANIMAL-009** (decision 29, approved by Neil at 19:14 alongside the 15:44 approval): `renderBooleanIconCell`, `Icon` `Check` / `Close`, export, and the Animals grid's Is Furry / Has Hooves switched over (T-ANIMAL-003 S14 / S15). T-ANIMAL-006 S5 is rescoped to string-array cells.
- **Round 3 fixes:** F-13, F-14, F-15, F-18, F-20, F-21, F-22, F-23, F-24 resolved; F-25 superseded; F-19 partly resolved (see the status table under **Findings**).
- **Plan / test docs** changed while this review ran (History rows 30–32): test-fix cap decision, scenario IDs frozen, encoding repair. Doc-only; I re-read them and cite the frozen IDs. Test Bot's run 1 landed at 19:27 and is covered in **Test review**.

Summary:
- Resolved: F-13 (in code; live needs an API restart), F-14, F-15, F-18, F-20, F-21, F-22, F-23, F-24
- Superseded: F-25 (by T-ANIMAL-009)
- Still open: F-19 (Nit, partly done)
- New: F-26 (Minor), F-27, F-28, F-29, F-30 (Nit)
- Regressions: none found.
  - The list stays on the page (0 dialogs).
  - The row menu is portalled and fully visible in light and dark.
  - Escape layering holds for the menu, the form and the confirm.
  - Edit, create and delete behave as in round 3.
  - The global button / modal token changes improve dark mode without changing light mode (5.66:1 as before).
  - Nothing else uses `renderBooleanSwitchCell`, and it's unchanged.

## Out of scope / pre-existing notes

These don't affect the verdict.

- **Suspected spec issue, for Plan Bot / Neil: boolean icon contrast.** T-ANIMAL-009 prescribes `var(--system-green)` / `var(--system-red)` and notes they aren't overridden in dark mode. Measured live against WCAG 2.1 1.4.11 (non-text contrast, 3:1):

  | Icon | Light | Light, row hover | Dark | Dark, row hover |
  |------|-------|------------------|------|-----------------|
  | Green tick | **2.51:1** ✗ | **2.40:1** ✗ | 4.61:1 ✓ | 3.71:1 ✓ |
  | Red cross | 5.52:1 ✓ | 5.29:1 ✓ | **2.09:1** ✗ | **1.69:1** ✗ |

  The cell is still understandable without colour: tick vs cross shape, plus the Yes / No name. But the icons themselves are faint. The code does exactly what the ticket says, so this isn't a PR finding.

  Suggested change for Plan Bot: semantic tokens such as `--app-boolean-true-fg` / `--app-boolean-false-fg` that flip in dark mode, for example:
  - light green `#2e7d32`: 5.13:1 on white, 4.91:1 on hover;
  - dark red `#ff9aa8` (the F-22 error red): 5.75:1, and 4.63:1 on hover;
  - the current green and red kept where they already pass.

  This needs a ticket wording change (T-ANIMAL-009 work item 3, S1 / S2 "uses the theme colour var(--system-…)").
- **F-13 needs an API restart.** The new 404 body is in code but not in the running process (started 17:55:38). Restarting API.Framework would let Neil see it; I didn't restart anything.
- **Dev Bot edited a framework rule doc:** `api/API.Framework/.cursor/rules/api-framework-testing.mdc` (19:19:58), now "Scaffolding ownership (Neil-approved 08/10/2026)". It matches `handoff/README.md` → Testing alongside review, point 2. It's not plan code and isn't in the manifest; noted, not reviewed as a finding.
- **`blocked_tests_allow_approval: true` is still an unsettled default** (`ai-framework.config.yaml:415`). This approval relies on it, so Neil may want to confirm or change it.
- **Paginator icons:** Previous / Next are `#95999d`: 2.87:1 on white and 4.03:1 in dark. Pre-existing; `EntityGridPaginator` isn't in this plan (same as round 3).
- **Dev-only seeded password** in `DefaultUserSeeder.cs` (seeded only when `IsDevelopment()`); pre-existing, consider user secrets (as round 3).
- **Carried forward from rounds 2–3:**
  - `ManageReferenceDataItemsModal` lists in a modal (predates the list-pages rule);
  - `checklists/ui-nextjs-checklist.md` doesn't cite `nextjs-list-pages.mdc`;
  - the Standard group's seeded description;
  - `Modal` focus restore / `ConfirmModal` auto-focus;
  - `deleteById` doesn't encode the id;
  - `DateCompareValidator` uses `DateTime.UtcNow`.
- **No git:** neither repo is under git, so there's no commit to pin and "secret committed" can't be checked.
- **Not assessed:** production build; build / lint / automated tests by the reviewer; the DST case for Last Amended (T-ANIMAL-003 S5) live; null booleans live (T-ANIMAL-009 S5; no page renders one).

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: Not applicable — direct hand-off. Logged in `reviews/review-log.md` (Decision 29 cycle 1: code review + test review, test round 1).</sub>
