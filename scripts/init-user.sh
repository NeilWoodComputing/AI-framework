#!/usr/bin/env bash
# init-user.sh
# ---------------------------------------------------------------------------
# Initialises or refreshes a user's ai-framework configuration.
#
# This script:
#   1. Creates or updates the user preferences file
#   2. Caches the framework and resolved config on the bot machine
#   3. Is safe to re-run (idempotent)
#   4. Migrates from old users/<name>.yaml format if found
#
# Usage:
#   ./scripts/init-user.sh [username]
#
# If username is not provided, it uses $USER or prompts for input.
# The username is used only to fill the `user:` field in the config file.
# ---------------------------------------------------------------------------

set -euo pipefail

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# Script directory and framework root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Configuration
BOT_MACHINE_CONFIG="${AI_FRAMEWORK_USER_CONFIG:-/home/box/ai-framework/user-preferences.yaml}"
LOCAL_CONFIG="${AI_FRAMEWORK_USER_CONFIG:-$HOME/.ai-framework/user-preferences.yaml}"
BOT_MACHINE_CACHE_DIR="${AI_FRAMEWORK_BOT_CACHE_DIR:-/home/box/ai-framework/cache}"

echo -e "${BLUE}=== AI Framework User Initialisation ===${NC}\n"

# Determine username
USERNAME="${1:-${USER:-}}"
if [[ -z "$USERNAME" ]]; then
    read -p "Enter your username: " USERNAME
fi

if [[ -z "$USERNAME" ]]; then
    echo -e "${RED}Error: Username is required${NC}"
    exit 1
fi

echo -e "Username: ${GREEN}$USERNAME${NC}"

# Determine if we're on the bot machine and which config file to use
IS_BOT_MACHINE=false
if [[ -d "/home/box" ]] && [[ -w "/home/box" ]]; then
    IS_BOT_MACHINE=true
    echo -e "Environment: ${GREEN}Bot machine${NC}"
    USER_CONFIG_FILE="$BOT_MACHINE_CONFIG"
else
    echo -e "Environment: ${GREEN}Local developer machine${NC}"
    USER_CONFIG_FILE="$LOCAL_CONFIG"
fi

# Step 1: Create or update user preference file
echo -e "\n${BLUE}Step 1: User preferences file${NC}"
echo "Location: $USER_CONFIG_FILE"

# Check for migration from old format
OLD_USER_DIR="$(dirname "$USER_CONFIG_FILE")/users"
OLD_USER_FILE="$OLD_USER_DIR/$USERNAME.yaml"

if [[ -f "$OLD_USER_FILE" ]] && [[ ! -f "$USER_CONFIG_FILE" ]]; then
    echo -e "${YELLOW}Found old user config format at $OLD_USER_FILE${NC}"
    echo "Migrating to new single-file format..."
    
    # Ensure directory exists
    mkdir -p "$(dirname "$USER_CONFIG_FILE")"
    
    # Copy old file to new location
    cp "$OLD_USER_FILE" "$USER_CONFIG_FILE"
    
    echo -e "${GREEN}✓ Migrated from old format${NC}"
    echo "Old file preserved at: $OLD_USER_FILE"
    echo "You can safely delete the old users/ directory after verification."
elif [[ -f "$USER_CONFIG_FILE" ]]; then
    echo -e "${YELLOW}Existing config found. Keeping existing preferences.${NC}"
    echo "To reset preferences, delete $USER_CONFIG_FILE and re-run this script."
else
    # Create new config
    echo "Creating new user preferences file from template..."
    
    # Ensure directory exists
    mkdir -p "$(dirname "$USER_CONFIG_FILE")"
    
    cat > "$USER_CONFIG_FILE" << EOF
# User preferences for ai-framework
# ---------------------------------------------------------------------------
# This file contains runtime preferences that override the shared
# ai-framework.config.yaml settings. It should NOT be committed to the
# repository.
#
# One file per machine: each person runs the framework on their own bot machine,
# so only one person's preferences live on a given machine.
#
# Location precedence (highest to lowest):
#   1. User preferences file (this file)
#   2. Per-role setting in ai-framework.config.yaml (runtime.<role>)
#   3. Shared default in ai-framework.config.yaml (runtime.default)
# ---------------------------------------------------------------------------

# Your username (for identification only)
user: $USERNAME

# Runtime preferences
# Supported runtimes:
#   cursor        - Cursor Cloud Agents (Cursor-managed VMs). This is the
#                   shared default. The bot machine coordinates cloud agent work.
#                   Local Windows PC execution is NEVER the default.
#   cursor-local  - Cursor IDE on your local machine (opt-in only, not the default)
#   claude-code   - Claude Code or other Claude interfaces
#
# Uncomment and set the default to override the shared default for all your roles.
# runtime:
#   default: cursor

# Per-role overrides (optional). Uncomment and set to override for specific roles.
# runtime:
#   planning: cursor
#   code: cursor
#   review: cursor
#   testing: cursor
EOF
    echo -e "${GREEN}✓ Created user preferences file${NC}"
fi

# Step 2: Cache framework on bot machine
if [[ "$IS_BOT_MACHINE" == true ]]; then
    echo -e "\n${BLUE}Step 2: Cache framework on bot machine${NC}"
    echo "Cache location: $BOT_MACHINE_CACHE_DIR"
    
    mkdir -p "$BOT_MACHINE_CACHE_DIR"
    
    # Check if it's a git repo we can pull, otherwise copy
    if [[ -d "$BOT_MACHINE_CACHE_DIR/.git" ]]; then
        echo "Updating cached framework (git pull)..."
        cd "$BOT_MACHINE_CACHE_DIR"
        git pull origin main 2>/dev/null || {
            echo -e "${YELLOW}Warning: git pull failed. Falling back to copying files.${NC}"
            cd "$FRAMEWORK_ROOT"
            rsync -a --delete --exclude='.git' --exclude='node_modules' --exclude='bin' --exclude='obj' \
                  "$FRAMEWORK_ROOT/" "$BOT_MACHINE_CACHE_DIR/"
        }
        cd "$FRAMEWORK_ROOT"
    else
        echo "Creating cached copy of framework..."
        # If cache dir exists but isn't a git repo, clear it first
        if [[ -d "$BOT_MACHINE_CACHE_DIR" ]]; then
            rm -rf "$BOT_MACHINE_CACHE_DIR"
        fi
        
        # Try to clone, fall back to copy
        if git remote get-url origin &>/dev/null; then
            REMOTE_URL=$(git remote get-url origin)
            git clone "$REMOTE_URL" "$BOT_MACHINE_CACHE_DIR" 2>/dev/null || {
                echo -e "${YELLOW}Warning: git clone failed. Copying files instead.${NC}"
                mkdir -p "$BOT_MACHINE_CACHE_DIR"
                rsync -a --exclude='.git' --exclude='node_modules' --exclude='bin' --exclude='obj' \
                      "$FRAMEWORK_ROOT/" "$BOT_MACHINE_CACHE_DIR/"
            }
        else
            mkdir -p "$BOT_MACHINE_CACHE_DIR"
            rsync -a --exclude='.git' --exclude='node_modules' --exclude='bin' --exclude='obj' \
                  "$FRAMEWORK_ROOT/" "$BOT_MACHINE_CACHE_DIR/"
        fi
    fi
    
    echo -e "${GREEN}✓ Framework cached${NC}"
    
    # Save resolved configuration
    echo "Saving resolved configuration..."
    RESOLVED_CONFIG="$BOT_MACHINE_CACHE_DIR/.resolved-config-$USERNAME.yaml"
    cat > "$RESOLVED_CONFIG" << EOF
# Resolved configuration for $USERNAME
# Generated: $(date -Iseconds)
# User config: $USER_CONFIG_FILE
# Shared config: $FRAMEWORK_ROOT/ai-framework.config.yaml

# This file shows the effective runtime configuration after merging:
#   1. User preferences ($USER_CONFIG_FILE)
#   2. Shared config (ai-framework.config.yaml)

# To see your effective configuration, agents should:
#   1. Read user preferences file if it exists
#   2. Read shared config
#   3. Merge with precedence: user preferences > per-role > default

user: $USERNAME
user_config: $USER_CONFIG_FILE
shared_config: $FRAMEWORK_ROOT/ai-framework.config.yaml
EOF
    echo -e "${GREEN}✓ Resolved config saved to $RESOLVED_CONFIG${NC}"
else
    echo -e "\n${BLUE}Step 2: Bot machine cache${NC}"
    echo -e "${YELLOW}Skipped (not on bot machine)${NC}"
    echo "The bot machine will need its own initialisation to cache the framework."
fi

# Summary
echo -e "\n${GREEN}=== Initialisation Complete ===${NC}\n"
echo "User preferences: $USER_CONFIG_FILE"
if [[ "$IS_BOT_MACHINE" == true ]]; then
    echo "Framework cache: $BOT_MACHINE_CACHE_DIR"
fi
echo ""
echo "Next steps:"
echo "  1. Edit $USER_CONFIG_FILE to set your runtime preferences"
echo "  2. Agents will automatically resolve configuration from:"
echo "     - Your user preferences file (highest priority)"
echo "     - Per-role settings in ai-framework.config.yaml"
echo "     - Shared default in ai-framework.config.yaml (lowest priority)"
echo ""
echo "To switch to a different runtime (e.g. claude-code), edit the user preferences file."
echo "See README.md for more details."
