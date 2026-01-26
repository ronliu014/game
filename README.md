# 电路修复游戏 (Circuit Repair Game)

一款基于 Pygame 的益智解谜游戏，玩家需要通过旋转电路板上的元件来连接电源和终端。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎮 游戏简介

电路修复游戏是一款蒸汽朋克风格的益智游戏。玩家需要在限定时间内，通过旋转电路板上的元件，建立从电源到终端的完整电路路径。

### 核心玩法

- 🔄 **旋转元件**: 点击黑色方块旋转电路元件（90°顺时针）
- ⚡ **连接电路**: 建立从电源（红色）到终端（绿色）的完整路径
- ⏱️ **限时挑战**: 在倒计时结束前完成关卡
- ⭐ **星级评分**: 根据用时和移动次数获得1-3星评价

## 📦 安装说明

### 方式一：运行可执行文件（推荐）

1. 下载最新版本的 `CircuitRepairGame-v1.0.0.zip`
2. 解压到任意目录
3. 双击 `CircuitRepairGame.exe` 启动游戏

### 方式二：从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/circuit-repair-game.git
cd circuit-repair-game

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行游戏
python main.py
```

## 🎯 快速开始

### 游戏操作

| 操作 | 说明 |
|------|------|
| **鼠标左键** | 点击黑色方块旋转元件 |
| **ESC** | 暂停/返回 |
| **F3** | 显示/隐藏调试信息 |

### 难度说明

| 难度 | 时间限制 | 特点 |
|------|---------|------|
| 简单 | 60秒 | 适合新手 |
| 普通 | 45秒 | 标准难度 |
| 困难 | 30秒 | 需要快速思考 |
| 地狱 | 15秒 | 极限挑战 |

## 📊 技术栈

- **游戏引擎**: Pygame 2.6+
- **编程语言**: Python 3.8+
- **测试框架**: pytest
- **打包工具**: PyInstaller

## 📚 文档

- **[用户指南](docs/USER_GUIDE.md)** - 详细的游戏说明和操作指南
- **[构建说明](docs/BUILD.md)** - 如何从源码构建可执行文件
- **[测试指南](docs/TESTING.md)** - 测试说明和测试用例
- **[更新日志](CHANGELOG.md)** - 版本更新记录

## 🛠️ 开发相关

### 构建可执行文件

```bash
# Windows
build.bat

# Linux/Mac
./build.sh
```

详细说明请参考 [构建文档](docs/BUILD.md)

### 运行测试

```bash
pytest tests/ -v
```

详细说明请参考 [测试文档](docs/TESTING.md)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**享受游戏！Have fun! 🎮**
