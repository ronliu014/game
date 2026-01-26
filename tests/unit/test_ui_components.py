"""
Unit tests for UI components.

Tests all basic UI components: Button, Panel, Label, ProgressBar, Image.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pytest
import pygame
from src.ui.components.button import Button
from src.ui.components.panel import Panel
from src.ui.components.label import Label
from src.ui.components.progress_bar import ProgressBar
from src.ui.components.image import Image


@pytest.fixture(scope="module")
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


class TestButton:
    """Test Button component."""

    def test_button_creation(self, pygame_init):
        """Test button can be created."""
        button = Button(100, 100, 200, 50, "Test Button")
        assert button.x == 100
        assert button.y == 100
        assert button.width == 200
        assert button.height == 50
        assert button.label == "Test Button"
        assert button.visible is True
        assert button.enabled is True

    def test_button_states(self, pygame_init):
        """Test button state transitions."""
        button = Button(100, 100, 200, 50, "Test")

        # Initial state should be normal
        assert button.get_state() == Button.STATE_NORMAL

        # Test state changes
        button.set_state(Button.STATE_HOVER)
        assert button.get_state() == Button.STATE_HOVER

        button.set_state(Button.STATE_PRESSED)
        assert button.get_state() == Button.STATE_PRESSED

        button.set_state(Button.STATE_DISABLED)
        assert button.get_state() == Button.STATE_DISABLED

    def test_button_click_callback(self, pygame_init):
        """Test button click callback."""
        clicked = [False]

        def on_click():
            clicked[0] = True

        button = Button(100, 100, 200, 50, "Test", on_click=on_click)

        # Simulate click
        button._is_pressed = True
        event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (150, 125)})
        button.handle_event(event)

        assert clicked[0] is True

    def test_button_contains_point(self, pygame_init):
        """Test button point collision detection."""
        button = Button(100, 100, 200, 50, "Test")

        assert button.contains_point(150, 125) is True
        assert button.contains_point(50, 50) is False
        assert button.contains_point(350, 125) is False


class TestPanel:
    """Test Panel component."""

    def test_panel_creation(self, pygame_init):
        """Test panel can be created."""
        panel = Panel(50, 50, 300, 200, background_color=(100, 100, 100))
        assert panel.x == 50
        assert panel.y == 50
        assert panel.width == 300
        assert panel.height == 200
        assert panel.visible is True

    def test_panel_background_color(self, pygame_init):
        """Test panel background color."""
        panel = Panel(50, 50, 300, 200, background_color=(100, 100, 100))
        panel.set_background_color((200, 200, 200))
        assert panel._background_color == (200, 200, 200)

    def test_panel_border(self, pygame_init):
        """Test panel border."""
        panel = Panel(50, 50, 300, 200)
        panel.set_border((255, 255, 255), 3)
        assert panel._border_color == (255, 255, 255)
        assert panel._border_width == 3

    def test_panel_alpha(self, pygame_init):
        """Test panel transparency."""
        panel = Panel(50, 50, 300, 200, alpha=128)
        assert panel._alpha == 128

        panel.set_alpha(200)
        assert panel._alpha == 200

        # Test clamping
        panel.set_alpha(300)
        assert panel._alpha == 255

        panel.set_alpha(-10)
        assert panel._alpha == 0


class TestLabel:
    """Test Label component."""

    def test_label_creation(self, pygame_init):
        """Test label can be created."""
        label = Label(100, 100, 300, 50, "Test Label")
        assert label.x == 100
        assert label.y == 100
        assert label.get_text() == "Test Label"
        assert label.visible is True

    def test_label_text_change(self, pygame_init):
        """Test label text can be changed."""
        label = Label(100, 100, 300, 50, "Original")
        assert label.get_text() == "Original"

        label.set_text("Updated")
        assert label.get_text() == "Updated"

    def test_label_alignment(self, pygame_init):
        """Test label text alignment."""
        label = Label(100, 100, 300, 50, "Test", alignment=Label.ALIGN_CENTER)
        assert label._alignment == Label.ALIGN_CENTER

        label.set_alignment(Label.ALIGN_RIGHT)
        assert label._alignment == Label.ALIGN_RIGHT

        label.set_alignment(Label.ALIGN_LEFT)
        assert label._alignment == Label.ALIGN_LEFT

    def test_label_color(self, pygame_init):
        """Test label text color."""
        label = Label(100, 100, 300, 50, "Test", text_color=(255, 0, 0))
        assert label._text_color == (255, 0, 0)

        label.set_text_color((0, 255, 0))
        assert label._text_color == (0, 255, 0)


class TestProgressBar:
    """Test ProgressBar component."""

    def test_progress_bar_creation(self, pygame_init):
        """Test progress bar can be created."""
        progress_bar = ProgressBar(100, 100, 300, 30)
        assert progress_bar.x == 100
        assert progress_bar.y == 100
        assert progress_bar.width == 300
        assert progress_bar.height == 30
        assert progress_bar.get_progress() == 0.0

    def test_progress_bar_set_progress(self, pygame_init):
        """Test setting progress value."""
        progress_bar = ProgressBar(100, 100, 300, 30)

        progress_bar.set_progress_immediate(0.5)
        assert progress_bar.get_progress() == 0.5

        progress_bar.set_progress_immediate(1.0)
        assert progress_bar.get_progress() == 1.0

        # Test clamping
        progress_bar.set_progress_immediate(1.5)
        assert progress_bar.get_progress() == 1.0

        progress_bar.set_progress_immediate(-0.5)
        assert progress_bar.get_progress() == 0.0

    def test_progress_bar_animation(self, pygame_init):
        """Test progress bar animation."""
        progress_bar = ProgressBar(100, 100, 300, 30, animation_speed=1.0)

        progress_bar.set_progress(0.5)
        assert progress_bar.get_target_progress() == 0.5
        assert progress_bar.get_progress() == 0.0  # Not animated yet

        # Simulate 500ms update
        progress_bar.update(500)
        assert progress_bar.get_progress() == 0.5  # Should reach target

    def test_progress_bar_reset(self, pygame_init):
        """Test progress bar reset."""
        progress_bar = ProgressBar(100, 100, 300, 30)
        progress_bar.set_progress_immediate(0.75)

        progress_bar.reset()
        assert progress_bar.get_progress() == 0.0
        assert progress_bar.get_target_progress() == 0.0

    def test_progress_bar_colors(self, pygame_init):
        """Test progress bar color customization."""
        progress_bar = ProgressBar(100, 100, 300, 30)

        progress_bar.set_colors(
            bar_color=(255, 0, 0),
            background_color=(50, 50, 50),
            border_color=(255, 255, 255)
        )

        assert progress_bar._bar_color == (255, 0, 0)
        assert progress_bar._background_color == (50, 50, 50)
        assert progress_bar._border_color == (255, 255, 255)


class TestImage:
    """Test Image component."""

    def test_image_creation(self, pygame_init):
        """Test image can be created."""
        # Create a test surface
        test_surface = pygame.Surface((100, 100))
        test_surface.fill((255, 0, 0))

        image = Image(100, 100, 200, 200, test_surface)
        assert image.x == 100
        assert image.y == 100
        assert image.width == 200
        assert image.height == 200
        assert image.visible is True

    def test_image_scale(self, pygame_init):
        """Test image scaling."""
        test_surface = pygame.Surface((100, 100))
        image = Image(100, 100, 200, 200, test_surface)

        assert image.get_scale() == 1.0

        image.set_scale(2.0)
        assert image.get_scale() == 2.0

        image.set_scale(0.5)
        assert image.get_scale() == 0.5

    def test_image_rotation(self, pygame_init):
        """Test image rotation."""
        test_surface = pygame.Surface((100, 100))
        image = Image(100, 100, 200, 200, test_surface)

        assert image.get_rotation() == 0.0

        image.set_rotation(45)
        assert image.get_rotation() == 45.0

        image.set_rotation(360)
        assert image.get_rotation() == 0.0  # Normalized

        image.set_rotation(450)
        assert image.get_rotation() == 90.0  # Normalized

    def test_image_alpha(self, pygame_init):
        """Test image transparency."""
        test_surface = pygame.Surface((100, 100))
        image = Image(100, 100, 200, 200, test_surface, alpha=200)

        assert image.get_alpha() == 200

        image.set_alpha(128)
        assert image.get_alpha() == 128

        # Test clamping
        image.set_alpha(300)
        assert image.get_alpha() == 255

        image.set_alpha(-10)
        assert image.get_alpha() == 0

    def test_image_set_image(self, pygame_init):
        """Test changing image."""
        test_surface1 = pygame.Surface((100, 100))
        test_surface1.fill((255, 0, 0))

        test_surface2 = pygame.Surface((150, 150))
        test_surface2.fill((0, 255, 0))

        image = Image(100, 100, 200, 200, test_surface1)
        assert image.get_image() == test_surface1

        image.set_image(test_surface2)
        assert image.get_image() == test_surface2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
