# 构建说明 (Build Instructions)

本文档说明如何将电路修复游戏打包为可执行文件。

This document explains how to package the Circuit Repair Game as an executable.

---

## 📋 前置要求 (Prerequisites)

### Windows

- Python 3.8+ (推荐使用 conda 环境 `Game`)
- PyInstaller (`pip install pyinstaller`)
- 所有项目依赖 (`pip install -r requirements.txt`)

### Linux/Mac

- Python 3.8+
- PyInstaller (`pip3 install pyinstaller`)
- 所有项目依赖 (`pip3 install -r requirements.txt`)

---

## 🚀 快速构建 (Quick Build)

### Windows

```bash
# 方式一：使用构建脚本（推荐）
build.bat

# 方式二：手动构建
conda activate Game
pyinstaller circuit_repair_game.spec
```

### Linux/Mac

```bash
# 方式一：使用构建脚本（推荐）
./build.sh

# 方式二：手动构建
pyinstaller circuit_repair_game.spec
```

---

## 📦 构建输出 (Build Output)

构建完成后，输出文件位于：

After building, the output files are located at:

```
dist/
└── CircuitRepairGame/
    ├── CircuitRepairGame.exe    # Windows 可执行文件
    ├── CircuitRepairGame         # Linux/Mac 可执行文件
    ├── assets/                   # 游戏资源
    ├── data/                     # 游戏数据
    └── [其他依赖文件]
```

---

## 🧪 测试构建 (Test Build)

### Windows

```bash
cd dist\CircuitRepairGame
CircuitRepairGame.exe
```

### Linux/Mac

```bash
cd dist/CircuitRepairGame
./CircuitRepairGame
```

---

## 📤 发布准备 (Release Preparation)

### 创建发布包 (Create Release Package)

#### Windows (ZIP)

```bash
# 进入 dist 目录
cd dist

# 创建 ZIP 文件
powershell Compress-Archive -Path CircuitRepairGame -DestinationPath CircuitRepairGame-v1.0.0-windows.zip
```

#### Linux/Mac (tar.gz)

```bash
# 进入 dist 目录
cd dist

# 创建 tar.gz 文件
tar -czf CircuitRepairGame-v1.0.0-linux.tar.gz CircuitRepairGame/
```

### 发布包内容检查 (Release Package Checklist)

确保发布包包含以下内容：

- ✅ 可执行文件 (CircuitRepairGame.exe / CircuitRepairGame)
- ✅ assets/ 目录（游戏资源）
- ✅ data/ 目录（配置和关卡数据）
- ✅ 所有依赖库文件
- ✅ README.md（用户文档）
- ✅ LICENSE（许可证）

---

## 🔧 高级配置 (Advanced Configuration)

### 单文件模式 (Single-File Mode)

如果需要创建单个可执行文件（启动较慢但分发更方便），编辑 `circuit_repair_game.spec`：

1. 注释掉当前的 `COLLECT` 配置
2. 取消注释文件末尾的单文件 `EXE` 配置
3. 重新构建

### 自定义图标 (Custom Icon)

1. 将图标文件放置在 `assets/icon.ico`
2. 重新构建（spec 文件会自动检测）

### 减小文件大小 (Reduce File Size)

在 `circuit_repair_game.spec` 中：

1. 添加更多排除项到 `excludes` 列表
2. 启用 UPX 压缩（`upx=True`）
3. 移除不需要的资源文件

---

## ❓ 常见问题 (FAQ)

### Q: 构建失败，提示找不到模块？

A: 确保所有依赖都已安装：
```bash
pip install -r requirements.txt
```

### Q: 可执行文件启动很慢？

A: 这是正常现象。首次启动需要解压资源。可以考虑使用目录模式而非单文件模式。

### Q: 可执行文件体积很大？

A: PyInstaller 会打包所有依赖。可以通过以下方式减小体积：
- 使用虚拟环境，只安装必要的包
- 在 spec 文件中排除不需要的模块
- 启用 UPX 压缩

### Q: 杀毒软件报毒？

A: 这是误报。PyInstaller 打包的程序可能被某些杀毒软件误判。可以：
- 添加到白名单
- 使用代码签名证书签名可执行文件

### Q: 如何在其他电脑上运行？

A: 打包后的程序是独立的，可以直接在其他电脑上运行，无需安装 Python。

---

## 📝 构建日志 (Build Log)

构建过程中的日志文件：

- `build/` - 构建临时文件
- `dist/` - 最终输出文件
- `*.spec` - PyInstaller 配置文件

---

## 🔗 相关文档 (Related Documentation)

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [项目 README](README.md)
- [用户指南](USER_GUIDE.md)
- [更新日志](CHANGELOG.md)

---

**最后更新**: 2026-01-24
