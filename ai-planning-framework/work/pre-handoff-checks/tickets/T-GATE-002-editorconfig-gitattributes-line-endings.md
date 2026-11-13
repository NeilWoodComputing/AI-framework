# Ticket: T-GATE-002 — .editorconfig / .gitattributes and one-off line-ending normalisation (both targets)

| Field | Value |
|-------|--------|
| ID | T-GATE-002 |
| Type | Cross-cutting (repository hygiene) |
| Feature | pre-handoff-checks |
| Priority | High |
| Owner | dev-bot |
| Specs | None; `plan.md` §5.3 |
| Journey (optional) | — |

## User story

**As** a reviewer of API.Framework and UI.NextJs.Framework  
**I want** one line-ending, final-newline and encoding rule per target, written down and checked  
**So that** mixed CRLF / LF files stop showing up as review findings

## Full-stack scope

No UI controls or DB columns. Files: `.editorconfig` and `.gitattributes` in `ai-code-framework/api/API.Framework/` and `ai-code-framework/ui/UI.NextJs.Framework/`; existing text files rewritten for line endings / BOM only.

## Work to do

1. Add `.editorconfig` (`root = true`) in each target: `charset = utf-8` without BOM (D7), `end_of_line = crlf` in API.Framework and `lf` in UI.NextJs.Framework (D5), `insert_final_newline = true`, `trim_trailing_whitespace = true` except `*.md`; `*.ps1` / `*.cmd` / `*.bat` CRLF.
2. Add `.gitattributes` in each target matching `.editorconfig` (`* text=auto`, explicit `eol=` per type, images / fonts / `*.xlsx` / `*.pfx` as `binary`). Inert until the target is a git repo (note it in the file header).
3. Provide the `eol` check used by the runner (T-GATE-005): reports files whose line endings, final newline or BOM differ from the target's rule.
4. One-off normalisation (D12): only when no feature is `in-development` / `in-review` with open Dev Bot work; rewrite line endings / BOM only; verify byte-level that nothing else changed; record counts in `handoff.md`.

## Acceptance criteria

### Scenario: S1 — Each target declares its rule

```gherkin
Given API.Framework and UI.NextJs.Framework
When I open each target's .editorconfig and .gitattributes
Then end_of_line is crlf in API.Framework and lf in UI.NextJs.Framework, charset is utf-8 without BOM, and insert_final_newline is true
And .gitattributes eol settings match .editorconfig for the same file types
And *.ps1, *.cmd and *.bat are CRLF in both targets
```

### Scenario: S2 — The check finds a wrong line ending

```gherkin
Given a file in a target whose line endings differ from that target's end_of_line
When the eol check runs
Then it fails and lists the file with the expected and found line endings
```

### Scenario: S3 — The check finds a mixed file, a missing final newline and a BOM

```gherkin
Given one file with mixed CRLF and LF, one with no final newline, and one with a UTF-8 BOM where the rule says no BOM
When the eol check runs
Then it fails and lists all three files with the reason for each
```

### Scenario: S4 — Excluded paths are skipped

```gherkin
Given files with wrong line endings under bin, obj, node_modules, .next* or a .env* file
When the eol check runs
Then none of them are reported and no .env* file is opened
```

### Scenario: S5 — Normalisation changes only line endings and BOM

```gherkin
Given the current files in both targets
When the one-off normalisation runs
Then every text file matches its target's rule
And for every changed file the content is identical after normalising line endings and stripping the BOM
And the counts of changed files per target and type are recorded in handoff.md
```

### Scenario: S6 — Clean after normalisation

```gherkin
Given both targets after normalisation
When the eol check runs on the whole target
Then it passes
```

Checklist (derived from scenarios):

- [ ] `.editorconfig` + `.gitattributes` in both targets, consistent with each other
- [ ] `eol` check reports wrong / mixed endings, missing final newline, BOM
- [ ] Normalisation done once, while idle, with a byte-level "only endings / BOM changed" check

## Out of scope

- Reformatting code (indentation, quotes)
- Unity.API and UI.Angular.Framework
- Creating git repos

## Notes

- Stable ID for DevOps upsert: `T-GATE-002`
- Today (2026-10-09): API.Framework `.cs` 148 CRLF / 6 LF, 15 with BOM; `.md`/`.mdc` 19 CRLF / 18 LF / 3 mixed. UI.NextJs.Framework `.ts`/`.tsx` 138 CRLF / 30 LF; `.md`/`.mdc`/`.feature`/`.mjs` mostly LF. Neil's git `core.autocrlf = true`; Unity.API `.gitattributes` is `* text=auto`.
- Churn: with D5's split, ~170 UI files and ~27 API files change on disk. No git diff noise today (not repos); concurrent edits are the real risk.
- Decisions (Neil, 2026-10-09 10:32 BST, accepted defaults; plan.md §6): D5, D7, D12, D14, D17.
