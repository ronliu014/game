"""
Panel UI Component Module

This module provides the Panel class for creating container panels
that can hold other UI components.

Classes:
    Panel: Container panel for grouping UI components

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import List, Optional, Tuple
import pygame

from src.rendering.ui.ui_component import UIComponent
from src.config.constants import COLOR_BACKGROUND, COLOR_WHITE

# Configure logger
logger = logging.getLogger(__name__)


class Panel(UIComponent):
    """
    Container panel for grouping UI components.

    Can contain multiple child components and handle their drawing and events.

    Attributes:
        _children: List of child UI components
        _bg_color: Background color
        _border_color: Border color (None for no border)
        _border_width: Border width in pixels

    Example:
        >>> panel = Panel(50, 50, 400, 300)
        >>> button = Button(100, 100, 200, 50, "Click Me")
        >>> panel.add_child(button)
        >>> panel.draw(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        bg_color: Optional[Tuple[int, int, int]] = None,
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 2
    ) -> None:
        """
        Initialize the panel.

        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
            bg_color: Background color (uses default if None)
            border_color: Border color (None for no border)
            border_width: Border width in pixels
        """
        super().__init__(x, y, width, height)

        self._children: List[UIComponent] = []
        self._bg_color = bg_color or COLOR_BACKGROUND
        self._border_color = border_color
        self._border_width = border_width

        logger.debug(f"Panel created at ({x}, {y}) with size ({width}, {height})")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the panel and all its children.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Draw background
        pygame.draw.rect(surface, self._bg_color, self.get_rect())

        # Draw border if specified
        if self._border_color:
            pygame.draw.rect(
                surface,
                self._border_color,
                self.get_rect(),
                self._border_width
            )

        # Draw all children
        for child in self._children:
            if child.is_visible():
                child.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events and pass them to children.

        Args:
            event: Pygame event to handle

        Returns:
            True if any child handled the event, False otherwise
        """
        if not self.visible or not self.enabled:
            return False

        # Pass event to children (in reverse order for proper z-order)
        for child in reversed(self._children):
            if child.is_enabled() and child.handle_event(event):
                return True

        return False

    def add_child(self, component: UIComponent) -> None:
        """
        Add a child component to the panel.

        Args:
            component: UI component to add

        Example:
            >>> button = Button(100, 100, 200, 50, "Click")
            >>> panel.add_child(button)
        """
        self._children.append(component)
        logger.debug(f"Child component added to panel: {type(component).__name__}")

    def remove_child(self, component: UIComponent) -> bool:
        """
        Remove a child component from the panel.

        Args:
            component: UI component to remove

        Returns:
            True if component was removed, False if not found

        Example:
            >>> panel.remove_child(button)
            True
        """
        if component in self._children:
            self._children.remove(component)
            logger.debug(f"Child component removed from panel: {type(component).__name__}")
            return True
        return False

    def clear_children(self) -> None:
        """
        Remove all child components.

        Example:
            >>> panel.clear_children()
        """
        count = len(self._children)
        self._children.clear()
        logger.debug(f"Panel children cleared: {count} components removed")

    def get_children(self) -> List[UIComponent]:
        """
        Get all child components.

        Returns:
            List of child UI components

        Example:
            >>> children = panel.get_children()
            >>> print(f"Panel has {len(children)} children")
        """
        return self._children.copy()

    def get_child_count(self) -> int:
        """
        Get the number of child components.

        Returns:
            Number of children

        Example:
            >>> count = panel.get_child_count()
        """
        return len(self._children)

    def set_background_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set the panel background color.

        Args:
            color: RGB color tuple

        Example:
            >>> panel.set_background_color((50, 50, 50))
        """
        self._bg_color = color

    def set_border(
        self,
        color: Optional[Tuple[int, int, int]],
        width: int = 2
    ) -> None:
        """
        Set the panel border.

        Args:
            color: Border color (None to remove border)
            width: Border width in pixels

        Example:
            >>> panel.set_border((255, 255, 255), 3)
            >>> panel.set_border(None)  # Remove border
        """
        self._border_color = color
        self._border_width = width
