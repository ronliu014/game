"""
Current Flow Animation Module

This module provides the CurrentFlowAnimation class for animating electrical
current flowing through circuit tiles.

Classes:
    CurrentFlowAnimation: Animation for electrical current flow effect

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import List, Tuple

from src.rendering.animation.animator import Animator

# Configure logger
logger = logging.getLogger(__name__)


class CurrentFlowAnimation(Animator):
    """
    Animation for electrical current flow effect.

    Creates a flowing effect along a path of tiles to visualize electrical
    current flowing from power source to terminal.

    Attributes:
        path: List of (x, y) grid positions representing the current path
        current_position: Current position index in the path
        flow_speed: Speed of the flow effect (positions per second)

    Example:
        >>> path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        >>> anim = CurrentFlowAnimation(path, duration_ms=1000)
        >>> anim.start()
        >>> while anim.is_playing:
        ...     anim.update(16.67)
        ...     pos = anim.get_current_position()
        ...     print(f"Current at: {pos}")
    """

    def __init__(
        self,
        path: List[Tuple[int, int]],
        duration_ms: float = 1000,
        loop: bool = True
    ) -> None:
        """
        Initialize the current flow animation.

        Args:
            path: List of (x, y) grid positions for the current path
            duration_ms: Animation duration in milliseconds
            loop: Whether to loop the animation
        """
        super().__init__(duration_ms, loop=loop)

        self.path = path
        self.current_position = 0
        self._flow_progress = 0.0

        logger.debug(
            f"CurrentFlowAnimation created: {len(path)} tiles, "
            f"duration={duration_ms}ms, loop={loop}"
        )

    def update_animation(self, progress: float) -> None:
        """
        Update the current flow based on progress.

        Args:
            progress: Animation progress from 0.0 to 1.0
        """
        if not self.path:
            return

        # Calculate current position in path
        path_length = len(self.path)
        position_float = progress * path_length

        self.current_position = int(position_float) % path_length
        self._flow_progress = position_float - int(position_float)

    def get_current_position(self) -> Tuple[int, int]:
        """
        Get the current grid position of the flow.

        Returns:
            (x, y) grid position

        Example:
            >>> x, y = anim.get_current_position()
        """
        if not self.path:
            return (0, 0)

        return self.path[self.current_position]

    def get_flow_progress(self) -> float:
        """
        Get the progress within the current tile.

        Returns:
            Progress from 0.0 to 1.0 within current tile

        Example:
            >>> progress = anim.get_flow_progress()
        """
        return self._flow_progress

    def get_path_length(self) -> int:
        """
        Get the length of the current path.

        Returns:
            Number of tiles in the path

        Example:
            >>> length = anim.get_path_length()
        """
        return len(self.path)

    def set_path(self, path: List[Tuple[int, int]]) -> None:
        """
        Set a new path for the animation.

        Args:
            path: New list of (x, y) grid positions

        Example:
            >>> new_path = [(0, 0), (1, 0), (1, 1)]
            >>> anim.set_path(new_path)
        """
        self.path = path
        self.current_position = 0
        self._flow_progress = 0.0
        logger.debug(f"Current flow path set: {len(path)} tiles")

    def get_visible_tiles(self, trail_length: int = 3) -> List[Tuple[int, int]]:
        """
        Get the tiles that should be visible in the current flow.

        Args:
            trail_length: Number of tiles to show in the trail

        Returns:
            List of (x, y) positions for visible tiles

        Example:
            >>> visible = anim.get_visible_tiles(trail_length=3)
            >>> for x, y in visible:
            ...     draw_glow(x, y)
        """
        if not self.path:
            return []

        visible = []
        path_length = len(self.path)

        for i in range(trail_length):
            index = (self.current_position - i) % path_length
            if index >= 0:
                visible.append(self.path[index])

        return visible
