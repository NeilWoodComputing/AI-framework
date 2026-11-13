# Review: DIRECT-manage-animals-2 — Manage Animals

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (round 2; re-review of the round 1 fixes) |
| Trigger | direct-handoff |
| Review scope | Plan scope (`direct_scope: plan`) — details in **Review scope** |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git (API and UI; `code.api.head_commit` / `code.ui.head_commit` are null) — files read from disk on 08/10/2026 (Dev Bot fix files last written 16:47) |
| Linked tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007 (from `handoff.md` `tickets` and the `implementation` manifest) |
| Feature(s) | `ai-planning-framework/work/manage-animals/` |
| Specs reviewed | `specs/manage-animals.yaml` (`excel/manage-animals.xlsx`), `specs/add-edit-animal.yaml` (`excel/add-edit-animal.xlsx`); journey `journeys/j-animal-manage.md` used as context (all unchanged since round 1) |
| Active API / UI | API.Framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` (api-framework-overview, -ui-contract, -controllers, -auth-permissions, -data-migrations, -services, -testing, json-schema-forms) and the `.cursor/skills` "Check" sections, + shared `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc`; Next.js `AGENTS.md`, `README.md` and `.cursor/rules` (framework/, style/, implementation/) taken from `development.ui.options.nextjs.rules` (+ general practice where no rule applies); `checklists/ui-nextjs-checklist.md` (updated 16:56 today, sections A–C), `full-stack-checklist.md`, `api-checklist.md`, `security-checklist.md`, `severity.md` |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 08/10/2026 17:05 (Europe/London) |
| Review iteration | 2 |

## Verdict

**Approve**

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 0 | 0 | 4 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`.

## Summary

Hi Dev Bot, thanks for a really tidy round of fixes. Round 2 re-reviewed all 79 manifest files whole (now including `Modal.tsx`, `ConfirmModal.tsx`, `RoutedModal.tsx` and `tokens.css`) against both specs, all 62 Given / When / Then scenarios in T-ANIMAL-001 to 007, the API.Framework rules and skills, and the Next.js `AGENTS.md`, `README.md` and `.cursor/rules` (now named directly in the config), with the refreshed `checklists/ui-nextjs-checklist.md`. All 12 round 1 findings are resolved: Name and Date Born now show the required marker, Escape only closes the top-most menu / modal, the delete confirm is red, shows a loading state, can't double-fire and closes on failure so the API's message is visible, the modal shows "Animal catalogue", and the dark-mode colours use semantic tokens. I didn't find any regressions, including for the reference-data forms that share the renderers and modals. The four new findings are all Nits (a bare `NotFound()` on GET, missing final newlines, and one stacking `level`), so the verdict is **Approve** and it goes to Neil to merge. Tests are still a tooling decision for Neil, not findings (see **Tests**).

## Review scope

How the scope was built: Plan scope — started from the `implementation` manifest in `handoff.md` (recorded 16:49:30; 79 files: 18 api, 3 migrations, 58 ui; `tests: []`), then searched `ai-code-framework/api/API.Framework` and `ai-code-framework/ui/UI.NextJs.Framework` again for page names (Manage Animals, Add \| Edit Animal), routes (`/examples/animals`, `v1/Animal`, `v1/schemas/animal`), Service `Animals`, `creatures.animals` / `Animal.*` columns, `animals_write` / `AnimalsWrite`, ticket IDs and derived names (`Animal*`, `animal-*`, `animals-*`), plus every consumer of the shared code changed in this round (`ConfirmModal`, `RoutedModal`, `Modal`, `requiredField`, the new tokens). I also compared every file against the round 1 copy (read at 16:12) to see exactly what changed.

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
| ui | `src/app/examples/animals/@modal/(.)manage/page.tsx` | ui | manifest | T-ANIMAL-003 |
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
| ui | `src/features/animals/animals-landing/AnimalsLanding.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-005; controls: Delete Animal |
| ui | `src/features/animals/manage-animals-modal/AnimalsGrid.tsx` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/manage-animals-modal/use-animals-grid.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-005, T-ANIMAL-007; controls: + Add Animal, Edit Animal, Delete Animal |
| ui | `src/features/animals/manage-animals-modal/columns/animals-grid-columns.tsx` | ui | manifest | T-ANIMAL-003, T-ANIMAL-006; controls: Name, Is Furry, Has Hooves, Date Born, Attributes, Last Amended; `Animal.Name`, `Animal.IsFurry`, `Animal.HasHooves`, `Animal.DateBorn`, `Animal.Attributes`, `Animal.UpdatedUtc`, `Animal.UpdatedBy` |
| ui | `src/features/animals/manage-animals-modal/state/animals-search.data-provider.ts` | ui | manifest | T-ANIMAL-003 |
| ui | `src/features/animals/animal-form-modal/AnimalFormModal.tsx` | ui | manifest | T-ANIMAL-004; controls: Save, Cancel |
| ui | `src/features/animals/animal-form-modal/state/animal-entity.data-provider.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/features/animals/animal-form-modal/state/animal-ui-schema.ts` | ui | manifest | T-ANIMAL-004 |
| ui | `src/features/animals/animal-form-modal/ui-schemas/animal.ui-schema.json` | ui | manifest | T-ANIMAL-004; controls: Name, Date Born, Attributes, Is Furry, Has Hooves |
| ui | `src/framework/auth/permissions.ts` | ui | manifest | T-ANIMAL-007, T-ANIMAL-003 |
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
| ui | `src/framework/entity-framework/components/entity-grid-auth-gate/EntityGridAuthGate.tsx` | ui | manifest (existing, dependency) | T-ANIMAL-003 |
| ui | `src/framework/auth/context/AuthProvider.tsx` | ui | manifest (existing, dependency) | T-ANIMAL-003, T-ANIMAL-007 |
| ui | `src/framework/design-system/components/modal/Modal.tsx` | ui | manifest (new in round 2; changed) | T-ANIMAL-005, T-ANIMAL-007; Escape closes only the top-most modal (F-02) |
| ui | `src/framework/design-system/components/modal/ConfirmModal.tsx` | ui | manifest (new in round 2; changed) | T-ANIMAL-005; controls: Delete Animal (`confirmTheme`, `loading`; F-03, F-05) |
| ui | `src/framework/design-system/components/modal/RoutedModal.tsx` | ui | manifest (new in round 2; changed) | T-ANIMAL-003; page sub-text (`subtitle`; F-04) |
| ui | `src/framework/design-system/theme/tokens.css` | ui | manifest (new in round 2; changed) | T-ANIMAL-006, T-ANIMAL-007; new semantic tokens with dark values (F-06) |
| ui | `src/framework/design-system/components/modal/ModalShell.tsx` | ui | dependency (read for context) | renders `subtitle` above the title; F-04 |
| ui | `src/framework/design-system/buttons/button/Button.tsx` | ui | dependency (read for context) | spreads `aria-haspopup`, so the menu can return focus to its trigger; `loading` state |
| ui | `src/framework/design-system/forms/input/Input.tsx` | ui | dependency (read for context) | `requiredField`; F-01 |
| ui | `src/framework/design-system/forms/form-field/FormField.tsx` | ui | dependency (read for context) | `FormFieldLabel requiredField`; F-01 |
| ui | `src/framework/api/unity-api-fetch.ts` | ui | dependency (read for context) | bearer token on every animal call |
| ui | `src/framework/json-schema-form/services/json-schema-data.service.ts` | ui | dependency (read for context) | schema fetch throws a plain `Error`, so the new 404 branch only reacts to the record read |
| api | `Api.Framework.Services/DataFramework/JsonSchemaValidation/RecordValidationRequest.cs` | api | dependency (read for context) | null-value handling behind the "required" messages |
| api | `Api.Framework/Controllers/V1/Examples/CatalogueItemController.cs` | api | dependency (read for context) | existing GET-by-id pattern compared for F-13 |
| api | `Api.Framework.Services/Models/AuthContracts.cs` | api | dependency (read for context) | `MessageResponse` shape for F-13 |

- Manifest: 79 files · Discovered (not in manifest): 0 · Diff / dependency: 9 (read for context only)
- Changed since round 1: 13 UI files and 2 API files. Dev Bot's fixes are the 13 UI files plus `LoginDbContext.cs` (F-08). `AnimalService.cs:15` (the comment) was written at 16:24:36, before Dev Bot's pickup at 16:43 (see F-07). Nothing else in either repo changed.
- Whole files reviewed: yes (plan scope)
- Not implemented (no file in scope): none
- Deferred by the ticket's out-of-scope list: none affecting this review (View Animal / View mode was dropped by decision 20 and is correctly absent)
- Excluded: outside `review.scope_include` (only API / UI code is reviewed): planning artefacts (specs, tickets, journey, `handoff.md`) read as the reference only; `review.scope_exclude`: `bin/`, `obj/`, `node_modules/`, `.next/`, generated `tsconfig.tsbuildinfo`, and `UI.NextJs.Framework/.env.local` (never opened). Consumers of the changed shared code checked for regressions but not re-reviewed: reference-data grids and form modals, `SignInForm`, `DesignSystemShowcase.tsx` (also confirms `Switch` is in the showcase, the design-system `README.md:27` and `index.ts:6`)

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix |
|----|----------|------|-----------|---------|-----------------------|---------------|
| F-13 | Nit | API standards | `api/API.Framework/Api.Framework/Controllers/V1/Animals/AnimalController.cs:28` | `GET v1/Animal/{id}` returns a bare `NotFound()` (an empty ProblemDetails with no `message`), while PUT and DELETE return the animal failure body with "The animal was not found." (`AnimalService.cs:111,157`). So opening a deleted animal's Edit URL shows the new generic fallback "This record could not be found. It may have been deleted." (`use-json-schema-entity-form.ts:201-204`), not the API's text that the hand-off note describes. T-ANIMAL-004/S12 is still met and the wording is fine, which is why this is only a Nit (the rule says "preferred", and `CatalogueItemController.cs:60` uses the same bare pattern). | `api/API.Framework/.cursor/rules/api-framework-ui-contract.mdc` → "Preferred failure body (Animals): {success, message, errorMessages, validationErrors}"; T-ANIMAL-004 → Scenario: Deleted animal cannot be opened | Reuse the controller's existing helper: `return item is null ? NotFound(Missing("The animal was not found.")) : Ok(item);` |
| F-14 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/design-system/forms/switch/Switch.tsx:43`, `Switch.module.css:49` | Both new Switch files end without a final newline; they are the only two files in the UI codebase that do. | Next.js `.cursor/rules/style/nextjs-formatting.mdc` → Final newline: yes (formatter point, so Nit per `checklists/ui-nextjs-checklist.md` B and `checklists/severity.md` → Caps) | Add a trailing newline to both files |
| F-15 | Nit | API standards | `api/API.Framework/Api.Framework.Data/Models/Animal.cs:28` (and the other files listed) | The new animal files end without a final newline: `Animal.cs`, `AnimalRecord.cs`, `AnimalJsonSchemaBuilder.cs`, `AnimalContracts.cs`, `IAnimalService.cs`, `AnimalService.cs:313`, `AnimalController.cs:75`, `AnimalSchemaController.cs` and `animalSchema.json`. Every other API.Framework source file (including `AnimalPolicies.cs`) has one. I missed this in round 1, sorry. | General practice (consistency with the codebase; API.Framework has no formatting rule or `.editorconfig`, so formatter-level and capped at Nit) | Add a trailing newline to each of the nine files |
| F-16 | Nit | UI standards | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:42-52` | The "Delete &lt;Name&gt;?" `ConfirmModal` opens over the Manage Animals modal but keeps the default `level="primary"`, so both use z-index 1000 and the confirm is only on top because it's later in the DOM. It works today; it just doesn't say so the way the stacking rule asks. | Next.js `.cursor/rules/framework/nextjs-modal-routing.mdc` → "`size` / `level` — match stacking (e.g. form over manage grid → `level=\"secondary\"`)"; `style/nextjs-design-system.mdc` → `ModalLevel` (stacking) | Pass `level="secondary"` to the delete `ConfirmModal` (it already accepts `level`) |

## Spec conformance (per control)

Spec: `specs/add-edit-animal.yaml` — Basic Form — Add \| Edit Animal (rendered as "Add Animal" / "Edit Animal" by mode, `AnimalFormModal.tsx:53`)

| Section / step | Control | Control type | Mandatory | Editable | Enablement | Min / max | Validation message | Status | Notes / finding |
|----------------|---------|--------------|-----------|----------|------------|-----------|--------------------|--------|-----------------|
| Animal Details | Name | Keyed Input → text `Input` (`unity-json-form-renderers.tsx:34-63`, `animal.ui-schema.json:12-17`) | Yes ✓ server (`animalSchema.json:4,10`) ✓ UI marker (`requiredField={required}`, :52) | Yes ✓ | Always ✓ | 1–100 → `minLength 1`, `maxLength 100`, `pattern \S`, input restricted to 100 ✓ | "Name is required" ✓ (`animalSchema.json:15-17`); "An animal with this name already exists" ✓ (`AnimalService.cs:69-71`) | Match | F-01 resolved. Trim before validate / save ✓ (`AnimalService.cs:166-177`); unique ignoring case among non-deleted ✓ |
| Animal Details | Date Born | Date Picker → native date `Input` (`unity-json-form-renderers.tsx:34-63`) | Yes ✓ server (`animalSchema.json:4,25`) ✓ UI marker (:52) | Yes ✓ | Always ✓ | N/A ✓ | "Date Born is required" ✓; "Date Born must be before today" ✓ (`animalSchema.json:35-36`) | Match | F-01 resolved. UI checks the browser's local date (`unity-schema-validation.ts:100-105`), API the UTC date (`DateCompareValidator`) ✓ |
| Animal Details | Attributes | Tag Input → `UnityTagInputControl` (`unity-json-form-renderers.tsx:282-353`) | No ✓ (no marker, as `required` is false) | Yes ✓ | Always ✓ | 0–50 per tag, max 20 → items `maxLength 50`, `maxItems 20` ✓ (`animalSchema.json:39-53`) | "Each attribute tag must be 50 characters or fewer" ✓; "A maximum of 20 attributes is allowed" ✓ | Match | Starts empty on Add ✓ (`unity-schema.adapter.ts:125-127`); any characters ✓; chip colour now `--app-tag-chip-bg` (light and dark) ✓ |
| Characteristics | Is Furry | Switch → `UnitySwitchControl` + design-system `Switch` (`unity-json-form-renderers.tsx:259-280`) | No ✓ | Yes ✓ | Always ✓ | N/A ✓ | none in spec ✓ | Match | Default Off ✓ (`animalSchema.json:59`, adapter :131-133). Track / thumb / on colours from tokens ✓ (`Switch.module.css:19,25,35`) |
| Characteristics | Has Hooves | Switch → `UnitySwitchControl` | No ✓ | Yes ✓ | Always ✓ | N/A ✓ | none in spec ✓ | Match | Default Off ✓ (`animalSchema.json:65`) |
| (form) | Section titles | "Animal Details", "Characteristics" → `Group` labels (`animal.ui-schema.json:6,34`) | — | — | — | — | — | Match | Group border now `--app-grid-border` ✓ |
| (form) | Save / Cancel | Buttons (`AnimalFormModal.tsx:77-91`) | — | — | Save disabled while loading / saving ✓ | — | Field errors on controls; record-level errors in the modal ✓ | Match | Add and Edit only, no View mode ✓; without permission no form ✓ (`AnimalsModalRoutes.tsx:28-29`); Escape on the form closes only the form (`Modal.tsx:76-88`) ✓ |

Manage list: `specs/manage-animals.yaml` — Modal — Manage Animals ("Animal catalogue")

| Column / action | Population source / action on click | Display format / sortable | Status | Notes / finding |
|-----------------|-------------------------------------|---------------------------|--------|-----------------|
| (page) Title / sub-text | "Manage Animals" / "Animal catalogue" | — | Match | `ManageAnimalsModal.tsx:27-28`; `RoutedModal.tsx:14,30,51` forwards `subtitle` to `ModalShell` ✓ (F-04 resolved) |
| + Add Animal | Open Add \| Edit Animal in Add mode (`use-animals-grid.tsx:74-82`) | Primary action / — | Match | Shown only with `animals_write` ✓ |
| Name | `Animal.Name` (`animals-grid-columns.tsx:14-19`) | Char / Yes, default ascending ✓ (`use-animals-grid.tsx:49`, `AnimalService.cs:249-250`) | Match | |
| Is Furry | `Animal.IsFurry` (`animals-grid-columns.tsx:20-25`) | Switch (read-only) / Yes ✓ | Match | |
| Has Hooves | `Animal.HasHooves` (`animals-grid-columns.tsx:26-32`) | Switch (read-only) / Yes ✓ | Match | |
| Date Born | `Animal.DateBorn` (`animals-grid-columns.tsx:33-38`) | DD/MM/YYYY ✓ (`grid-cell-renderers.tsx:19`) / Yes ✓ | Match | |
| Attributes | `Animal.Attributes` (`animals-grid-columns.tsx:39-44`) | Comma-separated, empty array → empty cell ✓ (`grid-cell-renderers.tsx:12`) / No ✓ | Match | |
| Last Amended | `Animal.UpdatedUtc` & `UpdatedBy` → `User.DisplayName`, fallback `User.Email` (`AnimalService.cs:214-228`; `animals-grid-columns.tsx:45-55`) | "DD/MM/YYYY HH:MM Display name", browser local time ✓ (`grid-cell-renderers.tsx:25`) / Yes, by `UpdatedUtc` ✓ (`AnimalService.cs:246-247`) | Match | |
| Actions column | Last column, header "Actions", not sortable (`EntityGrid.tsx:55-60`) | — / No ✓ | Match | Row click does nothing ✓ |
| Edit Animal (icon Edit) | Open Add \| Edit Animal in Edit mode (`use-animals-grid.tsx:55-61`) | Menu item / — | Match | Escape closes only the menu and returns focus to "Actions" (`EntityGridRowActionsMenu.tsx:35-41`) ✓; menu colours from tokens (`EntityGrid.module.css:80-82,103`) ✓ |
| Delete Animal (icon Delete) | Confirmation "Delete &lt;Name&gt;?" with Cancel / Delete, soft delete, refresh (`use-animals-grid.tsx:63-72,90-106`; `ManageAnimalsModal.tsx:41-53`) | Menu item / — | Match | Message only, no duplicate title ✓ (F-10); red `system-red` button ✓ (F-03); loading / double-click guard, confirm closes on failure, API message shown ✓ (F-05); stacking `level` → F-16 |
| No-permission callout | "You do not have permission to manage animals." (`AnimalsAccessNotice.tsx:8,21-22`) | Warning `Callout` / — | Match | |

## Data mapping (per control)

No mapping code changed in this round (only the `AnimalService.cs:15` comment and a blank line in `LoginDbContext.cs`). Re-checked against the specs:

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

There is still no automated test project in API.Framework (by rule) and no test runner in UI.NextJs.Framework, so no scenario can be **Covered**. Scenarios whose code I traced and found correct are marked **Partial** with "code ✓"; see **Tests** for why this is a note and not a set of findings.

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
| T-ANIMAL-003/S1 | Open Manage Animals from the nav | Partial | `SiteNav.tsx:32-37`; `AnimalsLanding.tsx:21-29`; `app/examples/animals/@modal/(.)manage/page.tsx`; `ManageAnimalsModal.tsx:27-28` | none | code ✓ (title and "Animal catalogue" sub-text; F-04 resolved) |
| T-ANIMAL-003/S2 | List shows non-deleted animals | Partial | `animals-search.data-provider.ts:13`; `animals-grid-columns.tsx:13-56`; `AnimalService.cs:30` | none | code ✓ |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user | Partial | `animals-grid-columns.tsx:45-55`; `grid-cell-renderers.tsx:25` | none | code ✓ |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | Partial | `grid-cell-renderers.tsx:25` | none | code ✓ |
| T-ANIMAL-003/S5 | Last Amended outside summer time | Partial | `grid-cell-renderers.tsx:25` | none | code ✓ (uses the browser's own offset) |
| T-ANIMAL-003/S6 | Default sort by Name ascending | Partial | `use-animals-grid.tsx:27,49`; `AnimalService.cs:234-250` | none | code ✓ |
| T-ANIMAL-003/S7 | Add opens Basic Form | Partial | `use-animals-grid.tsx:74-82`; `app/examples/animals/@modal/(.)manage/item/page.tsx` | none | code ✓ (required markers now shown) |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | Partial | `use-animals-grid.tsx:55-61`; `use-json-schema-entity-form.ts:182-198` | none | code ✓ |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | Partial | `EntityGrid.tsx:43-60,130-136`; `use-animals-grid.tsx:52-73` | none | code ✓ (F-02 and F-06 resolved) |
| T-ANIMAL-003/S10 | User without animals_write cannot open Manage Animals | Partial | `AnimalsModalRoutes.tsx:13-14,28-29`; `AnimalsAccessNotice.tsx:8,21-22`; `AnimalsLanding.tsx:31` | none | code ✓ (no `v1/Animal` request without the permission) |
| T-ANIMAL-003/S11 | User-management permissions alone do not give access to animals | Partial | `animal-permissions.ts:6-8`; `use-animals-access.ts:13`; `SiteNav.tsx:32` | none | code ✓ |
| T-ANIMAL-004/S1 | Add mode opens with defaults | Partial | `unity-schema.adapter.ts:125-136`; `animalSchema.json:59,65`; `unity-json-form-renderers.tsx:52` | none | code ✓ (Name and Date Born marked required; F-01 resolved) |
| T-ANIMAL-004/S2 | Create animal with required fields | Partial | `use-json-schema-entity-form.ts:219-262`; `unity-schema-value.mapper.ts:15-31`; `AnimalFormModal.tsx:32-35` | none | code ✓ (closes and refreshes the grid) |
| T-ANIMAL-004/S3 | Name is mandatory | Partial | `unity-schema-validation.ts:214-223`; `animalSchema.json:14-17`; `unity-json-form-renderers.tsx:52` | none | code ✓ (message and marker) |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | Partial | `api-error.utils.ts:26-60`; `use-json-schema-entity-form.ts:253-257` | none | code ✓ (API message shown on Name) |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | Partial | `AnimalService.cs:69` | none | code ✓ |
| T-ANIMAL-004/S6 | Date Born must be before today | Partial | `unity-schema-validation.ts:100-163` | none | code ✓ (browser local date) |
| T-ANIMAL-004/S7 | Date Born is mandatory | Partial | `unity-schema-validation.ts:214-223`; `unity-json-form-renderers.tsx:52` | none | code ✓ (message and marker) |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | Partial | `unity-schema-value.mapper.ts:22-28`; `AnimalService.cs:276-277` | none | code ✓ |
| T-ANIMAL-004/S9 | Attribute tag limits | Partial | `unity-schema-validation.ts:225-232`; `unity-json-form-renderers.tsx:348-350` | none | code ✓ |
| T-ANIMAL-004/S10 | Edit persists changed fields | Partial | `use-json-schema-entity-form.ts:243-247`; `AnimalService.cs:102-146` | none | code ✓ (Last Amended updated) |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | Partial | `animal-routes.ts:6`; `AnimalFormModal.tsx:53` | none | code ✓ (no View) |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | Partial | `AnimalService.cs:49-54`; `AnimalController.cs:28`; `use-json-schema-entity-form.ts:199-210`; `AnimalFormModal.tsx:93-94` | none | code ✓ ("This record could not be found. It may have been deleted."; F-09 resolved; API body → F-13) |
| T-ANIMAL-005/S1 | Confirmation names the animal | Partial | `ManageAnimalsModal.tsx:41-53` | none | code ✓ ("Delete &lt;Name&gt;?" once, red Delete; F-03 and F-10 resolved; F-16) |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | Partial | `use-animals-grid.tsx:90-106`; `AnimalService.cs:149-165` | none | code ✓ (F-05 resolved) |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | Partial | `ManageAnimalsModal.tsx:50`; `use-animals-grid.tsx:118-120`; `Modal.tsx:76-88` | none | code ✓ (Cancel or Escape closes only the confirm; F-02 resolved) |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | Partial | `AnimalService.cs:30,51,69,108,154` | none | code ✓ |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | Partial | `AnimalController.cs:57-58`; `use-animals-grid.tsx:67` | none | code ✓ |
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Partial | `unity-json-form-renderers.tsx:259-280`; `Switch.tsx:12-37` | none | code ✓ (token colours; F-06 resolved) |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Partial | `unity-json-form-renderers.tsx:282-353` | none | code ✓ |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Partial | `unity-json-form-renderers.tsx:348-350`; `unity-schema-validation.ts:225-232` | none | code ✓ |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Partial | `unity-json-form-renderers.tsx:263,273,287,317,330`; `Switch.tsx:36-37` | none | code ✓ |
| T-ANIMAL-006/S5 | Grid cells | Partial | `grid-cell-renderers.tsx:7-30`; `animals-grid-columns.tsx:24,31,43` | none | code ✓ |
| T-ANIMAL-007/S1 | Row actions menu in the last column | Partial | `EntityGrid.tsx:55-60,130-136` | none | code ✓ |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | Partial | `EntityGridRowActionsMenu.tsx:78-82` | none | code ✓ |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Partial | `EntityGrid.tsx:44-49`; `permissions.ts:6-13` | none | code ✓ |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Partial | `permissions.ts:10-12` | none | code ✓ |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Partial | `EntityGrid.tsx:55` | none | code ✓ |
| T-ANIMAL-007/S6 | Per-row visibility | Partial | `EntityGrid.tsx:51-52` | none | code ✓ |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Partial | `EntityGridRowActionsMenu.tsx:51` | none | code ✓ |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | Partial | `EntityGrid.tsx:130-150` | none | code ✓ (button rendering kept when `rowActionsDisplay` isn't `menu`); no pre-change copy to diff against (see notes) |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | Partial | `EntityGridRowActionsMenu.tsx:29-49` | none | code ✓ (Escape stops at the menu and focus returns to the trigger; F-02 resolved) |

## Security and data

| Spec rule / check | Status | Reference |
|-------------------|--------|-----------|
| Every animal endpoint (list, get, create, update, delete, form schema) requires `animals_write` | Enforced server-side | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` |
| User-management permissions alone give no access | Enforced server-side | `Program.cs:86-87` (policy checks only `animals_write`); UI `animal-permissions.ts:6-8` |
| Name mandatory, 1–100, trimmed | Enforced server-side (+ client, now with required marker) | `animalSchema.json:6-18`; `AnimalService.cs:166-177` |
| Name unique (case-insensitive, non-deleted) | Enforced server-side (service check + filtered unique index) | `AnimalService.cs:69-71,92-97,121-126,140-143`; `LoginDbContext.cs:467-470` |
| Date Born mandatory and before today | Enforced server-side (UTC) + client (local date) | `animalSchema.json:20-37`; `unity-schema-validation.ts:100-163` |
| Attributes ≤ 50 characters per tag, ≤ 20 tags | Enforced server-side (+ client) | `animalSchema.json:39-53` |
| Soft delete only; deleted rows never listed or opened | Enforced server-side | `AnimalService.cs:30,51,108,154-162` |
| Delete can't double-fire from the UI | Client guard (server is idempotent-safe: a second DELETE gets 404) | `use-animals-grid.tsx:91,118-120`; `ConfirmModal.tsx:51-57` |
| Audit `UpdatedUtc` / `UpdatedBy` from the token, not the client | Enforced server-side | `AnimalController.cs` (`sub` claim); `AnimalService.cs:86-87,135-136,161-162` |
| Error messages don't leak internals | Yes — UI shows the API's `message` or a plain fallback, never the HTTP status | `use-animals-grid.tsx:97-100`; `use-json-schema-entity-form.ts:199-210` |
| Injection | No raw SQL; LINQ only | `AnimalService.cs` |
| Secrets / tokens | None seen in reviewed code; `.env*` files not opened, created or edited; `src/config/environment.ts` unchanged; "committed" can't be checked without git | — |
| PII | List returns the last amender's display name or email to `animals_write` users, as the spec requires; nothing logged | `AnimalService.cs:228` |
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
| UI scenarios T-ANIMAL-003, -004, -005, -006, -007 (including the round 1 fixes: required markers, Escape stacking, delete error path) | none | Untested |

**Why these are not findings.** Same as round 1, and I've kept it consistent: `review-tests` would normally raise a Major for an untested mandatory, uniqueness or persistence rule, but API.Framework has no test project and its own rule (`api/API.Framework/.cursor/rules/api-framework-testing.mdc`) says not to create one "unless Neil asks", and UI.NextJs.Framework has no test runner (`checklists/ui-nextjs-checklist.md` C notes there is none in `package.json`). The implementing agent couldn't add tests without breaking that rule, so this is a tooling decision for the human owner (Neil), not a defect in this change, and it doesn't affect the verdict. It's a good fit for the `ai-test-framework` Neil is considering. The suggested tests from round 1 still stand.

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
- UI (if a runner such as Vitest is added): `validateUnitySchemaData` cases for blank / whitespace Name, today's date in local time, 21 tags and a 51-character tag; `hasAnyPermission` any-of cases; `Modal` stack (Escape on a confirm over Manage Animals closes only the confirm); `EntityGridRowActionsMenu` Escape not reaching the modal; `useAnimalsGrid.confirmDelete` ignoring a second call while in flight and showing the API message on failure.

Checks run: none by the reviewer (read-only review; no build, lint or tests run). The hand-off records `dotnet build` (Release) and `npm run build` passing after the fixes, and `npm run lint` not run because there is no ESLint configuration (pre-existing).

## Changes since last review

Round 1 report: `reviews/DIRECT-manage-animals-1-review.md` (Request changes; Blocker 0 · Major 1 · Minor 5 · Nit 6).

| Round 1 finding | Severity | Status | Evidence |
|-----------------|----------|--------|----------|
| F-01 Required markers on Name / Date Born | Major | Resolved | `unity-json-form-renderers.tsx:34,52` takes `required` from `ControlProps` and passes `requiredField`; also on `FormFieldLabel` in TextArea (:77), IconPicker (:112), InlineList (:152) and TagInput (:309). Switch has no marker, which is right because both switches are optional |
| F-02 Escape leaking to Manage Animals | Minor | Resolved | Menu: `EntityGridRowActionsMenu.tsx:35-41` stops propagation and returns focus to the trigger. Stacked modals: `Modal.tsx:22-27,57-88` keeps an open-modal stack and only the top-most modal handles Escape (also covers the Add \| Edit form over the grid and reference-data stacks). Checked the mount order when Manage Animals and the form open in the same commit: the form ends up on top |
| F-03 Destructive button colour | Minor | Resolved | `ConfirmModal.tsx:18,34,55` adds `confirmTheme` (default unchanged); `ManageAnimalsModal.tsx:47` passes `system-red` |
| F-04 Modal sub-text | Minor | Resolved | `RoutedModal.tsx:14,30,51` forwards `subtitle`; `ManageAnimalsModal.tsx:28` "Animal catalogue" |
| F-05 Delete error handling | Minor | Resolved | `use-animals-grid.tsx:90-106`: goes through `AnimalEntityDataProvider.deleteById`, guards on `deleteInFlight`, shows the API's message or "The animal could not be deleted.", closes the confirm in `finally`; `cancelDelete` ignored while in flight (:118-120); `ConfirmModal` `loading` disables Cancel and shows Delete loading (:51-57) |
| F-06 Undefined `--color-*` tokens / dark mode | Minor | Resolved | `EntityGrid.module.css:80-82,103`, `JsonSchemaForm.module.css:43,59,66,70,96,111`, `Switch.module.css:19,25,35` now use `--app-*` / `--primary-action`; new tokens have light and dark values in `tokens.css`; no `var(--color-*)` left in the UI |
| F-07 `auth.animals` comment | Nit | Resolved | `AnimalService.cs:15` now reads `creatures.animals`. A note for the record: the round 1 copy (read at 16:12) did say `auth.animals`; the file was changed at 16:24:36, before Dev Bot's pickup at 16:43, which is why Dev Bot found it already correct |
| F-08 Double blank line | Nit | Resolved | `LoginDbContext.cs:453-455` has a single blank line before the `Animal` block |
| F-09 Deleted-animal message | Nit | Resolved | `use-json-schema-entity-form.ts:199-210` shows a not-found message on a 404 instead of "Please try again." It shows the generic fallback rather than "The animal was not found." because GET returns a bare 404 → new F-13 |
| F-10 Duplicate confirm title | Nit | Resolved | `ManageAnimalsModal.tsx:42-52` has no `title`; message `Delete ${name}?` only |
| F-11 Misplaced comment / typo | Nit | Resolved | `JsonSchemaForm.tsx:11` "additionalErrors"; validation doc moved onto `JsonSchemaFormValidation` (:14-21) |
| F-12 Unused `.switchCell` | Nit | Resolved | Removed from `EntityGrid.module.css` |

- Resolved: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12
- Still open: none
- New: F-13, F-14, F-15, F-16 (all Nit)
- Regressions: none found. Reference-data grids, forms and modals use the same renderers and modals; the changes there are additive (required markers on genuinely required fields, Escape only on the top-most modal, `confirmTheme` / `loading` / `subtitle` optional with unchanged defaults)

## Out of scope / pre-existing notes

These do not affect the verdict.

- **Config and checklist:** the config now names `ai-code-framework/ui/UI.NextJs.Framework/.cursor/rules` (`development.ui.options.nextjs.rules`, `agent_docs: [AGENTS.md, README.md]`), and `checklists/ui-nextjs-checklist.md` was rewritten at 16:56 today to cite those rules (sections A and B) with general practice only in section C. The framework docs (`AGENT-BRIEF.md`, `README.md`, `severity.md`, the `review-code-standards` and `write-review-report` skills, the report template) were updated at 16:55 to match. This round used the updated versions; round 1's "config still `null`" note is closed.
- **API skills:** API.Framework gained `.cursor/skills` at 16:25 today; their "Check" sections (area policy on every endpoint, `PagedQuery` / `PagedBody`, Release build) are satisfied by this change.
- **Tests:** still a tooling decision for Neil (see **Tests**).
- **No git:** neither repo is under git, so there is no commit to pin and "secret committed" can't be checked. "Existing forms and grids unaffected" (T-ANIMAL-006, T-ANIMAL-007/S8) was checked by reading the code paths and, for this round, by diffing against the round 1 copy.
- **Spec / planning note (carried forward):** the Standard group's seeded description (`LoginDbContext.cs:158`) still says "Can view users and groups." although decision 25 gives that group `animals_write`. Changing seed text needs a migration, so it's for the planning agent to decide (Dev Bot also flagged it as out of scope).
- **Pre-existing:** `Modal` doesn't return focus to the element that opened it when it closes, and `ConfirmModal` auto-focuses the confirm button (so Enter on the delete confirm deletes). Both predate this plan and affect every modal; worth a framework ticket rather than a feature fix.
- **Pre-existing:** `AbstractEntityDataProvider.deleteById` doesn't `encodeURIComponent` the id (animal ids are GUIDs, so no impact here).
- **Pre-existing:** `DateCompareValidator` uses `DateTime.UtcNow` rather than `TimeProvider`, so date rules can't be tested with a fake clock.
- **Docs outside the manifest (carried forward):** the Next.js `README.md` still describes `Unity.UI.Next` / `cp .env.example .env.local` setup, and the design-system `README.md:17` lists a `Visibility` icon that `Icon.tsx` no longer has.
- **Hand-off note accuracy:** the hand-off says the Edit URL of a deleted animal shows "The animal was not found."; it shows "This record could not be found. It may have been deleted." (F-13 explains why).
- **Raw `<button>` in the row actions menu and tag chips:** checked against `checklists/ui-nextjs-checklist.md` B → "`Button` for all actions (no raw `<button>` where the primitive fits)". `Button` has no menu-item or chip variant, so the primitive doesn't fit and this isn't a finding.
- **Migration:** `Down` drops `creatures.animals` but leaves the empty `creatures` schema (EF's default); fine, noted for awareness.
- **Not assessed live:** no database run, no browser click-through, no build / lint by the reviewer (dark mode, Escape, focus and the delete error path were assessed from the code).

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: Not applicable — direct hand-off. Logged in `reviews/review-log.md` (round 2).</sub>
