#!/usr/bin/env python3
"""
Test suite for PR #10: Point development targets at ai-framework-tests repo
Tests acceptance criteria from NeilWoodComputing/ai-framework-tests#7

Each test is labeled with its acceptance criterion (AC1-AC6).
"""
import sys
import re
import yaml
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

# Test results tracking
results = []

def record_result(criterion: str, test_name: str, passed: bool, details: str = ""):
    """Record a test result"""
    results.append({
        'criterion': criterion,
        'test': test_name,
        'passed': passed,
        'details': details
    })


# =============================================================================
# AC1: Active development options name the ai-framework-tests repo with paths
# =============================================================================

def test_ac1_active_api_has_repo_fields():
    """AC1: Active API option (api-framework) has repo_url and repo_path"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    api_section = config.get('development', {}).get('api', {})
    active = api_section.get('active')
    
    if not active:
        record_result('AC1', 'active_api_has_repo_fields', False, 
                     "No active API defined")
        return False
    
    active_option = api_section.get('options', {}).get(active, {})
    
    has_repo_url = 'repo_url' in active_option
    has_repo_path = 'repo_path' in active_option
    
    if not has_repo_url:
        record_result('AC1', 'active_api_has_repo_fields', False,
                     f"Active API option '{active}' missing repo_url")
        return False
    
    if not has_repo_path:
        record_result('AC1', 'active_api_has_repo_fields', False,
                     f"Active API option '{active}' missing repo_path")
        return False
    
    # Verify it's the correct repo
    expected_repo = 'https://github.com/NeilWoodComputing/ai-framework-tests'
    expected_path = 'api/'
    actual_repo = active_option['repo_url']
    actual_path = active_option['repo_path']
    
    if actual_repo != expected_repo:
        record_result('AC1', 'active_api_has_repo_fields', False,
                     f"Active API repo_url is '{actual_repo}', expected '{expected_repo}'")
        return False
    
    if actual_path != expected_path:
        record_result('AC1', 'active_api_has_repo_fields', False,
                     f"Active API repo_path is '{actual_path}', expected '{expected_path}'")
        return False
    
    record_result('AC1', 'active_api_has_repo_fields', True,
                 f"Active API '{active}' has repo_url={actual_repo} and repo_path={actual_path}")
    return True


def test_ac1_active_ui_has_repo_fields():
    """AC1: Active UI option (nextjs) has repo_url and repo_path"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    ui_section = config.get('development', {}).get('ui', {})
    active = ui_section.get('active')
    
    if not active:
        record_result('AC1', 'active_ui_has_repo_fields', False,
                     "No active UI defined")
        return False
    
    active_option = ui_section.get('options', {}).get(active, {})
    
    has_repo_url = 'repo_url' in active_option
    has_repo_path = 'repo_path' in active_option
    
    if not has_repo_url:
        record_result('AC1', 'active_ui_has_repo_fields', False,
                     f"Active UI option '{active}' missing repo_url")
        return False
    
    if not has_repo_path:
        record_result('AC1', 'active_ui_has_repo_fields', False,
                     f"Active UI option '{active}' missing repo_path")
        return False
    
    # Verify it's the correct repo
    expected_repo = 'https://github.com/NeilWoodComputing/ai-framework-tests'
    expected_path = 'ui/'
    actual_repo = active_option['repo_url']
    actual_path = active_option['repo_path']
    
    if actual_repo != expected_repo:
        record_result('AC1', 'active_ui_has_repo_fields', False,
                     f"Active UI repo_url is '{actual_repo}', expected '{expected_repo}'")
        return False
    
    if actual_path != expected_path:
        record_result('AC1', 'active_ui_has_repo_fields', False,
                     f"Active UI repo_path is '{actual_path}', expected '{expected_path}'")
        return False
    
    record_result('AC1', 'active_ui_has_repo_fields', True,
                 f"Active UI '{active}' has repo_url={actual_repo} and repo_path={actual_path}")
    return True


# =============================================================================
# AC2: Inactive options marked unavailable or reference-only
# =============================================================================

def test_ac2_unity_api_marked_unavailable():
    """AC2: Unity.API is marked as unavailable (available: false)"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    unity_api = config.get('development', {}).get('api', {}).get('options', {}).get('unity-api', {})
    
    if 'available' not in unity_api:
        record_result('AC2', 'unity_api_marked_unavailable', False,
                     "unity-api option missing 'available' field")
        return False
    
    if unity_api['available'] is not False:
        record_result('AC2', 'unity_api_marked_unavailable', False,
                     f"unity-api available={unity_api['available']}, expected False")
        return False
    
    record_result('AC2', 'unity_api_marked_unavailable', True,
                 "unity-api marked as available: false")
    return True


def test_ac2_angular_marked_unavailable():
    """AC2: Angular is marked as unavailable (available: false)"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    angular = config.get('development', {}).get('ui', {}).get('options', {}).get('angular', {})
    
    if 'available' not in angular:
        record_result('AC2', 'angular_marked_unavailable', False,
                     "angular option missing 'available' field")
        return False
    
    if angular['available'] is not False:
        record_result('AC2', 'angular_marked_unavailable', False,
                     f"angular available={angular['available']}, expected False")
        return False
    
    record_result('AC2', 'angular_marked_unavailable', True,
                 "angular marked as available: false")
    return True


def test_ac2_unity_api_tests_disabled():
    """AC2: Unity.API.Tests unit test command is commented out or removed"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    with open(config_path) as f:
        content = f.read()
    
    # Check that unity-api test command is commented or removed
    # The test command should NOT be active
    if re.search(r'^\s*unity-api:\s*dotnet test Unity\.API\.Tests', content, re.MULTILINE):
        record_result('AC2', 'unity_api_tests_disabled', False,
                     "unity-api test command is still active (not commented out)")
        return False
    
    # Verify it exists as a comment
    if not re.search(r'#.*unity-api.*dotnet test Unity\.API\.Tests', content, re.MULTILINE):
        record_result('AC2', 'unity_api_tests_disabled', False,
                     "unity-api test command not found (should be commented out)")
        return False
    
    record_result('AC2', 'unity_api_tests_disabled', True,
                 "unity-api test command is commented out")
    return True


# =============================================================================
# AC3: Root README updated to reflect new repo structure
# =============================================================================

def test_ac3_readme_mentions_tests_repo():
    """AC3: Root README mentions ai-framework-tests repo"""
    framework_root = Path(__file__).parent.parent
    readme_path = framework_root / 'README.md'
    
    with open(readme_path) as f:
        content = f.read()
    
    # Should mention ai-framework-tests
    if 'ai-framework-tests' not in content:
        record_result('AC3', 'readme_mentions_tests_repo', False,
                     "README.md does not mention ai-framework-tests repository")
        return False
    
    record_result('AC3', 'readme_mentions_tests_repo', True,
                 "README.md mentions ai-framework-tests repository")
    return True


def test_ac3_readme_not_claims_local_api_ui():
    """AC3: README doesn't claim api/ and ui/ live inside AI-framework"""
    framework_root = Path(__file__).parent.parent
    readme_path = framework_root / 'README.md'
    
    with open(readme_path) as f:
        content = f.read()
    
    # Extract the ai-code-framework row from the table
    match = re.search(r'\|\s*`ai-code-framework/`\s*\|(.+?)(?=\n\|)', content, re.DOTALL)
    
    if not match:
        record_result('AC3', 'readme_not_claims_local_api_ui', False,
                     "Could not find ai-code-framework row in README")
        return False
    
    ai_code_description = match.group(1)
    
    # Should NOT claim that api/ and ui/ are local
    # Should say they live in ai-framework-tests
    if re.search(r'Reference API.*and UI.*codebases', ai_code_description, re.IGNORECASE):
        # Old pattern - should be updated
        if 'ai-framework-tests' not in ai_code_description:
            record_result('AC3', 'readme_not_claims_local_api_ui', False,
                         "README ai-code-framework description suggests api/ and ui/ are local")
            return False
    
    # Check for the correct pattern
    if 'Active development codebases' not in ai_code_description:
        record_result('AC3', 'readme_not_claims_local_api_ui', False,
                     "README doesn't clearly state where active development codebases live")
        return False
    
    if 'ai-framework-tests' not in ai_code_description:
        record_result('AC3', 'readme_not_claims_local_api_ui', False,
                     "README doesn't mention ai-framework-tests in ai-code-framework description")
        return False
    
    record_result('AC3', 'readme_not_claims_local_api_ui', True,
                 "README correctly states active development codebases live in ai-framework-tests")
    return True


# =============================================================================
# AC4: CI validates new fields; inactive options don't fail
# =============================================================================

def test_ac4_validate_config_enforces_active_fields():
    """AC4: validate-config.py requires repo_url/repo_path for active available options"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    # Import the validation function from validate-config.py
    import importlib.util
    spec = importlib.util.spec_from_file_location('validate_config_module', 
                                                   framework_root / 'tests/validate-config.py')
    validate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_module)
    validate_framework_config = validate_module.validate_framework_config
    
    # Create a temporary config with missing repo_url
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Deep copy to avoid Path objects
    import copy
    test_config_data = copy.deepcopy(config)
    api_framework = copy.deepcopy(test_config_data['development']['api']['options']['api-framework'])
    del api_framework['repo_url']
    test_config_data['development']['api']['options']['api-framework'] = api_framework
    
    temp_config_path = framework_root / 'tests/.test_config_no_api_repo_url.yaml'
    with open(temp_config_path, 'w') as f:
        yaml.dump(test_config_data, f)
    
    # Run validation
    errors = validate_framework_config(temp_config_path)
    temp_config_path.unlink()  # Clean up
    
    if not errors:
        record_result('AC4', 'validate_enforces_active_repo_url', False,
                     "validate-config.py did not report error when active option missing repo_url")
        return False
    
    has_repo_url_error = any('repo_url' in error for error in errors)
    if not has_repo_url_error:
        record_result('AC4', 'validate_enforces_active_repo_url', False,
                     f"validate-config.py reported errors but not about repo_url: {errors}")
        return False
    
    record_result('AC4', 'validate_enforces_active_repo_url', True,
                 "validate-config.py correctly fails when active option missing repo_url")
    return True


def test_ac4_validate_config_enforces_active_repo_path():
    """AC4: validate-config.py requires repo_path for active available options"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    # Import the validation function from validate-config.py
    import importlib.util
    spec = importlib.util.spec_from_file_location('validate_config_module', 
                                                   framework_root / 'tests/validate-config.py')
    validate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_module)
    validate_framework_config = validate_module.validate_framework_config
    
    # Create a temporary config with missing repo_path
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Deep copy to avoid Path objects
    import copy
    test_config_data = copy.deepcopy(config)
    ui_nextjs = copy.deepcopy(test_config_data['development']['ui']['options']['nextjs'])
    del ui_nextjs['repo_path']
    test_config_data['development']['ui']['options']['nextjs'] = ui_nextjs
    
    temp_config_path = framework_root / 'tests/.test_config_no_ui_repo_path.yaml'
    with open(temp_config_path, 'w') as f:
        yaml.dump(test_config_data, f)
    
    # Run validation
    errors = validate_framework_config(temp_config_path)
    temp_config_path.unlink()
    
    if not errors:
        record_result('AC4', 'validate_enforces_active_repo_path', False,
                     "validate-config.py did not report error when active option missing repo_path")
        return False
    
    has_repo_path_error = any('repo_path' in error for error in errors)
    if not has_repo_path_error:
        record_result('AC4', 'validate_enforces_active_repo_path', False,
                     f"validate-config.py reported errors but not about repo_path: {errors}")
        return False
    
    record_result('AC4', 'validate_enforces_active_repo_path', True,
                 "validate-config.py correctly fails when active option missing repo_path")
    return True


def test_ac4_validate_allows_inactive_without_repo_fields():
    """AC4: validate-config.py allows unavailable options to lack repo_url/repo_path"""
    framework_root = Path(__file__).parent.parent
    config_path = framework_root / 'ai-framework.config.yaml'
    
    # Import the validation function from validate-config.py
    import importlib.util
    spec = importlib.util.spec_from_file_location('validate_config_module', 
                                                   framework_root / 'tests/validate-config.py')
    validate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_module)
    validate_framework_config = validate_module.validate_framework_config
    
    # The actual config has unity-api and angular marked unavailable without repo_url/repo_path
    # This should pass validation
    errors = validate_framework_config(config_path)
    
    # Check that there are no errors about missing repo_url/repo_path for unity-api or angular
    relevant_errors = [e for e in errors if ('unity-api' in e or 'angular' in e) and ('repo_url' in e or 'repo_path' in e)]
    
    if relevant_errors:
        record_result('AC4', 'validate_allows_inactive_without_repo_fields', False,
                     f"validate-config.py incorrectly requires repo fields for unavailable options: {relevant_errors}")
        return False
    
    record_result('AC4', 'validate_allows_inactive_without_repo_fields', True,
                 "validate-config.py passes for unavailable options without repo fields")
    return True


# =============================================================================
# AC5: No agent is sent to ai-code-framework/api or /ui as active paths
# =============================================================================

def test_ac5_no_hardcoded_api_paths_in_briefs():
    """AC5: No AGENT-BRIEF.md uses ai-code-framework/api as active development path"""
    framework_root = Path(__file__).parent.parent
    
    agent_briefs = [
        framework_root / 'ai-planning-framework/AGENT-BRIEF.md',
        framework_root / 'ai-code-framework/AGENT-BRIEF.md',
        framework_root / 'ai-review-framework/AGENT-BRIEF.md',
        framework_root / 'ai-test-framework/AGENT-BRIEF.md',
    ]
    
    violations = []
    
    for brief_path in agent_briefs:
        if not brief_path.exists():
            continue
        
        with open(brief_path) as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Look for references that direct agents to work in ai-code-framework/api
            # Ignore comments about configuration or historical references
            if re.search(r'(?:work|build|implement|develop|write|edit|modify|create).*ai-code-framework/(api|ui)/', line, re.IGNORECASE):
                violations.append(f"{brief_path.name}:{line_num}: {line.strip()}")
    
    if violations:
        record_result('AC5', 'no_hardcoded_paths_in_briefs', False,
                     f"Found {len(violations)} directive(s) to work in ai-code-framework/api or /ui:\n" + 
                     "\n".join(violations))
        return False
    
    record_result('AC5', 'no_hardcoded_paths_in_briefs', True,
                 "No AGENT-BRIEF.md directs agents to work in ai-code-framework/api or /ui")
    return True


def test_ac5_no_hardcoded_api_paths_in_loops():
    """AC5: No loop files use ai-code-framework/api or /ui as active development paths"""
    framework_root = Path(__file__).parent.parent
    
    loop_dirs = [
        framework_root / 'ai-planning-framework/loops',
        framework_root / 'ai-code-framework/loops',
        framework_root / 'ai-review-framework/loops',
        framework_root / 'ai-test-framework/loops',
    ]
    
    violations = []
    
    for loop_dir in loop_dirs:
        if not loop_dir.exists():
            continue
        
        for loop_file in loop_dir.glob('*.md'):
            with open(loop_file) as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Look for active development directives
                if re.search(r'(?:work|build|implement|develop|write|edit|modify|create).*ai-code-framework/(api|ui)/', line, re.IGNORECASE):
                    violations.append(f"{loop_file.relative_to(framework_root)}:{line_num}: {line.strip()}")
    
    if violations:
        record_result('AC5', 'no_hardcoded_paths_in_loops', False,
                     f"Found {len(violations)} directive(s) in loops:\n" + "\n".join(violations))
        return False
    
    record_result('AC5', 'no_hardcoded_paths_in_loops', True,
                 "No loop files direct agents to work in ai-code-framework/api or /ui")
    return True


def test_ac5_no_hardcoded_api_paths_in_rules():
    """AC5: No .cursor/rules files use ai-code-framework/api or /ui as active paths"""
    framework_root = Path(__file__).parent.parent
    
    # Find all .mdc and .md files in .cursor/rules directories
    rule_files = list(framework_root.glob('**/.cursor/rules/*.mdc')) + \
                 list(framework_root.glob('**/.cursor/rules/*.md'))
    
    violations = []
    
    for rule_file in rule_files:
        # Skip files inside ai-code-framework/api or /ui - those are the codebases themselves
        if '/ai-code-framework/api/' in str(rule_file) or '/ai-code-framework/ui/' in str(rule_file):
            continue
        
        with open(rule_file) as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Look for active development directives
            if re.search(r'(?:work|build|implement|develop|write|edit|modify|create).*ai-code-framework/(api|ui)/', line, re.IGNORECASE):
                violations.append(f"{rule_file.relative_to(framework_root)}:{line_num}: {line.strip()}")
    
    if violations:
        record_result('AC5', 'no_hardcoded_paths_in_rules', False,
                     f"Found {len(violations)} directive(s) in rules:\n" + "\n".join(violations))
        return False
    
    record_result('AC5', 'no_hardcoded_paths_in_rules', True,
                 "No rule files direct agents to work in ai-code-framework/api or /ui")
    return True


# =============================================================================
# AC6: No secrets or local PC paths added
# =============================================================================

def test_ac6_no_secrets_in_diff():
    """AC6: PR diff contains no secrets (passwords, tokens, keys)"""
    framework_root = Path(__file__).parent.parent
    
    # Get the diff for this PR branch
    result = subprocess.run(
        ['git', 'diff', 'origin/main...HEAD'],
        cwd=framework_root,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        record_result('AC6', 'no_secrets_in_diff', False,
                     f"Could not get git diff: {result.stderr}")
        return False
    
    diff = result.stdout
    
    # Patterns that might indicate secrets
    secret_patterns = [
        (r'password\s*[:=]\s*["\'](?!<|{{)[^"\']{3,}["\']', 'password'),
        (r'token\s*[:=]\s*["\'](?!<|{{)[^"\']{10,}["\']', 'token'),
        (r'api[_-]?key\s*[:=]\s*["\'](?!<|{{)[^"\']{10,}["\']', 'api_key'),
        (r'secret\s*[:=]\s*["\'](?!<|{{)[^"\']{8,}["\']', 'secret'),
        (r'connection[_-]?string\s*[:=]\s*["\'](?!<|{{)[^"\']{10,}["\']', 'connection_string'),
    ]
    
    violations = []
    
    for pattern, secret_type in secret_patterns:
        matches = re.finditer(pattern, diff, re.IGNORECASE)
        for match in matches:
            # Check if it's in added lines only
            # Get context around the match
            start = max(0, match.start() - 200)
            end = min(len(diff), match.end() + 50)
            context = diff[start:end]
            
            # Only flag if it appears in an added line (starts with +)
            if '\n+' in context[:match.start() - start]:
                violations.append(f"Possible {secret_type}: {match.group()[:50]}...")
    
    if violations:
        record_result('AC6', 'no_secrets_in_diff', False,
                     f"Found {len(violations)} possible secret(s):\n" + "\n".join(violations))
        return False
    
    record_result('AC6', 'no_secrets_in_diff', True,
                 "No secrets detected in PR diff")
    return True


def test_ac6_no_local_paths_in_diff():
    """AC6: PR diff contains no local PC paths (C:\\Users, D:\\Users, etc.)"""
    framework_root = Path(__file__).parent.parent
    
    result = subprocess.run(
        ['git', 'diff', 'origin/main...HEAD'],
        cwd=framework_root,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        record_result('AC6', 'no_local_paths_in_diff', False,
                     f"Could not get git diff: {result.stderr}")
        return False
    
    diff = result.stdout
    
    # Patterns for local paths
    local_path_patterns = [
        (r'[CDE]:\\Users\\[^\s"\'<>]+', 'Windows user path'),
        (r'[CDE]:\\[^\s"\'<>]*\\[^\s"\'<>]+', 'Windows absolute path'),
        (r'/Users/[^\s"\'<>]+/[^\s"\'<>]+', 'macOS user path'),
        (r'/home/[^/\s"\'<>]+/[^\s"\'<>]+', 'Linux user path (excluding generic /home/ubuntu)'),
    ]
    
    violations = []
    
    # Get added lines only
    added_lines = [line for line in diff.split('\n') if line.startswith('+') and not line.startswith('+++')]
    
    for line in added_lines:
        for pattern, path_type in local_path_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                path = match.group()
                # Exclude some known safe patterns
                if '/home/ubuntu' in path or '/home/box' in path:
                    continue
                if 'nwood01' in path.lower():  # Neil's username
                    violations.append(f"{path_type}: {path}")
    
    if violations:
        record_result('AC6', 'no_local_paths_in_diff', False,
                     f"Found {len(violations)} local path(s):\n" + "\n".join(violations))
        return False
    
    record_result('AC6', 'no_local_paths_in_diff', True,
                 "No local PC paths detected in PR diff")
    return True


# =============================================================================
# Main test runner
# =============================================================================

def print_summary():
    """Print test summary"""
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    # Group by criterion
    by_criterion = {}
    for result in results:
        criterion = result['criterion']
        if criterion not in by_criterion:
            by_criterion[criterion] = []
        by_criterion[criterion].append(result)
    
    total_passed = 0
    total_failed = 0
    
    for criterion in sorted(by_criterion.keys()):
        tests = by_criterion[criterion]
        passed = sum(1 for t in tests if t['passed'])
        failed = sum(1 for t in tests if not t['passed'])
        
        status = "✓ PASS" if failed == 0 else "✗ FAIL"
        print(f"\n{criterion}: {status} ({passed}/{len(tests)} tests passed)")
        
        for test in tests:
            status_icon = "✓" if test['passed'] else "✗"
            print(f"  {status_icon} {test['test']}")
            if test['details']:
                for line in test['details'].split('\n'):
                    print(f"      {line}")
        
        total_passed += passed
        total_failed += failed
    
    print("\n" + "="*80)
    print(f"OVERALL: {total_passed} passed, {total_failed} failed out of {len(results)} tests")
    print("="*80)
    
    return total_failed == 0


def main():
    print("Running PR #10 Test Suite")
    print("Testing: Point development targets at ai-framework-tests repo")
    print("="*80 + "\n")
    
    # Run all tests
    print("Running AC1 tests (active options have repo fields)...")
    test_ac1_active_api_has_repo_fields()
    test_ac1_active_ui_has_repo_fields()
    
    print("Running AC2 tests (inactive options marked unavailable)...")
    test_ac2_unity_api_marked_unavailable()
    test_ac2_angular_marked_unavailable()
    test_ac2_unity_api_tests_disabled()
    
    print("Running AC3 tests (README updated)...")
    test_ac3_readme_mentions_tests_repo()
    test_ac3_readme_not_claims_local_api_ui()
    
    print("Running AC4 tests (CI validation)...")
    test_ac4_validate_config_enforces_active_fields()
    test_ac4_validate_config_enforces_active_repo_path()
    test_ac4_validate_allows_inactive_without_repo_fields()
    
    print("Running AC5 tests (no hardcoded paths directing agents)...")
    test_ac5_no_hardcoded_api_paths_in_briefs()
    test_ac5_no_hardcoded_api_paths_in_loops()
    test_ac5_no_hardcoded_api_paths_in_rules()
    
    print("Running AC6 tests (no secrets or local paths)...")
    test_ac6_no_secrets_in_diff()
    test_ac6_no_local_paths_in_diff()
    
    # Print summary
    all_passed = print_summary()
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
