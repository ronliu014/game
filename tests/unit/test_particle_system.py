"""
Unit tests for ParticleSystem

Tests particle creation, update, and rendering.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame
import math

from src.rendering.effects.particle_system import Particle, ParticleSystem


class TestParticleInit:
    """Test Particle initialization."""

    def test_init_basic(self):
        """Test basic particle initialization."""
        particle = Particle(100.0, 200.0, 50.0, -30.0, 1000.0, (255, 0, 0), 5.0)

        assert particle.x == 100.0
        assert particle.y == 200.0
        assert particle.vx == 50.0
        assert particle.vy == -30.0
        assert particle.lifetime == 1000.0
        assert particle.age == 0.0
        assert particle.color == (255, 0, 0)
        assert particle.size == 5.0
        assert particle.alpha == 255


class TestParticleUpdate:
    """Test particle updates."""

    def test_update_position(self):
        """Test particle position update."""
        particle = Particle(100.0, 100.0, 100.0, 50.0, 1000.0, (255, 0, 0), 5.0)

        # Update for 100ms (0.1 seconds)
        alive = particle.update(100.0)

        assert alive is True
        assert particle.x == 110.0  # 100 + 100*0.1
        assert particle.y == 105.0  # 100 + 50*0.1
        assert particle.age == 100.0

    def test_update_with_gravity(self):
        """Test particle update with gravity."""
        particle = Particle(100.0, 100.0, 0.0, 0.0, 1000.0, (255, 0, 0), 5.0)

        # Update with gravity (100 pixels/s^2) for 100ms
        alive = particle.update(100.0, gravity=100.0)

        assert alive is True
        assert particle.vy == 10.0  # 0 + 100*0.1

    def test_update_alpha_fade(self):
        """Test particle alpha fading."""
        particle = Particle(100.0, 100.0, 0.0, 0.0, 1000.0, (255, 0, 0), 5.0)

        # Update to halfway through lifetime
        particle.update(500.0)

        assert particle.alpha == 127  # 255 * (1 - 0.5)

    def test_update_expiration(self):
        """Test particle expiration."""
        particle = Particle(100.0, 100.0, 0.0, 0.0, 1000.0, (255, 0, 0), 5.0)

        # Update beyond lifetime
        alive = particle.update(1500.0)

        assert alive is False

    def test_update_multiple_steps(self):
        """Test multiple update steps."""
        particle = Particle(100.0, 100.0, 100.0, 0.0, 1000.0, (255, 0, 0), 5.0)

        # Update in multiple steps
        for _ in range(5):
            alive = particle.update(100.0)

        assert alive is True
        assert particle.x == 150.0  # 100 + 100*0.5
        assert particle.age == 500.0


class TestParticleDraw:
    """Test particle drawing."""

    @patch('pygame.Surface')
    @patch('pygame.draw.circle')
    def test_draw_basic(self, mock_draw_circle, mock_surface_class):
        """Test basic particle drawing."""
        particle = Particle(100.0, 100.0, 0.0, 0.0, 1000.0, (255, 0, 0), 5.0)
        surface = Mock()

        particle.draw(surface)

        # Should create temp surface and blit
        assert surface.blit.called

    @patch('pygame.Surface')
    def test_draw_zero_alpha(self, mock_surface_class):
        """Test drawing particle with zero alpha."""
        particle = Particle(100.0, 100.0, 0.0, 0.0, 1000.0, (255, 0, 0), 5.0)
        particle.alpha = 0
        surface = Mock()

        particle.draw(surface)

        # Should not draw anything
        surface.blit.assert_not_called()


class TestParticleSystemInit:
    """Test ParticleSystem initialization."""

    def test_init_default(self):
        """Test default initialization."""
        system = ParticleSystem()

        assert system.get_particle_count() == 0
        assert system.get_gravity() == 0.0

    def test_init_with_gravity(self):
        """Test initialization with gravity."""
        system = ParticleSystem(gravity=100.0)

        assert system.get_gravity() == 100.0


class TestParticleSystemEmitBurst:
    """Test burst emission."""

    def test_emit_burst_count(self):
        """Test burst emission creates correct number of particles."""
        system = ParticleSystem()

        system.emit_burst(100.0, 100.0, count=10)

        assert system.get_particle_count() == 10

    def test_emit_burst_position(self):
        """Test burst particles start at correct position."""
        system = ParticleSystem()

        system.emit_burst(150.0, 200.0, count=5)

        # All particles should start at emission point
        for particle in system._particles:
            assert particle.x == 150.0
            assert particle.y == 200.0

    def test_emit_burst_color(self):
        """Test burst particles have correct color."""
        system = ParticleSystem()
        color = (100, 150, 200)

        system.emit_burst(100.0, 100.0, count=5, color=color)

        for particle in system._particles:
            assert particle.color == color

    def test_emit_burst_multiple(self):
        """Test multiple burst emissions."""
        system = ParticleSystem()

        system.emit_burst(100.0, 100.0, count=5)
        system.emit_burst(200.0, 200.0, count=3)

        assert system.get_particle_count() == 8


class TestParticleSystemEmitFountain:
    """Test fountain emission."""

    def test_emit_fountain_count(self):
        """Test fountain emission creates correct number of particles."""
        system = ParticleSystem()

        system.emit_fountain(100.0, 100.0, count=15)

        assert system.get_particle_count() == 15

    def test_emit_fountain_upward(self):
        """Test fountain particles move upward."""
        system = ParticleSystem()

        system.emit_fountain(100.0, 100.0, count=10)

        # Most particles should have negative vy (upward)
        upward_count = sum(1 for p in system._particles if p.vy < 0)
        assert upward_count >= 8  # At least 80% should be upward


class TestParticleSystemEmitSparks:
    """Test spark emission."""

    def test_emit_sparks_count(self):
        """Test spark emission creates correct number of particles."""
        system = ParticleSystem()

        system.emit_sparks(100.0, 100.0, count=20)

        assert system.get_particle_count() == 20

    def test_emit_sparks_default_count(self):
        """Test spark emission with default count."""
        system = ParticleSystem()

        system.emit_sparks(100.0, 100.0)

        assert system.get_particle_count() == 20


class TestParticleSystemEmitVictory:
    """Test victory effect emission."""

    def test_emit_victory_effect(self):
        """Test victory effect creates particles."""
        system = ParticleSystem()

        system.emit_victory_effect(100.0, 100.0)

        # Should create 30 + 20 = 50 particles
        assert system.get_particle_count() == 50


class TestParticleSystemUpdate:
    """Test particle system updates."""

    def test_update_particles(self):
        """Test updating all particles."""
        system = ParticleSystem()
        system.emit_burst(100.0, 100.0, count=10)

        system.update(100.0)

        # All particles should have aged
        for particle in system._particles:
            assert particle.age == 100.0

    def test_update_removes_dead_particles(self):
        """Test that dead particles are removed."""
        system = ParticleSystem()
        system.emit_burst(100.0, 100.0, count=10,
                         lifetime_range=(100.0, 100.0))  # Very short lifetime

        # Update beyond lifetime
        system.update(200.0)

        assert system.get_particle_count() == 0

    def test_update_with_gravity(self):
        """Test updating particles with gravity."""
        system = ParticleSystem(gravity=100.0)
        system.emit_burst(100.0, 100.0, count=5)

        system.update(100.0)

        # All particles should have been affected by gravity
        for particle in system._particles:
            assert particle.vy != 0.0  # Velocity should have changed


class TestParticleSystemDraw:
    """Test particle system drawing."""

    @patch('pygame.draw.circle')
    @patch('pygame.Surface')
    def test_draw_all_particles(self, mock_surface_class, mock_draw_circle):
        """Test drawing all particles."""
        system = ParticleSystem()
        system.emit_burst(100.0, 100.0, count=5)
        surface = Mock()

        system.draw(surface)

        # Should attempt to draw all particles
        # (exact call count depends on implementation)
        assert surface.blit.call_count >= 5


class TestParticleSystemClear:
    """Test clearing particles."""

    def test_clear(self):
        """Test clearing all particles."""
        system = ParticleSystem()
        system.emit_burst(100.0, 100.0, count=10)

        system.clear()

        assert system.get_particle_count() == 0


class TestParticleSystemGravity:
    """Test gravity control."""

    def test_set_gravity(self):
        """Test setting gravity."""
        system = ParticleSystem()

        system.set_gravity(200.0)

        assert system.get_gravity() == 200.0

    def test_get_gravity(self):
        """Test getting gravity."""
        system = ParticleSystem(gravity=150.0)

        gravity = system.get_gravity()

        assert gravity == 150.0
