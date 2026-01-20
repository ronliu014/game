"""
网格管理器

管理游戏网格，包括瓦片的创建、访问、旋转等操作。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

from typing import Optional, List, Tuple, Dict
from copy import deepcopy
from src.core.grid.tile import Tile
from src.core.grid.tile_type import TileType
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class GridManager:
    """
    网格管理器类

    管理NxN的游戏网格，提供瓦片访问、旋转和状态管理功能。

    Attributes:
        grid_size: 网格大小（NxN）
        _grid: 二维网格数据结构
        _initial_state: 初始状态（用于重置）
        _power_source_pos: 电源端位置
        _terminal_pos: 终端位置

    Example:
        >>> manager = GridManager(4)
        >>> manager.set_tile(0, 0, Tile(0, 0, TileType.POWER_SOURCE, 0))
        >>> tile = manager.get_tile(0, 0)
        >>> manager.rotate_tile(1, 1)
    """

    def __init__(self, grid_size: int) -> None:
        """
        初始化网格管理器

        Args:
            grid_size: 网格大小（必须≥2）

        Raises:
            ValueError: 网格大小无效

        Example:
            >>> manager = GridManager(4)
            >>> manager.grid_size
            4
        """
        if grid_size < 2:
            raise ValueError(f"Grid size must be at least 2, got {grid_size}")

        self.grid_size = grid_size
        self._grid: Dict[Tuple[int, int], Tile] = {}
        self._initial_state: Dict[Tuple[int, int], Tile] = {}
        self._power_source_pos: Optional[Tuple[int, int]] = None
        self._terminal_pos: Optional[Tuple[int, int]] = None

        logger.info(f"GridManager initialized with size {grid_size}x{grid_size}")

    def _validate_coordinates(self, x: int, y: int) -> bool:
        """
        验证坐标是否在网格范围内

        Args:
            x: x坐标
            y: y坐标

        Returns:
            bool: 坐标是否有效

        Example:
            >>> manager = GridManager(4)
            >>> manager._validate_coordinates(0, 0)
            True
            >>> manager._validate_coordinates(5, 5)
            False
        """
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        获取指定位置的瓦片

        Args:
            x: x坐标
            y: y坐标

        Returns:
            Optional[Tile]: 瓦片对象，如果位置无效或为空则返回None

        Example:
            >>> manager = GridManager(4)
            >>> tile = manager.get_tile(0, 0)
            >>> tile is None
            True
        """
        if not self._validate_coordinates(x, y):
            logger.warning(f"Invalid coordinates: ({x}, {y})")
            return None

        return self._grid.get((x, y))

    def set_tile(self, x: int, y: int, tile: Tile) -> bool:
        """
        设置指定位置的瓦片

        Args:
            x: x坐标
            y: y坐标
            tile: 瓦片对象

        Returns:
            bool: 是否设置成功

        Example:
            >>> manager = GridManager(4)
            >>> tile = Tile(0, 0, TileType.POWER_SOURCE, 0)
            >>> manager.set_tile(0, 0, tile)
            True
        """
        if not self._validate_coordinates(x, y):
            logger.warning(f"Cannot set tile at invalid coordinates: ({x}, {y})")
            return False

        # 更新瓦片的坐标（确保一致性）
        tile.x = x
        tile.y = y

        # 记录特殊瓦片位置
        if tile.tile_type == TileType.POWER_SOURCE:
            self._power_source_pos = (x, y)
            logger.debug(f"Power source set at ({x}, {y})")
        elif tile.tile_type == TileType.TERMINAL:
            self._terminal_pos = (x, y)
            logger.debug(f"Terminal set at ({x}, {y})")

        self._grid[(x, y)] = tile
        return True

    def rotate_tile(self, x: int, y: int) -> bool:
        """
        旋转指定位置的瓦片（顺时针90度）

        Args:
            x: x坐标
            y: y坐标

        Returns:
            bool: 是否旋转成功

        Note:
            只有可旋转的瓦片才能被旋转（STRAIGHT, CORNER）

        Example:
            >>> manager = GridManager(4)
            >>> tile = Tile(1, 1, TileType.STRAIGHT, 0)
            >>> manager.set_tile(1, 1, tile)
            >>> manager.rotate_tile(1, 1)
            True
            >>> manager.get_tile(1, 1).rotation
            90
        """
        tile = self.get_tile(x, y)

        if tile is None:
            logger.warning(f"Cannot rotate: no tile at ({x}, {y})")
            return False

        if not tile.is_rotatable():
            logger.debug(f"Cannot rotate: tile at ({x}, {y}) is not rotatable")
            return False

        old_rotation = tile.rotation
        tile.rotate_clockwise()
        logger.debug(f"Rotated tile at ({x}, {y}) from {old_rotation}° to {tile.rotation}°")

        return True

    def get_power_source(self) -> Optional[Tile]:
        """
        获取电源端瓦片

        Returns:
            Optional[Tile]: 电源端瓦片，如果不存在则返回None

        Example:
            >>> manager = GridManager(4)
            >>> tile = Tile(0, 0, TileType.POWER_SOURCE, 0)
            >>> manager.set_tile(0, 0, tile)
            >>> power = manager.get_power_source()
            >>> power.tile_type == TileType.POWER_SOURCE
            True
        """
        if self._power_source_pos is None:
            return None

        return self._grid.get(self._power_source_pos)

    def get_terminal(self) -> Optional[Tile]:
        """
        获取终端瓦片

        Returns:
            Optional[Tile]: 终端瓦片，如果不存在则返回None

        Example:
            >>> manager = GridManager(4)
            >>> tile = Tile(3, 3, TileType.TERMINAL, 0)
            >>> manager.set_tile(3, 3, tile)
            >>> terminal = manager.get_terminal()
            >>> terminal.tile_type == TileType.TERMINAL
            True
        """
        if self._terminal_pos is None:
            return None

        return self._grid.get(self._terminal_pos)

    def get_all_tiles(self) -> List[Tile]:
        """
        获取所有瓦片

        Returns:
            List[Tile]: 所有瓦片的列表

        Example:
            >>> manager = GridManager(2)
            >>> manager.set_tile(0, 0, Tile(0, 0, TileType.EMPTY, 0))
            >>> len(manager.get_all_tiles())
            1
        """
        return list(self._grid.values())

    def save_initial_state(self) -> None:
        """
        保存当前状态为初始状态（用于重置）

        Note:
            应在关卡加载完成后调用此方法

        Example:
            >>> manager = GridManager(4)
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 90)
            >>> manager.set_tile(0, 0, tile)
            >>> manager.save_initial_state()
            >>> manager.rotate_tile(0, 0)
            >>> manager.reset_grid()
            >>> manager.get_tile(0, 0).rotation
            90
        """
        self._initial_state = {}
        for pos, tile in self._grid.items():
            # 深拷贝瓦片以保存状态
            self._initial_state[pos] = Tile(
                tile.x,
                tile.y,
                tile.tile_type,
                tile.rotation,
                tile.is_clickable
            )

        logger.info("Initial grid state saved")

    def reset_grid(self) -> None:
        """
        重置网格到初始状态

        Note:
            需要先调用save_initial_state()保存初始状态

        Example:
            >>> manager = GridManager(4)
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> manager.set_tile(0, 0, tile)
            >>> manager.save_initial_state()
            >>> manager.rotate_tile(0, 0)
            >>> manager.reset_grid()
            >>> manager.get_tile(0, 0).rotation
            0
        """
        if not self._initial_state:
            logger.warning("Cannot reset: no initial state saved")
            return

        self._grid = {}
        for pos, tile in self._initial_state.items():
            # 深拷贝以避免修改初始状态
            self._grid[pos] = Tile(
                tile.x,
                tile.y,
                tile.tile_type,
                tile.rotation,
                tile.is_clickable
            )

        logger.info("Grid reset to initial state")

    def clear_grid(self) -> None:
        """
        清空网格

        Example:
            >>> manager = GridManager(4)
            >>> manager.set_tile(0, 0, Tile(0, 0, TileType.EMPTY, 0))
            >>> manager.clear_grid()
            >>> len(manager.get_all_tiles())
            0
        """
        self._grid.clear()
        self._initial_state.clear()
        self._power_source_pos = None
        self._terminal_pos = None
        logger.info("Grid cleared")

    def get_tile_count(self) -> int:
        """
        获取网格中的瓦片数量

        Returns:
            int: 瓦片数量

        Example:
            >>> manager = GridManager(4)
            >>> manager.set_tile(0, 0, Tile(0, 0, TileType.EMPTY, 0))
            >>> manager.get_tile_count()
            1
        """
        return len(self._grid)

    def is_position_empty(self, x: int, y: int) -> bool:
        """
        检查指定位置是否为空

        Args:
            x: x坐标
            y: y坐标

        Returns:
            bool: 位置是否为空

        Example:
            >>> manager = GridManager(4)
            >>> manager.is_position_empty(0, 0)
            True
        """
        if not self._validate_coordinates(x, y):
            return False

        return (x, y) not in self._grid

    def __str__(self) -> str:
        """返回网格的字符串表示"""
        return f"GridManager({self.grid_size}x{self.grid_size}, {self.get_tile_count()} tiles)"

    def __repr__(self) -> str:
        """返回网格的详细表示"""
        return (f"GridManager(grid_size={self.grid_size}, "
                f"tile_count={self.get_tile_count()}, "
                f"has_power_source={self._power_source_pos is not None}, "
                f"has_terminal={self._terminal_pos is not None})")
