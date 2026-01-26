# 根目录清理计划 (Root Directory Cleanup Plan)

**日期**: 2026-01-25
**目的**: 整理根目录，将文档移动到合适位置

---

## 📋 当前根目录文件分析

### ✅ 应该保留在根目录的文件

这些是标准的项目根文件：

```
✅ .gitignore                    # Git忽略规则
✅ README.md                     # 项目说明（必须在根目录）
✅ LICENSE                       # 许可证（必须在根目录）
✅ CHANGELOG.md                  # 更新日志（标准位置）
✅ requirements.txt              # Python依赖（标准位置）
✅ start_game.py                 # 启动脚本（必须在根目录）
✅ circuit_repair_game.spec      # PyInstaller配置（构建文件）
✅ version_info.txt              # 版本信息（构建文件）
✅ build.bat                     # Windows构建脚本
✅ build.sh                      # Linux/Mac构建脚本
```

---

### 📁 应该移动到 docs/ 的文件

这些是文档，应该放在 docs/ 目录：

```
📁 BUILD.md                      → docs/BUILD.md
📁 TESTING.md                    → docs/TESTING.md
📁 USER_GUIDE.md                 → docs/USER_GUIDE.md
📁 CLAUDE.md                     → 保留在根目录（特殊：Claude Code配置）
```

**说明**:
- `BUILD.md` - 构建文档，应该在 docs/
- `TESTING.md` - 测试文档，应该在 docs/
- `USER_GUIDE.md` - 用户指南，应该在 docs/
- `CLAUDE.md` - Claude Code的配置文件，通常放在根目录

---

### 🗑️ 应该删除的文件

这些是临时文件或不应该提交的文件：

```
❌ debug_level.json              # 调试文件（应该在.gitignore中）
❌ build_output.log              # 构建日志（应该在.gitignore中）
```

---

## 🔧 执行计划

### 阶段 1: 移动文档文件

```bash
# 移动构建文档
mv BUILD.md docs/BUILD.md

# 移动测试文档
mv TESTING.md docs/TESTING.md

# 移动用户指南
mv USER_GUIDE.md docs/USER_GUIDE.md
```

### 阶段 2: 删除临时文件

```bash
# 删除调试文件
rm debug_level.json

# 删除构建日志（已经在.gitignore中）
rm build_output.log
```

### 阶段 3: 更新 .gitignore

确保以下规则存在：
```gitignore
# Debug files
debug_*.json

# Build logs
build_output.log
*.log
```

### 阶段 4: 更新文档引用

需要更新以下文件中的文档路径引用：

1. **README.md**
   - 更新 BUILD.md 的链接
   - 更新 TESTING.md 的链接
   - 更新 USER_GUIDE.md 的链接

2. **其他文档**
   - 检查是否有其他文档引用了这些文件

---

## 📊 清理后的根目录结构

```
project_root/
├── .gitignore                   # Git配置
├── .claude/                     # Claude Code配置
├── README.md                    # 项目说明 ⭐
├── LICENSE                      # 许可证
├── CHANGELOG.md                 # 更新日志
├── CLAUDE.md                    # Claude Code指令
├── requirements.txt             # Python依赖
├── start_game.py                # 启动脚本
├── circuit_repair_game.spec     # PyInstaller配置
├── version_info.txt             # 版本信息
├── build.bat                    # Windows构建脚本
├── build.sh                     # Linux/Mac构建脚本
├── src/                         # 源代码
├── assets/                      # 游戏资源
├── data/                        # 游戏数据
├── tests/                       # 测试代码
├── tools/                       # 开发工具
├── docs/                        # 📚 所有文档
│   ├── BUILD.md                 # 构建文档（从根目录移动）
│   ├── TESTING.md               # 测试文档（从根目录移动）
│   ├── USER_GUIDE.md            # 用户指南（从根目录移动）
│   ├── specifications/          # 规范文档
│   ├── design/                  # 设计文档
│   ├── reports/                 # 报告文档
│   └── archive/                 # 归档文档
├── logs/                        # 日志文件（.gitignore）
├── build/                       # 构建输出（.gitignore）
└── dist/                        # 发布包（.gitignore）
```

---

## ✅ 预期效果

### 清理前
- 根目录文件: 16个
- 文档文件: 混杂在根目录
- 临时文件: 存在

### 清理后
- 根目录文件: 11个（减少5个）
- 文档文件: 全部在 docs/ 目录
- 临时文件: 已删除

### 收益
- ✅ 根目录更清爽
- ✅ 文档组织更规范
- ✅ 符合项目最佳实践
- ✅ 更易于维护

---

## 📝 注意事项

1. **README.md 更新**: 移动文档后需要更新README中的链接
2. **相对路径**: 确保所有文档内部的相对路径引用正确
3. **Git提交**: 使用 `git mv` 命令保留文件历史
4. **测试**: 移动后测试所有文档链接是否正常

---

## 🎯 执行顺序

1. ✅ 创建此清理计划
2. ⏳ 移动文档文件（使用 git mv）
3. ⏳ 删除临时文件
4. ⏳ 更新 README.md 中的链接
5. ⏳ 验证所有链接正常
6. ⏳ 提交更改

---

**创建时间**: 2026-01-25
**执行状态**: 待执行
