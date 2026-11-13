# UI checklist — Angular (UI.Angular.Framework)

Applies when `development.ui.active` is `angular`. Sources are under `ai-code-framework/ui/UI.Angular.Framework/.cursor/rules/` (index: `README.md`). Brief by design — open the cited rule for detail.

## Framework first

- [ ] Shared framework used before custom code: entity grid, datasets, JSON schema modals / wizards, routed modals, design-system components, data providers, `AbstractUpdatedService` — `framework/angular-framework-overview.mdc`
- [ ] Framework imported via path aliases (`@entity-framework/*`, `@design-system/*`, `@json-schema-form/*`, …), never deep relative paths into `src/framework/` — `framework/angular-framework-overview.mdc`
- [ ] New product areas copy `src/app/submodules/Example.Subrepo/README.md` (catalogue-item slice), not domain-specific subrepos — rules `README.md`, `framework/angular-framework-overview.mdc`
- [ ] Submodule wiring: module loader, `app.routes.ts`, `activeAreas`; `{domain}.routes.ts` with `PermissionRouteGuard`, `{domain}-modal-routes.ts`, `{domain}-api-routes.ts` — `framework/angular-framework-overview.mdc`, `framework/angular-submodule-features.mdc`

## JSON schema forms and wizards

- [ ] Layout per `framework/angular-json-schema-forms.mdc`: `ui-schemas/{step}.ui-schema.json`, `{feature}-wizard.config.ts`, `state/`
- [ ] Single-entity modal extends `AbstractJsonSchemaFormModalComponent`; template uses `<app-json-schema-form-body>` or the wizard shell, not a hand-built field list
- [ ] Wizard steps defined as `JsonSchemaWizardStepDefinition[]` with `id`, `label`, `schemaUrl`, `formLayout`, `reviewLayout` (+ `validateUrl`, `editSectionSlug` when needed); template uses only `<app-json-schema-wizard-shell>`
- [ ] Feature renderers registered with the framework's renderer registration, not by forking the core list
- [ ] Grid refresh after save via an `AbstractUpdatedService` subclass

## Grids, modals, state

- [ ] Entity grid recipe — `framework/angular-entity-grid.mdc`; datasets — `framework/angular-datasets.mdc`; routed modals — `framework/angular-modal-routing.mdc`; data providers and state — `framework/angular-state-layer.mdc`

## Components and style

- [ ] Standalone components, `ChangeDetectionStrategy.OnPush`, `app-` prefix, `@UntilDestroy()` for subscriptions, `tid="..."` on interactive elements — `framework/angular-framework-overview.mdc`, `style/angular-components.mdc`
- [ ] Templates use the design system — `style/angular-design-system.mdc`; SCSS and variables — `style/angular-css.mdc`, `style/angular-scss-variable-naming.mdc`; responsive — `style/angular-responsive-design-patterns.mdc`; formatting — `style/angular-formatting.mdc`
- [ ] New design-system components have Storybook stories — `style/angular-storybook.mdc`

## Errors, logging, docs

- [ ] Error handling and user-facing errors — `error-handling/angular-error-handling-patterns.mdc`, `error-handling/angular-user-facing-errors.mdc`, `error-handling/angular-custom-error-classes.mdc`
- [ ] Logging via `@logging` — `error-handling/angular-logging-configuration.mdc`
- [ ] Documentation comments — `documentation/angular-*-documentation.mdc`

## Tests

- [ ] Unit tests and naming — `testing/angular-tests.mdc`, `testing/angular-testing-framework.mdc`, `testing/angular-testing-best-practices.mdc`
- [ ] E2E with Playwright + Cucumber — `testing/angular-e2e-testing.mdc` (Given / When / Then scenarios map to feature files)
