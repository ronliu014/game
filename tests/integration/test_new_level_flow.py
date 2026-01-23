"""
Test the new level design with vertical path
"""
from src.core.level.level_loader import LevelLoader
from src.core.circuit.connectivity_checker import ConnectivityChecker

def test_new_level():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("NEW LEVEL LAYOUT TEST")
    print("=" * 60)
    print()

    print("Initial state (scrambled):")
    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile and tile.tile_type.value != "empty":
                exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
                print(f"  ({row},{col}): {tile.tile_type.value:15s} rot={tile.rotation:3d}deg exits={exits}")

    print()
    print("Checking connectivity (should be False)...")
    checker = ConnectivityChecker()
    is_connected = checker.check_connectivity(grid)
    print(f"Is connected: {is_connected}")

    print()
    print("=" * 60)
    print("SETTING TO SOLUTION STATE")
    print("=" * 60)
    print()

    # Set to solution
    solution_rotations = {
        (1, 0): 90,   # straight vertical
        (2, 0): 0,    # corner east+south
        (2, 1): 0,    # straight horizontal
        (2, 2): 0,    # straight horizontal
        (2, 3): 0,    # corner east+south
    }

    for (x, y), rotation in solution_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)
            print(f"Set ({x},{y}) to {rotation}deg")

    print()
    print("Solution state:")
    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile and tile.tile_type.value != "empty":
                exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
                print(f"  ({row},{col}): {tile.tile_type.value:15s} rot={tile.rotation:3d}deg exits={exits}")

    print()
    print("Checking connectivity (should be True)...")
    is_connected = checker.check_connectivity(grid)
    print(f"Is connected: {is_connected}")

    if is_connected:
        print("\nYES! Path found!")
        path = checker.find_path(grid)
        if path:
            print(f"Path length: {len(path)} tiles")
            print("Path:")
            for pos in path:
                tile = grid.get_tile(pos[0], pos[1])
                if tile:
                    print(f"  {pos} - {tile.tile_type.value}")
    else:
        print("\nNO! Path not found - let me trace manually...")

        # Manual trace
        power = grid.get_power_source()
        print(f"\nPower at ({power.x}, {power.y}), exits: {[str(d).split('.')[-1] for d in power.get_exit_directions()]}")

        from src.config.constants import Direction
        next_pos = power.get_neighbor_position(Direction.SOUTH)
        print(f"Going SOUTH to {next_pos}")
        next_tile = grid.get_tile(*next_pos)
        if next_tile:
            print(f"Found: {next_tile.tile_type.value}, exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
            print(f"Can enter from SOUTH? {next_tile.has_entrance_from(Direction.SOUTH)}")

if __name__ == "__main__":
    test_new_level()
