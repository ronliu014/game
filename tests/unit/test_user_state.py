"""
Test to simulate the user's current state from screenshot
"""
from src.core.level.level_loader import LevelLoader
from src.core.circuit.connectivity_checker import ConnectivityChecker

def test_user_state():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("SIMULATING USER'S STATE FROM SCREENSHOT")
    print("=" * 60)
    print()

    # Based on screenshot, set tiles to what appears to be the current state
    # User has made 8 moves
    user_rotations = {
        (1, 0): 0,   # straight horizontal - looks correct in screenshot
        (2, 0): 90,  # corner - looks correct in screenshot
        (2, 1): 90,  # straight vertical - shows 90° in screenshot
        (2, 2): 90,  # straight vertical - shows 90° in screenshot
        (2, 3): 90,  # corner - THIS IS THE PROBLEM! Should be 270°
    }

    print("Setting tiles to user's current state:")
    for (x, y), rotation in user_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)
            exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
            print(f"  ({x},{y}): {tile.tile_type.value:12s} rot={rotation:3d}° exits={exits}")

    print()
    print("=" * 60)
    print("TESTING CONNECTIVITY WITH USER'S STATE")
    print("=" * 60)

    checker = ConnectivityChecker()
    is_connected = checker.check_connectivity(grid)
    print(f"\nIs connected: {is_connected}")

    if not is_connected:
        print("\nX NOT CONNECTED!")
        print("\nProblem: (2,3) is at 90 degrees but needs to be at 270 degrees")
        print("  - At 90 degrees: corner exits SOUTH+WEST (cannot reach terminal at east)")
        print("  - At 270 degrees: corner exits NORTH+EAST (can reach terminal at east)")
        print("\nSolution: Click (2,3) TWO more times to rotate from 90 -> 180 -> 270")

    print()
    print("=" * 60)
    print("NOW TESTING WITH CORRECT ROTATION AT (2,3)")
    print("=" * 60)

    # Fix (2,3) to 270 degrees
    tile_2_3 = grid.get_tile(2, 3)
    if tile_2_3:
        tile_2_3.set_rotation(270)
        exits = [str(d).split('.')[-1] for d in tile_2_3.get_exit_directions()]
        print(f"\nFixed: (2,3): {tile_2_3.tile_type.value:12s} rot=270 degrees exits={exits}")

    is_connected = checker.check_connectivity(grid)
    print(f"\nIs connected: {is_connected}")

    if is_connected:
        print("\nY CONNECTED! Victory should trigger now!")
        path = checker.find_path(grid)
        if path:
            print(f"\nPath found with {len(path)} positions:")
            for pos in path:
                tile = grid.get_tile(pos[0], pos[1])
                if tile:
                    print(f"  {pos} - {tile.tile_type.value}")

if __name__ == "__main__":
    test_user_state()
