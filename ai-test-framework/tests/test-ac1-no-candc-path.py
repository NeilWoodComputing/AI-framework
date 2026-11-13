#!/usr/bin/env python3
"""
Test AC1: Test Bot's brief (ai-test-framework/AGENT-BRIEF.md) does not mention `projects/candc/work`.

Scenario ID: AC1
"""

import sys
from pathlib import Path

def test_ac1():
    """Test that AGENT-BRIEF.md does not mention projects/candc/work"""
    repo_root = Path(__file__).parent.parent.parent
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
