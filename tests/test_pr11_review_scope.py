#!/usr/bin/env python3
"""
Test suite for PR #11: Review scope dual-repo configuration
Tests acceptance criteria from NeilWoodComputing/ai-framework-tests#9

This test verifies the config changes that enable Review Bot to review PRs
on both AI-framework (framework changes) and ai-framework-tests (app code).
"""

import sys
import yaml
from pathlib import Path
from typing import Any, Dict, List

# Test results tracker
test_results = {
    "passed": 0,
    "failed": 0,
    "blocked": 0,
    "tests": []
}

def log_test(criterion: str, test_name: str, status: str, details: str = ""):
    """Log test result"""
    test_results["tests"].append({
        "criterion": criterion,
        "test": test_name,
        "status": status,
        "details": details
    })
    if status == "PASS":
        test_results["passed"] += 1
    elif status == "FAIL":
        test_results["failed"] += 1
    elif status == "BLOCKED":
        test_results["blocked"] += 1
    print(f"[{status}] {criterion} - {test_name}")
    if details:
        print(f"       {details}")


def load_config() -> Dict[str, Any]:
    """Load ai-framework.config.yaml"""
    config_path = Path(__file__).parent.parent / "ai-framework.config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def test_ac1_framework_folders_in_scope(config: Dict[str, Any]) -> None:
    """
    AC1: A PR that only changes `ai-planning-framework/` or `handoff/` 
    in AI-framework is in review scope.
    """
    criterion = "AC1"
    scope_include = config.get("review", {}).get("scope_include", [])
    
    # Check for all required framework folders
    required_patterns = [
        "ai-planning-framework/**",
        "ai-code-framework/**", 
        "ai-review-framework/**",
        "ai-test-framework/**",
        "handoff/**",
        "scripts/**",
        "tests/**",
        "ai-framework.config.yaml",
        "project.yaml",
        "README.md"
    ]
    
    missing = []
    for pattern in required_patterns:
        if pattern not in scope_include:
            missing.append(pattern)
    
    if missing:
        log_test(
            criterion,
            "Framework folders in scope_include",
            "FAIL",
            f"Missing patterns: {', '.join(missing)}"
        )
    else:
        log_test(
            criterion,
            "Framework folders in scope_include",
            "PASS",
            f"All {len(required_patterns)} framework patterns present"
        )


def test_ac2_app_folders_in_scope(config: Dict[str, Any]) -> None:
    """
    AC2: A PR touching `api/` or `ui/` in ai-framework-tests is in review scope.
    """
    criterion = "AC2"
    scope_include = config.get("review", {}).get("scope_include", [])
    
    required_patterns = ["api/**", "ui/**"]
    missing = [p for p in required_patterns if p not in scope_include]
    
    if missing:
        log_test(
            criterion,
            "App folders (api/**, ui/**) in scope_include",
            "FAIL",
            f"Missing patterns: {', '.join(missing)}"
        )
    else:
        log_test(
            criterion,
            "App folders (api/**, ui/**) in scope_include", 
            "PASS",
            "Both api/** and ui/** patterns present"
        )


def test_ac3_multiple_repos_supported(config: Dict[str, Any]) -> None:
    """
    AC3: Review comments post to whichever repo the PR is in.
    Tests that review.github supports multiple repositories.
    """
    criterion = "AC3"
    github_config = config.get("review", {}).get("github", {})
    
    # Check for repositories field (plural) instead of repository (singular)
    repositories = github_config.get("repositories")
    repository = github_config.get("repository")
    
    if repositories is None and repository is None:
        log_test(
            criterion,
            "Multiple repository support",
            "FAIL",
            "Neither 'repositories' nor 'repository' field found in review.github"
        )
        return
    
    if repository is not None and repositories is None:
        log_test(
            criterion,
            "Multiple repository support",
            "FAIL",
            f"Found single 'repository' field: {repository}, expected 'repositories' list"
        )
        return
    
    if not isinstance(repositories, list):
        log_test(
            criterion,
            "Multiple repository support",
            "FAIL",
            f"'repositories' is not a list: {type(repositories).__name__}"
        )
        return
    
    expected_repos = ["AI-framework", "ai-framework-tests"]
    if set(repositories) != set(expected_repos):
        log_test(
            criterion,
            "Multiple repository support",
            "FAIL",
            f"Repositories list {repositories} doesn't match expected {expected_repos}"
        )
    else:
        log_test(
            criterion,
            "Multiple repository support",
            "PASS",
            f"Both repositories configured: {repositories}"
        )


def test_ac4_no_vote_approval(config: Dict[str, Any]) -> None:
    """
    AC4: Agents still never vote, approve or merge (set_vote: false).
    """
    criterion = "AC4"
    set_vote = config.get("review", {}).get("publish", {}).get("set_vote")
    
    if set_vote is None:
        log_test(
            criterion,
            "review.publish.set_vote is false",
            "FAIL",
            "set_vote field not found in review.publish"
        )
    elif set_vote is not False:
        log_test(
            criterion,
            "review.publish.set_vote is false",
            "FAIL",
            f"set_vote is {set_vote}, expected false"
        )
    else:
        log_test(
            criterion,
            "review.publish.set_vote is false",
            "PASS",
            "Agents never vote, approve, or merge"
        )


def test_documentation_updated() -> None:
    """
    Additional test: Verify documentation files were updated consistently.
    """
    criterion = "DOC"
    
    doc_files = [
        "ai-review-framework/AGENT-BRIEF.md",
        "ai-review-framework/README.md",
        "ai-review-framework/loops/pr-review.md",
        "ai-review-framework/skills/gather-pr-context/SKILL.md",
        "ai-review-framework/templates/review-report.md"
    ]
    
    base_path = Path(__file__).parent.parent
    missing_files = []
    
    for doc_file in doc_files:
        doc_path = base_path / doc_file
        if not doc_path.exists():
            missing_files.append(doc_file)
    
    if missing_files:
        log_test(
            criterion,
            "Documentation files exist",
            "FAIL",
            f"Missing files: {', '.join(missing_files)}"
        )
    else:
        log_test(
            criterion,
            "Documentation files exist",
            "PASS",
            f"All {len(doc_files)} documentation files present"
        )


def main():
    print("=" * 80)
    print("Test Suite: PR #11 - Review scope dual-repo configuration")
    print("Issue: NeilWoodComputing/ai-framework-tests#9")
    print("=" * 80)
    print()
    
    try:
        # Load configuration
        print("Loading ai-framework.config.yaml...")
        config = load_config()
        print("✓ Config loaded successfully\n")
        
        # Run tests for each acceptance criterion
        print("Running acceptance criteria tests...\n")
        
        test_ac1_framework_folders_in_scope(config)
        test_ac2_app_folders_in_scope(config)
        test_ac3_multiple_repos_supported(config)
        test_ac4_no_vote_approval(config)
        test_documentation_updated()
        
        # Summary
        print()
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total tests: {len(test_results['tests'])}")
        print(f"Passed:      {test_results['passed']}")
        print(f"Failed:      {test_results['failed']}")
        print(f"Blocked:     {test_results['blocked']}")
        print("=" * 80)
        
        # Exit with appropriate code
        if test_results['failed'] > 0:
            print("\n❌ TEST SUITE FAILED")
            sys.exit(1)
        elif test_results['blocked'] > 0:
            print("\n⚠️  TEST SUITE BLOCKED")
            sys.exit(2)
        else:
            print("\n✅ TEST SUITE PASSED")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()
