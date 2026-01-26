"""
Scene Flow Integration Tests

Tests for complete scene flow and transitions.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pytest
import pygame
import time
from src.scenes.scene_manager import SceneManager
from src.scenes.main_menu_scene import MainMenuScene
from src.scenes.loading_scene import LoadingScene
from src.scenes.result_scene import ResultScene


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    """Initialize pygame before running tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))


@pytest.fixture
def scene_manager():
    """Create a scene manager for testing."""
    manager = SceneManager()
    manager.set_transition_duration(100)  # Fast transitions for testing
    manager.set_transition_type('fade')
    return manager


class TestSceneFlowBasic:
    """Test basic scene flow operations."""

    def test_main_menu_to_loading(self, scene_manager, screen):
        """Test transition from main menu to loading scene."""
        # Start with main menu
        scene_manager.push_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            }
        )

        assert not scene_manager.is_empty()
        assert len(scene_manager._scene_stack) == 1

        # Transition to loading scene
        scene_manager.replace_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'resources': []
            },
            transition=True
        )

        # Update through transition
        for _ in range(20):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        assert len(scene_manager._scene_stack) == 1

    def test_loading_to_result(self, scene_manager, screen):
        """Test transition from loading to result scene."""
        # Start with loading scene
        scene_manager.push_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'resources': []
            }
        )

        # Transition to result scene
        scene_manager.replace_scene(
            ResultScene,
            data={
                'victory': True,
                'level': 1,
                'time_taken': 30.0,
                'moves': 12,
                'stars': 3,
                'difficulty': 'normal',
                'screen_width': 800,
                'screen_height': 600
            },
            transition=True
        )

        # Update through transition
        for _ in range(20):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        assert len(scene_manager._scene_stack) == 1

    def test_result_back_to_menu(self, scene_manager, screen):
        """Test returning from result to main menu."""
        # Start with result scene
        scene_manager.push_scene(
            ResultScene,
            data={
                'victory': True,
                'level': 1,
                'time_taken': 30.0,
                'moves': 12,
                'stars': 3,
                'difficulty': 'normal',
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Return to main menu
        scene_manager.replace_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            },
            transition=True
        )

        # Update through transition
        for _ in range(20):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        assert len(scene_manager._scene_stack) == 1


class TestSceneFlowComplete:
    """Test complete scene flow sequences."""

    def test_complete_victory_flow(self, scene_manager, screen):
        """Test complete flow: Menu → Loading → Result (Victory) → Menu."""
        # 1. Main Menu
        scene_manager.push_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Update main menu
        for _ in range(10):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        # 2. Loading Scene
        scene_manager.replace_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'resources': []
            },
            transition=True
        )

        # Update through transition and loading
        for _ in range(30):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        # 3. Result Scene (Victory)
        scene_manager.replace_scene(
            ResultScene,
            data={
                'victory': True,
                'level': 1,
                'time_taken': 25.5,
                'moves': 10,
                'stars': 3,
                'difficulty': 'normal',
                'screen_width': 800,
                'screen_height': 600
            },
            transition=True
        )

        # Update through transition and result
        for _ in range(30):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        # 4. Back to Main Menu
        scene_manager.replace_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            },
            transition=True
        )

        # Update through transition
        for _ in range(20):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        # Verify final state
        assert len(scene_manager._scene_stack) == 1
        assert not scene_manager.is_empty()

    def test_complete_failure_flow(self, scene_manager, screen):
        """Test complete flow: Menu → Loading → Result (Failure) → Menu."""
        # 1. Main Menu
        scene_manager.push_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # 2. Loading Scene
        scene_manager.replace_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'resources': []
            },
            transition=True
        )

        for _ in range(30):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        # 3. Result Scene (Failure)
        scene_manager.replace_scene(
            ResultScene,
            data={
                'victory': False,
                'level': 1,
                'time_taken': 60.0,
                'moves': 25,
                'stars': 0,
                'difficulty': 'hard',
                'screen_width': 800,
                'screen_height': 600
            },
            transition=True
        )

        for _ in range(30):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        # 4. Back to Main Menu
        scene_manager.replace_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            },
            transition=True
        )

        for _ in range(20):
            scene_manager.update(16.67)
            scene_manager.draw(screen)

        assert len(scene_manager._scene_stack) == 1


class TestSceneDataPassing:
    """Test data passing between scenes."""

    def test_difficulty_data_passing(self, scene_manager, screen):
        """Test difficulty setting passed through scenes."""
        # Main menu with difficulty selection
        scene_manager.push_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Simulate difficulty selection and start game
        difficulty = 'hard'

        # Loading scene receives difficulty
        scene_manager.replace_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'difficulty': difficulty,
                'resources': []
            }
        )

        for _ in range(20):
            scene_manager.update(16.67)

        # Result scene receives difficulty
        scene_manager.replace_scene(
            ResultScene,
            data={
                'victory': True,
                'level': 1,
                'time_taken': 28.0,
                'moves': 15,
                'stars': 2,
                'difficulty': difficulty,
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Verify difficulty was passed
        current_scene = scene_manager.get_current_scene()
        assert current_scene is not None
        result_data = current_scene.get_result_data()
        assert result_data['difficulty'] == difficulty

    def test_level_progression_data(self, scene_manager, screen):
        """Test level number progression through scenes."""
        levels = [1, 2, 3]

        for level in levels:
            # Result scene for each level
            scene_manager.replace_scene(
                ResultScene,
                data={
                    'victory': True,
                    'level': level,
                    'time_taken': 30.0,
                    'moves': 12,
                    'stars': 3,
                    'difficulty': 'normal',
                    'screen_width': 800,
                    'screen_height': 600
                }
            )

            for _ in range(10):
                scene_manager.update(16.67)

            # Verify level number
            current_scene = scene_manager.get_current_scene()
            result_data = current_scene.get_result_data()
            assert result_data['level'] == level

    def test_star_rating_data_passing(self, scene_manager, screen):
        """Test star rating data passed correctly."""
        star_ratings = [1, 2, 3]

        for stars in star_ratings:
            scene_manager.replace_scene(
                ResultScene,
                data={
                    'victory': True,
                    'level': 1,
                    'time_taken': 30.0,
                    'moves': 12,
                    'stars': stars,
                    'difficulty': 'normal',
                    'screen_width': 800,
                    'screen_height': 600
                }
            )

            for _ in range(10):
                scene_manager.update(16.67)

            current_scene = scene_manager.get_current_scene()
            result_data = current_scene.get_result_data()
            assert result_data['stars'] == stars


class TestSceneMemoryManagement:
    """Test memory management during scene transitions."""

    def test_scene_cleanup_on_replace(self, scene_manager, screen):
        """Test that replaced scenes are properly cleaned up."""
        # Create initial scene
        scene_manager.push_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            }
        )

        initial_scene = scene_manager.get_current_scene()
        assert initial_scene.is_active

        # Replace with new scene
        scene_manager.replace_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'resources': []
            }
        )

        # Update to complete transition
        for _ in range(20):
            scene_manager.update(16.67)

        # Old scene should be inactive
        assert not initial_scene.is_active

    def test_multiple_transitions_no_leak(self, scene_manager, screen):
        """Test multiple transitions don't cause memory leaks."""
        scenes = [MainMenuScene, LoadingScene, ResultScene]

        for _ in range(3):  # Repeat cycle 3 times
            for scene_class in scenes:
                if scene_class == ResultScene:
                    data = {
                        'victory': True,
                        'level': 1,
                        'time_taken': 30.0,
                        'moves': 12,
                        'stars': 3,
                        'difficulty': 'normal',
                        'screen_width': 800,
                        'screen_height': 600
                    }
                else:
                    data = {
                        'screen_width': 800,
                        'screen_height': 600
                    }

                scene_manager.replace_scene(scene_class, data=data)

                for _ in range(10):
                    scene_manager.update(16.67)
                    scene_manager.draw(screen)

        # Should only have one scene in stack
        assert len(scene_manager._scene_stack) == 1


class TestScenePerformance:
    """Test scene performance."""

    def test_scene_update_performance(self, scene_manager, screen):
        """Test that scene updates are fast enough for 60 FPS."""
        scene_manager.push_scene(
            ResultScene,
            data={
                'victory': True,
                'level': 1,
                'time_taken': 30.0,
                'moves': 12,
                'stars': 3,
                'difficulty': 'normal',
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Measure update time
        update_times = []
        for _ in range(100):
            start = time.perf_counter()
            scene_manager.update(16.67)
            end = time.perf_counter()
            update_times.append((end - start) * 1000)  # Convert to ms

        avg_update_time = sum(update_times) / len(update_times)

        # Should be well under 16.67ms for 60 FPS
        assert avg_update_time < 10.0, f"Average update time {avg_update_time:.2f}ms is too slow"

    def test_scene_draw_performance(self, scene_manager, screen):
        """Test that scene drawing is fast enough for 60 FPS."""
        scene_manager.push_scene(
            ResultScene,
            data={
                'victory': True,
                'level': 1,
                'time_taken': 30.0,
                'moves': 12,
                'stars': 3,
                'difficulty': 'normal',
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Measure draw time
        draw_times = []
        for _ in range(100):
            scene_manager.update(16.67)
            start = time.perf_counter()
            scene_manager.draw(screen)
            end = time.perf_counter()
            draw_times.append((end - start) * 1000)  # Convert to ms

        avg_draw_time = sum(draw_times) / len(draw_times)

        # Should be well under 16.67ms for 60 FPS
        assert avg_draw_time < 10.0, f"Average draw time {avg_draw_time:.2f}ms is too slow"

    def test_transition_performance(self, scene_manager, screen):
        """Test that scene transitions are smooth."""
        scene_manager.push_scene(
            MainMenuScene,
            data={
                'screen_width': 800,
                'screen_height': 600
            }
        )

        # Measure transition time
        start = time.perf_counter()

        scene_manager.replace_scene(
            LoadingScene,
            data={
                'screen_width': 800,
                'screen_height': 600,
                'resources': []
            },
            transition=True
        )

        # Update through transition
        frame_times = []
        for _ in range(30):
            frame_start = time.perf_counter()
            scene_manager.update(16.67)
            scene_manager.draw(screen)
            frame_end = time.perf_counter()
            frame_times.append((frame_end - frame_start) * 1000)

        end = time.perf_counter()
        total_time = (end - start) * 1000

        # Transition should complete in reasonable time
        assert total_time < 1000, f"Transition took {total_time:.2f}ms, too slow"

        # All frames should be fast enough for 60 FPS
        max_frame_time = max(frame_times)
        assert max_frame_time < 20.0, f"Slowest frame {max_frame_time:.2f}ms is too slow"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
