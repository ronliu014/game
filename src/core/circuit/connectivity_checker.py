"""
电路连通性检测器

使用BFS算法检测电源端到终端的连通性，并找到连接路径。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

from typing import Optional, List, Set, Tuple, Deque
from collections import deque
from src.core.grid.grid_manager import GridManager
from src.core.grid.tile import Tile
from src.core.grid.tile_type import TileType
from src.config.constants import Direction
from src.utils.logger import GameLogger
from src.utils.timer import PerformanceTimer

logger = GameLogger.get_logger(__name__)


class ConnectivityChecker:
    """
    电路连通性检测器类

    使用广度优先搜索(BFS)算法检测从电源端到终端的电路连通性。

    性能要求:
        - 4x4网格: < 5ms
        - 8x8网格: < 20ms

    Example:
        >>> checker = ConnectivityChecker()
        >>> grid = GridManager(4)
        >>> # ... 设置瓦片 ...
        >>> is_connected = checker.check_connectivity(grid)
        >>> if is_connected:
        ...     path = checker.find_path(grid)
    """

    def __init__(self) -> None:
        """
        初始化连通性检测器

        Example:
            >>> checker = ConnectivityChecker()
        """
        logger.debug("ConnectivityChecker initialized")

    def _is_valid_position(self, grid: GridManager, x: int, y: int) -> bool:
        """
        检查坐标是否在网格范围内

        Args:
            grid: 网格管理器
            x: x坐标
            y: y坐标

        Returns:
            bool: 坐标是否有效
        """
        return 0 <= x < grid.grid_size and 0 <= y < grid.grid_size

    def check_connectivity(self, grid: GridManager) -> bool:
        """
        检查电源端到终端是否连通

        Args:
            grid: 网格管理器

        Returns:
            bool: 是否连通

        Example:
            >>> checker = ConnectivityChecker()
            >>> grid = GridManager(4)
            >>> # ... 设置连通的电路 ...
            >>> checker.check_connectivity(grid)
            True
        """
        with PerformanceTimer("check_connectivity", grid_size=grid.grid_size):
            path = self.find_path(grid)
            is_connected = path is not None

            logger.info(f"Connectivity check: {is_connected} (grid size: {grid.grid_size}x{grid.grid_size})")
            return is_connected

    def find_path(self, grid: GridManager) -> Optional[List[Tile]]:
        """
        查找从电源端到终端的路径

        使用BFS算法遍历电路，找到一条从电源端到终端的有效路径。

        Args:
            grid: 网格管理器

        Returns:
            Optional[List[Tile]]: 路径瓦片列表，如果不连通则返回None

        Note:
            路径包含电源端和终端

        Example:
            >>> checker = ConnectivityChecker()
            >>> grid = GridManager(4)
            >>> # ... 设置瓦片 ...
            >>> path = checker.find_path(grid)
            >>> if path:
            ...     print(f"Path length: {len(path)}")
        """
        # 获取电源端和终端
        power_source = grid.get_power_source()
        terminal = grid.get_terminal()

        if power_source is None:
            logger.warning("No power source found in grid")
            return None

        if terminal is None:
            logger.warning("No terminal found in grid")
            return None

        # BFS初始化
        queue: Deque[Tile] = deque([power_source])
        visited: Set[Tuple[int, int]] = {(power_source.x, power_source.y)}
        parent: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            (power_source.x, power_source.y): None
        }

        # BFS搜索
        while queue:
            current = queue.popleft()

            # 检查是否到达终端
            if current.x == terminal.x and current.y == terminal.y:
                # 重建路径
                path = self._reconstruct_path(parent, power_source, terminal)
                logger.debug(f"Path found with length {len(path)}")
                return path

            # 遍历当前瓦片的所有出口方向
            for direction in current.get_exit_directions():
                # 获取邻居位置
                neighbor_pos = current.get_neighbor_position(direction)

                # 检查坐标是否在网格范围内
                if not self._is_valid_position(grid, neighbor_pos[0], neighbor_pos[1]):
                    continue

                neighbor_tile = grid.get_tile(*neighbor_pos)

                # 检查邻居是否有效
                if neighbor_tile is None:
                    continue

                # 检查是否已访问
                if neighbor_pos in visited:
                    continue

                # 检查邻居是否有从当前方向进入的入口
                if not neighbor_tile.has_entrance_from(direction):
                    continue

                # 标记为已访问并加入队列
                visited.add(neighbor_pos)
                parent[neighbor_pos] = (current.x, current.y)
                queue.append(neighbor_tile)

        # 未找到路径
        logger.debug("No path found from power source to terminal")
        return None

    def _reconstruct_path(
        self,
        parent: dict[Tuple[int, int], Optional[Tuple[int, int]]],
        power_source: Tile,
        terminal: Tile
    ) -> List[Tile]:
        """
        从parent字典重建路径

        Args:
            parent: BFS生成的父节点字典
            power_source: 电源端瓦片
            terminal: 终端瓦片

        Returns:
            List[Tile]: 从电源端到终端的路径

        Note:
            这是一个内部方法，由find_path调用
        """
        path = []
        current_pos = (terminal.x, terminal.y)

        # 从终端回溯到电源端
        while current_pos is not None:
            path.append(current_pos)
            current_pos = parent.get(current_pos)

        # 反转路径（从电源端到终端）
        path.reverse()
        return path

    def get_connected_tiles(self, grid: GridManager) -> Set[Tile]:
        """
        获取所有从电源端连通的瓦片集合

        用于动画显示 - 只有连通的瓦片会显示电流动画。

        Args:
            grid: 网格管理器

        Returns:
            Set[Tile]: 连通瓦片集合

        Example:
            >>> checker = ConnectivityChecker()
            >>> grid = GridManager(4)
            >>> # ... 设置瓦片 ...
            >>> connected = checker.get_connected_tiles(grid)
            >>> print(f"Connected tiles: {len(connected)}")
        """
        power_source = grid.get_power_source()

        if power_source is None:
            logger.warning("No power source found in grid")
            return set()

        # BFS遍历所有连通的瓦片
        queue: Deque[Tile] = deque([power_source])
        visited: Set[Tuple[int, int]] = {(power_source.x, power_source.y)}
        connected_tiles: Set[Tile] = {power_source}

        while queue:
            current = queue.popleft()

            # 遍历当前瓦片的所有出口方向
            for direction in current.get_exit_directions():
                neighbor_pos = current.get_neighbor_position(direction)

                # 检查坐标是否在网格范围内
                if not self._is_valid_position(grid, neighbor_pos[0], neighbor_pos[1]):
                    continue

                neighbor_tile = grid.get_tile(*neighbor_pos)

                # 检查邻居是否有效
                if neighbor_tile is None:
                    continue

                # 检查是否已访问
                if neighbor_pos in visited:
                    continue

                # 检查邻居是否有从当前方向进入的入口
                if not neighbor_tile.has_entrance_from(direction):
                    continue

                # 标记为已访问并加入队列
                visited.add(neighbor_pos)
                connected_tiles.add(neighbor_tile)
                queue.append(neighbor_tile)

        logger.debug(f"Found {len(connected_tiles)} connected tiles")
        return connected_tiles

    def get_path_positions(self, grid: GridManager) -> Optional[List[Tuple[int, int]]]:
        """
        获取从电源端到终端的路径位置列表

        Args:
            grid: 网格管理器

        Returns:
            Optional[List[Tuple[int, int]]]: 路径位置列表(x, y)，如果不连通则返回None

        Example:
            >>> checker = ConnectivityChecker()
            >>> grid = GridManager(4)
            >>> # ... 设置瓦片 ...
            >>> positions = checker.get_path_positions(grid)
            >>> if positions:
            ...     for x, y in positions:
            ...         print(f"({x}, {y})")
        """
        path = self.find_path(grid)

        if path is None:
            return None

        return path

    def is_tile_in_path(self, grid: GridManager, x: int, y: int) -> bool:
        """
        检查指定位置的瓦片是否在连通路径中

        Args:
            grid: 网格管理器
            x: x坐标
            y: y坐标

        Returns:
            bool: 瓦片是否在路径中

        Example:
            >>> checker = ConnectivityChecker()
            >>> grid = GridManager(4)
            >>> # ... 设置瓦片 ...
            >>> checker.is_tile_in_path(grid, 1, 1)
            True
        """
        path = self.find_path(grid)

        if path is None:
            return False

        return (x, y) in path
