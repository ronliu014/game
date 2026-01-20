"""
日志系统单元测试

测试日志系统的各项功能，确保符合《日志系统规范》要求。
"""

import unittest
import logging
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.utils.logger import (
    GameLogger,
    JsonFormatter,
    log_performance,
    log_execution,
    get_logger
)


class TestJsonFormatter(unittest.TestCase):
    """测试JSON格式化器"""

    def setUp(self):
        """测试前准备"""
        self.formatter = JsonFormatter()

    def test_format_basic_record(self):
        """测试基本日志记录格式化"""
        record = logging.LogRecord(
            name='test.module',
            level=logging.INFO,
            pathname='test.py',
            lineno=42,
            msg='Test message',
            args=(),
            exc_info=None,
            func='test_function'
        )

        result = self.formatter.format(record)
        log_data = json.loads(result)

        self.assertEqual(log_data['level'], 'INFO')
        self.assertEqual(log_data['module'], 'test.module')
        self.assertEqual(log_data['function'], 'test_function')
        self.assertEqual(log_data['line'], 42)
        self.assertEqual(log_data['message'], 'Test message')
        self.assertIn('timestamp', log_data)

    def test_format_with_context(self):
        """测试带上下文的日志格式化"""
        record = logging.LogRecord(
            name='test.module',
            level=logging.INFO,
            pathname='test.py',
            lineno=42,
            msg='Test message',
            args=(),
            exc_info=None,
            func='test_function'
        )
        record.context = {'level_id': '001', 'grid_size': 4}

        result = self.formatter.format(record)
        log_data = json.loads(result)

        self.assertIn('context', log_data)
        self.assertEqual(log_data['context']['level_id'], '001')
        self.assertEqual(log_data['context']['grid_size'], 4)

    def test_format_with_exception(self):
        """测试带异常信息的日志格式化"""
        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name='test.module',
            level=logging.ERROR,
            pathname='test.py',
            lineno=42,
            msg='Error occurred',
            args=(),
            exc_info=exc_info,
            func='test_function'
        )

        result = self.formatter.format(record)
        log_data = json.loads(result)

        self.assertIn('exception', log_data)
        self.assertIn('ValueError', log_data['exception'])
        self.assertIn('Test error', log_data['exception'])


class TestGameLogger(unittest.TestCase):
    """测试游戏日志管理器"""

    def setUp(self):
        """测试前准备"""
        # 重置初始化状态
        GameLogger._initialized = False

    def test_initialize_creates_log_directory(self):
        """测试初始化时创建日志目录"""
        log_dir = Path('logs')
        if log_dir.exists():
            # 如果目录已存在，先删除（仅用于测试）
            pass

        GameLogger.initialize()
        self.assertTrue(log_dir.exists())

    def test_initialize_only_once(self):
        """测试日志系统只初始化一次"""
        GameLogger.initialize()
        self.assertTrue(GameLogger._initialized)

        # 再次调用应该被忽略
        GameLogger.initialize()
        self.assertTrue(GameLogger._initialized)

    def test_initialize_with_missing_config(self):
        """测试配置文件不存在时使用默认配置"""
        GameLogger.initialize(config_path='nonexistent_config.json')
        self.assertTrue(GameLogger._initialized)

        # 应该能正常获取logger
        logger = GameLogger.get_logger('test')
        self.assertIsNotNone(logger)

    def test_get_logger(self):
        """测试获取Logger实例"""
        GameLogger.initialize()
        logger = GameLogger.get_logger('test.module')

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'test.module')

    def test_log_with_context(self):
        """测试带上下文的日志记录"""
        GameLogger.initialize()
        logger = GameLogger.get_logger('test')

        with self.assertLogs(logger, level='INFO') as cm:
            context = {'level_id': '001', 'grid_size': 4}
            GameLogger.log_with_context(logger, logging.INFO, "Test message", context)

        self.assertEqual(len(cm.output), 1)
        self.assertIn('Test message', cm.output[0])
        self.assertIn('level_id', cm.output[0])
        self.assertIn('001', cm.output[0])


class TestLogPerformance(unittest.TestCase):
    """测试性能日志功能"""

    def setUp(self):
        """测试前准备"""
        GameLogger.initialize()

    def test_log_performance_basic(self):
        """测试基本性能日志记录"""
        with self.assertLogs('performance', level='INFO') as cm:
            log_performance('test_operation', 123.45)

        self.assertEqual(len(cm.output), 1)
        self.assertIn('Performance: test_operation', cm.output[0])

    def test_log_performance_with_context(self):
        """测试带上下文的性能日志"""
        with self.assertLogs('performance', level='INFO') as cm:
            log_performance(
                'level_loading',
                250.5,
                level_id='001',
                tiles_count=16
            )

        self.assertEqual(len(cm.output), 1)
        self.assertIn('Performance: level_loading', cm.output[0])


class TestLogExecutionDecorator(unittest.TestCase):
    """测试日志执行装饰器"""

    def setUp(self):
        """测试前准备"""
        GameLogger.initialize()

    def test_decorator_logs_execution(self):
        """测试装饰器记录函数执行"""
        @log_execution
        def test_function(x, y):
            return x + y

        # 由于装饰器使用DEBUG级别，需要捕获DEBUG日志
        logger = logging.getLogger(__name__)
        with self.assertLogs(logger, level='DEBUG') as cm:
            result = test_function(2, 3)

        self.assertEqual(result, 5)
        # 应该有调用和完成两条日志
        self.assertGreaterEqual(len(cm.output), 1)

    def test_decorator_logs_exception(self):
        """测试装饰器记录异常"""
        @log_execution
        def failing_function():
            raise ValueError("Test error")

        logger = logging.getLogger(__name__)
        with self.assertLogs(logger, level='ERROR') as cm:
            with self.assertRaises(ValueError):
                failing_function()

        # 应该记录了错误日志
        self.assertGreaterEqual(len(cm.output), 1)
        self.assertTrue(any('failed' in output for output in cm.output))

    def test_decorator_preserves_function_metadata(self):
        """测试装饰器保留函数元数据"""
        @log_execution
        def documented_function():
            """This is a test function"""
            pass

        self.assertEqual(documented_function.__name__, 'documented_function')
        self.assertEqual(documented_function.__doc__, 'This is a test function')


class TestGetLoggerConvenience(unittest.TestCase):
    """测试便捷函数"""

    def setUp(self):
        """测试前准备"""
        GameLogger.initialize()

    def test_get_logger_convenience_function(self):
        """测试便捷的get_logger函数"""
        logger = get_logger('test.module')

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'test.module')


class TestLogLevels(unittest.TestCase):
    """测试日志级别"""

    def setUp(self):
        """测试前准备"""
        GameLogger.initialize()
        self.logger = GameLogger.get_logger('test')

    def test_debug_level(self):
        """测试DEBUG级别"""
        with self.assertLogs(self.logger, level='DEBUG') as cm:
            self.logger.debug("Debug message")

        self.assertEqual(len(cm.output), 1)
        self.assertIn('DEBUG', cm.output[0])

    def test_info_level(self):
        """测试INFO级别"""
        with self.assertLogs(self.logger, level='INFO') as cm:
            self.logger.info("Info message")

        self.assertEqual(len(cm.output), 1)
        self.assertIn('INFO', cm.output[0])

    def test_warning_level(self):
        """测试WARNING级别"""
        with self.assertLogs(self.logger, level='WARNING') as cm:
            self.logger.warning("Warning message")

        self.assertEqual(len(cm.output), 1)
        self.assertIn('WARNING', cm.output[0])

    def test_error_level(self):
        """测试ERROR级别"""
        with self.assertLogs(self.logger, level='ERROR') as cm:
            self.logger.error("Error message")

        self.assertEqual(len(cm.output), 1)
        self.assertIn('ERROR', cm.output[0])

    def test_critical_level(self):
        """测试CRITICAL级别"""
        with self.assertLogs(self.logger, level='CRITICAL') as cm:
            self.logger.critical("Critical message")

        self.assertEqual(len(cm.output), 1)
        self.assertIn('CRITICAL', cm.output[0])


if __name__ == '__main__':
    unittest.main()
