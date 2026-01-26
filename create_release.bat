@echo off
REM Circuit Repair Game - Release Package Script
setlocal enabledelayedexpansion

echo ========================================
echo Circuit Repair Game - Release Packager
echo ========================================
echo.

REM Get version from git tag or use default
for /f "tokens=*" %%i in ('git describe --tags --abbrev=0 2^>nul') do set VERSION=%%i
if "%VERSION%"=="" set VERSION=v1.0.1

echo Version: %VERSION%
echo.

REM Check if dist directory exists
if not exist "dist\CircuitRepairGame" (
    echo ERROR: dist\CircuitRepairGame not found
    echo Please run build.bat first to create the package
    pause
    exit /b 1
)

REM Create release directory
set RELEASE_DIR=release
if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"

REM Package name
set PACKAGE_NAME=CircuitRepairGame-%VERSION%-win64

echo [1/4] Copying files...
REM Copy the game directory
if exist "%RELEASE_DIR%\%PACKAGE_NAME%" rmdir /s /q "%RELEASE_DIR%\%PACKAGE_NAME%"
xcopy /E /I /Q "dist\CircuitRepairGame" "%RELEASE_DIR%\%PACKAGE_NAME%"

REM Copy user readme
copy /Y "README_USER.txt" "%RELEASE_DIR%\%PACKAGE_NAME%\README.txt"

REM Copy license
if exist "LICENSE" copy /Y "LICENSE" "%RELEASE_DIR%\%PACKAGE_NAME%\LICENSE.txt"

REM Copy changelog
if exist "CHANGELOG.md" copy /Y "CHANGELOG.md" "%RELEASE_DIR%\%PACKAGE_NAME%\CHANGELOG.txt"

echo OK: Files copied
echo.

echo [2/4] Verifying package...
python tools\scripts\verify_package.py "%RELEASE_DIR%\%PACKAGE_NAME%" > nul 2>&1
if errorlevel 1 (
    echo WARNING: Package verification failed
    echo Please check the package manually
) else (
    echo OK: Package verified
)
echo.

echo [3/4] Creating ZIP archive...
REM Remove old zip if exists
if exist "%RELEASE_DIR%\%PACKAGE_NAME%.zip" del /f "%RELEASE_DIR%\%PACKAGE_NAME%.zip"

REM Create zip using PowerShell
powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\%PACKAGE_NAME%' -DestinationPath '%RELEASE_DIR%\%PACKAGE_NAME%.zip' -CompressionLevel Optimal"

if errorlevel 1 (
    echo ERROR: Failed to create ZIP archive
    pause
    exit /b 1
)

REM Get zip file size
for %%A in ("%RELEASE_DIR%\%PACKAGE_NAME%.zip") do set ZIP_SIZE=%%~zA
set /a ZIP_SIZE_MB=%ZIP_SIZE% / 1048576

echo OK: ZIP created (%ZIP_SIZE_MB% MB)
echo.

echo [4/4] Generating checksums...
REM Generate SHA256 checksum using certutil (built-in Windows tool)
certutil -hashfile "%RELEASE_DIR%\%PACKAGE_NAME%.zip" SHA256 > "%RELEASE_DIR%\%PACKAGE_NAME%.zip.sha256.tmp"
if errorlevel 1 (
    echo WARNING: Could not generate checksum
) else (
    REM Extract just the hash value (second line)
    for /f "skip=1 tokens=1" %%h in (%RELEASE_DIR%\%PACKAGE_NAME%.zip.sha256.tmp) do (
        echo %%h > "%RELEASE_DIR%\%PACKAGE_NAME%.zip.sha256"
        goto :hash_done
    )
    :hash_done
    del "%RELEASE_DIR%\%PACKAGE_NAME%.zip.sha256.tmp"
    echo OK: Checksum generated
)
echo.

echo ========================================
echo Release package created successfully!
echo ========================================
echo.
echo Package: %RELEASE_DIR%\%PACKAGE_NAME%.zip
echo Size: %ZIP_SIZE_MB% MB
echo Checksum: %RELEASE_DIR%\%PACKAGE_NAME%.zip.sha256
echo.
echo You can now:
echo 1. Test the package on a clean machine
echo 2. Upload to GitHub Releases
echo 3. Distribute to users
echo.

REM Show checksum
echo SHA256 Checksum:
type "%RELEASE_DIR%\%PACKAGE_NAME%.zip.sha256"
echo.

pause
