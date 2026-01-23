"""
占位符资源生成工具

用于快速生成临时的UI资源，便于开发和测试。
生成的资源为占位符，后期可替换为正式美术资源。

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pygame
from src.utils.logger import GameLogger

# 初始化日志
GameLogger.initialize()
logger = GameLogger.get_logger(__name__)


class PlaceholderGenerator:
    """占位符资源生成器"""

    def __init__(self):
        """初始化生成器"""
        pygame.init()
        self.assets_dir = project_root / "assets"
        logger.info("Placeholder generator initialized")

    def generate_button_placeholder(
        self,
        width: int,
        height: int,
        label: str,
        output_dir: Path
    ) -> None:
        """
        生成按钮占位符

        Args:
            width: 按钮宽度
            height: 按钮高度
            label: 按钮文字
            output_dir: 输出目录
        """
        states = {
            'normal': (100, 100, 100),
            'hover': (150, 150, 150),
            'pressed': (80, 80, 80)
        }

        output_dir.mkdir(parents=True, exist_ok=True)

        for state, color in states.items():
            surface = pygame.Surface((width, height))
            surface.fill(color)

            # 绘制边框
            pygame.draw.rect(surface, (200, 200, 200), (0, 0, width, height), 3)

            # 绘制文字
            try:
                # 尝试使用中文字体
                font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", 20)
            except Exception:
                # 降级到默认字体
                font = pygame.font.Font(None, 24)

            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(width//2, height//2))
            surface.blit(text, text_rect)

            # 保存
            filename = f"{label.lower().replace(' ', '_')}_{state}.png"
            filepath = output_dir / filename
            pygame.image.save(surface, str(filepath))
            logger.debug(f"Generated button: {filepath}")

        logger.info(f"Button '{label}' generated with 3 states")

    def generate_background_placeholder(
        self,
        width: int,
        height: int,
        colors: List[Tuple[int, int, int]],
        name: str,
        output_dir: Path
    ) -> None:
        """
        生成背景渐变占位符

        Args:
            width: 背景宽度
            height: 背景高度
            colors: 渐变颜色列表 [(r1,g1,b1), (r2,g2,b2)]
            name: 文件名
            output_dir: 输出目录
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        surface = pygame.Surface((width, height))

        # 垂直渐变
        for y in range(height):
            ratio = y / height
            color = tuple(
                int(colors[0][i] + (colors[1][i] - colors[0][i]) * ratio)
                for i in range(3)
            )
            pygame.draw.line(surface, color, (0, y), (width, y))

        # 保存
        filepath = output_dir / name
        pygame.image.save(surface, str(filepath))
        logger.info(f"Background '{name}' generated: {filepath}")

    def generate_icon_placeholder(
        self,
        size: int,
        icon_type: str,
        color: Tuple[int, int, int],
        output_dir: Path
    ) -> None:
        """
        生成图标占位符

        Args:
            size: 图标大小
            icon_type: 图标类型 (exit/debug/settings)
            color: 图标颜色
            output_dir: 输出目录
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # 根据类型绘制不同的简单图标
        center = size // 2
        if icon_type == 'exit':
            # 绘制X
            pygame.draw.line(surface, color, (10, 10), (size-10, size-10), 4)
            pygame.draw.line(surface, color, (size-10, 10), (10, size-10), 4)
        elif icon_type == 'debug':
            # 绘制齿轮（简化）
            pygame.draw.circle(surface, color, (center, center), size//3, 4)
            pygame.draw.circle(surface, color, (center, center), size//5, 4)
        elif icon_type == 'settings':
            # 绘制三条横线
            for i in range(3):
                y = 10 + i * (size - 20) // 2
                pygame.draw.line(surface, color, (10, y), (size-10, y), 4)
        else:
            # 默认绘制圆形
            pygame.draw.circle(surface, color, (center, center), size//2 - 5, 4)

        # 保存
        filename = f"{icon_type}_icon.png"
        filepath = output_dir / filename
        pygame.image.save(surface, str(filepath))
        logger.info(f"Icon '{icon_type}' generated: {filepath}")

    def generate_logo_placeholder(
        self,
        width: int,
        height: int,
        text: str,
        output_dir: Path
    ) -> None:
        """
        生成游戏标题LOGO占位符

        Args:
            width: LOGO宽度
            height: LOGO高度
            text: LOGO文字
            output_dir: 输出目录
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # 绘制边框
        pygame.draw.rect(
            surface,
            (184, 115, 51),  # 铜色
            (0, 0, width, height),
            5
        )

        # 绘制标题文字
        try:
            # 尝试使用中文字体
            font = pygame.font.Font("C:/WINDOWS/fonts/msyh.ttc", 48)
        except Exception:
            # 降级到默认字体
            font = pygame.font.Font(None, 64)

        text_surface = font.render(text, True, (255, 215, 0))  # 金色
        text_rect = text_surface.get_rect(center=(width//2, height//2))
        surface.blit(text_surface, text_rect)

        # 保存
        filename = "game_title.png"
        filepath = output_dir / filename
        pygame.image.save(surface, str(filepath))
        logger.info(f"Logo generated: {filepath}")

    def generate_all_placeholders(self) -> None:
        """生成所有占位符资源"""
        logger.info("="*60)
        logger.info("Starting placeholder generation...")
        logger.info("="*60)

        # 1. 生成按钮
        logger.info("Generating buttons...")
        button_dir = self.assets_dir / "ui" / "buttons"

        buttons = [
            (200, 50, "开始游戏", "start_button"),
            (200, 50, "退出游戏", "exit_button"),
            (200, 50, "下一关卡", "next_level"),
            (200, 50, "返回主菜单", "back_menu"),
            (200, 50, "重试一次", "retry"),
            (120, 40, "简单", "difficulty_easy"),
            (120, 40, "普通", "difficulty_normal"),
            (120, 40, "困难", "difficulty_hard"),
            (120, 40, "地狱", "difficulty_hell"),
        ]

        for width, height, label, _ in buttons:
            self.generate_button_placeholder(width, height, label, button_dir)

        # 2. 生成背景
        logger.info("Generating backgrounds...")
        bg_dir = self.assets_dir / "ui" / "backgrounds"

        backgrounds = [
            # (宽, 高, [颜色1, 颜色2], 文件名)
            (800, 600, [(80, 50, 30), (120, 80, 50)], "main_menu_bg.png"),
            (800, 600, [(60, 80, 100), (40, 60, 80)], "loading_bg_01.png"),
            (800, 600, [(80, 60, 90), (60, 40, 70)], "loading_bg_02.png"),
            (800, 600, [(90, 70, 60), (70, 50, 40)], "loading_bg_03.png"),
            (800, 600, [(40, 40, 40), (60, 60, 60)], "gameplay_bg.png"),
            (800, 600, [(255, 215, 0), (184, 115, 51)], "victory_bg.png"),
            (800, 600, [(80, 80, 80), (50, 50, 50)], "defeat_bg.png"),
        ]

        for width, height, colors, name in backgrounds:
            self.generate_background_placeholder(width, height, colors, name, bg_dir)

        # 3. 生成图标
        logger.info("Generating icons...")
        icon_dir = self.assets_dir / "ui" / "icons"

        icons = [
            (40, "exit", (255, 100, 100)),
            (40, "debug", (100, 200, 255)),
            (40, "settings", (200, 200, 200)),
        ]

        for size, icon_type, color in icons:
            self.generate_icon_placeholder(size, icon_type, color, icon_dir)

        # 4. 生成LOGO
        logger.info("Generating logo...")
        logo_dir = self.assets_dir / "ui" / "logo"
        self.generate_logo_placeholder(400, 120, "电路修复", logo_dir)

        # 5. 生成游戏图标（.ico格式需要额外处理）
        logger.info("Generating game icon...")
        icon_dir = self.assets_dir / "ui" / "icon"
        icon_dir.mkdir(parents=True, exist_ok=True)

        # 生成PNG图标（可以用工具转换为.ico）
        surface = pygame.Surface((256, 256))
        surface.fill((184, 115, 51))  # 铜色背景
        pygame.draw.circle(surface, (255, 215, 0), (128, 128), 100, 10)  # 金色圆环

        # 绘制简单的电路符号
        pygame.draw.line(surface, (255, 215, 0), (60, 128), (196, 128), 8)
        pygame.draw.circle(surface, (255, 215, 0), (128, 128), 30, 8)

        icon_path = icon_dir / "game_icon.png"
        pygame.image.save(surface, str(icon_path))
        logger.info(f"Game icon generated: {icon_path}")
        logger.warning("Note: .ico file needs to be converted from PNG using external tool")

        logger.info("="*60)
        logger.info("✓ All placeholders generated successfully!")
        logger.info("="*60)

        # 生成资源清单
        self._generate_resource_list()

    def _generate_resource_list(self) -> None:
        """生成资源清单文档"""
        list_file = self.assets_dir / "PLACEHOLDER_RESOURCES.md"

        content = """# 占位符资源清单

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
"""

        list_file.write_text(content, encoding='utf-8')
        logger.info(f"Resource list generated: {list_file}")


def main():
    """主函数"""
    print("="*60)
    print("占位符资源生成工具")
    print("Circuit Repair Game - Placeholder Generator")
    print("="*60)
    print()

    generator = PlaceholderGenerator()

    try:
        generator.generate_all_placeholders()
        print()
        print("="*60)
        print("✓ 所有占位符资源生成成功！")
        print()
        print("资源位置:")
        print(f"  - 按钮: {generator.assets_dir}/ui/buttons/")
        print(f"  - 背景: {generator.assets_dir}/ui/backgrounds/")
        print(f"  - 图标: {generator.assets_dir}/ui/icons/")
        print(f"  - LOGO: {generator.assets_dir}/ui/logo/")
        print(f"  - 应用图标: {generator.assets_dir}/ui/icon/")
        print()
        print("资源清单:")
        print(f"  - {generator.assets_dir}/PLACEHOLDER_RESOURCES.md")
        print()
        print("注意: 这些资源仅用于开发测试，")
        print("      正式发布前需要替换为正式美术资源。")
        print("="*60)

    except Exception as e:
        logger.error(f"Failed to generate placeholders: {e}", exc_info=True)
        print()
        print("="*60)
        print("✗ 生成失败！请查看日志了解详情。")
        print("="*60)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
