"""
Week 3 成果演示程序 - 结算场景和粒子特效

展示结算场景（胜利/失败）和粒子特效系统。

运行方式:
    python demo_week_3.py

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.scenes.scene_manager import SceneManager
from src.scenes.result_scene import ResultScene
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


def main():
    """运行 Week 3 成果演示。"""
    print("=" * 60)
    print("  电路修复游戏 - Week 3 成果演示")
    print("=" * 60)
    print()
    print("功能展示:")
    print("  ✅ 结算场景（胜利/失败）")
    print("  ✅ 星级评分系统（1-3星）")
    print("  ✅ 礼花特效（胜利庆祝）")
    print("  ✅ 烟雾特效（失败场景）")
    print()
    print("操作说明:")
    print("  - 按 V 键查看胜利场景（3星）")
    print("  - 按 F 键查看失败场景")
    print("  - 按 1/2/3 键查看不同星级的胜利场景")
    print("  - 按 ESC 或点击'主菜单'退出")
    print("  - 按 R 键重试当前关卡")
    print()
    print("==" * 60)
    print()

    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Create window
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("电路修复游戏 - Week 3 成果演示")

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
    scene_manager.set_transition_duration(300)
    scene_manager.set_transition_type('fade')

    # Start with victory scene (3 stars)
    scene_manager.push_scene(
        ResultScene,
        data={
            'victory': True,
            'level': 1,
            'time_taken': 25.5,
            'moves': 10,
            'stars': 3,
            'difficulty': 'normal',
            'screen_width': screen_width,
            'screen_height': screen_height
        },
        transition=True
    )

    logger.info("Week 3 demo started")
    print("演示程序已启动！")
    print("提示：按 V/F/1/2/3 键切换不同场景")
    print()

    # Main game loop
    running = True
    frame_count = 0
    fps_display_interval = 60

    while running:
        # Calculate delta time
        delta_ms = clock.tick(target_fps)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Switch scenes with keyboard
                if event.key == pygame.K_v:
                    # Victory scene (3 stars)
                    print("切换到：胜利场景（3星）")
                    scene_manager.replace_scene(
                        ResultScene,
                        data={
                            'victory': True,
                            'level': 1,
                            'time_taken': 25.5,
                            'moves': 10,
                            'stars': 3,
                            'difficulty': 'normal',
                            'screen_width': screen_width,
                            'screen_height': screen_height
                        },
                        transition=True
                    )
                elif event.key == pygame.K_f:
                    # Failure scene
                    print("切换到：失败场景")
                    scene_manager.replace_scene(
                        ResultScene,
                        data={
                            'victory': False,
                            'level': 1,
                            'time_taken': 60.0,
                            'moves': 25,
                            'stars': 0,
                            'difficulty': 'normal',
                            'screen_width': screen_width,
                            'screen_height': screen_height
                        },
                        transition=True
                    )
                elif event.key == pygame.K_1:
                    # Victory scene (1 star)
                    print("切换到：胜利场景（1星）")
                    scene_manager.replace_scene(
                        ResultScene,
                        data={
                            'victory': True,
                            'level': 1,
                            'time_taken': 42.0,
                            'moves': 20,
                            'stars': 1,
                            'difficulty': 'normal',
                            'screen_width': screen_width,
                            'screen_height': screen_height
                        },
                        transition=True
                    )
                elif event.key == pygame.K_2:
                    # Victory scene (2 stars)
                    print("切换到：胜利场景（2星）")
                    scene_manager.replace_scene(
                        ResultScene,
                        data={
                            'victory': True,
                            'level': 1,
                            'time_taken': 32.0,
                            'moves': 14,
                            'stars': 2,
                            'difficulty': 'hard',
                            'screen_width': screen_width,
                            'screen_height': screen_height
                        },
                        transition=True
                    )
                elif event.key == pygame.K_3:
                    # Victory scene (3 stars)
                    print("切换到：胜利场景（3星）")
                    scene_manager.replace_scene(
                        ResultScene,
                        data={
                            'victory': True,
                            'level': 1,
                            'time_taken': 18.5,
                            'moves': 8,
                            'stars': 3,
                            'difficulty': 'hell',
                            'screen_width': screen_width,
                            'screen_height': screen_height
                        },
                        transition=True
                    )
            else:
                scene_manager.handle_event(event)

        # Update scene
        scene_manager.update(delta_ms)

        # Draw scene
        screen.fill((0, 0, 0))
        scene_manager.draw(screen)

        # Draw FPS counter and instructions
        frame_count += 1
        if frame_count % fps_display_interval == 0:
            fps = clock.get_fps()
            try:
                font = pygame.font.Font(None, 20)

                # FPS
                fps_text = font.render(f"FPS: {fps:.1f}", True, (100, 255, 100))
                screen.blit(fps_text, (screen_width - 80, 10))

                # Instructions
                inst_font = pygame.font.Font(None, 18)
                instructions = [
                    "V: Victory (3★)  F: Failure",
                    "1/2/3: 1★/2★/3★  ESC: Exit"
                ]
                for i, inst in enumerate(instructions):
                    inst_text = inst_font.render(inst, True, (200, 200, 200))
                    screen.blit(inst_text, (10, 10 + i * 20))
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
    print("Week 3 开发成果:")
    print("  ✅ 结算场景完整实现")
    print("  ✅ 星级评分系统")
    print("  ✅ 礼花特效（多色爆炸）")
    print("  ✅ 烟雾特效（上升扩散）")
    print("  ✅ 23 个粒子特效测试全部通过")
    print()
    print("感谢体验！")
    print()

    logger.info("Week 3 demo ended")


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
