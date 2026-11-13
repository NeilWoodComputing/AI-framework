# Pester tests for scripts/init-user.ps1
# Run with: pwsh -Command "Invoke-Pester tests/init-user.Tests.ps1"

BeforeAll {
    $script:FrameworkRoot = Split-Path -Parent $PSScriptRoot
    $script:InitScript = Join-Path $FrameworkRoot "scripts/init-user.ps1"
    $script:TemplateFile = Join-Path $FrameworkRoot "user-preferences.example.yaml"
}

Describe "init-user.ps1" {
    BeforeEach {
        # Create temp directory for each test (cross-platform temp path)
        $TempPath = [System.IO.Path]::GetTempPath()
        $script:TestDir = Join-Path $TempPath "ai-framework-test-$(New-Guid)"
        New-Item -ItemType Directory -Path $script:TestDir -Force | Out-Null
        $env:AI_FRAMEWORK_USER_CONFIG = Join-Path $script:TestDir "user-preferences.yaml"
        $env:AI_FRAMEWORK_BOT_CACHE_DIR = Join-Path $script:TestDir "cache"
        $env:AI_FRAMEWORK_BOT_MACHINE = "false"
    }
    
    AfterEach {
        # Clean up temp directory
        if (Test-Path $script:TestDir) {
            Remove-Item -Path $script:TestDir -Recurse -Force -ErrorAction SilentlyContinue
        }
        Remove-Item Env:\AI_FRAMEWORK_USER_CONFIG -ErrorAction SilentlyContinue
        Remove-Item Env:\AI_FRAMEWORK_BOT_CACHE_DIR -ErrorAction SilentlyContinue
        Remove-Item Env:\AI_FRAMEWORK_BOT_MACHINE -ErrorAction SilentlyContinue
    }
    
    It "creates config from template" {
        & pwsh -NoProfile -File $script:InitScript -Username "testuser" *>$null
        
        $env:AI_FRAMEWORK_USER_CONFIG | Should -Exist
        
        $content = Get-Content $env:AI_FRAMEWORK_USER_CONFIG -Raw
        $content | Should -Match "user: testuser"
        $content | Should -Not -Match "user: example-user"
    }
    
    It "is idempotent - re-run keeps existing settings" {
        # First run
        & pwsh -NoProfile -File $script:InitScript -Username "user1" *>$null
        
        # Add custom content
        Add-Content -Path $env:AI_FRAMEWORK_USER_CONFIG -Value "runtime:"
        Add-Content -Path $env:AI_FRAMEWORK_USER_CONFIG -Value "  code: claude-code"
        
        # Second run with different username
        & pwsh -NoProfile -File $script:InitScript -Username "user2" *>$null
        
        # Should keep original username and settings
        $content = Get-Content $env:AI_FRAMEWORK_USER_CONFIG -Raw
        $content | Should -Match "user: user1"
        $content | Should -Match "code: claude-code"
    }
    
    It "migrates from old users/<name>.yaml format" {
        # Create old format file
        $oldDir = Join-Path (Split-Path $env:AI_FRAMEWORK_USER_CONFIG) "users"
        New-Item -ItemType Directory -Path $oldDir -Force | Out-Null
        $oldFile = Join-Path $oldDir "olduser.yaml"
        
        @"
user: olduser
runtime:
  default: claude-code
"@ | Set-Content -Path $oldFile
        
        # Run init
        & pwsh -NoProfile -File $script:InitScript -Username "olduser" *>$null
        
        # Check migration happened
        $env:AI_FRAMEWORK_USER_CONFIG | Should -Exist
        $content = Get-Content $env:AI_FRAMEWORK_USER_CONFIG -Raw
        $content | Should -Match "user: olduser"
        $content | Should -Match "claude-code"
        
        # Old file should still exist
        $oldFile | Should -Exist
    }
    
    It "respects AI_FRAMEWORK_USER_CONFIG override" {
        $customConfig = Join-Path $script:TestDir "custom/my-config.yaml"
        $env:AI_FRAMEWORK_USER_CONFIG = $customConfig
        
        & pwsh -NoProfile -File $script:InitScript -Username "customuser" *>$null
        
        $customConfig | Should -Exist
        $content = Get-Content $customConfig -Raw
        $content | Should -Match "user: customuser"
    }
    
    It "AI_FRAMEWORK_BOT_MACHINE=false skips caching" {
        $env:AI_FRAMEWORK_BOT_MACHINE = "false"
        
        & pwsh -NoProfile -File $script:InitScript -Username "testuser" *>$null
        
        # Cache directory should not be created
        $env:AI_FRAMEWORK_BOT_CACHE_DIR | Should -Not -Exist
    }
    
    It "AI_FRAMEWORK_BOT_MACHINE=true enables caching" {
        $env:AI_FRAMEWORK_BOT_MACHINE = "true"
        
        & pwsh -NoProfile -File $script:InitScript -Username "testuser" *>$null
        
        # Cache directory should exist
        $env:AI_FRAMEWORK_BOT_CACHE_DIR | Should -Exist
    }
    
    It "handles missing template file gracefully" {
        $backup = "$script:TemplateFile.bak"
        
        if (Test-Path $script:TemplateFile) {
            Move-Item $script:TemplateFile $backup
            
            # Script should exit with non-zero code when template is missing
            & pwsh -NoProfile -File $script:InitScript -Username "testuser" 2>$null
            $LASTEXITCODE | Should -Not -Be 0
            
            Move-Item $backup $script:TemplateFile
        }
    }
}
