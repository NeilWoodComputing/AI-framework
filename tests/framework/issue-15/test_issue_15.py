#!/usr/bin/env python3
"""Acceptance tests for ai-framework-tests#15: handoff.plan_to_code board route.

Tests live under tests/framework/issue-15/ as specified by Plan Bot.
(PR #14 agreed tests/pr/issue-<N>/ for Test Bot's PR tests; this path was
Plan Bot's choice for the implementation tests of issue 15.)
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def find_repo_root(start=None) -> Path:
    p = Path(start or __file__).resolve()
    if p.is_file():
        p = p.parent
    for candidate in [p, *p.parents]:
        if (candidate / "ai-framework.config.yaml").is_file():
            return candidate
    raise SystemExit(f"Could not find repository root from {start}")


def load_validate_config(repo: Path):
    path = repo / "tests" / "validate-config.py"
    spec = importlib.util.spec_from_file_location("validate_config_issue15", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Result:
    def __init__(self, ac: str, name: str, passed: bool, details: str = "", evidence=None):
        self.ac = ac
        self.name = name
        self.passed = passed
        self.details = details
        self.evidence = evidence or []

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"{status}: [{self.ac}] {self.name}"]
        if self.details:
            lines.append(f"    {self.details}")
        for item in self.evidence:
            lines.append(f"    - {item}")
        return "\n".join(lines)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_plan_to_code_is_board(config, raw: str) -> Result:
    value = (config.get("handoff") or {}).get("plan_to_code")
    if value != "board":
        return Result("AC1", "handoff.plan_to_code is board", False, f"Found: {value!r}")
    comment_ok = "board | direct" in raw and "devops" in raw and "alias" in raw
    if not comment_ok:
        return Result(
            "AC1",
            "handoff.plan_to_code is board",
            False,
            "Value is board, but the inline comment does not list board | direct and the devops alias",
        )
    return Result("AC1", "handoff.plan_to_code is board", True, f"Found: plan_to_code: {value}")


def test_comments_provider_neutral(raw: str) -> Result:
    # Comment block immediately above plan_to_code.
    idx = raw.find("\n  plan_to_code:")
    if idx < 0:
        idx = raw.find("\nplan_to_code:")
    if idx < 0:
        return Result("AC1", "plan_to_code comments are provider-neutral", False, "Could not find plan_to_code")
    block = raw[max(0, idx - 1200) : idx]
    evidence = []
    failures = []
    if "tickets.github" not in block and "tickets.target" not in block:
        failures.append("Comment block does not mention tickets.github or tickets.target")
    else:
        evidence.append("Mentions tickets.github or tickets.target")
    if "devops" not in block.lower() or "alias" not in block.lower():
        failures.append("Comment block does not describe devops as an alias")
    else:
        evidence.append("Describes devops as an alias")
    if "board" not in block:
        failures.append("Comment block does not mention board")
    else:
        evidence.append("Mentions board")
    # The old sole-requirement wording must be gone.
    stale = "no <placeholders> under tickets, and the DevOps connector."
    if stale in block:
        failures.append("Still says the DevOps connector is a hard requirement without a GitHub alternative")
    else:
        evidence.append("No longer requires the DevOps connector as the only access path")
    if "tickets.github" in block:
        evidence.append("GitHub requirements point at the tickets.github block")
    if failures:
        return Result("AC1", "plan_to_code comments are provider-neutral", False, "Issues:", failures)
    return Result("AC1", "plan_to_code comments are provider-neutral", True, "Comment block is provider-neutral", evidence)


def test_approval_kept(config) -> Result:
    approvals = ((config.get("handoff") or {}).get("require_human_approval") or {})
    value = approvals.get("plan_to_code")
    if value is True:
        return Result("AC1", "require_human_approval.plan_to_code stays true", True, "Found: true")
    return Result(
        "AC1",
        "require_human_approval.plan_to_code stays true",
        False,
        f"Expected True, found {value!r}",
    )


def test_docs_flow(repo: Path) -> Result:
    files = {
        "handoff/README.md": [
            ("human owner", "Human plan sign-off"),
            ("board", "Board route"),
            ("ai-framework-tests", "Tickets go to ai-framework-tests"),
            ("Closes NeilWoodComputing/ai-framework-tests#", "Cross-repo Closes keyword"),
            ("direct", "Direct route still described"),
            ("fallback", "Direct is the fallback"),
            ("tickets.github", "GitHub needs the tickets.github block"),
            ("devops", "devops alias mentioned"),
        ],
        "ai-planning-framework/AGENT-BRIEF.md": [
            ("require_human_approval.plan_to_code", "Keeps the plan sign-off step"),
            ("Route `board`", "Board route"),
            ("ai-framework-tests", "GitHub issues in ai-framework-tests"),
            ("deprecated alias", "devops alias"),
            ("Route `direct`", "Direct route"),
            ("fallback", "Direct is the fallback"),
            ("tickets.github", "GitHub requirements"),
        ],
        "ai-code-framework/AGENT-BRIEF.md": [
            ("plan_to_code: board", "Board pickup"),
            ("ai-framework-tests", "Issues in ai-framework-tests"),
            ("Closes NeilWoodComputing/ai-framework-tests#", "Closes keyword"),
            ("deprecated alias", "devops alias"),
            ("fallback", "Direct is the fallback"),
        ],
        "README.md": [
            ("ticket board", "Root README uses provider-neutral board wording"),
            ("ai-framework-tests", "Mentions ai-framework-tests"),
            ("require_human_approval.plan_to_code", "Keeps the plan sign-off"),
            ("fallback", "Direct is the fallback"),
        ],
    }
    failures = []
    evidence = []
    for rel, checks in files.items():
        path = repo / rel
        if not path.is_file():
            failures.append(f"{rel}: missing")
            continue
        content = read(path)
        for snippet, label in checks:
            if snippet not in content:
                # case-insensitive fallback for a few phrases
                if snippet.lower() not in content.lower():
                    failures.append(f"{rel}: missing {label} ({snippet!r})")
                else:
                    evidence.append(f"{rel}: {label}")
            else:
                evidence.append(f"{rel}: {label}")
    if failures:
        return Result("AC2", "Docs and AGENT-BRIEFs describe the board flow", False, "Missing elements:", failures)
    return Result(
        "AC2",
        "Docs and AGENT-BRIEFs describe the board flow",
        True,
        f"All {len(evidence)} expected elements found",
        evidence,
    )


def test_direct_fallback(repo: Path, vc, config) -> Result:
    failures = []
    evidence = []
    # Validator accepts direct
    errs = vc.validate_plan_to_code_value("direct")
    if errs:
        failures.append(f"Validator rejected direct: {errs}")
    else:
        evidence.append("Validator accepts direct")
    if vc.canonicalize_plan_to_code("direct") != "direct":
        failures.append("canonicalize_plan_to_code('direct') is not 'direct'")
    else:
        evidence.append("direct stays canonical")
    if vc.is_board_route("direct"):
        failures.append("is_board_route('direct') should be False")
    else:
        evidence.append("direct is not the board route")
    # Docs
    for rel in (
        "handoff/README.md",
        "ai-planning-framework/AGENT-BRIEF.md",
        "ai-code-framework/AGENT-BRIEF.md",
        "ai-framework.config.yaml",
    ):
        content = read(repo / rel)
        if "fallback" not in content.lower():
            failures.append(f"{rel}: does not describe direct as the fallback")
        else:
            evidence.append(f"{rel}: describes direct as the fallback")
    if failures:
        return Result("AC3", "direct route still works and is the fallback", False, "Issues:", failures)
    return Result("AC3", "direct route still works and is the fallback", True, "direct is accepted and documented as the fallback", evidence)


def test_validator_and_devops_alias(vc, repo: Path, config) -> Result:
    failures = []
    evidence = []
    # Committed config
    errs = vc.validate_framework_config(repo / "ai-framework.config.yaml")
    if errs:
        failures.append(f"Committed config failed validation: {errs}")
    else:
        evidence.append("Committed config (plan_to_code: board) validates")
    # Allowed values
    allowed = set(vc.PLAN_TO_CODE_ALLOWED)
    expected = {"board", "direct", "devops"}
    if allowed != expected:
        failures.append(f"PLAN_TO_CODE_ALLOWED is {allowed}, expected {expected}")
    else:
        evidence.append("Allowed values: board, direct, devops")
    # Alias behaviour
    if vc.canonicalize_plan_to_code("devops") != "board":
        failures.append("canonicalize_plan_to_code('devops') is not 'board'")
    else:
        evidence.append("devops canonicalises to board")
    if vc.canonicalize_plan_to_code("board") != "board":
        failures.append("canonicalize_plan_to_code('board') is not 'board'")
    else:
        evidence.append("board is already canonical")
    if not (vc.is_board_route("devops") and vc.is_board_route("board")):
        failures.append("is_board_route is not True for both devops and board")
    else:
        evidence.append("devops and board are the same route")
    if vc.validate_plan_to_code_value("devops"):
        failures.append(f"Validator rejected devops: {vc.validate_plan_to_code_value('devops')}")
    else:
        evidence.append("Validator accepts devops (deprecated alias)")
    if vc.validate_plan_to_code_value("board"):
        failures.append(f"Validator rejected board: {vc.validate_plan_to_code_value('board')}")
    else:
        evidence.append("Validator accepts board")
    # Invalid rejected
    bad = vc.validate_plan_to_code_value("github")
    if not bad:
        failures.append("Validator accepted 'github' as plan_to_code; only board/direct/devops should pass")
    else:
        evidence.append("Validator rejects 'github' as a plan_to_code value (provider belongs in tickets.target)")
    bad2 = vc.validate_plan_to_code_value("not-a-route")
    if not bad2:
        failures.append("Validator accepted an unknown value")
    else:
        evidence.append("Validator rejects unknown values")
    # Full-file validation with devops: copy config text, swap the value, write temp next to repo so paths resolve
    raw = read(repo / "ai-framework.config.yaml")
    if "plan_to_code: board" not in raw:
        failures.append("Cannot load a devops variant: committed value is not board")
    else:
        import yaml
        data = yaml.safe_load(raw)
        data["handoff"]["plan_to_code"] = "devops"
        errs_dev = []
        vc.validate_plan_to_code_value(data["handoff"]["plan_to_code"], errs_dev)
        if errs_dev:
            failures.append(f"In-memory config with devops failed: {errs_dev}")
        else:
            evidence.append("A config with plan_to_code: devops passes the same plan_to_code validator")
        if vc.is_board_route(data["handoff"]["plan_to_code"]) != vc.is_board_route("board"):
            failures.append("devops in a loaded config is not treated as board")
        else:
            evidence.append("Loaded devops value is treated as the board route")
    if failures:
        return Result("AC4", "Validators accept board; devops alias still works", False, "Issues:", failures)
    return Result("AC4", "Validators accept board; devops alias still works", True, "Alias behaviour matches board", evidence)


def test_version_changelog(repo: Path) -> Result:
    version_path = repo / "ai-planning-framework" / "VERSION"
    changelog_path = repo / "ai-planning-framework" / "CHANGELOG.md"
    version = read(version_path).strip()
    changelog = read(changelog_path)
    failures = []
    evidence = []
    if version != "1.3.0":
        failures.append(f"VERSION is {version!r}, expected '1.3.0'")
    else:
        evidence.append("VERSION is 1.3.0")
    if "## 1.3.0" not in changelog:
        failures.append("CHANGELOG.md has no 1.3.0 heading")
    else:
        evidence.append("CHANGELOG has a 1.3.0 heading")
    # The new section should mention the board route before the previous 1.2.0 section.
    idx_new = changelog.find("## 1.3.0")
    idx_old = changelog.find("## 1.2.0")
    if idx_new < 0 or idx_old < 0 or idx_new > idx_old:
        failures.append("1.3.0 section is missing or is not above 1.2.0")
    else:
        section = changelog[idx_new:idx_old]
        for snippet, label in (
            ("plan_to_code", "mentions plan_to_code"),
            ("board", "mentions board"),
            ("devops", "mentions devops alias"),
            ("tickets.github", "mentions tickets.github"),
            ("direct", "mentions direct fallback"),
        ):
            if snippet not in section:
                failures.append(f"1.3.0 changelog section missing {label}")
            else:
                evidence.append(f"Changelog: {label}")
    if failures:
        return Result("AC5", "VERSION bumped and changelog updated", False, "Issues:", failures)
    return Result("AC5", "VERSION bumped and changelog updated", True, "1.3.0 recorded", evidence)


def test_branch_pattern(config) -> Result:
    bp = (config.get("handoff") or {}).get("branch_pattern") or {}
    board = bp.get("board")
    devops = bp.get("devops")
    direct = bp.get("direct")
    if not board:
        return Result("AC1", "branch_pattern.board is present", False, f"branch_pattern={bp}")
    if board != devops:
        return Result(
            "AC4",
            "branch_pattern.devops aliases board",
            False,
            f"board={board!r} devops={devops!r}",
        )
    if not direct or "ticket-id" not in str(direct):
        return Result("AC3", "branch_pattern.direct still present", False, f"direct={direct!r}")
    return Result(
        "AC4",
        "branch_pattern.board exists and devops is the same pattern",
        True,
        f"board=devops={board!r}; direct={direct!r}",
    )



def test_no_stale_devops_direct_route_list(repo: Path) -> Result:
    """F-T15-01: living docs must list plan_to_code as board | direct, not devops | direct."""
    failures = []
    evidence = []
    loop = repo / "ai-planning-framework" / "loops" / "feature-planning.md"
    content = read(loop)
    if "approval + devops | direct" in content:
        failures.append("feature-planning.md still has 'approval + devops | direct' on the stage-7 overview")
    if "board | direct" not in content:
        failures.append("feature-planning.md does not list 'board | direct'")
    else:
        evidence.append("feature-planning.md lists 'board | direct'")
    if "deprecated alias" not in content:
        failures.append("feature-planning.md no longer mentions devops as a deprecated alias")
    else:
        evidence.append("feature-planning.md still mentions devops as a deprecated alias")

    stale = "devops | direct"
    skip_parts = {".git", "node_modules", "__pycache__", ".next", "bin", "obj"}
    skip_prefixes = (
        "ai-planning-framework/work/",
        "tests/pr/",
    )
    text_suffixes = {".md", ".yaml", ".yml", ".py", ".sh", ".ps1", ".txt", ".json"}
    offenders = []
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        try:
            rel = path.relative_to(repo).as_posix()
        except ValueError:
            continue
        if rel.startswith(skip_prefixes):
            continue
        # This test file itself quotes the stale phrase; skip it.
        if rel == "tests/framework/issue-15/test_issue_15.py":
            continue
        if path.suffix.lower() not in text_suffixes:
            continue
        try:
            text = read(path)
        except (UnicodeDecodeError, OSError):
            continue
        if stale in text:
            # Report line numbers
            for i, line in enumerate(text.splitlines(), 1):
                if stale in line:
                    offenders.append(f"{rel}:{i}: {line.strip()}")
    if offenders:
        failures.append("Stale 'devops | direct' still present in living files:")
        failures.extend(offenders)
    else:
        evidence.append("No living file (excluding work/ and tests/pr/) contains 'devops | direct'")

    if failures:
        return Result(
            "AC2",
            "No stale 'devops | direct' route list in living docs (F-T15-01)",
            False,
            "Issues:",
            failures,
        )
    return Result(
        "AC2",
        "No stale 'devops | direct' route list in living docs (F-T15-01)",
        True,
        "Stage-7 overview lists board | direct; no leftover 'devops | direct'",
        evidence,
    )



def main() -> int:
    repo = find_repo_root(__file__)
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 80)
    print("Issue 15 tests: handoff.plan_to_code board route")
    print("https://github.com/NeilWoodComputing/ai-framework-tests/issues/15")
    print(f"Repo: {repo}")
    print("=" * 80)
    print()

    import yaml

    raw = read(repo / "ai-framework.config.yaml")
    config = yaml.safe_load(raw)
    vc = load_validate_config(repo)

    results = [
        test_plan_to_code_is_board(config, raw),
        test_comments_provider_neutral(raw),
        test_approval_kept(config),
        test_docs_flow(repo),
        test_no_stale_devops_direct_route_list(repo),
        test_direct_fallback(repo, vc, config),
        test_validator_and_devops_alias(vc, repo, config),
        test_version_changelog(repo),
        test_branch_pattern(config),
    ]

    for r in results:
        print(r)
        print()

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    print("=" * 80)
    print(f"SUMMARY: {passed}/{len(results)} passed, {failed}/{len(results)} failed")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
