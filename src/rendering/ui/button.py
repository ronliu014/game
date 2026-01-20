"""
Button UI Component Module

This module provides the Button class for creating interactive buttons.

Classes:
    Button: Interactive button component with hover and click states

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import Optional, Callable, Tuple
import pygame

from src.rendering.ui.ui_component import UIComponent
from src.config.constants import (
    COLOR_BUTTON_NORMAL, COLOR_BUTTON_HOVER, COLOR_BUTTON_PRESSED,
    COLOR_TEXT, COLOR_WHITE
)

# Configure logger
logger = logging.getLogger(__name__)


class Button(UIComponent):
    """
    Interactive button component.

    Supports hover effects, click handling, and customizable appearance.

    Attributes:
        text: Button text
        font_size: Font size for the text
        on_click: Callback function called when button is clicked
        _is_hovered: Whether the mouse is hovering over the button
        _is_pressed: Whether the button is currently pressed
        _font: Pygame font object
        _color_normal: Normal state color
        _color_hover: Hover state color
        _color_pressed: Pressed state color
        _text_color: Text color

    Example:
        >>> def on_button_click():
        ...     print("Button clicked!")
        >>> button = Button(100, 100, 200, 50, "Click Me", on_click=on_button_click)
        >>> button.draw(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 24,
        on_click: Optional[Callable[[], None]] = None,
        color_normal: Optional[Tuple[int, int, int]] = None,
        color_hover: Optional[Tuple[int, int, int]] = None,
        color_pressed: Optional[Tuple[int, int, int]] = None,
        text_color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """
        Initialize the button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
            font_size: Font size for the text
            on_click: Callback function for click events
            color_normal: Normal state color (uses default if None)
            color_hover: Hover state color (uses default if None)
            color_pressed: Pressed state color (uses default if None)
            text_color: Text color (uses default if None)
        """
        super().__init__(x, y, width, height)

        self.text = text
        self.font_size = font_size
        self.on_click = on_click

        # State tracking
        self._is_hovered = False
        self._is_pressed = False

        # Colors
        self._color_normal = color_normal or COLOR_BUTTON_NORMAL
        self._color_hover = color_hover or COLOR_BUTTON_HOVER
        self._color_pressed = color_pressed or COLOR_BUTTON_PRESSED
        self._text_color = text_color or COLOR_TEXT

        # Font
        try:
            self._font = pygame.font.Font(None, font_size)
        except Exception as e:
            logger.error(f"Failed to create font: {e}")
            self._font = pygame.font.Font(None, 24)

        logger.debug(f"Button created: '{text}' at ({x}, {y})")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Determine button color based on state
        if not self.enabled:
            color = self._color_normal
        elif self._is_pressed:
            color = self._color_pressed
        elif self._is_hovered:
            color = self._color_hover
        else:
            color = self._color_normal

        # Draw button background
        pygame.draw.rect(surface, color, self.get_rect())

        # Draw button border
        pygame.draw.rect(surface, COLOR_WHITE, self.get_rect(), 2)

        # Draw button text
        text_surface = self._font.render(self.text, True, self._text_color)
        text_rect = text_surface.get_rect(center=self.get_rect().center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for the button.

        Args:
            event: Pygame event to handle

        Returns:
            True if the event was handled, False otherwise
        """
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            self._is_hovered = self.contains_point(event.pos[0], event.pos[1])
            return self._is_hovered

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.contains_point(event.pos[0], event.pos[1]):
                    self._is_pressed = True
                    logger.debug(f"Button pressed: '{self.text}'")
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                was_pressed = self._is_pressed
                self._is_pressed = False

                if was_pressed and self.contains_point(event.pos[0], event.pos[1]):
                    # Button was clicked
                    logger.info(f"Button clicked: '{self.text}'")
                    if self.on_click:
                        self.on_click()
                    return True

        return False

    def set_text(self, text: str) -> None:
        """
        Set the button text.

        Args:
            text: New button text

        Example:
            >>> button.set_text("New Text")
        """
        self.text = text
        logger.debug(f"Button text changed to: '{text}'")

    def set_callback(self, callback: Callable[[], None]) -> None:
        """
        Set the click callback function.

        Args:
            callback: Function to call when button is clicked

        Example:
            >>> button.set_callback(lambda: print("Clicked!"))
        """
        self.on_click = callback

    def is_hovered(self) -> bool:
        """
        Check if the button is currently hovered.

        Returns:
            True if hovered, False otherwise

        Example:
            >>> if button.is_hovered():
            ...     print("Mouse over button")
        """
        return self._is_hovered

    def is_pressed(self) -> bool:
        """
        Check if the button is currently pressed.

        Returns:
            True if pressed, False otherwise

        Example:
            >>> if button.is_pressed():
            ...     print("Button is pressed")
        """
        return self._is_pressed
