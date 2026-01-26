"""
Resource Manager Module
资源管理模块

This module provides utilities for loading game resources (images, audio, etc.)
with proper path handling for both development and PyInstaller packaged environments.

该模块提供游戏资源（图片、音频等）加载工具，
能够正确处理开发环境和PyInstaller打包环境下的路径。
"""

import os
import sys
from pathlib import Path
from typing import Union


class ResourceManager:
    """
    Resource Manager for handling file paths in both development and packaged environments.
    资源管理器，处理开发环境和打包环境下的文件路径。

    When packaged with PyInstaller, resources are extracted to sys._MEIPASS.
    使用PyInstaller打包时，资源会被解压到sys._MEIPASS目录。
    """

    _base_path: Path = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the resource manager.
        Must be called before using any resource paths.

        初始化资源管理器。
        在使用任何资源路径之前必须调用。
        """
        if hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            # PyInstaller打包后的环境
            cls._base_path = Path(sys._MEIPASS)
        else:
            # Running in development environment
            # 开发环境
            # Get project root (3 levels up from this file)
            # 获取项目根目录（从当前文件向上3级）
            cls._base_path = Path(__file__).parent.parent.parent

    @classmethod
    def get_base_path(cls) -> Path:
        """
        Get the base path for resources.
        获取资源的基础路径。

        Returns:
            Path: Base directory path
        """
        if cls._base_path is None:
            cls.initialize()
        return cls._base_path

    @classmethod
    def get_resource_path(cls, relative_path: Union[str, Path]) -> Path:
        """
        Get the absolute path to a resource file.
        获取资源文件的绝对路径。

        Args:
            relative_path: Path relative to project root (e.g., "assets/sprites/tile.png")
                         相对于项目根目录的路径（例如："assets/sprites/tile.png"）

        Returns:
            Path: Absolute path to the resource file
                  资源文件的绝对路径

        Example:
            >>> ResourceManager.get_resource_path("assets/sprites/tiles/tile_corner.png")
            Path("/path/to/project/assets/sprites/tiles/tile_corner.png")  # Development
            Path("C:/Users/.../AppData/Local/Temp/_MEIxxx/assets/sprites/tiles/tile_corner.png")  # Packaged
        """
        if cls._base_path is None:
            cls.initialize()

        # Convert to Path if string
        if isinstance(relative_path, str):
            relative_path = Path(relative_path)

        # Return absolute path
        return cls._base_path / relative_path

    @classmethod
    def get_asset_path(cls, asset_type: str, filename: str) -> Path:
        """
        Get path to an asset file by type.
        根据类型获取资源文件路径。

        Args:
            asset_type: Type of asset ("sprites/tiles", "sprites/ui", "audio/sfx", "audio/bgm", "fonts")
                       资源类型（"sprites/tiles", "sprites/ui", "audio/sfx", "audio/bgm", "fonts"）
            filename: Name of the file
                     文件名

        Returns:
            Path: Absolute path to the asset file
                  资源文件的绝对路径

        Example:
            >>> ResourceManager.get_asset_path("sprites/tiles", "tile_corner.png")
            Path("/path/to/project/assets/sprites/tiles/tile_corner.png")
        """
        return cls.get_resource_path(f"assets/{asset_type}/{filename}")

    @classmethod
    def get_data_path(cls, data_type: str, filename: str) -> Path:
        """
        Get path to a data file by type.
        根据类型获取数据文件路径。

        Args:
            data_type: Type of data ("levels", "config", "saves")
                      数据类型（"levels", "config", "saves"）
            filename: Name of the file
                     文件名

        Returns:
            Path: Absolute path to the data file
                  数据文件的绝对路径

        Example:
            >>> ResourceManager.get_data_path("config", "game_config.json")
            Path("/path/to/project/data/config/game_config.json")
        """
        return cls.get_resource_path(f"data/{data_type}/{filename}")

    @classmethod
    def resource_exists(cls, relative_path: Union[str, Path]) -> bool:
        """
        Check if a resource file exists.
        检查资源文件是否存在。

        Args:
            relative_path: Path relative to project root
                         相对于项目根目录的路径

        Returns:
            bool: True if file exists, False otherwise
                  文件存在返回True，否则返回False
        """
        path = cls.get_resource_path(relative_path)
        return path.exists()


# Auto-initialize on module import
# 模块导入时自动初始化
ResourceManager.initialize()
