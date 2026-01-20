"""
配置管理模块

提供统一的配置加载和访问接口，支持JSON配置文件和默认值。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """
    配置管理器（单例模式）

    负责加载、管理和访问游戏配置。支持从JSON文件加载配置，
    并提供点分隔键路径访问和默认值支持。

    Example:
        >>> ConfigManager.initialize('data/config/game_config.json')
        >>> config = ConfigManager.get_instance()
        >>> window_width = config.get('window.width', 800)
    """

    _instance: Optional['ConfigManager'] = None
    _initialized: bool = False

    def __new__(cls) -> 'ConfigManager':
        """确保单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """初始化配置管理器"""
        if not ConfigManager._initialized:
            self._config: Dict[str, Any] = {}
            self._config_path: Optional[Path] = None
            ConfigManager._initialized = True

    @classmethod
    def initialize(cls, config_path: str = 'data/config/game_config.json') -> 'ConfigManager':
        """
        初始化配置管理器并加载配置文件

        Args:
            config_path: 配置文件路径

        Returns:
            ConfigManager: 配置管理器实例

        Raises:
            FileNotFoundError: 配置文件不存在且无法使用默认配置
        """
        instance = cls.get_instance()
        instance._config_path = Path(config_path)

        if instance._config_path.exists():
            instance.load_config(str(instance._config_path))
            logger.info(f"Configuration loaded from: {config_path}")
        else:
            logger.warning(f"Configuration file not found: {config_path}, using defaults")
            instance._load_default_config()

        return instance

    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        """
        获取配置管理器实例

        Returns:
            ConfigManager: 配置管理器实例
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_config(self, config_path: str) -> None:
        """
        从JSON文件加载配置

        Args:
            config_path: 配置文件路径

        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: JSON格式错误
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            self._config_path = path
            logger.info(f"Configuration loaded successfully from: {config_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse configuration file: {config_path}", exc_info=True)
            raise

    def _load_default_config(self) -> None:
        """加载默认配置"""
        from src.config.constants import (
            WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
            GRID_SIZE_DEFAULT, TILE_SIZE, TILE_PADDING,
            AUDIO_VOLUME_DEFAULT, AUDIO_BGM_VOLUME, AUDIO_SFX_VOLUME,
            DEBUG_MODE, DEBUG_SHOW_FPS
        )

        self._config = {
            'window': {
                'width': WINDOW_WIDTH,
                'height': WINDOW_HEIGHT,
                'title': WINDOW_TITLE,
                'fps': FPS
            },
            'grid': {
                'default_size': GRID_SIZE_DEFAULT,
                'tile_size': TILE_SIZE,
                'tile_padding': TILE_PADDING
            },
            'audio': {
                'volume': AUDIO_VOLUME_DEFAULT,
                'bgm_volume': AUDIO_BGM_VOLUME,
                'sfx_volume': AUDIO_SFX_VOLUME
            },
            'debug': {
                'enabled': DEBUG_MODE,
                'show_fps': DEBUG_SHOW_FPS
            }
        }
        logger.info("Default configuration loaded")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（支持点分隔键路径）

        Args:
            key: 配置键，支持点分隔路径（如 'window.width'）
            default: 默认值，当键不存在时返回

        Returns:
            Any: 配置值或默认值

        Example:
            >>> config = ConfigManager.get_instance()
            >>> width = config.get('window.width', 800)
            >>> title = config.get('window.title', 'Game')
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            logger.debug(f"Configuration key not found: {key}, using default: {default}")
            return default

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值（支持点分隔键路径）

        Args:
            key: 配置键，支持点分隔路径（如 'window.width'）
            value: 配置值

        Example:
            >>> config = ConfigManager.get_instance()
            >>> config.set('window.width', 1024)
        """
        keys = key.split('.')
        config = self._config

        # 导航到最后一级的父节点
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value
        logger.debug(f"Configuration updated: {key} = {value}")

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置

        Returns:
            Dict[str, Any]: 完整的配置字典
        """
        return self._config.copy()

    def save(self, config_path: Optional[str] = None) -> None:
        """
        保存配置到JSON文件

        Args:
            config_path: 配置文件路径，如果为None则使用初始化时的路径

        Raises:
            ValueError: 没有指定配置文件路径
        """
        path = Path(config_path) if config_path else self._config_path

        if path is None:
            raise ValueError("No configuration file path specified")

        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to: {path}")
        except Exception as e:
            logger.error(f"Failed to save configuration to: {path}", exc_info=True)
            raise

    def reload(self) -> None:
        """
        重新加载配置文件

        Raises:
            ValueError: 没有配置文件路径
        """
        if self._config_path is None:
            raise ValueError("No configuration file path to reload")

        self.load_config(str(self._config_path))
        logger.info("Configuration reloaded")

    def has(self, key: str) -> bool:
        """
        检查配置键是否存在

        Args:
            key: 配置键，支持点分隔路径

        Returns:
            bool: 键是否存在
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return True
        except (KeyError, TypeError):
            return False

    def __repr__(self) -> str:
        """返回配置管理器的字符串表示"""
        return f"<ConfigManager(config_path={self._config_path}, keys={len(self._config)})>"
