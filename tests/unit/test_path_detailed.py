"""
Detailed path trace to find the break
"""
from src.core.level.level_loader import LevelLoader
from src.config.constants import Direction

def detailed_trace():
    loader = LevelLoader()
    grid = loader.load_level('data/levels/level_001.json')

    # Set to solution
    solution_rotations = {
        (1, 0): 90,
        (2, 0): 0,
        (2, 1): 0,
        (2, 2): 0,
        (2, 3): 0,  # Changed from 270 to 0
    }

    for (x, y), rotation in solution_rotations.items():
        tile = grid.get_tile(x, y)
        if tile:
            tile.set_rotation(rotation)

    print("=" * 60)
    print("DETAILED PATH TRACE")
    print("=" * 60)
    print()

    # Expected path:
    # (0,0) power SOUTH -> (1,0) straight SOUTH -> (2,0) corner EAST ->
    # (2,1) straight EAST -> (2,2) straight EAST -> (2,3) corner SOUTH ->
    # (3,3) terminal

    current = grid.get_power_source()
    step = 1

    print(f"Step {step}: Power at ({current.x}, {current.y})")
    print(f"  Exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print()

    # Step 2: (0,0) -> (1,0)
    step += 1
    print(f"Step {step}: Going SOUTH from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.SOUTH)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Rotation: {next_tile.rotation}deg")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from NORTH? {next_tile.has_entrance_from(Direction.NORTH)}")
        if next_tile.has_entrance_from(Direction.NORTH):
            current = next_tile
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED!")
            return
    print()

    # Step 3: (1,0) -> (2,0)
    step += 1
    print(f"Step {step}: At ({current.x}, {current.y}), exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print(f"  Going SOUTH from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.SOUTH)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Rotation: {next_tile.rotation}deg")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from NORTH? {next_tile.has_entrance_from(Direction.NORTH)}")
        if next_tile.has_entrance_from(Direction.NORTH):
            current = next_tile
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED!")
            return
    print()

    # Step 4: (2,0) -> (2,1)
    step += 1
    print(f"Step {step}: At ({current.x}, {current.y}), exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print(f"  Going EAST from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.EAST)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Rotation: {next_tile.rotation}deg")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from WEST? {next_tile.has_entrance_from(Direction.WEST)}")
        if next_tile.has_entrance_from(Direction.WEST):
            current = next_tile
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED!")
            return
    print()

    # Step 5: (2,1) -> (2,2)
    step += 1
    print(f"Step {step}: At ({current.x}, {current.y}), exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print(f"  Going EAST from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.EAST)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Rotation: {next_tile.rotation}deg")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from WEST? {next_tile.has_entrance_from(Direction.WEST)}")
        if next_tile.has_entrance_from(Direction.WEST):
            current = next_tile
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED!")
            return
    print()

    # Step 6: (2,2) -> (2,3)
    step += 1
    print(f"Step {step}: At ({current.x}, {current.y}), exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print(f"  Going EAST from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.EAST)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Rotation: {next_tile.rotation}deg")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from WEST? {next_tile.has_entrance_from(Direction.WEST)}")
        if next_tile.has_entrance_from(Direction.WEST):
            current = next_tile
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED!")
            return
    print()

    # Step 7: (2,3) -> (3,3)
    step += 1
    print(f"Step {step}: At ({current.x}, {current.y}), exits: {[str(d).split('.')[-1] for d in current.get_exit_directions()]}")
    print(f"  Going SOUTH from ({current.x}, {current.y})")
    next_pos = current.get_neighbor_position(Direction.SOUTH)
    print(f"  Next position: {next_pos}")
    next_tile = grid.get_tile(*next_pos)
    if next_tile:
        print(f"  Found: {next_tile.tile_type.value}")
        print(f"  Rotation: {next_tile.rotation}deg")
        print(f"  Exits: {[str(d).split('.')[-1] for d in next_tile.get_exit_directions()]}")
        print(f"  Can enter from NORTH? {next_tile.has_entrance_from(Direction.NORTH)}")
        if next_tile.has_entrance_from(Direction.NORTH):
            current = next_tile
            print(f"  SUCCESS! Reached terminal!")
        else:
            print(f"  FAILED!")
            return
    print()

    print("=" * 60)
    print("PATH COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    detailed_trace()
