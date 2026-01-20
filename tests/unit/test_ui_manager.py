"""
Unit tests for UIManager

Tests UI component management and event handling.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
import pygame
from unittest.mock import Mock

from src.rendering.ui.ui_manager import UIManager
from src.rendering.ui.button import Button


@pytest.fixture
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def ui_manager():
    """Create a UIManager instance for testing."""
    return UIManager()


@pytest.fixture
def button(pygame_init):
    """Create a Button for testing."""
    return Button(100, 100, 200, 50, "Test")


class TestUIManagerInit:
    """Test UIManager initialization."""

    def test_init(self, ui_manager):
        """Test UIManager initialization."""
        assert ui_manager.get_component_count() == 0


class TestUIManagerComponents:
    """Test component management."""

    def test_add_component(self, ui_manager, button):
        """Test adding a component."""
        ui_manager.add_component(button)
        assert ui_manager.get_component_count() == 1

    def test_add_multiple_components(self, ui_manager, pygame_init):
        """Test adding multiple components."""
        button1 = Button(0, 0, 100, 50, "Button 1")
        button2 = Button(0, 100, 100, 50, "Button 2")

        ui_manager.add_component(button1)
        ui_manager.add_component(button2)

        assert ui_manager.get_component_count() == 2

    def test_remove_component(self, ui_manager, button):
        """Test removing a component."""
        ui_manager.add_component(button)
        result = ui_manager.remove_component(button)

        assert result is True
        assert ui_manager.get_component_count() == 0

    def test_remove_nonexistent_component(self, ui_manager, button):
        """Test removing a component that doesn't exist."""
        result = ui_manager.remove_component(button)

        assert result is False

    def test_clear_components(self, ui_manager, pygame_init):
        """Test clearing all components."""
        button1 = Button(0, 0, 100, 50, "Button 1")
        button2 = Button(0, 100, 100, 50, "Button 2")

        ui_manager.add_component(button1)
        ui_manager.add_component(button2)
        ui_manager.clear_components()

        assert ui_manager.get_component_count() == 0

    def test_get_components(self, ui_manager, button):
        """Test getting all components."""
        ui_manager.add_component(button)
        components = ui_manager.get_components()

        assert len(components) == 1
        assert button in components


class TestUIManagerDraw:
    """Test drawing functionality."""

    def test_draw_empty(self, ui_manager, pygame_init):
        """Test drawing with no components."""
        surface = pygame.Surface((800, 600))
        # Should not raise exception
        ui_manager.draw(surface)

    def test_draw_with_components(self, ui_manager, button, pygame_init):
        """Test drawing with components."""
        surface = pygame.Surface((800, 600))
        ui_manager.add_component(button)
        # Should not raise exception
        ui_manager.draw(surface)

    def test_draw_hidden_component(self, ui_manager, button, pygame_init):
        """Test that hidden components are not drawn."""
        surface = pygame.Surface((800, 600))
        button.hide()
        ui_manager.add_component(button)
        # Should not raise exception
        ui_manager.draw(surface)


class TestUIManagerEvents:
    """Test event handling."""

    def test_handle_event_no_components(self, ui_manager):
        """Test handling event with no components."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        result = ui_manager.handle_event(event)

        assert result is False

    def test_handle_event_with_component(self, ui_manager, pygame_init):
        """Test handling event with component."""
        callback = Mock()
        button = Button(100, 100, 200, 50, "Test", on_click=callback)
        ui_manager.add_component(button)

        # Click button
        down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        ui_manager.handle_event(down_event)

        up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (150, 125)})
        result = ui_manager.handle_event(up_event)

        assert result is True
        callback.assert_called_once()


class TestUIManagerBulkOperations:
    """Test bulk operations on components."""

    def test_show_all(self, ui_manager, pygame_init):
        """Test showing all components."""
        button1 = Button(0, 0, 100, 50, "Button 1")
        button2 = Button(0, 100, 100, 50, "Button 2")
        button1.hide()
        button2.hide()

        ui_manager.add_component(button1)
        ui_manager.add_component(button2)
        ui_manager.show_all()

        assert button1.is_visible() is True
        assert button2.is_visible() is True

    def test_hide_all(self, ui_manager, pygame_init):
        """Test hiding all components."""
        button1 = Button(0, 0, 100, 50, "Button 1")
        button2 = Button(0, 100, 100, 50, "Button 2")

        ui_manager.add_component(button1)
        ui_manager.add_component(button2)
        ui_manager.hide_all()

        assert button1.is_visible() is False
        assert button2.is_visible() is False

    def test_enable_all(self, ui_manager, pygame_init):
        """Test enabling all components."""
        button1 = Button(0, 0, 100, 50, "Button 1")
        button2 = Button(0, 100, 100, 50, "Button 2")
        button1.disable()
        button2.disable()

        ui_manager.add_component(button1)
        ui_manager.add_component(button2)
        ui_manager.enable_all()

        assert button1.is_enabled() is True
        assert button2.is_enabled() is True

    def test_disable_all(self, ui_manager, pygame_init):
        """Test disabling all components."""
        button1 = Button(0, 0, 100, 50, "Button 1")
        button2 = Button(0, 100, 100, 50, "Button 2")

        ui_manager.add_component(button1)
        ui_manager.add_component(button2)
        ui_manager.disable_all()

        assert button1.is_enabled() is False
        assert button2.is_enabled() is False
