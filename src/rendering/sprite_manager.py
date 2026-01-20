"""
Sprite Manager Module

This module provides the SpriteManager class for loading, caching, and managing
game sprites and images. It handles resource loading with error handling and
provides efficient sprite access through caching.

Classes:
    SpriteManager: Manages sprite loading, caching, and retrieval

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import os
import logging
from typing import Dict, Optional, Tuple
import pygame

from src.utils.file_utils import get_project_root, safe_join_path

# Configure logger
logger = logging.getLogger(__name__)


class SpriteManager:
    """
    Manages sprite loading, caching, and retrieval.

    Provides centralized sprite management with automatic caching to avoid
    redundant file I/O. Supports sprite loading, scaling, and rotation.

    Attributes:
        _cache: Dictionary mapping file paths to loaded pygame.Surface objects
        _project_root: Project root directory path

    Example:
        >>> manager = SpriteManager()
        >>> sprite = manager.load_sprite("assets/sprites/tiles/power_source.png")
        >>> scaled = manager.load_sprite("assets/sprites/tiles/line.png", size=(64, 64))
        >>> rotated = manager.get_rotated_sprite(sprite, 90)
    """

    def __init__(self) -> None:
        """Initialize the SpriteManager with empty cache."""
        self._cache: Dict[str, pygame.Surface] = {}
        self._project_root: str = get_project_root()
        logger.info("SpriteManager initialized")

    def load_sprite(
        self,
        relative_path: str,
        size: Optional[Tuple[int, int]] = None,
        use_cache: bool = True
    ) -> Optional[pygame.Surface]:
        """
        Load a sprite from file with optional scaling.

        Args:
            relative_path: Path relative to project root
            size: Optional (width, height) tuple to scale the sprite
            use_cache: Whether to use cached sprite if available

        Returns:
            Loaded pygame.Surface or None if loading fails

        Example:
            >>> sprite = manager.load_sprite("assets/sprites/tiles/line.png")
            >>> scaled = manager.load_sprite("assets/sprites/tiles/line.png", size=(64, 64))
        """
        # Create cache key including size if specified
        cache_key = f"{relative_path}_{size}" if size else relative_path

        # Return cached sprite if available and caching is enabled
        if use_cache and cache_key in self._cache:
            logger.debug(f"Sprite loaded from cache: {relative_path}")
            return self._cache[cache_key]

        # Construct full path
        full_path = safe_join_path(self._project_root, relative_path)

        # Check if file exists
        if not os.path.exists(full_path):
            logger.error(f"Sprite file not found: {full_path}")
            return None

        try:
            # Load sprite
            sprite = pygame.image.load(full_path).convert_alpha()
            logger.debug(f"Sprite loaded: {relative_path}")

            # Scale if size specified
            if size:
                sprite = pygame.transform.scale(sprite, size)
                logger.debug(f"Sprite scaled to {size}: {relative_path}")

            # Cache the sprite
            if use_cache:
                self._cache[cache_key] = sprite

            return sprite

        except pygame.error as e:
            logger.error(f"Failed to load sprite {relative_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error loading sprite {relative_path}: {e}")
            return None

    def get_rotated_sprite(
        self,
        sprite: pygame.Surface,
        angle: int
    ) -> pygame.Surface:
        """
        Get a rotated version of a sprite.

        Args:
            sprite: Original pygame.Surface to rotate
            angle: Rotation angle in degrees (clockwise)

        Returns:
            Rotated pygame.Surface

        Note:
            Pygame rotates counter-clockwise, so we negate the angle
            to achieve clockwise rotation as expected in the game.

        Example:
            >>> original = manager.load_sprite("assets/sprites/tiles/line.png")
            >>> rotated_90 = manager.get_rotated_sprite(original, 90)
        """
        # Pygame rotates counter-clockwise, negate for clockwise rotation
        return pygame.transform.rotate(sprite, -angle)

    def create_placeholder_sprite(
        self,
        size: Tuple[int, int],
        color: Tuple[int, int, int] = (255, 0, 255)
    ) -> pygame.Surface:
        """
        Create a placeholder sprite (for missing assets).

        Args:
            size: (width, height) of the placeholder
            color: RGB color tuple (default: magenta for visibility)

        Returns:
            pygame.Surface filled with the specified color

        Example:
            >>> placeholder = manager.create_placeholder_sprite((128, 128))
        """
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill(color)
        logger.warning(f"Created placeholder sprite of size {size}")
        return surface

    def preload_sprites(self, sprite_paths: list[str]) -> int:
        """
        Preload multiple sprites into cache.

        Args:
            sprite_paths: List of relative paths to preload

        Returns:
            Number of successfully loaded sprites

        Example:
            >>> paths = ["assets/sprites/tiles/line.png", "assets/sprites/tiles/corner.png"]
            >>> loaded_count = manager.preload_sprites(paths)
        """
        loaded_count = 0

        for path in sprite_paths:
            sprite = self.load_sprite(path, use_cache=True)
            if sprite:
                loaded_count += 1

        logger.info(f"Preloaded {loaded_count}/{len(sprite_paths)} sprites")
        return loaded_count

    def clear_cache(self) -> None:
        """
        Clear the sprite cache to free memory.

        Example:
            >>> manager.clear_cache()
        """
        cache_size = len(self._cache)
        self._cache.clear()
        logger.info(f"Sprite cache cleared ({cache_size} sprites removed)")

    def get_cache_size(self) -> int:
        """
        Get the number of cached sprites.

        Returns:
            Number of sprites in cache

        Example:
            >>> size = manager.get_cache_size()
        """
        return len(self._cache)

    def get_sprite_size(self, sprite: pygame.Surface) -> Tuple[int, int]:
        """
        Get the size of a sprite.

        Args:
            sprite: pygame.Surface to measure

        Returns:
            (width, height) tuple

        Example:
            >>> sprite = manager.load_sprite("assets/sprites/tiles/line.png")
            >>> width, height = manager.get_sprite_size(sprite)
        """
        return sprite.get_size()
