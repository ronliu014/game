"""
瓦片类型枚举

定义游戏中所有瓦片的类型。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

from enum import Enum


class TileType(Enum):
    """
    瓦片类型枚举

    定义电路板上所有可能的瓦片类型。
    """

    EMPTY = "empty"                  # 空瓦片（无电路）
    POWER_SOURCE = "power_source"    # 电源端（起点）
    TERMINAL = "terminal"            # 终端（终点）
    STRAIGHT = "straight"            # 直线电路
    CORNER = "corner"                # 转角电路

    def __str__(self) -> str:
        """返回瓦片类型的字符串表示"""
        return self.value

    def __repr__(self) -> str:
        """返回瓦片类型的详细表示"""
        return f"TileType.{self.name}"

    @classmethod
    def from_string(cls, value: str) -> 'TileType':
        """
        从字符串创建TileType

        Args:
            value: 瓦片类型字符串

        Returns:
            TileType: 对应的瓦片类型

        Raises:
            ValueError: 无效的瓦片类型字符串

        Example:
            >>> TileType.from_string('power_source')
            TileType.POWER_SOURCE
        """
        for tile_type in cls:
            if tile_type.value == value:
                return tile_type
        raise ValueError(f"Invalid tile type: {value}")

    def is_rotatable(self) -> bool:
        """
        检查瓦片是否可旋转

        Returns:
            bool: 瓦片是否可旋转

        Note:
            电源端和终端不可旋转，其他类型可旋转

        Example:
            >>> TileType.POWER_SOURCE.is_rotatable()
            False
            >>> TileType.STRAIGHT.is_rotatable()
            True
        """
        return self not in (TileType.POWER_SOURCE, TileType.TERMINAL, TileType.EMPTY)

    def has_circuit(self) -> bool:
        """
        检查瓦片是否包含电路

        Returns:
            bool: 瓦片是否包含电路

        Example:
            >>> TileType.EMPTY.has_circuit()
            False
            >>> TileType.STRAIGHT.has_circuit()
            True
        """
        return self != TileType.EMPTY
