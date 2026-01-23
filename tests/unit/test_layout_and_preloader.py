"""
Unit tests for LayoutManager and ResourcePreloader.

Tests layout management and resource loading functionality.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pytest
import pygame
from pathlib import Path
from src.ui.layouts.layout_manager import LayoutManager
from src.ui.resource_preloader import ResourcePreloader, ResourceType
from src.ui.components.button import Button
from src.ui.components.panel import Panel


@pytest.fixture(scope="module")
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    pygame.mixer.init()
    yield
    pygame.mixer.quit()
    pygame.quit()


class TestLayoutManager:
    """Test LayoutManager functionality."""

    def test_layout_manager_creation(self, pygame_init):
        """Test layout manager can be created."""
        layout = LayoutManager(800, 600)
        assert layout.get_screen_size() == (800, 600)

    def test_center_component(self, pygame_init):
        """Test centering a component."""
        layout = LayoutManager(800, 600)
        button = Button(0, 0, 200, 50, "Test")

        # Center both horizontally and vertically
        layout.center_component(button, horizontal=True, vertical=True)
        assert button.x == (800 - 200) // 2
        assert button.y == (600 - 50) // 2

        # Center only horizontally
        button.set_position(0, 0)
        layout.center_component(button, horizontal=True, vertical=False)
        assert button.x == (800 - 200) // 2
        assert button.y == 0

        # Center with offset
        layout.center_component(button, horizontal=True, vertical=True, offset_x=50, offset_y=30)
        assert button.x == (800 - 200) // 2 + 50
        assert button.y == (600 - 50) // 2 + 30

    def test_arrange_vertical(self, pygame_init):
        """Test vertical arrangement."""
        layout = LayoutManager(800, 600)
        buttons = [
            Button(0, 0, 200, 50, "Button 1"),
            Button(0, 0, 200, 50, "Button 2"),
            Button(0, 0, 200, 50, "Button 3")
        ]

        layout.arrange_vertical(buttons, start_x=100, start_y=100, spacing=10)

        assert buttons[0].x == 100
        assert buttons[0].y == 100
        assert buttons[1].y == 100 + 50 + 10
        assert buttons[2].y == 100 + 50 + 10 + 50 + 10

    def test_arrange_horizontal(self, pygame_init):
        """Test horizontal arrangement."""
        layout = LayoutManager(800, 600)
        buttons = [
            Button(0, 0, 100, 50, "Button 1"),
            Button(0, 0, 100, 50, "Button 2"),
            Button(0, 0, 100, 50, "Button 3")
        ]

        layout.arrange_horizontal(buttons, start_x=50, start_y=200, spacing=20)

        assert buttons[0].x == 50
        assert buttons[0].y == 200
        assert buttons[1].x == 50 + 100 + 20
        assert buttons[2].x == 50 + 100 + 20 + 100 + 20

    def test_anchor_component(self, pygame_init):
        """Test anchor positioning."""
        layout = LayoutManager(800, 600)
        button = Button(0, 0, 200, 50, "Test")

        # Top left
        layout.anchor_component(button, LayoutManager.ANCHOR_TOP_LEFT, margin_x=10, margin_y=10)
        assert button.x == 10
        assert button.y == 10

        # Top center
        layout.anchor_component(button, LayoutManager.ANCHOR_TOP_CENTER)
        assert button.x == (800 - 200) // 2
        assert button.y == 0

        # Bottom right
        layout.anchor_component(button, LayoutManager.ANCHOR_BOTTOM_RIGHT, margin_x=10, margin_y=10)
        assert button.x == 800 - 200 - 10
        assert button.y == 600 - 50 - 10

        # Center
        layout.anchor_component(button, LayoutManager.ANCHOR_CENTER)
        assert button.x == (800 - 200) // 2
        assert button.y == (600 - 50) // 2

    def test_arrange_grid(self, pygame_init):
        """Test grid arrangement."""
        layout = LayoutManager(800, 600)
        buttons = [Button(0, 0, 100, 50, f"Button {i}") for i in range(6)]

        layout.arrange_grid(buttons, columns=3, start_x=50, start_y=100, spacing_x=10, spacing_y=10)

        # First row
        assert buttons[0].x == 50
        assert buttons[0].y == 100
        assert buttons[1].x == 50 + 100 + 10
        assert buttons[2].x == 50 + 100 + 10 + 100 + 10

        # Second row
        assert buttons[3].x == 50
        assert buttons[3].y == 100 + 50 + 10

    def test_distribute_horizontal(self, pygame_init):
        """Test horizontal distribution."""
        layout = LayoutManager(800, 600)
        buttons = [
            Button(0, 0, 100, 50, "Button 1"),
            Button(0, 0, 100, 50, "Button 2"),
            Button(0, 0, 100, 50, "Button 3")
        ]

        layout.distribute_horizontal(buttons, start_x=100, end_x=700, y=200)

        assert buttons[0].x == 100
        assert buttons[0].y == 200
        assert buttons[2].x == 700 - 100  # Last button at end
        # Middle button should be evenly spaced

    def test_distribute_vertical(self, pygame_init):
        """Test vertical distribution."""
        layout = LayoutManager(800, 600)
        buttons = [
            Button(0, 0, 100, 50, "Button 1"),
            Button(0, 0, 100, 50, "Button 2"),
            Button(0, 0, 100, 50, "Button 3")
        ]

        layout.distribute_vertical(buttons, x=300, start_y=100, end_y=500)

        assert buttons[0].x == 300
        assert buttons[0].y == 100
        assert buttons[2].y == 500 - 50  # Last button at end

    def test_set_screen_size(self, pygame_init):
        """Test updating screen size."""
        layout = LayoutManager(800, 600)
        assert layout.get_screen_size() == (800, 600)

        layout.set_screen_size(1024, 768)
        assert layout.get_screen_size() == (1024, 768)


class TestResourcePreloader:
    """Test ResourcePreloader functionality."""

    def test_resource_preloader_creation(self, pygame_init):
        """Test resource preloader can be created."""
        preloader = ResourcePreloader()
        assert preloader.get_cache_size() == 0
        assert preloader.get_progress() == 1.0

    def test_add_resources_to_queue(self, pygame_init):
        """Test adding resources to load queue."""
        preloader = ResourcePreloader()

        preloader.add_image("test_image", "assets/test.png")
        preloader.add_sound("test_sound", "assets/test.wav")
        preloader.add_music("test_music", "assets/test.ogg")
        preloader.add_font("test_font", "assets/test.ttf", 24)

        # Queue should have 4 items
        assert len(preloader._load_queue) == 4

    def test_load_placeholder_images(self, pygame_init):
        """Test loading actual placeholder images."""
        preloader = ResourcePreloader()

        # Add some placeholder images that should exist
        placeholder_dir = Path("assets/ui/buttons")
        if placeholder_dir.exists():
            button_files = list(placeholder_dir.glob("button_start_*.png"))
            if button_files:
                for i, button_file in enumerate(button_files[:3]):
                    preloader.add_image(f"button_{i}", str(button_file))

                # Load all resources
                progress_values = []
                def track_progress(p):
                    progress_values.append(p)

                success = preloader.load_all(progress_callback=track_progress)

                # Check progress was tracked
                assert len(progress_values) > 0
                assert progress_values[-1] == 1.0

                # Check resources were loaded
                if success:
                    assert preloader.get_cache_size() > 0

    def test_get_resource(self, pygame_init):
        """Test retrieving resources."""
        preloader = ResourcePreloader()

        # Create a test surface and add it directly to cache
        test_surface = pygame.Surface((100, 100))
        test_surface.fill((255, 0, 0))
        preloader._resources["test_image"] = test_surface

        # Retrieve the resource
        retrieved = preloader.get_image("test_image")
        assert retrieved is not None
        assert retrieved.get_size() == (100, 100)

    def test_has_resource(self, pygame_init):
        """Test checking if resource exists."""
        preloader = ResourcePreloader()

        assert preloader.has_resource("nonexistent") is False

        # Add a resource directly
        preloader._resources["test"] = pygame.Surface((10, 10))
        assert preloader.has_resource("test") is True

    def test_remove_resource(self, pygame_init):
        """Test removing a resource."""
        preloader = ResourcePreloader()

        # Add a resource
        preloader._resources["test"] = pygame.Surface((10, 10))
        assert preloader.has_resource("test") is True

        # Remove it
        result = preloader.remove_resource("test")
        assert result is True
        assert preloader.has_resource("test") is False

        # Try to remove non-existent resource
        result = preloader.remove_resource("nonexistent")
        assert result is False

    def test_clear_cache(self, pygame_init):
        """Test clearing the cache."""
        preloader = ResourcePreloader()

        # Add some resources
        preloader._resources["test1"] = pygame.Surface((10, 10))
        preloader._resources["test2"] = pygame.Surface((20, 20))
        assert preloader.get_cache_size() == 2

        # Clear cache
        preloader.clear_cache()
        assert preloader.get_cache_size() == 0

    def test_progress_tracking(self, pygame_init):
        """Test progress tracking during loading."""
        preloader = ResourcePreloader()

        # Create test surfaces
        for i in range(5):
            surface = pygame.Surface((10, 10))
            preloader._resources[f"test_{i}"] = surface

        # Simulate loading progress
        preloader._total_resources = 5
        preloader._loaded_resources = 0

        assert preloader.get_progress() == 0.0

        preloader._loaded_resources = 2
        assert preloader.get_progress() == 0.4

        preloader._loaded_resources = 5
        assert preloader.get_progress() == 1.0

    def test_get_counts(self, pygame_init):
        """Test getting resource counts."""
        preloader = ResourcePreloader()

        preloader._total_resources = 10
        preloader._loaded_resources = 7

        assert preloader.get_total_count() == 10
        assert preloader.get_loaded_count() == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
