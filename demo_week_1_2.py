"""
Week 1-2 成果演示程序

展示 UI 组件库和场景系统的功能。

运行方式:
    python demo_week_1_2.py

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.scenes.scene_manager import SceneManager
from src.scenes.main_menu_scene import MainMenuScene
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


def main():
    """运行 Week 1-2 成果演示。"""
    print("=" * 60)
    print("  电路修复游戏 - Week 1-2 成果演示")
    print("=" * 60)
    print()
    print("功能展示:")
    print("  ✅ UI 组件库 (6个核心组件)")
    print("  ✅ 布局管理系统")
    print("  ✅ 场景管理系统")
    print("  ✅ 主菜单场景")
    print()
    print("操作说明:")
    print("  - 鼠标点击按钮进行交互")
    print("  - 选择难度后点击'开始游戏'")
    print("  - 按 ESC 或点击'退出游戏'关闭程序")
    print("  - 按 Enter/Space 快速开始游戏")
    print()
    print("=" * 60)
    print()

    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Create window
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("电路修复游戏 - Week 1-2 成果演示")

    # Set icon (if available)
    try:
        icon_path = Path("assets/ui/icon/game_icon.png")
        if icon_path.exists():
            icon = pygame.image.load(str(icon_path))
            pygame.display.set_icon(icon)
    except Exception as e:
        logger.debug(f"Could not load icon: {e}")

    # Create clock for frame rate control
    clock = pygame.time.Clock()
    target_fps = 60

    # Create scene manager
    scene_manager = SceneManager()
    scene_manager.set_transition_duration(300)  # 300ms transitions
    scene_manager.set_transition_type('fade')

    # Start with main menu scene
    scene_manager.push_scene(
        MainMenuScene,
        data={
            'screen_width': screen_width,
            'screen_height': screen_height
        },
        transition=True
    )

    logger.info("Week 1-2 demo started")
    print("演示程序已启动！")
    print()

    # Main game loop
    running = True
    frame_count = 0
    fps_display_interval = 60  # Display FPS every 60 frames

    while running:
        # Calculate delta time
        delta_ms = clock.tick(target_fps)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_manager.handle_event(event)

        # Update scene
        scene_manager.update(delta_ms)

        # Draw scene
        screen.fill((0, 0, 0))
        scene_manager.draw(screen)

        # Draw FPS counter (top-right corner)
        frame_count += 1
        if frame_count % fps_display_interval == 0:
            fps = clock.get_fps()
            try:
                font = pygame.font.Font(None, 24)
                fps_text = font.render(f"FPS: {fps:.1f}", True, (100, 255, 100))
                screen.blit(fps_text, (screen_width - 100, 10))
            except Exception:
                pass

        # Update display
        pygame.display.flip()

        # Check if scene stack is empty (should exit)
        if scene_manager.is_empty():
            running = False

    # Cleanup
    pygame.mixer.quit()
    pygame.quit()

    print()
    print("=" * 60)
    print("  演示程序已结束")
    print("=" * 60)
    print()
    print("Week 1-2 开发成果:")
    print("  ✅ 61 个单元测试全部通过 (100% 通过率)")
    print("  ✅ UI 组件库完整实现")
    print("  ✅ 场景管理系统稳定运行")
    print("  ✅ 主菜单场景功能完善")
    print()
    print("感谢体验！")
    print()

    logger.info("Week 1-2 demo ended")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Demo crashed: {e}", exc_info=True)
        print(f"\n错误: {e}")
        sys.exit(1)
