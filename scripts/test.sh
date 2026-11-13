#!/usr/bin/env bash
# Test runner for ai-framework
# Runs all quality checks and tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$FRAMEWORK_ROOT"

# Colours
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

FAILED=0
TOTAL=0

run_check() {
    local name="$1"
    shift
    
    TOTAL=$((TOTAL + 1))
    echo -e "\n${BLUE}▶ $name${NC}"
    
    if "$@"; then
        echo -e "${GREEN}✓ Passed${NC}"
    else
        echo -e "${RED}✗ Failed${NC}"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

check_command() {
    if ! command -v "$1" &>/dev/null; then
        echo -e "${YELLOW}Warning: $1 not found (skipping $2)${NC}"
        return 1
    fi
    return 0
}

echo -e "${BLUE}=== AI Framework Test Suite ===${NC}"
echo "Running quality checks and tests..."

# 1. Config validation
if check_command python3 "config validation"; then
    run_check "Config Validation" python3 tests/validate-config.py || true
fi

# 2. Framework consistency checks
if check_command python3 "framework consistency"; then
    run_check "Framework Consistency" python3 tests/check-framework.py || true
fi

# 3. Shell script checks
if check_command shellcheck "shellcheck"; then
    run_check "ShellCheck (init-user.sh)" shellcheck scripts/init-user.sh || true
fi

# 4. PowerShell script checks
if check_command pwsh "PSScriptAnalyzer"; then
    if pwsh -Command "Get-Module -ListAvailable PSScriptAnalyzer" &>/dev/null; then
        run_check "PSScriptAnalyzer (init-user.ps1)" \
            pwsh -Command "Invoke-ScriptAnalyzer -Path scripts/init-user.ps1 -Settings PSGallery" || true
    else
        echo -e "${YELLOW}Warning: PSScriptAnalyzer module not found (skipping PowerShell analysis)${NC}"
    fi
fi

# 5. YAML linting
if check_command yamllint "YAML linting"; then
    run_check "yamllint" yamllint ai-framework.config.yaml user-preferences.example.yaml || true
fi

# 6. Markdown linting
if check_command markdownlint "markdown linting"; then
    run_check "markdownlint" markdownlint README.md \
        ai-planning-framework/AGENT-BRIEF.md \
        ai-code-framework/AGENT-BRIEF.md \
        ai-review-framework/AGENT-BRIEF.md \
        ai-test-framework/AGENT-BRIEF.md \
        handoff/README.md || true
elif check_command npx "markdown linting"; then
    run_check "markdownlint (via npx)" npx markdownlint-cli README.md \
        ai-planning-framework/AGENT-BRIEF.md \
        ai-code-framework/AGENT-BRIEF.md \
        ai-review-framework/AGENT-BRIEF.md \
        ai-test-framework/AGENT-BRIEF.md \
        handoff/README.md || true
fi

# 7. Bash script tests
if check_command bats "bash script tests"; then
    run_check "Bash Script Tests (bats)" bats tests/init-user.bats || true
fi

# 8. PowerShell script tests
if check_command pwsh "PowerShell script tests"; then
    if pwsh -Command "Get-Module -ListAvailable Pester" &>/dev/null; then
        run_check "PowerShell Script Tests (Pester)" \
            pwsh -Command "Invoke-Pester tests/init-user.Tests.ps1 -Output Detailed" || true
    else
        echo -e "${YELLOW}Warning: Pester module not found (skipping PowerShell tests)${NC}"
    fi
fi

# Summary
echo -e "\n${BLUE}=== Summary ===${NC}"
echo "Total checks: $TOTAL"
echo "Failed: $FAILED"
echo "Passed: $((TOTAL - FAILED))"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ All checks passed!${NC}"
    exit 0
else
    echo -e "\n${RED}✗ $FAILED check(s) failed${NC}"
    exit 1
fi
