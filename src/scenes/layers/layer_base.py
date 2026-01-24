"""
Layer Base Class

Abstract base class for scene layers.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from abc import ABC, abstractmethod
from typing import Optional
import pygame
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class LayerBase(ABC):
    """
    Abstract base class for scene layers.

    Provides common interface for all layers in a scene.

    Layers are rendered in order:
    1. Background Layer (bottom)
    2. Game Layer
    3. HUD Layer
    4. Debug Layer (top)

    Example:
        >>> class MyLayer(LayerBase):
        ...     def update(self, delta_ms):
        ...         pass
        ...     def draw(self, surface):
        ...         pass
        ...     def handle_event(self, event):
        ...         return False
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the layer.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._visible = True
        self._enabled = True

        logger.debug(f"{self.__class__.__name__} initialized")

    @abstractmethod
    def update(self, delta_ms: float) -> None:
        """
        Update layer logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the layer.

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
            bool: True if event was handled, False otherwise
        """
        pass

    def on_enter(self) -> None:
        """Called when the layer becomes active."""
        logger.debug(f"{self.__class__.__name__} entered")

    def on_exit(self) -> None:
        """Called when the layer is being removed."""
        logger.debug(f"{self.__class__.__name__} exited")

    def set_visible(self, visible: bool) -> None:
        """
        Set layer visibility.

        Args:
            visible: Whether the layer should be visible
        """
        self._visible = visible

    def is_visible(self) -> bool:
        """
        Check if layer is visible.

        Returns:
            bool: True if visible, False otherwise
        """
        return self._visible

    def set_enabled(self, enabled: bool) -> None:
        """
        Set layer enabled state.

        Args:
            enabled: Whether the layer should be enabled
        """
        self._enabled = enabled

    def is_enabled(self) -> bool:
        """
        Check if layer is enabled.

        Returns:
            bool: True if enabled, False otherwise
        """
        return self._enabled

    def get_screen_size(self) -> tuple:
        """
        Get screen dimensions.

        Returns:
            tuple: (width, height)
        """
        return (self._screen_width, self._screen_height)

    def __repr__(self) -> str:
        """String representation of the layer."""
        return f"{self.__class__.__name__}(visible={self._visible}, enabled={self._enabled})"
