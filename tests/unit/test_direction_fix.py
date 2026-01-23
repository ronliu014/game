"""
Manual trace with corrected coordinates
"""
from src.core.level.level_loader import LevelLoader
from src.config.constants import Direction

def test_manual_trace():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    if not grid:
        print("Failed to load grid")
        return

    # Set to solution state
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

    print("=" * 60)
    print("MANUAL PATH TRACE WITH CORRECT COORDINATES")
    print("=" * 60)
    print()

    # Start from power source at (0, 0)
    current = grid.get_power_source()
    print(f"Step 1: Power source at ({current.x}, {current.y})")
    print(f"  Rotation: {current.rotation}deg")
    print(f"  Exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print()

    # Step 2: Go EAST to (1, 0)
    print(f"Step 2: From ({current.x}, {current.y}), going EAST")
    next_pos = current.get_neighbor_position(Direction.EAST)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from EAST? {next_tile.has_entrance_from(Direction.EAST)}")
    else:
        print(f"  Tile is: {next_tile}")
    print()

    # Actually, power source is at (0, 0) and going EAST should be (1, 0) which is empty
    # Let me check the direction vectors
    print("Direction vectors:")
    from src.config.constants import DIRECTION_VECTORS
    for direction, vector in DIRECTION_VECTORS.items():
        print(f"  {direction}: {vector}")
    print()

    print("Actual next position calculation:")
    print(f"  Current: ({current.x}, {current.y})")
    print(f"  Direction: EAST = {DIRECTION_VECTORS[Direction.EAST]}")
    print(f"  Next = ({current.x + DIRECTION_VECTORS[Direction.EAST][0]}, {current.y + DIRECTION_VECTORS[Direction.EAST][1]})")
    print()

    # Wait, EAST is (1, 0), so from (0, 0) + (1, 0) = (1, 0)
    # But according to the grid layout, (1, 0) is empty
    # The correct path should be (0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2) -> (3, 2) -> (3, 3)

    print("Expected visual layout (row, col):")
    print("  Row 0: (0,0)power  (0,1)straight  (0,2)corner  (0,3)empty")
    print("  Row 1: (1,0)empty  (1,1)empty     (1,2)straight  (1,3)empty")
    print("  Row 2: (2,0)empty  (2,1)empty     (2,2)straight  (2,3)empty")
    print("  Row 3: (3,0)empty  (3,1)empty     (3,2)corner  (3,3)terminal")
    print()

    print("With EAST = (1, 0), going EAST from (0, 0) gives (1, 0) which is empty!")
    print("This is WRONG!")
    print()

    print("The problem is: EAST should move along columns, not rows!")
    print("  EAST should be (0, 1) not (1, 0)")
    print("  SOUTH should be (1, 0) not (0, 1)")

if __name__ == "__main__":
    test_manual_trace()
