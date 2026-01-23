"""
Test the new rotation-matching victory condition
"""
from src.core.level.level_loader import LevelLoader
from src.core.level.level_manager import LevelManager

def test_rotation_match():
    loader = LevelLoader()
    manager = LevelManager(loader)

    # Load level
    success = manager.load_level('data/levels/level_001.json')
    if not success:
        print("Failed to load level")
        return

    print("=" * 60)
    print("TEST 1: Initial State (Scrambled) - Should be False")
    print("=" * 60)
    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: False")
    print(f"PASS" if not is_complete else "FAIL")
    print()

    print("=" * 60)
    print("TEST 2: Solution State - Should be True")
    print("=" * 60)

    # Set all tiles to solution rotation
    solution_rotations = {
        (1, 0): 90,   # straight vertical
        (2, 0): 0,    # corner east+south
        (2, 1): 0,    # straight horizontal
        (2, 2): 0,    # straight horizontal
        (2, 3): 0,    # corner east+south
    }

    grid = manager.get_grid()
    for (x, y), rotation in solution_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)
            print(f"Set ({x},{y}) to {rotation}deg")

    is_complete = manager.check_win_condition()
    print(f"\nResult: {is_complete}")
    print(f"Expected: True")
    print(f"PASS" if is_complete else "FAIL")
    print()

    print("=" * 60)
    print("TEST 3: Straight Line Equivalence (0deg = 180deg)")
    print("=" * 60)

    # Set straight tile at (2,1) to 180deg (should be equivalent to 0deg)
    tile_21 = grid.get_tile(2, 1)
    if tile_21:
        tile_21.set_rotation(180)
        print(f"Set (2,1) straight tile to 180deg (solution is 0deg)")

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: True (0deg and 180deg are equivalent for straight)")
    print(f"PASS" if is_complete else "FAIL")
    print()

    print("=" * 60)
    print("TEST 4: Straight Line Equivalence (90deg = 270deg)")
    print("=" * 60)

    # Reset (2,1) to 0deg
    tile_21.set_rotation(0)

    # Set straight tile at (1,0) to 270deg (should be equivalent to 90deg)
    tile_10 = grid.get_tile(1, 0)
    if tile_10:
        tile_10.set_rotation(270)
        print(f"Set (1,0) straight tile to 270deg (solution is 90deg)")

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: True (90deg and 270deg are equivalent for straight)")
    print(f"PASS" if is_complete else "FAIL")
    print()

    print("=" * 60)
    print("TEST 5: Corner Wrong Rotation - Should be False")
    print("=" * 60)

    # Reset (1,0) to 90deg
    tile_10.set_rotation(90)

    # Set corner tile at (2,0) to wrong rotation
    tile_20 = grid.get_tile(2, 0)
    if tile_20:
        tile_20.set_rotation(90)  # Wrong! Should be 0
        print(f"Set (2,0) corner tile to 90deg (solution is 0deg)")

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: False (corner rotation mismatch)")
    print(f"PASS" if not is_complete else "FAIL")
    print()

    print("=" * 60)
    print("TEST 6: All Tests Summary")
    print("=" * 60)
    print("New victory condition uses angle matching instead of connectivity.")
    print("Straight tiles accept equivalent rotations (0=180, 90=270).")
    print("This approach is simpler and lets humans define the solution.")

if __name__ == "__main__":
    test_rotation_match()
