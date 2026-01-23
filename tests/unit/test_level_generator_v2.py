"""
Test script for LevelGeneratorV2

Tests the improved level generator with different difficulty levels.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.level.level_generator_v2 import LevelGeneratorV2
from src.core.level.difficulty_config import DifficultyLevel
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


def visualize_path(level_data: dict) -> None:
    """
    Visualize the generated level path in ASCII.

    Args:
        level_data: Level data dictionary
    """
    grid_size = level_data['grid_size']
    path = level_data['path']
    solution = level_data['solution']

    # Create grid
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    # Mark path
    for x, y in path:
        grid[x][y] = '#'

    # Mark power source and terminal
    for tile in solution:
        if tile['type'] == 'power_source':
            grid[tile['x']][tile['y']] = 'P'
        elif tile['type'] == 'terminal':
            grid[tile['x']][tile['y']] = 'T'

    # Print grid
    print("\nPath visualization:")
    print("  " + " ".join(str(i) for i in range(grid_size)))
    for i, row in enumerate(grid):
        print(f"{i} " + " ".join(row))
    print("\nLegend: P=Power Source, T=Terminal, #=Path, .=Empty")


def print_tile_details(level_data: dict) -> None:
    """
    Print detailed tile information.

    Args:
        level_data: Level data dictionary
    """
    solution = level_data['solution']
    initial_state = level_data['initial_state']

    print("\nTile details:")
    print(f"{'Pos':<8} {'Type':<15} {'Correct':<10} {'Initial':<10} {'Clickable':<10}")
    print("-" * 65)

    initial_dict = {(t['x'], t['y']): t['rotation'] for t in initial_state}

    for tile in solution:
        if tile['type'] != 'empty':
            pos = f"({tile['x']},{tile['y']})"
            tile_type = tile['type']
            correct_rot = f"{tile['rotation']}°"
            initial_rot = f"{initial_dict.get((tile['x'], tile['y']), 'N/A')}°"
            clickable = "Yes" if tile['is_clickable'] else "No"

            print(f"{pos:<8} {tile_type:<15} {correct_rot:<10} {initial_rot:<10} {clickable:<10}")


def test_difficulty(difficulty: DifficultyLevel) -> None:
    """
    Test level generation for a specific difficulty.

    Args:
        difficulty: Difficulty level to test
    """
    print(f"\n{'='*70}")
    print(f"Testing Difficulty: {difficulty.value.upper()}")
    print(f"{'='*70}")

    try:
        generator = LevelGeneratorV2(difficulty=difficulty)
        level_data = generator.generate()

        print(f"\n[OK] Level generated successfully!")
        print(f"  Grid size: {level_data['grid_size']}x{level_data['grid_size']}")
        print(f"  Path length: {len(level_data['path'])}")
        print(f"  Movable tiles: {level_data['movable_count']}")
        print(f"  Corner tiles: {level_data['corner_count']}")
        print(f"  Difficulty: {level_data['difficulty']}")

        visualize_path(level_data)
        print_tile_details(level_data)

        # Validate scramble ratio
        solution = level_data['solution']
        initial_state = level_data['initial_state']
        initial_dict = {(t['x'], t['y']): t['rotation'] for t in initial_state}

        scrambled_count = 0
        clickable_count = 0

        for tile in solution:
            if tile['is_clickable']:
                clickable_count += 1
                correct_rot = tile['rotation']
                initial_rot = initial_dict.get((tile['x'], tile['y']))

                # Check if rotation is incorrect
                accepted = tile.get('accepted_rotations', [correct_rot])
                if initial_rot not in accepted:
                    scrambled_count += 1

        actual_ratio = scrambled_count / clickable_count if clickable_count > 0 else 0
        print(f"\nScramble validation:")
        print(f"  Scrambled tiles: {scrambled_count}/{clickable_count}")
        print(f"  Actual ratio: {actual_ratio:.1%}")
        print(f"  Expected ratio: {generator.config.scramble_ratio:.1%}")

    except Exception as e:
        print(f"\n[FAIL] Failed to generate level: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function."""
    print("="*70)
    print("LevelGeneratorV2 Test Suite")
    print("="*70)

    # Test all difficulty levels
    for difficulty in DifficultyLevel:
        test_difficulty(difficulty)

    print(f"\n{'='*70}")
    print("All tests completed!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
