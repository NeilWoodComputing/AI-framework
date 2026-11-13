# Agent brief — AI code framework (implementing agent)

Short instructions for the **implementing agent** (`agents.code` in `../ai-framework.config.yaml`; handoff id `dev-bot`), whichever agent builds features in this folder. The planning agent plans them (`../ai-planning-framework/`), the reviewing agent reviews them (`../ai-review-framework/`). How work moves between the three: `../handoff/README.md`.

## Read first

0. `../ai-framework.config.yaml` — shared config (paths relative to the `ai-framework` root):
   - `runtime` — which agent runtime performs the work. Resolve: user-preferences.yaml → per-role → shared default. **Verify correct runtime before work; if wrong, stop and hand off.**
   - `development.api.active` / `development.ui.active` — the **only** API and UI you build in; each option's `path`, `agent_docs`, `rules`, `skills`
   - `frameworks.code.rules` — shared rules (`.cursor/rules/`)
   - `output.work_dir` — where each `<feature>/` lives (specs, Excel, tickets, `handoff.md`)
   - `handoff` — your pick-up route (`plan_to_code`), your hand-off route (`code_to_review`), `branch_pattern`, `max_review_cycles` (code-review rounds only), `require_human_approval`; also `testing.max_test_fix_cycles` (failing-test fix loops — separate from review rounds)
   - `agents` — role → agent mapping: you are `agents.code`; message the planning agent, the reviewing agent and the human owner by their `agents.<role>.name`
   - `review.direct_scope` — what a direct review covers (`plan`: all code implementing the plan, from your `implementation` manifest; `diff`: a git diff)
   - `review.target_branch` — base branch, needed only for the PR route or `direct_scope: diff`; `tickets` — the board when the route is `devops`
1. `loops/feature-build.md` — ordered stages and gates for one feature
2. The active codebase's own docs and rules (below)
3. The feature's `handoff.md`, then its `tickets/`, `specs/` and `excel/`

If a value you need is still a `<placeholder>`, stop and report. Do not guess.

## Pick up work

- **`plan_to_code: direct`** — the planning agent messages you a feature path. Open `<work_dir>/<feature>/handoff.md`.
- **`plan_to_code: devops`** — take the work item from the board (`tickets.azure_devops` or `tickets.github`). Its title holds `T-<DOMAIN>-NNN`; find `<work_dir>/*/tickets/T-<DOMAIN>-NNN-*.md` and that feature's `handoff.md`. For GitHub Issues (`tickets.target: github`), the planning agent messages you an issue number and link; implement via a cloud agent, then open a PR with the cross-repo closing keyword `Closes NeilWoodComputing/ai-framework-tests#N` (or `Closes #N` when tickets and code are in the same repo). Run a daily sweep for missed issues if configured. Change board state only if the human owner has allowed it and the connector exists.
- Act only when `handoff.md` says owner `dev-bot` and stage `in-development` or `changes-requested`. Set `pickup: accepted`, `updated_at`, `updated_by` and add a History row before any code work.
- Ignore any `handoff.md` with `example: true`.
- A feature at `planned`, or waiting on `approvals.plan_to_code`, is not yours yet.

## Build against the active codebase

| Config | Read before coding |
|--------|--------------------|
| `development.api.active: unity-api` | `api/Unity.API/AGENTS.md`, `CLAUDE.md`, `.cursor/rules/` (index `README.md`), `.cursor/skills/`; run the slices with `.cursor/skills/unity-api-feature-loop/SKILL.md` |
| `development.api.active: api-framework` | `api/API.Framework/AGENTS.md`, `CLAUDE.md`, `.cursor/rules/` (index `README.md`), `.cursor/skills/`; shared `.cursor/rules/api-json-schema-forms.mdc` |
| `development.ui.active: nextjs` | `ui/UI.NextJs.Framework/AGENTS.md`, `README.md`, `.cursor/rules/` (index `README.md`; start with design-system). Copy the closest existing feature, e.g. `src/features/animals/manage-animals/` or `src/features/reference-data/reference-data-types-grid/`. A routed list page shows filters + results on the page; modals are only for create / edit forms and confirmations (`framework/nextjs-list-pages.mdc`). Angular rules are a reference for patterns only, not a standard to cite. |
| `development.ui.active: angular` | `ui/UI.Angular.Framework/CLAUDE.md`, `README.md`, `.cursor/rules/`, and the feature spec in `src/app/submodules/Example.Subrepo/README.md` |

Do not change code outside the active API and UI paths. If the work needs another codebase, stop and ask the human owner.

## Honour the specs

- **YAML specs are the contract.** Excel is a generated view; if they disagree, follow YAML and note it in `handoff.md`.
- Every control in the linked specs is rendered with the spec's label, control type, input format, mandatory, editable, enablement, min / max, validation rules and exact messages.
- Every control's data goes to its **Service / Target DB Table / Target DB Column**. Manage grids read their **Population Source**. Do not invent, rename or add columns; a missing mapping is a spec gap (below), not something to fill in.
- Every **Given / When / Then** scenario in the linked tickets is implemented (trace each scenario to code in the implementation manifest). Scenario tests are owned by the testing agent (`test-bot`), not by you.
- Scope is the tickets. Anything extra goes in **Notes for the next owner**, not into the code.

## Definition of done

All of these, before hand-off (details in `loops/feature-build.md`):

- [ ] Builds (API: `dotnet build` on the active solution `--configuration Release`; UI: `npm run build` when the change needs it)
- [ ] Pre-handoff checks pass: `node ai-code-framework/scripts/pre-handoff-checks.mjs --feature <work_dir>/<feature> --record <work_dir>/<feature>/handoff.md` (lint, typecheck, line endings / BOM, secrets, duplicate doc paragraphs, existing unit tests). Results in `code.verification`, `code.pre_handoff_gate: pass` and `code.pre_handoff_gate_at`. A failed or missing gate blocks hand-off (`../handoff/README.md` rule 12; `loops/feature-build.md` stage 5)
- [ ] Optimise pass done: Unity.API's **Framework compliance and cleanup** slice (when that is the active API), plus the same clean-up on UI files (no dead code, debug output, duplicate helpers or unused imports)
- [ ] Self-check against `../ai-review-framework/checklists/` — `full-stack-checklist.md`, the API checklist named by `api-checklist.md` for the active API, the active UI checklist (`ui-nextjs-checklist.md` or `ui-angular-checklist.md`) and `security-checklist.md`; fix what you find
- [ ] Every spec control and every Given / When / Then scenario accounted for in code (trace scenarios to code in the manifest; do **not** write scenario tests yourself)
- [ ] When a feature test plan requires them: scaffolding / reset keys / test users the plan needs exist (created by you). Do **not** create `Api.Framework.Tests`, Playwright suites, or a reset endpoint until Neil asks or a feature test plan needs those files listed. Manifest `tests` lists scaffolding only when present.
- [ ] `handoff.md` `code` section filled: repos, branch / base branch / head commit where the repo is under git, build / verification commands run
- [ ] `handoff.md` `implementation` manifest filled (see below); hand-off is blocked while it is empty

## Hand off (implementing agent → reviewing agent)

Branch: one per feature, named from `handoff.branch_pattern`, **the same name in every repo touched** (API and UI), containing the ticket ID. Commit with the ticket ID in the message. A branch is required for the PR route and for `direct_scope: diff`. With `direct_scope: plan` (the default) it is optional: use one in repos that are under git, and leave `branch` null in a repo that is not (e.g. UI.NextJs.Framework today).

**Implementation manifest.** Before every hand-off (including after changes requested), fill `implementation` in `handoff.md`: one entry per file that implements the plan, under `api`, `ui`, `tests` or `migrations`. That means files you created or changed, plus existing files the feature relies on to render a control or persist a mapping (`change: existing`). Each entry has its repo-relative `path` under the active API / UI path, `tickets`, and what it implements: `spec_pages`, `controls`, `db` (`Service:Table.Column`), and `scenarios` as code traces. Manifest `tests` lists scaffolding only when present (you create scaffolding when a test plan requires it; scenario tests belong to test-bot). Exclude build output, node_modules, bin/obj, generated files and secret / `.env` files. This is the starting point of the reviewing agent's plan-scope review. The reviewing agent also searches the codebase, and any relevant file you left out is a Minor "manifest incomplete" finding. **Do not hand off with an empty manifest.**

The review is automatic on both routes (`review.auto_review`). You never ask the human owner or anyone else to start a review, and `require_human_approval.code_to_review` is `false`, so you hand off without asking.

- **`code_to_review: direct`** — no PR needed. Fill the manifest; where a repo is under git, commit to the feature branch and record `branch` and `head_commit` (and `base_branch` when `direct_scope: diff`). Your message to the reviewing agent is the `direct-handoff` trigger. The reviewing agent reviews straight away, covering all code relevant to the plan (`direct_scope: plan`), or the git diff when `direct_scope: diff`.
- **`code_to_review: pr`** — needs `review.provider` configured with no placeholders and a way to raise PRs. Raise one PR per repo, title `[T-<DOMAIN>-NNN] <title>` (all ticket IDs it delivers), description listing ticket IDs, the feature path and the `handoff.md` path, target `base_branch`. Record each PR in `pull_requests`. Never set auto-complete. Raising or updating the PR is the trigger (`pr-opened` / `pr-updated`). Until a DevOps service hook exists, **also message the reviewing agent with the PR id** so the review starts.
- Then set `routes.code_to_review`, **`routes.code_to_test: direct`**, stage `in-review`, owner `review-bot`, `pickup: pending`, add a History row, and message the **reviewing agent** and the **testing agent** together (`agents.review.name` and `agents.testing.name`) with `../handoff/templates/handoff-message.md`. Stage and owner stay `in-review` / `review-bot` (test-bot is never an owner). **Never edit** the `testing` section of `handoff.md` — that belongs to test-bot.
- If the route is `pr` but a PR cannot be raised, stop and ask the human owner whether to hand off `direct`.
- (Only if the human owner ever sets `require_human_approval.code_to_review: true`: set owner `human` and get their approval before the hand-off. It is `false` by default.)

## Changes requested

1. The reviewing agent sets stage `changes-requested` and messages you the report path. Every round's comments (`file:line`, severity, comment, suggested fix) are also in `reviews/review-log.md`, and on the PR when publishing is on. **Code defects from a test review** also arrive this way: you fix the product code, not Test Bot's tests. If a test itself looks wrong, say so in the handback notes so Review Bot can route it to Test Bot.
2. Accept it in `handoff.md`, then fix every **Blocker** and **Major** finding (and Minor where cheap). Do not argue with a finding by changing the spec.
3. If a finding says the spec itself is wrong, that is the planning agent's call: spec gap (below).
4. Re-run build, the pre-handoff gate (`--record`) and self-check; commit to the **same** branch (or push to the same PR) where git is used; update `head_commit` and the `implementation` manifest; hand back with stage `in-review`, `routes.code_to_test: direct`, and message the reviewing agent **and** the testing agent. The re-review starts automatically (`direct-handoff`, or `pr-updated` plus your message with the PR id).

**Failing-test fix loops vs review rounds.** Fixes driven by failing or defective tests use `testing.max_test_fix_cycles` in `../ai-framework.config.yaml` (currently **5**). That counter lives on `handoff.md` `testing.test_fix_cycle` (owned by test-bot — **never edit the `testing` section**). These loops do **not** count toward `handoff.max_review_cycles` (currently **3** code-review rounds). `testing.failures_count_toward_review_cycles` is `false`. On exhaustion of the test-fix cap, escalate to Neil; do not burn a review round on a test-fix loop.

## Spec gap

If a ticket or spec is missing a mapping, contradicts itself, or cannot be built as written: add it to `blockers`, set stage `planned`, owner `plan-bot`, add a History row, and message the planning agent with the one-line gap. Do not edit `specs/`, `excel/` or `tickets/` yourself.

## Never

- **Never merge**, complete a PR, approve-vote, or delete a branch. Merging is the human owner's (`require_human_approval.merge`).
- Never push to or rewrite `review.target_branch`, force-push, or rewrite pushed history.
- Never read, print or store token values; the config only names env vars.
- Never run `git init` or change repo remotes without asking the human owner. An active folder that is not a git repo is fine for `code_to_review: direct` with `review.direct_scope: plan` (list its files in the manifest). It is a blocker only for the PR route or `direct_scope: diff`: record it in `blockers` and ask the human owner.
- Never edit another agent's framework (`ai-planning-framework/`, `ai-review-framework/`) apart from the feature's `handoff.md`.

## Working tree reminder

```text
ai-code-framework/
  AGENT-BRIEF.md            ← this file
  loops/feature-build.md    ← stages and gates for one feature
  .cursor/rules/            ← shared rules
  api/<active>/             ← development.api.active (its own AGENTS.md / CLAUDE.md / .cursor)
  ui/<active>/              ← development.ui.active (its own AGENTS.md / README / .cursor)

<work_dir>/<feature>/       ← the planning agent's artefacts (read-only for you)
  handoff.md                ← pipeline state; you update it at pick-up and hand-off
  reviews/review-log.md     ← every review round's comments (read on changes-requested)
  reviews/*-review.md       ← full review reports
```
