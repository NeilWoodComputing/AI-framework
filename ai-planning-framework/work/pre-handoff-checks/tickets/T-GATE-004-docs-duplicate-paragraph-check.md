# Ticket: T-GATE-004 — Duplicate-paragraph docs check

| Field | Value |
|-------|--------|
| ID | T-GATE-004 |
| Type | Cross-cutting (docs tooling) |
| Feature | pre-handoff-checks |
| Priority | Medium |
| Owner | dev-bot |
| Specs | None; `plan.md` §5.2 |
| Journey (optional) | — |

## User story

**As** a reviewer  
**I want** repeated paragraphs in a target's README and docs flagged automatically  
**So that** duplicated README text (5 of 6 manage-animals rounds) is fixed before review

## Full-stack scope

No UI controls or DB columns. Files: the `docs-dup` check in the runner; optional allowlist entries (rule `docs-dup`).

## Work to do

1. Implement `docs-dup` (in scope now, D8): within one target, split `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/**/*.md`, `.cursor/rules/**/*.mdc` and `.claude/rules/**/*.md` into paragraphs (blank-line separated, code fences excluded); normalise whitespace and case; report any paragraph of at least 25 words (D8) that appears more than once.
2. Known intentional mirrors (e.g. `.cursor/rules/*.mdc` ↔ `.claude/rules/*.md` copies) are handled by an allowlist entry per pair, not by skipping folders silently.
3. Output: the paragraph's first 10 words and every `file:line` where it appears.
4. Full markdownlint stays out of scope (later ticket if Neil wants it).

## Acceptance criteria

### Scenario: S1 — Same paragraph in two docs fails

```gherkin
Given README.md and docs/setup.md in one target both contain the same 30-word paragraph
When the docs-dup check runs
Then it fails
And it lists the paragraph's first 10 words with both file:line locations
```

### Scenario: S2 — Short repeats and code blocks are ignored

```gherkin
Given two docs that share a 10-word sentence and an identical fenced code block
When the docs-dup check runs
Then neither is reported
```

### Scenario: S3 — Whitespace and case differences still match

```gherkin
Given the same paragraph in two files, one wrapped across lines and with different capitalisation
When the docs-dup check runs
Then it is reported as a duplicate
```

### Scenario: S4 — Allowlisted mirror pair passes

```gherkin
Given an allowlist entry for a .cursor/rules/x.mdc and .claude/rules/x.md mirror pair with a reason
When the docs-dup check finds paragraphs repeated only between that pair
Then it passes and reports them as allowlisted
```

Checklist (derived from scenarios):

- [ ] Paragraph threshold (≥ 25 words) and file set per D8
- [ ] Code fences excluded; normalised comparison
- [ ] Mirror pairs allowlisted explicitly

## Out of scope

- markdownlint rules (headings, list style, line length)
- Comparing docs across targets

## Notes

- Stable ID for DevOps upsert: `T-GATE-004`
- In scope now (D8); full markdownlint is a later ticket.
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D8, D13.
