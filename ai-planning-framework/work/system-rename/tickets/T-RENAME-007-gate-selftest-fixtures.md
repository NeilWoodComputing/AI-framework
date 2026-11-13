# Ticket: T-RENAME-007 — Pre-handoff gate selftest and fixtures

| Field | Value |
|-------|--------|
| ID | T-RENAME-007 |
| Type | Tooling |
| Feature | system-rename |
| Priority | Medium |
| Owner | dev-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** the implementing agent running the pre-handoff gate  
**I want** the gate's fixtures and selftest to use the new names  
**So that** the gate selftest stays green and does not encode old names

## Full-stack scope

No controls. Files: `ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` (lines 52, 58, 62 and any other `unity-login` / `/v1/`), `scripts/fixtures/pre-handoff/api-bad/appsettings.json` (6–7), `api-bad/appsettings.Commented.json` (5), `api-good/appsettings.json` (6–7), `api-good/appsettings.Development.json` (3).

## Work to do

1. `unity-login` → `system-login` and `https://localhost:7188/v1/` → `https://localhost:7188/` in the selftest's inline fixtures and the fixture files. Keep CRLF for the API fixtures, as today.
2. Do not change what the fixtures test (bad stays bad, good stays good). The allowlist is unchanged unless a renamed path needs it.
3. Run `node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs` and the gate on both targets.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-007/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — Selftest passes with new names

```gherkin
Given the updated fixtures
When node ai-code-framework/scripts/pre-handoff-checks.selftest.mjs runs
Then every case passes with the same expectations as before
```

### Scenario: S2 — Fixtures hold no old names

```gherkin
Given scripts/fixtures/pre-handoff and the selftest
When I search for "unity-login" and "/v1/"
Then there are no matches
```

### Scenario: S3 — Gate passes on both targets

```gherkin
Given T-RENAME-001..006 are done
When node ai-code-framework/scripts/pre-handoff-checks.mjs --target all --feature ai-planning-framework/work/system-rename --record ai-planning-framework/work/system-rename/handoff.md runs
Then code.pre_handoff_gate is pass and one line per check is recorded with no secret value
```

Checklist (derived from scenarios):

- [ ] Selftest + 4 fixture files updated
- [ ] Selftest green
- [ ] Gate pass recorded

## Out of scope

- Runner logic
- The allowlist (unless needed)

## Notes

- Stable ID for DevOps upsert: `T-RENAME-007`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
