"""
Unit tests for AudioManager

Tests audio system initialization, volume control, and state management.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame

from src.audio.audio_manager import AudioManager


class TestAudioManagerInit:
    """Test AudioManager initialization."""

    def test_init_default(self):
        """Test default initialization."""
        manager = AudioManager()

        assert manager.is_initialized() is False
        assert manager.get_master_volume() == 1.0
        assert manager.get_sfx_volume() == 1.0
        assert manager.get_bgm_volume() == 0.2  # Default 20% per spec


class TestAudioManagerInitialization:
    """Test audio system initialization and shutdown."""

    @patch('pygame.mixer.init')
    def test_initialize_success(self, mock_init):
        """Test successful initialization."""
        manager = AudioManager()
        result = manager.initialize()

        assert result is True
        assert manager.is_initialized() is True
        mock_init.assert_called_once_with(44100, -16, 2, 512)

    @patch('pygame.mixer.init')
    def test_initialize_custom_params(self, mock_init):
        """Test initialization with custom parameters."""
        manager = AudioManager()
        result = manager.initialize(frequency=22050, size=-8, channels=1, buffer=1024)

        assert result is True
        mock_init.assert_called_once_with(22050, -8, 1, 1024)

    @patch('pygame.mixer.init', side_effect=pygame.error("Test error"))
    def test_initialize_failure(self, mock_init):
        """Test initialization failure."""
        manager = AudioManager()
        result = manager.initialize()

        assert result is False
        assert manager.is_initialized() is False

    @patch('pygame.mixer.init')
    def test_initialize_already_initialized(self, mock_init):
        """Test initializing when already initialized."""
        manager = AudioManager()
        manager.initialize()
        result = manager.initialize()

        assert result is True
        assert mock_init.call_count == 1  # Should not call init again

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.quit')
    def test_shutdown(self, mock_quit, mock_init):
        """Test shutdown."""
        manager = AudioManager()
        manager.initialize()
        manager.shutdown()

        assert manager.is_initialized() is False
        mock_quit.assert_called_once()

    @patch('pygame.mixer.quit')
    def test_shutdown_not_initialized(self, mock_quit):
        """Test shutdown when not initialized."""
        manager = AudioManager()
        manager.shutdown()

        mock_quit.assert_not_called()

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.quit', side_effect=pygame.error("Test error"))
    def test_shutdown_error(self, mock_quit, mock_init):
        """Test shutdown with error."""
        manager = AudioManager()
        manager.initialize()
        manager.shutdown()  # Should not raise exception

        mock_quit.assert_called_once()


class TestAudioManagerMasterVolume:
    """Test master volume control."""

    def test_set_master_volume_valid(self):
        """Test setting valid master volume."""
        manager = AudioManager()
        manager.set_master_volume(0.5)

        assert manager.get_master_volume() == 0.5

    def test_set_master_volume_clamp_high(self):
        """Test clamping high master volume."""
        manager = AudioManager()
        manager.set_master_volume(1.5)

        assert manager.get_master_volume() == 1.0

    def test_set_master_volume_clamp_low(self):
        """Test clamping low master volume."""
        manager = AudioManager()
        manager.set_master_volume(-0.5)

        assert manager.get_master_volume() == 0.0

    def test_mute_all(self):
        """Test muting all audio."""
        manager = AudioManager()
        manager.set_master_volume(0.8)
        manager.mute_all()

        assert manager.get_master_volume() == 0.0

    def test_unmute_all(self):
        """Test unmuting all audio."""
        manager = AudioManager()
        manager.set_master_volume(0.0)
        manager.unmute_all()

        assert manager.get_master_volume() == 1.0


class TestAudioManagerSFXVolume:
    """Test sound effects volume control."""

    def test_set_sfx_volume_valid(self):
        """Test setting valid SFX volume."""
        manager = AudioManager()
        manager.set_sfx_volume(0.7)

        assert manager.get_sfx_volume() == 0.7

    def test_set_sfx_volume_clamp_high(self):
        """Test clamping high SFX volume."""
        manager = AudioManager()
        manager.set_sfx_volume(1.2)

        assert manager.get_sfx_volume() == 1.0

    def test_set_sfx_volume_clamp_low(self):
        """Test clamping low SFX volume."""
        manager = AudioManager()
        manager.set_sfx_volume(-0.3)

        assert manager.get_sfx_volume() == 0.0

    def test_get_effective_sfx_volume(self):
        """Test getting effective SFX volume."""
        manager = AudioManager()
        manager.set_master_volume(0.8)
        manager.set_sfx_volume(0.5)

        assert manager.get_effective_sfx_volume() == 0.4  # 0.8 * 0.5


class TestAudioManagerBGMVolume:
    """Test background music volume control."""

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.music.set_volume')
    def test_set_bgm_volume_valid(self, mock_set_volume, mock_init):
        """Test setting valid BGM volume."""
        manager = AudioManager()
        manager.initialize()
        manager.set_bgm_volume(0.3)

        assert manager.get_bgm_volume() == 0.3
        mock_set_volume.assert_called_with(0.3)  # master=1.0 * bgm=0.3

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.music.set_volume')
    def test_set_bgm_volume_clamp_high(self, mock_set_volume, mock_init):
        """Test clamping high BGM volume."""
        manager = AudioManager()
        manager.initialize()
        manager.set_bgm_volume(1.5)

        assert manager.get_bgm_volume() == 1.0

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.music.set_volume')
    def test_set_bgm_volume_clamp_low(self, mock_set_volume, mock_init):
        """Test clamping low BGM volume."""
        manager = AudioManager()
        manager.initialize()
        manager.set_bgm_volume(-0.2)

        assert manager.get_bgm_volume() == 0.0

    def test_set_bgm_volume_not_initialized(self):
        """Test setting BGM volume when not initialized."""
        manager = AudioManager()
        manager.set_bgm_volume(0.5)

        assert manager.get_bgm_volume() == 0.5  # Should still set internal value

    def test_get_effective_bgm_volume(self):
        """Test getting effective BGM volume."""
        manager = AudioManager()
        manager.set_master_volume(0.8)
        manager.set_bgm_volume(0.5)

        assert manager.get_effective_bgm_volume() == 0.4  # 0.8 * 0.5


class TestAudioManagerPlaybackControl:
    """Test audio playback control."""

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.pause')
    @patch('pygame.mixer.music.pause')
    def test_pause_all(self, mock_music_pause, mock_pause, mock_init):
        """Test pausing all audio."""
        manager = AudioManager()
        manager.initialize()
        manager.pause_all()

        mock_pause.assert_called_once()
        mock_music_pause.assert_called_once()

    @patch('pygame.mixer.pause')
    @patch('pygame.mixer.music.pause')
    def test_pause_all_not_initialized(self, mock_music_pause, mock_pause):
        """Test pausing when not initialized."""
        manager = AudioManager()
        manager.pause_all()

        mock_pause.assert_not_called()
        mock_music_pause.assert_not_called()

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.unpause')
    @patch('pygame.mixer.music.unpause')
    def test_resume_all(self, mock_music_unpause, mock_unpause, mock_init):
        """Test resuming all audio."""
        manager = AudioManager()
        manager.initialize()
        manager.resume_all()

        mock_unpause.assert_called_once()
        mock_music_unpause.assert_called_once()

    @patch('pygame.mixer.unpause')
    @patch('pygame.mixer.music.unpause')
    def test_resume_all_not_initialized(self, mock_music_unpause, mock_unpause):
        """Test resuming when not initialized."""
        manager = AudioManager()
        manager.resume_all()

        mock_unpause.assert_not_called()
        mock_music_unpause.assert_not_called()

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.stop')
    @patch('pygame.mixer.music.stop')
    def test_stop_all(self, mock_music_stop, mock_stop, mock_init):
        """Test stopping all audio."""
        manager = AudioManager()
        manager.initialize()
        manager.stop_all()

        mock_stop.assert_called_once()
        mock_music_stop.assert_called_once()

    @patch('pygame.mixer.stop')
    @patch('pygame.mixer.music.stop')
    def test_stop_all_not_initialized(self, mock_music_stop, mock_stop):
        """Test stopping when not initialized."""
        manager = AudioManager()
        manager.stop_all()

        mock_stop.assert_not_called()
        mock_music_stop.assert_not_called()
