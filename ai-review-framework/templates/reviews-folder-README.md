# reviews/

PR review reports for this feature, written by `ai-review-framework` (`loops/pr-review.md`).

- `review-log.md` — append-only history of every review round, whichever route was used (date, source, branch or PR, verdict, and each comment as `file:line`, severity, comment, suggested fix).
- PR route: one report per pull request, `PR-<id>-review.md`. A re-review after new commits **overwrites** it; the header records the reviewed commit and iteration.
- Direct route (implementing agent hand-off, no PR): one report per round, `DIRECT-<branch-slug>-<n>-review.md` (`DIRECT-<feature>-<n>-review.md` when no branch is recorded). By default it reviews all code relevant to the plan (`review.direct_scope: plan`), not a diff.
- Reviews start automatically when the implementing agent hands off or a PR is raised or updated.
- These files are written on every round. Comments are posted to the PR only on Azure DevOps with `review.publish.enabled: true`; until then (and always for GitHub, Cursor Origin or local git) these files are the whole review.
- Each report checks the PR against this feature's `specs/` (controls and Service / Target DB Table / Target DB Column) and `tickets/` (Given / When / Then), plus the active API / UI rules from `ai-framework.config.yaml`. Only code under the API / UI folders (`review.scope_include`) is reviewed; the specs and tickets are the reference, not reviewed.
- Reports are advisory. A human reviewer owns the merge decision.
