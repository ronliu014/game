"""
Fireworks Effect

Provides fireworks particle effects for victory celebrations.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
import random
import math
from typing import List, Tuple
from src.rendering.effects.particle_system import ParticleSystem
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class FireworksEffect:
    """
    Fireworks effect for victory celebrations.

    Creates colorful fireworks explosions with multiple stages:
    - Launch phase: Rocket shoots upward
    - Explosion phase: Burst of colorful particles
    - Fade phase: Particles fall with gravity

    Example:
        >>> fireworks = FireworksEffect(screen_width=800, screen_height=600)
        >>> fireworks.launch(x=400, y=600)  # Launch from bottom center
        >>> fireworks.update(16.67)  # Update at 60 FPS
        >>> fireworks.draw(screen)
    """

    # Fireworks colors (vibrant celebration colors)
    COLORS = [
        (255, 50, 50),    # Red
        (50, 255, 50),    # Green
        (50, 50, 255),    # Blue
        (255, 255, 50),   # Yellow
        (255, 50, 255),   # Magenta
        (50, 255, 255),   # Cyan
        (255, 150, 50),   # Orange
        (150, 50, 255),   # Purple
        (255, 215, 0),    # Gold
        (255, 255, 255),  # White
    ]

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """
        Initialize the fireworks effect.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._particle_system = ParticleSystem(gravity=200.0)  # Gravity for falling particles
        self._rockets: List[dict] = []  # Active rockets
        self._auto_launch_timer = 0.0
        self._auto_launch_interval = 800.0  # Launch new firework every 800ms
        self._is_active = False

        logger.debug("FireworksEffect initialized")

    def start(self) -> None:
        """Start the fireworks effect."""
        self._is_active = True
        self._auto_launch_timer = 0.0
        logger.info("Fireworks effect started")

    def stop(self) -> None:
        """Stop the fireworks effect."""
        self._is_active = False
        self._rockets.clear()
        self._particle_system.clear()
        logger.info("Fireworks effect stopped")

    def launch(self, x: float = None, y: float = None, color: Tuple[int, int, int] = None) -> None:
        """
        Launch a firework rocket.

        Args:
            x: Launch X position (default: random horizontal position)
            y: Launch Y position (default: bottom of screen)
            color: Firework color (default: random from COLORS)
        """
        if x is None:
            # Random horizontal position (avoid edges)
            x = random.uniform(self._screen_width * 0.2, self._screen_width * 0.8)

        if y is None:
            # Launch from bottom
            y = self._screen_height

        if color is None:
            # Random color
            color = random.choice(self.COLORS)

        # Random explosion height (upper half of screen)
        explosion_y = random.uniform(self._screen_height * 0.2, self._screen_height * 0.5)

        # Calculate launch velocity to reach explosion height
        # Using physics: v = sqrt(2 * g * h)
        height_diff = y - explosion_y
        launch_speed = math.sqrt(2 * self._particle_system.get_gravity() * height_diff)

        rocket = {
            'x': x,
            'y': y,
            'vy': -launch_speed,  # Negative for upward
            'explosion_y': explosion_y,
            'color': color,
            'exploded': False
        }

        self._rockets.append(rocket)
        logger.debug(f"Firework launched at ({x:.1f}, {y:.1f}) targeting ({x:.1f}, {explosion_y:.1f})")

    def _explode_rocket(self, rocket: dict) -> None:
        """
        Explode a rocket into particles.

        Args:
            rocket: Rocket dictionary
        """
        x = rocket['x']
        y = rocket['y']
        color = rocket['color']

        # Main explosion burst
        particle_count = random.randint(40, 60)
        self._particle_system.emit_burst(
            x, y,
            count=particle_count,
            speed_range=(100.0, 300.0),
            lifetime_range=(1000.0, 2000.0),
            color=color,
            size_range=(2.0, 5.0)
        )

        # Secondary sparkles (white/gold)
        sparkle_count = random.randint(15, 25)
        sparkle_color = (255, 255, 200) if random.random() > 0.5 else (255, 215, 0)
        self._particle_system.emit_burst(
            x, y,
            count=sparkle_count,
            speed_range=(150.0, 250.0),
            lifetime_range=(800.0, 1500.0),
            color=sparkle_color,
            size_range=(1.0, 3.0)
        )

        rocket['exploded'] = True
        logger.debug(f"Firework exploded at ({x:.1f}, {y:.1f}) with {particle_count + sparkle_count} particles")

    def update(self, delta_ms: float) -> None:
        """
        Update the fireworks effect.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if not self._is_active:
            return

        # Auto-launch new fireworks
        self._auto_launch_timer += delta_ms
        if self._auto_launch_timer >= self._auto_launch_interval:
            self._auto_launch_timer = 0.0
            self.launch()

        # Update rockets
        delta_s = delta_ms / 1000.0
        for rocket in self._rockets[:]:
            if rocket['exploded']:
                continue

            # Update rocket position
            rocket['y'] += rocket['vy'] * delta_s
            rocket['vy'] += self._particle_system.get_gravity() * delta_s

            # Check if reached explosion height
            if rocket['y'] <= rocket['explosion_y']:
                self._explode_rocket(rocket)

        # Remove exploded rockets
        self._rockets = [r for r in self._rockets if not r['exploded']]

        # Update particle system
        self._particle_system.update(delta_ms)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the fireworks effect.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw rockets (small trails)
        for rocket in self._rockets:
            if not rocket['exploded']:
                x = int(rocket['x'])
                y = int(rocket['y'])
                color = rocket['color']

                # Draw rocket as a small circle with trail
                pygame.draw.circle(surface, color, (x, y), 3)

                # Draw trail (3 small circles behind)
                for i in range(1, 4):
                    trail_y = y + i * 5
                    trail_alpha = 255 - i * 60
                    if trail_alpha > 0:
                        trail_color = (*color, trail_alpha)
                        try:
                            temp_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                            pygame.draw.circle(temp_surface, trail_color, (3, 3), 2)
                            surface.blit(temp_surface, (x - 3, trail_y - 3))
                        except (ValueError, TypeError):
                            pygame.draw.circle(surface, color, (x, trail_y), 2)

        # Draw particles
        self._particle_system.draw(surface)

    def is_active(self) -> bool:
        """
        Check if the effect is active.

        Returns:
            bool: True if active, False otherwise
        """
        return self._is_active

    def get_particle_count(self) -> int:
        """
        Get the number of active particles.

        Returns:
            int: Number of active particles
        """
        return self._particle_system.get_particle_count() + len(self._rockets)

    def set_auto_launch_interval(self, interval_ms: float) -> None:
        """
        Set the auto-launch interval.

        Args:
            interval_ms: Interval in milliseconds between launches
        """
        self._auto_launch_interval = interval_ms
        logger.debug(f"Auto-launch interval set to {interval_ms}ms")
