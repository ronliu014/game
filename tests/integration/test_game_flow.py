"""
Integration tests for game flow

Tests the complete game flow including GameAPI, GameController,
GameLoop, and SceneManager integration.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame

from src.integration.game_api import GameAPI
from src.integration.game_controller import GameController
from src.integration.game_loop import GameLoop
from src.integration.scene_manager import SceneManager, Scene, SceneType
from src.core.game_state.game_state import GameState


class TestSceneManagerIntegration:
    """Test SceneManager integration."""

    def test_scene_registration_and_switching(self):
        """Test registering and switching between scenes."""
        manager = SceneManager()

        # Create test scenes
        menu_scene = Scene(SceneType.MENU)
        game_scene = Scene(SceneType.GAME)

        # Register scenes
        manager.register_scene(SceneType.MENU, menu_scene)
        manager.register_scene(SceneType.GAME, game_scene)

        # Push menu scene
        assert manager.push_scene(SceneType.MENU) is True
        assert manager.get_current_scene() == menu_scene
        assert menu_scene.is_active() is True

        # Change to game scene
        assert manager.change_scene(SceneType.GAME) is True
        assert manager.get_current_scene() == game_scene
        assert game_scene.is_active() is True
        assert menu_scene.is_active() is False

    def test_scene_stack_operations(self):
        """Test scene stack push and pop operations."""
        manager = SceneManager()

        menu_scene = Scene(SceneType.MENU)
        game_scene = Scene(SceneType.GAME)
        pause_scene = Scene(SceneType.PAUSE)

        manager.register_scene(SceneType.MENU, menu_scene)
        manager.register_scene(SceneType.GAME, game_scene)
        manager.register_scene(SceneType.PAUSE, pause_scene)

        # Build scene stack
        manager.push_scene(SceneType.MENU)
        manager.push_scene(SceneType.GAME)
        manager.push_scene(SceneType.PAUSE)

        assert manager.get_scene_count() == 3
        assert manager.get_current_scene() == pause_scene

        # Pop scenes
        popped = manager.pop_scene()
        assert popped == pause_scene
        assert manager.get_scene_count() == 2
        assert manager.get_current_scene() == game_scene

    def test_scene_clear(self):
        """Test clearing all scenes."""
        manager = SceneManager()

        menu_scene = Scene(SceneType.MENU)
        game_scene = Scene(SceneType.GAME)

        manager.register_scene(SceneType.MENU, menu_scene)
        manager.register_scene(SceneType.GAME, game_scene)

        manager.push_scene(SceneType.MENU)
        manager.push_scene(SceneType.GAME)

        assert manager.get_scene_count() == 2

        manager.clear_scenes()

        assert manager.get_scene_count() == 0
        assert manager.get_current_scene() is None


class TestGameLoopIntegration:
    """Test GameLoop integration."""

    def test_game_loop_initialization(self):
        """Test game loop initialization."""
        loop = GameLoop(target_fps=60)

        assert loop.is_running() is False
        assert loop.get_target_fps() == 60

    def test_game_loop_start_stop(self):
        """Test starting and stopping game loop."""
        loop = GameLoop()

        loop.start()
        assert loop.is_running() is True

        loop.stop()
        assert loop.is_running() is False

    def test_game_loop_fps_setting(self):
        """Test setting target FPS."""
        loop = GameLoop(target_fps=30)

        assert loop.get_target_fps() == 30

        loop.set_target_fps(60)
        assert loop.get_target_fps() == 60


@patch('pygame.display.set_mode')
@patch('pygame.display.set_caption')
@patch('pygame.init')
class TestGameControllerIntegration:
    """Test GameController integration."""

    def test_controller_initialization(self, mock_init, mock_caption, mock_set_mode):
        """Test game controller initialization."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface

        controller = GameController()
        success = controller.initialize(800, 600)

        assert success is True
        mock_init.assert_called()

    def test_controller_shutdown(self, mock_init, mock_caption, mock_set_mode):
        """Test game controller shutdown."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface

        controller = GameController()
        controller.initialize(800, 600)
        controller.shutdown()

        # Should not raise any exceptions

    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_load_levels(self, mock_load_level, mock_init, mock_caption, mock_set_mode):
        """Test loading levels."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True

        controller = GameController()
        controller.initialize(800, 600)

        level_ids = ["level_001", "level_002"]
        success = controller.load_levels(level_ids)

        assert success is True
        assert controller._level_ids == level_ids
        assert controller._current_level_index == 0

    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_next_level(self, mock_load_level, mock_init, mock_caption, mock_set_mode):
        """Test advancing to next level."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True

        controller = GameController()
        controller.initialize(800, 600)
        controller.load_levels(["level_001", "level_002"])

        # Advance to next level
        has_next = controller.next_level()

        assert has_next is True
        assert controller._current_level_index == 1

        # Try to advance beyond last level
        has_next = controller.next_level()

        assert has_next is False

    def test_get_state(self, mock_init, mock_caption, mock_set_mode):
        """Test getting game state."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface

        controller = GameController()
        controller.initialize(800, 600)

        state = controller.get_state()
        assert isinstance(state, GameState)


@patch('pygame.display.set_mode')
@patch('pygame.display.set_caption')
@patch('pygame.init')
@patch('pygame.mixer.init')
class TestGameAPIIntegration:
    """Test GameAPI integration."""

    def test_api_initialization(self, mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test API initialization."""
        api = GameAPI()

        assert api.is_running() is False

    def test_api_status_not_started(self, mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test getting status when game not started."""
        api = GameAPI()

        status = api.get_status()

        assert status["is_running"] is False
        assert status["current_state"] == "not_started"
        assert status["current_level"] == 0
        assert status["total_levels"] == 0

    @patch('src.integration.game_loop.GameLoop.run')
    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_api_start_game_basic(self, mock_load_level, mock_run,
                                  mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test starting game with basic parameters."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True

        api = GameAPI()

        # Mock game loop to exit immediately
        def mock_run_impl(controller):
            pass

        mock_run.side_effect = mock_run_impl

        success = api.start_game(level_ids=["level_001"])

        assert success is True
        mock_load_level.assert_called_once()

    @patch('src.integration.game_loop.GameLoop.run')
    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_api_start_game_with_callbacks(self, mock_load_level, mock_run,
                                          mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test starting game with callbacks."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True

        api = GameAPI()

        on_complete_called = []
        on_exit_called = []

        def on_complete(stats):
            on_complete_called.append(stats)

        def on_exit():
            on_exit_called.append(True)

        # Mock game loop
        def mock_run_impl(controller):
            pass

        mock_run.side_effect = mock_run_impl

        api.start_game(
            level_ids=["level_001"],
            on_complete=on_complete,
            on_exit=on_exit
        )

        # Exit callback should be called
        assert len(on_exit_called) == 1

    def test_api_start_game_no_levels(self, mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test starting game with no levels."""
        api = GameAPI()

        success = api.start_game(level_ids=[])

        assert success is False

    @patch('src.integration.game_loop.GameLoop.run')
    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_api_stop_game(self, mock_load_level, mock_run,
                          mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test stopping game."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True

        api = GameAPI()

        # Mock game loop to simulate running
        def mock_run_impl(controller):
            # Simulate game loop running
            api._game_loop._running = True
            # Then stop it
            api.stop_game()

        mock_run.side_effect = mock_run_impl

        api.start_game(level_ids=["level_001"])

        # Game should have been stopped
        assert api.is_running() is False


class TestCompleteGameFlow:
    """Test complete game flow scenarios."""

    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.event.get')
    @patch('src.integration.game_loop.GameLoop.run')
    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_single_level_flow(self, mock_load_level, mock_run, mock_event_get,
                               mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test complete flow for a single level."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True
        mock_event_get.return_value = []

        api = GameAPI()

        completion_stats = []

        def on_complete(stats):
            completion_stats.append(stats)

        # Mock game loop
        def mock_run_impl(controller):
            # Simulate level completion
            controller._state_machine.transition_to(GameState.VICTORY)

        mock_run.side_effect = mock_run_impl

        api.start_game(
            level_ids=["level_001"],
            on_complete=on_complete
        )

        # Completion callback should have been called
        assert len(completion_stats) == 1
        assert completion_stats[0]["total_levels"] == 1

    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('src.integration.game_loop.GameLoop.run')
    @patch('src.core.level.level_manager.LevelManager.load_level')
    def test_multi_level_flow(self, mock_load_level, mock_run,
                             mock_mixer_init, mock_init, mock_caption, mock_set_mode):
        """Test complete flow for multiple levels."""
        mock_surface = Mock()
        mock_set_mode.return_value = mock_surface
        mock_load_level.return_value = True

        api = GameAPI()

        # Mock game loop
        def mock_run_impl(controller):
            pass

        mock_run.side_effect = mock_run_impl

        success = api.start_game(level_ids=["level_001", "level_002", "level_003"])

        assert success is True
        # Should have attempted to load first level
        assert mock_load_level.call_count >= 1
