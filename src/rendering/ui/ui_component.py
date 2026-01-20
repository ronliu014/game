"""
UI Component Base Module

This module provides the base UIComponent class that all UI elements inherit from.
It defines the common interface and behavior for UI components.

Classes:
    UIComponent: Abstract base class for all UI components

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
import pygame


class UIComponent(ABC):
    """
    Abstract base class for all UI components.

    Provides common functionality for position, size, visibility, and event handling.

    Attributes:
        x: X position of the component
        y: Y position of the component
        width: Width of the component
        height: Height of the component
        visible: Whether the component is visible
        enabled: Whether the component is enabled for interaction

    Example:
        >>> class MyButton(UIComponent):
        ...     def draw(self, surface):
        ...         pygame.draw.rect(surface, (255, 0, 0), self.get_rect())
        ...     def handle_event(self, event):
        ...         pass
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        visible: bool = True,
        enabled: bool = True
    ) -> None:
        """
        Initialize the UI component.

        Args:
            x: X position
            y: Y position
            width: Component width
            height: Component height
            visible: Initial visibility state
            enabled: Initial enabled state
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible
        self.enabled = enabled

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the component on the given surface.

        Args:
            surface: Pygame surface to draw on

        Note:
            This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle a pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            True if the event was handled, False otherwise

        Note:
            This method must be implemented by subclasses.
        """
        pass

    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle of the component.

        Returns:
            pygame.Rect representing the component's bounds

        Example:
            >>> component = MyButton(100, 100, 200, 50)
            >>> rect = component.get_rect()
            >>> rect.topleft
            (100, 100)
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if a point is inside the component.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if the point is inside, False otherwise

        Example:
            >>> component = MyButton(100, 100, 200, 50)
            >>> component.contains_point(150, 125)
            True
            >>> component.contains_point(50, 50)
            False
        """
        return self.get_rect().collidepoint(x, y)

    def set_position(self, x: int, y: int) -> None:
        """
        Set the position of the component.

        Args:
            x: New X position
            y: New Y position

        Example:
            >>> component.set_position(200, 300)
        """
        self.x = x
        self.y = y

    def set_size(self, width: int, height: int) -> None:
        """
        Set the size of the component.

        Args:
            width: New width
            height: New height

        Example:
            >>> component.set_size(300, 100)
        """
        self.width = width
        self.height = height

    def show(self) -> None:
        """
        Make the component visible.

        Example:
            >>> component.show()
        """
        self.visible = True

    def hide(self) -> None:
        """
        Hide the component.

        Example:
            >>> component.hide()
        """
        self.visible = False

    def enable(self) -> None:
        """
        Enable the component for interaction.

        Example:
            >>> component.enable()
        """
        self.enabled = True

    def disable(self) -> None:
        """
        Disable the component from interaction.

        Example:
            >>> component.disable()
        """
        self.enabled = False

    def is_visible(self) -> bool:
        """
        Check if the component is visible.

        Returns:
            True if visible, False otherwise

        Example:
            >>> component.is_visible()
            True
        """
        return self.visible

    def is_enabled(self) -> bool:
        """
        Check if the component is enabled.

        Returns:
            True if enabled, False otherwise

        Example:
            >>> component.is_enabled()
            True
        """
        return self.enabled
