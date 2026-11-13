# Test Bot report — issue 8, round 1

**Head SHA:** not recorded
**Date:** not recorded

| Field | Value |
|-------|-------|
| PR | https://github.com/NeilWoodComputing/AI-framework/pull/8 |
| Head SHA | not recorded |
| Date | not recorded |

Converted from `tests/pr/issue-8/TEST-issue-8-r1-report.md`. Key lines from the original run output:

```text
================================================================================
PR #8 Automated Tests: Align handoff routes with GitHub pipeline
Issue: https://github.com/NeilWoodComputing/ai-framework-tests/issues/8
================================================================================

Testing Criterion 1: Config changes...
Testing Criterion 2: No stale 'Azure-only' phrases...
Testing Criterion 3: Dev Bot GitHub issue pickup...
Testing Criterion 4: Root README describes GitHub flow...
Testing Criterion 5: CI validation...

================================================================================
TEST RESULTS
================================================================================

✓ PASS: handoff.code_to_review is 'pr'
    Found: handoff.code_to_review: pr

✓ PASS: handoff.plan_to_code unchanged ('direct')
    Found: handoff.plan_to_code: direct

✓ PASS: tickets.target unchanged ('azure-devops')
    Found: tickets.target: azure-devops

✗ FAIL: No stale 'Azure-only' or 'GitHub off' phrases
    Found 1 stale phrase(s) in 4 file(s)
    - handoff/README.md:53: Says posting is off until Azure DevOps
      Context: ...reviewing agent reviews the **PR diff**, writes `reviews/PR-<id>-review.md`, posts inline + summary comments to the PR only when `review.publish` allows (provider `azure-devops` only; off until Azure DevOps is in use), and appends a round summary to `reviews/review-log.md`. Needs `review.provider` configu...

✓ PASS: Dev Bot describes GitHub issue pickup and closing keyword
    All 7 required elements found
    - ai-code-framework/AGENT-BRIEF.md line 25: Mentions GitHub issues
    - ai-code-framework/AGENT-BRIEF.md line 25: Shows cross-repo closing keyword format (Closes owner/repo#N)
    - ai-code-framework/AGENT-BRIEF.md line 25: Mentions ai-framework-tests repo
    - ai-code-framework/AGENT-BRIEF.md line 25: Mentions daily sweep for missed issues
    - ai-code-framework/AGENT-BRIEF.md line 25: Mentions implementation via cloud agent
    - ai-code-framework/loops/feature-build.md line 51: Mentions GitHub issues
    - ai-code-framework/loops/feature-build.md line 51: Shows cross-repo closing keyword

✓ PASS: Root README describes GitHub issues and PRs
    All 2 required elements found
    - Mentions GitHub Issues (line ~21)
    - Mentions PRs (line ~9)

✓ PASS: CI passes (run separately)
    This test verifies other CI checks exist; actual CI runs via GitHub Actions

================================================================================
SUMMARY: 6/7 passed, 1/7 failed
================================================================================
```
