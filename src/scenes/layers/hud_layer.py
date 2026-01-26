"""
HUD Layer

Provides heads-up display for game information.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
from typing import Optional, Callable
from src.scenes.layers.layer_base import LayerBase
from src.ui.components.panel import Panel
from src.ui.components.label import Label
from src.ui.components.button import Button
from src.core.timer.game_timer import GameTimer
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class HUDLayer(LayerBase):
    """
    HUD (Heads-Up Display) layer for game information.

    Displays:
        - Level information
        - Move counter
        - Countdown timer
        - Pause/Exit button

    Features:
        - Dynamic timer color (green/yellow/red)
        - Move counter
        - Level display
        - Pause button

    Example:
        >>> timer = GameTimer(60.0)
        >>> layer = HUDLayer(800, 600, level=1, timer=timer)
        >>> layer.update(16.67)
        >>> layer.draw(screen)
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        level: int = 1,
        difficulty: str = 'normal',
        timer: Optional[GameTimer] = None,
        on_pause: Optional[Callable[[], None]] = None,
        on_exit: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the HUD layer.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            level: Current level number
            difficulty: Difficulty level
            timer: GameTimer instance
            on_pause: Callback for pause button
            on_exit: Callback for exit button
        """
        super().__init__(screen_width, screen_height)

        self._level = level
        self._difficulty = difficulty
        self._timer = timer
        self._move_count = 0
        self._on_pause = on_pause
        self._on_exit = on_exit
        self._is_paused = False

        # Cache for avoiding unnecessary updates
        self._last_timer_text = ""
        self._last_timer_color = (0, 255, 0)

        # UI components
        self._hud_panel: Optional[Panel] = None
        self._level_label: Optional[Label] = None
        self._timer_label: Optional[Label] = None
        self._moves_label: Optional[Label] = None
        self._debug_button: Optional[Button] = None
        self._pause_button: Optional[Button] = None
        self._exit_button: Optional[Button] = None

        # Debug toggle callback
        self._on_debug_toggle: Optional[Callable[[], None]] = None

        # Create UI
        self._create_ui()

        logger.debug(f"HUDLayer initialized for level {level}")

    def _create_ui(self) -> None:
        """Create HUD UI components."""
        # HUD panel (top bar)
        panel_height = 60
        self._hud_panel = Panel(
            0, 0,
            self._screen_width,
            panel_height,
            background_color=(30, 30, 40),
            border_color=(100, 100, 100),
            border_width=2,
            alpha=220
        )

        # Level label (left)
        difficulty_names = {
            'easy': '简单',
            'normal': '普通',
            'hard': '困难',
            'hell': '地狱'
        }
        difficulty_text = difficulty_names.get(self._difficulty, '未知')

        self._level_label = Label(
            10, 10,
            200, 40,
            f"关卡 {self._level} - {difficulty_text}",
            font_size=20,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_LEFT
        )

        # Timer label (center)
        timer_text = self._timer.format_time() if self._timer else "00:00"
        self._timer_label = Label(
            self._screen_width // 2 - 100, 10,
            200, 40,
            timer_text,
            font_size=28,
            text_color=(0, 255, 0),
            alignment=Label.ALIGN_CENTER
        )

        # Moves label (right-center)
        self._moves_label = Label(
            self._screen_width - 380, 10,
            100, 40,
            f"移动: {self._move_count}",
            font_size=20,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_RIGHT
        )

        # Debug button (right side, before exit/pause buttons)
        self._debug_button = Button(
            self._screen_width - 270, 10,
            80, 40,
            "调试",
            on_click=self._on_debug_clicked,
            font_size=18
        )

        # Exit button (far right)
        self._exit_button = Button(
            self._screen_width - 180, 10,
            80, 40,
            "退出",
            on_click=self._on_exit_clicked,
            font_size=18
        )

        # Pause button (next to exit button)
        self._pause_button = Button(
            self._screen_width - 90, 10,
            80, 40,
            "暂停",
            on_click=self._on_pause_clicked,
            font_size=18
        )

    def update(self, delta_ms: float) -> None:
        """
        Update HUD layer.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if not self._enabled:
            logger.warning(f"HUD update skipped - layer disabled")
            return

        # Update timer display (only if changed)
        if self._timer and self._timer_label:
            timer_text = self._timer.format_time()

            # Only update if text changed
            if timer_text != self._last_timer_text:
                logger.debug(f"Timer text changed: {self._last_timer_text} -> {timer_text}")
                self._timer_label.set_text(timer_text)
                self._last_timer_text = timer_text

            # Only update color if changed
            color = self._timer.get_color_hint()
            if color != self._last_timer_color:
                logger.debug(f"Timer color changed: {self._last_timer_color} -> {color}")
                self._timer_label.set_text_color(color)
                self._last_timer_color = color

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the HUD.

        Args:
            surface: Pygame surface to draw on
        """
        if not self._visible:
            logger.warning(f"HUD draw skipped - layer invisible")
            return

        logger.debug(f"HUD drawing - visible={self._visible}, enabled={self._enabled}")

        # Draw HUD panel
        if self._hud_panel:
            self._hud_panel.draw(surface)

        # Draw labels
        if self._level_label:
            self._level_label.draw(surface)
        if self._timer_label:
            self._timer_label.draw(surface)
        if self._moves_label:
            self._moves_label.draw(surface)

        # Draw buttons
        if self._debug_button:
            self._debug_button.draw(surface)
        if self._exit_button:
            self._exit_button.draw(surface)
        if self._pause_button:
            self._pause_button.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if event was handled, False otherwise
        """
        if not self._enabled:
            return False

        # Handle debug button
        if self._debug_button and self._debug_button.handle_event(event):
            return True

        # Handle exit button
        if self._exit_button and self._exit_button.handle_event(event):
            return True

        # Handle pause button
        if self._pause_button and self._pause_button.handle_event(event):
            return True

        return False

    def set_move_count(self, count: int) -> None:
        """
        Set move counter.

        Args:
            count: Number of moves
        """
        self._move_count = count
        if self._moves_label:
            self._moves_label.set_text(f"移动: {count}")

    def increment_move_count(self) -> None:
        """Increment move counter by 1."""
        self.set_move_count(self._move_count + 1)

    def get_move_count(self) -> int:
        """
        Get current move count.

        Returns:
            int: Number of moves
        """
        return self._move_count

    def set_timer(self, timer: GameTimer) -> None:
        """
        Set the game timer.

        Args:
            timer: GameTimer instance
        """
        self._timer = timer

    def get_timer(self) -> Optional[GameTimer]:
        """
        Get the game timer.

        Returns:
            Optional[GameTimer]: The timer instance
        """
        return self._timer

    def _on_pause_clicked(self) -> None:
        """Handle pause button click."""
        self._is_paused = not self._is_paused

        # Update button text based on pause state
        if self._pause_button:
            if self._is_paused:
                self._pause_button.set_label("继续")
                logger.info("Game paused")
            else:
                self._pause_button.set_label("暂停")
                logger.info("Game resumed")

        # Call the pause callback
        if self._on_pause:
            self._on_pause()

    def _on_exit_clicked(self) -> None:
        """Handle exit button click."""
        logger.info("Exit button clicked")
        if self._on_exit:
            self._on_exit()

    def _on_debug_clicked(self) -> None:
        """Handle debug button click."""
        logger.info("Debug button clicked")
        if self._on_debug_toggle:
            self._on_debug_toggle()

    def set_paused(self, is_paused: bool) -> None:
        """
        Set the pause state.

        Args:
            is_paused: Whether the game is paused
        """
        self._is_paused = is_paused
        if self._pause_button:
            if is_paused:
                self._pause_button.set_label("继续")
            else:
                self._pause_button.set_label("暂停")

    def is_paused(self) -> bool:
        """
        Get the pause state.

        Returns:
            bool: True if paused, False otherwise
        """
        return self._is_paused

    def set_pause_callback(self, callback: Callable[[], None]) -> None:
        """
        Set pause button callback.

        Args:
            callback: Function to call when pause is clicked
        """
        self._on_pause = callback
        if self._pause_button:
            self._pause_button.set_on_click(callback)

    def set_debug_toggle_callback(self, callback: Callable[[], None]) -> None:
        """
        Set debug toggle button callback.

        Args:
            callback: Function to call when debug button is clicked
        """
        self._on_debug_toggle = callback
