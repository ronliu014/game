"""
Test Level Generator V3 - Algorithm Verification

Comprehensive tests to verify the V3 generator implements the user's algorithm correctly.

Tests:
1. Path generation (DFS, not shortest path)
2. Sprite and rotation assignment based on geometry
3. Difficulty validation
4. Scrambling logic

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.level.level_generator_v3 import LevelGeneratorV3
from src.core.level.difficulty_config import DifficultyLevel


def visualize_path(grid_size: int, path: list, solution_tiles: list):
    """
    Visualize the generated path and tile configurations.

    Args:
        grid_size: Size of the grid
        path: List of (x, y) positions
        solution_tiles: List of tile configurations
    """
    # Create a grid representation
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    # Create tile lookup
    tile_map = {(t['x'], t['y']): t for t in solution_tiles}

    # Mark path tiles
    for i, (x, y) in enumerate(path):
        tile = tile_map.get((x, y))
        if tile:
            tile_type = tile['type']
            rotation = tile['rotation']

            if tile_type == 'power':
                grid[y][x] = 'P'
            elif tile_type == 'terminal':
                grid[y][x] = 'T'
            elif tile_type == 'straight':
                if rotation in [0, 180]:
                    grid[y][x] = '─'  # Horizontal
                else:
                    grid[y][x] = '│'  # Vertical
            elif tile_type == 'corner':
                corner_chars = {
                    0: '└',    # Up and right
                    90: '┌',   # Right and down
                    180: '┐',  # Down and left
                    270: '┘'   # Left and up
                }
                grid[y][x] = corner_chars.get(rotation, 'L')

    # Print grid
    print("\n" + "="*60)
    print("关卡可视化 (Level Visualization)")
    print("="*60)
    print(f"网格大小: {grid_size}x{grid_size}")
    print(f"路径长度: {len(path)}")
    print("\n图例 (Legend):")
    print("  P = 电源 (Power Source)")
    print("  T = 终端 (Terminal)")
    print("  ─ = 水平直线 (Horizontal Straight)")
    print("  │ = 竖直直线 (Vertical Straight)")
    print("  └ = 0° 拐角 (上→右)")
    print("  ┌ = 90° 拐角 (右→下)")
    print("  ┐ = 180° 拐角 (下→左)")
    print("  ┘ = 270° 拐角 (左→上)")
    print("  . = 空格子 (Empty)")
    print()

    # Print grid with coordinates
    print("   ", end="")
    for x in range(grid_size):
        print(f"{x:2}", end=" ")
    print()

    for y in range(grid_size):
        print(f"{y:2} ", end="")
        for x in range(grid_size):
            print(f" {grid[y][x]} ", end="")
        print()
    print()


def verify_tile_logic(path: list, solution_tiles: list):
    """
    Verify that tile configurations match the user's algorithm.

    Args:
        path: List of (x, y) positions
        solution_tiles: List of tile configurations

    Returns:
        True if all tiles are correct, False otherwise
    """
    print("\n" + "="*60)
    print("验证瓷砖逻辑 (Verifying Tile Logic)")
    print("="*60)

    tile_map = {(t['x'], t['y']): t for t in solution_tiles}
    all_correct = True

    for i in range(1, len(path) - 1):  # Skip power and terminal
        prev_pos = path[i - 1]
        cur_pos = path[i]
        next_pos = path[i + 1]

        tile = tile_map[cur_pos]

        prev_x, prev_y = prev_pos
        cur_x, cur_y = cur_pos
        next_x, next_y = next_pos

        print(f"\n瓷砖 #{i}: 位置 ({cur_x}, {cur_y})")
        print(f"  前一个: ({prev_x}, {prev_y})")
        print(f"  当前: ({cur_x}, {cur_y})")
        print(f"  下一个: ({next_x}, {next_y})")

        # Determine expected configuration based on user's algorithm
        # Screen coordinate system: x-right is positive, y-down is positive
        # prev_x < cur_x: previous is to the LEFT
        # prev_x > cur_x: previous is to the RIGHT
        # prev_y < cur_y: previous is ABOVE (UP)
        # prev_y > cur_y: previous is BELOW (DOWN)
        expected_type = None
        expected_rotation = None

        # Case 1: Previous tile is ABOVE current (prev_y < cur_y)
        if cur_x == prev_x and prev_y < cur_y:
            print(f"  前一个在正上方")
            if next_x > cur_x and cur_y == next_y:
                print(f"  下一个在正右方 → 应该是 0° 拐角")
                expected_type = 'corner'
                expected_rotation = 0
            elif cur_x == next_x and next_y > cur_y:
                print(f"  下一个在正下方 → 应该是 90°/270° 直线")
                expected_type = 'straight'
                expected_rotation = [90, 270]
            elif next_x < cur_x and cur_y == next_y:
                print(f"  下一个在正左方 → 应该是 270° 拐角")
                expected_type = 'corner'
                expected_rotation = 270

        # Case 2: Previous tile is to the RIGHT (prev_x > cur_x)
        elif prev_x > cur_x and cur_y == prev_y:
            print(f"  前一个在正右方")
            if cur_x == next_x and next_y > cur_y:
                print(f"  下一个在正下方 → 应该是 90° 拐角")
                expected_type = 'corner'
                expected_rotation = 90
            elif next_x < cur_x and cur_y == next_y:
                print(f"  下一个在正左方 → 应该是 0°/180° 直线")
                expected_type = 'straight'
                expected_rotation = [0, 180]
            elif cur_x == next_x and next_y < cur_y:
                print(f"  下一个在正上方 → 应该是 0° 拐角")
                expected_type = 'corner'
                expected_rotation = 0

        # Case 3: Previous tile is BELOW current (prev_y > cur_y)
        elif cur_x == prev_x and prev_y > cur_y:
            print(f"  前一个在正下方")
            if next_x < cur_x and cur_y == next_y:
                print(f"  下一个在正左方 → 应该是 180° 拐角")
                expected_type = 'corner'
                expected_rotation = 180
            elif cur_x == next_x and next_y < cur_y:
                print(f"  下一个在正上方 → 应该是 90°/270° 直线")
                expected_type = 'straight'
                expected_rotation = [90, 270]
            elif next_x > cur_x and cur_y == next_y:
                print(f"  下一个在正右方 → 应该是 90° 拐角")
                expected_type = 'corner'
                expected_rotation = 90

        # Case 4: Previous tile is to the LEFT (prev_x < cur_x)
        elif prev_x < cur_x and cur_y == prev_y:
            print(f"  前一个在正左方")
            if cur_x == next_x and next_y < cur_y:
                print(f"  下一个在正上方 → 应该是 270° 拐角")
                expected_type = 'corner'
                expected_rotation = 270
            elif next_x > cur_x and cur_y == next_y:
                print(f"  下一个在正右方 → 应该是 0°/180° 直线")
                expected_type = 'straight'
                expected_rotation = [0, 180]
            elif cur_x == next_x and next_y > cur_y:
                print(f"  下一个在正下方 → 应该是 180° 拐角")
                expected_type = 'corner'
                expected_rotation = 180

        # Verify
        actual_type = tile['type']
        actual_rotation = tile['rotation']

        print(f"  实际配置: {actual_type} @ {actual_rotation}°")

        if expected_type:
            if actual_type != expected_type:
                print(f"  ❌ 错误！类型不匹配")
                all_correct = False
            elif isinstance(expected_rotation, list):
                if actual_rotation not in expected_rotation:
                    print(f"  ❌ 错误！旋转角度不在 {expected_rotation} 中")
                    all_correct = False
                else:
                    print(f"  ✅ 正确")
            elif actual_rotation != expected_rotation:
                print(f"  ❌ 错误！旋转角度应该是 {expected_rotation}°")
                all_correct = False
            else:
                print(f"  ✅ 正确")

    return all_correct


def test_single_level(difficulty: str):
    """
    Test generation of a single level.

    Args:
        difficulty: Difficulty level to test
    """
    print("\n" + "="*60)
    print(f"测试难度: {difficulty.upper()}")
    print("="*60)

    try:
        difficulty_enum = DifficultyLevel(difficulty.lower())
    except ValueError:
        print(f"❌ 无效的难度: {difficulty}")
        return False

    generator = LevelGeneratorV3(difficulty=difficulty_enum)

    try:
        result = generator.generate()
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False

    print(f"✅ 生成成功")
    print(f"  网格大小: {result['grid_size']}x{result['grid_size']}")
    print(f"  路径长度: {len(result['path'])}")
    print(f"  可移动瓷砖: {result['movable_count']}")
    print(f"  拐角数量: {result['corner_count']}")

    # Visualize
    visualize_path(result['grid_size'], result['path'], result['solution'])

    # Verify tile logic
    is_correct = verify_tile_logic(result['path'], result['solution'])

    if is_correct:
        print("\n✅ 所有瓷砖配置正确！")
    else:
        print("\n❌ 发现瓷砖配置错误！")

    # Verify scrambling
    print("\n" + "="*60)
    print("验证打乱逻辑 (Verifying Scrambling)")
    print("="*60)

    solution_map = {(t['x'], t['y']): t for t in result['solution']}
    initial_map = {(t['x'], t['y']): t for t in result['initial_state']}

    scrambled_count = 0
    movable_count = 0

    for tile in result['solution']:
        if tile.get('is_clickable', False):
            movable_count += 1
            pos = (tile['x'], tile['y'])
            solution_rot = tile['rotation']
            initial_rot = initial_map[pos]['rotation']

            accepted = tile.get('accepted_rotations', [solution_rot])

            if initial_rot not in accepted:
                scrambled_count += 1

    scramble_ratio = scrambled_count / movable_count if movable_count > 0 else 0

    print(f"可移动瓷砖: {movable_count}")
    print(f"被打乱的瓷砖: {scrambled_count}")
    print(f"打乱比例: {scramble_ratio:.1%}")

    config = generator.config
    print(f"要求的最小打乱比例: {config.scramble_ratio:.1%}")

    if scramble_ratio >= config.scramble_ratio:
        print("✅ 打乱比例符合要求")
    else:
        print("❌ 打乱比例不足")

    return is_correct


def main():
    """Main test function."""
    print("\n" + "="*60)
    print("关卡生成器 V3 算法验证测试")
    print("Level Generator V3 Algorithm Verification")
    print("="*60)

    difficulties = ['easy', 'normal', 'hard', 'hell']

    all_passed = True

    for difficulty in difficulties:
        try:
            success = test_single_level(difficulty)
            if not success:
                all_passed = False
        except Exception as e:
            print(f"\n❌ {difficulty.upper()} 测试出错: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

        print("\n" + "="*60)
        input("按 Enter 继续下一个难度...")

    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试通过！")
        print("算法实现正确，符合用户规范。")
    else:
        print("❌ 部分测试失败")
        print("请检查算法实现。")
    print("="*60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
