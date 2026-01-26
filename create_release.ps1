# Circuit Repair Game - Release Package Script
# 电路修复游戏 - 发行打包脚本

# Set encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Circuit Repair Game - Release Packager" -ForegroundColor Cyan
Write-Host "电路修复游戏 - 发行打包工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get version from git tag or use default
try {
    $VERSION = git describe --tags --abbrev=0 2>$null
    if (-not $VERSION) {
        $VERSION = "v1.0.1"
    }
} catch {
    $VERSION = "v1.0.1"
}

Write-Host "Version: $VERSION" -ForegroundColor Green
Write-Host ""

# Check if dist directory exists
if (-not (Test-Path "dist\CircuitRepairGame")) {
    Write-Host "ERROR: dist\CircuitRepairGame not found" -ForegroundColor Red
    Write-Host "Please run build.bat first to create the package" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create release directory
$RELEASE_DIR = "release"
if (-not (Test-Path $RELEASE_DIR)) {
    New-Item -ItemType Directory -Path $RELEASE_DIR | Out-Null
}

# Package name
$PACKAGE_NAME = "CircuitRepairGame-$VERSION-win64"

# Step 1: Copy files
Write-Host "[1/4] Copying files..." -ForegroundColor Yellow

# Remove old package directory if exists
if (Test-Path "$RELEASE_DIR\$PACKAGE_NAME") {
    Remove-Item -Path "$RELEASE_DIR\$PACKAGE_NAME" -Recurse -Force
}

# Copy the game directory
Copy-Item -Path "dist\CircuitRepairGame" -Destination "$RELEASE_DIR\$PACKAGE_NAME" -Recurse

# Copy user readme
if (Test-Path "README_USER.txt") {
    Copy-Item -Path "README_USER.txt" -Destination "$RELEASE_DIR\$PACKAGE_NAME\README.txt" -Force
}

# Copy license
if (Test-Path "LICENSE") {
    Copy-Item -Path "LICENSE" -Destination "$RELEASE_DIR\$PACKAGE_NAME\LICENSE.txt" -Force
}

# Copy changelog
if (Test-Path "CHANGELOG.md") {
    Copy-Item -Path "CHANGELOG.md" -Destination "$RELEASE_DIR\$PACKAGE_NAME\CHANGELOG.txt" -Force
}

Write-Host "OK: Files copied" -ForegroundColor Green
Write-Host ""

# Step 2: Verify package
Write-Host "[2/4] Verifying package..." -ForegroundColor Yellow

try {
    $verifyResult = python tools\scripts\verify_package.py "$RELEASE_DIR\$PACKAGE_NAME" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK: Package verified" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Package verification failed" -ForegroundColor Yellow
        Write-Host "Please check the package manually" -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARNING: Could not run verification script" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Create ZIP archive
Write-Host "[3/4] Creating ZIP archive..." -ForegroundColor Yellow

# Remove old zip if exists
$ZIP_PATH = "$RELEASE_DIR\$PACKAGE_NAME.zip"
if (Test-Path $ZIP_PATH) {
    Remove-Item -Path $ZIP_PATH -Force
}

# Create zip
try {
    Compress-Archive -Path "$RELEASE_DIR\$PACKAGE_NAME" -DestinationPath $ZIP_PATH -CompressionLevel Optimal

    # Get zip file size
    $ZIP_SIZE = (Get-Item $ZIP_PATH).Length
    $ZIP_SIZE_MB = [math]::Round($ZIP_SIZE / 1MB, 1)

    Write-Host "OK: ZIP created ($ZIP_SIZE_MB MB)" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to create ZIP archive" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Step 4: Generate checksums
Write-Host "[4/4] Generating checksums..." -ForegroundColor Yellow

try {
    # Use certutil (built-in Windows tool, works on all versions)
    $certutilOutput = certutil -hashfile $ZIP_PATH SHA256 2>&1
    if ($LASTEXITCODE -eq 0) {
        # Extract hash from certutil output (second line)
        $lines = $certutilOutput -split "`n"
        $HASH = $lines[1].Trim()
        $HASH | Out-File -FilePath "$ZIP_PATH.sha256" -Encoding ASCII
        Write-Host "OK: Checksum generated" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Could not generate checksum" -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARNING: Could not generate checksum" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Release package created successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Package: $ZIP_PATH" -ForegroundColor White
Write-Host "Size: $ZIP_SIZE_MB MB" -ForegroundColor White
Write-Host "Checksum: $ZIP_PATH.sha256" -ForegroundColor White
Write-Host ""
Write-Host "You can now:" -ForegroundColor Yellow
Write-Host "1. Test the package on a clean machine" -ForegroundColor White
Write-Host "2. Upload to GitHub Releases" -ForegroundColor White
Write-Host "3. Distribute to users" -ForegroundColor White
Write-Host ""

# Show checksum
if (Test-Path "$ZIP_PATH.sha256") {
    Write-Host "SHA256 Checksum:" -ForegroundColor Cyan
    Get-Content "$ZIP_PATH.sha256"
    Write-Host ""
}

# Show package contents summary
Write-Host "Package contents:" -ForegroundColor Cyan
$fileCount = (Get-ChildItem -Path "$RELEASE_DIR\$PACKAGE_NAME" -Recurse -File).Count
$dirCount = (Get-ChildItem -Path "$RELEASE_DIR\$PACKAGE_NAME" -Recurse -Directory).Count
Write-Host "  - $fileCount files" -ForegroundColor White
Write-Host "  - $dirCount directories" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
