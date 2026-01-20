"""
计时器工具模块

提供性能监控和时间测量工具。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

import time
from typing import Optional, Callable, Any
from contextlib import contextmanager
from src.utils.logger import get_logger, log_performance

logger = get_logger(__name__)


class Timer:
    """
    计时器类，用于测量代码执行时间

    Example:
        >>> timer = Timer()
        >>> timer.start()
        >>> # ... 执行操作 ...
        >>> elapsed = timer.stop()
        >>> print(f"Elapsed: {elapsed}ms")
    """

    def __init__(self, name: str = "Timer") -> None:
        """
        初始化计时器

        Args:
            name: 计时器名称
        """
        self.name = name
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._elapsed_ms: float = 0.0

    def start(self) -> None:
        """开始计时"""
        self._start_time = time.time()
        self._end_time = None
        logger.debug(f"Timer '{self.name}' started")

    def stop(self) -> float:
        """
        停止计时

        Returns:
            float: 经过的时间（毫秒）

        Raises:
            RuntimeError: 计时器未启动
        """
        if self._start_time is None:
            raise RuntimeError(f"Timer '{self.name}' was not started")

        self._end_time = time.time()
        self._elapsed_ms = (self._end_time - self._start_time) * 1000
        logger.debug(f"Timer '{self.name}' stopped: {self._elapsed_ms:.2f}ms")
        return self._elapsed_ms

    def reset(self) -> None:
        """重置计时器"""
        self._start_time = None
        self._end_time = None
        self._elapsed_ms = 0.0
        logger.debug(f"Timer '{self.name}' reset")

    def elapsed(self) -> float:
        """
        获取经过的时间（不停止计时器）

        Returns:
            float: 经过的时间（毫秒）

        Raises:
            RuntimeError: 计时器未启动
        """
        if self._start_time is None:
            raise RuntimeError(f"Timer '{self.name}' was not started")

        current_time = time.time()
        return (current_time - self._start_time) * 1000

    def is_running(self) -> bool:
        """
        检查计时器是否正在运行

        Returns:
            bool: 计时器是否正在运行
        """
        return self._start_time is not None and self._end_time is None

    def __enter__(self) -> 'Timer':
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """上下文管理器出口"""
        self.stop()

    def __repr__(self) -> str:
        """返回计时器的字符串表示"""
        status = "running" if self.is_running() else "stopped"
        return f"<Timer(name='{self.name}', status={status}, elapsed={self._elapsed_ms:.2f}ms)>"


class PerformanceTimer(Timer):
    """
    性能计时器，自动记录性能日志

    Example:
        >>> with PerformanceTimer('level_loading', level_id='001'):
        ...     load_level('001')
    """

    def __init__(self, operation: str, **context: Any) -> None:
        """
        初始化性能计时器

        Args:
            operation: 操作名称
            **context: 额外的上下文信息
        """
        super().__init__(name=operation)
        self.operation = operation
        self.context = context

    def stop(self) -> float:
        """
        停止计时并记录性能日志

        Returns:
            float: 经过的时间（毫秒）
        """
        elapsed = super().stop()
        log_performance(self.operation, elapsed, **self.context)
        return elapsed


@contextmanager
def measure_time(operation: str, **context: Any):
    """
    上下文管理器：测量代码块执行时间并记录性能日志

    Args:
        operation: 操作名称
        **context: 额外的上下文信息

    Yields:
        Timer: 计时器实例

    Example:
        >>> with measure_time('database_query', query_type='SELECT'):
        ...     execute_query()
    """
    timer = PerformanceTimer(operation, **context)
    timer.start()
    try:
        yield timer
    finally:
        timer.stop()


def time_function(func: Callable) -> Callable:
    """
    装饰器：测量函数执行时间

    Args:
        func: 被装饰的函数

    Returns:
        Callable: 装饰后的函数

    Example:
        >>> @time_function
        ... def slow_function():
        ...     time.sleep(1)
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        timer = Timer(name=func.__name__)
        timer.start()
        try:
            result = func(*args, **kwargs)
            elapsed = timer.stop()
            logger.info(f"Function '{func.__name__}' executed in {elapsed:.2f}ms")
            return result
        except Exception as e:
            timer.stop()
            logger.error(f"Function '{func.__name__}' failed after {timer._elapsed_ms:.2f}ms")
            raise

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


class FPSCounter:
    """
    FPS计数器，用于监控帧率

    Example:
        >>> fps_counter = FPSCounter()
        >>> while running:
        ...     fps_counter.tick()
        ...     current_fps = fps_counter.get_fps()
    """

    def __init__(self, sample_size: int = 60) -> None:
        """
        初始化FPS计数器

        Args:
            sample_size: 采样大小（帧数）
        """
        self.sample_size = sample_size
        self._frame_times: list = []
        self._last_time: float = time.time()

    def tick(self) -> None:
        """记录一帧"""
        current_time = time.time()
        frame_time = current_time - self._last_time
        self._last_time = current_time

        self._frame_times.append(frame_time)

        # 保持采样大小
        if len(self._frame_times) > self.sample_size:
            self._frame_times.pop(0)

    def update(self) -> None:
        """记录一帧（tick的别名方法）"""
        self.tick()

    def get_fps(self) -> float:
        """
        获取当前FPS

        Returns:
            float: 当前FPS

        Example:
            >>> fps_counter = FPSCounter()
            >>> fps_counter.tick()
            >>> fps = fps_counter.get_fps()
        """
        if not self._frame_times:
            return 0.0

        avg_frame_time = sum(self._frame_times) / len(self._frame_times)
        if avg_frame_time == 0:
            return 0.0

        return 1.0 / avg_frame_time

    def reset(self) -> None:
        """重置FPS计数器"""
        self._frame_times.clear()
        self._last_time = time.time()

    def __repr__(self) -> str:
        """返回FPS计数器的字符串表示"""
        return f"<FPSCounter(fps={self.get_fps():.1f}, samples={len(self._frame_times)})>"


def get_timestamp() -> float:
    """
    获取当前时间戳（秒）

    Returns:
        float: 当前时间戳

    Example:
        >>> timestamp = get_timestamp()
    """
    return time.time()


def get_timestamp_ms() -> int:
    """
    获取当前时间戳（毫秒）

    Returns:
        int: 当前时间戳（毫秒）

    Example:
        >>> timestamp_ms = get_timestamp_ms()
    """
    return int(time.time() * 1000)


def sleep_ms(milliseconds: int) -> None:
    """
    休眠指定毫秒数

    Args:
        milliseconds: 休眠时间（毫秒）

    Example:
        >>> sleep_ms(100)  # 休眠100毫秒
    """
    time.sleep(milliseconds / 1000.0)
