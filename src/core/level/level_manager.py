"""
Level Manager Module

This module provides the LevelManager class for managing level state and progression.
It coordinates between LevelLoader, GridManager, and ConnectivityChecker.

Classes:
    LevelManager: Manages level state, move counting, and win condition checking

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from typing import Optional, List, Tuple, Dict, Any
import logging

from src.core.grid.grid_manager import GridManager
from src.core.grid.tile import Tile
from src.core.circuit.connectivity_checker import ConnectivityChecker
from src.core.level.level_loader import LevelLoader, LevelData

# Configure logger
logger = logging.getLogger(__name__)


class LevelManager:
    """
    Manages level state and progression.

    Coordinates between LevelLoader, GridManager, and ConnectivityChecker
    to provide level management functionality including loading, resetting,
    move tracking, and win condition checking.

    Attributes:
        _level_loader: LevelLoader instance for loading level data
        _current_level_id: ID of currently loaded level
        _current_filepath: Filepath of currently loaded level
        _grid: GridManager instance for current level
        _connectivity_checker: ConnectivityChecker instance
        _move_count: Number of moves made in current level
        _is_completed: Whether current level is completed
        _level_data: Parsed level data

    Example:
        >>> loader = LevelLoader()
        >>> manager = LevelManager(loader)
        >>> manager.load_level("data/levels/level_001.json")
        True
        >>> manager.rotate_tile(1, 0)
        True
        >>> manager.get_move_count()
        1
        >>> manager.check_win_condition()
        False
    """

    def __init__(self, level_loader: LevelLoader) -> None:
        """
        Initialize LevelManager.

        Args:
            level_loader: LevelLoader instance for loading level data

        Raises:
            ValueError: If level_loader is None
        """
        if level_loader is None:
            raise ValueError("level_loader cannot be None")

        self._level_loader = level_loader
        self._current_level_id: Optional[str] = None
        self._current_filepath: Optional[str] = None
        self._grid: Optional[GridManager] = None
        self._connectivity_checker: Optional[ConnectivityChecker] = None
        self._move_count: int = 0
        self._is_completed: bool = False
        self._level_data: Optional[LevelData] = None

        logger.info("LevelManager initialized")

    def load_level(self, filepath: str) -> bool:
        """
        Load a level from file.

        Args:
            filepath: Path to level JSON file

        Returns:
            True if level loaded successfully, False otherwise

        Example:
            >>> manager.load_level("data/levels/level_001.json")
            True
        """
        if not filepath:
            logger.error("Cannot load level: filepath is empty")
            return False

        logger.info(f"Loading level from: {filepath}")

        # Load level data
        level_data = self._level_loader.get_level_data(filepath)
        if level_data is None:
            logger.error(f"Failed to load level data from: {filepath}")
            return False

        # Create grid from level data
        grid = self._level_loader.load_level(filepath)
        if grid is None:
            logger.error(f"Failed to create grid from level data: {filepath}")
            return False

        # Initialize components
        self._level_data = level_data
        self._current_level_id = level_data.level_id
        self._current_filepath = filepath
        self._grid = grid
        self._connectivity_checker = ConnectivityChecker()
        self._move_count = 0
        self._is_completed = False

        logger.info(
            f"Level loaded successfully: {level_data.name} "
            f"(ID: {level_data.level_id}, Size: {level_data.grid_size}x{level_data.grid_size})"
        )

        return True

    def load_generated_level(
        self,
        difficulty: str = "normal",
        grid_size: Optional[int] = None,
        level_number: int = 1
    ) -> bool:
        """
        Load a procedurally generated level with difficulty support.

        Uses the V3 generator which implements the user's algorithm specification.

        Args:
            difficulty: Difficulty level ("easy", "normal", "hard", "hell")
            grid_size: Optional fixed grid size (overrides difficulty config)
            level_number: Level number for display purposes

        Returns:
            True if level generated and loaded successfully

        Example:
            >>> manager.load_generated_level(difficulty="normal")
            True
            >>> manager.load_generated_level(difficulty="hard", grid_size=7)
            True
        """
        from src.core.level.level_generator_v3 import LevelGeneratorV3
        from src.core.level.difficulty_config import DifficultyLevel

        # Convert string to DifficultyLevel enum
        try:
            difficulty_enum = DifficultyLevel(difficulty.lower())
        except ValueError:
            logger.error(f"Invalid difficulty: {difficulty}, defaulting to NORMAL")
            difficulty_enum = DifficultyLevel.NORMAL

        logger.info(
            f"Generating level #{level_number}: difficulty={difficulty_enum.value}, "
            f"grid_size={grid_size or 'auto'}"
        )

        # Generate level using V3 generator (implements user's algorithm)
        generator = LevelGeneratorV3(
            difficulty=difficulty_enum,
            grid_size=grid_size
        )

        try:
            generated = generator.generate()
        except RuntimeError as e:
            logger.error(f"Failed to generate level: {e}")
            return False

        # Create LevelData from generated data
        difficulty_names = {
            "easy": "简单",
            "normal": "普通",
            "hard": "困难",
            "hell": "地狱"
        }
        difficulty_display = difficulty_names.get(difficulty_enum.value, difficulty_enum.value)

        level_data = LevelData(
            level_id=f"generated_{level_number}",
            version="1.0",
            name=f"关卡 #{level_number} ({difficulty_display})",
            difficulty=list(DifficultyLevel).index(difficulty_enum) + 1,
            grid_size=generated['grid_size'],
            solution_tiles=generated['solution'],
            rotated_tiles=generated['initial_state']
        )

        # Create grid using LevelLoader's internal method
        grid = self._level_loader._create_grid(level_data)
        if grid is None:
            logger.error("Failed to create grid from generated level")
            return False

        # Initialize components
        self._level_data = level_data
        self._current_level_id = level_data.level_id
        self._current_filepath = None  # No file for generated levels
        self._grid = grid
        self._connectivity_checker = ConnectivityChecker()
        self._move_count = 0
        self._is_completed = False

        logger.info(
            f"Generated level loaded: {level_data.name} "
            f"(Grid: {generated['grid_size']}x{generated['grid_size']}, "
            f"Path length: {len(generated['path'])}, "
            f"Movable: {generated['movable_count']}, "
            f"Corners: {generated['corner_count']})"
        )

        return True

    def reset_level(self) -> bool:
        """
        Reset current level to initial state.

        Resets the grid to its initial configuration and resets move count.
        Does not reset completion status.

        Returns:
            True if level reset successfully, False if no level loaded

        Example:
            >>> manager.load_level("data/levels/level_001.json")
            >>> manager.rotate_tile(1, 0)
            >>> manager.reset_level()
            True
            >>> manager.get_move_count()
            0
        """
        if self._grid is None:
            logger.warning("Cannot reset level: no level loaded")
            return False

        logger.info(f"Resetting level: {self._current_level_id}")

        self._grid.reset_grid()
        self._move_count = 0

        logger.info(f"Level reset successfully: {self._current_level_id}")

        return True

    def rotate_tile(self, x: int, y: int) -> bool:
        """
        Rotate a tile at specified coordinates.

        Increments move count if rotation is successful.
        Cannot rotate if level is already completed.

        Args:
            x: X coordinate of tile
            y: Y coordinate of tile

        Returns:
            True if tile rotated successfully, False otherwise

        Example:
            >>> manager.load_level("data/levels/level_001.json")
            >>> manager.rotate_tile(1, 0)
            True
            >>> manager.get_move_count()
            1
        """
        if self._grid is None:
            logger.warning("Cannot rotate tile: no level loaded")
            return False

        if self._is_completed:
            logger.warning("Cannot rotate tile: level already completed")
            return False

        success = self._grid.rotate_tile(x, y)

        if success:
            self._move_count += 1
            logger.debug(f"Tile rotated at ({x}, {y}), move count: {self._move_count}")
        else:
            logger.debug(f"Failed to rotate tile at ({x}, {y})")

        return success

    def check_win_condition(self) -> bool:
        """
        Check if current level is completed.

        A level is completed when all clickable tiles match their solution
        rotation angles. For straight tiles, equivalent rotations are accepted:
        - 0° is equivalent to 180°
        - 90° is equivalent to 270°

        Returns:
            True if level is completed, False otherwise

        Example:
            >>> manager.load_level("data/levels/level_001.json")
            >>> manager.check_win_condition()
            False
            >>> # ... rotate tiles to match solution ...
            >>> manager.check_win_condition()
            True
        """
        if self._grid is None or self._level_data is None:
            logger.warning("Cannot check win condition: no level loaded")
            return False

        # Check if all clickable tiles match their solution rotation
        is_match = self._check_rotation_match()

        if is_match and not self._is_completed:
            self._is_completed = True
            logger.info(
                f"Level completed: {self._current_level_id} "
                f"(Moves: {self._move_count})"
            )

        return is_match

    def _check_rotation_match(self) -> bool:
        """
        Check if all clickable tiles match their accepted rotations.

        Each tile in the solution can have an accepted_rotations list that
        defines which rotation angles are considered correct. This allows
        level designers full flexibility in defining puzzle solutions.

        Returns:
            True if all rotations match, False otherwise
        """
        if self._grid is None or self._level_data is None:
            return False

        # Build solution map: (x, y) -> accepted_rotations
        solution_map: Dict[tuple, list] = {}
        for tile_data in self._level_data.solution_tiles:
            x = tile_data.get('x')
            y = tile_data.get('y')
            is_clickable = tile_data.get('is_clickable', False)
            accepted_rotations = tile_data.get('accepted_rotations')

            if is_clickable and x is not None and y is not None:
                # If accepted_rotations not specified, default to single rotation
                if accepted_rotations is None:
                    accepted_rotations = [tile_data.get('rotation', 0)]
                solution_map[(x, y)] = accepted_rotations

        # Check each clickable tile
        for pos, accepted_rotations in solution_map.items():
            x, y = pos
            tile = self._grid.get_tile(x, y)

            if tile is None:
                logger.debug(f"Tile at ({x}, {y}) not found")
                return False

            current_rotation = tile.rotation

            # Check if current rotation is in accepted list
            if not self._is_rotation_accepted(current_rotation, accepted_rotations):
                logger.debug(
                    f"Tile at ({x}, {y}) rotation mismatch: "
                    f"current={current_rotation}°, accepted={accepted_rotations}"
                )
                return False

        logger.debug("All tiles match accepted rotations")
        return True

    def _is_rotation_accepted(self, current: int, accepted_rotations: list) -> bool:
        """
        Check if current rotation is in the list of accepted rotations.

        Args:
            current: Current rotation angle
            accepted_rotations: List of accepted rotation angles

        Returns:
            True if current rotation is accepted, False otherwise
        """
        # Normalize current angle to 0-359 range
        current = current % 360

        # Check if current rotation is in accepted list
        for accepted in accepted_rotations:
            if current == (accepted % 360):
                return True

        return False

    def get_move_count(self) -> int:
        """
        Get current move count.

        Returns:
            Number of moves made in current level

        Example:
            >>> manager.get_move_count()
            5
        """
        return self._move_count

    def is_level_completed(self) -> bool:
        """
        Check if level is marked as completed.

        Returns:
            True if level is completed, False otherwise

        Example:
            >>> manager.is_level_completed()
            False
        """
        return self._is_completed

    def get_grid(self) -> Optional[GridManager]:
        """
        Get current grid manager.

        Returns:
            GridManager instance if level loaded, None otherwise

        Example:
            >>> grid = manager.get_grid()
            >>> if grid:
            ...     tile = grid.get_tile(0, 0)
        """
        return self._grid

    def get_connected_path(self) -> Optional[List[Tile]]:
        """
        Get the connected path from power source to terminal.

        Returns:
            List of tiles in the connected path, or None if no path exists

        Example:
            >>> path = manager.get_connected_path()
            >>> if path:
            ...     print(f"Path length: {len(path)}")
        """
        if self._grid is None or self._connectivity_checker is None:
            logger.warning("Cannot get connected path: no level loaded")
            return None

        return self._connectivity_checker.find_path(self._grid)

    def get_current_level_id(self) -> Optional[str]:
        """
        Get current level ID.

        Returns:
            Level ID if level loaded, None otherwise

        Example:
            >>> manager.get_current_level_id()
            '001'
        """
        return self._current_level_id

    def get_level_data(self) -> Optional[LevelData]:
        """
        Get current level data.

        Returns:
            LevelData instance if level loaded, None otherwise

        Example:
            >>> data = manager.get_level_data()
            >>> if data:
            ...     print(f"Level: {data.name}, Difficulty: {data.difficulty}")
        """
        return self._level_data

    def get_grid_size(self) -> Optional[int]:
        """
        Get current grid size.

        Returns:
            Grid size if level loaded, None otherwise

        Example:
            >>> manager.get_grid_size()
            4
        """
        if self._grid is None:
            return None
        return self._grid.grid_size

    def has_level_loaded(self) -> bool:
        """
        Check if a level is currently loaded.

        Returns:
            True if level is loaded, False otherwise

        Example:
            >>> manager.has_level_loaded()
            False
            >>> manager.load_level("data/levels/level_001.json")
            >>> manager.has_level_loaded()
            True
        """
        return self._grid is not None

    def reload_level(self) -> bool:
        """
        Reload current level from file.

        Useful for resetting level to original state including
        any file changes.

        Returns:
            True if level reloaded successfully, False if no level loaded

        Example:
            >>> manager.reload_level()
            True
        """
        if self._current_filepath is None:
            logger.warning("Cannot reload level: no level loaded")
            return False

        logger.info(f"Reloading level from: {self._current_filepath}")

        return self.load_level(self._current_filepath)
