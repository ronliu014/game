"""
Panel Component

Provides a panel UI component for grouping other components.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Tuple
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class Panel(UIComponent):
    """
    Panel component for grouping UI elements.

    Supports background color, image, border, and transparency.

    Attributes:
        background_color (Optional[Tuple[int, int, int]]): Background color
        background_image (Optional[pygame.Surface]): Background image
        border_color (Optional[Tuple[int, int, int]]): Border color
        border_width (int): Border width in pixels
        alpha (int): Transparency (0-255)

    Example:
        >>> panel = Panel(50, 50, 300, 200, background_color=(50, 50, 50))
        >>> panel.draw(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        background_color: Optional[Tuple[int, int, int]] = None,
        background_image: Optional[pygame.Surface] = None,
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 0,
        alpha: int = 255
    ):
        """
        Initialize the panel.

        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
            background_color: Background color (r, g, b)
            background_image: Background image surface
            border_color: Border color (r, g, b)
            border_width: Border width in pixels
            alpha: Transparency (0=transparent, 255=opaque)
        """
        super().__init__(x, y, width, height)
        self._background_color = background_color
        self._background_image = background_image
        self._border_color = border_color
        self._border_width = border_width
        self._alpha = alpha

        # Create surface for transparency support
        if self._alpha < 255:
            self._surface = pygame.Surface((width, height), pygame.SRCALPHA)
        else:
            self._surface = None

        logger.debug(f"Panel created at ({x}, {y}) withize ({width}, {height})")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the panel on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Use temporary surface for transparency
        if self._surface:
            self._surface.fill((0, 0, 0, 0))  # Clear with transparent
            draw_surface = self._surface
            draw_x, draw_y = 0, 0
        else:
            draw_surface = surface
            draw_x, draw_y = self.x, self.y

        # Draw background
        if self._background_image:
            # Scale image to panel size if needed
            if self._background_image.get_size() != (self.width, self.height):
                scaled_image = pygame.transform.scale(
                    self._background_image,
                    (self.width, self.height)
                )
                draw_surface.blit(scaled_image, (draw_x, draw_y))
            else:
                draw_surface.blit(self._background_image, (draw_x, draw_y))
        elif self._background_color:
            # Draw solid color background
            if self._alpha < 255:
                color_with_alpha = (*self._background_color, self._alpha)
                pygame.draw.rect(
                    draw_surface,
                    color_with_alpha,
                    (draw_x, draw_y, self.width, self.height)
                )
            else:
                pygame.draw.rect(
                    draw_surface,
                    self._background_color,
                    (draw_x, draw_y, self.width, self.height)
                )

        # Draw border
        if self._border_color and self._border_width > 0:
            pygame.draw.rect(
                draw_surface,
                self._border_color,
                (draw_x, draw_y, self.width, self.height),
                self._border_width
            )

        # Blit temporary surface to main surface if using transparency
        if self._surface:
            surface.blit(self._surface, (self.x, self.y))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event (panels don't handle events by default).

        Args:
            event: Pygame event to handle

        Returns:
            bool: False (panels don't handle events)
        """
        return False

    def set_background_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set the panel background color.

        Args:
            color: Background color (r, g, b)
        """
        self._background_color = color

    def set_background_image(self, image: pygame.Surface) -> None:
        """
        Set the panel background image.

        Args:
            image: Background image surface
        """
        self._background_image = image

    def set_border(self, color: Tuple[int, int, int], width: int) -> None:
        """
        Set the panel border.

        Args:
            color: Border color (r, g, b)
            width: Border width in pixels
        """
        self._border_color = color
        self._border_width = width

    def set_alpha(self, alpha: int) -> None:
        """
        Set the panel transparency.

        Args:
            alpha: Transparency (0=transparent, 255=opaque)
        """
        self._alpha = max(0, min(255, alpha))
        # Recreate surface if needed
        if self._alpha < 255 and not self._surface:
            self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        elif self._alpha == 255:
            self._surface = None
