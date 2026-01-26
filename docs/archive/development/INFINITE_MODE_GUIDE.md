# 无限关卡模式使用指南
# Infinite Level Mode Guide

## 📋 概述 (Overview)

游戏现已完全采用**程序化关卡生成系统**，提供无限的关卡挑战。每个关卡都是实时动态生成的，永不重复！

The game now uses a **procedural level generation system**, providing infinite level challenges. Each level is dynamically generated in real-time and never repeats!

---

## 🎮 核心特性 (Core Features)

### ✅ 已实现的功能

1. **完全动态生成** - 无需预定义关卡文件
2. **四种难度等级** - 简单、普通、困难、地狱
3. **无限模式** - 关卡永不结束，挑战你的极限
4. **智能算法** - 保证每个关卡都有解
5. **难度配置** - 每个难度有不同的参数设置

### ❌ 已移除的功能

- ~~固定 JSON 关卡文件~~ (不再需要)
- ~~关卡列表加载~~ (改为动态生成)
- ~~关卡总数限制~~ (无限模式)

---

## 🚀 快速开始 (Quick Start)

### 方法 1：使用快速启动脚本

```bash
# 默认难度（普通）
python start_game.py

# 指定难度
python start_game.py --difficulty easy
python start_game.py --difficulty normal
python start_game.py --difficulty hard
python start_game.py --difficulty hell
```

### 方法 2：使用主程序

```bash
# 默认难度
python src/main.py

# 指定难度和窗口大小
python src/main.py --difficulty hard --width 1024 --height 768

# 指定帧率
python src/main.py --difficulty easy --fps 120
```

---

## 🎯 难度等级详解 (Difficulty Levels)

### 简单 (Easy)
- **网格大小**: 4x4 或 5x5
- **可移动瓷砖**: 3-8 个
- **打乱比例**: 70%
- **拐角数量**: 1-6 个
- **适合**: 新手玩家，学习游戏机制

### 普通 (Normal) - 默认
- **网格大小**: 5x5 或 6x6
- **可移动瓷砖**: 4-10 个
- **打乱比例**: 80%
- **拐角数量**: 2-8 个
- **适合**: 有一定经验的玩家

### 困难 (Hard)
- **网格大小**: 6x6 或 7x7
- **可移动瓷砖**: 5-12 个
- **打乱比例**: 90%
- **拐角数量**: 3-10 个
- **适合**: 寻求挑战的玩家

### 地狱 (Hell)
- **网格大小**: 7x7 或 8x8
- **可移动瓷砖**: 6-15 个
- **打乱比例**: 100%
- **拐角数量**: 4-12 个
- **适合**: 极限挑战者

---

## 🔧 API 使用 (API Usage)

### 基础用法

```python
from src.integration.game_api import GameAPI

# 创建游戏实例
api = GameAPI()

# 启动游戏（默认普通难度）
api.start_game(difficulty="normal")
```

### 高级用法

```python
from src.integration.game_api import GameAPI

def on_exit():
    print("游戏结束，感谢游玩！")

# 创建游戏实例
api = GameAPI()

# 启动游戏并设置回调
api.start_game(
    difficulty="hard",
    on_exit=on_exit,
    width=1024,
    height=768,
    fps=60
)
```

### 动态切换难度

```python
from src.integration.game_controller import GameController

controller = GameController()
controller.initialize()

# 启动游戏
controller.start_game(difficulty="easy")

# 游戏过程中切换难度（下一关生效）
controller.set_difficulty("hard")

# 获取当前难度
current_difficulty = controller.get_difficulty()
print(f"当前难度: {current_difficulty}")
```

---

## 📊 关卡生成算法 (Level Generation Algorithm)

### 生成流程

1. **选择端点** - 随机放置电源和终端
2. **路径查找** - 使用 DFS 算法生成随机路径
3. **瓷砖配置** - 根据路径方向分配直线/拐角瓷砖
4. **旋转计算** - 计算每个瓷砖的正确旋转角度
5. **打乱瓷砖** - 根据难度打乱���分瓷砖
6. **验证关卡** - 确保关卡符合难度要求

### 关键特性

- **不重复路径** - 使用 DFS 确保路径不交叉
- **难度验证** - 自动验证关卡是否符合难度参数
- **重试机制** - 最多重试 50 次直到生成合格关卡
- **性能优化** - 生成速度快，无明显延迟

---

## 🎨 自定义难度配置 (Custom Difficulty)

如果你想自定义难度参数，可以修改 `src/core/level/difficulty_config.py`：

```python
from src.core.level.difficulty_config import DifficultyLevel, DifficultyConfig

# 获取配置
config = DifficultyConfig.get_config(DifficultyLevel.NORMAL)

# 查看参数
print(f"最小可移动瓷砖: {config.min_movable_tiles}")
print(f"最大可移动瓷砖: {config.max_movable_tiles}")
print(f"打乱比例: {config.scramble_ratio}")
print(f"网格大小范围: {config.grid_size_range}")
```

---

## 🐛 故障排除 (Troubleshooting)

### 问题：关卡生成失败

**症状**: 看到错误 "Failed to generate valid level after 50 attempts"

**解决方案**:
1. 检查难度配置是否合理
2. 确保网格大小足够容纳最小路径长度
3. 降低难度或增加网格大小

### 问题：游戏启动失败

**症状**: 游戏无法启动或黑屏

**解决方案**:
1. 确保已安装所有依赖：`pip install -r requirements.txt`
2. 检查 Python 版本（需要 3.8+）
3. 查看日志文件：`logs/game.log`

### 问题：性能问题

**症状**: 游戏卡顿或帧率低

**解决方案**:
1. 降低目标帧率：`--fps 30`
2. 减小窗口大小：`--width 640 --height 480`
3. 选择较小的难度（网格更小）

---

## 📝 开发者注意事项 (Developer Notes)

### 关键文件

- `src/core/level/level_generator_v2.py` - 关卡生成器（推荐使用）
- `src/core/level/difficulty_config.py` - 难度配置
- `src/core/level/level_manager.py` - 关卡管理器
- `src/integration/game_controller.py` - 游戏控制器
- `src/integration/game_api.py` - 外部 API

### 已弃用的文件

- `src/core/level/level_generator.py` - 旧版生成器（已被 V2 替代）
- `data/levels/*.json` - 固定关卡文件（不再使用）

### 扩展建议

1. **添加新难度等级** - 在 `difficulty_config.py` 中添加新的枚举值和配置
2. **自定义生成算法** - 继承 `LevelGeneratorV2` 并重写生成方法
3. **关卡统计** - 在 `GameController` 中添加统计追踪
4. **成就系统** - 基于关卡数量和难度实现成就

---

## 🎉 总结 (Summary)

新的无限关卡系统提供了：

✅ **无限可玩性** - 永不重复的关卡
✅ **灵活难度** - 四种难度等级可选
✅ **智能生成** - 保证每个关卡都有解
✅ **简洁 API** - 易于集成到其他系统
✅ **高性能** - 实时生成无延迟

享受游戏吧！🎮

---

**最后更新**: 2026-01-23
**版本**: 2.0.0 (Infinite Mode)
