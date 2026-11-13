# Ticket: T-RENAME-008 — Test framework docs and e2e scenario steps

| Field | Value |
|-------|--------|
| ID | T-RENAME-008 |
| Type | Test framework (cross-framework) |
| Feature | system-rename |
| Priority | Medium |
| Owner | test-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** the testing agent  
**I want** its docs, skills and scenario steps to use versionless routes and System names  
**So that** test plans and e2e steps match the renamed system

## Full-stack scope

Test Bot's own files: `ai-test-framework/README.md` (lines 93, 105 and any other active-target `v1` / `NEXT_PUBLIC_UNITY_API_ROOT`), `skills/add-test-data-reset/SKILL.md` (54, 56, 65, 77), plus `examples` / `templates` only where they describe API.Framework routes. Scenario code: `UI.NextJs.Framework/e2e/features/animals/animals.steps.ts:42, 44, 275` (`\/v1\/Animal`, `\/v1\/schemas\/create-animal`), `e2e/features/common/auth.steps.ts:12` (comment naming `unity-auth-session`).

## Work to do

1. Drop `v1/` from the TestData reset routes and API URLs in the README and skills; `NEXT_PUBLIC_UNITY_API_ROOT` → `NEXT_PUBLIC_SYSTEM_API_ROOT`.
2. Keep the Unity.API / Unity.API.Tests / Unity.UI.Framework references (real repos), and leave historical test reports and the manage-animals test plan as they are.
3. Update the `animals.steps.ts` regexes to match `/Animal` and `/schemas/create-animal` without `/v1` (anchored on the API root so they don't match UI routes), and the `auth.steps.ts` comment.
4. Plan Bot does not edit these files; Test Bot updates them itself.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-008/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — Reset routes documented without v1

```gherkin
Given ai-test-framework README and skills/add-test-data-reset/SKILL.md
When I search for "v1/TestData"
Then there are no matches and the routes read POST TestData/Reset/master and POST TestData/Reset/{scenarioKey}
```

### Scenario: S2 — Animals steps observe the new routes

```gherkin
Given the manage-animals e2e scenarios
When they run against the renamed API
Then the network observers match GET /Animal and /schemas/create-animal, and the "no further GET /Animal" assertion (line 275) still counts correctly
```

### Scenario: S3 — Real Unity references stay

```gherkin
Given the test framework docs
When the rename is done
Then mentions of Unity.API, Unity.API.Tests and Unity.UI.Framework are unchanged
```

Checklist (derived from scenarios):

- [ ] README + reset skill updated
- [ ] Steps regexes updated
- [ ] Real Unity references kept

## Out of scope

- e2e helpers / scaffolding (Dev Bot, T-RENAME-004 / 005)
- Historical test reports

## Notes

- Stable ID for DevOps upsert: `T-RENAME-008`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
- Cross-framework ticket drafted by Plan Bot for Test Bot (owners update their own files).
