"""
Quick Test for Level Generator V3

Simple test to verify the V3 generator works correctly.

Usage:
    python tests/quick_test_v3.py

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.level.level_generator_v3 import LevelGeneratorV3
from src.core.level.difficulty_config import DifficultyLevel


def quick_test():
    """Quick test of V3 generator."""
    print("\n" + "="*60)
    print("关卡生成器 V3 快速测试")
    print("Level Generator V3 Quick Test")
    print("="*60)

    difficulties = ['easy', 'normal', 'hard', 'hell']

    for difficulty in difficulties:
        print(f"\n测试难度: {difficulty.upper()}")
        print("-" * 60)

        try:
            difficulty_enum = DifficultyLevel(difficulty.lower())
            generator = LevelGeneratorV3(difficulty=difficulty_enum)
            result = generator.generate()

            print(f"✅ 生成成功")
            print(f"   网格大小: {result['grid_size']}x{result['grid_size']}")
            print(f"   路径长度: {len(result['path'])}")
            print(f"   可移动瓷砖: {result['movable_count']}")
            print(f"   拐角数量: {result['corner_count']}")

            # Quick visualization
            path_str = " → ".join([f"({x},{y})" for x, y in result['path'][:5]])
            if len(result['path']) > 5:
                path_str += " → ..."
            print(f"   路径示例: {path_str}")

        except Exception as e:
            print(f"❌ 生成失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    print("\n" + "="*60)
    print("✅ 所有难度测试通过！")
    print("V3 生成器工作正常。")
    print("="*60 + "\n")

    return True


if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
