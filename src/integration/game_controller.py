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

        # Infinite level generation mode
        self._current_level_number: int = 1
        self._difficulty: str = "normal"  # Default difficulty
        self._infinite_mode: bool = True  # Always use infinite mode
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

    def start_game(self, difficulty: str = "normal") -> bool:
        """
        Start the game with infinite procedurally generated levels.

        Args:
            difficulty: Difficulty level ("easy", "normal", "hard", "hell")

        Returns:
            bool: True if successful, False otherwise
        """
        self._difficulty = difficulty.lower()
        self._current_level_number = 1
        self._infinite_mode = True

        self._logger.info(f"Starting infinite mode with difficulty: {self._difficulty}")

        # Generate and load first level
        return self._load_next_generated_level()

    def set_difficulty(self, difficulty: str) -> None:
        """
        Set the difficulty level for future levels.

        Args:
            difficulty: Difficulty level ("easy", "normal", "hard", "hell")
        """
        self._difficulty = difficulty.lower()
        self._logger.info(f"Difficulty set to: {self._difficulty}")

    def get_difficulty(self) -> str:
        """
        Get the current difficulty level.

        Returns:
            str: Current difficulty level
        """
        return self._difficulty

    def _update_grid_offset(self) -> None:
        """
        Calculate and update grid offset to center the grid on screen.
        Also dynamically adjusts tile size to fit the grid in the window.
        """
        grid = self._level_manager.get_grid()
        if not grid:
            return

        # Get window size from config
        config = ConfigManager.get_instance()
        window_width = config.get("window.width", 800)
        window_height = config.get("window.height", 600)

        # Get grid size
        grid_size = grid.grid_size

        # Reserve space for HUD (top area)
        hud_height = 80  # Reserve 80px for HUD text at top
        available_width = window_width - 40  # 20px margin on each side
        available_height = window_height - hud_height - 40  # 20px margin on bottom

        # Calculate maximum tile size that fits in available space
        tile_padding = 4
        max_tile_size_width = (available_width - (grid_size - 1) * tile_padding) // grid_size
        max_tile_size_height = (available_height - (grid_size - 1) * tile_padding) // grid_size

        # Use the smaller of the two to ensure it fits both dimensions
        tile_size = min(max_tile_size_width, max_tile_size_height, 128)  # Cap at 128px max

        # Ensure minimum tile size
        tile_size = max(tile_size, 48)  # Minimum 48px for visibility

        # Update mouse handler with new tile size
        self._mouse_handler.set_tile_size(tile_size, tile_padding)

        # Calculate total grid dimensions with new tile size
        tile_total_size = tile_size + tile_padding
        total_grid_width = grid_size * tile_total_size - tile_padding
        total_grid_height = grid_size * tile_total_size - tile_padding

        # Calculate offset to center the grid (accounting for HUD space)
        offset_x = (window_width - total_grid_width) // 2
        offset_y = hud_height + (available_height - total_grid_height) // 2

        # Set the offset
        self._mouse_handler.set_grid_offset(offset_x, offset_y)
        self._logger.info(
            f"Grid layout: {grid_size}x{grid_size}, tile_size={tile_size}px, "
            f"offset=({offset_x}, {offset_y})"
        )

    def _load_next_generated_level(self) -> bool:
        """
        Generate and load the next level.

        Returns:
            bool: True if successful, False otherwise
        """
        self._logger.info("="*60)
        self._logger.info(f"Generating new level #{self._current_level_number}")
        self._logger.info(f"Difficulty: {self._difficulty}")
        self._logger.info("="*60)

        self._state_machine.transition_to(GameState.LOADING)

        # Generate level with current difficulty
        if not self._level_manager.load_generated_level(
            difficulty=self._difficulty,
            level_number=self._current_level_number
        ):
            self._logger.error(f"Failed to generate level #{self._current_level_number}")
            return False

        # Log level details
        grid = self._level_manager.get_grid()
        if grid:
            self._logger.info(f"Level generated successfully:")
            self._logger.info(f"  - Grid size: {grid.grid_size}x{grid.grid_size}")
            self._logger.info(f"  - Total tiles: {grid.grid_size * grid.grid_size}")

            # Count tile types
            power_count = 0
            terminal_count = 0
            clickable_count = 0
            empty_count = 0

            for row in range(grid.grid_size):
                for col in range(grid.grid_size):
                    tile = grid.get_tile(row, col)
                    if tile:
                        if tile.tile_type.value == "power_source":
                            power_count += 1
                        elif tile.tile_type.value == "terminal":
                            terminal_count += 1
                        elif tile.tile_type.value == "empty":
                            empty_count += 1
                        if tile.is_clickable:
                            clickable_count += 1

            self._logger.info(f"  - Power sources: {power_count}")
            self._logger.info(f"  - Terminals: {terminal_count}")
            self._logger.info(f"  - Clickable tiles: {clickable_count}")
            self._logger.info(f"  - Empty tiles: {empty_count}")

        # Calculate and set grid offset to center the grid on screen
        self._update_grid_offset()

        self._state_machine.transition_to(GameState.PLAYING)
        self._logger.info(f"Level #{self._current_level_number} ready to play!")
        self._logger.info("="*60)
        return True

    def next_level(self) -> bool:
        """
        Generate and load the next level (infinite mode).

        Returns:
            bool: Always True in infinite mode
        """
        self._current_level_number += 1
        return self._load_next_generated_level()

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
            self._logger.debug(f"Click at screen position {pos} - outside grid")
            return

        row, col = grid_pos
        self._logger.info(f"User clicked tile at grid position ({row}, {col}), screen position {pos}")

        # Get tile info before rotation
        grid = self._level_manager.get_grid()
        if grid:
            tile = grid.get_tile(row, col)
            if tile:
                old_rotation = tile.rotation
                self._logger.debug(f"Tile at ({row}, {col}): type={tile.tile_type.value}, rotation={old_rotation}°, clickable={tile.is_clickable}")

        # Try to rotate tile
        if self._level_manager.rotate_tile(row, col):
            # Get new rotation
            if grid and tile:
                new_rotation = tile.rotation
                self._logger.info(f"Tile rotated: ({row}, {col}) from {old_rotation}° to {new_rotation}°")

            # Play rotation sound
            self._sound_player.play_sound("sfx/tile_rotate.wav")

            # Emit spark particles
            screen_pos = self._mouse_handler.grid_to_screen(row, col)
            if screen_pos:
                self._particle_system.emit_sparks(screen_pos[0], screen_pos[1], count=10)

            # Check if level is complete (this actually checks connectivity)
            if self._level_manager.check_win_condition():
                self._on_level_complete()
        else:
            self._logger.debug(f"Tile at ({row}, {col}) cannot be rotated (not clickable or invalid)")

    def _on_level_complete(self) -> None:
        """Handle level completion."""
        move_count = self._level_manager.get_move_count()
        self._logger.info("="*60)
        self._logger.info(f"🎉 LEVEL COMPLETE! 🎉")
        self._logger.info(f"Level #{self._current_level_number} ({self._difficulty})")
        self._logger.info(f"Total moves: {move_count}")
        self._logger.info("="*60)

        self._state_machine.transition_to(GameState.VICTORY)

        # Play victory sound
        self._sound_player.play_sound("sfx/victory.wav")

        # Emit victory particles at terminal
        grid = self._level_manager.get_grid()
        if grid:
            terminal_tile = grid.get_terminal()
            if terminal_tile:
                screen_pos = self._mouse_handler.grid_to_screen(terminal_tile.x, terminal_tile.y)
                if screen_pos:
                    # Emit victory particles
                    self._particle_system.emit_victory_effect(screen_pos[0], screen_pos[1])
                    # Emit additional sparks for celebration
                    self._particle_system.emit_sparks(screen_pos[0], screen_pos[1], count=50)

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
        surface = self._renderer._screen
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
        tile_size, tile_padding = self._mouse_handler.get_tile_size()

        for row in range(rows):
            for col in range(cols):
                tile = grid.get_tile(row, col)
                if tile:
                    screen_pos = self._mouse_handler.grid_to_screen(row, col)
                    if screen_pos:
                        surface = self._renderer._screen
                        if surface:
                            # Draw background based on tile type
                            tile_rect = pygame.Rect(screen_pos[0], screen_pos[1], tile_size, tile_size)

                            if tile.tile_type.value == "empty":
                                # Draw light gray background for empty tiles to show grid structure
                                pygame.draw.rect(surface, (60, 60, 60), tile_rect)
                                # Draw subtle border
                                pygame.draw.rect(surface, (80, 80, 80), tile_rect, 1)
                            elif tile.is_clickable:
                                # Draw black background for clickable tiles
                                pygame.draw.rect(surface, (30, 30, 30), tile_rect)
                                # Draw border to make it more visible
                                pygame.draw.rect(surface, (100, 100, 100), tile_rect, 2)

                        # Load and draw tile sprite (skip empty tiles)
                        if tile.tile_type.value != "empty":
                            sprite_path = f"assets/sprites/tiles/tile_{tile.tile_type.value}.png"
                            # Load sprite with dynamic size
                            sprite = self._renderer._sprite_manager.load_sprite(sprite_path, size=(tile_size, tile_size))
                            if sprite:
                                # Rotate sprite if needed
                                if tile.rotation != 0:
                                    sprite = self._renderer._sprite_manager.get_rotated_sprite(sprite, tile.rotation)
                                self._renderer.draw_sprite(sprite, screen_pos)

                            # Draw debug info: current rotation and target rotation
                            if tile.is_clickable:
                                # Get accepted rotations from level data
                                level_data = self._level_manager.get_level_data()
                                accepted_rotations = []
                                if level_data:
                                    for tile_data in level_data.solution_tiles:
                                        if tile_data.get('x') == row and tile_data.get('y') == col:
                                            accepted_rotations = tile_data.get('accepted_rotations', [tile_data.get('rotation', 0)])
                                            break

                                # Format accepted rotations
                                if accepted_rotations:
                                    target_text = "/".join([f"{r}°" for r in accepted_rotations])
                                else:
                                    target_text = "?"

                                # Draw current rotation (yellow)
                                current_text = f"Current: {tile.rotation}°"
                                self._renderer.draw_text(current_text,
                                                        (screen_pos[0] + 5, screen_pos[1] + 5),
                                                        font_size=14,
                                                        color=(255, 255, 0))

                                # Draw target rotation (green)
                                target_display = f"Target: {target_text}"
                                self._renderer.draw_text(target_display,
                                                        (screen_pos[0] + 5, screen_pos[1] + 25),
                                                        font_size=14,
                                                        color=(0, 255, 0))

                        # Draw glow on terminal if connected
                        if tile.tile_type.value == "terminal" and self._level_manager.is_level_completed():
                            surface = self._renderer._screen
                            if surface:
                                self._glow_effect.draw_glow_circle(surface, screen_pos[0], screen_pos[1],
                                                                   radius=32, glow_radius=15)

        # Draw HUD
        move_count = self._level_manager.get_move_count()

        # Display difficulty
        difficulty_display = {
            "easy": "简单",
            "normal": "普通",
            "hard": "困难",
            "hell": "地狱"
        }.get(self._difficulty, self._difficulty)

        self._renderer.draw_text(f"关卡 #{self._current_level_number} ({difficulty_display})", (10, 10))
        self._renderer.draw_text(f"移动次数: {move_count}", (10, 40))

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
