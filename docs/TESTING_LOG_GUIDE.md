# 测试日志查看指南 (Testing Log Viewing Guide)

**目的**: 在测试过程中实时查看日志，方便沟通和问题定位

---

## 📋 日志文件说明

游戏运行时会生成以下日志文件（在 `logs/` 目录）：

| 日志文件 | 内容 | 用途 |
|---------|------|------|
| **game.log** | 所有日志（DEBUG级别） | 查看详细的操作记录 |
| **error.log** | 仅错误日志 | 快速定位错误 |
| **performance.log** | 性能日志 | 查看性能指标 |
| **game_YYYYMMDD_HHMMSS.log** | 带时间戳的日志 | 每次启动的独立日志 |

---

## 🔍 如何实时查看日志

### 方式1: 使用PowerShell实时监控（推荐）

**打开两个窗口**：

**窗口1 - 运行游戏**:
```powershell
python start_game.py
```

**窗口2 - 实时查看日志**:
```powershell
# 实时查看主日志
Get-Content logs/game.log -Wait -Tail 50

# 或者只看INFO级别以上的日志（更清晰）
Get-Content logs/game.log -Wait -Tail 50 | Select-String -Pattern "\[INFO\]|\[WARNING\]|\[ERROR\]"
```

---

### 方式2: 使用Git Bash实时监控

**窗口1 - 运行游戏**:
```bash
python start_game.py
```

**窗口2 - 实时查看日志**:
```bash
# 实时查看主日志
tail -f logs/game.log

# 或者只看重要日志
tail -f logs/game.log | grep -E "INFO|WARNING|ERROR"
```

---

### 方式3: 使用文本编辑器自动刷新

某些编辑器支持自动刷新功能：

- **VS Code**: 安装 "Log File Highlighter" 插件，打开 `logs/game.log`
- **Notepad++**: 打开文件后，View → Monitoring (tail -f)
- **Sublime Text**: 安装 "Tail" 插件

---

## 📊 关键日志标记

在测试时，注意以下关键日志：

### 场景切换
```
[INFO] [src.scenes.main_menu_scene] [on_enter] - MainMenuScene entered
[INFO] [src.scenes.level_select_scene] [on_enter] - Level select scene entered with difficulty: normal
[INFO] [src.scenes.gameplay_scene] [on_enter] - GameplayScene entered: level=1, difficulty=normal, time_limit=45s
```

### 按钮点击
```
[INFO] [src.ui.components.button] [handle_event] - Button '关卡选择' clicked
[INFO] [src.scenes.level_select_scene] [_on_level_clicked] - Level 1 selected
```

### 游戏状态
```
[INFO] [src.scenes.gameplay_scene] [_start_game] - Game started
[INFO] [src.scenes.gameplay_scene] [_toggle_pause] - Game paused
[INFO] [src.scenes.gameplay_scene] [_toggle_pause] - Game resumed
[INFO] [src.scenes.gameplay_scene] [_on_timeout] - Timer timeout - game over
[INFO] [src.scenes.gameplay_scene] [_on_game_over] - Game over: victory=True, moves=5, time=12.3s
```

### 进度保存
```
[INFO] [src.progression.save_manager] [save_progress] - Progress saved successfully
[INFO] [src.progression.level_progression] [complete_level] - Level 1 completed with 3 stars
```

### 错误信息
```
[ERROR] [src.audio.sound_player] [load_sound] - Sound file not found: assets/audio/sfx/tile_rotate.wav
[WARNING] [src.scenes.loading_scene] [_load_resources] - Resource loading failed: ...
```

---

## 🎯 测试时的日志检查清单

### 启动阶段
- [ ] 看到 "Logging system initialized successfully"
- [ ] 看到 "MainMenuScene entered"
- [ ] 没有 ERROR 级别的日志

### 主菜单操作
- [ ] 点击难度按钮时看到 "Difficulty selected: xxx"
- [ ] 点击"关卡选择"看到 "Level select button clicked"
- [ ] 进入关卡选择看到 "Level select scene entered"

### 关卡选择操作
- [ ] 点击关卡看到 "Level X selected"
- [ ] 进入游戏看到 "GameplayScene entered: level=X"
- [ ] 点击返回看到 "Back to main menu"

### 游戏过程
- [ ] 开始游戏看到 "Game started"
- [ ] 旋转方块时看到相关日志
- [ ] 暂停时看到 "Game paused"
- [ ] 完成关卡看到 "Game over: victory=True"

### 进度系统
- [ ] 完成关卡后看到 "Level X completed with Y stars"
- [ ] 看到 "Progress saved successfully"

---

## 🐛 如何报告问题

当发现问题时，请提供以下信息：

### 1. 问题描述
```
简短描述问题是什么
```

### 2. 操作步骤
```
1. 第一步做了什么
2. 第二步做了什么
3. ...
```

### 3. 相关日志
```
从 logs/game.log 中复制相关的日志行
（包括问题发生前后的日志）
```

### 4. 时间戳
```
问题发生的大概时间，方便在日志中定位
```

---

## 💡 日志查看技巧

### 1. 过滤特定模块的日志
```powershell
# 只看场景相关的日志
Get-Content logs/game.log | Select-String "scenes"

# 只看按钮点击
Get-Content logs/game.log | Select-String "Button.*clicked"

# 只看错误和警告
Get-Content logs/game.log | Select-String "ERROR|WARNING"
```

### 2. 查看最近的日志
```powershell
# 查看最后50行
Get-Content logs/game.log -Tail 50

# 查看最后100行
Get-Content logs/game.log -Tail 100
```

### 3. 搜索特定内容
```powershell
# 搜索关卡选择相关
Get-Content logs/game.log | Select-String "level.*select"

# 搜索特定关卡
Get-Content logs/game.log | Select-String "Level 1"
```

### 4. 按时间范围查看
```powershell
# 查看特定时间段的日志
Get-Content logs/game.log | Select-String "12:00:.*12:05:"
```

---

## 📝 测试日志模板

在测试时，你可以这样记录：

```markdown
## 测试项: [测试内容]

### 操作步骤
1. [步骤1]
2. [步骤2]
3. ...

### 预期结果
[应该发生什么]

### 实际结果
[实际发生了什么]

### 相关日志
```
[从 logs/game.log 复制的相关日志]
```

### 问题截图
[如果有的话]
```

---

## 🚀 快速开始测试

**推荐的测试流程**：

1. **清空旧日志**（可选）
   ```bash
   rm logs/*.log
   ```

2. **打开日志监控窗口**
   ```powershell
   # PowerShell
   Get-Content logs/game.log -Wait -Tail 50
   ```

3. **启动游戏**
   ```bash
   python start_game.py
   ```

4. **开始测试**
   - 按照测试清单逐项测试
   - 观察日志输出
   - 记录发现的问题

5. **测试完成后**
   - 保存日志文件（如果需要）
   - 整理发现的问题
   - 提供日志片段

---

## 📞 沟通示例

**好的问题报告**：
```
问题：点击关卡选择后没有反应

操作步骤：
1. 启动游戏
2. 在主菜单点击"关卡选择"按钮
3. 没有进入关卡选择场景

日志显示：
[2026-01-25 12:00:15] [INFO] [src.scenes.main_menu_scene] - Level select button clicked
[2026-01-25 12:00:15] [ERROR] [src.scenes.scene_manager] - Scene 'level_select' not registered

时间：12:00左右
```

**不好的问题报告**：
```
关卡选择有问题
```

---

## ✅ 准备就绪检查

在开始测试前，确认：

- [ ] 能够打开并查看 `logs/game.log`
- [ ] 了解如何实时监控日志
- [ ] 知道关键日志标记的含义
- [ ] 知道如何报告问题

---

**准备好了就开始测试吧！** 🎮

有任何问题随时告诉我，我会通过日志帮你定位问题！
