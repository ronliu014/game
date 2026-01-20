"""
Particle System

Manages particle effects for visual feedback (victory effects, sparks, etc.).

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
import random
import math
from typing import List, Tuple, Optional
from src.utils.logger import GameLogger


class Particle:
    """
    Individual particle in the particle system.

    Attributes:
        x (float): X position
        y (float): Y position
        vx (float): X velocity
        vy (float): Y velocity
        lifetime (float): Total lifetime in milliseconds
        age (float): Current age in milliseconds
        color (Tuple[int, int, int]): RGB color
        size (float): Particle size
        alpha (int): Transparency (0-255)
    """

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 lifetime: float, color: Tuple[int, int, int], size: float):
        """
        Initialize a particle.

        Args:
            x: Initial X position
            y: Initial Y position
            vx: X velocity (pixels per second)
            vy: Y velocity (pixels per second)
            lifetime: Particle lifetime in milliseconds
            color: RGB color tuple
            size: Particle size in pixels
        """
        self.x: float = x
        self.y: float = y
        self.vx: float = vx
        self.vy: float = vy
        self.lifetime: float = lifetime
        self.age: float = 0.0
        self.color: Tuple[int, int, int] = color
        self.size: float = size
        self.alpha: int = 255

    def update(self, delta_ms: float, gravity: float = 0.0) -> bool:
        """
        Update particle state.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
            gravity: Gravity acceleration (pixels per second squared)

        Returns:
            bool: True if particle is still alive, False if expired
        """
        # Update age
        self.age += delta_ms

        # Check if expired
        if self.age >= self.lifetime:
            return False

        # Update position
        delta_s = delta_ms / 1000.0
        self.x += self.vx * delta_s
        self.y += self.vy * delta_s

        # Apply gravity
        if gravity != 0.0:
            self.vy += gravity * delta_s

        # Update alpha based on age (fade out)
        life_ratio = self.age / self.lifetime
        self.alpha = int(255 * (1.0 - life_ratio))

        return True

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the particle.

        Args:
            surface: Pygame surface to draw on
        """
        if self.alpha <= 0:
            return

        # Create color with alpha
        color_with_alpha = (*self.color, self.alpha)

        # Draw particle as a circle
        try:
            # Create a temporary surface for alpha blending
            temp_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color_with_alpha,
                             (int(self.size), int(self.size)), int(self.size))
            surface.blit(temp_surface, (int(self.x - self.size), int(self.y - self.size)))
        except (ValueError, TypeError):
            # Fallback to simple circle without alpha
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))


class ParticleSystem:
    """
    Particle system for creating visual effects.

    Manages creation, update, and rendering of particles.

    Attributes:
        _particles (List[Particle]): Active particles
        _gravity (float): Gravity acceleration
        _logger (GameLogger): Logger instance
    """

    def __init__(self, gravity: float = 0.0):
        """
        Initialize the particle system.

        Args:
            gravity: Gravity acceleration (pixels per second squared)
        """
        self._particles: List[Particle] = []
        self._gravity: float = gravity
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def emit_burst(self, x: float, y: float, count: int,
                   speed_range: Tuple[float, float] = (50.0, 150.0),
                   lifetime_range: Tuple[float, float] = (500.0, 1500.0),
                   color: Tuple[int, int, int] = (255, 200, 0),
                   size_range: Tuple[float, float] = (2.0, 5.0)) -> None:
        """
        Emit a burst of particles from a point.

        Args:
            x: X position
            y: Y position
            count: Number of particles to emit
            speed_range: Min and max speed (pixels per second)
            lifetime_range: Min and max lifetime (milliseconds)
            color: RGB color tuple
            size_range: Min and max particle size
        """
        for _ in range(count):
            # Random angle
            angle = random.uniform(0, 2 * math.pi)

            # Random speed
            speed = random.uniform(*speed_range)

            # Calculate velocity
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # Random lifetime
            lifetime = random.uniform(*lifetime_range)

            # Random size
            size = random.uniform(*size_range)

            # Create particle
            particle = Particle(x, y, vx, vy, lifetime, color, size)
            self._particles.append(particle)

        self._logger.debug(f"Emitted {count} particles at ({x}, {y})")

    def emit_fountain(self, x: float, y: float, count: int,
                     angle_range: Tuple[float, float] = (-math.pi/4, -3*math.pi/4),
                     speed_range: Tuple[float, float] = (100.0, 200.0),
                     lifetime_range: Tuple[float, float] = (800.0, 1500.0),
                     color: Tuple[int, int, int] = (100, 200, 255),
                     size_range: Tuple[float, float] = (2.0, 4.0)) -> None:
        """
        Emit particles in a fountain pattern (upward spray).

        Args:
            x: X position
            y: Y position
            count: Number of particles to emit
            angle_range: Min and max angle in radians (default: upward spray)
            speed_range: Min and max speed (pixels per second)
            lifetime_range: Min and max lifetime (milliseconds)
            color: RGB color tuple
            size_range: Min and max particle size
        """
        for _ in range(count):
            # Random angle within range
            angle = random.uniform(*angle_range)

            # Random speed
            speed = random.uniform(*speed_range)

            # Calculate velocity
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # Random lifetime
            lifetime = random.uniform(*lifetime_range)

            # Random size
            size = random.uniform(*size_range)

            # Create particle
            particle = Particle(x, y, vx, vy, lifetime, color, size)
            self._particles.append(particle)

        self._logger.debug(f"Emitted fountain of {count} particles at ({x}, {y})")

    def emit_sparks(self, x: float, y: float, count: int = 20,
                   color: Tuple[int, int, int] = (255, 220, 100)) -> None:
        """
        Emit spark particles (fast, short-lived).

        Args:
            x: X position
            y: Y position
            count: Number of sparks
            color: RGB color tuple (default: golden yellow)
        """
        self.emit_burst(
            x, y, count,
            speed_range=(200.0, 400.0),
            lifetime_range=(200.0, 500.0),
            color=color,
            size_range=(1.0, 3.0)
        )

    def emit_victory_effect(self, x: float, y: float) -> None:
        """
        Emit a victory celebration effect.

        Args:
            x: X position
            y: Y position
        """
        # Golden burst
        self.emit_burst(
            x, y, 30,
            speed_range=(100.0, 250.0),
            lifetime_range=(1000.0, 2000.0),
            color=(255, 215, 0),  # Gold
            size_range=(3.0, 6.0)
        )

        # Blue sparkles
        self.emit_burst(
            x, y, 20,
            speed_range=(150.0, 300.0),
            lifetime_range=(800.0, 1500.0),
            color=(100, 200, 255),  # Light blue
            size_range=(2.0, 4.0)
        )

        self._logger.info(f"Victory effect emitted at ({x}, {y})")

    def update(self, delta_ms: float) -> None:
        """
        Update all particles.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Update particles and remove dead ones
        self._particles = [p for p in self._particles if p.update(delta_ms, self._gravity)]

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw all particles.

        Args:
            surface: Pygame surface to draw on
        """
        for particle in self._particles:
            particle.draw(surface)

    def clear(self) -> None:
        """Clear all particles."""
        self._particles.clear()
        self._logger.debug("All particles cleared")

    def get_particle_count(self) -> int:
        """
        Get the number of active particles.

        Returns:
            int: Number of active particles
        """
        return len(self._particles)

    def set_gravity(self, gravity: float) -> None:
        """
        Set gravity acceleration.

        Args:
            gravity: Gravity acceleration (pixels per second squared)
        """
        self._gravity = gravity
        self._logger.debug(f"Gravity set to {gravity}")

    def get_gravity(self) -> float:
        """
        Get current gravity acceleration.

        Returns:
            float: Gravity acceleration
        """
        return self._gravity
