"""
Tests for Level Select Scene

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

import pytest
import pygame
from unittest.mock import Mock, MagicMock, patch
from src.scenes.level_select_scene import LevelSelectScene
from src.progression.progress_data import GameProgress, LevelProgress


@pytest.fixture
def mock_scene_manager():
    """Create a mock scene manager."""
    manager = Mock()
    manager.screen = pygame.Surface((800, 600))
    manager.replace_scene = Mock()
    return manager


@pytest.fixture
def mock_progression_manager():
    """Create a mock progression manager with test data."""
    manager = Mock()

    # Create test progress
    progress = GameProgress()
    progress.unlock_level(1)
    progress.unlock_level(2)
    progress.complete_level(1, stars=3, time=30.0, moves=10)

    manager.get_progress.return_value = progress
    return manager


@pytest.fixture
def level_select_scene(mock_scene_manager):
    """Create a level select scene instance."""
    pygame.init()
    scene = LevelSelectScene(mock_scene_manager)
    return scene


class TestLevelSelectSceneInitialization:
    """Test level select scene initialization."""

    def test_init(self, level_select_scene):
        """Test scene initialization."""
        assert level_select_scene is not None
        assert level_select_scene._screen_width == 800
        assert level_select_scene._screen_height == 600
        assert level_select_scene._difficulty == 'normal'

    def test_on_enter_without_data(self, level_select_scene):
        """Test entering scene without data."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            assert level_select_scene._background_panel is not None
            assert level_select_scene._title_label is not None
            assert level_select_scene._back_button is not None
            assert len(level_select_scene._level_buttons) == LevelSelectScene.MAX_LEVELS

    def test_on_enter_with_difficulty(self, level_select_scene):
        """Test entering scene with difficulty data."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter({'difficulty': 'hard'})

            assert level_select_scene._difficulty == 'hard'

    def test_on_exit(self, level_select_scene):
        """Test exiting scene."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()
            level_select_scene.on_exit()
            # Should not raise any exceptions


class TestLevelSelectSceneUI:
    """Test level select scene UI components."""

    def test_level_buttons_created(self, level_select_scene):
        """Test that all level buttons are created."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            assert len(level_select_scene._level_buttons) == LevelSelectScene.MAX_LEVELS

            # Check that buttons have correct IDs
            for level_id in range(1, LevelSelectScene.MAX_LEVELS + 1):
                assert level_id in level_select_scene._level_buttons

    def test_unlocked_level_button_enabled(self, level_select_scene, mock_progression_manager):
        """Test that unlocked level buttons are enabled."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager', return_value=mock_progression_manager):
            level_select_scene.on_enter()

            # Level 1 should be unlocked and enabled
            button = level_select_scene._level_buttons[1]
            assert button.enabled

    def test_locked_level_button_disabled(self, level_select_scene, mock_progression_manager):
        """Test that locked level buttons are disabled."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager', return_value=mock_progression_manager):
            level_select_scene.on_enter()

            # Level 10 should be locked and disabled
            button = level_select_scene._level_buttons[10]
            assert not button.enabled

    def test_completed_level_shows_stars(self, level_select_scene, mock_progression_manager):
        """Test that completed levels show star ratings."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager', return_value=mock_progression_manager):
            level_select_scene.on_enter()

            # Level 1 is completed with 3 stars
            assert 1 in level_select_scene._star_labels
            star_label = level_select_scene._star_labels[1]
            assert "★" in star_label.get_text()

    def test_locked_level_shows_lock_icon(self, level_select_scene, mock_progression_manager):
        """Test that locked levels show lock icon."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager', return_value=mock_progression_manager):
            level_select_scene.on_enter()

            # Level 10 is locked
            assert 10 in level_select_scene._star_labels
            lock_label = level_select_scene._star_labels[10]
            assert "🔒" in lock_label.get_text()


class TestLevelSelectSceneInteraction:
    """Test level select scene user interactions."""

    def test_level_button_click(self, level_select_scene, mock_scene_manager, mock_progression_manager):
        """Test clicking on a level button."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager', return_value=mock_progression_manager):
            level_select_scene.on_enter({'difficulty': 'normal'})

            # Simulate clicking level 1
            level_select_scene._on_level_clicked(1)

            # Should transition to gameplay scene
            mock_scene_manager.replace_scene.assert_called_once_with(
                'gameplay',
                {'level': 1, 'difficulty': 'normal'}
            )

    def test_back_button_click(self, level_select_scene, mock_scene_manager):
        """Test clicking the back button."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            # Simulate clicking back button
            level_select_scene._on_back_clicked()

            # Should return to main menu
            mock_scene_manager.replace_scene.assert_called_once_with('main_menu')

    def test_escape_key_returns_to_menu(self, level_select_scene, mock_scene_manager):
        """Test that ESC key returns to main menu."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            # Simulate ESC key press
            event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
            level_select_scene.handle_event(event)

            # Should return to main menu
            mock_scene_manager.replace_scene.assert_called_once_with('main_menu')


class TestLevelSelectSceneUpdate:
    """Test level select scene update logic."""

    def test_update(self, level_select_scene):
        """Test scene update."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            # Update should not raise exceptions
            level_select_scene.update(0.016)

    def test_update_buttons(self, level_select_scene):
        """Test that buttons are updated."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            # Mock button update methods
            for button in level_select_scene._level_buttons.values():
                button.update = Mock()

            level_select_scene._back_button.update = Mock()

            # Update scene
            level_select_scene.update(0.016)

            # All buttons should be updated
            for button in level_select_scene._level_buttons.values():
                button.update.assert_called_once_with(0.016)

            level_select_scene._back_button.update.assert_called_once_with(0.016)


class TestLevelSelectSceneDraw:
    """Test level select scene drawing."""

    def test_draw(self, level_select_scene):
        """Test scene drawing."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            screen = pygame.Surface((800, 600))

            # Draw should not raise exceptions
            level_select_scene.draw(screen)

    def test_draw_all_components(self, level_select_scene):
        """Test that all components are drawn."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            screen = pygame.Surface((800, 600))

            # Mock draw methods
            level_select_scene._background_panel.draw = Mock()
            level_select_scene._title_label.draw = Mock()
            level_select_scene._back_button.draw = Mock()

            for button in level_select_scene._level_buttons.values():
                button.draw = Mock()

            for label in level_select_scene._star_labels.values():
                label.draw = Mock()

            # Draw scene
            level_select_scene.draw(screen)

            # All components should be drawn
            level_select_scene._background_panel.draw.assert_called_once()
            level_select_scene._title_label.draw.assert_called_once()
            level_select_scene._back_button.draw.assert_called_once()

            for button in level_select_scene._level_buttons.values():
                button.draw.assert_called_once()

            for label in level_select_scene._star_labels.values():
                label.draw.assert_called_once()


class TestLevelSelectSceneLayout:
    """Test level select scene layout."""

    def test_level_grid_layout(self, level_select_scene):
        """Test that levels are arranged in a grid."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            # Check that buttons are positioned in a grid
            for level_id in range(1, LevelSelectScene.MAX_LEVELS + 1):
                button = level_select_scene._level_buttons[level_id]

                # Button should have valid position
                assert button.x >= 0
                assert button.y >= 0
                assert button.x < 800
                assert button.y < 600

    def test_levels_per_row(self, level_select_scene):
        """Test that levels are arranged with correct number per row."""
        with patch('src.scenes.level_select_scene.LevelProgressionManager'):
            level_select_scene.on_enter()

            # Get Y positions of first row
            first_row_y = level_select_scene._level_buttons[1].y

            # Check that first LEVELS_PER_ROW buttons have same Y
            for level_id in range(1, LevelSelectScene.LEVELS_PER_ROW + 1):
                button = level_select_scene._level_buttons[level_id]
                assert button.y == first_row_y

            # Check that next button is in different row
            if LevelSelectScene.MAX_LEVELS > LevelSelectScene.LEVELS_PER_ROW:
                next_button = level_select_scene._level_buttons[LevelSelectScene.LEVELS_PER_ROW + 1]
                assert next_button.y != first_row_y


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
