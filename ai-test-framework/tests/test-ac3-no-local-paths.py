#!/usr/bin/env python3
r"""
Test AC3: No living test-framework doc (anywhere under ai-test-framework, outside any work/ folder)
contains `D:\Users\nwood01` (case-insensitive, also check forward-slash variants).

Scenario ID: AC3
"""

import sys
from pathlib import Path
import re

def test_ac3():
    r"""Test that no living test-framework docs contain D:\Users\nwood01 paths"""
    repo_root = Path(__file__).parent.parent.parent
    test_framework_dir = repo_root / "ai-test-framework"
    
    if not test_framework_dir.exists():
        print(f"FAIL: {test_framework_dir} does not exist")
        return False
    
    # Patterns to search for (case-insensitive)
    patterns = [
        r"D:\\Users\\nwood01",
        r"D:/Users/nwood01",
    ]
    
    failures = []
    
    # Search all files under ai-test-framework, excluding work/ folders and tests/ folder
    for filepath in test_framework_dir.rglob("*"):
        # Skip directories
        if not filepath.is_file():
            continue
        
        # Skip if inside any work/ folder
        if "/work/" in str(filepath) or "\\work\\" in str(filepath):
            continue
        
        # Skip the tests directory itself (these are test files, not living docs)
        if "/tests/" in str(filepath) or "\\tests\\" in str(filepath):
            continue
        
        # Skip binary and generated files
        if filepath.suffix in ['.pyc', '.pyo', '.so', '.dll', '.exe']:
            continue
        
        try:
            content = filepath.read_text(encoding="utf-8")
            
            # Check each pattern (case-insensitive)
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    failures.append(str(filepath.relative_to(repo_root)))
                    break
        except (UnicodeDecodeError, PermissionError):
            # Skip files that can't be read as text
            continue
    
    if failures:
        print(f"FAIL: Found D:\\Users\\nwood01 references in the following files:")
        for f in failures:
            print(f"  - {f}")
        return False
    
    print(f"PASS: No D:\\Users\\nwood01 paths found in living test-framework docs")
    return True

if __name__ == "__main__":
    success = test_ac3()
    sys.exit(0 if success else 1)
