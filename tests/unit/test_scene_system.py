"""
Unit tests for Scene system.

Tests SceneBase and SceneManager functionality.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pytest
import pygame
from src.scenes.scene_base import SceneBase
from src.scenes.scene_manager import SceneManager


@pytest.fixture(scope="module")
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


# Test scene implementations
class TestScene1(SceneBase):
    """Test scene 1."""

    def __init__(self, scene_manager=None):
        super().__init__(scene_manager)
        self.update_count = 0
        self.draw_count = 0
        self.event_count = 0

    def update(self, delta_ms):
        self.update_count += 1

    def draw(self, surface):
        self.draw_count += 1
        surface.fill((255, 0, 0))

    def handle_event(self, event):
        self.event_count += 1
        return True


class TestScene2(SceneBase):
    """Test scene 2."""

    def __init__(self, scene_manager=None):
        super().__init__(scene_manager)
        self.update_count = 0

    def update(self, delta_ms):
        self.update_count += 1

    def draw(self, surface):
        surface.fill((0, 255, 0))

    def handle_event(self, event):
        return False


class TestSceneBase:
    """Test SceneBase functionality."""

    def test_scene_creation(self, pygame_init):
        """Test scene can be created."""
        scene = TestScene1()
        assert scene.is_active is False
        assert scene.transition_data == {}
        assert scene.scene_manager is None

    def test_scene_lifecycle(self, pygame_init):
        """Test scene lifecycle methods."""
        scene = TestScene1()

        # Test on_enter
        data = {'level': 1, 'difficulty': 'easy'}
        scene.on_enter(data)
        assert scene.is_active is True
        assert scene.transition_data == data

        # Test on_exit
        scene.on_exit()
        assert scene.is_active is False

    def test_scene_update(self, pygame_init):
        """Test scene update method."""
        scene = TestScene1()
        scene.on_enter()

        assert scene.update_count == 0
        scene.update(16.67)
        assert scene.update_count == 1
        scene.update(16.67)
        assert scene.update_count == 2

    def test_scene_draw(self, pygame_init):
        """Test scene draw method."""
        scene = TestScene1()
        surface = pygame.Surface((800, 600))

        assert scene.draw_count == 0
        scene.draw(surface)
        assert scene.draw_count == 1

    def test_scene_handle_event(self, pygame_init):
        """Test scene event handling."""
        scene = TestScene1()
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})

        assert scene.event_count == 0
        result = scene.handle_event(event)
        assert result is True
        assert scene.event_count == 1

    def test_transition_data(self, pygame_init):
        """Test transition data management."""
        scene = TestScene1()

        # Set data
        scene.set_transition_data('score', 100)
        scene.set_transition_data('level', 5)

        # Get data
        assert scene.get_transition_data('score') == 100
        assert scene.get_transition_data('level') == 5
        assert scene.get_transition_data('nonexistent', 'default') == 'default'

    def test_pause_resume(self, pygame_init):
        """Test scene pause and resume."""
        scene = TestScene1()
        scene.on_enter({'initial': 'data'})

        # Pause
        scene.pause()
        # No specific assertion, just ensure it doesn't crash

        # Resume with new data
        resume_data = {'resumed': True}
        scene.resume(resume_data)
        assert scene.transition_data['resumed'] is True
        assert scene.transition_data['initial'] == 'data'


class TestSceneManager:
    """Test SceneManager functionality."""

    def test_scene_manager_creation(self, pygame_init):
        """Test scene manager can be created."""
        manager = SceneManager()
        assert manager.is_empty() is True
        assert manager.get_stack_size() == 0
        assert manager.get_current_scene() is None

    def test_push_scene(self, pygame_init):
        """Test pushing scenes onto the stack."""
        manager = SceneManager()

        # Push first scene
        manager.push_scene(TestScene1, transition=False)
        assert manager.get_stack_size() == 1
        assert manager.is_empty() is False

        current = manager.get_current_scene()
        assert isinstance(current, TestScene1)
        assert current.is_active is True

        # Push second scene
        manager.push_scene(TestScene2, transition=False)
        assert manager.get_stack_size() == 2

        current = manager.get_current_scene()
        assert isinstance(current, TestScene2)

    def test_pop_scene(self, pygame_init):
        """Test popping scenes from the stack."""
        manager = SceneManager()

        # Push two scenes
        manager.push_scene(TestScene1, transition=False)
        manager.push_scene(TestScene2, transition=False)
        assert manager.get_stack_size() == 2

        # Pop one scene
        manager.pop_scene(transition=False)
        assert manager.get_stack_size() == 1

        current = manager.get_current_scene()
        assert isinstance(current, TestScene1)

        # Pop last scene
        manager.pop_scene(transition=False)
        assert manager.is_empty() is True

    def test_replace_scene(self, pygame_init):
        """Test replacing the current scene."""
        manager = SceneManager()

        # Push first scene
        manager.push_scene(TestScene1, transition=False)
        assert manager.get_stack_size() == 1

        # Replace with second scene
        manager.replace_scene(TestScene2, transition=False)
        assert manager.get_stack_size() == 1

        current = manager.get_current_scene()
        assert isinstance(current, TestScene2)

    def test_clear_stack(self, pygame_init):
        """Test clearing the scene stack."""
        manager = SceneManager()

        # Push multiple scenes
        manager.push_scene(TestScene1, transition=False)
        manager.push_scene(TestScene2, transition=False)
        manager.push_scene(TestScene1, transition=False)
        assert manager.get_stack_size() == 3

        # Clear stack
        manager.clear_stack()
        assert manager.is_empty() is True
        assert manager.get_stack_size() == 0

    def test_scene_data_passing(self, pygame_init):
        """Test passing data between scenes."""
        manager = SceneManager()

        # Push scene with data
        data = {'level': 5, 'score': 1000}
        manager.push_scene(TestScene1, data=data, transition=False)

        current = manager.get_current_scene()
        assert current.get_transition_data('level') == 5
        assert current.get_transition_data('score') == 1000

    def test_scene_manager_update(self, pygame_init):
        """Test scene manager update."""
        manager = SceneManager()
        manager.push_scene(TestScene1, transition=False)

        current = manager.get_current_scene()
        assert current.update_count == 0

        # Update manager
        manager.update(16.67)
        assert current.update_count == 1

        manager.update(16.67)
        assert current.update_count == 2

    def test_scene_manager_draw(self, pygame_init):
        """Test scene manager draw."""
        manager = SceneManager()
        surface = pygame.Surface((800, 600))

        # Draw with empty stack (should not crash)
        manager.draw(surface)

        # Push scene and draw
        manager.push_scene(TestScene1, transition=False)
        current = manager.get_current_scene()
        assert current.draw_count == 0

        manager.draw(surface)
        assert current.draw_count == 1

    def test_scene_manager_handle_event(self, pygame_init):
        """Test scene manager event handling."""
        manager = SceneManager()
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})

        # Handle event with empty stack
        result = manager.handle_event(event)
        assert result is False

        # Push scene and handle event
        manager.push_scene(TestScene1, transition=False)
        current = manager.get_current_scene()
        assert current.event_count == 0

        result = manager.handle_event(event)
        assert result is True
        assert current.event_count == 1

    def test_scene_request_change(self, pygame_init):
        """Test scene requesting scene change."""
        manager = SceneManager()
        manager.push_scene(TestScene1, transition=False)

        scene1 = manager.get_current_scene()

        # Request replace
        scene1.request_scene_change(TestScene2, data={'from': 'scene1'}, replace=True)
        assert manager.get_stack_size() == 1
        assert isinstance(manager.get_current_scene(), TestScene2)

        # Request push
        scene2 = manager.get_current_scene()
        scene2.request_scene_change(TestScene1, replace=False)
        assert manager.get_stack_size() == 2
        assert isinstance(manager.get_current_scene(), TestScene1)

    def test_scene_request_pop(self, pygame_init):
        """Test scene requesting pop."""
        manager = SceneManager()
        manager.push_scene(TestScene1, transition=False)
        manager.push_scene(TestScene2, transition=False)

        assert manager.get_stack_size() == 2

        # Request pop
        scene2 = manager.get_current_scene()
        scene2.request_scene_pop(data={'result': 'success'})

        assert manager.get_stack_size() == 1
        assert isinstance(manager.get_current_scene(), TestScene1)

    def test_transition_settings(self, pygame_init):
        """Test transition settings."""
        manager = SceneManager()

        # Set transition duration
        manager.set_transition_duration(1000)
        assert manager._transition_duration == 1000

        # Set transition type
        manager.set_transition_type('fade')
        assert manager._transition_type == 'fade'

        manager.set_transition_type('none')
        assert manager._transition_type == 'none'

    def test_transition_animation(self, pygame_init):
        """Test transition animation."""
        manager = SceneManager()
        manager.set_transition_duration(100)  # 100ms transition

        # Push scene with transition
        manager.push_scene(TestScene1, transition=True)
        assert manager._transition_active is True
        assert manager._transition_progress == 0.0

        # Update transition
        manager.update(50)  # 50% progress
        assert manager._transition_active is True
        assert 0.4 < manager._transition_progress < 0.6

        # Complete transition
        manager.update(60)  # Should complete
        assert manager._transition_active is False

    def test_scene_manager_repr(self, pygame_init):
        """Test scene manager string representation."""
        manager = SceneManager()
        manager.push_scene(TestScene1, transition=False)
        manager.push_scene(TestScene2, transition=False)

        repr_str = repr(manager)
        assert 'SceneManager' in repr_str
        assert 'TestScene1' in repr_str
        assert 'TestScene2' in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
