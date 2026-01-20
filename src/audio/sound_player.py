"""
Sound Player

Handles loading and playback of sound effects.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
from typing import Dict, Optional
from pathlib import Path
from src.utils.logger import GameLogger
from src.utils.file_utils import get_project_root


class SoundPlayer:
    """
    Sound effect player with caching and volume control.

    Manages loading, caching, and playback of sound effects.
    Supports multiple simultaneous sound playback.

    Attributes:
        _sound_cache (Dict[str, pygame.mixer.Sound]): Cached sound objects
        _audio_manager: Reference to AudioManager for volume control
        _logger (GameLogger): Logger instance
    """

    def __init__(self, audio_manager) -> None:
        """
        Initialize the sound player.

        Args:
            audio_manager: AudioManager instance for volume control
        """
        self._sound_cache: Dict[str, pygame.mixer.Sound] = {}
        self._audio_manager = audio_manager
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def load_sound(self, relative_path: str, use_cache: bool = True) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound effect from file.

        Args:
            relative_path: Path relative to assets/audio/ directory
            use_cache: Whether to use cached sound if available

        Returns:
            pygame.mixer.Sound: Loaded sound object, or None if failed
        """
        # Check cache first
        if use_cache and relative_path in self._sound_cache:
            self._logger.debug(f"Sound loaded from cache: {relative_path}")
            return self._sound_cache[relative_path]

        # Build full path
        project_root = get_project_root()
        full_path = project_root / "assets" / "audio" / relative_path

        # Check if file exists
        if not full_path.exists():
            self._logger.error(f"Sound file not found: {full_path}")
            return None

        # Load sound
        try:
            sound = pygame.mixer.Sound(str(full_path))

            # Cache the sound
            if use_cache:
                self._sound_cache[relative_path] = sound
                self._logger.debug(f"Sound loaded and cached: {relative_path}")
            else:
                self._logger.debug(f"Sound loaded (no cache): {relative_path}")

            return sound

        except pygame.error as e:
            self._logger.error(f"Failed to load sound {relative_path}: {e}")
            return None

    def play_sound(self, relative_path: str, volume: Optional[float] = None,
                   loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> bool:
        """
        Play a sound effect.

        Args:
            relative_path: Path relative to assets/audio/ directory
            volume: Override volume (0.0 to 1.0), None uses AudioManager volume
            loops: Number of times to loop (-1 for infinite, 0 for once)
            maxtime: Stop playback after this many milliseconds (0 for no limit)
            fade_ms: Fade in duration in milliseconds

        Returns:
            bool: True if playback started successfully, False otherwise
        """
        if not self._audio_manager.is_initialized():
            self._logger.warning("Cannot play sound: AudioManager not initialized")
            return False

        # Load sound
        sound = self.load_sound(relative_path)
        if sound is None:
            return False

        # Set volume
        if volume is not None:
            # Use provided volume with master volume
            effective_volume = self._audio_manager.get_master_volume() * volume
        else:
            # Use AudioManager's SFX volume
            effective_volume = self._audio_manager.get_effective_sfx_volume()

        sound.set_volume(effective_volume)

        # Play sound
        try:
            sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
            self._logger.debug(
                f"Playing sound: {relative_path} (volume={effective_volume:.2f})"
            )
            return True

        except pygame.error as e:
            self._logger.error(f"Failed to play sound {relative_path}: {e}")
            return False

    def stop_sound(self, relative_path: str) -> None:
        """
        Stop a specific sound effect.

        Args:
            relative_path: Path relative to assets/audio/ directory
        """
        if relative_path in self._sound_cache:
            sound = self._sound_cache[relative_path]
            sound.stop()
            self._logger.debug(f"Stopped sound: {relative_path}")

    def stop_all_sounds(self) -> None:
        """Stop all currently playing sound effects."""
        pygame.mixer.stop()
        self._logger.debug("All sounds stopped")

    def preload_sounds(self, sound_paths: list[str]) -> int:
        """
        Preload multiple sound effects into cache.

        Args:
            sound_paths: List of paths relative to assets/audio/ directory

        Returns:
            int: Number of sounds successfully loaded
        """
        loaded_count = 0
        for path in sound_paths:
            if self.load_sound(path) is not None:
                loaded_count += 1

        self._logger.info(f"Preloaded {loaded_count}/{len(sound_paths)} sounds")
        return loaded_count

    def clear_cache(self) -> None:
        """Clear the sound cache to free memory."""
        self._sound_cache.clear()
        self._logger.info("Sound cache cleared")

    def get_cached_sound_count(self) -> int:
        """
        Get the number of sounds in cache.

        Returns:
            int: Number of cached sounds
        """
        return len(self._sound_cache)

    def is_sound_cached(self, relative_path: str) -> bool:
        """
        Check if a sound is in cache.

        Args:
            relative_path: Path relative to assets/audio/ directory

        Returns:
            bool: True if sound is cached, False otherwise
        """
        return relative_path in self._sound_cache

    def fade_out_all(self, fade_ms: int) -> None:
        """
        Fade out all currently playing sounds.

        Args:
            fade_ms: Fade out duration in milliseconds
        """
        pygame.mixer.fadeout(fade_ms)
        self._logger.debug(f"Fading out all sounds over {fade_ms}ms")
