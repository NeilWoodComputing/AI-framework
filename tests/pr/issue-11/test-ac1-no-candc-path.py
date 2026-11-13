#!/usr/bin/env python3
"""
Test AC1: Test Bot's brief (ai-test-framework/AGENT-BRIEF.md) does not mention `projects/candc/work`.

Scenario ID: AC1
"""

import sys
from pathlib import Path

def find_repo_root(start=None):
    """Walk up from this file to the folder that holds ai-framework.config.yaml."""
    p = Path(start or __file__).resolve()
    if p.is_file():
        p = p.parent
    for candidate in [p, *p.parents]:
        if (candidate / "ai-framework.config.yaml").is_file():
            return candidate
    raise SystemExit(f"Could not find repository root from {start}")


def test_ac1():
    """Test that AGENT-BRIEF.md does not mention projects/candc/work"""
    repo_root = find_repo_root(__file__)
    brief_path = repo_root / "ai-test-framework" / "AGENT-BRIEF.md"
    
    if not brief_path.exists():
        print(f"FAIL: {brief_path} does not exist")
        return False
    
    content = brief_path.read_text(encoding="utf-8")
    
    if "projects/candc/work" in content:
        print(f"FAIL: Found 'projects/candc/work' in {brief_path}")
        return False
    
    print(f"PASS: No 'projects/candc/work' found in {brief_path}")
    return True

if __name__ == "__main__":
    success = test_ac1()
    sys.exit(0 if success else 1)
