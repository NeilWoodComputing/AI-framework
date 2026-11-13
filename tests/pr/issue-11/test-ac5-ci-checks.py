#!/usr/bin/env python3
"""
Test AC5: CI and leftover-terms check pass - run the repo's check
(tools/check.py or whatever CI runs) and report result.

Scenario ID: AC5
"""

import sys
import subprocess
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


def test_ac5():
    """Test that CI checks pass"""
    repo_root = find_repo_root(__file__)
    
    # Check for planning framework check.py
    planning_check = repo_root / "ai-planning-framework" / "tools" / "check.py"
    
    if not planning_check.exists():
        print(f"FAIL: {planning_check} does not exist")
        return False
    
    # Run the check from ai-planning-framework directory
    planning_dir = repo_root / "ai-planning-framework"
    
    try:
        # Determine python command
        python_cmd = sys.executable
        
        result = subprocess.run(
            [python_cmd, "tools/check.py"],
            cwd=planning_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("=== check.py output ===")
        print(result.stdout)
        if result.stderr:
            print("=== stderr ===")
            print(result.stderr)
        
        # Check for PASS in output
        if "RESULT: PASS" in result.stdout:
            print("\nPASS: check.py returned RESULT: PASS")
            return True
        else:
            print(f"\nFAIL: check.py did not return RESULT: PASS (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print("FAIL: check.py timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"FAIL: Error running check.py: {e}")
        return False

if __name__ == "__main__":
    success = test_ac5()
    sys.exit(0 if success else 1)
