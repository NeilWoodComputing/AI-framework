#!/usr/bin/env python3
"""
Framework consistency checks:
- All referenced paths exist
- All AGENT-BRIEF.md files contain runtime verification
- README precedence matches config comments
"""
import sys
import re
from pathlib import Path

def check_agent_briefs_have_runtime():
    """Check all AGENT-BRIEF.md files contain runtime verification instructions"""
    errors = []
    
    framework_root = Path(__file__).parent.parent
    agent_briefs = [
        framework_root / 'ai-planning-framework/AGENT-BRIEF.md',
        framework_root / 'ai-code-framework/AGENT-BRIEF.md',
        framework_root / 'ai-review-framework/AGENT-BRIEF.md',
        framework_root / 'ai-test-framework/AGENT-BRIEF.md',
    ]
    
    # Expected patterns
    required_patterns = [
        r'runtime',  # Must mention runtime
        r'user-preferences\.yaml',  # Must mention the config file
        r'per-role',  # Must mention per-role override
        r'shared default',  # Must mention shared default
        r'Verify.*runtime.*before.*work',  # Must have verification instruction
        r'stop.*hand off',  # Must say to stop and hand off if wrong
    ]
    
    for brief_path in agent_briefs:
        if not brief_path.exists():
            errors.append(f"Missing: {brief_path.relative_to(framework_root)}")
            continue
        
        content = brief_path.read_text()
        
        missing = []
        for pattern in required_patterns:
            if not re.search(pattern, content, re.IGNORECASE):
                missing.append(pattern)
        
        if missing:
            errors.append(f"{brief_path.relative_to(framework_root)}: Missing required runtime patterns: {', '.join(missing)}")
    
    return errors

def check_readme_precedence():
    """Check README precedence description matches expected format"""
    errors = []
    
    framework_root = Path(__file__).parent.parent
    readme_path = framework_root / 'README.md'
    
    if not readme_path.exists():
        return [f"README.md not found"]
    
    content = readme_path.read_text()
    
    # Check for precedence section
    if 'Precedence' not in content:
        errors.append("README.md: Missing 'Precedence' section")
        return errors
    
    # Extract precedence section
    precedence_match = re.search(
        r'###\s+Precedence.*?(?=###|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    
    if not precedence_match:
        errors.append("README.md: Could not find Precedence section")
        return errors
    
    precedence_section = precedence_match.group(0)
    
    # Check required elements are present and in correct order
    required_order = [
        r'user preferences',
        r'per-role',
        r'shared default',
    ]
    
    positions = []
    for i, pattern in enumerate(required_order):
        match = re.search(pattern, precedence_section, re.IGNORECASE)
        if match:
            positions.append((i, match.start(), pattern))
        else:
            errors.append(f"README.md Precedence: Missing '{pattern}'")
    
    # Check they appear in the correct order
    if len(positions) == len(required_order):
        for i in range(len(positions) - 1):
            if positions[i][1] >= positions[i+1][1]:
                errors.append(f"README.md Precedence: '{positions[i][2]}' should come before '{positions[i+1][2]}'")
    
    return errors

def check_referenced_paths():
    """Check all paths referenced in config exist"""
    errors = []
    
    framework_root = Path(__file__).parent.parent
    
    # Check paths mentioned in AGENT-BRIEF files
    paths_to_check = [
        'ai-framework.config.yaml',
        'user-preferences.example.yaml',
        'scripts/init-user.sh',
        'scripts/init-user.ps1',
        'handoff/README.md',
    ]
    
    for path_str in paths_to_check:
        path = framework_root / path_str
        if not path.exists():
            errors.append(f"Referenced path does not exist: {path_str}")
    
    # Check all framework directories exist
    framework_dirs = [
        'ai-planning-framework',
        'ai-code-framework',
        'ai-review-framework',
        'ai-test-framework',
        'handoff',
    ]
    
    for dir_name in framework_dirs:
        dir_path = framework_root / dir_name
        if not dir_path.is_dir():
            errors.append(f"Framework directory does not exist: {dir_name}")
        else:
            # Check AGENT-BRIEF.md exists in each framework
            if dir_name != 'handoff':
                brief_path = dir_path / 'AGENT-BRIEF.md'
                if not brief_path.exists():
                    errors.append(f"Missing AGENT-BRIEF.md in {dir_name}")
    
    return errors

def main():
    all_errors = []
    
    print("Checking framework consistency...\n")
    
    # Check 1: Agent briefs have runtime verification
    print("1. Checking AGENT-BRIEF.md files contain runtime verification...")
    errors = check_agent_briefs_have_runtime()
    if errors:
        print(f"   ❌ {len(errors)} error(s):")
        for error in errors:
            print(f"      - {error}")
        all_errors.extend(errors)
    else:
        print("   ✓ All briefs have runtime verification")
    
    # Check 2: README precedence
    print("\n2. Checking README.md precedence section...")
    errors = check_readme_precedence()
    if errors:
        print(f"   ❌ {len(errors)} error(s):")
        for error in errors:
            print(f"      - {error}")
        all_errors.extend(errors)
    else:
        print("   ✓ Precedence section is correct")
    
    # Check 3: Referenced paths exist
    print("\n3. Checking referenced paths exist...")
    errors = check_referenced_paths()
    if errors:
        print(f"   ❌ {len(errors)} error(s):")
        for error in errors:
            print(f"      - {error}")
        all_errors.extend(errors)
    else:
        print("   ✓ All referenced paths exist")
    
    if all_errors:
        print(f"\n❌ Framework consistency check failed with {len(all_errors)} error(s)")
        return 1
    else:
        print("\n✓ All framework consistency checks passed")
        return 0

if __name__ == '__main__':
    sys.exit(main())
