# ============================================
# GitHub Release Upload Script
# Usage:
#   $env:GITHUB_TOKEN = "your-token-here"
#   .\release_binary.ps1 -Version "v1.0"
# ============================================
param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    [switch]$UploadOnly
)

# Configuration
$REPO       = "luohuazju/roblox-game"
$ASSET_PATH = "D:\work\sillycat\roblox-game\dist\WolfGod_windows.zip"
$ASSET_NAME = "WolfGod_windows.zip"
# -----------------------------------------------------------------------

# Check token
if (-not $env:GITHUB_TOKEN) {
    Write-Host "[ERROR] GITHUB_TOKEN environment variable is not set." -ForegroundColor Red
    Write-Host "   Please run: `$env:GITHUB_TOKEN = 'your-token-here'" -ForegroundColor Yellow
    exit 1
}

# Check asset file exists
if (-not (Test-Path $ASSET_PATH)) {
    Write-Host "[ERROR] Binary not found at $ASSET_PATH" -ForegroundColor Red
    Write-Host "   Please run build_windows.bat first." -ForegroundColor Yellow
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $env:GITHUB_TOKEN"
    "Accept"        = "application/vnd.github+json"
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  GitHub Release Upload" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Repo   : $REPO"
Write-Host "  Version: $Version"
Write-Host "  Asset  : $ASSET_NAME"
Write-Host ""

# Step 1: Create or fetch the release
if ($UploadOnly) {
    Write-Host "[1/2] Fetching existing release $Version ..." -ForegroundColor Yellow
    try {
        $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$REPO/releases/tags/$Version" `
            -Headers $headers
        Write-Host "[OK] Found release: $($release.html_url)" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to find release $Version : $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[1/2] Creating release $Version ..." -ForegroundColor Yellow
    $releaseBody = @{
        tag_name         = $Version
        name             = "Wolf God $Version - Windows 11"
        body             = "## Wolf God Flying Game - Windows 11 Build`n`n- Platform: Windows 11 x86_64`n- Built with PyInstaller`n- No Python installation required`n`n### How to Play`n1. Download and unzip WolfGod_windows.zip`n2. Double-click WolfGod_windows.exe`n3. Enjoy the game!"
        draft            = $false
        prerelease       = $false
    } | ConvertTo-Json
    try {
        $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$REPO/releases" `
            -Method Post `
            -Headers $headers `
            -Body $releaseBody `
            -ContentType "application/json"
        Write-Host "[OK] Release created: $($release.html_url)" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to create release: $_" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Upload the binary
Write-Host ""
Write-Host "[2/2] Uploading $ASSET_NAME ..." -ForegroundColor Yellow
$uploadUrl = $release.upload_url -replace '[{]\?name,label[}]', "?name=$ASSET_NAME"
$fileBytes = [System.IO.File]::ReadAllBytes($ASSET_PATH)
$fileSize  = [math]::Round($fileBytes.Length / 1MB, 1)
Write-Host "   File size: $fileSize MB"

try {
    $upload = Invoke-RestMethod -Uri $uploadUrl `
        -Method Post `
        -Headers $headers `
        -Body $fileBytes `
        -ContentType "application/octet-stream"
    Write-Host "[OK] Upload complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  Release URL:" -ForegroundColor Cyan
    Write-Host "  $($release.html_url)" -ForegroundColor Cyan
    Write-Host "  Download URL:" -ForegroundColor Cyan
    Write-Host "  $($upload.browser_download_url)" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
} catch {
    Write-Host "[ERROR] Failed to upload asset: $_" -ForegroundColor Red
    exit 1
}