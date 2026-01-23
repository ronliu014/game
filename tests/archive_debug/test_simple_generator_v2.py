"""
Simple test for LevelGeneratorV2
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.level.level_generator_v2 import LevelGeneratorV2
from src.core.level.difficulty_config import DifficultyLevel

print("Testing LevelGeneratorV2...")

try:
    generator = LevelGeneratorV2(difficulty=DifficultyLevel.EASY)
    print(f"Generator created: grid_size={generator.grid_size}")

    level_data = generator.generate()
    print(f"Level generated successfully!")
    print(f"  Grid size: {level_data['grid_size']}")
    print(f"  Path length: {len(level_data['path'])}")
    print(f"  Movable tiles: {level_data['movable_count']}")
    print(f"  Corner tiles: {level_data['corner_count']}")

    # Print path
    print(f"\nPath: {level_data['path']}")

    # Check for duplicates
    path = level_data['path']
    if len(path) != len(set(path)):
        print("WARNING: Path has duplicates!")
        duplicates = [pos for pos in path if path.count(pos) > 1]
        print(f"Duplicates: {set(duplicates)}")
    else:
        print("Path validation: OK (no duplicates)")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
