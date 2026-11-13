# Ticket: T-RENAME-003 — UI.NextJs.Framework: code renames (functions, types, files, package, env var names, keyword)

| Field | Value |
|-------|--------|
| ID | T-RENAME-003 |
| Type | UI framework (cross-cutting) |
| Feature | system-rename |
| Priority | High |
| Owner | dev-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** a developer working in UI.NextJs.Framework  
**I want** the framework's identifiers and files to say system instead of unity  
**So that** the code matches the product name

## Full-stack scope

No controls or DB columns. Identifiers: `unityApiFetch`, `readUnityApiJson`, `isUnityApiSuccess`, `UnityApiFetchInit`, `UnityJsonSchema*`, `UnitySchema*`, `unityCookieService`, the `Unity*` renderers. Files (8): `src/framework/api/unity-api-fetch.ts`, `auth/storage/unity-cookie.service.ts`, `json-schema-form/components/renderers/unity-json-form-renderers.tsx`, `models/unity-json-schema.model.ts`, `schema/unity-schema-api.mapper.ts`, `schema/unity-schema-value.mapper.ts`, `schema/unity-schema.adapter.ts`, `validation/unity-schema-validation.ts`. Also `src/config/environment.ts`, `scripts/dev-test.mjs:47`, `package.json`, `package-lock.json`.

## Work to do

1. Rename the identifiers above to `System*` / `system*` (D15) and update every reference, including local variables like `unitySchema` and the `json-schema-form/index.ts` barrel.
2. Rename the 8 files to `system-*` and update all imports. Keep LF, UTF-8 without BOM.
3. Env var names in code: `NEXT_PUBLIC_UNITY_API_ROOT` → `NEXT_PUBLIC_SYSTEM_API_ROOT`, `NEXT_PUBLIC_UNITY_APP_ID` → `NEXT_PUBLIC_SYSTEM_APP_ID` (`environment.ts`, `dev-test.mjs`). Keep the fallback values (D14). Coordinate the landing moment with Neil's step N1 (T-RENAME-011).
4. Package name `unity-ui-next` → `system-ui-next` in `package.json` and the two `name` fields of `package-lock.json` (no dependency changes).
5. Error-object keyword `'unity'` → `'system'` (`unity-schema-validation.ts:269`) and anything that reads it (tests included).
6. Never touch `IsSystemAdmin`, `system-admin`, `@design-system`, `--system-red/green` or `system-ui`. `npx tsc --noEmit`, `npm run lint` and `npm test` pass.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-003/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — No unity identifiers or file names remain in code

```gherkin
Given the UI source under src, scripts and e2e/helpers
When I search case-sensitively for "Unity" and "unity" in identifiers and file names
Then none remain except text kept by D10
```

### Scenario: S2 — Imports resolve after the file renames

```gherkin
Given the 8 files are renamed to system-*
When npx tsc --noEmit and npm run build run
Then both pass
```

### Scenario: S3 — The UI reads the new env var names

```gherkin
Given NEXT_PUBLIC_SYSTEM_API_ROOT is set to the API root without /v1
When the UI calls the API
Then requests go to that root
And the code no longer reads NEXT_PUBLIC_UNITY_API_ROOT or NEXT_PUBLIC_UNITY_APP_ID
```

### Scenario: S4 — Validation errors carry the system keyword

```gherkin
Given a JSON schema form with a failing server-side constraint
When the UI maps the error
Then the error object has keyword "system" and the field shows the same message as before
```

### Scenario: S5 — Package is renamed

```gherkin
Given package.json and package-lock.json
When I read the name fields
Then they are system-ui-next and the dependency tree is unchanged
```

### Scenario: S6 — Existing system names are untouched

```gherkin
Given the counts recorded on 2026-10-09 (IsSystemAdmin 40, @design-system 47, --system-red 17, --system-green 15, system-ui 7)
When I count them again in the UI
Then the counts are unchanged
```

Checklist (derived from scenarios):

- [ ] Identifiers and barrel renamed
- [ ] 8 files renamed, imports fixed
- [ ] `NEXT_PUBLIC_SYSTEM_*` in code; landing coordinated with N1
- [ ] Package and keyword renamed
- [ ] tsc / lint / vitest pass

## Out of scope

- Visible text and storage keys (T-RENAME-004)
- `.env.local` / `.env.example` (Neil, T-RENAME-011 N1)
- node_modules and `.next*` output

## Notes

- Stable ID for DevOps upsert: `T-RENAME-003`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
- Ordering risk: if this lands before Neil sets `NEXT_PUBLIC_SYSTEM_API_ROOT`, the UI silently calls the Unity.API v2 fallback (`environment.ts:6`).
