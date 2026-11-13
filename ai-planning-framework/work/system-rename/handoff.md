---
# handoff.md: pipeline state for ONE feature. Rules: handoff/README.md
# Copy to <output.work_dir>/<feature>/handoff.md. Only the current `owner` edits
# this file, except the `testing` section, which the testing agent (test-bot) may
# write while review-bot owns the feature (handoff/README.md -> Testing alongside review). On every transition, update this front matter AND append a row to
# History. Paths are relative to this feature folder unless they start with ai-.
handoff_version: 1
example: false                # true = illustrative only; never picked up
feature: system-rename
feature_path: ai-planning-framework/work/system-rename   # output.work_dir/<feature>
stage: merged                # planned | in-development | in-review | changes-requested | approved | merged
owner: human             # plan-bot | dev-bot | review-bot | human   (agents.<role>.id in the config; test-bot is never an owner)
pickup: pending               # pending (handed over, not started) | accepted (owner is working it)
waiting_on: "Neil (system-rename merged 2026-10-09 14:47 BST on your word; no git): open to-dos. (1) Secret rotations: dev DB password, Jwt secret and DefaultUser:Password (D1); optionally E2E_TESTDATA_ADMIN_PASSWORD (review Notes round 2). (2) Decide F-01 (Angular example UI /v1 or the UI-contract wording). (3) F-56 deleted .next-test-tb although D16 said no manual deletion: reconcile (keep D16 or record the exception). (4) F-14: ratify the post-approval handoff edits in History rows 12-13 (incl. plan-bot row 13). Also restart the Development API (7088/5088 not listening since about 13:59; unity_login migrates on start). Optional Nits: Test Bot F-07 (npm run build when :3003 is free), F-10, F-11; Dev Bot F-12, F-13, F-15"
updated_at: 2026-10-09T15:58:22+01:00
updated_by: plan-bot
parked: false                 # true = the human owner has paused this feature; read-only for every agent until resumed (handoff/README.md rule 13)
parked_at: null               # ISO 8601 with offset, set when parked
parked_by: null               # human (only the human owner parks or resumes)

routes:                       # the route actually used (from handoff in the config)
  plan_to_code: direct        # devops | direct   (set by the planning agent at hand-off)
  code_to_review: direct      # pr | direct       (set by the implementing agent at hand-off)
  code_to_test: direct        # direct            (set by the implementing agent at the same hand-off; the testing agent runs alongside the review)
  review_feedback: direct     # direct

tickets:                      # every T-<DOMAIN>-NNN in tickets/; id must match the filename
  - id: T-RENAME-001
    file: tickets/T-RENAME-001-api-remove-v1-versioning.md
    devops_work_item_id: null
  - id: T-RENAME-002
    file: tickets/T-RENAME-002-api-unity-to-system.md
    devops_work_item_id: null
  - id: T-RENAME-003
    file: tickets/T-RENAME-003-ui-code-renames.md
    devops_work_item_id: null
  - id: T-RENAME-004
    file: tickets/T-RENAME-004-ui-visible-text-runtime-keys.md
    devops_work_item_id: null
  - id: T-RENAME-005
    file: tickets/T-RENAME-005-v1-consumers.md
    devops_work_item_id: null
  - id: T-RENAME-006
    file: tickets/T-RENAME-006-code-framework-docs.md
    devops_work_item_id: null
  - id: T-RENAME-007
    file: tickets/T-RENAME-007-gate-selftest-fixtures.md
    devops_work_item_id: null
  - id: T-RENAME-008
    file: tickets/T-RENAME-008-test-framework-docs-e2e-steps.md
    devops_work_item_id: null
  - id: T-RENAME-009
    file: tickets/T-RENAME-009-planning-framework-and-config.md
    devops_work_item_id: null
  - id: T-RENAME-010
    file: tickets/T-RENAME-010-review-framework-checklists.md
    devops_work_item_id: null
  - id: T-RENAME-011
    file: tickets/T-RENAME-011-neil-steps-final-verification.md
    devops_work_item_id: null

devops:                       # only when plan_to_code = devops
  board_url: null
  published_at: null

code:                         # set by the implementing agent; repos from development.api/ui active paths
  api:
    repo: ai-code-framework/api/API.Framework
    branch: null              # handoff.branch_pattern; same name in every repo touched. Required for the PR route
                              # and direct_scope: diff; optional for direct_scope: plan (null if not a git repo)
    base_branch: null         # PR target / diff base (review.target_branch unless stated); not used by direct_scope: plan
    head_commit: null         # commit handed to review, when the repo is under git
  ui:
    repo: ai-code-framework/ui/UI.NextJs.Framework
    branch: null
    base_branch: null
    head_commit: null
  build: pass                 # pass | fail
  tests: pass                 # pass | fail  (existing tests and checks the implementing agent ran; scenario test results are in `testing`)
  verification:               # commands run, e.g. "dotnet test ... --filter ...", plus one line per pre-handoff check (never a secret value)
    - "dotnet build Api.Framework.sln --configuration Release -> pass (0 errors; 5 warnings, all pre-existing: NU1510 x2, xUnit1031 x3)"
    - "dotnet test Api.Framework.Tests --configuration Release -> pass (57/57)"
    - "dotnet ef migrations add RenameUnityToSystem (Api.Framework.Data, startup Api.Framework, Release) -> 20261009114033_RenameUnityToSystem (UpdateData by id only)"
    - "ASPNETCORE_ENVIRONMENT=Test dotnet ef database update -> applied to api_framework_test; features 7 / permissions 25 / tenant_features 14 before and after; 0 unity names left; unity_login (dev DB) not touched"
    - "backup compare: 16 pre-existing migration files byte-identical to D:\\Users\\nwood01\\Documents\\Candc\\backups\\ai-framework-pre-rename-20261009-1120.zip; only LoginDbContextModelSnapshot.cs differs (T-RENAME-002/S4)"
    - "UI: npm run typecheck -> pass; npm run lint -> 0 errors, 2 warnings (pre-existing, animal-ui-schema.ts unused params); npm test (vitest) -> 10/10"
    - "e2e: npx tsc --noEmit -p e2e/tsconfig.json -> pass; npx bddgen -> pass"
    - "node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs -> pass (64 ok)"
    - "smoke API (Test env, Release, :7189/:5189): swagger.json 46 paths / 66 operations, none with /v1; swagger UI 200; POST /Authorisation/SignIn 200, token iss/aud system-login; GET /Animal, /schemas/create-animal, /Authorisation/Me 200; /v1/Animal, /v1/schemas/create-animal, /v1/Authorisation/Me, /v1/Authorisation/SignIn, /v1/TestData/Reset/master 404; unity-login token 401 (same claims re-signed as system-login 200); CORS preflight from http://localhost:3003 allowed (SystemUi); no api-supported-versions header; POST /TestData/Reset/master 200 (reseeded with System names)"
    - "smoke UI (dev:test :3023 -> https://localhost:7189/, scratch build dir removed afterwards): heading System Login, intro and title System UI Next; sign-in as animals-tester OK; sessionStorage system-auth-session only; localStorage system-theme only; API calls POST /Authorisation/SignIn, GET /Animal, GET /schemas/create-animal on :7189 without /v1; nothing called :7104"
    - "leftover scan (git grep, active targets, excl. bin/obj/node_modules/.next*/Migrations/.auth/.env*): every remaining Unity hit is the real Unity product/repos (D10), unity_login (D7) or Test Bot's auth.steps.ts comment (T-RENAME-008); every remaining /v1 is versionless guidance, the Swagger doc v1 (D6), the stale-/v1 guard in e2e/helpers/config.ts or Test Bot's animals.steps.ts regexes (T-RENAME-008)"
    - "post-approval follow-up (2026-10-09T13:47:00+01:00, History row 12): dotnet build Api.Framework.sln --configuration Release -> pass (0 errors; 5 warnings, all pre-existing: NU1510 x2, xUnit1031 x3), built with the Test API stopped (bin/Release lock)"
    - "post-approval follow-up: dotnet test Api.Framework.Tests --configuration Release -> pass (68/68; new SystemUiCorsTests 6/6; TokenIssuerTests 5/5 covers F-03)"
    - "post-approval follow-up: UI npm test (vitest) -> 26/26 in 6 files (new e2e/helpers/config.test.ts 9, scripts/api-root.test.mjs 7); npx tsc --noEmit -p e2e/tsconfig.json -> pass; dev:test with E2E_UI_API_ROOT ending /v1/ -> exit 1 with the stale-/v1 message before next dev starts"
    - "post-approval follow-up: Test API (launch profile Test, Release, :7188/:5188, env from the registry) restarted as pid 32536; OPTIONS /Authorisation/SignIn with Origin http://localhost:3013 -> 204 + Access-Control-Allow-Origin: http://localhost:3013 on both ports (https://localhost:3013 and http://localhost:3003 also allowed; http://localhost:9999 -> 204 with no CORS headers); GET /schemas/sign-in 200, /v1/schemas/sign-in 404. Neil's dev API (7088, pid 2732) and UI (3003) not touched"
    - "pre-handoff: eol api-framework -> pass (221 files, 0 findings)"
    - "pre-handoff: secrets api-framework -> pass (221 files, 0 skipped secret files, 0 findings)"
    - "pre-handoff: docs-dup api-framework -> pass (22 docs, 0 findings, 54 allowlisted)"
    - "pre-handoff: unit api-framework -> pass (68 passed, 0 failed, 0 skipped, 0 findings)"
    - "pre-handoff: lint nextjs -> pass (152 files, 0 errors, 2 warnings, 0 findings)"
    - "pre-handoff: typecheck nextjs -> pass (0 errors, 0 findings)"
    - "pre-handoff: eol nextjs -> pass (234 files, 0 findings)"
    - "pre-handoff: secrets nextjs -> pass (234 files, 2 skipped secret files, 0 findings)"
    - "pre-handoff: docs-dup nextjs -> pass (17 docs, 0 findings)"
    - "pre-handoff: unit nextjs -> pass (26 passed, 0 failed, 6 files, 0 findings)"
    - "pre-handoff: api-framework: not a git repo: working tree scanned"
    - "pre-handoff: nextjs: not a git repo: working tree scanned"
  pre_handoff_gate: pass      # pass | fail   result of the LAST pre-handoff run (config `verification`; feature-build stage 5).
                              # in-development / changes-requested -> in-review needs pass
  pre_handoff_gate_at: 2026-10-09T13:43:28+01:00   # ISO 8601 with offset of that run

implementation:               # MANIFEST of what the implementing agent built; the reviewing agent's starting point for direct_scope: plan
  # Filled by the implementing agent at self-review / hand-off. Hand-off is BLOCKED while every list is empty.
  # One entry per file that implements the plan: files created or changed for the feature, plus
  # existing files the feature relies on to render a control or persist a mapping (change: existing).
  # `path` is repo-relative under code.api.repo (api, migrations) or code.ui.repo (ui); tests say which.
  # Never list build output, node_modules, bin/obj, generated files or secret / .env files.
  recorded_at: 2026-10-09T13:47:00+01:00   # ISO 8601 with offset
  # Rename only: no spec pages, controls or DB columns. tests[] also holds framework files outside both repos (repo: framework, ai- paths).
  # Not edited (owners per plan): e2e/features/** (Test Bot, T-RENAME-008), ai-framework.config.yaml (Plan Bot, T-RENAME-009, done), Review Bot checklists (T-RENAME-010), .env.local / .env.example (Neil, T-RENAME-011 N1/N2).
  api:
    - path: "Api.Framework/Program.cs"
      change: modified
      tickets: [T-RENAME-001, T-RENAME-002]
      note: "using Asp.Versioning and the AddApiVersioning block (URL-segment + x-api-version readers, ApiExplorer substitution) removed; using Api.Framework.Controllers.TestData; CORS policy UnityUi -> SystemUi (AddPolicy + UseCors); SwaggerDoc 'v1' and /swagger/v1/swagger.json kept (D6); post-approval (row 12): CORS via AddSystemUiCors(builder.Configuration) + UseCors(SystemUiCors.PolicyName), origins from Cors:AllowedOrigins"
      scenarios: [T-RENAME-001/S3, T-RENAME-001/S5, T-RENAME-002/S1]
    - path: "Api.Framework/Api.Framework.csproj"
      change: modified
      tickets: [T-RENAME-001]
      note: "Asp.Versioning.Mvc and Asp.Versioning.Mvc.ApiExplorer 10.2.1 removed (D2)"
      scenarios: [T-RENAME-001/S3]
    - path: "Api.Framework/Controllers/Animals/AnimalController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Animals/AnimalController.cs (D1); namespace Api.Framework.Controllers.Animals; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Auth/AuthController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Auth/AuthController.cs (D1); namespace Api.Framework.Controllers.Auth; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Directory/DirectoryControllers.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Directory/DirectoryControllers.cs (D1); namespace Api.Framework.Controllers.Directory; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Directory/TenantController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Directory/TenantController.cs (D1); namespace Api.Framework.Controllers.Directory; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Examples/AddressLookupController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Examples/AddressLookupController.cs (D1); namespace Api.Framework.Controllers.Examples; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Examples/CatalogueItemController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Examples/CatalogueItemController.cs (D1); namespace Api.Framework.Controllers.Examples; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Examples/ComponentShowcaseController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Examples/ComponentShowcaseController.cs (D1); namespace Api.Framework.Controllers.Examples; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/ReferenceData/ReferenceDataController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/ReferenceData/ReferenceDataController.cs (D1); namespace Api.Framework.Controllers.ReferenceData; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Schemas/AnimalSchemaController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Schemas/AnimalSchemaController.cs (D1); namespace Api.Framework.Controllers.Schemas; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Schemas/ExampleSchemaController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Schemas/ExampleSchemaController.cs (D1); namespace Api.Framework.Controllers.Schemas; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Schemas/ReferenceDataSchemaController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Schemas/ReferenceDataSchemaController.cs (D1); namespace Api.Framework.Controllers.Schemas; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Schemas/SignInSchemaController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Schemas/SignInSchemaController.cs (D1); namespace Api.Framework.Controllers.Schemas; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/Schemas/TenantSchemaController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/Schemas/TenantSchemaController.cs (D1); namespace Api.Framework.Controllers.Schemas; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/Controllers/TestData/TestDataController.cs"
      change: modified
      tickets: [T-RENAME-001]
      note: "moved from Controllers/V1/TestData/TestDataController.cs (D1); namespace Api.Framework.Controllers.TestData; [ApiVersion(\"1\")] and using Asp.Versioning removed; route prefix v{version:apiVersion}/ dropped"
      scenarios: [T-RENAME-001/S1, T-RENAME-001/S2, T-RENAME-001/S4]
    - path: "Api.Framework/appsettings.json"
      change: modified
      tickets: [T-RENAME-002]
      note: "Jwt Issuer / Audience unity-login -> system-login (no secret touched); post-approval (row 12): Cors:AllowedOrigins = the 4 origins Program.cs used to hard-code (4200 / 3003, http + https)"
      scenarios: [T-RENAME-002/S2]
    - path: "Api.Framework/appsettings.Test.json"
      change: modified
      tickets: [T-RENAME-002]
      note: "Jwt Issuer / Audience unity-login -> system-login; post-approval (row 12): Cors:AllowedOrigins = the 4 defaults + http(s)://localhost:3013 for the Test UI (config arrays merge by index, so the full list)"
      scenarios: [T-RENAME-002/S2]
    - path: "Api.Framework/Cors/SystemUiCors.cs"
      change: added
      tickets: [T-RENAME-002]
      note: "post-approval (row 12): SystemUi CORS policy; origins from Cors:AllowedOrigins (trimmed, no trailing slash, de-duplicated); throws naming the setting when none are configured"
      scenarios: [T-RENAME-002/S1]
    - path: "Api.Framework.Services/Options/JwtOptions.cs"
      change: modified
      tickets: [T-RENAME-002]
      note: "Issuer / Audience defaults system-login"
      scenarios: [T-RENAME-002/S2]
    - path: "Api.Framework.Data/LoginFeatures.cs"
      change: modified
      tickets: [T-RENAME-002]
      note: "BasicName SystemBasicFeatures; feature 3 System messenger (name + permission category); summary comment"
      scenarios: [T-RENAME-002/S3]
    - path: "Api.Framework.Data/LoginPermissions.cs"
      change: modified
      tickets: [T-RENAME-002]
      note: "system_messenger_dashboard; category System messenger on ids 3, 4, 12; summary comment (System UI)"
      scenarios: [T-RENAME-002/S3]
    - path: "Api.Framework.Services/DataFramework/JsonSchemaValidation/ReferenceDataSchemaBinding.cs"
      change: existing
      tickets: [T-RENAME-002]
      note: "kept: \"Unity's schema builder\" names the real Unity product (D10)"
      scenarios: [T-RENAME-002/S6]
    - path: "Api.Framework.Tests/TestData/TestDataGuardAndServiceTests.cs"
      change: existing
      tickets: [T-RENAME-002]
      note: "kept: \"unity_login\" is the dev database name (D7)"
      scenarios: [T-RENAME-002/S6]
    - path: "Api.Framework/Api.Framework.http"
      change: modified
      tickets: [T-RENAME-005]
      note: "4 requests without /v1"
      scenarios: [T-RENAME-005/S5]
    - path: "AGENTS.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "System JSON schema forms; versionless routes; Controllers/{Area}; NEXT_PUBLIC_SYSTEM_API_ROOT without /v1/"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S4]
    - path: "CLAUDE.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "schema controllers in Controllers/Schemas"
      scenarios: [T-RENAME-006/S1]
    - path: ".cursor/rules/api-framework-auth-permissions.mdc"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/rules/api-framework-auth-permissions.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/rules/api-framework-controllers.mdc"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/rules/api-framework-controllers.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/rules/api-framework-overview.mdc"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/rules/api-framework-overview.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/rules/api-framework-testing.mdc"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/rules/api-framework-testing.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/rules/api-framework-ui-contract.mdc"
      change: modified
      tickets: [T-RENAME-006]
      note: "post-approval (row 12): CORS section describes Cors:AllowedOrigins (defaults + Test 3013)"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/rules/api-framework-ui-contract.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy (incl. the post-approval CORS section, row 12)"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/rules/json-schema-forms.mdc"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/rules/json-schema-forms.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/skills/api-framework-crud-feature/SKILL.md"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/skills/api-framework-crud-feature/SKILL.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/skills/api-framework-json-schema/SKILL.md"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/skills/api-framework-json-schema/SKILL.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".cursor/skills/api-framework-ui-contract/SKILL.md"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
    - path: ".claude/skills/api-framework-ui-contract/SKILL.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "same edits as the .cursor copy"
      scenarios: [T-RENAME-006/S1, T-RENAME-006/S2]
  ui:
    - path: "package.json"
      change: modified
      tickets: [T-RENAME-003]
      note: "name system-ui-next"
      scenarios: [T-RENAME-003/S5]
    - path: "package-lock.json"
      change: modified
      tickets: [T-RENAME-003]
      note: "the two name fields only; dependency tree unchanged"
      scenarios: [T-RENAME-003/S5]
    - path: "scripts/dev-test.mjs"
      change: modified
      tickets: [T-RENAME-003, T-RENAME-005]
      note: "sets NEXT_PUBLIC_SYSTEM_API_ROOT; default E2E_UI_API_ROOT https://localhost:7188/; post-approval (row 12, F-05): E2E_UI_API_ROOT resolved by scripts/api-root.mjs (blank or trailing /v1 fails fast, exit 1)"
      scenarios: [T-RENAME-003/S3, T-RENAME-005/S4]
    - path: "scripts/api-root.mjs"
      change: added
      tickets: [T-RENAME-005]
      note: "post-approval (row 12, F-05): resolveTestApiRoot: unset/empty -> https://localhost:7188/; blank or trailing /v1 -> error naming E2E_UI_API_ROOT, never its value"
      scenarios: [T-RENAME-005/S3, T-RENAME-005/S4]
    - path: "vitest.config.mts"
      change: modified
      tickets: [T-RENAME-005]
      note: "post-approval (row 12): include also e2e/helpers/**/*.test.ts and scripts/**/*.test.mjs (Node tests, @vitest-environment node)"
    - path: "src/config/environment.ts"
      change: modified
      tickets: [T-RENAME-003]
      note: "reads NEXT_PUBLIC_SYSTEM_APP_ID / NEXT_PUBLIC_SYSTEM_API_ROOT; fallback values unchanged (D14)"
      scenarios: [T-RENAME-003/S3]
    - path: "src/framework/api/system-api-fetch.ts"
      change: added
      tickets: [T-RENAME-003, T-RENAME-004]
      note: "renamed from src/framework/api/unity-api-fetch.ts; systemApiFetch, readSystemApiJson, isSystemApiSuccess, SystemApiFetchInit, isUnauthenticatedSystemApiUrl; \"System API returned ...\" / \"Unable to reach System API\" errors"
      scenarios: [T-RENAME-003/S1, T-RENAME-003/S2, T-RENAME-004/S1]
    - path: "src/framework/auth/storage/system-cookie.service.ts"
      change: added
      tickets: [T-RENAME-003, T-RENAME-004]
      note: "renamed from src/framework/auth/storage/unity-cookie.service.ts; systemCookieService; dispatches system-auth-cleared"
      scenarios: [T-RENAME-003/S1, T-RENAME-004/S4]
    - path: "src/framework/json-schema-form/components/renderers/system-json-form-renderers.tsx"
      change: added
      tickets: [T-RENAME-003]
      note: "renamed from src/framework/json-schema-form/components/renderers/unity-json-form-renderers.tsx; System* renderers, systemJsonFormRenderers"
      scenarios: [T-RENAME-003/S1, T-RENAME-003/S2]
    - path: "src/framework/json-schema-form/models/system-json-schema.model.ts"
      change: added
      tickets: [T-RENAME-003]
      note: "renamed from src/framework/json-schema-form/models/unity-json-schema.model.ts; SystemJsonSchema* types; line 65 keeps the real Unity schema endpoint reference (D10)"
      scenarios: [T-RENAME-003/S1]
    - path: "src/framework/json-schema-form/schema/system-schema-api.mapper.ts"
      change: added
      tickets: [T-RENAME-003]
      note: "renamed from src/framework/json-schema-form/schema/unity-schema-api.mapper.ts"
      scenarios: [T-RENAME-003/S1]
    - path: "src/framework/json-schema-form/schema/system-schema-value.mapper.ts"
      change: added
      tickets: [T-RENAME-003]
      note: "renamed from src/framework/json-schema-form/schema/unity-schema-value.mapper.ts"
      scenarios: [T-RENAME-003/S1]
    - path: "src/framework/json-schema-form/schema/system-schema.adapter.ts"
      change: added
      tickets: [T-RENAME-003]
      note: "renamed from src/framework/json-schema-form/schema/unity-schema.adapter.ts"
      scenarios: [T-RENAME-003/S1]
    - path: "src/framework/json-schema-form/validation/system-schema-validation.ts"
      change: added
      tickets: [T-RENAME-003]
      note: "renamed from src/framework/json-schema-form/validation/unity-schema-validation.ts; error-object keyword 'unity' -> 'system'; validateSystemSchemaData"
      scenarios: [T-RENAME-003/S1, T-RENAME-003/S4]
    - path: "src/framework/json-schema-form/index.ts"
      change: modified
      tickets: [T-RENAME-003]
      note: "barrel re-exports the system-* files"
      scenarios: [T-RENAME-003/S2]
    - path: "src/framework/json-schema-form/components/JsonSchemaForm.tsx"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/json-schema-form/components/JsonSchemaForm.test.tsx"
      change: modified
      tickets: [T-RENAME-003]
      scenarios: [T-RENAME-003/S4]
    - path: "src/framework/json-schema-form/hooks/use-json-schema-entity-form.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/json-schema-form/hooks/use-json-schema-entity-form.test.tsx"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/json-schema-form/services/json-schema-data.service.ts"
      change: modified
      tickets: [T-RENAME-003]
      note: "fetch/prefetch/clear/requestSystemJsonSchema"
    - path: "src/framework/entity-framework/providers/abstract-entity.data-provider.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/entity-framework/providers/abstract-search.data-provider.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/auth/providers/authorisation.data-provider.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/auth/token-refresh.service.ts"
      change: modified
      tickets: [T-RENAME-003, T-RENAME-004]
      note: "dispatches system-auth-refreshed"
      scenarios: [T-RENAME-004/S5]
    - path: "src/framework/auth/context/AuthProvider.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "listens for system-auth-refreshed / system-auth-cleared"
      scenarios: [T-RENAME-004/S4, T-RENAME-004/S5]
    - path: "src/framework/auth/constants/auth-cookies.ts"
      change: modified
      tickets: [T-RENAME-004]
      note: "AUTH_SESSION_STORAGE_KEY system-auth-session; line 1 keeps the real Unity.UI.Framework UnityCookieService reference (D10)"
      scenarios: [T-RENAME-004/S2, T-RENAME-004/S6]
    - path: "src/framework/auth/models/auth-state.model.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/auth/normalize-auth-state.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/design-system/theme/ThemeProvider.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "localStorage key system-theme"
      scenarios: [T-RENAME-004/S3, T-RENAME-004/S6]
    - path: "src/framework/design-system/components/modal/use-modal-navigate.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/framework/README.md"
      change: modified
      tickets: [T-RENAME-006]
    - path: "src/framework/design-system/README.md"
      change: modified
      tickets: [T-RENAME-004, T-RENAME-006]
      note: "system-theme"
    - path: "src/app/layout.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "title System UI Next; inline theme script reads system-theme; description keeps 'Unity-style' (D10)"
      scenarios: [T-RENAME-004/S1, T-RENAME-004/S3]
    - path: "src/app/auth/sign-in/page.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "Sign in with your System credentials."
      scenarios: [T-RENAME-004/S1]
    - path: "src/features/auth/sign-in/SignInForm.tsx"
      change: modified
      tickets: [T-RENAME-003, T-RENAME-004]
      note: "heading System Login; systemCookieService"
      scenarios: [T-RENAME-004/S1]
    - path: "src/app/examples/reference-data/page.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "visible text: wired to System ReferenceData"
    - path: "src/app/examples/reference-data/manage/[referenceDataType]/page.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "visible text: wired to System ReferenceData"
    - path: "src/app/examples/reference-data/manage/[referenceDataType]/item/page.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "visible text: wired to System ReferenceData"
    - path: "src/app/examples/reference-data/manage/[referenceDataType]/item/[id]/page.tsx"
      change: modified
      tickets: [T-RENAME-004]
      note: "visible text: wired to System ReferenceData"
    - path: "src/features/animals/manage-animals/ManageAnimals.tsx"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/features/animals/animal-form-modal/state/animal-ui-schema.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/features/animals/shared/models/animal.model.ts"
      change: modified
      tickets: [T-RENAME-005]
      note: "comment: from `Animal` (no v1)"
    - path: "src/features/reference-data/manage-reference-data-items-modal/ManageReferenceDataItemsModal.tsx"
      change: modified
      tickets: [T-RENAME-003]
    - path: "src/features/reference-data/reference-data-item-form-modal/state/reference-data-item-ui-schema.ts"
      change: modified
      tickets: [T-RENAME-003]
    - path: "README.md"
      change: modified
      tickets: [T-RENAME-005, T-RENAME-006]
      note: "System UI Next; NEXT_PUBLIC_SYSTEM_* names; API root without /v1/; systemApiFetch"
      scenarios: [T-RENAME-005/S5]
    - path: "AGENTS.md"
      change: modified
      tickets: [T-RENAME-006]
      note: "systemApiFetch; NEXT_PUBLIC_SYSTEM_API_ROOT / _APP_ID Neil-owned"
      scenarios: [T-RENAME-006/S4]
    - path: "e2e/README.md"
      change: modified
      tickets: [T-RENAME-005]
      note: "no /v1; NEXT_PUBLIC_SYSTEM_API_ROOT; API_URL default http://localhost:5188; unity_login kept (D7); post-approval (row 12): blank API_URL error, E2E_UI_API_ROOT guard, Test API CORS 3003 / 3013"
      scenarios: [T-RENAME-005/S5]
    - path: ".cursor/rules/framework/nextjs-framework-overview.mdc"
      change: modified
      tickets: [T-RENAME-006]
      scenarios: [T-RENAME-006/S4]
    - path: ".cursor/rules/framework/nextjs-json-schema-forms.mdc"
      change: modified
      tickets: [T-RENAME-006]
    - path: ".cursor/rules/framework/nextjs-modal-routing.mdc"
      change: modified
      tickets: [T-RENAME-006]
    - path: ".cursor/rules/framework/nextjs-state-layer.mdc"
      change: modified
      tickets: [T-RENAME-006]
    - path: ".cursor/rules/style/nextjs-css.mdc"
      change: modified
      tickets: [T-RENAME-006]
    - path: ".cursor/rules/style/nextjs-design-system.mdc"
      change: modified
      tickets: [T-RENAME-006]
  tests:                      # test SCAFFOLDING the implementing agent owns: Api.Framework.Tests project, Playwright / e2e setup, test-data fixtures. Scenario tests are recorded by the testing agent in testing.results
    - path: "Api.Framework.Tests/Animals/AnimalPoliciesTests.cs"
      repo: api
      change: modified
      tickets: [T-RENAME-001]
      note: "imports Api.Framework.Controllers.Animals / .Schemas; comment without v1"
      scenarios: [T-RENAME-001/S4, T-RENAME-001/S6]
    - path: "e2e/helpers/config.ts"
      repo: ui
      change: modified
      tickets: [T-RENAME-005]
      note: "getApiUrl: no /v1 appended, default http://localhost:5188, fails fast naming API_URL when it still ends with /v1 (S3 default); post-approval (row 12, F-04): a blank (whitespace-only) API_URL also fails fast naming API_URL"
      scenarios: [T-RENAME-005/S1, T-RENAME-005/S2, T-RENAME-005/S3]
    - path: "e2e/helpers/authentication.ts"
      repo: ui
      change: modified
      tickets: [T-RENAME-004]
      note: "session key system-auth-session"
      scenarios: [T-RENAME-004/S2]
    - path: "e2e/setup/sign-in-child.cjs"
      repo: ui
      change: modified
      tickets: [T-RENAME-004]
      note: "session key system-auth-session (setup sign-in child)"
      scenarios: [T-RENAME-004/S2]
    - path: "ai-code-framework/scripts/pre-handoff-checks.selftest.mjs"
      repo: framework
      change: modified
      tickets: [T-RENAME-007]
      note: "inline fixtures: system-login (5), https://localhost:7188/ (1); expectations unchanged"
      scenarios: [T-RENAME-007/S1, T-RENAME-007/S2]
    - path: "ai-code-framework/scripts/fixtures/pre-handoff/api-bad/appsettings.json"
      repo: framework
      change: modified
      tickets: [T-RENAME-007]
      note: "system-login / no /v1/ (CRLF kept)"
      scenarios: [T-RENAME-007/S2]
    - path: "ai-code-framework/scripts/fixtures/pre-handoff/api-bad/appsettings.Commented.json"
      repo: framework
      change: modified
      tickets: [T-RENAME-007]
      note: "system-login / no /v1/ (CRLF kept)"
      scenarios: [T-RENAME-007/S2]
    - path: "ai-code-framework/scripts/fixtures/pre-handoff/api-good/appsettings.json"
      repo: framework
      change: modified
      tickets: [T-RENAME-007]
      note: "system-login / no /v1/ (CRLF kept)"
      scenarios: [T-RENAME-007/S2]
    - path: "ai-code-framework/scripts/fixtures/pre-handoff/api-good/appsettings.Development.json"
      repo: framework
      change: modified
      tickets: [T-RENAME-007]
      note: "system-login / no /v1/ (CRLF kept)"
      scenarios: [T-RENAME-007/S2]
    - path: "ai-code-framework/.cursor/rules/api-json-schema-forms.mdc"
      repo: framework
      change: modified
      tickets: [T-RENAME-006]
      note: "framework rule (doc, outside both repos): Controllers/{Area}, Controllers/Schemas"
      scenarios: [T-RENAME-006/S1]
    - path: "ai-code-framework/loops/feature-build.md"
      repo: framework
      change: modified
      tickets: [T-RENAME-006]
      note: "framework doc: Next.js calls the active API through systemApiFetch"
    - path: "Api.Framework.Tests/Cors/SystemUiCorsTests.cs"
      repo: api
      change: added
      tickets: [T-RENAME-002]
      note: "post-approval (row 12): policy uses the configured origins; preflight from a configured origin allowed, other origin not; trimming / de-dup; nothing configured throws; appsettings.json = 4 defaults; + appsettings.Test.json adds 3013"
      scenarios: [T-RENAME-002/S1]
    - path: "e2e/helpers/config.test.ts"
      repo: ui
      change: added
      tickets: [T-RENAME-005]
      note: "post-approval (row 12, F-04): getApiUrl default, trimming, blank-value error, stale-/v1 guard (message never prints the value); runs in root npm test"
      scenarios: [T-RENAME-005/S2, T-RENAME-005/S3]
    - path: "scripts/api-root.test.mjs"
      repo: ui
      change: added
      tickets: [T-RENAME-005]
      note: "post-approval (row 12, F-05): resolveTestApiRoot default, blank-value error, stale-/v1 guard"
      scenarios: [T-RENAME-005/S3, T-RENAME-005/S4]
  migrations:
    - path: "Api.Framework.Data/Migrations/20261009114033_RenameUnityToSystem.cs"
      change: added
      tickets: [T-RENAME-002]
      note: "dotnet ef migrations add RenameUnityToSystem: UpdateData by existing ids only (features ...201, ...203; permissions ...003, ...004, ...012); Down restores the Unity names; applied to api_framework_test"
      scenarios: [T-RENAME-002/S3]
    - path: "Api.Framework.Data/Migrations/20261009114033_RenameUnityToSystem.Designer.cs"
      change: added
      tickets: [T-RENAME-002]
      note: "generated by dotnet ef (BOM stripped)"
      scenarios: [T-RENAME-002/S3]
    - path: "Api.Framework.Data/Migrations/LoginDbContextModelSnapshot.cs"
      change: modified
      tickets: [T-RENAME-002]
      note: "regenerated by dotnet ef (BOM stripped); the 16 older migration files are byte-identical to the 11:20 backup"
      scenarios: [T-RENAME-002/S3, T-RENAME-002/S4]
  # Entry shape (copy into the lists above):
  #  - path: Unity.API/Controllers/V2/<Name>Controller.cs
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
  cycle: 1                    # +1 each time a code-review round ends with a final verdict or a change request (max handoff.max_review_cycles).
                              # Test-fix rounds do NOT count here (testing.failures_count_toward_review_cycles: false); see testing.test_fix_cycle
  report: reviews/DIRECT-system-rename-1-review.md                # latest full report: reviews/PR-<id>-review.md | reviews/DIRECT-<branch-slug>-<n>-review.md
  log: reviews/review-log.md                   # reviews/review-log.md (review.log_file); every code review and test review, both routes
  code_verdict: approve-with-comments          # PROVISIONAL code-review verdict until the test review: approve | approve-with-comments | request-changes
  test_verdict: approve          # test review (testing.test_review): approve | request-changes | blocked-noted (testing blocked, approval allowed by default (2))
  verdict: approve-with-comments               # FINAL: approve | approve-with-comments only when testing.final_approval_requires are all met; request-changes otherwise
  routed_to: null             # who fixes the latest findings: code | testing | both (testing.defect_routing)
  reviewed_commits: {api: "not under git", ui: "not under git"}   # compared with the 2026-10-09 11:20 backup zip

testing:                      # CARVE-OUT: written ONLY by the testing agent (test-bot), also while review-bot owns the feature.
  # Everything else in this file stays the owner's. Rules: handoff/README.md -> Testing alongside review.
  status: passed              # pending | running | passed | failed | blocked   (running = the testing agent has picked the run up)
                              # passed = run 2: no Fail, no Waiting/Blocked (T-RENAME-011/S1 passed after N1)
  round: 2                    # +1 per test run; n in tests/TEST-<feature>-<n>-report.md
  test_fix_cycle: 0           # test-fix rounds used / max testing.max_test_fix_cycles (5); separate from review.cycle. +1 when the testing agent
                              # starts the re-run after a failure was routed back (code or test defect); at max, the next one escalates to the human owner
  plan: tests/test-plan.md
  report: tests/TEST-system-rename-2-report.md   # latest run; log tests/test-log.md
  summary:                    # counts from the latest report
    scenarios: 50
    passed: 36
    failed: 0
    blocked: 0
    waiting: 0
    not_automated: 14
  results:                    # one entry per scenario, keyed by the ticket's explicit ID (testing.scenario_ids: explicit)
    - scenario: T-RENAME-001/S1
      layers: [api-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-001/S1", "e2e/features/animals/AnimalsApi.feature (15 scenarios)"]
      result: pass
      note: "GET /schemas/create-animal 200 (JSON object), GET /Animal 200; old /v1 body no longer comparable"
    - scenario: T-RENAME-001/S2
      layers: [api-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-001/S2"]
      result: pass
      note: "GET /v1/Animal and /v1/schemas/create-animal -> 404"
    - scenario: T-RENAME-001/S3
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-001/S3]"]
      result: pass
      note: "0 versioning hits in source (one guidance line saying routes have no version)"
    - scenario: T-RENAME-001/S4
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-001/S4]"]
      result: pass
      note: "no V1 folder; same 14 controller files as the backup under Controllers/{Area}; 0 Controllers.V1"
    - scenario: T-RENAME-001/S5
      layers: [api-check]
      tests: ["GET https://localhost:7188/swagger/v1/swagger.json"]
      result: pass
      note: "46 paths / 66 operations, 0 with /v1 (Test env serves the same document as Development)"
    - scenario: T-RENAME-001/S6
      layers: [unit]
      tests: ["Api.Framework.Tests (Release)"]
      result: pass
      note: "run 2: 68/68 (incl. 5 new F-03 TokenIssuerTests and Dev Bot's CORS tests); build 0 errors"
    - scenario: T-RENAME-002/S1
      layers: [ui-e2e, static]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-005/S4", "CORS preflight OPTIONS /Animal"]
      result: pass
      note: "run 2: cross-origin calls from the Test UI :3013 -> :7188 pass; origins from Cors:AllowedOrigins (Test adds localhost:3013, Dev Bot 13:45); preflight from 3013 -> 204 with Allow-Origin, unlisted origin -> no Allow-Origin; SystemUi 2 / UnityUi 0 in Program.cs"
    - scenario: T-RENAME-002/S2
      layers: [api-e2e, unit]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-002/S2", "Api.Framework.Tests/Auth/TokenIssuerTests.cs (5 tests)"]
      result: pass
      note: "iss and aud = system-login (e2e). F-03: unity-login issuer and/or audience fails TokenService.CreateValidationParameters (JwtBearer -> 401), ReadUserId null; 5/5 unit, random key per run"
    - scenario: T-RENAME-002/S3
      layers: []
      tests: []
      result: not-automated
      note: "one-off migration; Dev Bot applied it to api_framework_test (7/25/14 before and after); master reset reseeds renamed HasData OK"
    - scenario: T-RENAME-002/S4
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-002/S4]"]
      result: pass
      note: "16 migration files byte-identical to the 11:20 backup; only the snapshot differs"
    - scenario: T-RENAME-002/S5
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-002/S5]"]
      result: pass
      note: "0 hits; Release build passes"
    - scenario: T-RENAME-002/S6
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-002/S6]"]
      result: pass
      note: "15 hits, all real Unity.API / Unity UI text (D10) or unity_login (D7)"
    - scenario: T-RENAME-003/S1
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-003/S1]"]
      result: pass
      note: "0 file names, 0 identifiers; 23 comment / copy hits naming real Unity products (D10)"
    - scenario: T-RENAME-003/S2
      layers: [ui-e2e]
      tests: ["full e2e suite (next dev compile)", "e2e tsc --noEmit"]
      result: pass
      note: "partial: npm run build (F-07) deferred while Neil's dev UI runs on :3003; gate typecheck nextjs pass"
    - scenario: T-RENAME-003/S3
      layers: [ui-e2e, static]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-005/S4"]
      result: pass
      note: "calls go to the NEXT_PUBLIC_SYSTEM_API_ROOT dev:test sets; 0 NEXT_PUBLIC_UNITY in src/scripts/e2e helpers"
    - scenario: T-RENAME-003/S4
      layers: [ui-e2e, static]
      tests: ["e2e/features/animals/AddEditAnimal.feature::@T-ANIMAL-004/S4"]
      result: pass
      note: "server message shown on the field; keyword 'system' in system-schema-validation.ts:269"
    - scenario: T-RENAME-003/S5
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-003/S5]"]
      result: pass
      note: "package.json / lock name system-ui-next (dependency tree not diffed)"
    - scenario: T-RENAME-003/S6
      layers: [static, ui-e2e]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-003/S6]", "e2e/features/animals/ManageAnimalsGrid.feature::@T-ANIMAL-009/S7"]
      result: pass
      note: "counts equal to the 11:20 backup (same scope): 9 / 39 / 8 / 7 / 2"
    - scenario: T-RENAME-004/S1
      layers: [ui-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-004/S1"]
      result: pass
      note: null
    - scenario: T-RENAME-004/S2
      layers: [ui-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-004/S2"]
      result: pass
      note: "session accepted under system-auth-session; nothing under unity-auth-session"
    - scenario: T-RENAME-004/S3
      layers: [ui-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-004/S3"]
      result: pass
      note: "dark before hydration; system-theme=dark; no unity-theme"
    - scenario: T-RENAME-004/S4
      layers: [ui-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-004/S4"]
      result: pass
      note: "reworded S4 (same tab; Plan Bot 13:10, ticket saved 13:12:09): session under system-auth-session; sign-out fires system-auth-cleared, removes the session, same tab signed out; real refresh fires system-auth-refreshed (extra). Re-run 13:12 pass"
    - scenario: T-RENAME-004/S5
      layers: []
      tests: []
      result: not-automated
      note: "needs a real token about to expire; no hook without a faked token"
    - scenario: T-RENAME-004/S6
      layers: [ui-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-004/S6"]
      result: pass
      note: null
    - scenario: T-RENAME-005/S1
      layers: [api-e2e]
      tests: ["global setup + API steps (getApiUrl with API_URL=http://localhost:5188)"]
      result: pass
      note: "indirect; no helper unit runner"
    - scenario: T-RENAME-005/S2
      layers: []
      tests: []
      result: not-automated
      note: "e2e helpers have no unit runner; code read only (default http://localhost:5188)"
    - scenario: T-RENAME-005/S3
      layers: []
      tests: []
      result: not-automated
      note: "as S2; code read only (guard names API_URL, prints no value)"
    - scenario: T-RENAME-005/S4
      layers: [ui-e2e]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-005/S4"]
      result: pass
      note: "GET /Animal on https://localhost:7188; nothing with /v1/ or :7104"
    - scenario: T-RENAME-005/S5
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-005/S5]"]
      result: pass
      note: "on intent: 2 README sentences contain the text /v1 while saying there is no /v1; flagged"
    - scenario: T-RENAME-006/S1
      layers: []
      tests: []
      result: not-automated
      note: "Dev Bot docs; Review Bot full review (D8)"
    - scenario: T-RENAME-006/S2
      layers: []
      tests: []
      result: not-automated
      note: "Dev Bot docs; Review Bot full review (D8)"
    - scenario: T-RENAME-006/S3
      layers: []
      tests: []
      result: not-automated
      note: "Dev Bot docs; Review Bot full review (D8)"
    - scenario: T-RENAME-006/S4
      layers: []
      tests: []
      result: not-automated
      note: "Dev Bot docs; Review Bot full review (D8)"
    - scenario: T-RENAME-007/S1
      layers: [script]
      tests: ["ai-code-framework/scripts/pre-handoff-checks.selftest.mjs"]
      result: pass
      note: "64 ok"
    - scenario: T-RENAME-007/S2
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-007/S2]"]
      result: pass
      note: "0 hits"
    - scenario: T-RENAME-007/S3
      layers: [script]
      tests: ["pre-handoff-checks.mjs --target all --checks lint,typecheck,eol,secrets,docs-dup (not recorded)"]
      result: pass
      note: "pass 13:07:56; unit via the separate run; code.pre_handoff_gate is Dev Bot's (pass 12:51:05)"
    - scenario: T-RENAME-008/S1
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-008/S1]"]
      result: pass
      note: null
    - scenario: T-RENAME-008/S2
      layers: [ui-e2e]
      tests: ["e2e/features/animals/ManageAnimalsGrid.feature::@T-ANIMAL-003/S12", "e2e/features/animals/ManageAnimalsPage.feature::@T-ANIMAL-008/S2", "e2e/features/animals/DeleteAnimal.feature::@T-ANIMAL-005/S3"]
      result: pass
      note: "observers match GET /Animal (page 2 seen) and the no-list-request check (now line 307) counts 0"
    - scenario: T-RENAME-008/S3
      layers: [static]
      tests: ["%TEMP%/tb-run/rename/static-checks.ps1::[T-RENAME-008/S3]"]
      result: pass
      note: "Unity.API 21/21, Unity.API.Tests 11/11, Unity.UI.Framework 11/11 vs backup"
    - scenario: T-RENAME-009/S1
      layers: []
      tests: []
      result: not-automated
      note: "Plan Bot config / docs; Review Bot full review"
    - scenario: T-RENAME-009/S2
      layers: []
      tests: []
      result: not-automated
      note: "Plan Bot config / docs; Review Bot full review"
    - scenario: T-RENAME-009/S3
      layers: []
      tests: []
      result: not-automated
      note: "Plan Bot config / docs; Review Bot full review"
    - scenario: T-RENAME-009/S4
      layers: []
      tests: []
      result: not-automated
      note: "Plan Bot config / docs; Review Bot full review"
    - scenario: T-RENAME-010/S1
      layers: []
      tests: []
      result: not-automated
      note: "Review Bot checklists"
    - scenario: T-RENAME-010/S2
      layers: []
      tests: []
      result: not-automated
      note: "Review Bot checklists"
    - scenario: T-RENAME-011/S1
      layers: [ui-e2e, read-only-check]
      tests: ["e2e/features/system-rename/SystemRename.feature::@T-RENAME-011/S1", "%TEMP%/tb-run/rename/probe-ui-apiroot.cjs"]
      result: pass
      note: "Test UI :3013 signed in: API calls on the Test API root, no /v1/, none to 7104 (13:46 alone + full run). N1 read-only check passed 13:30: Neil's dev UI :3003 sign-in page only (no sign-in, no writes) has API root https://localhost:7088/ compiled in, no /v1, no fallback, no NEXT_PUBLIC_UNITY_; .env never opened"
    - scenario: T-RENAME-011/S2
      layers: [api-e2e]
      tests: ["e2e/global-setup.ts (resetMaster)"]
      result: pass
      note: "POST {API_URL}/TestData/Reset/master OK in both run-2 e2e runs"
    - scenario: T-RENAME-011/S3
      layers: [script]
      tests: ["pre-handoff-checks.mjs --target all (not recorded)"]
      result: pass
      note: "Dev Bot gate pass 13:43 after the CORS fix (unit 68/68); Test Bot --target all from run 1"
    - scenario: T-RENAME-011/S4
      layers: [ui-e2e]
      tests: ["full e2e suite (setup + 67 manage-animals + 7 system-rename)"]
      result: pass
      note: "setup re-signed all personas on the Test UI (12 .auth files, counted not opened); manage-animals 67/67; full run 80/80"
    - scenario: T-RENAME-011/S5
      layers: [scan]
      tests: ["%TEMP%/tb-run/scan-secrets.ps1"]
      result: pass
      note: "0 hits; e2e/.auth no longer opened (files counted only); reports and handoff hold env var names only"
  blockers: []
  updated_at: 2026-10-09T13:56:00+01:00       # ISO 8601 with offset
  updated_by: test-bot

approvals:                    # required = handoff.require_human_approval at the time of the gate
  plan_to_code:
    required: true
    approved_by: human        # Neil, explicit reply 2026-10-09 11:47 BST (all Q1-Q16 defaults accepted)
    approved_at: 2026-10-09T11:47:00+01:00
  code_to_review:
    required: false
    approved_by: null
    approved_at: null
  merge:
    required: true            # always; agents never merge
    approved_by: human        # Neil's instruction in chat (2026-10-09 14:47 BST) is the merge; no git
    approved_at: 2026-10-09T14:47:00+01:00

blockers: []                  # D3 blocker cleared by plan-bot: Neil confirmed the merges of manage-animals and pre-handoff-checks at 12:37 BST via Dev Bot
---

# Handoff: Rename Unity to System and drop v1

> **Now:** `approved` · owner `human` · pickup `pending` · final verdict Approve with comments (code review + test review round 2, 2026-10-09 14:05 BST; Test Bot run 2 passed, 36 / 0 / 0 / 14) · open: F-01 (Minor, Neil) + Nits
> **Next:** Neil decides the merge (agents never merge), decides F-01, ratifies History rows 12-13 and restarts the Development API. Optional Nits: Test Bot F-07 / F-10 / F-11, Dev Bot F-12 / F-13 / F-15.

## Summary

Rename Unity → System across the active targets (UI.NextJs.Framework, API.Framework, framework docs / rules / skills, test framework docs, config) and drop `v1` from the API.Framework routes and every consumer. No new pages: no UI spec, Excel, journey or stubs are needed. Rollback: `D:\Users\nwood01\Documents\Candc\backups\ai-framework-pre-rename-20261009-1120.zip` (920 entries; no git).

## Artefacts

| Artefact | Path |
|----------|------|
| Plan | `plan.md` |
| Page specs / Excel / journeys / UI ↔ DB stubs | None: no new or changed pages, controls or DB columns (see `plan.md` header) |
| Tickets | `tickets/T-RENAME-001` … `T-RENAME-011` (see `plan.md` §8) |
| Review log | `reviews/review-log.md` (none yet) |
| Review reports | `reviews/DIRECT-system-rename-<n>-review.md` (none yet) |
| Test plan (testing agent) | `tests/test-plan.md` (none yet) |
| Test reports / log (testing agent) | `tests/TEST-system-rename-<n>-report.md` / `tests/test-log.md` (none yet) |

## Notes for the next owner

- Decisions D1–D16 (Neil, 2026-10-09 11:47 BST: all suggested defaults accepted) are in `plan.md` §6. Start condition D3: build starts only after Neil's merges of manage-animals and pre-handoff-checks.
- Source: Dev Bot's scan; Neil approved Dev Bot's defaults. Plan Bot spot-checked the versioning lines, the controller count, `config.ts` and the collisions (`plan.md` §2.2), and found extra items (§2.3: the Tests project's V1 imports, more fixture lines, config 155–156, Review Bot's checklists).
- Each ticket names its owner: dev-bot 001–007, test-bot 008, plan-bot 009, review-bot 010, Neil + dev-bot + test-bot 011.
- Never introduce a plain `System` type or namespace. Keep the existing `system` names (`IsSystemAdmin`, `system-admin`, `@design-system`, `--system-*`, `system-ui`).
- Agents never open `.env*` or `e2e/.auth`. Neil does N1 / N2 himself. Report env var names only, never values.
- Dev Bot hand-off (2026-10-09): N1 / N2 are still Neil's. Until he renames `NEXT_PUBLIC_UNITY_API_ROOT` / `_APP_ID` to `NEXT_PUBLIC_SYSTEM_API_ROOT` / `_APP_ID` in `.env.local` (and drops `/v1/` from the root), a plain `npm run dev` falls back to `https://localhost:7104/v2/` (D14). `npm run dev:test` is not affected (it sets `NEXT_PUBLIC_SYSTEM_API_ROOT` itself). Neil's dev API (5088/7088) and his `dev:test` UI (3003) were left running and need a restart; his dev DB `unity_login` gets the new migration at the next dev API start (`MigrateDatabase`).
- N3 done: user env var `API_URL` no longer ends with `/v1`; `E2E_UI_API_ROOT` is not set at user level (name-only check). Test Bot: restart the shell / IDE so the new `API_URL` is picked up; `e2e/helpers/config.ts` now fails fast if `API_URL` still ends with `/v1`.
- Test API smoke used Release output on spare ports 7189 / 5189; HTTP 5189 redirects to HTTPS (307), so authenticated smoke calls used HTTPS. The master reset was run once on `api_framework_test` (reseeded with the System names).

## History

Append one row per transition or pickup. Newest last. Never edit earlier rows. The owner writes History; the testing agent does not (its runs are in `tests/test-log.md`, and the reviewing agent records each test review here).

| # | When | Stage | Owner | Route / gate | By | Note |
|---|------|-------|-------|--------------|----|------|
| 1 | 2026-10-09T11:26:20+01:00 | — → planned | — → plan-bot | — (draft, not approved) | plan-bot | Draft plan + tickets T-RENAME-001..011 from Dev Bot's scan (Neil approved its defaults). No UI spec / Excel / journey (no new pages). Q1–Q16 open with suggested defaults; plan_to_code not approved |
| 2 | 2026-10-09T12:34:13+01:00 | planned | plan-bot → dev-bot | plan_to_code · direct (approved by Neil 2026-10-09 11:47) | plan-bot | Neil accepted all Q1–Q16 defaults (D1–D16 in plan.md §6) and approved the hand-off. Start condition D3: Dev Bot starts only after Neil records the merges of manage-animals AND pre-handoff-checks; T-RENAME-009 (plan-bot) waits too. No message sent |
| 3 | 2026-10-09T12:36:54+01:00 | planned | dev-bot | pickup · accepted (waiting on D3) | dev-bot | Dev Bot accepted pickup; waiting on Neil's merges of manage-animals and pre-handoff-checks (D3) before any rename build |
| 4 | 2026-10-09T12:38:49+01:00 | planned (unchanged) | dev-bot (unchanged) | D3 start condition met; T-RENAME-009 done (no gate) | plan-bot | D3 blocker cleared: Neil told Dev Bot at 12:37 BST to treat manage-animals and pre-handoff-checks as merged (no git); both recorded as merged. waiting_on set to the build in progress. T-RENAME-009 applied to ai-framework.config.yaml (Next.js description: System UI / system-ui-next / NEXT_PUBLIC_SYSTEM_API_ROOT, Unity.API v2 fallback noted per D14; /v1 dropped from api_base_url, master_route, batch_route); planning framework unchanged (D11). Front matter stage/owner untouched |
| 5 | 2026-10-09T12:39:39+01:00 | planned → in-development | dev-bot | start condition D3 met | dev-bot | Neil told Dev Bot directly in chat at 12:37 BST to treat manage-animals and pre-handoff-checks as merged and start the rename (none of the framework code is in git, by design, so there is no merge to record in their handoff.md). Build of T-RENAME-001..007 started in D4 order |
| 6 | 2026-10-09T12:51:40+01:00 | in-development | dev-bot | pre-handoff gate · pass (2026-10-09T12:51:05+01:00) | dev-bot | T-RENAME-001..007 built in D4 order: 14 controllers flattened out of Controllers/V1, versioning packages and AddApiVersioning removed, Swagger doc v1 kept (D6); SystemUi CORS, system-login issuer/audience, migration 20261009114033_RenameUnityToSystem (UpdateData by id) applied to api_framework_test; UI identifiers, 8 system-* files, package system-ui-next, NEXT_PUBLIC_SYSTEM_* names, visible text, storage keys / events renamed; e2e getApiUrl without /v1 (stale-/v1 guard); docs (.cursor + .claude identical), gate selftest + fixtures. Build, 57 API tests, UI typecheck / lint / 10 vitest, e2e tsc + bddgen, selftest 64 ok, API + UI smoke pass. T-RENAME-011 N3: user env var API_URL no longer ends with /v1 (E2E_UI_API_ROOT not set). No .env* file opened |
| 7 | 2026-10-09T12:51:40+01:00 | in-development → in-review | dev-bot → review-bot | code_to_review · direct; code_to_test · direct (D5) | dev-bot | Hand-off with manifest (api 44, ui 51, tests 11, migrations 3) and gate pass. Review Bot: full review (D8) + T-RENAME-010; Test Bot alongside: T-RENAME-008, .auth regeneration, e2e run. Neil: N1 / N2 (.env.local / .env.example) and dev-server restarts still to do. Messages to Review Bot / Test Bot relayed by the main agent |
| 8 | 2026-10-09T13:09:00+01:00 | in-review | review-bot | pickup + review_feedback · direct (option B, D5) | review-bot | Code review round 1 (D8, direct_scope: plan, 109 manifest entries vs the 11:20 backup zip): **Approve with comments**, provisional, awaiting Test Bot's run 1 and the test review (`testing:` untouched; test_verdict / verdict null). Migration 20261009114033_RenameUnityToSystem: 5 UpdateData by id covering all 7 old seeded values, Down() exact, 16 older migration files byte-identical, snapshot = Designer; Test reset reseeds System names. 14 controllers: routes unchanged apart from the version prefix, auth attributes unchanged; Swagger 46 paths / 66 operations, 0 /v1. Gate pass on a copy (13:03:48) and in place, check-only (13:05:13; UI 231 files = Test Bot's 2 new e2e files); self-test 64/64; API 57/57, UI 10/10. Anonymous smoke on the Test API: /v1 404, plain routes 200/401, CORS SystemUi OK; UI 3003 shows System texts. Findings: F-01 Angular example UI environment.ts still /v1 (Minor, Neil), F-02 DB rollback order undocumented (Minor), F-03 no issuer unit test (Minor), F-04..F-06 Nit. T-RENAME-010 not done (framework docs; awaiting Neil; also needs ui-nextjs-checklist.md:10). Development API (10:58) still old build. No sign-in, no token minting, no reset POST, no secret printed; nothing merged |
| 9 | 2026-10-09T13:11:26+01:00 | in-review (unchanged) | review-bot (unchanged) | ticket doc fix (no gate) | plan-bot | T-RENAME-004/S4 reworded to the same-tab case (heading 'Auth events still work in the same tab'; sign-out fires system-auth-cleared and removes system-auth-session; refresh fires system-auth-refreshed). Out of scope: cross-tab sign-out (the app never had it; the rename changes no behaviour), answering Test Bot's question in TEST-system-rename-1-report.md. Doc-only; front matter untouched |
| 10 | 2026-10-09T13:12:09+01:00 | in-review (unchanged) | review-bot (unchanged) | ticket doc fix (no gate) | plan-bot | Neil 2026-10-09: T-RENAME-004/S4 now sign-out in the same tab only (refresh 'And' removed; refresh is S5, not automatable). T-RENAME-005/S5 Then clarified: no configured API root, route, default or code path contains /v1; prose explaining /v1 was removed and the S3 stale-value guard are allowed (answers Test Bot's run-1 flag). Doc-only; front matter untouched |
| 11 | 2026-10-09T13:17:00+01:00 | in-review → approved | review-bot → human | test_review + final verdict · direct (option B, D5) | review-bot | **Tests blocked: T-RENAME-011/S1** (Neil's N1, .env.local). Test review of run 1 + 13:15 addendum: **blocked-noted**; final verdict **Approve with comments** (code + test review; blocked_tests_allow_approval). 35 Pass / 0 Fail / 1 Waiting / 14 Not automated, all 14 justified (002/S3, 005/S2-S3, 006/S1-S4, 009/S1-S4, 010/S1-S2 review-verified under D8; 004/S5 not automatable per row 10, Then observed by the extended S4). 004/S4 same-tab ruling (rows 9-10) checked: full Pass. 005/S5: Plan Bot's clarified Then (row 10) recorded, pass stands. Tags, reset-first, no mocks, real assertions OK; F-51 and F-56 resolved. Review Bot secret re-scan: 197 files + 3 embedded-zip entries, 0 hits. T-RENAME-010 done 13:10 by review-bot on Neil's go-ahead (13:09), 3 checklist lines, backup in Candc\ai-framework-edit-backup-20261009-1310. Findings 0 Blocker / 0 Major / 3 Minor (F-01..F-03) / 6 Nit (F-04..F-09); nothing routed. Agents never merge |
| 12 | 2026-10-09T13:47:00+01:00 | approved (unchanged) | human (unchanged) | post-approval Dev follow-up (no gate, no owner change) | dev-bot | Test Bot was blocked on T-RENAME-011/S1: the Test API CORS policy hard-coded 4200 / 3003 and Test Bot's Test UI is now on 3013 (Neil's dev UI has 3003). SystemUi origins now come from Cors:AllowedOrigins (Api.Framework/Cors/SystemUiCors.cs; appsettings.json keeps the 4 previous origins, appsettings.Test.json adds http(s)://localhost:3013) + SystemUiCorsTests (6). Test API pid 15796 stopped, Release rebuilt, restarted the same way (launch profile Test, env from the registry) as pid 32536; preflight from http://localhost:3013 to /Authorisation/SignIn -> 204 with Access-Control-Allow-Origin. F-03: already covered by TokenIssuerTests (unity-login issuer -> SecurityTokenInvalidIssuerException; audience; system-login valid), no duplicate added. F-04: blank API_URL fails fast naming API_URL; e2e/helpers/config.test.ts (blank + stale-/v1). F-05: E2E_UI_API_ROOT stale-/v1 / blank guard in dev-test.mjs via scripts/api-root.mjs + test. F-06: rollback zip path corrected to D:\Users\nwood01\Documents\Candc\backups\ai-framework-pre-rename-20261009-1120.zip in code.verification and the Summary (row 7 itself left as written: History rows are never edited, rule 2). Docs: api-framework-ui-contract CORS section (.cursor + .claude identical), e2e/README.md. Kept: layout.tsx meta "Unity-style design system" (D10). Not done: F-01 (Neil), F-02 (Plan Bot). Build pass, API 68/68, UI vitest 26/26, gate --record pass (2026-10-09T13:43:28+01:00). Neil's dev API (7088) and UI (3003) untouched; no .env* opened; testing: untouched |
| 13 | 2026-10-09T13:56:19+01:00 | approved (unchanged) | human (unchanged) | plan doc fix (no gate) | plan-bot | Review F-02 (Neil 2026-10-09 13:53 BST): plan.md §9 now gives the DB rollback order. Step 1: on the NEW code, run `dotnet ef database update 20261008150221_AddAnimals --project Api.Framework.Data --startup-project Api.Framework` from API.Framework (Down of RenameUnityToSystem). Step 2: THEN restore backups\ai-framework-pre-rename-20261009-1120.zip. Restoring the zip first leaves System-named seed rows, and sign-in returns 400 (TenantService.cs:335). Doc only; front matter unchanged |
| 14 | 2026-10-09T14:05:00+01:00 | approved (unchanged) | human (unchanged) | test_review round 2 + code delta · direct (option B, D5) | review-bot | Test review of run 2 (TEST-system-rename-2-report.md, 13:56): **approve**; final verdict **Approve with comments**; "Tests blocked" cleared. 36 Pass / 0 Fail / 0 Waiting / 14 Not automated; unit 68/68, e2e 80/80 on the Test UI :3013 vs 7188 / api_framework_test. 011/S1 Then asserted (calls on the Test root, none /v1 or 7104); the N1 probe of :3003 is HTTP-only, no .env opened. F-03 TokenIssuerTests (5) real; F-08 done; F-07 deferred. Code delta after 13:16: SystemUi CORS from Cors:AllowedOrigins (explicit origins, no wildcard, no credentials, 3013 Test only, fail-fast when empty) + 6 tests; anonymous preflight on 7188: 3003 / 3013 / 4200 allowed, evil / 3014 / null get no CORS headers. F-02 (plan §9, row 13), F-04, F-05, F-06 resolved. Gate on a copy pass (68/68, UI 26), self-test 64/64; in place check-only: all pass except API unit (bin\Release locked by the running Test API; environment, F-15). Secret re-scan 208 files, 0 hits. New Nits F-10..F-15 (F-14: post-approval handoff edits in rows 12-13 for Neil to ratify). Open: Minor 1 (F-01), Nit 7. Development API not listening since about 13:59 (not stopped by review-bot). review.cycle stays 1; testing: untouched; nothing routed; agents never merge |
| 15 | 2026-10-09T15:58:22+01:00 | approved → merged | human (unchanged) | merge (human) | plan-bot | merged — recorded by plan-bot on Neil's word 2026-10-09 14:47 BST (no git; Neil's instruction is the merge). approvals.merge human 14:47. waiting_on keeps Neil's open to-dos: secret rotations (D1; optional E2E_TESTDATA_ADMIN_PASSWORD), F-01 Angular example UI /v1 decision, F-56 .next-test-tb deletion vs D16, F-14 ratifying History rows 12-13 (incl. plan-bot row 13). testing section untouched |
