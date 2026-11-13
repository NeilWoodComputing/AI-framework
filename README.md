# ai-framework

Four frameworks that work together to plan, build, test and review full-stack features: **what renders on screen** and **where that data lives in the database**.

| Folder | Role |
|--------|------|
| `ai-planning-framework/` | Skills and loops that turn a feature into a plan, UI ↔ DB page specs (YAML + Excel), user journeys, Given / When / Then tickets and framework-agnostic stubs. Start with its `AGENT-BRIEF.md`. |
| `ai-code-framework/` | Framework-owned reference codebases and shared rules (`.cursor/rules/`). **Active development codebases** (`api/` and `ui/`) live in the [ai-framework-tests](https://github.com/NeilWoodComputing/ai-framework-tests) repository. |
| `ai-review-framework/` | Skills and a loop that review a raised PR against the planning specs (controls and Service / Table / Column), the Given / When / Then tickets and the active API/UI rules, then write `reviews/PR-<id>-review.md`. Start with its `AGENT-BRIEF.md`. |
| `ai-test-framework/` | Skills and a loop that turn each ticket's Given / When / Then scenarios (by explicit ID `<ticket>/S<n>`) into unit and e2e tests, run them against a dedicated test environment and write `tests/TEST-<feature>-<n>-report.md`. Runs alongside the review. Start with its `AGENT-BRIEF.md`. |
| `handoff/` | How a feature moves between the agents: pipeline, stages, rules, and the `handoff.md` / message templates. Start with `handoff/README.md`. |
| `ai-framework.config.yaml` | Shared configuration: framework paths, agents, handoff routes and gates, testing, active API/UI folder, output folder and ticket target. |

## Agents: read the config first

Before running any skill or loop, read `ai-framework.config.yaml`:

- `runtime` — which agent runtime performs the work (Cursor Cloud Agents, Claude Code, etc.). The shared default is `cursor` (Cursor Cloud Agents on Cursor-managed VMs). **Local Windows PC execution is NEVER the default.** Per-user preferences override the shared config (see **Runtime configuration** below).
- `development` — which API and UI folder is the active target (`active:` picks one option each)
- `output.work_dir` — where per-feature artefacts are written (`<work_dir>/<feature>/plan.md`, `specs/`, `excel/`, `journeys/`, `tickets/`, `stubs/`, `tests/`, `reviews/` incl. `reviews/review-log.md`, and `handoff.md`)
- `tickets` — where stories are published (Azure DevOps). If `enabled` is `false` or any value is still a `<placeholder>`, stop and report; do not guess.
- `review` — automatic reviews (`auto_review`, `triggers`: PR opened / updated or direct hand-off), how PRs are fetched (`provider`: `azure-devops`, `github`, `cursor-origin` or `local-git`; `target_branch`), the severity that forces Request changes, the per-feature review log (`log_file`), and whether comments are posted to PRs (`publish.enabled`, supported on `github` and `azure-devops`; GitHub uses COMMENT event only; `auto_post_on_pr`).
- `testing` — how tests run alongside the review (`mode`, the test review, final approval needs code review **and** test review, flagged defaults), who owns test scaffolding vs scenario tests, and the test environment placeholders
- `secrets` — environment variable **names** only (e.g. `AZURE_DEVOPS_PAT`). Values never go in the file, so it is safe to commit.
- `agents` / `handoff` — which agent fills each role (planning, implementing, reviewing, human owner), the `handoff.md` owner ids, and how work moves between them (see below).

Paths in the config are relative to this folder.

## Runtime configuration

The framework is runtime-agnostic: it maps roles (planning, code, review, testing) to runtimes (Cursor Cloud Agents, Claude Code, or other tools).

### Supported runtimes

- **`cursor`** — Cursor Cloud Agents (Cursor-managed VMs), coordinated from the bot machine. **This is the shared default.** The bot machine (always-on Linux) coordinates all work. Neil's Windows PC may be switched off.
- **`cursor-local`** — Cursor IDE on a developer's local machine. **Opt-in only, never the default.**
- **`claude-code`** — Claude Code or other Claude interfaces.
- More runtimes can be added later.

### Precedence

Configuration is resolved in this order (highest to lowest priority):

1. **User preferences file** — `user-preferences.yaml` (not committed to the repo)
2. **Per-role setting** in `ai-framework.config.yaml` (`runtime.planning`, `runtime.code`, etc.)
3. **Shared default** in `ai-framework.config.yaml` (`runtime.default`)

### User preferences file

One file per machine (not committed): `user-preferences.yaml`

**Locations:**
- Bot machine: `/home/box/ai-framework/user-preferences.yaml`
- Developer machine: `~/.ai-framework/user-preferences.yaml`
- Custom: set `AI_FRAMEWORK_USER_CONFIG=/path/to/user-preferences.yaml`

### Setting up your preferences

**Run the init script:**

```bash
# Linux / macOS / WSL
./scripts/init-user.sh [username]

# On the bot machine, enable caching:
AI_FRAMEWORK_BOT_MACHINE=true ./scripts/init-user.sh [username]
```

```powershell
# Windows PowerShell
.\scripts\init-user.ps1 [-Username <username>]

# On the bot machine, enable caching:
$env:AI_FRAMEWORK_BOT_MACHINE="true"; .\scripts\init-user.ps1
```

Username is optional (fills `user:` field only). The script creates the preferences file, caches the framework on bot machines, and migrates old formats automatically.

**Edit the preferences file:**

```yaml
user: neil
runtime:
  default: cursor        # or claude-code, cursor-local
  # code: claude-code    # per-role override (optional)
```

### Switching to Claude Code

Edit `user-preferences.yaml` and set:
```yaml
runtime:
  code: claude-code
```

### Agent responsibility

Before working, each agent must:
1. Resolve effective runtime (user preferences → per-role → shared default)
2. Verify it's running under the correct runtime
3. **Stop and hand off if wrong** — never run under the wrong subscription

## Agents and handoff

One agent per framework, each filling a role: the **planning agent** (`ai-planning-framework/`), the **implementing agent** (`ai-code-framework/`), the **testing agent** (`ai-test-framework/`) and the **reviewing agent** (`ai-review-framework/`), plus the **human owner** for approvals and the merge. Each agent starts from its framework's `AGENT-BRIEF.md`. The docs refer to these roles; `agents` in the config says which agent fills each (`name`) and its `handoff.md` owner id, so another agent can take a role without doc changes.

- Planning agent → implementing agent through the DevOps board or directly (`handoff.plan_to_code`).
- Implementing agent → reviewing agent through a PR or directly (`handoff.code_to_review`), and at the same time → testing agent (`handoff.code_to_test`), which writes and runs the scenario tests and records them in `handoff.md` `testing` while the feature stays `in-review`.
- The reviewing agent's code verdict is provisional until the test run finishes; it then reviews the tests, and final approval needs both (`testing.final_approval_requires`).
- The reviewing agent reviews automatically when the implementing agent hands off or a PR is raised or updated; nobody asks for it. Every round goes into `reviews/review-log.md`; findings go back to the implementing agent, or an approval goes to the human owner (`handoff.review_feedback`).
- Gates: the human owner approves the plan before code starts and always does the merge (`handoff.require_human_approval`). Agents never merge.

Each feature's state (stage, owner, route, branch, PR, review, approvals, history) is in `<output.work_dir>/<feature>/handoff.md`. Agents pass each other only the feature path. Full rules: `handoff/README.md`.

## Testing

The framework includes automated quality checks and tests that run on every PR and push to main.

### Running Tests Locally

```bash
./scripts/test.sh
```

This runs all available checks:
- **Config validation** — validates `ai-framework.config.yaml` and `user-preferences.example.yaml` schemas
- **Framework consistency** — checks AGENT-BRIEF.md files, README precedence, and referenced paths
- **ShellCheck** — static analysis of `init-user.sh`
- **PSScriptAnalyzer** — static analysis of `init-user.ps1`
- **yamllint** — YAML formatting and style
- **markdownlint** — Markdown formatting and style
- **Bash tests (bats)** — behaviour tests for `init-user.sh`
- **PowerShell tests (Pester)** — behaviour tests for `init-user.ps1`

### Test Coverage

**Init script tests:**
- Fresh config creation from template
- Idempotent re-runs (preserves existing settings)
- Migration from old `users/<name>.yaml` format
- Environment variable handling (`AI_FRAMEWORK_USER_CONFIG`, `AI_FRAMEWORK_BOT_MACHINE`)
- Cache creation and refresh (bot machine mode)
- Git and rsync fallback handling

**Quality checks:**
- Config schema validation (runtime values, agent mappings, required fields)
- All AGENT-BRIEF.md files contain runtime verification instructions
- README precedence matches config precedence
- Referenced framework paths exist
- Shell and PowerShell scripts pass static analysis
- YAML and Markdown files follow style guidelines

### CI/CD

GitHub Actions runs the full pipeline automatically on:
- Pull requests to `main`
- Pushes to `main`

The pipeline includes parallel validation, linting, and testing jobs. See `.github/workflows/pipeline.yml` for the complete CI configuration.
