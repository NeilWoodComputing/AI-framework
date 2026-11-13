# Ticket: T-RENAME-010 — Review framework checklists (cross-framework)

| Field | Value |
|-------|--------|
| ID | T-RENAME-010 |
| Type | Review framework (cross-framework) |
| Feature | system-rename |
| Priority | Low |
| Owner | review-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** the reviewing agent  
**I want** its checklists to describe versionless routes and the System env var names  
**So that** reviews don't flag correct code against old rules

## Full-stack scope

Review Bot's own files: `ai-review-framework/checklists/api-checklist.md:78` (layout `Controllers/V1/{Area}`, `Controllers/V1/Schemas`) and `checklists/ui-nextjs-checklist.md:9` (`NEXT_PUBLIC_UNITY_API_ROOT`). Leave Angular / Unity.API checklist items and sample reviews (real repos / historical).

## Work to do

1. Update the two lines to `Controllers/{Area}` / `Controllers/Schemas` and `NEXT_PUBLIC_SYSTEM_API_ROOT`.
2. Plan Bot does not edit these files (D9).

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-010/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — API checklist describes the new layout

```gherkin
Given the flattened controller layout (D1)
When I read api-checklist.md item 78
Then it matches the controller layout Neil chose and has no v1 route guidance
```

### Scenario: S2 — Next.js checklist uses the new env var

```gherkin
Given ui-nextjs-checklist.md
When I search for "NEXT_PUBLIC_UNITY"
Then there are no matches
```

Checklist (derived from scenarios):

- [ ] 2 checklist lines updated

## Out of scope

- Angular and Unity.API checklists
- Historical reviews

## Notes

- Stable ID for DevOps upsert: `T-RENAME-010`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
- In scope by D9.
