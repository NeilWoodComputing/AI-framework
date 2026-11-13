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
    # Note: We only validate the structure, not the actual API/UI paths
    # since those live in separate codebases and won't exist in this framework repo
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
