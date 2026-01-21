"""
Circuit Repair Game - Main Entry Point

A standalone puzzle game where players rotate circuit pieces to connect
a power source to a terminal.

Usage:
    python src/main.py
    python src/main.py --level level_001
    python src/main.py --levels level_001,level_002,level_003

Author: Circuit Repair Game Team
Date: 2026-01-21
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.integration.game_api import GameAPI
from src.utils.logger import GameLogger
from src.config.config_manager import ConfigManager


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Circuit Repair Game - A puzzle game about connecting circuits"
    )

    parser.add_argument(
        '--level',
        type=str,
        help='Single level ID to play (e.g., level_001)'
    )

    parser.add_argument(
        '--levels',
        type=str,
        help='Comma-separated level IDs to play (e.g., level_001,level_002)'
    )

    parser.add_argument(
        '--width',
        type=int,
        default=800,
        help='Window width in pixels (default: 800)'
    )

    parser.add_argument(
        '--height',
        type=int,
        default=600,
        help='Window height in pixels (default: 600)'
    )

    parser.add_argument(
        '--fps',
        type=int,
        default=60,
        help='Target FPS (default: 60)'
    )

    return parser.parse_args()


def on_level_complete(stats: dict):
    """
    Callback function called when all levels are completed.

    Args:
        stats: Game statistics dictionary
    """
    logger = GameLogger.get_logger(__name__)
    logger.info("=" * 50)
    logger.info("🎉 ALL LEVELS COMPLETED! 🎉")
    logger.info("=" * 50)
    logger.info(f"Levels completed: {stats.get('levels_completed', 0)}/{stats.get('total_levels', 0)}")
    logger.info(f"Total moves: {stats.get('total_moves', 0)}")
    logger.info(f"Final state: {stats.get('final_state', 'unknown')}")
    logger.info("=" * 50)

    print("\n" + "=" * 50)
    print("🎉 CONGRATULATIONS! ALL LEVELS COMPLETED! 🎉")
    print("=" * 50)
    print(f"Levels completed: {stats.get('levels_completed', 0)}/{stats.get('total_levels', 0)}")
    print(f"Total moves: {stats.get('total_moves', 0)}")
    print("=" * 50)


def on_game_exit():
    """
    Callback function called when game exits.
    """
    logger = GameLogger.get_logger(__name__)
    logger.info("Game exited by user")
    print("\nThank you for playing Circuit Repair Game!")


def main():
    """
    Main entry point for the game.
    """
    # Parse command line arguments
    args = parse_arguments()

    # Initialize logger
    logger = GameLogger.get_logger(__name__)

    # Initialize configuration
    ConfigManager.initialize('data/config/game_config.json')

    # Determine which levels to load
    if args.level:
        # Single level specified
        level_ids = [args.level]
    elif args.levels:
        # Multiple levels specified
        level_ids = [lvl.strip() for lvl in args.levels.split(',')]
    else:
        # Default: play all available levels
        level_ids = ['level_001', 'level_002', 'level_003', 'level_004', 'level_005']

    # Print welcome message
    print("\n" + "=" * 50)
    print("  CIRCUIT REPAIR GAME")
    print("=" * 50)
    print(f"Levels to play: {len(level_ids)}")
    print(f"Window size: {args.width}x{args.height}")
    print(f"Target FPS: {args.fps}")
    print("=" * 50)
    print("\nHow to play:")
    print("  - Click on black tiles to rotate circuit pieces")
    print("  - Connect the power source to the terminal")
    print("  - Complete all levels to win!")
    print("=" * 50 + "\n")

    logger.info(f"Starting game with {len(level_ids)} levels: {level_ids}")

    # Create game API
    game_api = GameAPI()

    # Start the game
    try:
        success = game_api.start_game(
            level_ids=level_ids,
            on_complete=on_level_complete,
            on_exit=on_game_exit,
            width=args.width,
            height=args.height,
            fps=args.fps
        )

        if not success:
            logger.error("Failed to start game")
            print("\nError: Failed to start game. Please check the logs for details.")
            return 1

    except KeyboardInterrupt:
        logger.info("Game interrupted by user (Ctrl+C)")
        print("\n\nGame interrupted by user.")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nError: {e}")
        print("Please check the logs for details.")
        return 1

    logger.info("Game ended normally")
    return 0


if __name__ == "__main__":
    sys.exit(main())
