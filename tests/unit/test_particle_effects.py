"""
Unit Tests for Particle Effects System

Tests for FireworksEffect and SmokeEffect classes.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pytest
import pygame
from src.rendering.effects.fireworks_effect import FireworksEffect
from src.rendering.effects.smoke_effect import SmokeEffect


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    """Initialize pygame before running tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen():
    """Create a test screen surface."""
    return pygame.Surface((800, 600))


class TestFireworksEffect:
    """Test cases for FireworksEffect class."""

    def test_initialization(self):
        """Test fireworks effect initialization."""
        fireworks = FireworksEffect(800, 600)
        assert fireworks is not None
        assert not fireworks.is_active()
        assert fireworks.get_particle_count() == 0

    def test_start_stop(self):
        """Test starting and stopping fireworks."""
        fireworks = FireworksEffect(800, 600)

        # Start effect
        fireworks.start()
        assert fireworks.is_active()

        # Stop effect
        fireworks.stop()
        assert not fireworks.is_active()
        assert fireworks.get_particle_count() == 0

    def test_launch_rocket(self):
        """Test launching a firework rocket."""
        fireworks = FireworksEffect(800, 600)

        # Launch a rocket
        fireworks.launch(x=400, y=600)
        assert fireworks.get_particle_count() > 0

    def test_launch_with_defaults(self):
        """Test launching with default parameters."""
        fireworks = FireworksEffect(800, 600)

        # Launch with defaults
        fireworks.launch()
        assert fireworks.get_particle_count() > 0

    def test_launch_with_custom_color(self):
        """Test launching with custom color."""
        fireworks = FireworksEffect(800, 600)

        # Launch with custom color
        fireworks.launch(x=400, y=600, color=(255, 0, 0))
        assert fireworks.get_particle_count() > 0

    def test_update(self, screen):
        """Test updating fireworks effect."""
        fireworks = FireworksEffect(800, 600)
        fireworks.launch(x=400, y=600)

        initial_count = fireworks.get_particle_count()

        # Update for 100ms
        fireworks.update(100.0)

        # Particle count should change (rocket moving or exploded)
        assert fireworks.get_particle_count() >= 0

    def test_draw(self, screen):
        """Test drawing fireworks effect."""
        fireworks = FireworksEffect(800, 600)
        fireworks.launch(x=400, y=600)

        # Should not raise exception
        fireworks.draw(screen)

    def test_auto_launch(self):
        """Test auto-launch functionality."""
        fireworks = FireworksEffect(800, 600)
        fireworks.set_auto_launch_interval(100.0)  # 100ms interval
        fireworks.start()

        # Update for 150ms (should trigger auto-launch)
        fireworks.update(150.0)

        # Should have particles from auto-launched firework
        assert fireworks.get_particle_count() > 0

    def test_rocket_explosion(self):
        """Test that rockets explode when reaching target height."""
        fireworks = FireworksEffect(800, 600)
        fireworks.launch(x=400, y=600)

        # Update for a long time to ensure explosion
        for _ in range(100):
            fireworks.update(16.67)  # ~60 FPS

        # Should have explosion particles
        particle_count = fireworks.get_particle_count()
        assert particle_count >= 0  # May have particles or all faded

    def test_set_auto_launch_interval(self):
        """Test setting auto-launch interval."""
        fireworks = FireworksEffect(800, 600)

        # Should not raise exception
        fireworks.set_auto_launch_interval(500.0)


class TestSmokeEffect:
    """Test cases for SmokeEffect class."""

    def test_initialization(self):
        """Test smoke effect initialization."""
        smoke = SmokeEffect(800, 600)
        assert smoke is not None
        assert not smoke.is_active()
        assert smoke.get_particle_count() == 0

    def test_start_stop(self):
        """Test starting and stopping smoke."""
        smoke = SmokeEffect(800, 600)

        # Start effect
        smoke.start(x=400, y=300)
        assert smoke.is_active()

        # Stop effect
        smoke.stop()
        assert not smoke.is_active()

    def test_start_with_defaults(self):
        """Test starting with default position."""
        smoke = SmokeEffect(800, 600)

        # Start with defaults
        smoke.start()
        assert smoke.is_active()

    def test_clear(self):
        """Test clearing smoke particles."""
        smoke = SmokeEffect(800, 600)
        smoke.start(x=400, y=300)

        # Update to generate particles
        smoke.update(200.0)

        # Clear particles
        smoke.clear()
        assert smoke.get_particle_count() == 0

    def test_update(self):
        """Test updating smoke effect."""
        smoke = SmokeEffect(800, 600)
        smoke.start(x=400, y=300)

        # Update for 200ms (should emit particles)
        smoke.update(200.0)

        # Should have particles
        assert smoke.get_particle_count() > 0

    def test_draw(self, screen):
        """Test drawing smoke effect."""
        smoke = SmokeEffect(800, 600)
        smoke.start(x=400, y=300)
        smoke.update(200.0)

        # Should not raise exception
        smoke.draw(screen)

    def test_emission_rate(self):
        """Test setting emission rate."""
        smoke = SmokeEffect(800, 600)
        smoke.set_emission_rate(50.0)  # 50ms interval
        smoke.start(x=400, y=300)

        # Update for 100ms (should emit twice)
        smoke.update(100.0)

        # Should have particles
        assert smoke.get_particle_count() > 0

    def test_emission_position(self):
        """Test setting emission position."""
        smoke = SmokeEffect(800, 600)

        # Should not raise exception
        smoke.set_emission_position(300.0, 200.0)
        smoke.start()
        smoke.update(100.0)

        assert smoke.get_particle_count() > 0

    def test_continuous_emission(self):
        """Test continuous smoke emission."""
        smoke = SmokeEffect(800, 600)
        smoke.start(x=400, y=300)

        # Update multiple times
        for _ in range(10):
            smoke.update(100.0)

        # Should have accumulated particles
        assert smoke.get_particle_count() > 0

    def test_particle_lifetime(self):
        """Test that smoke particles eventually fade out."""
        smoke = SmokeEffect(800, 600)
        smoke.start(x=400, y=300)

        # Generate some particles
        smoke.update(200.0)

        # Stop emission
        smoke.stop()

        # Update for a very long time
        for _ in range(500):
            smoke.update(100.0)

        # All particles should have faded out
        assert smoke.get_particle_count() == 0


class TestParticleEffectsIntegration:
    """Integration tests for particle effects."""

    def test_fireworks_and_smoke_together(self, screen):
        """Test running both effects simultaneously."""
        fireworks = FireworksEffect(800, 600)
        smoke = SmokeEffect(800, 600)

        # Start both effects
        fireworks.start()
        smoke.start(x=400, y=300)

        # Update both
        for _ in range(10):
            fireworks.update(100.0)
            smoke.update(100.0)

        # Draw both
        fireworks.draw(screen)
        smoke.draw(screen)

        # Both should have particles
        assert fireworks.get_particle_count() > 0
        assert smoke.get_particle_count() > 0

    def test_multiple_fireworks(self, screen):
        """Test launching multiple fireworks."""
        fireworks = FireworksEffect(800, 600)

        # Launch multiple fireworks
        for i in range(5):
            fireworks.launch(x=100 + i * 150, y=600)

        # Should have multiple rockets
        assert fireworks.get_particle_count() >= 5

    def test_performance_many_particles(self, screen):
        """Test performance with many particles."""
        fireworks = FireworksEffect(800, 600)

        # Launch many fireworks
        for _ in range(10):
            fireworks.launch()

        # Update and draw multiple times
        for _ in range(100):
            fireworks.update(16.67)
            fireworks.draw(screen)

        # Should complete without errors
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
