"""
Debug level generator to see what's being generated
"""
from src.core.level.level_generator import LevelGenerator
import json

def test_debug_generator():
    """Generate a level and print detailed debug info."""

    print("=" * 60)
    print("DEBUG: Level Generator")
    print("=" * 60)
    print()

    # Generate level
    generator = LevelGenerator(grid_size=4, min_path_length=5)
    result = generator.generate()

    print(f"Grid size: {result['grid_size']}")
    print(f"Path length: {len(result['path'])}")
    print()

    print("Path positions:")
    for i, pos in enumerate(result['path']):
        print(f"  [{i}] {pos}")
    print()

    print("Solution tiles:")
    for tile in result['solution']:
        if tile['type'] != 'empty':
            accepted = tile.get('accepted_rotations', [tile['rotation']])
            print(f"  ({tile['x']}, {tile['y']}): {tile['type']:12s} "
                  f"rotation={tile['rotation']:3d}° "
                  f"clickable={tile['is_clickable']} "
                  f"accepted={accepted}")
    print()

    # Save to JSON for inspection
    with open('debug_level.json', 'w', encoding='utf-8') as f:
        json.dump({
            'solution': {'tiles': result['solution']},
            'initial_state': {'rotated_tiles': result['initial_state']},
            'path': result['path']
        }, f, indent=2, ensure_ascii=False)

    print("Saved to debug_level.json")

if __name__ == "__main__":
    test_debug_generator()
