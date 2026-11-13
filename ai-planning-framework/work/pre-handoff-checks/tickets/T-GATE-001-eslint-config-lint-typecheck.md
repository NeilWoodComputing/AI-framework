# Ticket: T-GATE-001 — ESLint flat config and lint / typecheck scripts (UI.NextJs.Framework)

| Field | Value |
|-------|--------|
| ID | T-GATE-001 |
| Type | Cross-cutting (build tooling) |
| Feature | pre-handoff-checks |
| Priority | High |
| Owner | dev-bot |
| Specs | None (no UI pages); `plan.md` §5.2 |
| Journey (optional) | — |

## User story

**As** the implementing agent  
**I want** `npm run lint` and `npm run typecheck` to run non-interactively in UI.NextJs.Framework  
**So that** lint and type errors are caught before hand-off instead of in code review

## Full-stack scope

No UI controls or DB columns. Files: `ai-code-framework/ui/UI.NextJs.Framework/eslint.config.mjs` (new), `package.json` (`scripts`), any source fixes needed for a clean baseline.

## Work to do

1. Add `eslint.config.mjs` (flat config) with the agreed ruleset (D2): `FlatCompat` extending `next/core-web-vitals` and `next/typescript`, ignoring `.next*`, `node_modules`, `e2e/` (D11), `next-env.d.ts`.
2. Replace `"lint": "next lint"` (deprecated in Next 15.5, prompts for setup) with `"lint": "eslint ."`; add `"typecheck": "tsc --noEmit"`.
3. Run both on the current code; fix **errors** (no behaviour change). Record the warning count as the baseline (D3). If errors cannot be cleared in this ticket, fall back to linting touched files with the recorded baseline (D17) and note it in `handoff.md`.
4. No new devDependencies (D2 uses packages already installed).

## Acceptance criteria

### Scenario: S1 — Lint runs without prompting

```gherkin
Given UI.NextJs.Framework with eslint.config.mjs and "lint": "eslint ."
When I run npm run lint in a non-interactive shell
Then ESLint runs against the source without asking to set up a config
And it exits 0 when there are no lint errors
```

### Scenario: S2 — A lint error fails the run

```gherkin
Given a source file with a rule violation configured as an error (for example a rules-of-hooks violation)
When I run npm run lint
Then it exits non-zero
And the output names the file, line and rule
```

### Scenario: S3 — Warnings follow the agreed policy

```gherkin
Given a source file with only a rule configured as a warning
When I run npm run lint
Then it exits 0 and reports the warning count (D3)
```

### Scenario: S4 — Typecheck script

```gherkin
Given "typecheck": "tsc --noEmit" in package.json
When I run npm run typecheck on code with a type error
Then it exits non-zero and names the file and line
When the type error is fixed
Then it exits 0
```

### Scenario: S5 — Build output and the e2e package are ignored

```gherkin
Given .next, .next-test, node_modules and e2e/ folders exist
When I run npm run lint
Then no file under those folders is linted
```

### Scenario: S6 — Clean baseline on current code

```gherkin
Given the current UI.NextJs.Framework source after this ticket
When I run npm run lint and npm run typecheck
Then both exit 0
And the lint warning count is recorded in handoff.md code.verification
```

Checklist (derived from scenarios):

- [ ] `eslint.config.mjs` present; `next lint` no longer used
- [ ] `lint` and `typecheck` scripts in `package.json`
- [ ] Ignores cover build output, node_modules and `e2e/`
- [ ] Current code passes with errors = 0; warning baseline recorded

## Out of scope

- Prettier / formatting rules
- Linting Test Bot's `e2e/` package (D11)
- Failing on warnings (D3: counted, not failed)

## Notes

- Stable ID for DevOps upsert: `T-GATE-001`
- Installed today: eslint 9.39.5, eslint-config-next 15.5.27, @eslint/eslintrc 3.3.7, @next/eslint-plugin-next 15.5.27, eslint-plugin-react-hooks 5.2.0; no typescript-eslint.
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D2, D3, D11, D17.
