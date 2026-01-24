@echo off
REM Circuit Repair Game - Build Script (Windows)
REM 电路修复游戏 - 构建脚本 (Windows)

echo ========================================
echo Circuit Repair Game - Build Script
echo 电路修复游戏 - 构建脚本
echo ========================================
echo.

REM Activate conda environment
echo [1/5] Activating conda environment...
call conda activate Game
if errorlevel 1 (
    echo ERROR: Failed to activate conda environment 'Game'
    echo Please ensure conda is installed and the 'Game' environment exists
    pause
    exit /b 1
)
echo OK: Conda environment activated
echo.

REM Check if PyInstaller is installed
echo [2/5] Checking PyInstaller installation...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo OK: PyInstaller is installed
echo.

REM Clean previous build
echo [3/5] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo OK: Previous build cleaned
echo.

REM Build the executable
echo [4/5] Building executable...
echo This may take several minutes...
pyinstaller circuit_repair_game.spec
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo OK: Build completed successfully
echo.

REM Verify the build
echo [5/5] Verifying build...
if exist "dist\CircuitRepairGame\CircuitRepairGame.exe" (
    echo OK: Executable created successfully
    echo.
    echo ========================================
    echo Build completed!
    echo ========================================
    echo.
    echo Output location: dist\CircuitRepairGame\
    echo Executable: dist\CircuitRepairGame\CircuitRepairGame.exe
    echo.
    echo You can now:
    echo 1. Test the executable: cd dist\CircuitRepairGame ^&^& CircuitRepairGame.exe
    echo 2. Create a zip file for distribution
    echo.
) else (
    echo ERROR: Executable not found
    echo Build may have failed
    pause
    exit /b 1
)

pause
