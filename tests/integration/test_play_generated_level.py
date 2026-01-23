"""
Test playing a randomly generated level
"""
import sys
import pygame
from src.integration.game_controller import GameController
from src.core.level.level_manager import LevelManager
from src.core.level.level_loader import LevelLoader

def test_play_generated_level():
    """Test playing a procedurally generated level."""

    print("=" * 60, flush=True)
    print("LOADING RANDOMLY GENERATED LEVEL", flush=True)
    print("=" * 60, flush=True)
    print(flush=True)

    # Create game controller
    controller = GameController()
    print("GameController created", flush=True)

    # Initialize
    if not controller.initialize():
        print("Failed to initialize game controller!", flush=True)
        return

    print("GameController initialized", flush=True)

    # Load a randomly generated level
    level_manager = controller.get_level_manager()
    print("Loading generated level...", flush=True)
    success = level_manager.load_generated_level(
        grid_size=4,
        min_path_length=5,
        level_id="random_generated"
    )

    if not success:
        print("Failed to generate level!", flush=True)
        return

    print("Level loaded successfully", flush=True)

    # IMPORTANT: Update grid offset to center the grid on screen
    controller._update_grid_offset()
    print("Grid offset updated", flush=True)

    # IMPORTANT: Transition to PLAYING state so the game will render
    # Must go through LOADING state first (INIT -> LOADING -> PLAYING)
    from src.core.game_state.state_machine import GameState
    controller._state_machine.transition_to(GameState.LOADING)
    controller._state_machine.transition_to(GameState.PLAYING)
    print("State transitioned to PLAYING", flush=True)

    print("Level generated successfully!", flush=True)
    print(f"Grid size: 4x4", flush=True)
    print(f"Level ID: random_generated", flush=True)
    print(flush=True)
    print("Starting game...", flush=True)
    print("Click on tiles to rotate them and connect the circuit!", flush=True)
    print(flush=True)

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            controller.handle_event(event)

        # Update
        delta_ms = clock.tick(60)
        controller.update(delta_ms)

        # Draw
        controller.draw()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    test_play_generated_level()
