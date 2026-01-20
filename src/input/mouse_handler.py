"""
Mouse Handler Module

This module provides the MouseHandler class for mouse-specific operations
including coordinate transformations for grid-based games.

Classes:
    MouseHandler: Handler for mouse operations and coordinate transformations

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import Tuple, Optional
import pygame

from src.config.constants import TILE_SIZE, TILE_PADDING

# Configure logger
logger = logging.getLogger(__name__)


class MouseHandler:
    """
    Handler for mouse operations and coordinate transformations.

    Provides utilities for converting screen coordinates to grid coordinates
    and detecting clicks on grid tiles.

    Attributes:
        _grid_offset_x: X offset of the grid on screen
        _grid_offset_y: Y offset of the grid on screen
        _tile_size: Size of each tile in pixels
        _tile_padding: Padding between tiles in pixels

    Example:
        >>> handler = MouseHandler(grid_offset_x=100, grid_offset_y=100)
        >>> grid_x, grid_y = handler.screen_to_grid(250, 250)
        >>> print(f"Clicked on grid position ({grid_x}, {grid_y})")
    """

    def __init__(
        self,
        grid_offset_x: int = 0,
        grid_offset_y: int = 0,
        tile_size: int = TILE_SIZE,
        tile_padding: int = TILE_PADDING
    ) -> None:
        """
        Initialize the MouseHandler.

        Args:
            grid_offset_x: X offset of the grid on screen
            grid_offset_y: Y offset of the grid on screen
            tile_size: Size of each tile in pixels
            tile_padding: Padding between tiles in pixels
        """
        self._grid_offset_x = grid_offset_x
        self._grid_offset_y = grid_offset_y
        self._tile_size = tile_size
        self._tile_padding = tile_padding

        logger.debug(
            f"MouseHandler initialized: offset=({grid_offset_x}, {grid_offset_y}), "
            f"tile_size={tile_size}, padding={tile_padding}"
        )

    def screen_to_grid(self, screen_x: int, screen_y: int) -> Optional[Tuple[int, int]]:
        """
        Convert screen coordinates to grid coordinates.

        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate

        Returns:
            (grid_x, grid_y) tuple or None if outside grid

        Example:
            >>> pos = handler.screen_to_grid(250, 250)
            >>> if pos:
            ...     grid_x, grid_y = pos
        """
        # Adjust for grid offset
        rel_x = screen_x - self._grid_offset_x
        rel_y = screen_y - self._grid_offset_y

        # Check if within grid bounds
        if rel_x < 0 or rel_y < 0:
            return None

        # Calculate tile size including padding
        tile_total_size = self._tile_size + self._tile_padding

        # Calculate grid position
        grid_x = rel_x // tile_total_size
        grid_y = rel_y // tile_total_size

        # Check if click is on padding (between tiles)
        tile_local_x = rel_x % tile_total_size
        tile_local_y = rel_y % tile_total_size

        if tile_local_x >= self._tile_size or tile_local_y >= self._tile_size:
            # Click is on padding
            return None

        return (grid_x, grid_y)

    def grid_to_screen(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        Convert grid coordinates to screen coordinates (top-left of tile).

        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate

        Returns:
            (screen_x, screen_y) tuple

        Example:
            >>> screen_x, screen_y = handler.grid_to_screen(2, 3)
        """
        tile_total_size = self._tile_size + self._tile_padding

        screen_x = self._grid_offset_x + grid_x * tile_total_size
        screen_y = self._grid_offset_y + grid_y * tile_total_size

        return (screen_x, screen_y)

    def get_tile_rect(self, grid_x: int, grid_y: int) -> pygame.Rect:
        """
        Get the screen rectangle for a grid tile.

        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate

        Returns:
            pygame.Rect for the tile

        Example:
            >>> rect = handler.get_tile_rect(2, 3)
            >>> pygame.draw.rect(screen, (255, 0, 0), rect, 2)
        """
        screen_x, screen_y = self.grid_to_screen(grid_x, grid_y)
        return pygame.Rect(screen_x, screen_y, self._tile_size, self._tile_size)

    def is_point_in_tile(
        self,
        screen_x: int,
        screen_y: int,
        grid_x: int,
        grid_y: int
    ) -> bool:
        """
        Check if a screen point is within a specific grid tile.

        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate
            grid_x: Grid X coordinate to check
            grid_y: Grid Y coordinate to check

        Returns:
            True if point is in tile, False otherwise

        Example:
            >>> if handler.is_point_in_tile(250, 250, 2, 2):
            ...     print("Point is in tile (2, 2)")
        """
        tile_rect = self.get_tile_rect(grid_x, grid_y)
        return tile_rect.collidepoint(screen_x, screen_y)

    def set_grid_offset(self, offset_x: int, offset_y: int) -> None:
        """
        Set the grid offset on screen.

        Args:
            offset_x: New X offset
            offset_y: New Y offset

        Example:
            >>> handler.set_grid_offset(150, 150)
        """
        self._grid_offset_x = offset_x
        self._grid_offset_y = offset_y
        logger.debug(f"Grid offset set to ({offset_x}, {offset_y})")

    def get_grid_offset(self) -> Tuple[int, int]:
        """
        Get the current grid offset.

        Returns:
            (offset_x, offset_y) tuple

        Example:
            >>> offset_x, offset_y = handler.get_grid_offset()
        """
        return (self._grid_offset_x, self._grid_offset_y)

    def set_tile_size(self, tile_size: int, tile_padding: int) -> None:
        """
        Set the tile size and padding.

        Args:
            tile_size: New tile size in pixels
            tile_padding: New padding in pixels

        Example:
            >>> handler.set_tile_size(64, 2)
        """
        self._tile_size = tile_size
        self._tile_padding = tile_padding
        logger.debug(f"Tile size set to {tile_size}, padding to {tile_padding}")

    def get_tile_size(self) -> Tuple[int, int]:
        """
        Get the current tile size and padding.

        Returns:
            (tile_size, tile_padding) tuple

        Example:
            >>> tile_size, padding = handler.get_tile_size()
        """
        return (self._tile_size, self._tile_padding)
