"""
Game Layer

Wraps GameController for use in layered scene system.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
from typing import Optional
from src.scenes.layers.layer_base import LayerBase
from src.integration.game_controller import GameController
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class GameLayer(LayerBase):
    """
    Game layer that wraps GameController.

    Integrates existing game logic into the layered scene system.

    Features:
        - Wraps GameController
        - Event delegation
        - State synchronization

    Example:
        >>> controller = GameController()
        >>> layer = GameLayer(800, 600, controller)
        >>> layer.update(16.67)
        >>> layer.draw(screen)
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        game_controller: Optional[GameController] = None
    ):
        """
        Initialize the game layer.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            game_controller: GameController instance (optional)
        """
        super().__init__(screen_width, screen_height)

        self._game_controller = game_controller
        self._game_surface: Optional[pygame.Surface] = None

        # Create game surface for rendering
        if game_controller:
            self._game_surface = pygame.Surface((screen_width, screen_height))

        logger.debug("GameLayer initialized")

    def update(self, delta_ms: float) -> None:
        """
        Update game logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if not self._enabled or not self._game_controller:
            return

        # Update game controller
        self._game_controller.update(delta_ms)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the game.

        Args:
            surface: Pygame surface to draw on
        """
        if not self._visible or not self._game_controller or not self._game_surface:
            return

        # Clear game surface
        self._game_surface.fill((0, 0, 0))

        # Draw game to game surface
        self._game_controller.draw(self._game_surface)

        # Blit game surface to main surface
        surface.blit(self._game_surface, (0, 0))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if event was handled, False otherwise
        """
        if not self._enabled or not self._game_controller:
            return False

        # Delegate to game controller
        return self._game_controller.handle_event(event)

    def set_game_controller(self, controller: GameController) -> None:
        """
        Set the game controller.

        Args:
            controller: GameController instance
        """
        self._game_controller = controller
        self._game_surface = pygame.Surface((self._screen_width, self._screen_height))
        logger.debug("Game controller set")

    def get_game_controller(self) -> Optional[GameController]:
        """
        Get the game controller.

        Returns:
            Optional[GameController]: The game controller instance
        """
        return self._game_controller

    def is_game_over(self) -> bool:
        """
        Check if game is over.

        Returns:
            bool: True if game is over, False otherwise
        """
        if not self._game_controller:
            return False

        return self._game_controller.is_game_over()

    def is_victory(self) -> bool:
        """
        Check if player won.

        Returns:
            bool: True if player won, False otherwise
        """
        if not self._game_controller:
            return False

        return self._game_controller.is_victory()

    def get_game_state(self) -> dict:
        """
        Get current game state.

        Returns:
            dict: Game state information
        """
        if not self._game_controller:
            return {}

        return {
            'is_game_over': self._game_controller.is_game_over(),
            'is_victory': self._game_controller.is_victory(),
            'move_count': self._game_controller.get_move_count(),
            'elapsed_time': self._game_controller.get_elapsed_time()
        }
