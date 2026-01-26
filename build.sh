#!/bin/bash
# Circuit Repair Game - Build Script (Linux/Mac)
# 电路修复游戏 - 构建脚本 (Linux/Mac)

set -e  # Exit on error

echo "========================================"
echo "Circuit Repair Game - Build Script"
echo "电路修复游戏 - 构建脚本"
echo "========================================"
echo ""

# Check if Python is available
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
echo "OK: Python 3 is installed"
echo ""

# Check if PyInstaller is installed
echo "[2/5] Checking PyInstaller installation..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller not found. Installing..."
    pip3 install pyinstaller
fi
echo "OK: PyInstaller is installed"
echo ""

# Clean previous build
echo "[3/5] Cleaning previous build..."
rm -rf build dist
echo "OK: Previous build cleaned"
echo ""

# Build the executable
echo "[4/5] Building executable..."
echo "This may take several minutes..."
pyinstaller circuit_repair_game.spec
echo "OK: Build completed successfully"
echo ""

# Verify the build
echo "[5/5] Verifying build..."
if [ -f "dist/CircuitRepairGame/CircuitRepairGame" ]; then
    echo "OK: Executable created successfully"
    echo ""
    echo "========================================"
    echo "Build completed!"
    echo "========================================"
    echo ""
    echo "Output location: dist/CircuitRepairGame/"
    echo "Executable: dist/CircuitRepairGame/CircuitRepairGame"
    echo ""
    echo "You can now:"
    echo "1. Test the executable: cd dist/CircuitRepairGame && ./CircuitRepairGame"
    echo "2. Create a tar.gz file for distribution"
    echo ""
else
    echo "ERROR: Executable not found"
    echo "Build may have failed"
    exit 1
fi
