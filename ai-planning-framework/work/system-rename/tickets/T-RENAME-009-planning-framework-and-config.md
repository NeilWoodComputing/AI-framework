# Ticket: T-RENAME-009 — Planning framework and ai-framework.config.yaml

| Field | Value |
|-------|--------|
| ID | T-RENAME-009 |
| Type | Framework docs / config |
| Feature | system-rename |
| Priority | Medium |
| Owner | plan-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** the planning agent  
**I want** Plan Bot's files and the shared config to describe the renamed targets  
**So that** agents read correct routes and names from the config

## Full-stack scope

`ai-framework.config.yaml` (D12: Plan Bot): line 436 `api_base_url: <https://localhost:<api-port>/v1>`, 439 `master_route: v1/TestData/Reset/master`, 441 `batch_route: v1/TestData/Reset/{scenarioKey}`, and the nextjs `description` lines 155–156 ("Unity.UI.Next … Calls Unity.API v2 via NEXT_PUBLIC_UNITY_API_ROOT"). Keep the `unity-api` entries (real repo). Planning framework, unchanged by D11 (keep): `schemas/page-spec.schema.json:45-47`, `generators/excel_spec.py:332-333`, `templates/yaml/manage-list-contacts.yaml:9`, `templates/yaml/paginated-grid-sample.yaml:10`.

## Work to do

1. Config: drop `/v1` and `v1/` on lines 436, 439, 441; rewrite the nextjs description to describe the System UI calling the active API via `NEXT_PUBLIC_SYSTEM_API_ROOT` (D14: the fallback stays Unity.API v2; say so). Validate YAML on the box, LF, UTF-8 without BOM, minimal edit, re-read and hash-check first.
2. Planning framework (D11: keep): no planning framework file changes. `unity_feature` / "Unity Feature" stay because they mirror the "Unity Feature" column of Neil's source spreadsheets.
3. Do not edit `work/*` historical specs or the shared handoff template's Unity.API examples.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-009/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — Config routes have no v1

```gherkin
Given ai-framework.config.yaml
When I read testing.api_base_url, master_route and batch_route
Then none contains v1 and the file parses as YAML
```

### Scenario: S2 — Next.js description is current

```gherkin
Given development.ui.nextjs.description
When I read it
Then it names NEXT_PUBLIC_SYSTEM_API_ROOT and no longer says it calls Unity.API v2 via NEXT_PUBLIC_UNITY_API_ROOT
```

### Scenario: S3 — Planning framework is unchanged

```gherkin
Given D11 (keep unity_feature)
When T-RENAME-009 is done
Then no file under ai-planning-framework has changed except this feature's own work folder
```

### Scenario: S4 — Real Unity entries stay

```gherkin
Given the config's unity-api, Angular and branch-pattern comments
When the edit is done
Then they are unchanged
```

Checklist (derived from scenarios):

- [ ] 3 config routes + description updated; YAML valid
- [ ] Planning framework per D11
- [ ] Historical specs untouched

## Out of scope

- Other frameworks' files
- `out/*.xlsx`, source attachments

## Notes

- Stable ID for DevOps upsert: `T-RENAME-009`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
- Not applied yet: like every other ticket, it waits for the start condition (Neil 2026-10-09 11:47).
- **Done 2026-10-09T12:38:50+01:00 (plan-bot)**, after the D3 start condition was met (Neil to Dev Bot 12:37 BST). ai-framework.config.yaml: `development.ui.options.nextjs.description` rewritten (System UI Next / `system-ui-next`, `NEXT_PUBLIC_SYSTEM_API_ROOT`, no `/v1`; Unity.API v2 fallback noted per D14); `testing.api_base_url`, `reset_endpoint.master_route` and `batch_route` without `v1` (S1, S2). Planning framework unchanged per D11 (S3). Unity.API / Unity.UI.Framework / UI.Angular entries, branch-pattern comment and `unity_login` untouched (S4). YAML validated on the box; only those lines changed (2 description lines became 4; 3 route lines)
