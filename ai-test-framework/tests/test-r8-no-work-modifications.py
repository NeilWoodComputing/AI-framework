#!/usr/bin/env python3
"""
Test R8: Verify that historical files under ai-planning-framework/work/ were not modified by the PR.

This validates rule R8 from the planning framework.
"""

import sys
import subprocess
from pathlib import Path

def test_r8():
    """Test that no files under work/ were modified"""
    repo_root = Path(__file__).parent.parent.parent
    
    try:
        # Get the list of modified files in the PR branch compared to main
        result = subprocess.run(
            ["git", "diff", "main...HEAD", "--name-only"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"FAIL: git diff command failed: {result.stderr}")
            return False
        
        modified_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        # Check for any files under ai-planning-framework/work/
        work_files = [f for f in modified_files if f.startswith("ai-planning-framework/work/")]
        
        if work_files:
            print(f"FAIL: Found {len(work_files)} modified file(s) under ai-planning-framework/work/:")
            for f in work_files:
                print(f"  - {f}")
            return False
        
        print("PASS: No files under ai-planning-framework/work/ were modified (rule R8 satisfied)")
        return True
        
    except Exception as e:
        print(f"FAIL: Error checking git diff: {e}")
        return False

if __name__ == "__main__":
    success = test_r8()
    sys.exit(0 if success else 1)
