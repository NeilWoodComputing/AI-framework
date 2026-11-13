#!/usr/bin/env python3
"""
Validate ai-framework.config.yaml and user-preferences.example.yaml
"""
import sys
import yaml
from pathlib import Path

# Valid runtime values
VALID_RUNTIMES = {'cursor', 'cursor-local', 'claude-code'}

# Required roles
REQUIRED_ROLES = {'planning', 'code', 'review', 'testing'}

# Allowed handoff.plan_to_code values. `devops` is a deprecated alias of `board`
# and canonicalises to it (same behaviour).
PLAN_TO_CODE_ALIASES = {"devops": "board"}
PLAN_TO_CODE_CANONICAL = frozenset({"board", "direct"})
PLAN_TO_CODE_ALLOWED = PLAN_TO_CODE_CANONICAL | frozenset(PLAN_TO_CODE_ALIASES)


def canonicalize_plan_to_code(value):
    """Return the canonical plan_to_code value. `devops` maps to `board`."""
    if isinstance(value, str) and value in PLAN_TO_CODE_ALIASES:
        return PLAN_TO_CODE_ALIASES[value]
    return value


def is_board_route(value):
    """True when the value is the board route (`board` or the `devops` alias)."""
    return canonicalize_plan_to_code(value) == "board"


def validate_plan_to_code_value(value, errors=None, field="handoff.plan_to_code"):
    """Validate one plan_to_code value. Appends to and returns the errors list."""
    if errors is None:
        errors = []
    if value is None:
        errors.append(f"Missing '{field}'")
        return errors
    if not isinstance(value, str) or value not in PLAN_TO_CODE_ALLOWED:
        allowed = ", ".join(sorted(PLAN_TO_CODE_CANONICAL))
        errors.append(
            f"Invalid {field}: {value!r} (must be one of {allowed}; "
            "`devops` is a deprecated alias of `board`)"
        )
    return errors


def validate_framework_config(config_path):
    """Validate ai-framework.config.yaml"""
    errors = []
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Check runtime section exists
    if 'runtime' not in config:
        errors.append("Missing 'runtime' section")
        return errors
    
    runtime = config['runtime']
    
    # Check default runtime exists and is valid
    if 'default' not in runtime:
        errors.append("Missing 'runtime.default'")
    elif runtime['default'] not in VALID_RUNTIMES:
        errors.append(f"Invalid runtime.default: '{runtime['default']}' (must be one of {VALID_RUNTIMES})")
    
    # Check per-role runtimes if present
    for role in REQUIRED_ROLES:
        if role in runtime and runtime[role] not in VALID_RUNTIMES:
            errors.append(f"Invalid runtime.{role}: '{runtime[role]}' (must be one of {VALID_RUNTIMES})")
    
    # Check agents section
    if 'agents' not in config:
        errors.append("Missing 'agents' section")
        return errors
    
    agents = config['agents']
    
    # Check all required roles have agent mappings
    for role in REQUIRED_ROLES:
        if role not in agents:
            errors.append(f"Missing agent mapping for role: {role}")
        else:
            agent = agents[role]
            if 'name' not in agent:
                errors.append(f"Missing 'name' for agent role: {role}")
            if 'id' not in agent:
                errors.append(f"Missing 'id' for agent role: {role}")
            if 'framework' not in agent:
                errors.append(f"Missing 'framework' for agent role: {role}")
    
    # Check referenced paths exist
    framework_root = config_path.parent
    
    # Check frameworks paths
    if 'frameworks' in config:
        for framework_name, framework_config in config['frameworks'].items():
            if 'path' in framework_config:
                path = framework_root / framework_config['path']
                if not path.exists():
                    errors.append(f"frameworks.{framework_name}.path does not exist: {framework_config['path']}")
            
            if 'agent_brief' in framework_config:
                path = framework_root / framework_config['agent_brief']
                if not path.exists():
                    errors.append(f"frameworks.{framework_name}.agent_brief does not exist: {framework_config['agent_brief']}")
    
    # Check development paths
    if 'development' in config:
        for dev_type in ['api', 'ui']:
            if dev_type in config['development']:
                dev_section = config['development'][dev_type]
                if 'active' not in dev_section:
                    errors.append(f"Missing 'active' in development.{dev_type}")
                elif 'options' in dev_section:
                    active = dev_section['active']
                    if active not in dev_section['options']:
                        errors.append(f"development.{dev_type}.active references '{active}' which is not in options")
                    else:
                        active_option = dev_section['options'][active]
                        # Check if the option is available (default to True if not specified)
                        is_available = active_option.get('available', True)
                        
                        if is_available:
                            # Active and available options must have repo_url and repo_path
                            if 'repo_url' not in active_option:
                                errors.append(f"development.{dev_type}.options.{active}: active option missing 'repo_url'")
                            if 'repo_path' not in active_option:
                                errors.append(f"development.{dev_type}.options.{active}: active option missing 'repo_path'")
                            
                            # Warn if the checked-out path is missing (but don't fail)
                            if 'path' in active_option:
                                path = framework_root / active_option['path']
                                if not path.exists():
                                    print(f"  ⚠ development.{dev_type}.options.{active}.path does not exist: {active_option['path']}")
                        
                        # Inactive or unavailable options don't need repo_url/repo_path
                        # and their missing paths don't fail CI
    

    # PR-based framework test layout (ai-framework-tests#13).
    # Keep testing.report_names as a map (feature tests). The new keys sit alongside it.
    if "testing" not in config:
        errors.append("Missing 'testing' section")
    else:
        testing = config["testing"]
        report_names = testing.get("report_names")
        if report_names is None:
            errors.append("Missing 'testing.report_names'")
        elif not isinstance(report_names, dict):
            errors.append(
                f"testing.report_names must remain a map of feature report paths, found {type(report_names).__name__}"
            )
        else:
            for key in ("plan", "report", "log"):
                if key not in report_names:
                    errors.append(f"Missing 'testing.report_names.{key}'")
        if "pr_tests_dir" not in testing:
            errors.append("Missing 'testing.pr_tests_dir'")
        else:
            pr_dir = testing["pr_tests_dir"]
            if not isinstance(pr_dir, str) or not pr_dir.strip():
                errors.append("testing.pr_tests_dir must be a string path")
            else:
                pr_path = framework_root / pr_dir
                if not pr_path.exists():
                    errors.append(f"testing.pr_tests_dir does not exist: {pr_dir}")
        if "pr_report_names" not in testing:
            errors.append("Missing 'testing.pr_report_names'")
        elif not isinstance(testing["pr_report_names"], str) or not testing["pr_report_names"].strip():
            errors.append("testing.pr_report_names must be a string pattern")

    # Handoff plan_to_code: board | direct, with devops as a deprecated alias of board.
    if "handoff" not in config:
        errors.append("Missing 'handoff' section")
    else:
        handoff = config["handoff"]
        if not isinstance(handoff, dict):
            errors.append("'handoff' section must be a map")
        else:
            validate_plan_to_code_value(handoff.get("plan_to_code"), errors)

    return errors

def validate_user_preferences(template_path):
    """Validate user-preferences.example.yaml"""
    errors = []
    
    with open(template_path) as f:
        config = yaml.safe_load(f)
    
    # Check user field exists
    if 'user' not in config:
        errors.append("Missing 'user' field")
    elif config['user'] != 'example-user':
        errors.append(f"Template should have 'user: example-user', found: '{config['user']}'")
    
    # Check runtime section if present (it's commented out in template, so this checks if uncommented)
    if 'runtime' in config:
        runtime = config['runtime']
        if 'default' in runtime and runtime['default'] not in VALID_RUNTIMES:
            errors.append(f"Invalid runtime.default in template: '{runtime['default']}'")
        
        for role in REQUIRED_ROLES:
            if role in runtime and runtime[role] not in VALID_RUNTIMES:
                errors.append(f"Invalid runtime.{role} in template: '{runtime[role]}'")
    
    return errors

def main():
    script_dir = Path(__file__).parent
    framework_root = script_dir.parent
    
    all_errors = []
    
    # Validate framework config
    config_path = framework_root / 'ai-framework.config.yaml'
    if config_path.exists():
        print(f"Validating {config_path.name}...")
        errors = validate_framework_config(config_path)
        if errors:
            print(f"  ❌ {len(errors)} error(s):")
            for error in errors:
                print(f"     - {error}")
            all_errors.extend(errors)
        else:
            print("  ✓ Valid")
    else:
        print(f"  ❌ Not found: {config_path}")
        all_errors.append(f"Config file not found: {config_path}")
    
    # Validate user preferences template
    template_path = framework_root / 'user-preferences.example.yaml'
    if template_path.exists():
        print(f"\nValidating {template_path.name}...")
        errors = validate_user_preferences(template_path)
        if errors:
            print(f"  ❌ {len(errors)} error(s):")
            for error in errors:
                print(f"     - {error}")
            all_errors.extend(errors)
        else:
            print("  ✓ Valid")
    else:
        print(f"  ❌ Not found: {template_path}")
        all_errors.append(f"Template file not found: {template_path}")
    
    if all_errors:
        print(f"\n❌ Validation failed with {len(all_errors)} error(s)")
        return 1
    else:
        print("\n✓ All validations passed")
        return 0

if __name__ == '__main__':
    sys.exit(main())
