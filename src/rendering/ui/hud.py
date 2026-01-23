"""
HUD (Heads-Up Display) UI Component Module

This module provides the HUD class for displaying game information like
level number, move count, and FPS.

Classes:
    HUD: Heads-up display component for game information

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import Optional, Dict, Any
import pygame

from src.rendering.ui.ui_component import UIComponent
from src.config.constants import COLOR_TEXT, COLOR_BACKGROUND

# Configure logger
logger = logging.getLogger(__name__)


class HUD(UIComponent):
    """
    Heads-up display component for showing game information.

    Displays text-based information like level number, move count, FPS, etc.

    Attributes:
        font_size: Font size for the text
        _font: Pygame font object
        _text_color: Color for the text
        _bg_color: Background color (None for transparent)
        _data: Dictionary of data to display

    Example:
        >>> hud = HUD(10, 10, 300, 100)
        >>> hud.set_data("level", "Level 1")
        >>> hud.set_data("moves", "Moves: 5")
        >>> hud.draw(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font_size: int = 20,
        text_color: Optional[tuple] = None,
        bg_color: Optional[tuple] = None
    ) -> None:
        """
        Initialize the HUD.

        Args:
            x: X position
            y: Y position
            width: HUD width
            height: HUD height
            font_size: Font size for the text
            text_color: Text color (uses default if None)
            bg_color: Background color (None for transparent)
        """
        super().__init__(x, y, width, height)

        self.font_size = font_size
        self._text_color = text_color or COLOR_TEXT
        self._bg_color = bg_color
        self._data: Dict[str, Any] = {}

        # Font
        try:
            # Use Microsoft YaHei for Chinese support
            chinese_font = "C:/WINDOWS/fonts/msyh.ttc"
            self._font = pygame.font.Font(chinese_font, font_size)
        except Exception as e:
            logger.warning(f"Failed to load Chinese font, using default: {e}")
            try:
                self._font = pygame.font.Font(None, font_size)
            except Exception as e2:
                logger.error(f"Failed to create font: {e2}")
                self._font = pygame.font.Font(None, 20)

        logger.debug(f"HUD created at ({x}, {y})")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the HUD on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Draw background if specified
        if self._bg_color:
            pygame.draw.rect(surface, self._bg_color, self.get_rect())

        # Draw each data item
        y_offset = self.y + 5
        for key, value in self._data.items():
            text = f"{value}"
            text_surface = self._font.render(text, True, self._text_color)
            surface.blit(text_surface, (self.x + 5, y_offset))
            y_offset += self.font_size + 5

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events (HUD doesn't handle events by default).

        Args:
            event: Pygame event to handle

        Returns:
            False (HUD doesn't handle events)
        """
        return False

    def set_data(self, key: str, value: Any) -> None:
        """
        Set a data value to display.

        Args:
            key: Data key
            value: Data value to display

        Example:
            >>> hud.set_data("level", "Level 1")
            >>> hud.set_data("moves", 5)
        """
        self._data[key] = value

    def get_data(self, key: str) -> Optional[Any]:
        """
        Get a data value.

        Args:
            key: Data key

        Returns:
            Data value or None if key doesn't exist

        Example:
            >>> level = hud.get_data("level")
        """
        return self._data.get(key)

    def clear_data(self) -> None:
        """
        Clear all data.

        Example:
            >>> hud.clear_data()
        """
        self._data.clear()
        logger.debug("HUD data cleared")

    def remove_data(self, key: str) -> None:
        """
        Remove a specific data item.

        Args:
            key: Data key to remove

        Example:
            >>> hud.remove_data("level")
        """
        if key in self._data:
            del self._data[key]
            logger.debug(f"HUD data removed: {key}")
