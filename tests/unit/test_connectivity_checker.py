"""
连通性检测器单元测试

测试ConnectivityChecker类的所有功能。
"""

import unittest
import time
from src.core.circuit.connectivity_checker import ConnectivityChecker
from src.core.grid.grid_manager import GridManager
from src.core.grid.tile import Tile
from src.core.grid.tile_type import TileType


class TestConnectivityCheckerInitialization(unittest.TestCase):
    """测试连通性检测器初始化"""

    def test_checker_creation(self):
        """测试创建检测器"""
        checker = ConnectivityChecker()
        self.assertIsNotNone(checker)


class TestConnectivityCheckerBasic(unittest.TestCase):
    """测试基本连通性检测"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()
        self.grid = GridManager(4)

    def test_no_power_source(self):
        """测试没有电源端的情况"""
        # 只有终端
        terminal = Tile(3, 3, TileType.TERMINAL, 0)
        self.grid.set_tile(3, 3, terminal)

        self.assertFalse(self.checker.check_connectivity(self.grid))
        self.assertIsNone(self.checker.find_path(self.grid))

    def test_no_terminal(self):
        """测试没有终端的情况"""
        # 只有电源端
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        self.grid.set_tile(0, 0, power)

        self.assertFalse(self.checker.check_connectivity(self.grid))
        self.assertIsNone(self.checker.find_path(self.grid))

    def test_empty_grid(self):
        """测试空网格"""
        self.assertFalse(self.checker.check_connectivity(self.grid))
        self.assertIsNone(self.checker.find_path(self.grid))

    def test_disconnected_circuit(self):
        """测试断开的电路"""
        # 创建断开的电路
        # 电源端 -> 直线（但没有连接到终端）
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight = Tile(1, 0, TileType.STRAIGHT, 0)
        terminal = Tile(3, 3, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight)
        self.grid.set_tile(3, 3, terminal)

        self.assertFalse(self.checker.check_connectivity(self.grid))
        self.assertIsNone(self.checker.find_path(self.grid))


class TestConnectivityCheckerSimplePaths(unittest.TestCase):
    """测试简单路径"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()
        self.grid = GridManager(5)  # Use 5x5 to have room for longer paths

    def test_straight_horizontal_path(self):
        """测试水平直线路径"""
        # 创建简单的水平路径
        # [Power] -> [Straight] -> [Straight] -> [Terminal]
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight1 = Tile(1, 0, TileType.STRAIGHT, 0)
        straight2 = Tile(2, 0, TileType.STRAIGHT, 0)
        terminal = Tile(3, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(2, 0, straight2)
        self.grid.set_tile(3, 0, terminal)

        # 检查连通性
        self.assertTrue(self.checker.check_connectivity(self.grid))

        # 检查路径
        path = self.checker.find_path(self.grid)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], (0, 0))  # 电源端
        self.assertEqual(path[-1], (3, 0))  # 终端

    def test_straight_vertical_path(self):
        """测试垂直路径"""
        # Terminal has exit WEST, so entrance from EAST
        # Power(0,0) → Corner(1,0) → Straight(1,1) → Straight(1,2) → Corner(1,3) → Terminal(2,3)
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)      # Exit EAST
        corner1 = Tile(1, 0, TileType.CORNER, 90)         # Exits SOUTH,WEST (receive from EAST, exit SOUTH)
        straight1 = Tile(1, 1, TileType.STRAIGHT, 90)     # Exits SOUTH,NORTH
        straight2 = Tile(1, 2, TileType.STRAIGHT, 90)     # Exits SOUTH,NORTH
        corner2 = Tile(1, 3, TileType.CORNER, 270)        # Exits NORTH,EAST (receive from SOUTH, exit EAST)
        terminal = Tile(2, 3, TileType.TERMINAL, 0)       # Exit WEST, entrance from EAST

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, corner1)
        self.grid.set_tile(1, 1, straight1)
        self.grid.set_tile(1, 2, straight2)
        self.grid.set_tile(1, 3, corner2)
        self.grid.set_tile(2, 3, terminal)

        self.assertTrue(self.checker.check_connectivity(self.grid))

    def test_l_shaped_path(self):
        """测试L形路径"""
        # Power(0,0) → Straight(1,0) → Straight(2,0) → Corner(3,0) → Straight(3,1) → Corner(3,2) → Terminal(4,2)
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)  # Exit EAST
        straight1 = Tile(1, 0, TileType.STRAIGHT, 0)  # Exits EAST,WEST
        straight2 = Tile(2, 0, TileType.STRAIGHT, 0)  # Exits EAST,WEST
        corner1 = Tile(3, 0, TileType.CORNER, 90)     # Exits SOUTH,WEST (receive from EAST, exit SOUTH)
        straight3 = Tile(3, 1, TileType.STRAIGHT, 90) # Exits SOUTH,NORTH
        corner2 = Tile(3, 2, TileType.CORNER, 270)    # Exits NORTH,EAST (receive from SOUTH, exit EAST)
        terminal = Tile(4, 2, TileType.TERMINAL, 0)   # Exit WEST, entrance from EAST

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(2, 0, straight2)
        self.grid.set_tile(3, 0, corner1)
        self.grid.set_tile(3, 1, straight3)
        self.grid.set_tile(3, 2, corner2)
        self.grid.set_tile(4, 2, terminal)

        self.assertTrue(self.checker.check_connectivity(self.grid))

        path = self.checker.find_path(self.grid)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 7)


class TestConnectivityCheckerComplexPaths(unittest.TestCase):
    """测试复杂路径"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()
        self.grid = GridManager(5)

    def test_zigzag_path(self):
        """测试简单曲折路径"""
        # Power → Straight → Corner → Straight → Corner → Terminal
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)       # Exit EAST
        straight1 = Tile(1, 0, TileType.STRAIGHT, 0)       # Exits EAST,WEST
        corner1 = Tile(2, 0, TileType.CORNER, 90)          # Exits SOUTH,WEST (receive from EAST, exit SOUTH)
        straight2 = Tile(2, 1, TileType.STRAIGHT, 90)      # Exits SOUTH,NORTH
        corner2 = Tile(2, 2, TileType.CORNER, 270)         # Exits NORTH,EAST (receive from SOUTH, exit EAST)
        terminal = Tile(3, 2, TileType.TERMINAL, 0)        # Exit WEST, entrance from EAST

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(2, 0, corner1)
        self.grid.set_tile(2, 1, straight2)
        self.grid.set_tile(2, 2, corner2)
        self.grid.set_tile(3, 2, terminal)

        self.assertTrue(self.checker.check_connectivity(self.grid))

    def test_spiral_path(self):
        """测试螺旋状路径"""
        grid = GridManager(5)

        # Path that wraps around
        grid.set_tile(0, 0, Tile(0, 0, TileType.POWER_SOURCE, 0))  # EAST
        grid.set_tile(1, 0, Tile(1, 0, TileType.STRAIGHT, 0))      # EAST,WEST
        grid.set_tile(2, 0, Tile(2, 0, TileType.STRAIGHT, 0))      # EAST,WEST
        grid.set_tile(3, 0, Tile(3, 0, TileType.CORNER, 90))       # SOUTH,WEST (receive from EAST, exit SOUTH)
        grid.set_tile(3, 1, Tile(3, 1, TileType.STRAIGHT, 90))     # SOUTH,NORTH
        grid.set_tile(3, 2, Tile(3, 2, TileType.CORNER, 270))      # NORTH,EAST (receive from SOUTH, exit EAST)
        grid.set_tile(4, 2, Tile(4, 2, TileType.TERMINAL, 0))      # WEST exit, entrance from EAST

        self.assertTrue(self.checker.check_connectivity(grid))


class TestConnectivityCheckerWrongRotation(unittest.TestCase):
    """测试错误旋转的情况"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()
        self.grid = GridManager(4)

    def test_wrong_rotation_disconnects(self):
        """测试错误的旋转导致断开"""
        # 创建路径但有一个瓦片旋转错误
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight1 = Tile(1, 0, TileType.STRAIGHT, 0)
        straight2 = Tile(2, 0, TileType.STRAIGHT, 90)  # 错误旋转！
        terminal = Tile(3, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(2, 0, straight2)
        self.grid.set_tile(3, 0, terminal)

        # 应该不连通
        self.assertFalse(self.checker.check_connectivity(self.grid))

    def test_correct_rotation_connects(self):
        """测试修正旋转后连通"""
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight1 = Tile(1, 0, TileType.STRAIGHT, 90)  # 初始错误（垂直）
        straight2 = Tile(2, 0, TileType.STRAIGHT, 0)
        terminal = Tile(3, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(2, 0, straight2)
        self.grid.set_tile(3, 0, terminal)

        # 初始不连通（90度是垂直的）
        self.assertFalse(self.checker.check_connectivity(self.grid))

        # 旋转到180度（水平的，应该连通）
        self.grid.rotate_tile(1, 0)  # 90 -> 180
        self.assertTrue(self.checker.check_connectivity(self.grid))

        # 旋转到270度（垂直的，不连通）
        self.grid.rotate_tile(1, 0)  # 180 -> 270
        self.assertFalse(self.checker.check_connectivity(self.grid))

        # 旋转到0度（水平的，连通）
        self.grid.rotate_tile(1, 0)  # 270 -> 0
        self.assertTrue(self.checker.check_connectivity(self.grid))


class TestConnectivityCheckerConnectedTiles(unittest.TestCase):
    """测试连通瓦片获取"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()
        self.grid = GridManager(4)

    def test_get_connected_tiles_simple(self):
        """测试获取简单路径的连通瓦片"""
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight1 = Tile(1, 0, TileType.STRAIGHT, 0)
        straight2 = Tile(2, 0, TileType.STRAIGHT, 0)
        terminal = Tile(3, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(2, 0, straight2)
        self.grid.set_tile(3, 0, terminal)

        connected = self.checker.get_connected_tiles(self.grid)
        self.assertEqual(len(connected), 4)

    def test_get_connected_tiles_partial(self):
        """测试获取部分连通的瓦片"""
        # 创建部分连通的电路
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight1 = Tile(1, 0, TileType.STRAIGHT, 0)
        # 没有更多连接
        terminal = Tile(3, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight1)
        self.grid.set_tile(3, 0, terminal)

        connected = self.checker.get_connected_tiles(self.grid)
        # 只有电源端和第一个直线连通
        self.assertEqual(len(connected), 2)

    def test_get_connected_tiles_no_power(self):
        """测试没有电源端时的连通瓦片"""
        connected = self.checker.get_connected_tiles(self.grid)
        self.assertEqual(len(connected), 0)


class TestConnectivityCheckerUtilities(unittest.TestCase):
    """测试工具方法"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()
        self.grid = GridManager(4)

    def test_get_path_positions(self):
        """测试获取路径位置"""
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight = Tile(1, 0, TileType.STRAIGHT, 0)
        terminal = Tile(2, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight)
        self.grid.set_tile(2, 0, terminal)

        positions = self.checker.get_path_positions(self.grid)
        self.assertIsNotNone(positions)
        self.assertEqual(len(positions), 3)
        self.assertIn((0, 0), positions)
        self.assertIn((1, 0), positions)
        self.assertIn((2, 0), positions)

    def test_get_path_positions_no_path(self):
        """测试没有路径时获取位置"""
        positions = self.checker.get_path_positions(self.grid)
        self.assertIsNone(positions)

    def test_is_tile_in_path(self):
        """测试瓦片是否在路径中"""
        power = Tile(0, 0, TileType.POWER_SOURCE, 0)
        straight = Tile(1, 0, TileType.STRAIGHT, 0)
        terminal = Tile(2, 0, TileType.TERMINAL, 0)

        self.grid.set_tile(0, 0, power)
        self.grid.set_tile(1, 0, straight)
        self.grid.set_tile(2, 0, terminal)

        self.assertTrue(self.checker.is_tile_in_path(self.grid, 0, 0))
        self.assertTrue(self.checker.is_tile_in_path(self.grid, 1, 0))
        self.assertTrue(self.checker.is_tile_in_path(self.grid, 2, 0))
        self.assertFalse(self.checker.is_tile_in_path(self.grid, 3, 0))

    def test_is_tile_in_path_no_path(self):
        """测试没有路径时检查瓦片"""
        self.assertFalse(self.checker.is_tile_in_path(self.grid, 0, 0))


class TestConnectivityCheckerPerformance(unittest.TestCase):
    """测试性能要求"""

    def setUp(self):
        """设置测试环境"""
        self.checker = ConnectivityChecker()

    def test_performance_4x4(self):
        """测试4x4网格性能（< 5ms）"""
        grid = GridManager(4)

        # 创建复杂的连通路径
        grid.set_tile(0, 0, Tile(0, 0, TileType.POWER_SOURCE, 0))
        grid.set_tile(1, 0, Tile(1, 0, TileType.STRAIGHT, 0))
        grid.set_tile(2, 0, Tile(2, 0, TileType.CORNER, 0))
        grid.set_tile(2, 1, Tile(2, 1, TileType.STRAIGHT, 90))
        grid.set_tile(2, 2, Tile(2, 2, TileType.CORNER, 90))
        grid.set_tile(1, 2, Tile(1, 2, TileType.STRAIGHT, 0))
        grid.set_tile(0, 2, Tile(0, 2, TileType.TERMINAL, 0))

        # 测试性能
        start = time.perf_counter()
        for _ in range(100):  # 运行100次取平均
            self.checker.check_connectivity(grid)
        end = time.perf_counter()

        avg_time_ms = ((end - start) / 100) * 1000
        print(f"\n4x4 grid average time: {avg_time_ms:.3f}ms")
        self.assertLess(avg_time_ms, 5, "4x4 grid should take less than 5ms")

    def test_performance_8x8(self):
        """测试8x8网格性能（< 20ms）"""
        grid = GridManager(8)

        # 创建较长的路径
        for i in range(7):
            grid.set_tile(i, 0, Tile(i, 0, TileType.STRAIGHT, 0))

        grid.set_tile(0, 0, Tile(0, 0, TileType.POWER_SOURCE, 0))
        grid.set_tile(7, 0, Tile(7, 0, TileType.CORNER, 0))

        for i in range(1, 7):
            grid.set_tile(7, i, Tile(7, i, TileType.STRAIGHT, 90))

        grid.set_tile(7, 7, Tile(7, 7, TileType.TERMINAL, 0))

        # 测试性能
        start = time.perf_counter()
        for _ in range(50):  # 运行50次取平均
            self.checker.check_connectivity(grid)
        end = time.perf_counter()

        avg_time_ms = ((end - start) / 50) * 1000
        print(f"\n8x8 grid average time: {avg_time_ms:.3f}ms")
        self.assertLess(avg_time_ms, 20, "8x8 grid should take less than 20ms")


if __name__ == '__main__':
    unittest.main()
