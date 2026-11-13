#!/usr/bin/env bash
# init-user.sh
# ---------------------------------------------------------------------------
# Initialises or refreshes user preferences for ai-framework.
#
# Creates or updates user-preferences.yaml and caches the framework on the
# bot machine. Safe to re-run (idempotent).
#
# Usage:
#   ./scripts/init-user.sh [username]
#   AI_FRAMEWORK_BOT_MACHINE=true ./scripts/init-user.sh [username]
#
# Username is optional and fills the `user:` field only.
# Set AI_FRAMEWORK_BOT_MACHINE=true to enable bot machine caching.
# ---------------------------------------------------------------------------

set -euo pipefail

# Colours
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Paths
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly TEMPLATE_FILE="$FRAMEWORK_ROOT/user-preferences.example.yaml"

# Configuration from environment
readonly IS_BOT_MACHINE="${AI_FRAMEWORK_BOT_MACHINE:-false}"
readonly BOT_MACHINE_CONFIG="${AI_FRAMEWORK_USER_CONFIG:-/home/box/ai-framework/user-preferences.yaml}"
readonly LOCAL_CONFIG="${AI_FRAMEWORK_USER_CONFIG:-$HOME/.ai-framework/user-preferences.yaml}"
readonly BOT_MACHINE_CACHE_DIR="${AI_FRAMEWORK_BOT_CACHE_DIR:-/home/box/ai-framework/cache}"

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

# Determine config file location
if [[ "$IS_BOT_MACHINE" == "true" ]]; then
    echo -e "Environment: ${GREEN}Bot machine${NC}"
    USER_CONFIG_FILE="$BOT_MACHINE_CONFIG"
else
    echo -e "Environment: ${GREEN}Local developer machine${NC}"
    USER_CONFIG_FILE="$LOCAL_CONFIG"
fi

# Step 1: Create or update user preferences file
echo -e "\n${BLUE}Step 1: User preferences file${NC}"
echo "Location: $USER_CONFIG_FILE"

# Check for migration from old format (users/<name>.yaml)
OLD_USER_DIR="$(dirname "$USER_CONFIG_FILE")/users"
OLD_USER_FILE="$OLD_USER_DIR/$USERNAME.yaml"

if [[ -f "$OLD_USER_FILE" ]] && [[ ! -f "$USER_CONFIG_FILE" ]]; then
    echo -e "${YELLOW}Migrating from old format: $OLD_USER_FILE${NC}"
    mkdir -p "$(dirname "$USER_CONFIG_FILE")"
    cp "$OLD_USER_FILE" "$USER_CONFIG_FILE"
    echo -e "${GREEN}✓ Migrated${NC} (old file preserved; safe to delete users/ directory)"
elif [[ -f "$USER_CONFIG_FILE" ]]; then
    echo -e "${YELLOW}Existing config found. Keeping current settings.${NC}"
else
    # Create from template
    if [[ ! -f "$TEMPLATE_FILE" ]]; then
        echo -e "${RED}Error: Template not found: $TEMPLATE_FILE${NC}"
        exit 1
    fi
    
    echo "Creating from template..."
    mkdir -p "$(dirname "$USER_CONFIG_FILE")"
    
    # Generate config by replacing example-user with actual username
    sed "s/user: example-user/user: $USERNAME/" "$TEMPLATE_FILE" > "$USER_CONFIG_FILE"
    
    echo -e "${GREEN}✓ Created user preferences file${NC}"
fi

# Step 2: Cache framework on bot machine
if [[ "$IS_BOT_MACHINE" == "true" ]]; then
    echo -e "\n${BLUE}Step 2: Cache framework on bot machine${NC}"
    echo "Cache location: $BOT_MACHINE_CACHE_DIR"
    
    mkdir -p "$BOT_MACHINE_CACHE_DIR"
    
    # Try git pull if already a repo, otherwise clone or copy
    if [[ -d "$BOT_MACHINE_CACHE_DIR/.git" ]]; then
        echo "Updating cache (git pull)..."
        if (cd "$BOT_MACHINE_CACHE_DIR" && git pull origin main 2>/dev/null); then
            echo -e "${GREEN}✓ Updated from git${NC}"
        else
            echo -e "${YELLOW}Warning: git pull failed, trying copy...${NC}"
            if command -v rsync &>/dev/null; then
                rsync -a --delete --exclude='.git' --exclude='node_modules' --exclude='bin' --exclude='obj' \
                      "$FRAMEWORK_ROOT/" "$BOT_MACHINE_CACHE_DIR/"
                echo -e "${GREEN}✓ Copied with rsync${NC}"
            else
                cp -r "$FRAMEWORK_ROOT"/* "$BOT_MACHINE_CACHE_DIR/" 2>/dev/null || true
                echo -e "${GREEN}✓ Copied${NC}"
            fi
        fi
    else
        # Fresh cache: try clone, fall back to copy
        if [[ -d "$BOT_MACHINE_CACHE_DIR" ]] && [[ -n "$(ls -A "$BOT_MACHINE_CACHE_DIR")" ]]; then
            rm -rf "$BOT_MACHINE_CACHE_DIR"
        fi
        mkdir -p "$BOT_MACHINE_CACHE_DIR"
        
        if git remote get-url origin &>/dev/null; then
            REMOTE_URL=$(git remote get-url origin)
            echo "Cloning from $REMOTE_URL..."
            if git clone --quiet "$REMOTE_URL" "$BOT_MACHINE_CACHE_DIR" 2>/dev/null; then
                echo -e "${GREEN}✓ Cloned from git${NC}"
            else
                echo -e "${YELLOW}Warning: git clone failed, copying instead...${NC}"
                if command -v rsync &>/dev/null; then
                    rsync -a --exclude='.git' --exclude='node_modules' --exclude='bin' --exclude='obj' \
                          "$FRAMEWORK_ROOT/" "$BOT_MACHINE_CACHE_DIR/"
                else
                    cp -r "$FRAMEWORK_ROOT"/* "$BOT_MACHINE_CACHE_DIR/" 2>/dev/null || true
                fi
                echo -e "${GREEN}✓ Cached${NC}"
            fi
        else
            echo "No git remote, copying..."
            if command -v rsync &>/dev/null; then
                rsync -a --exclude='.git' --exclude='node_modules' --exclude='bin' --exclude='obj' \
                      "$FRAMEWORK_ROOT/" "$BOT_MACHINE_CACHE_DIR/"
            else
                cp -r "$FRAMEWORK_ROOT"/* "$BOT_MACHINE_CACHE_DIR/" 2>/dev/null || true
            fi
            echo -e "${GREEN}✓ Cached${NC}"
        fi
    fi
else
    echo -e "\n${BLUE}Step 2: Bot machine cache${NC}"
    echo -e "${YELLOW}Skipped${NC} (set AI_FRAMEWORK_BOT_MACHINE=true to enable caching)"
fi

# Summary
echo -e "\n${GREEN}=== Initialisation Complete ===${NC}\n"
echo "User preferences: $USER_CONFIG_FILE"
if [[ "$IS_BOT_MACHINE" == "true" ]]; then
    echo "Framework cache: $BOT_MACHINE_CACHE_DIR"
fi
echo ""
echo "Edit $USER_CONFIG_FILE to configure runtime preferences."
echo "See README.md for details."
