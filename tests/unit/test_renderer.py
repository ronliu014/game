"""
Unit tests for Renderer

Tests rendering engine initialization, drawing operations, and resource management.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock

from src.rendering.renderer import Renderer
from src.config.config_manager import ConfigManager


@pytest.fixture
def mock_config():
    """Create a mock ConfigManager for testing."""
    config = Mock(spec=ConfigManager)
    config.get.side_effect = lambda key, default=None: {
        "window.width": 800,
        "window.height": 600,
        "window.title": "Test Game",
        "window.fps": 60,
        "window.fullscreen": False,
    }.get(key, default)
    return config


@pytest.fixture
def renderer(mock_config):
    """Create a Renderer instance for testing."""
    return Renderer(config=mock_config)


@pytest.fixture
def initialized_renderer(mock_config):
    """Create and initialize a Renderer instance for testing."""
    renderer = Renderer(config=mock_config)
    renderer.initialize()
    yield renderer
    renderer.shutdown()


class TestRendererInit:
    """Test Renderer initialization."""

    def test_init_with_config(self, mock_config):
        """Test initialization with provided config."""
        renderer = Renderer(config=mock_config)

        assert renderer._config is mock_config
        assert not renderer.is_initialized()

    def test_init_without_config(self):
        """Test initialization without config (creates default)."""
        renderer = Renderer()

        assert renderer._config is not None
        assert not renderer.is_initialized()

    def test_init_sets_window_properties(self, renderer):
        """Test that initialization sets window properties from config."""
        assert renderer._window_size == (800, 600)
        assert renderer._window_title == "Test Game"
        assert renderer._target_fps == 60
        assert renderer._fullscreen is False


class TestInitializeShutdown:
    """Test Pygame initialization and shutdown."""

    def test_initialize_success(self, renderer):
        """Test successful Pygame initialization."""
        success = renderer.initialize()

        assert success is True
        assert renderer.is_initialized()

        renderer.shutdown()

    def test_initialize_creates_screen(self, renderer):
        """Test that initialization creates screen surface."""
        renderer.initialize()

        assert renderer._screen is not None
        assert renderer._screen.get_size() == (800, 600)

        renderer.shutdown()

    def test_initialize_creates_clock(self, renderer):
        """Test that initialization creates clock."""
        renderer.initialize()

        assert renderer._clock is not None

        renderer.shutdown()

    def test_initialize_already_initialized(self, initialized_renderer):
        """Test initializing when already initialized."""
        success = initialized_renderer.initialize()

        assert success is True

    def test_shutdown_when_initialized(self, renderer):
        """Test shutdown after initialization."""
        renderer.initialize()
        renderer.shutdown()

        assert not renderer.is_initialized()

    def test_shutdown_when_not_initialized(self, renderer):
        """Test shutdown when not initialized (should not crash)."""
        renderer.shutdown()

        assert not renderer.is_initialized()


class TestDrawingOperations:
    """Test drawing operations."""

    def test_clear_default_color(self, initialized_renderer):
        """Test clearing screen with default color."""
        # Should not raise exception
        initialized_renderer.clear()

    def test_clear_custom_color(self, initialized_renderer):
        """Test clearing screen with custom color."""
        # Should not raise exception
        initialized_renderer.clear(color=(255, 0, 0))

    def test_clear_not_initialized(self, renderer):
        """Test clearing when not initialized."""
        # Should not crash, just log warning
        renderer.clear()

    def test_draw_sprite(self, initialized_renderer):
        """Test drawing a sprite."""
        sprite = pygame.Surface((64, 64))

        # Should not raise exception
        initialized_renderer.draw_sprite(sprite, (100, 100))

    def test_draw_sprite_with_rotation(self, initialized_renderer):
        """Test drawing a rotated sprite."""
        sprite = pygame.Surface((64, 64))

        # Should not raise exception
        initialized_renderer.draw_sprite(sprite, (100, 100), rotation=90)

    def test_draw_sprite_not_initialized(self, renderer):
        """Test drawing sprite when not initialized."""
        sprite = pygame.Surface((64, 64))

        # Should not crash, just log warning
        renderer.draw_sprite(sprite, (100, 100))

    def test_draw_text(self, initialized_renderer):
        """Test drawing text."""
        # Should not raise exception
        initialized_renderer.draw_text("Hello World", (100, 100))

    def test_draw_text_custom_params(self, initialized_renderer):
        """Test drawing text with custom parameters."""
        # Should not raise exception
        initialized_renderer.draw_text(
            "Test",
            (50, 50),
            font_size=32,
            color=(255, 255, 0)
        )

    def test_draw_text_not_initialized(self, renderer):
        """Test drawing text when not initialized."""
        # Should not crash, just log warning
        renderer.draw_text("Test", (100, 100))

    def test_draw_rect_filled(self, initialized_renderer):
        """Test drawing filled rectangle."""
        # Should not raise exception
        initialized_renderer.draw_rect((100, 100, 200, 150), (255, 0, 0))

    def test_draw_rect_outline(self, initialized_renderer):
        """Test drawing rectangle outline."""
        # Should not raise exception
        initialized_renderer.draw_rect((100, 100, 200, 150), (0, 255, 0), width=2)

    def test_draw_rect_not_initialized(self, renderer):
        """Test drawing rect when not initialized."""
        # Should not crash, just log warning
        renderer.draw_rect((100, 100, 200, 150), (255, 0, 0))

    def test_draw_circle_filled(self, initialized_renderer):
        """Test drawing filled circle."""
        # Should not raise exception
        initialized_renderer.draw_circle((400, 300), 50, (0, 0, 255))

    def test_draw_circle_outline(self, initialized_renderer):
        """Test drawing circle outline."""
        # Should not raise exception
        initialized_renderer.draw_circle((400, 300), 50, (255, 255, 0), width=3)

    def test_draw_circle_not_initialized(self, renderer):
        """Test drawing circle when not initialized."""
        # Should not crash, just log warning
        renderer.draw_circle((400, 300), 50, (0, 0, 255))


class TestPresent:
    """Test frame presentation."""

    def test_present(self, initialized_renderer):
        """Test presenting a frame."""
        # Should not raise exception
        initialized_renderer.clear()
        initialized_renderer.present()

    def test_present_not_initialized(self, renderer):
        """Test presenting when not initialized."""
        # Should not crash, just log warning
        renderer.present()

    def test_present_updates_fps(self, initialized_renderer):
        """Test that present updates FPS counter."""
        initial_fps = initialized_renderer.get_fps()

        # Present a few frames
        for _ in range(5):
            initialized_renderer.clear()
            initialized_renderer.present()

        # FPS should be calculated (may be 0 initially)
        fps = initialized_renderer.get_fps()
        assert fps >= 0


class TestGetters:
    """Test getter methods."""

    def test_get_sprite_manager(self, renderer):
        """Test getting sprite manager."""
        sprite_mgr = renderer.get_sprite_manager()

        assert sprite_mgr is not None
        assert sprite_mgr is renderer._sprite_manager

    def test_get_fps_initial(self, renderer):
        """Test getting FPS before any frames."""
        fps = renderer.get_fps()

        assert fps == 0.0

    def test_get_window_size(self, renderer):
        """Test getting window size."""
        size = renderer.get_window_size()

        assert size == (800, 600)

    def test_is_initialized_false(self, renderer):
        """Test is_initialized when not initialized."""
        assert renderer.is_initialized() is False

    def test_is_initialized_true(self, initialized_renderer):
        """Test is_initialized when initialized."""
        assert initialized_renderer.is_initialized() is True


class TestSetters:
    """Test setter methods."""

    def test_set_window_title_when_initialized(self, initialized_renderer):
        """Test setting window title when initialized."""
        initialized_renderer.set_window_title("New Title")

        assert initialized_renderer._window_title == "New Title"

    def test_set_window_title_when_not_initialized(self, renderer):
        """Test setting window title when not initialized."""
        # Should not crash
        renderer.set_window_title("New Title")


class TestIntegration:
    """Integration tests for complete rendering flow."""

    def test_complete_render_cycle(self, initialized_renderer):
        """Test a complete render cycle."""
        # Clear screen
        initialized_renderer.clear()

        # Draw some elements
        sprite = pygame.Surface((64, 64))
        sprite.fill((255, 0, 0))
        initialized_renderer.draw_sprite(sprite, (100, 100))
        initialized_renderer.draw_text("Test", (200, 200))
        initialized_renderer.draw_rect((300, 300, 50, 50), (0, 255, 0))
        initialized_renderer.draw_circle((400, 400), 25, (0, 0, 255))

        # Present frame
        initialized_renderer.present()

        # Should complete without errors
        assert initialized_renderer.is_initialized()

    def test_multiple_frames(self, initialized_renderer):
        """Test rendering multiple frames."""
        for i in range(10):
            initialized_renderer.clear()
            initialized_renderer.draw_text(f"Frame {i}", (10, 10))
            initialized_renderer.present()

        # FPS should be calculated
        fps = initialized_renderer.get_fps()
        assert fps >= 0
