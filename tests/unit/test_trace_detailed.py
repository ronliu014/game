"""
Detailed trace of connectivity checking to find the issue
"""
from src.core.level.level_loader import LevelLoader
from src.config.constants import Direction

def test_detailed_trace():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    print("=" * 60)
    print("DETAILED CONNECTIVITY TRACE")
    print("=" * 60)
    print()

    # Set tiles to screenshot state (based on visual appearance)
    # From screenshot, the circuit LOOKS connected
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

    print()
    print("=" * 60)
    print("MANUAL PATH TRACE")
    print("=" * 60)
    print()

    # Start from power source
    power = grid.get_power_source()
    if not power:
        print("No power source found!")
        return

    print(f"Step 1: Power source at ({power.x}, {power.y})")
    print(f"  Rotation: {power.rotation}°")
    exits = [str(d).split('.')[-1] for d in power.get_exit_directions()]
    print(f"  Exits: {exits}")
    print()

    # Try to follow the path
    current = power
    step = 2

    # Power -> (1,0)
    print(f"Step {step}: Trying to go EAST from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.EAST)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value} at ({next_tile.x}, {next_tile.y})")
        print(f"  Rotation: {next_tile.rotation}°")
        exits = [str(d).split('.')[-1] for d in next_tile.get_exit_directions()]
        print(f"  Exits: {exits}")
        can_enter = next_tile.has_entrance_from(Direction.EAST)
        print(f"  Can enter from EAST? {can_enter}")
        if can_enter:
            print(f"  SUCCESS - can enter!")
            current = next_tile
            step += 1
        else:
            print(f"  FAILED - cannot enter!")
            return
    else:
        print(f"  No tile found!")
        return
    print()

    # (1,0) -> (2,0)
    print(f"Step {step}: Trying to go EAST from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.EAST)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value} at ({next_tile.x}, {next_tile.y})")
        print(f"  Rotation: {next_tile.rotation}°")
        exits = [str(d).split('.')[-1] for d in next_tile.get_exit_directions()]
        print(f"  Exits: {exits}")
        can_enter = next_tile.has_entrance_from(Direction.EAST)
        print(f"  Can enter from EAST? {can_enter}")
        if can_enter:
            print(f"  SUCCESS - can enter!")
            current = next_tile
            step += 1
        else:
            print(f"  FAILED - cannot enter!")
            print()
            print("=" * 60)
            print("PROBLEM FOUND!")
            print("=" * 60)
            print(f"Tile at ({next_tile.x}, {next_tile.y}) is a corner at {next_tile.rotation}°")
            print(f"  Exits: {exits}")
            print(f"  To enter from EAST, it needs a WEST exit")
            print(f"  But it has exits: {exits}")
            print()
            print("SOLUTION:")
            print(f"  The corner at ({next_tile.x}, {next_tile.y}) should be at 90° (exits SOUTH+WEST)")
            print(f"  Currently it's at {next_tile.rotation}° (exits {exits})")
            return
    else:
        print(f"  No tile found!")
        return
    print()

    # (2,0) -> (2,1)
    print(f"Step {step}: Trying to go from ({current.x}, {current.y})")
    print(f"  Current tile exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    # Corner at 180° has exits WEST+NORTH, so it should go NORTH
    print(f"  Trying to go NORTH...")
    next_pos = current.get_neighbor_position(Direction.NORTH)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value} at ({next_tile.x}, {next_tile.y})")
        print(f"  Rotation: {next_tile.rotation}°")
        exits = [str(d).split('.')[-1] for d in next_tile.get_exit_directions()]
        print(f"  Exits: {exits}")
        can_enter = next_tile.has_entrance_from(Direction.NORTH)
        print(f"  Can enter from NORTH? {can_enter}")
        if can_enter:
            print(f"  SUCCESS - can enter!")
            current = next_tile
            step += 1
        else:
            print(f"  FAILED - cannot enter from NORTH!")
            print(f"  To enter from NORTH, need a SOUTH exit, but exits are: {exits}")
            return
    else:
        print(f"  No tile found!")
        return
    print()

    # Continue tracing...
    for i in range(10):  # max 10 steps to avoid infinite loop
        print(f"Step {step}: At ({current.x}, {current.y})")
        print(f"  Tile type: {current.tile_type.value}")
        print(f"  Rotation: {current.rotation}°")
        exits = [str(d).split('.')[-1] for d in current.get_exit_directions()]
        print(f"  Exits: {exits}")

        # Check if we reached terminal
        if current.tile_type.value == "terminal":
            print("\n" + "=" * 60)
            print("SUCCESS! Reached terminal!")
            print("=" * 60)
            return

        # Try each exit direction
        for direction in current.get_exit_directions():
            next_pos = current.get_neighbor_position(direction)
            next_tile = grid.get_tile(*next_pos)

            if next_tile and next_tile.has_entrance_from(direction):
                print(f"  Going {str(direction).split('.')[-1]} to {next_pos}")
                current = next_tile
                step += 1
                break
        else:
            print("  No valid exit found!")
            return
        print()

if __name__ == "__main__":
    test_detailed_trace()
