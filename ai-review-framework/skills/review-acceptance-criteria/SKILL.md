# Skill: review-acceptance-criteria

Trace each Given / When / Then scenario in the linked tickets to the code that implements it and the tests that prove it.

## Purpose

Tickets carry the agreed behaviour as Gherkin-style scenarios. This stage shows, scenario by scenario, whether the PR delivers it: **Covered**, **Partial** or **Missing**.

## Inputs

| Name | Required | Description |
|------|----------|-------------|
| `context_pack` | Yes | Scenario list `<ticket>/S<n>` with full Given / When / Then text |
| `diff` + `files` | Yes | Review scope from `gather-pr-context`: PR diff + files, or on the direct route the plan-scope files read whole (or local diff): implementation and test files |
| `stage_2_3_results` | Yes | Spec conformance and data mapping rows (reuse their references) |

## Steps

1. For each scenario, split it into steps: each `Given`, `When`, `Then` and `And` / `But`.
2. For each **Given**: confirm the precondition can exist (mode, parent context, seed data, permissions).
3. For each **When**: find the entry point (UI action, form submit, API route).
4. For each **Then / And**: find the code that produces the outcome:
   - UI outcomes (form closes, message shown, control read-only, Save hidden)
   - Validation outcomes (exact message text, no write made)
   - Persistence outcomes naming Service / Table / Column (write, update, unchanged columns left alone)
5. Find tests that assert the outcome (API unit tests, schema validation tests, UI tests, E2E). Reuse `review-tests` conventions for where to look.
6. Mark the scenario:

   | Status | Meaning |
   |--------|---------|
   | **Covered** | Every Then / And traced to code, and at least one test asserts the key outcome |
   | **Partial** | Code traced but no test, or some Then / And not traced |
   | **Missing** | The When or a core Then is not implemented |
   | **Out of PR scope** | The ticket's out-of-scope list or the PR description defers it explicitly |

7. Raise findings using `checklists/severity.md`:
   - **Missing** → Major; Blocker when it means data is written wrongly or a mandatory or uniqueness rule is not enforced
   - **Partial** with an untraced Then → Major
   - **Partial** only for lack of a test → Minor (stage 7 suggests the test)

## Outputs

- GWT coverage table rows: Scenario ID | Scenario | Status | Code reference(s) | Test reference(s) | Notes
- Findings with `file:line` and ticket reference (`tickets/T-<DOMAIN>-NNN-*.md` → Scenario: <name>)

## Quality checks

- [ ] Every scenario in every linked ticket has a row
- [ ] Every Then / And naming a column is checked against stage 3
- [ ] Exact validation messages from the scenario are confirmed in code
- [ ] "Covered" always has both a code and a test reference
- [ ] No scenarios invented; gaps in the ticket go to out-of-scope notes
