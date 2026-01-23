"""
瓦片数据结构

定义单个瓦片的数据模型和行为。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

from dataclasses import dataclass
from typing import List, Tuple
from src.core.grid.tile_type import TileType
from src.config.constants import Direction, DIRECTION_VECTORS


@dataclass
class Tile:
    """
    瓦片类

    表示电路板上的单个瓦片，包含位置、类型和旋转角度。

    Attributes:
        x: 瓦片的x坐标（列）
        y: 瓦片的y坐标（行）
        tile_type: 瓦片类型
        rotation: 旋转角度（0, 90, 180, 270）
        is_clickable: 是否可点击（用于UI）

    Example:
        >>> tile = Tile(0, 0, TileType.POWER_SOURCE, 0)
        >>> tile.rotate_clockwise()
        >>> tile.rotation
        0  # 电源端不可旋转
    """

    x: int
    y: int
    tile_type: TileType
    rotation: int = 0
    is_clickable: bool = False

    def __post_init__(self) -> None:
        """初始化后验证"""
        # 标准化旋转角度
        self.rotation = self.rotation % 360

        # 验证旋转角度
        if self.rotation not in (0, 90, 180, 270):
            raise ValueError(f"Invalid rotation angle: {self.rotation}. Must be 0, 90, 180, or 270")

    def rotate_clockwise(self) -> None:
        """
        顺时针旋转90度

        Note:
            电源端和终端不可旋转，调用此方法不会改变它们的旋转角度

        Example:
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> tile.rotate_clockwise()
            >>> tile.rotation
            90
        """
        if self.is_rotatable():
            self.rotation = (self.rotation + 90) % 360

    def rotate_counterclockwise(self) -> None:
        """
        逆时针旋转90度

        Example:
            >>> tile = Tile(0, 0, TileType.CORNER, 90)
            >>> tile.rotate_counterclockwise()
            >>> tile.rotation
            0
        """
        if self.is_rotatable():
            self.rotation = (self.rotation - 90) % 360

    def set_rotation(self, angle: int) -> None:
        """
        设置旋转角度

        Args:
            angle: 旋转角度（0, 90, 180, 270）

        Raises:
            ValueError: 无效的旋转角度

        Example:
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> tile.set_rotation(180)
            >>> tile.rotation
            180
        """
        angle = angle % 360
        if angle not in (0, 90, 180, 270):
            raise ValueError(f"Invalid rotation angle: {angle}")

        if self.is_rotatable():
            self.rotation = angle

    def is_rotatable(self) -> bool:
        """
        检查瓦片是否可旋转

        Returns:
            bool: 瓦片是否可旋转

        Example:
            >>> Tile(0, 0, TileType.POWER_SOURCE, 0).is_rotatable()
            False
            >>> Tile(0, 0, TileType.STRAIGHT, 0).is_rotatable()
            True
        """
        return self.tile_type.is_rotatable()

    def get_exit_directions(self) -> List[Direction]:
        """
        获取当前旋转角度下的出口方向

        Returns:
            List[Direction]: 出口方向列表

        Note:
            - EMPTY: 无出口
            - POWER_SOURCE: 1个出口（东）
            - TERMINAL: 1个入口（西）
            - STRAIGHT: 2个出口（相对方向）
            - CORNER: 2个出口（相邻方向）

        Example:
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> tile.get_exit_directions()
            [Direction.EAST, Direction.WEST]
        """
        # 获取基础出口方向（0度时）
        base_exits = self._get_base_exit_directions()

        # 根据旋转角度调整方向
        return [self._rotate_direction(d, self.rotation) for d in base_exits]

    def _get_base_exit_directions(self) -> List[Direction]:
        """
        获取0度旋转时的基础出口方向

        Returns:
            List[Direction]: 基础出口方向列表

        Note:
            Straight tile at 0° or 180°: horizontal line (EAST-WEST, connects left-right)
            Straight tile at 90° or 270°: vertical line (NORTH-SOUTH, connects up-down)
            Corner tile at 0°: connects NORTH and EAST (L shape, opening right-up)

            Coordinate system: (x, y) where x=row, y=column
            - Same y value = same column = vertical arrangement = need vertical line (90°)
            - Same x value = same row = horizontal arrangement = need horizontal line (0°)
        """
        if self.tile_type == TileType.EMPTY:
            return []
        elif self.tile_type == TileType.POWER_SOURCE:
            return [Direction.EAST]
        elif self.tile_type == TileType.TERMINAL:
            return [Direction.WEST]
        elif self.tile_type == TileType.STRAIGHT:
            # 0° straight: horizontal line (EAST-WEST, connects left-right)
            return [Direction.EAST, Direction.WEST]
        elif self.tile_type == TileType.CORNER:
            # 0° corner: connects NORTH and EAST (L shape, opening right-up)
            return [Direction.NORTH, Direction.EAST]
        else:
            return []

    def _rotate_direction(self, direction: Direction, angle: int) -> Direction:
        """
        旋转方向

        Args:
            direction: 原始方向
            angle: 旋转角度（0, 90, 180, 270）

        Returns:
            Direction: 旋转后的方向

        Example:
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> tile._rotate_direction(Direction.EAST, 90)
            Direction.SOUTH
        """
        # 方向顺序：北 -> 东 -> 南 -> 西
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        current_index = directions.index(direction)

        # 计算旋转步数（每90度一步）
        steps = (angle // 90) % 4
        new_index = (current_index + steps) % 4

        return directions[new_index]

    def has_entrance_from(self, direction: Direction) -> bool:
        """
        检查是否有从指定方向进入的入口

        Args:
            direction: 进入方向

        Returns:
            bool: 是否有入口

        Note:
            入口方向是出口方向的相反方向

        Example:
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> tile.has_entrance_from(Direction.WEST)
            True
        """
        exits = self.get_exit_directions()
        # 入口是出口的相反方向
        opposite = self._get_opposite_direction(direction)
        return opposite in exits

    def _get_opposite_direction(self, direction: Direction) -> Direction:
        """
        获取相反方向

        Args:
            direction: 原始方向

        Returns:
            Direction: 相反方向

        Example:
            >>> tile = Tile(0, 0, TileType.STRAIGHT, 0)
            >>> tile._get_opposite_direction(Direction.NORTH)
            Direction.SOUTH
        """
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[direction]

    def get_neighbor_position(self, direction: Direction) -> Tuple[int, int]:
        """
        获取指定方向的邻居位置

        Args:
            direction: 方向

        Returns:
            Tuple[int, int]: 邻居的(x, y)坐标

        Example:
            >>> tile = Tile(1, 1, TileType.STRAIGHT, 0)
            >>> tile.get_neighbor_position(Direction.EAST)
            (2, 1)
        """
        dx, dy = DIRECTION_VECTORS[direction]
        return (self.x + dx, self.y + dy)

    def __str__(self) -> str:
        """返回瓦片的字符串表示"""
        return f"Tile({self.x}, {self.y}, {self.tile_type.value}, {self.rotation}°)"

    def __repr__(self) -> str:
        """返回瓦片的详细表示"""
        return (f"Tile(x={self.x}, y={self.y}, tile_type={self.tile_type!r}, "
                f"rotation={self.rotation}, is_clickable={self.is_clickable})")

    def __eq__(self, other: object) -> bool:
        """比较两个瓦片是否相等"""
        if not isinstance(other, Tile):
            return NotImplemented
        return (self.x == other.x and
                self.y == other.y and
                self.tile_type == other.tile_type and
                self.rotation == other.rotation)

    def __hash__(self) -> int:
        """返回瓦片的哈希值"""
        return hash((self.x, self.y, self.tile_type, self.rotation))
