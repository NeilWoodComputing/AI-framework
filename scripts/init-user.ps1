# init-user.ps1
# ---------------------------------------------------------------------------
# Initialises or refreshes a user's ai-framework configuration.
#
# This script:
#   1. Creates or updates the user's preference file
#   2. Caches the framework and resolved config on the bot machine
#   3. Is safe to re-run (idempotent)
#
# Usage:
#   .\scripts\init-user.ps1 [-Username <username>]
#
# If Username is not provided, it uses $env:USERNAME or prompts for input.
# ---------------------------------------------------------------------------

param(
    [string]$Username = $env:USERNAME
)

$ErrorActionPreference = "Stop"

# Script directory and framework root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FrameworkRoot = Split-Path -Parent $ScriptDir

# Configuration
$BotMachineUserDir = if ($env:AI_FRAMEWORK_BOT_USER_DIR) { $env:AI_FRAMEWORK_BOT_USER_DIR } else { "/home/box/ai-framework/users" }
$BotMachineCacheDir = if ($env:AI_FRAMEWORK_BOT_CACHE_DIR) { $env:AI_FRAMEWORK_BOT_CACHE_DIR } else { "/home/box/ai-framework/cache" }
$LocalUserDir = if ($env:AI_FRAMEWORK_LOCAL_USER_DIR) { $env:AI_FRAMEWORK_LOCAL_USER_DIR } else { "$env:USERPROFILE\.ai-framework\users" }

Write-Host "`n=== AI Framework User Initialisation ===`n" -ForegroundColor Blue

# Determine username
if ([string]::IsNullOrWhiteSpace($Username)) {
    $Username = Read-Host "Enter your username"
}

if ([string]::IsNullOrWhiteSpace($Username)) {
    Write-Host "Error: Username is required" -ForegroundColor Red
    exit 1
}

Write-Host "Username: " -NoNewline
Write-Host $Username -ForegroundColor Green

# Determine if we're on the bot machine
$IsBotMachine = $false
if (Test-Path "/home/box" -ErrorAction SilentlyContinue) {
    try {
        $null = New-Item -ItemType Directory -Path "/home/box/test-write" -Force -ErrorAction Stop
        Remove-Item "/home/box/test-write" -Force -ErrorAction SilentlyContinue
        $IsBotMachine = $true
    } catch {
        $IsBotMachine = $false
    }
}

if ($IsBotMachine) {
    Write-Host "Environment: " -NoNewline
    Write-Host "Bot machine" -ForegroundColor Green
    $UserConfigDir = $BotMachineUserDir
} else {
    Write-Host "Environment: " -NoNewline
    Write-Host "Local developer machine" -ForegroundColor Green
    $UserConfigDir = $LocalUserDir
}

$UserConfigFile = Join-Path $UserConfigDir "$Username.yaml"

# Step 1: Create or update user preference file
Write-Host "`nStep 1: User preference file" -ForegroundColor Blue
Write-Host "Location: $UserConfigFile"

if (-not (Test-Path $UserConfigDir)) {
    New-Item -ItemType Directory -Path $UserConfigDir -Force | Out-Null
}

if (Test-Path $UserConfigFile) {
    Write-Host "Existing config found. Keeping existing preferences." -ForegroundColor Yellow
    Write-Host "To reset preferences, delete $UserConfigFile and re-run this script."
} else {
    Write-Host "Creating new user config from template..."
    
    $ConfigContent = @"
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
user: $Username

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
"@
    
    Set-Content -Path $UserConfigFile -Value $ConfigContent -Encoding UTF8
    Write-Host "✓ Created user config" -ForegroundColor Green
}

# Step 2: Cache framework on bot machine
if ($IsBotMachine) {
    Write-Host "`nStep 2: Cache framework on bot machine" -ForegroundColor Blue
    Write-Host "Cache location: $BotMachineCacheDir"
    
    if (-not (Test-Path $BotMachineCacheDir)) {
        New-Item -ItemType Directory -Path $BotMachineCacheDir -Force | Out-Null
    }
    
    # Check if it's a git repo we can pull, otherwise copy
    $CacheGitDir = Join-Path $BotMachineCacheDir ".git"
    if (Test-Path $CacheGitDir) {
        Write-Host "Updating cached framework (git pull)..."
        Push-Location $BotMachineCacheDir
        try {
            git pull origin main 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "Git pull failed"
            }
        } catch {
            Write-Host "Warning: git pull failed. Falling back to copying files." -ForegroundColor Yellow
            Pop-Location
            # Copy files (excluding specific directories)
            $ExcludeDirs = @('.git', 'node_modules', 'bin', 'obj')
            Get-ChildItem -Path $FrameworkRoot -Recurse | Where-Object {
                $item = $_
                -not ($ExcludeDirs | Where-Object { $item.FullName -like "*\$_\*" -or $item.FullName -like "*/$_/*" })
            } | Copy-Item -Destination { Join-Path $BotMachineCacheDir $_.FullName.Substring($FrameworkRoot.Length) } -Force
        }
        Pop-Location
    } else {
        Write-Host "Creating cached copy of framework..."
        
        # Try to clone, fall back to copy
        try {
            Push-Location $FrameworkRoot
            $RemoteUrl = git remote get-url origin 2>&1
            Pop-Location
            
            if ($LASTEXITCODE -eq 0 -and $RemoteUrl) {
                git clone $RemoteUrl $BotMachineCacheDir 2>&1 | Out-Null
                if ($LASTEXITCODE -ne 0) {
                    throw "Git clone failed"
                }
            } else {
                throw "No remote URL"
            }
        } catch {
            Write-Host "Warning: git clone failed. Copying files instead." -ForegroundColor Yellow
            # Copy files excluding specific directories
            robocopy $FrameworkRoot $BotMachineCacheDir /E /XD .git node_modules bin obj /NFL /NDL /NJH /NJS | Out-Null
        }
    }
    
    Write-Host "✓ Framework cached" -ForegroundColor Green
    
    # Save resolved configuration
    Write-Host "Saving resolved configuration..."
    $ResolvedConfig = Join-Path $BotMachineCacheDir ".resolved-config-$Username.yaml"
    $Timestamp = Get-Date -Format "o"
    
    $ResolvedContent = @"
# Resolved configuration for $Username
# Generated: $Timestamp
# User config: $UserConfigFile
# Shared config: $FrameworkRoot/ai-framework.config.yaml

# This file shows the effective runtime configuration after merging:
#   1. User preferences ($UserConfigFile)
#   2. Shared config (ai-framework.config.yaml)

# To see your effective configuration, agents should:
#   1. Read user config if it exists
#   2. Read shared config
#   3. Merge with precedence: user > per-role > default

user: $Username
user_config: $UserConfigFile
shared_config: $FrameworkRoot/ai-framework.config.yaml
"@
    
    Set-Content -Path $ResolvedConfig -Value $ResolvedContent -Encoding UTF8
    Write-Host "✓ Resolved config saved to $ResolvedConfig" -ForegroundColor Green
} else {
    Write-Host "`nStep 2: Bot machine cache" -ForegroundColor Blue
    Write-Host "Skipped (not on bot machine)" -ForegroundColor Yellow
    Write-Host "The bot machine will need its own initialisation to cache the framework."
}

# Summary
Write-Host "`n=== Initialisation Complete ===`n" -ForegroundColor Green
Write-Host "User config: $UserConfigFile"
if ($IsBotMachine) {
    Write-Host "Framework cache: $BotMachineCacheDir"
}
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit $UserConfigFile to set your runtime preferences"
Write-Host "  2. Agents will automatically resolve configuration from:"
Write-Host "     - Your user config (highest priority)"
Write-Host "     - Per-role settings in ai-framework.config.yaml"
Write-Host "     - Shared default in ai-framework.config.yaml (lowest priority)"
Write-Host ""
Write-Host "To switch to a different runtime (e.g. claude-code), edit the user config file."
Write-Host "See README.md for more details."
Write-Host ""
