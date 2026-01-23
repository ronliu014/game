"""
Test connectivity for level_001
"""
from src.core.level.level_loader import LevelLoader
from src.core.circuit.connectivity_checker import ConnectivityChecker

def test_connectivity():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print(f"Grid loaded: {grid.grid_size}x{grid.grid_size}")
    print()

    # Check power source and terminal
    power = grid.get_power_source()
    terminal = grid.get_terminal()

    if power:
        print(f"Power source at: ({power.x}, {power.y})")
        print(f"  Rotation: {power.rotation}°")
        print(f"  Exits: {[str(d) for d in power.get_exit_directions()]}")
    else:
        print("No power source found!")

    print()

    if terminal:
        print(f"Terminal at: ({terminal.x}, {terminal.y})")
        print(f"  Rotation: {terminal.rotation}°")
        print(f"  Exits: {[str(d) for d in terminal.get_exit_directions()]}")
    else:
        print("No terminal found!")

    print()
    print("=" * 50)
    print("Checking connectivity with INITIAL state (scrambled):")
    print("=" * 50)

    checker = ConnectivityChecker()
    is_connected = checker.check_connectivity(grid)
    print(f"Is connected: {is_connected}")

    if is_connected:
        path = checker.find_path(grid)
        if path:
            print(f"Path found with {len(path)} positions:")
            for pos in path:
                print(f"  {pos}")
    else:
        print("No path found (expected - tiles are scrambled)")

    print()
    print("=" * 50)
    print("Resetting to SOLUTION state:")
    print("=" * 50)

    # Reset all tiles to solution rotation
    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            tile = grid.get_tile(row, col)
            if tile and tile.is_clickable:
                # Get the solution rotation from level data
                # For now, just print what we have
                print(f"Tile at ({row}, {col}): {tile.tile_type.value}, rotation={tile.rotation}°")

    print()
    print("Checking connectivity after reset:")
    is_connected = checker.check_connectivity(grid)
    print(f"Is connected: {is_connected}")

    if is_connected:
        path = checker.find_path(grid)
        if path:
            print(f"Path found with {len(path)} positions:")
            for pos in path:
                print(f"  {pos}")

if __name__ == "__main__":
    test_connectivity()
