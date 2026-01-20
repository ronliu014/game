"""
计时器工具单元测试

测试timer模块的所有计时功能。
"""

import unittest
import time
from src.utils.timer import (
    Timer,
    PerformanceTimer,
    measure_time,
    time_function,
    FPSCounter,
    get_timestamp,
    get_timestamp_ms,
    sleep_ms
)


class TestTimer(unittest.TestCase):
    """测试基础计时器"""

    def test_timer_start_stop(self):
        """测试计时器启动和停止"""
        timer = Timer("test")
        timer.start()
        time.sleep(0.01)  # 休眠10ms
        elapsed = timer.stop()

        self.assertGreater(elapsed, 0)
        self.assertGreater(elapsed, 5)  # 至少5ms

    def test_timer_not_started(self):
        """测试未启动的计时器"""
        timer = Timer("test")

        with self.assertRaises(RuntimeError):
            timer.stop()

        with self.assertRaises(RuntimeError):
            timer.elapsed()

    def test_timer_reset(self):
        """测试计时器重置"""
        timer = Timer("test")
        timer.start()
        time.sleep(0.01)
        timer.stop()

        timer.reset()
        self.assertFalse(timer.is_running())
        self.assertEqual(timer._elapsed_ms, 0.0)

    def test_timer_elapsed(self):
        """测试获取经过时间（不停止）"""
        timer = Timer("test")
        timer.start()
        time.sleep(0.01)
        elapsed1 = timer.elapsed()
        time.sleep(0.01)
        elapsed2 = timer.elapsed()

        # 第二次应该更大
        self.assertGreater(elapsed2, elapsed1)
        # 计时器应该还在运行
        self.assertTrue(timer.is_running())

    def test_timer_is_running(self):
        """测试计时器运行状态"""
        timer = Timer("test")
        self.assertFalse(timer.is_running())

        timer.start()
        self.assertTrue(timer.is_running())

        timer.stop()
        self.assertFalse(timer.is_running())

    def test_timer_context_manager(self):
        """测试计时器作为上下文管理器"""
        with Timer("test") as timer:
            time.sleep(0.01)
            self.assertTrue(timer.is_running())

        self.assertFalse(timer.is_running())
        self.assertGreater(timer._elapsed_ms, 0)

    def test_timer_repr(self):
        """测试计时器字符串表示"""
        timer = Timer("test")
        repr_str = repr(timer)
        self.assertIn("Timer", repr_str)
        self.assertIn("test", repr_str)


class TestPerformanceTimer(unittest.TestCase):
    """测试性能计时器"""

    def test_performance_timer_logs(self):
        """测试性能计时器记录日志"""
        timer = PerformanceTimer("test_operation", test_param="value")
        timer.start()
        time.sleep(0.01)
        elapsed = timer.stop()

        self.assertGreater(elapsed, 0)

    def test_performance_timer_context_manager(self):
        """测试性能计时器作为上下文管理器"""
        with PerformanceTimer("test_operation", param1="value1"):
            time.sleep(0.01)


class TestMeasureTime(unittest.TestCase):
    """测试measure_time上下文管理器"""

    def test_measure_time(self):
        """测试测量时间上下文管理器"""
        with measure_time("test_operation", test_key="test_value") as timer:
            time.sleep(0.01)
            self.assertTrue(timer.is_running())

        self.assertFalse(timer.is_running())
        self.assertGreater(timer._elapsed_ms, 0)


class TestTimeFunctionDecorator(unittest.TestCase):
    """测试time_function装饰器"""

    def test_time_function_decorator(self):
        """测试函数计时装饰器"""
        @time_function
        def test_func():
            time.sleep(0.01)
            return "result"

        result = test_func()
        self.assertEqual(result, "result")

    def test_time_function_with_exception(self):
        """测试装饰器处理异常"""
        @time_function
        def failing_func():
            time.sleep(0.01)
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            failing_func()


class TestFPSCounter(unittest.TestCase):
    """测试FPS计数器"""

    def test_fps_counter_initialization(self):
        """测试FPS计数器初始化"""
        counter = FPSCounter(sample_size=30)
        self.assertEqual(counter.sample_size, 30)
        self.assertEqual(counter.get_fps(), 0.0)

    def test_fps_counter_tick(self):
        """测试FPS计数器记录帧"""
        counter = FPSCounter()

        # 模拟60 FPS
        for _ in range(10):
            counter.tick()
            time.sleep(1/60)  # 约16.67ms

        fps = counter.get_fps()
        # FPS应该接近60（允许误差）
        self.assertGreater(fps, 30)
        self.assertLess(fps, 100)

    def test_fps_counter_reset(self):
        """测试FPS计数器重置"""
        counter = FPSCounter()

        for _ in range(5):
            counter.tick()
            time.sleep(0.01)

        counter.reset()
        self.assertEqual(len(counter._frame_times), 0)

    def test_fps_counter_repr(self):
        """测试FPS计数器字符串表示"""
        counter = FPSCounter()
        counter.tick()
        repr_str = repr(counter)
        self.assertIn("FPSCounter", repr_str)
        self.assertIn("fps=", repr_str)


class TestTimestampFunctions(unittest.TestCase):
    """测试时间戳函数"""

    def test_get_timestamp(self):
        """测试获取时间戳（秒）"""
        timestamp = get_timestamp()
        self.assertIsInstance(timestamp, float)
        self.assertGreater(timestamp, 0)

    def test_get_timestamp_ms(self):
        """测试获取时间戳（毫秒）"""
        timestamp_ms = get_timestamp_ms()
        self.assertIsInstance(timestamp_ms, int)
        self.assertGreater(timestamp_ms, 0)

    def test_timestamp_consistency(self):
        """测试时间戳一致性"""
        ts1 = get_timestamp()
        time.sleep(0.01)
        ts2 = get_timestamp()
        self.assertGreater(ts2, ts1)


class TestSleepMs(unittest.TestCase):
    """测试毫秒休眠"""

    def test_sleep_ms(self):
        """测试毫秒休眠"""
        start = time.time()
        sleep_ms(50)
        elapsed = (time.time() - start) * 1000

        # 应该至少休眠了50ms（允许一些误差）
        self.assertGreater(elapsed, 40)
        self.assertLess(elapsed, 100)


if __name__ == '__main__':
    unittest.main()
