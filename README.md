# 电路板修复游戏 (Circuit Repair Game)

一款工业蒸汽朋克风格的电路板修复拼图游戏，可作为独立模块被外部系统调用。

## 项目状态

**当前阶段**: 阶段1完成 → 准备进入阶段2
**版本**: v0.1.0-stage1
**状态**: 🚧 开发中

### 开发进度

- ✅ **阶段0**: 环境搭建与技术选型 (100%)
- ✅ **阶段1**: 核心框架开发 (100%)
  - 日志系统 (96% 覆盖率, 19个测试)
  - 配置管理系统 (97% 覆盖率, 21个测试)
  - 基础工具类 (97% 覆盖率, 55个测试)
  - 数据结构定义 (98% 覆盖率, 32个测试)
- ⏳ **阶段2**: 游戏逻辑实现 (0%)
- ⏳ **阶段3**: 渲染与交互 (0%)
- ⏳ **阶段4**: 音效特效与优化 (0%)
- ⏳ **阶段5**: 集成测试与文档 (0%)
- ⏳ **阶段6**: 发布与部署 (0%)

**总体进度**: 28.6% (2/7 阶段完成)

## 功能特性

- 🎮 **网格拼图玩法**: 通过旋转电路元件连接电源与终端
- 🎨 **工业蒸汽朋克风格**: 铜/黄铜质感的视觉设计
- ⚡ **动态电流效果**: 实时电流流动动画和粒子特效
- 🎵 **完整音效系统**: 旋转音效、连接音效、背景音乐
- 📦 **模块化设计**: 可被外部系统无缝集成调用
- 🎯 **关卡系统**: 数据驱动的关卡配置，易于扩展

## 快速开始

### 环境要求

- **Python**: 3.8+
- **Conda**: Anaconda/Miniconda
- **操作系统**: Windows/Linux/macOS

### 安装步骤

```bash
# 1. 克隆仓库
git clone <repository-url>
cd game

# 2. 激活conda环境
conda activate Game

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行游戏（开发完成后）
python src/main.py
```

### 开发环境配置

```bash
# 安装开发工具
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 代码格式化
black src/

# 代码检查
pylint src/
mypy src/
```

## 项目结构

```
circuit-repair-game/
├── docs/                   # 📚 项目文档
│   ├── INDEX.md           # 文档索引（入口）⭐
│   ├── specifications/    # 规范文档
│   │   ├── 00_项目规划总纲.md
│   │   ├── 01_技术方案文档.md
│   │   ├── 02_目录结构规范.md
│   │   ├── 03_文档编写规范.md
│   │   ├── 04_日志系统规范.md
│   │   ├── 05_开发规范.md
│   │   ├── 06_项目实施路线图.md
│   │   ├── 07_版本控制规范.md
│   │   ├── 10_美术资源规范.md
│   │   └── 11_音效资源规范.md
│   ├── design/            # 设计文档
│   │   ├── 派对游戏 - 修复电路板_设计文档.md
│   │   └── 30_关卡生成算法设计文档.md
│   ├── development/       # 开发文档
│   │   ├── ALGORITHM_V3_IMPLEMENTATION.md
│   │   ├── INFINITE_MODE_GUIDE.md
│   │   ├── MIGRATION_TO_INFINITE_MODE.md
│   │   ├── V3_COMPLETION_REPORT.md
│   │   ├── DESIGN_DOC_UPDATE_SUMMARY.md
│   │   └── README_INFINITE_MODE.md
│   ├── changelog/         # 版本记录
│   │   └── CHANGELOG.md
│   ├── archive/           # 归档文档
│   └── assets/            # 资源文档
│       └── image/         # UI设计稿
├── src/                    # 🔧 源代码
│   ├── core/              # 核心游戏逻辑
│   ├── rendering/         # 渲染层
│   ├── audio/             # 音频系统
│   ├── integration/       # 外部集成接口
│   └── utils/             # 工具类
├── assets/                # 🎨 游戏资源
│   ├── sprites/           # 精灵图
│   ├── audio/             # 音频文件
│   └── fonts/             # 字体
├── data/                  # 📊 数据文件
│   ├── levels/            # 关卡数据
│   └── config/            # 配置文件
├── tests/                 # 🧪 测试代码
└── tools/                 # 🛠️ 开发工具
    └── scripts/           # 辅助脚本
```

详细目录结构请参考：[目录结构规范](docs/specifications/02_目录结构规范.md)

## 外部集成

### API使用示例

```python
from src.integration.game_api import GameAPI

# 创建游戏实例
game = GameAPI()

# 定义回调函数
def on_complete(level_id, stats):
    print(f"关卡 {level_id} 完成！用时: {stats['time']}秒")

def on_exit():
    print("玩家退出游戏")

# 启动游戏（单关卡）
game.start_game(
    level_ids=['001'],
    on_complete=on_complete,
    on_exit=on_exit
)

# 启动游戏（多关卡）
game.start_game(
    level_ids=['001', '002', '003'],
    on_complete=on_complete,
    on_exit=on_exit
)
```

详细API文档请参考：[API接口文档](docs/design/20_API接口文档.md)（开发中）

## 开发指南

### 📚 文档导航

**文档索引**: [docs/INDEX.md](docs/INDEX.md) ⭐ **所有文档的入口**

### 必读文档

所有开发人员必须熟读以下规范文档：

1. [文档索引](docs/INDEX.md) - 快速查找所有文档 ⭐⭐⭐
2. [项目规划总纲](docs/specifications/00_项目规划总纲.md) - 项目整体规划 ⭐⭐⭐
3. [目录结构规范](docs/specifications/02_目录结构规范.md) - 文件组织规则 ⭐⭐⭐
4. [文档编写规范](docs/specifications/03_文档编写规范.md) - 文档标准 ⭐⭐⭐
5. [日志系统规范](docs/specifications/04_日志系统规范.md) - 日志记录标准 ⭐⭐⭐
6. [开发规范](docs/specifications/05_开发规范.md) - 代码风格与流程 ⭐⭐⭐
7. [项目实施路线图](docs/specifications/06_项目实施路线图.md) - 开发计划 ⭐⭐

### 开发流程

```
需求分析 → 技术设计 → 编码实现 → 单元测试 → 代码审查 → 集成测试 → 部署发布
```

### Git工作流

```bash
# 创建功能分支
git checkout -b feature/your-feature-name

# 提交代码（遵循提交规范）
git commit -m "feat(module): add new feature"

# 推送并创建Pull Request
git push origin feature/your-feature-name
```

提交信息格式：`<type>(<scope>): <subject>`

类型：`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

### 代码规范

- 遵循 [PEP 8](https://pep8.org/) 标准
- 使用类型注解
- 单元测试覆盖率 ≥ 80%
- 所有公共接口必须有文档字符串

详细规范请参考：[开发规范](docs/specifications/05_开发规范.md)

## 测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成覆盖率报告
pytest --cov=src tests/
```

## 性能指标

- **帧率**: ≥ 60 FPS
- **启动时间**: ≤ 2秒
- **关卡加载**: ≤ 500ms
- **内存占用**: ≤ 100MB

## 技术栈

- **语言**: Python 3.13.11
- **游戏引擎**: Pygame 2.6.1 ✅
- **数值计算**: NumPy 2.4.1
- **图像处理**: Pillow 12.1.0
- **测试框架**: pytest 7.4.0
- **代码质量**: black 23.7.0, pylint 2.17.5, mypy 1.4.1

详细技术方案请参考：[技术方案文档](docs/specifications/01_技术方案文档.md)

## 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码审查检查清单

- [ ] 代码符合开发规范
- [ ] 所有测试通过
- [ ] 测试覆盖率达标
- [ ] 文档已更新
- [ ] 无编译/运行错误

## 路线图

- [x] **阶段0**: 环境搭建与技术选型（当前）
- [ ] **阶段1**: 核心框架开发（Week 3-4）
- [ ] **阶段2**: 游戏逻辑实现（Week 5-6）
- [ ] **阶段3**: 渲染与交互（Week 7-8）
- [ ] **阶段4**: 音效特效与优化（Week 9-10）
- [ ] **阶段5**: 集成与测试（Week 11）
- [ ] **阶段6**: 发布与部署（Week 12）

详细路线图请参考：[项目实施路线图](docs/specifications/06_项目实施路线图.md)

## 常见问题

### Q: 如何添加新关卡？

A: 在 `data/levels/` 目录下创建JSON文件，格式参考现有关卡。

### Q: 如何修改游戏配置？

A: 编辑 `data/config/game_config.json` 文件。

### Q: 如何集成到外部系统？

A: 参考 [API接口文档](docs/20_API接口文档.md) 和示例代码。

## 许可证

[待定]

## 联系方式

- **项目负责人**: [待填写]
- **技术负责人**: [待填写]
- **问题反馈**: [GitHub Issues]

## 致谢

感谢所有为本项目做出贡献的开发者。

---

**注意**: 本项目目前处于开发阶段，API和功能可能会发生变化。
