"""
Game Scene Implementation

Concrete implementation of the game playing scene.

Author: Circuit Repair Game Team
Date: 2026-01-21
"""

from typing import Optional
import pygame

from src.integration.scene_manager import Scene, SceneType
from src.utils.logger import GameLogger


class GameScene(Scene):
    """
    Main game playing scene.

    Handles the game board display and player interactions during gameplay.

    Attributes:
        _controller: Reference to game controller
        _logger: Logger instance
    """

    def __init__(self, controller):
        """
        Initialize the game scene.

        Args:
            controller: GameController instance
        """
        super().__init__(SceneType.GAME)
        self._controller = controller
        self._logger = GameLogger.get_logger(__name__)

    def enter(self, **kwargs):
        """
        Called when entering the game scene.

        Args:
            **kwargs: Scene parameters
        """
        super().enter(**kwargs)
        self._logger.debug("Entered game scene")

    def exit(self):
        """Called when exiting the game scene."""
        super().exit()
        self._logger.debug("Exited game scene")

    def update(self, delta_ms: float):
        """
        Update game logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Game logic is handled by GameController
        pass

    def draw(self, renderer):
        """
        Draw the game scene.

        Args:
            renderer: Renderer instance
        """
        # Game rendering is handled by GameController
        pass

    def handle_event(self, event):
        """
        Handle pygame event.

        Args:
            event: Pygame event
        """
        # Events are handled by GameController
        pass


class MenuScene(Scene):
    """
    Main menu scene.

    Displays the main menu with options to start game or exit.

    Attributes:
        _logger: Logger instance
    """

    def __init__(self):
        """Initialize the menu scene."""
        super().__init__(SceneType.MENU)
        self._logger = GameLogger.get_logger(__name__)

    def enter(self, **kwargs):
        """
        Called when entering the menu scene.

        Args:
            **kwargs: Scene parameters
        """
        super().enter(**kwargs)
        self._logger.debug("Entered menu scene")

    def exit(self):
        """Called when exiting the menu scene."""
        super().exit()
        self._logger.debug("Exited menu scene")

    def update(self, delta_ms: float):
        """
        Update menu logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    def draw(self, renderer):
        """
        Draw the menu scene.

        Args:
            renderer: Renderer instance
        """
        # Simple menu display
        surface = renderer.get_surface()
        if surface:
            # Draw menu title
            renderer.draw_text("CIRCUIT REPAIR GAME", (200, 200), font_size=48, color=(255, 215, 0))
            renderer.draw_text("Press any key to start", (250, 300), font_size=24, color=(255, 255, 255))

    def handle_event(self, event):
        """
        Handle pygame event.

        Args:
            event: Pygame event
        """
        # Any key press starts the game
        if event.type == pygame.KEYDOWN:
            # Signal to change to game scene
            pass


class VictoryScene(Scene):
    """
    Victory scene.

    Displays victory message after completing a level or all levels.

    Attributes:
        _logger: Logger instance
        _stats: Victory statistics
    """

    def __init__(self):
        """Initialize the victory scene."""
        super().__init__(SceneType.VICTORY)
        self._logger = GameLogger.get_logger(__name__)
        self._stats = {}

    def enter(self, **kwargs):
        """
        Called when entering the victory scene.

        Args:
            **kwargs: Scene parameters (should contain 'stats')
        """
        super().enter(**kwargs)
        self._stats = kwargs.get('stats', {})
        self._logger.debug(f"Entered victory scene with stats: {self._stats}")

    def exit(self):
        """Called when exiting the victory scene."""
        super().exit()
        self._logger.debug("Exited victory scene")

    def update(self, delta_ms: float):
        """
        Update victory scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    def draw(self, renderer):
        """
        Draw the victory scene.

        Args:
            renderer: Renderer instance
        """
        surface = renderer.get_surface()
        if surface:
            # Draw victory message
            renderer.draw_text("VICTORY!", (300, 200), font_size=64, color=(255, 215, 0))

            # Draw statistics
            moves = self._stats.get('moves', 0)
            renderer.draw_text(f"Moves: {moves}", (320, 300), font_size=32, color=(255, 255, 255))

            renderer.draw_text("Press any key to continue", (250, 400), font_size=24, color=(200, 200, 200))

    def handle_event(self, event):
        """
        Handle pygame event.

        Args:
            event: Pygame event
        """
        # Any key press continues to next level
        if event.type == pygame.KEYDOWN:
            # Signal to continue
            pass


class PauseScene(Scene):
    """
    Pause scene.

    Displays pause menu with options to resume or quit.

    Attributes:
        _logger: Logger instance
    """

    def __init__(self):
        """Initialize the pause scene."""
        super().__init__(SceneType.PAUSE)
        self._logger = GameLogger.get_logger(__name__)

    def enter(self, **kwargs):
        """
        Called when entering the pause scene.

        Args:
            **kwargs: Scene parameters
        """
        super().enter(**kwargs)
        self._logger.debug("Entered pause scene")

    def exit(self):
        """Called when exiting the pause scene."""
        super().exit()
        self._logger.debug("Exited pause scene")

    def update(self, delta_ms: float):
        """
        Update pause scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    def draw(self, renderer):
        """
        Draw the pause scene.

        Args:
            renderer: Renderer instance
        """
        surface = renderer.get_surface()
        if surface:
            # Draw pause overlay
            renderer.draw_text("PAUSED", (330, 250), font_size=48, color=(255, 255, 255))
            renderer.draw_text("Press ESC to resume", (270, 350), font_size=24, color=(200, 200, 200))

    def handle_event(self, event):
        """
        Handle pygame event.

        Args:
            event: Pygame event
        """
        # ESC resumes the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Signal to resume
            pass
