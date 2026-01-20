"""
关卡加载器

从JSON文件加载关卡数据并创建游戏网格。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from src.core.grid.grid_manager import GridManager
from src.core.grid.tile import Tile
from src.core.grid.tile_type import TileType
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class LevelData:
    """
    关卡数据类

    存储从JSON加载的关卡数据。

    Attributes:
        level_id: 关卡ID
        version: 版本号
        name: 关卡名称
        difficulty: 难度等级（1-5）
        grid_size: 网格大小
        solution_tiles: 正确解法的瓦片列表
        rotated_tiles: 初始错误旋转的瓦片列表

    Example:
        >>> data = LevelData(
        ...     level_id="001",
        ...     version="1.0",
        ...     name="初学者",
        ...     difficulty=1,
        ...     grid_size=4,
        ...     solution_tiles=[...],
        ...     rotated_tiles=[...]
        ... )
    """

    def __init__(
        self,
        level_id: str,
        version: str,
        name: str,
        difficulty: int,
        grid_size: int,
        solution_tiles: List[Dict[str, Any]],
        rotated_tiles: List[Dict[str, int]]
    ) -> None:
        """
        初始化关卡数据

        Args:
            level_id: 关卡ID
            version: 版本号
            name: 关卡名称
            difficulty: 难度等级
            grid_size: 网格大小
            solution_tiles: 正确解法的瓦片列表
            rotated_tiles: 初始错误旋转的瓦片列表

        Example:
            >>> data = LevelData("001", "1.0", "初学者", 1, 4, [], [])
        """
        self.level_id = level_id
        self.version = version
        self.name = name
        self.difficulty = difficulty
        self.grid_size = grid_size
        self.solution_tiles = solution_tiles
        self.rotated_tiles = rotated_tiles

    def __repr__(self) -> str:
        """返回关卡数据的详细表示"""
        return (f"LevelData(level_id={self.level_id}, "
                f"name={self.name}, "
                f"difficulty={self.difficulty}, "
                f"grid_size={self.grid_size})")


class LevelLoader:
    """
    关卡加载器类

    从JSON文件加载关卡数据并创建游戏网格。

    Example:
        >>> loader = LevelLoader()
        >>> grid = loader.load_level("data/levels/level_001.json")
        >>> if grid:
        ...     print(f"Level loaded: {grid.grid_size}x{grid.grid_size}")
    """

    def __init__(self) -> None:
        """
        初始化关卡加载器

        Example:
            >>> loader = LevelLoader()
        """
        logger.debug("LevelLoader initialized")

    def load_level(self, filepath: str) -> Optional[GridManager]:
        """
        从JSON文件加载关卡

        Args:
            filepath: 关卡文件路径

        Returns:
            Optional[GridManager]: 加载的网格管理器，失败返回None

        Example:
            >>> loader = LevelLoader()
            >>> grid = loader.load_level("data/levels/level_001.json")
            >>> if grid:
            ...     print("Level loaded successfully")
        """
        try:
            # 加载JSON数据
            level_data = self._load_json(filepath)
            if level_data is None:
                return None

            # 验证数据
            if not self._validate_level_data(level_data):
                logger.error(f"Invalid level data in {filepath}")
                return None

            # 解析数据
            parsed_data = self._parse_level_data(level_data)
            if parsed_data is None:
                return None

            # 创建网格
            grid = self._create_grid(parsed_data)

            logger.info(f"Level loaded: {parsed_data.name} (ID: {parsed_data.level_id})")
            return grid

        except Exception as e:
            logger.error(f"Failed to load level from {filepath}: {e}")
            return None

    def _load_json(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        加载JSON文件

        Args:
            filepath: 文件路径

        Returns:
            Optional[Dict]: JSON数据，失败返回None
        """
        try:
            path = Path(filepath)
            if not path.exists():
                logger.error(f"Level file not found: {filepath}")
                return None

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.debug(f"JSON loaded from {filepath}")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filepath}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load JSON from {filepath}: {e}")
            return None

    def _validate_level_data(self, data: Dict[str, Any]) -> bool:
        """
        验证关卡数据格式

        Args:
            data: 关卡数据字典

        Returns:
            bool: 数据是否有效
        """
        # 检查必需字段
        required_fields = ["level_id", "version", "name", "difficulty", "grid_size", "solution", "initial_state"]
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False

        # 检查解法数据
        if "tiles" not in data["solution"]:
            logger.error("Missing tiles in solution")
            return False

        # 检查初始状态数据
        if "rotated_tiles" not in data["initial_state"]:
            logger.error("Missing rotated_tiles in initial_state")
            return False

        # 检查数据类型
        if not isinstance(data["grid_size"], int) or data["grid_size"] < 2:
            logger.error(f"Invalid grid_size: {data['grid_size']}")
            return False

        if not isinstance(data["difficulty"], int) or not (1 <= data["difficulty"] <= 5):
            logger.error(f"Invalid difficulty: {data['difficulty']}")
            return False

        return True

    def _parse_level_data(self, data: Dict[str, Any]) -> Optional[LevelData]:
        """
        解析关卡数据

        Args:
            data: 原始JSON数据

        Returns:
            Optional[LevelData]: 解析后的关卡数据，失败返回None
        """
        try:
            return LevelData(
                level_id=data["level_id"],
                version=data["version"],
                name=data["name"],
                difficulty=data["difficulty"],
                grid_size=data["grid_size"],
                solution_tiles=data["solution"]["tiles"],
                rotated_tiles=data["initial_state"]["rotated_tiles"]
            )
        except Exception as e:
            logger.error(f"Failed to parse level data: {e}")
            return None

    def _create_grid(self, level_data: LevelData) -> GridManager:
        """
        根据关卡数据创建网格

        Args:
            level_data: 关卡数据

        Returns:
            GridManager: 创建的网格管理器
        """
        # 创建网格
        grid = GridManager(level_data.grid_size)

        # 放置正确解法的瓦片
        for tile_data in level_data.solution_tiles:
            x = tile_data["x"]
            y = tile_data["y"]
            tile_type_str = tile_data["type"]
            rotation = tile_data["rotation"]

            # 转换瓦片类型
            tile_type = TileType.from_string(tile_type_str)

            # 创建瓦片（电源端和终端不可点击）
            is_clickable = tile_type not in (TileType.POWER_SOURCE, TileType.TERMINAL)
            tile = Tile(x, y, tile_type, rotation, is_clickable)

            grid.set_tile(x, y, tile)

        # 应用初始错误旋转
        for rotated_tile in level_data.rotated_tiles:
            x = rotated_tile["x"]
            y = rotated_tile["y"]
            target_rotation = rotated_tile["rotation"]

            # 获取瓦片并设置旋转
            tile = grid.get_tile(x, y)
            if tile and tile.is_rotatable():
                tile.set_rotation(target_rotation)

        # 保存初始状态（用于重置）
        grid.save_initial_state()

        logger.debug(f"Grid created with {grid.get_tile_count()} tiles")
        return grid
