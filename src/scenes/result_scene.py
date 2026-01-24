"""
Result Scene

Provides the game result screen (victory/failure).

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Dict, Any
import pygame
from src.scenes.scene_base import SceneBase
from src.ui.components.button import Button
from src.ui.components.panel import Panel
from src.ui.components.label import Label
from src.ui.components.image import Image
from src.ui.layouts.layout_manager import LayoutManager
from src.rendering.effects.fireworks_effect import FireworksEffect
from src.rendering.effects.smoke_effect import SmokeEffect
from src.progression.level_progression import LevelProgressionManager
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class ResultScene(SceneBase):
    """
    Result scene for displaying game completion results.

    Shows victory or failure screen with statistics and options.

    Features:
        - Victory/Failure message
        - Star rating (1-3 stars based on performance)
        - Statistics panel (time, moves, etc.)
        - Next level / Retry / Exit buttons
        - Particle effects (fireworks for victory)

    Example:
        >>> scene = ResultScene(scene_manager)
        >>> scene.on_enter(data={
        ...     'victory': True,
        ...     'level': 1,
        ...     'time_taken': 45.5,
        ...     'moves': 12,
        ...     'stars': 3
        ... })
    """

    def __init__(self, scene_manager=None):
        """
        Initialize the result scene.

        Args:
            scene_manager: Reference to the scene manager
        """
        super().__init__(scene_manager)

        # Screen dimensions
        self._screen_width = 800
        self._screen_height = 600

        # UI components
        self._background_panel: Optional[Panel] = None
        self._result_panel: Optional[Panel] = None
        self._title_label: Optional[Label] = None
        self._message_label: Optional[Label] = None
        self._stats_labels: Dict[str, Label] = {}
        self._star_images: list = []
        self._next_button: Optional[Button] = None
        self._retry_button: Optional[Button] = None
        self._menu_button: Optional[Button] = None

        # Layout manager
        self._layout: Optional[LayoutManager] = None

        # Result data
        self._is_victory = False
        self._level = 1
        self._time_taken = 0.0
        self._moves = 0
        self._stars = 0
        self._difficulty = 'normal'
        self._is_new_best = False
        self._unlocked_levels = []

        # Progression manager
        self._progression_manager: Optional[LevelProgressionManager] = None

        # Animation state
        self._animation_time = 0.0
        self._stars_revealed = 0
        self._star_reveal_interval = 500.0  # ms between star reveals

        # Particle effects
        self._fireworks_effect: Optional[FireworksEffect] = None
        self._smoke_effect: Optional[SmokeEffect] = None

        logger.debug("ResultScene initialized")

    def on_enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when the scene becomes active.

        Args:
            data: Optional data containing:
                - victory (bool): Whether the player won
                - level (int): Level number
                - time_taken (float): Time taken in seconds
                - moves (int): Number of moves made
                - stars (int): Star rating (1-3)
                - difficulty (str): Difficulty level
                - screen_width (int): Screen width
                - screen_height (int): Screen height
        """
        super().on_enter(data)

        # Get screen dimensions
        self._screen_width = self.get_transition_data('screen_width', 800)
        self._screen_height = self.get_transition_data('screen_height', 600)

        # Get result data
        self._is_victory = self.get_transition_data('victory', False)
        self._level = self.get_transition_data('level', 1)
        self._time_taken = self.get_transition_data('time_taken', 0.0)
        self._moves = self.get_transition_data('moves', 0)
        self._stars = self.get_transition_data('stars', 0)
        self._difficulty = self.get_transition_data('difficulty', 'normal')

        # Initialize layout manager
        self._layout = LayoutManager(self._screen_width, self._screen_height)

        # Initialize progression manager
        self._progression_manager = LevelProgressionManager()

        # Save progress if victory
        if self._is_victory:
            self._save_progress()

        # Initialize particle effects
        self._fireworks_effect = FireworksEffect(self._screen_width, self._screen_height)
        self._smoke_effect = SmokeEffect(self._screen_width, self._screen_height)

        # Create UI components
        self._create_background()
        self._create_result_panel()
        self._create_title()
        self._create_message()
        self._create_statistics()
        self._create_star_display()
        self._create_buttons()

        # Reset animation state
        self._animation_time = 0.0
        self._stars_revealed = 0

        # Start appropriate particle effect
        if self._is_victory:
            self._fireworks_effect.start()
        else:
            # Start smoke at center of result panel
            panel_center_x = self._result_panel.x + self._result_panel.width // 2
            panel_center_y = self._result_panel.y + self._result_panel.height // 2
            self._smoke_effect.start(panel_center_x, panel_center_y)

        logger.info(f"ResultScene entered: victory={self._is_victory}, level={self._level}, stars={self._stars}")

    def _save_progress(self) -> None:
        """Save level completion progress."""
        if not self._progression_manager:
            return

        try:
            # Complete the level and save progress
            result = self._progression_manager.complete_level(
                level_id=self._level,
                stars=self._stars,
                time=self._time_taken,
                moves=self._moves,
                auto_save=True
            )

            self._is_new_best = result['is_new_best']
            self._unlocked_levels = result['unlocked_levels']

            logger.info(f"Progress saved: new_best={self._is_new_best}, unlocked={self._unlocked_levels}")

        except Exception as e:
            logger.error(f"Failed to save progress: {e}")

    def on_exit(self) -> None:
        """Called when the scene is being replaced or removed."""
        super().on_exit()

        # Stop particle effects
        if self._fireworks_effect:
            self._fireworks_effect.stop()
        if self._smoke_effect:
            self._smoke_effect.stop()

        logger.info("ResultScene exited")

    def update(self, delta_ms: float) -> None:
        """
        Update scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Update animation time
        self._animation_time += delta_ms

        # Reveal stars one by one
        if self._is_victory and self._stars_revealed < self._stars:
            stars_to_reveal = int(self._animation_time / self._star_reveal_interval)
            if stars_to_reveal > self._stars_revealed:
                self._stars_revealed = min(stars_to_reveal, self._stars)
                logger.debug(f"Revealed {self._stars_revealed} stars")

        # Update particle effects
        if self._fireworks_effect:
            self._fireworks_effect.update(delta_ms)
        if self._smoke_effect:
            self._smoke_effect.update(delta_ms)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the scene.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw background
        if self._background_panel:
            self._background_panel.draw(surface)

        # Draw particle effects (behind UI for victory, in front for failure)
        if not self._is_victory and self._smoke_effect:
            self._smoke_effect.draw(surface)

        # Draw result panel
        if self._result_panel:
            self._result_panel.draw(surface)

        # Draw title
        if self._title_label:
            self._title_label.draw(surface)

        # Draw message
        if self._message_label:
            self._message_label.draw(surface)

        # Draw statistics
        for label in self._stats_labels.values():
            label.draw(surface)

        # Draw stars (only revealed ones)
        for i in range(self._stars_revealed):
            if i < len(self._star_images):
                self._star_images[i].draw(surface)

        # Draw buttons
        if self._next_button:
            self._next_button.draw(surface)
        if self._retry_button:
            self._retry_button.draw(surface)
        if self._menu_button:
            self._menu_button.draw(surface)

        # Draw fireworks on top for victory
        if self._is_victory and self._fireworks_effect:
            self._fireworks_effect.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        # Handle button events
        if self._next_button and self._next_button.handle_event(event):
            return True
        if self._retry_button and self._retry_button.handle_event(event):
            return True
        if self._menu_button and self._menu_button.handle_event(event):
            return True

        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_menu_clicked()
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self._is_victory:
                    self._on_next_clicked()
                else:
                    self._on_retry_clicked()
                return True
            elif event.key == pygame.K_r:
                self._on_retry_clicked()
                return True

        return False

    def _create_background(self) -> None:
        """Create the background panel."""
        # Different background colors for victory/failure
        if self._is_victory:
            bg_color = (20, 40, 30)  # Dark green tint
        else:
            bg_color = (40, 20, 20)  # Dark red tint

        self._background_panel = Panel(
            0, 0,
            self._screen_width,
            self._screen_height,
            background_color=bg_color,
            alpha=255
        )

    def _create_result_panel(self) -> None:
        """Create the main result panel."""
        panel_width = 500
        panel_height = 450

        self._result_panel = Panel(
            0, 0,
            panel_width,
            panel_height,
            background_color=(40, 40, 50),
            border_color=(150, 150, 150),
            border_width=3,
            alpha=240
        )

        # Center the panel
        self._layout.center_component(self._result_panel)

    def _create_title(self) -> None:
        """Create the title label."""
        if self._is_victory:
            title_text = "🎉 胜利！"
            title_color = (100, 255, 100)
        else:
            title_text = "💔 失败"
            title_color = (255, 100, 100)

        self._title_label = Label(
            0, 0,
            500, 80,
            title_text,
            font_size=48,
            text_color=title_color,
            alignment=Label.ALIGN_CENTER
        )

        # Position at top of result panel
        panel_x = self._result_panel.x
        panel_y = self._result_panel.y
        self._title_label.set_position(panel_x, panel_y + 20)

    def _create_message(self) -> None:
        """Create the message label."""
        if self._is_victory:
            message_text = f"恭喜完成第 {self._level} 关！"
        else:
            message_text = "时间到了，再试一次吧！"

        self._message_label = Label(
            0, 0,
            500, 40,
            message_text,
            font_size=20,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_CENTER
        )

        # Position below title
        panel_x = self._result_panel.x
        panel_y = self._result_panel.y
        self._message_label.set_position(panel_x, panel_y + 100)

    def _create_statistics(self) -> None:
        """Create statistics labels."""
        panel_x = self._result_panel.x
        panel_y = self._result_panel.y

        # Format time
        minutes = int(self._time_taken // 60)
        seconds = int(self._time_taken % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"

        # Create stat labels
        stats = [
            ("难度", self._get_difficulty_name()),
            ("用时", time_str),
            ("移动次数", str(self._moves))
        ]

        start_y = panel_y + 200
        label_height = 35
        spacing = 10

        for i, (key, value) in enumerate(stats):
            # Key label
            key_label = Label(
                panel_x + 80, start_y + i * (label_height + spacing),
                150, label_height,
                f"{key}:",
                font_size=20,
                text_color=(180, 180, 180),
                alignment=Label.ALIGN_RIGHT
            )
            self._stats_labels[f"{key}_key"] = key_label

            # Value label
            value_label = Label(
                panel_x + 240, start_y + i * (label_height + spacing),
                150, label_height,
                value,
                font_size=20,
                text_color=(255, 255, 100),
                alignment=Label.ALIGN_LEFT
            )
            self._stats_labels[f"{key}_value"] = value_label

    def _create_star_display(self) -> None:
        """Create star rating display."""
        if not self._is_victory or self._stars <= 0:
            return

        panel_x = self._result_panel.x
        panel_y = self._result_panel.y

        star_size = 50
        star_spacing = 10
        total_width = self._stars * star_size + (self._stars - 1) * star_spacing
        start_x = panel_x + (500 - total_width) // 2
        star_y = panel_y + 320

        # Create star placeholders (will be filled with actual stars later)
        for i in range(self._stars):
            # For now, create colored panels as star placeholders
            star_panel = Panel(
                start_x + i * (star_size + star_spacing),
                star_y,
                star_size,
                star_size,
                background_color=(255, 215, 0),  # Gold color
                border_color=(255, 255, 100),
                border_width=2
            )
            self._star_images.append(star_panel)

    def _create_buttons(self) -> None:
        """Create action buttons."""
        button_width = 140
        button_height = 50
        button_spacing = 15

        panel_x = self._result_panel.x
        panel_y = self._result_panel.y
        button_y = panel_y + 390

        if self._is_victory:
            # Victory: Next Level + Retry + Menu
            self._next_button = Button(
                0, button_y,
                button_width, button_height,
                "下一关",
                on_click=self._on_next_clicked,
                font_size=20
            )

            self._retry_button = Button(
                0, button_y,
                button_width, button_height,
                "重试",
                on_click=self._on_retry_clicked,
                font_size=20
            )

            self._menu_button = Button(
                0, button_y,
                button_width, button_height,
                "主菜单",
                on_click=self._on_menu_clicked,
                font_size=20
            )

            # Arrange buttons horizontally
            buttons = [self._next_button, self._retry_button, self._menu_button]
            total_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
            start_x = panel_x + (500 - total_width) // 2

            for i, button in enumerate(buttons):
                button.set_position(start_x + i * (button_width + button_spacing), button_y)

        else:
            # Failure: Retry + Menu
            self._retry_button = Button(
                0, button_y,
                button_width, button_height,
                "重试",
                on_click=self._on_retry_clicked,
                font_size=20
            )

            self._menu_button = Button(
                0, button_y,
                button_width, button_height,
                "主菜单",
                on_click=self._on_menu_clicked,
                font_size=20
            )

            # Arrange buttons horizontally
            buttons = [self._retry_button, self._menu_button]
            total_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
            start_x = panel_x + (500 - total_width) // 2

            for i, button in enumerate(buttons):
                button.set_position(start_x + i * (button_width + button_spacing), button_y)

    def _get_difficulty_name(self) -> str:
        """
        Get the localized difficulty name.

        Returns:
            str: Difficulty name in Chinese
        """
        difficulty_names = {
            'easy': '简单',
            'normal': '普通',
            'hard': '困难',
            'hell': '地狱'
        }
        return difficulty_names.get(self._difficulty, '未知')

    def _on_next_clicked(self) -> None:
        """Handle next level button click."""
        logger.info("Next level button clicked")
        # TODO: Transition to next level
        # self.request_scene_change(LoadingScene, data={
        #     'next_scene': GameplayScene,
        #     'level': self._level + 1,
        #     'difficulty': self._difficulty
        # })

    def _on_retry_clicked(self) -> None:
        """Handle retry button click."""
        logger.info("Retry button clicked")
        # TODO: Restart current level
        # self.request_scene_change(LoadingScene, data={
        #     'next_scene': GameplayScene,
        #     'level': self._level,
        #     'difficulty': self._difficulty
        # })

    def _on_menu_clicked(self) -> None:
        """Handle menu button click."""
        logger.info("Menu button clicked")
        # TODO: Return to main menu
        # from src.scenes.main_menu_scene import MainMenuScene
        # self.request_scene_change(MainMenuScene, data={
        #     'screen_width': self._screen_width,
        #     'screen_height': self._screen_height
        # })

    def get_result_data(self) -> Dict[str, Any]:
        """
        Get the result data.

        Returns:
            Dict containing result information
        """
        return {
            'victory': self._is_victory,
            'level': self._level,
            'time_taken': self._time_taken,
            'moves': self._moves,
            'stars': self._stars,
            'difficulty': self._difficulty
        }
