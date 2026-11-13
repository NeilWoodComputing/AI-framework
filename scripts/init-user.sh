#!/usr/bin/env bash
# init-user.sh
# ---------------------------------------------------------------------------
# Initialises or refreshes a user's ai-framework configuration.
#
# This script:
#   1. Creates or updates the user's preference file
#   2. Caches the framework and resolved config on the bot machine
#   3. Is safe to re-run (idempotent)
#
# Usage:
#   ./scripts/init-user.sh [username]
#
# If username is not provided, it uses $USER or prompts for input.
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
BOT_MACHINE_USER_DIR="${AI_FRAMEWORK_BOT_USER_DIR:-/home/box/ai-framework/users}"
BOT_MACHINE_CACHE_DIR="${AI_FRAMEWORK_BOT_CACHE_DIR:-/home/box/ai-framework/cache}"
LOCAL_USER_DIR="${AI_FRAMEWORK_LOCAL_USER_DIR:-$HOME/.ai-framework/users}"

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

# Determine if we're on the bot machine
IS_BOT_MACHINE=false
if [[ -d "/home/box" ]] && [[ -w "/home/box" ]]; then
    IS_BOT_MACHINE=true
    echo -e "Environment: ${GREEN}Bot machine${NC}"
    USER_CONFIG_DIR="$BOT_MACHINE_USER_DIR"
else
    echo -e "Environment: ${GREEN}Local developer machine${NC}"
    USER_CONFIG_DIR="$LOCAL_USER_DIR"
fi

USER_CONFIG_FILE="$USER_CONFIG_DIR/$USERNAME.yaml"

# Step 1: Create or update user preference file
echo -e "\n${BLUE}Step 1: User preference file${NC}"
echo "Location: $USER_CONFIG_FILE"

mkdir -p "$USER_CONFIG_DIR"

if [[ -f "$USER_CONFIG_FILE" ]]; then
    echo -e "${YELLOW}Existing config found. Keeping existing preferences.${NC}"
    echo "To reset preferences, delete $USER_CONFIG_FILE and re-run this script."
else
    echo "Creating new user config from template..."
    cat > "$USER_CONFIG_FILE" << EOF
# User preferences for ai-framework
# ---------------------------------------------------------------------------
# This file contains per-user runtime preferences that override the shared
# ai-framework.config.yaml settings. It should NOT be committed to the
# repository.
#
# Location precedence (highest to lowest):
#   1. User config file (this file)
#   2. Per-role setting in ai-framework.config.yaml (runtime.<role>)
#   3. Shared default in ai-framework.config.yaml (runtime.default)
# ---------------------------------------------------------------------------

# Your username (for identification only)
user: $USERNAME

# Runtime preferences
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
    echo -e "${GREEN}✓ Created user config${NC}"
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
#   1. Read user config if it exists
#   2. Read shared config
#   3. Merge with precedence: user > per-role > default

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
echo "User config: $USER_CONFIG_FILE"
if [[ "$IS_BOT_MACHINE" == true ]]; then
    echo "Framework cache: $BOT_MACHINE_CACHE_DIR"
fi
echo ""
echo "Next steps:"
echo "  1. Edit $USER_CONFIG_FILE to set your runtime preferences"
echo "  2. Agents will automatically resolve configuration from:"
echo "     - Your user config (highest priority)"
echo "     - Per-role settings in ai-framework.config.yaml"
echo "     - Shared default in ai-framework.config.yaml (lowest priority)"
echo ""
echo "To switch to a different runtime (e.g. claude-code), edit the user config file."
echo "See README.md for more details."
