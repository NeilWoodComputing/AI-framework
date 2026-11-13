# Review log: manage-animals

Append-only history of every review round for this feature, whichever route was used: a direct hand-off from the implementing agent or a pull request. The reviewing agent appends one **Round** block per review, at loop stage 10 of `loops/pr-review.md`, with no human request needed.

- Feature: `ai-planning-framework/work/manage-animals/`
- Pipeline state: `handoff.md`
- Full reports, one per round: `reviews/DIRECT-<branch-slug>-<n>-review.md` or `reviews/DIRECT-<feature>-<n>-review.md` with no branch (direct route) · `reviews/PR-<id>-review.md` (PR route, overwritten on each PR update)

Rules:

- Append only. Newest round at the bottom. Never edit or delete an earlier round; a correction goes in a new round's **Notes**.
- **Direct route:** the **Comments** table is required, with one row per finding, matching the full report.
- **PR route:** the round block plus **Summary** is required. The comments are in the full report (and on the PR only when publishing is on, which needs provider `azure-devops`), so the **Comments** table is optional.
- Dates in Europe/London. No tokens, connection strings or personal data from fixtures.
- Copy this file to `<work_dir>/<feature>/reviews/review-log.md` (`review.log_file`) the first time a feature is reviewed. Keep this header and drop the template block below.

---

## Round 1 — 08/10/2026 16:34 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: 75 manifest + 0 discovered files, 0 not implemented |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007 |
| Verdict | **Request changes** |
| Findings | Blocker 0 · Major 1 · Minor 5 · Nit 6 |
| Full report | `reviews/DIRECT-manage-animals-1-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | implementing agent, Dev Bot (changes-requested) |

### Summary

Manage Animals (API, migration, Next.js grid, form and shared Switch / Tag Input / row actions menu) was reviewed whole against `specs/manage-animals.yaml`, `specs/add-edit-animal.yaml`, all 62 scenarios in T-ANIMAL-001 to 007, the API.Framework rules and the Next.js rules referenced from its README. Data mapping, server-side validation, uniqueness, soft delete and the `AnimalsWrite` policy are all correct. Request changes because the mandatory Name and Date Born fields aren't marked as required in the UI (F-01, Major); the Minor and Nit items can go in the same pass.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-01 | `ui/UI.NextJs.Framework/src/framework/json-schema-form/components/renderers/unity-json-form-renderers.tsx:34-61` | Major | Name and Date Born are mandatory in the spec and in the server schema (`animalSchema.json:4`), but the form never shows them as required. `UnityTextControl` renders `Input` without `requiredField`, so neither label gets the required marker. Why it matters: people can't tell which fields they must fill in until Save fails, and the spec checklist treats "mandatory" as both server-enforced **and** visible in the UI. (`specs/add-edit-animal.yaml` → Animal Details → Name / Date Born (`mandatory: "Yes"`); `checklists/full-stack-checklist.md` → **Mandatory** ("in the server schema `required` and shown as required in the UI"); T-ANIMAL-004 checklist "UI behaviour matches the Excel control rows (… mandatory …)"; Next.js `.cursor/rules/style/nextjs-design-system.mdc` → Form controls (`Input` takes `requiredField`)) | Take `required` from `ControlProps` (JSON Forms sets it from the schema's root `required` array, which `toJsonFormsSchema` keeps) and pass `requiredField={required}` to `Input` at :48-60. For consistency, pass `requiredField={required}` to `FormFieldLabel` in the other label-rendering controls (:75, :146, :302). This also adds the marker to required fields on existing reference-data forms, which is the correct behaviour |
| F-02 | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGridRowActionsMenu.tsx:35-36` | Minor | Pressing Escape with a row's actions menu open closes the menu **and** the whole Manage Animals modal. The menu listens on `document`, and `Modal` (`src/framework/design-system/components/modal/Modal.tsx:62-69`) closes on any Escape it sees on `window`, so the same key press reaches both. The same happens on the "Delete &lt;Name&gt;?" confirmation: Escape cancels it and also closes Manage Animals, so the row is no longer "visible on Manage Animals". Why it matters: Escape should only dismiss the top-most thing, and losing the list is surprising. (T-ANIMAL-007 → Scenario: Menu closes on Escape and outside click; T-ANIMAL-005 → Scenario: Cancel leaves the animal unchanged; `checklists/ui-nextjs-checklist.md` B → Accessibility ("focus managed when modals open and close") — General practice) | In the menu's `handleKey`, call `event.stopPropagation()` before `setOpen(false)` (the `document` listener runs before `Modal`'s `window` listener, so this is enough), and return focus to the trigger. For stacked modals, make `Modal` act only when it is the top-most open modal (for example a small module-level stack in `Modal.tsx`), which fixes the confirm and the Add \| Edit Animal form over the grid in one place |
| F-03 | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:41-50` | Minor | The Delete button on the "Delete &lt;Name&gt;?" confirmation uses the normal primary style, because `ConfirmModal` always renders its confirm button with `theme="primary-action"` (`ConfirmModal.tsx:49`). Why it matters: a red destructive button is the visual cue that this action removes something. (Next.js `.cursor/rules/style/nextjs-design-system.mdc` → Buttons ("Destructive confirm actions use `theme=\"system-red\"`")) | Add an optional `confirmTheme?: ButtonTheme` prop to `ConfirmModal` (default `primary-action`, so existing callers don't change) and pass `confirmTheme="system-red"` here |
| F-04 | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:25-32` | Minor | The spec's page sub-text "Animal catalogue" doesn't appear in the Manage Animals modal; it is only on the Animals page header behind it (`app/examples/animals/page.tsx`). `ModalShell` already supports a `subtitle`, but `RoutedModal` (`RoutedModal.tsx:11-24`) doesn't pass one through. Why it matters: the modal header should match the spec's title and sub-text pair. (`specs/manage-animals.yaml` → `page_title: Manage Animals`, `page_sub_text: "Animal catalogue"`) | Add `subtitle?: ReactNode` to `RoutedModalProps` and forward it to `ModalShell`, then pass `subtitle="Animal catalogue"` from `ManageAnimalsModal` |
| F-05 | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/use-animals-grid.tsx:88-104` | Minor | If the delete call fails: (1) the message is the technical "Delete failed: 404" rather than the API's text ("The animal was not found."); (2) the confirm stays open and the error `Callout` (`ManageAnimalsModal.tsx:33`) renders behind it, so the user sees nothing happen; (3) nothing stops a second click while the first DELETE is in flight (`deleteInFlight` is tracked but not used), which turns a successful delete into a confusing 404 error. Why it matters: errors should reach the user in plain words, and destructive actions shouldn't double-fire. (`checklists/ui-nextjs-checklist.md` B → "Loading, empty and error states handled for each data call; errors shown to the user without leaking internals" — General practice; Next.js `.cursor/rules/framework/nextjs-json-schema-forms.mdc` → "Extend `AbstractEntityDataProvider` … Persist goes through the provider") | Call `AnimalEntityDataProvider.deleteById(id)` (it already throws `ApiRequestError` with the body), show `getErrorMessage(error, 'The animal could not be deleted.')`, close the confirm on failure (or show the error inside it), and return early from `confirmDelete` when `deleteInFlight` is true (and disable / show loading on the Delete button if `ConfirmModal` gains a `loading` prop) |
| F-06 | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGrid.module.css:80-102` | Minor | The new row actions menu, Switch and tag chips use `--color-surface`, `--color-border` and `--color-surface-alt`, which aren't defined anywhere (`tokens.css` defines `--app-*` tokens), so the hard-coded fallbacks always apply. In dark mode the menu is white (`#fff`) while its text inherits the dark-mode text colour (`#e8eaed`), so the items are almost unreadable; tag chips (`JsonSchemaForm.module.css:96`) have the same problem, and the Switch track uses `#c8c8c8` (`Switch.module.css:19`). Why it matters: the theme toggle is a framework feature and these components should follow it. (Next.js `.cursor/rules/style/nextjs-css.mdc` → Token sources (priority) ("Semantic CSS variables from `tokens.css`"; "Never introduce a new hardcoded hex when an existing token fits") and → Dark mode) | Use the existing tokens: menu `background: var(--app-surface-raised)`, `border: 1px solid var(--app-grid-border)`, hover / focus `var(--app-grid-row-hover-bg)`; tag chip `var(--app-grid-row-hover-bg)` (or a new semantic token in `tokens.css` with a dark value); Switch track `var(--app-input-border)`; group border (`JsonSchemaForm.module.css:70`) `var(--app-grid-border)` |
| F-07 | `api/API.Framework/Api.Framework.Services/Animals/AnimalService.cs:15` | Nit | The doc comment says the service persists to `auth.animals`; the table is `creatures.animals` (decision 21). Why it matters: the next reader will look in the wrong schema. (T-ANIMAL-001 → Scenario: Table lives in the creatures schema) | Change the comment to `creatures.animals` |
| F-08 | `api/API.Framework/Api.Framework.Data/LoginDbContext.cs:454-455` | Nit | Two blank lines before the `Animal` entity block (a formatter would remove one). (`checklists/severity.md` → Caps (formatter points are Nit)) | Remove one blank line |
| F-09 | `ui/UI.NextJs.Framework/src/features/animals/animal-form-modal/AnimalFormModal.tsx:25-40` | Nit | Opening a deleted animal's Edit URL shows "Unable to load the form. Please try again." The scenario is met (error state, no fields), but "try again" suggests a temporary problem when the animal is actually gone; the hook's catch (`use-json-schema-entity-form.ts:199-206`) drops the API's 404 message. (T-ANIMAL-004 → Scenario: Deleted animal cannot be opened) | Pass `schemaLoadErrorMessage="This animal could not be found. It may have been deleted."`, or let the hook use `getErrorMessage(error)` when the read returns 404 |
| F-10 | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:43-44` | Nit | The confirmation's `title` and `message` are both "Delete Bessie?", so the question appears twice. (`specs/manage-animals.yaml` → actions_menu → Delete Animal (confirmation "Delete &lt;Name&gt;?")) | Keep `message` as `Delete ${name}?` (the spec text) and drop `title` (it is optional in `ConfirmModal`), or use a neutral title such as "Delete Animal" |
| F-11 | `ui/UI.NextJs.Framework/src/framework/json-schema-form/components/JsonSchemaForm.tsx:11-16` | Nit | The new doc comment about schema-driven validation (:11-15) sits above the type alias instead of the component or prop it describes, and the next comment has a typo ("dditionalErrors"). (General practice (comments)) | Move the :11-15 block onto `JsonSchemaFormValidation` / the `validation` prop and fix the typo to "additionalErrors" |
| F-12 | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGrid.module.css:111-113` | Nit | `.switchCell` isn't used anywhere (the switch cells come from `grid-cell-renderers.tsx`). (Next.js `.cursor/rules/style/nextjs-css.mdc` → CSS modules) | Remove the class, or use it in `renderBooleanSwitchCell` |

### Changes since last round

First review.

### Notes

- Tests: API.Framework has no test project (its `api-framework-testing.mdc` rule forbids adding one unless Neil asks) and UI.NextJs.Framework has no test runner, so untested scenarios are recorded as a tooling gap for Neil, not as findings. Suggested tests are in the full report.
- Config: `development.ui.options.nextjs.rules` is `null` although UI.NextJs.Framework now has `.cursor/rules/`; the review applied them via the README. Recommend updating the config and `checklists/ui-nextjs-checklist.md`.
- Planning: the Standard group's seeded description (`LoginDbContext.cs:158`) is out of date after decision 25.
- Not assessed live: no database run or browser click-through; neither repo is under git.

## Round 2 — 08/10/2026 17:05 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: 79 manifest + 0 discovered files, 0 not implemented |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007 |
| Verdict | **Approve** |
| Findings | Blocker 0 · Major 0 · Minor 0 · Nit 4 |
| Full report | `reviews/DIRECT-manage-animals-2-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | human owner, Neil Wood (approved, ready to merge) |

### Summary

Re-review of Dev Bot's round 1 fixes. All 79 manifest files were reviewed whole again (now including `Modal.tsx`, `ConfirmModal.tsx`, `RoutedModal.tsx` and `tokens.css`) against both specs, all 62 scenarios in T-ANIMAL-001 to 007, the API.Framework rules and skills, and the Next.js `AGENTS.md`, `README.md` and `.cursor/rules` (now named in the config), using the updated `checklists/ui-nextjs-checklist.md`. All 12 round 1 findings are resolved and there are no regressions, including for the reference-data screens that share the changed renderers and modals. The four new findings are Nits, so the verdict is Approve and the feature goes to Neil to merge.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-13 | `api/API.Framework/Api.Framework/Controllers/V1/Animals/AnimalController.cs:28` | Nit | GET by id returns a bare `NotFound()` with no `message`, while PUT and DELETE return "The animal was not found.". So a deleted animal's Edit URL shows the generic "This record could not be found. It may have been deleted." rather than the API text the hand-off describes. T-ANIMAL-004/S12 is still met. (`api-framework-ui-contract.mdc` → "Preferred failure body (Animals)"; `CatalogueItemController.cs:60` uses the same bare pattern) | `return item is null ? NotFound(Missing("The animal was not found.")) : Ok(item);` |
| F-14 | `ui/UI.NextJs.Framework/src/framework/design-system/forms/switch/Switch.tsx:43`, `Switch.module.css:49` | Nit | Neither new Switch file has a final newline. They are the only UI files without one. (Next.js `.cursor/rules/style/nextjs-formatting.mdc` → Final newline: yes; formatter point) | Add a trailing newline |
| F-15 | `api/API.Framework/Api.Framework.Data/Models/Animal.cs:28` (+ `AnimalRecord.cs`, `AnimalJsonSchemaBuilder.cs`, `AnimalContracts.cs`, `IAnimalService.cs`, `AnimalService.cs:313`, `AnimalController.cs:75`, `AnimalSchemaController.cs`, `animalSchema.json`) | Nit | These nine new animal files have no final newline. Every other API.Framework source file has one. This was missed in round 1. (General practice: consistency; no API formatting rule) | Add a trailing newline to each |
| F-16 | `ui/UI.NextJs.Framework/src/features/animals/manage-animals-modal/ManageAnimalsModal.tsx:42-52` | Nit | The delete `ConfirmModal` stacks over Manage Animals but keeps `level="primary"`, so it is on top only because it comes later in the DOM. (Next.js `.cursor/rules/framework/nextjs-modal-routing.mdc` → "`size` / `level` — match stacking") | Pass `level="secondary"` |

### Changes since last round

Resolved: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12. Still open: none. New: F-13, F-14, F-15, F-16 (all Nit).

### Notes

- F-07: the round 1 copy (read at 16:12) did say `auth.animals`. `AnimalService.cs` was changed at 16:24:36, before Dev Bot's pickup at 16:43, so the comment was already correct when Dev Bot looked. Resolved either way.
- F-09: resolved by the new 404 handling in `use-json-schema-entity-form.ts`. The exact wording differs from the hand-off note (see F-13).
- Tests: still no test project in API.Framework (rule `api-framework-testing.mdc`) and no test runner in UI.NextJs.Framework. This is recorded as a tooling decision for Neil, not as findings, and is the same treatment as round 1. Suggested tests are in the full report.
- Config: this round applied the Next.js rules named in `development.ui.options.nextjs.rules` and the `checklists/ui-nextjs-checklist.md` rewritten at 16:56 today. This closes round 1's config note.
- Planning (carried forward): the Standard group's seeded description (`LoginDbContext.cs:158`) is out of date after decision 25.
- Not assessed live: no database run, browser click-through, build or lint by the reviewer. Neither repo is under git.

## Round 3 — 08/10/2026 19:08 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: 82 manifest + 5 discovered files, 0 not implemented; live browser check |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-008 |
| Verdict | **Approve with comments** |
| Findings | Blocker 0 · Major 0 · Minor 4 · Nit 7 (open; includes F-13 to F-15 from round 2) |
| Full report | `reviews/DIRECT-manage-animals-3-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | human owner, Neil Wood (approved with comments; review cap of 3 reached) |

### Summary

Final round (3 of 3). It re-reviewed the list-on-page change (decision 27), the portalled `DropdownMenu` row menu and the auth normalisation against both specs, all 67 scenarios in T-ANIMAL-001 to 008 (decision 28 split; Q37 accepted at 19:00, so T-ANIMAL-003 S12 / S13 are final) and the new `nextjs-list-pages.mdc` rule, which the Animals page meets. This round included a live browser check as the Development default user:
- nav and route, required markers and validation, create, edit, duplicate name, delete, Escape stacking, the deleted-record URL, the direct form URL and simulated no-permission all behaved as specified;
- the row actions menu was fully visible in light and dark mode, at 1024×600, and when flipped above the trigger.

Round 2 missed that the menu was clipped, because it was judged from the code alone. That miss is logged as F-17 (Major); it was already fixed at 18:40. Four Minor findings: dark-mode button contrast, dark-mode tag-chip "×", five files missing from the manifest, and `DropdownMenu` not in the showcase. With no Blocker or Major open, the verdict is Approve with comments, and it goes to Neil.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-17 | `ui/UI.NextJs.Framework/src/framework/entity-framework/components/entity-grid/EntityGrid.module.css:5,20` (old menu inside `.grid` / `.tableWrap`) | Major (resolved before this round) | Round 2 miss: the row actions menu was clipped to a thin sliver by `overflow: hidden` / `overflow-x: auto`. Neil's live check at about 18:06 found it. Fixed at 18:40 by the portalled `DropdownMenu`, and verified live this round | None (resolved) |
| F-18 | `ui/UI.NextJs.Framework/src/framework/design-system/components/menu/DropdownMenu.tsx:1` (+ `DropdownMenu.module.css`, `components/modal/use-modal-navigate.ts`, `json-schema-form/services/json-schema-data.service.ts`, `api/unity-api-fetch.ts`) | Minor | Manifest incomplete: five files the feature now depends on aren't in `implementation.ui` | Add them to the manifest |
| F-19 | `handoff.md` → `implementation` | Nit | The manifest still cites the old T-ANIMAL-003 S1 / S10 / S11 and has no T-ANIMAL-008. Read as T-ANIMAL-008 S1–S3 per decision 28 | Re-point on the next manifest update |
| F-20 | `ui/UI.NextJs.Framework/src/features/design-system-showcase/DesignSystemShowcase.tsx:1` | Minor | `DropdownMenu` is user-visible but has no showcase section (`style/nextjs-design-system.mdc:152-153`) | Add a showcase section |
| F-21 | `ui/UI.NextJs.Framework/src/framework/design-system/theme/tokens.css:21-23,43` | Minor | Dark mode: the secondary buttons (white fill, pale-blue text), the primary buttons and the modal close (white on `#6aa3c9`) all measure 2.73:1 live (`style/nextjs-css.mdc` → Dark mode; WCAG 1.4.3). The tokens predate the plan but show on every Animals screen | Dark values for the secondary action tokens and a dark foreground for primary fills |
| F-22 | `ui/UI.NextJs.Framework/src/framework/json-schema-form/components/JsonSchemaForm.module.css:111`; `tokens.css:20` | Minor | Dark mode: the tag-chip "×" (`--app-form-error-text`, which has no dark value) measures 1.69:1 live; field errors would be about 2.09:1 by calculation | A dark `--app-form-error-text` ≥ 4.5:1, or a neutral colour for the chip "×" |
| F-23 | `ui/UI.NextJs.Framework/src/framework/auth/normalize-auth-state.ts:1` (+ `authorisation.data-provider.ts`, `token-refresh.service.ts`, `api/unity-api-fetch.ts`) | Nit | UTF-8 BOM and mixed line endings in the four files changed at 18:02–18:03 | Re-save without BOM, consistent EOL |
| F-24 | `ui/UI.NextJs.Framework/src/framework/json-schema-form/services/json-schema-data.service.ts:18,27-29` | Nit | The schema cache comment says it clears on sign-out, but manual Sign out doesn't dispatch `unity-auth-cleared`. No data impact | Dispatch the event in `signOut()` or reword the comment |
| F-25 | `ui/UI.NextJs.Framework/src/framework/entity-framework/grid/grid-cell-renderers.tsx:6-8`; `Switch.tsx:36-37`; `Switch.module.css:9-12` | Nit | The read-only grid switches work as specified (clicks do nothing, no request), but look almost identical to editable ones (opacity 0.7 only). Whether to change the display is a spec question for Neil | Stronger read-only styling or a tooltip |

F-13, F-14 and F-15 (Nit) from round 2 are unchanged and still open.

### Changes since last round

Resolved: F-16 (the confirm now sits directly over the page, so `level` primary is correct) and F-17 (fixed before this round). Still open: F-13, F-14, F-15 (Nit). New: F-18, F-20, F-21, F-22 (Minor); F-19, F-23, F-24, F-25 (Nit).

### Notes

- **Live check:** UI http://localhost:3003 and API.Framework 5088 / 7088, both already running.
  - Credentials were passed by env var to a child process only and never printed or stored.
  - I touched only "ZZ Test Animal 202610081756", which was deleted through the UI and confirmed gone.
  - Screenshots are on the box in `/workspace/manage-animals-check/round3/`.
- **List reloads:** 2 requests on first load (React StrictMode in dev) and exactly 1 after each create, edit and delete. Neil's 2–3 reloads on the old modal version are gone.
- **Hand-off edits during review:** Plan Bot edited `handoff.md` while it was in review (decision 28 at 18:56, Q37 at 19:01). Planning content only.
- **Tests:** still a tooling decision for Neil, as in rounds 1 and 2.
- **Out of scope:** reference data's items list modal (predates the list-pages rule), paginator icon contrast and the dev-only seeded password in `DefaultUserSeeder.cs`.
- **Not assessed:** production build, build / lint / automated tests by the reviewer. Neither repo is under git.

## Decision 29 cycle 1 — code review — 08/10/2026 19:45 (Europe/London)

A fresh review cycle for Decision 29 (T-ANIMAL-009). This is cycle 1, not round 4 of the earlier cap; `review.cycle` goes 0 → 1.

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff (Dev Bot, 19:20:33; History row 29) |
| Branch / PR | no branch (direct) |
| Scope | plan: 91 manifest + 0 discovered files, 0 not implemented; live browser check |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005, T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-008, T-ANIMAL-009 |
| Verdict | **Tests blocked — Approve with comments** (code: Approve with comments; test review: blocked-noted; final: Approve with comments under `testing.blocked_tests_allow_approval: true`, a flagged default) |
| Findings | Blocker 0 · Major 0 · Minor 1 · Nit 5 (open; includes F-19 from round 3) |
| Full report | `reviews/DIRECT-manage-animals-d29-1-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | human owner, Neil Wood (approved with comments, **Tests blocked**; Neil decides at merge) |

### Summary

Reviewed T-ANIMAL-009 (`renderBooleanIconCell`, `Icon` `Check` / `Close`, Animals Is Furry / Has Hooves switched over) and the round 3 fixes against both specs and all 75 frozen scenarios (T-ANIMAL-001 to 009).

Live check, light and dark, with two rows of my own (all-true / all-false):
- tick and cross render, named "Yes" / "No" in Chromium;
- 0 switches in the grid;
- clicks send no request and Tab never stops on a cell;
- the menu is portalled and fully visible, and Escape layering holds;
- dark buttons now 9.6 / 6.49:1, error text 5.75:1, chip "×" 4.63:1;
- Sign out fires `unity-auth-cleared` once.

F-13 is fixed in code but not visible live until API.Framework is restarted. One Minor: `aria-label` sits on a role-less `span` (F-26). Nits: mixed EOL, stale README icon list, inline style, double event dispatch, plus F-19 partly done.

Spec note for Plan Bot: the green tick is 2.51:1 on white and the red cross 2.09:1 on dark, below 3:1 for non-text, with the tokens the ticket prescribes.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-26 | `ui/UI.NextJs.Framework/src/framework/entity-framework/grid/grid-cell-renderers.tsx:35,43,50` | Minor | The Yes / No / Not set name is an `aria-label` on a role-less `span` (generic role; naming prohibited in ARIA 1.2). Chromium exposes it, but other AT may not. T-ANIMAL-009 S1 / S2 / S5 need the name (WCAG 4.1.2, general practice) | Add `role="img"` (or visually hidden text) |
| F-19 | `handoff.md` → `implementation.ui` (form route files) | Nit | Partly resolved: old IDs remapped and page files tagged T-ANIMAL-008. The form fallbacks / intercepting routes are still T-ANIMAL-004 only, and T-ANIMAL-008/S4–S6 aren't referenced | Tag them on the next manifest update |
| F-27 | 9 API files + `Switch.tsx` / `.module.css` (last line); `Button.module.css:25-27`; `entity-framework/index.ts:32-34`; `DesignSystemShowcase.tsx:249-250` | Nit | New mixed line endings: LF lines inside CRLF files. Also a double blank line | Normalise each file; consider `.editorconfig` |
| F-28 | `ui/UI.NextJs.Framework/src/framework/design-system/README.md:17` | Nit | The Icon names list still says "Visibility, Edit, Delete"; it lacks `Check` / `Close` (`nextjs-design-system.mdc:152`) | Update the list |
| F-29 | `ui/UI.NextJs.Framework/src/framework/entity-framework/grid/grid-cell-renderers.tsx:35,43` | Nit | Inline `style` for colour / layout, where the framework uses co-located CSS modules (`nextjs-design-system.mdc:140-141`) | Move to a module class |
| F-30 | `ui/UI.NextJs.Framework/src/framework/auth/token-refresh.service.ts:32-33,50-51` | Nit | `clearAuthState()` now dispatches `unity-auth-cleared`, and token refresh dispatches it again (fires twice; listeners are idempotent) | Drop the two extra dispatches |

### Changes since last round

Against round 3:
- Resolved: F-13 (in code; live needs an API restart), F-14, F-15, F-18, F-20, F-21, F-22, F-23, F-24.
- Superseded: F-25 (by T-ANIMAL-009).
- Still open: F-19 (Nit, partly done).
- New: F-26 (Minor); F-27, F-28, F-29, F-30 (Nit).
- Regressions: none.

### Notes

- **Live check:** UI http://localhost:3003 and API.Framework 5088 / 7088, both already running; nothing started or restarted.
  - Credentials went by env var to a child process only.
  - Only "ZZ Test Animal 202610081831 T" / "… F" were touched. Both were deleted through the UI, with 404 confirmed.
  - Screenshots are on the box in `/workspace/manage-animals-check/d29/`.
- **Hand-off edits during review:** Plan Bot (rows 30–32: test-fix cap, frozen IDs, encoding) and Test Bot (`testing` section). Docs only.
- **Out of scope:**
  - boolean icon contrast (spec tokens);
  - Dev Bot's edit to `api-framework-testing.mdc`;
  - `blocked_tests_allow_approval` is still an unsettled default;
  - paginator icon contrast;
  - the dev-only seeded password.

## Decision 29 cycle 1 — test review (test round 1) — 08/10/2026 19:45 (Europe/London)

| Type | Test round | Report | Result (pass / fail / waiting) | Test-fix cycle | Test verdict | Routed to | Note |
|------|-----------|--------|--------------------------------|----------------|--------------|-----------|------|
| test | 1 | `tests/TEST-manage-animals-1-report.md` (plan `tests/test-plan.md`) | 0 / 0 / 75 (all 75 frozen IDs present, all Waiting / blocked) | 0 of 5 (a blocked run isn't a round) | **blocked-noted** | code (scaffolding: Api.Framework.Tests, Next.js e2e + playwright-bdd, reset endpoint + batch keys, personas, optional component harness) and human (Test environment, test DB, `E2E_TEST_DATA_KEY` / persona passwords, `testing` placeholders) | **Tests blocked**: no test code to review yet. Final approval allowed by `testing.blocked_tests_allow_approval: true` (config line 415, flagged default); Neil decides at merge. Doesn't count toward `review.cycle` |

## Decision 30 cycle 1 — code review (d30-1) — 08/10/2026 20:30 (Europe/London)

| Type | Cycle | Report | Code verdict | Test verdict | Final verdict | Routed to | Note |
|------|-------|--------|--------------|--------------|---------------|-----------|------|
| code | 1 | `reviews/DIRECT-manage-animals-d30-1-review.md` | **Request changes** | *(untouched — Provisional, awaiting test review)* | null (option B) | **code** (Dev Bot) | Decision 30 filled-circle + knock-out (Neil 20:19) live ✓ (fill vs row/hover ≥ 3:1 light/dark; transparent cut-outs; role=img). Scaffolding reviewed. **Blocker F-31** committed Test DB password in `appsettings.Test.json` + `e2e/README.md` (R8/R12). Minors F-32 (unused scaffolding `signInAs`; suite uses real `signInViaUi`)…F-35; Nits F-36/F-37 + open F-19/F-27…F-30. F-26 resolved. d29-1 SUPERSEDED. Follow-ups in-cycle: harness `notFound()` in production, EntityGrid `sessionPermissions` (harness-only), `animals-nodisplayname` rename. Stale API process (17:55) — TestData 404. No Test Bot report for this build. |

## Decision 30 cycle 2 — code review (d30-2) — 08/10/2026 20:50 (Europe/London)

| Type | Cycle | Report | Code verdict | Test verdict | Final verdict | Routed to | Note |
|------|-------|--------|--------------|--------------|---------------|-----------|------|
| code | 2 | `reviews/DIRECT-manage-animals-d30-2-review.md` | **Approve with comments** | *(untouched — Provisional, awaiting test review)* | null (option B) | **test** (Test Bot) | d30-1 F-31…F-37 + F-19/F-27…F-30 **Resolved**. Knock-out live ≥ 3:1 light/dark; instant modal pending ~10–16 ms (`animal-form-modal-pending`); Cancel/Esc OK. **Minor F-38** browser Back leaves orphaned pending shell; Nits F-39 (README dup paragraph in env table), F-40 (csproj EOL). Unit 45/2; ui+e2e tsc pass. Live API was Dev 5088/7088 (Test 5188/7188 not up). No new TEST report → provisional. testing: untouched. |

## Decision 30 cycle 2 — test review (test round 2) — 09/10/2026 09:05 (Europe/London)

| Type | Test round | Report | Result (pass / fail / blocked) | Test-fix cycle | Test verdict | Routed to | Note |
|------|-----------|--------|--------------------------------|----------------|--------------|-----------|------|
| test | 2 | `tests/TEST-manage-animals-2-report.md` (review: `reviews/DIRECT-manage-animals-d30-2-review.md` → Test review) | 76 / 0 / 1 (T-ANIMAL-007/S8 `@skip @fixme`, owner Plan Bot / Neil); unit 45 pass + 2 Skip; e2e + harness 64/64 | 0 of 5 → this routing is test-fix round 1 when Test Bot re-runs (not counted toward `review.cycle`) | **request-changes** | **testing** (Test Bot); human: rotate persona passwords | **Major F-41**: run-5 HTML report holds persona passwords in plain text on `Fill` step titles (tester 37, viewer 4, usermanager 1; reset key / tokens / conn string 0). Minor F-42: S11/S13 reflection Facts empty + skipped for a stale reason (ProjectReference exists), so S13's Program.cs policy Then is untested; F-43: S13 e2e GET-only, S11 no nothing-written check; F-44: `testing.status` should be `blocked` (T-007/S8). F-46: F6 retry may mask early-input loss. Nits F-45 (dialog selector matches loading fallback), F-47 (positional td). Harness no-reset exemption confirmed (0 API requests live). No front-end mocks; reset-first OK; only api_framework_test / 5188/7188. No code defects; code_verdict stays approve-with-comments. Final verdict null. |

## Decision 30 cycle 2 — test review (test round 3) — 09/10/2026 09:58 (Europe/London)

| Type | Test round | Report | Result (pass / fail / blocked) | Test-fix cycle | Test verdict | Routed to | Note |
|------|-----------|--------|--------------------------------|----------------|--------------|-----------|------|
| test | 3 | `tests/TEST-manage-animals-3-report.md` incl. Addendum (09:48) and Addendum 2 (09:56) (review: `reviews/DIRECT-manage-animals-d30-2-review.md` → Test review — test round 3) | **77 / 0 / 0** (T-ANIMAL-007/S8 unblocked after Neil's 09:46 baseline, passes); unit 52/52, 0 Skip; e2e run 11 73/73 (67 + 6 setup), 0 flaky | 1 of 5 (not counted toward `review.cycle`, still 2) | **approve** | **human** (Neil: merge decision; rotate persona passwords) | Final **verdict approve-with-comments**, stage approved, owner human. Resolved: F-38, F-39, F-40 (code); F-41 Major (setup sign-in in untraced child process `sign-in-child.cjs`; scan 0 persona passwords / 0 reset key / 0 JWT outside .auth across 24 files); F-42, F-43, F-44, F-45, F-47; F-46 = code defect fixed by Dev Bot (load-generation guard + JsonForms middleware, Vitest regression tests); F-48 (modal-closed check covers -fallback/-pending/-shell/-loading); F-49 resolved/accepted (traced request context documented); F-54 (handoff YAML parses, BEL removed). Open Nits: F-50 (:3003 shared with dev UI; reuseExistingServer), F-51 (fillStable retry), F-52 (rule file blank line), F-55 (child inherits full env), F-56 (.next-test-tb not ignored); note F-53 (no ESLint config, pre-existing). Rule change flagged to Neil: nextjs-modal-routing.mdc (one element per tid; -fallback/-pending/-shell/-loading; Back clears pending; early typing kept). |
