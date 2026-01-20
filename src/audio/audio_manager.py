"""
Audio Manager

Centralized audio management system for the game.
Handles initialization, volume control, and coordination of sound effects and BGM.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
from typing import Optional
from src.utils.logger import GameLogger


class AudioManager:
    """
    Centralized audio manager for the game.

    Manages pygame mixer initialization, global volume control,
    and provides access to sound player and BGM controller.

    Attributes:
        _initialized (bool): Whether pygame mixer is initialized
        _master_volume (float): Master volume (0.0 to 1.0)
        _sfx_volume (float): Sound effects volume (0.0 to 1.0)
        _bgm_volume (float): Background music volume (0.0 to 1.0)
        _logger (GameLogger): Logger instance
    """

    def __init__(self) -> None:
        """Initialize the audio manager."""
        self._initialized: bool = False
        self._master_volume: float = 1.0
        self._sfx_volume: float = 1.0
        self._bgm_volume: float = 0.2  # BGM at 20% by default (per spec)
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def initialize(self, frequency: int = 44100, size: int = -16,
                   channels: int = 2, buffer: int = 512) -> bool:
        """
        Initialize pygame mixer for audio playback.

        Args:
            frequency: Sample rate in Hz (default: 44100)
            size: Sample size in bits (default: -16 for signed 16-bit)
            channels: Number of audio channels (default: 2 for stereo)
            buffer: Audio buffer size (default: 512)

        Returns:
            bool: True if initialization successful, False otherwise
        """
        if self._initialized:
            self._logger.warning("AudioManager already initialized")
            return True

        try:
            pygame.mixer.init(frequency, size, channels, buffer)
            self._initialized = True
            self._logger.info(
                f"AudioManager initialized: {frequency}Hz, {channels} channels, "
                f"buffer={buffer}"
            )
            return True
        except pygame.error as e:
            self._logger.error(f"Failed to initialize audio: {e}")
            return False

    def shutdown(self) -> None:
        """Shutdown the audio system and release resources."""
        if not self._initialized:
            return

        try:
            pygame.mixer.quit()
            self._initialized = False
            self._logger.info("AudioManager shutdown complete")
        except pygame.error as e:
            self._logger.error(f"Error during audio shutdown: {e}")

    def is_initialized(self) -> bool:
        """
        Check if audio system is initialized.

        Returns:
            bool: True if initialized, False otherwise
        """
        return self._initialized

    def set_master_volume(self, volume: float) -> None:
        """
        Set master volume for all audio.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        self._master_volume = volume
        self._logger.debug(f"Master volume set to {volume:.2f}")

    def get_master_volume(self) -> float:
        """
        Get current master volume.

        Returns:
            float: Master volume (0.0 to 1.0)
        """
        return self._master_volume

    def set_sfx_volume(self, volume: float) -> None:
        """
        Set volume for sound effects.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        self._sfx_volume = volume
        self._logger.debug(f"SFX volume set to {volume:.2f}")

    def get_sfx_volume(self) -> float:
        """
        Get current sound effects volume.

        Returns:
            float: SFX volume (0.0 to 1.0)
        """
        return self._sfx_volume

    def get_effective_sfx_volume(self) -> float:
        """
        Get effective SFX volume (master * sfx).

        Returns:
            float: Effective SFX volume (0.0 to 1.0)
        """
        return self._master_volume * self._sfx_volume

    def set_bgm_volume(self, volume: float) -> None:
        """
        Set volume for background music.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        self._bgm_volume = volume

        # Apply to pygame music if initialized
        if self._initialized:
            effective_volume = self._master_volume * self._bgm_volume
            pygame.mixer.music.set_volume(effective_volume)

        self._logger.debug(f"BGM volume set to {volume:.2f}")

    def get_bgm_volume(self) -> float:
        """
        Get current background music volume.

        Returns:
            float: BGM volume (0.0 to 1.0)
        """
        return self._bgm_volume

    def get_effective_bgm_volume(self) -> float:
        """
        Get effective BGM volume (master * bgm).

        Returns:
            float: Effective BGM volume (0.0 to 1.0)
        """
        return self._master_volume * self._bgm_volume

    def mute_all(self) -> None:
        """Mute all audio (set master volume to 0)."""
        self.set_master_volume(0.0)
        self._logger.info("All audio muted")

    def unmute_all(self) -> None:
        """Unmute all audio (restore master volume to 1.0)."""
        self.set_master_volume(1.0)
        self._logger.info("All audio unmuted")

    def pause_all(self) -> None:
        """Pause all audio playback."""
        if not self._initialized:
            return

        pygame.mixer.pause()
        pygame.mixer.music.pause()
        self._logger.debug("All audio paused")

    def resume_all(self) -> None:
        """Resume all audio playback."""
        if not self._initialized:
            return

        pygame.mixer.unpause()
        pygame.mixer.music.unpause()
        self._logger.debug("All audio resumed")

    def stop_all(self) -> None:
        """Stop all audio playback."""
        if not self._initialized:
            return

        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self._logger.debug("All audio stopped")
