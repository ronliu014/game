"""
Level Manager Module

This module provides the LevelManager class for managing level state and progression.
It coordinates between LevelLoader, GridManager, and ConnectivityChecker.

Classes:
    LevelManager: Manages level state, move counting, and win condition checking

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from typing import Optional, List, Tuple
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

        A level is completed when there is a valid path from power source
        to terminal. Updates completion status if level is completed.

        Returns:
            True if level is completed, False otherwise

        Example:
            >>> manager.load_level("data/levels/level_001.json")
            >>> manager.check_win_condition()
            False
            >>> # ... rotate tiles to complete circuit ...
            >>> manager.check_win_condition()
            True
        """
        if self._grid is None or self._connectivity_checker is None:
            logger.warning("Cannot check win condition: no level loaded")
            return False

        is_connected = self._connectivity_checker.check_connectivity(self._grid)

        if is_connected and not self._is_completed:
            self._is_completed = True
            logger.info(
                f"Level completed: {self._current_level_id} "
                f"(Moves: {self._move_count})"
            )

        return is_connected

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
