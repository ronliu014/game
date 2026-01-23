"""
UI Component Base Class

Provides the base class for all UI components.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
import pygame


class UIComponent(ABC):
    """
    Base class for all UI components.

    Provides common functionality for position, size, visibility, and event handling.

    Attributes:
        x (int): X position of the component
        y (int): Y position of the component
        width (int): Width of the component
        height (int): Height of the component
        visible (bool): Whether the component is visible
        enabled (bool): Whether the component is enabled for interaction

    Example:
        >>> class MyButton(UIComponent):
        ...     def draw(self, surface):
        ...         pygame.draw.rect(surface, (100, 100, 100), self.get_rect())
        ...     def handle_event(self, event):
        ...         return False
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize the UI component.

        Args:
            x: X position
            y: Y position
            width: Component width
            height: Component height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the component on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        pass

    def update(self, delta_ms: float) -> None:
        """
        Update component logic (optional).

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    def get_rect(self) -> pygame.Rect:
        """
        Get the component's bounding rectangle.

        Returns:
            pygame.Rect: Bounding rectangle
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if a point is inside the component.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            bool: True if point is inside, False otherwise
        """
        return self.get_rect().collidepoint(x, y)

    def set_position(self, x: int, y: int) -> None:
        """
        Set the component's position.

        Args:
            x: New X position
            y: New Y position
        """
        self.x = x
        self.y = y

    def set_size(self, width: int, height: int) -> None:
        """
        Set the component's size.

        Args:
            width: New width
            height: New height
        """
        self.width = width
        self.height = height

    def show(self) -> None:
        """Make the component visible."""
        self.visible = True

    def hide(self) -> None:
        """Hide the component."""
        self.visible = False

    def enable(self) -> None:
        """Enable the component for interaction."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the component for interaction."""
        self.enabled = False
