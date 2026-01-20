"""
文件工具函数单元测试

测试file_utils模块的所有文件操作函数。
"""

import unittest
import tempfile
from pathlib import Path
from src.utils.file_utils import (
    get_project_root,
    safe_path,
    ensure_dir,
    find_resource,
    get_file_size,
    get_file_extension,
    list_files,
    read_text_file,
    write_text_file,
    file_exists,
    dir_exists,
    get_relative_path
)


class TestProjectRoot(unittest.TestCase):
    """测试项目根目录获取"""

    def test_get_project_root(self):
        """测试获取项目根目录"""
        root = get_project_root()
        self.assertIsInstance(root, Path)
        self.assertTrue(root.exists())
        # 项目根目录应该包含src和data目录
        self.assertTrue((root / 'src').exists())
        self.assertTrue((root / 'data').exists())


class TestSafePath(unittest.TestCase):
    """测试安全路径"""

    def test_safe_path_valid(self):
        """测试有效的安全路径"""
        root = get_project_root()
        safe = safe_path('data/levels')
        self.assertTrue(str(safe).startswith(str(root)))

    def test_safe_path_traversal_attack(self):
        """测试路径遍历攻击防护"""
        with self.assertRaises(ValueError):
            safe_path('../../../etc/passwd')


class TestEnsureDir(unittest.TestCase):
    """测试目录创建"""

    def test_ensure_dir_creates_directory(self):
        """测试创建目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / 'test' / 'nested' / 'dir'
            result = ensure_dir(str(test_dir))
            self.assertTrue(result.exists())
            self.assertTrue(result.is_dir())

    def test_ensure_dir_existing_directory(self):
        """测试已存在的目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 第一次创建
            ensure_dir(tmpdir)
            # 第二次应该不报错
            result = ensure_dir(tmpdir)
            self.assertTrue(result.exists())


class TestFindResource(unittest.TestCase):
    """测试资源查找"""

    def test_find_existing_resource(self):
        """测试查找存在的资源"""
        # 查找配置文件
        result = find_resource('game_config.json')
        if result:
            self.assertTrue(result.exists())
            self.assertEqual(result.name, 'game_config.json')

    def test_find_nonexistent_resource(self):
        """测试查找不存在的资源"""
        result = find_resource('nonexistent_file_12345.xyz')
        self.assertIsNone(result)


class TestFileSize(unittest.TestCase):
    """测试文件大小获取"""

    def test_get_file_size(self):
        """测试获取文件大小"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('Hello, World!')
            temp_path = f.name

        try:
            size = get_file_size(temp_path)
            self.assertGreater(size, 0)
        finally:
            Path(temp_path).unlink()

    def test_get_file_size_nonexistent(self):
        """测试获取不存在文件的大小"""
        with self.assertRaises(FileNotFoundError):
            get_file_size('nonexistent_file.txt')


class TestFileExtension(unittest.TestCase):
    """测试文件扩展名获取"""

    def test_get_file_extension(self):
        """测试获取文件扩展名"""
        self.assertEqual(get_file_extension('file.txt'), 'txt')
        self.assertEqual(get_file_extension('file.JSON'), 'json')
        self.assertEqual(get_file_extension('path/to/file.png'), 'png')
        self.assertEqual(get_file_extension('file'), '')


class TestListFiles(unittest.TestCase):
    """测试文件列表"""

    def test_list_files_with_extension(self):
        """测试列出指定扩展名的文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试文件
            (Path(tmpdir) / 'file1.txt').touch()
            (Path(tmpdir) / 'file2.txt').touch()
            (Path(tmpdir) / 'file3.json').touch()

            txt_files = list_files(tmpdir, extension='txt')
            self.assertEqual(len(txt_files), 2)

    def test_list_files_all(self):
        """测试列出所有文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / 'file1.txt').touch()
            (Path(tmpdir) / 'file2.json').touch()

            all_files = list_files(tmpdir)
            self.assertEqual(len(all_files), 2)

    def test_list_files_recursive(self):
        """测试递归列出文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建嵌套目录和文件
            subdir = Path(tmpdir) / 'subdir'
            subdir.mkdir()
            (Path(tmpdir) / 'file1.txt').touch()
            (subdir / 'file2.txt').touch()

            files = list_files(tmpdir, extension='txt', recursive=True)
            self.assertEqual(len(files), 2)

    def test_list_files_nonexistent_directory(self):
        """测试列出不存在目录的文件"""
        files = list_files('nonexistent_directory')
        self.assertEqual(len(files), 0)


class TestReadWriteTextFile(unittest.TestCase):
    """测试文本文件读写"""

    def test_write_and_read_text_file(self):
        """测试写入和读取文本文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / 'test.txt')
            content = 'Hello, World!\n测试内容'

            # 写入
            write_text_file(file_path, content)

            # 读取
            read_content = read_text_file(file_path)
            self.assertEqual(read_content, content)

    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            read_text_file('nonexistent_file.txt')


class TestFileExists(unittest.TestCase):
    """测试文件存在性检查"""

    def test_file_exists(self):
        """测试文件存在检查"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            self.assertTrue(file_exists(temp_path))
        finally:
            Path(temp_path).unlink()

        self.assertFalse(file_exists(temp_path))

    def test_dir_exists(self):
        """测试目录存在检查"""
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertTrue(dir_exists(tmpdir))

        self.assertFalse(dir_exists(tmpdir))


class TestRelativePath(unittest.TestCase):
    """测试相对路径获取"""

    def test_get_relative_path(self):
        """测试获取相对路径"""
        root = get_project_root()
        full_path = root / 'data' / 'config' / 'game_config.json'
        relative = get_relative_path(str(full_path))

        self.assertIsInstance(relative, Path)
        # 相对路径应该不包含根目录
        self.assertNotIn(str(root), str(relative))


if __name__ == '__main__':
    unittest.main()
