# 项目目录结构清理计划

## 审查日期
2026-01-24

## 审查目的
对照《目录结构规范》(02_目录结构规范.md)，检查当前项目目录，识别需要清理、归档或重新组织的文件。

---

## 📋 审查结果总览

### 统计数据
- **需要删除的文件**: 15个
- **需要归档的文件**: 8个
- **需要移动的文件**: 6个
- **需要保留的文件**: 符合规范

---

## 🗑️ 需要删除的文件

### 1. 临时和调试文件

#### 根目录临时文件
```
❌ ./debug_level.json                    # 调试用关卡文件
❌ ./demo_week_1_2.py                    # 演示脚本
❌ ./demo_week_3.py                      # 演示脚本
```
**原因**: 临时调试文件，不应保留在项目根目录

#### temp 目录
```
❌ ./temp/nul                            # 空文件
```
**建议**: 整个 temp 目录可以删除或添加到 .gitignore

#### 测试调试文件
```
❌ ./tests/debug_scrambling.py           # 调试脚本
❌ ./tests/quick_test_v3.py              # 快速测试脚本
```
**原因**: 临时调试文件，应移到 tests/archive_debug/

### 2. 覆盖率报告文件

```
❌ ./.coverage                           # 覆盖率数据文件
❌ ./htmlcov/                            # 整个目录（HTML覆盖率报告）
```
**原因**:
- 这些是测试覆盖率工具生成的临时文件
- 应该添加到 .gitignore
- 每次运行测试都会重新生成

### 3. 日志文件

```
❌ ./logs/error.log                      # 运行时日志
❌ ./logs/game.log                       # 运行时日志
❌ ./logs/game_20260123_181544.log       # 历史日志
❌ ./logs/game_20260123_182940.log       # 历史日志
❌ ./logs/performance.log                # 性能日志
```
**原因**: 运行时生成的日志文件，不应提交到版本控制

---

## 📦 需要归档的文件

### 1. 开发文档（已过时）

```
📦 ./docs/development/ALGORITHM_V3_IMPLEMENTATION.md
📦 ./docs/development/BUG_FIX_REPORT_20260123.md
📦 ./docs/development/DESIGN_DOC_UPDATE_SUMMARY.md
📦 ./docs/development/GRID_LAYOUT_FIX_20260123.md
📦 ./docs/development/INFINITE_MODE_GUIDE.md
📦 ./docs/development/MIGRATION_TO_INFINITE_MODE.md
📦 ./docs/development/README_INFINITE_MODE.md
📦 ./docs/development/V3_COMPLETION_REPORT.md
```
**建议**: 移动到 `docs/archive/development/`

### 2. 项目审查报告（已完成）

```
📦 ./docs/PROJECT_RESTRUCTURE_REPORT.md
📦 ./docs/PROJECT_STRUCTURE_AUDIT.md
```
**建议**: 移动到 `docs/archive/`

---

## 📁 需要移动/重组织的文件

### 1. 文档位置不规范

#### Week 总结文档
```
📁 ./docs/WEEK_2_SUMMARY.md              → docs/reports/WEEK_2_SUMMARY.md
📁 ./docs/WEEK_3_SUMMARY.md              → docs/reports/WEEK_3_SUMMARY.md
📁 ./docs/WEEK_4_SUMMARY.md              → docs/reports/WEEK_4_SUMMARY.md
📁 ./docs/WEEK_5_SUMMARY.md              → docs/reports/WEEK_5_SUMMARY.md
📁 ./docs/WEEK_6_SUMMARY.md              → docs/reports/WEEK_6_SUMMARY.md
📁 ./docs/WEEK_6_SUMMARY_FINAL.md        → docs/reports/WEEK_6_SUMMARY_FINAL.md
📁 ./docs/WEEK_7_SUMMARY.md              → docs/reports/WEEK_7_SUMMARY.md
```
**原因**: 应该统一放在 reports 目录下

#### 演示文档
```
📁 ./docs/DEMO_WEEK_1_2.md               → docs/archive/demos/
```
**原因**: 演示文档应归档

### 2. 资源文件位置重复

```
⚠️ ./assets/ui/                          # 与 assets/sprites/ui/ 重复
```
**建议**:
- 检查两个目录的内容
- 合并到 `assets/sprites/ui/`
- 删除重复的 `assets/ui/`

---

## ✅ 符合规范的目录结构

### 核心代码目录 ✅
```
✅ src/
   ├── core/              # 核心逻辑
   ├── rendering/         # 渲染层
   ├── audio/             # 音频系统
   ├── input/             # 输入处理
   ├── integration/       # 外部接口
   ├── config/            # 配置管理
   ├── utils/             # 工具类
   ├── ui/                # UI组件
   ├── scenes/            # 场景系统
   └── progression/       # 进度系统
```

### 资源目录 ✅
```
✅ assets/
   ├── sprites/           # 精灵图
   ├── audio/             # 音频文件
   ├── fonts/             # 字体
   └── icon.ico           # 应用图标
```

### 数据目录 ✅
```
✅ data/
   ├── levels/            # 关卡数据
   ├── config/            # 配置文件
   └── saves/             # 存档目录
```

### 测试目录 ✅
```
✅ tests/
   ├── unit/              # 单元测试
   ├── integration/       # 集成测试
   ├── fixtures/          # 测试数据
   └── archive_debug/     # 归档的调试脚本
```

### 文档目录 ✅
```
✅ docs/
   ├── specifications/    # 规范文档
   ├── design/            # 设计文档
   ├── reports/           # 报告文档
   ├── archive/           # 归档文档
   └── assets/            # 文档资源
```

### 工具目录 ✅
```
✅ tools/
   ├── level_editor/      # 关卡编辑器
   ├── scripts/           # 脚本工具
   └── create_icon.py     # 图标生成器
```

### 根目录文件 ✅
```
✅ README.md              # 项目说明
✅ USER_GUIDE.md          # 用户指南
✅ CHANGELOG.md           # 更新日志
✅ LICENSE                # 许可证
✅ BUILD.md               # 构建说明
✅ TESTING.md             # 测试指南
✅ CLAUDE.md              # Claude 指令
✅ requirements.txt       # Python 依赖
✅ start_game.py          # 启动脚本
✅ build.bat              # Windows 构建脚本
✅ build.sh               # Linux/Mac 构建脚本
✅ circuit_repair_game.spec  # PyInstaller 配置
✅ version_info.txt       # 版本信息
```

---

## 🔧 .gitignore 需要添加的规则

```gitignore
# 覆盖率报告
.coverage
htmlcov/
.pytest_cache/

# 日志文件
logs/*.log
*.log

# 临时文件
temp/
*.tmp
debug_*.json

# Python 缓存
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE 配置
.vscode/
.idea/
*.swp
*.swo

# 构建输出
build/
dist/
*.spec.bak

# 存档文件
data/saves/*.json
data/saves/*.backup
```

---

## 📝 执行计划

### 阶段 1: 删除临时文件（立即执行）
1. 删除根目录临时文件
2. 删除覆盖率报告
3. 删除日志文件
4. 删除 temp 目录

### 阶段 2: 归档文档（立即执行）
1. 创建 `docs/archive/development/` 目录
2. 移动开发文档到归档目录
3. 移动项目审查报告到归档目录

### 阶段 3: 重组织文件（立即执行）
1. 移动 Week 总结到 `docs/reports/`
2. 移动演示文档到 `docs/archive/demos/`
3. 检查并合并 UI 资源目录

### 阶段 4: 更新 .gitignore（立即执行）
1. 添加覆盖率报告规则
2. 添加日志文件规则
3. 添加临时文件规则

---

## ⚠️ 注意事项

1. **备份**: 在删除任何文件前，确保已经提交到 Git
2. **验证**: 删除后运行测试确保项目正常工作
3. **文档**: 更新相关文档中的文件路径引用
4. **团队通知**: 如果是团队项目，通知其他成员目录结构变更

---

## 📊 预期效果

### 清理前
- 文件总数: ~300+
- 目录层级: 混乱
- 临时文件: 多个

### 清理后
- 文件总数: ~280
- 目录层级: 清晰规范
- 临时文件: 0（��过 .gitignore 排除）

### 收益
- ✅ 符合项目规范
- ✅ 更易于导航
- ✅ 减少仓库大小
- ✅ 提高可维护性

---

**审查人**: Claude Code
**审查日期**: 2026-01-24
**下一步**: 执行清理计划
