"""
Test the new configuration-based victory condition using accepted_rotations
"""
from src.core.level.level_loader import LevelLoader
from src.core.level.level_manager import LevelManager

def test_config_based_victory():
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
    print(f"{'PASS' if not is_complete else 'FAIL'}")
    print()

    print("=" * 60)
    print("TEST 2: Solution State - Should be True")
    print("=" * 60)
    print("Setting tiles to solution rotations:")
    print("  (1,0): 90deg  - accepted: [90, 270]")
    print("  (2,0): 0deg   - accepted: [0]")
    print("  (2,1): 0deg   - accepted: [0, 180]")
    print("  (2,2): 0deg   - accepted: [0, 180]")
    print("  (2,3): 0deg   - accepted: [0]")
    print()

    solution_rotations = {
        (1, 0): 90,
        (2, 0): 0,
        (2, 1): 0,
        (2, 2): 0,
        (2, 3): 0,
    }

    grid = manager.get_grid()
    for (x, y), rotation in solution_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: True")
    print(f"{'PASS' if is_complete else 'FAIL'}")
    print()

    print("=" * 60)
    print("TEST 3: Straight Line Accepts 180deg (Config-Based)")
    print("=" * 60)
    print("(2,1) has accepted_rotations: [0, 180]")
    print("Setting (2,1) to 180deg (designer allows this)")

    tile_21 = grid.get_tile(2, 1)
    if tile_21:
        tile_21.set_rotation(180)

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: True (180 is in accepted list)")
    print(f"{'PASS' if is_complete else 'FAIL'}")
    print()

    print("=" * 60)
    print("TEST 4: Straight Line Accepts 270deg (Config-Based)")
    print("=" * 60)
    print("(1,0) has accepted_rotations: [90, 270]")
    print("Setting (1,0) to 270deg (designer allows this)")

    # Reset (2,1) to 0deg
    tile_21.set_rotation(0)

    tile_10 = grid.get_tile(1, 0)
    if tile_10:
        tile_10.set_rotation(270)

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: True (270 is in accepted list)")
    print(f"{'PASS' if is_complete else 'FAIL'}")
    print()

    print("=" * 60)
    print("TEST 5: Corner Only Accepts Single Rotation")
    print("=" * 60)
    print("(2,0) has accepted_rotations: [0] (only one value)")
    print("Setting (2,0) to 90deg (NOT in accepted list)")

    # Reset (1,0) to 90deg
    tile_10.set_rotation(90)

    tile_20 = grid.get_tile(2, 0)
    if tile_20:
        tile_20.set_rotation(90)

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: False (90 not in accepted list [0])")
    print(f"{'PASS' if not is_complete else 'FAIL'}")
    print()

    print("=" * 60)
    print("TEST 6: Invalid Rotation for Straight Line")
    print("=" * 60)
    print("(2,1) has accepted_rotations: [0, 180]")
    print("Setting (2,1) to 90deg (NOT in accepted list)")

    # Reset (2,0) to 0deg
    tile_20.set_rotation(0)

    tile_21.set_rotation(90)

    is_complete = manager.check_win_condition()
    print(f"Result: {is_complete}")
    print(f"Expected: False (90 not in accepted list [0, 180])")
    print(f"{'PASS' if not is_complete else 'FAIL'}")
    print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("The new system is fully configuration-based:")
    print("- Level designers define accepted_rotations for each tile")
    print("- Game logic simply checks if current rotation is in the list")
    print("- No hardcoded rules about tile types")
    print("- Maximum flexibility for puzzle design")
    print()
    print("Examples of flexibility:")
    print("- Straight tile can accept [0, 180] for symmetric solutions")
    print("- Straight tile can accept [0] to force exact rotation")
    print("- Future diode can accept [0] for one-way flow")
    print("- Designer could even set [0, 90] for creative puzzles")

if __name__ == "__main__":
    test_config_based_victory()
