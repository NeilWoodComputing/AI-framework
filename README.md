# ai-framework

Four frameworks that work together to plan, build, test and review full-stack features: **what renders on screen** and **where that data lives in the database**.

| Folder | Role |
|--------|------|
| `ai-planning-framework/` | Skills and loops that turn a feature into a plan, UI ↔ DB page specs (YAML + Excel), user journeys, Given / When / Then tickets and framework-agnostic stubs. Start with its `AGENT-BRIEF.md`. |
| `ai-code-framework/` | Reference API (`api/`) and UI (`ui/`) codebases, each with its own rules and skills, plus shared rules in `.cursor/rules/`. |
| `ai-review-framework/` | Skills and a loop that review a raised PR against the planning specs (controls and Service / Table / Column), the Given / When / Then tickets and the active API/UI rules, then write `reviews/PR-<id>-review.md`. Start with its `AGENT-BRIEF.md`. |
| `ai-test-framework/` | Skills and a loop that turn each ticket's Given / When / Then scenarios (by explicit ID `<ticket>/S<n>`) into unit and e2e tests, run them against a dedicated test environment and write `tests/TEST-<feature>-<n>-report.md`. Runs alongside the review. Start with its `AGENT-BRIEF.md`. |
| `handoff/` | How a feature moves between the agents: pipeline, stages, rules, and the `handoff.md` / message templates. Start with `handoff/README.md`. |
| `ai-framework.config.yaml` | Shared configuration: framework paths, agents, handoff routes and gates, testing, active API/UI folder, output folder and ticket target. |

## Agents: read the config first

Before running any skill or loop, read `ai-framework.config.yaml`:

- `development` — which API and UI folder is the active target (`active:` picks one option each)
- `output.work_dir` — where per-feature artefacts are written (`<work_dir>/<feature>/plan.md`, `specs/`, `excel/`, `journeys/`, `tickets/`, `stubs/`, `tests/`, `reviews/` incl. `reviews/review-log.md`, and `handoff.md`)
- `tickets` — where stories are published (Azure DevOps). If `enabled` is `false` or any value is still a `<placeholder>`, stop and report; do not guess.
- `review` — automatic reviews (`auto_review`, `triggers`: PR opened / updated or direct hand-off), how PRs are fetched (`provider`: `azure-devops`, `github`, `cursor-origin` or `local-git`; `target_branch`), the severity that forces Request changes, the per-feature review log (`log_file`), and whether comments are posted to PRs (`publish.enabled`, off until Azure DevOps is in use, and only ever on `azure-devops`; `auto_post_on_pr`).
- `testing` — how tests run alongside the review (`mode`, the test review, final approval needs code review **and** test review, flagged defaults), who owns test scaffolding vs scenario tests, and the test environment placeholders
- `secrets` — environment variable **names** only (e.g. `AZURE_DEVOPS_PAT`). Values never go in the file, so it is safe to commit.
- `agents` / `handoff` — which agent fills each role (planning, implementing, reviewing, human owner), the `handoff.md` owner ids, and how work moves between them (see below).

Paths in the config are relative to this folder.

## Agents and handoff

One agent per framework, each filling a role: the **planning agent** (`ai-planning-framework/`), the **implementing agent** (`ai-code-framework/`), the **testing agent** (`ai-test-framework/`) and the **reviewing agent** (`ai-review-framework/`), plus the **human owner** for approvals and the merge. Each agent starts from its framework's `AGENT-BRIEF.md`. The docs refer to these roles; `agents` in the config says which agent fills each (`name`) and its `handoff.md` owner id, so another agent can take a role without doc changes.

- Planning agent → implementing agent through the DevOps board or directly (`handoff.plan_to_code`).
- Implementing agent → reviewing agent through a PR or directly (`handoff.code_to_review`), and at the same time → testing agent (`handoff.code_to_test`), which writes and runs the scenario tests and records them in `handoff.md` `testing` while the feature stays `in-review`.
- The reviewing agent's code verdict is provisional until the test run finishes; it then reviews the tests, and final approval needs both (`testing.final_approval_requires`).
- The reviewing agent reviews automatically when the implementing agent hands off or a PR is raised or updated; nobody asks for it. Every round goes into `reviews/review-log.md`; findings go back to the implementing agent, or an approval goes to the human owner (`handoff.review_feedback`).
- Gates: the human owner approves the plan before code starts and always does the merge (`handoff.require_human_approval`). Agents never merge.

Each feature's state (stage, owner, route, branch, PR, review, approvals, history) is in `<output.work_dir>/<feature>/handoff.md`. Agents pass each other only the feature path. Full rules: `handoff/README.md`.
