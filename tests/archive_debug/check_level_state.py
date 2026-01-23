"""
Check what tiles are actually loaded and rendered
"""
from src.core.level.level_loader import LevelLoader

def check_loaded_level():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("COMPLETE GRID STATE")
    print("=" * 60)
    print()

    print("Grid layout (visual representation):")
    print("   Col0      Col1      Col2      Col3")

    for row in range(grid.grid_size):
        row_str = f"R{row} "
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile:
                tile_type = tile.tile_type.value[:6]  # First 6 chars
                row_str += f"{tile_type:8s} "
            else:
                row_str += "None     "
        print(row_str)

    print()
    print("=" * 60)
    print("DETAILED TILE INFORMATION")
    print("=" * 60)
    print()

    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile and tile.tile_type.value != "empty":
                exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
                print(f"({row},{col}): {tile.tile_type.value:15s} rot={tile.rotation:3d}deg exits={exits} clickable={tile.is_clickable}")

    print()
    print("=" * 60)
    print("EXPECTED VISUAL PATH")
    print("=" * 60)
    print()
    print("From screenshot, the tiles that SHOULD be in the path:")
    print("  Power (0,0) -> needs to connect to something on its RIGHT (0,1)")
    print("  But (0,1) appears EMPTY in the screenshot!")
    print()
    print("Let me check what's at (0,1):")
    tile_01 = grid.get_tile(0, 1)
    if tile_01:
        print(f"  (0,1) has: {tile_01.tile_type.value}, rotation={tile_01.rotation}deg")
        print(f"  Clickable: {tile_01.is_clickable}")
        print(f"  Exits: {[str(d).split('.')[-1] for d in tile_01.get_exit_directions()]}")
    else:
        print(f"  (0,1) is None!")

    print()
    print("The tiles visible in screenshot are at:")
    print("  (1,0) - horizontal straight")
    print("  (2,0) - corner")
    print("  (2,1) - vertical straight")
    print("  (2,2) - vertical straight")
    print("  (2,3) - corner")
    print()
    print("These positions don't connect to power source at (0,0)!")

if __name__ == "__main__":
    check_loaded_level()
