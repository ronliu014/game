"""
Debug Scrambling Logic

Quick test to verify scrambling ratio is correct.
"""
# -*- coding: utf-8 -*-

import sys
import io
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.level.level_generator_v3 import LevelGeneratorV3
from src.core.level.difficulty_config import DifficultyLevel


def test_scrambling():
    """Test scrambling logic."""
    # Set UTF-8 output for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("\n" + "="*60)
    print("测试打乱逻辑 (Testing Scrambling Logic)")
    print("="*60)

    for difficulty in [DifficultyLevel.EASY, DifficultyLevel.NORMAL, DifficultyLevel.HARD, DifficultyLevel.HELL]:
        print(f"\n难度: {difficulty.value.upper()}")
        print("-" * 60)

        generator = LevelGeneratorV3(difficulty=difficulty)
        result = generator.generate()

        # Count scrambled tiles
        solution_map = {(t['x'], t['y']): t for t in result['solution']}
        initial_map = {(t['x'], t['y']): t for t in result['initial_state']}

        scrambled_count = 0
        movable_count = result['movable_count']

        for tile in result['solution']:
            if tile.get('is_clickable', False):
                pos = (tile['x'], tile['y'])
                solution_rot = tile['rotation']
                initial_rot = initial_map[pos]['rotation']
                accepted = tile.get('accepted_rotations', [solution_rot])

                if initial_rot not in accepted:
                    scrambled_count += 1

        scramble_ratio = scrambled_count / movable_count if movable_count > 0 else 0
        required_ratio = generator.config.scramble_ratio

        print(f"可移动瓷砖: {movable_count}")
        print(f"被打乱的瓷砖: {scrambled_count}")
        print(f"实际打乱比例: {scramble_ratio:.1%}")
        print(f"要求的最小比例: {required_ratio:.1%}")

        if scramble_ratio >= required_ratio:
            print("✅ 打乱比例符合要求")
        else:
            print(f"❌ 打乱比例不足 ({scramble_ratio:.1%} < {required_ratio:.1%})")

            # Debug: show which tiles were scrambled
            print("\n详细信息:")
            for i, tile in enumerate(result['solution']):
                if tile.get('is_clickable', False):
                    pos = (tile['x'], tile['y'])
                    solution_rot = tile['rotation']
                    initial_rot = initial_map[pos]['rotation']
                    accepted = tile.get('accepted_rotations', [solution_rot])
                    is_scrambled = initial_rot not in accepted

                    print(f"  瓷砖 {i}: 位置{pos}, 正确={solution_rot}°, 初始={initial_rot}°, "
                          f"接受={accepted}, 打乱={'是' if is_scrambled else '否'}")


if __name__ == "__main__":
    test_scrambling()
