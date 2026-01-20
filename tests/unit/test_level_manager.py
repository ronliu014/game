"""
Unit tests for LevelManager

Tests level state management, move counting, and win condition checking.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import unittest
import tempfile
import os
import json
from typing import Dict, Any

from src.core.level.level_manager import LevelManager
from src.core.level.level_loader import LevelLoader
from src.core.grid.tile_type import TileType


class TestLevelManagerInitialization(unittest.TestCase):
    """Test LevelManager initialization"""

    def test_init_with_valid_loader(self):
        """测试使用有效加载器初始化"""
        loader = LevelLoader()
        manager = LevelManager(loader)

        self.assertIsNotNone(manager)
        self.assertFalse(manager.has_level_loaded())
        self.assertEqual(manager.get_move_count(), 0)
        self.assertFalse(manager.is_level_completed())

    def test_init_with_none_loader(self):
        """测试使用None加载器初始化应该失败"""
        with self.assertRaises(ValueError) as context:
            LevelManager(None)

        self.assertIn("cannot be None", str(context.exception))


class TestLevelManagerLoading(unittest.TestCase):
    """Test level loading functionality"""

    def setUp(self):
        self.loader = LevelLoader()
        self.manager = LevelManager(self.loader)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: Dict[str, Any]) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def _create_simple_level_data(self) -> Dict[str, Any]:
        """创建简单关卡数据"""
        return {
            "level_id": "test_001",
            "version": "1.0",
            "name": "测试关卡",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 3, "y": 0, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 90}
                ]
            }
        }

    def test_load_valid_level(self):
        """测试加载有效关卡"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)

        success = self.manager.load_level(filepath)

        self.assertTrue(success)
        self.assertTrue(self.manager.has_level_loaded())
        self.assertEqual(self.manager.get_current_level_id(), "test_001")
        self.assertEqual(self.manager.get_grid_size(), 4)
        self.assertEqual(self.manager.get_move_count(), 0)
        self.assertFalse(self.manager.is_level_completed())

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        success = self.manager.load_level("nonexistent.json")

        self.assertFalse(success)
        self.assertFalse(self.manager.has_level_loaded())

    def test_load_empty_filepath(self):
        """测试加载空文件路径"""
        success = self.manager.load_level("")

        self.assertFalse(success)
        self.assertFalse(self.manager.has_level_loaded())

    def test_load_invalid_json(self):
        """测试加载无效JSON"""
        filepath = os.path.join(self.temp_dir, "invalid.json")
        with open(filepath, 'w') as f:
            f.write("{ invalid json }")

        success = self.manager.load_level(filepath)

        self.assertFalse(success)
        self.assertFalse(self.manager.has_level_loaded())

    def test_get_level_data(self):
        """测试获取关卡数据"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)

        self.manager.load_level(filepath)
        data = self.manager.get_level_data()

        self.assertIsNotNone(data)
        self.assertEqual(data.level_id, "test_001")
        self.assertEqual(data.name, "测试关卡")
        self.assertEqual(data.difficulty, 1)
        self.assertEqual(data.grid_size, 4)

    def test_get_level_data_no_level_loaded(self):
        """测试未加载关卡时获取数据"""
        data = self.manager.get_level_data()

        self.assertIsNone(data)


class TestLevelManagerRotation(unittest.TestCase):
    """Test tile rotation functionality"""

    def setUp(self):
        self.loader = LevelLoader()
        self.manager = LevelManager(self.loader)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: Dict[str, Any]) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def _create_simple_level_data(self) -> Dict[str, Any]:
        """创建简单关卡数据"""
        return {
            "level_id": "test_001",
            "version": "1.0",
            "name": "测试关卡",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 3, "y": 0, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 90}
                ]
            }
        }

    def test_rotate_tile_success(self):
        """测试成功旋转瓦片"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        success = self.manager.rotate_tile(1, 0)

        self.assertTrue(success)
        self.assertEqual(self.manager.get_move_count(), 1)

    def test_rotate_tile_increments_move_count(self):
        """测试旋转瓦片增加移动计数"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(2, 0)
        self.manager.rotate_tile(1, 0)

        self.assertEqual(self.manager.get_move_count(), 3)

    def test_rotate_tile_no_level_loaded(self):
        """测试未加载关卡时旋转瓦片"""
        success = self.manager.rotate_tile(1, 0)

        self.assertFalse(success)
        self.assertEqual(self.manager.get_move_count(), 0)

    def test_rotate_nonexistent_tile(self):
        """测试旋转不存在的瓦片"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        success = self.manager.rotate_tile(5, 5)

        self.assertFalse(success)
        self.assertEqual(self.manager.get_move_count(), 0)

    def test_rotate_non_rotatable_tile(self):
        """测试旋转不可旋转的瓦片（电源）"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        success = self.manager.rotate_tile(0, 0)  # Power source

        self.assertFalse(success)
        self.assertEqual(self.manager.get_move_count(), 0)

    def test_rotate_after_completion(self):
        """测试完成后不能旋转"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        # Complete the level
        self.manager.rotate_tile(1, 0)  # Rotate to 180
        self.manager.rotate_tile(1, 0)  # Rotate to 270
        self.manager.rotate_tile(1, 0)  # Rotate to 0 (correct)
        self.manager.rotate_tile(2, 0)  # Rotate to 180
        self.manager.rotate_tile(2, 0)  # Rotate to 270
        self.manager.rotate_tile(2, 0)  # Rotate to 0 (correct)

        # Check if completed
        is_completed = self.manager.check_win_condition()
        self.assertTrue(is_completed)

        # Try to rotate after completion
        move_count_before = self.manager.get_move_count()
        success = self.manager.rotate_tile(1, 0)

        self.assertFalse(success)
        self.assertEqual(self.manager.get_move_count(), move_count_before)


class TestLevelManagerReset(unittest.TestCase):
    """Test level reset functionality"""

    def setUp(self):
        self.loader = LevelLoader()
        self.manager = LevelManager(self.loader)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: Dict[str, Any]) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def _create_simple_level_data(self) -> Dict[str, Any]:
        """创建简单关卡数据"""
        return {
            "level_id": "test_001",
            "version": "1.0",
            "name": "测试关卡",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 3, "y": 0, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 90}
                ]
            }
        }

    def test_reset_level_success(self):
        """测试成功重置关卡"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        # Make some moves
        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(2, 0)
        self.assertEqual(self.manager.get_move_count(), 2)

        # Reset
        success = self.manager.reset_level()

        self.assertTrue(success)
        self.assertEqual(self.manager.get_move_count(), 0)

    def test_reset_level_restores_initial_state(self):
        """测试重置关卡恢复初始状态"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        grid = self.manager.get_grid()
        initial_rotation_1 = grid.get_tile(1, 0).rotation
        initial_rotation_2 = grid.get_tile(2, 0).rotation

        # Make some moves
        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(2, 0)

        # Verify rotations changed
        self.assertNotEqual(grid.get_tile(1, 0).rotation, initial_rotation_1)
        self.assertNotEqual(grid.get_tile(2, 0).rotation, initial_rotation_2)

        # Reset
        self.manager.reset_level()

        # Verify rotations restored
        self.assertEqual(grid.get_tile(1, 0).rotation, initial_rotation_1)
        self.assertEqual(grid.get_tile(2, 0).rotation, initial_rotation_2)

    def test_reset_level_no_level_loaded(self):
        """测试未加载关卡时重置"""
        success = self.manager.reset_level()

        self.assertFalse(success)

    def test_reload_level(self):
        """测试重新加载关卡"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        # Make some moves
        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(2, 0)
        self.assertEqual(self.manager.get_move_count(), 2)

        # Reload
        success = self.manager.reload_level()

        self.assertTrue(success)
        self.assertEqual(self.manager.get_move_count(), 0)
        self.assertEqual(self.manager.get_current_level_id(), "test_001")

    def test_reload_level_no_level_loaded(self):
        """测试未加载关卡时重新加载"""
        success = self.manager.reload_level()

        self.assertFalse(success)


class TestLevelManagerWinCondition(unittest.TestCase):
    """Test win condition checking"""

    def setUp(self):
        self.loader = LevelLoader()
        self.manager = LevelManager(self.loader)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: Dict[str, Any]) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def _create_simple_level_data(self) -> Dict[str, Any]:
        """创建简单关卡数据"""
        return {
            "level_id": "test_001",
            "version": "1.0",
            "name": "测试关卡",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 3, "y": 0, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 90}
                ]
            }
        }

    def test_check_win_condition_not_completed(self):
        """测试检查未完成的关卡"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        is_completed = self.manager.check_win_condition()

        self.assertFalse(is_completed)
        self.assertFalse(self.manager.is_level_completed())

    def test_check_win_condition_completed(self):
        """测试检查已完成的关卡"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        # Complete the level
        self.manager.rotate_tile(1, 0)  # Rotate to 180
        self.manager.rotate_tile(1, 0)  # Rotate to 270
        self.manager.rotate_tile(1, 0)  # Rotate to 0 (correct)
        self.manager.rotate_tile(2, 0)  # Rotate to 180
        self.manager.rotate_tile(2, 0)  # Rotate to 270
        self.manager.rotate_tile(2, 0)  # Rotate to 0 (correct)

        is_completed = self.manager.check_win_condition()

        self.assertTrue(is_completed)
        self.assertTrue(self.manager.is_level_completed())

    def test_check_win_condition_no_level_loaded(self):
        """测试未加载关卡时检查胜利条件"""
        is_completed = self.manager.check_win_condition()

        self.assertFalse(is_completed)

    def test_get_connected_path_when_completed(self):
        """测试完成时获取连接路径"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        # Complete the level
        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(1, 0)
        self.manager.rotate_tile(2, 0)
        self.manager.rotate_tile(2, 0)
        self.manager.rotate_tile(2, 0)

        path = self.manager.get_connected_path()

        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)  # Power source + 2 straights + terminal

    def test_get_connected_path_when_not_completed(self):
        """测试未完成时获取连接路径"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        path = self.manager.get_connected_path()

        self.assertIsNone(path)

    def test_get_connected_path_no_level_loaded(self):
        """测试未加载关卡时获取连接路径"""
        path = self.manager.get_connected_path()

        self.assertIsNone(path)


class TestLevelManagerGetters(unittest.TestCase):
    """Test getter methods"""

    def setUp(self):
        self.loader = LevelLoader()
        self.manager = LevelManager(self.loader)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_temp_level(self, filename: str, data: Dict[str, Any]) -> str:
        """创建临时关卡文件"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def _create_simple_level_data(self) -> Dict[str, Any]:
        """创建简单关卡数据"""
        return {
            "level_id": "test_001",
            "version": "1.0",
            "name": "测试关卡",
            "difficulty": 1,
            "grid_size": 4,
            "solution": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "power_source", "rotation": 0},
                    {"x": 1, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 2, "y": 0, "type": "straight", "rotation": 0},
                    {"x": 3, "y": 0, "type": "terminal", "rotation": 0}
                ]
            },
            "initial_state": {
                "rotated_tiles": [
                    {"x": 1, "y": 0, "rotation": 90},
                    {"x": 2, "y": 0, "rotation": 90}
                ]
            }
        }

    def test_get_grid(self):
        """测试获取网格"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        grid = self.manager.get_grid()

        self.assertIsNotNone(grid)
        self.assertEqual(grid.grid_size, 4)

    def test_get_grid_no_level_loaded(self):
        """测试未加载关卡时获取网格"""
        grid = self.manager.get_grid()

        self.assertIsNone(grid)

    def test_get_current_level_id(self):
        """测试获取当前关卡ID"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        level_id = self.manager.get_current_level_id()

        self.assertEqual(level_id, "test_001")

    def test_get_current_level_id_no_level_loaded(self):
        """测试未加载关卡时获取ID"""
        level_id = self.manager.get_current_level_id()

        self.assertIsNone(level_id)

    def test_get_grid_size(self):
        """测试获取网格大小"""
        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        grid_size = self.manager.get_grid_size()

        self.assertEqual(grid_size, 4)

    def test_get_grid_size_no_level_loaded(self):
        """测试未加载关卡时获取网格大小"""
        grid_size = self.manager.get_grid_size()

        self.assertIsNone(grid_size)

    def test_has_level_loaded(self):
        """测试检查是否加载关卡"""
        self.assertFalse(self.manager.has_level_loaded())

        level_data = self._create_simple_level_data()
        filepath = self._create_temp_level("test_level.json", level_data)
        self.manager.load_level(filepath)

        self.assertTrue(self.manager.has_level_loaded())


if __name__ == '__main__':
    unittest.main()
