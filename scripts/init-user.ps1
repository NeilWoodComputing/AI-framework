# init-user.ps1
# ---------------------------------------------------------------------------
# Initialises or refreshes user preferences for ai-framework.
#
# Creates or updates user-preferences.yaml and caches the framework on the
# bot machine. Safe to re-run (idempotent).
#
# Usage:
#   .\scripts\init-user.ps1 [-Username <username>]
#   $env:AI_FRAMEWORK_BOT_MACHINE="true"; .\scripts\init-user.ps1
#
# Username is optional and fills the `user:` field only.
# Set AI_FRAMEWORK_BOT_MACHINE=true to enable bot machine caching.
# ---------------------------------------------------------------------------

param(
    [string]$Username = $env:USERNAME
)

$ErrorActionPreference = "Stop"

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FrameworkRoot = Split-Path -Parent $ScriptDir
$TemplateFile = Join-Path $FrameworkRoot "user-preferences.example.yaml"

# Configuration from environment
$IsBotMachine = ($env:AI_FRAMEWORK_BOT_MACHINE -eq "true")
$BotMachineConfig = if ($env:AI_FRAMEWORK_USER_CONFIG) { $env:AI_FRAMEWORK_USER_CONFIG } else { "/home/box/ai-framework/user-preferences.yaml" }
$LocalConfig = if ($env:AI_FRAMEWORK_USER_CONFIG) { $env:AI_FRAMEWORK_USER_CONFIG } else { "$env:USERPROFILE\.ai-framework\user-preferences.yaml" }
$BotMachineCacheDir = if ($env:AI_FRAMEWORK_BOT_CACHE_DIR) { $env:AI_FRAMEWORK_BOT_CACHE_DIR } else { "/home/box/ai-framework/cache" }

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

# Determine config file location
if ($IsBotMachine) {
    Write-Host "Environment: " -NoNewline
    Write-Host "Bot machine" -ForegroundColor Green
    $UserConfigFile = $BotMachineConfig
} else {
    Write-Host "Environment: " -NoNewline
    Write-Host "Local developer machine" -ForegroundColor Green
    $UserConfigFile = $LocalConfig
}

# Step 1: Create or update user preferences file
Write-Host "`nStep 1: User preferences file" -ForegroundColor Blue
Write-Host "Location: $UserConfigFile"

# Check for migration from old format (users/<name>.yaml)
$UserConfigDir = Split-Path -Parent $UserConfigFile
$OldUserDir = Join-Path $UserConfigDir "users"
$OldUserFile = Join-Path $OldUserDir "$Username.yaml"

if ((Test-Path $OldUserFile) -and -not (Test-Path $UserConfigFile)) {
    Write-Host "Migrating from old format: $OldUserFile" -ForegroundColor Yellow
    $ParentDir = Split-Path -Parent $UserConfigFile
    if (-not (Test-Path $ParentDir)) {
        New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
    }
    Copy-Item -Path $OldUserFile -Destination $UserConfigFile -Force
    Write-Host "✓ Migrated " -ForegroundColor Green -NoNewline
    Write-Host "(old file preserved; safe to delete users/ directory)"
} elseif (Test-Path $UserConfigFile) {
    Write-Host "Existing config found. Keeping current settings." -ForegroundColor Yellow
} else {
    # Create from template
    if (-not (Test-Path $TemplateFile)) {
        Write-Host "Error: Template not found: $TemplateFile" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Creating from template..."
    $ParentDir = Split-Path -Parent $UserConfigFile
    if (-not (Test-Path $ParentDir)) {
        New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
    }
    
    # Generate config by replacing example-user with actual username
    $Content = Get-Content $TemplateFile -Raw
    $Content = $Content -replace 'user: example-user', "user: $Username"
    Set-Content -Path $UserConfigFile -Value $Content -Encoding UTF8 -NoNewline
    
    Write-Host "✓ Created user preferences file" -ForegroundColor Green
}

# Step 2: Cache framework on bot machine
if ($IsBotMachine) {
    Write-Host "`nStep 2: Cache framework on bot machine" -ForegroundColor Blue
    Write-Host "Cache location: $BotMachineCacheDir"
    
    if (-not (Test-Path $BotMachineCacheDir)) {
        New-Item -ItemType Directory -Path $BotMachineCacheDir -Force | Out-Null
    }
    
    # Try git pull if already a repo, otherwise clone or copy
    $CacheGitDir = Join-Path $BotMachineCacheDir ".git"
    if (Test-Path $CacheGitDir) {
        Write-Host "Updating cache (git pull)..."
        Push-Location $BotMachineCacheDir
        try {
            git pull origin main 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Updated from git" -ForegroundColor Green
            } else {
                throw "Git pull failed"
            }
        } catch {
            Write-Host "Warning: git pull failed, trying copy..." -ForegroundColor Yellow
            if (Get-Command robocopy -ErrorAction SilentlyContinue) {
                robocopy $FrameworkRoot $BotMachineCacheDir /E /XD .git node_modules bin obj /NFL /NDL /NJH /NJS | Out-Null
            } else {
                Copy-Item -Path "$FrameworkRoot\*" -Destination $BotMachineCacheDir -Recurse -Force -ErrorAction SilentlyContinue
            }
            Write-Host "✓ Copied" -ForegroundColor Green
        } finally {
            Pop-Location
        }
    } else {
        # Fresh cache: try clone, fall back to copy
        if ((Test-Path $BotMachineCacheDir) -and (Get-ChildItem $BotMachineCacheDir | Measure-Object).Count -gt 0) {
            Remove-Item -Path $BotMachineCacheDir -Recurse -Force
        }
        New-Item -ItemType Directory -Path $BotMachineCacheDir -Force | Out-Null
        
        Push-Location $FrameworkRoot
        try {
            $RemoteUrl = git remote get-url origin 2>&1
            Pop-Location
            
            if ($LASTEXITCODE -eq 0 -and $RemoteUrl) {
                Write-Host "Cloning from $RemoteUrl..."
                git clone --quiet $RemoteUrl $BotMachineCacheDir 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✓ Cloned from git" -ForegroundColor Green
                } else {
                    throw "Git clone failed"
                }
            } else {
                throw "No remote URL"
            }
        } catch {
            Pop-Location -ErrorAction SilentlyContinue
            Write-Host "Warning: git clone failed, copying instead..." -ForegroundColor Yellow
            if (Get-Command robocopy -ErrorAction SilentlyContinue) {
                robocopy $FrameworkRoot $BotMachineCacheDir /E /XD .git node_modules bin obj /NFL /NDL /NJH /NJS | Out-Null
            } else {
                Copy-Item -Path "$FrameworkRoot\*" -Destination $BotMachineCacheDir -Recurse -Force -ErrorAction SilentlyContinue
            }
            Write-Host "✓ Cached" -ForegroundColor Green
        }
    }
} else {
    Write-Host "`nStep 2: Bot machine cache" -ForegroundColor Blue
    Write-Host "Skipped " -ForegroundColor Yellow -NoNewline
    Write-Host "(set AI_FRAMEWORK_BOT_MACHINE=true to enable caching)"
}

# Summary
Write-Host "`n=== Initialisation Complete ===`n" -ForegroundColor Green
Write-Host "User preferences: $UserConfigFile"
if ($IsBotMachine) {
    Write-Host "Framework cache: $BotMachineCacheDir"
}
Write-Host ""
Write-Host "Edit $UserConfigFile to configure runtime preferences."
Write-Host "See README.md for details."
Write-Host ""
