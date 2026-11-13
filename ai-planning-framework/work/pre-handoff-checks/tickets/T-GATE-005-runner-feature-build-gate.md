# Ticket: T-GATE-005 — Pre-handoff runner and feature-build stage 5 gate + AGENT-BRIEF item

| Field | Value |
|-------|--------|
| ID | T-GATE-005 |
| Type | Cross-cutting (framework loop) |
| Feature | pre-handoff-checks |
| Priority | High |
| Owner | dev-bot (owns `ai-code-framework`) |
| Specs | None; `plan.md` §5.1, §5.4 |
| Journey (optional) | — |

## User story

**As** Neil  
**I want** one command that runs every pre-handoff check, wired into the implementing agent's loop as a gate  
**So that** a feature cannot reach review with mechanical problems the tools can catch

## Full-stack scope

No UI controls or DB columns. Files: the runner (`ai-code-framework/scripts/pre-handoff-checks.mjs`, D15), `ai-code-framework/loops/feature-build.md` (stages 5, 6, 8 and the agent checklist), `ai-code-framework/AGENT-BRIEF.md` (Definition of done).

## Work to do

1. Runner: `--target api-framework|nextjs|all`, `--json`; runs the checks configured in `verification.targets` (T-GATE-006) for each target touched by the feature (from the `implementation` manifest), secrets on both; prints `<check> <target> -> pass|fail (<counts>)`; exit 0 / 1. Includes `npm run lint`, `npm run typecheck` (T-GATE-001), `eol` (T-GATE-002), `secrets` (T-GATE-003), `docs-dup` (T-GATE-004, D8), and the existing unit tests: `npm test` (vitest) and `dotnet test` on Api.Framework.Tests (D6).
2. `feature-build.md` stage 5: rename to *tests + pre-handoff checks*; run build then the runner; 3 attempts then blocker (as for build); write each check line to `code.verification` and `code.pre_handoff_gate` / `_at` (D9). Update the stage-5 line "record that the UI has no test runner when `package.json` has none" (vitest exists).
3. Stage 6: keep "Re-run stage 5 after changes"; the last run before stage 8 is the recorded one.
4. Stage 8 gate: do not hand off unless `code.pre_handoff_gate: pass`.
5. `AGENT-BRIEF.md` Definition of done: add "Pre-handoff checks pass (runner); results in `code.verification`; `code.pre_handoff_gate: pass`"; align the existing build line (lint is now always configured).
6. Agent checklist (per loop) in `feature-build.md`: add the gate item.

## Acceptance criteria

### Scenario: S1 — All checks pass

```gherkin
Given both targets with no lint, type, line-ending, secret or duplicate-paragraph problems
When the implementing agent runs the pre-handoff runner with --target all
Then every configured check prints "pass"
And the runner exits 0
```

### Scenario: S2 — One failing check fails the gate

```gherkin
Given a target with one seeded violation for a single check (for example a lint error)
When the runner runs
Then that check prints "fail" with its counts and the other checks still run and report
And the runner exits 1
```

### Scenario: S3 — Results recorded in handoff.md

```gherkin
Given a feature at stage 5 of feature-build
When the implementing agent runs the gate
Then code.verification has one line per check with target, result and counts
And code.pre_handoff_gate is pass or fail with code.pre_handoff_gate_at set
And no secret value appears in handoff.md
```

### Scenario: S4 — A failed gate blocks hand-off

```gherkin
Given code.pre_handoff_gate: fail after three fix attempts
When the implementing agent reaches stage 8
Then it does not move the feature to in-review
And it records a blocker naming the failing checks
```

### Scenario: S5 — The recorded result is the last run

```gherkin
Given the gate passed in stage 5 and stage 6 changed files
When stage 5 is re-run after optimise
Then code.verification and code.pre_handoff_gate reflect the re-run, not the earlier one
```

### Scenario: S6 — Only touched targets run their target checks

```gherkin
Given a feature whose implementation manifest lists only API files
When the runner runs for that feature
Then lint and typecheck for nextjs are not run
And the secrets check still runs on both targets
```

### Scenario: S7 — Docs list the gate

```gherkin
Given feature-build.md and AGENT-BRIEF.md after this ticket
When an implementing agent reads stage 5, stage 8, the agent checklist and the Definition of done
Then each names the pre-handoff runner, where results go and that a failed gate blocks hand-off
And no line says UI.NextJs.Framework has no test runner
```

Checklist (derived from scenarios):

- [ ] Runner with per-target checks and a single exit code
- [ ] Stage 5 / 6 / 8, agent checklist and Definition of done updated
- [ ] Results and gate field written to `handoff.md`; no values printed

## Out of scope

- Unity.API / UI.Angular.Framework loops
- e2e / scenario tests (Test Bot)
- Git hooks / CI

## Notes

- Stable ID for DevOps upsert: `T-GATE-005`
- Depends on T-GATE-001..004 and T-GATE-006 (field names). The gate becomes blocking only after the first full run passes (T-GATE-008 first, D1).
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D6, D9, D11, D15, D17.
