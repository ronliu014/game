# 占位符资源清单

本文档列出了所有生成的占位符资源。这些资源仅用于开发和测试，后期需要替换为正式美术资源。

**生成时间**: 2026-01-23
**生成工具**: `tools/scripts/generate_placeholders.py`

---

## 按钮资源

**位置**: `assets/ui/buttons/`

| 按钮 | 文件名前缀 | 尺寸 | 状态 |
|------|-----------|------|------|
| 开始游戏 | `start_button_` | 200×50 | normal/hover/pressed |
| 退出游戏 | `exit_button_` | 200×50 | normal/hover/pressed |
| 下一关卡 | `next_level_` | 200×50 | normal/hover/pressed |
| 返回主菜单 | `back_menu_` | 200×50 | normal/hover/pressed |
| 重试一次 | `retry_` | 200×50 | normal/hover/pressed |
| 简单 | `difficulty_easy_` | 120×40 | normal/hover/pressed |
| 普通 | `difficulty_normal_` | 120×40 | normal/hover/pressed |
| 困难 | `difficulty_hard_` | 120×40 | normal/hover/pressed |
| 地狱 | `difficulty_hell_` | 120×40 | normal/hover/pressed |

**状态说明**:
- `normal`: 正常状态（灰色）
- `hover`: 鼠标悬停状态（亮灰色）
- `pressed`: 按下状态（深灰色）

---

## 背景资源

**位置**: `assets/ui/backgrounds/`

| 背景 | 文件名 | 尺寸 | 用途 |
|------|--------|------|------|
| 主菜单背景 | `main_menu_bg.png` | 800×600 | 启动场景 |
| 加载背景1 | `loading_bg_01.png` | 800×600 | 加载场景（随机） |
| 加载背景2 | `loading_bg_02.png` | 800×600 | 加载场景（随机） |
| 加载背景3 | `loading_bg_03.png` | 800×600 | 加载场景（随机） |
| 游戏背景 | `gameplay_bg.png` | 800×600 | 游戏场景 |
| 胜利背景 | `victory_bg.png` | 800×600 | 胜利场景（金色渐变） |
| 失败背景 | `defeat_bg.png` | 800×600 | 失败场景（灰色渐变） |

**说明**: 所有背景均为垂直渐变色，无复杂图案。

---

## 图标资源

**位置**: `assets/ui/icons/`

| 图标 | 文件名 | 尺寸 | 用途 |
|------|--------|------|------|
| 退出图标 | `exit_icon.png` | 40×40 | 退出按钮 |
| 调试图标 | `debug_icon.png` | 40×40 | 调试开关 |
| 设置图标 | `settings_icon.png` | 40×40 | 设置按钮 |

**说明**: 图标使用简单的几何形状，支持透明背景。

---

## LOGO资源

**位置**: `assets/ui/logo/`

| LOGO | 文件名 | 尺寸 | 用途 |
|------|--------|------|------|
| 游戏标题 | `game_title.png` | 400×120 | 主菜单显示 |

**说明**: LOGO包含"电路修复"文字，铜色边框，金色文字。

---

## 游戏图标

**位置**: `assets/ui/icon/`

| 图标 | 文件名 | 尺寸 | 用途 |
|------|--------|------|------|
| 应用图标 | `game_icon.png` | 256×256 | 应用程序图标 |

**说明**: PNG格式，需要使用工具转换为.ico格式用于打包。

**转换工具推荐**:
- 在线工具: https://convertio.co/zh/png-ico/
- 本地工具: ImageMagick

**转换命令**:
```bash
magick convert game_icon.png -define icon:auto-resize=256,128,64,48,32,16 game_icon.ico
```

---

## 替换指南

### 如何替换占位符资源

1. **准备正式资源**:
   - 按照上述尺寸要求制作美术资源
   - 保持相同的文件名
   - 使用PNG格式（支持透明）

2. **替换文件**:
   - 直接覆盖对应目录下的文件
   - 无需修改代码（路径通过配置文件管理）

3. **测试验证**:
   - 运行游戏检查资源显示
   - 确认所有场景的资源都已替换

### 资源制作规范

详见：
- [美术资源规范](../../docs/specifications/10_美术资源规范.md)
- [音效资源规范](../../docs/specifications/11_音效资源规范.md)

---

## 注意事项

1. **占位符限制**:
   - 仅用于开发测试，不适合正式发布
   - 视觉效果简陋，缺少细节和质感
   - 不符合蒸汽朋克美术风格

2. **优先替换**:
   - 主菜单背景和LOGO（用户第一印象）
   - 游戏背景（游戏主体场景）
   - 按钮资源（交互频繁）

3. **后期替换**:
   - 图标资源（视觉影响较小）
   - 加载背景（显示时间短）

---

**生成工具**: `python tools/scripts/generate_placeholders.py`
**最后更新**: 2026-01-23
