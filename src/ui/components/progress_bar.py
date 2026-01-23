"""
ProgressBar Component

Provides a progress bar UI component with animation support.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Tuple
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class ProgressBar(UIComponent):
    """
    Progress bar component for displaying progress.

    Supports smooth animation, custom colors, and percentage display.

    Attributes:
        progress (float): Current progress value (0.0 to 1.0)
        bar_color (Tuple[int, int, int]): Progress bar color
        background_color (Tuple[int, int, int]): Background color
        border_color (Optional[Tuple[int, int, int]]): Border color
        show_percentage (bool): Whether to show percentage text

    Example:
        >>> progress_bar = ProgressBar(100, 100, 300, 30, bar_color=(0, 255, 0))
        >>> progress_bar.set_progress(0.75)  # 75%
        >>> progress_bar.draw(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        bar_color: Tuple[int, int, int] = (0, 200, 0),
        background_color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Optional[Tuple[int, int, int]] = (200, 200, 200),
        border_width: int = 2,
        show_percentage: bool = True,
        animation_speed: float = 2.0
    ):
        """
        Initialize the progress bar.

        Args:
            x: X position
            y: Y position
            width: Progress bar width
            height: Progress bar height
            bar_color: Progress bar fill color (r, g, b)
            background_color: Background color (r, g, b)
            border_color: Border color (r, g, b), None for no border
            border_width: Border width in pixels
            show_percentage: Whether to display percentage text
            animation_speed: Animation speed (progress units per second)
        """
        super().__init__(x, y, width, height)
        self._bar_color = bar_color
        self._background_color = background_color
        self._border_color = border_color
        self._border_width = border_width
        self._show_percentage = show_percentage
        self._animation_speed = animation_speed

        # Progress values
        self._target_progress = 0.0  # Target progress (0.0 to 1.0)
        self._current_progress = 0.0  # Current animated progress
        self._min_progress = 0.0
        self._max_progress = 1.0

        # Load font for percentage text
        try:
            self._font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", 16)
        except Exception:
            logger.warning("Failed to load Chinese font, using default")
            self._font = pygame.font.Font(None, 16)

        logger.debug(f"ProgressBar created at ({x}, {y}) with size ({width}, {height})")

    def update(self, delta_ms: float) -> None:
        """
        Update progress animation.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if self._current_progress != self._target_progress:
            # Animate progress towards target
            delta_seconds = delta_ms / 1000.0
            progress_change = self._animation_speed * delta_seconds

            if self._current_progress < self._target_progress:
                self._current_progress = min(
                    self._current_progress + progress_change,
                    self._target_progress
                )
            else:
                self._current_progress = max(
                    self._current_progress - progress_change,
                    self._target_progress
                )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the progress bar on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Draw background
        pygame.draw.rect(
            surface,
            self._background_color,
            (self.x, self.y, self.width, self.height)
        )

        # Draw progress bar
        progress_width = int(self.width * self._current_progress)
        if progress_width > 0:
            pygame.draw.rect(
                surface,
                self._bar_color,
                (self.x, self.y, progress_width, self.height)
            )

        # Draw border
        if self._border_color and self._border_width > 0:
            pygame.draw.rect(
                surface,
                self._border_color,
                (self.x, self.y, self.width, self.height),
                self._border_width
            )

        # Draw percentage text
        if self._show_percentage:
            percentage = int(self._current_progress * 100)
            text = f"{percentage}%"
            text_surface = self._font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2)
            )
            surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event (progress bars don't handle events by default).

        Args:
            event: Pygame event to handle

        Returns:
            bool: False (progress bars don't handle events)
        """
        return False

    def set_progress(self, progress: float) -> None:
        """
        Set the target progress value.

        Args:
            progress: Progress value (0.0 to 1.0)
        """
        self._target_progress = max(self._min_progress, min(self._max_progress, progress))
        logger.debug(f"Progress set to {self._target_progress:.2%}")

    def set_progress_immediate(self, progress: float) -> None:
        """
        Set the progress value immediately without animation.

        Args:
            progress: Progress value (0.0 to 1.0)
        """
        self._target_progress = max(self._min_progress, min(self._max_progress, progress))
        self._current_progress = self._target_progress

    def get_progress(self) -> float:
        """
        Get the current progress value.

        Returns:
            float: Current progress (0.0 to 1.0)
        """
        return self._current_progress

    def get_target_progress(self) -> float:
        """
        Get the target progress value.

        Returns:
            float: Target progress (0.0 to 1.0)
        """
        return self._target_progress

    def set_colors(
        self,
        bar_color: Optional[Tuple[int, int, int]] = None,
        background_color: Optional[Tuple[int, int, int]] = None,
        border_color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """
        Set the progress bar colors.

        Args:
            bar_color: Progress bar fill color (r, g, b)
            background_color: Background color (r, g, b)
            border_color: Border color (r, g, b)
        """
        if bar_color is not None:
            self._bar_color = bar_color
        if background_color is not None:
            self._background_color = background_color
        if border_color is not None:
            self._border_color = border_color

    def set_show_percentage(self, show: bool) -> None:
        """
        Set whether to show percentage text.

        Args:
            show: True to show percentage, False to hide
        """
        self._show_percentage = show

    def reset(self) -> None:
        """Reset progress to 0."""
        self._target_progress = 0.0
        self._current_progress = 0.0
