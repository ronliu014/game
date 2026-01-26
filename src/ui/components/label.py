"""
Label Component

Provides a text label UI component with multi-line support.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Tuple, List
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class Label(UIComponent):
    """
    Label component for displaying text.

    Supports multi-line text, alignment, and Chinese fonts.

    Attributes:
        text (str): Label text content
        font_size (int): Font size in pixels
        text_color (Tuple[int, int, int]): Text color (r, g, b)
        alignment (str): Text alignment (left/center/right)
        line_spacing (int): Spacing between lines in pixels

    Example:
        >>> label = Label(100, 100, 300, 50, "Hello World", font_size=24)
        >>> label.draw(screen)
    """

    # Alignment constants
    ALIGN_LEFT = 'left'
    ALIGN_CENTER = 'center'
    ALIGN_RIGHT = 'right'

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 20,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        alignment: str = ALIGN_LEFT,
        line_spacing: int = 5,
        word_wrap: bool = True
    ):
        """
        Initialize the label.

        Args:
            x: X position
            y: Y position
            width: Label width (for word wrapping)
            height: Label height
            text: Text content
            font_size: Font size in pixels
            text_color: Text color (r, g, b)
            alignment: Text alignment (left/center/right)
            line_spacing: Spacing between lines
            word_wrap: Enable word wrapping
        """
        super().__init__(x, y, width, height)
        self._text = text
        self._font_size = font_size
        self._text_color = text_color
        self._alignment = alignment
        self._line_spacing = line_spacing
        self._word_wrap = word_wrap

        # Load font
        try:
            self._font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", font_size)
        except Exception:
            logger.warning("Failed to load Chinese font, using default")
            self._font = pygame.font.Font(None, font_size)

        # Cache rendered lines
        self._rendered_lines: List[pygame.Surface] = []
        self._render_text()

        logger.debug(f"Label created at ({x}, {y}) with text: '{text[:20]}...'")

    def _render_text(self) -> None:
        """Render text into lines with word wrapping if enabled."""
        self._rendered_lines = []

        if not self._text:
            return

        if self._word_wrap:
            # Split text into lines that fit within width
            words = self._text.split(' ')
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                test_surface = self._font.render(test_line, True, self._text_color)

                if test_surface.get_width() <= self.width:
                    current_line = test_line
                else:
                    # Current line is full, render it
                    if current_line:
                        line_surface = self._font.render(current_line.strip(), True, self._text_color)
                        self._rendered_lines.append(line_surface)
                    current_line = word + " "

            # Render remaining text
            if current_line:
                line_surface = self._font.render(current_line.strip(), True, self._text_color)
                self._rendered_lines.append(line_surface)
        else:
            # No word wrap, split by newlines only
            lines = self._text.split('\n')
            for line in lines:
                line_surface = self._font.render(line, True, self._text_color)
                self._rendered_lines.append(line_surface)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the label on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible or not self._rendered_lines:
            return

        current_y = self.y
        line_height = self._font.get_height()

        for line_surface in self._rendered_lines:
            # Calculate x position based on alignment
            if self._alignment == self.ALIGN_CENTER:
                line_x = self.x + (self.width - line_surface.get_width()) // 2
            elif self._alignment == self.ALIGN_RIGHT:
                line_x = self.x + self.width - line_surface.get_width()
            else:  # ALIGN_LEFT
                line_x = self.x

            # Draw the line
            surface.blit(line_surface, (line_x, current_y))
            current_y += line_height + self._line_spacing

            # Stop if we exceed the label height
            if current_y > self.y + self.height:
                break

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event (labels don't handle events by default).

        Args:
            event: Pygame event to handle

        Returns:
            bool: False (labels don't handle events)
        """
        return False

    def set_text(self, text: str) -> None:
        """
        Set the label text.

        Args:
            text: New text content
        """
        self._text = text
        self._render_text()

    def get_text(self) -> str:
        """
        Get the label text.

        Returns:
            str: Current text content
        """
        return self._text

    def set_text_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set the text color.

        Args:
            color: Text color (r, g, b)
        """
        self._text_color = color
        self._render_text()

    def set_alignment(self, alignment: str) -> None:
        """
        Set the text alignment.

        Args:
            alignment: Text alignment (left/center/right)
        """
        if alignment in [self.ALIGN_LEFT, self.ALIGN_CENTER, self.ALIGN_RIGHT]:
            self._alignment = alignment
        else:
            logger.warning(f"Invalid alignment: {alignment}")

    def set_font_size(self, font_size: int) -> None:
        """
        Set the font size.

        Args:
            font_size: Font size in pixels
        """
        self._font_size = font_size
        try:
            self._font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", font_size)
        except Exception:
            self._font = pygame.font.Font(None, font_size)
        self._render_text()
