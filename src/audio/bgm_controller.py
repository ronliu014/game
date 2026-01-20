"""
BGM Controller

Handles background music playback and control.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
from typing import Optional
from pathlib import Path
from src.utils.logger import GameLogger
from src.utils.file_utils import get_project_root


class BGMController:
    """
    Background music controller.

    Manages loading and playback of background music using pygame.mixer.music.
    Supports looping, volume control, and fade effects.

    Attributes:
        _audio_manager: Reference to AudioManager for volume control
        _current_bgm (Optional[str]): Currently loaded BGM path
        _is_playing (bool): Whether BGM is currently playing
        _logger (GameLogger): Logger instance
    """

    def __init__(self, audio_manager) -> None:
        """
        Initialize the BGM controller.

        Args:
            audio_manager: AudioManager instance for volume control
        """
        self._audio_manager = audio_manager
        self._current_bgm: Optional[str] = None
        self._is_playing: bool = False
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def load_bgm(self, relative_path: str) -> bool:
        """
        Load a background music file.

        Args:
            relative_path: Path relative to assets/audio/ directory

        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not self._audio_manager.is_initialized():
            self._logger.warning("Cannot load BGM: AudioManager not initialized")
            return False

        # Build full path
        project_root = get_project_root()
        full_path = project_root / "assets" / "audio" / relative_path

        # Check if file exists
        if not full_path.exists():
            self._logger.error(f"BGM file not found: {full_path}")
            return False

        # Stop current BGM if playing
        if self._is_playing:
            self.stop()

        # Load BGM
        try:
            pygame.mixer.music.load(str(full_path))
            self._current_bgm = relative_path

            # Set volume
            effective_volume = self._audio_manager.get_effective_bgm_volume()
            pygame.mixer.music.set_volume(effective_volume)

            self._logger.info(f"BGM loaded: {relative_path}")
            return True

        except pygame.error as e:
            self._logger.error(f"Failed to load BGM {relative_path}: {e}")
            return False

    def play(self, loops: int = -1, start: float = 0.0, fade_ms: int = 0) -> bool:
        """
        Play the loaded background music.

        Args:
            loops: Number of times to loop (-1 for infinite, 0 for once)
            start: Starting position in seconds
            fade_ms: Fade in duration in milliseconds

        Returns:
            bool: True if playback started successfully, False otherwise
        """
        if not self._audio_manager.is_initialized():
            self._logger.warning("Cannot play BGM: AudioManager not initialized")
            return False

        if self._current_bgm is None:
            self._logger.warning("Cannot play BGM: No BGM loaded")
            return False

        try:
            pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
            self._is_playing = True
            self._logger.info(
                f"Playing BGM: {self._current_bgm} (loops={loops}, fade_ms={fade_ms})"
            )
            return True

        except pygame.error as e:
            self._logger.error(f"Failed to play BGM: {e}")
            return False

    def stop(self) -> None:
        """Stop the background music."""
        if not self._is_playing:
            return

        pygame.mixer.music.stop()
        self._is_playing = False
        self._logger.debug("BGM stopped")

    def pause(self) -> None:
        """Pause the background music."""
        if not self._is_playing:
            return

        pygame.mixer.music.pause()
        self._logger.debug("BGM paused")

    def unpause(self) -> None:
        """Resume the background music."""
        pygame.mixer.music.unpause()
        self._logger.debug("BGM resumed")

    def fade_out(self, fade_ms: int) -> None:
        """
        Fade out the background music.

        Args:
            fade_ms: Fade out duration in milliseconds
        """
        if not self._is_playing:
            return

        pygame.mixer.music.fadeout(fade_ms)
        self._is_playing = False
        self._logger.debug(f"BGM fading out over {fade_ms}ms")

    def set_volume(self, volume: float) -> None:
        """
        Set BGM volume through AudioManager.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self._audio_manager.set_bgm_volume(volume)

    def get_volume(self) -> float:
        """
        Get current BGM volume from AudioManager.

        Returns:
            float: BGM volume (0.0 to 1.0)
        """
        return self._audio_manager.get_bgm_volume()

    def is_playing(self) -> bool:
        """
        Check if BGM is currently playing.

        Returns:
            bool: True if playing, False otherwise
        """
        # Update internal state based on pygame
        if self._is_playing and not pygame.mixer.music.get_busy():
            self._is_playing = False

        return self._is_playing

    def get_current_bgm(self) -> Optional[str]:
        """
        Get the currently loaded BGM path.

        Returns:
            Optional[str]: Current BGM path, or None if no BGM loaded
        """
        return self._current_bgm

    def rewind(self) -> None:
        """Rewind the background music to the beginning."""
        pygame.mixer.music.rewind()
        self._logger.debug("BGM rewound to start")

    def set_position(self, position: float) -> None:
        """
        Set playback position (OGG only).

        Args:
            position: Position in seconds
        """
        try:
            pygame.mixer.music.set_pos(position)
            self._logger.debug(f"BGM position set to {position}s")
        except pygame.error as e:
            self._logger.warning(f"Failed to set BGM position: {e}")

    def get_busy(self) -> bool:
        """
        Check if music is actively playing.

        Returns:
            bool: True if music is playing, False otherwise
        """
        return pygame.mixer.music.get_busy()
