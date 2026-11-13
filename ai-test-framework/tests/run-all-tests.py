#!/usr/bin/env python3
"""
Test runner for PR #9 acceptance criteria.

Runs all tests and generates a summary report.
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_script):
    """Run a single test script and return its result"""
    try:
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return {
            'passed': result.returncode == 0,
            'output': result.stdout + result.stderr,
            'exit_code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'passed': False,
            'output': 'Test timed out after 120 seconds',
            'exit_code': -1
        }
    except Exception as e:
        return {
            'passed': False,
            'output': f'Error running test: {e}',
            'exit_code': -1
        }

def main():
    """Run all tests and generate summary"""
    test_dir = Path(__file__).parent
    
    # Define tests in order
    tests = [
        ('AC1', 'test-ac1-no-candc-path.py', 
         "Test Bot's brief does not mention projects/candc/work"),
        ('AC2', 'test-ac2-handoff-readme-reference.py',
         "Test Bot's brief points to handoff/README.md for shared editing rules"),
        ('AC3', 'test-ac3-no-local-paths.py',
         "No living test-framework doc contains D:\\Users\\nwood01"),
        ('AC4', 'test-ac4-candc-example-labeled.py',
         "CandC examples are clearly labelled"),
        ('AC5', 'test-ac5-ci-checks.py',
         "CI and leftover-terms check pass"),
        ('R8', 'test-r8-no-work-modifications.py',
         "No files under ai-planning-framework/work/ modified"),
        ('LINKS', 'test-links.py',
         "Links in changed files resolve"),
    ]
    
    print("=" * 80)
    print("PR #9 Test Suite - Fix stale Test Bot brief")
    print("=" * 80)
    print()
    
    results = []
    
    for test_id, test_file, description in tests:
        test_path = test_dir / test_file
        
        if not test_path.exists():
            print(f"❌ {test_id}: {description}")
            print(f"   BLOCKED: Test file {test_file} not found")
            results.append({
                'id': test_id,
                'description': description,
                'status': 'BLOCKED',
                'output': f"Test file {test_file} not found"
            })
            print()
            continue
        
        print(f"Running {test_id}: {description}...")
        result = run_test(test_path)
        
        status = 'PASS' if result['passed'] else 'FAIL'
        symbol = '✅' if result['passed'] else '❌'
        
        print(f"{symbol} {test_id}: {description}")
        print(f"   Status: {status}")
        
        results.append({
            'id': test_id,
            'description': description,
            'status': status,
            'output': result['output']
        })
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    blocked = sum(1 for r in results if r['status'] == 'BLOCKED')
    total = len(results)
    
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Blocked: {blocked}")
    print()
    
    # Show failures
    if failed > 0 or blocked > 0:
        print("=" * 80)
        print("FAILURES AND BLOCKED TESTS")
        print("=" * 80)
        for r in results:
            if r['status'] in ['FAIL', 'BLOCKED']:
                print(f"\n{r['id']}: {r['description']}")
                print(f"Status: {r['status']}")
                print("Output:")
                print(r['output'])
                print("-" * 80)
    
    # Generate detailed report file
    report_path = test_dir / "test-report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("PR #9 Test Report - Fix stale Test Bot brief\n")
        f.write("=" * 80 + "\n\n")
        
        for r in results:
            f.write(f"{r['id']}: {r['description']}\n")
            f.write(f"Status: {r['status']}\n")
            f.write(f"\nOutput:\n{r['output']}\n")
            f.write("-" * 80 + "\n\n")
        
        f.write(f"\nSummary: {passed} PASS, {failed} FAIL, {blocked} BLOCKED out of {total} total\n")
    
    print(f"\nDetailed report saved to: {report_path}")
    
    # Exit with appropriate code
    sys.exit(0 if (failed == 0 and blocked == 0) else 1)

if __name__ == "__main__":
    main()
