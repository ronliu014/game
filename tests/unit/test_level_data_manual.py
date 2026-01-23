"""
Test if generated level data has correct accepted_rotations
"""
from src.integration.game_api import GameAPI
from src.core.level.level_generator import LevelGenerator

def test_generated_level_data():
    """Test that generated level has correct accepted_rotations."""

    print("=" * 60)
    print("TEST: Generated Level Data")
    print("=" * 60)
    print()

    # Generate a level
    generator = LevelGenerator(grid_size=4, min_path_length=5)
    result = generator.generate()

    print("Generated solution tiles:")
    for tile in result['solution']:
        if tile['type'] not in ['empty']:
            accepted = tile.get('accepted_rotations', 'MISSING!')
            print(f"  ({tile['x']}, {tile['y']}): {tile['type']:12s} "
                  f"rotation={tile['rotation']:3d}° "
                  f"clickable={tile['is_clickable']} "
                  f"accepted={accepted}")
    print()

    # Now test loading it through the game system
    print("Testing through GameAPI...")
    game_api = GameAPI()

    # Access the level manager
    from src.core.level.level_loader import LevelLoader
    from src.core.level.level_manager import LevelManager

    loader = LevelLoader()
    manager = LevelManager(loader)

    # Load generated level
    success = manager.load_generated_level(grid_size=4, min_path_length=5)

    if success:
        print("Level loaded successfully!")
        level_data = manager.get_level_data()

        if level_data:
            print("\nLevel data solution_tiles:")
            for tile_data in level_data.solution_tiles:
                if tile_data.get('type') not in ['empty']:
                    accepted = tile_data.get('accepted_rotations', 'MISSING!')
                    print(f"  ({tile_data.get('x')}, {tile_data.get('y')}): "
                          f"{tile_data.get('type'):12s} "
                          f"rotation={tile_data.get('rotation'):3d}° "
                          f"clickable={tile_data.get('is_clickable')} "
                          f"accepted={accepted}")
        else:
            print("ERROR: level_data is None!")
    else:
        print("ERROR: Failed to load generated level!")

if __name__ == "__main__":
    test_generated_level_data()
