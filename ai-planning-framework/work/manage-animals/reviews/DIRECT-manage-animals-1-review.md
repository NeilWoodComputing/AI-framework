# Review: DIRECT-manage-animals-1 — Manage Animals

| Field | Value |
|-------|-------|
| PR / hand-off | Direct hand-off — `handoff.md` (round 1) |
| Trigger | direct-handoff |
| Review scope | Plan scope (`direct_scope: plan`) — details in **Review scope** |
| Source → target | n/a (plan scope) |
| Provider | n/a (plan scope) |
| Reviewed commit | not under git (API and UI; `code.api.head_commit` / `code.ui.head_commit` are null) — files read from disk on 08/10/2026 |
| Linked tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007 (from `handoff.md` `tickets` and the `implementation` manifest) |
| Feature(s) | `ai-planning-framework/work/manage-animals/` |
| Specs reviewed | `specs/manage-animals.yaml` (`excel/manage-animals.xlsx`), `specs/add-edit-animal.yaml` (`excel/add-edit-animal.xlsx`); journey `journeys/j-animal-manage.md` used as context |
| Active API / UI | API.Framework (`ai-code-framework/api/API.Framework`) / nextjs (`ai-code-framework/ui/UI.NextJs.Framework`) |
| Rule sets applied | API.Framework `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` (api-framework-overview, -ui-contract, -controllers, -auth-permissions, -data-migrations, -services, -testing, json-schema-forms) + shared `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc`; Next.js `README.md` → `AGENTS.md` and the `.cursor/rules/` it points to (framework/, style/, implementation/), with `checklists/ui-nextjs-checklist.md` section B as **General practice**; `checklists/full-stack-checklist.md`, `api-checklist.md`, `security-checklist.md`, `severity.md` |
| Reviewer agent | ai-review-framework (Review Bot) |
| Review date | 08/10/2026 16:34 (Europe/London) |
| Review iteration | 1 |

## Verdict

**Request changes**

| Blocker | Major | Minor | Nit |
|---------|-------|-------|-----|
| 0 | 1 | 5 | 6 |

Severity threshold for Request changes: `major`. Rules: `checklists/severity.md`.

## Summary

Hi Dev Bot, this is a really solid first round: every control, column and audit field in the two specs is built and persisted to the right `Animal` (`creatures.animals`) column, the API enforces mandatory, length, date and uniqueness rules on the server with the exact spec messages, every animal endpoint sits behind the single `AnimalsWrite` policy, and delete is a proper soft delete. I reviewed all 75 manifest files whole (9,204 lines) against both specs, all 62 Given / When / Then scenarios in T-ANIMAL-001 to 007, the API.Framework rules and the Next.js rules the README points to. The verdict is **Request changes** for one reason: Name and Date Born are mandatory in the spec but the form doesn't mark them as required (F-01, Major, and a one-line fix in the shared text renderer). The Minor items are worth doing in the same pass: Escape leaking from the row menu / delete confirm to the Manage Animals modal, the delete error being hidden behind the confirm, the missing modal sub-text, the destructive button colour and some dark-mode colour tokens. The Nits are optional polish. No Blockers and no data mapping problems.

## Review scope

How the scope was built: Plan scope — started from the `implementation` manifest in `handoff.md` (75 files: 18 api, 3 migrations, 54 ui; `tests: []`), then searched `ai-code-framework/api/API.Framework` and `ai-code-framework/ui/UI.NextJs.Framework` for page names (Manage Animals, Add \| Edit Animal), routes (`/examples/animals`, `v1/Animal`, `v1/schemas/animal`), Service `Animals`, `creatures.animals` / `Animal.*` columns, `animals_write` / `AnimalsWrite`, ticket IDs and derived names (`Animal*`, `animal-*`, `animals-*`).

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
| ui | `src/framework/design-system/components/modal/Modal.tsx` | ui | dependency (read for context; not changed by this plan) | Escape handling behind F-02 |
| ui | `src/framework/design-system/components/modal/RoutedModal.tsx` | ui | dependency (read for context) | Manage Animals / Add \| Edit Animal modal chrome; F-04 |
| ui | `src/framework/design-system/components/modal/ModalShell.tsx` | ui | dependency (read for context) | `subtitle` support; F-04 |
| ui | `src/framework/design-system/components/modal/ConfirmModal.tsx` | ui | dependency (read for context) | "Delete &lt;Name&gt;?" confirmation; F-03, F-05 |
| ui | `src/framework/design-system/forms/input/Input.tsx` | ui | dependency (read for context) | `requiredField` support; F-01 |
| ui | `src/framework/design-system/forms/form-field/FormField.tsx` | ui | dependency (read for context) | `FormFieldLabel requiredField`; F-01 |
| ui | `src/framework/design-system/theme/tokens.css` | ui | dependency (read for context) | semantic colour tokens; F-06 |
| ui | `src/framework/api/unity-api-fetch.ts` | ui | dependency (read for context) | bearer token on every animal call |
| ui | `src/framework/json-schema-form/services/json-schema-data.service.ts` | ui | dependency (read for context) | schema fetch for Add / Edit |
| api | `Api.Framework.Services/DataFramework/JsonSchemaValidation/RecordValidationRequest.cs` | api | dependency (read for context) | null-value handling that makes the "required" messages work |

- Manifest: 75 files · Discovered (not in manifest): 0 · Diff / dependency: 10 (read for context only)
- Whole files reviewed: yes (plan scope)
- Not implemented (no file in scope): none
- Deferred by the ticket's out-of-scope list: none affecting this review (View Animal / View mode was dropped by decision 20 and is correctly absent)
- Excluded: outside `review.scope_include` (only API / UI code is reviewed): planning artefacts (specs, tickets, journey, `handoff.md`) read as the reference only; `review.scope_exclude`: `bin/`, `obj/`, `node_modules/`, `.next/`, generated `tsconfig.tsbuildinfo`, and `UI.NextJs.Framework/.env.local` (never opened). Search hits judged not relevant and not reviewed: `NormalizedName` on Role / Tenant and `TenantService`, older migration designers, `DesignSystemShowcase.tsx` (Switch demo) and the design-system `README.md` (both edited outside this manifest; see notes)

## Findings

| ID | Severity | Area | File:line | Finding | Spec / rule reference | Suggested fix |
|----|----------|------|-----------|---------|-----------------------|---------------|
| F-01 | Major | Spec conformance | `ui/UI.NextJs.Framework/src/framework/json-schema-form/components/renderers/unity-json-form-renderers.tsx:34-61` | Name and Date Born are mandatory in the spec and in the server schema (`animalSchema.json:4`), but the form never shows them as required. `UnityTextControl` renders `Input` without `requiredField`, so neither label gets the required marker. Why it matters: people can't tell which fields they must fill in until Save fails, and the spec checklist treats "mandatory" as both server-enforced **and** visible in the UI. | `specs/add-edit-animal.yaml` → Animal Details → Name / Date Born (`mandatory: "Yes"`); `checklists/full-stack-checklist.md` → **Mandatory** ("in the server schema `required` and shown as required in the UI"); T-ANIMAL-004 checklist "UI behaviour matches the Excel control rows (… mandatory …)"; Next.js `.cursor/rules/style/nextjs-design-system.mdc` → Form controls (`Input` takes `requiredField`) | Take `required` from `ControlProps` (JSON Forms sets it from the schema's root `required` array, which `toJsonFormsSchema` keeps) and pass `requiredField={required}` to `Input` at :48-60. For consistency, pass `requiredField={required}` to `FormFieldLabel` in the other label-rendering controls (:75, :146, :302). This also adds the marker to required fields on existing reference-data forms, which is the correct behaviour |
| F-02 | Minor | Acceptance criteria | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGridRowActionsMenu.tsx:35-36` | Pressing Escape with a row's actions menu open closes the menu **and** the whole Manage Animals modal. The menu listens on `document`, and `Modal` (`src/framework/design-system/components/modal/Modal.tsx:62-69`) closes on any Escape it sees on `window`, so the same key press reaches both. The same happens on the "Delete &lt;Name&gt;?" confirmation: Escape cancels it and also closes Manage Animals, so the row is no longer "visible on Manage Animals". Why it matters: Escape should only dismiss the top-most thing, and losing the list is surprising. | T-ANIMAL-007 → Scenario: Menu closes on Escape and outside click; T-ANIMAL-005 → Scenario: Cancel leaves the animal unchanged; `checklists/ui-nextjs-checklist.md` B → Accessibility ("focus managed when modals open and close") — General practice | In the menu's `handleKey`, call `event.stopPropagation()` before `setOpen(false)` (the `document` listener runs before `Modal`'s `window` listener, so this is enough), and return focus to the trigger. For stacked modals, make `Modal` act only when it is the top-most open modal (for example a small module-level stack in `Modal.tsx`), which fixes the confirm and the Add \| Edit Animal form over the grid in one place |
| F-03 | Minor | UI standards | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:41-50` | The Delete button on the "Delete &lt;Name&gt;?" confirmation uses the normal primary style, because `ConfirmModal` always renders its confirm button with `theme="primary-action"` (`ConfirmModal.tsx:49`). Why it matters: a red destructive button is the visual cue that this action removes something. | Next.js `.cursor/rules/style/nextjs-design-system.mdc` → Buttons ("Destructive confirm actions use `theme=\"system-red\"`") | Add an optional `confirmTheme?: ButtonTheme` prop to `ConfirmModal` (default `primary-action`, so existing callers don't change) and pass `confirmTheme="system-red"` here |
| F-04 | Minor | Spec conformance | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:25-32` | The spec's page sub-text "Animal catalogue" doesn't appear in the Manage Animals modal; it is only on the Animals page header behind it (`app/examples/animals/page.tsx`). `ModalShell` already supports a `subtitle`, but `RoutedModal` (`RoutedModal.tsx:11-24`) doesn't pass one through. Why it matters: the modal header should match the spec's title and sub-text pair. | `specs/manage-animals.yaml` → `page_title: Manage Animals`, `page_sub_text: "Animal catalogue"` | Add `subtitle?: ReactNode` to `RoutedModalProps` and forward it to `ModalShell`, then pass `subtitle="Animal catalogue"` from `ManageAnimalsModal` |
| F-05 | Minor | UI standards | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/use-animals-grid.tsx:88-104` | If the delete call fails: (1) the message is the technical "Delete failed: 404" rather than the API's text ("The animal was not found."); (2) the confirm stays open and the error `Callout` (`ManageAnimalsModal.tsx:33`) renders behind it, so the user sees nothing happen; (3) nothing stops a second click while the first DELETE is in flight (`deleteInFlight` is tracked but not used), which turns a successful delete into a confusing 404 error. Why it matters: errors should reach the user in plain words, and destructive actions shouldn't double-fire. | `checklists/ui-nextjs-checklist.md` B → "Loading, empty and error states handled for each data call; errors shown to the user without leaking internals" — General practice; Next.js `.cursor/rules/framework/nextjs-json-schema-forms.mdc` → "Extend `AbstractEntityDataProvider` … Persist goes through the provider" | Call `AnimalEntityDataProvider.deleteById(id)` (it already throws `ApiRequestError` with the body), show `getErrorMessage(error, 'The animal could not be deleted.')`, close the confirm on failure (or show the error inside it), and return early from `confirmDelete` when `deleteInFlight` is true (and disable / show loading on the Delete button if `ConfirmModal` gains a `loading` prop) |
| F-06 | Minor | UI standards | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGrid.module.css:80-102` | The new row actions menu, Switch and tag chips use `--color-surface`, `--color-border` and `--color-surface-alt`, which aren't defined anywhere (`tokens.css` defines `--app-*` tokens), so the hard-coded fallbacks always apply. In dark mode the menu is white (`#fff`) while its text inherits the dark-mode text colour (`#e8eaed`), so the items are almost unreadable; tag chips (`JsonSchemaForm.module.css:96`) have the same problem, and the Switch track uses `#c8c8c8` (`Switch.module.css:19`). Why it matters: the theme toggle is a framework feature and these components should follow it. | Next.js `.cursor/rules/style/nextjs-css.mdc` → Token sources (priority) ("Semantic CSS variables from `tokens.css`"; "Never introduce a new hardcoded hex when an existing token fits") and → Dark mode | Use the existing tokens: menu `background: var(--app-surface-raised)`, `border: 1px solid var(--app-grid-border)`, hover / focus `var(--app-grid-row-hover-bg)`; tag chip `var(--app-grid-row-hover-bg)` (or a new semantic token in `tokens.css` with a dark value); Switch track `var(--app-input-border)`; group border (`JsonSchemaForm.module.css:70`) `var(--app-grid-border)` |
| F-07 | Nit | API standards | `api/API.Framework/Api.Framework.Services/Animals/AnimalService.cs:15` | The doc comment says the service persists to `auth.animals`; the table is `creatures.animals` (decision 21). Why it matters: the next reader will look in the wrong schema. | T-ANIMAL-001 → Scenario: Table lives in the creatures schema | Change the comment to `creatures.animals` |
| F-08 | Nit | API standards | `api/API.Framework/Api.Framework.Data/LoginDbContext.cs:454-455` | Two blank lines before the `Animal` entity block (a formatter would remove one). | `checklists/severity.md` → Caps (formatter points are Nit) | Remove one blank line |
| F-09 | Nit | UI standards | `ui/UI.NextJs.Framework/src/features/animals/animal-form-modal/AnimalFormModal.tsx:25-40` | Opening a deleted animal's Edit URL shows "Unable to load the form. Please try again." The scenario is met (error state, no fields), but "try again" suggests a temporary problem when the animal is actually gone; the hook's catch (`use-json-schema-entity-form.ts:199-206`) drops the API's 404 message. | T-ANIMAL-004 → Scenario: Deleted animal cannot be opened | Pass `schemaLoadErrorMessage="This animal could not be found. It may have been deleted."`, or let the hook use `getErrorMessage(error)` when the read returns 404 |
| F-10 | Nit | UI standards | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:43-44` | The confirmation's `title` and `message` are both "Delete Bessie?", so the question appears twice. | `specs/manage-animals.yaml` → actions_menu → Delete Animal (confirmation "Delete &lt;Name&gt;?") | Keep `message` as `Delete ${name}?` (the spec text) and drop `title` (it is optional in `ConfirmModal`), or use a neutral title such as "Delete Animal" |
| F-11 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/json-schema-form/components/JsonSchemaForm.tsx:11-16` | The new doc comment about schema-driven validation (:11-15) sits above the type alias instead of the component or prop it describes, and the next comment has a typo ("dditionalErrors"). | General practice (comments) | Move the :11-15 block onto `JsonSchemaFormValidation` / the `validation` prop and fix the typo to "additionalErrors" |
| F-12 | Nit | UI standards | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGrid.module.css:111-113` | `.switchCell` isn't used anywhere (the switch cells come from `grid-cell-renderers.tsx`). | Next.js `.cursor/rules/style/nextjs-css.mdc` → CSS modules | Remove the class, or use it in `renderBooleanSwitchCell` |

## Spec conformance (per control)

Spec: `specs/add-edit-animal.yaml` — Basic Form — Add \| Edit Animal (rendered as "Add Animal" / "Edit Animal" by mode, `AnimalFormModal.tsx:53`)

| Section / step | Control | Control type | Mandatory | Editable | Enablement | Min / max | Validation message | Status | Notes / finding |
|----------------|---------|--------------|-----------|----------|------------|-----------|--------------------|--------|-----------------|
| Animal Details | Name | Keyed Input → text `Input` (`unity-json-form-renderers.tsx:34-61`, `animal.ui-schema.json:12-17`) | Yes ✓ server (`animalSchema.json:4,10`) / ✗ UI marker | Yes ✓ | Always ✓ | 1–100 → `minLength 1`, `maxLength 100`, `pattern \S`, input restricted to 100 ✓ | "Name is required" ✓ (`animalSchema.json:15-17`); "An animal with this name already exists" ✓ (`AnimalService.cs:69-71`) | Mismatch | F-01 (required marker). Trim before validate / save ✓ (`AnimalService.cs:166-177`); unique ignoring case among non-deleted ✓ |
| Animal Details | Date Born | Date Picker → native date `Input` (`unity-json-form-renderers.tsx:41-46`) | Yes ✓ server (`animalSchema.json:4,25`) / ✗ UI marker | Yes ✓ | Always ✓ | N/A ✓ | "Date Born is required" ✓; "Date Born must be before today" ✓ (`animalSchema.json:35-36`) | Mismatch | F-01. UI checks the browser's local date (`unity-schema-validation.ts:100-105`), API the UTC date (`DateCompareValidator`) ✓ |
| Animal Details | Attributes | Tag Input → `UnityTagInputControl` (`unity-json-form-renderers.tsx:276-343`) | No ✓ | Yes ✓ | Always ✓ | 0–50 per tag, max 20 → items `maxLength 50`, `maxItems 20` ✓ (`animalSchema.json:39-53`) | "Each attribute tag must be 50 characters or fewer" ✓; "A maximum of 20 attributes is allowed" ✓ | Match | Starts empty on Add ✓ (`unity-schema.adapter.ts:125-127`); any characters ✓ |
| Characteristics | Is Furry | Switch → `UnitySwitchControl` + design-system `Switch` (`unity-json-form-renderers.tsx:253-272`) | No ✓ | Yes ✓ | Always ✓ | N/A ✓ | none in spec ✓ | Match | Default Off ✓ (`animalSchema.json:59`, adapter :131-133). Dark-mode colour → F-06 |
| Characteristics | Has Hooves | Switch → `UnitySwitchControl` | No ✓ | Yes ✓ | Always ✓ | N/A ✓ | none in spec ✓ | Match | Default Off ✓ (`animalSchema.json:65`) |
| (form) | Section titles | "Animal Details", "Characteristics" → `Group` labels (`animal.ui-schema.json:6,34`) | — | — | — | — | — | Match | |
| (form) | Save / Cancel | Buttons (`AnimalFormModal.tsx:77-91`) | — | — | Save disabled while loading / saving ✓ | — | Field errors on controls; record-level errors in the modal ✓ | Match | Conditional visibility: Add and Edit only, no View mode ✓; without permission no form ✓ (`AnimalsModalRoutes.tsx:28-29`) |

Manage list: `specs/manage-animals.yaml` — Modal — Manage Animals ("Animal catalogue")

| Column / action | Population source / action on click | Display format / sortable | Status | Notes / finding |
|-----------------|-------------------------------------|---------------------------|--------|-----------------|
| (page) Title / sub-text | "Manage Animals" / "Animal catalogue" | — | Mismatch | Title ✓ (`ManageAnimalsModal.tsx:27`); sub-text missing from the modal → F-04 |
| + Add Animal | Open Add \| Edit Animal in Add mode (`use-animals-grid.tsx:72-80`) | Primary action / — | Match | Shown only with `animals_write` ✓ |
| Name | `Animal.Name` (`animals-grid-columns.tsx:14-19`) | Char / Yes, default ascending ✓ (`use-animals-grid.tsx:47`, `AnimalService.cs:249-250`) | Match | |
| Is Furry | `Animal.IsFurry` (`animals-grid-columns.tsx:20-25`) | Switch (read-only) / Yes ✓ | Match | |
| Has Hooves | `Animal.HasHooves` (`animals-grid-columns.tsx:26-32`) | Switch (read-only) / Yes ✓ | Match | |
| Date Born | `Animal.DateBorn` (`animals-grid-columns.tsx:33-38`) | DD/MM/YYYY ✓ (`grid-cell-renderers.tsx:19`) / Yes ✓ | Match | |
| Attributes | `Animal.Attributes` (`animals-grid-columns.tsx:39-44`) | Comma-separated, empty array → empty cell ✓ (`grid-cell-renderers.tsx:12`) / No ✓ | Match | |
| Last Amended | `Animal.UpdatedUtc` & `UpdatedBy` → `User.DisplayName`, fallback `User.Email` (`AnimalService.cs:214-228`; `animals-grid-columns.tsx:45-55`) | "DD/MM/YYYY HH:MM Display name", browser local time ✓ (`grid-cell-renderers.tsx:25`) / Yes, by `UpdatedUtc` ✓ (`AnimalService.cs:246-247`) | Match | |
| Actions column | Last column, header "Actions", not sortable (`EntityGrid.tsx:55-60`) | — / No ✓ | Match | Row click does nothing ✓ |
| Edit Animal (icon Edit) | Open Add \| Edit Animal in Edit mode (`use-animals-grid.tsx:53-60`) | Menu item / — | Match | Escape behaviour → F-02; dark mode → F-06 |
| Delete Animal (icon Delete) | Confirmation "Delete &lt;Name&gt;?" with Cancel / Delete, soft delete, refresh (`use-animals-grid.tsx:61-70,88-104`; `ManageAnimalsModal.tsx:40-50`) | Menu item / — | Match | F-03 (button colour), F-05 (error handling), F-10 (duplicate title) |
| No-permission callout | "You do not have permission to manage animals." (`AnimalsAccessNotice.tsx:8,21-22`) | Warning `Callout` / — | Match | |

## Data mapping (per control)

| Control | Spec: Service · Table.Column | UI binding | API record / DTO | Mapper | Entity / downstream model | Migration | Status |
|---------|------------------------------|------------|------------------|--------|---------------------------|-----------|--------|
| Name | Animals · `Animal.Name` (+ derived `NormalizedName`) | `#/properties/name` | `AnimalWriteRequest.Name` → `AnimalRecord.Name` | `AnimalService.cs:166-177` (trim), `:78-79`, `:129-130` | `Animal.Name`, `Animal.NormalizedName` (`Animal.cs:7,9`) | `20261008150221_AddAnimals.cs` (`name`, `normalized_name` varchar(100)) | Mapped |
| Date Born | Animals · `Animal.DateBorn` | `#/properties/dateBorn` | `AnimalWriteRequest.DateBorn` → `AnimalRecord.DateBorn` | `AnimalService.cs:80,131`; UI `unity-schema-value.mapper.ts:90-94` (date only) | `Animal.DateBorn` (`DateOnly`, `Animal.cs:11`) | `date_born` date | Mapped |
| Attributes | Animals · `Animal.Attributes` | `#/properties/attributes` | `AnimalWriteRequest.Attributes` (`[]` when missing) | `AnimalService.cs:175,276-277`; UI `unity-schema-value.mapper.ts:22-28` (`submitEmptyArrays`) | `Animal.Attributes` (jsonb, default `'[]'`, `LoginDbContext.cs:463`) | `attributes` jsonb | Mapped |
| Is Furry | Animals · `Animal.IsFurry` | `#/properties/isFurry` | `AnimalWriteRequest.IsFurry` | `AnimalService.cs:82,133` | `Animal.IsFurry` | `is_furry` boolean default false | Mapped |
| Has Hooves | Animals · `Animal.HasHooves` | `#/properties/hasHooves` | `AnimalWriteRequest.HasHooves` | `AnimalService.cs:83,134` | `Animal.HasHooves` | `has_hooves` boolean default false | Mapped |
| Last Amended (list) | Animals · `Animal.UpdatedUtc` & `UpdatedBy` → `User.DisplayName` / `User.Email` | grid column `updatedUtc` | `AnimalModel.UpdatedUtc`, `UpdatedByName` | `AnimalService.cs:205-229` | `Animal.UpdatedUtc`, `Animal.UpdatedBy` → `User` (FK restrict, `LoginDbContext.cs:473-477`) | `updated_utc`, `updated_by` + `fk_animals_users_updated_by` (principal schema `auth`) | Mapped |
| (soft delete) | Animals · `Animal.IsDeleted` | — | — | `AnimalService.cs:160-162` | `Animal.IsDeleted` | `is_deleted` boolean default false; filtered unique index `NOT is_deleted` | Mapped |

`UpdatedUtc` / `UpdatedBy` are set from `TimeProvider` and the JWT `sub` claim on create, update and soft delete (`AnimalService.cs:86-87,135-136,161-162`).

Columns or properties in the reviewed code that are not in any linked spec:

- none. `Id`, `CreatedUtc`, `NormalizedName` and `IsDeleted` are specified by T-ANIMAL-001 (table design), not by a control.

## Acceptance criteria coverage (per scenario)

There is no automated test project in API.Framework (by rule) and no test runner in UI.NextJs.Framework, so no scenario can be **Covered**. Scenarios whose code I traced and found correct are marked **Partial** with "code ✓"; see **Tests** for why this is a note and not a set of findings.

| Scenario ID | Scenario | Status | Code reference(s) | Test reference(s) | Notes |
|-------------|----------|--------|-------------------|-------------------|-------|
| T-ANIMAL-001/S1 | Animal table stores all mapped columns | Partial | `Animal.cs:3-28`; `LoginDbContext.cs:456-478`; `20261008150221_AddAnimals.cs:19-46` | none | code ✓ (snake_case columns, `creatures.animals`) |
| T-ANIMAL-001/S2 | Attributes default to an empty array | Partial | `LoginDbContext.cs:463`; `Animal.cs:13` | none | code ✓ |
| T-ANIMAL-001/S3 | Normalised name is unique among non-deleted rows | Partial | `LoginDbContext.cs:468-471`; `20261008150221_AddAnimals.cs:64-70` | none | code ✓ (filtered unique index `NOT is_deleted`) |
| T-ANIMAL-001/S4 | A soft-deleted animal's name can be reused | Partial | `LoginDbContext.cs:468-471` | none | code ✓ |
| T-ANIMAL-001/S5 | Soft-deleted flag exists | Partial | `Animal.cs:19`; `LoginDbContext.cs:466` | none | code ✓ |
| T-ANIMAL-001/S6 | Table lives in the creatures schema | Partial | `LoginDbContext.cs:12,458`; `20261008150221_AddAnimals.cs:16-20` | none | code ✓; F-07 (stale comment) |
| T-ANIMAL-001/S7 | The animals permission is seeded for our users | Partial | `LoginPermissions.cs:36`; `LoginDbContext.cs:483-504`; `20261008150221_AddAnimals.cs:48-62` | none | code ✓ (Administrators and Standard groups) |
| T-ANIMAL-002/S1 | Create animal with valid fields | Partial | `AnimalService.cs:56-100`; `AnimalController.cs:31-42` | none | code ✓ |
| T-ANIMAL-002/S2 | Missing Attributes are stored as an empty array | Partial | `AnimalService.cs:170-177,276-277` | none | code ✓ |
| T-ANIMAL-002/S3 | Duplicate name is rejected | Partial | `AnimalService.cs:69-71,92-97` | none | code ✓ (409 + exact message, also on a unique-index race) |
| T-ANIMAL-002/S4 | Name of a soft-deleted animal can be reused | Partial | `AnimalService.cs:69` | none | code ✓ |
| T-ANIMAL-002/S5 | Date Born must be before today | Partial | `animalSchema.json:26-36`; `DateCompareValidator.cs` | none | code ✓ (UTC date) |
| T-ANIMAL-002/S6 | Date Born is mandatory | Partial | `animalSchema.json:4,25,35` | none | code ✓ |
| T-ANIMAL-002/S7 | Name is mandatory | Partial | `animalSchema.json:10-17`; `AnimalService.cs:166-177,261-265` | none | code ✓ (whitespace-only name → "Name is required") |
| T-ANIMAL-002/S8 | Attribute tag limits | Partial | `animalSchema.json:39-53` | none | code ✓ |
| T-ANIMAL-002/S9 | List returns non-deleted animals with Last Amended | Partial | `AnimalService.cs:28-47,205-229` | none | code ✓ (DisplayName, fallback Email) |
| T-ANIMAL-002/S10 | Soft delete and not found afterwards | Partial | `AnimalService.cs:49-54,108-111,149-165` | none | code ✓ |
| T-ANIMAL-002/S11 | Users without animals_write are rejected on every endpoint | Partial | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` | none | code ✓ |
| T-ANIMAL-002/S12 | User-management permissions alone do not grant access to animals | Partial | `Program.cs:86-87`; `AnimalPolicies.cs:8-10` | none | code ✓ (no `DirectoryPolicies` on animal endpoints) |
| T-ANIMAL-002/S13 | AnimalsWrite guards every animal endpoint | Partial | `AnimalController.cs:17-58`; `AnimalSchemaController.cs:15` | none | code ✓ |
| T-ANIMAL-003/S1 | Open Manage Animals from the nav | Partial | `SiteNav.tsx:32-37`; `AnimalsLanding.tsx:21-29`; `app/examples/animals/@modal/(.)manage/page.tsx` | none | code ✓; F-04 (modal sub-text) |
| T-ANIMAL-003/S2 | List shows non-deleted animals | Partial | `animals-search.data-provider.ts:13`; `animals-grid-columns.tsx:13-56`; `AnimalService.cs:30` | none | code ✓ |
| T-ANIMAL-003/S3 | Last Amended shows date, time and user | Partial | `animals-grid-columns.tsx:45-55`; `grid-cell-renderers.tsx:25` | none | code ✓ |
| T-ANIMAL-003/S4 | Last Amended is shown in the browser's local time | Partial | `grid-cell-renderers.tsx:25` | none | code ✓ |
| T-ANIMAL-003/S5 | Last Amended outside summer time | Partial | `grid-cell-renderers.tsx:25` | none | code ✓ (uses the browser's own offset) |
| T-ANIMAL-003/S6 | Default sort by Name ascending | Partial | `use-animals-grid.tsx:47`; `AnimalService.cs:234-250` | none | code ✓ |
| T-ANIMAL-003/S7 | Add opens Basic Form | Partial | `use-animals-grid.tsx:72-80`; `app/examples/animals/@modal/(.)manage/item/page.tsx` | none | code ✓; F-01 |
| T-ANIMAL-003/S8 | Edit opens Basic Form with existing data | Partial | `use-animals-grid.tsx:53-60`; `use-json-schema-entity-form.ts:182-198` | none | code ✓ |
| T-ANIMAL-003/S9 | Row actions menu in the last column; row click does nothing | Partial | `EntityGrid.tsx:43-60,130-136`; `use-animals-grid.tsx:50-71` | none | code ✓; F-02, F-06 |
| T-ANIMAL-003/S10 | User without animals_write cannot open Manage Animals | Partial | `AnimalsModalRoutes.tsx:13-14,28-29`; `AnimalsAccessNotice.tsx:8,21-22`; `AnimalsLanding.tsx:31` | none | code ✓ (no `v1/Animal` request without the permission) |
| T-ANIMAL-003/S11 | User-management permissions alone do not give access to animals | Partial | `animal-permissions.ts:6-8`; `use-animals-access.ts:13`; `SiteNav.tsx:32` | none | code ✓ |
| T-ANIMAL-004/S1 | Add mode opens with defaults | Partial | `unity-schema.adapter.ts:125-136`; `animalSchema.json:59,65` | none | code ✓; F-01 (required markers missing) |
| T-ANIMAL-004/S2 | Create animal with required fields | Partial | `use-json-schema-entity-form.ts:214-256`; `unity-schema-value.mapper.ts:15-31`; `AnimalFormModal.tsx:32-35` | none | code ✓ (closes and refreshes the grid) |
| T-ANIMAL-004/S3 | Name is mandatory | Partial | `unity-schema-validation.ts:214-223`; `animalSchema.json:14-17` | none | code ✓ (message); F-01 |
| T-ANIMAL-004/S4 | Duplicate name is rejected on Save | Partial | `api-error.utils.ts:26-60`; `use-json-schema-entity-form.ts:248-252` | none | code ✓ (API message shown on Name) |
| T-ANIMAL-004/S5 | Name of a deleted animal can be reused | Partial | `AnimalService.cs:69` | none | code ✓ |
| T-ANIMAL-004/S6 | Date Born must be before today | Partial | `unity-schema-validation.ts:100-163` | none | code ✓ (browser local date) |
| T-ANIMAL-004/S7 | Date Born is mandatory | Partial | `unity-schema-validation.ts:214-223` | none | code ✓ (message); F-01 |
| T-ANIMAL-004/S8 | Attributes persist as JSON tags | Partial | `unity-schema-value.mapper.ts:22-28`; `AnimalService.cs:276-277` | none | code ✓ |
| T-ANIMAL-004/S9 | Attribute tag limits | Partial | `unity-schema-validation.ts:225-232`; `unity-json-form-renderers.tsx:335-337` | none | code ✓ |
| T-ANIMAL-004/S10 | Edit persists changed fields | Partial | `use-json-schema-entity-form.ts:229-242`; `AnimalService.cs:102-146` | none | code ✓ (Last Amended updated) |
| T-ANIMAL-004/S11 | Only Add and Edit modes exist | Partial | `animal-routes.ts:6`; `AnimalFormModal.tsx:53` | none | code ✓ (no View) |
| T-ANIMAL-004/S12 | Deleted animal cannot be opened | Partial | `AnimalService.cs:49-54`; `use-json-schema-entity-form.ts:199-206`; `AnimalFormModal.tsx:93-94` | none | code ✓; F-09 (wording) |
| T-ANIMAL-005/S1 | Confirmation names the animal | Partial | `ManageAnimalsModal.tsx:40-50` | none | code ✓; F-03, F-10 |
| T-ANIMAL-005/S2 | Soft delete removes row from the list | Partial | `use-animals-grid.tsx:88-104`; `AnimalService.cs:149-165` | none | code ✓; F-05 (failure path) |
| T-ANIMAL-005/S3 | Cancel leaves the animal unchanged | Partial | `ManageAnimalsModal.tsx:48` | none | code ✓ with the Cancel button; Escape also closes Manage Animals → F-02 |
| T-ANIMAL-005/S4 | Deleted animal is gone everywhere but its name is free | Partial | `AnimalService.cs:30,51,69,108,154` | none | code ✓ |
| T-ANIMAL-005/S5 | Users without animals_write cannot delete | Partial | `AnimalController.cs:57-58`; `use-animals-grid.tsx:65` | none | code ✓ |
| T-ANIMAL-006/S1 | Switch renders and binds a boolean | Partial | `unity-json-form-renderers.tsx:253-272`; `Switch.tsx:12-37` | none | code ✓; F-06 |
| T-ANIMAL-006/S2 | Tag Input adds and removes chips | Partial | `unity-json-form-renderers.tsx:276-343` | none | code ✓ |
| T-ANIMAL-006/S3 | Tag Input shows the schema limit errors | Partial | `unity-json-form-renderers.tsx:335-337`; `unity-schema-validation.ts:225-232` | none | code ✓ |
| T-ANIMAL-006/S4 | Read-only rendering (generic framework capability) | Partial | `unity-json-form-renderers.tsx:256-257,280-281,307,319`; `Switch.tsx:36-37` | none | code ✓ |
| T-ANIMAL-006/S5 | Grid cells | Partial | `grid-cell-renderers.tsx:7-30`; `animals-grid-columns.tsx:24,31,43` | none | code ✓ |
| T-ANIMAL-007/S1 | Row actions menu in the last column | Partial | `EntityGrid.tsx:55-60,130-136` | none | code ✓ |
| T-ANIMAL-007/S2 | Choosing an item runs it for that row | Partial | `EntityGridRowActionsMenu.tsx:74-78` | none | code ✓ |
| T-ANIMAL-007/S3 | Items are hidden without the required permission | Partial | `EntityGrid.tsx:44-49`; `permissions.ts:6-13` | none | code ✓ |
| T-ANIMAL-007/S4 | Any one of several permissions is enough | Partial | `permissions.ts:10-12` | none | code ✓ |
| T-ANIMAL-007/S5 | No Actions column when no item is allowed | Partial | `EntityGrid.tsx:55` | none | code ✓ |
| T-ANIMAL-007/S6 | Per-row visibility | Partial | `EntityGrid.tsx:51-52` | none | code ✓ |
| T-ANIMAL-007/S7 | A row with no visible items has no trigger | Partial | `EntityGridRowActionsMenu.tsx:47` | none | code ✓ |
| T-ANIMAL-007/S8 | Existing text-button grids are unaffected | Partial | `EntityGrid.tsx:130-150` | none | code ✓ (button rendering kept when `rowActionsDisplay` isn't `menu`); no pre-change copy to diff against (see notes) |
| T-ANIMAL-007/S9 | Menu closes on Escape and outside click | Partial | `EntityGridRowActionsMenu.tsx:29-45` | none | menu closes ✓, but Escape also closes Manage Animals → F-02 |

## Security and data

| Spec rule / check | Status | Reference |
|-------------------|--------|-----------|
| Every animal endpoint (list, get, create, update, delete, form schema) requires `animals_write` | Enforced server-side | `AnimalController.cs:17,24,32,45,58`; `AnimalSchemaController.cs:15`; `Program.cs:86-87` |
| User-management permissions alone give no access | Enforced server-side | `Program.cs:86-87` (policy checks only `animals_write`); UI `animal-permissions.ts:6-8` |
| Name mandatory, 1–100, trimmed | Enforced server-side (+ client) | `animalSchema.json:6-18`; `AnimalService.cs:166-177` |
| Name unique (case-insensitive, non-deleted) | Enforced server-side (service check + filtered unique index) | `AnimalService.cs:69-71,92-97,121-126,140-143`; `LoginDbContext.cs:468-471` |
| Date Born mandatory and before today | Enforced server-side (UTC) + client (local date) | `animalSchema.json:20-37`; `unity-schema-validation.ts:100-163` |
| Attributes ≤ 50 characters per tag, ≤ 20 tags | Enforced server-side (+ client) | `animalSchema.json:39-53` |
| Soft delete only; deleted rows never listed or opened | Enforced server-side | `AnimalService.cs:30,51,108,154-162` |
| Audit `UpdatedUtc` / `UpdatedBy` from the token, not the client | Enforced server-side | `AnimalController.cs` (`sub` claim); `AnimalService.cs:86-87,135-136,161-162` |
| Injection | No raw SQL; LINQ only | `AnimalService.cs` |
| Secrets / tokens | None seen in reviewed code; `.env.local` not opened; "committed" can't be checked without git | — |
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
| UI scenarios T-ANIMAL-003, -004, -005, -006, -007 | none | Untested |

**Why these are not findings.** `review-tests` would normally raise a Major for an untested mandatory, uniqueness or persistence rule. API.Framework has no test project, and its own rule (`api/API.Framework/.cursor/rules/api-framework-testing.mdc`) says not to create one "unless Neil asks"; UI.NextJs.Framework has no test runner. The implementing agent could not add tests without breaking that rule, so I've treated this the way the skill treats a UI codebase with no runner: a tooling gap for the human owner (Neil) to decide on, recorded here and in the notes, not a defect in this change. The hand-off records throwaway checks run outside both repos (API 20/20, UI 14/14), which matches the rule's "throwaway … checks are fine … do not commit them". If Neil approves a test project, these are the first tests I'd suggest.

Suggested tests (for when a test project is approved):

- `Create_NameBlankAfterTrim_ReturnsNameIsRequired` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — arrange a request with Name "   "; act `CreateAsync`; assert 400 and `validationErrors` name = "Name is required".
- `Create_DuplicateNameDifferentCase_ReturnsConflict` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — seed "Bessie"; create "  bessie "; assert 409 and "An animal with this name already exists".
- `Create_NameOfSoftDeletedAnimal_Succeeds` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — seed deleted "Bessie"; create "Bessie"; assert 201.
- `Create_DateBornToday_ReturnsBeforeTodayMessage` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — fake `TimeProvider`; DateBorn = today (UTC); assert 400 "Date Born must be before today".
- `Create_AttributesMissing_StoresEmptyArray` in `Api.Framework.Tests/Animals/AnimalServiceTests.cs` — omit Attributes; assert stored `[]` and model `Attributes` empty.
- `Create_TwentyOneAttributes_ReturnsMaximumMessage` and `Create_AttributeOver50Chars_ReturnsLengthMessage` in the same class — assert the exact spec messages.
- `Delete_ExistingAnimal_SetsIsDeletedAndAudit` then `Get_DeletedAnimal_ReturnsNotFound` — assert `IsDeleted`, `UpdatedUtc` / `UpdatedBy`, then 404 "The animal was not found.".
- `List_ExcludesDeleted_SortsByNameAndFallsBackToEmail` — seed users with and without DisplayName; assert order and `UpdatedByName`.
- `AnimalEndpoints_WithoutAnimalsWrite_Return403` — policy test per action (list, get, create, update, delete, schema) with a principal holding only `user_management_write`.
- UI (if a runner such as Vitest is added): `validateUnitySchemaData` cases for blank / whitespace Name, today's date in local time, 21 tags and a 51-character tag; `hasAnyPermission` any-of cases; `EntityGridRowActionsMenu` Escape not reaching the modal (F-02).

Checks run: none by the reviewer (read-only review; no build, lint or tests run). The hand-off records `dotnet build` and `npm run build` passing, lint not run (no ESLint configuration), and the throwaway checks above.

## Changes since last review

Iteration 1: n/a.

## Out of scope / pre-existing notes

These do not affect the verdict.

- **Config for the human owner:** `development.ui.options.nextjs.rules` is `null`, but UI.NextJs.Framework now has `AGENTS.md` and `.cursor/rules/` (framework/, style/, implementation/, created 15:55–15:58 today) and its `README.md` points to them. I applied them via the README (and the Minor caps would be the same as General practice). Recommend updating the config so the next review uses them directly, and updating `checklists/ui-nextjs-checklist.md`, which still says the codebase has no rules.
- **Tests:** API.Framework has no test project by rule and UI.NextJs.Framework has no test runner; whether to add them is Neil's call (see **Tests**).
- **No git:** neither repo is under git, so there is no commit to pin and "secret committed" can't be checked. I also couldn't diff the shared framework files against their pre-change versions (the earlier full backup of the framework folder is no longer on disk), so "existing forms and grids unaffected" (T-ANIMAL-006, T-ANIMAL-007/S8) was checked by reading the code paths, not by diff.
- **Pre-existing:** `Modal.tsx:62-69` closes every open modal on Escape (stacked modals all react); it predates this plan and also affects reference data. F-02 covers the part this feature exposes.
- **Pre-existing:** `JsonSchemaForm.module.css:43,59,66` already used undefined `--color-*` variables before this change; worth tidying with F-06.
- **Pre-existing:** `DateCompareValidator` uses `DateTime.UtcNow` rather than `TimeProvider`, so date rules can't be tested with a fake clock.
- **Spec / planning note:** the Standard group's seeded description (`LoginDbContext.cs:158`) still says "Can view users and groups." although decision 25 now gives that group `animals_write`. Changing seed text needs a migration, so I've left it for the planning agent to decide.
- **Docs outside the manifest:** the Next.js `README.md` still describes `Unity.UI.Next` / `cp .env.example .env.local` setup, and the design-system `README.md:17` lists a `Visibility` icon that `Icon.tsx` no longer has (that README and `DesignSystemShowcase.tsx` were edited outside this manifest).
- **Rule files edited after the hand-off:** API.Framework `CLAUDE.md`, `AGENTS.md` and `.cursor/rules` changed at about 16:10, after the 16:09 hand-off; the `.cursor` and `.claude` copies are identical. Not part of this review.
- **Migration:** `Down` drops `creatures.animals` but leaves the empty `creatures` schema (EF's default); fine, noted for awareness. EF will log a warning that the `bool` defaults are database-generated; harmless here because the database default is also `false`.
- **Not assessed live:** no database run, no browser click-through (dark mode, Escape and focus behaviour were assessed from the code).

---

<sub>Generated by ai-review-framework using `loops/pr-review.md`. Publishing: Not applicable — direct hand-off. Logged in `reviews/review-log.md` (round 1).</sub>
