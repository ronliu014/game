"""
Test to check if the connectivity checker is working correctly
with the visual state from screenshot
"""
from src.core.level.level_loader import LevelLoader
from src.core.circuit.connectivity_checker import ConnectivityChecker

def test_visual_connectivity():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("TESTING VISUAL CONNECTIVITY FROM SCREENSHOT")
    print("=" * 60)
    print()

    # From screenshot, the visual circuit appears connected
    # Let's test with the angles shown in the debug display
    screenshot_rotations = {
        (1, 0): 180,  # straight - shown as 180° in screenshot
        (2, 0): 180,  # corner - shown as 180° in screenshot
        (2, 1): 270,  # straight - shown as 270° in screenshot
        (2, 2): 270,  # straight - shown as 270° in screenshot
        (2, 3): 270,  # corner - should be 270° based on visual
    }

    print("Setting tiles to screenshot state:")
    for (x, y), rotation in screenshot_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)
            exits = [str(d).split('.')[-1] for d in tile.get_exit_directions()]
            print(f"  ({x},{y}): {tile.tile_type.value:12s} rot={rotation:3d}° exits={exits}")

    print()
    print("=" * 60)
    print("CHECKING CONNECTIVITY")
    print("=" * 60)

    checker = ConnectivityChecker()
    is_connected = checker.check_connectivity(grid)
    print(f"\nIs connected: {is_connected}")

    if is_connected:
        print("\nY Circuit is connected! Victory should trigger!")
        path = checker.find_path(grid)
        if path:
            print(f"\nPath found with {len(path)} positions:")
            for pos in path:
                tile = grid.get_tile(pos[0], pos[1])
                if tile:
                    print(f"  {pos} - {tile.tile_type.value}")
    else:
        print("\nX Circuit is NOT connected")
        print("\nLet's trace the path manually:")

        power = grid.get_power_source()
        if power:
            print(f"\nPower source at ({power.x}, {power.y})")
            print(f"  Exits: {[str(d).split('.')[-1] for d in power.get_exit_directions()]}")

            # Check each connection
            from src.config.constants import Direction

            # Power -> (1,0)
            next_tile = grid.get_tile(1, 0)
            if next_tile:
                print(f"\n(1,0): {next_tile.tile_type.value} rot={next_tile.rotation}°")
                print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
                print(f"  Can enter from WEST? {next_tile.has_entrance_from(Direction.WEST)}")

if __name__ == "__main__":
    test_visual_connectivity()
