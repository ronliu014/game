"""
Level Generator Module

This module provides procedural level generation for the Circuit Repair Game.
It generates random but solvable puzzles with configurable difficulty.

Classes:
    LevelGenerator: Generates random circuit puzzles

Author: Circuit Repair Game Team
Date: 2026-01-21
"""

import random
from typing import List, Tuple, Dict, Optional, Set
from enum import Enum

from src.config.constants import Direction
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class PathDirection(Enum):
    """Direction of path movement in grid coordinates."""
    NORTH = (-1, 0)  # row-1, up
    EAST = (0, 1)    # col+1, right
    SOUTH = (1, 0)   # row+1, down
    WEST = (0, -1)   # col-1, left


class LevelGenerator:
    """
    Procedural level generator for circuit puzzles.

    Generates random but solvable puzzles by:
    1. Randomly placing power source and terminal
    2. Finding a random path between them
    3. Placing appropriate tiles (straight/corner) along the path
    4. Calculating correct rotations based on path directions
    5. Scrambling tiles to create the puzzle

    Attributes:
        grid_size: Size of the grid (N for NxN)
        min_path_length: Minimum number of tiles in the path

    Example:
        >>> generator = LevelGenerator(grid_size=5, min_path_length=6)
        >>> level_data = generator.generate()
        >>> print(f"Generated level with {len(level_data['path'])} tiles")
    """

    def __init__(self, grid_size: int = 4, min_path_length: int = 5):
        """
        Initialize the level generator.

        Args:
            grid_size: Size of the grid (N for NxN grid)
            min_path_length: Minimum number of movable tiles in path
        """
        self.grid_size = grid_size
        self.min_path_length = min_path_length

        logger.info(
            f"LevelGenerator initialized: grid_size={grid_size}, "
            f"min_path_length={min_path_length}"
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

        Example:
            >>> generator = LevelGenerator(grid_size=4, min_path_length=5)
            >>> level = generator.generate()
            >>> print(level['grid_size'])
            4
        """
        logger.info("Generating new level...")

        # Step 1: Choose random start and end positions
        power_pos, terminal_pos = self._choose_endpoints()
        logger.debug(f"Endpoints: power={power_pos}, terminal={terminal_pos}")

        # Step 2: Find a random path between them
        path = self._find_random_path(power_pos, terminal_pos)

        if path is None or len(path) < self.min_path_length:
            logger.warning(
                f"Path too short ({len(path) if path else 0} < {self.min_path_length}), "
                "retrying..."
            )
            return self.generate()  # Retry

        logger.debug(f"Generated path with {len(path)} tiles")

        # Step 3: Create tile configurations based on path
        solution_tiles = self._create_tiles_from_path(path, power_pos, terminal_pos)

        # Step 4: Create scrambled initial state
        initial_state = self._create_scrambled_state(solution_tiles)

        logger.info(f"Level generated successfully with {len(path)} tiles in path")

        return {
            'solution': solution_tiles,
            'initial_state': initial_state,
            'path': path,
            'grid_size': self.grid_size
        }

    def _choose_endpoints(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Randomly choose positions for power source and terminal.

        Ensures they are not adjacent to increase difficulty.

        Returns:
            Tuple of (power_position, terminal_position)
        """
        # Choose random positions
        power_pos = (
            random.randint(0, self.grid_size - 1),
            random.randint(0, self.grid_size - 1)
        )

        # Choose terminal position (not adjacent to power)
        while True:
            terminal_pos = (
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1)
            )

            # Check if positions are different and not adjacent
            dx = abs(power_pos[0] - terminal_pos[0])
            dy = abs(power_pos[1] - terminal_pos[1])

            if (dx + dy) >= 2:  # Manhattan distance >= 2
                break

        return power_pos, terminal_pos

    def _find_random_path(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find a random path from start to end using random walk with backtracking.

        This is NOT A* - we want varied paths, not shortest paths.
        Prefers straight lines over corners to create more natural circuits.

        Args:
            start: Starting position (x, y)
            end: Ending position (x, y)

        Returns:
            List of positions forming the path, or None if no path found
        """
        # Use random DFS to find a path
        visited = set()
        path = []

        def dfs(pos: Tuple[int, int], prev_dir: Optional[PathDirection] = None) -> bool:
            """Recursive DFS with randomization and direction preference."""
            if pos == end:
                return True

            visited.add(pos)
            path.append(pos)

            # Get neighbors
            neighbors = self._get_neighbors(pos)

            # Sort neighbors: prefer continuing in same direction (70% chance)
            if prev_dir and random.random() < 0.7:
                # Try to continue in same direction first
                dx, dy = prev_dir.value
                straight_pos = (pos[0] + dx, pos[1] + dy)
                if straight_pos in neighbors and straight_pos not in visited:
                    # Try straight first
                    if dfs(straight_pos, prev_dir):
                        return True

            # Otherwise try random neighbors
            random.shuffle(neighbors)
            for next_pos in neighbors:
                if next_pos not in visited:
                    # Calculate direction to next position
                    next_dir = self._get_direction(pos, next_pos)
                    if dfs(next_pos, next_dir):
                        return True

            # Backtrack
            path.pop()
            return False

        if dfs(start):
            path.append(end)  # Add terminal position
            return path

        return None

    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get valid neighboring positions.

        Args:
            pos: Current position (x, y)

        Returns:
            List of valid neighbor positions
        """
        x, y = pos
        neighbors = []

        for direction in PathDirection:
            dx, dy = direction.value
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))

        return neighbors

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
            entry_dir = self._get_direction(prev_pos, pos)
            exit_dir = self._get_direction(pos, next_pos)

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

        Terminal base (0°) accepts from WEST (exits WEST).

        Args:
            entry_dir: Direction entering terminal

        Returns:
            Rotation angle in degrees
        """
        # Terminal accepts from opposite direction of its exit
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

        Args:
            entry_dir: Direction entering the tile
            exit_dir: Direction exiting the tile

        Returns:
            Tuple of (tile_type, rotation, accepted_rotations)
        """
        # Check if it's a straight line (same or opposite directions)
        if self._is_straight_line(entry_dir, exit_dir):
            # Straight tile
            if entry_dir in [PathDirection.EAST, PathDirection.WEST]:
                # Horizontal: 0° or 180°
                return 'straight', 0, [0, 180]
            else:
                # Vertical: 90° or 270°
                return 'straight', 90, [90, 270]
        else:
            # Corner tile
            rotation = self._get_corner_rotation(entry_dir, exit_dir)
            return 'corner', rotation, [rotation]

    def _is_opposite(self, dir1: PathDirection, dir2: PathDirection) -> bool:
        """Check if two directions are opposite."""
        opposites = {
            PathDirection.NORTH: PathDirection.SOUTH,
            PathDirection.SOUTH: PathDirection.NORTH,
            PathDirection.EAST: PathDirection.WEST,
            PathDirection.WEST: PathDirection.EAST
        }
        return opposites[dir1] == dir2

    def _is_straight_line(self, dir1: PathDirection, dir2: PathDirection) -> bool:
        """Check if two directions form a straight line (same or opposite)."""
        return dir1 == dir2 or self._is_opposite(dir1, dir2)

    def _get_corner_rotation(
        self,
        entry_dir: PathDirection,
        exit_dir: PathDirection
    ) -> int:
        """
        Get rotation for corner tile based on entry and exit directions.

        Corner rotations (bidirectional):
        - 0°: NORTH↔EAST (up→right or right→up)
        - 90°: EAST↔SOUTH (right→down or down→right)
        - 180°: SOUTH↔WEST (down→left or left→down)
        - 270°: WEST↔NORTH (left→up or up→left)

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
                f"Invalid corner combination: entry={entry_dir.name}, exit={exit_dir.name}. "
                f"This should not happen - corners only connect perpendicular directions."
            )
            return 0
        return result

    def _create_scrambled_state(self, solution_tiles: List[Dict]) -> List[Dict]:
        """
        Create scrambled initial state by randomly rotating clickable tiles.

        Args:
            solution_tiles: List of solution tile configurations

        Returns:
            List of rotated tile configurations for initial state
        """
        scrambled = []

        for tile in solution_tiles:
            if tile['is_clickable']:
                # Randomly rotate (0, 90, 180, 270)
                random_rotation = random.choice([0, 90, 180, 270])

                # Ensure it's different from solution (at least 50% of the time)
                if random.random() < 0.7:  # 70% chance to scramble
                    accepted = tile.get('accepted_rotations', [tile['rotation']])
                    # Choose a rotation NOT in accepted list
                    invalid_rotations = [r for r in [0, 90, 180, 270] if r not in accepted]
                    if invalid_rotations:
                        random_rotation = random.choice(invalid_rotations)

                scrambled.append({
                    'x': tile['x'],
                    'y': tile['y'],
                    'rotation': random_rotation
                })

        return scrambled
