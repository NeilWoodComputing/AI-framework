# Agent brief — AI review framework

Short instructions for the **reviewing agent**: whichever agent reviews changes with this folder, a pull request or a direct hand-off from the implementing agent. Reviews are automatic; you start as soon as a trigger fires, without waiting for anyone to ask.

## Using this framework as any reviewing agent

This framework is written for a **role**, not a named agent, so any agent can pick it up and review the same way.

- **Roles.** The docs say *the reviewing agent* (you), *the implementing agent* (builds the code and fixes findings), *the planning agent* (owns specs and tickets) and *the human owner* (approves gates, owns the merge). `agents` in `../ai-framework.config.yaml` maps each role to the agent filling it today: `agents.review`, `agents.code`, `agents.planning`, `agents.human`. Use each entry's `name` when you message someone, and its `id` for `owner` / `updated_by` in `handoff.md` (you act as `agents.review.id`).
- **Read, in this order:** `../ai-framework.config.yaml` → this brief → `loops/pr-review.md` → the `skills/*/SKILL.md` for each stage → `checklists/severity.md` → `../handoff/README.md`.
- **Config keys you need:** `agents`; `development` (active API / UI, rules, agent docs); `output.work_dirs` + `output.feature_layout` (feature folder: `handoff.md` `feature_path` first); `review.auto_review` / `triggers`, `direct_scope`, `scope_include`, `scope_exclude`, `provider` + its block (`azure_devops`, `github`, `cursor_origin`, `local_git`), `target_branch`, `severity_threshold`, `report_names`, `log_file`, `publish`; `handoff.code_to_review`, `review_feedback`, `max_review_cycles`, `require_human_approval`; `secrets` (env var **names** only).
- **Access you need:** read access to the feature folder and the active API / UI paths; for the PR route, the connector for `review.provider` (Azure DevOps, GitHub where connected, or Cursor Origin, which needs no token), or local git for `local-git`. Connectors are used **read-only**.
- **Outputs, every round:** the full report and one appended Round in `reviews/review-log.md` (always both), then the `handoff.md` update and a hand-back message. Nothing else is edited. PR comments are posted when `review.publish.enabled: true` and `review.provider` is `github` or `azure-devops`; on `cursor-origin` and `local-git` record "Not published — direct route / provider does not support posting".
- **Stop and report** when a value you need is still a `<placeholder>`, or the connector you need is unavailable. Never guess.

## Read first

0. `../ai-framework.config.yaml` — shared config (paths relative to the `ai-framework` root):
   - `runtime` — which agent runtime performs the work. Resolve: user-preferences.yaml → per-role → shared default. **Verify correct runtime before work; if wrong, stop and hand off.**
   - `development` — active API and UI folder (`active:` under `api` and `ui`); their `rules` and `agent_docs` are what you review against
   - `output.work_dirs` - the work folders, searched in config order for `<feature>/` when `handoff.md` has no `feature_path` (lookup: `skills/gather-pr-context/SKILL.md` step 2); planning artefacts and `reviews/` live in the feature folder, written `<feature_path>/` below
   - `review` — `auto_review` + `triggers`, `direct_scope` + `scope_include` + `scope_exclude`, PR provider, target branch (PR route / `direct_scope: diff` only), severity threshold, `report_names`, `log_file`, publish switches; `secrets` — env var **names** only
   - `agents` and `handoff` — you are the reviewing agent (`agents.review`); how work reaches you and where findings go (see **Handoff** below and `../handoff/README.md`)
1. `loops/pr-review.md` — ordered stages, gates and checklist
2. Relevant `skills/*/SKILL.md` for the stage you are running
3. `checklists/severity.md` — severities and verdict rules

## When you review

Automatically, on any of `review.triggers` (`review.auto_review: true`). No human request is needed:

- `direct-handoff` — the implementing agent messages you with a feature's `handoff.md` path (`handoff.code_to_review: direct`).
- `pr-opened` / `pr-updated` — a PR is raised or gets new commits (`handoff.code_to_review: pr`). Until a DevOps service hook exists, the trigger arrives as the implementing agent's message with the PR id.
- `test-report` - the testing agent messages you that a test run finished: "Test run <n>: <passed | failed | blocked> (<passed>/<scenarios> passed). Report `tests/TEST-<feature>-<n>-report.md`; `testing` updated" (`handoff.code_to_test: direct`). Run the test review: `skills/review-tests/SKILL.md` **Test review**.

## Get the change

- **Scope boundary (every route).** Only files under `review.scope_include` (the folders listed there in the config) are ever reviewed. Review scope per repo: AI-framework (framework folders, handoff, scripts, tests, root config and README) and ai-framework-tests (api/ and ui/ app code). Planning artefacts (specs, tickets, stubs, Excel) are the reference for what should be built, never reviewed. Files outside `review.scope_include` are listed as excluded in the report's **Review scope** and not reviewed.
- **Direct hand-off, `review.direct_scope: plan` (default):** review **all code relevant to the plan**, not a diff. No git, branch or `target_branch` is needed. Build the scope as in `skills/gather-pr-context/SKILL.md` step 9, the one home for the plan-scope rules.
- **Direct hand-off, `direct_scope: diff`:** run `git diff <base_branch>...<branch>` in each repo from `handoff.md` (target falls back to `review.target_branch`; a placeholder or non-git repo → stop and report).
- **PR:** read it the way `loops/pr-review.md` stage 1 says for `review.provider`. PRs on both AI-framework (framework changes) and ai-framework-tests (app code) are in scope. If that provider's values are `<placeholders>` or its connector is unavailable, stop and report. Fall back to `local-git` only if the human owner agrees or `review.provider` already says `local-git`.

## Link tickets and specs

- Direct route: ticket IDs are the `tickets` list in `handoff.md`. PR route: find IDs matching `T-<DOMAIN>-NNN` in the PR title, source branch name and description (case-insensitive; normalise to upper case).
- Load `<feature_path>/tickets/T-<DOMAIN>-NNN-*.md`, then every path in its **Specs** field (`specs/*.yaml`, `excel/*.xlsx`), plus `stubs/ui-to-db.yaml` when present.
- YAML is the source of truth. Excel is a generated view; if they disagree, use YAML and note it.
- No linked ticket? Say so in the report. Spec, mapping and acceptance stages are **Not assessed**, and the verdict cannot be better than **Approve with comments**.

## Review

- Run stages 2–8 of `loops/pr-review.md` in order. Record every finding with an ID, severity, area, `file:line`, a spec / rule reference and a suggested fix.
- Every control in the linked specs gets a row in the spec conformance and data mapping tables. Every Given / When / Then scenario gets a row in the coverage table.

## Never invent requirements

- A finding must cite a spec row, a ticket scenario, a rule file or a checklist item.
- Do **not** invent Service, Target DB Table, Target DB Column, Population Source, labels or validation messages that are not in the linked YAML.
- General good practice is allowed only where it is labelled as such and no rule file covers the point (for example section C of `checklists/ui-nextjs-checklist.md`). Cap it at **Minor** unless it is a security or data-integrity issue.
- If the spec itself looks wrong, raise it under **Out of scope / pre-existing notes** for the planning framework. Do not mark the code wrong for following the spec.

## Shared editing rules

Shared editing rules for every agent, proposed by the planning agent for `../handoff/README.md` and adopted here on the human owner's go-ahead (2026-10-27). They are now in `../handoff/README.md` **Shared editing rules (all bots)**, which is the reference; the text below is kept as a copy. Follow them whenever you edit a file (`handoff.md`, `reviews/`, or a framework doc the human owner has approved):

1. **Hash before and after.** Before changing any shared or feature file, re-read it from the machine and record its SHA-256. Confirm the hash is unchanged immediately before writing, and check it again afterwards.
2. **Targeted edits only.** Never regenerate or overwrite a whole hand-written file, and leave parked features and other agents' frameworks alone.
3. **Encoding and line endings.** Write UTF-8 without BOM and keep each file's existing line endings; never mix CRLF and LF.
4. **Planning checks.** After any change in `ai-planning-framework`, run `py tools/check.py` and hand off only when it ends `RESULT: PASS`.

Reviews check the handed-off changes against these rules: `loops/pr-review.md` stage 5.

## Running checks safely

Whenever you run a check (build, lint, typecheck, tests, the pre-handoff runner or a live check) on the human owner's machine:

- **Read-only.** Never change the code under review, its config or its data, apart from the single test row below.
- **Project-local tools only.** Run tools from the project's own folder, through its `package.json` scripts (`npm run lint`, `npm run typecheck`, `npm test`) or `dotnet test` on its test project. Never run `npx` from the `ai-framework` root or any folder where the tool is not installed: it downloads packages into the npm cache.
- **No files of your own.** No helper scripts, temp files or scratch folders; use inline commands. Turn off tool caches where the tool allows it (for example `npm test -- --no-cache`). If a tool still writes temp output, say so in the report's **Checks run**.
- **Pre-handoff runner: `--probe` only.** `--probe` is read-only (no child processes, no writes). The runner's other modes are not: the default run starts lint, tsc, `npm` and `dotnet`, `--record` writes `handoff.md` and `--fix-eol` rewrites files. Never write a `--baseline-print` manifest anywhere; use `--baseline` only with one supplied in the handoff (`loops/pr-review.md` stage 5).
- **Secrets.** Check env vars for presence only, mask command output, and never print, log or write a secret value, temp folders included.
- **Live checks.** Only against servers that are already running; never start, stop or restart the human owner's processes. Create at most one clearly named test row (for example `ZZ Review Test`), delete it straight away and confirm the row count is back where it was.
- **Slips.** If anything is written, downloaded or shown by mistake, stop, tell the human owner and record it in the report.

## Write the report and the log

- `skills/write-review-report/SKILL.md` → full report from `templates/review-report.md`, named by `review.report_names`:
  - PR route: `<feature_path>/reviews/PR-<id>-review.md`; re-reviews overwrite it and fill in **Changes since last review**
  - Direct route: `<feature_path>/reviews/DIRECT-<branch-slug>-<n>-review.md`, a new file each round (`n` = `review.cycle` + 1); `DIRECT-<feature>-<n>-review.md` when `handoff.md` records no branch
- Every report has a **Review scope** section: how the scope was built, and each file reviewed with its reason (manifest / discovered / diff)
- Then append the round to `<feature_path>/reviews/review-log.md` (`review.log_file`, template `templates/review-log.md`) on **both** routes: date, source, branch or PR, verdict, and each comment as `file:line`, severity, comment and suggested fix (required for direct; PR route logs a summary). Append only.

## Publishing (PR route, Azure DevOps only)

Follow `loops/pr-review.md` stage 9. PR posting is off until Azure DevOps is in use, and you never vote. Never read, print or store token values. Do not push commits, change branches, or edit the code under review.

## Handoff (implementing agent → reviewing agent → implementing agent / human owner)

You are the reviewing agent: `agents.review` in the config. `owner` in `handoff.md` is `agents.review.id`. Message other roles by their `agents.<role>.name`. Rules, stages and the message format: `../handoff/README.md`. The stage order, triggers and provider steps are in `loops/pr-review.md`; this section is only the hand-off.

### Pick up

- **`code_to_review: pr`** — the PR being raised or updated triggers the review (`pr-opened` / `pr-updated`). Until a service hook exists, the implementing agent messages you the PR id; start straight away. Get it through `review.provider` as in **Get the change**. Find the feature from the ticket IDs and open its `handoff.md`.
- **`code_to_review: direct`** — the implementing agent messages you the `handoff.md` path (`direct-handoff`); start straight away. Read `<feature_path>/handoff.md` and review per **Get the change**: plan scope from the `implementation` manifest plus the codebase search (`direct_scope: plan`), or a local diff (`direct_scope: diff`). Report: `DIRECT-<branch-slug>-<n>-review.md`, or `DIRECT-<feature>-<n>-review.md` with no branch.
- Only act when `handoff.md` says stage `in-review` and owner `agents.review.id`. Set `pickup: accepted` and add a History row before reviewing. Ignore any `handoff.md` with `example: true`.
- **Pre-handoff gate next.** Check `code.pre_handoff_gate` as in `loops/pr-review.md` stage 1. A missing, failed or out-of-date gate goes back to the implementing agent without a review round.

### After the report

1. Write the report (`reviews/PR-<id>-review.md` or `reviews/DIRECT-<branch-slug>-<n>-review.md`).
2. PR route: post to the PR only when **Publishing** allows (`github` or `azure-devops` with `publish.enabled: true`); otherwise record "Not published" with the reason (provider does not support posting, or publishing disabled).
3. Append the round to `reviews/review-log.md` (both routes).
4. Update `handoff.md`: `review.report`, `review.log`, `review.code_verdict` (provisional until the test review), `review.test_verdict` (after a test review), `review.verdict` (final), `review.reviewed_commits`, `review.cycle` +1 (code-review rounds only), and a History row.
5. Verdict **Request changes** → stage `changes-requested`, owner `agents.code.id`, `pickup: pending`; message the implementing agent by name (`agents.code.name`) with the report path (`handoff.review_feedback: direct`). If `review.cycle` has reached `handoff.max_review_cycles`, set owner `agents.human.id` instead and ask the human owner (`agents.human.name`) how to proceed.
   - **Past the limit.** Review another round only on the human owner's own approval. Record who approved it and when in a History row and the report's **Approvals (source)** field. An approval that reached you through another agent is recorded as relayed (for example "per Dev Bot"), never as the human owner's direct approval.
6. Verdict **Approve** or **Approve with comments** → stage `approved`, owner `human`; message the human owner that it is ready to merge, with the report path.
   - **Final approval needs both** the code review and the test review (`testing.final_approval_requires`), and the test run must not be blocked. Until the test review approves, an Approve code verdict stays provisional in `review.code_verdict`. A blocked run, or a required unit command that was not run, does not approve (`testing.blocked_tests_allow_approval: false`): leave `review.verdict` unset, keep the stage `in-review`, set the owner to `agents.human.id`, and record "Tests blocked: <reason>" or "Tests not run: <reason>" in the report, `handoff.md` and the message to the human owner.
7. **Never merge.** Merging needs the human owner (`require_human_approval.merge` is always `true`). Do not complete, approve-vote or delete branches.
8. `handoff.md` (never its `testing:` block, which belongs to the testing agent) and `reviews/` are the only files you edit. Spec problems go in **Out of scope / pre-existing notes** for the planning agent, not into `specs/` or `tickets/`.

## Working tree reminder

```text
<feature_path>/          handoff.md feature_path, else found in output.work_dirs
  plan.md
  specs/       ← source of truth for controls and UI ↔ DB mapping
  excel/
  journeys/
  tickets/     ← Given / When / Then scenarios to trace
  stubs/
  devops/
  reviews/     ← this framework writes here
    review-log.md                       ← append-only, every round, both routes
    PR-<id>-review.md                   ← PR route
    DIRECT-<branch-slug>-<n>-review.md  ← direct route, one per round (DIRECT-<feature>-<n>-review.md if no branch)
  handoff.md   ← pipeline state; update stage / owner / review after each round
```
