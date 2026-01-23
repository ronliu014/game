"""
Show the generated path visually
"""
from src.core.level.level_generator import LevelGenerator

def test_show_path():
    """Generate a level and show the path visually."""

    print("=" * 60)
    print("VISUAL PATH DISPLAY")
    print("=" * 60)
    print()

    # Generate level
    generator = LevelGenerator(grid_size=4, min_path_length=5)
    result = generator.generate()

    print(f"Grid size: {result['grid_size']}")
    print(f"Path length: {len(result['path'])}")
    print()

    # Create a visual grid
    grid = [[' ' for _ in range(4)] for _ in range(4)]

    # Mark path positions with numbers
    for i, (x, y) in enumerate(result['path']):
        if i == 0:
            grid[x][y] = 'P'  # Power
        elif i == len(result['path']) - 1:
            grid[x][y] = 'T'  # Terminal
        else:
            grid[x][y] = str(i)  # Path index

    # Print grid
    print("Path visualization (P=Power, T=Terminal, numbers=path order):")
    print("   ", end="")
    for col in range(4):
        print(f" {col} ", end="")
    print()
    print("   " + "---" * 4)

    for row in range(4):
        print(f" {row} |", end="")
        for col in range(4):
            print(f" {grid[row][col]} ", end="")
        print("|")
    print("   " + "---" * 4)
    print()

    # Print path with directions
    print("Path with directions:")
    for i in range(len(result['path']) - 1):
        curr = result['path'][i]
        next_pos = result['path'][i + 1]
        dx = next_pos[0] - curr[0]
        dy = next_pos[1] - curr[1]

        direction = ""
        if dx == -1: direction = "NORTH (up)"
        elif dx == 1: direction = "SOUTH (down)"
        elif dy == -1: direction = "WEST (left)"
        elif dy == 1: direction = "EAST (right)"

        print(f"  {curr} -> {next_pos}: {direction}")
    print()

    # Print tile configurations
    print("Tile configurations:")
    for tile in result['solution']:
        if tile['type'] not in ['empty', 'power_source', 'terminal']:
            accepted = tile.get('accepted_rotations', [tile['rotation']])
            print(f"  ({tile['x']}, {tile['y']}): {tile['type']:10s} "
                  f"rotation={tile['rotation']:3d}° accepted={accepted}")

if __name__ == "__main__":
    test_show_path()
