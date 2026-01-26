"""
验证打包完整性脚本

检查打包后的程序是否包含所有必要的依赖和资源。
"""

import os
import sys
from pathlib import Path

def verify_package(package_dir: str) -> bool:
    """
    验证打包目录的完整性

    Args:
        package_dir: 打包目录路径（如 dist/CircuitRepairGame）

    Returns:
        bool: 验证是否通过
    """
    package_path = Path(package_dir)

    if not package_path.exists():
        print(f"❌ 错误：打包目录不存在: {package_dir}")
        return False

    print("=" * 60)
    print("📦 打包完整性验证")
    print("=" * 60)
    print()

    checks = []

    # 1. 检查主程序
    exe_name = "CircuitRepairGame.exe" if sys.platform == "win32" else "CircuitRepairGame"
    exe_path = package_path / exe_name
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ 主程序存在: {exe_name} ({size_mb:.1f} MB)")
        checks.append(True)
    else:
        print(f"❌ 主程序不存在: {exe_name}")
        checks.append(False)

    # 2. 检查 _internal 目录
    internal_path = package_path / "_internal"
    if internal_path.exists():
        print(f"✅ 依赖目录存在: _internal/")
        checks.append(True)

        # 统计文件数量
        pyd_files = list(internal_path.glob("*.pyd"))
        dll_files = list(internal_path.glob("*.dll"))
        print(f"   - Python扩展模块: {len(pyd_files)} 个 .pyd 文件")
        print(f"   - 系统库: {len(dll_files)} 个 .dll 文件")
    else:
        print(f"❌ 依赖目录不存在: _internal/")
        checks.append(False)

    # 3. 检查资源目录
    assets_path = internal_path / "assets"
    if assets_path.exists():
        print(f"✅ 资源目录存在: _internal/assets/")
        checks.append(True)

        # 检查子目录
        subdirs = ["sprites", "audio", "fonts"]
        for subdir in subdirs:
            subdir_path = assets_path / subdir
            if subdir_path.exists():
                file_count = len(list(subdir_path.rglob("*.*")))
                print(f"   - {subdir}/: {file_count} 个文件")
    else:
        print(f"❌ 资源目录不存在: _internal/assets/")
        checks.append(False)

    # 4. 检查数据目录
    data_path = internal_path / "data"
    if data_path.exists():
        print(f"✅ 数据目录存在: _internal/data/")
        checks.append(True)

        # 检查子目录
        subdirs = ["config", "levels"]
        for subdir in subdirs:
            subdir_path = data_path / subdir
            if subdir_path.exists():
                file_count = len(list(subdir_path.glob("*.json")))
                print(f"   - {subdir}/: {file_count} 个JSON文件")
    else:
        print(f"❌ 数据目录不存在: _internal/data/")
        checks.append(False)

    # 5. 计算总大小
    total_size = sum(f.stat().st_size for f in package_path.rglob("*") if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    print()
    print(f"📊 总大小: {total_size_mb:.1f} MB")

    # 总结
    print()
    print("=" * 60)
    if all(checks):
        print("✅ 验证通过！打包完整，可以发行。")
        print()
        print("📋 发行说明：")
        print("   1. 目标机器无需安装Python")
        print("   2. 目标机器无需安装任何依赖库")
        print("   3. 解压后直接运行 CircuitRepairGame.exe")
        print("   4. 建议将整个目录打包成zip文件发行")
        print()
        return True
    else:
        print("❌ 验证失败！打包不完整，请检查。")
        print()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        package_dir = sys.argv[1]
    else:
        package_dir = "dist/CircuitRepairGame"

    success = verify_package(package_dir)
    sys.exit(0 if success else 1)
