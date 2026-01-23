"""
Test to check the actual tile rotations in level_001
"""
from src.core.level.level_loader import LevelLoader

def test_current_state():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("INITIAL STATE (after loading with scrambled rotations)")
    print("=" * 60)
    print()

    # Print all tiles with their rotations
    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile and tile.tile_type.value != "empty":
                exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
                clickable = "Y" if tile.is_clickable else "N"
                print(f"({row},{col}): {tile.tile_type.value:15s} rot={tile.rotation:3d}° exits={exits} clickable={clickable}")

    print()
    print("=" * 60)
    print("EXPECTED SOLUTION STATE")
    print("=" * 60)
    print("(1,0): straight         rot=  0° (horizontal)")
    print("(2,0): corner           rot= 90° (exits SOUTH+WEST)")
    print("(2,1): straight         rot= 90° (vertical)")
    print("(2,2): straight         rot= 90° (vertical)")
    print("(2,3): corner           rot=270° (exits NORTH+EAST)")
    print()

if __name__ == "__main__":
    test_current_state()
