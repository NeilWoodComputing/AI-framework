# Skill: write-review-report

Turn the stage 2–7 results into one report, decide the verdict and write it next to the feature's planning artefacts (loop stage 8). Then append the round to the feature's review log (loop stage 10). Both routes, direct hand-off and PR, use this skill; it runs automatically as part of every review, with no human request.

## Purpose

Give the implementing agent, the PR author and the human owner a single, traceable document: verdict, findings, and per-control, per-column and per-scenario tables they can check against the specs.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | Change metadata, **review scope** (files with reasons, exclusions, not implemented / deferred), linked tickets, specs, active API / UI |
| `findings` | Yes | From stages 2–7 |
| `tables` | Yes | Spec conformance, data mapping, GWT coverage, tests |
| `config` | Yes | `review.severity_threshold`, `review.report_names`, `review.log_file`, `output.work_dirs` (via `feature_path`), `output.feature_layout.reviews` |
| `route` | Yes | `direct` or `pr` (`handoff.md` `routes.code_to_review`), plus the trigger |
| `previous_report` | No | PR route: existing `PR-<id>-review.md`. Direct route: the previous round's `DIRECT-<branch-slug|feature>-<n-1>-review.md` |
| `publish_result` | No | From loop stage 9 (PR route): what was posted, or why nothing was |

## Steps

1. **Number findings** `F-01`, `F-02`, … ordered by severity (Blocker → Nit), then by file.
2. **Check each finding** has: severity, area, `file:line`, the finding, a spec / rule reference, and a suggested fix. Drop or rewrite any finding without a reference.
3. **Decide the verdict** from `checklists/severity.md`:
   - Any Blocker → **Request changes**
   - Any mandatory spec control missing or any DB mapping unmet (Mismatch / Unmapped) → **Request changes**
   - Any finding at or above `review.severity_threshold` (default `major`) → **Request changes**
   - Otherwise any Minor → **Approve with comments**
   - Otherwise (Nits only, or nothing) → **Approve**
   - No linked ticket → verdict capped at **Approve with comments**
   - This is the code verdict (`review.code_verdict`). It does not by itself approve the feature. Final approval is loop stage 11: it also needs an approving test review, a test run that is not blocked, and a pass for each required unit command (`skills/review-tests/SKILL.md`).
4. **Write the Review scope section.** Say how the scope was built: PR diff; plan scope (manifest + codebase search, whole files); or local diff. List every file reviewed with its repo, class and reason (**manifest**, **discovered**, **diff**, **dependency**), give manifest vs discovered counts, list excluded patterns and any PR / diff files left out for being outside `review.scope_include`, and list controls / mappings found **Not implemented** or **Deferred**. Every **discovered** file has its Minor "manifest incomplete" finding.
5. **Write the summary** (3–6 sentences): what the change does, which tickets and specs it was checked against, which rule sets were applied (and, if any, which points were judged as General practice because no rule covers them), and the main reasons for the verdict.
6. **Fill the template** `templates/review-report.md`. Keep every table; write `Not assessed — <reason>` rather than deleting a section. Put unrelated pre-existing issues found in plan-scope files under **Out of scope / pre-existing notes**. They are not findings and do not affect the verdict.
7. **Re-review.** If a previous report exists, keep its header fields, bump **Review iteration**, update **Reviewed commit**, and fill **Changes since last review** (findings resolved, still open, new). Record the round type in **Review scope**: scoped re-review or full pass (`skills/gather-pr-context/SKILL.md` step 9, item 7).
8. **Write the file** to `<feature_path>/<output.feature_layout.reviews>/`, named by `review.report_names`:
   - PR route: `PR-<id>-review.md` (overwrite on each PR update)
   - Direct route: `DIRECT-<branch-slug>-<n>-review.md`, a new file per round (`<branch-slug>` = branch with `/` replaced by `-`; `n` = `review.cycle` + 1 from `handoff.md`). With no branch in `handoff.md`: `DIRECT-<feature>-<n>-review.md`
   - `<feature>` from the first linked ticket; other features listed in the header
   - No linked ticket → `ai-planning-framework/work/_unlinked/reviews/`
   - New `reviews/` folder → also copy `templates/reviews-folder-README.md` to `reviews/README.md`
9. **Publishing** is loop stage 9, not this skill: its rules, including the report footer wording, live in `loops/pr-review.md` stage 9. The report and the log are written on every round regardless.

## Review log (loop stage 10, both routes)

10. **Open the log** `<feature_path>/<output.feature_layout.reviews>/<review.log_file>` (default `reviews/review-log.md`). If it does not exist, create it from `templates/review-log.md`: keep the header, drop the template block.
11. **Append one Round block** at the bottom, copied from the template: round `n`, date (Europe/London), source (`direct` / `pr`), trigger, branch or PR id + url, **scope** (e.g. "plan: 7 manifest + 1 discovered, 0 not implemented" / "PR diff: 9 files"), target, repos @ commit, tickets, verdict, counts, full report path, what was posted to the PR, and who it was handed to.
12. **Comments.** Direct route: one row per finding — ID, `file:line`, severity, comment, suggested fix — matching the report exactly. PR route: the Summary is required; the Comments table is optional because the comments are in the report and on the PR.
13. **Append only.** Never edit or delete earlier rounds. Fill **Changes since last round** from the previous round's IDs.

## Outputs

- `<feature_path>/reviews/PR-<id>-review.md` (PR route) or `DIRECT-<branch-slug>-<n>-review.md` / `DIRECT-<feature>-<n>-review.md` (direct route)
- One new Round block appended to `<feature_path>/reviews/review-log.md`
- A one-paragraph summary for the hand-back message: verdict, counts by severity, report path, log path

## Quality checks

- [ ] Verdict matches the rules above and the configured threshold
- [ ] Findings table complete; every row has a reference and suggested fix
- [ ] Spec conformance and data mapping tables have a row per control; GWT table has a row per scenario
- [ ] Dates in Europe/London; reviewed commit recorded
- [ ] Review scope section complete: method, every file with its reason, manifest vs discovered, exclusions, not implemented / deferred
- [ ] Out of scope / pre-existing notes hold suspected spec issues, files outside the active codebases and unrelated pre-existing issues; none of them counted in the verdict
- [ ] Report named per `review.report_names` for the route used
- [ ] Round appended to `review-log.md`; earlier rounds untouched; direct route lists every comment
- [ ] Nothing posted to the PR from this skill (posting is loop stage 9)
