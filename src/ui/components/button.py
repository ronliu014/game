"""
Button Component

Provides a clickable button UI component with multiple states.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Callable, Dict, Tuple
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class Button(UIComponent):
    """
    Button component with support for multiple states and click events.

    Supports both sprite-based and color-based rendering.

    Attributes:
        label (str): Button text label
        on_click (Callable): Callback function when button is clicked
        state (str): Current button state (normal/hover/pressed/disabled)

    Example:
        >>> def on_button_click():
        ...     print("Button clicked!")
        >>> button = Button(100, 100, 200, 50, "Start Game", on_button_click)
        >>> button.draw(screen)
    """

    # Button states
    STATE_NORMAL = 'normal'
    STATE_HOVER = 'hover'
    STATE_PRESSED = 'pressed'
    STATE_DISABLED = 'disabled'

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        on_click: Optional[Callable] = None,
        sprites: Optional[Dict[str, pygame.Surface]] = None,
        colors: Optional[Dict[str, Tuple[int, int, int]]] = None,
        font_size: int = 20,
        text_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """
        Initialize the button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            label: Button text
            on_click: Callback function when clicked
            sprites: Dictionary of state sprites {state: surface}
            colors: Dictionary of state colors {state: (r, g, b)}
            font_size: Font size for label
            text_color: Text color
        """
        super().__init__(x, y, width, height)
        self.label = label
        self.on_click = on_click
        self._sprites = sprites or {}
        self._colors = colors or {
            self.STATE_NORMAL: (100, 100, 100),
            self.STATE_HOVER: (150, 150, 150),
            self.STATE_PRESSED: (80, 80, 80),
            self.STATE_DISABLED: (60, 60, 60)
        }
        self._font_size = font_size
        self._text_color = text_color
        self._state = self.STATE_NORMAL
        self._is_pressed = False

        # Load font
        try:
            self._font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", font_size)
        except Exception:
            logger.warning("Failed to load Chinese font, using default")
            self._font = pygame.font.Font(None, font_size)

        logger.debug(f"Button '{label}' created at ({x}, {y})")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Determine current state for rendering
        render_state = self._state if self.enabled else self.STATE_DISABLED

        # Draw button background
        if render_state in self._sprites:
            # Use sprite if available
            sprite = self._sprites[render_state]
            # Scale sprite to button size if needed
            if sprite.get_size() != (self.width, self.height):
                sprite = pygame.transform.scale(sprite, (self.width, self.height))
            surface.blit(sprite, (self.x, self.y))
        else:
            # Use color background
            color = self._colors.get(render_state, self._colors[self.STATE_NORMAL])
            pygame.draw.rect(surface, color, self.get_rect())
            # Draw border
            border_color = (200, 200, 200) if self.enabled else (100, 100, 100)
            pygame.draw.rect(surface, border_color, self.get_rect(), 2)

        # Draw label text
        text_surface = self._font.render(self.label, True, self._text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            if self.contains_point(event.pos[0], event.pos[1]):
                if not self._is_pressed:
                    self._state = self.STATE_HOVER
                return True
            else:
                if not self._is_pressed:
                    self._state = self.STATE_NORMAL
                return False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.contains_point(event.pos[0], event.pos[1]):
                    self._state = self.STATE_PRESSED
                    self._is_pressed = True
                    logger.debug(f"Button '{self.label}' pressed")
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                was_pressed = self._is_pressed
                self._is_pressed = False

                if self.contains_point(event.pos[0], event.pos[1]):
                    self._state = self.STATE_HOVER
                    if was_pressed and self.on_click:
                        logger.info(f"Button '{self.label}' clicked")
                        self.on_click()
                    return True
                else:
                    self._state = self.STATE_NORMAL

        return False

    def set_state(self, state: str) -> None:
        """
        Set the button state manually.

        Args:
            state: Button state (normal/hover/pressed/disabled)
        """
        if state in [self.STATE_NORMAL, self.STATE_HOVER, self.STATE_PRESSED, self.STATE_DISABLED]:
            self._state = state
        else:
            logger.warning(f"Invalid button state: {state}")

    def get_state(self) -> str:
        """
        Get the current button state.

        Returns:
            str: Current state
        """
        return self._state

    def set_label(self, label: str) -> None:
        """
        Set the button label text.

        Args:
            label: New label text
        """
        self.label = label

    def set_sprites(self, sprites: Dict[str, pygame.Surface]) -> None:
        """
        Set button sprites for different states.

        Args:
            sprites: Dictionary of state sprites {state: surface}
        """
        self._sprites = sprites

    def set_colors(self, colors: Dict[str, Tuple[int, int, int]]) -> None:
        """
        Set button colors for different states.

        Args:
            colors: Dictionary of state colors {state: (r, g, b)}
        """
        self._colors = colors
