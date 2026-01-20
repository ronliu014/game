"""
Unit tests for BGMController

Tests background music loading, playback, and control.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import pygame

from src.audio.bgm_controller import BGMController


@pytest.fixture
def mock_audio_manager():
    """Create a mock AudioManager."""
    manager = Mock()
    manager.is_initialized.return_value = True
    manager.get_effective_bgm_volume.return_value = 0.2
    manager.get_bgm_volume.return_value = 0.2
    return manager


@pytest.fixture
def bgm_controller(mock_audio_manager):
    """Create a BGMController instance with mock AudioManager."""
    return BGMController(mock_audio_manager)


class TestBGMControllerInit:
    """Test BGMController initialization."""

    def test_init(self, mock_audio_manager):
        """Test initialization."""
        controller = BGMController(mock_audio_manager)

        assert controller._audio_manager is mock_audio_manager
        assert controller._current_bgm is None
        assert controller._is_playing is False


class TestBGMControllerLoadBGM:
    """Test BGM loading."""

    @patch('src.audio.bgm_controller.get_project_root')
    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.set_volume')
    def test_load_bgm_success(self, mock_set_volume, mock_load, mock_get_root,
                              bgm_controller, mock_audio_manager):
        """Test successful BGM loading."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root

        with patch('pathlib.Path.exists', return_value=True):
            result = bgm_controller.load_bgm("bgm/theme.mp3")

        assert result is True
        assert bgm_controller._current_bgm == "bgm/theme.mp3"
        mock_load.assert_called_once()
        mock_set_volume.assert_called_once_with(0.2)

    @patch('src.audio.bgm_controller.get_project_root')
    def test_load_bgm_file_not_found(self, mock_get_root, bgm_controller):
        """Test loading non-existent BGM."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root

        with patch('pathlib.Path.exists', return_value=False):
            result = bgm_controller.load_bgm("bgm/missing.mp3")

        assert result is False
        assert bgm_controller._current_bgm is None

    @patch('src.audio.bgm_controller.get_project_root')
    @patch('pygame.mixer.music.load', side_effect=pygame.error("Test error"))
    def test_load_bgm_pygame_error(self, mock_load, mock_get_root, bgm_controller):
        """Test BGM loading with pygame error."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root

        with patch('pathlib.Path.exists', return_value=True):
            result = bgm_controller.load_bgm("bgm/error.mp3")

        assert result is False
        assert bgm_controller._current_bgm is None

    def test_load_bgm_not_initialized(self, bgm_controller, mock_audio_manager):
        """Test loading BGM when audio not initialized."""
        mock_audio_manager.is_initialized.return_value = False

        result = bgm_controller.load_bgm("bgm/theme.mp3")

        assert result is False

    @patch('src.audio.bgm_controller.get_project_root')
    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.set_volume')
    @patch('pygame.mixer.music.stop')
    def test_load_bgm_stops_current(self, mock_stop, mock_set_volume, mock_load,
                                    mock_get_root, bgm_controller):
        """Test loading new BGM stops current BGM."""
        mock_root = Path("/fake/root")
        mock_get_root.return_value = mock_root
        bgm_controller._is_playing = True

        with patch('pathlib.Path.exists', return_value=True):
            bgm_controller.load_bgm("bgm/new_theme.mp3")

        mock_stop.assert_called_once()


class TestBGMControllerPlay:
    """Test BGM playback."""

    @patch('pygame.mixer.music.play')
    def test_play_success(self, mock_play, bgm_controller):
        """Test successful BGM playback."""
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.play()

        assert result is True
        assert bgm_controller._is_playing is True
        mock_play.assert_called_once_with(loops=-1, start=0.0, fade_ms=0)

    @patch('pygame.mixer.music.play')
    def test_play_with_loops(self, mock_play, bgm_controller):
        """Test playing BGM with custom loops."""
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.play(loops=3)

        assert result is True
        mock_play.assert_called_once_with(loops=3, start=0.0, fade_ms=0)

    @patch('pygame.mixer.music.play')
    def test_play_with_start_position(self, mock_play, bgm_controller):
        """Test playing BGM from specific position."""
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.play(start=10.5)

        assert result is True
        mock_play.assert_called_once_with(loops=-1, start=10.5, fade_ms=0)

    @patch('pygame.mixer.music.play')
    def test_play_with_fade_in(self, mock_play, bgm_controller):
        """Test playing BGM with fade in."""
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.play(fade_ms=2000)

        assert result is True
        mock_play.assert_called_once_with(loops=-1, start=0.0, fade_ms=2000)

    def test_play_no_bgm_loaded(self, bgm_controller):
        """Test playing when no BGM is loaded."""
        result = bgm_controller.play()

        assert result is False
        assert bgm_controller._is_playing is False

    def test_play_not_initialized(self, bgm_controller, mock_audio_manager):
        """Test playing when audio not initialized."""
        mock_audio_manager.is_initialized.return_value = False
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.play()

        assert result is False

    @patch('pygame.mixer.music.play', side_effect=pygame.error("Test error"))
    def test_play_pygame_error(self, mock_play, bgm_controller):
        """Test playing with pygame error."""
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.play()

        assert result is False


class TestBGMControllerStop:
    """Test stopping BGM."""

    @patch('pygame.mixer.music.stop')
    def test_stop(self, mock_stop, bgm_controller):
        """Test stopping BGM."""
        bgm_controller._is_playing = True

        bgm_controller.stop()

        assert bgm_controller._is_playing is False
        mock_stop.assert_called_once()

    @patch('pygame.mixer.music.stop')
    def test_stop_not_playing(self, mock_stop, bgm_controller):
        """Test stopping when not playing."""
        bgm_controller._is_playing = False

        bgm_controller.stop()

        mock_stop.assert_not_called()


class TestBGMControllerPause:
    """Test pausing and resuming BGM."""

    @patch('pygame.mixer.music.pause')
    def test_pause(self, mock_pause, bgm_controller):
        """Test pausing BGM."""
        bgm_controller._is_playing = True

        bgm_controller.pause()

        mock_pause.assert_called_once()

    @patch('pygame.mixer.music.pause')
    def test_pause_not_playing(self, mock_pause, bgm_controller):
        """Test pausing when not playing."""
        bgm_controller._is_playing = False

        bgm_controller.pause()

        mock_pause.assert_not_called()

    @patch('pygame.mixer.music.unpause')
    def test_unpause(self, mock_unpause, bgm_controller):
        """Test resuming BGM."""
        bgm_controller.unpause()

        mock_unpause.assert_called_once()


class TestBGMControllerFadeOut:
    """Test fade out functionality."""

    @patch('pygame.mixer.music.fadeout')
    def test_fade_out(self, mock_fadeout, bgm_controller):
        """Test fading out BGM."""
        bgm_controller._is_playing = True

        bgm_controller.fade_out(1500)

        assert bgm_controller._is_playing is False
        mock_fadeout.assert_called_once_with(1500)

    @patch('pygame.mixer.music.fadeout')
    def test_fade_out_not_playing(self, mock_fadeout, bgm_controller):
        """Test fading out when not playing."""
        bgm_controller._is_playing = False

        bgm_controller.fade_out(1500)

        mock_fadeout.assert_not_called()


class TestBGMControllerVolume:
    """Test volume control."""

    def test_set_volume(self, bgm_controller, mock_audio_manager):
        """Test setting BGM volume."""
        bgm_controller.set_volume(0.5)

        mock_audio_manager.set_bgm_volume.assert_called_once_with(0.5)

    def test_get_volume(self, bgm_controller, mock_audio_manager):
        """Test getting BGM volume."""
        volume = bgm_controller.get_volume()

        assert volume == 0.2
        mock_audio_manager.get_bgm_volume.assert_called_once()


class TestBGMControllerIsPlaying:
    """Test playback status checking."""

    @patch('pygame.mixer.music.get_busy', return_value=True)
    def test_is_playing_true(self, mock_get_busy, bgm_controller):
        """Test checking if BGM is playing (true)."""
        bgm_controller._is_playing = True

        result = bgm_controller.is_playing()

        assert result is True

    @patch('pygame.mixer.music.get_busy', return_value=False)
    def test_is_playing_false_updates_state(self, mock_get_busy, bgm_controller):
        """Test that is_playing updates internal state."""
        bgm_controller._is_playing = True

        result = bgm_controller.is_playing()

        assert result is False
        assert bgm_controller._is_playing is False

    @patch('pygame.mixer.music.get_busy', return_value=False)
    def test_is_playing_false(self, mock_get_busy, bgm_controller):
        """Test checking if BGM is playing (false)."""
        bgm_controller._is_playing = False

        result = bgm_controller.is_playing()

        assert result is False


class TestBGMControllerGetCurrentBGM:
    """Test getting current BGM."""

    def test_get_current_bgm_loaded(self, bgm_controller):
        """Test getting current BGM when loaded."""
        bgm_controller._current_bgm = "bgm/theme.mp3"

        result = bgm_controller.get_current_bgm()

        assert result == "bgm/theme.mp3"

    def test_get_current_bgm_none(self, bgm_controller):
        """Test getting current BGM when none loaded."""
        result = bgm_controller.get_current_bgm()

        assert result is None


class TestBGMControllerRewind:
    """Test rewinding BGM."""

    @patch('pygame.mixer.music.rewind')
    def test_rewind(self, mock_rewind, bgm_controller):
        """Test rewinding BGM."""
        bgm_controller.rewind()

        mock_rewind.assert_called_once()


class TestBGMControllerSetPosition:
    """Test setting playback position."""

    @patch('pygame.mixer.music.set_pos')
    def test_set_position_success(self, mock_set_pos, bgm_controller):
        """Test setting playback position."""
        bgm_controller.set_position(30.5)

        mock_set_pos.assert_called_once_with(30.5)

    @patch('pygame.mixer.music.set_pos', side_effect=pygame.error("Not supported"))
    def test_set_position_error(self, mock_set_pos, bgm_controller):
        """Test setting position with error (e.g., MP3 format)."""
        bgm_controller.set_position(30.5)  # Should not raise exception

        mock_set_pos.assert_called_once_with(30.5)


class TestBGMControllerGetBusy:
    """Test checking if music is busy."""

    @patch('pygame.mixer.music.get_busy', return_value=True)
    def test_get_busy_true(self, mock_get_busy, bgm_controller):
        """Test get_busy returns True."""
        result = bgm_controller.get_busy()

        assert result is True
        mock_get_busy.assert_called_once()

    @patch('pygame.mixer.music.get_busy', return_value=False)
    def test_get_busy_false(self, mock_get_busy, bgm_controller):
        """Test get_busy returns False."""
        result = bgm_controller.get_busy()

        assert result is False
        mock_get_busy.assert_called_once()
