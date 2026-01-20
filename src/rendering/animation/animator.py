"""
Animator Base Module

This module provides the base Animator class for creating animations.

Classes:
    Animator: Abstract base class for all animations

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from abc import ABC, abstractmethod
import logging
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)


class Animator(ABC):
    """
    Abstract base class for all animations.

    Provides common functionality for animation timing, state management,
    and update logic.

    Attributes:
        duration_ms: Animation duration in milliseconds
        elapsed_ms: Elapsed time since animation start
        is_playing: Whether the animation is currently playing
        is_finished: Whether the animation has finished
        loop: Whether the animation should loop

    Example:
        >>> class MyAnimation(Animator):
        ...     def update_animation(self, progress):
        ...         # Update animation based on progress (0.0 to 1.0)
        ...         pass
        >>> anim = MyAnimation(duration_ms=300)
        >>> anim.start()
        >>> anim.update(16.67)  # Update with delta time
    """

    def __init__(self, duration_ms: float, loop: bool = False) -> None:
        """
        Initialize the animator.

        Args:
            duration_ms: Animation duration in milliseconds
            loop: Whether the animation should loop
        """
        self.duration_ms = duration_ms
        self.elapsed_ms = 0.0
        self.is_playing = False
        self.is_finished = False
        self.loop = loop

        logger.debug(f"{self.__class__.__name__} created: duration={duration_ms}ms, loop={loop}")

    def start(self) -> None:
        """
        Start the animation.

        Example:
            >>> anim.start()
        """
        self.is_playing = True
        self.is_finished = False
        self.elapsed_ms = 0.0
        logger.debug(f"{self.__class__.__name__} started")

    def stop(self) -> None:
        """
        Stop the animation.

        Example:
            >>> anim.stop()
        """
        self.is_playing = False
        logger.debug(f"{self.__class__.__name__} stopped")

    def reset(self) -> None:
        """
        Reset the animation to the beginning.

        Example:
            >>> anim.reset()
        """
        self.elapsed_ms = 0.0
        self.is_finished = False
        logger.debug(f"{self.__class__.__name__} reset")

    def update(self, delta_ms: float) -> None:
        """
        Update the animation with delta time.

        Args:
            delta_ms: Time elapsed since last update in milliseconds

        Example:
            >>> anim.update(16.67)  # ~60 FPS
        """
        if not self.is_playing or self.is_finished:
            return

        self.elapsed_ms += delta_ms

        if self.elapsed_ms >= self.duration_ms:
            if self.loop:
                # Loop the animation
                self.elapsed_ms = self.elapsed_ms % self.duration_ms
            else:
                # Animation finished
                self.elapsed_ms = self.duration_ms
                self.is_finished = True
                self.is_playing = False
                logger.debug(f"{self.__class__.__name__} finished")

        # Calculate progress (0.0 to 1.0)
        progress = min(self.elapsed_ms / self.duration_ms, 1.0)

        # Call subclass implementation
        self.update_animation(progress)

    @abstractmethod
    def update_animation(self, progress: float) -> None:
        """
        Update the animation based on progress.

        Args:
            progress: Animation progress from 0.0 to 1.0

        Note:
            This method must be implemented by subclasses.
        """
        pass

    def get_progress(self) -> float:
        """
        Get the current animation progress.

        Returns:
            Progress from 0.0 to 1.0

        Example:
            >>> progress = anim.get_progress()
            >>> print(f"Animation is {progress * 100:.1f}% complete")
        """
        if self.duration_ms == 0:
            return 1.0
        return min(self.elapsed_ms / self.duration_ms, 1.0)

    def set_loop(self, loop: bool) -> None:
        """
        Set whether the animation should loop.

        Args:
            loop: True to enable looping, False to disable

        Example:
            >>> anim.set_loop(True)
        """
        self.loop = loop
