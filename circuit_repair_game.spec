# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Circuit Repair Game
电路修复游戏打包配置文件

This spec file configures PyInstaller to create a standalone executable
for the Circuit Repair Game.

Usage:
    pyinstaller circuit_repair_game.spec

Output:
    dist/CircuitRepairGame.exe (Windows)
    dist/CircuitRepairGame (Linux/Mac)
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Project root directory
project_root = os.path.abspath(SPECPATH)

# Collect all pygame data files
pygame_datas = collect_data_files('pygame')

# Collect all submodules from src
hidden_imports = collect_submodules('src')

# Additional hidden imports
hidden_imports += [
    'pygame',
    'pygame.mixer',
    'pygame.font',
    'pygame.image',
    'pygame.transform',
    'pygame.draw',
    'pygame.display',
    'pygame.event',
    'pygame.time',
    'pygame.mouse',
    'pygame.key',
    'pygame.surface',
    'pygame.rect',
    'pygame.color',
]

# Data files to include
datas = [
    # Assets directory
    (os.path.join(project_root, 'assets'), 'assets'),
    # Data directory (configs, levels, saves)
    (os.path.join(project_root, 'data'), 'data'),
    # Include pygame data files
    *pygame_datas,
]

# Binary files to exclude (reduce size)
binaries = []

# Analysis configuration
a = Analysis(
    # Entry point script
    [os.path.join(project_root, 'start_game.py')],
    
    # Path to search for imports
    pathex=[project_root],
    
    # Binary files
    binaries=binaries,
    
    # Data files
    datas=datas,
    
    # Hidden imports
    hiddenimports=hidden_imports,
    
    # Hook directories
    hookspath=[],
    
    # Runtime hooks
    hooksconfig={},
    runtime_hooks=[],
    
    # Exclusions (reduce size)
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    
    # Windows-specific
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    
    # Code signing
    cipher=None,
    
    # No UPX compression (faster startup)
    noarchive=False,
)

# PYZ (Python zip archive)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

# EXE configuration
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,

    # Application name
    name='CircuitRepairGame',

    # Debug options
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI app)

    # Windows-specific options
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,

    # Version information (Windows only)
    version='version_info.txt',

    # Icon file
    icon=os.path.join(project_root, 'assets', 'icon.ico') if os.path.exists(os.path.join(project_root, 'assets', 'icon.ico')) else None,
)

# COLLECT (bundle all files)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CircuitRepairGame',
)

# Optional: Create a single-file executable (uncomment if needed)
# Note: Single-file mode is slower to start but easier to distribute
"""
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CircuitRepairGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'assets', 'icon.ico') if os.path.exists(os.path.join(project_root, 'assets', 'icon.ico')) else None,
)
"""
