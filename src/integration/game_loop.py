"""
Game Loop

Main game loop implementation with event handling, update, and rendering.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
from typing import Optional
from src.utils.logger import GameLogger
from src.utils.timer import FPSCounter


class GameLoop:
    """
    Main game loop.

    Handles event processing, game logic updates, and rendering.

    Attributes:
        _running (bool): Whether game loop is running
        _clock (pygame.time.Clock): Pygame clock for FPS control
        _fps_counter (FPSCounter): FPS counter
        _target_fps (int): Target frames per second
        _logger (GameLogger): Logger instance
    """

    def __init__(self, target_fps: int = 60):
        """
        Initialize the game loop.

        Args:
            target_fps: Target frames per second
        """
        self._running: bool = False
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._fps_counter: FPSCounter = FPSCounter()
        self._target_fps: int = target_fps
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def start(self) -> None:
        """Start the game loop."""
        self._running = True
        self._logger.info(f"Game loop started (target FPS: {self._target_fps})")

    def stop(self) -> None:
        """Stop the game loop."""
        self._running = False
        self._logger.info("Game loop stopped")

    def is_running(self) -> bool:
        """
        Check if game loop is running.

        Returns:
            bool: True if running, False otherwise
        """
        return self._running

    def get_fps(self) -> float:
        """
        Get current FPS.

        Returns:
            float: Current frames per second
        """
        return self._fps_counter.get_fps()

    def get_delta_time(self) -> float:
        """
        Get delta time since last frame.

        Returns:
            float: Delta time in milliseconds
        """
        return self._clock.get_time()

    def run(self, game_controller) -> None:
        """
        Run the main game loop.

        Args:
            game_controller: Game controller instance
        """
        self.start()

        while self._running:
            # Get delta time
            delta_ms = self._clock.get_time()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break

                # Pass event to game controller
                game_controller.handle_event(event)

            # Update game logic
            if self._running:
                game_controller.update(delta_ms)

            # Render
            if self._running:
                game_controller.draw()

            # Update FPS counter
            self._fps_counter.update()

            # Cap frame rate
            self._clock.tick(self._target_fps)

        self._logger.info("Game loop ended")

    def set_target_fps(self, fps: int) -> None:
        """
        Set target FPS.

        Args:
            fps: Target frames per second
        """
        self._target_fps = fps
        self._logger.debug(f"Target FPS set to {fps}")

    def get_target_fps(self) -> int:
        """
        Get target FPS.

        Returns:
            int: Target frames per second
        """
        return self._target_fps
