#!/usr/bin/env python3
"""
check.py: verify ai-review-framework. Exit code 0 = all checks pass.

    py tools/check.py            # Windows (from the ai-review-framework folder)
    python3 tools/check.py

Checks:
  files     the API index, both API checklists and the report template exist,
            and the template still has the sections the loop requires
  paths     no doc still sends new features to the old per-project work folder
  terms     project-specific names stay out of the generic docs
            (stack checklists may name their own stack)

Reads only. No dependencies beyond Python 3.10+.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

FW = Path(__file__).resolve().parent.parent

REQUIRED = [
    "checklists/api-checklist.md",
    "checklists/api-csharp-checklist.md",
    "checklists/api-framework-checklist.md",
    "checklists/ui-nextjs-checklist.md",
    "checklists/ui-angular-checklist.md",
    "templates/review-report.md",
    "loops/pr-review.md",
]
REPORT_HEADINGS = [
    "## Verdict",
    "## Review scope",
    "## Findings",
    "## Spec conformance",
    "## Data mapping",
    "## Acceptance criteria coverage",
    "Execution (required",
]
CONFIG = FW.parent / "ai-framework.config.yaml"
# Stack checklists describe one codebase, so its own names are expected there.
STACK_FILES = {
    "checklists/api-csharp-checklist.md",
    "checklists/api-framework-checklist.md",
    "checklists/security-checklist.md",
}
TERMS = [
    (re.compile(r"\bCandC\b"), "a project name"),
    (re.compile(r"\bNeil\b"), "a person's name"),
    (re.compile(r"\breview-bot\b"), "a hardcoded agent id; use agents.review.id"),
    (re.compile(r"\bdev-bot\b"), "a hardcoded agent id; use agents.code.id"),
    (re.compile(r"projects/candc/work"), "the old per-project work folder"),
    (re.compile(r"add-edit-contact"), "a project feature"),
]
STALE = ["projects/candc/work", "ai-planning-framework/projects/"]


def rel(p: Path) -> str:
    return p.relative_to(FW).as_posix()


def main() -> int:
    errors: list[str] = []

    for name in REQUIRED:
        if not (FW / name).is_file():
            errors.append(f"files: missing {name}")
    report = FW / "templates" / "review-report.md"
    if report.is_file():
        text = report.read_text(encoding="utf-8")
        for heading in REPORT_HEADINGS:
            if heading not in text:
                errors.append(f"files: templates/review-report.md has no {heading}")
    index = FW / "checklists" / "api-checklist.md"
    if index.is_file():
        idx = index.read_text(encoding="utf-8")
        for name in ("api-csharp-checklist.md", "api-framework-checklist.md"):
            if name not in idx:
                errors.append(f"files: api-checklist.md does not point at {name}")

    for p in sorted(FW.rglob("*.md")):
        name = rel(p)
        text = p.read_text(encoding="utf-8")
        for stale in STALE:
            if stale in text:
                errors.append(f"paths: {name} still mentions {stale}")
        if name in STACK_FILES:
            continue
        for rx, why in TERMS:
            if rx.search(text):
                line = text[: rx.search(text).start()].count("\n") + 1
                errors.append(f"terms: {name}:{line} {rx.pattern} ({why})")

    skill = FW / "skills" / "review-tests" / "SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text(encoding="utf-8")
        if "Optionally, if the agent" in skill_text or "**Required run.**" not in skill_text:
            errors.append("tests: review-tests does not require the unit run")
        if "blocked_tests_allow_approval` is `false`" not in skill_text:
            errors.append("tests: review-tests still allows approval when testing is blocked")
    if CONFIG.is_file():
        if "blocked_tests_allow_approval: false" not in CONFIG.read_text(encoding="utf-8"):
            errors.append("tests: ai-framework.config.yaml blocked_tests_allow_approval is not false")
    else:
        errors.append("tests: ai-framework.config.yaml not found")

    print(f"{'FAIL' if errors else 'PASS'}  review-framework  errors={len(errors)}")
    for msg in errors:
        print(f"      ERROR  {msg}")
    print("RESULT: " + ("FAIL" if errors else "PASS"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
