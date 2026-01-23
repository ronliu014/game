"""
Main Menu Scene Demo

Demonstrates the main menu scene functionality.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

import pygame
import sys
from src.scenes.scene_manager import SceneManager
from src.scenes.main_menu_scene import MainMenuScene
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


def main():
    """Run the main menu scene demo."""
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Create window
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Circuit Repair Game - Main Menu Demo")

    # Create clock for frame rate control
    clock = pygame.time.Clock()
    target_fps = 60

    # Create scene manager
    scene_manager = SceneManager()
    scene_manager.set_transition_duration(300)  # 300ms transitions

    # Start with main menu scene
    scene_manager.push_scene(
        MainMenuScene,
        data={
            'screen_width': screen_width,
            'screen_height': screen_height
        },
        transition=False
    )

    logger.info("Main menu demo started")

    # Main game loop
    running = True
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

        # Update display
        pygame.display.flip()

        # Check if scene stack is empty (should exit)
        if scene_manager.is_empty():
            running = False

    # Cleanup
    pygame.mixer.quit()
    pygame.quit()
    logger.info("Main menu demo ended")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Demo crashed: {e}", exc_info=True)
        sys.exit(1)
