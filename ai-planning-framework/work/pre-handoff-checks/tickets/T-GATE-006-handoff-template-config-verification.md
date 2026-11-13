# Ticket: T-GATE-006 — Handoff template / README code.verification + gate field, config verification block

| Field | Value |
|-------|--------|
| ID | T-GATE-006 |
| Type | Cross-cutting (pipeline docs / config) |
| Feature | pre-handoff-checks |
| Priority | High |
| Owner | plan-bot (shared handoff template / README and `ai-framework.config.yaml`) |
| Specs | None; `plan.md` §5.4 (draft config block) |
| Journey (optional) | — |

## User story

**As** every agent in the pipeline  
**I want** the gate's settings in config and its result in a fixed place in `handoff.md`  
**So that** the implementing agent knows what to run and the reviewing agent can check one field

## Full-stack scope

No UI controls or DB columns. Files: `handoff/templates/handoff.md` (`code:` block), `handoff/README.md` (fields + stage rule), `ai-framework.config.yaml` (new `verification:` block).

## Work to do

1. Template `code:` block: keep `verification: []` and say entries include pre-handoff check lines; add `pre_handoff_gate: null  # pass | fail` and `pre_handoff_gate_at: null` (D9).
2. `handoff/README.md`: document the two fields; add the rule "`in-development → in-review` needs `code.pre_handoff_gate: pass`"; describe Review Bot's response to a missing / failed gate (D10: returned without a review round, no `review.cycle` increment).
3. `ai-framework.config.yaml`: add the `verification:` block from `plan.md` §5.4 with Neil's answers (runner, allowlist, `fail_on_warnings`, `blocks_handoff`, per-target checks, `not_in_git`). Env var names only; no secrets.
4. Validate the YAML; existing feature `handoff.md` files are not rewritten (the fields apply from the next hand-off).

## Acceptance criteria

### Scenario: S1 — Template carries the gate fields

```gherkin
Given handoff/templates/handoff.md after this ticket
When a planning agent copies it for a new feature
Then code has build, tests, verification, pre_handoff_gate and pre_handoff_gate_at
And the comments say what goes in each
```

### Scenario: S2 — README states the blocking rule

```gherkin
Given handoff/README.md after this ticket
When an agent reads the stage rules
Then it says in-development → in-review needs code.pre_handoff_gate: pass
And it says what the reviewing agent does when the gate is missing or failed
```

### Scenario: S3 — Config block is valid and secret-free

```gherkin
Given ai-framework.config.yaml with the new verification block
When it is parsed as YAML
Then it parses without error
And verification.targets lists api-framework and nextjs with their paths and checks
And the block contains no secret values
```

### Scenario: S4 — Existing features are not rewritten

```gherkin
Given work/manage-animals/handoff.md and other existing feature handoff files
When this ticket is done
Then their content is unchanged
```

Checklist (derived from scenarios):

- [ ] Template and README updated together
- [ ] Config block added and validated
- [ ] No existing `handoff.md` touched

## Out of scope

- The runner and loop text (T-GATE-005)
- Review Bot's files (T-GATE-007)

## Notes

- Stable ID for DevOps upsert: `T-GATE-006`
- **Done** by plan-bot 2026-10-09T10:34:24+01:00: template `code.verification` comment + `pre_handoff_gate` / `pre_handoff_gate_at`; README transitions rows + rule 12; config `verification:` block (YAML validated; other sections unchanged). S1–S4 met (S4: no existing feature `handoff.md` touched).
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D3, D6, D9, D10, D14, D15.
