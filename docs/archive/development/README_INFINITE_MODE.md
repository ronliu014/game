# 🎮 电路修复游戏 - 无限模式 v2.0

## 🚀 重大更新！

游戏现已升级为**无限关卡模式**，采用程序化生成系统，提供永不重复的挑战！

---

## ✨ 新特性

### 🎯 无限关卡生成
- ✅ 每个关卡都是实时动态生成
- ✅ 永不重复，无限挑战
- ✅ 智能算法保证每个关卡都有解

### 🎚️ 四种难度等级
- **简单 (Easy)**: 4x4-5x5 网格，适合新手
- **普通 (Normal)**: 5x5-6x6 网格，默认难度
- **困难 (Hard)**: 6x6-7x7 网格，寻求挑战
- **地狱 (Hell)**: 7x7-8x8 网格，极限挑战

### ⚡ 性能优化
- 关卡生成速度更快（<30ms）
- 内存占用更少
- 无需预加载关卡文件

---

## 🎮 快速开始

### 方法 1：使用快速启动脚本（推荐）

```bash
# 默认难度（普通）
python start_game.py

# 指定难度
python start_game.py --difficulty easy
python start_game.py --difficulty hard
python start_game.py --difficulty hell
```

### 方法 2：使用主程序

```bash
# 默认难度
python src/main.py

# 自定义设置
python src/main.py --difficulty hard --width 1024 --height 768 --fps 60
```

---

## 📖 命令行参数

```bash
python start_game.py [选项]

选项:
  --difficulty {easy,normal,hard,hell}
                        难度等级 (默认: normal)
  --width WIDTH         窗口宽度 (默认: 800)
  --height HEIGHT       窗口高度 (默认: 600)
  --fps FPS            目标帧率 (默认: 60)
```

---

## 🎯 难度对比

| 难度 | 网格大小 | 可移动瓷砖 | 打乱比例 | 拐角数量 |
|------|---------|-----------|---------|---------|
| 简单 | 4x4-5x5 | 3-8 个 | 70% | 1-6 个 |
| 普通 | 5x5-6x6 | 4-10 个 | 80% | 2-8 个 |
| 困难 | 6x6-7x7 | 5-12 个 | 90% | 3-10 个 |
| 地狱 | 7x7-8x8 | 6-15 个 | 100% | 4-12 个 |

---

## 💻 API 使用

### 基础用法

```python
from src.integration.game_api import GameAPI

# 创建游戏实例
api = GameAPI()

# 启动游戏
api.start_game(difficulty="normal")
```

### 高级用法

```python
from src.integration.game_api import GameAPI

def on_exit():
    print("游戏结束！")

api = GameAPI()
api.start_game(
    difficulty="hard",
    on_exit=on_exit,
    width=1024,
    height=768,
    fps=60
)
```

---

## 🧪 测试

```bash
# 测试无限模式生成
python tests/integration/test_infinite_mode.py

# 运行所有测试
python -m pytest tests/ -v
```

---

## 📚 文档

- **[无限模式使用指南](docs/INFINITE_MODE_GUIDE.md)** - 详细使用说明
- **[迁移指南](docs/MIGRATION_TO_INFINITE_MODE.md)** - 从旧版本迁移
- **[完整文档索引](docs/INDEX.md)** - 所有文档导航

---

## 🔄 从旧版本迁移

### ⚠️ 破坏性变更

1. **移除了固定关卡系统**
   ```python
   # ❌ 旧方式（不再支持）
   api.start_game(level_ids=["level_001", "level_002"])

   # ✅ 新方式
   api.start_game(difficulty="normal")
   ```

2. **命令行参数变更**
   ```bash
   # ❌ 旧方式（不再支持）
   python src/main.py --levels level_001,level_002

   # ✅ 新方式
   python start_game.py --difficulty normal
   ```

详细迁移指南请查看 [MIGRATION_TO_INFINITE_MODE.md](docs/MIGRATION_TO_INFINITE_MODE.md)

---

## 🎨 游戏截图

（待添加）

---

## 🛠️ 技术栈

- **Python 3.8+**
- **Pygame** - 游戏引擎
- **程序化生成** - DFS 算法
- **难度系统** - 可配置参数

---

## 📦 项目结构

```
game/
├── src/
│   ├── core/
│   │   ├── level/
│   │   │   ├── level_generator_v2.py    # 关卡生成器
│   │   │   ├── difficulty_config.py     # 难度配置
│   │   │   └── level_manager.py         # 关卡管理
│   │   ├── grid/                        # 网格系统
│   │   ├── circuit/                     # 电路连接
│   │   └── game_state/                  # 状态机
│   ├── integration/
│   │   ├── game_api.py                  # 外部 API
│   │   ├── game_controller.py           # 游戏控制器
│   │   └── game_loop.py                 # 游戏循环
│   └── main.py                          # 主入口
├── tests/
│   └── integration/
│       └── test_infinite_mode.py        # 无限模式测试
├── docs/                                # 文档
├── start_game.py                        # 快速启动脚本
└── README.md                            # 本文件
```

---

## 🐛 故障排除

### 问题：关卡生成失败

**解决方案**:
1. 检查难度配置是否合理
2. 确保网格大小足够
3. 查看日志：`logs/game.log`

### 问题：游戏启动失败

**解决方案**:
1. 安装依赖：`pip install -r requirements.txt`
2. 检查 Python 版本（需要 3.8+）
3. 激活 conda 环境：`conda activate Game`

### 问题：性能问题

**解决方案**:
1. 降低帧率：`--fps 30`
2. 减小窗口：`--width 640 --height 480`
3. 选择较低难度

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

（待添加）

---

## 🎉 更新日志

### v2.0.0 (2026-01-23)
- ✨ 新增无限关卡生成系统
- ✨ 新增四种难度等级
- ✨ 新增快速启动脚本
- 🔥 移除固定关卡系统
- ⚡ 性能优化
- 📚 完善文档

### v1.0.0 (2026-01-20)
- 🎮 初始版本
- 基础游戏功能
- 固定关卡系统

---

## 📞 联系方式

- **项目**: Circuit Repair Game
- **团队**: Circuit Repair Game Team
- **更新**: 2026-01-23

---

**享受无限的挑战吧！🎮**
