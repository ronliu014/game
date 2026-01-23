"""
Level Generator V3 - Based on User's Algorithm

Completely rewritten based on user's detailed algorithm specification.

Key Points:
1. Use BFS/DFS to find a path from power source to terminal
2. For each tile in the path, determine sprite and rotation based on:
   - Previous tile position (where we came from)
   - Next tile position (where we're going to)
3. Sprite definitions (screen coordinate system: x-right, y-down):
   - tile_straight.png:
     * 0°: horizontal line (left to right)
     * 90°: vertical line (top to bottom)
     * 180°: horizontal line (right to left) - equivalent to 0°
     * 270°: vertical line (bottom to top) - equivalent to 90°
   - tile_corner.png:
     * 0°: connects top and right (from top, turn right)
     * 90°: connects right and bottom (from right, turn down)
     * 180°: connects bottom and left (from bottom, turn left)
     * 270°: connects left and top (from left, turn up)

Author: Circuit Repair Game Team
Date: 2026-01-23
Version: 3.0
"""

import random
import logging
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
from src.core.level.difficulty_config import DifficultyLevel, DifficultyConfig

logger = logging.getLogger(__name__)


class Direction(Enum):
    """Direction enumeration for grid navigation."""
    UP = (0, -1)      # y decreases
    DOWN = (0, 1)     # y increases
    LEFT = (-1, 0)    # x decreases
    RIGHT = (1, 0)    # x increases


class LevelGeneratorV3:
    """
    Level generator V3 - implements user's algorithm specification.

    Generates levels by:
    1. Selecting random power source and terminal positions
    2. Finding a path between them using DFS
    3. Assigning correct sprites and rotations based on path geometry
    4. Scrambling tiles according to difficulty settings
    """

    def __init__(
        self,
        difficulty: DifficultyLevel = DifficultyLevel.NORMAL,
        grid_size: Optional[int] = None
    ):
        """
        Initialize level generator.

        Args:
            difficulty: Difficulty level
            grid_size: Optional fixed grid size (overrides difficulty config)
        """
        self.difficulty = difficulty
        self.config = DifficultyConfig.get_config(difficulty)

        # Determine grid size
        if grid_size is not None:
            self.grid_size = grid_size
        else:
            # Random size within difficulty range
            min_size, max_size = self.config.grid_size_range
            self.grid_size = random.randint(min_size, max_size)

        logger.info(
            f"Initialized LevelGeneratorV3: "
            f"difficulty={difficulty.value}, grid_size={self.grid_size}"
        )

    def generate(self) -> Dict:
        """
        Generate a complete level.

        Returns:
            Dict containing:
                - grid_size: Grid dimensions
                - solution: List of tile configurations (correct state)
                - initial_state: List of scrambled tile configurations
                - path: List of (x, y) positions in the path
                - movable_count: Number of movable tiles
                - corner_count: Number of corner tiles

        Raises:
            RuntimeError: If failed to generate valid level after max attempts
        """
        max_attempts = 50

        for attempt in range(1, max_attempts + 1):
            try:
                logger.debug(f"Generation attempt {attempt}/{max_attempts}")

                # Step 1: Select power source and terminal positions
                power_pos, terminal_pos = self._select_endpoints()

                # Step 2: Find a path from power to terminal
                path = self._find_path(power_pos, terminal_pos)

                if path is None or len(path) < 3:
                    # Path too short (need at least power + 1 middle + terminal)
                    logger.debug(f"Path too short: {len(path) if path else 0} tiles")
                    continue

                # Step 3: Assign sprites and rotations based on path geometry
                solution_tiles = self._create_solution_tiles(path)

                # Step 4: Validate difficulty requirements
                movable_count = sum(1 for t in solution_tiles if t.get('is_clickable', False))
                corner_count = sum(1 for t in solution_tiles if t.get('type') == 'corner')

                if not self._validate_difficulty(movable_count, corner_count):
                    logger.debug(
                        f"Failed difficulty validation: "
                        f"movable={movable_count}, corners={corner_count}"
                    )
                    continue

                # Step 5: Create scrambled initial state
                initial_state = self._create_scrambled_state(solution_tiles, movable_count)

                # Step 6: Add empty tiles for all non-path positions
                solution_tiles_with_empty = self._add_empty_tiles(solution_tiles, path)
                initial_state_with_empty = self._add_empty_tiles(initial_state, path)

                logger.info(
                    f"Level generated successfully: "
                    f"grid={self.grid_size}x{self.grid_size}, "
                    f"path_length={len(path)}, "
                    f"movable={movable_count}, "
                    f"corners={corner_count}"
                )

                return {
                    'grid_size': self.grid_size,
                    'solution': solution_tiles_with_empty,
                    'initial_state': initial_state_with_empty,
                    'path': path,
                    'movable_count': movable_count,
                    'corner_count': corner_count
                }

            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                continue

        raise RuntimeError(
            f"Failed to generate valid level after {max_attempts} attempts. "
            f"Try adjusting difficulty settings or grid size."
        )

    def _select_endpoints(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Select random positions for power source and terminal.

        Ensures they are not adjacent (need at least 1 tile between them).

        Returns:
            Tuple of (power_pos, terminal_pos) where each is (x, y)
        """
        while True:
            power_x = random.randint(0, self.grid_size - 1)
            power_y = random.randint(0, self.grid_size - 1)

            terminal_x = random.randint(0, self.grid_size - 1)
            terminal_y = random.randint(0, self.grid_size - 1)

            # Check Manhattan distance (must be at least 2 to have 1 tile between)
            distance = abs(power_x - terminal_x) + abs(power_y - terminal_y)

            if distance >= 2:
                return (power_x, power_y), (terminal_x, terminal_y)

    def _find_path(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find a path from start to end using DFS.

        Does NOT find shortest path - finds any valid path.
        This creates more interesting puzzles.

        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)

        Returns:
            List of (x, y) positions forming the path, or None if no path found
        """
        visited: Set[Tuple[int, int]] = set()
        path: List[Tuple[int, int]] = []

        def dfs(pos: Tuple[int, int]) -> bool:
            """DFS helper function."""
            if pos == end:
                path.append(pos)
                return True

            if pos in visited:
                return False

            visited.add(pos)
            path.append(pos)

            # Try all four directions in random order
            directions = list(Direction)
            random.shuffle(directions)

            for direction in directions:
                dx, dy = direction.value
                next_x = pos[0] + dx
                next_y = pos[1] + dy
                next_pos = (next_x, next_y)

                # Check bounds
                if not (0 <= next_x < self.grid_size and 0 <= next_y < self.grid_size):
                    continue

                # Check not visited
                if next_pos in visited:
                    continue

                # Recursively explore
                if dfs(next_pos):
                    return True

            # Backtrack
            path.pop()
            return False

        if dfs(start):
            return path
        else:
            return None

    def _create_solution_tiles(self, path: List[Tuple[int, int]]) -> List[Dict]:
        """
        Create solution tiles based on path geometry.

        Implements the user's algorithm for determining sprite and rotation
        based on previous and next tile positions.

        Args:
            path: List of (x, y) positions in the path

        Returns:
            List of tile configuration dictionaries
        """
        tiles = []

        # Process each tile in the path
        for i in range(len(path)):
            pos = path[i]
            x, y = pos

            if i == 0:
                # Power source (start)
                next_pos = path[i + 1]
                rotation = self._get_power_rotation(pos, next_pos)

                tiles.append({
                    'x': x,
                    'y': y,
                    'type': 'power_source',
                    'rotation': rotation,
                    'is_clickable': False
                })

            elif i == len(path) - 1:
                # Terminal (end)
                prev_pos = path[i - 1]
                rotation = self._get_terminal_rotation(prev_pos, pos)

                tiles.append({
                    'x': x,
                    'y': y,
                    'type': 'terminal',
                    'rotation': rotation,
                    'is_clickable': False
                })

            else:
                # Middle tile - use user's algorithm
                prev_pos = path[i - 1]
                next_pos = path[i + 1]

                tile_type, rotation, accepted_rotations = self._determine_tile_config(
                    prev_pos, pos, next_pos
                )

                tiles.append({
                    'x': x,
                    'y': y,
                    'type': tile_type,
                    'rotation': rotation,
                    'is_clickable': True,
                    'accepted_rotations': accepted_rotations
                })

        return tiles

    def _determine_tile_config(
        self,
        prev_pos: Tuple[int, int],
        cur_pos: Tuple[int, int],
        next_pos: Tuple[int, int]
    ) -> Tuple[str, int, List[int]]:
        """
        Determine tile type, rotation, and accepted rotations.

        Implements user's algorithm logic based on relative positions.

        Screen coordinate system: x-right is positive, y-down is positive
        - prev_x < cur_x: previous is to the LEFT
        - prev_x > cur_x: previous is to the RIGHT
        - prev_y < cur_y: previous is ABOVE (UP)
        - prev_y > cur_y: previous is BELOW (DOWN)

        Args:
            prev_pos: Previous tile position (x, y)
            cur_pos: Current tile position (x, y)
            next_pos: Next tile position (x, y)

        Returns:
            Tuple of (tile_type, rotation, accepted_rotations)
        """
        prev_x, prev_y = prev_pos
        cur_x, cur_y = cur_pos
        next_x, next_y = next_pos

        # Case 1: Previous tile is ABOVE current (prev_y < cur_y)
        if cur_x == prev_x and prev_y < cur_y:
            if next_x > cur_x and cur_y == next_y:
                # Next is RIGHT: connect top and right -> 0° corner
                return 'corner', 0, [0]
            elif cur_x == next_x and next_y > cur_y:
                # Next is DOWN: connect top and bottom -> 90° or 270° straight
                return 'straight', 90, [90, 270]
            elif next_x < cur_x and cur_y == next_y:
                # Next is LEFT: connect top and left -> 270° corner
                return 'corner', 270, [270]
            else:
                raise ValueError(f"Invalid path geometry: prev={prev_pos}, cur={cur_pos}, next={next_pos}")

        # Case 2: Previous tile is to the RIGHT (prev_x > cur_x)
        elif prev_x > cur_x and cur_y == prev_y:
            if cur_x == next_x and next_y > cur_y:
                # Next is DOWN: connect right and down -> 90° corner
                return 'corner', 90, [90]
            elif next_x < cur_x and cur_y == next_y:
                # Next is LEFT: connect right and left -> 0° or 180° straight
                return 'straight', 0, [0, 180]
            elif cur_x == next_x and next_y < cur_y:
                # Next is UP: connect right and top -> 0° corner
                return 'corner', 0, [0]
            else:
                raise ValueError(f"Invalid path geometry: prev={prev_pos}, cur={cur_pos}, next={next_pos}")

        # Case 3: Previous tile is BELOW current (prev_y > cur_y)
        elif cur_x == prev_x and prev_y > cur_y:
            if next_x < cur_x and cur_y == next_y:
                # Next is LEFT: connect bottom and left -> 180° corner
                return 'corner', 180, [180]
            elif cur_x == next_x and next_y < cur_y:
                # Next is UP: connect bottom and top -> 90° or 270° straight
                return 'straight', 90, [90, 270]
            elif next_x > cur_x and cur_y == next_y:
                # Next is RIGHT: connect bottom and right -> 90° corner
                return 'corner', 90, [90]
            else:
                raise ValueError(f"Invalid path geometry: prev={prev_pos}, cur={cur_pos}, next={next_pos}")

        # Case 4: Previous tile is to the LEFT (prev_x < cur_x)
        elif prev_x < cur_x and cur_y == prev_y:
            if cur_x == next_x and next_y < cur_y:
                # Next is UP: connect left and top -> 270° corner
                return 'corner', 270, [270]
            elif next_x > cur_x and cur_y == next_y:
                # Next is RIGHT: connect left and right -> 0° or 180° straight
                return 'straight', 0, [0, 180]
            elif cur_x == next_x and next_y > cur_y:
                # Next is DOWN: connect left and bottom -> 180° corner
                return 'corner', 180, [180]
            else:
                raise ValueError(f"Invalid path geometry: prev={prev_pos}, cur={cur_pos}, next={next_pos}")

        else:
            raise ValueError(f"Invalid path geometry: prev={prev_pos}, cur={cur_pos}, next={next_pos}")

    def _get_power_rotation(
        self,
        power_pos: Tuple[int, int],
        next_pos: Tuple[int, int]
    ) -> int:
        """
        Get rotation for power source based on where it connects.

        Power source base (0°) exits to the right (EAST).

        Args:
            power_pos: Power source position (x, y)
            next_pos: Next tile position (x, y)

        Returns:
            Rotation angle in degrees
        """
        px, py = power_pos
        nx, ny = next_pos

        if nx > px:  # Next is right
            return 0
        elif ny > py:  # Next is down
            return 90
        elif nx < px:  # Next is left
            return 180
        elif ny < py:  # Next is up
            return 270
        else:
            raise ValueError(f"Invalid power connection: power={power_pos}, next={next_pos}")

    def _get_terminal_rotation(
        self,
        prev_pos: Tuple[int, int],
        terminal_pos: Tuple[int, int]
    ) -> int:
        """
        Get rotation for terminal based on where it connects from.

        Terminal base (0°) accepts from the left (WEST).

        Args:
            prev_pos: Previous tile position (x, y)
            terminal_pos: Terminal position (x, y)

        Returns:
            Rotation angle in degrees
        """
        px, py = prev_pos
        tx, ty = terminal_pos

        if px < tx:  # Previous is left
            return 0
        elif py < ty:  # Previous is up
            return 90
        elif px > tx:  # Previous is right
            return 180
        elif py > ty:  # Previous is down
            return 270
        else:
            raise ValueError(f"Invalid terminal connection: prev={prev_pos}, terminal={terminal_pos}")

    def _validate_difficulty(self, movable_count: int, corner_count: int) -> bool:
        """
        Validate that the level meets difficulty requirements.

        Args:
            movable_count: Number of movable tiles
            corner_count: Number of corner tiles

        Returns:
            True if level meets requirements, False otherwise
        """
        # Check movable tile count
        if not (self.config.min_movable_tiles <= movable_count <= self.config.max_movable_tiles):
            return False

        # Check corner count
        if not (self.config.min_corners <= corner_count <= self.config.max_corners):
            return False

        return True

    def _create_scrambled_state(
        self,
        solution_tiles: List[Dict],
        movable_count: int
    ) -> List[Dict]:
        """
        Create scrambled initial state by rotating tiles.

        Ensures that the required percentage of tiles need rotation.

        Args:
            solution_tiles: List of solution tile configurations
            movable_count: Number of movable tiles

        Returns:
            List of scrambled tile configurations (only clickable tiles)
        """
        import math

        scrambled = []

        # Calculate how many tiles must be scrambled (use ceiling to ensure minimum ratio)
        min_scrambled = max(1, math.ceil(movable_count * self.config.scramble_ratio))

        # Get only clickable tiles
        clickable_tiles = [
            tile for tile in solution_tiles
            if tile.get('is_clickable', False)
        ]

        # Randomly select which tiles to scramble
        num_to_scramble = min(min_scrambled, len(clickable_tiles))
        scramble_indices = set(random.sample(range(len(clickable_tiles)), num_to_scramble))

        for i, tile in enumerate(clickable_tiles):
            if i in scramble_indices:
                # Scramble this tile - choose an invalid rotation
                accepted = tile.get('accepted_rotations', [tile['rotation']])

                # Get all possible rotations
                all_rotations = [0, 90, 180, 270]

                # Remove accepted rotations
                invalid_rotations = [r for r in all_rotations if r not in accepted]

                if invalid_rotations:
                    # Choose a random invalid rotation
                    rotation = random.choice(invalid_rotations)
                else:
                    # If all rotations are valid (shouldn't happen), just rotate 90°
                    rotation = (tile['rotation'] + 90) % 360
            else:
                # Keep correct rotation
                rotation = tile['rotation']

            scrambled.append({
                'x': tile['x'],
                'y': tile['y'],
                'rotation': rotation
            })

        return scrambled

    def _add_empty_tiles(
        self,
        tiles: List[Dict],
        path: List[Tuple[int, int]]
    ) -> List[Dict]:
        """
        Add empty tiles for all non-path positions in the grid.

        Args:
            tiles: List of existing tile configurations
            path: List of (x, y) positions in the path

        Returns:
            List of tile configurations including empty tiles
        """
        # Create a set of path positions for fast lookup
        path_positions = set(path)

        # Create result list with existing tiles
        result = list(tiles)

        # Add empty tiles for all non-path positions
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (x, y) not in path_positions:
                    result.append({
                        'x': x,
                        'y': y,
                        'type': 'empty',
                        'rotation': 0,
                        'is_clickable': False
                    })

        return result
