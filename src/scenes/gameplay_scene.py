"""
Gameplay Scene

Main game scene with layered rendering system.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Dict, Any, List
import pygame
from src.scenes.scene_base import SceneBase
from src.scenes.layers.background_layer import BackgroundLayer
from src.scenes.layers.game_layer import GameLayer
from src.scenes.layers.hud_layer import HUDLayer
from src.scenes.layers.debug_layer import DebugLayer
from src.scenes.layers.layer_base import LayerBase
from src.core.timer.game_timer import GameTimer
from src.integration.game_controller import GameController
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class GameplayScene(SceneBase):
    """
    Main gameplay scene with 4-layer rendering system.

    Layers (bottom to top):
        1. Background Layer - Background rendering
        2. Game Layer - Game logic and rendering
        3. HUD Layer - UI overlay (timer, moves, etc.)
        4. Debug Layer - Debug information

    Features:
        - Layered rendering system
        - GameController integration
        - Countdown timer
        - Move counter
        - Pause functionality
        - Debug overlay (F3 to toggle)

    Example:
        >>> scene = GameplayScene(scene_manager)
        >>> scene.on_enter(data={
        ...     'level': 1,
        ...     'difficulty': 'normal',
        ...     'time_limit': 60.0,
        ...     'screen_width': 800,
        ...     'screen_height': 600
        ... })
    """

    def __init__(self, scene_manager=None):
        """
        Initialize the gameplay scene.

        Args:
            scene_manager: Reference to the scene manager
        """
        super().__init__(scene_manager)

        # Screen dimensions
        self._screen_width = 800
        self._screen_height = 600

        # Game data
        self._level = 1
        self._difficulty = 'normal'
        self._time_limit = 60.0

        # Layers
        self._layers: List[LayerBase] = []
        self._background_layer: Optional[BackgroundLayer] = None
        self._game_layer: Optional[GameLayer] = None
        self._hud_layer: Optional[HUDLayer] = None
        self._debug_layer: Optional[DebugLayer] = None

        # Game components
        self._game_controller: Optional[GameController] = None
        self._game_timer: Optional[GameTimer] = None

        # State
        self._is_paused = False
        self._game_started = False

        logger.debug("GameplayScene initialized")

    def on_enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when the scene becomes active.

        Args:
            data: Optional data containing:
                - level (int): Level number
                - difficulty (str): Difficulty level
                - time_limit (float): Time limit in seconds
                - screen_width (int): Screen width
                - screen_height (int): Screen height
                - game_controller (GameController): Optional game controller
        """
        super().on_enter(data)

        # Get screen dimensions
        self._screen_width = self.get_transition_data('screen_width', 800)
        self._screen_height = self.get_transition_data('screen_height', 600)

        # Get game data
        self._level = self.get_transition_data('level', 1)
        self._difficulty = self.get_transition_data('difficulty', 'normal')
        self._time_limit = self.get_transition_data('time_limit', 60.0)

        # Get or create game controller
        self._game_controller = self.get_transition_data('game_controller', None)

        # Create game timer
        self._game_timer = GameTimer(self._time_limit)
        self._game_timer.set_timeout_callback(self._on_timeout)

        # Create layers
        self._create_layers()

        # Start game
        self._start_game()

        logger.info(f"GameplayScene entered: level={self._level}, difficulty={self._difficulty}, time_limit={self._time_limit}s")

    def on_exit(self) -> None:
        """Called when the scene is being replaced or removed."""
        super().on_exit()

        # Stop timer
        if self._game_timer:
            self._game_timer.stop()

        # Clean up layers
        for layer in self._layers:
            layer.on_exit()

        logger.info("GameplayScene exited")

    def update(self, delta_ms: float) -> None:
        """
        Update scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if self._is_paused:
            return

        # Update timer
        if self._game_timer:
            self._game_timer.update(delta_ms)

        # Update all layers
        for layer in self._layers:
            if layer.is_enabled():
                layer.update(delta_ms)

        # Update HUD with game state
        if self._hud_layer and self._game_controller:
            move_count = self._game_controller.get_move_count()
            self._hud_layer.set_move_count(move_count)

        # Update debug info
        if self._debug_layer:
            self._update_debug_info()

        # Check for game over
        if self._game_controller and self._game_controller.is_game_over():
            self._on_game_over()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the scene.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw all layers in order
        for layer in self._layers:
            if layer.is_visible():
                layer.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        # Handle pause key (ESC)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._toggle_pause()
                return True

        # Pass event to layers (top to bottom)
        for layer in reversed(self._layers):
            if layer.is_enabled() and layer.handle_event(event):
                return True

        return False

    def _create_layers(self) -> None:
        """Create all scene layers."""
        # 1. Background Layer
        self._background_layer = BackgroundLayer(
            self._screen_width,
            self._screen_height,
            background_color=(20, 30, 40)
        )

        # 2. Game Layer
        self._game_layer = GameLayer(
            self._screen_width,
            self._screen_height,
            self._game_controller
        )

        # 3. HUD Layer
        self._hud_layer = HUDLayer(
            self._screen_width,
            self._screen_height,
            level=self._level,
            difficulty=self._difficulty,
            timer=self._game_timer,
            on_pause=self._toggle_pause
        )

        # 4. Debug Layer
        self._debug_layer = DebugLayer(
            self._screen_width,
            self._screen_height
        )

        # Add layers in rendering order
        self._layers = [
            self._background_layer,
            self._game_layer,
            self._hud_layer,
            self._debug_layer
        ]

        # Call on_enter for all layers
        for layer in self._layers:
            layer.on_enter()

        logger.debug("All layers created")

    def _start_game(self) -> None:
        """Start the game."""
        if self._game_timer:
            self._game_timer.start()

        self._game_started = True
        self._is_paused = False

        logger.info("Game started")

    def _toggle_pause(self) -> None:
        """Toggle pause state."""
        self._is_paused = not self._is_paused

        if self._game_timer:
            if self._is_paused:
                self._game_timer.pause()
            else:
                self._game_timer.resume()

        logger.info(f"Game {'paused' if self._is_paused else 'resumed'}")

    def _on_timeout(self) -> None:
        """Handle timer timeout."""
        logger.info("Timer timeout - game over")
        self._on_game_over(victory=False)

    def _on_game_over(self, victory: Optional[bool] = None) -> None:
        """
        Handle game over.

        Args:
            victory: Whether player won (None = check game controller)
        """
        if victory is None and self._game_controller:
            victory = self._game_controller.is_victory()

        # Stop timer
        if self._game_timer:
            self._game_timer.stop()

        # Prepare result data
        result_data = {
            'victory': victory,
            'level': self._level,
            'time_taken': self._game_timer.get_elapsed_time() if self._game_timer else 0.0,
            'moves': self._game_controller.get_move_count() if self._game_controller else 0,
            'stars': 0,  # Will be calculated by ResultScene
            'difficulty': self._difficulty,
            'screen_width': self._screen_width,
            'screen_height': self._screen_height
        }

        logger.info(f"Game over: victory={victory}, moves={result_data['moves']}, time={result_data['time_taken']:.1f}s")

        # Transition to result scene
        from src.scenes.result_scene import ResultScene
        self.request_scene_change(ResultScene, data=result_data, replace=True)

    def _update_debug_info(self) -> None:
        """Update debug layer information."""
        if not self._debug_layer:
            return

        # FPS (approximate from delta time)
        self._debug_layer.set_debug_value('Level', self._level)
        self._debug_layer.set_debug_value('Difficulty', self._difficulty)

        if self._game_timer:
            self._debug_layer.set_debug_value('Time', self._game_timer.format_time())
            self._debug_layer.set_debug_value('Paused', self._is_paused)

        if self._game_controller:
            self._debug_layer.set_debug_value('Moves', self._game_controller.get_move_count())

    def is_paused(self) -> bool:
        """
        Check if game is paused.

        Returns:
            bool: True if paused, False otherwise
        """
        return self._is_paused

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get current game state.

        Returns:
            Dict containing game state information
        """
        return {
            'level': self._level,
            'difficulty': self._difficulty,
            'time_limit': self._time_limit,
            'time_remaining': self._game_timer.get_remaining_time() if self._game_timer else 0.0,
            'moves': self._game_controller.get_move_count() if self._game_controller else 0,
            'is_paused': self._is_paused,
            'game_started': self._game_started
        }
