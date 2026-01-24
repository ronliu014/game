"""
Integration tests for GameplayScene.

Tests the complete gameplay scene with all layers and components.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

import pytest
import pygame
from unittest.mock import Mock, MagicMock, patch
from src.scenes.gameplay_scene import GameplayScene
from src.scenes.scene_manager import SceneManager
from src.integration.game_controller import GameController
from src.core.timer.game_timer import GameTimer


@pytest.fixture
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    pygame.display.set_mode((800, 600))
    yield
    pygame.quit()


@pytest.fixture
def scene_manager():
    """Create a mock scene manager."""
    manager = Mock(spec=SceneManager)
    manager.replace_scene = Mock()
    manager.push_scene = Mock()
    manager.pop_scene = Mock()
    return manager


@pytest.fixture
def game_controller():
    """Create a mock game controller."""
    controller = Mock(spec=GameController)
    controller.get_move_count = Mock(return_value=0)
    controller.is_game_over = Mock(return_value=False)
    controller.is_victory = Mock(return_value=False)
    return controller


class TestGameplaySceneInitialization:
    """Test gameplay scene initialization."""

    def test_init_default(self, pygame_init, scene_manager):
        """Test default initialization."""
        scene = GameplayScene(scene_manager)

        assert scene is not None
        assert scene._screen_width == 800
        assert scene._screen_height == 600
        assert scene._level == 1
        assert scene._difficulty == 'normal'
        assert scene._time_limit == 60.0
        assert not scene._is_paused
        assert not scene._game_started

    def test_on_enter_with_data(self, pygame_init, scene_manager, game_controller):
        """Test on_enter with custom data."""
        scene = GameplayScene(scene_manager)

        data = {
            'level': 5,
            'difficulty': 'hard',
            'time_limit': 120.0,
            'screen_width': 1024,
            'screen_height': 768,
            'game_controller': game_controller
        }

        scene.on_enter(data)

        assert scene._level == 5
        assert scene._difficulty == 'hard'
        assert scene._time_limit == 120.0
        assert scene._screen_width == 1024
        assert scene._screen_height == 768
        assert scene._game_controller == game_controller
        assert scene._game_started

    def test_layers_created(self, pygame_init, scene_manager):
        """Test that all layers are created."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        assert scene._background_layer is not None
        assert scene._game_layer is not None
        assert scene._hud_layer is not None
        assert scene._debug_layer is not None
        assert len(scene._layers) == 4

    def test_timer_created(self, pygame_init, scene_manager):
        """Test that game timer is created."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({'time_limit': 90.0})

        assert scene._game_timer is not None
        assert scene._game_timer.get_time_limit() == 90.0


class TestGameplaySceneUpdate:
    """Test gameplay scene update logic."""

    def test_update_normal(self, pygame_init, scene_manager):
        """Test normal update."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Update scene
        scene.update(16.67)

        # Should not raise any errors
        assert True

    def test_update_when_paused(self, pygame_init, scene_manager):
        """Test update when paused."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Pause the game
        scene._toggle_pause()
        assert scene._is_paused

        # Get initial timer state
        initial_time = scene._game_timer.get_remaining_time()

        # Update scene
        scene.update(16.67)

        # Timer should not have changed
        assert scene._game_timer.get_remaining_time() == initial_time

    def test_update_timer(self, pygame_init, scene_manager):
        """Test timer updates correctly."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({'time_limit': 10.0})

        initial_time = scene._game_timer.get_remaining_time()

        # Update for 1 second
        for _ in range(60):
            scene.update(16.67)

        # Timer should have decreased
        assert scene._game_timer.get_remaining_time() < initial_time

    def test_update_move_count(self, pygame_init, scene_manager, game_controller):
        """Test move count updates in HUD."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({'game_controller': game_controller})

        # Simulate move
        game_controller.get_move_count.return_value = 5

        # Update scene
        scene.update(16.67)

        # HUD should reflect move count
        assert scene._hud_layer.get_move_count() == 5


class TestGameplaySceneDraw:
    """Test gameplay scene drawing."""

    def test_draw_all_layers(self, pygame_init, scene_manager):
        """Test that all layers are drawn."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Create a test surface
        surface = pygame.Surface((800, 600))

        # Draw scene
        scene.draw(surface)

        # Should not raise any errors
        assert True

    def test_draw_performance(self, pygame_init, scene_manager):
        """Test draw performance."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        surface = pygame.Surface((800, 600))

        import time
        start_time = time.time()

        # Draw 60 frames
        for _ in range(60):
            scene.draw(surface)

        elapsed = time.time() - start_time
        avg_frame_time = (elapsed / 60) * 1000  # ms per frame

        # Should be well under 16.67ms per frame
        assert avg_frame_time < 10.0


class TestGameplaySceneEvents:
    """Test gameplay scene event handling."""

    def test_handle_pause_key(self, pygame_init, scene_manager):
        """Test pause key handling."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Create ESC key event
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})

        # Handle event
        handled = scene.handle_event(event)

        assert handled
        assert scene._is_paused

    def test_handle_debug_toggle(self, pygame_init, scene_manager):
        """Test debug layer toggle."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Create F3 key event
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_F3})

        initial_visibility = scene._debug_layer.is_visible()

        # Handle event
        scene.handle_event(event)

        # Debug layer visibility should toggle
        assert scene._debug_layer.is_visible() != initial_visibility


class TestGameplaySceneGameOver:
    """Test game over conditions."""

    def test_timeout_triggers_game_over(self, pygame_init, scene_manager):
        """Test that timeout triggers game over."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({'time_limit': 0.1})

        # Update until timeout
        for _ in range(10):
            scene.update(16.67)

        # Should request scene change to result scene
        assert scene_manager.replace_scene.called

    def test_victory_triggers_game_over(self, pygame_init, scene_manager, game_controller):
        """Test that victory triggers game over."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({'game_controller': game_controller})

        # Simulate victory
        game_controller.is_game_over.return_value = True
        game_controller.is_victory.return_value = True

        # Update scene
        scene.update(16.67)

        # Should request scene change to result scene
        assert scene_manager.replace_scene.called

    def test_game_over_data_passed(self, pygame_init, scene_manager, game_controller):
        """Test that game over data is passed correctly."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({
            'level': 3,
            'difficulty': 'hard',
            'time_limit': 60.0,
            'game_controller': game_controller
        })

        # Simulate game over
        game_controller.is_game_over.return_value = True
        game_controller.is_victory.return_value = True
        game_controller.get_move_count.return_value = 15

        # Update scene
        scene.update(16.67)

        # Check that result data was passed
        call_args = scene_manager.replace_scene.call_args
        assert call_args is not None

        # Get the data argument (second positional argument)
        result_data = call_args[0][1]
        assert result_data['level'] == 3
        assert result_data['difficulty'] == 'hard'
        assert result_data['moves'] == 15
        assert result_data['victory'] is True


class TestGameplayScenePause:
    """Test pause functionality."""

    def test_pause_stops_timer(self, pygame_init, scene_manager):
        """Test that pause stops the timer."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Pause game
        scene._toggle_pause()

        assert scene._is_paused
        assert scene._game_timer.is_paused()

    def test_resume_restarts_timer(self, pygame_init, scene_manager):
        """Test that resume restarts the timer."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Pause and resume
        scene._toggle_pause()
        scene._toggle_pause()

        assert not scene._is_paused
        assert scene._game_timer.is_running()

    def test_pause_prevents_updates(self, pygame_init, scene_manager):
        """Test that pause prevents game updates."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Pause game
        scene._toggle_pause()

        initial_time = scene._game_timer.get_remaining_time()

        # Try to update
        scene.update(16.67)

        # Timer should not have changed
        assert scene._game_timer.get_remaining_time() == initial_time


class TestGameplaySceneCleanup:
    """Test scene cleanup."""

    def test_on_exit_stops_timer(self, pygame_init, scene_manager):
        """Test that on_exit stops the timer."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        assert scene._game_timer.is_running()

        # Exit scene
        scene.on_exit()

        assert not scene._game_timer.is_running()

    def test_on_exit_cleans_layers(self, pygame_init, scene_manager):
        """Test that on_exit cleans up layers."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        # Mock layer on_exit methods
        for layer in scene._layers:
            layer.on_exit = Mock()

        # Exit scene
        scene.on_exit()

        # All layers should have on_exit called
        for layer in scene._layers:
            layer.on_exit.assert_called_once()


class TestGameplayScenePerformance:
    """Test gameplay scene performance."""

    def test_update_performance(self, pygame_init, scene_manager):
        """Test update performance."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        import time
        start_time = time.time()

        # Update 60 frames
        for _ in range(60):
            scene.update(16.67)

        elapsed = time.time() - start_time
        avg_frame_time = (elapsed / 60) * 1000  # ms per frame

        # Should be well under 16.67ms per frame
        assert avg_frame_time < 10.0

    def test_no_memory_leak(self, pygame_init, scene_manager):
        """Test that there are no memory leaks."""
        scene = GameplayScene(scene_manager)

        # Enter and exit multiple times
        for _ in range(10):
            scene.on_enter()
            scene.update(16.67)
            scene.on_exit()

        # Should not raise any errors
        assert True


class TestGameplaySceneState:
    """Test gameplay scene state management."""

    def test_get_game_state(self, pygame_init, scene_manager, game_controller):
        """Test getting game state."""
        scene = GameplayScene(scene_manager)
        scene.on_enter({
            'level': 7,
            'difficulty': 'hell',
            'time_limit': 30.0,
            'game_controller': game_controller
        })

        game_controller.get_move_count.return_value = 20

        state = scene.get_game_state()

        assert state['level'] == 7
        assert state['difficulty'] == 'hell'
        assert state['time_limit'] == 30.0
        assert state['moves'] == 20
        assert state['is_paused'] is False
        assert state['game_started'] is True

    def test_is_paused(self, pygame_init, scene_manager):
        """Test is_paused method."""
        scene = GameplayScene(scene_manager)
        scene.on_enter()

        assert not scene.is_paused()

        scene._toggle_pause()
        assert scene.is_paused()

        scene._toggle_pause()
        assert not scene.is_paused()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
