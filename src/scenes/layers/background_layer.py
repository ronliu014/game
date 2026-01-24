"""
Background Layer

Provides background rendering for game scenes.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
from typing import Optional
from src.scenes.layers.layer_base import LayerBase
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class BackgroundLayer(LayerBase):
    """
    Background layer for game scenes.

    Renders a solid color or image background.

    Features:
        - Solid color background
        - Image background (optional)
        - Parallax scrolling (optional)

    Example:
        >>> layer = BackgroundLayer(800, 600, background_color=(20, 30, 40))
        >>> layer.update(16.67)
        >>> layer.draw(screen)
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        background_color: tuple = (20, 30, 40),
        background_image: Optional[pygame.Surface] = None
    ):
        """
        Initialize the background layer.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            background_color: RGB color tuple for solid background
            background_image: Optional background image surface
        """
        super().__init__(screen_width, screen_height)

        self._background_color = background_color
        self._background_image = background_image
        self._parallax_offset = 0.0
        self._parallax_speed = 0.0

        logger.debug(f"BackgroundLayer initialized with color {background_color}")

    def update(self, delta_ms: float) -> None:
        """
        Update background layer.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Update parallax scrolling if enabled
        if self._parallax_speed != 0:
            self._parallax_offset += self._parallax_speed * (delta_ms / 1000.0)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the background.

        Args:
            surface: Pygame surface to draw on
        """
        if not self._visible:
            return

        # Draw solid color background
        surface.fill(self._background_color)

        # Draw image background if available
        if self._background_image:
            # TODO: Implement parallax scrolling
            surface.blit(self._background_image, (0, 0))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: Always False (background doesn't handle events)
        """
        return False

    def set_background_color(self, color: tuple) -> None:
        """
        Set background color.

        Args:
            color: RGB color tuple
        """
        self._background_color = color

    def set_background_image(self, image: pygame.Surface) -> None:
        """
        Set background image.

        Args:
            image: Background image surface
        """
        self._background_image = image

    def set_parallax_speed(self, speed: float) -> None:
        """
        Set parallax scrolling speed.

        Args:
            speed: Scrolling speed (pixels per second)
        """
        self._parallax_speed = speed
