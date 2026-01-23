"""
Test Infinite Mode Level Generation

Tests the new infinite level generation system with different difficulty levels.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.level.level_manager import LevelManager
from src.core.level.level_loader import LevelLoader
from src.core.level.difficulty_config import DifficultyLevel


def test_generate_level(difficulty: str, count: int = 3):
    """
    Test level generation for a specific difficulty.

    Args:
        difficulty: Difficulty level to test
        count: Number of levels to generate
    """
    print(f"\n{'='*60}")
    print(f"测试难度 (Testing Difficulty): {difficulty.upper()}")
    print(f"{'='*60}")

    loader = LevelLoader()
    manager = LevelManager(loader)

    for i in range(1, count + 1):
        print(f"\n生成关卡 #{i} (Generating Level #{i})...")

        success = manager.load_generated_level(
            difficulty=difficulty,
            level_number=i
        )

        if success:
            level_data = manager.get_level_data()
            grid = manager.get_grid()

            print(f"  ✅ 生成成功 (Success)")
            print(f"  📊 关卡信息 (Level Info):")
            print(f"     - 名称 (Name): {level_data.name}")
            print(f"     - 网格大小 (Grid Size): {level_data.grid_size}x{level_data.grid_size}")
            print(f"     - 难度 (Difficulty): {level_data.difficulty}")

            # Count movable tiles
            movable_count = sum(1 for tile_data in level_data.solution_tiles
                              if tile_data.get('is_clickable', False))
            print(f"     - 可移动瓷砖 (Movable Tiles): {movable_count}")

            # Count corner tiles
            corner_count = sum(1 for tile_data in level_data.solution_tiles
                             if tile_data.get('type') == 'corner')
            print(f"     - 拐角瓷砖 (Corner Tiles): {corner_count}")

        else:
            print(f"  ❌ 生成失败 (Failed)")
            return False

    return True


def main():
    """Main test function."""
    print("\n" + "="*60)
    print("  无限模式测试 (Infinite Mode Test)")
    print("="*60)
    print("\n测试程序化关卡生成系统...")
    print("Testing procedural level generation system...\n")

    difficulties = ['easy', 'normal', 'hard', 'hell']

    all_passed = True

    for difficulty in difficulties:
        try:
            success = test_generate_level(difficulty, count=3)
            if not success:
                all_passed = False
                print(f"\n❌ {difficulty.upper()} 难度测试失败")
        except Exception as e:
            print(f"\n❌ {difficulty.upper()} 难度测试出错: {e}")
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试通过！(All tests passed!)")
        print("无限模式系统运行正常。")
        print("Infinite mode system is working correctly.")
    else:
        print("❌ 部分测试失败 (Some tests failed)")
        print("请检查日志获取详细信息。")
        print("Please check logs for details.")
    print("="*60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
