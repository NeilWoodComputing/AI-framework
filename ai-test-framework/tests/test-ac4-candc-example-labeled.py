#!/usr/bin/env python3
"""
Test AC4: Any remaining CandC example (e.g. examples/manage-animals-test-plan.md)
is clearly labelled as CandC-specific near the top.

Scenario ID: AC4
"""

import sys
from pathlib import Path

def test_ac4():
    """Test that CandC examples are clearly labelled"""
    repo_root = Path(__file__).parent.parent.parent
    examples_dir = repo_root / "ai-test-framework" / "examples"
    
    if not examples_dir.exists():
        print(f"FAIL: {examples_dir} does not exist")
        return False
    
    # Known CandC-specific examples
    candc_examples = [
        "manage-animals-test-plan.md",
        "unity-ui-e2e-reference.md"
    ]
    
    failures = []
    
    for example_name in candc_examples:
        example_path = examples_dir / example_name
        if not example_path.exists():
            continue
        
        content = example_path.read_text(encoding="utf-8")
        lines = content.split('\n')
        
        # Check the first 10 lines for CandC label
        top_content = '\n'.join(lines[:10]).lower()
        
        # Look for CandC indicators near the top
        has_candc_label = any([
            "candc-specific" in top_content,
            "candc specific" in top_content,
            "candc project" in top_content and lines.index([l for l in lines[:10] if "candc project" in l.lower()][0]) < 5,
        ])
        
        if not has_candc_label:
            failures.append(example_name)
    
    if failures:
        print(f"FAIL: The following CandC examples are not clearly labelled near the top:")
        for f in failures:
            print(f"  - {f}")
        return False
    
    print(f"PASS: All CandC examples are clearly labelled")
    return True

if __name__ == "__main__":
    success = test_ac4()
    sys.exit(0 if success else 1)
