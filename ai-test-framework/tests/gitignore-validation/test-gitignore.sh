#!/bin/bash
# Test script for .gitignore validation
# Tests acceptance criteria for PR #7 (widen root gitignore)
# Issue: NeilWoodComputing/ai-framework-tests#10

set -euo pipefail

REPO_ROOT="/agent/repos/AI-framework"
cd "$REPO_ROOT"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
BLOCKED_TESTS=0

# Test results storage
declare -a TEST_RESULTS

# Function to log test result
log_test() {
    local test_id="$1"
    local test_name="$2"
    local status="$3"
    local details="$4"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    case "$status" in
        PASS)
            PASSED_TESTS=$((PASSED_TESTS + 1))
            echo -e "${GREEN}✓ PASS${NC} $test_id: $test_name"
            ;;
        FAIL)
            FAILED_TESTS=$((FAILED_TESTS + 1))
            echo -e "${RED}✗ FAIL${NC} $test_id: $test_name"
            echo -e "  ${RED}Details: $details${NC}"
            ;;
        BLOCKED)
            BLOCKED_TESTS=$((BLOCKED_TESTS + 1))
            echo -e "${YELLOW}⊘ BLOCKED${NC} $test_id: $test_name"
            echo -e "  ${YELLOW}Details: $details${NC}"
            ;;
    esac
    
    TEST_RESULTS+=("$test_id|$test_name|$status|$details")
}

# Function to test git check-ignore for a pattern
test_check_ignore() {
    local test_id="$1"
    local pattern="$2"
    local test_path="$3"
    local should_ignore="$4"  # "yes" or "no"
    
    # Test with git check-ignore
    if git check-ignore -q "$test_path" 2>/dev/null; then
        is_ignored="yes"
    else
        is_ignored="no"
    fi
    
    if [ "$is_ignored" = "$should_ignore" ]; then
        log_test "$test_id" "Pattern '$pattern' matches '$test_path'" "PASS" ""
    else
        if [ "$should_ignore" = "yes" ]; then
            log_test "$test_id" "Pattern '$pattern' should match '$test_path'" "FAIL" "Expected: ignored, Actual: not ignored"
        else
            log_test "$test_id" "Pattern '$pattern' should not match '$test_path'" "FAIL" "Expected: not ignored, Actual: ignored"
        fi
    fi
}

echo "=========================================="
echo "Git Ignore Validation Test Suite"
echo "PR #7 - Widen root .gitignore"
echo "Issue: NeilWoodComputing/ai-framework-tests#10"
echo "=========================================="
echo ""
echo "Repository: $REPO_ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo ""
echo "=========================================="
echo "AC1: New patterns match test paths"
echo "=========================================="
echo ""

# AC1: Test each pattern
echo "Testing __pycache__/ pattern..."
test_check_ignore "AC1.1" "__pycache__/" "some/path/__pycache__/test.pyc" "yes"
test_check_ignore "AC1.1b" "__pycache__/" "__pycache__/test.pyc" "yes"
test_check_ignore "AC1.1c" "__pycache__/" "ai-planning-framework/__pycache__/cache.pyc" "yes"

echo ""
echo "Testing *.pyc pattern..."
test_check_ignore "AC1.2" "*.pyc" "test.pyc" "yes"
test_check_ignore "AC1.2b" "*.pyc" "some/deep/path/module.pyc" "yes"
test_check_ignore "AC1.2c" "*.pyc" "ai-planning-framework/tools/helper.pyc" "yes"

echo ""
echo "Testing node_modules/ pattern..."
test_check_ignore "AC1.3" "node_modules/" "node_modules/package/index.js" "yes"
test_check_ignore "AC1.3b" "node_modules/" "some/path/node_modules/lib.js" "yes"
test_check_ignore "AC1.3c" "node_modules/" "ai-code-framework/scripts/node_modules/dep.js" "yes"

echo ""
echo "Testing .next/ pattern..."
test_check_ignore "AC1.4" ".next/" ".next/build/page.js" "yes"
test_check_ignore "AC1.4b" ".next/" "frontend/.next/static/chunk.js" "yes"

echo ""
echo "Testing .vs/ pattern..."
test_check_ignore "AC1.5" ".vs/" ".vs/config.json" "yes"
test_check_ignore "AC1.5b" ".vs/" "project/.vs/settings.json" "yes"

echo ""
echo "Testing bin/ pattern..."
test_check_ignore "AC1.6" "bin/" "bin/Debug/app.dll" "yes"
test_check_ignore "AC1.6b" "bin/" "Api.Framework/bin/Release/lib.dll" "yes"

echo ""
echo "Testing obj/ pattern..."
test_check_ignore "AC1.7" "obj/" "obj/Debug/temp.cs" "yes"
test_check_ignore "AC1.7b" "obj/" "project/obj/Release/build.obj" "yes"

echo ""
echo "Testing TestResults/ pattern..."
test_check_ignore "AC1.8" "TestResults/" "TestResults/results.trx" "yes"
test_check_ignore "AC1.8b" "TestResults/" "tests/TestResults/output.xml" "yes"

echo ""
echo "Testing playwright-report/ pattern..."
test_check_ignore "AC1.9" "playwright-report/" "playwright-report/index.html" "yes"
test_check_ignore "AC1.9b" "playwright-report/" "e2e/playwright-report/trace.zip" "yes"

echo ""
echo "Testing test-results/ pattern..."
test_check_ignore "AC1.10" "test-results/" "test-results/screenshots/error.png" "yes"
test_check_ignore "AC1.10b" "test-results/" "e2e/test-results/video.webm" "yes"

echo ""
echo "Testing dist/ pattern..."
test_check_ignore "AC1.11" "dist/" "dist/bundle.js" "yes"
test_check_ignore "AC1.11b" "dist/" "frontend/dist/app.min.js" "yes"

echo ""
echo "Testing coverage/ pattern..."
test_check_ignore "AC1.12" "coverage/" "coverage/index.html" "yes"
test_check_ignore "AC1.12b" "coverage/" "tests/coverage/lcov.info" "yes"

echo ""
echo "Testing .env pattern..."
test_check_ignore "AC1.13" ".env" ".env" "yes"
test_check_ignore "AC1.13b" ".env" "api/.env" "yes"

echo ""
echo "Testing .env.* pattern..."
test_check_ignore "AC1.14" ".env.*" ".env.local" "yes"
test_check_ignore "AC1.14b" ".env.*" ".env.production" "yes"
test_check_ignore "AC1.14c" ".env.*" "app/.env.development" "yes"

echo ""
echo "=========================================="
echo "AC2: Fixture files remain tracked"
echo "=========================================="
echo ""

# AC2: Check that existing tracked files are still tracked
FIXTURE_DIR="ai-code-framework/scripts/fixtures/pre-handoff/api-bad"

if [ ! -d "$FIXTURE_DIR" ]; then
    log_test "AC2" "Fixture directory exists" "BLOCKED" "Directory $FIXTURE_DIR does not exist"
else
    # Get list of tracked files in fixture directory
    TRACKED_FILES=$(git ls-files "$FIXTURE_DIR")
    
    if [ -z "$TRACKED_FILES" ]; then
        log_test "AC2" "Fixture files are tracked" "FAIL" "No files tracked in $FIXTURE_DIR"
    else
        FILE_COUNT=$(echo "$TRACKED_FILES" | wc -l)
        
        # Check specific critical files
        if echo "$TRACKED_FILES" | grep -q ".env.local"; then
            log_test "AC2.1" ".env.local fixture file is tracked" "PASS" ""
        else
            log_test "AC2.1" ".env.local fixture file is tracked" "FAIL" "File should be tracked but isn't"
        fi
        
        if echo "$TRACKED_FILES" | grep -q "bin/Release/Generated.cs"; then
            log_test "AC2.2" "bin/Release/Generated.cs fixture file is tracked" "PASS" ""
        else
            log_test "AC2.2" "bin/Release/Generated.cs fixture file is tracked" "FAIL" "File should be tracked but isn't"
        fi
        
        log_test "AC2.3" "All fixture files remain tracked" "PASS" "Found $FILE_COUNT tracked files in $FIXTURE_DIR"
    fi
fi

echo ""
echo "=========================================="
echo "AC3: Old patterns still work"
echo "=========================================="
echo ""

# AC3: Verify existing ignore patterns still work
echo "Testing user-preferences.yaml pattern..."
test_check_ignore "AC3.1" "user-preferences.yaml" "user-preferences.yaml" "yes"

echo ""
echo "Testing users/ pattern..."
test_check_ignore "AC3.2" "users/" "users/config.yaml" "yes"

echo ""
echo "Testing cache/ pattern..."
test_check_ignore "AC3.3" "cache/" "cache/data.json" "yes"

echo ""
echo "Testing .resolved-config-*.yaml pattern..."
test_check_ignore "AC3.4" ".resolved-config-*.yaml" ".resolved-config-test.yaml" "yes"
test_check_ignore "AC3.4b" ".resolved-config-*.yaml" ".resolved-config-production.yaml" "yes"

echo ""
echo "=========================================="
echo "AC4: CI Pre-handoff checks"
echo "=========================================="
echo ""

# AC4: Run pre-handoff checks
if [ ! -f "ai-planning-framework/tools/check.py" ]; then
    log_test "AC4.1" "Pre-handoff check script exists" "BLOCKED" "Script ai-planning-framework/tools/check.py not found"
else
    echo "Running: python3 ai-planning-framework/tools/check.py"
    
    # Capture both output and exit code
    if CHECK_OUTPUT=$(cd ai-planning-framework && python3 tools/check.py 2>&1); then
        CHECK_EXIT=$?
    else
        CHECK_EXIT=$?
    fi
    
    echo "$CHECK_OUTPUT"
    echo ""
    
    if [ $CHECK_EXIT -eq 0 ] && echo "$CHECK_OUTPUT" | grep -q "RESULT: PASS"; then
        log_test "AC4.1" "Pre-handoff check passes" "PASS" "Exit code: $CHECK_EXIT"
    else
        log_test "AC4.1" "Pre-handoff check passes" "FAIL" "Exit code: $CHECK_EXIT, output did not contain 'RESULT: PASS'"
    fi
fi

# Check for CI workflow files
echo ""
if [ -d ".github/workflows" ]; then
    WORKFLOW_COUNT=$(find .github/workflows -name "*.yml" -o -name "*.yaml" | wc -l)
    log_test "AC4.2" "CI workflow files exist" "PASS" "Found $WORKFLOW_COUNT workflow files"
else
    log_test "AC4.2" "CI workflow files exist" "BLOCKED" "No .github/workflows directory found"
fi

echo ""
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo ""
echo "Total Tests:   $TOTAL_TESTS"
echo "Passed:        $PASSED_TESTS"
echo "Failed:        $FAILED_TESTS"
echo "Blocked:       $BLOCKED_TESTS"
echo ""

if [ $FAILED_TESTS -eq 0 ] && [ $BLOCKED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    exit 0
elif [ $BLOCKED_TESTS -gt 0 ]; then
    echo -e "${YELLOW}⊘ SOME TESTS BLOCKED${NC}"
    exit 2
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    exit 1
fi
