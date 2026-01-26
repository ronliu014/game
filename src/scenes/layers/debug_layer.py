"""
Debug Layer

Provides debug information overlay for development.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
from typing import Optional, Dict, Any
from src.scenes.layers.layer_base import LayerBase
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class DebugLayer(LayerBase):
    """
    Debug layer for displaying development information.

    Shows:
        - FPS counter
        - Memory usage
        - Game state information
        - Custom debug values

    Features:
        - Toggle visibility with key
        - Customizable debug info
        - Performance metrics

    Example:
        >>> layer = DebugLayer(800, 600)
        >>> layer.set_debug_value('fps', 60.0)
        >>> layer.update(16.67)
        >>> layer.draw(screen)
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the debug layer.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        super().__init__(screen_width, screen_height)

        self._debug_values: Dict[str, Any] = {}
        self._font: Optional[pygame.font.Font] = None
        self._visible = False  # Hidden by default

        # Try to load font
        try:
            self._font = pygame.font.Font(None, 20)
        except Exception as e:
            logger.warning(f"Could not load debug font: {e}")

        logger.debug("DebugLayer initialized")

    def update(self, delta_ms: float) -> None:
        """
        Update debug layer.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Debug layer doesn't need updates
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw debug information.

        Args:
            surface: Pygame surface to draw on
        """
        if not self._visible or not self._font:
            return

        # Draw semi-transparent background
        debug_surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        debug_surface.fill((0, 0, 0, 180))
        surface.blit(debug_surface, (10, 70))

        # Draw debug values
        y_offset = 80
        line_height = 25

        # Title
        title_text = self._font.render("Debug Info", True, (255, 255, 0))
        surface.blit(title_text, (20, y_offset))
        y_offset += line_height

        # Draw each debug value
        for key, value in self._debug_values.items():
            text = f"{key}: {value}"
            debug_text = self._font.render(text, True, (200, 200, 200))
            surface.blit(debug_text, (20, y_offset))
            y_offset += line_height

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if event was handled, False otherwise
        """
        # Toggle debug layer with F3 key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.toggle_visibility()
                return True

        return False

    def set_debug_value(self, key: str, value: Any) -> None:
        """
        Set a debug value to display.

        Args:
            key: Debug value name
            value: Debug value
        """
        self._debug_values[key] = value

    def remove_debug_value(self, key: str) -> None:
        """
        Remove a debug value.

        Args:
            key: Debug value name to remove
        """
        if key in self._debug_values:
            del self._debug_values[key]

    def clear_debug_values(self) -> None:
        """Clear all debug values."""
        self._debug_values.clear()

    def toggle_visibility(self) -> None:
        """Toggle debug layer visibility."""
        self._visible = not self._visible
        logger.debug(f"Debug layer visibility: {self._visible}")

    def get_debug_values(self) -> Dict[str, Any]:
        """
        Get all debug values.

        Returns:
            Dict[str, Any]: Dictionary of debug values
        """
        return self._debug_values.copy()
