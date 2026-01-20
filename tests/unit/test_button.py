"""
Unit tests for Button UI component

Tests button creation, interaction, and event handling.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
import pygame
from unittest.mock import Mock, MagicMock

from src.rendering.ui.button import Button


@pytest.fixture
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def button(pygame_init):
    """Create a Button instance for testing."""
    return Button(100, 100, 200, 50, "Test Button")


@pytest.fixture
def button_with_callback(pygame_init):
    """Create a Button with a callback for testing."""
    callback = Mock()
    return Button(100, 100, 200, 50, "Click Me", on_click=callback), callback


class TestButtonInit:
    """Test Button initialization."""

    def test_init_basic(self, button):
        """Test basic button initialization."""
        assert button.x == 100
        assert button.y == 100
        assert button.width == 200
        assert button.height == 50
        assert button.text == "Test Button"
        assert button.visible is True
        assert button.enabled is True

    def test_init_with_callback(self, button_with_callback):
        """Test button initialization with callback."""
        button, callback = button_with_callback
        assert button.on_click is callback

    def test_init_custom_colors(self, pygame_init):
        """Test button initialization with custom colors."""
        button = Button(
            0, 0, 100, 50, "Test",
            color_normal=(255, 0, 0),
            color_hover=(0, 255, 0),
            color_pressed=(0, 0, 255),
            text_color=(255, 255, 0)
        )
        assert button._color_normal == (255, 0, 0)
        assert button._color_hover == (0, 255, 0)
        assert button._color_pressed == (0, 0, 255)
        assert button._text_color == (255, 255, 0)


class TestButtonDraw:
    """Test Button drawing."""

    def test_draw_visible(self, button, pygame_init):
        """Test drawing a visible button."""
        surface = pygame.Surface((800, 600))
        # Should not raise exception
        button.draw(surface)

    def test_draw_hidden(self, button, pygame_init):
        """Test that hidden button doesn't draw."""
        surface = pygame.Surface((800, 600))
        button.hide()
        # Should not raise exception
        button.draw(surface)

    def test_draw_disabled(self, button, pygame_init):
        """Test drawing a disabled button."""
        surface = pygame.Surface((800, 600))
        button.disable()
        # Should not raise exception
        button.draw(surface)


class TestButtonEvents:
    """Test Button event handling."""

    def test_mouse_motion_hover(self, button):
        """Test mouse motion creates hover state."""
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (150, 125)})
        result = button.handle_event(event)

        assert result is True
        assert button.is_hovered() is True

    def test_mouse_motion_no_hover(self, button):
        """Test mouse motion outside button."""
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (50, 50)})
        result = button.handle_event(event)

        assert result is False
        assert button.is_hovered() is False

    def test_mouse_button_down(self, button):
        """Test mouse button down on button."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        result = button.handle_event(event)

        assert result is True
        assert button.is_pressed() is True

    def test_mouse_button_down_outside(self, button):
        """Test mouse button down outside button."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (50, 50)})
        result = button.handle_event(event)

        assert result is False
        assert button.is_pressed() is False

    def test_mouse_button_up_click(self, button_with_callback):
        """Test complete click (down then up)."""
        button, callback = button_with_callback

        # Press button
        down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        button.handle_event(down_event)

        # Release button
        up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (150, 125)})
        result = button.handle_event(up_event)

        assert result is True
        assert button.is_pressed() is False
        callback.assert_called_once()

    def test_mouse_button_up_no_click(self, button_with_callback):
        """Test button up without prior down (no click)."""
        button, callback = button_with_callback

        up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (150, 125)})
        result = button.handle_event(up_event)

        assert result is False
        callback.assert_not_called()

    def test_mouse_button_up_outside(self, button_with_callback):
        """Test button up outside after pressing (no click)."""
        button, callback = button_with_callback

        # Press button
        down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        button.handle_event(down_event)

        # Release outside
        up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (50, 50)})
        result = button.handle_event(up_event)

        assert result is False
        callback.assert_not_called()

    def test_disabled_button_no_events(self, button_with_callback):
        """Test that disabled button doesn't handle events."""
        button, callback = button_with_callback
        button.disable()

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        result = button.handle_event(event)

        assert result is False
        callback.assert_not_called()

    def test_hidden_button_no_events(self, button_with_callback):
        """Test that hidden button doesn't handle events."""
        button, callback = button_with_callback
        button.hide()

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        result = button.handle_event(event)

        assert result is False
        callback.assert_not_called()


class TestButtonMethods:
    """Test Button methods."""

    def test_set_text(self, button):
        """Test setting button text."""
        button.set_text("New Text")
        assert button.text == "New Text"

    def test_set_callback(self, button):
        """Test setting callback function."""
        new_callback = Mock()
        button.set_callback(new_callback)
        assert button.on_click is new_callback

    def test_get_rect(self, button):
        """Test getting button rectangle."""
        rect = button.get_rect()
        assert rect.x == 100
        assert rect.y == 100
        assert rect.width == 200
        assert rect.height == 50

    def test_contains_point_inside(self, button):
        """Test point inside button."""
        assert button.contains_point(150, 125) is True

    def test_contains_point_outside(self, button):
        """Test point outside button."""
        assert button.contains_point(50, 50) is False

    def test_set_position(self, button):
        """Test setting button position."""
        button.set_position(200, 300)
        assert button.x == 200
        assert button.y == 300

    def test_set_size(self, button):
        """Test setting button size."""
        button.set_size(300, 100)
        assert button.width == 300
        assert button.height == 100


class TestButtonStates:
    """Test Button state management."""

    def test_initial_state(self, button):
        """Test initial button state."""
        assert button.is_visible() is True
        assert button.is_enabled() is True
        assert button.is_hovered() is False
        assert button.is_pressed() is False

    def test_show_hide(self, button):
        """Test show/hide functionality."""
        button.hide()
        assert button.is_visible() is False

        button.show()
        assert button.is_visible() is True

    def test_enable_disable(self, button):
        """Test enable/disable functionality."""
        button.disable()
        assert button.is_enabled() is False

        button.enable()
        assert button.is_enabled() is True
