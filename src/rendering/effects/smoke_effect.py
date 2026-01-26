"""
Smoke Effect

Provides smoke particle effects for failure/disappointment scenes.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
import random
import math
from typing import Tuple
from src.rendering.effects.particle_system import ParticleSystem
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class SmokeEffect:
    """
    Smoke effect for failure/disappointment scenes.

    Creates rising smoke particles that drift upward and disperse:
    - Dark gray smoke particles
    - Upward drift with horizontal dispersion
    - Gradual fade out
    - Slight expansion as particles age

    Example:
        >>> smoke = SmokeEffect(screen_width=800, screen_height=600)
        >>> smoke.start(x=400, y=300)  # Start smoke at center
        >>> smoke.update(16.67)  # Update at 60 FPS
        >>> smoke.draw(screen)
    """

    # Smoke colors (dark gray to light gray)
    SMOKE_COLORS = [
        (60, 60, 60),     # Dark gray
        (80, 80, 80),     # Medium-dark gray
        (100, 100, 100),  # Medium gray
        (120, 120, 120),  # Medium-light gray
    ]

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """
        Initialize the smoke effect.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._particle_system = ParticleSystem(gravity=-50.0)  # Negative gravity for upward drift
        self._emission_timer = 0.0
        self._emission_interval = 100.0  # Emit smoke every 100ms
        self._is_active = False
        self._emission_x = screen_width // 2
        self._emission_y = screen_height // 2

        logger.debug("SmokeEffect initialized")

    def start(self, x: float = None, y: float = None) -> None:
        """
        Start the smoke effect.

        Args:
            x: Emission X position (default: center)
            y: Emission Y position (default: center)
        """
        self._is_active = True
        self._emission_timer = 0.0

        if x is not None:
            self._emission_x = x
        if y is not None:
            self._emission_y = y

        logger.info(f"Smoke effect started at ({self._emission_x:.1f}, {self._emission_y:.1f})")

    def stop(self) -> None:
        """Stop the smoke effect (particles will continue to fade out)."""
        self._is_active = False
        logger.info("Smoke effect stopped")

    def clear(self) -> None:
        """Clear all smoke particles immediately."""
        self._particle_system.clear()
        logger.debug("Smoke particles cleared")

    def _emit_smoke_puff(self) -> None:
        """Emit a puff of smoke particles."""
        # Random color from smoke palette
        color = random.choice(self.SMOKE_COLORS)

        # Emit particles with upward and outward motion
        particle_count = random.randint(3, 6)

        for _ in range(particle_count):
            # Random horizontal spread
            angle = random.uniform(-math.pi/3, -2*math.pi/3)  # Upward cone
            speed = random.uniform(20.0, 60.0)

            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # Add horizontal drift
            vx += random.uniform(-30.0, 30.0)

            # Random lifetime (longer than fireworks)
            lifetime = random.uniform(2000.0, 4000.0)

            # Random size (larger than fireworks)
            size = random.uniform(4.0, 8.0)

            # Create particle manually to add to system
            from src.rendering.effects.particle_system import Particle
            particle = Particle(
                self._emission_x + random.uniform(-10, 10),  # Slight position variation
                self._emission_y + random.uniform(-10, 10),
                vx, vy,
                lifetime,
                color,
                size
            )
            self._particle_system._particles.append(particle)

        logger.debug(f"Emitted smoke puff with {particle_count} particles")

    def update(self, delta_ms: float) -> None:
        """
        Update the smoke effect.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Emit new smoke if active
        if self._is_active:
            self._emission_timer += delta_ms
            if self._emission_timer >= self._emission_interval:
                self._emission_timer = 0.0
                self._emit_smoke_puff()

        # Update particle system
        self._particle_system.update(delta_ms)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the smoke effect.

        Args:
            surface: Pygame surface to draw on
        """
        self._particle_system.draw(surface)

    def is_active(self) -> bool:
        """
        Check if the effect is actively emitting.

        Returns:
            bool: True if actively emitting, False otherwise
        """
        return self._is_active

    def get_particle_count(self) -> int:
        """
        Get the number of active smoke particles.

        Returns:
            int: Number of active particles
        """
        return self._particle_system.get_particle_count()

    def set_emission_rate(self, interval_ms: float) -> None:
        """
        Set the smoke emission rate.

        Args:
            interval_ms: Interval in milliseconds between emissions
        """
        self._emission_interval = interval_ms
        logger.debug(f"Emission interval set to {interval_ms}ms")

    def set_emission_position(self, x: float, y: float) -> None:
        """
        Set the smoke emission position.

        Args:
            x: X position
            y: Y position
        """
        self._emission_x = x
        self._emission_y = y
        logger.debug(f"Emission position set to ({x:.1f}, {y:.1f})")
