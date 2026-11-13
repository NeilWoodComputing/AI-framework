# Agent brief — AI planning framework

Short instructions for any agent working this folder (including a later ticket publisher).

## Read first

1. `../ai-framework.config.yaml` — shared config (paths relative to the `ai-framework` root):
   - `runtime` — which agent runtime performs the work. Resolve: user-preferences.yaml → per-role → shared default. **Verify correct runtime before work; if wrong, stop and hand off.**
   - `project` — the active project: `project.profile` (read it next) and `project.work_dir` (where **new** features go; the shared `ai-planning-framework/work/`)
   - `output.work_dir` / `output.work_dirs` — where existing features live (see **Where features live** below)
   - `development` — active API and UI folder (`active:` under `api` and `ui`)
   - `tickets` — publish target; `secrets` — env var **names** only
   - `agents` and `handoff` — you are the planning agent (`agents.planning`); how finished work goes to the implementing agent (see **Handoff** below and `../handoff/README.md`)
2. The project profile (`project.profile`, beside the shared config; framework defaults in `projects/_template/project.yaml`) — services, glossary, permission pattern, DB naming and conventions, header labels, ticket prefixes, stack hints, and which framework rules are on (`rules`). See `projects/README.md`.
3. `RULES.md` — the framework rules (R1–R9), referred to by ID everywhere else
4. `loops/feature-planning.md` — ordered stages and `work/<feature>/` layout  
5. Relevant `skills/*/SKILL.md` for the stage you are running  
6. Page YAML under `work/<feature>/specs/` and Excel under `work/<feature>/excel/` — source of truth for UI ↔ DB

## Where features live

`work/<feature>/` in this framework's docs means **the feature folder** (`<feature_dir>`):

- **New feature:** `<project.work_dir>/<feature-slug>/` (today `ai-planning-framework/work/<feature-slug>/`). If the config has no `project` block, use `output.work_dir`.
- **Existing feature:** the folder its `handoff.md` `feature_path` names; otherwise the one folder among `output.work_dirs` that contains `<feature-slug>/`. If two contain it, stop and report (**R8**). Features are never moved between work folders.
- **Slugs are unique (R8):** before creating a feature, confirm `<feature-slug>/` exists in none of the work folders; `tools/check.py` fails on a duplicate.

Write `feature_path` in `handoff.md` as the real folder, relative to the `ai-framework` root.

## Create tickets only from tickets/

- User stories / backlog items live in `work/<feature>/tickets/*.md`.
- When asked to create tracker work items (Azure DevOps, GitHub, Jira, …), **only** use those files.
- Do **not** invent new stories from journeys or chat alone at publish time.
- Filename and ID: `T-<DOMAIN>-NNN-<slug>.md` / `T-<DOMAIN>-NNN` (`<DOMAIN>` tokens from the profile's `tickets.domain_tokens`) — **upsert by that ID**, never duplicate.

## Specs and Excel

- Every ticket’s Specs field should point at `specs/*.yaml` and `excel/*.xlsx`.
- Excel specs follow the starter workbook `templates/excel/page-spec-templates.xlsx` (canonical layout; do not edit, copy it to fill in). See `templates/README.md`.
- When publishing, **attach or link** those excel + specs artefacts to the work item.
- Full-stack scope in a ticket must match the specs.
- A routed feature list is a `Paginated Grid` page, never a list modal (**R1**), with a page ticket and a paginated grid ticket (**R2**).
- Specs must validate and generate (**R7**): run the generator, then `tools/check.py` before hand-off.
- Code is reviewed automatically against these specs and tickets by the reviewing agent (`../ai-review-framework/`), on both the PR and direct routes (reports and `review-log.md` go to `work/<feature>/reviews/`), so keep them current when scope changes.

## Never invent DB columns

- **R4**: no Service, Target DB Table, Target DB Column or Population Source that is not in the linked YAML / Excel. If a mapping is missing, stop and fix `generate-ui-spec` (and regenerate Excel) before tickets or publish.

## Publishing tickets (when tracker access exists)

- Follow `skills/publish-tickets/SKILL.md`, which picks the adapter for `tickets.target` (`azure-devops`, `github`, `jira`) in `../ai-framework.config.yaml`.
- Take the target's settings (for Azure DevOps: organisation, project, Area / Iteration, work item types, tags) and the ID pattern from `tickets` in the config.
- Map tickets → the tracker's story type (or task only when explicitly typed as such), as the adapter says.
- Description must keep **Given / When / Then**.
- If `tickets.enabled` is `false`, the adapter is a stub, or any value is still a `<placeholder>`, **stop and report** — do not guess; a dry-run `devops/publish-plan.md` is the most you may write.
- No live publish until the connector is available **and** the user explicitly asks to publish.

## Editing rules (R9)

Apply to every file in this framework, the shared config and the feature folders:

1. **The machine copy is the source of truth.** Re-read a file immediately before changing it; never edit from memory or an old copy.
2. **Hash-check before writing.** Record the file's SHA-256 when you read it and confirm it is unchanged just before you write; if it changed, re-read and redo the edit. After writing, confirm the new hash.
3. **Targeted edits only.** Change the lines that need changing; never regenerate or overwrite a whole hand-written file. Generated files (`.xlsx`, `tests/golden/`) are rewritten only by their tools.
4. **Encoding.** UTF-8 **without BOM**; keep each file's existing line endings (LF, or CRLF where a file already uses it; never mix). No mojibake (text that was decoded with the wrong encoding, e.g. a curly quote turned into three odd characters).
5. **Stay in your lane.** Do not edit other agents' frameworks, parked features (`parked: true` in `handoff.md`) or `handoff/README.md`; propose changes to their owners instead.
6. **No secrets** in any file (env var names only), no `git init` without the human owner.
7. **Verify.** Run `tools/check.py` after a change; it must end `RESULT: PASS`. If golden output changes on purpose, run `--update-golden`, review the diff and say so in `CHANGELOG.md`.

`.editorconfig` sets UTF-8 / LF / final newline for editors; `tools/check.py` checks BOMs, mixed endings and mojibake.

## Running the tools

The generator and `tools/check.py` need Python 3.10+ with `openpyxl`, `PyYAML` and `jsonschema` (`python -m pip install --user -r requirements.txt`). Run them wherever Python is available, the human owner's PC included (`py tools/check.py` on Windows); the agent box is the fallback.

## Handoff (planning agent → implementing agent)

You are the planning agent: `agents.planning` in the config, `owner` id `agents.planning.id` in `handoff.md`. Other roles' owner ids are `agents.<role>.id`; message them by `agents.<role>.name`. Rules, stages and the message format: `../handoff/README.md`.

1. **After tickets** (loop stage 4, plus stubs if run), create `work/<feature>/handoff.md` from `../handoff/templates/handoff.md` (or update it if it exists): stage `planned`, owner `agents.planning.id`, every ticket ID and file listed, artefact table filled, open questions from `plan.md` under **Notes for the next owner**. Add a History row.
2. **Read `handoff` in the config** and note `plan_to_code` and `require_human_approval.plan_to_code`.
3. **Approval gate.** When `require_human_approval.plan_to_code` is `true` (the default), set owner `agents.human.id` and `waiting_on: "human owner: plan_to_code approval"`, then ask the human owner (`agents.human.name`) to approve the plan and tickets for hand-off. Do not hand off until the human owner explicitly says yes. Record `approvals.plan_to_code.approved_by` / `approved_at` from their reply.
4. **Route `board`** (also when `plan_to_code` is `devops`, a deprecated alias that behaves the same) — only when `plan_to_code` is `board` or `devops` **and** `tickets.enabled: true` with no `<placeholders>` under the active `tickets.target`, and access for that target is available (GitHub: the `tickets.github` block filled in, and a GitHub connector or the token env var; Azure DevOps: the `tickets.azure_devops` block filled in, and the DevOps connector or PAT). Publish via `skills/publish-tickets/SKILL.md` (adapter for `tickets.target`; upsert by stable ID). Record each `devops_work_item_id` (the tracker item id, whatever the tracker; the field name is historical) and `devops.board_url` / `published_at` in `handoff.md`. Set stage `in-development`, owner `agents.code.id`, `pickup: pending`, `routes.plan_to_code: board` (or `devops` if that is the configured value). The implementing agent picks the items up from the board; a message is optional (for GitHub, a courtesy message with the issue number and link is helpful). For GitHub (`tickets.target: github`), tickets are published as issues in `ai-framework-tests`.
5. **Route `direct`** — the fallback, and what you use while `tickets.enabled` is `false`: set stage `in-development`, owner `agents.code.id`, `pickup: pending`, `routes.plan_to_code: direct`, then message the implementing agent by name (`agents.code.name`) with `../handoff/templates/handoff-message.md` (feature path + `handoff.md` path + expected).
6. If the config says `board` (or `devops`) but publishing is not possible, **stop and ask the human owner** whether to hand off `direct` instead. Do not switch routes on your own.
7. **Spec gap from the implementing agent** (stage back to `planned`, owner `agents.planning.id`): fix `specs/` → regenerate Excel → update `tickets/`, add a History row, then go through steps 3–5 again.
8. You never edit code, branches or PRs. After hand-off, you only touch the feature again when it comes back to you.

## Working tree reminder

The feature folder layout is in `loops/feature-planning.md` → Working folder convention. `tickets/` is the only source for tracker stories.
