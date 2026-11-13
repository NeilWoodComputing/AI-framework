# Loop: pr-review

End-to-end review of one change: a **pull request** (`handoff.code_to_review: pr`) or a **direct hand-off** from the implementing agent (`handoff.code_to_review: direct`). **Primary outcome:** a report that says whether the PR renders the controls in the specs and writes their data to the right **Service / Target DB Table / Target DB Column**, to the standards of the active API and UI. Code standards, security and tests follow. A PR is reviewed on its diff. A direct hand-off is reviewed on its **plan scope**: the whole of every file that implements the feature's plan (`review.direct_scope: plan`, the default). Every round is appended to the feature's review log. PR comments are posted on GitHub (COMMENT event only) and Azure DevOps when publishing is enabled; on `cursor-origin` and `local-git` the report and the log are the whole output.

## When to run

Automatically, with no human request (`review.auto_review: true`), whenever one of `review.triggers` fires:

| Trigger | Route | Source of the change |
|---------|-------|----------------------|
| `direct-handoff` | `direct` | The implementing agent messages the reviewing agent with the feature's `handoff.md` path. Scope: plan scope from the `implementation` manifest plus a codebase search (`direct_scope: plan`), or `git diff <base_branch>...<branch>` (`direct_scope: diff`). |
| `pr-opened` | `pr` | A PR is raised against a branch in the active API or UI codebase (service hook, or the implementing agent's message with the PR id until one exists; see `../handoff/README.md`). |
| `pr-updated` | `pr` | New commits / iteration on a PR already reviewed. |
| `test-report` | testing (`handoff.code_to_test`) | The testing agent messages the reviewing agent: "Test run <n>: <passed \| failed \| blocked> (...). Report `tests/TEST-<feature>-<n>-report.md`; `testing` updated". Ready when `handoff.md` `testing.status` is `passed`, `failed` or `blocked` and `testing.report` / `testing.round` point at the new report. Run the **Test review** in `skills/review-tests/SKILL.md`, then stages 8, 10 and 11 |

Also re-run stages 2–4, 8 and 10 when the specs or tickets change after a review.

## Config first

Read `../ai-framework.config.yaml` (paths relative to the `ai-framework` root) before stage 1:

- Planning artefacts are in the feature folder: `handoff.md` `feature_path`, else the `<feature>/` found by searching `output.work_dirs` in config order (`skills/gather-pr-context/SKILL.md` step 2; stop and report if two folders match). Shown as `work/<feature>/` below
- Active API / UI folder, rules and agent docs come from `development`; shared rules from `frameworks.code.rules`
- Triggers from `review.auto_review` / `review.triggers`; route from `handoff.code_to_review`
- PR source comes from `review.provider` (`azure-devops` | `github` | `cursor-origin` | `local-git`) and its block (`review.azure_devops` / `review.github` / `review.cursor_origin` / `review.local_git`); default PR target from `review.target_branch`
- Role → agent names and `handoff.md` owner ids come from `agents` (you are `agents.review`)
- Direct-route scope from `review.direct_scope`: `plan` (default, no git or target branch needed) or `diff` (local `git diff <base_branch>...<branch>`, needs `review.target_branch` when `base_branch` is empty); the only reviewable folders from `review.scope_include` (API / UI code, every route); exclusions from `review.scope_exclude`
- Verdict threshold from `review.severity_threshold`; report names from `review.report_names`; log from `review.log_file`; publishing from `review.publish`
- If a value the current stage needs is still a `<placeholder>`, stop and report

## Ordered stages

```text
1. gather-pr-context           config, PR or handoff.md, review scope (PR diff | plan scope | local diff), tickets + specs, rules
        ↓
2. review-spec-conformance     controls on screen vs YAML / Excel
        ↓
3. review-data-mapping         Service / Target DB Table / Target DB Column honoured end to end
        ↓
4. review-acceptance-criteria  each Given / When / Then traced to code and tests
        ↓
5. review-code-standards       active API / UI rules from the config
        ↓
6. review-security-and-data    authZ, tenant scope, server-side validation, secrets, PII, injection, soft delete
        ↓
7. review-tests                tests for validation rules and scenarios; suggest missing ones
        ↓
8. write-review-report         scope, summary, tables, verdict → reviews/PR-<id>-review.md | DIRECT-<branch-slug|feature>-<n>-review.md
        ↓
9. publish                      inline + summary comments when review.publish allows (azure-devops, github); else record "Not published"; never a vote
        ↓
10. write-review-log           append the round to reviews/review-log.md (BOTH routes)
        ↓
11. hand back                  update handoff.md; message the implementing agent (changes) or the human owner (approved)
```

Stages 2–4 are the critical path. Stages 5–7 still run when no ticket is linked. Stages 8, 10 and 11 run on both routes; stage 9 posts only on the PR route with provider `azure-devops` (otherwise it just records why nothing was posted).

## Stage details

### 1. gather-pr-context

- Run `skills/gather-pr-context/SKILL.md`
- Every route: only files under `review.scope_include` enter the review scope. Specs, tickets and stubs are loaded as the reference, not reviewed; PR / diff files outside `review.scope_include` are listed as excluded
- Direct route: read `<feature_path>/handoff.md` (stage `in-review`, owner `agents.review.id`, not `example: true`): repos, tickets, the `implementation` manifest, and branch / head commit where present. Review round `n` = `review.cycle` + 1
  - `direct_scope: plan` (default): build the plan scope as in `skills/gather-pr-context/SKILL.md` step 9, the one home for the plan-scope rules. No git needed
  - `direct_scope: diff`: `git diff <base_branch>...<branch>` in each repo (target falls back to `review.target_branch`)
  - Round `n` 2 or later: scoped re-review, with a full pass on the final round (`skills/gather-pr-context/SKILL.md` step 9, item 7)
- Pre-handoff gate (every route, before any review work; `../handoff/README.md` rule 12): if `code.pre_handoff_gate` in `handoff.md` is not `pass`, or `code.pre_handoff_gate_at` is missing or earlier than the History row that handed the feature to `in-review`, send it back without a review round: no report, no review-log round and no `review.cycle` increment. Set stage `changes-requested`, owner `agents.code.id`, `pickup: pending`, add a History row giving the reason, and message the implementing agent by name
- PR route: PR metadata and diff from `review.provider`, read-only; find the feature's `handoff.md` from the linked ticket
  - `azure-devops`: Azure DevOps connector (token env var from `secrets.azure_devops_pat_env`)
  - `github`: a connected GitHub connector where available, else the token env var from `secrets.github_token_env`
  - `cursor-origin`: Cursor Origin connector for `review.cursor_origin.namespace` / `repository`, no token env var: pull request read (summary, files, commits), compare commits (`<target>...<source>` merge-base diff), get file contents (whole files / dependencies at the head ref), list commits. Never its write tools
  - `local-git`: `git diff <target>...<source>` in `review.local_git.repo_paths`; also covers a local clone of an Origin or GitHub repo
- Output: context pack — change metadata, **review scope** (each file with class and reason: diff / dependency / manifest / discovered; exclusions; not implemented / deferred items), linked tickets, spec control inventory, scenario list (`<ticket>/S<n>`), applicable rules
- Gate: every file in the review scope is under `review.scope_include`; nothing outside it is reviewed
- Gate: `code.pre_handoff_gate` is `pass` and up to date, or the hand-off was sent back without a review round
- Gate: PR route — PR id, source and target branch known; diff obtained
- Gate: direct route, `plan` — manifest read, codebase searched, scope listed with reasons; `diff` — branch and target known, diff obtained
- Gate: at least one ticket linked **or** the report states "No linked ticket" (stages 2–4 then **Not assessed**; verdict capped at Approve with comments)
- Gate: every linked ticket's Specs paths resolve; YAML loaded

### 2. review-spec-conformance (critical path)

- Run `skills/review-spec-conformance/SKILL.md`
- Output: one row per spec control (and per grid column / action) — Match / Mismatch / Missing / Extra / Not in PR (PR route) / Not implemented / Deferred (direct plan scope)
- Gate: every control in the linked specs has a row
- Gate: validation messages compared as exact strings

### 3. review-data-mapping (critical path)

- Run `skills/review-data-mapping/SKILL.md`, using `checklists/full-stack-checklist.md`
- Output: one row per control — UI binding → API record / DTO → mapper → entity or downstream model → table.column → migration
- Gate: every control's Service / Target DB Table / Target DB Column checked; unmapped, renamed or extra columns and missing migrations are findings
- Gate: grid Population Sources traced to list model fields

### 4. review-acceptance-criteria (critical path)

- Run `skills/review-acceptance-criteria/SKILL.md`
- Output: one row per scenario — Covered / Partial / Missing / Out of PR scope (PR route) / Deferred (ticket out-of-scope list), with code and test references
- Gate: every scenario in every linked ticket has a row

### 5. review-code-standards

- Run `skills/review-code-standards/SKILL.md` with the checklist `checklists/api-checklist.md` names for `development.api.active`, and the active UI checklist (`ui-nextjs-checklist.md` or `ui-angular-checklist.md`)
- Gate: each finding cites a rule file (or is labelled **General practice** when no rule covers the point)
- Shared editing rules (`AGENT-BRIEF.md` **Shared editing rules**; `../handoff/README.md` **Shared editing rules (all bots)**, the reference): check the handed-off changes for
  - encoding: UTF-8 without BOM, and no BOM added to a file that had none; evidence: the probe's `bom` and `utf8-invalid` results (below)
  - line endings: each file keeps its existing endings; no mixed CRLF / LF; evidence: the probe's `eol-mixed` result, and `eol-changed` as below
  - targeted edits: no whole-file rewrite or regeneration of a hand-written file
  - parked features (`parked: true`) and other agents' frameworks left untouched
  - SHA-256: before / after values recorded in `handoff.md`; when they are absent, report **Not verifiable**, not a finding
  - `ai-planning-framework` changes: evidence that `py tools/check.py` ended `RESULT: PASS`
- Probe evidence for encoding and line endings: from the `ai-framework` root run `node ai-code-framework/scripts/pre-handoff-checks.mjs --probe --json --target <api-framework | nextjs | all>` for the targets in `review.scope_include` (`--target nextjs --path <ui folder>` for another UI tree)
  - output is `{ file, rule, line }` only (`--json` adds summary counts); the allowlist is not applied, so use only findings on handed-off files; older findings elsewhere are not this round's
  - `bom` or `utf8-invalid` on a handed-off file: encoding finding; `eol-mixed`: line-endings finding
  - `eol-changed` needs `--baseline <file>`: use it only when a baseline manifest was supplied with the handoff (its path recorded in `handoff.md`). Never write a baseline (`--baseline-print` redirected to a file) into the human owner's repo, the framework or a temp folder. With no baseline, check changed endings by comparing the diff (a whole-file line-ending change shows every line changed), else report **Not verifiable**
  - `--probe` is read-only: it starts no child processes, writes nothing and refuses `--record` and `--fix-eol`. The other gate modes are not read-only: the default run starts lint, tsc, `npm` and `dotnet`, `--record` writes `handoff.md` and `--fix-eol` rewrites files. Reviewers run `--probe` only; the gate result itself comes from `code.pre_handoff_gate` (stage 1)
  - `open-redirect-sink` findings go to stage 6 as leads (`skills/review-security-and-data/SKILL.md` step 7)
  - record the command and result in the report's **Checks run**
- Gate: each shared editing rule has a result (Pass / Finding / Not verifiable / Not applicable)

### 6. review-security-and-data

- Run `skills/review-security-and-data/SKILL.md` with `checklists/security-checklist.md`
- Gate: every spec rule mentioning uniqueness, organisation / tenant scope or soft delete has been checked server-side

### 7. review-tests

- Run `skills/review-tests/SKILL.md`
- Output: tests found per validation rule and scenario; suggested missing tests with names and locations; the Execution table for the required unit commands
- Gate: every spec validation rule and every scenario has a test status
- Gate: the active API unit command (`testing.unit`) and the active UI unit command were run and recorded under **Checks run**. A failure, or a missing test project, is a Major finding for the implementing agent. A command that cannot be started is `not run` with a reason and withholds final approval (stage 11). Neither is a pass
- Test review (`test-report` trigger): `skills/review-tests/SKILL.md` **Test review**. A claimed scenario with no executed test that asserts the Then is a Major test defect (`review.test_verdict: request-changes`). A blocked run records `blocked-noted` and does not approve (`testing.blocked_tests_allow_approval: false`)

### 8. write-review-report

- Run `skills/write-review-report/SKILL.md`
- Artefact from `templates/review-report.md`, named by `review.report_names`:
  - PR route: `work/<feature>/reviews/PR-<id>-review.md` (overwritten on each PR update)
  - Direct route: `work/<feature>/reviews/DIRECT-<branch-slug>-<n>-review.md` (new file per round), or `DIRECT-<feature>-<n>-review.md` when `handoff.md` records no branch
- Gate: the **Review scope** section lists how the scope was built and every file reviewed with its reason (manifest / discovered / diff)
- Create `reviews/README.md` from `templates/reviews-folder-README.md` if the folder is new
- Gate: verdict follows `checklists/severity.md` and `review.severity_threshold`
- Gate: every finding has severity, area, `file:line`, reference and suggested fix

### 9. publish (PR route, GitHub and Azure DevOps)

- PR posting is supported on GitHub and Azure DevOps. This stage is the one home for the publishing rules; the other docs point here
- **GitHub:** Posts on a PR-route round, without anyone asking, when **all** of these hold: `review.provider` is `github` with no placeholders, `review.publish.enabled` is `true`, `review.publish.auto_post_on_pr` is `true` (the default), and the GitHub connector is available (or the token env var named in `secrets.github_token_env` is set). Posts use the COMMENT review event only, never APPROVE or REQUEST_CHANGES
- **Azure DevOps:** Posts when `review.provider` is `azure-devops` with no placeholders, `review.publish.enabled` is `true`, `review.publish.auto_post_on_pr` is `true`, the token env var named in `secrets.azure_devops_pat_env` is set (never read into the report or printed), and the DevOps connector is available
- `cursor-origin`, `local-git` → post nothing, even if `publish.enabled` is `true`; record "Not published — provider does not support posting" in the report footer and the log
- `post_inline_comments` → one comment per finding using `templates/review-comment.md`, anchored at `file:line`
- `post_summary_comment` → verdict + summary + link to the report path
- `set_vote` stays `false`: never approve, reject, complete or merge the PR. GitHub: COMMENT event only, never APPROVE or REQUEST_CHANGES
- Any other condition not met → post nothing and record in the report footer and the log why (e.g. "Not published — `review.publish.enabled` is false")
- Posted: record in the report footer and the log what was posted (date, inline count, summary yes / no, vote: none)
- Direct route: skipped (nothing to post to); the report and log are the output; record "Not applicable - direct hand-off" in the report footer
- Gate: the report (stage 8) and the log (stage 10) are written on every round, whatever the publish outcome

### 10. write-review-log (both routes)

- Run the **Review log** step of `skills/write-review-report/SKILL.md`
- Append one Round block to `work/<feature>/reviews/<review.log_file>` (default `review-log.md`) from `templates/review-log.md`, including its **Scope** line; create the file from the template on the first round
- Direct route: every finding as a Comments row (`file:line`, severity, comment, suggested fix)
- PR route: the round block and summary; Comments table optional
- Gate: append only; earlier rounds untouched; verdict and counts match the report

### 11. hand back

- Follow **Handoff** in `AGENT-BRIEF.md`: update `handoff.md` (`review.report`, `review.log`, `review.code_verdict`, `review.test_verdict`, `review.verdict`, `review.reviewed_commits`, `review.cycle` +1, stage, owner, History)
- Request changes → stage `changes-requested`, owner `agents.code.id`; message the implementing agent by name (`agents.code.name`) with the report path (review cap reached → owner `agents.human.id`, message the human owner, `agents.human.name`)
- Approve / Approve with comments → stage `approved`, owner `human`, only when the test review has also approved and the required unit commands passed. Message the human owner that it is ready to merge
- Final approval needs both the code review and the test review (`testing.final_approval_requires`), a test run that is not blocked, and a pass for each required unit command. `testing.status: blocked`, or a required unit command not run, leaves `review.verdict` unset, the stage `in-review` and the owner `agents.human.id`, with "Tests blocked: <reason>" or "Tests not run: <reason>" in the report and in the message to the human owner. Never edit `handoff.md` `testing:`
- Gate: nothing merged, completed or vote set

## Agent checklist (per loop)

- [ ] `../ai-framework.config.yaml` read; active API / UI, `review` and `handoff` settings noted
- [ ] Started automatically from a trigger (`direct-handoff`, `pr-opened`, `pr-updated`, `test-report`); no human request needed
- [ ] `test-report`: test review done; `review.code_verdict` and `review.test_verdict` recorded separately; final approval only when both approve and the run is not blocked; a missing or unexecuted scenario test is request-changes; `handoff.md` `testing:` untouched
- [ ] Active API and UI unit commands run and recorded; a failure or a missing test project is a Major finding; a command that cannot start withholds final approval
- [ ] Pre-handoff gate checked (`code.pre_handoff_gate: pass` and up to date); otherwise sent back with a History row and no review round
- [ ] PR route / `direct_scope: diff`: diff taken as `<target>...<source>` (or from the provider); reviewed commit recorded
- [ ] Direct `plan` scope: manifest + codebase search; discovered files flagged Minor; unimplemented controls / mappings raised; whole files reviewed; exclusions honoured
- [ ] Only files under `review.scope_include` reviewed; specs, tickets and stubs used as reference only
- [ ] Pre-existing issues unrelated to the plan kept in notes, outside the verdict
- [ ] Ticket IDs found and their specs loaded (or "No linked ticket" stated)
- [ ] Every spec control has a spec conformance row and a data mapping row
- [ ] Every Given / When / Then scenario has a coverage row
- [ ] No requirement, label, message or Service / Table / Column invented beyond the specs
- [ ] Code-standards findings cite a rule file, or are labelled General practice and capped at Minor
- [ ] Shared editing rules checked on the handed-off changes: no BOM, line endings kept and not mixed, targeted edits only, parked features and other agents' frameworks untouched, SHA-256 before / after recorded (else **Not verifiable**), `py tools/check.py` ended `RESULT: PASS` for `ai-planning-framework` changes; encoding and line endings evidenced by `--probe --json` (`eol-changed` only with a handed-off baseline, else by diff or **Not verifiable**; no baseline file written)
- [ ] Uniqueness, tenant scope and soft-delete rules checked server-side
- [ ] Verdict follows `checklists/severity.md`
- [ ] Report (with **Review scope**) written to `work/<feature>/reviews/PR-<id>-review.md` or `DIRECT-<branch-slug|feature>-<n>-review.md`
- [ ] PR route: comments posted on `github` (COMMENT event only) or `azure-devops` when every publish condition is met (else "Not published" recorded); never a vote or blocking review state
- [ ] Round appended to `work/<feature>/reviews/review-log.md`
- [ ] `handoff.md` updated and the implementing agent (or the human owner) messaged

## Working folder convention

```text
work/<feature-slug>/
  plan.md
  specs/
  excel/
  journeys/
  tickets/
  stubs/
  devops/
  reviews/
    review-log.md   # append-only history of every round, both routes
    PR-<id>-review.md                  # PR route; overwritten on each PR update
    DIRECT-<branch-slug>-<n>-review.md # direct route; one per round (DIRECT-<feature>-<n>-review.md if no branch)
  handoff.md        # pipeline state; the reviewing agent updates it in stage 11
```

`work/<feature>/` stands for the feature folder: `handoff.md` `feature_path`, else found in `output.work_dirs` (`../ai-framework.config.yaml`).
