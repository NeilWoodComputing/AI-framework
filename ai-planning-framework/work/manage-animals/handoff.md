---
# handoff.md: pipeline state for ONE feature. Rules: handoff/README.md
# Copy to <output.work_dir>/<feature>/handoff.md. Only the current `owner` edits
# this file. On every transition, update this front matter AND append a row to
# History. Paths are relative to this feature folder unless they start with ai-.
handoff_version: 1
example: false                # true = illustrative only; never picked up
feature: manage-animals
feature_path: ai-planning-framework/work/manage-animals   # output.work_dir/<feature>
stage: merged        # planned | in-development | in-review | changes-requested | approved | merged
owner: human                   # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config)
pickup: pending               # pending (handed over, not started) | accepted (owner is working it)
waiting_on: "Nothing for agents: MERGED 2026-10-09 12:37 BST (Neil's word to Dev Bot; no git). Neil's open to-dos remain (not blocking): rotate animals-tester / animals-viewer / animals-usermanager test passwords (F-41) and refresh e2e/.auth; optional Nits F-50 F-51 F-52 F-55 F-56, note F-53; rule change nextjs-modal-routing.mdc"
updated_at: 2026-10-27T11:28:23+00:00
updated_by: plan-bot

routes:                       # the route actually used (from handoff in the config)
  plan_to_code: direct        # devops | direct   (from handoff.plan_to_code; confirmed by the planning agent at hand-off)
  code_to_review: direct      # pr | direct       (set by the implementing agent at hand-off)
  code_to_test: direct         # direct (set at hand-off; message Test Bot with Review Bot)
  review_feedback: direct     # direct

tickets:                      # every T-<DOMAIN>-NNN in tickets/; id must match the filename
  - id: T-ANIMAL-001
    file: tickets/T-ANIMAL-001-animal-schema.md
    devops_work_item_id: null # set by the planning agent when plan_to_code = devops
  - id: T-ANIMAL-002
    file: tickets/T-ANIMAL-002-animals-service.md
    devops_work_item_id: null
  - id: T-ANIMAL-003
    file: tickets/T-ANIMAL-003-manage-animals-grid.md
    devops_work_item_id: null
  - id: T-ANIMAL-004
    file: tickets/T-ANIMAL-004-add-edit-animal-form.md
    devops_work_item_id: null
  - id: T-ANIMAL-005
    file: tickets/T-ANIMAL-005-soft-delete.md
    devops_work_item_id: null
  - id: T-ANIMAL-006
    file: tickets/T-ANIMAL-006-shared-switch-tag-input.md
    devops_work_item_id: null
  - id: T-ANIMAL-007
    file: tickets/T-ANIMAL-007-shared-grid-actions-column.md
    devops_work_item_id: null
  - id: T-ANIMAL-008
    file: tickets/T-ANIMAL-008-manage-animals-page.md
    devops_work_item_id: null
  - id: T-ANIMAL-009
    file: tickets/T-ANIMAL-009-shared-boolean-icon-grid-cell.md
    devops_work_item_id: null

devops:                       # only when plan_to_code = devops
  board_url: null
  published_at: null

code:                         # set by the implementing agent; repos from development.api/ui active paths
  api:
    repo: ai-code-framework/api/API.Framework       # development.api.active: api-framework
    branch: null              # handoff.branch_pattern; same name in every repo touched. Required for the PR route
                              # and direct_scope: diff; optional for direct_scope: plan (null if not a git repo)
    base_branch: null         # PR target / diff base (review.target_branch unless stated); not used by direct_scope: plan
    head_commit: null         # commit handed to review, when the repo is under git
  ui:
    repo: ai-code-framework/ui/UI.NextJs.Framework  # development.ui.active: nextjs
    branch: null
    base_branch: null
    head_commit: null
  build: pass                 # pass | fail
  tests: scaffolding-ready    # null | scaffolding-ready | pass | fail — Api.Framework.Tests + e2e present; scenario suites are Test Bot's
  # 2026-10-08 Dev Bot: Decision 30 UI + scaffolding ready. code.tests stays scaffolding-ready (scenario suites are Test Bot's).

  verification:
    - "T-ANIMAL-009 + round-3 pass (2026-10-08T19:20:33+01:00): ui npx tsc --noEmit -> pass; API AnimalController GET NotFound body + final newlines only (no full API rebuild this pass); framework docs AGENT-BRIEF / feature-build / api-framework-testing.mdc updated"
    - "api: dotnet ef migrations remove --force --project Api.Framework.Data --startup-project Api.Framework --configuration Release --no-build -> removed 20261008131327_AddAnimals (auth.animals) and reverted the snapshot (no database had applied it, Q27)"
    - "api: dotnet ef migrations add AddAnimals --project Api.Framework.Data --startup-project Api.Framework --output-dir Migrations --configuration Release --no-build -> 20261008150221_AddAnimals: EnsureSchema creatures, creates creatures.animals (pk_animals, ix_animals_normalized_name_active, ix_animals_updated_by, fk_animals_users_updated_by -> auth.users restrict), InsertData animals_write + Administrators / Standard links"
    - "api: dotnet build Api.Framework.sln --configuration Release -> pass, 0 warnings, 0 errors"
    - "api: dotnet ef migrations has-pending-model-changes --project Api.Framework.Data --startup-project Api.Framework --configuration Release --no-build -> No changes have been made to the model since the last migration"
    - "api (ad-hoc, %TEMP% console referencing Api.Framework.Services + Api.Framework.Data, Npgsql model without a connection + EF InMemory, deleted afterwards): 20/20 pass - Animal mapped to creatures.animals (default schema still auth), FK to auth.users restrict, animals_write seeded once (id ...025, 'Manage animals', category Animals, only permission in Animals) and linked to Administrators and Standard only; AnimalService T-ANIMAL-002 S1-S10 (create/trim/normalise, attributes [], duplicate 409, today/future 400, required messages, tag limits, list order + Last Amended name fallback, soft delete + 404s, deleted name reuse) and update"
    - "ui: npx tsc --noEmit -> pass"
    - "ui: npm run build (Next 15.5.27) -> pass; /examples/animals, /manage, /manage/item, /manage/item/[id] and the (.)manage intercepting routes generated"
    - "ui (ad-hoc, esbuild + react-dom/server on Grok Bot's box, outside both repos): EntityGrid static render with stubbed useAuth for T-ANIMAL-007 S1, S3-S8 (Actions last + not sortable, one trigger per row, unpermitted items hidden not disabled, any-of permissions, no Actions column when nothing permitted or signed out, per-row isVisible, empty cell with no trigger, default text-button grid unchanged) + hasAnyPermission -> 14/14 pass"
    - "ui (ad-hoc, 14:26 run, unchanged since): validateUnitySchemaData against the create-animal schema (defaults, required messages, whitespace name, today/future/blank date, 51-char tag, 21 tags, payload mapping, additionalErrors) -> pass"
    - "ui: npm run lint -> NOT RUN (unchanged, pre-existing: no ESLint config in the project, next lint prompts interactively and would create one). No project config was created"
    - "round 1 fixes, api: dotnet build Api.Framework.sln --configuration Release -> pass, 0 warnings, 0 errors"
    - "round 1 fixes, api: dotnet ef migrations has-pending-model-changes --project Api.Framework.Data --startup-project Api.Framework --configuration Release --no-build -> No changes have been made to the model since the last migration (F-08 was whitespace only)"
    - "round 1 fixes, ui: npx tsc --noEmit -> pass"
    - "round 1 fixes, ui: npm run build (Next 15.5.27) -> pass; all /examples/animals routes generated"
    - "round 1 fixes, ui: npm run lint -> still NOT RUN (unchanged, pre-existing: next lint prompts interactively to create an ESLint config; none was created)"
    - "not run: API with a real database (Neil runs it; the API applies migrations at start-up), browser click-through of the UI, menu Escape / outside-click behaviour (T-ANIMAL-007 S9, code unchanged from the 14:30 build)"
    - "Decision 30 (2026-10-08T20:04:30+01:00): ui npx tsc --noEmit -> pass; renderBooleanIconCell filled-circle (Check/Close glyph --ink-100 / --app-boolean-glyph) with --app-boolean-true-fill / --app-boolean-false-fill light+dark; --system-green/--system-red unchanged (S8); contrast S7 checked against ticket targets (fills >=3:1 on row/hover; glyph >=4.5:1 on fills)"
    - "2026-10-08 scaffolding (confirmed at Decision 30 hand-off): dotnet test Api.Framework.Tests --configuration Release -> 21/21 pass; e2e Playwright + playwright-bdd scaffold ready (scenario .feature files are Test Bot's)"
    - "d30-1 fixes (2026-10-08T20:45:00+01:00): F-31 password scrubbed from appsettings.Test.json (LoginConnection empty) + e2e/README (env-only ConnectionStrings__LoginConnection, least-privilege role docs); grep Password= on those files = 0; committed Test conn pattern hits = 0. F-32 signInAs = real UI path (no __E2E_ACCESS_TOKEN). F-33 reset/sign-in use untraced request.newContext. F-34 Test profile ports 5188/7188; e2e default API_URL 5188. F-35 R6 name-mismatch + R13 pending-migrations + R13a baseline unit proofs. F-36 client-safe Conflict messages. F-37/F-27 BOM/EOL pass. F-28 Icon README. F-29 CSS module. F-30 redundant unity-auth-cleared removed. F-19 form/route manifest tags include T-ANIMAL-008/S4-S6. Verify: dotnet test Api.Framework.Tests -c Release -> 45 pass / 2 skip; ui+e2e npx tsc --noEmit -> pass"
    - "d30-1 follow-up (2026-10-08T20:22:13+01:00, Neil 20:19 BST: glyph transparent): ui npx tsc --noEmit -> pass; boolean circle now drawn by <Icon knockout=\"circle\"> as ONE evenodd SVG path (circle + Check/Close), so the glyph is a transparent hole and the row / hover background shows through; --app-boolean-glyph removed; visible glyph contrast = fill vs row (light 3.35/3.36 on #fff, 3.21/3.22 on #fafafa; dark 5.61/5.75 on #2d3a4a, 4.52/4.63 on #3d4854). Rendered preview checked on white and dark rows (box, cairosvg)"

implementation:               # MANIFEST of what the implementing agent built; the reviewing agent's starting point for direct_scope: plan
  # Filled by the implementing agent at self-review / hand-off. Hand-off is BLOCKED while every list is empty.
  # One entry per file that implements the plan: files created or changed for the feature, plus
  # existing files the feature relies on to render a control or persist a mapping (change: existing).
  # `path` is repo-relative under code.api.repo (api, migrations) or code.ui.repo (ui); tests say which.
  # Never list build output, node_modules, bin/obj, generated files or secret / .env files.
  recorded_at: 2026-10-08T20:45:00+01:00   # d30-1 Request-changes fixes (F-31..F-37 + open nits); Decision 30 cycle 2 hand-back
  api:
    - path: Api.Framework.Data/Models/Animal.cs
      change: added
      tickets: [T-ANIMAL-001]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended]
      db: [Animals:Animal.Id, Animals:Animal.Name, Animals:Animal.NormalizedName, Animals:Animal.DateBorn, Animals:Animal.Attributes, Animals:Animal.IsFurry, Animals:Animal.HasHooves, Animals:Animal.IsDeleted, Animals:Animal.CreatedUtc, Animals:Animal.UpdatedUtc, Animals:Animal.UpdatedBy]
      scenarios: [T-ANIMAL-001/S1, T-ANIMAL-001/S5]
    - path: Api.Framework.Data/LoginDbContext.cs
      change: modified
      tickets: [T-ANIMAL-001]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended]
      db: [Animals:Animal.NormalizedName, Animals:Animal.Attributes, Animals:Animal.UpdatedBy]
      scenarios: [T-ANIMAL-001/S1, T-ANIMAL-001/S2, T-ANIMAL-001/S3, T-ANIMAL-001/S4, T-ANIMAL-001/S5, T-ANIMAL-001/S6, T-ANIMAL-001/S7]
    - path: Api.Framework.Data/LoginPermissions.cs
      change: modified
      tickets: [T-ANIMAL-001]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [+ Add Animal, Edit Animal, Delete Animal]
      db: []
      scenarios: [T-ANIMAL-001/S7]
    - path: Api.Framework.Services/Validation/Schemas/animalSchema.json
      change: added
      tickets: [T-ANIMAL-002, T-ANIMAL-004]
      spec_pages: [add-edit-animal]
      controls: [Name, Date Born, Attributes, Is Furry, Has Hooves]
      db: [Animals:Animal.Name, Animals:Animal.DateBorn, Animals:Animal.Attributes, Animals:Animal.IsFurry, Animals:Animal.HasHooves]
      scenarios: [T-ANIMAL-002/S5, T-ANIMAL-002/S6, T-ANIMAL-002/S7, T-ANIMAL-002/S8, T-ANIMAL-004/S1, T-ANIMAL-004/S3, T-ANIMAL-004/S6, T-ANIMAL-004/S7, T-ANIMAL-004/S9]
    - path: Api.Framework.Services/Records/AnimalRecord.cs
      change: added
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal]
      controls: [Name, Date Born, Attributes, Is Furry, Has Hooves]
      db: []
      scenarios: []
    - path: Api.Framework.Services/Records/AnimalJsonSchemaBuilder.cs
      change: added
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal]
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/FormSchemaDependenciesRegistrar.cs
      change: modified
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal]
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Animals/AnimalContracts.cs
      change: added
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended]
      db: []
      scenarios: []
    - path: Api.Framework.Services/Animals/IAnimalService.cs
      change: added
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal, manage-animals]
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Services/Animals/AnimalService.cs
      change: added
      tickets: [T-ANIMAL-002, T-ANIMAL-005]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended, Delete Animal]
      db: [Animals:Animal.Name, Animals:Animal.NormalizedName, Animals:Animal.DateBorn, Animals:Animal.Attributes, Animals:Animal.IsFurry, Animals:Animal.HasHooves, Animals:Animal.IsDeleted, Animals:Animal.CreatedUtc, Animals:Animal.UpdatedUtc, Animals:Animal.UpdatedBy]
      scenarios: [T-ANIMAL-002/S1, T-ANIMAL-002/S2, T-ANIMAL-002/S3, T-ANIMAL-002/S4, T-ANIMAL-002/S5, T-ANIMAL-002/S6, T-ANIMAL-002/S7, T-ANIMAL-002/S8, T-ANIMAL-002/S9, T-ANIMAL-002/S10, T-ANIMAL-005/S2, T-ANIMAL-005/S4]
    - path: Api.Framework.Services/Animals/AnimalPolicies.cs
      change: added
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [+ Add Animal, Edit Animal, Delete Animal]
      db: []
      scenarios: [T-ANIMAL-002/S11, T-ANIMAL-002/S12, T-ANIMAL-002/S13]
    - path: Api.Framework.Services/LoginServiceCollectionExtensions.cs
      change: modified
      tickets: [T-ANIMAL-002]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework/Program.cs
      change: modified
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal, manage-animals]
      controls: []
      db: []
      scenarios: [T-ANIMAL-002/S11, T-ANIMAL-002/S12, T-ANIMAL-002/S13]
    - path: Api.Framework/Controllers/V1/Animals/AnimalController.cs
      change: added
      tickets: [T-ANIMAL-002, T-ANIMAL-005]
      spec_pages: [add-edit-animal, manage-animals]
      controls: [+ Add Animal, Edit Animal, Delete Animal]
      db: []
      scenarios: [T-ANIMAL-002/S11, T-ANIMAL-002/S12, T-ANIMAL-002/S13, T-ANIMAL-005/S5]
    - path: Api.Framework/Controllers/V1/Schemas/AnimalSchemaController.cs
      change: added
      tickets: [T-ANIMAL-002, T-ANIMAL-004]
      spec_pages: [add-edit-animal]
      controls: []
      db: []
      scenarios: [T-ANIMAL-002/S11, T-ANIMAL-002/S12, T-ANIMAL-002/S13, T-ANIMAL-004/S11]
    - path: Api.Framework.Services/DataFramework/JsonSchemaValidation/RecordSchemaValidator.cs
      change: existing
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal]
      controls: [Name, Date Born, Attributes]
      db: []
      scenarios: []
    - path: Api.Framework.Services/DataFramework/JsonSchemaValidation/CustomValidation/DateCompareValidator.cs
      change: existing
      tickets: [T-ANIMAL-002]
      spec_pages: [add-edit-animal]
      controls: [Date Born]
      db: []
      scenarios: [T-ANIMAL-002/S5]
    - path: Api.Framework.Services/Auth/TokenService.cs
      change: existing
      tickets: [T-ANIMAL-001, T-ANIMAL-002]
      spec_pages: [add-edit-animal, manage-animals]
      controls: []
      db: []
      scenarios: [T-ANIMAL-001/S7]

    # --- Test-data scaffolding (2026-10-08, Dev Bot; Test environment only) ---
    - {path: Api.Framework.Services/TestData/TestDataOptions.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/TestDataRegistration.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/TestDataService.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/TestDataGuard.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/TestDataAccessFilter.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/Personas/AnimalsPersonasUnit.cs, change: added, tickets: [T-ANIMAL-002, T-ANIMAL-003], spec_pages: [], controls: [], db: [], scenarios: [T-ANIMAL-002/S9, T-ANIMAL-003/S3]}  # d30-1 follow-up: persona animals-tester-emailonly renamed animals-nodisplayname (animals_write, no display name; password env E2E_ANIMALS_NODISPLAYNAME_PASSWORD); same fixed GUIDs
    - {path: Api.Framework.Services/TestData/Personas/TestDataAdminPersonasUnit.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/Personas/ReferenceDataPersonasUnit.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/Animals/AnimalsPageBatch.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/Animals/AnimalsGridBatch.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: Ziggy UpdatedBy = animals-nodisplayname (list, last-amended-times, booleans)
    - {path: Api.Framework.Services/TestData/Animals/AnimalsFormBatch.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/Animals/AnimalsDeleteBatch.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Services/TestData/Animals/AnimalsApiBatch.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: animals.api.list Ziggy UpdatedBy = animals-nodisplayname
    - {path: Api.Framework.Services/TestData/Animals/AnimalsBatchSupport.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: FeaturePersonaIds uses AnimalsNoDisplayNameUserId
    - {path: Api.Framework.Services/TestData/TestDataIds.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: AnimalsTesterEmailOnly* renamed AnimalsNoDisplayName* (GUIDs unchanged)
    - {path: Api.Framework.Services/TestData/ReferenceData/ReferenceDataTypesGridBatch.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework/Controllers/V1/TestData/TestDataController.cs, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework/Program.cs, change: modified, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework/appsettings.Test.json, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework/appsettings.Production.json, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework/Properties/launchSettings.json, change: modified, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
  ui:
    - {path: src/app/examples/animals/layout.tsx, change: added, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S1]}
    - {path: src/app/examples/animals/page.tsx, change: added, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S1, T-ANIMAL-008/S2, T-ANIMAL-008/S3]}
    - {path: "src/app/examples/animals/@modal/default.tsx", change: added, tickets: [T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: []}
    - {path: "src/app/examples/animals/@modal/(.)manage/item/page.tsx", change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-003/S7]}
    - {path: "src/app/examples/animals/@modal/(.)manage/item/[id]/page.tsx", change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-003/S8, T-ANIMAL-004/S11]}
    - {path: src/app/examples/animals/manage/page.tsx, change: added, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S4, T-ANIMAL-008/S5, T-ANIMAL-008/S6]}
    - {path: src/app/examples/animals/manage/item/page.tsx, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S11]}
    - {path: "src/app/examples/animals/manage/item/[id]/page.tsx", change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S11, T-ANIMAL-004/S12]}
    - {path: src/shell/components/SiteNav.tsx, change: modified, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [Animals], db: [], scenarios: [T-ANIMAL-008/S1, T-ANIMAL-008/S2, T-ANIMAL-008/S3]}
    - {path: src/config/api-routes.ts, change: modified, tickets: [T-ANIMAL-003, T-ANIMAL-004, T-ANIMAL-005], spec_pages: [add-edit-animal, manage-animals], controls: [], db: [], scenarios: []}
    - {path: src/features/animals/shared/models/animal.model.ts, change: added, tickets: [T-ANIMAL-003, T-ANIMAL-004], spec_pages: [add-edit-animal, manage-animals], controls: [Name, Date Born, Attributes, Is Furry, Has Hooves, Last Amended], db: [], scenarios: []}
    - {path: src/features/animals/shared/utils/animal-routes.ts, change: added, tickets: [T-ANIMAL-003, T-ANIMAL-004], spec_pages: [add-edit-animal, manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-004/S11]}
    - {path: src/features/animals/shared/utils/animal-permissions.ts, change: added, tickets: [T-ANIMAL-003, T-ANIMAL-005], spec_pages: [manage-animals], controls: [+ Add Animal, Edit Animal, Delete Animal], db: [], scenarios: [T-ANIMAL-008/S2, T-ANIMAL-008/S3, T-ANIMAL-005/S5]}
    - {path: src/features/animals/shared/utils/use-animals-access.ts, change: added, tickets: [T-ANIMAL-003, T-ANIMAL-004], spec_pages: [add-edit-animal, manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S2, T-ANIMAL-008/S3, T-ANIMAL-004/S11]}
    - {path: src/features/animals/shared/components/AnimalsAccessNotice.tsx, change: added, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S2, T-ANIMAL-008/S3]}
    - {path: src/features/animals/shared/state/animals-update.service.ts, change: added, tickets: [T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-005/S2]}
    - {path: src/features/animals/shared/routes/AnimalsModalRoutes.tsx, change: added, tickets: [T-ANIMAL-003, T-ANIMAL-004], spec_pages: [add-edit-animal, manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-003/S7, T-ANIMAL-003/S8, T-ANIMAL-008/S2, T-ANIMAL-004/S11]}
    - {path: src/features/animals/manage-animals/ManageAnimalsPage.tsx, change: added, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S1, T-ANIMAL-008/S2, T-ANIMAL-008/S3]}
    - {path: src/features/animals/manage-animals/ManageAnimals.tsx, change: added, tickets: [T-ANIMAL-003, T-ANIMAL-005], spec_pages: [manage-animals], controls: [Delete Animal], db: [], scenarios: [T-ANIMAL-008/S1, T-ANIMAL-005/S1, T-ANIMAL-005/S2, T-ANIMAL-005/S3]}
    - {path: src/features/animals/manage-animals/AnimalsGrid.tsx, change: added, tickets: [T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-003/S2]}
    - {path: src/features/animals/manage-animals/use-animals-grid.tsx, change: modified, tickets: [T-ANIMAL-003, T-ANIMAL-005, T-ANIMAL-007, T-ANIMAL-004], spec_pages: [manage-animals, add-edit-animal], controls: [+ Add Animal, Edit Animal, Delete Animal], db: [], scenarios: [T-ANIMAL-003/S6, T-ANIMAL-003/S7, T-ANIMAL-003/S8, T-ANIMAL-003/S9, T-ANIMAL-005/S1, T-ANIMAL-005/S2, T-ANIMAL-005/S5, T-ANIMAL-004/S1, T-ANIMAL-004/S2]}  # open(..., pending) so Add/Edit shell + CompanyLoader paint on click
    - {path: src/features/animals/manage-animals/columns/animals-grid-columns.tsx, change: modified, tickets: [T-ANIMAL-003, T-ANIMAL-009], spec_pages: [manage-animals], controls: [Name, Is Furry, Has Hooves, Date Born, Attributes, Last Amended], db: [Animals:Animal.Name, Animals:Animal.IsFurry, Animals:Animal.HasHooves, Animals:Animal.DateBorn, Animals:Animal.Attributes, Animals:Animal.UpdatedUtc], scenarios: [T-ANIMAL-003/S2, T-ANIMAL-003/S14, T-ANIMAL-003/S15, T-ANIMAL-009/S1, T-ANIMAL-009/S2, T-ANIMAL-009/S5]}
    - {path: src/features/animals/manage-animals/state/animals-search.data-provider.ts, change: added, tickets: [T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-003/S2, T-ANIMAL-003/S6]}
    - {path: src/features/animals/animal-form-modal/AnimalFormModal.tsx, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-008], spec_pages: [add-edit-animal], controls: [Save, Cancel], db: [], scenarios: [T-ANIMAL-004/S1, T-ANIMAL-004/S2, T-ANIMAL-004/S3, T-ANIMAL-004/S4, T-ANIMAL-004/S5, T-ANIMAL-004/S6, T-ANIMAL-004/S7, T-ANIMAL-004/S8, T-ANIMAL-004/S9, T-ANIMAL-004/S10, T-ANIMAL-004/S11, T-ANIMAL-004/S12, T-ANIMAL-008/S4, T-ANIMAL-008/S5, T-ANIMAL-008/S6]}  # loading={schemaLoading || !formVm}; modal opens with CompanyLoader while schema/record load
    - {path: src/features/animals/animal-form-modal/state/animal-entity.data-provider.ts, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S2, T-ANIMAL-004/S10, T-ANIMAL-004/S12]}
    - {path: src/features/animals/animal-form-modal/state/animal-ui-schema.ts, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    - {path: src/features/animals/animal-form-modal/ui-schemas/animal.ui-schema.json, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [Name, Date Born, Attributes, Is Furry, Has Hooves], db: [], scenarios: [T-ANIMAL-004/S1]}
    - {path: src/framework/auth/permissions.ts, change: added, tickets: [T-ANIMAL-007, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-007/S3, T-ANIMAL-007/S4, T-ANIMAL-007/S5]}
    - {path: src/framework/auth/normalize-auth-state.ts, change: added, tickets: [T-ANIMAL-001, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-001/S7, T-ANIMAL-008/S2]}
    - {path: src/framework/auth/providers/authorisation.data-provider.ts, change: modified, tickets: [T-ANIMAL-001, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-001/S7, T-ANIMAL-008/S2]}
    - {path: src/framework/auth/token-refresh.service.ts, change: modified, tickets: [T-ANIMAL-001, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-001/S7, T-ANIMAL-008/S2]}
    - {path: src/framework/design-system/forms/switch/Switch.tsx, change: modified, tickets: [T-ANIMAL-006], spec_pages: [add-edit-animal, manage-animals], controls: [Is Furry, Has Hooves], db: [], scenarios: [T-ANIMAL-006/S1, T-ANIMAL-006/S4, T-ANIMAL-006/S5]}
    - {path: src/framework/design-system/forms/switch/Switch.module.css, change: modified, tickets: [T-ANIMAL-006], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: src/framework/design-system/components/icon/Icon.tsx, change: modified, tickets: [T-ANIMAL-009, T-ANIMAL-007], spec_pages: [manage-animals], controls: [Is Furry, Has Hooves, Edit Animal, Delete Animal], db: [], scenarios: [T-ANIMAL-009/S1, T-ANIMAL-009/S2]}  # d30-1 follow-up: knockout="circle" variant (circle + glyph in one evenodd path; glyph is a transparent hole)
    - {path: src/framework/design-system/index.ts, change: modified, tickets: [T-ANIMAL-006, T-ANIMAL-004], spec_pages: [], controls: [], db: [], scenarios: []}  # exports CompanyLoader, PendingRoutedModalHost, RoutedModalLoadingFallback
    - {path: src/framework/json-schema-form/components/renderers/unity-json-form-renderers.tsx, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-006], spec_pages: [add-edit-animal], controls: [Name, Date Born, Attributes, Is Furry, Has Hooves], db: [], scenarios: [T-ANIMAL-006/S1, T-ANIMAL-006/S2, T-ANIMAL-006/S3, T-ANIMAL-006/S4]}
    - {path: src/framework/json-schema-form/components/JsonSchemaForm.tsx, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    - {path: src/framework/json-schema-form/components/JsonSchemaForm.module.css, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-006], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: src/framework/json-schema-form/validation/unity-schema-validation.ts, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [Name, Date Born, Attributes], db: [], scenarios: [T-ANIMAL-004/S3, T-ANIMAL-004/S6, T-ANIMAL-004/S7, T-ANIMAL-004/S9, T-ANIMAL-006/S3]}
    - {path: src/framework/json-schema-form/hooks/use-json-schema-entity-form.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [Save], db: [], scenarios: [T-ANIMAL-004/S2, T-ANIMAL-004/S4, T-ANIMAL-004/S10]}  # schemaLoading starts true (and stays true on reset) so RoutedModal never paints an empty body
    - {path: src/framework/json-schema-form/models/unity-json-schema.model.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    - {path: src/framework/json-schema-form/schema/unity-schema-api.mapper.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [Attributes, Date Born], db: [], scenarios: []}
    - {path: src/framework/json-schema-form/schema/unity-schema.adapter.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [Is Furry, Has Hooves, Attributes], db: [], scenarios: [T-ANIMAL-004/S1]}
    - {path: src/framework/json-schema-form/schema/unity-schema-value.mapper.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [Attributes], db: [], scenarios: [T-ANIMAL-002/S2, T-ANIMAL-004/S8]}
    - {path: src/framework/json-schema-form/index.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: src/framework/entity-framework/utils/api-error.utils.ts, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-005], spec_pages: [add-edit-animal, manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-004/S4]}
    - {path: src/framework/entity-framework/providers/abstract-entity.data-provider.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S4]}
    - {path: src/framework/entity-framework/index.ts, change: modified, tickets: [T-ANIMAL-009, T-ANIMAL-003], spec_pages: [manage-animals], controls: [Is Furry, Has Hooves], db: [], scenarios: [T-ANIMAL-009/S6]}
    - {path: src/framework/entity-framework/grid/grid-column.ts, change: modified, tickets: [T-ANIMAL-007], spec_pages: [manage-animals], controls: [Edit Animal, Delete Animal], db: [], scenarios: [T-ANIMAL-007/S3, T-ANIMAL-007/S4, T-ANIMAL-007/S6, T-ANIMAL-007/S7]}
    - {path: src/framework/entity-framework/grid/entity-grid-config.ts, change: modified, tickets: [T-ANIMAL-007], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-007/S1, T-ANIMAL-007/S8]}
    - {path: src/framework/entity-framework/grid/grid-cell-renderers.module.css, change: added, tickets: [T-ANIMAL-009], spec_pages: [manage-animals], controls: [Is Furry, Has Hooves], db: [], scenarios: [T-ANIMAL-009/S1, T-ANIMAL-009/S2]}
    - {path: src/framework/entity-framework/grid/grid-cell-renderers.tsx, change: modified, tickets: [T-ANIMAL-009, T-ANIMAL-003, T-ANIMAL-006], spec_pages: [manage-animals], controls: [Is Furry, Has Hooves, Date Born, Attributes], db: [Animals:Animal.IsFurry, Animals:Animal.HasHooves, Animals:Animal.DateBorn, Animals:Animal.Attributes], scenarios: [T-ANIMAL-009/S1, T-ANIMAL-009/S2, T-ANIMAL-009/S3, T-ANIMAL-009/S4, T-ANIMAL-009/S5, T-ANIMAL-009/S6, T-ANIMAL-009/S7, T-ANIMAL-009/S8, T-ANIMAL-003/S14, T-ANIMAL-003/S15, T-ANIMAL-006/S5]}  # Decision 30 + d30-1 follow-up: filled circle with the Check/Close glyph cut out (transparent, row shows through); renderBooleanSwitchCell kept
    - {path: src/framework/entity-framework/components/entity-grid/EntityGrid.tsx, change: modified, tickets: [T-ANIMAL-007, T-ANIMAL-003], spec_pages: [manage-animals], controls: [+ Add Animal, Actions], db: [], scenarios: [T-ANIMAL-007/S1, T-ANIMAL-007/S2, T-ANIMAL-007/S3, T-ANIMAL-007/S4, T-ANIMAL-007/S5, T-ANIMAL-007/S6, T-ANIMAL-007/S7, T-ANIMAL-007/S8, T-ANIMAL-003/S7, T-ANIMAL-003/S9]}  # d30-1 follow-up: optional sessionPermissions prop (defaults to the signed-in session) so the dev-only harness drives the real grid; product pages do not pass it
    - {path: src/framework/entity-framework/components/entity-grid/EntityGridRowActionsMenu.tsx, change: added, tickets: [T-ANIMAL-007], spec_pages: [manage-animals], controls: [Edit Animal, Delete Animal], db: [], scenarios: [T-ANIMAL-007/S1, T-ANIMAL-007/S2, T-ANIMAL-007/S7, T-ANIMAL-007/S9, T-ANIMAL-003/S9]}
    - {path: src/framework/entity-framework/components/entity-grid/EntityGrid.module.css, change: modified, tickets: [T-ANIMAL-007], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: src/framework/design-system/components/modal/Modal.tsx, change: modified, tickets: [T-ANIMAL-005, T-ANIMAL-007, T-ANIMAL-004], spec_pages: [manage-animals, add-edit-animal], controls: [Delete Animal], db: [], scenarios: [T-ANIMAL-005/S3, T-ANIMAL-007/S9]}  # shared body scroll-lock counter (pending shell → real RoutedModal overlap)
    - {path: src/framework/design-system/components/modal/ConfirmModal.tsx, change: modified, tickets: [T-ANIMAL-005], spec_pages: [manage-animals], controls: [Delete Animal], db: [], scenarios: [T-ANIMAL-005/S1, T-ANIMAL-005/S2, T-ANIMAL-005/S3]}
    - {path: src/framework/design-system/components/modal/RoutedModal.tsx, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S11]}  # clears pending shell on mount (layout effect)
    - {path: src/framework/design-system/theme/tokens.css, change: modified, tickets: [T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-004, T-ANIMAL-009], spec_pages: [add-edit-animal, manage-animals], controls: [+ Add Animal, Actions, Is Furry, Has Hooves, Attributes], db: [], scenarios: [T-ANIMAL-009/S7, T-ANIMAL-009/S8]}  # Decision 30 fills; + --app-loader-backdrop-bg-strong (light/dark) for CompanyLoader overlay
    - {path: src/framework/entity-framework/components/entity-grid-auth-gate/EntityGridAuthGate.tsx, change: existing, tickets: [T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S2]}
    - {path: src/framework/auth/context/AuthProvider.tsx, change: existing, tickets: [T-ANIMAL-003, T-ANIMAL-007], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S2, T-ANIMAL-007/S3]}
    - {path: .cursor/rules/framework/nextjs-list-pages.mdc, change: added, tickets: [T-ANIMAL-008, T-ANIMAL-003], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-008/S1]}
    - {path: src/framework/design-system/components/menu/DropdownMenu.tsx, change: added, tickets: [T-ANIMAL-007], spec_pages: [manage-animals], controls: [Actions, Edit Animal, Delete Animal], db: [], scenarios: [T-ANIMAL-007/S1, T-ANIMAL-007/S2]}
    - {path: src/framework/design-system/components/menu/DropdownMenu.module.css, change: added, tickets: [T-ANIMAL-007], spec_pages: [manage-animals], controls: [Actions], db: [], scenarios: [T-ANIMAL-007/S1]}
    - {path: src/framework/design-system/components/modal/use-modal-navigate.ts, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-008], spec_pages: [add-edit-animal, manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-004/S1, T-ANIMAL-004/S2]}  # open(href, pending?) paints PendingRoutedModalHost on click
    - {path: src/framework/json-schema-form/services/json-schema-data.service.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S1, T-ANIMAL-004/S11]}
    - {path: src/framework/api/unity-api-fetch.ts, change: modified, tickets: [T-ANIMAL-001, T-ANIMAL-003, T-ANIMAL-008], spec_pages: [manage-animals], controls: [], db: [], scenarios: [T-ANIMAL-001/S7, T-ANIMAL-008/S1]}
    - {path: src/features/design-system-showcase/DesignSystemShowcase.tsx, change: modified, tickets: [T-ANIMAL-007], spec_pages: [], controls: [Actions], db: [], scenarios: [T-ANIMAL-007/S1]}
    - {path: src/framework/design-system/buttons/button/Button.module.css, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-007], spec_pages: [add-edit-animal, manage-animals], controls: [+ Add Animal, Actions], db: [], scenarios: []}
    - {path: src/framework/design-system/components/modal/ModalShell.module.css, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}  # Unity company-loader overlay; body min-height 40rem while loading
    - {path: src/framework/auth/storage/unity-cookie.service.ts, change: modified, tickets: [T-ANIMAL-001, T-ANIMAL-004], spec_pages: [manage-animals, add-edit-animal], controls: [], db: [], scenarios: []}



    # --- Instant form-modal open + Unity CompanyLoader (Neil 20:22 BST) ---
    - {path: src/framework/design-system/components/loader/CompanyLoader.tsx, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}  # port of Unity app-company-loader
    - {path: src/framework/design-system/components/loader/CompanyLoader.module.css, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    - {path: src/framework/design-system/components/modal/ModalShell.tsx, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}  # uses CompanyLoader (Unity form-modal loading pattern)
    - {path: src/framework/design-system/components/modal/pending-routed-modal.ts, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    - {path: src/framework/design-system/components/modal/PendingRoutedModalHost.tsx, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}  # root-layout host; shell on click before route
    - {path: src/framework/design-system/components/modal/RoutedModalLoadingFallback.tsx, change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    - {path: src/app/layout.tsx, change: modified, tickets: [T-ANIMAL-004], spec_pages: [], controls: [], db: [], scenarios: []}  # mounts PendingRoutedModalHost
    - {path: "src/app/examples/animals/@modal/(.)manage/item/loading.tsx", change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S1]}
    - {path: "src/app/examples/animals/@modal/(.)manage/item/[id]/loading.tsx", change: added, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: [T-ANIMAL-004/S2]}
    - {path: src/features/reference-data/reference-data-item-form-modal/ReferenceDataItemFormModal.tsx, change: modified, tickets: [T-ANIMAL-004], spec_pages: [], controls: [], db: [], scenarios: []}  # same loading={schemaLoading || !formVm} pattern
    - {path: src/features/reference-data/manage-reference-data-items-modal/use-reference-data-items-grid.ts, change: modified, tickets: [T-ANIMAL-004], spec_pages: [], controls: [], db: [], scenarios: []}  # open(..., pending)
    - {path: .cursor/rules/framework/nextjs-modal-routing.mdc, change: modified, tickets: [T-ANIMAL-004, T-ANIMAL-008], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}  # standing rule: open immediately, load inside
    - {path: .cursor/rules/framework/nextjs-json-schema-forms.mdc, change: modified, tickets: [T-ANIMAL-004], spec_pages: [add-edit-animal], controls: [], db: [], scenarios: []}
    # --- Component harness + F-26/F-28 (test scaffolding pass) ---
    - {path: src/features/test-harness/ComponentTestHarness.tsx, change: added, tickets: [T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-009], spec_pages: [], controls: [], db: [], scenarios: [T-ANIMAL-006/S1, T-ANIMAL-006/S2, T-ANIMAL-006/S4, T-ANIMAL-007/S3, T-ANIMAL-007/S4, T-ANIMAL-007/S5, T-ANIMAL-007/S6, T-ANIMAL-007/S7, T-ANIMAL-009/S4, T-ANIMAL-009/S5, T-ANIMAL-009/S6]}  # d30-1 follow-up: row actions now on the real EntityGrid (menu) - grids harness-grid-permissions (S3/S4, incl. no-permission "Open"), -all-require (S5), -per-row (S6), -zero-visible (S7); form/switch JSON readouts (harness-json-form-value*, harness-switch-value); bool cells add undefined + custom Furry / Not furry. T-009 S7/S8 stay on the Animals page
    - {path: src/app/examples/test-harness/page.tsx, change: added, tickets: [T-ANIMAL-006, T-ANIMAL-007, T-ANIMAL-009], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up (Neil 20:09 BST): production guard - notFound() when NODE_ENV === production (e2e runs on next dev); robots noindex; not linked from SiteNav or any nav
    - {path: src/framework/design-system/README.md, change: modified, tickets: [T-ANIMAL-009], spec_pages: [], controls: [], db: [], scenarios: []}
  tests:
    - {path: Api.Framework.Tests/Api.Framework.Tests.csproj, repo: api, change: added, tickets: [T-ANIMAL-001, T-ANIMAL-002], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Tests/Helpers/TestDbFactory.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Tests/TestData/TestDataRegistrationTests.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Tests/TestData/SeedOrderTests.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Tests/TestData/TestPersonaTests.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: asserts animals-nodisplayname / E2E_ANIMALS_NODISPLAYNAME_PASSWORD (21/21 pass, Release)
    - {path: Api.Framework.Tests/TestData/TestDataGuardAndServiceTests.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Tests/TestData/TestDataAccessFilterTests.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: Api.Framework.Tests/TestData/AnimalsFormBatchTests.cs, repo: api, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/package.json, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/playwright.config.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/global-setup.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/helpers/config.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/helpers/selectors.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/helpers/authentication.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/helpers/test-data.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/helpers/wait-for-response.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/support/personas.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: exports personaNames (animals-nodisplayname replaces animals-tester-emailonly)
    - {path: e2e/features/common/fixtures.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/features/common/test-data.steps.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/scripts/reset-master.ts, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}
    - {path: e2e/README.md, repo: ui, change: added, tickets: [], spec_pages: [], controls: [], db: [], scenarios: []}  # d30-1 follow-up: persona/env rename, harness prod guard, harness data-tid table
  # 2026-10-08 scaffolding (Dev Bot): Api.Framework.Tests + Playwright/playwright-bdd e2e + reset endpoint/personas/batches ready for Test Bot. Scenario .feature files are Test Bot's. Plan Bot: set testing.e2e.nextjs.path to ai-code-framework/ui/UI.NextJs.Framework/e2e (drop placeholder).
  # 20261008131327_AddAnimals (auth.animals) was removed with `ef migrations remove --force` and regenerated as 20261008150221_AddAnimals (Q27).
  migrations:
    - path: Api.Framework.Data/Migrations/20261008150221_AddAnimals.cs
      change: added
      tickets: [T-ANIMAL-001]
      spec_pages: [add-edit-animal, manage-animals]
      controls: []
      db: [Animals:Animal.Id, Animals:Animal.Name, Animals:Animal.NormalizedName, Animals:Animal.DateBorn, Animals:Animal.Attributes, Animals:Animal.IsFurry, Animals:Animal.HasHooves, Animals:Animal.IsDeleted, Animals:Animal.CreatedUtc, Animals:Animal.UpdatedUtc, Animals:Animal.UpdatedBy]
      scenarios: [T-ANIMAL-001/S1, T-ANIMAL-001/S2, T-ANIMAL-001/S3, T-ANIMAL-001/S4, T-ANIMAL-001/S5, T-ANIMAL-001/S6, T-ANIMAL-001/S7]
    - path: Api.Framework.Data/Migrations/20261008150221_AddAnimals.Designer.cs
      change: added
      tickets: [T-ANIMAL-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: []
    - path: Api.Framework.Data/Migrations/LoginDbContextModelSnapshot.cs
      change: modified
      tickets: [T-ANIMAL-001]
      spec_pages: []
      controls: []
      db: []
      scenarios: [T-ANIMAL-001/S6, T-ANIMAL-001/S7]
  # Entry shape (copy into the lists above):
  #  - path: Api.Framework/Controllers/V1/<Area>/<Name>Controller.cs
  #    repo: api               # api | ui  (tests only; api / migrations are always api, ui is ui)
  #    change: added           # added | modified | existing
  #    tickets: [T-<DOMAIN>-NNN]
  #    spec_pages: [<page>]    # specs/<page>.yaml
  #    controls: [<label>]     # spec control labels, manage-list columns or actions
  #    db: [<Service>:<Table>.<Column>]   # spec Service / Target DB Table / Target DB Column (or Population Source)
  #    scenarios: [T-<DOMAIN>-NNN/S1]     # mainly for tests

pull_requests: []             # when code_to_review = pr; one entry per repo
#  - repo: ai-code-framework/api/Unity.API
#    id: 1234
#    url: https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/1234
#    source_branch: feat/T-CONTACT-001/add-edit-contact
#    target_branch: <review.target_branch>

review:
  cycle: 2                    # Decision 30 review cycle 2 (d30-1 Request changes fixed; fresh code re-review). Test-fix rounds do NOT count here
  report: reviews/DIRECT-manage-animals-d30-2-review.md   # Decision 30 cycle 2 (d30-1 kept on disk: Request changes, F-31 Blocker - resolved in d30-2)
  log: reviews/review-log.md  # reviews/review-log.md (review.log_file); every code review and test review, both routes
  code_verdict: approve-with-comments   # d30-2 (2026-10-08T20:52 BST) + code delta 09:08/09:35 BST reviewed in test review round 3 (2026-10-09T09:58): F-38/F-39/F-40 resolved, F-46 code defect fixed; open Nits F-50, F-52, F-55; note F-53
  test_verdict: approve         # test review round 3 (2026-10-09T09:58 BST, test-fix 1/5): 77/0/0, T-007/S8 unblocked and passing; F-41..F-48 resolved; open Nits F-51, F-56. Round 2 was request-changes (09:05)
  verdict: approve-with-comments   # FINAL 2026-10-09T09:58 BST: code_review + test_review both met (testing.final_approval_requires). Open: Nits F-50, F-51, F-52, F-55, F-56; note F-53. Neil decides merge
  routed_to: human            # no fixes required; human owner (Neil) for merge + password rotation (template lists code | testing | both; "human" per pipeline instruction)
  reviewed_commits: {api: "not under git", ui: "not under git"}
  # 2026-10-08T20:04:30+01:00 dev-bot: Decision 30 filled-circle UI + scaffolding confirmed; option-B hand-off. d29-1 Approve (19:45 / report d29-1) is SUPERSEDED — do not merge on it. Fresh Decision 30 cycle starts at cycle 0; Review Bot sets cycle 1 on pickup. approvals.merge left unset (Neil only).
  # (kept) d29-1 record: code approve-with-comments / test blocked-noted / final approve-with-comments at 19:45; superseded_by Decision 30 (Neil 19:57). Earlier rounds 1-3 reports kept on disk.
  # (kept) Round-3 report/log kept on disk (Approve with comments covers code up to Decision 28).
testing:                      # CARVE-OUT: written ONLY by the testing agent (test-bot), also while review-bot owns the feature.
  # Seeded from handoff/templates/handoff.md by plan-bot 2026-10-08T19:23:05+01:00 (Neil 19:19 BST: separate test-fix cap); test-bot fills it in. Rules: handoff/README.md -> Testing alongside review.
  # Run 1 picked up by test-bot 2026-10-08T19:24:27+01:00 (status running); finished 2026-10-08T19:27:45+01:00. First run, not a fix re-run.
  # 2026-10-08T20:08+01:00 test-bot: plan update only (no tests written or run). Tickets re-read 20:06 BST: Decision 30 (T-009 S1/S2/S5 reworded, S7/S8 new; T-003 S14/S15 reworded),
  # role personas for T-002 S9 / T-003 S3. Scaffolding verified on disk read-only (Api.Framework.Tests, e2e/, TestData reset + personas, /examples/test-harness): code-owner blockers dropped.
  # Component rows planned on the harness page (Neil 20:04 BST, Playwright). Local run target: UI :3003, API :5088/:7088, Docker Postgres :5432, separate DB api_framework_test only.
  # 2026-10-08T20:28+01:00 test-bot: scenario tests WRITTEN for all 77 IDs (unit Api.Framework.Tests/Animals + e2e features under UI.NextJs.Framework/e2e/features). Unit Release run: 22 Animals Facts, 20 pass + 2 Skip (scaffolding gap);
  # full project 43 total, 0 failed. E2e/harness NOT run (Neil has not pointed Test at api_framework_test / set secrets): tsc pass; bddgen + playwright --list = 64 scenarios (with @playwright/test 1.56.1; lockfile 1.64.0 breaks bddgen - owner code).
  # 2026-10-08T20:33+01:00 test-bot: boolean cells moved to the knock-out glyph (Icon knockout="circle", no --app-boolean-glyph). T-003 S14/S15, T-009 S7/S8 steps rewritten: fill = cell computed color, no glyph colour/#18181b; glyph token asserted undefined. Not run.
  # 2026-10-09T08:50+01:00 test-bot: ROUND 2 = first real run (test_fix_cycle 0). Safety gate: Database=api_framework_test @ localhost:5432. Test API (profile Test, :5188/:7188) + UI (:3003) started fresh with user env.
  # Unit Release 00:55 BST: 47 total, 45 pass, 2 Skip, 0 fail. E2e/harness: run 2 (07:35) 19/45 - env: UI .env.local API root = dev API :7088 (not running); UI restarted with process env
  # NEXT_PUBLIC_UNITY_API_ROOT=https://localhost:7188/v1/ (no file edited). Runs 3-4 exposed test defects, self-fixed before reporting (F1-F6, see report). Run 5 (08:36 BST): 64/64 pass. T-007 S8 @skip (not run).
  # 2026-10-09T09:26+01:00 test-bot: ROUND 3 = test-fix round 1 of 5 (Review Bot test review d30-2: F-41..F-47). Safety gate before every run: Database=api_framework_test @ localhost:5432.
  # T-007/S8 was then awaiting Plan Bot / Neil (unblocked in Addendum 2). F-41: scenario steps never type a password; scan 0 hits in report, traces, error-context, .auth, logs, trx (incl. a failed-scenario trace). Residual: note (5).
  # Dev Bot changed code + e2e scaffolding at 09:08 BST mid-round; services restarted on the new code (UI via npm run dev:test) and the suite re-run: unit 52/52, e2e 66/66 + 6 setup sign-ins (run 9).
  # 2026-10-09T09:48+01:00 test-bot: ADDENDUM to round 3 (round and test_fix_cycle unchanged). Dev Bot 09:27 asks: api.steps.ts request-context comment corrected; "no animal form modal" now covers -fallback / -pending / -shell / -loading.
  # Run on Dev Bot 09:35 code (e2e setup files 09:30:01, API code unchanged since 09:10, UI restarted 09:40:41): unit 52/52 (09:42), e2e 66/66 + 6 setup (run 10, 09:42-09:45 BST), scan 0. --trace=on probe 09:41: leak fixed.
  # 2026-10-09T09:56+01:00 test-bot: ADDENDUM 2 to round 3 (round 3, test_fix_cycle 1; no review returned, nothing routed). Neil confirmed T-007/S8 at 09:46 (Plan Bot 09:47): @fixme @skip removed,
  # scenario rewritten to the confirmed baseline (EXAMPLE_STATUS, SHOWCASE_OPTION, 2 active items each; reset reference-data.types-grid.baseline; reference-data-tester). S8 passes. Full e2e run 11 (09:49-09:52 BST):
  # 67/67 + 6 setup; unit not re-run (no API or unit change; 52/52 at 09:42). Scan 0. All 77 pass -> status passed.
  status: passed              # pending | running | passed | failed | blocked   (running = the testing agent has picked the run up)
  round: 3                    # +1 per test run; n in tests/TEST-<feature>-<n>-report.md
  test_fix_cycle: 1           # test-fix rounds used / max testing.max_test_fix_cycles (5); separate from review.cycle. +1 when the testing agent
                              # starts the re-run after a failure was routed back (code or test defect); at max, the next one escalates to Neil
  plan: tests/test-plan.md
  report: tests/TEST-manage-animals-3-report.md
  summary:                    # round 3 (2026-10-09, Addendum 2): all 77 pass. Unit 52/52 pass; e2e + harness 67/67 pass (run 11) + 6 setup sign-ins; 0 fail, 0 blocked
    scenarios: 77
    passed: 77
    failed: 0
    blocked: 0
    waiting: 0
    not_automated: 0
  results:                    # one entry per scenario, keyed by the ticket's explicit ID (testing.scenario_ids: explicit)
    - scenario: T-ANIMAL-001/S1
      layers: [unit]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalModelMetadataTests.cs::AnimalTable_StoresAllMappedColumns"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST)."
    - scenario: T-ANIMAL-001/S2
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalModelMetadataTests.cs::Attributes_DefaultSql_IsEmptyJsonArray"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Attributes default to an empty array via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-001/S3
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalModelMetadataTests.cs::NormalisedName_HasFilteredUniqueIndexAmongNonDeleted"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Duplicate normalised name is rejected by the database and the service"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-001/S4
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceListDeleteTests.cs::SoftDeletedName_CanBeReused_OnCreate"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Soft-deleted animal name can be reused"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-001/S5
      layers: [unit]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalModelMetadataTests.cs::SoftDeletedFlag_Exists_WithDefaultFalse"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST)."
    - scenario: T-ANIMAL-001/S6
      layers: [unit]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalModelMetadataTests.cs::Table_LivesInCreaturesSchema"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST)."
    - scenario: T-ANIMAL-001/S7
      layers: [unit]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalModelMetadataTests.cs::AnimalsWritePermission_IsSeeded_ForStandardAndAdministrators"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST)."
    - scenario: T-ANIMAL-002/S1
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_ValidFields_PersistsAnimal"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Create animal with valid fields via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S2
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_MissingAttributes_StoresEmptyArray"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Missing Attributes are stored as an empty array via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S3
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_DuplicateName_RejectedWithExactMessage"
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_DatabaseUniqueViolation_MapsToDuplicateMessage"
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Update_ToDuplicateName_RejectedAndOriginalUnchanged"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Duplicate normalised name is rejected by the database and the service"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S4
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_NameOfSoftDeleted_Succeeds"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Soft-deleted animal name can be reused"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S5
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_DateBornTodayOrLater_FailsWithExactMessage"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Date Born must be before today via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST). DateCompareValidator now uses the injected TimeProvider (Dev Bot 09:08 BST); earlier finding closed."
    - scenario: T-ANIMAL-002/S6
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_DateBornMissing_FailsWithExactMessage"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Date Born is mandatory via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S7
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_NameMissing_FailsWithExactMessage"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Name is mandatory via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S8
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceCreateTests.cs::Create_AttributeTagLimits_FailWithExactMessages"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Attribute tag limits via the API"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S9
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceListDeleteTests.cs::List_ReturnsNonDeleted_WithLastAmendedDisplayNameOrEmail"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::List returns non-deleted animals with Last Amended user"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S10
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalServiceListDeleteTests.cs::Delete_SoftDeletes_AndGetUpdateDeleteReturnNotFound"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Soft delete then not found on get update delete"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S11
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalPoliciesTests.cs::AnimalEndpoints_RejectUsersWithoutAnimalsWrite_ByPolicy"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Users without animals_write are rejected on every endpoint"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST). F-42: reflection Fact implemented and un-skipped (no anonymous access; effective policy needs the animals_write claim; IAuthorizationService refuses user_management_write only). F-43: denied POST / PUT send a valid body, then read-back as animals-tester: Bessie unchanged (full body equal) and the list is Bessie only."
    - scenario: T-ANIMAL-002/S12
      layers: [api-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::User-management permissions alone do not grant animals access"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-002/S13
      layers: [unit, api-e2e]
      tests:
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalPoliciesTests.cs::AnimalsWritePolicy_RequiresTheAnimalsWritePermissionClaim"
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalPoliciesTests.cs::AllAnimalEndpoints_RequireAnimalsWritePolicy"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::AnimalsWrite succeeds on every animal endpoint"
        - "ai-code-framework/api/API.Framework/Api.Framework.Tests/Animals/AnimalPoliciesTests.cs::ProgramCs_RegistersExactlyOneAnimalsPolicy_AnimalsWrite_RequiringThePermissionClaim"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AnimalsApi.feature::Without AnimalsWrite create update and delete are forbidden"
      result: passed
      note: "Round 3: unit pass (Release 09:42 BST); e2e pass (run 11, 09:52 BST). F-42: Program.cs host captured without starting it (HostBuilt): exactly one animals policy, AnimalsWrite, one ClaimsAuthorizationRequirement permission = [animals_write]; every animal action carries it. F-43: create, update (read back) and delete succeed as animals-tester; second scenario: animals-viewer gets 403 on create, update and delete."
    - scenario: T-ANIMAL-003/S2
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::List shows non-deleted animals with attributes as comma-separated tags"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S3
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Last Amended shows date, time and user display name or email"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S4
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Last Amended is shown in the browser's local time (BST)"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S5
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Last Amended outside summer time (GMT)"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S6
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Default sort by Name ascending"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S7
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Add opens the animal form"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S8
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Edit opens the animal form with existing data"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S9
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Row actions menu in the last column; row click does nothing"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S12
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Results are paged on the server"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S13
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::No animals to show"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S14
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::True shows a green circle with a tick, accessible name Yes"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-003/S15
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S1
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Add mode opens with defaults"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S2
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Create animal with required fields"
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Date Born typed as soon as the Add form opens is kept"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). F-46: no-retry check (Date Born typed once as soon as the Add form shows, value kept after 3 s) passes on the code before and after Dev Bot 09:08 changes (runs 6 and 9); no input loss seen, so no code defect."
    - scenario: T-ANIMAL-004/S3
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Name is mandatory"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S4
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Duplicate name is rejected on Save"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S5
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Name of a deleted animal can be reused"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S6
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Date Born must be before today"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S7
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Date Born is mandatory"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S8
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Attributes persist as JSON tags"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S9
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Attribute tag limits on the form"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S10
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Edit persists changed fields"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S11
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Only Add and Edit modes exist"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-004/S12
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Deleted animal cannot be opened"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-005/S1
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/DeleteAnimal.feature::Confirmation names the animal"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-005/S2
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/DeleteAnimal.feature::Soft delete removes row from the list"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-005/S3
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/DeleteAnimal.feature::Cancel leaves the animal unchanged"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-005/S4
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/DeleteAnimal.feature::Deleted animal is gone everywhere but its name is free"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-005/S5
      layers: [ui-e2e, api-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/DeleteAnimal.feature::Users without animals_write cannot delete"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-006/S1
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Switch renders and binds a boolean"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-006/S2
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Tag Input adds and removes chips"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-006/S3
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/AddEditAnimal.feature::Attribute tag limits on the form"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). Covered by the T-ANIMAL-004/S9 test (carries both tags)."
    - scenario: T-ANIMAL-006/S4
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Read-only Switch and Tag Input"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-006/S5
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::List shows non-deleted animals with attributes as comma-separated tags"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). Covered by the T-ANIMAL-003/S2 test (carries both tags)."
    - scenario: T-ANIMAL-007/S1
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Row actions menu in the last column; row click does nothing"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). Covered by the T-ANIMAL-003/S9 test (carries both tags)."
    - scenario: T-ANIMAL-007/S2
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Choosing Edit Animal runs it for that row only"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-007/S3
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Items are hidden without the required permission"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-007/S4
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Any one of several permissions is enough"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-007/S5
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::No Actions column when no item is allowed"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-007/S6
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Per-row visibility hides Delete for Bessie"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-007/S7
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::A row with no visible items has no trigger"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-007/S8
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/reference-data/ReferenceDataTypesGrid.feature::Existing text-button grids are unaffected"
      result: passed
      note: "Round 3 Addendum 2: e2e pass (run 11, 09:52 BST). Unblocked after Neil confirmed the baseline at 09:46: exactly EXAMPLE_STATUS then SHOWCASE_OPTION (Active items 2 and 2); Type key / Active items / Actions (last, not sortable); one Manage button per row, no menu trigger; Manage SHOWCASE_OPTION modal lists Widget and Gadget; close returns to the grid."
    - scenario: T-ANIMAL-007/S9
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Menu closes on Escape and outside click"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-008/S1
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsPage.feature::Open Manage Animals from the nav"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-008/S2
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsPage.feature::User without animals_write cannot open Manage Animals"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-008/S3
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsPage.feature::User-management permissions alone do not show Animals"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-008/S4
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsPage.feature::Add Animal opens as a modal over the page and closes back to it"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-008/S5
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsPage.feature::Opening a form URL directly shows the page with the form on top"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-008/S6
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsPage.feature::The old manage URL redirects to the page"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-009/S1
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::True shows a green circle with a tick, accessible name Yes"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). Covered by the T-ANIMAL-003/S14 test (carries both tags)."
    - scenario: T-ANIMAL-009/S2
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). Covered by the T-ANIMAL-003/S15 test (carries both tags)."
    - scenario: T-ANIMAL-009/S3
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::False shows a red circle with a cross; cells are not interactive"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST). Covered by the T-ANIMAL-003/S15 test (carries both tags)."
    - scenario: T-ANIMAL-009/S4
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Boolean labels are configurable with Yes/No defaults"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-009/S5
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Null and undefined show em dash named Not set"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-009/S6
      layers: [component]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ComponentHarness.feature::Existing switch cell still available"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-009/S7
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Circle fills meet contrast in light and dark mode"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
    - scenario: T-ANIMAL-009/S8
      layers: [ui-e2e]
      tests:
        - "ai-code-framework/ui/UI.NextJs.Framework/e2e/features/animals/ManageAnimalsGrid.feature::Dedicated tokens leave system buttons and callouts unchanged"
      result: passed
      note: "Round 3: e2e pass (run 11, 09:52 BST)."
  blockers: []                 # none: T-007/S8 unblocked 2026-10-09 09:46 (Neil) and passes
  # Notes for Dev Bot / Neil (not blockers): (1) Code defects from round 3: none. F-46 no-retry Date Born check passes before and after the 09:08 changes. (2) Scaffolding: after the 09:08 drop, untraced-http.ts
  # was still being edited (09:12); run 7 failed in global setup (HTTP 307 on the http API_URL) before that edit landed - green since. (3) e2e README "not present yet" line: fixed by Dev Bot (09:30).
  # (4) First scenario after a fresh dev:test start can hit net::ERR_ABORTED while .next-test cold-compiles (run 8, T-004/S1; green on the warm re-run 9) - addressed: Dev Bot helpers/warm-up.ts in global setup; run 10 warm-up 4/4 pages 200 on first attempt.
  # (5) F-41 residual (scaffolding, owner code): with CLI --trace=on the setup project traces (auth.setup.ts) record every persona password (signInThroughUi passes it as an evaluate argument; CLI overrides
  # the project trace: off). Default config: 0 hits. Probe artefacts deleted. Fix: sign in from an uninstrumented browser / child process, or drop the value from the traced call.
  # (5) FIXED (addendum): Dev Bot 09:30:01 setup signs in from an untraced child process (sign-in-child.cjs). Probe 09:41 with CLI --trace=on: 0 setup traces, 0 password hits (19 report + 4 result files); probe folders deleted.
  # (6) Neil: rotate all six persona passwords now that (5) is fixed (Review Bot F-41 named three). (7) Animal batch resets clear only footprint names - tests create footprint names only.
  # (8) Next dev auto-adds <distDir>/types to ui tsconfig.json and rewrites next-env.d.ts on start: test-bot reverted the tsconfig.json addition (.next-test-tb); next-env.d.ts left as Next wrote it (auto-generated).
  #     A parallel stack (API :7189 with a shared .next-test cache, 09:36) made the first addendum probe invalid (UI bundle pointed at :7189); UI moved to its own dist dir .next-test-tb. 3003/5188/7188 left running.
  # (9) T-007/S8 (Addendum 2): passed first time on the confirmed baseline; no code, test or data defect.
  updated_at: 2026-10-09T09:56:00+01:00
  updated_by: test-bot
approvals:                    # required = handoff.require_human_approval at the time of the gate
  plan_to_code:
    required: true
    approved_by: human        # Neil Wood. Re-approved 2026-10-08T15:44:00+01:00 after accepting the suggested defaults for Q23-Q27, Q32, Q34-Q36. Supersedes the 14:00 approval (human / Neil Wood, 2026-10-08T14:00:00+01:00), which was superseded by decisions 20-26; this approval covers decisions 1-26 and Q22-Q36. KEPT — not overwritten by the Decision 29 approval below
    approved_at: 2026-10-08T15:44:00+01:00
    # Alongside (does not overwrite 15:44): Neil 2026-10-08T19:14:00+01:00 approved plan_to_code for Decision 29 (boolean tick/cross cells, T-ANIMAL-009) and accepted Q38 (null → em dash + "Not set"); also chose to reopen the feature for Dev Bot + a fresh review before merge. Covers decisions 27-29 and Q37-Q38 on top of the 15:44 scope
    decision_29_approved_by: human
    decision_29_approved_at: 2026-10-08T19:14:00+01:00
    # Alongside (does not overwrite 15:44 or 19:14): Neil approved Decision 30 (Neil 19:57) - boolean cells as filled circles with a near-black glyph, dedicated light / dark tokens (T-ANIMAL-009, T-ANIMAL-003 S14 / S15) - after his 19:52 (dark-mode contrast, via Review Bot) and 19:53 (inverted circle) BST requests
    decision_30_approved_by: human
    decision_30_approved_at: 2026-10-08T19:57:00+01:00
  code_to_review:
    required: false
    approved_by: null
    approved_at: null
  merge:
    required: true            # always; agents never merge
    approved_by: human        # Neil, told Dev Bot directly 2026-10-09 12:37 BST: treat as merged (no git; Neil's instruction is the merge). Recorded by plan-bot
    approved_at: 2026-10-09T12:37:00+01:00

blockers: []                  # 2026-10-08T15:55:00+01:00 plan-bot: cleared at the re-approved hand-off. The plan-bot "WAITING ON NEIL" open-questions blocker is resolved (no open questions remain); Dev Bot's two blockers (View spec gap, creatures schema change) are resolved by the re-approved plan and are kept verbatim under "Notes for the next owner" as rework items
---

# Handoff: Manage Animals

> **Now:** `merged` (2026-10-09 12:37 BST, Neil's word to Dev Bot; no git) · owner `human` · was `approved` · owner `human` (Neil) · pickup `pending` · **Final verdict approve-with-comments** (d30-2 code approve-with-comments + test review round 3 approve, 2026-10-09 09:58 BST). Tests: 77 pass / 0 fail / 0 blocked (T-ANIMAL-007/S8 unblocked after Neil's 09:46 baseline); unit 52/52; e2e run 11 73/73. F-41 password leak closed (scan 0). Open Nits only: F-50, F-51, F-52, F-55, F-56; note F-53. Rule change: `nextjs-modal-routing.mdc` (one element per tid).
> **Next:** Neil: merge decision; rotate the animals-tester / animals-viewer / animals-usermanager test passwords (then re-run the e2e setup project), delete `.next-test-tb` and stale run logs; optionally schedule the Nits. Report: `reviews/DIRECT-manage-animals-d30-2-review.md` → "Test review — test round 3".


## Summary

Manage Animals list on its own page `/examples/animals` (list on the page, not in a modal: decision 27, Neil's standing UI rule; specified as one `Paginated Grid` page and delivered as two tickets, the page T-ANIMAL-008 and the paginated grid T-ANIMAL-003: decision 28) plus an Add | Edit Animal Basic Form opened as a modal over it (Add and Edit modes only; View dropped, decision 20). Every field is persisted through the **Animals** service to the **Animal** table, now in the new `creatures` schema (`creatures.animals`, decision 21), with soft delete. One animals permission, `animals_write` (policy `AnimalsWrite`), guards the whole feature: without it there is no nav link, no page and 403 from the API (decisions 22, 24); every user gets it through the seeded Administrators and Standard groups (decision 25). Edit and Delete are items of a row actions menu in the Actions column at the end of the grid (decisions 23, 26). Includes shared Switch and Tag Input controls (T-ANIMAL-006), the shared, permission-aware row actions menu (T-ANIMAL-007), and the shared boolean-icon grid cell renderer (T-ANIMAL-009; decision 29 tick/cross, **decision 30:** filled circle with near-black Check/Close glyph via dedicated light/dark tokens; not a read-only Switch).

## Artefacts

| Artefact | Path |
|----------|------|
| Plan | `plan.md` |
| Page specs (source of truth) | `specs/add-edit-animal.yaml`, `specs/manage-animals.yaml` |
| Excel | `excel/add-edit-animal.xlsx`, `excel/manage-animals.xlsx` |
| Journeys | `journeys/j-animal-manage.md` |
| Tickets | `tickets/T-ANIMAL-001-animal-schema.md`, `tickets/T-ANIMAL-002-animals-service.md`, `tickets/T-ANIMAL-003-manage-animals-grid.md`, `tickets/T-ANIMAL-004-add-edit-animal-form.md`, `tickets/T-ANIMAL-005-soft-delete.md`, `tickets/T-ANIMAL-006-shared-switch-tag-input.md`, `tickets/T-ANIMAL-007-shared-grid-actions-column.md`, `tickets/T-ANIMAL-008-manage-animals-page.md` (decision 28), `tickets/T-ANIMAL-009-shared-boolean-icon-grid-cell.md` (decision 29) |
| UI ↔ DB stubs | none (optional loop stage 5 not run) |
| Review log | `reviews/review-log.md` (rounds 1, 2 and 3 on 08/10/2026; Decision 29 cycle 1 code review + test review, test round 1) |
| Review reports | `reviews/DIRECT-manage-animals-1-review.md` (round 1: Request changes); `reviews/DIRECT-manage-animals-2-review.md` (round 2: Approve, superseded by decision 27); `reviews/DIRECT-manage-animals-3-review.md` (round 3, final: Approve with comments); `reviews/DIRECT-manage-animals-d29-1-review.md` (Decision 29 cycle 1: Tests blocked - Approve with comments; **SUPERSEDED by Decision 30**); Decision 30 cycle 1 pending (`reviews/DIRECT-manage-animals-d30-1-review.md`) |

## Notes for the next owner

- **Dev Bot hand-off (2026-10-08T20:04:30+01:00): Decision 30 + scaffolding to Review + Test (option B).** Filled-circle Yes/No cells (renderBooleanIconCell: CSS circle + Check/Close glyph using --app-boolean-glyph / --ink-100; fills --app-boolean-true-fill / --app-boolean-false-fill light+dark in tokens.css; --system-green/--system-red unchanged). Manage Animals Is Furry / Has Hooves use it; renderBooleanSwitchCell kept. npx tsc --noEmit pass; contrast S7 checked vs ticket targets. Scaffolding confirmed: Api.Framework.Tests 21/21 Release green; e2e Playwright+playwright-bdd ready; reset/personas/harness listed in implementation.tests. Manifest: one grid-cell-renderers.tsx entry (S1-S6,S8 + T-003 S14/S15 + T-006 S5); tokens.css scenarios S7/S8. **d29-1 Approve SUPERSEDED** - do not merge on it. Fresh Decision 30 cycle (review.verdict null, cycle: 0). routes.code_to_review + code_to_test: direct. approvals.merge left unset. Dev Bot did not message Review/Test Bot. **Neil before local tests:** separate Postgres DB (e.g. api_framework_test, never the dev DB); API.Framework Test environment + UI on localhost:3003 / API 5088|7088; set E2E_TEST_DATA_KEY and persona password env vars (agents never edit .env*).

- **Review Bot (Decision 29 cycle 1, 2026-10-08T19:45:00+01:00): Tests blocked — Approve with comments; to Neil for the merge decision.** Code review: Blocker 0 · Major 0 · Minor 1 · Nit 5. F-26 Minor: add `role="img"` to the boolean icon spans so the Yes/No name is valid ARIA. Nits: F-19 manifest tags for T-ANIMAL-008/S4-S6, F-27 mixed EOL, F-28 design-system README icon list, F-29 inline style, F-30 double `unity-auth-cleared` dispatch. Test review: blocked-noted (Test Bot run 1: 0/0/75 waiting). Blockers: Api.Framework.Tests, Next.js e2e scaffolding, reset endpoint + batch keys, personas, optional component harness (owner code); Test environment, test DB, secrets and `testing` placeholders (owner Neil). Spec note for Plan Bot / Neil: the prescribed `--system-green` tick is 2.51:1 on white and the `--system-red` cross is 2.09:1 on the dark surface (below 3:1 non-text); see the report's Out of scope. F-13 is fixed in code but the running API.Framework process (started 17:55) predates it.
- **Plan Bot hand-off (2026-10-08T19:15:00+01:00): Neil 19:14 BST reopen — T-ANIMAL-009 to Dev Bot + fresh review.** Neil accepted Q38 (em dash + "Not set"), approved `plan_to_code` for Decision 29 **alongside** the 15:44 approval (not overwritten), and chose to send T-ANIMAL-009 to Dev Bot now with a fresh review before merge (round counter reset for this change; round-3 Approve-with-comments kept for code up to Decision 28). Round-3 Minor/Nit comments remain open; Dev Bot may address them in the same pass. Manifest unchanged. Q38 marked accepted in plan.md / T-ANIMAL-009 S5 / manage spec + Excel regenerated.
- **Plan Bot update (2026-10-08T19:10:00+01:00), Neil 19:04 BST via Review Bot (Decision 29):** Is Furry / Has Hooves stay read-only but show a **green tick / red cross** (accessible Yes/No), not a read-only Switch. Reason: read-only switches look almost identical to editable ones. Applied to `plan.md` (decision 29; field inventory amended with a note; Q38 open for null/undefined with suggested default em dash + "Not set"), `specs/manage-animals.yaml` + `excel/manage-animals.xlsx` (regenerated; schema OK), journey, T-ANIMAL-003 (S14/S15 new; work item 3 amended; depends on T-ANIMAL-009), T-ANIMAL-006 (**rescoped**: boolean grid-cell half removed; "Grid cells" → "String-array grid cells"; form Switch/Tag Input stay), new **T-ANIMAL-009** (shared `renderBooleanIconCell`; add Material `Check`/`Close` to design-system `Icon`; colours `--system-green` / `--system-red`). Neil's own change: recorded as approved by him; no separate `plan_to_code` re-approval. **Needs Dev Bot** to implement T-ANIMAL-009 and switch the animals grid columns. Round 3 Approve-with-comments (19:08) does **not** cover Decision 29. Stage, owner, pickup, approvals, review sections and the implementation manifest were left unchanged.
- **Re-approval needed** *(resolved 2026-10-08T15:44:00+01:00: Neil re-approved `plan_to_code`; see the Plan Bot hand-off note below).* Neil approved the plan (`plan_to_code`) on 2026-10-08 at 14:00 BST. That approval is superseded by decision 20 (View dropped, 14:31 BST) and decision 21 (`creatures` schema, 14:35 BST); `approvals.plan_to_code` is reset to pending. Do not resume coding until Neil re-approves and the stage is `in-development` with owner `dev-bot`.
- **Plan Bot update (2026-10-08T14:41:28+01:00):** both decisions applied to `plan.md` (decisions 20 and 21; decisions 6, 11, 13 and 18 amended with notes; new Target stack section on how API.Framework assigns schemas), both specs, both workbooks (regenerated), the journey and all six tickets. T-ANIMAL-003 S9/S10 and T-ANIMAL-004 S11 were replaced in place (numbering unchanged); T-ANIMAL-001 gained S6 (schema `creatures`). Draft wording uses the suggested defaults and is marked pending. Spec Target DB Table now reads `Animal (creatures.animals)`; manifest `db` entries such as `Animals:Animal.Name` still refer to the same entity.
- **Open questions Q22–Q27** (in `plan.md`): read-only access to Manage Animals; row click; `creatures` registration / history table; DB privileges to create the schema; cross-schema `UpdatedBy` FK; replace vs move the `AddAnimals` migration.
- **Plan Bot update (2026-10-08T14:58:00+01:00), Neil's 14:47 BST decisions:** decision 22 (animals get their own permissions; supersedes decision 11, amended with a note) and decision 23 (Actions column at the end of the Manage Animals grid with an Edit icon per row, as a reusable UI.NextJs.Framework grid feature). Applied to `plan.md` (new Target stack sections on how API.Framework declares / registers / seeds / assigns permissions and how the Next.js `EntityGrid` Actions column works today), both specs (permission names on enablement / availability; `actions_menu` now lists the Actions-column icons), both workbooks (regenerated), the journey, T-ANIMAL-001 (permission seed, new S7), -002 (own `AnimalsRead` / `AnimalsWrite` policies, new S12 / S13), -003 (Actions column; S8 now clicks the Edit icon, S9 / S10 replaced in place, new S11), -004 (permission name), -005 (Delete icon in the Actions column, draft Q31) and new **T-ANIMAL-007** (shared grid Actions column). Neil did not answer Q22–Q27 individually; they stay open, with Q22 / Q23 revised. New open questions Q28–Q33. Draft names `animals_read` / `animals_write` are suggested defaults, not decisions. Dev Bot's code still uses `DirectoryPolicies.UserManagementRead/Write`, `animal-permissions.ts` (`user_management_*`) and `rowActionsDisplay: 'menu'` (`EntityGridRowActionsMenu.tsx`); manifest entries naming "View Animal" or the actions menu describe the code as built.
- **Open questions Q28–Q33** (in `plan.md`, added 14:58): permission names / shape; who gets them and how (seed); permission category / tenant feature; where Delete goes; Actions column details; keep or remove Dev Bot's `menu` mode. Q28–Q31 and Q33 were answered at 15:17 BST (next note).
- **Plan Bot update (2026-10-08T15:30:00+01:00), Neil's 15:17 BST answers:** decision 24 (Q22 / Q28: one permission `animals_write` "Manage animals", policy `AnimalsWrite`, on list, get, create, update, delete and the form schema; no read permission; without it no nav link, no page, 403), decision 25 (Q29 / Q30: "add this perm to our users" = seed it with `HasData` to the Administrators group (automatic) and the Standard group (default group); covers system admins and every default-tenant user in those groups; not other groups or other tenants, which is Q34; users get it after signing in again or refreshing their token) and decision 26 (Q31: Edit and Delete in a row actions menu in the Actions column; amends 23; resolves Q33 by keeping Dev Bot's `rowActionsDisplay: 'menu'` / `EntityGridRowActionsMenu.tsx`). Decisions 11, 22 and 23 are amended with notes; Q22, Q28–Q31 and Q33 stay in `plan.md` marked answered. Applied to `plan.md`, both specs, both workbooks (regenerated), the journey, T-ANIMAL-001 (single permission seed + Standard link, token note, S7 rewritten), -002 (`AnimalsWrite` everywhere; S11 / S13 rewritten in place), -003 (permission-gated page, row actions menu; S8–S11 updated in place), -004 (wording), -005 (Delete Animal in the menu; S5 rewritten) and -007 (re-scoped to the shared permission-aware row actions menu; same file name). All read-permission references removed from the artefacts. Q32 revised; new Q34 (users outside the seeded groups), Q35 (`animals_write` vs `animals_edit`), Q36 (what the URL shows without the permission). Dev Bot's code already has the `menu` mode; it still checks `user_management_write`, has the View item and uses `DirectoryPolicies`.
- **Decisions 1–19** (as originally approved; see decisions 20–21 above for later changes) are in `plan.md` › Decisions and applied to both specs, both workbooks, the journey and all tickets. Key effects: Last Amended = `UpdatedUtc` (stored UTC, shown in the browser's local time) + required `UpdatedBy` (FK to `auth.users`, set on create / update / soft delete; shown as display name, fallback email); persistence-only `NormalizedName` with a unique index filtered to non-deleted rows; `DateBorn` date only; `Attributes` `jsonb` NOT NULL default `[]`; reuse `UserManagementRead` / `UserManagementWrite` (read-only users see View only); global table `auth.animals`; `Animals` area at `v1/Animal`, schema `v1/schemas/create-animal`; `/examples/animals` page with nav label "Animals"; new shared Switch / Tag Input controls (T-ANIMAL-006). No open questions remain.
- **`.env` is Neil's:** he sets `NEXT_PUBLIC_UNITY_API_ROOT` in `.env.local` to API.Framework's `v1/` root. Agents never open or edit `.env*` files.
- **Git:** do not `git init` (or otherwise put under git) UI.NextJs.Framework or API.Framework without asking Neil first.
- Active targets: API.Framework (single form = `AbstractFormRecord` like `CatalogueItemRecord`, schema JSON in `Validation/Schemas`, EF model in `Api.Framework.Data`, controllers under `Controllers/V1`) and UI.NextJs.Framework (copy the reference-data grid and form modal; the list itself is on the page, not in a modal, per decision 27 and `.cursor/rules/framework/nextjs-list-pages.mdc`). See **Target stack** in `plan.md`.
- Hand-off to Review Bot will be `direct` with `review.direct_scope: plan`: fill in `implementation` (every file that implements the plan), then message Review Bot. Neither API.Framework nor UI.NextJs.Framework is a git repo today; that is fine for this route. Leave `code.*.branch` null and list the files in the manifest.
- **Dev Bot build status (2026-10-08T14:30:18+01:00):** T-ANIMAL-001..006 implemented; API Release build pass (0 warnings), migration `20261008131327_AddAnimals` added (not applied to any database), `npx tsc --noEmit` and `npm run build` pass. `npm run lint` cannot run (pre-existing: no ESLint config). No test projects exist; ad-hoc out-of-repo checks passed (see `code.verification`). Hand-off to Review Bot is on hold for the blocker only.
- **Dev Bot deviations / assumptions for review:** shared framework changes beyond the feature folder: renderer error display fixed (it showed only the first character of the first error), EntityGrid toolbar now also shows when only header toolbar actions exist, new row-actions menu (`rowActionsDisplay: 'menu'`), `ApiRequestError` carries the API error body, opt-in schema-driven client validation (`schemaDrivenValidation`, `submitEmptyArrays`) so reference-data forms behave as before. `/examples/animals` auto-opens Manage Animals (closing goes to `?manage=closed`). Delete confirmation title and message are both "Delete <Name>?" (no other prose in the spec). Save stays enabled; client-side schema errors block the request and show on the fields. Name input is capped at 100 characters with the `restrict` UI option. Tags are not trimmed (spec silent). No spec messages exist for Name > 100, an invalid date format or a plain 403, so the framework's fallback text is used there. API: schema-driven validation via `IRecordValidationApi`, then the uniqueness check (409 "An animal with this name already exists"); unknown or soft-deleted id -> 404 "The animal was not found.".
- **Timestamps note:** `.env.example`, `.env.local`, `README.md` and `src/config/environment.ts` in UI.NextJs.Framework, and `Api.Framework/Program.cs`, show last-write times of 13:03-13:11 BST today, before Dev Bot picked up at 14:04. Dev Bot did not open or change them.
- **Code status after the spec gap (2026-10-08T14:32:50+01:00):** code for T-ANIMAL-001..006 is built and still includes View (View Animal row action, View mode of the form, `?mode=view` routes). It has deliberately NOT been changed yet: Neil's 2026-10-08 14:31 BST decision to drop View is a spec change, so Dev Bot will remove View and update the `implementation` manifest and `code` section once Plan Bot's updated specs and tickets come back with `plan_to_code` approved. The `implementation` manifest and `code` section above describe the code as built at 14:30 BST.
- **DB schema change pending (2026-10-08T14:35:33+01:00):** the built code still uses `auth.animals` (`Animal` entity in `LoginDbContext` and migration `20261008131327_AddAnimals`, schema `auth`). Per Neil's 2026-10-08 14:35 BST decision the table moves to a new `creatures` schema (`creatures.animals`); names in the UI, tickets and API stay Animals / Animal. Dev Bot will rework the EF model and the migration (not applied to any database yet) once Plan Bot's updated specs come back with `plan_to_code` approved. No code has been changed for this decision.
- **Plan Bot hand-off (2026-10-08T15:55:00+01:00): plan re-approved, rework for Dev Bot.** Neil accepted the suggested defaults for Q23–Q27, Q32 and Q34–Q36 at 15:44 BST and re-approved `plan_to_code` (2026-10-08T15:44:00+01:00, covering decisions 1–26 and Q22–Q36). No open questions remain; draft / pending markers were removed from the specs, journey and tickets, both workbooks regenerated. Rework versus the code built at 14:30 BST (tickets are the source of truth):
  1. **Drop View** (decision 20): remove the View Animal row action, the View mode of the form and the `?mode=view` routes (T-ANIMAL-003, -004).
  2. **Move to `creatures.animals`** (decision 21, Q24–Q27): map `Animal` on `LoginDbContext` with `ToTable("animals", "creatures")` via a named schema constant; history table stays `auth.__ef_migrations_history`; no `GRANT`s; keep the `updated_by` → `auth.users(id)` FK (NOT NULL, restrict). Neil has not run the API since 14:13 BST, so **remove `20261008131327_AddAnimals` and regenerate it** so it creates `creatures.animals` directly and carries the permission seed (T-ANIMAL-001).
  3. **Single permission** (decisions 22, 24, 25; Q34, Q35): replace `DirectoryPolicies.UserManagementRead/Write` on the animals endpoints and the `user_management_*` checks in `animal-permissions.ts` with one permission `animals_write` (`Define(25, "animals_write", "Manage animals", "Animals")`) and `AnimalPolicies.AnimalsWrite` on every animal endpoint (list, get, create, update, delete, form schema); seed it with `HasData` to the Administrators and Standard groups; no feature, no back-fill (T-ANIMAL-001, -002, -003). Users get it after signing in again or refreshing their token.
  4. **Keep the row actions menu** (decisions 23, 26; Q23, Q32): keep `rowActionsDisplay: 'menu'` / `EntityGridRowActionsMenu.tsx` in the last "Actions" column with Edit Animal and Delete Animal only, made permission-aware per T-ANIMAL-007 (`requiredPermissions` any-of + `isVisible`, hidden not disabled, no trigger / no column when nothing is allowed, text-button grids unchanged). Clicking a row does nothing.
  5. **No-permission message** (Q36): without `animals_write`, no "Animals" nav link, no auto-open, no API call; show a warning `Callout` "You do not have permission to manage animals." on `/examples/animals` and the routed modal URLs (T-ANIMAL-003). *(Decision 27, 18:40: the list is on the page, so the callout replaces the list on the page and on the form URLs.)*
- **Resolved blocker, moved verbatim from `blockers` at 2026-10-08T15:55:00+01:00 (Dev Bot's View spec gap; rework item 1):** SPEC GAP, returned to plan-bot: Neil decided 2026-10-08 14:31 BST to drop the View feature entirely from manage-animals: no View Animal row action and no View mode form; read-only users do not get View. Affected and for Plan Bot to update: T-ANIMAL-003 View Animal row action and the scenarios 'Read-only user sees View only' and 'View opens read-only form'; T-ANIMAL-004 scenario 'View mode is read-only'; Decision 13; specs/add-edit-animal.yaml View mode. With View gone, the original schema-permission conflict goes away: GET v1/schemas/create-animal stays UserManagementWrite as T-ANIMAL-002 'Read-only users cannot change animals' and Decision 11 state. Code is built and has not been changed for this decision; Dev Bot removes View once the updated specs come back through plan_to_code. (raised by dev-bot 2026-10-08T14:30:18+01:00; Neil's decision recorded by dev-bot 2026-10-08T14:32:50+01:00)
- **Resolved blocker, moved verbatim from `blockers` at 2026-10-08T15:55:00+01:00 (Dev Bot's creatures schema change; now rework item 2):** SPEC CHANGE, forwarded to plan-bot: Neil decided 2026-10-08 14:35 BST to create a new database schema named creatures and move the animals table(s) into it, out of auth (creatures.animals instead of auth.animals). Only the DB schema grouping changes: Manage Animals / animal naming stays as is in the UI, tickets and API surface (v1/Animal, v1/schemas/create-animal, Animals service, Animal table). Plan Bot to update the plan (Decisions / Target stack), specs, workbooks, tickets and any UI-DB stubs so Target DB Schema = creatures (not auth). Code is built against auth.animals and has not been changed for this decision; Dev Bot reworks the EF model and the AddAnimals migration once the updated specs come back through plan_to_code. (recorded by dev-bot 2026-10-08T14:35:33+01:00)
- **Dev Bot rework hand-off (2026-10-08T16:09:59+01:00):** all five Plan Bot rework items done; `code` and `implementation` rewritten for the reworked code (the 14:30 notes above describe the earlier build).
  1. **View dropped:** no View Animal item, no View mode or read-only rendering of the form, no `?mode=view` URLs (`animalFormHref` has no mode; `[id]` routes no longer read `searchParams`); the unused `Visibility` icon was removed from `Icon`.
  2. **`creatures.animals`:** `ToTable("animals", LoginDbContext.CreaturesSchema)` (new constant `"creatures"` next to `Schema = "auth"`); `20261008131327_AddAnimals` removed with `ef migrations remove --force` and regenerated as `20261008150221_AddAnimals` (`EnsureSchema("creatures")`, table, both indexes, FK to `auth.users` restrict, permission seed). History table unchanged (`auth.__ef_migrations_history`); no GRANTs. `Down` drops the table and the seed rows but not the `creatures` schema (EF does not generate `DropSchema`). The migration files are EF-generated (UTF-8 with BOM, like the sibling migrations).
  3. **Permission:** `Define(25, "animals_write", "Manage animals", "Animals")`; `SeededGroupPermissions()` adds the Standard link (Administrators get it automatically). New `AnimalPolicies` (`AnimalsWrite`, `WritePermission`) registered in `Program.cs`; `[Authorize(Policy = AnimalPolicies.AnimalsWrite)]` on all five `AnimalController` actions and on `AnimalSchemaController`; no `DirectoryPolicies` left on the animals controllers. Signed-in users need to sign in again (or refresh their token) after the migration runs to get the claim.
  4. **Row actions menu (T-ANIMAL-007):** `GridRowAction` gained `requiredPermissions` (any-of) and `isVisible(row)`; shared `hasAnyPermission` in `src/framework/auth/permissions.ts`. `EntityGrid` reads `session.permissions` via `useAuth()`, hides unpermitted actions, omits the Actions column when none is permitted, and per row hides `isVisible === false` items (no trigger when a row has none). Applies to `buttons` too; grids without `requiredPermissions` render as before. Item clicks call `stopPropagation()`; there is still no row-click handler. Manage Animals: Edit Animal and Delete Animal with `requiredPermissions: ['animals_write']`.
  5. **No-permission state:** `SiteNav` shows "Animals" only with `animals_write`. `useAnimalsAccess` + `AnimalsAccessNotice`: without the permission `/examples/animals` does not auto-open, the routed Manage / form components mount nothing (no API or schema call), and the page body shows the warning `Callout` "You do not have permission to manage animals." (also on the full-page `/manage`, `/manage/item`, `/manage/item/[id]` URLs).
- **Dev Bot assumptions for review (rework):** signed-out users see the existing `EntityGridAuthGate` sign-in callout instead of the no-permission callout, and "Checking sign-in…" while auth loads (spec covers signed-in users only); intercepted modal routes render nothing without permission because the page underneath already shows the callout; "+ Add Animal" is also gated on `animals_write` (redundant with the page gate); `SiteNav` imports `hasAnimalsWrite` from the animals feature. The 14:30 deviations still apply (renderer error-display fix, toolbar fix, `ApiRequestError`, opt-in schema-driven validation, auto-open, "Delete <Name>?" title and message, Save enabled, Name `restrict` 100, tags not trimmed, framework fallback text where the spec has no message). Not verified: the API against a real database and a browser click-through (Neil runs both).
- **Concurrent edits noticed (not Dev Bot's):** UI.NextJs.Framework `README.md` (15:58:48 BST) and `src/features/design-system-showcase/DesignSystemShowcase.tsx` (15:58:24 BST, now LF line endings) were changed by someone else during the rework. Dev Bot did not touch them and they are not in `implementation`; the 16:03 BST `npm run build` included them and passed.
- **Dev Bot review round 1 fixes (2026-10-08T16:49:30+01:00), finding by finding** (report `reviews/DIRECT-manage-animals-1-review.md`; no finding said the spec is wrong, so nothing went back to Plan Bot):
  - **F-01 (Major) fixed:** `unity-json-form-renderers.tsx` takes `required` from JSON Forms `ControlProps` (from the schema's `required` array) and passes `requiredField={required}` to `Input` in the text control (Name, Date Born) and the icon picker, and to `FormFieldLabel` in the textarea, inline-list and tag-input controls. Name and Date Born now show the required marker; required fields on the reference-data forms get it too (as the review expects).
  - **F-02 (Minor) fixed:** `EntityGridRowActionsMenu` Escape handler calls `stopPropagation()` (the `document` listener runs before `Modal`'s `window` listener), closes the menu and returns focus to the Actions trigger. `Modal.tsx` keeps a module-level stack of open modals: Escape only closes the top-most one, and a handled key press is not reused by another modal. Escape on "Delete <Name>?" (or on Add/Edit Animal) now leaves Manage Animals open. The pre-existing "every modal closes on Escape" behaviour is fixed for all callers.
  - **F-03 (Minor) fixed:** `ConfirmModal` gained optional `confirmTheme` (default `primary-action`, existing callers unchanged); the delete confirm passes `system-red`.
  - **F-04 (Minor) fixed:** `RoutedModal` gained optional `subtitle` (forwarded to `ModalShell`); Manage Animals passes "Animal catalogue".
  - **F-05 (Minor) fixed:** delete goes through `AnimalEntityDataProvider.deleteById`; a failure shows the API's own message (e.g. "The animal was not found.") or "The animal could not be deleted.", never the HTTP status; the confirm closes either way so the error `Callout` on Manage Animals is visible; `confirmDelete` returns early while a delete is in flight, and `ConfirmModal`'s new optional `loading` prop shows the Delete button loading and disables both buttons.
  - **F-06 (Minor) fixed:** row menu uses `--app-surface-raised`, `--app-grid-border`, `--app-text-primary` and `--app-grid-row-hover-bg`; group border `--app-grid-border`. New semantic tokens in `tokens.css` with dark values: `--app-tag-chip-bg` (tag chips) and `--app-switch-track-off-bg` (Switch track; light `--ink-45` rather than the suggested `--app-input-border` because `#ebebed` behind a white thumb is near-invisible in light mode), plus `--app-switch-thumb-bg` for the thumb. The pre-existing undefined `--color-link/-danger/-text-muted` in `JsonSchemaForm.module.css` now use `--primary-action`, `--app-form-error-text` and `--app-input-placeholder` (closest existing tokens).
  - **F-07 (Nit) answered, no change by Dev Bot:** `AnimalService.cs:15` already says `creatures.animals` on disk. The file was last written at 16:24:36 BST, during the review, by someone other than Dev Bot (only that comment line differs from Dev Bot's 16:09 hand-off copy).
  - **F-08 (Nit) fixed:** one blank line removed before the `Animal` block in `LoginDbContext.cs` (no model change).
  - **F-09 (Nit) fixed:** `use-json-schema-entity-form` `initializeEdit` shows the API's message for a 404 read (e.g. "The animal was not found.") instead of "Unable to load the form. Please try again."; other failures keep `schemaLoadErrorMessage`.
  - **F-10 (Nit) fixed:** delete confirm has no `title`; the message stays "Delete <Name>?" (spec text).
  - **F-11 (Nit) fixed:** the schema-driven validation comment now sits on `JsonSchemaFormValidation`; the typo was a stray BEL control character (from an earlier PowerShell `` `a `` escape) in "additionalErrors", now fixed. No other control characters in the files read.
  - **F-12 (Nit) fixed:** unused `.switchCell` removed from `EntityGrid.module.css`.
  - **Out-of-scope notes from the review, not acted on:** Standard group seeded description ("Can view users and groups.") versus decision 25 is left to the planning agent (changing seed text needs a migration and is not in the tickets); design-system `README.md` still listing the `Visibility` icon, the Next.js `README.md` and `DesignSystemShowcase.tsx` are outside the manifest and were edited by someone else, so Dev Bot left them alone; `DateCompareValidator` clock and the empty `creatures` schema on `Down` are unchanged.
  - **Not verified:** Escape / focus and dark-mode behaviour were checked by reading the code and the build only (no browser click-through); no database run.

- **Dev Bot list-on-page + re-review hand-off (2026-10-08T18:48:20+01:00):** after Plan Bot's decision 27 conformance update (History row 20) and Neil's standing UI rule, the built UI already has the Manage Animals list on `/examples/animals` (no list modal; form modal only). `implementation.ui` refreshed to match disk: removed `AnimalsLanding.tsx`, `manage-animals-modal/*`, and `@modal/(.)manage/page.tsx`; added `manage-animals/*` (`ManageAnimalsPage`, `ManageAnimals`, grid/columns/providers), auth normalize (`normalize-auth-state.ts` + sign-in / refresh callers so `animals_write` reaches the session), and `.cursor/rules/framework/nextjs-list-pages.mdc`. Round 2 Approve at 17:06 does **not** cover this post-18:30 shape; `review.verdict` cleared to null; stage set `in-review`, owner `review-bot` for re-review round 3. `approvals.merge` left unset (Neil only). Parent agent will message Review Bot; Dev Bot did not message Review Bot.
- **Plan Bot plan restructuring (2026-10-08T18:56:00+01:00), Decision 28 (Neil, 18:46 BST):** "I think the tasks should be broken down into the page itself and the paginated grid but we can just have it as a paginated grid excel". The framework schema gained a `Paginated Grid` page type (route, search / filters, pagination, empty state; `Modal` stays for embedded lists). `specs/manage-animals.yaml` is now `page_type: Paginated Grid` (the decision 27 `presentation` field is gone) and `excel/manage-animals.xlsx` was regenerated. T-ANIMAL-003 is now the **paginated grid** ticket (same ID and file) and new **T-ANIMAL-008** is the **page** ticket (route, nav link, permission gate, no-permission callout, layout, hosting the grid and form modal). Scenario IDs are explicit. Old → new: T-ANIMAL-003/S1 → T-ANIMAL-008/S1, T-ANIMAL-003/S10 → T-ANIMAL-008/S2, T-ANIMAL-003/S11 → T-ANIMAL-008/S3; T-ANIMAL-003/S2–S9 unchanged. New: T-ANIMAL-003/S12 (paging) and S13 (empty state), drafts pending **Q37** (page size 20, options 5–200, "No results": what the code does today); T-ANIMAL-008/S4–S6 restate decision 27. No behaviour change, so `plan_to_code` re-approval is not needed. Plan Bot did not touch stage, owner, pickup, approvals, `implementation` or `code`. The manifest's `T-ANIMAL-003/S1`, `/S10` and `/S11` references should be read as T-ANIMAL-008/S1, S2 and S3; Dev Bot can re-point them on its next manifest update. *(Update 2026-10-08T19:01:00+01:00: Neil accepted Q37's suggested default at 19:00 BST, so T-ANIMAL-003/S12 and S13 are final and their draft markers are removed; no behaviour change.)*


- **Dev Bot hand-off (2026-10-08T19:20:33+01:00): T-ANIMAL-009 + round-3 Minor/Nit + framework docs.**
  - **T-009:** `Icon` Check/Close; `renderBooleanIconCell` (green/red via `currentColor` + `--system-green`/`--system-red`; Yes/No/Not set; null = em dash); Manage Animals Is Furry / Has Hooves switched to it; `renderBooleanSwitchCell` kept. Exported from `@entity-framework`.
  - **Findings:** F-13 GET NotFound now returns MessageResponse "The animal was not found."; F-14/F-15 final newlines; F-18 five files added to manifest; F-19 scenario remap T-003/S1,S10,S11 → T-008/S1,S2,S3 + page tickets tagged T-008; F-20 DropdownMenu showcase section; F-21 dark primary/secondary contrast tokens (`--app-primary-action-fg`, secondary dark surfaces); F-22 dark `--app-form-error-text: #ff9aa8`; F-23 stripped UTF-8 BOM + LF on auth/api files; F-24 `clearAuthState` dispatches `unity-auth-cleared` (schema cache clears on sign-out); F-25 superseded by T-009 icon cells (switches no longer used on Animals grid).
  - **Docs (Plan Bot framework updates):** `ai-code-framework/AGENT-BRIEF.md`, `loops/feature-build.md`, `api/API.Framework/.cursor/rules/api-framework-testing.mdc` — code_to_test + message Review+Test together; DoD drops “every scenario has a test”; scaffolding ownership; test-review code defects → changes-requested.
  - **Tests:** no scaffolding built (Neil has not asked; feature test plan does not yet require listed test files). Manifest `tests` empty / scaffolding-only. Test runs blocked until test env.
  - **API:** UI-heavy pass; only AnimalController Get body + final newlines on animal API files.

## History

Append one row per transition or pickup. Newest last. Never edit earlier rows.

| # | When | Stage | Owner | Route / gate | By | Note |
|---|------|-------|-------|--------------|----|------|
| 1 | 2026-10-08T13:32:00+01:00 | — → planned | — → plan-bot | — | plan-bot | Planning artefacts (written 07/10) audited against the current config (API.Framework + Next.js); plan updated, journey added, tickets linked; 2 specs, 2 workbooks, 1 journey, 5 tickets. Waiting on Neil's plan_to_code approval and open questions |
| 2 | 2026-10-08T13:45:00+01:00 | planned | plan-bot → human | plan_to_code (pending) | plan-bot | Neil accepted all 16 suggested defaults; decisions recorded in plan.md and applied to specs (Q1, Q2, Q4, Q5, Q7, Q8, Q11, Q14), both Excel workbooks regenerated, journey and T-ANIMAL-001..005 updated, T-ANIMAL-006 added (shared Switch + Tag Input, Q15). New open question 17 (Last Amended time zone). Waiting on Neil to review and approve the updated plan |
| 3 | 2026-10-08T14:03:00+01:00 | planned → in-development | human → dev-bot | plan_to_code (approved) · direct | plan-bot | Neil approved the updated plan at 2026-10-08T14:00:00+01:00 and answered Q17 (Last Amended in browser local time, stored UTC); accepted UpdatedBy required + FK (set on delete) and nav label "Animals" (decisions 17–19). manage-animals.xlsx regenerated; T-ANIMAL-003 updated. Handed off direct to Dev Bot for T-ANIMAL-001..006; implementation manifest left empty for Dev Bot |
| 4 | 2026-10-08T14:04:41+01:00 | in-development | dev-bot | pickup · direct | dev-bot | Dev Bot accepted T-ANIMAL-001..006. Gates checked: owner dev-bot, stage in-development, example false, plan_to_code approved by human 2026-10-08T14:00:00+01:00. Building against API.Framework + UI.NextJs.Framework (direct route, review.direct_scope: plan). Neither folder is a git repo; no git init, branches left null |
| 5 | 2026-10-08T14:30:18+01:00 | in-development | dev-bot | blocked (spec contradiction) | dev-bot | T-ANIMAL-001..006 built: API Release build pass, AddAnimals migration added, UI tsc + next build pass, lint not runnable (no ESLint config, pre-existing), no test projects (ad-hoc checks pass). implementation manifest filled. BLOCKED: GET v1/schemas/create-animal is write-only (T-ANIMAL-002) but read-only users must open the schema-driven View form (T-ANIMAL-003/004); waiting on Neil to pick option A or B. Stage 8 hand-off NOT done |
| 6 | 2026-10-08T14:32:50+01:00 | in-development → planned | dev-bot → plan-bot | spec gap (returned) | dev-bot | Spec gap returned to Plan Bot. Neil decided 2026-10-08 14:31 BST to drop View entirely (no View Animal action or View mode; read-only users get no View). Plan Bot to update T-ANIMAL-003 (View row action; 'Read-only user sees View only', 'View opens read-only form'), T-ANIMAL-004 ('View mode is read-only'), Decision 13 and specs/add-edit-animal.yaml View mode; the schema-permission conflict with T-ANIMAL-002 / Decision 11 goes away. plan_to_code gate applies again. Code built and unchanged; implementation manifest and code section kept as built |
| 7 | 2026-10-08T14:35:33+01:00 | planned | plan-bot | spec change (forwarded) | dev-bot | Neil's second decision (2026-10-08 14:35 BST) forwarded to Plan Bot: create DB schema creatures and move the animals table out of auth (creatures.animals); Animals / Animal naming unchanged in UI, tickets and API. Plan Bot to update plan, specs, workbooks, tickets and stubs for Target DB Schema = creatures, together with the View removal. Built code still on auth.animals and unchanged; plan_to_code gate applies again |
| 8 | 2026-10-08T14:41:28+01:00 | planned | plan-bot → human | plan_to_code (pending re-approval) | plan-bot | Applied Neil's decisions 20 (View dropped, 14:31 BST) and 21 (DB schema creatures, creatures.animals, 14:35 BST) to plan.md (decisions 6/11/13/18 amended with notes; Target stack section on API.Framework schema assignment: HasDefaultSchema("auth"), history table auth.__ef_migrations_history, Database.Migrate() at start-up), both specs, both workbooks (regenerated), journey and T-ANIMAL-001..006. New open questions Q22-Q27. plan_to_code reset to pending (14:00 approval superseded). Dev Bot's implementation manifest, code section, blockers and history kept as written. Waiting on Neil to answer open questions and re-approve |
| 9 | 2026-10-08T14:58:00+01:00 | planned | human | plan_to_code (pending re-approval) | plan-bot | Applied Neil's 14:47 BST decisions 22 (animals get their own permissions; supersedes decision 11, amended with a note) and 23 (Actions column at the END of the Manage Animals grid with an Edit icon per row; reusable grid feature in UI.NextJs.Framework) to plan.md (Target stack sections on API.Framework permissions and the Next.js EntityGrid Actions column), both specs, both workbooks (regenerated), journey and T-ANIMAL-001..005; added T-ANIMAL-007 (shared grid Actions column). Q22 / Q23 revised and kept open with Q24-Q27; new open questions Q28-Q33. plan_to_code stays pending. Dev Bot's implementation manifest, code section, blockers 1-2, notes and history rows 1-7 kept as written. Waiting on Neil to answer Q22-Q33 and re-approve |
| 10 | 2026-10-08T15:30:00+01:00 | planned | human | plan_to_code (pending re-approval) | plan-bot | Applied Neil's 15:17 BST answers as decisions 24 (Q22 / Q28: single permission animals_write, policy AnimalsWrite, on every animal endpoint; no read permission; amends 22), 25 (Q29 / Q30: seeded via HasData to the Administrators and Standard groups; other groups / tenants open as Q34) and 26 (Q31: Edit and Delete in a row actions menu in the Actions column; amends 23; Q33 resolved by keeping Dev Bot's rowActionsDisplay menu). Decisions 11 / 22 / 23 amended with notes. plan.md, both specs, both workbooks (regenerated), journey and T-ANIMAL-001..005, -007 (re-scoped) updated; read-permission references removed. Q32 revised; new Q34-Q36. plan_to_code stays pending. Dev Bot's implementation manifest, code section, blockers 1-2, notes and history rows 1-7 kept as written. Waiting on Neil to answer Q23-Q27, Q32, Q34-Q36 and re-approve |
| 11 | 2026-10-08T15:55:00+01:00 | planned → in-development | human → dev-bot | plan_to_code (re-approved) · direct | plan-bot | Neil accepted the suggested defaults for Q23-Q27, Q32, Q34-Q36 (Q27: he has not run the API since 14:13 BST, so AddAnimals is removed and regenerated; Q35: animals_write) and re-approved plan_to_code at 2026-10-08T15:44:00+01:00, covering decisions 1-26 and Q22-Q36 (supersedes the 14:00 approval). Questions marked accepted in plan.md (numbering kept); draft / pending markers removed from both specs, journey and T-ANIMAL-001..005, -007; both workbooks regenerated. Plan-bot open-questions blocker cleared; Dev Bot's View and creatures blockers resolved and moved verbatim to Notes as rework items. Handed off direct to Dev Bot to rework the built code (drop View; creatures.animals with AddAnimals regenerated; animals_write / AnimalPolicies.AnimalsWrite seeded to Administrators and Standard; permission-aware row actions menu; no-permission callout). Dev Bot's implementation manifest, code section, notes and history rows 1-7 kept as written |
| 12 | 2026-10-08T15:58:10+01:00 | in-development | dev-bot | pickup - direct | dev-bot | Dev Bot accepted the rework of T-ANIMAL-001..007. Gates checked: owner dev-bot, stage in-development, example false, plan_to_code re-approved by human 2026-10-08T15:44:00+01:00. Read handoff.md, plan.md decisions 20-26, both specs, journey and T-ANIMAL-001..007. Rework: drop View; creatures.animals with AddAnimals removed and regenerated; animals_write / AnimalPolicies.AnimalsWrite seeded to Administrators and Standard; permission-aware row actions menu; no-permission callout. No git init, branches null |
| 13 | 2026-10-08T16:09:59+01:00 | in-development → in-review | dev-bot → review-bot | code_to_review · direct | dev-bot | Rework of T-ANIMAL-001..007 to the re-approved plan done: View dropped; Animal moved to creatures.animals (AddAnimals removed and regenerated as 20261008150221_AddAnimals with the animals_write seed); animals_write / AnimalPolicies.AnimalsWrite on every animal endpoint, seeded to Administrators and Standard; shared permission-aware row actions menu (requiredPermissions any-of, isVisible); no-permission callout and hidden nav link. API Release build pass (0 warnings), no pending model changes, ad-hoc API checks 20/20; UI tsc + next build pass, ad-hoc grid render checks 14/14; lint still not runnable (no ESLint config, pre-existing); no test projects. implementation manifest and code section rewritten. Handed off direct to Review Bot (review.direct_scope: plan); Dev Bot did not message Review Bot |
| 14 | 2026-10-08T16:12:35+01:00 | in-review | review-bot | pickup · direct | review-bot | Review Bot accepted the direct hand-off of T-ANIMAL-001..007 (round 1 of max 3). Gates checked: owner review-bot, stage in-review, example false, plan_to_code re-approved by human 2026-10-08T15:44:00+01:00, implementation manifest not empty. Config re-read: development.api.active api-framework (ai-code-framework/api/API.Framework), development.ui.active nextjs (ai-code-framework/ui/UI.NextJs.Framework), review.direct_scope plan, scope_include ai-code-framework/api/** + ui/**. No branch recorded, so report DIRECT-manage-animals-1-review.md |
| 15 | 2026-10-08T16:40:48+01:00 | in-review → changes-requested | review-bot → dev-bot | review_feedback · direct | review-bot | Review round 1 of max 3 (direct, review.direct_scope: plan) finished: Request changes. Blocker 0 · Major 1 · Minor 5 · Nit 6. Reviewed all 75 manifest files whole (0 discovered, 0 not implemented) against both specs, all 62 scenarios of T-ANIMAL-001..007, API.Framework rules and the Next.js rules referenced from its README. Major F-01: mandatory Name and Date Born not shown as required in the UI. Data mapping, server-side validation, uniqueness, soft delete and AnimalsWrite all correct. No tests (no test project by rule; recorded as a tooling gap for Neil). Not assessed live: DB run, browser click-through; not under git. Report reviews/DIRECT-manage-animals-1-review.md; log reviews/review-log.md (round 1). Nothing merged, posted or voted. Review Bot did not message Dev Bot |
| 16 | 2026-10-08T16:43:37+01:00 | changes-requested | dev-bot | pickup · direct | dev-bot | Dev Bot accepted review round 1 of max 3 (reviews/DIRECT-manage-animals-1-review.md, verdict request-changes). Loaded findings F-01 (Major), F-02..F-06 (Minor), F-07..F-12 (Nit); 0 Blocker. No finding says the spec is wrong. Fixing in the active API/UI only; specs/tickets/excel/plan untouched. |
| 17 | 2026-10-08T16:49:30+01:00 | changes-requested → in-review | dev-bot → review-bot | code_to_review · direct | dev-bot | Review round 1 findings fixed or answered: F-01 (Major) required markers from the schema; F-02 Escape only closes the row menu / top-most modal; F-03 red Delete; F-04 "Animal catalogue" modal sub-text; F-05 delete via the entity provider with the API's message, confirm closes, no double fire; F-06 theme tokens; F-07 already correct on disk; F-08..F-12 Nits fixed. Shared files added to `implementation`: Modal.tsx, ConfirmModal.tsx, RoutedModal.tsx, tokens.css. Builds: API Release pass (0 warnings), no pending EF model changes, tsc pass, next build pass; lint still not runnable (pre-existing). Specs/tickets/excel/plan untouched. Hand-off ready for review round 2 of 3. |
| 18 | 2026-10-08T16:52:00+01:00 | in-review | review-bot | pickup · direct | review-bot | Review Bot accepted the direct hand-off for review round 2 of max 3 (T-ANIMAL-001..007, re-review of the round 1 fixes). Gates checked: owner review-bot, stage in-review, example false, plan_to_code re-approved by human 2026-10-08T15:44:00+01:00, implementation manifest not empty (79 files: 18 api, 3 migrations, 58 ui). Config re-read: development.api.active api-framework, development.ui.active nextjs (rules ai-code-framework/ui/UI.NextJs.Framework/.cursor/rules), review.direct_scope plan, scope_include ai-code-framework/api/** + ui/**. No branch recorded, so report DIRECT-manage-animals-2-review.md |
| 19 | 2026-10-08T17:06:14+01:00 | in-review → approved | review-bot → human | review_feedback · direct | review-bot | Review round 2 of max 3 (direct, review.direct_scope: plan) finished: Approve. Blocker 0 · Major 0 · Minor 0 · Nit 4. Re-reviewed all 79 manifest files whole (0 discovered, 0 not implemented) against both specs, all 62 scenarios of T-ANIMAL-001..007, the API.Framework rules and skills, and the Next.js AGENTS.md, README.md and .cursor/rules (from the updated config and ui-nextjs-checklist.md). Round 1: F-01..F-12 all resolved (F-07 was already fixed on disk at 16:24:36, before Dev Bot's pickup). New Nits: F-13 GET by id returns a bare NotFound() without the animal message; F-14 Switch files lack a final newline; F-15 nine animal API files lack a final newline; F-16 delete ConfirmModal should use level="secondary". No regressions found. Tests: no test project / runner, recorded as a tooling decision for Neil (not findings). Not assessed live: DB run, browser click-through, build or lint by the reviewer; not under git. Report reviews/DIRECT-manage-animals-2-review.md; log reviews/review-log.md (round 2). Nothing merged, posted or voted. Review Bot did not message anyone |
| 20 | 2026-10-08T18:40:00+01:00 | approved | human | conformance update (no gate) | plan-bot | Plan Bot conformance update: list on page (Decision 27). Neil's standing UI rule (2026-10-08, relayed by Dev Bot): a routed feature list page shows its search and results on the page, with no list modal; modals only for create / edit forms and confirms. Applied to plan.md (decision 27; decision 14 and Q36 amended with notes; pages and Next.js tables use Dev Bot's current paths under src/features/animals/manage-animals/), specs/manage-animals.yaml (presentation: page; page_type stays Modal because the schema has no routed list page type), excel/manage-animals.xlsx (regenerated), the journey and T-ANIMAL-003 (S1, S2, S10, S11 updated in place), -004, -007. Scenario changes implement Neil's own rule, so no plan_to_code re-approval is needed. Stage, owner, pickup, approvals, the implementation manifest and the code section are unchanged; only plan-related text in Summary and Notes was amended |
| 21 | 2026-10-08T18:48:20+01:00 | approved → in-review | human → review-bot | code_to_review · direct | dev-bot | Neil (via parent) authorised Dev Bot to refresh the implementation manifest after the list-on-page change (decision 27, ~18:30) and re-request review before merge. Manifest `ui` now matches disk (manage-animals/*, ManageAnimalsPage; removed AnimalsLanding, manage-animals-modal/*, @modal/(.)manage/page.tsx; added auth normalize + nextjs-list-pages.mdc). Round 2 Approve (17:06) superseded for current code; review.verdict cleared to null; approvals.merge still unset. Hand-off ready for Review Bot round 3 of max 3 (direct); Dev Bot did not message Review Bot |
| 22 | 2026-10-08T18:51:43+01:00 | in-review | review-bot | pickup · direct | review-bot | Review Bot accepted the direct hand-off for review round 3 of max 3 (final; T-ANIMAL-001..007, list-on-page per decision 27). Gates checked: owner review-bot, stage in-review, example false, plan_to_code approved by human 2026-10-08T15:44:00+01:00 (decision 27 conformance update needs no re-approval per History row 20), implementation manifest not empty. Config, checklists and rules re-read; Neil's list-pages rule (.cursor/rules/framework/nextjs-list-pages.mdc) applied directly. Round includes a live browser check (Neil approved signing in as the Development seeded user). Report DIRECT-manage-animals-3-review.md |
| 23 | 2026-10-08T18:56:00+01:00 | in-review | review-bot | plan restructuring (no gate) | plan-bot | Plan Bot plan restructuring: Paginated Grid page type and page / grid ticket split (Decision 28, Neil 18:46 BST). Manage Animals spec is now `page_type: Paginated Grid` (one Excel, regenerated); T-ANIMAL-003 is the paginated grid ticket and new T-ANIMAL-008 the page ticket; scenarios redistributed with the old → new mapping in both tickets (T-ANIMAL-003 S1 / S10 / S11 → T-ANIMAL-008 S1 / S2 / S3). New open question Q37 (page size, options, empty state; suggested default = current code). No behaviour change, so no re-approval needed. Stage, owner, pickup, approvals and manifest unchanged |
| 24 | 2026-10-08T19:01:00+01:00 | in-review | review-bot | open question answered (no gate) | plan-bot | Q37 accepted, S12/S13 final, no behaviour change. Neil accepted the suggested default at 19:00 BST: page size 20; options 5, 10, 20, 50, 100, 200; server-side paging as the code does now; the framework's "No results" empty state with "+ Add Animal" still shown. Draft markers removed from T-ANIMAL-003 S12 / S13 and the manage spec; plan.md says no open questions remain. Stage, owner, pickup, approvals, review sections and manifest unchanged |
| 25 | 2026-10-08T19:08:04+01:00 | in-review → approved | review-bot → human | review_feedback · direct | review-bot | Review round 3 of max 3 (final; direct, review.direct_scope: plan) finished: Approve with comments. Blocker 0 · Major 0 · Minor 4 · Nit 7 (open). Re-reviewed 82 manifest files plus 5 discovered (F-18) against both specs, all 67 scenarios of T-ANIMAL-001..008 (decision 28 mapping; T-ANIMAL-003 S12 / S13 final after Q37) and the new nextjs-list-pages.mdc rule (met). Live browser check on localhost:3003 as the Development seeded user: nav and route, validation, create / edit / duplicate / delete, Escape stacking, direct URLs and simulated no-permission all as specified. Row actions menu fully visible in light and dark mode and flips above. Round 2 miss acknowledged: menu clipping logged as F-17 (Major, already fixed by the 18:40 DropdownMenu). Minor: F-18 manifest incomplete, F-20 DropdownMenu not in showcase, F-21 dark-mode button contrast 2.73:1 (tokens.css), F-22 dark-mode tag-chip × 1.69:1. Nit: F-13..F-15 still open, F-19, F-23, F-24, F-25 (read-only switch styling; spec question for Neil). F-16 resolved. Test row created and deleted via the UI. Review cap reached; owner human. Tests remain a tooling decision for Neil |
| 26 | 2026-10-08T19:10:00+01:00 | approved | human | plan update (Neil change, no gate) | plan-bot | Plan Bot: Decision 29 boolean tick/cross cells (Neil 19:04), T-ANIMAL-009 added; needs Dev Bot. Is Furry / Has Hooves display_format → boolean icon; T-ANIMAL-003 S14/S15; T-ANIMAL-006 boolean grid cell rescoped out; new T-ANIMAL-009 (`renderBooleanIconCell`, Material Check/Close, --system-green/--system-red); Q38 open (null → em dash / Not set). Neil's own change, recorded approved; no re-approval. Round 3 Approve-with-comments does not cover this. Stage, owner, pickup, approvals, review sections and manifest unchanged |
| 27 | 2026-10-08T19:15:00+01:00 | approved → in-development | human → dev-bot | plan_to_code (Decision 29, alongside 15:44) · direct | plan-bot | Neil 19:14 BST: accepted Q38 (em dash + "Not set"); approved plan_to_code for Decision 29 alongside the 15:44 approval (not overwritten); reopened feature — T-ANIMAL-009 to Dev Bot, then fresh review before merge (round counter reset for Decision 29; round-3 Approve-with-comments intact for code up to Decision 28). Round-3 Minor/Nit still open; Dev Bot may fix in same pass. Manifest unchanged |
| 28 | 2026-10-08T19:20:33+01:00 | approved → in-development | human → dev-bot | pickup → direct | dev-bot | Dev Bot accepted T-ANIMAL-009 (Decision 29) + round-3 open Minor/Nit (F-13..F-15, F-18..F-25). Building against API.Framework + UI.NextJs.Framework. |
| 29 | 2026-10-08T19:20:33+01:00 | in-development → in-review | dev-bot → review-bot | code_to_review + code_to_test → direct | dev-bot | T-ANIMAL-009 done (renderBooleanIconCell, Check/Close icons, Animals Is Furry/Has Hooves on icon cells). Round-3 Minor/Nit fixed (F-13..F-15, F-18..F-25). Manifest remapped T-ANIMAL-003/S1,S10,S11 → T-ANIMAL-008/S1,S2,S3; F-18 files + T-009 files added. Framework docs updated (AGENT-BRIEF, feature-build, api-framework-testing.mdc). tsc --noEmit pass. Parent to message Review Bot and Test Bot (option B). Tests blocked until test env. Never edited testing section. |
| 30 | 2026-10-08T19:23:05+01:00 | in-review | review-bot | config decision (Neil, no gate) | plan-bot | Neil 19:19 BST: fixing failing tests gets its own limit of 5 rounds (`testing.max_test_fix_cycles: 5`), separate from the 3 code-review rounds (`handoff.max_review_cycles: 3` unchanged). Test-fix rounds no longer count toward review rounds (`failures_count_toward_review_cycles: false`; replaces flagged default 1). A round = each failed test run / test review routed back (code defect -> Dev Bot, test defect -> Test Bot); when 5 are used, the next escalates to Neil. `testing` section seeded from the template with `test_fix_cycle: 0` (max 5) for Test Bot to fill. Stage, owner, pickup, approvals, review and manifest unchanged |
| 31 | 2026-10-08T19:24:05+01:00 | in-review | review-bot | plan doc fix (no gate) | plan-bot | Scenario IDs frozen 2026-10-08 from current positions in T-ANIMAL-001 (S1-S7), -002 (S1-S13), -004 (S1-S12), -005 (S1-S5), -006 (S1-S5), -007 (S1-S9): headings now `### Scenario: S<n> - <title>` (em dash), referenced as `<ticket>/S<n>`. Doc-only, no wording or behaviour change; tests must use these IDs. T-ANIMAL-003 re-saved as UTF-8 without BOM and its mojibake repaired (text unchanged). Mojibake (double-encoded dashes/arrows/middots) repaired in this handoff.md too; wording unchanged. Stage, owner, pickup, approvals, review, testing and manifest unchanged |
| 32 | 2026-10-08T19:26:40+01:00 | in-review | review-bot | plan doc fix (no gate) | plan-bot | Encoding repair only: plan.md and specs/manage-animals.yaml re-saved as UTF-8 without BOM with double-encoded characters repaired (plan.md 103, spec 7: dashes, arrows, ellipsis, etc.); line endings and wording unchanged, spec still validates. excel/manage-animals.xlsx regenerated from the fixed spec (3 cells repaired, no other cell changes). No behaviour change. Stage, owner, pickup, approvals, review, testing and manifest unchanged |
| 33 | 2026-10-08T19:27:14+01:00 | in-review | review-bot | pickup · direct | review-bot | Review Bot accepted Dev Bot's direct hand-off (19:20:33) for the Decision 29 fresh review cycle, cycle 1 (not round 4 of the earlier cap): T-ANIMAL-001..009 incl. T-ANIMAL-009 boolean icon cells and the round-3 Minor/Nit fixes F-13..F-25. Gates checked: owner review-bot, stage in-review, example false, plan_to_code approved (15:44 + Decision 29 at 19:14), implementation manifest not empty. Report will be reviews/DIRECT-manage-animals-d29-1-review.md (the framework name DIRECT-manage-animals-1 would clash with round 1). Testing option B (Neil 19:07): this code verdict is provisional until Test Bot's test review; Review Bot does not touch review.test_verdict or the testing section. Test-fix loops are not counted as review cycles (Neil 19:19). Includes a live headless browser check |
| 34 | 2026-10-08T19:45:00+01:00 | in-review → approved | review-bot → human | review_feedback · direct | review-bot | Tests blocked: no Test environment / test DB (owner human) and no test scaffolding — Api.Framework.Tests, Next.js e2e, reset endpoint, personas (owner code) — so 0 of 75 scenarios tested (Test Bot run 1: 0/0/75 waiting; test_verdict blocked-noted). Decision 29 review cycle 1 (direct, review.direct_scope: plan; not round 4) finished: Approve with comments (code_verdict approve-with-comments; final verdict allowed by testing.blocked_tests_allow_approval: true, flagged default; Neil decides at merge). Blocker 0 · Major 0 · Minor 1 · Nit 5. Reviewed 91 manifest files (0 discovered) against both specs and all 75 frozen scenarios of T-ANIMAL-001..009, plus a live check in light and dark: tick / cross named Yes / No, 0 switches, cells not interactive, menu not clipped, Escape layering OK, dark contrast fixed. Round 3: F-13 (in code; API restart needed to see it), F-14, F-15, F-18, F-20..F-24 resolved; F-25 superseded; F-19 partly done. New: F-26 Minor (aria-label on a role-less span), F-27..F-30 Nit. Spec note to Plan Bot: tick 2.51:1 light / cross 2.09:1 dark with the prescribed tokens. Report reviews/DIRECT-manage-animals-d29-1-review.md; log reviews/review-log.md (code review + test review). Test-fix cycle unchanged (0 of 5). |
| 35 | 2026-10-08T20:00:24+01:00 | approved | human | plan update + approval (Decision 30) | plan-bot | Decision 30 (Neil 19:52 BST dark-mode request via Review Bot, 19:53 BST inverted-circle request, 19:57 BST approval): boolean cells become a filled circle (light Yes #609b44 / No #ef5673; dark Yes #8dc374 / No #ff9aa8) with a near-black Check / Close glyph (#18181b, --ink-100) via new tokens --app-boolean-true-fill / --app-boolean-false-fill / --app-boolean-glyph; --system-green / --system-red unchanged. Fills >= 3:1 on row and hover in both modes, glyph >= 4.5:1 on the fill. Updated plan.md (decision 30; amendment note on 29), T-ANIMAL-009 (S1, S2, S5 reworded in place; new S7 contrast, S8 system tokens unchanged; work items 3 and 7), T-ANIMAL-003 S14 / S15 (reworded, same IDs), spec (validates) and regenerated excel/manage-animals.xlsx, journey. Approval recorded in approvals.plan_to_code.decision_30_* |
| 36 | 2026-10-08T20:00:24+01:00 | approved | human | plan doc fix (no gate) | plan-bot | Test-data personas, wording only (Test Bot flag): T-ANIMAL-002 S9 and T-ANIMAL-003 S3 no longer name a real person - DisplayName "Animals Tester" and, for the user with no DisplayName, Email "animals-nodisplayname@e2e.test". Same IDs, no behaviour change; Notes line added in both tickets |
| 37 | 2026-10-08T20:00:24+01:00 | approved → in-development | human → dev-bot | plan_to_code (Decision 30) · direct | plan-bot | d29-1 review (19:44, approve-with-comments / tests blocked-noted) superseded by Decision 30 (Neil 19:57); do not merge on it; fresh review cycle follows the circle build. The d29-1 review fields are kept as a record (review.superseded_by). Dev Bot: build decision 30 (T-ANIMAL-009 S1–S8, T-ANIMAL-003 S14 / S15); d29-1 F-26 and Nits may be fixed in the same pass; then hand to Review Bot and Test Bot together |
| 38 | 2026-10-08T20:01:24+01:00 | in-development | dev-bot | scaffolding ready (no gate) | dev-bot | Test scaffolding ready for Test Bot: Api.Framework.Tests (21 scaffold unit tests pass Release), UI e2e Playwright+playwright-bdd, TestData reset master+batches (animals.page/grid/form/delete/api.*, reference-data.types-grid.baseline), personas (testdata-admin, animals-tester, animals-tester-emailonly, animals-viewer, animals-usermanager, reference-data-tester), component harness at /examples/test-harness for 11 component scenarios. F-26/F-28 applied. Separate DB api_framework_test (never unity_login). Decision 30 dark-mode circle colours NOT in this pass (parent applies separately). testing: section untouched. |
| 39 | 2026-10-08T20:04:30+01:00 | in-development | dev-bot | pickup · Decision 30 | dev-bot | Dev Bot accepted Decision 30 (T-ANIMAL-009 filled-circle Yes/No + tokens; T-ANIMAL-003 S14/S15). Scaffolding already on disk from History row 38. Gates: owner was dev-bot, plan_to_code Decision 30 approved 19:57, example false. No .env, no git init, testing: section not edited. |
| 40 | 2026-10-08T20:04:30+01:00 | in-development → in-review | dev-bot → review-bot | code_to_review + code_to_test · direct (option B) | dev-bot | Decision 30 UI done + scaffolding confirmed. Manifest: grid-cell-renderers.tsx (filled-circle Decision 30; scenarios T-ANIMAL-009/S1–S6,S8 + T-003/S14,S15 + T-006/S5); tokens.css S7/S8. code.tests scaffolding-ready; verification notes added (tsc pass, contrast S7, Api.Framework.Tests 21/21, e2e scaffold ready). **d29-1 Approve SUPERSEDED** (do not merge on it); review.verdict/code_verdict/test_verdict cleared; cycle 0 for fresh Decision 30 cycle (not round 4); report path d30-1. approvals.merge unset. Parent to message Review Bot and Test Bot together; Dev Bot did not message them. testing: section untouched. |
| 41 | 2026-10-08T20:11:00+01:00 | in-review | review-bot | pickup · direct (option B) | review-bot | Review Bot accepted Dev Bot's direct hand-off (20:04:30, History row 40) for the Decision 30 fresh review cycle, cycle 1 (not round 4): filled-circle boolean cells (grid-cell-renderers.tsx, tokens.css), T-ANIMAL-001..009 regressions, d29-1 open findings (F-19, F-26..F-30), and a code review of the test scaffolding in implementation.tests / TestData. d29-1 is superseded (not merged on). Gates checked: owner review-bot, stage in-review, example false, plan_to_code Decision 30 approved by Neil 19:57, manifest not empty. Report: reviews/DIRECT-manage-animals-d30-1-review.md. |
| 42 | 2026-10-08T20:22:13+01:00 | in-review | review-bot | d30-1 follow-up (no gate, no owner change) | dev-bot | Neil (20:19 BST) asked for the boolean cell glyph to be transparent instead of dark. renderBooleanIconCell now uses <Icon knockout="circle">: circle + Material Check/Close in one evenodd path, so the glyph is a hole and the row / hover background shows through in both themes. --app-boolean-glyph removed; fills unchanged; --system-green/--system-red unchanged; Yes/No/Not set, 1.6rem, em dash and renderBooleanSwitchCell unchanged. tsc pass. implementation manifest notes + verification updated; covered in the current d30-1 review. T-009 S1/S2/S7 still mention --app-boolean-glyph / glyph >= 4.5:1 (Plan Bot to reword). testing: not touched |
| 43 | 2026-10-08T20:29:03+01:00 | in-review | review-bot | plan doc fix (Neil 20:19 cut-out, no gate) | plan-bot | Neil 20:19 BST (via Dev Bot History row 42): boolean-cell glyph is a transparent cut-out (`Icon knockout="circle"`, evenodd) so the circle fill / row colour shows through the tick or cross. Planning docs amended to match: Decision 30 no longer requires `--app-boolean-glyph` / `#18181b` / glyph-vs-fill contrast; fills and fill tokens unchanged; T-ANIMAL-009 S1/S2/S7/S8 and T-ANIMAL-003 S14/S15 reworded in place (same IDs); spec + excel regenerated; journey updated. Doc-only — stage, owner, pickup, approvals, review and testing unchanged |
| 44 | 2026-10-08T20:36:00+01:00 | in-review → changes-requested | review-bot → dev-bot | review_feedback · direct (option B) | review-bot | Decision 30 cycle 1 code review (d30-1, incl. Dev Bot follow-ups 20:16:38 / 20:22:13 and Test Bot test-write notes 20:28 / 20:33): **Request changes**, provisional — awaiting test review (`test_verdict` untouched; TEST-manage-animals-1-report.md still 19:27). Blocker F-31 committed postgres password in appsettings.Test.json + e2e/README.md:34 (R8/R12/R8a). Minor F-32 unused scaffolding signInAs (suite uses real signInViaUi), F-33 trace artefacts capture reset key/passwords, F-34 Test ports shared with dev, F-35 R21 unit gaps. Nits F-36/F-37 + open F-19, F-27..F-30. F-26 resolved. Live knock-out: fill vs row 3.35/3.36 light, 5.61/5.75 dark; vs hover 3.21/3.22, 4.52/4.63; transparent cut-outs; role=img; non-interactive. Harness production notFound; EntityGrid sessionPermissions harness-only; animals-nodisplayname OK. Stale API (17:55): TestData 404. Report reviews/DIRECT-manage-animals-d30-1-review.md. |
| 45 | 2026-10-08T20:36:25+01:00 | changes-requested | plan-bot | 20:32 wipe recovered; content verified against snapshots; encoding repaired | plan-bot | Integrity check after 20:32:05 wipe. Machine file matched Review Bot snapshot `/workspace/rb-d30/out/handoff-new.md` (d30-1 Request changes → code, Blocker F-31; Test Bot testing: @ 20:33). Missing piece restored: plan-bot History row 43 (Neil 20:19 cut-out doc fix, from `/workspace/cut/after/handoff.md`); Review Bot's d30-1 History row renumbered 43→44. Encoding repaired (115 mojibake sequences → UTF-8). Front matter stage/owner/pickup left as Review Bot left them; no messages sent |
| 46 | 2026-10-08T20:45:00+01:00 | changes-requested -> in-review | dev-bot -> review-bot | code_to_review + code_to_test -> direct (option B, Decision 30 cycle 2) | dev-bot | Fixed d30-1 Request changes. **F-31 Blocker:** removed DB password from `appsettings.Test.json` (LoginConnection empty; fails closed without ConnectionStrings__LoginConnection) and e2e/README.md (env-only + least-privilege test role docs; Password= count 0). Minors: F-32 real UI signInAs (no __E2E_ACCESS_TOKEN); F-33 untraced reset contexts; F-34 Test ports 5188/7188; F-35 R6 name mismatch + R13 pending migrations + R13a baseline unit proofs. Nits: F-36 safe Conflict messages; F-37/F-27 BOM/EOL; F-28 Icon README; F-29 CSS module; F-30 drop redundant unity-auth-cleared; F-19 T-ANIMAL-008/S4-S6 on form/route manifest. Instant-modal/CompanyLoader left intact. Verify: Api.Framework.Tests 45 pass/2 skip; ui+e2e tsc pass. Neil still sets Test env secrets / least-privilege role / password rotation (agents never write .env*). |
| 47 | 2026-10-08T20:52:00+01:00 | in-review | review-bot | pickup + review_feedback · direct (option B, Decision 30 cycle 2) | review-bot | Review Bot accepted Dev Bot hand-off (History 46) and finished Decision 30 cycle 2 code review (d30-2): **Approve with comments**, provisional — awaiting test review (`test_verdict` untouched; TEST-manage-animals-1-report.md still 19:27; `testing:` untouched). d30-1 findings resolved: F-31 Blocker (appsettings.Test.json LoginConnection empty, Program fails closed, README env-only; Password= only in Dev appsettings + design-time factory), F-32 real UI signInAs, F-33 untraced resets, F-34 Test ports 5188/7188, F-35 R6/R13/R13a unit proofs, F-36 safe Conflict messages, F-37/F-27 BOM/EOL, F-28 README, F-29 CSS module, F-30 single unity-auth-cleared, F-19 T-ANIMAL-008/S4-S6 tags. New: Minor F-38 browser Back while pending modal is up leaves orphaned "Add Animal" shell over previous page (Cancel/Esc OK, no late modal); Nit F-39 e2e README duplicate paragraph inside env table; Nit F-40 Api.Framework.Tests.csproj mixed EOL. Live (own ZZ Test Animal 202610081946 T/F rows, deleted, GET 404): knock-out glyph vs fill 3.31/3.36 light, 5.47/5.75 dark; hover 3.17/3.22, 4.41/4.63; --app-boolean-glyph unset; role=img; non-interactive. Pending shell first paint 11-16 ms with CompanyLoader; Edit pending OK; harness noindex + local sessionPermissions (EntityGrid override harness-only). Verified Api.Framework.Tests 45 pass / 2 skip (temp copy) and ui + e2e tsc pass. Live API was Dev 5088/7088 (PID started 20:26:54); Test profile 5188/7188 not listening. Plan Bot T-009 glyph wording (History 43) closed. Stage stays in-review / owner review-bot; review.routed_to test. Report reviews/DIRECT-manage-animals-d30-2-review.md; log reviews/review-log.md. |
| 48 | 2026-10-09T09:05:00+01:00 | in-review | review-bot | test review · direct (option B; test round 2) → testing | review-bot | Test review of Test Bot round 2 (TEST-manage-animals-2-report.md, 08:51): **request-changes**, routed to **testing** (Test Bot); stage unchanged (in-review); this routing is test-fix round 1 of 5 when Test Bot re-runs (not a review cycle). Results 76 pass / 0 fail / 1 blocked (T-ANIMAL-007/S8 @skip @fixme, owner Plan Bot / Neil); unit 45 pass + 2 Skip; e2e + harness 64/64. **Major F-41 (security):** run-5 Playwright HTML report stores persona passwords in plain text on password Fill step titles (animals-tester 37, animals-viewer 4, animals-usermanager 1; reset key, tokens, connection string 0; test-results / trx / cucumber-report clean; earlier run-2 error-context copy wiped but treated as exposed) - Neil to rotate those three test passwords after the fix and delete e2e/playwright-report/. Minor F-42 S11/S13 reflection Facts empty and skipped for a stale reason (Api.Framework ProjectReference added in d30-2) so the S13 Program.cs policy Then is untested; F-43 S13 e2e GET-only, S11 lacks nothing-written read-back; F-44 testing.status should be blocked (run-tests-and-report step 7: no Fail but a Blocked frozen scenario) - approval then possible as blocked-noted under default (2) with "Tests blocked: T-007/S8"; F-46 F6 fillStable retry may mask early-input loss (not reproducible by Review Bot). Nits F-45 dialog selector also matches loading.tsx fallback, F-47 positional td. Confirmed: harness no-reset exemption (0 API requests live), no front-end mocks, reset-first on all 53 data scenarios + master reset in global setup, role personas, no secrets in test code, only api_framework_test and 5188/7188 (:3003 live calls go to 7188), api.steps.ts untraced sign-in fix in place. No code defects; code_verdict approve-with-comments unchanged; verdict null. testing: section untouched. Log reviews/review-log.md. |
| 49 | 2026-10-09T09:47:16+01:00 | in-review | review-bot | plan doc fix (T-ANIMAL-007 S8 baseline, no gate) | plan-bot | Neil 2026-10-09 09:46 BST approved the T-ANIMAL-007 S8 baseline and checks. S8 Given/When/Then rewritten in place (same ID and heading): seeded types EXAMPLE_STATUS and SHOWCASE_OPTION (2 active items each, existing migration seed, no extra reset rows; reset key reference-data.types-grid.baseline unchanged), user with user_management_read; exactly 2 rows in that order with Active items 2 / 2; columns Type key / Active items / Actions (last, not sortable); one Manage text button per row, no menu trigger; Manage on SHOWCASE_OPTION opens the Manage SHOWCASE_OPTION modal listing Widget and Gadget; close returns to the grid. Notes line added. Unblocks Test Bot to drop @fixme @skip on S8. Doc-only - front matter, stage, owner, review and testing unchanged |
| 50 | 2026-10-09T09:58:00+01:00 | in-review → approved | review-bot → human | test review · direct (option B; test round 3) → human | review-bot | Test review of Test Bot round 3 = test-fix round 1 of 5 (TEST-manage-animals-3-report.md incl. Addendum 09:48 and Addendum 2 09:56): **test_verdict approve**; with code_verdict approve-with-comments (d30-2 + Dev Bot code delta 09:08 / 09:35 reviewed) the **final verdict is approve-with-comments**; stage approved, owner human (Neil), pickup pending, routed_to human. Results 77 pass / 0 fail / 0 blocked (T-ANIMAL-007/S8 unblocked after Neil's 09:46 baseline, History 49, and passes against the rewritten Thens); unit 52/52 (0 Skip); e2e run 11 73/73 (67 + 6 setup), 0 flaky. Resolved: F-38, F-39, F-40, F-41 Major (setup sign-in in untraced child process e2e/setup/sign-in-child.cjs, password by env-var name only; Review Bot scan of 24 artefact files: 0 persona passwords, 0 reset key, 0 JWT outside e2e/.auth), F-42, F-43, F-44, F-45, F-47, F-46 (code defect fixed by Dev Bot with regression tests), F-48, F-49 (resolved/accepted), F-54 (handoff YAML parses; BEL removed). Open Nits: F-50 (:3003 shared with dev UI + reuseExistingServer; warm-up does not check API root), F-51 (fillStable retry), F-52 (rule-file blank line), F-55 (sign-in child inherits full env), F-56 (.next-test-tb not git-ignored); note F-53 (no ESLint config, pre-existing). Rule change for Neil: nextjs-modal-routing.mdc (one element per tid, -fallback / -pending / -shell / -loading; Back clears pending; early typing kept). Neil: rotate animals-tester / animals-viewer / animals-usermanager passwords. review.cycle stays 2; testing: section untouched. Log reviews/review-log.md. |
| 51 | 2026-10-09T12:38:49+01:00 | approved → merged | human | merge (human gate; Neil's instruction, no git) | plan-bot | merged — recorded by plan-bot on Neil's word to Dev Bot 2026-10-09 12:37 BST (no git; Neil's instruction is the merge). approvals.merge recorded (human, 12:37). Neil's open to-dos kept in waiting_on: test-password rotation (F-41) + e2e/.auth refresh, optional Nits, nextjs-modal-routing.mdc rule change |
| 52 | 2026-10-27T11:28:23+00:00 | merged | human | plan doc fix (Neil 2026-10-27 11:17 starter-workbook adoption, no gate) | plan-bot | Neil approved adopting his starter workbook (ai-planning-framework/templates/excel/page-spec-templates.xlsx) as the canonical Excel layout, keeping the pastel colours. specs/manage-animals.yaml: unity_feature renamed system_feature (Unity → System), required_permission: animals_write added to the page and to the Edit / Delete actions menu items (decision 24, no new behaviour). specs/add-edit-animal.yaml: required_permission: animals_write added (decision 24). Both workbooks regenerated in the starter layout (header rows 2-3 / 2-4, filter table row 9, Results Area row 12, Actions Menu row 19 with Req'd. Permission and Availability Logic columns). page_type stays Basic Form for Add | Edit Animal. Doc-only — stage, owner, pickup, approvals, review and testing unchanged; no code impact |
