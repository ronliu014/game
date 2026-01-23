"""
Main Menu Scene

Provides the main menu interface for the game.

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
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class MainMenuScene(SceneBase):
    """
    Main menu scene.

    Displays the game title, difficulty selection, and start/exit buttons.

    Features:
        - Game logo/title
        - Difficulty selection (Easy/Normal/Hard/Hell)
        - Start game button
        - Exit button
        - Background image/color

    Example:
        >>> scene = MainMenuScene(scene_manager)
        >>> scene.on_enter()
    """

    # Difficulty levels
    DIFFICULTY_EASY = 'easy'
    DIFFICULTY_NORMAL = 'normal'
    DIFFICULTY_HARD = 'hard'
    DIFFICULTY_HELL = 'hell'

    def __init__(self, scene_manager=None):
        """
        Initialize the main menu scene.

        Args:
            scene_manager: Reference to the scene manager
        """
        super().__init__(scene_manager)

        # Screen dimensions (will be set in on_enter)
        self._screen_width = 800
        self._screen_height = 600

        # UI components
        self._background_panel: Optional[Panel] = None
        self._title_label: Optional[Label] = None
        self._logo_image: Optional[Image] = None
        self._difficulty_label: Optional[Label] = None
        self._difficulty_buttons: Dict[str, Button] = {}
        self._start_button: Optional[Button] = None
        self._exit_button: Optional[Button] = None

        # Layout manager
        self._layout: Optional[LayoutManager] = None

        # State
        self._selected_difficulty = self.DIFFICULTY_NORMAL

        logger.debug("MainMenuScene initialized")

    def on_enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when the scene becomes active.

        Args:
            data: Optional data passed from previous scene
        """
        super().on_enter(data)

        # Get screen dimensions from data or use defaults
        self._screen_width = self.get_transition_data('screen_width', 800)
        self._screen_height = self.get_transition_data('screen_height', 600)

        # Initialize layout manager
        self._layout = LayoutManager(self._screen_width, self._screen_height)

        # Create UI components
        self._create_background()
        self._create_title()
        self._create_difficulty_selection()
        self._create_buttons()

        logger.info("MainMenuScene entered")

    def on_exit(self) -> None:
        """Called when the scene is being replaced or removed."""
        super().on_exit()
        logger.info("MainMenuScene exited")

    def update(self, delta_ms: float) -> None:
        """
        Update scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Update UI components if needed
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the scene.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw background
        if self._background_panel:
            self._background_panel.draw(surface)

        # Draw logo
        if self._logo_image:
            self._logo_image.draw(surface)

        # Draw title
        if self._title_label:
            self._title_label.draw(surface)

        # Draw difficulty label
        if self._difficulty_label:
            self._difficulty_label.draw(surface)

        # Draw difficulty buttons
        for button in self._difficulty_buttons.values():
            button.draw(surface)

        # Draw action buttons
        if self._start_button:
            self._start_button.draw(surface)
        if self._exit_button:
            self._exit_button.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        # Handle difficulty button events
        for button in self._difficulty_buttons.values():
            if button.handle_event(event):
                return True

        # Handle action button events
        if self._start_button and self._start_button.handle_event(event):
            return True
        if self._exit_button and self._exit_button.handle_event(event):
            return True

        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_exit_clicked()
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._on_start_clicked()
                return True

        return False

    def _create_background(self) -> None:
        """Create the background panel."""
        # Create background with dark color
        self._background_panel = Panel(
            0, 0,
            self._screen_width,
            self._screen_height,
            background_color=(30, 30, 40),
            alpha=255
        )

    def _create_title(self) -> None:
        """Create the title/logo."""
        # Create title label
        self._title_label = Label(
            0, 0,
            self._screen_width,
            100,
            "电路修复游戏",
            font_size=48,
            text_color=(255, 200, 100),
            alignment=Label.ALIGN_CENTER
        )

        # Position title at top center
        self._layout.anchor_component(
            self._title_label,
            LayoutManager.ANCHOR_TOP_CENTER,
            margin_y=50
        )

        # TODO: Load logo image when available
        # self._logo_image = Image(...)

    def _create_difficulty_selection(self) -> None:
        """Create difficulty selection UI."""
        # Create difficulty label
        self._difficulty_label = Label(
            0, 0,
            300, 40,
            "选择难度：",
            font_size=24,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_CENTER
        )

        # Position difficulty label
        self._layout.center_component(
            self._difficulty_label,
            horizontal=True,
            vertical=False,
            offset_y=-80
        )

        # Create difficulty buttons
        difficulties = [
            (self.DIFFICULTY_EASY, "简单 (60秒)"),
            (self.DIFFICULTY_NORMAL, "普通 (45秒)"),
            (self.DIFFICULTY_HARD, "困难 (30秒)"),
            (self.DIFFICULTY_HELL, "地狱 (15秒)")
        ]

        button_width = 150
        button_height = 50
        button_spacing = 20

        for i, (difficulty, label) in enumerate(difficulties):
            button = Button(
                0, 0,
                button_width,
                button_height,
                label,
                on_click=lambda d=difficulty: self._on_difficulty_selected(d),
                font_size=18
            )
            self._difficulty_buttons[difficulty] = button

        # Arrange difficulty buttons horizontally
        buttons_list = [self._difficulty_buttons[d] for d, _ in difficulties]
        self._layout.arrange_horizontal(
            buttons_list,
            start_y=self._screen_height // 2 - 20,
            spacing=button_spacing,
            center_vertical=False
        )

        # Center the group horizontally
        total_width = len(difficulties) * button_width + (len(difficulties) - 1) * button_spacing
        start_x = (self._screen_width - total_width) // 2
        for i, button in enumerate(buttons_list):
            button.set_position(start_x + i * (button_width + button_spacing), button.y)

        # Highlight selected difficulty
        self._update_difficulty_buttons()

    def _create_buttons(self) -> None:
        """Create action buttons (Start, Exit)."""
        button_width = 200
        button_height = 60

        # Create start button
        self._start_button = Button(
            0, 0,
            button_width,
            button_height,
            "开始游戏",
            on_click=self._on_start_clicked,
            font_size=24
        )

        # Create exit button
        self._exit_button = Button(
            0, 0,
            button_width,
            button_height,
            "退出游戏",
            on_click=self._on_exit_clicked,
            font_size=24
        )

        # Arrange buttons vertically
        self._layout.arrange_vertical(
            [self._start_button, self._exit_button],
            start_y=self._screen_height // 2 + 80,
            spacing=20,
            center_horizontal=True
        )

    def _on_difficulty_selected(self, difficulty: str) -> None:
        """
        Handle difficulty selection.

        Args:
            difficulty: Selected difficulty level
        """
        self._selected_difficulty = difficulty
        self._update_difficulty_buttons()
        logger.info(f"Difficulty selected: {difficulty}")

    def _update_difficulty_buttons(self) -> None:
        """Update difficulty button states to reflect selection."""
        for difficulty, button in self._difficulty_buttons.items():
            if difficulty == self._selected_difficulty:
                # Highlight selected button
                button.set_colors({
                    Button.STATE_NORMAL: (100, 150, 100),
                    Button.STATE_HOVER: (120, 170, 120),
                    Button.STATE_PRESSED: (80, 130, 80),
                    Button.STATE_DISABLED: (60, 60, 60)
                })
            else:
                # Normal button colors
                button.set_colors({
                    Button.STATE_NORMAL: (100, 100, 100),
                    Button.STATE_HOVER: (150, 150, 150),
                    Button.STATE_PRESSED: (80, 80, 80),
                    Button.STATE_DISABLED: (60, 60, 60)
                })

    def _on_start_clicked(self) -> None:
        """Handle start button click."""
        logger.info(f"Starting game with difficulty: {self._selected_difficulty}")

        # TODO: Transition to loading scene or gameplay scene
        # For now, just log the action
        # self.request_scene_change(LoadingScene, data={
        #     'difficulty': self._selected_difficulty
        # })

    def _on_exit_clicked(self) -> None:
        """Handle exit button click."""
        logger.info("Exit button clicked")

        # Post quit event
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def get_selected_difficulty(self) -> str:
        """
        Get the currently selected difficulty.

        Returns:
            str: Selected difficulty level
        """
        return self._selected_difficulty
