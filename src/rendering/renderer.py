"""
Renderer Module

This module provides the Renderer class for managing the game's rendering pipeline.
It handles Pygame initialization, window management, frame rendering, and FPS control.

Classes:
    Renderer: Main rendering engine for the game

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import Optional, Tuple
import pygame

from src.config.config_manager import ConfigManager
from src.config.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
    COLOR_BACKGROUND, COLOR_WHITE
)
from src.rendering.sprite_manager import SpriteManager
from src.utils.timer import FPSCounter

# Configure logger
logger = logging.getLogger(__name__)


class Renderer:
    """
    Main rendering engine for the game.

    Manages Pygame initialization, window creation, frame rendering, and FPS control.
    Provides methods for drawing sprites, text, and shapes.

    Attributes:
        _screen: Pygame display surface
        _clock: Pygame clock for FPS control
        _sprite_manager: SpriteManager instance for sprite loading
        _fps_counter: FPSCounter for performance monitoring
        _config: ConfigManager instance
        _window_size: (width, height) of the window
        _target_fps: Target frames per second
        _is_initialized: Whether Pygame has been initialized

    Example:
        >>> renderer = Renderer()
        >>> renderer.initialize()
        >>> renderer.clear()
        >>> renderer.draw_sprite(sprite, (100, 100))
        >>> renderer.present()
    """

    def __init__(self, config: Optional[ConfigManager] = None) -> None:
        """
        Initialize the Renderer.

        Args:
            config: Optional ConfigManager instance (creates new if None)
        """
        self._config = config or ConfigManager()
        self._sprite_manager = SpriteManager()
        self._fps_counter = FPSCounter()

        # Window settings
        self._window_size: Tuple[int, int] = (
            self._config.get("window.width", WINDOW_WIDTH),
            self._config.get("window.height", WINDOW_HEIGHT)
        )
        self._window_title: str = self._config.get("window.title", WINDOW_TITLE)
        self._target_fps: int = self._config.get("window.fps", FPS)
        self._fullscreen: bool = self._config.get("window.fullscreen", False)

        # Pygame objects (initialized later)
        self._screen: Optional[pygame.Surface] = None
        self._clock: Optional[pygame.time.Clock] = None
        self._is_initialized: bool = False

        logger.info("Renderer created")

    def initialize(self) -> bool:
        """
        Initialize Pygame and create the game window.

        Returns:
            True if initialization successful, False otherwise

        Example:
            >>> renderer = Renderer()
            >>> success = renderer.initialize()
        """
        if self._is_initialized:
            logger.warning("Renderer already initialized")
            return True

        try:
            # Initialize Pygame
            pygame.init()
            logger.info("Pygame initialized")

            # Create window
            flags = pygame.FULLSCREEN if self._fullscreen else 0
            self._screen = pygame.display.set_mode(self._window_size, flags)
            pygame.display.set_caption(self._window_title)
            logger.info(f"Window created: {self._window_size[0]}x{self._window_size[1]}")

            # Create clock
            self._clock = pygame.time.Clock()

            self._is_initialized = True
            logger.info("Renderer initialized successfully")
            return True

        except pygame.error as e:
            logger.error(f"Failed to initialize Pygame: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during initialization: {e}")
            return False

    def shutdown(self) -> None:
        """
        Shutdown Pygame and cleanup resources.

        Example:
            >>> renderer.shutdown()
        """
        if not self._is_initialized:
            return

        pygame.quit()
        self._is_initialized = False
        logger.info("Renderer shutdown")

    def clear(self, color: Optional[Tuple[int, int, int]] = None) -> None:
        """
        Clear the screen with a solid color.

        Args:
            color: RGB color tuple (uses background color if None)

        Example:
            >>> renderer.clear()
            >>> renderer.clear((255, 0, 0))  # Clear with red
        """
        if not self._is_initialized or not self._screen:
            logger.warning("Cannot clear: Renderer not initialized")
            return

        fill_color = color or COLOR_BACKGROUND
        self._screen.fill(fill_color)

    def present(self) -> None:
        """
        Present the rendered frame to the screen and update FPS.

        This should be called once per frame after all drawing is complete.

        Example:
            >>> renderer.clear()
            >>> # ... draw everything ...
            >>> renderer.present()
        """
        if not self._is_initialized:
            logger.warning("Cannot present: Renderer not initialized")
            return

        pygame.display.flip()

        # Update FPS counter
        if self._clock:
            self._clock.tick(self._target_fps)
            self._fps_counter.update()

    def draw_sprite(
        self,
        sprite: pygame.Surface,
        position: Tuple[int, int],
        rotation: int = 0
    ) -> None:
        """
        Draw a sprite at the specified position with optional rotation.

        Args:
            sprite: pygame.Surface to draw
            position: (x, y) position (top-left corner)
            rotation: Rotation angle in degrees (clockwise)

        Example:
            >>> sprite = renderer.get_sprite_manager().load_sprite("path/to/sprite.png")
            >>> renderer.draw_sprite(sprite, (100, 100))
            >>> renderer.draw_sprite(sprite, (200, 200), rotation=90)
        """
        if not self._is_initialized or not self._screen:
            logger.warning("Cannot draw sprite: Renderer not initialized")
            return

        # Rotate sprite if needed
        if rotation != 0:
            sprite = self._sprite_manager.get_rotated_sprite(sprite, rotation)

        self._screen.blit(sprite, position)

    def draw_text(
        self,
        text: str,
        position: Tuple[int, int],
        font_size: int = 24,
        color: Tuple[int, int, int] = COLOR_WHITE,
        font_name: Optional[str] = None
    ) -> None:
        """
        Draw text at the specified position.

        Args:
            text: Text string to draw
            position: (x, y) position (top-left corner)
            font_size: Font size in pixels
            color: RGB color tuple
            font_name: Font name or path (uses Chinese font if None)

        Example:
            >>> renderer.draw_text("Hello World", (100, 100))
            >>> renderer.draw_text("Score: 42", (10, 10), font_size=32, color=(255, 255, 0))
        """
        if not self._is_initialized or not self._screen:
            logger.warning("Cannot draw text: Renderer not initialized")
            return

        try:
            # Use Microsoft YaHei for Chinese support if no font specified
            if font_name is None:
                font_name = "C:/WINDOWS/fonts/msyh.ttc"

            font = pygame.font.Font(font_name, font_size)
            text_surface = font.render(text, True, color)
            self._screen.blit(text_surface, position)
        except Exception as e:
            logger.error(f"Failed to draw text: {e}")
            # Fallback to default font
            try:
                font = pygame.font.Font(None, font_size)
                text_surface = font.render(text, True, color)
                self._screen.blit(text_surface, position)
            except Exception as e2:
                logger.error(f"Failed to draw text with fallback font: {e2}")

    def draw_rect(
        self,
        rect: Tuple[int, int, int, int],
        color: Tuple[int, int, int],
        width: int = 0
    ) -> None:
        """
        Draw a rectangle.

        Args:
            rect: (x, y, width, height) tuple
            color: RGB color tuple
            width: Line width (0 for filled rectangle)

        Example:
            >>> renderer.draw_rect((100, 100, 200, 150), (255, 0, 0))  # Filled red rect
            >>> renderer.draw_rect((100, 100, 200, 150), (0, 255, 0), width=2)  # Green outline
        """
        if not self._is_initialized or not self._screen:
            logger.warning("Cannot draw rect: Renderer not initialized")
            return

        pygame.draw.rect(self._screen, color, rect, width)

    def draw_circle(
        self,
        center: Tuple[int, int],
        radius: int,
        color: Tuple[int, int, int],
        width: int = 0
    ) -> None:
        """
        Draw a circle.

        Args:
            center: (x, y) center position
            radius: Circle radius in pixels
            color: RGB color tuple
            width: Line width (0 for filled circle)

        Example:
            >>> renderer.draw_circle((400, 300), 50, (0, 0, 255))  # Filled blue circle
            >>> renderer.draw_circle((400, 300), 50, (255, 255, 0), width=3)  # Yellow outline
        """
        if not self._is_initialized or not self._screen:
            logger.warning("Cannot draw circle: Renderer not initialized")
            return

        pygame.draw.circle(self._screen, color, center, radius, width)

    def get_sprite_manager(self) -> SpriteManager:
        """
        Get the SpriteManager instance.

        Returns:
            SpriteManager instance

        Example:
            >>> sprite_mgr = renderer.get_sprite_manager()
            >>> sprite = sprite_mgr.load_sprite("path/to/sprite.png")
        """
        return self._sprite_manager

    def get_fps(self) -> float:
        """
        Get the current FPS.

        Returns:
            Current frames per second

        Example:
            >>> fps = renderer.get_fps()
            >>> print(f"FPS: {fps:.1f}")
        """
        return self._fps_counter.get_fps()

    def get_window_size(self) -> Tuple[int, int]:
        """
        Get the window size.

        Returns:
            (width, height) tuple

        Example:
            >>> width, height = renderer.get_window_size()
        """
        return self._window_size

    def is_initialized(self) -> bool:
        """
        Check if the renderer is initialized.

        Returns:
            True if initialized, False otherwise

        Example:
            >>> if renderer.is_initialized():
            ...     renderer.clear()
        """
        return self._is_initialized

    def set_window_title(self, title: str) -> None:
        """
        Set the window title.

        Args:
            title: New window title

        Example:
            >>> renderer.set_window_title("Circuit Repair - Level 1")
        """
        if self._is_initialized:
            pygame.display.set_caption(title)
            self._window_title = title
