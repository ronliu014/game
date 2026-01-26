"""
Level Select Scene

Provides a level selection interface showing all available levels,
their unlock status, star ratings, and best scores.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

from typing import Optional, Dict, List
import pygame
from src.scenes.scene_base import SceneBase
from src.ui.components.button import Button
from src.ui.components.panel import Panel
from src.ui.components.label import Label
from src.ui.layouts.layout_manager import LayoutManager
from src.progression.level_progression import LevelProgressionManager
from src.progression.progress_data import LevelProgress
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class LevelSelectScene(SceneBase):
    """
    Level selection scene.

    Displays all available levels with their status:
        - Locked/Unlocked
        - Star rating (0-3)
        - Best time
        - Best moves

    Features:
        - Grid layout of level buttons
        - Visual indication of locked levels
        - Star display for completed levels
        - Best score display
        - Back to main menu button

    Example:
        >>> scene = LevelSelectScene(scene_manager)
        >>> scene.on_enter({'difficulty': 'normal'})
    """

    # Layout constants
    LEVELS_PER_ROW = 5
    LEVEL_BUTTON_SIZE = 120
    LEVEL_BUTTON_SPACING = 20
    MAX_LEVELS = 10  # Total number of levels in the game

    def __init__(self, scene_manager=None):
        """
        Initialize the level select scene.

        Args:
            scene_manager: Reference to the scene manager
        """
        super().__init__(scene_manager)

        # Screen dimensions
        self._screen_width = 800
        self._screen_height = 600

        # UI components
        self._background_panel: Optional[Panel] = None
        self._title_label: Optional[Label] = None
        self._level_buttons: Dict[int, Button] = {}
        self._level_labels: Dict[int, Label] = {}
        self._star_labels: Dict[int, Label] = {}
        self._back_button: Optional[Button] = None

        # Layout manager
        self._layout: Optional[LayoutManager] = None

        # Progression manager
        self._progression_manager: Optional[LevelProgressionManager] = None

        # Selected difficulty
        self._difficulty = 'normal'

    def on_enter(self, data: Optional[Dict] = None):
        """
        Called when entering the scene.

        Args:
            data: Optional data dictionary with keys:
                - difficulty (str): Selected difficulty level
        """
        super().on_enter(data)

        # Get screen dimensions
        if self.scene_manager and hasattr(self.scene_manager, 'screen'):
            screen = self.scene_manager.screen
            self._screen_width = screen.get_width()
            self._screen_height = screen.get_height()

        # Get difficulty from data
        if data and 'difficulty' in data:
            self._difficulty = data['difficulty']

        # Initialize progression manager
        self._progression_manager = LevelProgressionManager()

        # Create UI
        self._create_ui()

        logger.info(f"Level select scene entered with difficulty: {self._difficulty}")

    def on_exit(self):
        """Called when exiting the scene."""
        super().on_exit()
        logger.info("Level select scene exited")

    def _create_ui(self):
        """Create all UI components."""
        # Create layout manager
        self._layout = LayoutManager(self._screen_width, self._screen_height)

        # Background panel
        self._background_panel = Panel(
            x=0, y=0,
            width=self._screen_width,
            height=self._screen_height,
            background_color=(30, 30, 40),
            border_color=(100, 100, 120),
            border_width=0
        )

        # Title label
        self._title_label = Label(
            x=0,
            y=50,
            width=self._screen_width,
            height=60,
            text="选择关卡 (Select Level)",
            font_size=48,
            text_color=(255, 255, 255),
            alignment=Label.ALIGN_CENTER
        )

        # Create level buttons in grid
        self._create_level_grid()

        # Back button
        self._back_button = Button(
            x=self._screen_width // 2 - 100,
            y=self._screen_height - 80,
            width=200,
            height=50,
            label="返回主菜单 (Back)",
            on_click=self._on_back_clicked
        )

    def _create_level_grid(self):
        """Create grid of level buttons."""
        # Calculate grid layout
        total_width = (self.LEVEL_BUTTON_SIZE * self.LEVELS_PER_ROW +
                      self.LEVEL_BUTTON_SPACING * (self.LEVELS_PER_ROW - 1))
        start_x = (self._screen_width - total_width) // 2
        start_y = 150

        # Get progress data
        progress = self._progression_manager.get_progress()

        # Create buttons for each level
        for level_id in range(1, self.MAX_LEVELS + 1):
            row = (level_id - 1) // self.LEVELS_PER_ROW
            col = (level_id - 1) % self.LEVELS_PER_ROW

            x = start_x + col * (self.LEVEL_BUTTON_SIZE + self.LEVEL_BUTTON_SPACING)
            y = start_y + row * (self.LEVEL_BUTTON_SIZE + self.LEVEL_BUTTON_SPACING + 40)

            # Check if level is unlocked
            is_unlocked = progress.is_level_unlocked(level_id)
            level_progress = progress.get_level_progress(level_id)

            # Create level button
            button = Button(
                x=x,
                y=y,
                width=self.LEVEL_BUTTON_SIZE,
                height=self.LEVEL_BUTTON_SIZE,
                label=str(level_id),
                on_click=lambda lid=level_id: self._on_level_clicked(lid),
                text_color=(100, 100, 110) if not is_unlocked else (255, 255, 255)
            )
            button.enabled = is_unlocked

            # Style based on unlock status
            if not is_unlocked:
                button.set_colors({
                    Button.STATE_NORMAL: (60, 60, 70),
                    Button.STATE_HOVER: (60, 60, 70),
                    Button.STATE_PRESSED: (60, 60, 70),
                    Button.STATE_DISABLED: (60, 60, 70)
                })
            elif level_progress and level_progress.completed:
                # Completed level - green tint
                button.set_colors({
                    Button.STATE_NORMAL: (50, 120, 50),
                    Button.STATE_HOVER: (60, 140, 60),
                    Button.STATE_PRESSED: (40, 100, 40)
                })

            self._level_buttons[level_id] = button

            # Create star label (below button)
            if level_progress and level_progress.completed:
                stars_text = "★" * level_progress.stars
                star_label = Label(
                    x=x,
                    y=y + self.LEVEL_BUTTON_SIZE + 10,
                    width=self.LEVEL_BUTTON_SIZE,
                    height=30,
                    text=stars_text,
                    font_size=20,
                    text_color=(255, 215, 0),  # Gold color
                    alignment=Label.ALIGN_CENTER
                )
                self._star_labels[level_id] = star_label
            elif not is_unlocked:
                # Locked indicator
                lock_label = Label(
                    x=x,
                    y=y + self.LEVEL_BUTTON_SIZE + 10,
                    width=self.LEVEL_BUTTON_SIZE,
                    height=30,
                    text="🔒",
                    font_size=20,
                    text_color=(150, 150, 160),
                    alignment=Label.ALIGN_CENTER
                )
                self._star_labels[level_id] = lock_label

    def _on_level_clicked(self, level_id: int):
        """
        Handle level button click.

        Args:
            level_id: ID of the clicked level
        """
        logger.info(f"Level {level_id} selected")

        # Transition to gameplay scene
        if self.scene_manager:
            self.scene_manager.replace_scene(
                'gameplay',
                {
                    'level': level_id,
                    'difficulty': self._difficulty
                }
            )

    def _on_back_clicked(self):
        """Handle back button click."""
        logger.info("Back to main menu")

        # Return to main menu
        from src.scenes.main_menu_scene import MainMenuScene
        self.request_scene_change(MainMenuScene, data={
            'screen_width': self._screen_width,
            'screen_height': self._screen_height
        }, replace=True)

    def update(self, dt: float):
        """
        Update scene logic.

        Args:
            dt: Delta time in seconds
        """
        # Update all buttons
        for button in self._level_buttons.values():
            button.update(dt)

        if self._back_button:
            self._back_button.update(dt)

    def draw(self, screen: pygame.Surface):
        """
        Draw the scene.

        Args:
            screen: Pygame surface to draw on
        """
        # Draw background
        if self._background_panel:
            self._background_panel.draw(screen)

        # Draw title
        if self._title_label:
            self._title_label.draw(screen)

        # Draw level buttons
        for button in self._level_buttons.values():
            button.draw(screen)

        # Draw star labels
        for label in self._star_labels.values():
            label.draw(screen)

        # Draw back button
        if self._back_button:
            self._back_button.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle pygame events.

        Args:
            event: Pygame event
        """
        # Handle level button events
        for button in self._level_buttons.values():
            button.handle_event(event)

        # Handle back button event
        if self._back_button:
            self._back_button.handle_event(event)

        # Handle ESC key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._on_back_clicked()
