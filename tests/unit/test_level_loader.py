"""
关卡加载器单元测试

测试LevelLoader类的所有功能。
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from src.core.level.level_loader import LevelLoader, LevelData
from src.core.grid.tile_type import TileType


class TestLevelDataInitialization(unittest.TestCase):
    """测试关卡数据初始化"""

    def test_level_data_creation(self):
        """测试创建关卡数据"""
        data = LevelData(
            level_id="001",
            version="1.0",
            name="Test Level",
            difficulty=1,
            grid_size=4,
            solution_tiles=[],
            rotated_tiles=[]
        )

        self.assertEqual(data.level_id, "001")
        self.assertEqual(data.version, "1.0")
        self.assertEqual(data.name, "Test Level")
        self.assertEqual(data.difficulty, 1)
        self.assertEqual(data.grid_size, 4)
        self.assertEqual(len(data.solution_tiles), 0)
        self.assertEqual(len(data.rotated_tiles), 0)

    def test_level_data_repr(self):
        """测试关卡数据字符串表示"""
        data = LevelData("001", "1.0", "Test", 1, 4, [], [])
        repr_str = repr(data)

        self.assertIn("001", repr_str)
        self.assertIn("Test", repr_str)
        self.assertIn("difficulty=1", repr_str)
        self.assertIn("grid_size=4", repr_str)


class TestLevelLoaderInitialization(unittest.TestCase):
    """测试关卡加载器初始化"""

    def test_loader_creation(self):
        """测试创建加载器"""
        loader = LevelLoader()
        self.assertIsNotNone(loader)


class TestLevelLoaderValidation(unittest.TestCase):
    """测试关卡数据验证"""

    def setUp(self):
        """设置测试环境"""
        self.loader = LevelLoader()

    def test_valid_level_data(self):
        """测试有效的关卡数据"""
        data = {
            "level_id": "001",
            "version": "1.0",
            "name": "Test",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {"tiles": []},
            "initial_state": {"rotated_tiles": []}
        }

        self.assertTrue(self.loader._validate_level_data(data))

    def test_missing_level_id(self):
        """测试缺少level_id"""
        data = {
            "version": "1.0",
            "name": "Test",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {"tiles": []},
            "initial_state": {"rotated_tiles": []}
        }

        self.assertFalse(self.loader._validate_level_data(data))

    def test_missing_solution(self):
        """测试缺少solution"""
        data = {
            "level_id": "001",
            "version": "1.0",
            "name": "Test",
            "difficulty": 1,
            "grid_size": 4,
            "initial_state": {"rotated_tiles": []}
        }

        self.assertFalse(self.loader._validate_level_data(data))

    def test_missing_tiles_in_solution(self):
        """测试solution中缺少tiles"""
        data = {
            "level_id": "001",
            "version": "1.0",
            "name": "Test",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {},
            "initial_state": {"rotated_tiles": []}
        }

        self.assertFalse(self.loader._validate_level_data(data))

    def test_invalid_grid_size(self):
        """测试无效的网格大小"""
        data = {
            "level_id": "001",
            "version": "1.0",
            "name": "Test",
            "difficulty": 1,
            "grid_size": 1,  # 太小
            "solution": {"tiles": []},
            "initial_state": {"rotated_tiles": []}
        }

        self.assertFalse(self.loader._validate_level_data(data))

    def test_invalid_difficulty(self):
        """测试无效的难度等级"""
        data = {
            "level_id": "001",
            "version": "1.0",
            "name": "Test",
            "difficulty": 6,  # 超出范围
            "grid_size": 4,
            "solution": {"tiles": []},
            "initial_state": {"rotated_tiles": []}
        }

        self.assertFalse(self.loader._validate_level_data(data))


class TestLevelLoaderLoading(unittest.TestCase):
    """测试关卡加载"""

    def setUp(self):
        """设置测试环境"""
        self.loader = LevelLoader()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """清理测试环境"""
        # 清理临时文件
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: dict) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def test_load_simple_level(self):
        """测试加载简单关卡"""
        level_data = {
            "level_id": "001",
            "version": "1.0",
            "name": "Simple Test",
            "difficulty": 1,
            "grid_size": 3,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": []
            }
        }

        filepath = self._create_temp_level("test_level.json", level_data)
        grid = self.loader.load_level(filepath)

        self.assertIsNotNone(grid)
        self.assertEqual(grid.grid_size, 3)
        self.assertEqual(grid.get_tile_count(), 3)
        self.assertIsNotNone(grid.get_power_source())
        self.assertIsNotNone(grid.get_terminal())

    def test_load_level_with_rotations(self):
        """测试加载带初始旋转的关卡"""
        level_data = {
            "level_id": "002",
            "version": "1.0",
            "name": "Rotation Test",
            "difficulty": 2,
            "grid_size": 4,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "corner", "rotation": 90},
                    {"x": 2, "y": 1, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 180}
                ]
            }
        }

        filepath = self._create_temp_level("test_rotations.json", level_data)
        grid = self.loader.load_level(filepath)

        self.assertIsNotNone(grid)
        # 检查初始错误旋转已应用
        self.assertEqual(grid.get_tile(1, 0).rotation, 90)
        self.assertEqual(grid.get_tile(2, 0).rotation, 180)

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        grid = self.loader.load_level("nonexistent_file.json")
        self.assertIsNone(grid)

    def test_load_invalid_json(self):
        """测试加载无效的JSON"""
        filepath = os.path.join(self.temp_dir, "invalid.json")
        with open(filepath, 'w') as f:
            f.write("{ invalid json }")

        grid = self.loader.load_level(filepath)
        self.assertIsNone(grid)

    def test_load_invalid_level_data(self):
        """测试加载无效的关卡数据"""
        level_data = {
            "level_id": "003",
            # 缺少必需字段
            "version": "1.0"
        }

        filepath = self._create_temp_level("invalid_level.json", level_data)
        grid = self.loader.load_level(filepath)
        self.assertIsNone(grid)


class TestLevelLoaderGridCreation(unittest.TestCase):
    """测试网格创建"""

    def setUp(self):
        """设置测试环境"""
        self.loader = LevelLoader()

    def test_create_grid_from_level_data(self):
        """测试从关卡数据创建网格"""
        level_data = LevelData(
            level_id="001",
            version="1.0",
            name="Test",
            difficulty=1,
            grid_size=4,
            solution_tiles=[
                {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                {"x": 2, "y": 0, "type": "terminal", "rotation": 0}
            ],
            rotated_tiles=[]
        )

        grid = self.loader._create_grid(level_data)

        self.assertEqual(grid.grid_size, 4)
        self.assertEqual(grid.get_tile_count(), 3)

        # 检查瓦片类型
        self.assertEqual(grid.get_tile(0, 0).tile_type, TileType.POWER_SOURCE)
        self.assertEqual(grid.get_tile(1, 0).tile_type, TileType.STRAIGHT)
        self.assertEqual(grid.get_tile(2, 0).tile_type, TileType.TERMINAL)

    def test_tile_clickability(self):
        """测试瓦片可点击性"""
        level_data = LevelData(
            level_id="001",
            version="1.0",
            name="Test",
            difficulty=1,
            grid_size=4,
            solution_tiles=[
                {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                {"x": 2, "y": 0, "type": "terminal", "rotation": 0}
            ],
            rotated_tiles=[]
        )

        grid = self.loader._create_grid(level_data)

        # 电源端和终端不可点击
        self.assertFalse(grid.get_tile(0, 0).is_clickable)
        self.assertFalse(grid.get_tile(2, 0).is_clickable)

        # 直线瓦片可点击
        self.assertTrue(grid.get_tile(1, 0).is_clickable)

    def test_initial_state_saved(self):
        """测试初始状态已保存"""
        level_data = LevelData(
            level_id="001",
            version="1.0",
            name="Test",
            difficulty=1,
            grid_size=4,
            solution_tiles=[
                {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                {"x": 1, "y": 0, "type": "straight", "rotation": 0}
            ],
            rotated_tiles=[
                {"x": 1, "y": 0, "rotation": 90}
            ]
        )

        grid = self.loader._create_grid(level_data)

        # 修改旋转
        grid.rotate_tile(1, 0)
        self.assertEqual(grid.get_tile(1, 0).rotation, 180)

        # 重置应该恢复到初始错误状态（90度）
        grid.reset_grid()
        self.assertEqual(grid.get_tile(1, 0).rotation, 90)


class TestLevelLoaderComplexLevels(unittest.TestCase):
    """测试复杂关卡加载"""

    def setUp(self):
        """设置测试环境"""
        self.loader = LevelLoader()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """清理测试环境"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: dict) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def test_load_complex_level(self):
        """测试加载复杂关卡"""
        level_data = {
            "level_id": "005",
            "version": "1.0",
            "name": "Complex Path",
            "difficulty": 3,
            "grid_size": 5,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "corner", "rotation": 90},
                    {"x": 2, "y": 1, "type": "straight", "rotation": 90},
                    {"x": 2, "y": 2, "type": "corner", "rotation": 270},
                    {"x": 3, "y": 2, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 180},
                    {"x": 2, "y": 1, "rotation": 0}
                ]
            }
        }

        filepath = self._create_temp_level("complex_level.json", level_data)
        grid = self.loader.load_level(filepath)

        self.assertIsNotNone(grid)
        self.assertEqual(grid.grid_size, 5)
        self.assertEqual(grid.get_tile_count(), 6)

        # 检查所有瓦片都已放置
        self.assertIsNotNone(grid.get_tile(0, 0))
        self.assertIsNotNone(grid.get_tile(1, 0))
        self.assertIsNotNone(grid.get_tile(2, 0))
        self.assertIsNotNone(grid.get_tile(2, 1))
        self.assertIsNotNone(grid.get_tile(2, 2))
        self.assertIsNotNone(grid.get_tile(3, 2))

        # 检查初始旋转
        self.assertEqual(grid.get_tile(1, 0).rotation, 90)
        self.assertEqual(grid.get_tile(2, 0).rotation, 180)
        self.assertEqual(grid.get_tile(2, 1).rotation, 0)


if __name__ == '__main__':
    unittest.main()
