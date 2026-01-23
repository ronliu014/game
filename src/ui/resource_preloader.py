"""
Resource Preloader

Provides resource preloading with progress tracking.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Dict, List, Callable, Optional, Any
from enum import Enum
import pygame
from pathlib import Path
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class ResourceType(Enum):
    """Resource type enumeration."""
    IMAGE = "image"
    SOUND = "sound"
    MUSIC = "music"
    FONT = "font"


class ResourcePreloader:
    """
    Resource preloader with progress tracking and caching.

    Supports asynchronous loading with progress callbacks.

    Attributes:
        resources (Dict[str, Any]): Cached resources
        total_resources (int): Total number of resources to load
        loaded_resources (int): Number of resources loaded

    Example:
        >>> preloader = ResourcePreloader()
        >>> preloader.add_image("button", "assets/ui/button.png")
        >>> preloader.add_sound("click", "assets/audio/click.wav")
        >>> preloader.load_all(progress_callback=lambda p: print(f"{p:.0%}"))
        >>> button_image = preloader.get_resource("button")
    """

    def __init__(self):
        """Initialize the resource preloader."""
        self._resources: Dict[str, Any] = {}
        self._load_queue: List[tuple] = []
        self._total_resources = 0
        self._loaded_resources = 0
        logger.debug("ResourcePreloader initialized")

    def add_image(self, name: str, path: str) -> None:
        """
        Add an image to the load queue.

        Args:
            name: Resource name for retrieval
            path: Path to image file
        """
        self._load_queue.append((name, path, ResourceType.IMAGE))
        logger.debug(f"Added image to queue: {name} -> {path}")

    def add_sound(self, name: str, path: str) -> None:
        """
        Add a sound effect to the load queue.

        Args:
            name: Resource name for retrieval
            path: Path to sound file
        """
        self._load_queue.append((name, path, ResourceType.SOUND))
        logger.debug(f"Added sound to queue: {name} -> {path}")

    def add_music(self, name: str, path: str) -> None:
        """
        Add background music to the load queue.

        Args:
            name: Resource name for retrieval
            path: Path to music file
        """
        self._load_queue.append((name, path, ResourceType.MUSIC))
        logger.debug(f"Added music to queue: {name} -> {path}")

    def add_font(self, name: str, path: str, size: int = 20) -> None:
        """
        Add a font to the load queue.

        Args:
            name: Resource name for retrieval
            path: Path to font file
            size: Font size in pixels
        """
        self._load_queue.append((name, path, ResourceType.FONT, size))
        logger.debug(f"Added font to queue: {name} -> {path} (size: {size})")

    def load_all(
        self,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """
        Load all queued resources.

        Args:
            progress_callback: Optional callback function(progress: float)
                             Called with progress value 0.0 to 1.0

        Returns:
            bool: True if all resources loaded successfully, False otherwise
        """
        self._total_resources = len(self._load_queue)
        self._loaded_resources = 0
        success = True

        logger.info(f"Starting to load {self._total_resources} resources")

        for item in self._load_queue:
            name = item[0]
            path = item[1]
            resource_type = item[2]

            try:
                if resource_type == ResourceType.IMAGE:
                    self._load_image(name, path)
                elif resource_type == ResourceType.SOUND:
                    self._load_sound(name, path)
                elif resource_type == ResourceType.MUSIC:
                    self._load_music(name, path)
                elif resource_type == ResourceType.FONT:
                    size = item[3] if len(item) > 3 else 20
                    self._load_font(name, path, size)

                self._loaded_resources += 1

                # Call progress callback
                if progress_callback:
                    progress = self._loaded_resources / self._total_resources
                    progress_callback(progress)

            except Exception as e:
                logger.error(f"Failed to load resource '{name}' from '{path}': {e}")
                success = False

        # Clear the queue after loading
        self._load_queue.clear()

        logger.info(f"Resource loading complete: {self._loaded_resources}/{self._total_resources} loaded")
        return success

    def _load_image(self, name: str, path: str) -> None:
        """
        Load an image resource.

        Args:
            name: Resource name
            path: Path to image file
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        image = pygame.image.load(path)
        self._resources[name] = image
        logger.debug(f"Loaded image: {name}")

    def _load_sound(self, name: str, path: str) -> None:
        """
        Load a sound effect resource.

        Args:
            name: Resource name
            path: Path to sound file
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Sound file not found: {path}")

        sound = pygame.mixer.Sound(path)
        self._resources[name] = sound
        logger.debug(f"Loaded sound: {name}")

    def _load_music(self, name: str, path: str) -> None:
        """
        Load a music resource (stores path only, music is loaded on demand).

        Args:
            name: Resource name
            path: Path to music file
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Music file not found: {path}")

        # Store the path for music (pygame.mixer.music loads one at a time)
        self._resources[name] = path
        logger.debug(f"Registered music: {name}")

    def _load_font(self, name: str, path: str, size: int) -> None:
        """
        Load a font resource.

        Args:
            name: Resource name
            path: Path to font file
            size: Font size in pixels
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Font file not found: {path}")

        font = pygame.font.Font(path, size)
        self._resources[name] = font
        logger.debug(f"Loaded font: {name} (size: {size})")

    def get_resource(self, name: str) -> Optional[Any]:
        """
        Get a loaded resource by name.

        Args:
            name: Resource name

        Returns:
            The loaded resource, or None if not found
        """
        resource = self._resources.get(name)
        if resource is None:
            logger.warning(f"Resource not found: {name}")
        return resource

    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """
        Get a loaded image resource.

        Args:
            name: Resource name

        Returns:
            pygame.Surface: The image surface, or None if not found
        """
        return self.get_resource(name)

    def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """
        Get a loaded sound resource.

        Args:
            name: Resource name

        Returns:
            pygame.mixer.Sound: The sound object, or None if not found
        """
        return self.get_resource(name)

    def get_music_path(self, name: str) -> Optional[str]:
        """
        Get the path to a music resource.

        Args:
            name: Resource name

        Returns:
            str: The music file path, or None if not found
        """
        return self.get_resource(name)

    def get_font(self, name: str) -> Optional[pygame.font.Font]:
        """
        Get a loaded font resource.

        Args:
            name: Resource name

        Returns:
            pygame.font.Font: The font object, or None if not found
        """
        return self.get_resource(name)

    def has_resource(self, name: str) -> bool:
        """
        Check if a resource is loaded.

        Args:
            name: Resource name

        Returns:
            bool: True if resource exists, False otherwise
        """
        return name in self._resources

    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self._resources.clear()
        logger.info("Resource cache cleared")

    def remove_resource(self, name: str) -> bool:
        """
        Remove a specific resource from cache.

        Args:
            name: Resource name

        Returns:
            bool: True if resource was removed, False if not found
        """
        if name in self._resources:
            del self._resources[name]
            logger.debug(f"Removed resource: {name}")
            return True
        return False

    def get_progress(self) -> float:
        """
        Get the current loading progress.

        Returns:
            float: Progress value from 0.0 to 1.0
        """
        if self._total_resources == 0:
            return 1.0
        return self._loaded_resources / self._total_resources

    def get_loaded_count(self) -> int:
        """
        Get the number of loaded resources.

        Returns:
            int: Number of resources loaded
        """
        return self._loaded_resources

    def get_total_count(self) -> int:
        """
        Get the total number of resources to load.

        Returns:
            int: Total number of resources
        """
        return self._total_resources

    def get_cache_size(self) -> int:
        """
        Get the number of cached resources.

        Returns:
            int: Number of cached resources
        """
        return len(self._resources)
