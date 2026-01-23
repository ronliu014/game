"""
Improved Level Generator Module (Version 2)

This module provides enhanced procedural level generation based on the improved algorithm:
1. Select start (power source) and end (terminal) positions
2. Use path-finding algorithm to find a valid path (not necessarily shortest)
3. Assign sprites and rotations based on path directions
4. Scramble tiles to create puzzle with configurable difficulty

Classes:
    LevelGeneratorV2: Enhanced level generator with difficulty support

Author: Circuit Repair Game Team
Date: 2026-01-22
"""

import random
from typing import List, Tuple, Dict, Optional, Set
from enum import Enum

from src.config.constants import Direction, DIRECTION_VECTORS
from src.core.level.difficulty_config import DifficultyLevel, DifficultyConfig
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class PathDirection(Enum):
    """Direction of path movement in grid coordinates."""
    NORTH = (-1, 0)  # row-1, up
    EAST = (0, 1)    # col+1, right
    SOUTH = (1, 0)   # row+1, down
    WEST = (0, -1)   # col-1, left


class LevelGeneratorV2:
    """
    Enhanced procedural level generator with difficulty support.

    Generates random but solvable puzzles by:
    1. Randomly placing power source and terminal
    2. Finding a valid path between them (not crossing, can backtrack)
    3. Assigning appropriate tiles (straight/corner) based on path directions
    4. Calculating correct rotations
    5. Scrambling tiles based on difficulty settings

    Attributes:
        difficulty: Difficulty level
        config: Difficulty configuration
        grid_size: Size of the grid (N for NxN)
        max_retries: Maximum number of generation attempts

    Example:
        >>> generator = LevelGeneratorV2(difficulty=DifficultyLevel.NORMAL)
        >>> level_data = generator.generate()
        >>> print(f"Generated level with {len(level_data['path'])} tiles")
    """

    def __init__(
        self,
        difficulty: DifficultyLevel = DifficultyLevel.NORMAL,
        grid_size: Optional[int] = None,
        max_retries: int = 50
    ):
        """
        Initialize the level generator.

        Args:
            difficulty: Difficulty level
            grid_size: Optional fixed grid size (overrides difficulty config)
            max_retries: Maximum number of generation attempts
        """
        self.difficulty = difficulty
        self.config = DifficultyConfig.get_config(difficulty)
        self.max_retries = max_retries

        # Use provided grid_size or random from difficulty range
        if grid_size is not None:
            self.grid_size = grid_size
        else:
            min_size, max_size = self.config.grid_size_range
            self.grid_size = random.randint(min_size, max_size)

        logger.info(
            f"LevelGeneratorV2 initialized: difficulty={difficulty.value}, "
            f"grid_size={self.grid_size}"
        )

    def generate(self) -> Dict:
        """
        Generate a random but solvable level.

        Returns:
            Dictionary containing:
                - solution: List of tile configurations
                - initial_state: List of scrambled rotations
                - path: List of (x, y) positions in the solution path
                - grid_size: Size of the grid
                - difficulty: Difficulty level
                - movable_count: Number of movable tiles
                - corner_count: Number of corner tiles

        Raises:
            RuntimeError: If unable to generate valid level after max_retries

        Example:
            >>> generator = LevelGeneratorV2(difficulty=DifficultyLevel.EASY)
            >>> level = generator.generate()
            >>> print(level['difficulty'])
            'easy'
        """
        logger.info(f"Generating new level (difficulty: {self.difficulty.value})...")

        for attempt in range(self.max_retries):
            try:
                # Step 1: Choose random start and end positions
                power_pos, terminal_pos = self._choose_endpoints()
                logger.debug(f"Attempt {attempt + 1}: power={power_pos}, terminal={terminal_pos}")

                # Step 2: Find a valid path between them
                path = self._find_valid_path(power_pos, terminal_pos)

                if path is None:
                    logger.debug(f"Attempt {attempt + 1}: No path found, retrying...")
                    continue

                # Validate path has no duplicates
                if len(path) != len(set(path)):
                    logger.warning(f"Attempt {attempt + 1}: Path has duplicate positions, retrying...")
                    continue

                # Step 3: Validate path meets difficulty requirements
                movable_count = len(path) - 2  # Exclude power source and terminal
                corner_count = self._count_corners(path)

                if not self.config.validate_path(movable_count, corner_count):
                    logger.debug(
                        f"Attempt {attempt + 1}: Path validation failed "
                        f"(movable={movable_count}, corners={corner_count}), retrying..."
                    )
                    continue

                logger.debug(
                    f"Attempt {attempt + 1}: Valid path found "
                    f"(length={len(path)}, movable={movable_count}, corners={corner_count})"
                )

                # Step 4: Create tile configurations based on path
                solution_tiles = self._create_tiles_from_path(path, power_pos, terminal_pos)

                # Step 5: Create scrambled initial state
                initial_state = self._create_scrambled_state(solution_tiles, movable_count)

                logger.info(
                    f"Level generated successfully: "
                    f"path_length={len(path)}, movable={movable_count}, corners={corner_count}"
                )

                return {
                    'solution': solution_tiles,
                    'initial_state': initial_state,
                    'path': path,
                    'grid_size': self.grid_size,
                    'difficulty': self.difficulty.value,
                    'movable_count': movable_count,
                    'corner_count': corner_count
                }

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed with error: {e}")
                continue

        # Failed to generate after max_retries
        error_msg = f"Failed to generate valid level after {self.max_retries} attempts"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    def _choose_endpoints(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Randomly choose positions for power source and terminal.

        Ensures they are not adjacent and have sufficient distance.

        Returns:
            Tuple of (power_position, terminal_position)
        """
        # Choose random power source position
        power_pos = (
            random.randint(0, self.grid_size - 1),
            random.randint(0, self.grid_size - 1)
        )

        # Choose terminal position (not adjacent, minimum distance based on difficulty)
        min_distance = self.config.min_movable_tiles + 1  # +1 for power and terminal

        while True:
            terminal_pos = (
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1)
            )

            # Check Manhattan distance
            dx = abs(power_pos[0] - terminal_pos[0])
            dy = abs(power_pos[1] - terminal_pos[1])
            manhattan_distance = dx + dy

            if manhattan_distance >= min_distance:
                break

        return power_pos, terminal_pos

    def _find_valid_path(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find a valid path from start to end using random DFS.

        The path:
        - Does NOT cross itself (no + junction tiles)
        - CAN backtrack (change direction)
        - Prefers variety in direction changes

        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)

        Returns:
            List of positions forming the path, or None if no valid path found
        """
        visited = set()
        path = []

        def dfs(pos: Tuple[int, int], prev_dir: Optional[PathDirection] = None) -> bool:
            """Recursive DFS with randomization."""
            if pos == end:
                return True

            visited.add(pos)
            path.append(pos)

            # Get valid neighbors (not visited, within bounds)
            neighbors = self._get_valid_neighbors(pos, visited)

            # Randomize neighbor order for variety
            random.shuffle(neighbors)

            # Try each neighbor
            for next_pos in neighbors:
                next_dir = self._get_direction(pos, next_pos)

                # Allow backtracking (direction can change)
                if dfs(next_pos, next_dir):
                    return True

            # Backtrack
            path.pop()
            return False

        if dfs(start):
            path.append(end)  # Add terminal position
            return path

        return None

    def _get_valid_neighbors(
        self,
        pos: Tuple[int, int],
        visited: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        Get valid neighboring positions (within bounds, not visited).

        Args:
            pos: Current position (x, y)
            visited: Set of visited positions

        Returns:
            List of valid neighbor positions
        """
        x, y = pos
        neighbors = []

        for direction in PathDirection:
            dx, dy = direction.value
            nx, ny = x + dx, y + dy

            # Check bounds
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                # Check not visited
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny))

        return neighbors

    def _get_direction(
        self,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int]
    ) -> PathDirection:
        """
        Get the direction from one position to another.

        Args:
            from_pos: Starting position
            to_pos: Ending position

        Returns:
            PathDirection enum value
        """
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]

        for direction in PathDirection:
            if direction.value == (dx, dy):
                return direction

        raise ValueError(f"Invalid direction from {from_pos} to {to_pos}")

    def _count_corners(self, path: List[Tuple[int, int]]) -> int:
        """
        Count the number of corner tiles in the path.

        Args:
            path: List of positions in the path

        Returns:
            Number of corner tiles
        """
        if len(path) < 3:
            return 0

        corner_count = 0

        for i in range(1, len(path) - 1):
            prev_pos = path[i - 1]
            curr_pos = path[i]
            next_pos = path[i + 1]

            # Get directions
            dir_in = self._get_direction(prev_pos, curr_pos)
            dir_out = self._get_direction(curr_pos, next_pos)

            # If directions are not opposite, it's a corner
            if not self._is_opposite(dir_in, dir_out):
                corner_count += 1

        return corner_count

    def _is_opposite(self, dir1: PathDirection, dir2: PathDirection) -> bool:
        """Check if two directions are opposite."""
        opposites = {
            PathDirection.NORTH: PathDirection.SOUTH,
            PathDirection.SOUTH: PathDirection.NORTH,
            PathDirection.EAST: PathDirection.WEST,
            PathDirection.WEST: PathDirection.EAST
        }
        return opposites[dir1] == dir2

    def _get_opposite_direction(self, direction: PathDirection) -> PathDirection:
        """Get the opposite direction."""
        opposites = {
            PathDirection.NORTH: PathDirection.SOUTH,
            PathDirection.SOUTH: PathDirection.NORTH,
            PathDirection.EAST: PathDirection.WEST,
            PathDirection.WEST: PathDirection.EAST
        }
        return opposites[direction]

    def _create_tiles_from_path(
        self,
        path: List[Tuple[int, int]],
        power_pos: Tuple[int, int],
        terminal_pos: Tuple[int, int]
    ) -> List[Dict]:
        """
        Create tile configurations based on the path.

        Determines tile type (straight/corner) and rotation based on
        the direction changes in the path.

        Args:
            path: List of positions in the path
            power_pos: Power source position
            terminal_pos: Terminal position

        Returns:
            List of tile configuration dictionaries
        """
        tiles = []

        # Create empty tiles for all positions
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tiles.append({
                    'x': x,
                    'y': y,
                    'type': 'empty',
                    'rotation': 0,
                    'is_clickable': False
                })

        # Place power source
        power_idx = power_pos[0] * self.grid_size + power_pos[1]
        power_exit_dir = self._get_direction(path[0], path[1])
        power_rotation = self._get_power_rotation(power_exit_dir)

        tiles[power_idx] = {
            'x': power_pos[0],
            'y': power_pos[1],
            'type': 'power_source',
            'rotation': power_rotation,
            'is_clickable': False
        }

        # Place tiles along the path (excluding start and end)
        for i in range(1, len(path) - 1):
            pos = path[i]
            prev_pos = path[i - 1]
            next_pos = path[i + 1]

            # Determine entry and exit directions
            # IMPORTANT: We need the tile's connection point directions, not movement directions
            # If current moves from prev to pos in SOUTH direction (downward),
            # the tile needs a connection point on the NORTH side (opposite)
            move_in = self._get_direction(prev_pos, pos)
            move_out = self._get_direction(pos, next_pos)

            # Convert movement directions to tile connection directions (opposite)
            entry_dir = self._get_opposite_direction(move_in)
            exit_dir = self._get_opposite_direction(move_out)

            # Determine tile type and rotation
            tile_type, rotation, accepted_rotations = self._get_tile_config(
                entry_dir, exit_dir
            )

            tile_idx = pos[0] * self.grid_size + pos[1]
            tiles[tile_idx] = {
                'x': pos[0],
                'y': pos[1],
                'type': tile_type,
                'rotation': rotation,
                'is_clickable': True,
                'accepted_rotations': accepted_rotations
            }

        # Place terminal
        terminal_idx = terminal_pos[0] * self.grid_size + terminal_pos[1]
        terminal_entry_dir = self._get_direction(path[-2], path[-1])
        terminal_rotation = self._get_terminal_rotation(terminal_entry_dir)

        tiles[terminal_idx] = {
            'x': terminal_pos[0],
            'y': terminal_pos[1],
            'type': 'terminal',
            'rotation': terminal_rotation,
            'is_clickable': False
        }

        return tiles

    def _get_power_rotation(self, exit_dir: PathDirection) -> int:
        """
        Get rotation for power source based on exit direction.

        Power source base (0°) exits EAST.

        Args:
            exit_dir: Direction power exits to

        Returns:
            Rotation angle in degrees
        """
        rotation_map = {
            PathDirection.EAST: 0,
            PathDirection.SOUTH: 90,
            PathDirection.WEST: 180,
            PathDirection.NORTH: 270
        }
        return rotation_map[exit_dir]

    def _get_terminal_rotation(self, entry_dir: PathDirection) -> int:
        """
        Get rotation for terminal based on entry direction.

        Terminal base (0°) accepts from WEST.

        Args:
            entry_dir: Direction entering terminal

        Returns:
            Rotation angle in degrees
        """
        rotation_map = {
            PathDirection.WEST: 0,    # Accepts from EAST
            PathDirection.NORTH: 90,  # Accepts from SOUTH
            PathDirection.EAST: 180,  # Accepts from WEST
            PathDirection.SOUTH: 270  # Accepts from NORTH
        }
        return rotation_map[entry_dir]

    def _get_tile_config(
        self,
        entry_dir: PathDirection,
        exit_dir: PathDirection
    ) -> Tuple[str, int, List[int]]:
        """
        Determine tile type, rotation, and accepted rotations.

        Based on user's algorithm:
        - Straight tile: entry and exit are opposite directions
        - Corner tile: entry and exit are perpendicular

        Sprite definitions:
        - tile_straight.png:
          * 0°: horizontal (EAST-WEST)
          * 90°: vertical (NORTH-SOUTH)
        - tile_corner.png:
          * 0°: connects NORTH and EAST (L shape, opening right-up)
          * 90°: connects EAST and SOUTH
          * 180°: connects SOUTH and WEST
          * 270°: connects WEST and NORTH

        Args:
            entry_dir: Direction entering the tile
            exit_dir: Direction exiting the tile

        Returns:
            Tuple of (tile_type, rotation, accepted_rotations)
        """
        # Check if it's a straight line (same or opposite directions)
        if entry_dir == exit_dir or self._is_opposite(entry_dir, exit_dir):
            # Straight tile
            if entry_dir in [PathDirection.EAST, PathDirection.WEST] or exit_dir in [PathDirection.EAST, PathDirection.WEST]:
                # Horizontal: 0° or 180° (equivalent)
                return 'straight', 0, [0, 180]
            else:
                # Vertical: 90° or 270° (equivalent)
                return 'straight', 90, [90, 270]
        else:
            # Corner tile
            rotation = self._get_corner_rotation(entry_dir, exit_dir)
            return 'corner', rotation, [rotation]

    def _get_corner_rotation(
        self,
        entry_dir: PathDirection,
        exit_dir: PathDirection
    ) -> int:
        """
        Get rotation for corner tile based on entry and exit directions.

        Corner rotations (bidirectional):
        - 0°: NORTH↔EAST (connects up and right)
        - 90°: EAST↔SOUTH (connects right and down)
        - 180°: SOUTH↔WEST (connects down and left)
        - 270°: WEST↔NORTH (connects left and up)

        Args:
            entry_dir: Direction entering the corner
            exit_dir: Direction exiting the corner

        Returns:
            Rotation angle in degrees
        """
        # Map (entry, exit) to rotation - corners are bidirectional
        corner_map = {
            # 0° corner: connects NORTH and EAST
            (PathDirection.NORTH, PathDirection.EAST): 0,
            (PathDirection.EAST, PathDirection.NORTH): 0,

            # 90° corner: connects EAST and SOUTH
            (PathDirection.EAST, PathDirection.SOUTH): 90,
            (PathDirection.SOUTH, PathDirection.EAST): 90,

            # 180° corner: connects SOUTH and WEST
            (PathDirection.SOUTH, PathDirection.WEST): 180,
            (PathDirection.WEST, PathDirection.SOUTH): 180,

            # 270° corner: connects WEST and NORTH
            (PathDirection.WEST, PathDirection.NORTH): 270,
            (PathDirection.NORTH, PathDirection.WEST): 270
        }

        result = corner_map.get((entry_dir, exit_dir))
        if result is None:
            logger.error(
                f"Invalid corner combination: entry={entry_dir.name}, exit={exit_dir.name}"
            )
            return 0
        return result

    def _create_scrambled_state(
        self,
        solution_tiles: List[Dict],
        movable_count: int
    ) -> List[Dict]:
        """
        Create scrambled initial state by randomly rotating clickable tiles.

        Uses difficulty-based scramble ratio to determine how many tiles
        need manual rotation.

        Args:
            solution_tiles: List of solution tile configurations
            movable_count: Number of movable tiles

        Returns:
            List of rotated tile configurations for initial state
        """
        scrambled = []
        clickable_tiles = [t for t in solution_tiles if t['is_clickable']]

        # Calculate how many tiles should be scrambled
        tiles_to_scramble = int(movable_count * self.config.scramble_ratio)
        tiles_to_scramble = max(1, tiles_to_scramble)  # At least 1 tile

        # Randomly select tiles to scramble
        tiles_to_scramble_set = set(
            random.sample(range(len(clickable_tiles)), min(tiles_to_scramble, len(clickable_tiles)))
        )

        logger.debug(
            f"Scrambling {len(tiles_to_scramble_set)}/{len(clickable_tiles)} tiles "
            f"(ratio: {self.config.scramble_ratio})"
        )

        for idx, tile in enumerate(clickable_tiles):
            if idx in tiles_to_scramble_set:
                # Scramble this tile - choose a rotation NOT in accepted list
                accepted = tile.get('accepted_rotations', [tile['rotation']])
                invalid_rotations = [r for r in [0, 90, 180, 270] if r not in accepted]

                if invalid_rotations:
                    random_rotation = random.choice(invalid_rotations)
                else:
                    # Fallback: just rotate randomly
                    random_rotation = random.choice([0, 90, 180, 270])
            else:
                # Keep correct rotation
                random_rotation = tile['rotation']

            scrambled.append({
                'x': tile['x'],
                'y': tile['y'],
                'rotation': random_rotation
            })

        return scrambled
