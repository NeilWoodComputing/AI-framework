#!/usr/bin/env bats
# Tests for scripts/init-user.sh
# Run with: bats tests/init-user.bats

setup() {
    # Create temp directory for each test
    TEST_DIR="$(mktemp -d)"
    export AI_FRAMEWORK_USER_CONFIG="$TEST_DIR/user-preferences.yaml"
    export AI_FRAMEWORK_BOT_CACHE_DIR="$TEST_DIR/cache"
    
    # Use framework root
    FRAMEWORK_ROOT="$(cd "$(dirname "$BATS_TEST_DIRNAME")" && pwd)"
    INIT_SCRIPT="$FRAMEWORK_ROOT/scripts/init-user.sh"
    TEMPLATE_FILE="$FRAMEWORK_ROOT/user-preferences.example.yaml"
}

teardown() {
    # Clean up temp directory
    rm -rf "$TEST_DIR"
}

@test "init-user.sh: creates config from template" {
    run bash "$INIT_SCRIPT" testuser
    [ "$status" -eq 0 ]
    [ -f "$AI_FRAMEWORK_USER_CONFIG" ]
    
    # Check username was replaced
    run grep "user: testuser" "$AI_FRAMEWORK_USER_CONFIG"
    [ "$status" -eq 0 ]
    
    # Check it's not still example-user
    run grep "user: example-user" "$AI_FRAMEWORK_USER_CONFIG"
    [ "$status" -eq 1 ]
}

@test "init-user.sh: idempotent re-run keeps existing settings" {
    # First run
    bash "$INIT_SCRIPT" user1 >/dev/null 2>&1
    
    # Add custom content
    echo "runtime:" >> "$AI_FRAMEWORK_USER_CONFIG"
    echo "  code: claude-code" >> "$AI_FRAMEWORK_USER_CONFIG"
    
    # Second run with different username
    run bash "$INIT_SCRIPT" user2
    [ "$status" -eq 0 ]
    
    # Should keep original username and settings
    run grep "user: user1" "$AI_FRAMEWORK_USER_CONFIG"
    [ "$status" -eq 0 ]
    run grep "code: claude-code" "$AI_FRAMEWORK_USER_CONFIG"
    [ "$status" -eq 0 ]
}

@test "init-user.sh: migrates from old users/<name>.yaml" {
    # Create old format file
    OLD_DIR="$(dirname "$AI_FRAMEWORK_USER_CONFIG")/users"
    mkdir -p "$OLD_DIR"
    cat > "$OLD_DIR/olduser.yaml" << EOF
user: olduser
runtime:
  default: claude-code
EOF
    
    # Run init
    run bash "$INIT_SCRIPT" olduser
    [ "$status" -eq 0 ]
    
    # Check migration happened
    [ -f "$AI_FRAMEWORK_USER_CONFIG" ]
    run grep "user: olduser" "$AI_FRAMEWORK_USER_CONFIG"
    [ "$status" -eq 0 ]
    run grep "claude-code" "$AI_FRAMEWORK_USER_CONFIG"
    [ "$status" -eq 0 ]
    
    # Old file should still exist
    [ -f "$OLD_DIR/olduser.yaml" ]
}

@test "init-user.sh: AI_FRAMEWORK_USER_CONFIG override works" {
    CUSTOM_CONFIG="$TEST_DIR/custom/my-config.yaml"
    export AI_FRAMEWORK_USER_CONFIG="$CUSTOM_CONFIG"
    
    run bash "$INIT_SCRIPT" customuser
    [ "$status" -eq 0 ]
    [ -f "$CUSTOM_CONFIG" ]
    
    run grep "user: customuser" "$CUSTOM_CONFIG"
    [ "$status" -eq 0 ]
}

@test "init-user.sh: AI_FRAMEWORK_BOT_MACHINE=false skips caching" {
    export AI_FRAMEWORK_BOT_MACHINE=false
    
    run bash "$INIT_SCRIPT" testuser
    [ "$status" -eq 0 ]
    
    # Cache directory should not be created
    [ ! -d "$AI_FRAMEWORK_BOT_CACHE_DIR" ]
}

@test "init-user.sh: AI_FRAMEWORK_BOT_MACHINE=true enables caching" {
    export AI_FRAMEWORK_BOT_MACHINE=true
    
    # Mock git remote to avoid actual cloning
    FRAMEWORK_ROOT="$(cd "$(dirname "$BATS_TEST_DIRNAME")" && pwd)"
    cd "$FRAMEWORK_ROOT"
    
    run bash "$INIT_SCRIPT" testuser
    [ "$status" -eq 0 ]
    
    # Cache directory should exist
    [ -d "$AI_FRAMEWORK_BOT_CACHE_DIR" ]
}

@test "init-user.sh: handles missing template file gracefully" {
    # Temporarily rename template
    FRAMEWORK_ROOT="$(cd "$(dirname "$BATS_TEST_DIRNAME")" && pwd)"
    TEMPLATE="$FRAMEWORK_ROOT/user-preferences.example.yaml"
    BACKUP="$FRAMEWORK_ROOT/user-preferences.example.yaml.bak"
    
    if [ -f "$TEMPLATE" ]; then
        mv "$TEMPLATE" "$BACKUP"
        
        run bash "$INIT_SCRIPT" testuser
        [ "$status" -ne 0 ]
        [[ "$output" == *"Template not found"* ]]
        
        mv "$BACKUP" "$TEMPLATE"
    fi
}

@test "init-user.sh: requires username" {
    # Run without username and with empty stdin
    run bash -c "echo '' | bash '$INIT_SCRIPT'"
    [ "$status" -ne 0 ]
    [[ "$output" == *"Username is required"* ]]
}
