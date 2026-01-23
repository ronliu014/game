"""
电路修复游戏 - 快速启动脚本
Circuit Repair Game - Quick Start Script

这是一个简化的启动脚本，用于快速启动游戏。
This is a simplified start script for quick game launch.

使用方法 (Usage):
    python start_game.py              # 默认难度（普通）
    python start_game.py --difficulty easy    # 简单难度
    python start_game.py --difficulty hard    # 困难难度
    python start_game.py --difficulty hell    # 地狱难度

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())
