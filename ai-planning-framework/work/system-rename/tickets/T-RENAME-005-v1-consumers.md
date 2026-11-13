# Ticket: T-RENAME-005 — v1 consumers: e2e helpers, dev-test.mjs, Api.Framework.http, UI READMEs

| Field | Value |
|-------|--------|
| ID | T-RENAME-005 |
| Type | Cross-cutting (tooling + docs) |
| Feature | system-rename |
| Priority | High |
| Owner | dev-bot |
| Specs | None (no UI pages, controls or DB columns change); `plan.md` §5 |
| Journey (optional) | — |

## User story

**As** a developer or the testing agent running the UI and e2e suite  
**I want** every API base URL in our tooling to have no /v1  
**So that** tests and local runs reach the routes from T-RENAME-001

## Full-stack scope

No controls or DB columns. Files: `UI.NextJs.Framework/e2e/helpers/config.ts:7-16` (logic), `scripts/dev-test.mjs:3, 27`, `API.Framework/Api.Framework/Api.Framework.http:4, 14, 23, 26`, `UI.NextJs.Framework/README.md` (lines 17, 26, plus the env var names), `e2e/README.md` (lines 3, 33, 56, 60, 95).

## Work to do

1. `getApiUrl()`: return `API_URL` trimmed of a trailing `/` without appending `/v1`; default `http://localhost:5188`; update the doc comment. If `API_URL` still ends with `/v1`, fail with a clear message rather than calling a dead route (default; avoids a silent 404).
2. `dev-test.mjs`: default `E2E_UI_API_ROOT` `https://localhost:7188/`; header comment updated (the `NEXT_PUBLIC_SYSTEM_API_ROOT` rename is in T-RENAME-003).
3. `Api.Framework.http`: drop `/v1` from the 4 requests.
4. UI README and e2e README: drop `/v1`, use `NEXT_PUBLIC_SYSTEM_*`; keep `unity_login` (D7). No env values copied from `.env*`.
5. Tell Neil the moment `config.ts` stops appending so step N3 (user env var `API_URL`, and `E2E_UI_API_ROOT` per D13) happens next.

## Acceptance criteria

Every heading has an explicit ID `S<n>` (full ID `T-RENAME-005/S<n>`). Never renumber or reuse an ID.

### Scenario: S1 — API URL has no v1

```gherkin
Given API_URL is "http://localhost:5188"
When getApiUrl() runs
Then it returns "http://localhost:5188"
```

### Scenario: S2 — Default API URL

```gherkin
Given API_URL is not set
When getApiUrl() runs
Then it returns "http://localhost:5188"
```

### Scenario: S3 — A stale v1 API_URL is reported

```gherkin
Given API_URL still ends with "/v1"
When getApiUrl() runs
Then it fails with a message naming API_URL and telling the user to drop /v1, without printing any secret
```

### Scenario: S4 — Test UI uses the new root

```gherkin
Given E2E_UI_API_ROOT is not set
When npm run dev:test starts
Then the UI is started with NEXT_PUBLIC_SYSTEM_API_ROOT "https://localhost:7188/"
```

### Scenario: S5 — http file and docs have no v1

```gherkin
Given Api.Framework.http, the UI README, the e2e README, e2e/helpers/config.ts and scripts/dev-test.mjs
When I search for "/v1" and "NEXT_PUBLIC_UNITY"
Then no configured API root, route, default value or code path contains "/v1", and there is no "NEXT_PUBLIC_UNITY"
And the only "/v1" matches are prose that explicitly explains /v1 was removed (e.g. a README note that the root has no /v1) and the S3 guard that rejects an API_URL still ending in /v1
```

Checklist (derived from scenarios):

- [ ] `config.ts` logic changed
- [ ] `dev-test.mjs` default changed
- [ ] `.http` and READMEs updated
- [ ] Neil told when N3 is due

## Out of scope

- `animals.steps.ts` regexes (Test Bot, T-RENAME-008)
- Config yaml (T-RENAME-009)
- The user env var change itself (T-RENAME-011 N3)

## Notes

- Stable ID for DevOps upsert: `T-RENAME-005`
- Approved (Neil 2026-10-09 11:47 BST; decisions D1–D16 in plan.md §6). **Start condition (D3):** build begins only after Neil records the merges of manage-animals AND pre-handoff-checks (stage `merged` in their handoff.md, or Neil tells Dev Bot directly).
- The stale-`/v1` guard in S3 is a Plan Bot in-ticket default (not one of Q1–Q16; Neil may override: alternative is to silently strip `/v1`).
- S5 Then clarified 2026-10-09 after Test Bot run 1 (explanatory mentions allowed)
