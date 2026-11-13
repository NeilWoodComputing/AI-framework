# Loop: feature-build

End-to-end build of one planned feature by the **implementing agent** (`agents.code`). **Primary outcome:** the controls in the specs render as specified, and their data reaches the right **Service / Target DB Table / Target DB Column** in the active API and UI, with every Given / When / Then scenario working and tested. Then hand off for review.

Brief: `../AGENT-BRIEF.md`. Pipeline rules: `../../handoff/README.md`.

## When to run

`<work_dir>/<feature>/handoff.md` says stage `in-development` (new work) or `changes-requested` (fixes), owner `dev-bot`.

## Config first

Read `../../ai-framework.config.yaml` (paths relative to the `ai-framework` root) before stage 1:

- Build only in `development.api.active` and `development.ui.active` paths, using their `agent_docs`, `rules` and `skills`, plus `frameworks.code.rules`
- Feature artefacts are under `output.work_dir/<feature>/` (shown as `work/<feature>/` below)
- Routes, branch naming, review cap and gates from `handoff` (`max_review_cycles` = code-review rounds only); what a direct review covers from `review.direct_scope`; base branch from `review.target_branch` (PR route or `direct_scope: diff` only)
- If a value a stage needs is still a `<placeholder>`, stop and report


### Test-fix loops (separate from review rounds)

When Test Bot reports failing or defective tests and you are sent back to fix **product code**, those fix loops are capped by `testing.max_test_fix_cycles` in `../../ai-framework.config.yaml` (currently **5**). Counter: `handoff.md` `testing.test_fix_cycle` (test-bot writes it — **never edit the `testing` section**). They do **not** consume `handoff.max_review_cycles` (currently **3**). Config: `testing.failures_count_toward_review_cycles: false` (Neil, 2026-10-08). Exhaustion → escalate to Neil; do not treat a test-fix loop as a review round.

## Ordered stages

```text
1. pick-up          handoff.md (direct) or board item (devops) → pickup: accepted
        ↓
2. branch           feature branch per git repo, same name, contains T-<DOMAIN>-NNN (optional for direct_scope: plan)
        ↓
3. implement-api    active API; C# API → its own feature loop (slices)
        ↓
4. implement-ui     active UI; controls + bindings per spec
        ↓
5. tests + gate     build, then the pre-handoff checks (runner records the result); scaffolding only when a test plan requires it (scenario tests = test-bot)
        ↓
6. optimise         compliance and clean-up on every touched file; re-run stage 5 (last gate run is the one recorded)
        ↓
7. self-review      ai-review-framework checklists; fill the implementation manifest
        ↓
8. handoff          manifest not empty + code.pre_handoff_gate: pass → code_to_review + code_to_test: direct → stage in-review, owner review-bot; message Review Bot and Test Bot
```

Skip stage 3 or 4 only when the tickets have no API or no UI work, and say so in `handoff.md`.

## Stage details

### 1. pick-up

- `direct`: open `work/<feature>/handoff.md`. `board` (or the `devops` alias): find the ticket ID in the work item or issue title (GitHub issue or Azure DevOps), then the feature's `handoff.md`. For GitHub Issues, use the cross-repo closing keyword `Closes owner/repo#N` in the PR when tickets and code are in different repositories.
- Load every ticket in `tickets`, every path in each ticket's **Specs** field (`specs/*.yaml`, `excel/*.xlsx`) and `stubs/ui-to-db.yaml` if present
- Build a control inventory (per control: section / step, label, type, mandatory, editable, enablement, min / max, validation + messages, Service / Table / Column) and a scenario list (`<ticket>/S1`, `S2`, …)
- On `changes-requested`: also load `review.report` (and the latest round in `review.log`, `reviews/review-log.md`) and list its findings by ID. If the handback is from a **test** failure / test-review code defect, also note `testing.test_fix_cycle` vs `testing.max_test_fix_cycles` (does not increment review cycle)
- Gate: owner is `dev-bot`; `example` is not `true`; `approvals.plan_to_code` is recorded when it was required
- Gate: every control has Service / Table / Column (or Population Source). If not → spec gap, stop
- Write: `pickup: accepted`, History row

### 2. branch

- Name from `handoff.branch_pattern` (`direct` or `board` form; `devops` is an alias of `board`); the same name in the API and UI repo; base = `code.<repo>.base_branch`, else `review.target_branch`
- On `changes-requested`, keep the existing branch
- Required for the PR route and `direct_scope: diff`: base branch is not a placeholder and each repo is a git repo (else blocker → ask the human owner)
- `direct_scope: plan`: branch in every repo that is under git; a repo that is not under git (e.g. UI.NextJs.Framework) is not a blocker. Leave its `branch` null and rely on the manifest
- Gate: do not stash, reset or discard someone else's uncommitted changes. If the repo has unrelated local changes, stop and ask the human owner
- Write: `code.<repo>.branch`, `base_branch`

### 3. implement-api

- `csharp-api`: follow the active C# API's feature loop skill. It owns the slice list, its state file (`.cursor/loops/{feature}.md` from `loop-state.template.md`), the iteration limit and the stop conditions. Do not duplicate it here.
- `api-framework`: follow `../api/API.Framework/CLAUDE.md` and `../.cursor/rules/api-json-schema-forms.mdc`
- Map every control to its Service / Target DB Table / Target DB Column: record / DTO → mapper → entity or downstream model → table.column, plus a migration when a BFF-owned table changes
- Server-side validation for every spec rule (mandatory, min / max, format, uniqueness, tenant scope, soft delete) with the spec's exact messages
- Gate: every control in the inventory is reachable through the API, or noted as out of this ticket's scope

### 4. implement-ui

- `nextjs`: follow `../ui/UI.NextJs.Framework/README.md`; copy the nearest existing feature (grids: `src/features/reference-data/reference-data-types-grid/`); call the active API through `systemApiFetch` and `src/config/` routes
- `angular`: follow `../ui/UI.Angular.Framework/CLAUDE.md`, `.cursor/rules/` and the submodule feature spec
- Render each control in spec order with the spec's label, type, mandatory, editable / enablement, conditional visibility and messages; bind to the API property that maps to its column
- Manage grids: one column per Population Source, plus the primary action and actions menu from the spec
- Gate: every control and grid column in the inventory is rendered, or noted as out of this ticket's scope

### 5. tests + pre-handoff checks

- API (`csharp-api`): the Verify section of the C# API feature loop (`dotnet build` on the solution, then targeted `dotnet test` when that loop requires it)
- API (`api-framework`): `dotnet build Api.Framework.sln --configuration Release`. Scenario tests are owned by test-bot (`[Trait("Scenario", "T-…/S<n>")]`); add `Api.Framework.Tests` scaffolding only when Neil asks or a feature test plan needs those files listed
- UI (`nextjs`): `npm run build` when the change needs it. Lint, typecheck and the Vitest unit tests (`npm test`) run in the gate below
- **Pre-handoff gate** (config `verification`; `../../handoff/README.md` rule 12). After the build, from the `ai-framework` root:

  ```powershell
  node ai-code-framework/scripts/pre-handoff-checks.mjs --feature <work_dir>/<feature> --record <work_dir>/<feature>/handoff.md
  ```

  Checks per target the `implementation` manifest touches (every target while the manifest is empty); `secrets` always runs on both:

  | Check | api-framework | nextjs | Fails on |
  |-------|---------------|--------|----------|
  | `lint` | - | `npm run lint` (`eslint .`, flat config; `e2e/` excluded) | any error; warnings counted, not failed (D3) |
  | `typecheck` | - | `npm run typecheck` (`tsc --noEmit`) | any error |
  | `eol` | CRLF | LF (`*.ps1` / `*.cmd` / `*.bat` CRLF) | wrong or mixed endings, no final newline, BOM (each target's `.editorconfig`) |
  | `secrets` | yes | yes (including `e2e/`) | a non-empty credential in config, code literals or docs; prints file:line + key only |
  | `docs-dup` | yes | yes | a paragraph of 25+ words repeated in the target's README / AGENTS / CLAUDE / docs / rules |
  | `unit` | `dotnet test Api.Framework.Tests` | `npm test` (Vitest) | any failing test |

- Fix every failure. Allowlist only with a reason and an expiry in `scripts/pre-handoff-allowlist.json` (never a value; a real credential needs the human owner's OK). Never allowlist to get past a real finding
- Do **not** add Given / When / Then scenario tests yourself. Trace each scenario to code in the implementation manifest. When a feature test plan requires scaffolding, reset keys or test users, create those; leave scenario authoring and runs to test-bot
- Gate: build passes **and** the pre-handoff gate passes (exit 0). Failures that survive 3 attempts are blockers: record them in `blockers`, naming the failing checks, and do not hand off
- Write: `code.build`, `code.tests` (scaffolding status or "none — scenario tests = test-bot"), `code.verification` (build commands; `--record` adds one `pre-handoff:` line per check and keeps the others), `code.pre_handoff_gate` / `code.pre_handoff_gate_at` (written by `--record`). Never a secret value
### 6. optimise

- C# API: the mandatory **Framework compliance and cleanup** slice of its feature loop
- UI and anything else touched: remove dead code, debug output, commented-out code, unused imports and duplicate helpers; reuse existing framework components instead of new ones
- Re-run stage 5 after changes (build + pre-handoff gate with `--record`); the last run before stage 8 is the one recorded in `handoff.md`
- Gate: no new warnings you introduced (compare the lint warning count with the previous gate run); build and gate still pass

### 7. self-review

- Walk `../../ai-review-framework/checklists/full-stack-checklist.md` for every control, then the API checklist named by `api-checklist.md` for the active API, the active UI checklist (`ui-nextjs-checklist.md` or `ui-angular-checklist.md`) and `security-checklist.md`
- Trace each scenario to code and test
- On `changes-requested`: confirm each finding in the report is fixed or answered
- Fill the `implementation` manifest in `handoff.md`, with one entry per file that implements the plan under `api`, `ui`, `tests` or `migrations`. Use repo-relative paths under the active API / UI path. Each entry gives `change` (added / modified / existing), `tickets`, `spec_pages`, `controls`, `db` (`Service:Table.Column`) and `scenarios` as code traces; `tests` = scaffolding only when present. Exclude build output, node_modules, bin/obj, generated files and secret / `.env` files
- Check the manifest against the control inventory: every spec control and DB mapping is covered by at least one entry, or is deferred by the ticket's out-of-scope list
- Gate: nothing you would expect the reviewing agent to rate Blocker or Major is left
- Gate: manifest filled and matching the control inventory

### 8. handoff

- Gate: **`implementation` is not empty.** If every list is empty, do not hand off; go back to stage 7
- Gate: **`code.pre_handoff_gate: pass`** from the last stage 5 run, after any stage 6 / 7 change. Missing or `fail`: do not hand off; go back to stage 5 (the reviewing agent returns a hand-off without it, no review round)
- Where a repo is under git: commit with ticket IDs in the message; record `head_commit`
- No approval needed by default (`require_human_approval.code_to_review: false`); the review starts automatically, so never ask anyone to request one
- `pr`: one PR per repo, title `[T-<DOMAIN>-NNN] <title>`, description with ticket IDs + feature path + `handoff.md` path; record `pull_requests`. The PR opening / updating triggers the review; until a DevOps service hook exists, your message with the PR id is what starts it
- `direct`: no PR; your message is the `direct-handoff` trigger. With `direct_scope: plan` the reviewing agent reviews the whole of every file that implements the plan, starting from your manifest, and needs no git. With `direct_scope: diff` it diffs `base_branch...branch`
- Set `routes.code_to_review`, **`routes.code_to_test: direct`**, stage `in-review`, owner `review-bot`, `pickup: pending`, History row; then message the reviewing agent **and** the testing agent (`agents.review.name` and `agents.testing.name`; `../../handoff/templates/handoff-message.md`). Stage/owner stay in-review/review-bot. Never edit the `testing` section
- Gate: never merge, auto-complete or push to the base branch

## Stop

Stop and report (keeping ownership, with the reason in `blockers`, and messaging the human owner) when:

- a spec gap is found → hand back to the planning agent instead (stage `planned`, owner `plan-bot`)
- a config value is a placeholder, a repo is not under git when the route needs git (PR route or `direct_scope: diff`), or a downstream contract / UI route is missing
- the C# API feature loop hits its own stop condition (iteration limit, same failure 3 times)
- the work needs a codebase other than the active API / UI

## Agent checklist (per loop)

- [ ] Config read; active API / UI, `handoff` and base branch noted
- [ ] `handoff.md` accepted (owner `dev-bot`, not an example, plan approval recorded when required)
- [ ] Control inventory and scenario list built from YAML specs and tickets
- [ ] Same branch name in every git repo, containing the ticket ID (required for PR / `direct_scope: diff`)
- [ ] Every control's Service / Target DB Table / Target DB Column honoured; nothing invented
- [ ] Every Given / When / Then scenario implemented and traced to code in the manifest (scenario tests = test-bot; scaffolding only when a test plan requires it)
- [ ] Build and tests pass; optimise pass done; self-review against the review checklists done
- [ ] Pre-handoff gate re-run after the last change and passed (`scripts/pre-handoff-checks.mjs --record`); `code.verification` lines and `code.pre_handoff_gate: pass` / `_at` in `handoff.md`
- [ ] `implementation` manifest filled (api / ui / tests / migrations, with tickets and spec pages / controls / DB columns); not empty
- [ ] `handoff.md` updated (code section, manifest, route, stage, owner, History) before messaging the reviewing agent
- [ ] Nothing merged, auto-completed or force-pushed

## Working folder convention

```text
work/<feature-slug>/          ← output.work_dir; the planning agent's artefacts are read-only for you
  handoff.md                  ← you update code / implementation manifest / routes / stage / owner / History
  tickets/  specs/  excel/  stubs/
  reviews/
    review-log.md             ← every review round, both routes (read on changes-requested)
    *-review.md               ← full reports: PR-<id>-review.md / DIRECT-<branch-slug>-<n>-review.md

ai-code-framework/api/<active>/   ← code changes (API)
ai-code-framework/ui/<active>/    ← code changes (UI)
```
