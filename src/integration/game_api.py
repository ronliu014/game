"""
Game API

External API for integrating the circuit repair game into other systems.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from typing import Optional, List, Callable, Dict, Any
from src.integration.game_controller import GameController
from src.integration.game_loop import GameLoop
from src.core.game_state.game_state import GameState
from src.utils.logger import GameLogger


class GameAPI:
    """
    External API for the circuit repair game.

    Provides a simple interface for starting, stopping, and monitoring the game.

    Example:
        ```python
        api = GameAPI()

        def on_complete(stats):
            print(f"Game completed! Total moves: {stats['total_moves']}")

        def on_exit():
            print("Game exited")

        api.start_game(
            level_ids=["level_001", "level_002", "level_003"],
            on_complete=on_complete,
            on_exit=on_exit
        )
        ```

    Attributes:
        _controller (GameController): Game controller
        _game_loop (GameLoop): Game loop
        _on_complete_callback (Optional[Callable]): Completion callback
        _on_exit_callback (Optional[Callable]): Exit callback
        _logger (GameLogger): Logger instance
    """

    def __init__(self):
        """Initialize the game API."""
        self._controller: Optional[GameController] = None
        self._game_loop: Optional[GameLoop] = None
        self._on_complete_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self._on_exit_callback: Optional[Callable[[], None]] = None
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def start_game(self,
                   difficulty: str = "normal",
                   on_complete: Optional[Callable[[Dict[str, Any]], None]] = None,
                   on_exit: Optional[Callable[[], None]] = None,
                   width: int = 800,
                   height: int = 600,
                   fps: int = 60) -> bool:
        """
        Start the game with infinite procedurally generated levels.

        Args:
            difficulty: Difficulty level ("easy", "normal", "hard", "hell")
            on_complete: Callback function called when all levels are completed.
                        Receives a dict with game statistics.
            on_exit: Callback function called when game exits (user closes window)
            width: Window width in pixels (default: 800)
            height: Window height in pixels (default: 600)
            fps: Target frames per second (default: 60)

        Returns:
            bool: True if game started successfully, False otherwise

        Example:
            ```python
            def on_complete(stats):
                print(f"Completed {stats['levels_completed']} levels")
                print(f"Total moves: {stats['total_moves']}")

            api.start_game(
                difficulty="normal",
                on_complete=on_complete
            )
            ```
        """
        # Store callbacks
        self._on_complete_callback = on_complete
        self._on_exit_callback = on_exit

        # Create game controller
        self._controller = GameController()

        # Initialize game systems
        if not self._controller.initialize(width, height):
            self._logger.error("Failed to initialize game controller")
            return False

        # Start game with infinite level generation
        if not self._controller.start_game(difficulty=difficulty):
            self._logger.error("Failed to start game")
            self._controller.shutdown()
            return False

        # Create and start game loop
        self._game_loop = GameLoop(target_fps=fps)

        try:
            self._game_loop.run(self._controller)
        except Exception as e:
            self._logger.error(f"Game loop error: {e}")
            return False
        finally:
            # Cleanup
            self._handle_game_end()

        return True

    def stop_game(self) -> None:
        """
        Stop the currently running game.

        This will exit the game loop and trigger the on_exit callback.
        """
        if self._game_loop and self._game_loop.is_running():
            self._game_loop.stop()
            self._logger.info("Game stopped by API call")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current game status.

        Returns:
            Dict containing:
                - is_running (bool): Whether game is running
                - current_state (str): Current game state
                - current_level (int): Current level number (1-indexed)
                - difficulty (str): Current difficulty level
                - move_count (int): Moves in current level
                - fps (float): Current FPS

        Example:
            ```python
            status = api.get_status()
            print(f"Level #{status['current_level']} ({status['difficulty']})")
            print(f"Moves: {status['move_count']}")
            ```
        """
        if not self._controller or not self._game_loop:
            return {
                "is_running": False,
                "current_state": "not_started",
                "current_level": 0,
                "difficulty": "normal",
                "move_count": 0,
                "fps": 0.0
            }

        level_manager = self._controller.get_level_manager()

        return {
            "is_running": self._game_loop.is_running(),
            "current_state": self._controller.get_state().value,
            "current_level": self._controller._current_level_number,
            "difficulty": self._controller.get_difficulty(),
            "move_count": level_manager.get_move_count() if level_manager else 0,
            "fps": self._game_loop.get_fps()
        }

    def _handle_game_end(self) -> None:
        """Handle game end (completion or exit)."""
        if not self._controller:
            return

        # In infinite mode, game never "completes" - only exits
        # Call exit callback
        if self._on_exit_callback:
            try:
                self._on_exit_callback()
            except Exception as e:
                self._logger.error(f"Error in exit callback: {e}")

        # Shutdown
        self._controller.shutdown()
        self._controller = None
        self._game_loop = None

    def _gather_statistics(self) -> Dict[str, Any]:
        """
        Gather game statistics.

        Returns:
            Dict containing game statistics
        """
        if not self._controller:
            return {}

        level_manager = self._controller.get_level_manager()

        return {
            "levels_completed": self._controller._current_level_number,
            "difficulty": self._controller.get_difficulty(),
            "total_moves": level_manager.get_move_count() if level_manager else 0,
            "final_state": self._controller.get_state().value
        }

    def is_running(self) -> bool:
        """
        Check if game is currently running.

        Returns:
            bool: True if game is running, False otherwise
        """
        return self._game_loop is not None and self._game_loop.is_running()
