"""
Unit tests for SoundPlayer

Tests sound effect loading, caching, and playback.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import pygame

from src.audio.sound_player import SoundPlayer


@pytest.fixture
def mock_audio_manager():
    """Create a mock AudioManager."""
    manager = Mock()
    manager.is_initialized.return_value = True
    manager.get_master_volume.return_value = 1.0
    manager.get_effective_sfx_volume.return_value = 0.8
    return manager


@pytest.fixture
def sound_player(mock_audio_manager):
    """Create a SoundPlayer instance with mock AudioManager."""
    return SoundPlayer(mock_audio_manager)


class TestSoundPlayerInit:
    """Test SoundPlayer initialization."""

    def test_init(self, mock_audio_manager):
        """Test initialization."""
        player = SoundPlayer(mock_audio_manager)

        assert player._audio_manager is mock_audio_manager
        assert len(player._sound_cache) == 0


class TestSoundPlayerLoadSound:
    """Test sound loading."""

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_load_sound_success(self, mock_sound_class, mock_get_root, sound_player):
        """Test successful sound loading."""
        # Setup mocks
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.load_sound("sfx/test.wav")

        assert result is mock_sound
        assert "sfx/test.wav" in sound_player._sound_cache
        mock_sound_class.assert_called_once()

    @patch('src.audio.sound_player.get_project_root')
    def test_load_sound_file_not_found(self, mock_get_root, sound_player):
        """Test loading non-existent sound."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root

        with patch('pathlib.Path.exists', return_value=False):
            result = sound_player.load_sound("sfx/missing.wav")

        assert result is None
        assert "sfx/missing.wav" not in sound_player._sound_cache

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound', side_effect=pygame.error("Test error"))
    def test_load_sound_pygame_error(self, mock_sound_class, mock_get_root, sound_player):
        """Test sound loading with pygame error."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.load_sound("sfx/error.wav")

        assert result is None
        assert "sfx/error.wav" not in sound_player._sound_cache

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_load_sound_from_cache(self, mock_sound_class, mock_get_root, sound_player):
        """Test loading sound from cache."""
        # Setup mocks
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        # Load sound first time
        with patch('pathlib.Path.exists', return_value=True):
            sound_player.load_sound("sfx/test.wav")

        # Load again (should use cache)
        result = sound_player.load_sound("sfx/test.wav")

        assert result is mock_sound
        assert mock_sound_class.call_count == 1  # Should only load once

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_load_sound_no_cache(self, mock_sound_class, mock_get_root, sound_player):
        """Test loading sound without caching."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.load_sound("sfx/test.wav", use_cache=False)

        assert result is mock_sound
        assert "sfx/test.wav" not in sound_player._sound_cache


class TestSoundPlayerPlaySound:
    """Test sound playback."""

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_play_sound_success(self, mock_sound_class, mock_get_root, sound_player, mock_audio_manager):
        """Test successful sound playback."""
        # Setup mocks
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.play_sound("sfx/test.wav")

        assert result is True
        mock_sound.set_volume.assert_called_once_with(0.8)  # effective_sfx_volume
        mock_sound.play.assert_called_once_with(loops=0, maxtime=0, fade_ms=0)

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_play_sound_with_custom_volume(self, mock_sound_class, mock_get_root, sound_player, mock_audio_manager):
        """Test playing sound with custom volume."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.play_sound("sfx/test.wav", volume=0.5)

        assert result is True
        mock_sound.set_volume.assert_called_once_with(0.5)  # master=1.0 * volume=0.5

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_play_sound_with_loops(self, mock_sound_class, mock_get_root, sound_player):
        """Test playing sound with loops."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.play_sound("sfx/test.wav", loops=3)

        assert result is True
        mock_sound.play.assert_called_once_with(loops=3, maxtime=0, fade_ms=0)

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_play_sound_with_fade(self, mock_sound_class, mock_get_root, sound_player):
        """Test playing sound with fade in."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.play_sound("sfx/test.wav", fade_ms=500)

        assert result is True
        mock_sound.play.assert_called_once_with(loops=0, maxtime=0, fade_ms=500)

    def test_play_sound_not_initialized(self, sound_player, mock_audio_manager):
        """Test playing sound when audio not initialized."""
        mock_audio_manager.is_initialized.return_value = False

        result = sound_player.play_sound("sfx/test.wav")

        assert result is False

    @patch('src.audio.sound_player.get_project_root')
    def test_play_sound_file_not_found(self, mock_get_root, sound_player):
        """Test playing non-existent sound."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root

        with patch('pathlib.Path.exists', return_value=False):
            result = sound_player.play_sound("sfx/missing.wav")

        assert result is False

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_play_sound_pygame_error(self, mock_sound_class, mock_get_root, sound_player):
        """Test playing sound with pygame error."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound.play.side_effect = pygame.error("Test error")
        mock_sound_class.return_value = mock_sound

        with patch('pathlib.Path.exists', return_value=True):
            result = sound_player.play_sound("sfx/test.wav")

        assert result is False


class TestSoundPlayerStopSound:
    """Test stopping sounds."""

    def test_stop_sound_cached(self, sound_player):
        """Test stopping a cached sound."""
        mock_sound = Mock()
        sound_player._sound_cache["sfx/test.wav"] = mock_sound

        sound_player.stop_sound("sfx/test.wav")

        mock_sound.stop.assert_called_once()

    def test_stop_sound_not_cached(self, sound_player):
        """Test stopping a non-cached sound."""
        sound_player.stop_sound("sfx/missing.wav")  # Should not raise exception

    @patch('pygame.mixer.stop')
    def test_stop_all_sounds(self, mock_stop, sound_player):
        """Test stopping all sounds."""
        sound_player.stop_all_sounds()

        mock_stop.assert_called_once()


class TestSoundPlayerCache:
    """Test sound cache management."""

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_preload_sounds(self, mock_sound_class, mock_get_root, sound_player):
        """Test preloading multiple sounds."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        sound_paths = ["sfx/sound1.wav", "sfx/sound2.wav", "sfx/sound3.wav"]

        with patch('pathlib.Path.exists', return_value=True):
            loaded_count = sound_player.preload_sounds(sound_paths)

        assert loaded_count == 3
        assert len(sound_player._sound_cache) == 3

    @patch('src.audio.sound_player.get_project_root')
    @patch('pygame.mixer.Sound')
    def test_preload_sounds_partial_failure(self, mock_sound_class, mock_get_root, sound_player):
        """Test preloading with some failures."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        mock_sound = Mock()
        mock_sound_class.return_value = mock_sound

        sound_paths = ["sfx/sound1.wav", "sfx/missing.wav", "sfx/sound3.wav"]

        # Create a list to track which files exist
        existing_files = [True, False, True]  # sound1 exists, missing doesn't, sound3 exists
        call_count = [0]

        def exists_impl():
            result = existing_files[call_count[0] % len(existing_files)]
            call_count[0] += 1
            return result

        with patch.object(Path, 'exists', side_effect=exists_impl):
            loaded_count = sound_player.preload_sounds(sound_paths)

        assert loaded_count == 2

    def test_clear_cache(self, sound_player):
        """Test clearing sound cache."""
        sound_player._sound_cache["sfx/test1.wav"] = Mock()
        sound_player._sound_cache["sfx/test2.wav"] = Mock()

        sound_player.clear_cache()

        assert len(sound_player._sound_cache) == 0

    def test_get_cached_sound_count(self, sound_player):
        """Test getting cached sound count."""
        sound_player._sound_cache["sfx/test1.wav"] = Mock()
        sound_player._sound_cache["sfx/test2.wav"] = Mock()

        count = sound_player.get_cached_sound_count()

        assert count == 2

    def test_is_sound_cached(self, sound_player):
        """Test checking if sound is cached."""
        sound_player._sound_cache["sfx/test.wav"] = Mock()

        assert sound_player.is_sound_cached("sfx/test.wav") is True
        assert sound_player.is_sound_cached("sfx/missing.wav") is False


class TestSoundPlayerFadeOut:
    """Test fade out functionality."""

    @patch('pygame.mixer.fadeout')
    def test_fade_out_all(self, mock_fadeout, sound_player):
        """Test fading out all sounds."""
        sound_player.fade_out_all(1000)

        mock_fadeout.assert_called_once_with(1000)
