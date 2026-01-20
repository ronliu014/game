"""
Unit tests for SpriteManager

Tests sprite loading, caching, rotation, and resource management.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import os
import pytest
import pygame
from unittest.mock import Mock, patch, MagicMock

from src.rendering.sprite_manager import SpriteManager


@pytest.fixture
def sprite_manager():
    """Create a SpriteManager instance for testing."""
    pygame.init()
    manager = SpriteManager()
    yield manager
    pygame.quit()


@pytest.fixture
def mock_sprite():
    """Create a mock pygame.Surface for testing."""
    sprite = pygame.Surface((128, 128), pygame.SRCALPHA)
    sprite.fill((255, 0, 0))
    return sprite


class TestSpriteManagerInit:
    """Test SpriteManager initialization."""

    def test_init_creates_empty_cache(self, sprite_manager):
        """Test that initialization creates an empty cache."""
        assert sprite_manager.get_cache_size() == 0

    def test_init_sets_project_root(self, sprite_manager):
        """Test that initialization sets project root."""
        assert sprite_manager._project_root is not None
        assert os.path.isabs(sprite_manager._project_root)


class TestLoadSprite:
    """Test sprite loading functionality."""

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_sprite_success(self, mock_exists, mock_load, sprite_manager, mock_sprite):
        """Test successful sprite loading."""
        mock_exists.return_value = True
        # Mock convert_alpha to return the sprite itself
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        sprite = sprite_manager.load_sprite("assets/test.png")

        assert sprite is not None
        assert sprite_manager.get_cache_size() == 1

    @patch('os.path.exists')
    def test_load_sprite_file_not_found(self, mock_exists, sprite_manager):
        """Test loading non-existent sprite."""
        mock_exists.return_value = False

        sprite = sprite_manager.load_sprite("assets/nonexistent.png")

        assert sprite is None
        assert sprite_manager.get_cache_size() == 0

    @patch('pygame.transform.scale')
    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_sprite_with_scaling(self, mock_exists, mock_load, mock_scale, sprite_manager, mock_sprite):
        """Test sprite loading with scaling."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        scaled_sprite = pygame.Surface((64, 64))
        mock_scale.return_value = scaled_sprite

        sprite = sprite_manager.load_sprite("assets/test.png", size=(64, 64))

        assert sprite is not None
        assert sprite.get_size() == (64, 64)

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_sprite_caching(self, mock_exists, mock_load, sprite_manager, mock_sprite):
        """Test that sprites are cached properly."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        # Load sprite twice
        sprite1 = sprite_manager.load_sprite("assets/test.png")
        sprite2 = sprite_manager.load_sprite("assets/test.png")

        # Should only load once
        assert mock_load.call_count == 1
        assert sprite1 is sprite2
        assert sprite_manager.get_cache_size() == 1

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_sprite_no_cache(self, mock_exists, mock_load, sprite_manager, mock_sprite):
        """Test loading sprite without caching."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        sprite = sprite_manager.load_sprite("assets/test.png", use_cache=False)

        assert sprite is not None
        assert sprite_manager.get_cache_size() == 0

    @patch('pygame.transform.scale')
    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_sprite_different_sizes_cached_separately(
        self, mock_exists, mock_load, mock_scale, sprite_manager, mock_sprite
    ):
        """Test that different sizes are cached separately."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        # Mock scale to return different sized sprites
        sprite_64 = pygame.Surface((64, 64))
        sprite_128 = pygame.Surface((128, 128))
        mock_scale.side_effect = [sprite_64, sprite_128]

        sprite1 = sprite_manager.load_sprite("assets/test.png", size=(64, 64))
        sprite2 = sprite_manager.load_sprite("assets/test.png", size=(128, 128))

        assert sprite_manager.get_cache_size() == 2
        assert sprite1.get_size() != sprite2.get_size()

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_load_sprite_pygame_error(self, mock_exists, mock_load, sprite_manager):
        """Test handling of pygame.error during loading."""
        mock_exists.return_value = True
        mock_load.side_effect = pygame.error("Test error")

        sprite = sprite_manager.load_sprite("assets/test.png")

        assert sprite is None


class TestRotateSprite:
    """Test sprite rotation functionality."""

    def test_get_rotated_sprite_90(self, sprite_manager, mock_sprite):
        """Test 90-degree rotation."""
        rotated = sprite_manager.get_rotated_sprite(mock_sprite, 90)

        assert rotated is not None
        # Rotation swaps width and height
        assert rotated.get_size() == (mock_sprite.get_height(), mock_sprite.get_width())

    def test_get_rotated_sprite_180(self, sprite_manager, mock_sprite):
        """Test 180-degree rotation."""
        rotated = sprite_manager.get_rotated_sprite(mock_sprite, 180)

        assert rotated is not None
        assert rotated.get_size() == mock_sprite.get_size()

    def test_get_rotated_sprite_270(self, sprite_manager, mock_sprite):
        """Test 270-degree rotation."""
        rotated = sprite_manager.get_rotated_sprite(mock_sprite, 270)

        assert rotated is not None
        assert rotated.get_size() == (mock_sprite.get_height(), mock_sprite.get_width())

    def test_get_rotated_sprite_0(self, sprite_manager, mock_sprite):
        """Test 0-degree rotation (no rotation)."""
        rotated = sprite_manager.get_rotated_sprite(mock_sprite, 0)

        assert rotated is not None
        assert rotated.get_size() == mock_sprite.get_size()


class TestPlaceholderSprite:
    """Test placeholder sprite creation."""

    def test_create_placeholder_sprite_default_color(self, sprite_manager):
        """Test creating placeholder with default color."""
        placeholder = sprite_manager.create_placeholder_sprite((100, 100))

        assert placeholder is not None
        assert placeholder.get_size() == (100, 100)

    def test_create_placeholder_sprite_custom_color(self, sprite_manager):
        """Test creating placeholder with custom color."""
        placeholder = sprite_manager.create_placeholder_sprite((50, 50), color=(255, 0, 0))

        assert placeholder is not None
        assert placeholder.get_size() == (50, 50)


class TestPreloadSprites:
    """Test sprite preloading functionality."""

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_preload_sprites_success(self, mock_exists, mock_load, sprite_manager, mock_sprite):
        """Test successful preloading of multiple sprites."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        paths = ["assets/sprite1.png", "assets/sprite2.png", "assets/sprite3.png"]
        loaded_count = sprite_manager.preload_sprites(paths)

        assert loaded_count == 3
        assert sprite_manager.get_cache_size() == 3

    @patch('os.path.exists')
    def test_preload_sprites_partial_failure(self, mock_exists, sprite_manager):
        """Test preloading with some failures."""
        # First two exist, third doesn't
        mock_exists.side_effect = [True, True, False]

        with patch('pygame.image.load') as mock_load:
            mock_sprite = pygame.Surface((10, 10))
            mock_sprite_with_alpha = Mock()
            mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
            mock_load.return_value = mock_sprite_with_alpha
            paths = ["assets/sprite1.png", "assets/sprite2.png", "assets/missing.png"]
            loaded_count = sprite_manager.preload_sprites(paths)

        assert loaded_count == 2
        assert sprite_manager.get_cache_size() == 2

    def test_preload_sprites_empty_list(self, sprite_manager):
        """Test preloading with empty list."""
        loaded_count = sprite_manager.preload_sprites([])

        assert loaded_count == 0
        assert sprite_manager.get_cache_size() == 0


class TestCacheManagement:
    """Test cache management functionality."""

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_clear_cache(self, mock_exists, mock_load, sprite_manager, mock_sprite):
        """Test clearing the sprite cache."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        # Load some sprites
        sprite_manager.load_sprite("assets/sprite1.png")
        sprite_manager.load_sprite("assets/sprite2.png")
        assert sprite_manager.get_cache_size() == 2

        # Clear cache
        sprite_manager.clear_cache()
        assert sprite_manager.get_cache_size() == 0

    def test_get_cache_size_empty(self, sprite_manager):
        """Test getting cache size when empty."""
        assert sprite_manager.get_cache_size() == 0

    @patch('pygame.image.load')
    @patch('os.path.exists')
    def test_get_cache_size_with_sprites(self, mock_exists, mock_load, sprite_manager, mock_sprite):
        """Test getting cache size with sprites loaded."""
        mock_exists.return_value = True
        mock_sprite_with_alpha = Mock()
        mock_sprite_with_alpha.convert_alpha.return_value = mock_sprite
        mock_load.return_value = mock_sprite_with_alpha

        sprite_manager.load_sprite("assets/sprite1.png")
        sprite_manager.load_sprite("assets/sprite2.png")
        assert sprite_manager.get_cache_size() == 2


class TestUtilityMethods:
    """Test utility methods."""

    def test_get_sprite_size(self, sprite_manager, mock_sprite):
        """Test getting sprite size."""
        size = sprite_manager.get_sprite_size(mock_sprite)

        assert size == (128, 128)

    def test_get_sprite_size_different_dimensions(self, sprite_manager):
        """Test getting size of sprite with different dimensions."""
        sprite = pygame.Surface((64, 32))
        size = sprite_manager.get_sprite_size(sprite)

        assert size == (64, 32)
