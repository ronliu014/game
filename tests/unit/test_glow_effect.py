"""
Unit tests for GlowEffect

Tests glow effect animation, intensity, and rendering.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame
import math

from src.rendering.effects.glow_effect import GlowEffect


class TestGlowEffectInit:
    """Test GlowEffect initialization."""

    def test_init_default(self):
        """Test default initialization."""
        glow = GlowEffect()

        assert glow.get_color() == (100, 200, 255)
        assert glow.get_max_intensity() == 0.8
        assert glow.get_pulse_speed() == 2.0
        assert glow.is_enabled() is True

    def test_init_custom(self):
        """Test initialization with custom parameters."""
        glow = GlowEffect(color=(255, 0, 0), max_intensity=0.5, pulse_speed=3.0)

        assert glow.get_color() == (255, 0, 0)
        assert glow.get_max_intensity() == 0.5
        assert glow.get_pulse_speed() == 3.0

    def test_init_clamp_intensity_high(self):
        """Test intensity clamping (high)."""
        glow = GlowEffect(max_intensity=1.5)

        assert glow.get_max_intensity() == 1.0

    def test_init_clamp_intensity_low(self):
        """Test intensity clamping (low)."""
        glow = GlowEffect(max_intensity=-0.5)

        assert glow.get_max_intensity() == 0.0


class TestGlowEffectUpdate:
    """Test glow effect updates."""

    def test_update_time(self):
        """Test time update."""
        glow = GlowEffect()

        glow.update(100.0)

        assert glow._current_time == 100.0

    def test_update_multiple(self):
        """Test multiple updates."""
        glow = GlowEffect()

        glow.update(100.0)
        glow.update(50.0)

        assert glow._current_time == 150.0

    def test_update_when_disabled(self):
        """Test update when disabled."""
        glow = GlowEffect()
        glow.disable()

        glow.update(100.0)

        assert glow._current_time == 0.0


class TestGlowEffectIntensity:
    """Test intensity calculations."""

    def test_get_current_intensity_initial(self):
        """Test initial intensity."""
        glow = GlowEffect(max_intensity=0.8)

        intensity = glow.get_current_intensity()

        # At time 0, sine wave should be at 0, so intensity should be 0.4 (midpoint)
        assert 0.0 <= intensity <= 0.8

    def test_get_current_intensity_after_update(self):
        """Test intensity after update."""
        glow = GlowEffect(max_intensity=0.8, pulse_speed=1.0)

        # Update to quarter cycle (should be at peak)
        glow.update(250.0)  # 0.25 seconds

        intensity = glow.get_current_intensity()
        assert 0.0 <= intensity <= 0.8

    def test_get_current_intensity_disabled(self):
        """Test intensity when disabled."""
        glow = GlowEffect()
        glow.disable()

        intensity = glow.get_current_intensity()

        assert intensity == 0.0

    def test_intensity_pulse_range(self):
        """Test that intensity stays within range."""
        glow = GlowEffect(max_intensity=0.8)

        # Test at various time points
        for ms in range(0, 2000, 100):
            glow.update(100.0)
            intensity = glow.get_current_intensity()
            assert 0.0 <= intensity <= 0.8


class TestGlowEffectDrawGlow:
    """Test glow rectangle drawing."""

    @patch('pygame.Surface')
    @patch('pygame.draw.rect')
    def test_draw_glow_basic(self, mock_draw_rect, mock_surface_class):
        """Test basic glow drawing."""
        glow = GlowEffect()
        glow.update(250.0)  # Set to non-zero intensity
        surface = Mock()

        glow.draw_glow(surface, 100, 100, 50, 50)

        # Should blit multiple layers
        assert surface.blit.call_count >= 1

    @patch('pygame.Surface')
    def test_draw_glow_disabled(self, mock_surface_class):
        """Test drawing when disabled."""
        glow = GlowEffect()
        glow.disable()
        surface = Mock()

        glow.draw_glow(surface, 100, 100, 50, 50)

        surface.blit.assert_not_called()

    @patch('pygame.Surface')
    def test_draw_glow_zero_intensity(self, mock_surface_class):
        """Test drawing with zero intensity."""
        glow = GlowEffect(max_intensity=0.0)
        surface = Mock()

        glow.draw_glow(surface, 100, 100, 50, 50)

        surface.blit.assert_not_called()


class TestGlowEffectDrawGlowCircle:
    """Test glow circle drawing."""

    @patch('pygame.Surface')
    @patch('pygame.draw.circle')
    def test_draw_glow_circle_basic(self, mock_draw_circle, mock_surface_class):
        """Test basic circle glow drawing."""
        glow = GlowEffect()
        glow.update(250.0)  # Set to non-zero intensity
        surface = Mock()

        glow.draw_glow_circle(surface, 100, 100, 25)

        # Should blit multiple layers
        assert surface.blit.call_count >= 1

    @patch('pygame.Surface')
    def test_draw_glow_circle_disabled(self, mock_surface_class):
        """Test circle drawing when disabled."""
        glow = GlowEffect()
        glow.disable()
        surface = Mock()

        glow.draw_glow_circle(surface, 100, 100, 25)

        surface.blit.assert_not_called()


class TestGlowEffectDrawOutlineGlow:
    """Test outline glow drawing."""

    @patch('pygame.Surface')
    @patch('pygame.draw.rect')
    def test_draw_outline_glow_basic(self, mock_draw_rect, mock_surface_class):
        """Test basic outline glow drawing."""
        glow = GlowEffect()
        glow.update(250.0)  # Set to non-zero intensity
        surface = Mock()

        glow.draw_outline_glow(surface, 100, 100, 50, 50)

        # Should blit to surface
        surface.blit.assert_called_once()

    @patch('pygame.Surface')
    def test_draw_outline_glow_disabled(self, mock_surface_class):
        """Test outline drawing when disabled."""
        glow = GlowEffect()
        glow.disable()
        surface = Mock()

        glow.draw_outline_glow(surface, 100, 100, 50, 50)

        surface.blit.assert_not_called()

    @patch('pygame.Surface')
    @patch('pygame.draw.rect')
    def test_draw_outline_glow_custom_thickness(self, mock_draw_rect, mock_surface_class):
        """Test outline drawing with custom thickness."""
        glow = GlowEffect()
        glow.update(250.0)
        surface = Mock()

        glow.draw_outline_glow(surface, 100, 100, 50, 50, thickness=5)

        surface.blit.assert_called_once()


class TestGlowEffectColor:
    """Test color control."""

    def test_set_color(self):
        """Test setting color."""
        glow = GlowEffect()

        glow.set_color((255, 100, 50))

        assert glow.get_color() == (255, 100, 50)

    def test_get_color(self):
        """Test getting color."""
        glow = GlowEffect(color=(200, 150, 100))

        color = glow.get_color()

        assert color == (200, 150, 100)


class TestGlowEffectMaxIntensity:
    """Test max intensity control."""

    def test_set_max_intensity_valid(self):
        """Test setting valid max intensity."""
        glow = GlowEffect()

        glow.set_max_intensity(0.6)

        assert glow.get_max_intensity() == 0.6

    def test_set_max_intensity_clamp_high(self):
        """Test clamping high max intensity."""
        glow = GlowEffect()

        glow.set_max_intensity(1.5)

        assert glow.get_max_intensity() == 1.0

    def test_set_max_intensity_clamp_low(self):
        """Test clamping low max intensity."""
        glow = GlowEffect()

        glow.set_max_intensity(-0.3)

        assert glow.get_max_intensity() == 0.0

    def test_get_max_intensity(self):
        """Test getting max intensity."""
        glow = GlowEffect(max_intensity=0.7)

        intensity = glow.get_max_intensity()

        assert intensity == 0.7


class TestGlowEffectPulseSpeed:
    """Test pulse speed control."""

    def test_set_pulse_speed(self):
        """Test setting pulse speed."""
        glow = GlowEffect()

        glow.set_pulse_speed(5.0)

        assert glow.get_pulse_speed() == 5.0

    def test_get_pulse_speed(self):
        """Test getting pulse speed."""
        glow = GlowEffect(pulse_speed=3.5)

        speed = glow.get_pulse_speed()

        assert speed == 3.5


class TestGlowEffectEnableDisable:
    """Test enable/disable functionality."""

    def test_enable(self):
        """Test enabling glow effect."""
        glow = GlowEffect()
        glow.disable()

        glow.enable()

        assert glow.is_enabled() is True

    def test_disable(self):
        """Test disabling glow effect."""
        glow = GlowEffect()

        glow.disable()

        assert glow.is_enabled() is False

    def test_is_enabled_default(self):
        """Test default enabled state."""
        glow = GlowEffect()

        assert glow.is_enabled() is True


class TestGlowEffectReset:
    """Test reset functionality."""

    def test_reset(self):
        """Test resetting glow effect."""
        glow = GlowEffect()
        glow.update(500.0)

        glow.reset()

        assert glow._current_time == 0.0

    def test_reset_preserves_settings(self):
        """Test that reset preserves settings."""
        glow = GlowEffect(color=(255, 0, 0), max_intensity=0.5, pulse_speed=3.0)
        glow.update(500.0)

        glow.reset()

        assert glow.get_color() == (255, 0, 0)
        assert glow.get_max_intensity() == 0.5
        assert glow.get_pulse_speed() == 3.0
