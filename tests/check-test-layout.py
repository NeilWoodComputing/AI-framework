#!/usr/bin/env python3
"""Fail if a PR-style test report or test_pr* file sits outside the agreed layout.

Allowed locations:
  - tests/pr/issue-<N>/
  - a feature tests folder (work/<feature>/tests/)
  - the explicit R8 exception:
    ai-planning-framework/work/manage-animals/tests/TEST-github-publishing-1-report.md
"""
from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

R8_EXCEPTION = Path(
    "ai-planning-framework/work/manage-animals/tests/TEST-github-publishing-1-report.md"
)
PATTERNS = ("TEST-*report*", "test_pr*")
# Directories that are always skipped.
SKIP_PARTS = {".git", "node_modules", "__pycache__", ".next", "bin", "obj"}


def is_allowed(rel: Path) -> bool:
    posix = rel.as_posix()
    if rel == R8_EXCEPTION or posix == R8_EXCEPTION.as_posix():
        return True
    parts = rel.parts
    # tests/pr/issue-<N>/...
    if (
        len(parts) >= 3
        and parts[0] == "tests"
        and parts[1] == "pr"
        and parts[2].startswith("issue-")
    ):
        return True
    # Feature tests: .../work/<feature>/tests/...
    for i, part in enumerate(parts):
        if part == "work" and i + 2 < len(parts) and parts[i + 2] == "tests":
            return True
    return False


def matches_pattern(name: str) -> bool:
    # fnmatch is case-insensitive on Windows; the agreed patterns are case-sensitive.
    return any(fnmatch.fnmatchcase(name, pat) for pat in PATTERNS)


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    roots = [repo / "tests", repo / "ai-test-framework"]
    # Also look at the R8 path so the exception is explicit, and at work/ tests
    # so a misplaced report there is judged against the allow list.
    extra = [repo / "ai-planning-framework" / "work"]
    offenders = []
    seen = set()

    def consider(path: Path) -> None:
        if not path.is_file():
            return
        try:
            rel = path.relative_to(repo)
        except ValueError:
            return
        key = rel.as_posix()
        if key in seen:
            return
        seen.add(key)
        if not matches_pattern(path.name):
            return
        if not is_allowed(rel):
            offenders.append(key)

    for root in roots + extra:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            consider(path)

    # Explicitly consider the R8 file (must not fail).
    r8 = repo / R8_EXCEPTION
    if r8.exists():
        consider(r8)

    if offenders:
        print("Test layout check failed. These files match TEST-*report* or test_pr*")
        print("but are not under tests/pr/issue-*/, a feature tests/ folder, or the R8 exception:")
        for item in offenders:
            print(f"  - {item}")
        return 1

    print("Test layout check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
