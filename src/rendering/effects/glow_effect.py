"""
Glow Effect

Provides glowing visual effects for terminals and other game elements.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
import math
from typing import Tuple, Optional
from src.utils.logger import GameLogger


class GlowEffect:
    """
    Glow effect for highlighting game elements.

    Creates pulsing glow effects with customizable color, intensity, and speed.

    Attributes:
        _color (Tuple[int, int, int]): Base RGB color
        _max_intensity (float): Maximum glow intensity (0.0 to 1.0)
        _pulse_speed (float): Pulse speed (cycles per second)
        _current_time (float): Current time in milliseconds
        _enabled (bool): Whether effect is enabled
        _logger (GameLogger): Logger instance
    """

    def __init__(self, color: Tuple[int, int, int] = (100, 200, 255),
                 max_intensity: float = 0.8, pulse_speed: float = 2.0):
        """
        Initialize the glow effect.

        Args:
            color: Base RGB color for the glow
            max_intensity: Maximum glow intensity (0.0 to 1.0)
            pulse_speed: Pulse speed in cycles per second
        """
        self._color: Tuple[int, int, int] = color
        self._max_intensity: float = max(0.0, min(1.0, max_intensity))
        self._pulse_speed: float = pulse_speed
        self._current_time: float = 0.0
        self._enabled: bool = True
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def update(self, delta_ms: float) -> None:
        """
        Update the glow effect animation.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if not self._enabled:
            return

        self._current_time += delta_ms

    def get_current_intensity(self) -> float:
        """
        Get current glow intensity based on pulse animation.

        Returns:
            float: Current intensity (0.0 to max_intensity)
        """
        if not self._enabled:
            return 0.0

        # Calculate pulse using sine wave
        time_seconds = self._current_time / 1000.0
        pulse = (math.sin(time_seconds * self._pulse_speed * 2 * math.pi) + 1.0) / 2.0

        return pulse * self._max_intensity

    def draw_glow(self, surface: pygame.Surface, x: int, y: int,
                  width: int, height: int, glow_radius: int = 10) -> None:
        """
        Draw a glowing rectangle.

        Args:
            surface: Pygame surface to draw on
            x: X position
            y: Y position
            width: Rectangle width
            height: Rectangle height
            glow_radius: Glow radius in pixels
        """
        if not self._enabled:
            return

        intensity = self.get_current_intensity()
        if intensity <= 0.0:
            return

        # Calculate glow color with intensity
        glow_color = tuple(int(c * intensity) for c in self._color)

        # Draw multiple layers for glow effect
        layers = 5
        for i in range(layers, 0, -1):
            layer_intensity = intensity * (i / layers)
            layer_color = tuple(int(c * layer_intensity) for c in self._color)
            layer_alpha = int(100 * layer_intensity)

            # Calculate layer size
            layer_offset = int(glow_radius * (layers - i + 1) / layers)

            # Create temporary surface for alpha blending
            temp_surface = pygame.Surface(
                (width + layer_offset * 2, height + layer_offset * 2),
                pygame.SRCALPHA
            )

            # Draw rounded rectangle with alpha
            color_with_alpha = (*layer_color, layer_alpha)
            pygame.draw.rect(
                temp_surface,
                color_with_alpha,
                (0, 0, width + layer_offset * 2, height + layer_offset * 2),
                border_radius=5
            )

            # Blit to main surface
            surface.blit(temp_surface, (x - layer_offset, y - layer_offset))

    def draw_glow_circle(self, surface: pygame.Surface, x: int, y: int,
                        radius: int, glow_radius: int = 10) -> None:
        """
        Draw a glowing circle.

        Args:
            surface: Pygame surface to draw on
            x: Center X position
            y: Center Y position
            radius: Circle radius
            glow_radius: Glow radius in pixels
        """
        if not self._enabled:
            return

        intensity = self.get_current_intensity()
        if intensity <= 0.0:
            return

        # Draw multiple layers for glow effect
        layers = 5
        for i in range(layers, 0, -1):
            layer_intensity = intensity * (i / layers)
            layer_color = tuple(int(c * layer_intensity) for c in self._color)
            layer_alpha = int(100 * layer_intensity)

            # Calculate layer radius
            layer_radius = radius + int(glow_radius * (layers - i + 1) / layers)

            # Create temporary surface for alpha blending
            size = layer_radius * 2 + 2
            temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)

            # Draw circle with alpha
            color_with_alpha = (*layer_color, layer_alpha)
            pygame.draw.circle(
                temp_surface,
                color_with_alpha,
                (layer_radius + 1, layer_radius + 1),
                layer_radius
            )

            # Blit to main surface
            surface.blit(temp_surface, (x - layer_radius - 1, y - layer_radius - 1))

    def draw_outline_glow(self, surface: pygame.Surface, x: int, y: int,
                         width: int, height: int, thickness: int = 3) -> None:
        """
        Draw a glowing outline around a rectangle.

        Args:
            surface: Pygame surface to draw on
            x: X position
            y: Y position
            width: Rectangle width
            height: Rectangle height
            thickness: Outline thickness
        """
        if not self._enabled:
            return

        intensity = self.get_current_intensity()
        if intensity <= 0.0:
            return

        # Calculate glow color with intensity
        glow_color = tuple(int(c * intensity) for c in self._color)
        alpha = int(255 * intensity)

        # Create temporary surface for alpha blending
        temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw outline with alpha
        color_with_alpha = (*glow_color, alpha)
        pygame.draw.rect(
            temp_surface,
            color_with_alpha,
            (0, 0, width, height),
            width=thickness,
            border_radius=3
        )

        # Blit to main surface
        surface.blit(temp_surface, (x, y))

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set the glow color.

        Args:
            color: RGB color tuple
        """
        self._color = color
        self._logger.debug(f"Glow color set to {color}")

    def get_color(self) -> Tuple[int, int, int]:
        """
        Get the current glow color.

        Returns:
            Tuple[int, int, int]: RGB color tuple
        """
        return self._color

    def set_max_intensity(self, intensity: float) -> None:
        """
        Set maximum glow intensity.

        Args:
            intensity: Maximum intensity (0.0 to 1.0)
        """
        self._max_intensity = max(0.0, min(1.0, intensity))
        self._logger.debug(f"Max intensity set to {self._max_intensity}")

    def get_max_intensity(self) -> float:
        """
        Get maximum glow intensity.

        Returns:
            float: Maximum intensity (0.0 to 1.0)
        """
        return self._max_intensity

    def set_pulse_speed(self, speed: float) -> None:
        """
        Set pulse speed.

        Args:
            speed: Pulse speed in cycles per second
        """
        self._pulse_speed = speed
        self._logger.debug(f"Pulse speed set to {speed}")

    def get_pulse_speed(self) -> float:
        """
        Get pulse speed.

        Returns:
            float: Pulse speed in cycles per second
        """
        return self._pulse_speed

    def enable(self) -> None:
        """Enable the glow effect."""
        self._enabled = True
        self._logger.debug("Glow effect enabled")

    def disable(self) -> None:
        """Disable the glow effect."""
        self._enabled = False
        self._logger.debug("Glow effect disabled")

    def is_enabled(self) -> bool:
        """
        Check if glow effect is enabled.

        Returns:
            bool: True if enabled, False otherwise
        """
        return self._enabled

    def reset(self) -> None:
        """Reset the glow effect animation."""
        self._current_time = 0.0
        self._logger.debug("Glow effect reset")
