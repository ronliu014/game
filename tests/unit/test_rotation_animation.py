"""
Unit tests for RotationAnimation

Tests rotation animation with easing functions.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock

from src.rendering.animation.rotation_animation import RotationAnimation


class TestRotationAnimationInit:
    """Test RotationAnimation initialization."""

    def test_init_basic(self):
        """Test basic initialization."""
        anim = RotationAnimation(0, 90, duration_ms=300)

        assert anim.start_angle == 0
        assert anim.end_angle == 90
        assert anim.current_angle == 0
        assert anim.duration_ms == 300
        assert anim.is_playing is False
        assert anim.is_finished is False

    def test_init_with_callback(self):
        """Test initialization with completion callback."""
        callback = Mock()
        anim = RotationAnimation(0, 90, on_complete=callback)

        assert anim.on_complete is callback


class TestRotationAnimationPlayback:
    """Test animation playback."""

    def test_start(self):
        """Test starting animation."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()

        assert anim.is_playing is True
        assert anim.is_finished is False
        assert anim.elapsed_ms == 0

    def test_stop(self):
        """Test stopping animation."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.stop()

        assert anim.is_playing is False

    def test_reset(self):
        """Test resetting animation."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.update(150)
        anim.reset()

        assert anim.elapsed_ms == 0
        assert anim.is_finished is False


class TestRotationAnimationUpdate:
    """Test animation updates."""

    def test_update_halfway(self):
        """Test update at halfway point."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.update(150)  # 50% progress

        # With easing, angle won't be exactly 45, but should be close
        assert 30 < anim.get_current_angle() < 60

    def test_update_complete(self):
        """Test update to completion."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.update(300)

        assert anim.get_current_angle() == 90
        assert anim.is_finished is True
        assert anim.is_playing is False

    def test_update_beyond_duration(self):
        """Test update beyond duration."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.update(500)

        assert anim.get_current_angle() == 90
        assert anim.is_finished is True

    def test_update_when_not_playing(self):
        """Test that update does nothing when not playing."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.update(150)

        assert anim.get_current_angle() == 0

    def test_update_incremental(self):
        """Test incremental updates."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()

        # Update in small increments
        for _ in range(10):
            anim.update(30)

        assert anim.get_current_angle() == 90
        assert anim.is_finished is True


class TestRotationAnimationCallback:
    """Test completion callback."""

    def test_callback_called_on_complete(self):
        """Test that callback is called when animation completes."""
        callback = Mock()
        anim = RotationAnimation(0, 90, duration_ms=300, on_complete=callback)
        anim.start()
        anim.update(300)

        callback.assert_called_once()

    def test_callback_not_called_before_complete(self):
        """Test that callback is not called before completion."""
        callback = Mock()
        anim = RotationAnimation(0, 90, duration_ms=300, on_complete=callback)
        anim.start()
        anim.update(150)

        callback.assert_not_called()

    def test_callback_called_only_once(self):
        """Test that callback is called only once."""
        callback = Mock()
        anim = RotationAnimation(0, 90, duration_ms=300, on_complete=callback)
        anim.start()
        anim.update(300)
        anim.update(100)  # Update again after completion

        callback.assert_called_once()


class TestRotationAnimationAngles:
    """Test angle calculations."""

    def test_get_current_angle_initial(self):
        """Test getting initial angle."""
        anim = RotationAnimation(45, 135, duration_ms=300)

        assert anim.get_current_angle() == 45

    def test_get_current_angle_final(self):
        """Test getting final angle."""
        anim = RotationAnimation(45, 135, duration_ms=300)
        anim.start()
        anim.update(300)

        assert anim.get_current_angle() == 135

    def test_set_angles(self):
        """Test setting new angles."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.set_angles(90, 180)

        assert anim.start_angle == 90
        assert anim.end_angle == 180
        assert anim.current_angle == 90

    def test_negative_angles(self):
        """Test animation with negative angles."""
        anim = RotationAnimation(-90, 0, duration_ms=300)
        anim.start()
        anim.update(300)

        assert anim.get_current_angle() == 0

    def test_reverse_rotation(self):
        """Test rotation in reverse direction."""
        anim = RotationAnimation(90, 0, duration_ms=300)
        anim.start()
        anim.update(300)

        assert anim.get_current_angle() == 0


class TestRotationAnimationProgress:
    """Test animation progress."""

    def test_get_progress_initial(self):
        """Test progress at start."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()

        assert anim.get_progress() == 0.0

    def test_get_progress_halfway(self):
        """Test progress at halfway."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.update(150)

        assert anim.get_progress() == 0.5

    def test_get_progress_complete(self):
        """Test progress at completion."""
        anim = RotationAnimation(0, 90, duration_ms=300)
        anim.start()
        anim.update(300)

        assert anim.get_progress() == 1.0
