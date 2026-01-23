# 项目目录整理方案

## 当前问题分析

### 1. 根目录混乱问题

**问题**：根目录下有大量测试文件和临时文件

**发现的问题文件**：
```
根目录下的测试文件（应该在 tests/ 目录）：
- check_level_state.py
- test_config_victory.py
- test_connectivity.py
- test_current_state.py
- test_debug_generator.py
- test_detailed_connectivity.py
- test_detailed_path.py
- test_detailed_trace.py
- test_direction_fix.py
- test_generator_v2.py
- test_level_data.py
- test_level_generator.py
- test_new_level.py
- test_play_generated.py
- test_rotation_match.py
- test_show_path.py
- test_simple_v2.py
- test_user_state.py
- test_visual_connectivity.py

临时/调试文件（应该删除或移动）：
- debug_level.json
- nul
- ScreenShot_1.png

关卡数据文件（应该在 data/levels/）：
- data/levels/level_001_new.json (临时文件)
- data/levels/level_generated_test.json (测试文件)
```

### 2. 文档目录问题

**问题**：`docs/algorithm_explanation.md` 应该移动到 `docs/design/` 或删除（已有正式文档）

### 3. 缺失的目录

根据规范，应该有但缺失的目录：
- `tests/debug/` - 调试测试脚本
- `tests/manual/` - 手动测试脚本
- `tools/debug/` - 调试工具

---

## 整理方案

### 阶段1：创建必要的目录结构

```bash
# 创建缺失的目录
mkdir -p tests/debug
mkdir -p tests/manual
mkdir -p tools/debug
mkdir -p temp
```

### 阶段2：移动测试文件

#### 2.1 单元测试（移动到 tests/unit/）

这些是针对特定功能的测试：
```bash
# 连通性测试
mv test_connectivity.py tests/unit/test_connectivity_manual.py
mv test_detailed_connectivity.py tests/unit/test_connectivity_detailed.py
mv test_detailed_path.py tests/unit/test_path_detailed.py
mv test_detailed_trace.py tests/unit/test_trace_detailed.py

# 关卡测试
mv test_level_data.py tests/unit/test_level_data_manual.py
mv test_config_victory.py tests/unit/test_victory_config.py

# 旋转测试
mv test_rotation_match.py tests/unit/test_rotation_matching.py
mv test_direction_fix.py tests/unit/test_direction_fix.py

# 状态测试
mv test_current_state.py tests/unit/test_current_state.py
mv test_user_state.py tests/unit/test_user_state.py
```

#### 2.2 集成测试（移动到 tests/integration/）

这些是测试完整流程的：
```bash
mv test_play_generated.py tests/integration/test_play_generated_level.py
mv test_new_level.py tests/integration/test_new_level_flow.py
mv test_show_path.py tests/integration/test_path_visualization.py
mv test_visual_connectivity.py tests/integration/test_visual_connectivity.py
```

#### 2.3 调试脚本（移动到 tests/debug/）

这些是临时调试用的：
```bash
mv check_level_state.py tests/debug/check_level_state.py
mv test_debug_generator.py tests/debug/test_debug_generator.py
```

#### 2.4 关卡生成器测试（移动到 tests/unit/）

```bash
mv test_level_generator.py tests/unit/test_level_generator_v1.py
mv test_generator_v2.py tests/unit/test_level_generator_v2.py
mv test_simple_v2.py tests/debug/test_simple_generator_v2.py
```

### 阶段3：整理临时文件

#### 3.1 移动到 temp/ 目录

```bash
# 临时调试文件
mv debug_level.json temp/
mv nul temp/

# 临时关卡文件
mv data/levels/level_001_new.json temp/
mv data/levels/level_generated_test.json temp/
```

#### 3.2 移动截图到 docs/assets/

```bash
mv ScreenShot_1.png docs/assets/screenshots/screenshot_001.png
```

### 阶段4：整理文档

```bash
# 删除重复的算法说明文档（已有正式设计文档）
rm docs/algorithm_explanation.md
```

### 阶段5：更新 .gitignore

添加以下内容：
```
# 临时文件目录
temp/

# 调试文件
debug_*.json
nul

# 测试生成的关卡
data/levels/*_test.json
data/levels/*_new.json
data/levels/*_generated*.json
```

---

## 整理后的目录结构

```
circuit-repair-game/
├── docs/                           # 文档
│   ├── specifications/             # 规范文档
│   ├── design/                     # 设计文档
│   ├── assets/                     # 文档资源
│   │   ├── image/                  # UI设计稿
│   │   └── screenshots/            # 截图
│   ├── archive/                    # 归档文档
│   └── INDEX.md                    # 文档索引
│
├── src/                            # 源代码
│   ├── core/                       # 核心逻辑
│   ├── rendering/                  # 渲染层
│   ├── audio/                      # 音频系统
│   ├── input/                      # 输入处理
│   ├── integration/                # 外部集成
│   ├── config/                     # 配置管理
│   ├── utils/                      # 工具类
│   └── main.py                     # 程序入口
│
├── tests/                          # 测试代码
│   ├── unit/                       # 单元测试
│   ├── integration/                # 集成测试
│   ├── debug/                      # 调试脚本
│   └── manual/                     # 手动测试
│
├── assets/                         # 游戏资源
│   ├── sprites/                    # 精灵图
│   ├── audio/                      # 音频文件
│   └── fonts/                      # 字体文件
│
├── data/                           # 数据文件
│   ├── levels/                     # 关卡数据（仅正式关卡）
│   └── config/                     # 配置文件
│
├── tools/                          # 开发工具
│   ├── scripts/                    # 脚本工具
│   └── debug/                      # 调试工具
│
├── examples/                       # 示例代码
│
├── temp/                           # 临时文件（不提交到git）
│
├── logs/                           # 日志文件（不提交到git）
│
├── htmlcov/                        # 测试覆盖率报告（不提交到git）
│
├── .claude/                        # Claude配置
├── .git/                           # Git仓库
├── .pytest_cache/                  # Pytest缓存
│
├── README.md                       # 项目说明
├── CLAUDE.md                       # Claude开发指南
├── CHANGELOG.md                    # 变更日志
├── LICENSE                         # 许可证
├── requirements.txt                # Python依赖
├── .gitignore                      # Git忽略规则
├── start_dev.bat                   # 开发启动脚本
└── start_game.bat                  # 游戏启动脚本
```

---

## 执行步骤

### 步骤1：备份当前状态
```bash
git add .
git commit -m "backup: 整理前的项目状态"
```

### 步骤2：创建必要目录
```bash
mkdir -p tests/debug tests/manual tools/debug temp docs/assets/screenshots
```

### 步骤3：执行文件移动
按照上述方案逐步移动文件

### 步骤4：更新 .gitignore
添加临时文件规则

### 步骤5：验证项目结构
运行测试确保没有破坏功能

### 步骤6：提交更改
```bash
git add .
git commit -m "refactor: 按照目录结构规范整理项目文件"
```

---

## 注意事项

1. **测试文件重命名**：移动后的测试文件需要更新导入路径
2. **保留功能**：确保所有测试仍然可以运行
3. **临时文件**：temp/ 目录的文件不提交到git
4. **文档同步**：更新CLAUDE.md中的目录结构说明

---

**创建日期**: 2026-01-22
**状态**: 待执行
