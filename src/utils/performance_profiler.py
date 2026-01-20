"""
Performance Profiler

Utility for profiling game performance and identifying bottlenecks.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import time
import psutil
import os
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from src.utils.logger import GameLogger


@dataclass
class PerformanceMetrics:
    """
    Performance metrics data.

    Attributes:
        fps: Frames per second
        frame_time_ms: Frame time in milliseconds
        memory_mb: Memory usage in megabytes
        cpu_percent: CPU usage percentage
    """
    fps: float
    frame_time_ms: float
    memory_mb: float
    cpu_percent: float


class PerformanceProfiler:
    """
    Performance profiler for monitoring game performance.

    Tracks FPS, frame time, memory usage, and CPU usage.
    Provides profiling for specific code sections.

    Attributes:
        _frame_times (List[float]): Recent frame times
        _max_samples (int): Maximum number of samples to keep
        _process: psutil Process for current process
        _logger (GameLogger): Logger instance
    """

    def __init__(self, max_samples: int = 60):
        """
        Initialize the performance profiler.

        Args:
            max_samples: Maximum number of frame time samples to keep
        """
        self._frame_times: List[float] = []
        self._max_samples: int = max_samples
        self._process = psutil.Process(os.getpid())
        self._logger: GameLogger = GameLogger.get_logger(__name__)
        self._section_timers: Dict[str, float] = {}

    def record_frame_time(self, frame_time_ms: float) -> None:
        """
        Record a frame time.

        Args:
            frame_time_ms: Frame time in milliseconds
        """
        self._frame_times.append(frame_time_ms)

        # Keep only recent samples
        if len(self._frame_times) > self._max_samples:
            self._frame_times.pop(0)

    def get_average_fps(self) -> float:
        """
        Get average FPS from recent frames.

        Returns:
            float: Average FPS, or 0.0 if no data
        """
        if not self._frame_times:
            return 0.0

        avg_frame_time_ms = sum(self._frame_times) / len(self._frame_times)
        if avg_frame_time_ms <= 0:
            return 0.0

        return 1000.0 / avg_frame_time_ms

    def get_average_frame_time(self) -> float:
        """
        Get average frame time from recent frames.

        Returns:
            float: Average frame time in milliseconds, or 0.0 if no data
        """
        if not self._frame_times:
            return 0.0

        return sum(self._frame_times) / len(self._frame_times)

    def get_memory_usage_mb(self) -> float:
        """
        Get current memory usage.

        Returns:
            float: Memory usage in megabytes
        """
        memory_info = self._process.memory_info()
        return memory_info.rss / (1024 * 1024)  # Convert bytes to MB

    def get_cpu_percent(self) -> float:
        """
        Get current CPU usage.

        Returns:
            float: CPU usage percentage
        """
        return self._process.cpu_percent()

    def get_current_metrics(self) -> PerformanceMetrics:
        """
        Get current performance metrics.

        Returns:
            PerformanceMetrics: Current performance metrics
        """
        return PerformanceMetrics(
            fps=self.get_average_fps(),
            frame_time_ms=self.get_average_frame_time(),
            memory_mb=self.get_memory_usage_mb(),
            cpu_percent=self.get_cpu_percent()
        )

    def start_section(self, section_name: str) -> None:
        """
        Start timing a code section.

        Args:
            section_name: Name of the section to profile
        """
        self._section_timers[section_name] = time.perf_counter()

    def end_section(self, section_name: str) -> float:
        """
        End timing a code section and return elapsed time.

        Args:
            section_name: Name of the section to profile

        Returns:
            float: Elapsed time in milliseconds, or 0.0 if section not started
        """
        if section_name not in self._section_timers:
            self._logger.warning(f"Section '{section_name}' was not started")
            return 0.0

        start_time = self._section_timers.pop(section_name)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        self._logger.debug(f"Section '{section_name}' took {elapsed_ms:.2f}ms")
        return elapsed_ms

    def profile_function(self, func: Callable, *args: Any, **kwargs: Any) -> tuple[Any, float]:
        """
        Profile a function call.

        Args:
            func: Function to profile
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            tuple: (function result, elapsed time in milliseconds)
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        self._logger.debug(f"Function '{func.__name__}' took {elapsed_ms:.2f}ms")
        return result, elapsed_ms

    def check_performance_targets(self) -> Dict[str, bool]:
        """
        Check if performance targets are met.

        Returns:
            Dict[str, bool]: Dictionary of target checks
        """
        metrics = self.get_current_metrics()

        targets = {
            "fps_target": metrics.fps >= 60.0,
            "memory_target": metrics.memory_mb <= 100.0,
        }

        return targets

    def log_performance_report(self) -> None:
        """Log a performance report."""
        metrics = self.get_current_metrics()
        targets = self.check_performance_targets()

        report = [
            "=== Performance Report ===",
            f"FPS: {metrics.fps:.1f} (target: ≥60) {'✓' if targets['fps_target'] else '✗'}",
            f"Frame Time: {metrics.frame_time_ms:.2f}ms",
            f"Memory: {metrics.memory_mb:.1f}MB (target: ≤100MB) {'✓' if targets['memory_target'] else '✗'}",
            f"CPU: {metrics.cpu_percent:.1f}%",
            "========================="
        ]

        for line in report:
            self._logger.info(line)

    def reset(self) -> None:
        """Reset all profiling data."""
        self._frame_times.clear()
        self._section_timers.clear()
        self._logger.debug("Performance profiler reset")
