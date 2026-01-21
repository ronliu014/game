"""
Game API Usage Example

Demonstrates how to use the GameAPI to integrate the circuit repair game.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from src.integration.game_api import GameAPI


def example_basic_usage():
    """Basic usage example - start game with default settings."""
    api = GameAPI()

    # Start game with 3 levels
    api.start_game(level_ids=["level_001", "level_002", "level_003"])


def example_with_callbacks():
    """Example with completion and exit callbacks."""
    api = GameAPI()

    def on_complete(stats):
        """Called when all levels are completed."""
        print("=" * 50)
        print("GAME COMPLETED!")
        print("=" * 50)
        print(f"Levels completed: {stats['levels_completed']}/{stats['total_levels']}")
        print(f"Total moves: {stats['total_moves']}")
        print(f"Final state: {stats['final_state']}")
        print("=" * 50)

    def on_exit():
        """Called when game exits."""
        print("Game exited. Thank you for playing!")

    # Start game with callbacks
    api.start_game(
        level_ids=["level_001", "level_002", "level_003"],
        on_complete=on_complete,
        on_exit=on_exit
    )


def example_custom_window():
    """Example with custom window size and FPS."""
    api = GameAPI()

    # Start game with custom settings
    api.start_game(
        level_ids=["level_001", "level_002"],
        width=1024,
        height=768,
        fps=60
    )


def example_single_level():
    """Example with a single level."""
    api = GameAPI()

    def on_complete(stats):
        print(f"Level completed in {stats['total_moves']} moves!")

    # Start game with single level
    api.start_game(
        level_ids=["level_001"],
        on_complete=on_complete
    )


def example_status_monitoring():
    """Example showing how to monitor game status (requires threading)."""
    import threading
    import time

    api = GameAPI()

    def monitor_status():
        """Monitor game status in a separate thread."""
        while api.is_running():
            status = api.get_status()
            print(f"Level {status['current_level']}/{status['total_levels']} | "
                  f"Moves: {status['move_count']} | "
                  f"FPS: {status['fps']:.1f} | "
                  f"State: {status['current_state']}")
            time.sleep(1)

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_status, daemon=True)
    monitor_thread.start()

    # Start game
    api.start_game(level_ids=["level_001", "level_002"])


def example_error_handling():
    """Example with error handling."""
    api = GameAPI()

    try:
        # Try to start game with invalid level IDs
        success = api.start_game(level_ids=[])
        if not success:
            print("Failed to start game: No levels provided")
    except Exception as e:
        print(f"Error starting game: {e}")


if __name__ == "__main__":
    # Run basic example
    print("Starting Circuit Repair Game...")
    print("Click on tiles to rotate them and connect the circuit!")
    print()

    # Choose which example to run
    example_with_callbacks()

    # Other examples (uncomment to try):
    # example_basic_usage()
    # example_custom_window()
    # example_single_level()
    # example_status_monitoring()
    # example_error_handling()
