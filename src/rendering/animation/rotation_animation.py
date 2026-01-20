"""
Rotation Animation Module

This module provides the RotationAnimation class for animating tile rotations.

Classes:
    RotationAnimation: Animation for rotating tiles with easing

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import Callable, Optional

from src.rendering.animation.animator import Animator
from src.utils.math_utils import ease_in_out

# Configure logger
logger = logging.getLogger(__name__)


class RotationAnimation(Animator):
    """
    Animation for rotating tiles with easing.

    Animates rotation from a start angle to an end angle with smooth easing.

    Attributes:
        start_angle: Starting rotation angle in degrees
        end_angle: Ending rotation angle in degrees
        current_angle: Current rotation angle
        easing_func: Easing function to use
        on_complete: Callback function called when animation completes

    Example:
        >>> def on_complete():
        ...     print("Rotation complete!")
        >>> anim = RotationAnimation(0, 90, duration_ms=300, on_complete=on_complete)
        >>> anim.start()
        >>> while anim.is_playing:
        ...     anim.update(16.67)
        ...     print(f"Current angle: {anim.get_current_angle()}")
    """

    def __init__(
        self,
        start_angle: float,
        end_angle: float,
        duration_ms: float = 300,
        easing_func: Optional[Callable[[float], float]] = None,
        on_complete: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Initialize the rotation animation.

        Args:
            start_angle: Starting rotation angle in degrees
            end_angle: Ending rotation angle in degrees
            duration_ms: Animation duration in milliseconds
            easing_func: Easing function (uses ease_in_out if None)
            on_complete: Callback function for completion
        """
        super().__init__(duration_ms, loop=False)

        self.start_angle = start_angle
        self.end_angle = end_angle
        self.current_angle = start_angle
        self.easing_func = easing_func or ease_in_out
        self.on_complete = on_complete

        logger.debug(
            f"RotationAnimation created: {start_angle}° -> {end_angle}° "
            f"over {duration_ms}ms"
        )

    def update_animation(self, progress: float) -> None:
        """
        Update the rotation based on progress.

        Args:
            progress: Animation progress from 0.0 to 1.0
        """
        # Apply easing function
        eased_progress = self.easing_func(progress)

        # Calculate current angle
        angle_delta = self.end_angle - self.start_angle
        self.current_angle = self.start_angle + angle_delta * eased_progress

        # Call completion callback if finished
        if self.is_finished and self.on_complete:
            self.on_complete()
            # Clear callback to prevent multiple calls
            self.on_complete = None

    def get_current_angle(self) -> float:
        """
        Get the current rotation angle.

        Returns:
            Current angle in degrees

        Example:
            >>> angle = anim.get_current_angle()
        """
        return self.current_angle

    def set_angles(self, start_angle: float, end_angle: float) -> None:
        """
        Set new start and end angles.

        Args:
            start_angle: New starting angle
            end_angle: New ending angle

        Example:
            >>> anim.set_angles(90, 180)
            >>> anim.start()
        """
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.current_angle = start_angle
        logger.debug(f"Rotation angles set: {start_angle}° -> {end_angle}°")
