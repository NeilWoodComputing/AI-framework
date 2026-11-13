# UI checklist — Next.js (UI.NextJs.Framework)

Applies when `development.ui.active` is `nextjs`.

> **Rules:** `development.ui.options.nextjs.rules` (`ai-code-framework/ui/UI.NextJs.Framework/.cursor/rules/`, index `README.md`) and `agent_docs` (`AGENTS.md`, `README.md`). Sections A and B cite the rule that backs each item; cite the rule file and heading in the finding (for example `style/nextjs-css.mdc` → Dark mode). Breaches are **Minor** unless they change behaviour the spec cares about (`checklists/severity.md`); points a formatter would fix stay **Nit**. Section C is **General practice** for React 19 / Next.js 15, kept only for points the rules don't cover: label those findings "General practice" and cap them at **Minor** unless they are a security or data-integrity issue.

## A. Architecture and feature patterns

- [ ] API URLs built from `apiRoutes` in `src/config/api-routes.ts`, driven by `environment.apiRoot` (`NEXT_PUBLIC_SYSTEM_API_ROOT`); no hard-coded hosts or API paths in features — `framework/nextjs-framework-overview.mdc` → API configuration
- [ ] API calls go through `systemApiFetch` (`src/framework/api/system-api-fetch.ts`), which adds `Authorization: Bearer …`; no raw `fetch` that skips it — `framework/nextjs-framework-overview.mdc` → Framework-first; `framework/nextjs-state-layer.mdc` → Data providers
- [ ] Code placed per the layout: `src/config/`, `src/framework/` (`api`, `auth`, `design-system`, `entity-framework`, `json-schema-form`), `src/features/<area>/`, `src/app/`, `src/shell/`; shared framework extended rather than reimplemented in a feature — `framework/nextjs-framework-overview.mdc` → Layout, Framework-first
- [ ] Imports use the `tsconfig.json` aliases (`@design-system`, `@entity-framework`, `@json-schema-form`, `@auth/*`, `@shell/*`, `@features/*`, `@/*`); no deep relative paths into `src/framework/` — `framework/nextjs-framework-overview.mdc` → Path aliases; `style/nextjs-components.mdc` → Imports
- [ ] Route files stay thin: `page.tsx` renders a feature component; behaviour lives in `src/features/...` — `style/nextjs-components.mdc` → Page composition; `implementation/nextjs-implementation.mdc`
- [ ] Grids compose `@entity-framework` (`EntityGrid`, `useAuthenticatedEntitySearch`, `useEntityGridState`, `EntityGridAuthGate`) in the documented folder shape (`columns/`, `state/`, `shared/state/*-update.service.ts`, `shared/utils/*-routes.ts`), copying the grid sample the rule names (`reference-data-types-grid/`) — `framework/nextjs-entity-grid.mdc` → Folder structure, Wiring
- [ ] Grid config sets `tid`, `defaultSortColumn`, `pageSize`, `hasPaging`; row actions through config `rowActions` (`rowActionsDisplay: 'menu'` for overflow menus), not ad-hoc button columns; Add / primary actions through `headerToolbarActions` — `framework/nextjs-entity-grid.mdc` → Grid config, Columns
- [ ] `updateService.trigger()` after every successful create / update / delete, with the update-service singleton passed to `useEntityGridState` — `framework/nextjs-entity-grid.mdc` → Refresh after mutations; `framework/nextjs-state-layer.mdc` → Update services
- [ ] Data providers extend `AbstractSearchDataProvider` / `AbstractEntityDataProvider`, resolve URLs only through `apiRoutes`, and are named `{feature}-search.data-provider.ts` / `{entity}-entity.data-provider.ts`; persistence goes through the provider — `framework/nextjs-state-layer.mdc` → Data providers; `framework/nextjs-json-schema-forms.mdc` → Data provider
- [ ] Form modals follow the documented layout (`{Entity}FormModal.tsx`, `state/*-entity.data-provider.ts`, `state/*-ui-schema.ts`, `ui-schemas/*.ui-schema.json`) and render through `JsonSchemaForm` + `useJsonSchemaEntityForm`; no field list hand-built in JSX — `framework/nextjs-json-schema-forms.mdc` → File layout, Modal wiring, UI schema
- [ ] Client validation runs against the server schema (`schemaDrivenValidation: true`); no hand-written validators that duplicate it; server-only checks (uniqueness, cross-record rules) run on submit and their errors show on the controls / modal — `framework/nextjs-json-schema-forms.mdc` → Standing rule; `AGENTS.md` → Standing forms rule
- [ ] UI schema controls use `"scope": "#/properties/<field>"`, matching the API's camelCase property names — `framework/nextjs-json-schema-forms.mdc` → UI schema
- [ ] Routed modals use the parallel `@modal` / intercepting route shape (`layout.tsx` renders `modal`, `@modal/default.tsx`, `(.)manage/...`, full-page `manage/...` fallback); open with `useModalNavigate().open` and close with `useModalDismiss` / `RoutedModal`; href builders in `shared/utils/{feature}-routes.ts` — `framework/nextjs-modal-routing.mdc` → App Router shape, Opening & closing
- [ ] `.env*` files are not created, edited or committed and `src/config/environment.ts` defaults are unchanged (environment values are the human owner's to set) — `framework/nextjs-framework-overview.mdc` → API configuration; `AGENTS.md` → API / env
- [ ] No `git init` and no agent-specific folder (`Grok/` or similar) — `implementation/nextjs-implementation.mdc` → Safety / repo hygiene; `AGENTS.md` → Do not

## B. Components, design system and styling

- [ ] UI composed from `@design-system` first; new reusable visuals go under `src/framework/design-system/`, are exported from its `index.ts` and documented in its `README.md` and the showcase — `style/nextjs-design-system.mdc` → Import rule, Adding a new design-system component; `AGENTS.md` → Component library first
- [ ] `Button` for all actions (no raw `<button>` where the primitive fits), `loading` for in-flight actions, destructive confirm actions `theme="system-red"` — `style/nextjs-design-system.mdc` → Catalogue, Button conventions
- [ ] Typography through `H1`–`H3` / `P` and pages through `PageLayout`, not bare headings with one-off classes — `style/nextjs-design-system.mdc` → Typography & layout
- [ ] Field errors on the control (`error` prop / `FormFieldError`); page- or modal-level messages in a `Callout`; no parallel error UI — `style/nextjs-design-system.mdc` → Form controls, Callouts & feedback
- [ ] Routed create / edit forms use `RoutedModal` (stacked forms `level="secondary"`); delete / confirm uses `ConfirmModal` — `style/nextjs-design-system.mdc` → Modals (component API); `framework/nextjs-modal-routing.mdc` → Modal component
- [ ] `tid` on interactive and container elements, rendered as `data-tid`, kebab-case values identical to the specs; grid root `tid` set in `EntityGridConfig` — `style/nextjs-components.mdc` → Test IDs
- [ ] Naming and files: PascalCase components, `use-*.ts(x)` hooks, kebab-case feature folders, `{Component}.module.css` beside the component, explicit `*Props` interfaces for shared components — `style/nextjs-components.mdc` → File & folder structure, Naming, Props & composition
- [ ] `'use client'` only where hooks, browser APIs, event handlers or interactive CSS-module trees need it; `src/app/**` defaults to Server Components — `style/nextjs-components.mdc` → Client vs server
- [ ] Colours and surfaces from `theme/tokens.css` (`--app-*`, `--ink-*`, `--primary-action`, …); no new hard-coded hex where a token fits; dark mode through semantic tokens; rem sizing; no Bootstrap component CSS — `style/nextjs-css.mdc` → Token sources, Dark mode, Rem sizing, What not to do
- [ ] TypeScript strict; no `any` (use `unknown` and narrow); 2-space indent, single quotes, semicolons, no double-spaced files — `style/nextjs-formatting.mdc` (formatter-level points are **Nit**)
- [ ] `npm run typecheck` (`tsc --noEmit`) passes, run from the project folder (project-local tools only, never a root `npx`) — `AGENTS.md` → Verify; `implementation/nextjs-implementation.mdc` → Implementation order

## C. General practice (React 19 / Next.js 15) — not covered by the rules

- [ ] Hooks follow the rules of hooks; effects have correct dependencies and clean up
- [ ] Lists render with stable `key`s (IDs, not array index, when rows can change)
- [ ] Loading, empty and error states handled for each data call; errors shown to the user without leaking internals (where the message is shown is covered in B)
- [ ] Accessibility: every control has a label; focus managed when modals open and close
- [ ] No secrets in `NEXT_PUBLIC_*` variables (they are shipped to the browser) — security, so not capped at Minor
- [ ] No `dangerouslySetInnerHTML` with user data — security, so not capped at Minor
- [ ] `npm run lint` (`eslint .`), `npm test` (`vitest run`) and `npm run build` pass where they can run (`package.json` scripts, from the project folder)
