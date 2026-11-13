# Skill: gather-pr-context

Collect everything the later stages need: config, the change (PR or direct hand-off), the **review scope**, linked tickets, their specs and the rules that apply. Read-only.

## Purpose

Build one **context pack** so every later stage reviews the same files against the same specs and the same rules, without re-discovering them.

The review scope depends on the route:

| Route | `review.direct_scope` | Scope |
|-------|-----------------------|-------|
| PR (`handoff.code_to_review: pr`) | — | The PR diff (changed files), plus the unchanged files they depend on |
| Direct (`handoff.code_to_review: direct`) | `plan` (default) | **Plan scope:** every file that implements the feature's plan, read whole. Built from the implementing agent's `implementation` manifest plus a search of the active API / UI paths (step 9). Needs no git and no target branch |
| Direct | `diff` | Local `git diff <base_branch>...<branch>` in each repo (old behaviour) |

On every route the scope holds only files under `review.scope_include` (the folders listed there in the config). Planning artefacts (specs, tickets, stubs, Excel) are loaded below as the reference for what should be built, but are never reviewed. Framework docs, the config and anything else outside `review.scope_include` are never in scope.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `config` | Yes | `../ai-framework.config.yaml` |
| `handoff` | Yes for the direct route | `<feature_path>/handoff.md`: repos, ticket IDs, the `implementation` manifest, and `branch` / `base_branch` / `head_commit` where the repo is under git |
| `pr_id` | Yes for `azure-devops` / `github` / `cursor-origin` | Provider PR number |
| `source_branch` | Yes for `local-git` PRs and `direct_scope: diff` | Branch with the changes |
| `target_branch` | PR route / `direct_scope: diff` only | Defaults to the PR's target, then `review.target_branch` |
| `description` | No | PR description, when the provider cannot supply it (`local-git`) |

## Steps

1. **Read the config.** Note:
   - `development.api.active` and `development.ui.active` → each option's `path`, `rules`, `agent_docs`, `skills`
   - `frameworks.code.rules`
   - `output.work_dirs` (searched in config order when `handoff.md` has no `feature_path`) and `output.feature_layout` (`specs`, `excel`, `tickets`, `stubs`, `reviews`)
   - `review.*` (provider and its block: `azure_devops`, `github`, `cursor_origin` or `local_git`; target branch, `direct_scope`, `scope_include`, `scope_exclude`, threshold, report names, publish) and `handoff.code_to_review`
   - `agents` — role → agent `name` and `handoff.md` owner `id` (you are `agents.review`)
2. **Get the change.**
   - **Find the feature folder (`<feature_path>`).** Use `feature_path` from `handoff.md` first. Without one, search each folder in `output.work_dirs`, in config order, for `<feature>/` (PR route: the feature that holds the linked ticket, step 4). New features are planned in `project.work_dir` (today `ai-planning-framework/work`). If two folders match the same feature name, stop and report; never pick one. A review with no `handoff.md` and no linked feature is written to `ai-planning-framework/work/_unlinked/reviews/`.
   - **Direct route:** read `handoff.md` (stage `in-review`, owner `agents.review.id`, not `example: true`). Take the repos, ticket IDs, `implementation` manifest, and `branch` / `head_commit` per repo where present. Review round `n` = `review.cycle` + 1. Report id: `DIRECT-<branch-slug>-<n>` (branch with `/` replaced by `-`), or `DIRECT-<feature>-<n>` when no branch is recorded.
     - `direct_scope: plan` — no git commands and no target branch needed. Go on to step 3; the scope is built in step 9.
     - `direct_scope: diff` — run the `local-git` commands below with `base_branch` (else `review.target_branch`) as target and `branch` as source. A repo that is not under git, or a placeholder target, → stop and report.
   - **PR route:** get PR metadata and diff from `review.provider`:
     - `azure-devops` — through the connector, read-only: title, description, source / target refs, latest iteration and commit, changed files, diff. Needs `review.azure_devops.*` filled and the env var named by `secrets.azure_devops_pat_env` set. Never print or store the token.
     - `github` — same, with `review.github.*`. Use a connected GitHub connector where available (no token needed); otherwise the env var named by `secrets.github_token_env`.
     - `cursor-origin` — through the Cursor Origin connector, read-only, with `owner` = `review.cursor_origin.namespace` and repository name = `review.cursor_origin.repository`. No token env var is needed:
       - **pull request read**, summary view → title, description, source (head) and target (base) branches, head commit; files view → changed files; commits view → commits in the PR
       - **compare commits** `<target>...<source>` (relative to the merge base, as a PR shows) → the diff
       - **get file contents** at the head ref → whole changed files and the unchanged files they depend on
      - **list commits** on the source branch → history and the reviewed commit
      - Never call the connector's write tools (reviews, comments, labels, reviewers, PR updates): publishing happens in stage 9 when conditions are met.
      - A local clone of the Origin repo can instead be reviewed with `local-git`.
     - `local-git` — in each repo from `review.local_git.repo_paths` (`active` means the active API and UI paths; skip a path that is not a git repo and say so):

       ```bash
       git rev-parse --verify <target>
       git rev-parse --verify <source>
       git log --format="%h %an %ad %s" --date=iso <target>..<source>
       git diff --stat <target>...<source>
       git diff <target>...<source>
       ```

       Three dots (`...`) compares against the merge base, which matches what a PR shows. The id is the provider's PR number. Fetching from a remote is fine; never push, reset or switch the user's branch. This also works for a local clone of an Origin or GitHub repo.
     - Provider values still `<placeholders>` or connector unavailable → stop and report. Fall back to `local-git` only if the human owner agrees.
     - Target branch still `<main-or-develop>` and the PR does not state one → stop and ask.
3. **Find ticket IDs.** Direct route: the `tickets` list in `handoff.md`. PR route: match `T-[A-Z][A-Z0-9]*-[0-9]{3}` case-insensitively in, in order, the PR title, source branch name and description. Normalise to upper case and de-duplicate. Commit messages are a secondary source. Record where each ID was found.
4. **Locate tickets.** For each ID, find `<feature_path>/<tickets>/<ID>-*.md`. With no `feature_path` (PR route), search `<dir>/*/<tickets>/<ID>-*.md` in each folder of `output.work_dirs`, in config order; the parent folder of `tickets/` is the feature. If two folders match the same feature name, stop and report (step 2). An ID with no file is recorded as "ticket not found" (a finding in stage 8, not a guess).
5. **Load ticket content.** From each ticket: user story, **Full-stack scope** table, **Specs** paths (relative to the feature folder), Given / When / Then scenarios, out-of-scope list. Number scenarios `<ticket>/S1`, `S2`, … in order of appearance.
6. **Load specs.** Every YAML in the ticket's Specs field. Build the control inventory:
   - Form Modal, Basic Form, Wizard Modal, Full-Page Wizard (for each wizard step also its format - Standard Form or List Form - visibility, sections and validation): step or section, label, control type, input format, min / max, enablement, editable, mandatory, validation rules, validation failure messages, service, target DB table, target DB column, conditional visibility
   - Paginated Grid, Embedded Grid Modal: results description, columns (title, population source, display format, sortable, additional functionality), paging, empty state, default sort, primary action, row actions (icon, required permission, availability logic, action on click)
   - Import: Download Template button, upload panel (`.xls` / `.xlsx` only, one file at a time, removable), Cancel / Upload buttons, template columns with their validation and Service / Target DB Table / Target DB Column
   - What each page type needs: `checklists/full-stack-checklist.md` **Page types**
   - Also load `stubs/ui-to-db.yaml` if present. Excel is a generated view; if it disagrees with YAML, YAML wins and the difference goes in out-of-scope notes.
7. **Load rules.** Shared `frameworks.code.rules`; the active API's `agent_docs` and `rules`; the active UI's `rules`, or its `agent_docs` when `rules` is `null`. Keep `alwaysApply: true` rules plus rules whose `globs` match a file in the review scope. Note the matching checklists: the file `checklists/api-checklist.md` names for `development.api.active`, and `ui-nextjs-checklist.md` or `ui-angular-checklist.md`.
8. **Classify files in scope** (only files under `review.scope_include`; drop any PR or diff file outside `review.scope_include` and record it as excluded, not reviewed) as `api`, `ui`, `migration`, `tests`, `config`, `rules` or `other`. Flag files outside the active API / UI paths (for example `API.Framework` while `unity-api` is active) for out-of-scope notes.
9. **Build the plan scope** (direct route with `direct_scope: plan` only):
   1. **Start from the manifest.** Every entry in `handoff.md` `implementation` (`api`, `ui`, `tests`, `migrations`) goes into scope, resolved against `code.api.repo` / `code.ui.repo`. Record its reason as **manifest**, with the tickets, pages, controls and DB columns it claims. A listed path that does not exist is a finding (Minor, area Manifest). An empty manifest means the implementing agent should not have handed off: say so as a Major finding and rely on discovery.
   2. **Cross-check against the plan.** Search the active API and UI paths (text search such as `rg`, honouring `review.scope_exclude`) for terms taken from the plan:
      - spec page titles and slugs (`specs/<page>.yaml`)
      - routes (from the ticket, `stubs/ui-to-db.yaml`, and the UI routes file, e.g. `src/config/api-routes.ts`)
      - Service names, Target DB Tables and Target DB Columns / Population Sources (e.g. `Contacts`, `Contact`, `EmailAddress`, `OrganisationId`)
      - ticket IDs (`T-CONTACT-001`)
      - names derived from them: DTO / record / entity / controller / mapper / component names (`ContactRecord`, `ContactsController`, `ContactMapper`, `ContactDto`, `AddEditContactForm`) and camelCase bindings (`#/properties/emailAddress`, `emailAddress`)

      Common words (`Name`, `Active`) only count together with the table, entity or route. A hit is **relevant** when the file renders a spec control, binds or maps one, persists or reads a spec column, defines the route or endpoint, or tests a ticket scenario. Merely mentioning a word does not make a file relevant.
   3. **Discovered files.** Add every relevant file that is not in the manifest to the scope with reason **discovered**. Raise one **Minor** finding per file, area **Manifest**, titled "Manifest incomplete: `<path>` implements <controls / columns> but is not listed in handoff.md `implementation`".
   4. **Not implemented.** Any spec control, grid column / action or DB mapping that no file in scope implements is a **Not implemented** finding at the severity `checklists/severity.md` sets for that unmet spec item: a mandatory control or DB mapping is a **Blocker**, an optional control a **Major**. Skip items the ticket's out-of-scope list defers, and record them as **Deferred**.
   5. **Read whole files.** Every file in scope is read in full: its current contents, not a diff. Later stages raise findings only about code relevant to the plan. Unrelated pre-existing issues in those files go to **Out of scope / pre-existing notes** and never affect the verdict.
   6. **Exclude** anything matching `review.scope_exclude`: build output, node_modules, bin / obj, `.next`, generated files and secrets / `.env` files. Never open secret or `.env` files, even to check them.
   7. **Re-review rounds (round `n` 2 or later).** Review the previous round's open findings plus every in-scope file changed since that round (from `reviewed_commits` where the repo is under git, the implementing agent's hand-off notes, or the before / after SHA-256 values recorded in `handoff.md`), each read whole. If what changed cannot be told, review the full plan scope. The final round - round `handoff.max_review_cycles`, or the last extra round the human owner has allowed past it - is always a full pass of the plan scope. Say which it was in the report's **Review scope** (round type).

## Outputs

A context pack (kept in working memory or as a scratch section; not a separate file) with:

- Change: PR id, title, source → target, provider, reviewed commit / iteration, author, description excerpt (PR route); or the `handoff.md` path, round `n`, report id, `direct_scope`, branch / head commit per repo where present (direct route)
- **Review scope:** how it was built (PR diff / plan scope / local diff); every file with its class and reason (diff, dependency, manifest, discovered); files excluded; controls and mappings not implemented or deferred
- Linked tickets: ID, file path, feature, where found; tickets not found
- Control inventory per spec file, with the file(s) implementing each control in plan scope
- Scenario list `<ticket>/S<n>` with titles
- Applicable rules and checklists
- Anything that stopped or limited the review

## Quality checks

- [ ] Config read; nothing taken from a `<placeholder>` the route actually needs
- [ ] PR route / `direct_scope: diff`: diff uses the merge base (`<target>...<source>`) or the provider's PR diff
- [ ] `direct_scope: plan`: manifest loaded, codebase searched, discovered files flagged Minor, unimplemented controls / mappings raised, whole files read
- [ ] Reviewed commit recorded where git is used, so re-reviews can say what changed
- [ ] Every ticket ID traced to a file or recorded as not found
- [ ] Every Specs path resolved; YAML used as the source of truth
- [ ] Rules list matches the active API / UI in the config
- [ ] Every file in scope is under `review.scope_include`; planning artefacts used as reference only
- [ ] `review.scope_exclude` honoured; no tokens or `.env` values read or printed
- [ ] Provider connectors used read-only; no PR comment, review or update tool called
