"""环境验证脚本

用途：验证开发环境是否正确配置
运行：python tools/scripts/verify_environment.py
"""
import sys
import importlib
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    print(f"  路径: {sys.executable}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ 警告: Python版本过低，需要3.8+")
        return False
    return True


def check_package(package_name, import_name=None, min_version=None):
    """检查包是否安装

    Args:
        package_name: 包名称（用于显示）
        import_name: 导入名称（如果与包名不同）
        min_version: 最低版本要求
    """
    if import_name is None:
        import_name = package_name

    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')

        # 特殊处理PIL
        if import_name == 'PIL':
            from PIL import Image
            version = Image.__version__

        print(f"✓ {package_name}: {version}")
        return True
    except ImportError:
        print(f"✗ {package_name}: 未安装")
        return False
    except Exception as e:
        print(f"✗ {package_name}: 检查失败 ({e})")
        return False


def check_conda_environment():
    """检查是否在conda环境中"""
    conda_prefix = Path(sys.prefix)
    conda_env_name = conda_prefix.name

    print(f"✓ Conda环境: {conda_env_name}")
    print(f"  路径: {conda_prefix}")

    if conda_env_name != "Game":
        print("⚠ 警告: 当前不在Game环境中")
        print("  请运行: conda activate Game")
        return False
    return True


def check_project_structure():
    """检查项目目录结构"""
    project_root = Path(__file__).parent.parent.parent

    required_dirs = [
        'docs',
        'docs/specifications',
        'tools',
        'tools/scripts'
    ]

    all_exist = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ (不存在)")
            all_exist = False

    return all_exist


def main():
    """主函数"""
    print("=" * 60)
    print("电路板修复游戏 - 环境验证")
    print("=" * 60)
    print()

    # 检查Python版本
    print("【Python环境】")
    python_ok = check_python_version()
    print()

    # 检查Conda环境
    print("【Conda环境】")
    conda_ok = check_conda_environment()
    print()

    # 检查核心依赖
    print("【核心依赖】")
    core_deps = [
        ('pygame', 'pygame'),
        ('numpy', 'numpy'),
        ('Pillow', 'PIL'),
    ]

    core_ok = all(check_package(name, import_name) for name, import_name in core_deps)
    print()

    # 检查开发工具
    print("【开发工具】")
    dev_tools = [
        ('pytest', 'pytest'),
        ('black', 'black'),
        ('pylint', 'pylint'),
        ('mypy', 'mypy'),
        ('isort', 'isort'),
    ]

    dev_ok = all(check_package(name, import_name) for name, import_name in dev_tools)
    print()

    # 检查项目结构
    print("【项目结构】")
    structure_ok = check_project_structure()
    print()

    # 总结
    print("=" * 60)
    print("验证结果")
    print("=" * 60)

    results = {
        "Python环境": python_ok,
        "Conda环境": conda_ok,
        "核心依赖": core_ok,
        "开发工具": dev_ok,
        "项目结构": structure_ok,
    }

    for name, status in results.items():
        status_str = "✓ 通过" if status else "✗ 失败"
        print(f"{name}: {status_str}")

    print()

    if all(results.values()):
        print("🎉 环境配置完成！可以开始开发了。")
        return 0
    else:
        print("⚠️  环境配置不完整，请参考 docs/specifications/08_环境配置指南.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())
