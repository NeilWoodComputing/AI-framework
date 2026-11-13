# Ticket: T-ANIMAL-009 — Shared boolean icon grid cell renderer (UI.NextJs.Framework)

| Field | Value |
|-------|--------|
| ID | T-ANIMAL-009 |
| Type | UI framework component |
| Feature | Manage Animals |
| Priority | P1 |
| Specs | `specs/manage-animals.yaml`, `excel/manage-animals.xlsx` (Is Furry / Has Hooves `display_format`: Boolean icon) |
| Journey (optional) | J-ANIMAL-001 (`journeys/j-animal-manage.md`) |
| Depends on | Design-system `Icon` and theme tokens (adds `Check` / `Close` to `Icon` if missing — see Work to do; adds the decision 30 boolean tokens to `tokens.css`). Used by T-ANIMAL-003 |
| Decisions | `plan.md` → Decisions 15, 29, 30 (filled-circle cells, light / dark tokens; Neil approved 19:57 BST); Q38 accepted 19:14 BST (null → em dash + "Not set") |

## User story

**As a** developer building Unity grids in UI.NextJs.Framework  
**I want** a shared read-only boolean cell that shows a filled green circle with a tick cut-out or a filled red circle with a cross cut-out (the row colour shows through, readable in light and dark mode) with an accessible Yes/No name  
**So that** Manage Animals (and any future grid) can show booleans without looking like editable Switches

## Full-stack scope

| UI label / column | Control or grid | Service | Target DB Table | Target DB Column / Population Source |
|-------------------|-----------------|---------|-----------------|--------------------------------------|
| Is Furry (grid) | Boolean icon cell (`renderBooleanIconCell`) | Animals | Animal (creatures.animals) | Animal.IsFurry |
| Has Hooves (grid) | Boolean icon cell (`renderBooleanIconCell`) | Animals | Animal (creatures.animals) | Animal.HasHooves |

## Findings from the current UI (read-only; do not invent names)

Checked in `ai-code-framework/ui/UI.NextJs.Framework` (read only):

- **Existing boolean grid helper:** `renderBooleanSwitchCell` in `src/framework/entity-framework/grid/grid-cell-renderers.tsx` — renders `@design-system` `Switch` with `readOnly` and `aria-label={label}`. Exported from `@entity-framework`. Animals uses it in `src/features/animals/manage-animals/columns/animals-grid-columns.tsx` for Is Furry / Has Hooves today.
- **Icon component:** `src/framework/design-system/components/icon/Icon.tsx` — Material icon paths (Apache 2.0), `fill="currentColor"`, default `size = '1.8rem'`, `aria-hidden` + `focusable="false"` on the SVG, `data-icon={name}`. **Current `IconName` values: only `Edit` and `Delete`.** There is **no** Check / Tick / Close / Cross icon yet — this ticket **adds** Material `Check` and `Close` to `ICON_PATHS` / `IconName`.
- **Colour tokens:** `src/framework/design-system/theme/tokens.css` already defines `--system-green: #72b453` and `--system-red: #cf1337` on `:root` (not overridden in dark theme). *(Decision 30: do **not** use or change these for the boolean cell — they also paint the system buttons and callout borders. Light-mode #72b453 is 2.51:1 on white and dark-mode #cf1337 is 2.09:1 on the dark row, both below 3:1. Dark overrides live in the `html[data-theme='dark']` block of the same file (set by `ThemeProvider.tsx`); the dark `--app-form-error-text` is `#ff9aa8`. Add new dedicated boolean fill tokens — see Work to do item 7; the glyph is a cut-out, not a colour token (Neil 20:19).)*
- **Aria pattern today:** `renderBooleanSwitchCell` puts the accessible name on the control (`aria-label`). Because `Icon` is `aria-hidden`, the boolean-icon cell must put `aria-label` (Yes / No / Not set) on a wrapping non-interactive element (e.g. `span`), not rely on colour alone.

## Work to do

1. In `src/framework/design-system/components/icon/Icon.tsx`, add Material icon paths for **`Check`** (tick) and **`Close`** (cross) to `ICON_PATHS` / `IconName`, same style as `Edit` / `Delete`. Do not invent other names.
2. In `src/framework/entity-framework/grid/grid-cell-renderers.tsx`, add **`renderBooleanIconCell`** next to `renderBooleanSwitchCell`. Suggested signature: `(value: boolean | null | undefined, options?: { trueLabel?: string; falseLabel?: string; nullLabel?: string; tid?: string; size?: number | string }) => ReactNode`. Defaults: `trueLabel = 'Yes'`, `falseLabel = 'No'`, `nullLabel = 'Not set'` (Q38, accepted 19:14 BST).
3. *(Amended by decision 30, Neil 19:57; cut-out amendment Neil 20:19.)* True → a **filled circle** in `var(--app-boolean-true-fill)` with Material `Check` as a **transparent cut-out** (the row / hover colour shows through the tick); false → a filled circle in `var(--app-boolean-false-fill)` with Material `Close` as a cut-out; null / undefined → em dash (`—`) only (no circle) in the theme text colour (`var(--app-text-primary)`), with accessible name from `nullLabel` (Q38, accepted 19:14 BST: default "Not set"). Build with `<Icon name="Check" | "Close" knockout="circle" />` (one evenodd SVG path: filled circle with the tick / cross punched out). Do **not** draw a separate coloured glyph on top of or behind the circle, and do **not** keep `--app-boolean-glyph`. Wrap in a non-interactive element with `aria-label` matching the label; no `onClick`, not a button/link, not in the tab order as a control (`tabIndex` unset / not focusable).
4. Keep **`renderBooleanSwitchCell`** exported and unchanged for other grids that still want a read-only switch.
5. Export `renderBooleanIconCell` from `@entity-framework` (`src/framework/entity-framework/index.ts`).
6. Suggested icon size for grid cells: smaller than the Icon default `1.8rem` (e.g. `1.6rem` or `20px`) so the cell matches other grid content — confirm with Neil only if it looks wrong; otherwise use `1.6rem`. *(Decision 30 / 20:19: `1.6rem` is the circle's diameter; the cut-out tick / cross sits inside it.)*
7. *(New, decision 30; amended Neil 20:19.)* In `src/framework/design-system/theme/tokens.css` add dedicated tokens on `:root` — `--app-boolean-true-fill: #609b44`, `--app-boolean-false-fill: #ef5673` — and dark overrides in the existing `html[data-theme='dark']` block — `--app-boolean-true-fill: #8dc374`, `--app-boolean-false-fill: #ff9aa8` (may be `var(--app-form-error-text)`). Do **not** add `--app-boolean-glyph` (Neil 20:19: the glyph is a cut-out, not a colour). Leave `--system-green` / `--system-red` and every other existing token unchanged. The renderer uses only the fill tokens (no hard-coded hex).

## Acceptance criteria

### Scenario: S1 — True shows a green circle with a tick, named Yes

```gherkin
Given a grid column that uses renderBooleanIconCell
And a row whose bound boolean is true
When the cell renders
Then it shows a filled circle coloured var(--app-boolean-true-fill)
And the design-system Icon named Check is a transparent cut-out of that circle (Icon knockout="circle"; the row colour shows through the tick)
And the cell has an accessible name "Yes" (not colour-only)
And the cell is not a switch
```

### Scenario: S2 — False shows a red circle with a cross, named No

```gherkin
Given a grid column that uses renderBooleanIconCell
And a row whose bound boolean is false
When the cell renders
Then it shows a filled circle coloured var(--app-boolean-false-fill)
And the design-system Icon named Close is a transparent cut-out of that circle (Icon knockout="circle"; the row colour shows through the cross)
And the cell has an accessible name "No" (not colour-only)
```

### Scenario: S3 — Cell is not interactive

```gherkin
Given a boolean-icon cell is shown for true or false
When I click the cell
Then no request is sent and no handler runs
And the cell is not focusable as a control (not a button, link or switch)
```

### Scenario: S4 — Labels are configurable with Yes/No defaults

```gherkin
Given renderBooleanIconCell is called with trueLabel "Furry" and falseLabel "Not furry"
When a true value and a false value render
Then the accessible names are "Furry" and "Not furry" respectively
When it is called with no label options
Then the accessible names default to "Yes" and "No"
```

### Scenario: S5 — Null / undefined shows em dash named Not set

```gherkin
Given a grid column that uses renderBooleanIconCell
And a row whose bound value is null or undefined
When the cell renders
Then it shows an em dash "—" (not a Check or Close icon, and no circle)
And the em dash uses the theme text colour var(--app-text-primary)
And the cell has an accessible name "Not set"
And it is not colour-coded as success or error
```

### Scenario: S6 — Existing switch cell still available

```gherkin
Given renderBooleanSwitchCell is still exported from @entity-framework
When another grid calls renderBooleanSwitchCell
Then it still renders a read-only Switch as before
And Manage Animals Is Furry / Has Hooves do not use it after T-ANIMAL-003 switches over
```

### Scenario: S7 — Circle fills meet contrast in light and dark mode

```gherkin
Given the boolean cell fill tokens in tokens.css
When the theme is light (no data-theme or data-theme="light")
Then --app-boolean-true-fill is #609b44 and --app-boolean-false-fill is #ef5673
And each fill is at least 3:1 against the grid row #ffffff and row hover #fafafa (3.35 / 3.21 and 3.36 / 3.22)
When the theme is dark (html data-theme="dark")
Then --app-boolean-true-fill is #8dc374 and --app-boolean-false-fill is #ff9aa8
And each fill is at least 3:1 against the grid row #2d3a4a and row hover #3d4854 (5.61 / 4.52 and 5.75 / 4.63)
And there is no --app-boolean-glyph token (the cut-out shows the row colour; Neil 20:19)
And switching the theme updates the circle colours without a reload
```

### Scenario: S8 — Dedicated tokens leave system buttons and callouts unchanged

```gherkin
Given the boolean cell uses --app-boolean-true-fill and --app-boolean-false-fill
When tokens.css is updated for decision 30
Then --system-green stays #72b453 and --system-red stays #cf1337 in both themes
And --app-boolean-glyph is not defined
And the System green / System red buttons and the success / error callouts look as before
And the renderer contains no hard-coded colour values
```

Checklist (derived from scenarios):

- [ ] `Check` and `Close` exist on design-system `Icon` (Material paths)
- [ ] `renderBooleanIconCell` lives next to `renderBooleanSwitchCell` and is exported
- [ ] Filled circle with Check / Close as a transparent cut-out (`Icon knockout="circle"`); colours use `--app-boolean-true-fill` / `--app-boolean-false-fill` only (no hard-coded hex, no `--app-boolean-glyph`; decision 30 / Neil 20:19)
- [ ] Fill tokens added on `:root` with dark overrides in `html[data-theme='dark']`; fill-vs-row contrast as in S7; `--system-green` / `--system-red` unchanged (S8)
- [ ] Accessible name always present (Yes / No / Not set or configured labels)
- [ ] Not interactive; `renderBooleanSwitchCell` unchanged for other callers

## Out of scope

- Wiring Is Furry / Has Hooves on Manage Animals to the new renderer (T-ANIMAL-003)
- Form Switch / Tag Input controls (T-ANIMAL-006)
- Changing existing token values, including `--system-green` / `--system-red` (decision 30 only adds new boolean tokens)

## Notes

- Stable ID for DevOps upsert: `T-ANIMAL-009`
- Decision 29 (Neil, 2026-10-08 19:04 BST via Review Bot); Q38 accepted 19:14 BST. Neil reopened the feature at 19:14 and approved `plan_to_code` for this change (alongside the 15:44 approval).
- Scenario IDs are new (S1–S6). No old → new remap: this ticket did not exist before. Boolean grid-cell behaviour previously lived under T-ANIMAL-006's "Grid cells" scenario (boolean part) and T-ANIMAL-003 work item 3 / display wording — see those tickets for the old → new notes.
- Q38 (Neil, 2026-10-08 19:14 BST): accepted suggested default — em dash (`—`) with accessible name "Not set". S5 is final.
- Decision 30 (Neil, 2026-10-08: 19:52 BST dark-mode request via Review Bot, 19:53 BST inverted-circle request, 19:57 BST approval; amended 20:19 BST): cells become a filled circle (light Yes #609b44 / No #ef5673; dark Yes #8dc374 / No #ff9aa8) with Check / Close as a transparent cut-out via tokens `--app-boolean-true-fill` / `--app-boolean-false-fill` (`--app-boolean-glyph` removed). S1 and S2 reworded in place (same IDs; shape and colours changed), S5 adds "no circle, theme text colour", S3, S4 and S6 unchanged; **S7** (fill-vs-row contrast, light and dark) and **S8** (system tokens unchanged) are new. Work item 3 amended, item 7 new.
- Neil 20:19 BST (via Dev Bot): glyph is a transparent cut-out (`Icon knockout="circle"`, evenodd path) so the circle fill / row colour shows through the tick or cross. `--app-boolean-glyph` / `#18181b` / `var(--ink-100)` as a glyph colour removed; fills and fill tokens unchanged. S1, S2, S7 and S8 reworded in place (same IDs); work items 3, 6 and 7 amended. Doc-only follow-up inside Decision 30 — no new scenario IDs.
