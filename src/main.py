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
        '--difficulty',
        type=str,
        choices=['easy', 'normal', 'hard', 'hell'],
        default='normal',
        help='Difficulty level: easy, normal, hard, hell (default: normal)'
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
    Callback function called when game session ends.

    Args:
        stats: Game statistics dictionary
    """
    logger = GameLogger.get_logger(__name__)
    logger.info("=" * 50)
    logger.info("🎮 GAME SESSION ENDED 🎮")
    logger.info("=" * 50)
    logger.info(f"Levels completed: {stats.get('levels_completed', 0)}")
    logger.info(f"Difficulty: {stats.get('difficulty', 'unknown')}")
    logger.info(f"Total moves: {stats.get('total_moves', 0)}")
    logger.info(f"Final state: {stats.get('final_state', 'unknown')}")
    logger.info("=" * 50)

    print("\n" + "=" * 50)
    print("🎮 GAME SESSION ENDED 🎮")
    print("=" * 50)
    print(f"Levels completed: {stats.get('levels_completed', 0)}")
    print(f"Difficulty: {stats.get('difficulty', 'unknown')}")
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

    # Difficulty display names
    difficulty_names = {
        'easy': '简单 (Easy)',
        'normal': '普通 (Normal)',
        'hard': '困难 (Hard)',
        'hell': '地狱 (Hell)'
    }

    # Print welcome message
    print("\n" + "=" * 60)
    print("  电路修复游戏 - CIRCUIT REPAIR GAME")
    print("=" * 60)
    print(f"游戏模式: 无限关卡 (Infinite Mode)")
    print(f"难度等级: {difficulty_names.get(args.difficulty, args.difficulty)}")
    print(f"窗口大小: {args.width}x{args.height}")
    print(f"目标帧率: {args.fps} FPS")
    print("=" * 60)
    print("\n玩法说明 (How to play):")
    print("  - 点击黑色方块旋转电路元件")
    print("    Click on black tiles to rotate circuit pieces")
    print("  - 连接电源到终端完成关卡")
    print("    Connect the power source to the terminal")
    print("  - 无限关卡，挑战你的极限！")
    print("    Infinite levels - challenge yourself!")
    print("=" * 60 + "\n")

    logger.info(f"Starting game in infinite mode with difficulty: {args.difficulty}")

    # Create game API
    game_api = GameAPI()

    # Start the game
    try:
        success = game_api.start_game(
            difficulty=args.difficulty,
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
