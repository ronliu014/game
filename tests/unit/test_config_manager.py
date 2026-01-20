"""
配置管理系统单元测试

测试ConfigManager的各项功能，确保配置加载、访问和保存正常工作。
"""

import unittest
import json
import tempfile
from pathlib import Path
from src.config.config_manager import ConfigManager
from src.config.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class TestConfigManager(unittest.TestCase):
    """测试配置管理器"""

    def setUp(self):
        """测试前准备"""
        # 重置单例状态
        ConfigManager._instance = None
        ConfigManager._initialized = False

    def test_singleton_pattern(self):
        """测试单例模式"""
        config1 = ConfigManager.get_instance()
        config2 = ConfigManager.get_instance()

        self.assertIs(config1, config2)
        self.assertEqual(id(config1), id(config2))

    def test_initialize_with_existing_config(self):
        """测试使用现有配置文件初始化"""
        config = ConfigManager.initialize('data/config/game_config.json')

        self.assertIsNotNone(config)
        self.assertTrue(ConfigManager._initialized)

    def test_initialize_with_missing_config(self):
        """测试配置文件不存在时使用默认配置"""
        config = ConfigManager.initialize('nonexistent_config.json')

        self.assertIsNotNone(config)
        # 应该加载默认配置
        self.assertEqual(config.get('window.width'), WINDOW_WIDTH)
        self.assertEqual(config.get('window.height'), WINDOW_HEIGHT)

    def test_load_config_success(self):
        """测试成功加载配置文件"""
        config = ConfigManager.get_instance()
        config.load_config('data/config/game_config.json')

        # 验证配置已加载
        self.assertIsNotNone(config.get('window'))
        self.assertIsNotNone(config.get('grid'))

    def test_load_config_file_not_found(self):
        """测试加载不存在的配置文件"""
        config = ConfigManager.get_instance()

        with self.assertRaises(FileNotFoundError):
            config.load_config('nonexistent_file.json')

    def test_load_config_invalid_json(self):
        """测试加载无效的JSON文件"""
        # 创建临时的无效JSON文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{ invalid json }')
            temp_path = f.name

        try:
            config = ConfigManager.get_instance()
            with self.assertRaises(json.JSONDecodeError):
                config.load_config(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_get_simple_key(self):
        """测试获取简单键值"""
        config = ConfigManager.initialize('data/config/game_config.json')

        window_config = config.get('window')
        self.assertIsNotNone(window_config)
        self.assertIsInstance(window_config, dict)

    def test_get_nested_key(self):
        """测试获取嵌套键值（点分隔路径）"""
        config = ConfigManager.initialize('data/config/game_config.json')

        width = config.get('window.width')
        self.assertEqual(width, 800)

        fps = config.get('window.fps')
        self.assertEqual(fps, 60)

    def test_get_with_default(self):
        """测试获取不存在的键时返回默认值"""
        config = ConfigManager.initialize('data/config/game_config.json')

        # 不存在的键应返回默认值
        value = config.get('nonexistent.key', 'default_value')
        self.assertEqual(value, 'default_value')

        # 深层不存在的键
        value = config.get('window.nonexistent.deep.key', 999)
        self.assertEqual(value, 999)

    def test_set_simple_key(self):
        """测试设置简单键值"""
        config = ConfigManager.get_instance()
        config._load_default_config()

        config.set('test_key', 'test_value')
        self.assertEqual(config.get('test_key'), 'test_value')

    def test_set_nested_key(self):
        """测试设置嵌套键值"""
        config = ConfigManager.get_instance()
        config._load_default_config()

        config.set('window.width', 1024)
        self.assertEqual(config.get('window.width'), 1024)

        # 设置深层嵌套键
        config.set('new.nested.key', 'value')
        self.assertEqual(config.get('new.nested.key'), 'value')

    def test_get_all(self):
        """测试获取所有配置"""
        config = ConfigManager.initialize('data/config/game_config.json')

        all_config = config.get_all()
        self.assertIsInstance(all_config, dict)
        self.assertIn('window', all_config)
        self.assertIn('grid', all_config)

        # 确保返回的是副本
        all_config['test'] = 'modified'
        self.assertIsNone(config.get('test'))

    def test_has_key(self):
        """测试检查键是否存在"""
        config = ConfigManager.initialize('data/config/game_config.json')

        # 存在的键
        self.assertTrue(config.has('window'))
        self.assertTrue(config.has('window.width'))

        # 不存在的键
        self.assertFalse(config.has('nonexistent'))
        self.assertFalse(config.has('window.nonexistent'))

    def test_save_config(self):
        """测试保存配置到文件"""
        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            config = ConfigManager.get_instance()
            config._load_default_config()
            config.set('test.key', 'test_value')

            # 保存配置
            config.save(temp_path)

            # 验证文件已创建
            self.assertTrue(Path(temp_path).exists())

            # 加载保存的配置验证内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)

            self.assertEqual(saved_config['test']['key'], 'test_value')
        finally:
            Path(temp_path).unlink()

    def test_save_without_path(self):
        """测试没有指定路径时保存配置"""
        config = ConfigManager.get_instance()
        config._load_default_config()

        # 没有配置文件路径应该抛出异常
        with self.assertRaises(ValueError):
            config.save()

    def test_reload_config(self):
        """测试重新加载配置"""
        config = ConfigManager.initialize('data/config/game_config.json')

        original_width = config.get('window.width')

        # 修改配置
        config.set('window.width', 1024)
        self.assertEqual(config.get('window.width'), 1024)

        # 重新加载应该恢复原始值
        config.reload()
        self.assertEqual(config.get('window.width'), original_width)

    def test_reload_without_path(self):
        """测试没有配置文件路径时重新加载"""
        config = ConfigManager.get_instance()
        config._load_default_config()

        with self.assertRaises(ValueError):
            config.reload()

    def test_default_config_values(self):
        """测试默认配置值"""
        config = ConfigManager.get_instance()
        config._load_default_config()

        # 验证默认值
        self.assertEqual(config.get('window.width'), WINDOW_WIDTH)
        self.assertEqual(config.get('window.height'), WINDOW_HEIGHT)
        self.assertEqual(config.get('window.fps'), FPS)

    def test_repr(self):
        """测试字符串表示"""
        config = ConfigManager.initialize('data/config/game_config.json')

        repr_str = repr(config)
        self.assertIn('ConfigManager', repr_str)
        self.assertIn('config_path', repr_str)


class TestConfigManagerIntegration(unittest.TestCase):
    """配置管理器集成测试"""

    def setUp(self):
        """测试前准备"""
        ConfigManager._instance = None
        ConfigManager._initialized = False

    def test_full_workflow(self):
        """测试完整的配置管理工作流"""
        # 1. 初始化
        config = ConfigManager.initialize('data/config/game_config.json')

        # 2. 读取配置
        window_width = config.get('window.width')
        self.assertIsNotNone(window_width)

        # 3. 修改配置
        config.set('window.width', 1024)
        self.assertEqual(config.get('window.width'), 1024)

        # 4. 创建临时文件保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            config.save(temp_path)

            # 5. 重新加载验证
            config2 = ConfigManager.get_instance()
            config2.load_config(temp_path)
            self.assertEqual(config2.get('window.width'), 1024)
        finally:
            Path(temp_path).unlink()

    def test_multiple_instances_share_state(self):
        """测试多个实例共享状态"""
        config1 = ConfigManager.initialize('data/config/game_config.json')
        config1.set('test.value', 123)

        config2 = ConfigManager.get_instance()
        self.assertEqual(config2.get('test.value'), 123)


if __name__ == '__main__':
    unittest.main()
