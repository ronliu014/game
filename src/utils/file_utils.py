"""
文件工具函数模块

提供文件和路径相关的工具函数，包括安全路径处理、资源查找等。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

import os
from pathlib import Path
from typing import Optional, List
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_project_root() -> Path:
    """
    获取项目根目录

    Returns:
        Path: 项目根目录路径

    Example:
        >>> root = get_project_root()
        >>> root.name
        'game'
    """
    # 从当前文件向上查找，直到找到包含特定标记文件的目录
    current = Path(__file__).resolve()

    # 向上查找，直到找到包含 src 目录的父目录
    while current.parent != current:
        if (current / 'src').exists() and (current / 'data').exists():
            return current
        current = current.parent

    # 如果找不到，返回当前工作目录
    return Path.cwd()


def safe_path(path: str, base_dir: Optional[str] = None) -> Path:
    """
    创建安全的路径，防止路径遍历攻击

    Args:
        path: 相对路径
        base_dir: 基础目录，默认为项目根目录

    Returns:
        Path: 安全的绝对路径

    Raises:
        ValueError: 路径试图访问基础目录之外的位置

    Example:
        >>> safe_path('data/levels/level_001.json')
        PosixPath('.../game/data/levels/level_001.json')
    """
    if base_dir is None:
        base_dir = str(get_project_root())

    base = Path(base_dir).resolve()
    target = (base / path).resolve()

    # 检查目标路径是否在基础目录内
    try:
        target.relative_to(base)
    except ValueError:
        raise ValueError(f"Path '{path}' is outside base directory '{base_dir}'")

    return target


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，如果不存在则创建

    Args:
        path: 目录路径

    Returns:
        Path: 目录路径对象

    Example:
        >>> ensure_dir('logs/temp')
        PosixPath('.../game/logs/temp')
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {dir_path}")
    return dir_path


def find_resource(
    filename: str,
    search_dirs: Optional[List[str]] = None
) -> Optional[Path]:
    """
    在指定目录中查找资源文件

    Args:
        filename: 文件名
        search_dirs: 搜索目录列表，默认为 ['assets', 'data']

    Returns:
        Optional[Path]: 找到的文件路径，未找到返回None

    Example:
        >>> find_resource('power_source.png')
        PosixPath('.../game/assets/sprites/tiles/power_source.png')
    """
    if search_dirs is None:
        search_dirs = ['assets', 'data']

    root = get_project_root()

    for search_dir in search_dirs:
        base_path = root / search_dir
        if not base_path.exists():
            continue

        # 递归搜索
        for file_path in base_path.rglob(filename):
            if file_path.is_file():
                logger.debug(f"Found resource: {file_path}")
                return file_path

    logger.warning(f"Resource not found: {filename}")
    return None


def get_file_size(path: str) -> int:
    """
    获取文件大小（字节）

    Args:
        path: 文件路径

    Returns:
        int: 文件大小（字节）

    Raises:
        FileNotFoundError: 文件不存在

    Example:
        >>> get_file_size('data/config/game_config.json')
        1234
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return file_path.stat().st_size


def get_file_extension(path: str) -> str:
    """
    获取文件扩展名（不含点）

    Args:
        path: 文件路径

    Returns:
        str: 文件扩展名（小写，不含点）

    Example:
        >>> get_file_extension('level_001.json')
        'json'
        >>> get_file_extension('sprite.PNG')
        'png'
    """
    return Path(path).suffix.lstrip('.').lower()


def list_files(
    directory: str,
    extension: Optional[str] = None,
    recursive: bool = False
) -> List[Path]:
    """
    列出目录中的文件

    Args:
        directory: 目录路径
        extension: 文件扩展名过滤（不含点），None表示所有文件
        recursive: 是否递归搜索子目录

    Returns:
        List[Path]: 文件路径列表

    Example:
        >>> list_files('data/levels', extension='json')
        [PosixPath('.../level_001.json'), PosixPath('.../level_002.json')]
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        logger.warning(f"Directory not found: {directory}")
        return []

    if recursive:
        pattern = '**/*' if extension is None else f'**/*.{extension}'
        files = list(dir_path.glob(pattern))
    else:
        pattern = '*' if extension is None else f'*.{extension}'
        files = list(dir_path.glob(pattern))

    # 只返回文件，不包括目录
    return [f for f in files if f.is_file()]


def read_text_file(path: str, encoding: str = 'utf-8') -> str:
    """
    读取文本文件内容

    Args:
        path: 文件路径
        encoding: 文件编码

    Returns:
        str: 文件内容

    Raises:
        FileNotFoundError: 文件不存在

    Example:
        >>> content = read_text_file('data/config/game_config.json')
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def write_text_file(path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    写入文本文件

    Args:
        path: 文件路径
        content: 文件内容
        encoding: 文件编码

    Example:
        >>> write_text_file('output.txt', 'Hello, World!')
    """
    file_path = Path(path)

    # 确保父目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)

    logger.debug(f"File written: {path}")


def file_exists(path: str) -> bool:
    """
    检查文件是否存在

    Args:
        path: 文件路径

    Returns:
        bool: 文件是否存在

    Example:
        >>> file_exists('data/config/game_config.json')
        True
    """
    return Path(path).is_file()


def dir_exists(path: str) -> bool:
    """
    检查目录是否存在

    Args:
        path: 目录路径

    Returns:
        bool: 目录是否存在

    Example:
        >>> dir_exists('data/levels')
        True
    """
    return Path(path).is_dir()


def get_relative_path(path: str, base: Optional[str] = None) -> Path:
    """
    获取相对于基础目录的相对路径

    Args:
        path: 目标路径
        base: 基础目录，默认为项目根目录

    Returns:
        Path: 相对路径

    Example:
        >>> get_relative_path('/path/to/game/data/levels/level_001.json')
        PosixPath('data/levels/level_001.json')
    """
    if base is None:
        base = str(get_project_root())

    target = Path(path).resolve()
    base_path = Path(base).resolve()

    try:
        return target.relative_to(base_path)
    except ValueError:
        # 如果无法计算相对路径，返回绝对路径
        return target


def safe_join_path(base: str, *paths: str) -> str:
    """
    安全地连接路径，防止路径遍历攻击

    Args:
        base: 基础目录
        *paths: 要连接的路径部分

    Returns:
        str: 连接后的安全路径

    Raises:
        ValueError: 路径试图访问基础目录之外的位置

    Example:
        >>> safe_join_path('/base', 'data', 'levels', 'level_001.json')
        '/base/data/levels/level_001.json'
    """
    base_path = Path(base).resolve()
    target_path = base_path.joinpath(*paths).resolve()

    # 检查目标路径是否在基础目录内
    try:
        target_path.relative_to(base_path)
    except ValueError:
        raise ValueError(f"Path {paths} is outside base directory '{base}'")

    return str(target_path)
