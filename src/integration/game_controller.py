"""
Game Controller

Coordinates all game modules and manages game flow.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import pygame
from typing import Optional, List
from src.core.level.level_manager import LevelManager
from src.core.level.level_loader import LevelLoader
from src.core.game_state.state_machine import StateMachine, GameState
from src.rendering.renderer import Renderer
from src.audio.audio_manager import AudioManager
from src.audio.sound_player import SoundPlayer
from src.audio.bgm_controller import BGMController
from src.rendering.effects.particle_system import ParticleSystem
from src.rendering.effects.glow_effect import GlowEffect
from src.input.input_manager import InputManager
from src.input.mouse_handler import MouseHandler
from src.integration.scene_manager import SceneManager, SceneType
from src.utils.logger import GameLogger
from src.config.config_manager import ConfigManager


class GameController:
    """
    Game controller that coordinates all game modules.

    Manages game state, level progression, rendering, audio, and input.

    Attributes:
        _level_manager (LevelManager): Level manager
        _state_machine (StateMachine): Game state machine
        _renderer (Renderer): Renderer
        _audio_manager (AudioManager): Audio manager
        _sound_player (SoundPlayer): Sound player
        _bgm_controller (BGMController): BGM controller
        _particle_system (ParticleSystem): Particle system
        _glow_effect (GlowEffect): Glow effect
        _input_manager (InputManager): Input manager
        _mouse_handler (MouseHandler): Mouse handler
        _scene_manager (SceneManager): Scene manager
        _current_level_index (int): Current level index
        _level_ids (List[str]): List of level IDs to play
        _logger (GameLogger): Logger instance
    """

    def __init__(self):
        """Initialize the game controller."""
        self._level_loader: LevelLoader = LevelLoader()
        self._level_manager: LevelManager = LevelManager(self._level_loader)
        self._state_machine: StateMachine = StateMachine()
        self._renderer: Renderer = Renderer()
        self._audio_manager: AudioManager = AudioManager()
        self._sound_player: SoundPlayer = SoundPlayer(self._audio_manager)
        self._bgm_controller: BGMController = BGMController(self._audio_manager)
        self._particle_system: ParticleSystem = ParticleSystem(gravity=200.0)
        self._glow_effect: GlowEffect = GlowEffect()
        self._input_manager: InputManager = InputManager()
        self._mouse_handler: MouseHandler = MouseHandler()
        self._scene_manager: SceneManager = SceneManager()

        self._current_level_index: int = 0
        self._level_ids: List[str] = []
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def initialize(self, width: int = 800, height: int = 600) -> bool:
        """
        Initialize all game systems.

        Args:
            width: Window width
            height: Window height

        Returns:
            bool: True if successful, False otherwise
        """
        # Update config with window size
        config = ConfigManager.get_instance()
        config.set("window.width", width)
        config.set("window.height", height)

        # Initialize renderer
        if not self._renderer.initialize():
            self._logger.error("Failed to initialize renderer")
            return False

        # Initialize audio
        if not self._audio_manager.initialize():
            self._logger.error("Failed to initialize audio")
            return False

        # State machine is already in INIT state, no need to transition
        self._logger.info("Game controller initialized")
        return True

    def shutdown(self) -> None:
        """Shutdown all game systems."""
        self._renderer.shutdown()
        self._audio_manager.shutdown()
        self._logger.info("Game controller shutdown")

    def load_levels(self, level_ids: List[str]) -> bool:
        """
        Load levels for gameplay.

        Args:
            level_ids: List of level IDs to load

        Returns:
            bool: True if successful, False otherwise
        """
        self._level_ids = level_ids
        self._current_level_index = 0

        if not self._level_ids:
            self._logger.error("No levels to load")
            return False

        # Load first level
        return self._load_current_level()

    def _load_current_level(self) -> bool:
        """
        Load the current level.

        Returns:
            bool: True if successful, False otherwise
        """
        if self._current_level_index >= len(self._level_ids):
            self._logger.error("Level index out of range")
            return False

        level_id = self._level_ids[self._current_level_index]

        # Convert level_id to file path
        # If level_id is just an ID (e.g., "level_001"), convert to full path
        if not level_id.endswith('.json'):
            level_path = f"data/levels/{level_id}.json"
        else:
            level_path = level_id

        self._state_machine.transition_to(GameState.LOADING)

        if not self._level_manager.load_level(level_path):
            self._logger.error(f"Failed to load level: {level_id}")
            return False

        self._state_machine.transition_to(GameState.PLAYING)
        self._logger.info(f"Loaded level {self._current_level_index + 1}/{len(self._level_ids)}: {level_id}")
        return True

    def next_level(self) -> bool:
        """
        Load the next level.

        Returns:
            bool: True if there is a next level, False if all levels completed
        """
        self._current_level_index += 1

        if self._current_level_index >= len(self._level_ids):
            self._logger.info("All levels completed!")
            return False

        return self._load_current_level()

    def reset_current_level(self) -> None:
        """Reset the current level."""
        self._level_manager.reset_level()
        self._particle_system.clear()
        self._logger.info("Level reset")

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame event.

        Args:
            event: Pygame event
        """
        # Note: InputManager uses update() with a list of events, not individual events
        # So we'll handle events directly here instead

        # Handle mouse clicks on tiles
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._state_machine.get_current_state() == GameState.PLAYING:
                self._handle_tile_click(event.pos)

        # Pass to scene manager
        self._scene_manager.handle_event(event)

    def _handle_tile_click(self, pos: tuple[int, int]) -> None:
        """
        Handle tile click.

        Args:
            pos: Mouse position (x, y)
        """
        # Convert screen to grid coordinates
        grid_pos = self._mouse_handler.screen_to_grid(pos[0], pos[1])

        if grid_pos is None:
            return

        row, col = grid_pos

        # Try to rotate tile
        if self._level_manager.rotate_tile(row, col):
            # Play rotation sound
            self._sound_player.play_sound("sfx/tile_rotate.wav")

            # Emit spark particles
            screen_pos = self._mouse_handler.grid_to_screen(row, col)
            if screen_pos:
                self._particle_system.emit_sparks(screen_pos[0], screen_pos[1], count=10)

            # Check if level is complete
            if self._level_manager.is_level_complete():
                self._on_level_complete()

    def _on_level_complete(self) -> None:
        """Handle level completion."""
        self._state_machine.transition_to(GameState.VICTORY)

        # Play victory sound
        self._sound_player.play_sound("sfx/victory.wav")

        # Emit victory particles
        grid = self._level_manager.get_grid()
        if grid:
            terminal_pos = grid.get_terminal()
            if terminal_pos:
                screen_pos = self._mouse_handler.grid_to_screen(terminal_pos[0], terminal_pos[1])
                if screen_pos:
                    self._particle_system.emit_victory_effect(screen_pos[0], screen_pos[1])

        self._logger.info(f"Level complete! Moves: {self._level_manager.get_move_count()}")

    def update(self, delta_ms: float) -> None:
        """
        Update game logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Update particle system
        self._particle_system.update(delta_ms)

        # Update glow effect
        self._glow_effect.update(delta_ms)

        # Update scene manager
        self._scene_manager.update(delta_ms)

    def draw(self) -> None:
        """Draw the game."""
        # Clear screen
        self._renderer.clear()

        # Draw game elements based on state
        current_state = self._state_machine.get_current_state()

        if current_state in [GameState.PLAYING, GameState.VICTORY]:
            self._draw_game()

        # Draw particles
        surface = self._renderer.get_surface()
        if surface:
            self._particle_system.draw(surface)

        # Draw scene
        self._scene_manager.draw(self._renderer)

        # Present
        self._renderer.present()

    def _draw_game(self) -> None:
        """Draw game elements."""
        grid = self._level_manager.get_grid()
        if not grid:
            return

        # Draw grid tiles
        rows = grid.grid_size
        cols = grid.grid_size
        for row in range(rows):
            for col in range(cols):
                tile = grid.get_tile(row, col)
                if tile:
                    screen_pos = self._mouse_handler.grid_to_screen(row, col)
                    if screen_pos:
                        # Draw tile sprite
                        sprite_name = f"tile_{tile.tile_type.value}.png"
                        self._renderer.draw_sprite(sprite_name, screen_pos[0], screen_pos[1],
                                                   rotation=tile.rotation)

                        # Draw glow on terminal if connected
                        if tile.tile_type.value == "terminal" and self._level_manager.is_level_complete():
                            surface = self._renderer.get_surface()
                            if surface:
                                self._glow_effect.draw_glow_circle(surface, screen_pos[0], screen_pos[1],
                                                                   radius=32, glow_radius=15)

        # Draw HUD
        move_count = self._level_manager.get_move_count()
        level_num = self._current_level_index + 1
        total_levels = len(self._level_ids)

        self._renderer.draw_text(f"Level: {level_num}/{total_levels}", (10, 10))
        self._renderer.draw_text(f"Moves: {move_count}", (10, 40))

        if self._state_machine.get_current_state() == GameState.VICTORY:
            self._renderer.draw_text("VICTORY!", (300, 250), font_size=48, color=(255, 215, 0))

    def get_state(self) -> GameState:
        """
        Get current game state.

        Returns:
            GameState: Current game state
        """
        return self._state_machine.get_current_state()

    def get_level_manager(self) -> LevelManager:
        """
        Get level manager.

        Returns:
            LevelManager: Level manager instance
        """
        return self._level_manager

    def get_renderer(self) -> Renderer:
        """
        Get renderer.

        Returns:
            Renderer: Renderer instance
        """
        return self._renderer
