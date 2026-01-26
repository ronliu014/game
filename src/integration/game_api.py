"""
Game API

External API for integrating the circuit repair game into other systems.

Author: Circuit Repair Game Team
Date: 2026-01-20
Updated: 2026-01-25 - Added scene system integration
"""

from typing import Optional, List, Callable, Dict, Any
import pygame
from src.scenes.scene_manager import SceneManager
from src.scenes.main_menu_scene import MainMenuScene
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
            difficulty="normal",
            on_complete=on_complete,
            on_exit=on_exit
        )
        ```

    Attributes:
        _scene_manager (SceneManager): Scene manager for handling game scenes
        _game_loop (GameLoop): Game loop
        _screen (pygame.Surface): Main display surface
        _on_complete_callback (Optional[Callable]): Completion callback
        _on_exit_callback (Optional[Callable]): Exit callback
        _logger (GameLogger): Logger instance
    """

    def __init__(self):
        """Initialize the game API."""
        self._scene_manager: Optional[SceneManager] = None
        self._game_loop: Optional[GameLoop] = None
        self._screen: Optional[pygame.Surface] = None
        self._on_complete_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self._on_exit_callback: Optional[Callable[[], None]] = None
        self._logger: GameLogger = GameLogger.get_logger(__name__)
        self._width: int = 800
        self._height: int = 600

    def start_game(self,
                   difficulty: str = "normal",
                   on_complete: Optional[Callable[[Dict[str, Any]], None]] = None,
                   on_exit: Optional[Callable[[], None]] = None,
                   width: int = 800,
                   height: int = 600,
                   fps: int = 60) -> bool:
        """
        Start the game with complete UI flow (Main Menu -> Loading -> Gameplay -> Result).

        Args:
            difficulty: Default difficulty level ("easy", "normal", "hard", "hell")
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
        # Store callbacks and settings
        self._on_complete_callback = on_complete
        self._on_exit_callback = on_exit
        self._width = width
        self._height = height

        # Initialize Pygame
        if not self._initialize_pygame(width, height):
            self._logger.error("Failed to initialize Pygame")
            return False

        # Create scene manager
        self._scene_manager = SceneManager()
        self._logger.info("SceneManager created")

        # Push main menu scene as the initial scene
        initial_data = {
            'screen_width': width,
            'screen_height': height,
            'default_difficulty': difficulty,
            'on_complete_callback': on_complete,
            'on_exit_callback': on_exit
        }
        self._logger.info(f"Pushing MainMenuScene with data: {initial_data}")
        self._scene_manager.push_scene(MainMenuScene, data=initial_data, transition=False)
        self._logger.info(f"MainMenuScene pushed. Current scene: {self._scene_manager.get_current_scene()}")

        # Create and start game loop
        self._game_loop = GameLoop(target_fps=fps)

        try:
            self._run_scene_loop()
        except Exception as e:
            self._logger.error(f"Game loop error: {e}", exc_info=True)
            return False
        finally:
            # Cleanup
            self._handle_game_end()

        return True

    def _initialize_pygame(self, width: int, height: int) -> bool:
        """
        Initialize Pygame and create display window.

        Args:
            width: Window width
            height: Window height

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pygame.init()
            pygame.mixer.init()

            # Create display window
            self._screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("电路板修复游戏 - Circuit Repair Game")

            self._logger.info(f"Pygame initialized: {width}x{height}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to initialize Pygame: {e}", exc_info=True)
            return False

    def _run_scene_loop(self) -> None:
        """
        Run the main game loop with scene manager.
        """
        self._logger.info(f"Starting scene loop. Current scene: {self._scene_manager.get_current_scene()}")
        self._logger.info(f"Scene stack size: {self._scene_manager.get_stack_size()}")

        self._game_loop.start()
        clock = pygame.time.Clock()

        while self._game_loop.is_running():
            # Get delta time
            delta_ms = clock.get_time()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game_loop.stop()
                    break

                # Pass event to scene manager
                if self._scene_manager:
                    self._scene_manager.handle_event(event)

            # Check if scene stack is empty (all scenes exited)
            if self._scene_manager and self._scene_manager.is_empty():
                self._logger.info("Scene stack empty, exiting game")
                self._game_loop.stop()
                break

            # Update scene manager
            if self._game_loop.is_running() and self._scene_manager:
                self._scene_manager.update(delta_ms)

            # Render
            if self._game_loop.is_running() and self._scene_manager:
                # Clear screen
                self._screen.fill((0, 0, 0))

                # Draw current scene
                self._scene_manager.draw(self._screen)

                # Update display
                pygame.display.flip()

            # Cap frame rate
            clock.tick(self._game_loop.get_target_fps())

        self._logger.info("Scene loop ended")

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
                - current_scene (str): Current scene name
                - stack_size (int): Number of scenes in stack

        Example:
            ```python
            status = api.get_status()
            print(f"Current scene: {status['current_scene']}")
            ```
        """
        if not self._scene_manager or not self._game_loop:
            return {
                "is_running": False,
                "current_scene": "none",
                "stack_size": 0
            }

        current_scene = self._scene_manager.get_current_scene()
        scene_name = current_scene.__class__.__name__ if current_scene else "none"

        return {
            "is_running": self._game_loop.is_running(),
            "current_scene": scene_name,
            "stack_size": self._scene_manager.get_stack_size()
        }

    def _handle_game_end(self) -> None:
        """Handle game end (completion or exit)."""
        # Call exit callback
        if self._on_exit_callback:
            try:
                self._on_exit_callback()
            except Exception as e:
                self._logger.error(f"Error in exit callback: {e}")

        # Cleanup scene manager
        if self._scene_manager:
            self._scene_manager.clear_stack()
            self._scene_manager = None

        # Cleanup pygame
        pygame.quit()

        self._game_loop = None
        self._screen = None

        self._logger.info("Game API cleanup completed")

    def is_running(self) -> bool:
        """
        Check if game is currently running.

        Returns:
            bool: True if game is running, False otherwise
        """
        return self._game_loop is not None and self._game_loop.is_running()
