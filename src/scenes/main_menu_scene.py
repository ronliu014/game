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
from src.ui.components.dropdown import Dropdown
from src.ui.layouts.layout_manager import LayoutManager
from src.progression.level_progression import LevelProgressionManager
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
        self._progress_panel: Optional[Panel] = None
        self._progress_label: Optional[Label] = None
        self._stars_label: Optional[Label] = None
        self._difficulty_dropdown: Optional[Dropdown] = None
        self._new_game_button: Optional[Button] = None
        self._level_select_button: Optional[Button] = None
        self._exit_button: Optional[Button] = None

        # Layout manager
        self._layout: Optional[LayoutManager] = None

        # Progression manager
        self._progression_manager: Optional[LevelProgressionManager] = None

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

        try:
            # Get screen dimensions from data or use defaults
            self._screen_width = self.get_transition_data('screen_width', 800)
            self._screen_height = self.get_transition_data('screen_height', 600)

            # Get default difficulty from data
            default_difficulty = self.get_transition_data('default_difficulty', self.DIFFICULTY_NORMAL)
            self._selected_difficulty = default_difficulty

            # Initialize layout manager
            self._layout = LayoutManager(self._screen_width, self._screen_height)

            # Initialize progression manager (with error handling)
            try:
                self._progression_manager = LevelProgressionManager()
            except Exception as e:
                logger.warning(f"Failed to initialize LevelProgressionManager: {e}")
                self._progression_manager = None

            # Create UI components
            self._create_background()
            self._create_title()
            if self._progression_manager:
                self._create_progress_display()
            self._create_difficulty_selection()
            self._create_buttons()

            logger.info("MainMenuScene entered successfully")
        except Exception as e:
            logger.error(f"Error in MainMenuScene.on_enter: {e}", exc_info=True)
            raise

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

        # Draw progress display
        if self._progress_panel:
            self._progress_panel.draw(surface)
        if self._progress_label:
            self._progress_label.draw(surface)
        if self._stars_label:
            self._stars_label.draw(surface)

        # Draw action buttons
        if self._new_game_button:
            self._new_game_button.draw(surface)
        if self._level_select_button:
            self._level_select_button.draw(surface)
        if self._exit_button:
            self._exit_button.draw(surface)

        # Draw difficulty dropdown LAST (so it appears on top when expanded)
        if self._difficulty_dropdown:
            self._difficulty_dropdown.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        # Handle difficulty dropdown events
        if self._difficulty_dropdown and self._difficulty_dropdown.handle_event(event):
            return True

        # Handle action button events
        if self._new_game_button and self._new_game_button.handle_event(event):
            return True
        if self._level_select_button and self._level_select_button.handle_event(event):
            return True
        if self._exit_button and self._exit_button.handle_event(event):
            return True

        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_exit_clicked()
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._on_new_game_clicked()
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

    def _create_progress_display(self) -> None:
        """Create progress display panel."""
        if not self._progression_manager:
            return

        # Get statistics
        stats = self._progression_manager.get_statistics()

        # Create progress panel (centered below title)
        panel_width = 300
        panel_height = 100
        panel_x = (self._screen_width - panel_width) // 2
        panel_y = 160  # Below title (title is at y=50, height=100, so 150 + 10 margin)

        self._progress_panel = Panel(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
            background_color=(40, 40, 50),
            border_color=(100, 100, 100),
            border_width=2,
            alpha=220
        )

        # Create progress label
        progress_text = f"进度: {stats['completed_levels']}/{stats['total_levels']} 关卡"
        self._progress_label = Label(
            panel_x + 10,
            panel_y + 10,
            panel_width - 20,
            30,
            progress_text,
            font_size=18,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_CENTER
        )

        # Create stars label
        stars_text = f"★ {stats['total_stars']}/{stats['max_stars']}"
        self._stars_label = Label(
            panel_x + 10,
            panel_y + 45,
            panel_width - 20,
            30,
            stars_text,
            font_size=20,
            text_color=(255, 215, 0),
            alignment=Label.ALIGN_CENTER
        )

    def _create_difficulty_selection(self) -> None:
        """Create difficulty selection UI."""
        # Create difficulty dropdown
        difficulty_options = [
            (self.DIFFICULTY_EASY, "简单 (60秒)"),
            (self.DIFFICULTY_NORMAL, "普通 (45秒)"),
            (self.DIFFICULTY_HARD, "困难 (30秒)"),
            (self.DIFFICULTY_HELL, "地狱 (15秒)")
        ]

        # Position to align with buttons below
        dropdown_width = 200
        dropdown_height = 60
        dropdown_x = (self._screen_width - dropdown_width) // 2
        dropdown_y = 300  # Same vertical spacing as buttons

        self._difficulty_dropdown = Dropdown(
            dropdown_x,
            dropdown_y,
            dropdown_width,
            dropdown_height,
            options=difficulty_options,
            selected_value=self._selected_difficulty,
            on_select=self._on_difficulty_selected,
            font_size=20
        )

    def _create_buttons(self) -> None:
        """Create action buttons (New Game, Level Select, Exit)."""
        button_width = 200
        button_height = 60

        buttons = []

        # Create new game button
        self._new_game_button = Button(
            0, 0,
            button_width,
            button_height,
            "新游戏",
            on_click=self._on_new_game_clicked,
            font_size=24
        )
        buttons.append(self._new_game_button)

        # Create level select button
        self._level_select_button = Button(
            0, 0,
            button_width,
            button_height,
            "关卡选择",
            on_click=self._on_level_select_clicked,
            font_size=24
        )
        buttons.append(self._level_select_button)

        # Create exit button
        self._exit_button = Button(
            0, 0,
            button_width,
            button_height,
            "退出游戏",
            on_click=self._on_exit_clicked,
            font_size=24
        )
        buttons.append(self._exit_button)

        # Arrange buttons vertically (starting below dropdown)
        # Dropdown is at y=300, height=60, so buttons start at y=380
        self._layout.arrange_vertical(
            buttons,
            start_y=380,
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
        logger.info(f"Difficulty selected: {difficulty}")

    def _on_new_game_clicked(self) -> None:
        """Handle new game button click."""
        logger.info(f"Starting new game with difficulty: {self._selected_difficulty}")

        # Start from level 1
        from src.scenes.loading_scene import LoadingScene
        from src.scenes.gameplay_scene import GameplayScene

        self.request_scene_change(LoadingScene, data={
            'level': 1,
            'difficulty': self._selected_difficulty,
            'screen_width': self._screen_width,
            'screen_height': self._screen_height,
            'next_scene': GameplayScene,
            'next_scene_data': {
                'level': 1,
                'difficulty': self._selected_difficulty,
                'screen_width': self._screen_width,
                'screen_height': self._screen_height
            }
        })

    def _on_level_select_clicked(self) -> None:
        """Handle level select button click."""
        logger.info("Level select button clicked")

        # Transition to level select scene
        from src.scenes.level_select_scene import LevelSelectScene

        self.request_scene_change(LevelSelectScene, data={
            'screen_width': self._screen_width,
            'screen_height': self._screen_height,
            'selected_difficulty': self._selected_difficulty
        })

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
