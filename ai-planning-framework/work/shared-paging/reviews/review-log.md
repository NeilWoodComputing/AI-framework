# Review log: shared-paging

Append-only history of every review round for this feature, whichever route was used: a direct hand-off from the implementing agent or a pull request. The reviewing agent appends one **Round** block per review, at loop stage 10 of `loops/pr-review.md`, with no human request needed.

- Feature: `ai-planning-framework/work/shared-paging/`
- Pipeline state: `handoff.md`
- Full reports, one per round: `reviews/DIRECT-<branch-slug>-<n>-review.md` or `reviews/DIRECT-<feature>-<n>-review.md` with no branch (direct route) · `reviews/PR-<id>-review.md` (PR route, overwritten on each PR update)

Rules:

- Append only. Newest round at the bottom. Never edit or delete an earlier round; a correction goes in a new round's **Notes**.
- **Direct route:** the **Comments** table is required, with one row per finding, matching the full report.
- **PR route:** the round block plus **Summary** is required. The comments are in the full report (and on the PR only when publishing is on, which needs provider `azure-devops`), so the **Comments** table is optional.
- Dates in Europe/London. No tokens, connection strings or personal data from fixtures.

---

## Round 1 — 09/10/2026 19:05 (Europe/London)

| Field | Value |
|-------|-------|
| Source | direct |
| Trigger | direct-handoff |
| Branch / PR | no branch (direct) |
| Scope | plan: 56 manifest files (api 36, ui 12, tests 8), 0 discovered, 0 not implemented; + `SystemUiCorsTests.cs` (dependency) |
| Target | n/a (plan scope) |
| Repos @ commit | not under git |
| Tickets | T-PAGING-001, T-PAGING-002, T-PAGING-003, T-PAGING-004, T-PAGING-005, T-PAGING-006 |
| Verdict | **Approve with comments** (provisional code verdict; option B, awaiting T-PAGING-007 + test review) |
| Findings | Blocker 0 · Major 0 · Minor 1 · Nit 6 (+ 1 note) |
| Full report | `reviews/DIRECT-shared-paging-1-review.md` |
| Posted to PR | n/a (direct) |
| Handed to | testing agent, Test Bot (T-PAGING-007, needs PostgreSQL on 5432); review stays with Review Bot |

### Summary

- **What changed:** one shared Paging area (contracts moved with identical members and JSON, `PageWindow`, whitelisted `SortMap` with an ascending secondary and a final Id tie-break, `ToPagedBodyAsync`); Animals Name search on `NormalizedName` (Npgsql escaped `LIKE`, proven model-only); a working ReferenceData Types search; a debounced, page-1-resetting `setFilters`; the Animals search box per decision 31.
- **Checks:**
  - gate on a copy and in place (check-only): pass;
  - API unit 127/127 (none needs PostgreSQL);
  - vitest 35/35;
  - self-test 64/64.
- **Not checked live:** PostgreSQL, the API and the UIs were down, so this is a code-only review.

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-01 | `Api.Framework.Tests/Cors/SystemUiCorsTests.cs:52-62` | Minor | Finds appsettings by walking up to `Api.Framework.sln`; 2 tests fail when built outside the tree (reproduced: 125/2). This limits how system-rename F-15 can be fixed | Copy the appsettings files into the test output (linked content) or stamp the project folder in; name the missing file in the failure |
| F-02 | `tickets/T-PAGING-002-…md:85` | Nit | S6 says DateBorn desc then Id; the code (and the pre-feature behaviour) is DateBorn desc, Name, Id | Plan Bot: reword S6 and describe the SortMap secondary in plan §5.1 |
| F-03 | `plan.md:26`, `:52`, P12 | Nit | The Types grid already kept search in the URL before this feature | Plan Bot: correct §2 and scope P12 to local grids |
| F-04 | `ReferenceDataTypesGrid.tsx:66-76` | Nit | The Types search box has no aria-label (the new rule requires one) | `aria-label="Filter types"` |
| F-05 | `ReferenceDataTypesGrid.tsx:59` | Nit | The local box value doesn't re-sync when the URL `searchText` changes (Back/Forward) | Re-sync when not pending; optional hook test with URL state |
| F-06 | `AnimalSearchSqlTests.cs:15-21` | Nit | `\` escaping not pinned | Add a `\` case |
| F-07 | `AnimalServiceSearchTests.cs:89-110`, `ReferenceDataQueryTests.cs:122-135` | Nit | The 400 is tested via `Validator` only, not the HTTP pipeline | e2e (T-PAGING-007) or a WebApplicationFactory test |

### Changes since last round

First review.

### Notes

- F-08 (note): `[StringLength]` counts untrimmed input. This agrees with the UI's `maxLength`, so no change.
- No sign-in, no process or container started or stopped, no `.env*` opened, no secret value written. Temporary copies only, under `%TEMP%`.
