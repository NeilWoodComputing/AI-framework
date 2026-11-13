# AI review framework

Skills, a loop, checklists and report templates that the **reviewing agent** uses to review a change automatically: a pull request when it is raised or updated, or a direct hand-off from the implementing agent. Any agent can take the reviewing role: `agents.review` in the config says which agent fills it today (roles: `../handoff/README.md`, and `AGENT-BRIEF.md` → **Using this framework as any reviewing agent**). **Primary question:** does the change build what the planning specs say — the right controls on screen, and the data landing in the right **Service / Target DB Table / Target DB Column** — to the standards of the active API and UI codebases?

The review never edits the code under review. It writes a full report and appends the round to `reviews/review-log.md`, next to the feature's planning artefacts. PR posting is off until Azure DevOps is in use: inline and summary comments are only ever posted when `review.provider` is `azure-devops` and `review.publish.enabled` is `true` (see **Publishing**). On `github`, `cursor-origin` and `local-git` the review is the report plus the review log only. It never votes, approves or merges.

## Review scope

| Route | What is reviewed |
|-------|------------------|
| PR (`handoff.code_to_review: pr`) | The PR diff, plus the unchanged files it depends on |
| Direct, `review.direct_scope: plan` (default) | **All code relevant to the plan**, from the implementing agent's `implementation` manifest plus a codebase search, every file read whole. No git or target branch needed. The rules: `skills/gather-pr-context/SKILL.md` step 9 |
| Direct, `direct_scope: diff` | Local `git diff <base_branch>...<branch>` in each repo (the old behaviour) |

**Only API / UI code is reviewed.** On every route (PR, direct `plan`, direct `diff`) a file is in scope only if it is under a `review.scope_include` folder: `ai-code-framework/api/` or `ai-code-framework/ui/`, the folders holding the `development.api` / `development.ui` codebases. A PR or diff file outside them is listed as excluded and not reviewed. Planning artefacts (`specs/`, `tickets/`, `stubs/`, `excel/`) are read as the reference for what should be built, but are never reviewed themselves. Framework docs, shared rules (`frameworks.code.rules`, read as reference only), `ai-framework.config.yaml` and anything else outside those folders are never in scope. The report and review log are still written to the feature's `reviews/` folder.

`review.scope_exclude` keeps build output, node_modules, bin / obj, generated files and secrets / `.env` files out of every scope. Each report has a **Review scope** section listing how the scope was built and why each file is included.

## When to run

Automatically, on `review.triggers` (`review.auto_review: true`). The trigger table, the stage order and what each stage writes are in `loops/pr-review.md`. Every round is appended to `reviews/review-log.md`. The review comes before the human owner's merge decision. A human still owns the merge.

## Config first

Read `../ai-framework.config.yaml` (paths relative to the `ai-framework` root) before anything else:

| Config key | Used for |
|------------|----------|
| `development.api.active` / `development.ui.active` | Which codebase's rules, agent docs and skills the code-standards stage applies |
| `frameworks.code.rules` | Shared cross-codebase rules |
| `output.work_dirs` + `output.feature_layout` | Finding the feature folder (`handoff.md` `feature_path` first, else `output.work_dirs` in config order; `skills/gather-pr-context/SKILL.md` step 2), where `specs/`, `excel/`, `tickets/`, `stubs/` are and `reviews/` is written |
| `review.auto_review` / `review.triggers` | Start automatically on `pr-opened`, `pr-updated`, `direct-handoff`, `test-report` |
| `handoff.code_to_review` | Route: `direct` (scope from `review.direct_scope`) or `pr` (PR diff) |
| `review.direct_scope` / `review.scope_include` / `review.scope_exclude` | Direct-route scope: `plan` (all code implementing the plan, default) or `diff`; the only folders ever reviewed (API / UI code, every route); what never enters any scope |
| `review.provider` | How to get the PR: `azure-devops`, `github`, `cursor-origin` (Cursor Origin connector, no token) or `local-git` (`git diff <target>...<source>`). See **PR providers** |
| `review.azure_devops` / `review.github` / `review.cursor_origin` / `review.local_git` | Settings for the chosen provider (`cursor_origin`: Origin `namespace` + `repository`) |
| `review.target_branch` | Target branch when the PR does not state one; also the fallback base for `direct_scope: diff`. Not used by `direct_scope: plan` |
| `review.severity_threshold` | Lowest severity that forces **Request changes** (default `major`) |
| `review.report_names` / `review.log_file` | Report file name per route; the per-feature review log (`review-log.md`) |
| `review.publish` | Whether comments are posted to the PR: only ever on `azure-devops`, with `enabled: true` (default `false`, off until Azure DevOps is in use; `auto_post_on_pr`); `set_vote` stays `false` |
| `secrets` | Environment variable **names** only (`AZURE_DEVOPS_PAT`; `GITHUB_TOKEN` only when no GitHub connector is connected). `cursor-origin` needs none |
| `agents` | Role → agent mapping. You are `agents.review`; `agents.code` is the implementing agent, `agents.human` the human owner; each `id` is the `owner` value in `handoff.md` |

If a value the review needs is still a `<placeholder>`, stop and report — do not guess.

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| PR metadata (id, title, description, source and target branch, commit / iteration) | PR route: provider from `review.provider` (Azure DevOps or GitHub connector, Cursor Origin connector), or the PR id in the implementing agent's message for `local-git` | PR route |
| Hand-off (repos, tickets, `implementation` manifest; branch / head commit where under git) | Direct route: `<feature_path>/handoff.md` | Direct route |
| Files to review | PR route: provider diff (`cursor-origin`: the connector's PR files view / compare commits, whole files via get file contents) or `git diff <target>...<source>`. Direct `plan`: manifest + codebase search, whole files. Direct `diff`: `git diff <base_branch>...<branch>`. Every route: only files under `review.scope_include` | Yes |
| Linked tickets | Direct route: `handoff.md` `tickets`. PR route: `T-<DOMAIN>-NNN` found in PR title, branch name or description → `<feature_path>/tickets/` | Yes (see gate in the loop) |
| Page specs | YAML under `<feature_path>/specs/` (source of truth); Excel under `excel/` is a generated view | Yes |
| UI ↔ DB stubs | `<feature_path>/stubs/ui-to-db.yaml` | No |
| Rules | Active API / UI `rules` and `agent_docs` from the config, plus `frameworks.code.rules` | Yes |

## Outputs

Written to the feature's `reviews/` folder on every round:

```text
<feature_path>/reviews/
  review-log.md                        ← append-only history of every round, both routes (review.log_file)
  PR-<id>-review.md                    ← PR route: one per PR, overwritten on each PR update
  DIRECT-<branch-slug>-<n>-review.md   ← direct route: one per round (DIRECT-<feature>-<n>-review.md if no branch)
```

- `<feature>` is the folder of the first linked ticket. Other linked features are listed in the report header.
- `<id>` is the provider's PR number. `<branch-slug>` is the branch with `/` replaced by `-`; with no branch recorded (e.g. a non-git UI on the plan scope) the feature slug is used instead. `<n>` is the review round (`handoff.md` `review.cycle` + 1).
- `review-log.md` gets one Round block per review: date, source (direct or PR), branch or PR, scope, verdict, and each comment as `file:line`, severity, comment and suggested fix (required on the direct route; the PR route logs a summary). Template: `templates/review-log.md`.
- If no ticket can be linked, write to `ai-planning-framework/work/_unlinked/reviews/` and say so in the report.
- When creating a feature's `reviews/` folder for the first time, copy `templates/reviews-folder-README.md` into it as `README.md`.
- PR re-reviews overwrite the same report. The header records the reviewed commit and iteration number.

The report follows `templates/review-report.md`. Inline comments (Azure DevOps PR route only, when publishing is enabled) follow `templates/review-comment.md`.

After each round the reviewing agent updates the feature's `handoff.md` and messages the implementing agent (changes requested) or the human owner (approved), by the names in `agents`. See `AGENT-BRIEF.md` → **Handoff**.

## PR providers

`review.provider` says where the PR route reads a pull request. Every provider is read-only. The provider steps, credentials and what may be posted live in `loops/pr-review.md` stage 1 and stage 9. A placeholder, or a connector that is unavailable, means stop and report.

## How it uses the planning artefacts

The planning framework (`../ai-planning-framework/`) defines **what should be built**. This framework checks the PR or direct hand-off against it:

| Planning artefact | Review stage |
|-------------------|--------------|
| `specs/*.yaml` control rows (label, control type, mandatory, editable, enablement, min/max, validation rules and messages) | 2 — spec conformance |
| `specs/*.yaml` Service / Target DB Table / Target DB Column and grid Population Source | 3 — data mapping |
| `tickets/T-<DOMAIN>-NNN-*.md` Given / When / Then scenarios | 4 — acceptance criteria, 7 — tests |
| Active API / UI rules from the config | 5 — code standards |
| Spec validation rules such as uniqueness per organisation, soft delete | 6 — security and data |

**Never invent requirements.** A finding must cite a spec row, a ticket scenario, a rule file or a checklist item. General good practice is allowed only where it is labelled as such and no rule file covers the point (for example the React / Next.js items in section C of `checklists/ui-nextjs-checklist.md`), and it is capped at **Minor** unless it is a security or data-integrity issue.

## Severity and verdict

Defined in `checklists/severity.md`. In short:

- **Blocker** — wrong or missing DB mapping, missing mandatory control, missing migration, cross-tenant data exposure, committed secret
- **Major** — spec or acceptance behaviour not met, server-side validation missing, untested Given / When / Then scenario that the PR claims to deliver
- **Minor** — deviation from codebase rules, small spec text differences, missing non-critical tests
- **Nit** — style and naming that does not affect behaviour

Verdict: any Blocker, any unmet mandatory spec control or DB mapping, or any finding at or above `review.severity_threshold` → **Request changes**. Otherwise Minor findings → **Approve with comments**; nothing above Nit → **Approve**. That code verdict stays provisional until the test review.

Stage 7 runs the active API unit command (`testing.unit`) and the active UI unit command, and records both under **Checks run**. A failure, or a missing test project, is Major. A command that cannot be started is not a pass. Final approval also needs a test review in which every scenario the change claims was executed and asserts its Then. A blocked test run does not approve (`testing.blocked_tests_allow_approval: false`): the stage stays `in-review` and the owner is the human owner.

## Layout

```text
ai-review-framework/
  README.md
  AGENT-BRIEF.md                 ← start here (reviewing agent)
  loops/
    pr-review.md                 ← ordered stages, gates, checklist
  skills/
    gather-pr-context/
    review-spec-conformance/
    review-data-mapping/
    review-acceptance-criteria/
    review-code-standards/
    review-security-and-data/
    review-tests/
    write-review-report/
  checklists/
    severity.md
    full-stack-checklist.md
    api-checklist.md             ← which API checklist to open
    api-unity-checklist.md       ← when development.api.active is unity-api
    api-framework-checklist.md   ← when development.api.active is api-framework
    ui-nextjs-checklist.md
    ui-angular-checklist.md
    security-checklist.md
  templates/
    review-report.md
    review-comment.md
    review-log.md                ← per-feature append-only log of review rounds
    reviews-folder-README.md
  examples/
    sample-review.md             ← illustrative only (a Library-domain page; not a real review)
  tools/
    check.py                     ← one command that verifies this framework (see tools/README.md)
```

## Publishing (PR route, Azure DevOps only)

The publishing rules live in one place, `loops/pr-review.md` stage 9: PR posting is off until Azure DevOps is in use, and agents never vote, approve or merge.
