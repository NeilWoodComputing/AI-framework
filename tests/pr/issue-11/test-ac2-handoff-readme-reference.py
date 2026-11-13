#!/usr/bin/env python3
"""
Test AC2: Test Bot's brief points to `handoff/README.md` for the shared editing rules,
and that README actually contains the 'Shared editing rules' section the brief refers to.

Scenario ID: AC2
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


def test_ac2():
    """Test that AGENT-BRIEF.md references handoff/README.md and that section exists"""
    repo_root = find_repo_root(__file__)
    brief_path = repo_root / "ai-test-framework" / "AGENT-BRIEF.md"
    handoff_readme_path = repo_root / "handoff" / "README.md"
    
    if not brief_path.exists():
        print(f"FAIL: {brief_path} does not exist")
        return False
    
    if not handoff_readme_path.exists():
        print(f"FAIL: {handoff_readme_path} does not exist")
        return False
    
    brief_content = brief_path.read_text(encoding="utf-8")
    handoff_content = handoff_readme_path.read_text(encoding="utf-8")
    
    # Check that AGENT-BRIEF.md points to handoff/README.md for shared editing rules
    if "../handoff/README.md" not in brief_content:
        print(f"FAIL: AGENT-BRIEF.md does not reference ../handoff/README.md")
        return False
    
    # Check that it mentions "Shared editing rules"
    if "Shared editing rules" not in brief_content:
        print(f"FAIL: AGENT-BRIEF.md does not mention 'Shared editing rules'")
        return False
    
    # Check that handoff/README.md contains the "Shared editing rules (all bots)" section
    if "## Shared editing rules (all bots)" not in handoff_content:
        print(f"FAIL: handoff/README.md does not contain '## Shared editing rules (all bots)' section")
        return False
    
    # Verify the section is around lines 105-111 as referenced
    lines = handoff_content.split('\n')
    found_at_line = None
    for i, line in enumerate(lines, 1):
        if "## Shared editing rules (all bots)" in line:
            found_at_line = i
            break
    
    if found_at_line is None:
        print(f"FAIL: Could not find the section heading")
        return False
    
    # Check it's approximately at the referenced line range (105-111)
    if not (100 <= found_at_line <= 115):
        print(f"WARNING: Section found at line {found_at_line}, brief references lines 105-111")
    
    print(f"PASS: AGENT-BRIEF.md correctly references handoff/README.md, and the 'Shared editing rules (all bots)' section exists at line {found_at_line}")
    return True

if __name__ == "__main__":
    success = test_ac2()
    sys.exit(0 if success else 1)
