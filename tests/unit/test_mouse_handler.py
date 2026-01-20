"""
Unit tests for MouseHandler

Tests coordinate transformations and mouse operations.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
import pygame

from src.input.mouse_handler import MouseHandler


@pytest.fixture
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mouse_handler(pygame_init):
    """Create a MouseHandler instance for testing."""
    return MouseHandler(grid_offset_x=100, grid_offset_y=100, tile_size=128, tile_padding=4)


class TestMouseHandlerInit:
    """Test MouseHandler initialization."""

    def test_init_default(self, pygame_init):
        """Test initialization with default values."""
        handler = MouseHandler()
        offset_x, offset_y = handler.get_grid_offset()
        tile_size, padding = handler.get_tile_size()

        assert offset_x == 0
        assert offset_y == 0
        assert tile_size == 128
        assert padding == 4

    def test_init_custom(self, mouse_handler):
        """Test initialization with custom values."""
        offset_x, offset_y = mouse_handler.get_grid_offset()
        tile_size, padding = mouse_handler.get_tile_size()

        assert offset_x == 100
        assert offset_y == 100
        assert tile_size == 128
        assert padding == 4


class TestScreenToGrid:
    """Test screen to grid coordinate conversion."""

    def test_screen_to_grid_first_tile(self, mouse_handler):
        """Test conversion for first tile (0, 0)."""
        result = mouse_handler.screen_to_grid(150, 150)
        assert result == (0, 0)

    def test_screen_to_grid_second_tile(self, mouse_handler):
        """Test conversion for second tile (1, 0)."""
        # 100 (offset) + 128 (tile) + 4 (padding) = 232
        result = mouse_handler.screen_to_grid(250, 150)
        assert result == (1, 0)

    def test_screen_to_grid_diagonal_tile(self, mouse_handler):
        """Test conversion for diagonal tile (1, 1)."""
        result = mouse_handler.screen_to_grid(250, 250)
        assert result == (1, 1)

    def test_screen_to_grid_on_padding(self, mouse_handler):
        """Test that clicks on padding return None."""
        # Click on padding between tiles
        result = mouse_handler.screen_to_grid(229, 150)  # On horizontal padding
        assert result is None

    def test_screen_to_grid_outside_grid(self, mouse_handler):
        """Test that clicks outside grid return None."""
        result = mouse_handler.screen_to_grid(50, 50)  # Before grid offset
        assert result is None

    def test_screen_to_grid_negative(self, mouse_handler):
        """Test that negative coordinates return None."""
        result = mouse_handler.screen_to_grid(-10, -10)
        assert result is None


class TestGridToScreen:
    """Test grid to screen coordinate conversion."""

    def test_grid_to_screen_origin(self, mouse_handler):
        """Test conversion for grid origin (0, 0)."""
        screen_x, screen_y = mouse_handler.grid_to_screen(0, 0)
        assert screen_x == 100
        assert screen_y == 100

    def test_grid_to_screen_second_tile(self, mouse_handler):
        """Test conversion for second tile (1, 0)."""
        screen_x, screen_y = mouse_handler.grid_to_screen(1, 0)
        # 100 (offset) + 1 * (128 + 4) = 232
        assert screen_x == 232
        assert screen_y == 100

    def test_grid_to_screen_diagonal(self, mouse_handler):
        """Test conversion for diagonal tile (2, 2)."""
        screen_x, screen_y = mouse_handler.grid_to_screen(2, 2)
        # 100 + 2 * 132 = 364
        assert screen_x == 364
        assert screen_y == 364


class TestGetTileRect:
    """Test getting tile rectangles."""

    def test_get_tile_rect_origin(self, mouse_handler):
        """Test getting rect for origin tile."""
        rect = mouse_handler.get_tile_rect(0, 0)

        assert rect.x == 100
        assert rect.y == 100
        assert rect.width == 128
        assert rect.height == 128

    def test_get_tile_rect_other_tile(self, mouse_handler):
        """Test getting rect for another tile."""
        rect = mouse_handler.get_tile_rect(1, 1)

        assert rect.x == 232
        assert rect.y == 232
        assert rect.width == 128
        assert rect.height == 128


class TestIsPointInTile:
    """Test point-in-tile checking."""

    def test_is_point_in_tile_true(self, mouse_handler):
        """Test point inside tile."""
        result = mouse_handler.is_point_in_tile(150, 150, 0, 0)
        assert result is True

    def test_is_point_in_tile_false(self, mouse_handler):
        """Test point outside tile."""
        result = mouse_handler.is_point_in_tile(50, 50, 0, 0)
        assert result is False

    def test_is_point_in_tile_edge(self, mouse_handler):
        """Test point on tile edge."""
        result = mouse_handler.is_point_in_tile(100, 100, 0, 0)
        assert result is True


class TestSetters:
    """Test setter methods."""

    def test_set_grid_offset(self, mouse_handler):
        """Test setting grid offset."""
        mouse_handler.set_grid_offset(200, 300)
        offset_x, offset_y = mouse_handler.get_grid_offset()

        assert offset_x == 200
        assert offset_y == 300

    def test_set_tile_size(self, mouse_handler):
        """Test setting tile size and padding."""
        mouse_handler.set_tile_size(64, 2)
        tile_size, padding = mouse_handler.get_tile_size()

        assert tile_size == 64
        assert padding == 2

    def test_set_tile_size_affects_conversion(self, mouse_handler):
        """Test that changing tile size affects conversions."""
        mouse_handler.set_tile_size(64, 2)

        # With smaller tiles, same screen position maps to different grid position
        result = mouse_handler.screen_to_grid(250, 250)
        # 250 - 100 = 150, 150 / 66 = 2
        assert result == (2, 2)


class TestRoundTrip:
    """Test round-trip conversions."""

    def test_round_trip_conversion(self, mouse_handler):
        """Test that grid->screen->grid conversion is consistent."""
        # Start with grid coordinates
        grid_x, grid_y = 2, 3

        # Convert to screen
        screen_x, screen_y = mouse_handler.grid_to_screen(grid_x, grid_y)

        # Add offset to click in middle of tile
        screen_x += 64
        screen_y += 64

        # Convert back to grid
        result = mouse_handler.screen_to_grid(screen_x, screen_y)

        assert result == (grid_x, grid_y)
