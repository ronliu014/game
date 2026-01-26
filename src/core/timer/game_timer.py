"""
Game Timer

Provides countdown timer functionality for game levels.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Callable
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class GameTimer:
    """
    Countdown timer for game levels.

    Tracks remaining time and detects timeout conditions.

    Features:
        - Countdown from specified time limit
        - Pause/resume support
        - Timeout detection
        - Time formatting (MM:SS)
        - Warning thresholds for UI feedback

    Example:
        >>> timer = GameTimer(time_limit=60.0)
        >>> timer.start()
        >>> timer.update(16.67)  # Update with delta time in ms
        >>> print(timer.get_remaining_time())  # 59.98
        >>> print(timer.format_time())  # "00:59"
        >>> if timer.is_timeout():
        ...     print("Time's up!")
    """

    # Warning thresholds (seconds)
    WARNING_THRESHOLD = 10.0  # Show warning when < 10s
    CRITICAL_THRESHOLD = 5.0  # Show critical warning when < 5s

    def __init__(self, time_limit: float):
        """
        Initialize the game timer.

        Args:
            time_limit: Time limit in seconds
        """
        self._time_limit = time_limit
        self._remaining_time = time_limit
        self._is_running = False
        self._is_paused = False
        self._timeout_callback: Optional[Callable[[], None]] = None

        logger.debug(f"GameTimer initialized with {time_limit}s limit")

    def start(self) -> None:
        """Start the timer."""
        self._is_running = True
        self._is_paused = False
        self._remaining_time = self._time_limit
        logger.info(f"Timer started: {self._time_limit}s")

    def stop(self) -> None:
        """Stop the timer."""
        self._is_running = False
        self._is_paused = False
        logger.info("Timer stopped")

    def pause(self) -> None:
        """Pause the timer."""
        if self._is_running and not self._is_paused:
            self._is_paused = True
            logger.debug("Timer paused")

    def resume(self) -> None:
        """Resume the timer."""
        if self._is_running and self._is_paused:
            self._is_paused = False
            logger.debug("Timer resumed")

    def reset(self) -> None:
        """Reset the timer to initial time limit."""
        self._remaining_time = self._time_limit
        self._is_running = False
        self._is_paused = False
        logger.debug("Timer reset")

    def update(self, delta_ms: float) -> None:
        """
        Update the timer.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if not self._is_running or self._is_paused:
            return

        # Convert ms to seconds
        delta_s = delta_ms / 1000.0

        # Update remaining time
        self._remaining_time -= delta_s

        # Check for timeout
        if self._remaining_time <= 0:
            self._remaining_time = 0
            self._is_running = False

            # Call timeout callback if set
            if self._timeout_callback:
                self._timeout_callback()

            logger.info("Timer timeout!")

    def get_remaining_time(self) -> float:
        """
        Get remaining time in seconds.

        Returns:
            float: Remaining time in seconds
        """
        return max(0.0, self._remaining_time)

    def get_elapsed_time(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            float: Elapsed time in seconds
        """
        return self._time_limit - self._remaining_time

    def get_time_limit(self) -> float:
        """
        Get the time limit.

        Returns:
            float: Time limit in seconds
        """
        return self._time_limit

    def get_progress(self) -> float:
        """
        Get timer progress (0.0 to 1.0).

        Returns:
            float: Progress ratio (0.0 = start, 1.0 = timeout)
        """
        if self._time_limit <= 0:
            return 1.0
        return 1.0 - (self._remaining_time / self._time_limit)

    def is_timeout(self) -> bool:
        """
        Check if timer has timed out.

        Returns:
            bool: True if timed out, False otherwise
        """
        return self._remaining_time <= 0

    def is_running(self) -> bool:
        """
        Check if timer is running.

        Returns:
            bool: True if running, False otherwise
        """
        return self._is_running and not self._is_paused

    def is_paused(self) -> bool:
        """
        Check if timer is paused.

        Returns:
            bool: True if paused, False otherwise
        """
        return self._is_paused

    def is_warning(self) -> bool:
        """
        Check if timer is in warning state (< 10s remaining).

        Returns:
            bool: True if in warning state, False otherwise
        """
        return 0 < self._remaining_time <= self.WARNING_THRESHOLD

    def is_critical(self) -> bool:
        """
        Check if timer is in critical state (< 5s remaining).

        Returns:
            bool: True if in critical state, False otherwise
        """
        return 0 < self._remaining_time <= self.CRITICAL_THRESHOLD

    def format_time(self, show_milliseconds: bool = False) -> str:
        """
        Format remaining time as string.

        Args:
            show_milliseconds: Whether to show milliseconds

        Returns:
            str: Formatted time string (e.g., "01:23" or "01:23.45")
        """
        remaining = max(0.0, self._remaining_time)

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        if show_milliseconds:
            milliseconds = int((remaining % 1) * 100)
            return f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def set_timeout_callback(self, callback: Callable[[], None]) -> None:
        """
        Set callback function to be called on timeout.

        Args:
            callback: Function to call when timer times out
        """
        self._timeout_callback = callback
        logger.debug("Timeout callback set")

    def add_time(self, seconds: float) -> None:
        """
        Add time to the timer (bonus time).

        Args:
            seconds: Seconds to add
        """
        self._remaining_time += seconds
        logger.debug(f"Added {seconds}s to timer")

    def subtract_time(self, seconds: float) -> None:
        """
        Subtract time from the timer (penalty).

        Args:
            seconds: Seconds to subtract
        """
        self._remaining_time = max(0.0, self._remaining_time - seconds)
        logger.debug(f"Subtracted {seconds}s from timer")

    def get_color_hint(self) -> tuple:
        """
        Get color hint based on remaining time.

        Returns:
            tuple: RGB color tuple for UI display
                - Green (0, 255, 0) when > 10s
                - Yellow (255, 255, 0) when 5-10s
                - Red (255, 0, 0) when < 5s
        """
        if self.is_critical():
            return (255, 0, 0)  # Red
        elif self.is_warning():
            return (255, 255, 0)  # Yellow
        else:
            return (0, 255, 0)  # Green

    def __repr__(self) -> str:
        """String representation of the timer."""
        status = "running" if self._is_running else "stopped"
        if self._is_paused:
            status = "paused"
        return f"GameTimer({self.format_time()}, {status})"
