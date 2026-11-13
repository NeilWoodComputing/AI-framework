# Test Bot report — issue 11, round 1

**Head SHA:** not recorded
**Date:** not recorded

| Field | Value |
|-------|-------|
| PR | https://github.com/NeilWoodComputing/AI-framework/pull/9 |
| Head SHA | not recorded |
| Date | not recorded |

Converted from `tests/pr/issue-11/TEST-issue-11-r1-report.md`. Key lines from the original run output:

```text
PR #9 Test Report - Fix stale Test Bot brief
================================================================================

AC1: Test Bot's brief does not mention projects/candc/work
Status: PASS

Output:
PASS: No 'projects/candc/work' found in /agent/repos/AI-framework/ai-test-framework/AGENT-BRIEF.md

--------------------------------------------------------------------------------

AC2: Test Bot's brief points to handoff/README.md for shared editing rules
Status: PASS

Output:
PASS: AGENT-BRIEF.md correctly references handoff/README.md, and the 'Shared editing rules (all bots)' section exists at line 105

--------------------------------------------------------------------------------

AC3: No living test-framework doc contains D:\Users\nwood01
Status: PASS

Output:
PASS: No D:\Users\nwood01 paths found in living test-framework docs

--------------------------------------------------------------------------------

AC4: CandC examples are clearly labelled
Status: PASS

Output:
PASS: All CandC examples are clearly labelled

--------------------------------------------------------------------------------

AC5: CI and leftover-terms check pass
Status: PASS

Output:
=== check.py output ===
PASS  schema    errors=0 warnings=17
      warn   tests/cases/legacy-names.yaml: deprecated field page_type: Modal (use Embedded Grid Modal)
      warn   tests/cases/legacy-names.yaml: deprecated field unity_feature
      warn   tests/cases/legacy-names.yaml: deprecated field primary_action
      ... 14 more warnings (-v to list)
PASS  profiles  errors=0 warnings=0
PASS  golden    errors=0 warnings=0
PASS  stored    errors=0 warnings=0
PASS  layout    errors=0 warnings=0
PASS  starter   errors=0 warnings=0
PASS  encoding  errors=0 warnings=0
PASS  terms     errors=0 warnings=0
PASS  slugs     errors=0 warnings=0
PASS  crossref  errors=0 warnings=0
RESULT: PASS  (framework 1.1.4)


PASS: check.py returned RESULT: PASS

--------------------------------------------------------------------------------

R8: No files under ai-planning-framework/work/ modified
Status: PASS

Output:
PASS: No files under ai-planning-framework/work/ were modified (rule R8 satisfied)

--------------------------------------------------------------------------------

LINKS: Links in changed files resolve
Status: PASS

Output:
PASS: All file links in 4 changed markdown file(s) resolve

--------------------------------------------------------------------------------


Summary: 7 PASS, 0 FAIL, 0 BLOCKED out of 7 total
```
