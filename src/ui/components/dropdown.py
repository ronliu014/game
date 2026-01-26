"""
Dropdown Component

Provides a dropdown/combobox UI component for selecting from a list of options.

Author: Circuit Repair Game Team
Date: 2026-01-26
"""

from typing import Optional, Callable, List, Tuple
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class Dropdown(UIComponent):
    """
    Dropdown component for selecting from a list of options.

    Features:
        - Click to expand/collapse
        - Mouse hover highlighting
        - Callback on selection change
        - Scrollable list (if needed)

    Example:
        >>> def on_select(value):
        ...     print(f"Selected: {value}")
        >>> dropdown = Dropdown(100, 100, 200, 40,
        ...                     options=[("easy", "简单"), ("normal", "普通")],
        ...                     on_select=on_select)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        options: List[Tuple[str, str]],  # List of (value, label) tuples
        selected_value: Optional[str] = None,
        on_select: Optional[Callable[[str], None]] = None,
        font_size: int = 20,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (80, 80, 80),
        hover_color: Tuple[int, int, int] = (120, 120, 120),
        border_color: Tuple[int, int, int] = (150, 150, 150)
    ):
        """
        Initialize the dropdown.

        Args:
            x: X position
            y: Y position
            width: Dropdown width
            height: Height of each option
            options: List of (value, label) tuples
            selected_value: Initially selected value
            on_select: Callback when selection changes
            font_size: Font size for text
            text_color: Text color
            bg_color: Background color
            hover_color: Hover background color
            border_color: Border color
        """
        super().__init__(x, y, width, height)
        self._options = options
        self._selected_value = selected_value or (options[0][0] if options else None)
        self._on_select = on_select
        self._font_size = font_size
        self._text_color = text_color
        self._bg_color = bg_color
        self._hover_color = hover_color
        self._border_color = border_color

        # State
        self._is_expanded = False
        self._hover_index = -1

        # Load font
        try:
            self._font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", font_size)
        except Exception:
            logger.warning("Failed to load Chinese font, using default")
            self._font = pygame.font.Font(None, font_size)

        logger.debug(f"Dropdown created at ({x}, {y}) with {len(options)} options")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the dropdown on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Draw main button (selected value)
        self._draw_main_button(surface)

        # Draw dropdown list if expanded
        if self._is_expanded:
            self._draw_dropdown_list(surface)

    def _draw_main_button(self, surface: pygame.Surface) -> None:
        """Draw the main dropdown button showing selected value."""
        # Background
        pygame.draw.rect(surface, self._bg_color, self.get_rect())
        pygame.draw.rect(surface, self._border_color, self.get_rect(), 2)

        # Selected label text
        label = self._get_label_for_value(self._selected_value)
        text_surface = self._font.render(label, True, self._text_color)
        text_rect = text_surface.get_rect(
            midleft=(self.x + 10, self.y + self.height // 2)
        )
        surface.blit(text_surface, text_rect)

        # Draw arrow indicator
        arrow_x = self.x + self.width - 20
        arrow_y = self.y + self.height // 2
        arrow_points = [
            (arrow_x - 5, arrow_y - 3),
            (arrow_x + 5, arrow_y - 3),
            (arrow_x, arrow_y + 3)
        ]
        pygame.draw.polygon(surface, self._text_color, arrow_points)

    def _draw_dropdown_list(self, surface: pygame.Surface) -> None:
        """Draw the expanded dropdown list."""
        list_y = self.y + self.height

        for i, (value, label) in enumerate(self._options):
            # Determine background color
            if i == self._hover_index:
                bg_color = self._hover_color
            elif value == self._selected_value:
                bg_color = (100, 120, 100)  # Highlight selected
            else:
                bg_color = self._bg_color

            # Draw option background
            option_rect = pygame.Rect(self.x, list_y + i * self.height, self.width, self.height)
            pygame.draw.rect(surface, bg_color, option_rect)
            pygame.draw.rect(surface, self._border_color, option_rect, 1)

            # Draw option text
            text_surface = self._font.render(label, True, self._text_color)
            text_rect = text_surface.get_rect(
                midleft=(self.x + 10, list_y + i * self.height + self.height // 2)
            )
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
            return self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event)

        return False

    def _handle_mouse_motion(self, event: pygame.event.Event) -> bool:
        """Handle mouse motion event."""
        if self._is_expanded:
            # Check if hovering over any option
            list_y = self.y + self.height
            for i in range(len(self._options)):
                option_rect = pygame.Rect(self.x, list_y + i * self.height, self.width, self.height)
                if option_rect.collidepoint(event.pos):
                    self._hover_index = i
                    return True
            self._hover_index = -1
        return False

    def _handle_mouse_click(self, event: pygame.event.Event) -> bool:
        """Handle mouse click event."""
        if event.button != 1:  # Only handle left click
            return False

        # Check if clicking main button
        if self.get_rect().collidepoint(event.pos):
            self._is_expanded = not self._is_expanded
            logger.debug(f"Dropdown {'expanded' if self._is_expanded else 'collapsed'}")
            return True

        # Check if clicking an option (when expanded)
        if self._is_expanded:
            list_y = self.y + self.height
            for i, (value, label) in enumerate(self._options):
                option_rect = pygame.Rect(self.x, list_y + i * self.height, self.width, self.height)
                if option_rect.collidepoint(event.pos):
                    # Select this option
                    old_value = self._selected_value
                    self._selected_value = value
                    self._is_expanded = False
                    logger.info(f"Dropdown option selected: {label} ({value})")

                    # Call callback if value changed
                    if old_value != value and self._on_select:
                        self._on_select(value)
                    return True

            # Clicked outside dropdown while expanded - collapse it
            self._is_expanded = False
            return True

        return False

    def _get_label_for_value(self, value: str) -> str:
        """Get the label for a given value."""
        for v, label in self._options:
            if v == value:
                return label
        return value

    def get_selected_value(self) -> str:
        """
        Get the currently selected value.

        Returns:
            str: Selected value
        """
        return self._selected_value

    def set_selected_value(self, value: str) -> None:
        """
        Set the selected value.

        Args:
            value: Value to select
        """
        if any(v == value for v, _ in self._options):
            self._selected_value = value
            logger.debug(f"Dropdown value set to: {value}")
        else:
            logger.warning(f"Invalid dropdown value: {value}")

    def set_on_select(self, callback: Callable[[str], None]) -> None:
        """
        Set the selection callback.

        Args:
            callback: Function to call when selection changes
        """
        self._on_select = callback

    def is_expanded(self) -> bool:
        """
        Check if dropdown is expanded.

        Returns:
            bool: True if expanded, False otherwise
        """
        return self._is_expanded

    def collapse(self) -> None:
        """Collapse the dropdown."""
        self._is_expanded = False
