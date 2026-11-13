# Plan: Rename Unity to System and drop v1 from API.Framework routes

| Field | Value |
|-------|-------|
| Feature | system-rename |
| Type | Cross-cutting rename (code, routes, runtime keys, framework docs, config) |
| Status | **Approved** for hand-off to Dev Bot (Neil, 2026-10-09 11:47 BST; all Q1–Q16 answered with the suggested defaults, decisions D1–D16 in §6). **Build starts only after the start condition in §8** |
| Requested | 2026-10-09, Neil (source: Dev Bot's scan; Neil approved Dev Bot's defaults) |
| Planned by | plan-bot, 2026-10-09 |
| UI spec / Excel / journeys | **None.** No new pages, controls or DB columns: existing names, routes and text change only. `specs/`, `excel/`, `journeys/` and `stubs/` are intentionally not created |
| Backup / rollback | `D:\Users\nwood01\Documents\candc\backups\ai-framework-pre-rename-20261009-1120.zip`. Plan Bot checked it: 920 entries, all under `ai-framework/`, 1,569,367 bytes, written 2026-10-09 11:20:15 BST. Neither target is a git repo, so this zip is the only rollback |

## 1. Summary

Across the **active** targets only (UI.NextJs.Framework, API.Framework, the framework docs / rules / skills, the test framework docs and `ai-framework.config.yaml`):

1. Rename the product name **Unity → System** in code identifiers, file names, the package name, env var names, visible text, runtime storage keys / events, the CORS policy, the JWT issuer / audience and the seeded feature / permission names (through a **new** EF migration).
2. Drop **`v1`** from the API.Framework endpoints (remove URL-segment versioning) and update every consumer.

References to the real **Unity.API**, **Unity.UI.Framework** and **UI.Angular** repos stay as they are, and so do historical work artefacts (plans, reviews, test reports), old migrations and the `unity_login` database name.

## 2. Evidence (Dev Bot's scan, spot-checked by Plan Bot 2026-10-09, read-only)

### 2.1 Scale (Dev Bot)

UI about 387 lines in 78 files; API 116 lines in 35 files; framework docs about 62 files. Plan Bot's own count uses a different file-type filter and gives the same order of size (below). It is not a replacement for Dev Bot's inventory.

| Target | Plan Bot count (case-insensitive `unity`) | Note |
|--------|-------------------------------------------|------|
| API.Framework (`.cs/.json/.http/.csproj/.md/.mdc/...`, no bin/obj) | 93 lines / 31 files | 58 lines / 10 files are in `Migrations/` (old migrations, Designer files and the model snapshot: **not hand-edited**) |
| UI.NextJs.Framework (source, docs, rules; no node_modules / `.next*`) | 478 lines / 69 files | The `.next-test` / `.next-test-tb` build output also contains the old strings. It is regenerated, never edited |

### 2.2 Spot-checks of Dev Bot's claims

| Claim | Result |
|-------|--------|
| `Program.cs:39-50`: `AddApiVersioning` with URL-segment + header readers, `SubstituteApiVersionInUrl` | **Confirmed.** Lines 39–51: `DefaultApiVersion = new ApiVersion(1, 0)`, `ReportApiVersions = true`, `ApiVersionReader.Combine(new UrlSegmentApiVersionReader(), new HeaderApiVersionReader("x-api-version"))`, `.AddMvc().AddApiExplorer(GroupNameFormat = "'v'VVV", SubstituteApiVersionInUrl = true)`. Also `using Asp.Versioning;` (line 1) and `using Api.Framework.Controllers.V1.TestData;` (line 12). Swagger: `SwaggerDoc("v1", …Version = "v1")` (lines 70–73), `SwaggerEndpoint("/swagger/v1/swagger.json", "v1")` (line 139). Packages `Asp.Versioning.Mvc` and `Asp.Versioning.Mvc.ApiExplorer` 10.2.1 in `Api.Framework.csproj` |
| 14 controllers use `[ApiVersion("1")]` and `[Route("v{version:apiVersion}/...")]` under `Controllers\V1` | **Confirmed.** 14 files, 1 controller class each, one `[ApiVersion(` and one `v{version:apiVersion}` each; every controller file is under `Controllers\V1\{Animals, Auth, Directory (2), Examples (3), ReferenceData, Schemas (5), TestData}`; 7 namespaces `Api.Framework.Controllers.V1.*`. **Missed by the scan:** `Api.Framework.Tests/Animals/AnimalPoliciesTests.cs:4-5` imports `Controllers.V1.Animals` / `.Schemas` (and a `GET v1/schemas/create-animal` comment at line 77) |
| `e2e/helpers/config.ts:7-16` appends `/v1` to `API_URL` | **Confirmed.** `getApiUrl()` returns `API_URL` trimmed, appending `/v1` unless it already ends with `/v1`; default `http://localhost:5188/v1`. This is a logic change, not a text replace |
| Collisions with existing "system" names | **Confirmed, all present today:** `IsSystemAdmin` 40 lines / 25 files; `system-admin` 2 / 2; `system@candc-uk.com` 1 / 1; `--system-red` 17 / 7; `--system-green` 15 / 7; `@design-system` 47 / 36; `system-ui` 7 / 4. The **new** names are free today: `SystemUi`, `system-login`, `system-auth*`, `system-theme`, `NEXT_PUBLIC_SYSTEM_*` all 0 hits. No C# type or namespace named plain `System` exists (49 C# files use `System.*` / `TimeProvider.System`, migrations included; Dev Bot says 45 without them) |
| Seeded names: check UI usages | **None in the UI.** `UnityBasicFeatures`, `unity_messenger_dashboard` and `Unity messenger` have 0 hits in `src/` and `e2e/`. They live in `Api.Framework.Data/LoginFeatures.cs` (lines 7, 11, 17) and `LoginPermissions.cs` (`unity_messenger_dashboard` line 14; group `Unity messenger` on lines 14, 15, 23 and possibly more rows). Old migrations and the snapshot hold the seeded values |
| `environment.ts:6` falls back to Unity.API v2 | **Confirmed:** `process.env.NEXT_PUBLIC_UNITY_API_ROOT ?? 'https://localhost:7104/v2/'`; line 4 `NEXT_PUBLIC_UNITY_APP_ID ?? '<app id GUID>'` |
| Ajv keyword `'unity'` | Confirmed at `validation/unity-schema-validation.ts:269` (`keyword: 'unity'` on the error objects the UI builds). No API schema emits a `unity` keyword |

### 2.3 Extra findings (not in the scan)

- `Api.Framework.Tests`: the V1 namespace imports above. Also `TestDataGuardAndServiceTests.cs:89` uses `"unity_login"` (the DB name, which stays).
- Gate fixtures: `unity-login` issuer / audience in `scripts/fixtures/pre-handoff/api-bad/appsettings.json`, `api-bad/appsettings.Commented.json`, `api-good/appsettings.json`, and `https://localhost:7188/v1/` in `api-good/appsettings.Development.json`. `pre-handoff-checks.selftest.mjs` lines 52 and 58 (issuer), not only line 62.
- `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc:13` describes the `Controllers/V1/{Area}` layout. This is a framework-level rule with only a `.cursor` copy (no `.claude` folder at that level).
- UI.NextJs.Framework has **no `.claude` folder**, only `.cursor`. The "both copies" rule applies to API.Framework (`.cursor` + `.claude`).
- `ai-framework.config.yaml:155-156` (nextjs `description`: "Unity.UI.Next … Calls Unity.API v2 via NEXT_PUBLIC_UNITY_API_ROOT") describes the active UI and needs updating, in addition to 436 / 439 / 441.
- `scripts/dev-test.mjs:47` sets `NEXT_PUBLIC_UNITY_API_ROOT` for the Test UI, as well as the `/v1/` default at lines 3 and 27. Both change together.
- Review Bot's framework has two active-target mentions: `checklists/api-checklist.md:78` (`Controllers/V1/{Area}` layout) and `checklists/ui-nextjs-checklist.md:9` (`NEXT_PUBLIC_UNITY_API_ROOT`). The other hits there refer to Unity.API / Unity.UI.Framework / Angular (keep). See D9.
- Code comments that name the **real** Unity UI as the origin of a ported pattern: `CompanyLoader.module.css:1` ("Port of Unity UI company-loader (UI.Angular.Framework …)"), `CompanyLoader.tsx:12`, `ModalShell.tsx:14/92`, `ModalShell.module.css:85`. Also visible showcase text in `DesignSystemShowcase.tsx:54/116/172` ("Unity-style primitives", "mirroring Unity form-modal", "default for Unity form modals"). See D10.
- Planning framework: see §5.6 and D11.

## 3. Actors and ownership

| Actor | Role here |
|-------|-----------|
| Neil (human owner) | Answered §7 and approved `plan_to_code` (2026-10-09 11:47 BST); does the `.env.local` / `.env.example` step (T-RENAME-011), merges. Merges manage-animals and pre-handoff-checks first (D3) |
| Dev Bot | API.Framework, UI.NextJs.Framework (code, e2e helpers / scaffolding, `dev-test.mjs`, `.http`), API / UI / ai-code-framework rules, skills and READMEs, gate selftest and fixtures, the user env var `API_URL` (T-RENAME-001..007, part of 011) |
| Test Bot | `ai-test-framework` docs and the e2e **scenario steps** it owns (`animals.steps.ts`, `auth.steps.ts`), `.auth` regeneration and the e2e run (T-RENAME-008, part of 011) |
| Plan Bot | `ai-planning-framework` files and `ai-framework.config.yaml` (precedent: T-GATE-006 and the `testing:` config changes) (T-RENAME-009; see D12) |
| Review Bot | Its two checklist lines (T-RENAME-010, cross-framework ticket; D9) and the review |

## 4. Scope

**In scope:** API.Framework, UI.NextJs.Framework (`src/`, `e2e/`, `scripts/`, README / AGENTS, `.cursor`), `ai-code-framework/.cursor`, `loops/`, `AGENT-BRIEF.md`, `ai-code-framework/scripts` (selftest + fixtures), `ai-test-framework` docs, `ai-framework.config.yaml`, and plan-bot / review-bot docs only where they describe the active targets.

**Keep as-is:** anything about the real Unity.API / Unity.UI.Framework / UI.Angular repos (config entries, `feature-build.md`, checklists, the add-edit-contact example); historical plans, reviews and test reports under `work/`; old EF migrations, their Designer files (the model snapshot changes only through `dotnet ef migrations add`); the `unity_login` database name (D7); `node_modules`, `.next*` and other build output.

**Rules for every ticket:**

- Never introduce a C# type or namespace named plain `System`. Search case-sensitively and by whole word, and never blind-replace `System`. Leave `IsSystemAdmin`, `system-admin`, `system@candc-uk.com`, `--system-red/green`, `@design-system` and `system-ui` untouched.
- Line endings: API CRLF, UI LF (pre-handoff decision D5). Renamed files keep their content's endings and are UTF-8 without BOM.
- Every rule / skill edit in API.Framework is made in both `.cursor` and `.claude`.
- Never open `.env*` files or `e2e/.auth`. Neil edits `.env.local` / `.env.example` himself.

## 5. Design

### 5.1 API v1 removal (T-RENAME-001)

Remove URL-segment versioning: delete `[ApiVersion("1")]`, change `[Route("v{version:apiVersion}/<x>")]` to `[Route("<x>")]`, and remove the `AddApiVersioning` block. D1: flatten `Controllers\V1\*` to `Controllers\*` with namespaces `Api.Framework.Controllers.*`, updating `Program.cs:12` and `AnimalPoliciesTests.cs:4-5`. D2: remove both Asp.Versioning packages and the `x-api-version` header reader. D6: Swagger keeps the `"v1"` OpenAPI doc name (a document version, not a URL segment); every endpoint must still appear in it.

### 5.2 API Unity → System (T-RENAME-002)

- CORS policy `UnityUi` → `SystemUi` (`Program.cs:116`, `:142`).
- JWT issuer / audience `unity-login` → `system-login` in `appsettings.json`, `appsettings.Test.json` and the `JwtOptions` defaults. This invalidates existing tokens (accepted locally).
- Seeded names, through a **new** EF migration only: `UnityBasicFeatures` → `SystemBasicFeatures`, `Unity messenger` → `System messenger` (feature name / description and every permission group using it), `unity_messenger_dashboard` → `system_messenger_dashboard`. Update `LoginFeatures` / `LoginPermissions`, then `dotnet ef migrations add` (UpdateData by the existing ids). Never edit old migrations or Designer files.
- Comments / docs inside API.Framework that describe the active target ("Reference .NET 10 API for Unity JSON schema forms", "Permission names the Unity UI checks") → System. Comments naming the real Unity.API stay (D10).

### 5.3 UI code renames (T-RENAME-003)

`unityApiFetch`, `readUnityApiJson`, `isUnityApiSuccess`, `UnityApiFetchInit`, `UnityJsonSchema*`, `UnitySchema*`, `unityCookieService` and the `Unity*` renderers (including `registerUnityJsonFormRenderers` if present) → `System*` / `system*`. The 8 `unity-*` files → `system-*`, with all imports and the `json-schema-form/index.ts` barrel updated. Env var names in code: `NEXT_PUBLIC_UNITY_API_ROOT` / `_APP_ID` → `NEXT_PUBLIC_SYSTEM_*` (`environment.ts`, `dev-test.mjs:47`). Package `unity-ui-next` → `system-ui-next` (`package.json`, and the two `name` fields in `package-lock.json` only). Error-object keyword `'unity'` → `'system'`, plus anything that matches on it.

### 5.4 UI visible text and runtime keys (T-RENAME-004)

- Text: `Unity Login` (SignInForm H2), `Sign in with your Unity credentials.`, title `Unity UI Next`, `Unity API returned …` errors → System.
- Keys: `unity-auth-session` (`auth-cookies.ts`, `e2e/helpers/authentication.ts`), `unity-theme` (`ThemeProvider.tsx`, the inline script in `layout.tsx`), events `unity-auth-cleared` / `unity-auth-refreshed` → `system-*`.
- Users get a one-time logout and theme reset (accepted locally). No migration code for old keys.

### 5.5 v1 consumers (T-RENAME-005, 007, 008, 009)

| Consumer | Change | Ticket |
|----------|--------|--------|
| `e2e/helpers/config.ts:7-16` | stop appending `/v1`; default `http://localhost:5188`; doc comment | 005 (dev-bot, scaffolding) |
| `scripts/dev-test.mjs:3, 27` | default `https://localhost:7188/` | 005 |
| `Api.Framework/Api.Framework.http` (lines 4, 14, 23, 26) | drop `/v1` | 005 |
| UI `README.md`, `e2e/README.md` | drop `/v1`, rename env vars | 005 |
| `e2e/features/animals/animals.steps.ts:42, 44, 275` regexes | drop `\/v1` | 008 (test-bot, scenario code) |
| API rules (`.cursor` + `.claude`), `api-framework-ui-contract` skill, AGENTS.md, ai-code-framework `.cursor/rules/api-json-schema-forms.mdc` | drop v1 / `Controllers/V1` | 006 |
| `ai-framework.config.yaml:436, 439, 441` (+155–156 description) | drop `v1`, describe System | 009 (plan-bot, D12) |
| `ai-test-framework/README.md`, `skills/add-test-data-reset/SKILL.md` | drop `v1/` from routes | 008 |
| gate fixtures, `pre-handoff-checks.selftest.mjs` (52, 58, 62) | `system-login`, no `/v1/` | 007 |

### 5.6 Planning framework (T-RENAME-009, plan-bot, not applied yet)

The `Unity`/`v1` mentions in Plan Bot's own files (skills, templates, README, AGENT-BRIEF, schema, sample YAMLs, generators):

| File | Line | Text | Refers to |
|------|------|------|-----------|
| `schemas/page-spec.schema.json` | 45–47 | property `unity_feature`, "Optional Unity feature label (Paginated Grid / Modal)." | The **"Unity Feature"** column of Neil's source spreadsheets (e.g. `examples/source-attachments/Manage-Contacts.xlsx` cell D2), i.e. the real Unity product's feature catalogue, not the active targets |
| `generators/excel_spec.py` | 332–333 | header label `"Unity Feature"`, reads `spec.get("unity_feature")` | same |
| `templates/yaml/manage-list-contacts.yaml` | 9 | `unity_feature: ""` | same |
| `templates/yaml/paginated-grid-sample.yaml` | 10 | `unity_feature: ""` | same |

No hits in `skills/`, `README.md`, `AGENT-BRIEF.md`, `loops/`, `generators/README.md`, `examples/README.md`, `out/*.md` or `templates/tickets|journeys|stubs`. `out/*.xlsx` and `examples/source-attachments/*.xlsx` are generated output or Neil's source documents (not edited). `work/*/specs/*.yaml` (add-edit-contact, manage-animals) also carry `unity_feature: ""`; they are historical. The shared handoff template's `Unity.API/Controllers/V2/...` examples refer to the real Unity.API (keep).

D11: keep these files (the field mirrors the real Unity spreadsheet column), so T-RENAME-009 changes only the config lines.

## 6. Decisions

Neil approved Dev Bot's scan defaults (2026-10-09): Unity → System across the active targets as listed in §5; drop v1; the keep-as-is list in §4; a one-time logout / theme reset is acceptable locally; seeded names change only through a new EF migration; never a plain `System` type or namespace.

Neil, 2026-10-09 11:47 BST: every suggested default in §7 accepted, and the plan approved for hand-off to Dev Bot (starting only after the merges, D3).

1. D1 (Q1) Flatten `Controllers\V1` to `Controllers\{Area}`, namespaces `Api.Framework.Controllers.{Area}` (incl. `Program.cs:12`, `AnimalPoliciesTests.cs:4-5`).
2. D2 (Q2) Remove the ApiVersioning packages entirely (`Asp.Versioning.Mvc`, `.ApiExplorer`), the `AddApiVersioning` block and the `x-api-version` reader.
3. D3 (Q3) Land after Neil's merges: **build begins only after Neil records the merges of manage-animals AND pre-handoff-checks** (stage `merged` in their `handoff.md`, or Neil tells Dev Bot directly).
4. D4 (Q4) One hand-off; tickets built in order API (001, 002) → UI (003–005) → gate / docs (006, 007), then 008 / 009 / 010; one review.
5. D5 (Q5) A Test Bot e2e run is required before approval (`code_to_test` alongside the review).
6. D6 (Q6) Keep the Swagger doc name / version `"v1"` and `/swagger/v1/swagger.json`.
7. D7 (Q7) Keep the `unity_login` database name.
8. D8 (Q8) Review Bot does a full review (`direct_scope: plan`) of every manifest file plus the gate result.
9. D9 (Q9) Review Bot updates its two checklist lines itself (T-RENAME-010).
10. D10 (Q10) Keep comments / showcase text that name the real Unity product or repo; rename only text describing the active target.
11. D11 (Q11) Keep the planning framework's `unity_feature` / "Unity Feature" (no planning framework file changes).
12. D12 (Q12) Plan Bot edits `ai-framework.config.yaml` (T-RENAME-009).
13. D13 (Q13) Dev Bot checks whether the user env var `E2E_UI_API_ROOT` is set (name only, never the value) and drops `/v1/` with `API_URL` in N3; Neil allows Dev Bot to change these user-level env vars.
14. D14 (Q14) Keep the `environment.ts` fallback value (`https://localhost:7104/v2/`); rename the variables only.
15. D15 (Q15) New names as Dev Bot listed: `System*` / `system*`, `system-*` files, `NEXT_PUBLIC_SYSTEM_API_ROOT` / `_APP_ID`, `system-ui-next`, `SystemUi`, `system-login`, `system-auth-session`, `system-theme`, `system-auth-cleared` / `-refreshed`, `SystemBasicFeatures`, `system_messenger_dashboard`, `System messenger`.
16. D16 (Q16) Leave the old `.next-test` / `.next-test-tb` output for the next build to overwrite; no manual deletion.

## 7. Open questions — all answered (Neil, 2026-10-09 11:47 BST: suggested defaults accepted; decisions D1–D16 in §6)

1. (→ D1) **Q1 Flatten `Controllers\V1`?** Default **yes**: `Controllers\{Area}` and namespaces `Api.Framework.Controllers.{Area}` (Dev Bot leans flatten). Includes `Program.cs:12` and `AnimalPoliciesTests.cs:4-5`.
2. (→ D2) **Q2 Remove the ApiVersioning packages entirely, or keep them header-only?** Default **remove** `Asp.Versioning.Mvc` + `Asp.Versioning.Mvc.ApiExplorer`, the `AddApiVersioning` block and the `x-api-version` reader; no `api-supported-versions` header afterwards.
3. (→ D3) **Q3 Land after Neil merges manage-animals and pre-handoff-checks?** Default **yes, wait**. Both are `approved` and waiting on Neil's merge. The rename touches the same files (AnimalController, `animals.steps.ts`, e2e helpers, `appsettings*.json`, gate selftest / fixtures), so building in parallel risks conflicting or lost edits (no git). If Neil wants it sooner: start only after both are merged or explicitly frozen.
4. (→ D4) **Q4 One hand-off or staged?** Default **one hand-off**, tickets built in order API (001, 002) → UI (003, 004, 005) → gate / docs (006, 007), then 008 / 009 / 010, one review.
5. (→ D5) **Q5 Test Bot e2e run required before approval?** Default **yes**. Routes, storage keys, the JWT issuer and `.auth` all change; `code_to_test` runs alongside the review.
6. (→ D6) **Q6 Swagger doc name?** Default **keep** the OpenAPI doc name / version `"v1"` and `/swagger/v1/swagger.json` (document version, not a route). Alternative: rename it to the Swashbuckle default.
7. (→ D7) **Q7 Rename the `unity_login` database?** Default **keep** (per Dev Bot). Also keep `unity_login` in `TestDataGuardAndServiceTests.cs:89` and the e2e README.
8. (→ D8) **Q8 Review Bot scope?** Default **full review** (`direct_scope: plan`) of every file in the manifest, plus the gate result. A rename-only diff review is not enough because of the logic changes (config.ts, versioning removal, migration).
9. (→ D9) **Q9 Review Bot's two checklist lines** (`api-checklist.md:78`, `ui-nextjs-checklist.md:9`)? Default **yes**: a cross-framework ticket T-RENAME-010 for Review Bot to update its own files. Plan Bot does not edit them.
10. (→ D10) **Q10 Comments and showcase text that name the real Unity UI as a pattern's origin** (CompanyLoader, ModalShell, "same idea as Unity", "Copy Unity.API BFF patterns", DesignSystemShowcase lines 54 / 116 / 172)? Default **keep** where the text names the real Unity product or repo (it is a reference to the source, per the keep-as-is rule). Rename only text that describes the active target itself. Alternative: reword the visible showcase text to drop "Unity".
11. (→ D11) **Q11 Planning framework `unity_feature` / "Unity Feature"?** Default **keep**: it mirrors the "Unity Feature" column in Neil's source spreadsheets. Renaming would change the schema key used by existing specs.
12. (→ D12) **Q12 Who edits `ai-framework.config.yaml`?** Default **Plan Bot** (T-RENAME-009), as with T-GATE-006 and the `testing:` changes. Alternative: Dev Bot within T-RENAME-006.
13. (→ D13) **Q13 `E2E_UI_API_ROOT` user env var:** if it is set at user level with `/v1/`, it must drop `/v1/` at the same time as `dev-test.mjs`. Default: Dev Bot checks whether the **name** is set (never prints the value) and updates it with `API_URL` in T-RENAME-011 step N3. Neil confirms Dev Bot may change user-level env vars.
14. (→ D14) **Q14 `environment.ts` fallback `https://localhost:7104/v2/` (Unity.API v2)?** Default **keep** the fallback value (renaming the variables only). Changing the default target is out of scope. Neil's same-moment `.env.local` edit (N1) is what prevents the fallback being used.
15. (→ D15) **Q15 Names of the new identifiers:** default as Dev Bot listed: `System*` / `system*`, `system-*` files, `NEXT_PUBLIC_SYSTEM_API_ROOT` / `NEXT_PUBLIC_SYSTEM_APP_ID`, `system-ui-next`, `SystemUi`, `system-login`, `system-auth-session`, `system-theme`, `system-auth-cleared` / `-refreshed`, `SystemBasicFeatures`, `system_messenger_dashboard`, `System messenger`. Confirm, especially `system-ui-next`, which sits close to the existing CSS `system-ui` font keyword (no technical clash).
16. (→ D16) **Q16 Old `.next-test` / `.next-test-tb` output** with the old strings: default leave it for the next `dev:test` / build to overwrite (it is excluded from the gate and review). No manual deletion.

## 8. Delivery slices and tickets

| Ticket | Title | Owner | Depends on |
|--------|-------|-------|------------|
| T-RENAME-001 | API.Framework: remove v1 URL versioning and flatten Controllers\V1 | dev-bot | D1, D2, D3, D6 |
| T-RENAME-002 | API.Framework: Unity → System (CORS, JWT issuer / audience, seeded names via a new EF migration) | dev-bot | 001, D7, D15 |
| T-RENAME-003 | UI.NextJs.Framework: code renames (functions, types, files, package, env var names, keyword) | dev-bot | D15 |
| T-RENAME-004 | UI.NextJs.Framework: visible text and runtime storage keys / events | dev-bot | 003, D10 |
| T-RENAME-005 | v1 consumers: e2e helpers, dev-test.mjs, Api.Framework.http, UI READMEs | dev-bot | 001, 003, D13 |
| T-RENAME-006 | Code framework rules, skills and docs (API `.cursor` + `.claude`, UI `.cursor`, ai-code-framework) | dev-bot | 001–005, D10 |
| T-RENAME-007 | Pre-handoff gate selftest and fixtures | dev-bot | 002, 005 |
| T-RENAME-008 | Test framework docs and e2e scenario steps | test-bot | 001, 004, D5 |
| T-RENAME-009 | Planning framework and ai-framework.config.yaml | plan-bot | 001, D11, D12 |
| T-RENAME-010 | Review framework checklists (cross-framework) | review-bot | 001, 003, D9 |
| T-RENAME-011 | Neil's environment steps and final verification (gate, .auth, e2e run) | human + dev-bot + test-bot | all |

**Start condition (D3):** no ticket (T-RENAME-009 included) starts until Neil records the merges of manage-animals AND pre-handoff-checks: stage `merged` in both `work/manage-animals/handoff.md` and `work/pre-handoff-checks/handoff.md`, or Neil tells Dev Bot directly. Dev Bot checks this before `pickup: accepted`.

Order (D4): [Neil merges manage-animals + pre-handoff-checks] → 001 → 002 → 003 → 004 → 005 (+ Neil N1 at the moment the UI env var rename lands, N3 after config.ts) → 006, 007 → 008, 009, 010 → 011 verification → one review (+ Test Bot run alongside).

## 9. Risks

- **No git.** The backup zip is the only rollback. Agents must not run concurrent edits on the same targets while this is in development (D3).
- **UI falls back to Unity.API v2** if `NEXT_PUBLIC_SYSTEM_API_ROOT` is not set when the code switches names (`environment.ts:6`). That is why N1 happens at the same moment.
- **Accidental `System` collisions** in C# (`using System`, `TimeProvider.System`) or the UI (`IsSystemAdmin`, `@design-system`, `--system-*`): never blind-replace, review the diff for these names.
- **Token invalidation and logout:** issuer change and storage keys force re-login; `.auth` must be regenerated before the e2e run.
- **EF migration:** wrong ids in UpdateData would duplicate rows. The migration must update by existing ids and be checked against the Test DB.
- **Stale strings** in `.next*` output can mislead a grep. Exclude build output when verifying.
- **DB rollback order (review F-02; Neil 2026-10-09 13:53 BST).** If the rename is rolled back, do the database FIRST and the files SECOND:
  1. With the NEW (System-named) code still in place and the Development API stopped, run from `ai-code-framework\api\API.Framework`:
     `dotnet ef database update 20261008150221_AddAnimals --project Api.Framework.Data --startup-project Api.Framework`
     (the DbContext is in Api.Framework.Data and the startup project is Api.Framework, the same flags as `api-framework-data-migrations.mdc:37`). This runs the `Down` of `20261009114033_RenameUnityToSystem`, which puts the five renamed seed rows back to their Unity names.
  2. THEN restore `D:\Users\nwood01\Documents\Candc\backups\ai-framework-pre-rename-20261009-1120.zip`.
  - **Why this order:** the zip does not contain the rename migration. If you restore it first, nothing is left that can undo the migration. The database keeps the System-named seed rows, the old code looks them up by their Unity names, and sign-in returns 400 (`Api.Framework.Services/Directory/TenantService.cs:335`, the Basic feature lookup by name: "The feature catalogue has not been seeded.").
  - Do not start the NEW API between step 1 and step 2. Development startup applies pending migrations (`InitialisationSettings:MigrateDatabase`), so it would apply the rename again.
  - `api-framework-data-migrations.mdc:44` says `dotnet ef database update` is not run against a shared database unless Neil asks. Only Neil runs this step, or an agent he names.
  - Open point (suggested default): if Test Bot's Test API has also applied the rename to the Test database, repeat step 1 against the Test database before restoring the zip.
