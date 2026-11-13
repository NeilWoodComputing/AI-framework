# Test report — GitHub ticket publishing — run 1

| Field | Value |
|-------|-------|
| Run | 1 · 2026-11-13 15:48 GMT · test-bot |
| Why this run | Testing PR #6 against issue #2 acceptance criteria |
| Feature | GitHub ticket publishing adapter (manage-animals dry-run example) |
| PR under test | https://github.com/NeilWoodComputing/AI-framework/pull/6 |
| Issue | https://github.com/NeilWoodComputing/ai-framework-tests/issues/2 |
| Branch | cursor/github-ticket-publishing-450c |
| Head commit | 17cda010efa894a533b56edd8c2ac6f6ec378904 |
| Test type | Documentation and configuration validation |
| Environment | Cloud Agent VM · Python 3.x · git 2.x |
| Commands | `python3 ai-planning-framework/tools/check.py`, encoding checks, diff analysis, pattern matching |
| Result | **PASS** |

Times: Europe/London local time, labelled GMT or BST for that date.

## Summary

Tested PR #6 (GitHub ticket publishing adapter) against all 7 acceptance criteria from issue NeilWoodComputing/ai-framework-tests#2. All checks passed. The framework validation (`check.py`) passes with 2 expected profile warnings (framework_version 1.1 vs VERSION 1.2.0, which will be updated separately). The dry-run plan demonstrates complete field mapping with correct title format, labels, acceptance criteria sections, and upsert decisions. No secrets, tokens or local paths were added. All files use UTF-8 encoding without BOM and consistent LF line endings.

## Test results by acceptance criterion

| Criterion | Status | Evidence |
|-----------|--------|----------|
| AC1: `adapters/github.md` complete, no longer marked as stub | **Pass** | File contains full field mapping documentation (title format, body structure, labels, sub-issues, upsert, authentication). No occurrence of "stub" in the file. Lines 1-144 document all requirements. |
| AC2: Config has `tickets.github` block and `tickets.target: github` | **Pass** | Config lines 271-276: `tickets.github` with `owner: NeilWoodComputing`, `repository: ai-framework-tests`, `project: AI testing`, `default_labels: [ai-planning-framework]`. Line 260: `tickets.target: github`. Line 257: `tickets.enabled: true`. No placeholders remain under active target. |
| AC3: `py ai-planning-framework/tools/check.py` passes | **Pass** | Exit code 0, `RESULT: PASS (framework 1.2.0)`. Schema: 17 warnings (unchanged from main). Profiles: 2 warnings (framework_version 1.1 vs 1.2.0 — expected, to be updated separately per PR description). All other sections: 0 errors, 0 warnings. |
| AC4: Dry-run publish plan demonstrates complete mapping | **Pass** | Plan at `work/manage-animals/devops/publish-plan-github-dry-run.md`: 9 tickets acknowledged in upsert table (all CREATE), 3 detailed examples with correct title format `[T-ANIMAL-NNN] <title> (<page type>)`, labels (stable ID + feature slug + page type + ai-planning-framework), acceptance criteria sections with checkable S-numbered bullets, source footers with GitHub links. All linked files exist. No real issues created (dry-run mode documented). |
| AC5: Cross-repo closing keyword documented | **Pass** | `handoff/README.md` line 167+: New "Cross-repo workflows" section documents `Closes NeilWoodComputing/ai-framework-tests#N` format with explanation of cross-repo linking. |
| AC6: No secrets, tokens or local PC paths added | **Pass** | Diff analysis: only env var **names** appear (`secrets.github_token_env`), never values. No occurrence of `C:\Users` or `D:\Users`. All paths are workspace-relative or GitHub URLs. |
| AC7: VERSION and CHANGELOG updated | **Pass** | VERSION bumped from 1.1.4 to 1.2.0 (minor: new feature). CHANGELOG.md has entry dated 2026-11-13 documenting GitHub adapter completion, config changes, cross-repo workflows, docs updates, and authentication approach. Entry is consistent with VERSION. |

### Check.py detailed results

```
PASS  schema    errors=0 warnings=17
PASS  profiles  errors=0 warnings=2
      warn   projects/_template/project.yaml: framework_version 1.1 but VERSION is 1.2.0
      warn   project.yaml: framework_version 1.1 but VERSION is 1.2.0
PASS  golden    errors=0 warnings=0
PASS  stored    errors=0 warnings=0
PASS  layout    errors=0 warnings=0
PASS  starter   errors=0 warnings=0
PASS  encoding  errors=0 warnings=0
PASS  terms     errors=0 warnings=0
PASS  slugs     errors=0 warnings=0
PASS  crossref  errors=0 warnings=0
RESULT: PASS  (framework 1.2.0)
```

**Warning comparison with main:**
- Schema warnings: 17 on both branches (unchanged, from legacy test cases)
- Profile warnings: 0 on main, 2 on PR branch (expected: framework_version will be updated in profiles separately)

### Dry-run plan verification

Verified against `ai-planning-framework/work/manage-animals/devops/publish-plan-github-dry-run.md`:

- ✓ All 9 manage-animals tickets acknowledged in upsert decisions table
- ✓ Detailed examples for T-ANIMAL-001, T-ANIMAL-002, T-ANIMAL-004
- ✓ Title format: `[T-ANIMAL-NNN] <title> (<page type>)` — all 3 examples correct
- ✓ Labels on all examples: stable ID + `manage-animals` + page type (`schema`, `api-service`, `form-modal`) + `ai-planning-framework`
- ✓ Acceptance criteria sections: 3 sections with S-numbered checkable bullets (7, 7, and 12 scenarios respectively)
- ✓ Upsert decisions: all 9 tickets marked CREATE (correct for dry-run with no existing issues)
- ✓ Source footers: links to specs and excel files in GitHub (10 links total)
- ✓ All linked files exist on the branch
- ✓ Dry-run mode clearly documented in plan notes

### Encoding and line endings

All changed files verified:

| File | Encoding | Line endings | BOM |
|------|----------|--------------|-----|
| ai-framework.config.yaml | UTF-8 | LF | None |
| handoff/README.md | UTF-8 | LF | None |
| ai-planning-framework/skills/publish-tickets/adapters/github.md | UTF-8 | LF | None |
| ai-planning-framework/VERSION | ASCII/UTF-8 | LF | None |
| ai-planning-framework/CHANGELOG.md | UTF-8 | LF | None |
| ai-planning-framework/skills/publish-tickets/SKILL.md | UTF-8 | LF | None |
| ai-planning-framework/README.md | UTF-8 | LF | None |
| ai-planning-framework/work/manage-animals/devops/publish-plan-github-dry-run.md | UTF-8 | LF | None |

✓ All files: UTF-8 without BOM, consistent LF line endings, no mixed line endings

### Security scan

Diff analysis for secrets and local paths:

```
Searched for: github_token, azure_devops_pat, password, secret, api_key, C:\Users, D:\Users
```

**Findings:** Only env var names appear in documentation (e.g., `secrets.github_token_env`), never values. No secrets, tokens, or local PC paths added.

## Files changed

All changes are in the AI-framework repository:

1. **ai-framework.config.yaml** (shared file) — added `tickets.github` block, set `target: github`, `enabled: true`
2. **handoff/README.md** (shared file) — added cross-repo workflows section
3. **ai-planning-framework/skills/publish-tickets/adapters/github.md** — completed adapter documentation
4. **ai-planning-framework/skills/publish-tickets/SKILL.md** — updated status table
5. **ai-planning-framework/README.md** — mentioned GitHub as complete adapter
6. **ai-planning-framework/VERSION** — bumped to 1.2.0
7. **ai-planning-framework/CHANGELOG.md** — added 1.2.0 entry
8. **ai-planning-framework/work/manage-animals/devops/publish-plan-github-dry-run.md** (new) — dry-run demonstration

Total: 8 files (2 shared, 6 planning framework, 1 new dry-run artefact)

## Test approach

This is a documentation and configuration change (no executable code), so testing focused on:

1. **Schema validation** — `check.py` validates all framework schemas, profiles, and layout
2. **Pattern verification** — systematic checks of the dry-run plan structure against adapter requirements
3. **Configuration completeness** — verified no placeholders remain under active target
4. **Documentation accuracy** — cross-referenced adapter doc, SKILL.md, and config
5. **Security** — diff scan for secrets, tokens, and local paths
6. **Encoding** — UTF-8 without BOM verification, line ending consistency check

Not automated:
- **Live GitHub API calls** — correctly excluded (dry-run only rule)
- **Actual issue creation** — out of scope per issue requirements
- **GitHub Projects board integration** — requires live access

## Compliance with test rules

✓ No real GitHub issues, labels or project items created (dry-run only)
✓ No changes to app, framework or docs files outside clearly documented additions
✓ No secrets in commits, comments or logs
✓ Check.py run and results recorded
✓ All acceptance criteria verified

## Notes

1. The 2 profile warnings (`framework_version 1.1` vs `VERSION 1.2.0`) are expected and documented in the PR description: "The 2 profile warnings are expected (framework_version will be updated separately in profiles)."

2. The dry-run plan shows detailed examples for 3 of 9 tickets, which is reasonable for a demonstration. All 9 tickets are acknowledged in the upsert decisions table.

3. The adapter uses the authentication priority documented in `adapters/github.md`: (1) connected GitHub connector where available, (2) env var named by `secrets.github_token_env`, (3) dry-run only if neither exists.

## For Review Bot

All 7 acceptance criteria: **Pass**

Ready for Review Bot's test review.
