# Changelog

Framework version is in `VERSION` (semantic: major = breaking layout or contract change, minor = new features, patch = fixes).

## 1.0.0 — 2026-11-13

Standardise PR-based framework test location and naming (ai-framework-tests#13). Feature tests are unchanged.

- **Root folder:** `tests/pr/`, with one folder per issue `tests/pr/issue-<N>/` (N is the ai-framework-tests issue number). Config keys: `testing.pr_tests_dir` and `testing.pr_report_names`. The existing `testing.report_names` map for feature tests is unchanged.
- **Names:** test code `test_issue_<N>.py` (or `.sh`), updated in place across rounds; reports `TEST-issue-<N>-r<round>-report.md`. Raw `.txt` / `.json` run output is not committed.
- **Docs:** `AGENT-BRIEF.md` (What you write, and the PR-based workflow line) and this framework's README describe the layout. The PR comment heading is `Test Bot: test results (round <round>)`.
- **CI:** `tests/check-test-layout.py` fails if a `TEST-*report*` or `test_pr*` file sits under `tests/` or `ai-test-framework/` outside `tests/pr/issue-*/` or a feature `tests/` folder. The manage-animals GitHub publishing report stays under the frozen work folder (rule R8) as an explicit exception.
