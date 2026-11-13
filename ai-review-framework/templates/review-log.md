# Review log: <feature-slug>

Append-only history of every review round for this feature, whichever route was used: a direct hand-off from the implementing agent or a pull request. The reviewing agent appends one **Round** block per review, at loop stage 10 of `loops/pr-review.md`, with no human request needed.

- Feature: `<feature_path>/`
- Pipeline state: `handoff.md`
- Full reports, one per round: `reviews/DIRECT-<branch-slug>-<n>-review.md` or `reviews/DIRECT-<feature>-<n>-review.md` with no branch (direct route) · `reviews/PR-<id>-review.md` (PR route, overwritten on each PR update)

Rules:

- Append only. Newest round at the bottom. Never edit or delete an earlier round; a correction goes in a new round's **Notes**.
- **Direct route:** the **Comments** table is required, with one row per finding, matching the full report.
- **PR route:** the round block plus **Summary** is required. The comments are in the full report (and on the PR only when publishing is on, which needs provider `azure-devops`), so the **Comments** table is optional.
- Dates in Europe/London. No tokens, connection strings or personal data from fixtures.
- Copy this file to `<feature_path>/reviews/review-log.md` (`review.log_file`) the first time a feature is reviewed. Keep this header and drop the template block below.

---

<!-- Template block: copy it for each round and append it below the last round. -->

## Round <n> — <DD/MM/YYYY HH:MM> (Europe/London)

| Field | Value |
|-------|-------|
| Source | <direct \| pr> |
| Trigger | <direct-handoff \| pr-opened \| pr-updated \| test-report> |
| Branch / PR | <`feat/T-<DOMAIN>-NNN/<slug>` or "no branch" (direct) \| PR-<id> <url> (pr)> |
| Scope | <plan: <n> manifest + <n> discovered files, <n> not implemented \| diff: <n> files (direct_scope: diff) \| PR diff: <n> files> |
| Target | `<base / target branch>` |
| Repos @ commit | `<api repo path>` @ `<short-sha>`; `<ui repo path>` @ `<short-sha>` \| "not under git" |
| Tickets | T-<DOMAIN>-NNN, … |
| Verdict | **<Approve \| Approve with comments \| Request changes>** |
| Code / test verdict | <code verdict> / <test verdict \| not yet \| Tests blocked: <reason>> |
| Findings | Blocker <n> · Major <n> · Minor <n> · Nit <n> |
| Full report | `reviews/<DIRECT-<branch-slug>-<n> \| DIRECT-<feature>-<n> \| PR-<id>>-review.md` |
| Posted to PR | <n/a (direct) \| Yes: inline <n>, summary yes (COMMENT event) \| No: provider does not support posting (<cursor-origin \| local-git>) \| No: `review.publish.enabled` is false> |
| Handed to | <implementing agent, <agents.code.name> (changes-requested) \| human owner, <agents.human.name> (approved, ready to merge) \| human owner, <agents.human.name> (review cap reached)> |

### Summary

<Two or three sentences: what changed, what it was checked against, the main reasons for the verdict.>

### Comments

| ID | File:line | Severity | Comment | Suggested fix |
|----|-----------|----------|---------|---------------|
| F-01 | `<path>:<line>` | <Blocker \| Major \| Minor \| Nit> | <What is wrong and why, citing the spec row, ticket scenario or rule file> | <Concrete change> |

### Changes since last round

<Round 1: "First review." Later rounds: resolved F-NN, still open F-NN, new F-NN.>

### Notes

<Optional. Corrections to earlier rounds, out-of-scope notes for the planning agent, tooling gaps.>
