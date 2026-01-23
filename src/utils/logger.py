"""
日志工具模块

提供统一的日志记录接口，支持结构化日志和上下文信息。

遵循《日志系统规范》(docs/specifications/04_日志系统规范.md)
"""

import logging
import logging.config
import json
import functools
import time
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """JSON格式化器，用于结构化日志输出"""

    def format(self, record: logging.LogRecord) -> str:
        """
        格式化日志记录为JSON格式

        Args:
            record: 日志记录对象

        Returns:
            str: JSON格式的日志字符串
        """
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            'level': record.levelname,
            'module': record.name,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }

        # 添加额外的上下文数据
        if hasattr(record, 'context'):
            log_data['context'] = record.context

        # 添加异常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class GameLogger:
    """
    游戏日志管理器

    提供统一的日志初始化和获取接口，确保日志系统的一致性。
    """

    _initialized = False

    @classmethod
    def initialize(cls, config_path: str = 'data/config/logging_config.json') -> None:
        """
        初始化日志系统

        Args:
            config_path: 日志配置文件路径

        Note:
            - 只会初始化一次，重复调用会被忽略
            - 如果配置文件不存在，使用默认配置
            - 自动创建logs目录
        """
        if cls._initialized:
            return

        # 创建日志目录
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # 加载配置
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logging.config.dictConfig(config)
            except Exception as e:
                # 配置加载失败，使用默认配置
                print(f"Warning: Failed to load logging config from {config_path}: {e}")
                cls._setup_default_logging()
        else:
            # 配置文件不存在，使用默认配置
            cls._setup_default_logging()

        cls._initialized = True

        # 记录日志系统初始化
        logger = logging.getLogger(__name__)
        logger.info("Logging system initialized successfully")

    @classmethod
    def _setup_default_logging(cls) -> None:
        """设置默认日志配置"""
        # Generate log filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f'logs/game_{timestamp}.log'

        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_filename, encoding='utf-8')
            ]
        )

        # Log the log file location
        logger = logging.getLogger(__name__)
        logger.info(f"Log file created: {log_filename}")

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        获取Logger实例

        Args:
            name: Logger名称（通常使用 __name__）

        Returns:
            logging.Logger: Logger实例

        Example:
            >>> logger = GameLogger.get_logger(__name__)
            >>> logger.info("Game started")
        """
        return logging.getLogger(name)

    @staticmethod
    def log_with_context(
        logger: logging.Logger,
        level: int,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        记录带上下文的日志

        Args:
            logger: Logger实例
            level: 日志级别 (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: 日志消息
            context: 上下文数据（字典）

        Example:
            >>> logger = GameLogger.get_logger(__name__)
            >>> context = {'level_id': '001', 'grid_size': 4}
            >>> GameLogger.log_with_context(logger, logging.INFO, "Level loaded", context)
        """
        if context:
            message = f"{message} {json.dumps(context, ensure_ascii=False)}"
        logger.log(level, message)


# 性能日志专用logger
performance_logger = logging.getLogger('performance')


def log_performance(operation: str, duration_ms: float, **kwargs: Any) -> None:
    """
    记录性能日志

    Args:
        operation: 操作名称
        duration_ms: 持续时间（毫秒）
        **kwargs: 额外的上下文信息

    Example:
        >>> start = time.time()
        >>> # ... 执行操作 ...
        >>> duration = (time.time() - start) * 1000
        >>> log_performance('level_loading', duration, level_id='001', tiles_count=16)
    """
    context = {
        'operation': operation,
        'duration_ms': round(duration_ms, 2),
        **kwargs
    }
    performance_logger.info(
        f"Performance: {operation}",
        extra={'context': context}
    )


def log_execution(func: Callable) -> Callable:
    """
    记录函数执行的装饰器

    自动记录函数的调用、执行时间和异常信息。

    Args:
        func: 被装饰的函数

    Returns:
        Callable: 装饰后的函数

    Example:
        >>> @log_execution
        ... def load_level(level_id: str):
        ...     # 加载关卡逻辑
        ...     pass
    """
    logger = GameLogger.get_logger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000

            logger.debug(f"{func.__name__} completed in {duration_ms:.2f}ms")
            log_performance(func.__name__, duration_ms)

            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}", exc_info=True)
            raise

    return wrapper


# 便捷函数：快速获取logger
def get_logger(name: str) -> logging.Logger:
    """
    快速获取logger的便捷函数

    Args:
        name: Logger名称

    Returns:
        logging.Logger: Logger实例
    """
    return GameLogger.get_logger(name)
