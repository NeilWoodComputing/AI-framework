# Ticket: T-GATE-007 — Review Bot: gate-enforced rules and stale "no test runner" lines (cross-framework)

| Field | Value |
|-------|--------|
| ID | T-GATE-007 |
| Type | Cross-cutting (cross-framework: ai-review-framework) |
| Feature | pre-handoff-checks |
| Priority | Medium |
| Owner | **review-bot** (owns `ai-review-framework`; Plan Bot and Dev Bot do not edit these files) |
| Specs | None; `plan.md` §2 (quoted stale lines), §5.4 |
| Journey (optional) | — |

## User story

**As** the reviewing agent  
**I want** my skills and checklists to know which points the pre-handoff gate enforces, and that UI.NextJs.Framework has a test runner  
**So that** I stop re-raising mechanical findings each round and stop reporting a tooling gap that no longer exists

## Full-stack scope

No UI controls or DB columns. Files (Review Bot's own): `skills/review-code-standards/SKILL.md`, `checklists/severity.md`, `skills/review-tests/SKILL.md`, `checklists/ui-nextjs-checklist.md`, `skills/review-security-and-data/SKILL.md`, `checklists/security-checklist.md`; optionally `examples/sample-review-add-edit-contact.md` and `templates/review-report.md` ("Tooling gaps, e.g. no UI test runner").

## Work to do

1. `review-code-standards` + `severity.md`: lint, type-check, line endings / final newline / BOM, duplicate doc paragraphs and committed secrets are **gate-enforced**. Do not re-raise them when `code.pre_handoff_gate: pass`; if the gate missed one, raise it once and note the gate gap (so the check gets fixed). A committed secret stays **Blocker** whatever the gate says.
2. On pickup: if `code.pre_handoff_gate` is missing or `fail`, return it to the implementing agent without a review round; no `review.cycle` increment (D10).
3. `review-tests/SKILL.md:22` and `:43`, `ui-nextjs-checklist.md:47`: replace "no test runner" with the current state — `npm test` (vitest, `src/**/*.test.{ts,tsx}`) and Playwright e2e in `e2e/` (Test Bot) — after Review Bot verifies it on disk.
4. Security skill / checklist: say the secrets scan runs in the gate and the reviewer still judges anything it cannot see (e.g. secrets in new file types).
5. Update the illustrative sample review (`examples/sample-review-add-edit-contact.md`) and the report template's "no UI test runner" tooling-gap example to the current tooling (default, Neil may override).

## Acceptance criteria

### Scenario: S1 — Gate-enforced points are not re-raised

```gherkin
Given a hand-off with code.pre_handoff_gate: pass
When Review Bot reviews the code
Then it does not raise lint, line-ending, BOM, final-newline or duplicate-paragraph findings already covered by the gate
```

### Scenario: S2 — A point the gate missed is raised once with a gate gap note

```gherkin
Given code.pre_handoff_gate: pass and a mixed-line-ending file the gate did not report
When Review Bot reviews the code
Then it raises one finding for the file
And the finding says the gate missed it and which check needs fixing
```

### Scenario: S3 — Committed secrets stay Blocker

```gherkin
Given a committed non-empty secret in reviewed config
When Review Bot reviews the code
Then it is a Blocker regardless of code.pre_handoff_gate
```

### Scenario: S4 — Missing or failed gate on pickup

```gherkin
Given a hand-off where code.pre_handoff_gate is null or fail
When Review Bot picks it up
Then it returns it to the implementing agent without a review round and without incrementing review.cycle (D10)
And it records a History row saying why
```

### Scenario: S5 — No stale "no test runner" lines

```gherkin
Given review-tests/SKILL.md and checklists/ui-nextjs-checklist.md after this ticket
When I search them for "no test runner"
Then there are no matches
And they name npm test (vitest) and the e2e package as the UI test tooling
```

Checklist (derived from scenarios):

- [ ] Code-standards / severity: gate-enforced list and gate-gap rule
- [ ] Pickup behaviour for missing / failed gate
- [ ] Stale test-runner lines replaced after on-disk check
- [ ] Secrets remain Blocker

## Out of scope

- Any edit by Plan Bot or Dev Bot to `ai-review-framework`
- Changing severity levels other than the gate-enforced cap

## Notes

- Stable ID for DevOps upsert: `T-GATE-007`
- Cross-framework ticket: Plan Bot drafts it; Review Bot owns and applies it.
- Stale lines as read 2026-10-09: `review-tests/SKILL.md:22` ("No test runner configured - `package.json` scripts are `dev`, `build`, `start`, `lint` …"), `review-tests/SKILL.md:43` (severity rule mentioning a UI codebase with no test runner), `ui-nextjs-checklist.md:47` ("… (no test runner is configured in `package.json`)"), `examples/sample-review-add-edit-contact.md:84, 106, 122`.
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D10, D16.
