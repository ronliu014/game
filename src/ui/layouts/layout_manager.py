"""
Layout Manager

Provides layout management for UI components.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import List, Tuple, Optional
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class LayoutManager:
    """
    Layout manager for arranging UI components.

    Supports center alignment, vertical/horizontal arrangement, and anchor positioning.

    Example:
        >>> layout = LayoutManager(800, 600)
        >>> layout.center_component(button, horizontal=True, vertical=True)
        >>> layout.arrange_vertical([button1, button2, button3], spacing=10)
    """

    # Anchor positions
    ANCHOR_TOP_LEFT = 'top_left'
    ANCHOR_TOP_CENTER = 'top_center'
    ANCHOR_TOP_RIGHT = 'top_right'
    ANCHOR_CENTER_LEFT = 'center_left'
    ANCHOR_CENTER = 'center'
    ANCHOR_CENTER_RIGHT = 'center_right'
    ANCHOR_BOTTOM_LEFT = 'bottom_left'
    ANCHOR_BOTTOM_CENTER = 'bottom_center'
    ANCHOR_BOTTOM_RIGHT = 'bottom_right'

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the layout manager.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        logger.debug(f"LayoutManager created for screen size ({screen_width}, {screen_height})")

    def center_component(
        self,
        component: UIComponent,
        horizontal: bool = True,
        vertical: bool = True,
        offset_x: int = 0,
        offset_y: int = 0
    ) -> None:
        """
        Center a component on the screen.

        Args:
            component: Component to center
            horizontal: Center horizontally
            vertical: Center vertically
            offset_x: Horizontal offset from center
            offset_y: Vertical offset from center
        """
        x = component.x
        y = component.y

        if horizontal:
            x = (self._screen_width - component.width) // 2 + offset_x

        if vertical:
            y = (self._screen_height - component.height) // 2 + offset_y

        component.set_position(x, y)
        logger.debug(f"Component centered at ({x}, {y})")

    def arrange_vertical(
        self,
        components: List[UIComponent],
        start_x: Optional[int] = None,
        start_y: Optional[int] = None,
        spacing: int = 10,
        center_horizontal: bool = False
    ) -> None:
        """
        Arrange components vertically.

        Args:
            components: List of components to arrange
            start_x: Starting X position (None = use current)
            start_y: Starting Y position (None = use current)
            spacing: Spacing between components in pixels
            center_horizontal: Center each component horizontally
        """
        if not components:
            return

        current_y = start_y if start_y is not None else components[0].y

        for component in components:
            if center_horizontal:
                x = (self._screen_width - component.width) // 2
            else:
                x = start_x if start_x is not None else component.x

            component.set_position(x, current_y)
            current_y += component.height + spacing

        logger.debug(f"Arranged {len(components)} components vertically")

    def arrange_horizontal(
        self,
        components: List[UIComponent],
        start_x: Optional[int] = None,
        start_y: Optional[int] = None,
        spacing: int = 10,
        center_vertical: bool = False
    ) -> None:
        """
        Arrange components horizontally.

        Args:
            components: List of components to arrange
            start_x: Starting X position (None = use current)
            start_y: Starting Y position (None = use current)
            spacing: Spacing between components in pixels
            center_vertical: Center each component vertically
        """
        if not components:
            return

        current_x = start_x if start_x is not None else components[0].x

        for component in components:
            if center_vertical:
                y = (self._screen_height - component.height) // 2
            else:
                y = start_y if start_y is not None else component.y

            component.set_position(current_x, y)
            current_x += component.width + spacing

        logger.debug(f"Arranged {len(components)} components horizontally")

    def anchor_component(
        self,
        component: UIComponent,
        anchor: str,
        margin_x: int = 0,
        margin_y: int = 0
    ) -> None:
        """
        Position a component using anchor positioning.

        Args:
            component: Component to position
            anchor: Anchor position (use ANCHOR_* constants)
            margin_x: Horizontal margin from anchor point
            margin_y: Vertical margin from anchor point
        """
        x, y = 0, 0

        # Calculate X position
        if anchor.endswith('_left'):
            x = margin_x
        elif anchor.endswith('_center') or anchor == 'center':
            x = (self._screen_width - component.width) // 2 + margin_x
        elif anchor.endswith('_right'):
            x = self._screen_width - component.width - margin_x

        # Calculate Y position
        if anchor.startswith('top_'):
            y = margin_y
        elif anchor.startswith('center_') or anchor == 'center':
            y = (self._screen_height - component.height) // 2 + margin_y
        elif anchor.startswith('bottom_'):
            y = self._screen_height - component.height - margin_y

        component.set_position(x, y)
        logger.debug(f"Component anchored to {anchor} at ({x}, {y})")

    def arrange_grid(
        self,
        components: List[UIComponent],
        columns: int,
        start_x: int,
        start_y: int,
        spacing_x: int = 10,
        spacing_y: int = 10,
        center_in_screen: bool = False
    ) -> None:
        """
        Arrange components in a grid layout.

        Args:
            components: List of components to arrange
            columns: Number of columns
            start_x: Starting X position
            start_y: Starting Y position
            spacing_x: Horizontal spacing between components
            spacing_y: Vertical spacing between components
            center_in_screen: Center the entire grid in the screen
        """
        if not components or columns <= 0:
            return

        # Calculate grid dimensions
        rows = (len(components) + columns - 1) // columns

        if center_in_screen and components:
            # Calculate total grid size
            total_width = sum(components[i].width for i in range(min(columns, len(components))))
            total_width += spacing_x * (min(columns, len(components)) - 1)

            # Find max height in first column
            max_height = max(components[i].height for i in range(0, len(components), columns))
            total_height = max_height * rows + spacing_y * (rows - 1)

            # Center the grid
            start_x = (self._screen_width - total_width) // 2
            start_y = (self._screen_height - total_height) // 2

        # Position components
        for i, component in enumerate(components):
            row = i // columns
            col = i % columns

            x = start_x + col * (component.width + spacing_x)
            y = start_y + row * (component.height + spacing_y)

            component.set_position(x, y)

        logger.debug(f"Arranged {len(components)} components in {rows}x{columns} grid")

    def distribute_horizontal(
        self,
        components: List[UIComponent],
        start_x: int,
        end_x: int,
        y: int
    ) -> None:
        """
        Distribute components evenly across horizontal space.

        Args:
            components: List of components to distribute
            start_x: Starting X position
            end_x: Ending X position
            y: Y position for all components
        """
        if not components:
            return

        if len(components) == 1:
            components[0].set_position(start_x, y)
            return

        # Calculate total width of all components
        total_component_width = sum(c.width for c in components)
        available_space = end_x - start_x - total_component_width
        spacing = available_space / (len(components) - 1)

        current_x = start_x
        for component in components:
            component.set_position(int(current_x), y)
            current_x += component.width + spacing

        logger.debug(f"Distributed {len(components)} components horizontally")

    def distribute_vertical(
        self,
        components: List[UIComponent],
        x: int,
        start_y: int,
        end_y: int
    ) -> None:
        """
        Distribute components evenly across vertical space.

        Args:
            components: List of components to distribute
            x: X position for all components
            start_y: Starting Y position
            end_y: Ending Y position
        """
        if not components:
            return

        if len(components) == 1:
            components[0].set_position(x, start_y)
            return

        # Calculate total height of all components
        total_component_height = sum(c.height for c in components)
        available_space = end_y - start_y - total_component_height
        spacing = available_space / (len(components) - 1)

        current_y = start_y
        for component in components:
            component.set_position(x, int(current_y))
            current_y += component.height + spacing

        logger.debug(f"Distributed {len(components)} components vertically")

    def set_screen_size(self, width: int, height: int) -> None:
        """
        Update the screen size.

        Args:
            width: New screen width
            height: New screen height
        """
        self._screen_width = width
        self._screen_height = height
        logger.debug(f"Screen size updated to ({width}, {height})")

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the current screen size.

        Returns:
            Tuple[int, int]: (width, height)
        """
        return (self._screen_width, self._screen_height)
