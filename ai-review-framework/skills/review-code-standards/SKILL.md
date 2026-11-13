# Skill: review-code-standards

Review the changed code against the rules of the **active** API and UI, as set in `../ai-framework.config.yaml`.

## Purpose

Each codebase in `ai-code-framework/` carries its own rules, agent docs and skills. This stage applies the ones that match the active pairing, so the PR follows the conventions the code agents were told to follow.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | Applicable rules, files in the review scope by class |
| `diff` + `files` | Yes | Review scope from `gather-pr-context`: PR diff + files, or on the direct route the plan-scope files read whole (or local diff). On the plan scope, findings only on plan-relevant code; unrelated pre-existing issues go to notes |
| `checklists` | Yes | The active API checklist (`checklists/api-checklist.md`) plus the active UI checklist |

## Which rules apply

| Config | Source of rules | Checklist |
|--------|-----------------|-----------|
| `development.api.active: csharp-api` | Active C# API's `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc` (index: `.cursor/rules/README.md`), `.cursor/skills/*/SKILL.md` "Check" sections | `checklists/api-csharp-checklist.md` |
| `development.api.active: api-framework` | `ai-code-framework/api/API.Framework/CLAUDE.md`, its `.cursor/rules`, and shared `ai-code-framework/.cursor/rules/api-json-schema-forms.mdc` | `checklists/api-framework-checklist.md` |
| `development.ui.active: nextjs` | `ai-code-framework/ui/UI.NextJs.Framework/AGENTS.md`, `README.md`, `.cursor/rules/**` (index: `README.md`) | `checklists/ui-nextjs-checklist.md` |
| `development.ui.active: angular` | `ai-code-framework/ui/UI.Angular.Framework/.cursor/rules/**` (index: `README.md`), `CLAUDE.md` | `checklists/ui-angular-checklist.md` |
| Always | `frameworks.code.rules` (`ai-code-framework/.cursor/rules/`) when their `globs` match | — |

Apply rules with `alwaysApply: true`, plus rules whose `globs` match a file in the review scope.

## Steps

1. List the rules that apply (from the context pack), with the files each one covers.
2. Walk the API checklist over the API files in scope, and the active UI checklist over the UI files in scope.
3. For each breach, record the rule file and the line or heading it comes from.
4. **General practice only where no rule applies.** When a point is not covered by the active codebase's rules or agent docs (for Next.js, section C of `checklists/ui-nextjs-checklist.md`):
   - Label it **General practice** in the reference column.
   - Cap General-practice findings at **Minor**, unless they are a security or data-integrity issue (then stage 6 severities apply).
   - If the active UI's `rules` is ever `null` again, say so in the report and review against its `agent_docs` plus general practice.
5. If the PR changes rule files themselves (`.cursor/rules`, `.claude/rules`, skills) on the C# API, both copies change together: Cursor `.mdc` first, then `.claude/rules/`.
6. Note pairing issues: a UI route or `apiRoutes` change without the matching API endpoint (or the reverse).
7. Do not repeat what a formatter or linter enforces unless a rule asks for it; such points are **Nit** at most.

## Outputs

- Findings with area `API standards` or `UI standards`, `file:line`, rule reference (`<path>.mdc` → heading) or **General practice**, and a suggested fix
- A one-line statement of which rule sets were applied (goes in the report summary)

## Quality checks

- [ ] Rules used match `development.*.active` in the config
- [ ] Every finding cites a rule file, the README, or is labelled General practice
- [ ] General-practice findings used only where no rule covers the point
- [ ] General-practice findings capped at Minor (unless security / data)
- [ ] No rules borrowed from the inactive codebase without saying so
