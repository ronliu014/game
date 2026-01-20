"""
网格管理器单元测试

测试GridManager类的所有功能。
"""

import unittest
from src.core.grid.grid_manager import GridManager
from src.core.grid.tile import Tile
from src.core.grid.tile_type import TileType


class TestGridManagerInitialization(unittest.TestCase):
    """测试网格管理器初始化"""

    def test_grid_creation(self):
        """测试创建网格"""
        manager = GridManager(4)
        self.assertEqual(manager.grid_size, 4)
        self.assertEqual(manager.get_tile_count(), 0)

    def test_grid_creation_minimum_size(self):
        """测试最小网格大小"""
        manager = GridManager(2)
        self.assertEqual(manager.grid_size, 2)

    def test_grid_creation_invalid_size(self):
        """测试无效的网格大小"""
        with self.assertRaises(ValueError):
            GridManager(1)

        with self.assertRaises(ValueError):
            GridManager(0)

        with self.assertRaises(ValueError):
            GridManager(-1)


class TestGridManagerTileAccess(unittest.TestCase):
    """测试瓦片访问"""

    def setUp(self):
        """设置测试环境"""
        self.manager = GridManager(4)

    def test_get_tile_empty(self):
        """测试获取空位置的瓦片"""
        tile = self.manager.get_tile(0, 0)
        self.assertIsNone(tile)

    def test_set_and_get_tile(self):
        """测试设置和获取瓦片"""
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        self.assertTrue(self.manager.set_tile(0, 0, tile))

        retrieved = self.manager.get_tile(0, 0)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.x, 0)
        self.assertEqual(retrieved.y, 0)
        self.assertEqual(retrieved.tile_type, TileType.STRAIGHT)

    def test_set_tile_updates_coordinates(self):
        """测试设置瓦片时更新坐标"""
        tile = Tile(5, 5, TileType.STRAIGHT, 0)
        self.manager.set_tile(1, 2, tile)

        # 坐标应该被更新为实际位置
        self.assertEqual(tile.x, 1)
        self.assertEqual(tile.y, 2)

    def test_get_tile_invalid_coordinates(self):
        """测试获取无效坐标的瓦片"""
        self.assertIsNone(self.manager.get_tile(-1, 0))
        self.assertIsNone(self.manager.get_tile(0, -1))
        self.assertIsNone(self.manager.get_tile(4, 0))
        self.assertIsNone(self.manager.get_tile(0, 4))
        self.assertIsNone(self.manager.get_tile(10, 10))

    def test_set_tile_invalid_coordinates(self):
        """测试设置无效坐标的瓦片"""
        tile = Tile(0, 0, TileType.STRAIGHT, 0)
        self.assertFalse(self.manager.set_tile(-1, 0, tile))
        self.assertFalse(self.manager.set_tile(0, -1, tile))
        self.assertFalse(self.manager.set_tile(4, 0, tile))
        self.assertFalse(self.manager.set_tile(0, 4, tile))

    def test_overwrite_tile(self):
        """测试覆盖瓦片"""
        tile1 = Tile(0, 0, TileType.STRAIGHT, 0)
        tile2 = Tile(0, 0, TileType.CORNER, 90)

        self.manager.set_tile(0, 0, tile1)
        self.manager.set_tile(0, 0, tile2)

        retrieved = self.manager.get_tile(0, 0)
        self.assertEqual(retrieved.tile_type, TileType.CORNER)
        self.assertEqual(retrieved.rotation, 90)


class TestGridManagerRotation(unittest.TestCase):
    """测试瓦片旋转"""

    def setUp(self):
        """设置测试环境"""
        self.manager = GridManager(4)

    def test_rotate_straight_tile(self):
        """测试旋转直线瓦片"""
        tile = Tile(1, 1, TileType.STRAIGHT, 0)
        self.manager.set_tile(1, 1, tile)

        self.assertTrue(self.manager.rotate_tile(1, 1))
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 90)

        self.assertTrue(self.manager.rotate_tile(1, 1))
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 180)

    def test_rotate_corner_tile(self):
        """测试旋转转角瓦片"""
        tile = Tile(1, 1, TileType.CORNER, 0)
        self.manager.set_tile(1, 1, tile)

        self.assertTrue(self.manager.rotate_tile(1, 1))
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 90)

    def test_rotate_non_rotatable_tile(self):
        """测试旋转不可旋转的瓦片"""
        # 电源端
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        self.manager.set_tile(0, 0, power)
        self.assertFalse(self.manager.rotate_tile(0, 0))
        self.assertEqual(self.manager.get_tile(0, 0).rotation, 0)

        # 终端
        terminal = Tile(1, 1, TileType.TERMINAL, 0)
        self.manager.set_tile(1, 1, terminal)
        self.assertFalse(self.manager.rotate_tile(1, 1))
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 0)

        # 空瓦片
        empty = Tile(2, 2, TileType.EMPTY, 0)
        self.manager.set_tile(2, 2, empty)
        self.assertFalse(self.manager.rotate_tile(2, 2))

    def test_rotate_empty_position(self):
        """测试旋转空位置"""
        self.assertFalse(self.manager.rotate_tile(0, 0))

    def test_rotate_invalid_coordinates(self):
        """测试旋转无效坐标"""
        self.assertFalse(self.manager.rotate_tile(-1, 0))
        self.assertFalse(self.manager.rotate_tile(0, -1))
        self.assertFalse(self.manager.rotate_tile(4, 0))


class TestGridManagerSpecialTiles(unittest.TestCase):
    """测试特殊瓦片访问"""

    def setUp(self):
        """设置测试环境"""
        self.manager = GridManager(4)

    def test_get_power_source_none(self):
        """测试获取不存在的电源端"""
        self.assertIsNone(self.manager.get_power_source())

    def test_get_terminal_none(self):
        """测试获取不存在的终端"""
        self.assertIsNone(self.manager.get_terminal())

    def test_set_and_get_power_source(self):
        """测试设置和获取电源端"""
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        self.manager.set_tile(0, 0, power)

        retrieved = self.manager.get_power_source()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.tile_type, TileType.POWER_SOURCE)
        self.assertEqual(retrieved.x, 0)
        self.assertEqual(retrieved.y, 0)

    def test_set_and_get_terminal(self):
        """测试设置和获取终端"""
        terminal = Tile(3, 3, TileType.TERMINAL, 0)
        self.manager.set_tile(3, 3, terminal)

        retrieved = self.manager.get_terminal()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.tile_type, TileType.TERMINAL)
        self.assertEqual(retrieved.x, 3)
        self.assertEqual(retrieved.y, 3)

    def test_move_power_source(self):
        """测试移动电源端"""
        power1 = Tile(0, 0, TileType.POWER_SOURCE, 0)
        self.manager.set_tile(0, 0, power1)

        power2 = Tile(1, 1, TileType.POWER_SOURCE, 0)
        self.manager.set_tile(1, 1, power2)

        # 应该返回新位置的电源端
        retrieved = self.manager.get_power_source()
        self.assertEqual(retrieved.x, 1)
        self.assertEqual(retrieved.y, 1)


class TestGridManagerState(unittest.TestCase):
    """测试网格状态管理"""

    def setUp(self):
        """设置测试环境"""
        self.manager = GridManager(4)

    def test_save_and_reset_state(self):
        """测试保存和重置状态"""
        # 设置初始状态
        tile = Tile(1, 1, TileType.STRAIGHT, 0)
        self.manager.set_tile(1, 1, tile)
        self.manager.save_initial_state()

        # 修改状态
        self.manager.rotate_tile(1, 1)
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 90)

        # 重置状态
        self.manager.reset_grid()
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 0)

    def test_reset_without_save(self):
        """测试未保存状态时重置"""
        tile = Tile(1, 1, TileType.STRAIGHT, 0)
        self.manager.set_tile(1, 1, tile)

        # 未保存状态，重置应该不做任何事
        self.manager.reset_grid()
        # 瓦片应该仍然存在
        self.assertIsNotNone(self.manager.get_tile(1, 1))

    def test_save_state_multiple_tiles(self):
        """测试保存多个瓦片的状态"""
        tile1 = Tile(0, 0, TileType.STRAIGHT, 0)
        tile2 = Tile(1, 1, TileType.CORNER, 90)
        tile3 = Tile(2, 2, TileType.STRAIGHT, 180)

        self.manager.set_tile(0, 0, tile1)
        self.manager.set_tile(1, 1, tile2)
        self.manager.set_tile(2, 2, tile3)
        self.manager.save_initial_state()

        # 修改所有瓦片
        self.manager.rotate_tile(0, 0)
        self.manager.rotate_tile(1, 1)
        self.manager.rotate_tile(2, 2)

        # 重置
        self.manager.reset_grid()

        # 验证所有瓦片都恢复到初始状态
        self.assertEqual(self.manager.get_tile(0, 0).rotation, 0)
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 90)
        self.assertEqual(self.manager.get_tile(2, 2).rotation, 180)

    def test_reset_preserves_special_tiles(self):
        """测试重置保留特殊瓦片"""
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        terminal = Tile(3, 3, TileType.TERMINAL, 0)
        tile = Tile(1, 1, TileType.STRAIGHT, 0)

        self.manager.set_tile(0, 0, power)
        self.manager.set_tile(3, 3, terminal)
        self.manager.set_tile(1, 1, tile)
        self.manager.save_initial_state()

        # 旋转普通瓦片
        self.manager.rotate_tile(1, 1)

        # 重置应该恢复所有瓦片包括特殊瓦片
        self.manager.reset_grid()
        self.assertIsNotNone(self.manager.get_power_source())
        self.assertIsNotNone(self.manager.get_terminal())
        self.assertEqual(self.manager.get_tile(1, 1).rotation, 0)


class TestGridManagerUtilities(unittest.TestCase):
    """测试网格工具方法"""

    def setUp(self):
        """设置测试环境"""
        self.manager = GridManager(4)

    def test_get_all_tiles_empty(self):
        """测试获取空网格的所有瓦片"""
        tiles = self.manager.get_all_tiles()
        self.assertEqual(len(tiles), 0)

    def test_get_all_tiles(self):
        """测试获取所有瓦片"""
        tile1 = Tile(0, 0, TileType.STRAIGHT, 0)
        tile2 = Tile(1, 1, TileType.CORNER, 90)
        tile3 = Tile(2, 2, TileType.POWER_SOURCE, 0)

        self.manager.set_tile(0, 0, tile1)
        self.manager.set_tile(1, 1, tile2)
        self.manager.set_tile(2, 2, tile3)

        tiles = self.manager.get_all_tiles()
        self.assertEqual(len(tiles), 3)

    def test_get_tile_count(self):
        """测试获取瓦片数量"""
        self.assertEqual(self.manager.get_tile_count(), 0)

        self.manager.set_tile(0, 0, Tile(0, 0, TileType.STRAIGHT, 0))
        self.assertEqual(self.manager.get_tile_count(), 1)

        self.manager.set_tile(1, 1, Tile(1, 1, TileType.CORNER, 0))
        self.assertEqual(self.manager.get_tile_count(), 2)

    def test_is_position_empty(self):
        """测试检查位置是否为空"""
        self.assertTrue(self.manager.is_position_empty(0, 0))

        self.manager.set_tile(0, 0, Tile(0, 0, TileType.STRAIGHT, 0))
        self.assertFalse(self.manager.is_position_empty(0, 0))

    def test_is_position_empty_invalid_coordinates(self):
        """测试检查无效坐标是否为空"""
        self.assertFalse(self.manager.is_position_empty(-1, 0))
        self.assertFalse(self.manager.is_position_empty(0, -1))
        self.assertFalse(self.manager.is_position_empty(4, 0))

    def test_clear_grid(self):
        """测试清空网格"""
        self.manager.set_tile(0, 0, Tile(0, 0, TileType.STRAIGHT, 0))
        self.manager.set_tile(1, 1, Tile(1, 1, TileType.CORNER, 0))
        self.manager.set_tile(2, 2, Tile(2, 2, TileType.POWER_SOURCE, 0))

        self.assertEqual(self.manager.get_tile_count(), 3)

        self.manager.clear_grid()

        self.assertEqual(self.manager.get_tile_count(), 0)
        self.assertIsNone(self.manager.get_power_source())
        self.assertIsNone(self.manager.get_terminal())

    def test_str_representation(self):
        """测试字符串表示"""
        manager = GridManager(4)
        str_repr = str(manager)
        self.assertIn("4x4", str_repr)
        self.assertIn("0 tiles", str_repr)

    def test_repr_representation(self):
        """测试详细表示"""
        manager = GridManager(4)
        manager.set_tile(0, 0, Tile(0, 0, TileType.POWER_SOURCE, 0))

        repr_str = repr(manager)
        self.assertIn("grid_size=4", repr_str)
        self.assertIn("tile_count=1", repr_str)
        self.assertIn("has_power_source=True", repr_str)


class TestGridManagerEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def test_large_grid(self):
        """测试大网格"""
        manager = GridManager(100)
        self.assertEqual(manager.grid_size, 100)

        # 测试边界位置
        tile = Tile(99, 99, TileType.STRAIGHT, 0)
        self.assertTrue(manager.set_tile(99, 99, tile))
        self.assertIsNotNone(manager.get_tile(99, 99))

    def test_multiple_rotations(self):
        """测试多次旋转"""
        manager = GridManager(4)
        tile = Tile(1, 1, TileType.STRAIGHT, 0)
        manager.set_tile(1, 1, tile)

        # 旋转4次应该回到初始状态
        for _ in range(4):
            manager.rotate_tile(1, 1)

        self.assertEqual(manager.get_tile(1, 1).rotation, 0)

    def test_state_independence(self):
        """测试状态独立性"""
        manager = GridManager(4)
        tile = Tile(1, 1, TileType.STRAIGHT, 0)
        manager.set_tile(1, 1, tile)
        manager.save_initial_state()

        # 修改瓦片
        manager.rotate_tile(1, 1)

        # 重置
        manager.reset_grid()

        # 再次修改
        manager.rotate_tile(1, 1)
        manager.rotate_tile(1, 1)

        # 重置应该回到初始状态，而不是第一次修改后的状态
        manager.reset_grid()
        self.assertEqual(manager.get_tile(1, 1).rotation, 0)


if __name__ == '__main__':
    unittest.main()
