"""
瓦片数据结构单元测试

测试TileType和Tile类的所有功能。
"""

import unittest
from src.core.grid.tile_type import TileType
from src.core.grid.tile import Tile
from src.config.constants import Direction


class TestTileType(unittest.TestCase):
    """测试瓦片类型枚举"""

    def test_tile_type_values(self):
        """测试瓦片类型的值"""
        self.assertEqual(TileType.EMPTY.value, "empty")
        self.assertEqual(TileType.POWER_SOURCE.value, "power_source")
        self.assertEqual(TileType.TERMINAL.value, "terminal")
        self.assertEqual(TileType.STRAIGHT.value, "straight")
        self.assertEqual(TileType.CORNER.value, "corner")

    def test_tile_type_str(self):
        """测试瓦片类型的字符串表示"""
        self.assertEqual(str(TileType.POWER_SOURCE), "power_source")
        self.assertEqual(str(TileType.STRAIGHT), "straight")

    def test_tile_type_repr(self):
        """测试瓦片类型的详细表示"""
        self.assertEqual(repr(TileType.POWER_SOURCE), "TileType.POWER_SOURCE")

    def test_from_string(self):
        """测试从字符串创建瓦片类型"""
        self.assertEqual(TileType.from_string("power_source"), TileType.POWER_SOURCE)
        self.assertEqual(TileType.from_string("straight"), TileType.STRAIGHT)
        self.assertEqual(TileType.from_string("corner"), TileType.CORNER)

    def test_from_string_invalid(self):
        """测试无效的字符串"""
        with self.assertRaises(ValueError):
            TileType.from_string("invalid_type")

    def test_is_rotatable(self):
        """测试瓦片是否可旋转"""
        # 不可旋转
        self.assertFalse(TileType.EMPTY.is_rotatable())
        self.assertFalse(TileType.POWER_SOURCE.is_rotatable())
        self.assertFalse(TileType.TERMINAL.is_rotatable())

        # 可旋转
        self.assertTrue(TileType.STRAIGHT.is_rotatable())
        self.assertTrue(TileType.CORNER.is_rotatable())

    def test_has_circuit(self):
        """测试瓦片是否包含电路"""
        self.assertFalse(TileType.EMPTY.has_circuit())
        self.assertTrue(TileType.POWER_SOURCE.has_circuit())
        self.assertTrue(TileType.TERMINAL.has_circuit())
        self.assertTrue(TileType.STRAIGHT.has_circuit())
        self.assertTrue(TileType.CORNER.has_circuit())


class TestTileInitialization(unittest.TestCase):
    """测试瓦片初始化"""

    def test_tile_creation(self):
        """测试创建瓦片"""
        tile = Tile(1, 2, TileType.STRAIGHT, 90)
        self.assertEqual(tile.x, 1)
        self.assertEqual(tile.y, 2)
        self.assertEqual(tile.tile_type, TileType.STRAIGHT)
        self.assertEqual(tile.rotation, 90)
        self.assertFalse(tile.is_clickable)

    def test_tile_default_rotation(self):
        """测试默认旋转角度"""
        tile = Tile(0, 0, TileType.STRAIGHT)
        self.assertEqual(tile.rotation, 0)

    def test_tile_rotation_normalization(self):
        """测试旋转角度标准化"""
        tile = Tile(0, 0, TileType.STRAIGHT, 450)
        self.assertEqual(tile.rotation, 90)

        tile = Tile(0, 0, TileType.STRAIGHT, -90)
        self.assertEqual(tile.rotation, 270)

    def test_tile_invalid_rotation(self):
        """测试无效的旋转角度"""
        with self.assertRaises(ValueError):
            Tile(0, 0, TileType.STRAIGHT, 45)


class TestTileRotation(unittest.TestCase):
    """测试瓦片旋转"""

    def test_rotate_clockwise(self):
        """测试顺时针旋转"""
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        tile.rotate_clockwise()
        self.assertEqual(tile.rotation, 90)

        tile.rotate_clockwise()
        self.assertEqual(tile.rotation, 180)

        tile.rotate_clockwise()
        self.assertEqual(tile.rotation, 270)

        tile.rotate_clockwise()
        self.assertEqual(tile.rotation, 0)

    def test_rotate_counterclockwise(self):
        """测试逆时针旋转"""
        tile = Tile(0, 0, TileType.CORNER, 0)
        tile.rotate_counterclockwise()
        self.assertEqual(tile.rotation, 270)

        tile.rotate_counterclockwise()
        self.assertEqual(tile.rotation, 180)

    def test_rotate_non_rotatable(self):
        """测试不可旋转的瓦片"""
        # 电源端
        tile = Tile(0, 0, TileType.POWER_SOURCE, 0)
        tile.rotate_clockwise()
        self.assertEqual(tile.rotation, 0)

        # 终端
        tile = Tile(0, 0, TileType.TERMINAL, 0)
        tile.rotate_clockwise()
        self.assertEqual(tile.rotation, 0)

    def test_set_rotation(self):
        """测试设置旋转角度"""
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        tile.set_rotation(180)
        self.assertEqual(tile.rotation, 180)

    def test_set_rotation_invalid(self):
        """测试设置无效的旋转角度"""
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        with self.assertRaises(ValueError):
            tile.set_rotation(45)

    def test_is_rotatable(self):
        """测试瓦片是否可旋转"""
        self.assertFalse(Tile(0, 0, TileType.POWER_SOURCE, 0).is_rotatable())
        self.assertFalse(Tile(0, 0, TileType.TERMINAL, 0).is_rotatable())
        self.assertTrue(Tile(0, 0, TileType.STRAIGHT, 0).is_rotatable())
        self.assertTrue(Tile(0, 0, TileType.CORNER, 0).is_rotatable())


class TestTileExitDirections(unittest.TestCase):
    """测试瓦片出口方向"""

    def test_empty_tile_exits(self):
        """测试空瓦片的出口"""
        tile = Tile(0, 0, TileType.EMPTY, 0)
        self.assertEqual(tile.get_exit_directions(), [])

    def test_power_source_exits(self):
        """测试电源端的出口"""
        tile = Tile(0, 0, TileType.POWER_SOURCE, 0)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 1)
        self.assertIn(Direction.EAST, exits)

    def test_terminal_exits(self):
        """测试终端的出口"""
        tile = Tile(0, 0, TileType.TERMINAL, 0)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 1)
        self.assertIn(Direction.WEST, exits)

    def test_straight_tile_exits(self):
        """测试直线瓦片的出口"""
        # 0度：东西
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 2)
        self.assertIn(Direction.EAST, exits)
        self.assertIn(Direction.WEST, exits)

        # 90度：南北
        tile = Tile(0, 0, TileType.STRAIGHT, 90)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 2)
        self.assertIn(Direction.SOUTH, exits)
        self.assertIn(Direction.NORTH, exits)

    def test_corner_tile_exits(self):
        """测试转角瓦片的出口"""
        # 0度：东南
        tile = Tile(0, 0, TileType.CORNER, 0)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 2)
        self.assertIn(Direction.EAST, exits)
        self.assertIn(Direction.SOUTH, exits)

        # 90度：南西
        tile = Tile(0, 0, TileType.CORNER, 90)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 2)
        self.assertIn(Direction.SOUTH, exits)
        self.assertIn(Direction.WEST, exits)

        # 180度：西北
        tile = Tile(0, 0, TileType.CORNER, 180)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 2)
        self.assertIn(Direction.WEST, exits)
        self.assertIn(Direction.NORTH, exits)

        # 270度：北东
        tile = Tile(0, 0, TileType.CORNER, 270)
        exits = tile.get_exit_directions()
        self.assertEqual(len(exits), 2)
        self.assertIn(Direction.NORTH, exits)
        self.assertIn(Direction.EAST, exits)


class TestTileEntrances(unittest.TestCase):
    """测试瓦片入口"""

    def test_has_entrance_from(self):
        """测试是否有从指定方向的入口"""
        # 直线瓦片（0度：东西）
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        # 从东边进入（出口在西边）
        self.assertTrue(tile.has_entrance_from(Direction.EAST))
        # 从西边进入（出口在东边）
        self.assertTrue(tile.has_entrance_from(Direction.WEST))
        # 从北边进入（无出口在南边）
        self.assertFalse(tile.has_entrance_from(Direction.NORTH))

    def test_corner_entrance(self):
        """测试转角瓦片的入口"""
        # 转角瓦片（0度：东南）
        tile = Tile(0, 0, TileType.CORNER, 0)
        # 从东边进入（出口在西边？不，出口在东边）
        # 入口是出口的相反方向，所以从西边和北边可以进入
        self.assertTrue(tile.has_entrance_from(Direction.WEST))
        self.assertTrue(tile.has_entrance_from(Direction.NORTH))
        self.assertFalse(tile.has_entrance_from(Direction.EAST))
        self.assertFalse(tile.has_entrance_from(Direction.SOUTH))


class TestTileNeighbor(unittest.TestCase):
    """测试瓦片邻居位置"""

    def test_get_neighbor_position(self):
        """测试获取邻居位置"""
        tile = Tile(1, 1, TileType.STRAIGHT, 0)

        # 东边邻居
        self.assertEqual(tile.get_neighbor_position(Direction.EAST), (2, 1))
        # 西边邻居
        self.assertEqual(tile.get_neighbor_position(Direction.WEST), (0, 1))
        # 北边邻居
        self.assertEqual(tile.get_neighbor_position(Direction.NORTH), (1, 0))
        # 南边邻居
        self.assertEqual(tile.get_neighbor_position(Direction.SOUTH), (1, 2))


class TestTileStringRepresentation(unittest.TestCase):
    """测试瓦片字符串表示"""

    def test_str(self):
        """测试字符串表示"""
        tile = Tile(1, 2, TileType.STRAIGHT, 90)
        self.assertEqual(str(tile), "Tile(1, 2, straight, 90°)")

    def test_repr(self):
        """测试详细表示"""
        tile = Tile(1, 2, TileType.CORNER, 180, is_clickable=True)
        repr_str = repr(tile)
        self.assertIn("x=1", repr_str)
        self.assertIn("y=2", repr_str)
        self.assertIn("TileType.CORNER", repr_str)
        self.assertIn("rotation=180", repr_str)
        self.assertIn("is_clickable=True", repr_str)


class TestTileEquality(unittest.TestCase):
    """测试瓦片相等性"""

    def test_equality(self):
        """测试瓦片相等"""
        tile1 = Tile(1, 2, TileType.STRAIGHT, 90)
        tile2 = Tile(1, 2, TileType.STRAIGHT, 90)
        self.assertEqual(tile1, tile2)

    def test_inequality_position(self):
        """测试位置不同的瓦片不相等"""
        tile1 = Tile(1, 2, TileType.STRAIGHT, 90)
        tile2 = Tile(2, 2, TileType.STRAIGHT, 90)
        self.assertNotEqual(tile1, tile2)

    def test_inequality_type(self):
        """测试���型不同的瓦片不相等"""
        tile1 = Tile(1, 2, TileType.STRAIGHT, 90)
        tile2 = Tile(1, 2, TileType.CORNER, 90)
        self.assertNotEqual(tile1, tile2)

    def test_inequality_rotation(self):
        """测试旋转不同的瓦片不相等"""
        tile1 = Tile(1, 2, TileType.STRAIGHT, 90)
        tile2 = Tile(1, 2, TileType.STRAIGHT, 180)
        self.assertNotEqual(tile1, tile2)

    def test_hash(self):
        """测试瓦片哈希"""
        tile1 = Tile(1, 2, TileType.STRAIGHT, 90)
        tile2 = Tile(1, 2, TileType.STRAIGHT, 90)
        # 相等的瓦片应该有相同的哈希值
        self.assertEqual(hash(tile1), hash(tile2))

        # 可以用作字典键
        tile_dict = {tile1: "value"}
        self.assertEqual(tile_dict[tile2], "value")


if __name__ == '__main__':
    unittest.main()
