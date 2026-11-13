# Ticket: T-RENAME-006 — Code framework rules, skills and docs (API .cursor + .claude, UI .cursor, ai-code-framework)

| Field | Value |
|-------|--------|
| ID | T-RENAME-006 |
| Type | Docs / rules |
| Feature | system-rename |
| Priority | Medium |
| Owner | dev-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** an agent reading the framework rules  
**I want** the rules to describe System and versionless routes  
**So that** agents stop generating v1 routes and Unity names

## Full-stack scope

Docs only. API.Framework: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc` and `.claude/rules/*.md` (auth-permissions, controllers, overview, testing, ui-contract, json-schema-forms), `.cursor/skills` and `.claude/skills` (crud-feature, json-schema, ui-contract, feature-loop, tests where they describe the active target). UI.NextJs.Framework: `AGENTS.md`, `.cursor/rules/framework/*` (framework-overview, json-schema-forms, modal-routing, state-layer), `.cursor/rules/style/*` (css, design-system), `src/framework/README.md`, `src/framework/design-system/README.md`. ai-code-framework: `.cursor/rules/api-json-schema-forms.mdc:13`, and `loops/feature-build.md` / `AGENT-BRIEF.md` only where they describe API.Framework / Next.js.

## Work to do

1. Replace `v1` routes, `Controllers/V1/...` layout text, `[ApiVersion]` guidance and `NEXT_PUBLIC_UNITY_*` with the new state.
2. Replace Unity names that describe the active target (e.g. "Reference .NET 10 API for Unity JSON schema forms") with System.
3. Keep every mention of the real Unity.API, Unity.UI.Framework and UI.Angular (e.g. "Copy Unity.API BFF patterns" as a don't, "same idea as Unity"), per D10.
4. Make every API.Framework rule / skill edit in **both** `.cursor` and `.claude`, with identical wording. UI.NextJs.Framework has only `.cursor`.
5. Run the pre-handoff docs-dup check.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-006/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — Rules describe versionless routes

```gherkin
Given the API.Framework and ai-code-framework rules and skills
When I search for "v1", "V1" and "apiVersion"
Then no match describes API.Framework routes or folders
```

### Scenario: S2 — Both rule copies match

```gherkin
Given each API.Framework rule or skill edited in .cursor
When I compare it with its .claude copy
Then the changed paragraphs are identical
```

### Scenario: S3 — Real Unity references are kept

```gherkin
Given the docs mention Unity.API, Unity.UI.Framework or UI.Angular
When the rename is done
Then those mentions are unchanged
```

### Scenario: S4 — Env var names in docs

```gherkin
Given the UI rules and AGENTS.md
When I search for "NEXT_PUBLIC_UNITY"
Then there are no matches and NEXT_PUBLIC_SYSTEM_API_ROOT / NEXT_PUBLIC_SYSTEM_APP_ID are documented as Neil-owned
```

Checklist (derived from scenarios):

- [ ] v1 / V1 text gone from active-target docs
- [ ] `.cursor` = `.claude` for every API edit
- [ ] Real Unity references kept
- [ ] docs-dup check passes

## Out of scope

- Unity.API and UI.Angular.Framework docs
- Test, review and planning framework docs (008, 010, 009)
- Historical `work/` artefacts

## Notes

- Stable ID for DevOps upsert: `T-RENAME-006`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
