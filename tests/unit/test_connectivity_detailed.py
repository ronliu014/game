"""
Detailed connectivity test for level_001
"""
from src.core.level.level_loader import LevelLoader
from src.core.circuit.connectivity_checker import ConnectivityChecker
from src.config.constants import Direction

def test_detailed_connectivity():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("GRID STATE AFTER LOADING (with initial scrambled rotations)")
    print("=" * 60)
    print()

    # Print all tiles
    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile:
                exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
                clickable = "Y" if tile.is_clickable else "N"
                print(f"({row},{col}): {tile.tile_type.value:12s} rot={tile.rotation:3d}° exits={exits} clickable={clickable}")

    print()
    print("=" * 60)
    print("MANUALLY SETTING TO SOLUTION STATE")
    print("=" * 60)

    # Manually set tiles to solution rotations
    solution_rotations = {
        (0, 1): 0,   # straight horizontal
        (0, 2): 90,  # corner turning down
        (1, 2): 90,  # straight vertical
        (2, 2): 90,  # straight vertical
        (3, 2): 270, # corner turning right
    }

    for (x, y), rotation in solution_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)
            print(f"Set ({x},{y}) to rotation {rotation}°")

    print()
    print("=" * 60)
    print("GRID STATE AFTER SETTING SOLUTION")
    print("=" * 60)
    print()

    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile:
                exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
                clickable = "Y" if tile.is_clickable else "N"
                print(f"({row},{col}): {tile.tile_type.value:12s} rot={tile.rotation:3d}° exits={exits} clickable={clickable}")

    print()
    print("=" * 60)
    print("TESTING CONNECTIVITY")
    print("=" * 60)

    checker = ConnectivityChecker()
    is_connected = checker.check_connectivity(grid)
    print(f"\nIs connected: {is_connected}")

    if is_connected:
        path = checker.find_path(grid)
        if path:
            print(f"\n✓ Path found with {len(path)} positions:")
            for pos in path:
                tile = grid.get_tile(pos[0], pos[1])
                if tile:
                    print(f"  {pos} - {tile.tile_type.value}")
    else:
        print("\n✗ No path found!")
        print("\nLet's trace manually:")

        power = grid.get_power_source()
        if power:
            print(f"\nStarting from power source at ({power.x}, {power.y})")
            print(f"  Exits: {[str(d).split('.')[-1] for d in power.get_exit_directions()]}")

            # Try to follow EAST
            next_pos = power.get_neighbor_position(Direction.EAST)
            print(f"\n  Going EAST to {next_pos}")
            next_tile = grid.get_tile(*next_pos)
            if next_tile:
                print(f"    Found: {next_tile.tile_type.value} at ({next_tile.x}, {next_tile.y})")
                print(f"    Rotation: {next_tile.rotation}°")
                print(f"    Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
                print(f"    Can enter from EAST? {next_tile.has_entrance_from(Direction.EAST)}")
            else:
                print(f"    No tile found!")

if __name__ == "__main__":
    test_detailed_connectivity()
