"""
Scene Manager

Manages scene transitions and the scene stack.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import List, Optional, Dict, Any, Type
import pygame
from src.scenes.scene_base import SceneBase
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class SceneManager:
    """
    Scene manager for handling scene transitions and the scene stack.

    Supports push/pop/replace operations with optional transition animations.

    Attributes:
        scene_stack (List[SceneBase]): Stack of active scenes
        transition_active (bool): Whether a transition is in progress
        transition_progress (float): Transition progress (0.0 to 1.0)

    Example:
        >>> manager = SceneManager()
        >>> manager.push_scene(MainMenuScene)
        >>> manager.update(16.67)  # ~60 FPS
        >>> manager.draw(screen)
    """

    def __init__(self):
        """Initialize the scene manager."""
        self._scene_stack: List[SceneBase] = []
        self._transition_active = False
        self._transition_progress = 0.0
        self._transition_duration = 500.0  # milliseconds
        self._transition_type = 'fade'
        self._transition_surface: Optional[pygame.Surface] = None
        self._pending_scene_change: Optional[tuple] = None
        logger.info("SceneManager initialized")

    def push_scene(
        self,
        scene_class: Type[SceneBase],
        data: Optional[Dict[str, Any]] = None,
        transition: bool = True
    ) -> None:
        """
        Push a new scene onto the stack.

        The current scene (if any) is paused, and the new scene becomes active.

        Args:
            scene_class: The scene class to instantiate and push
            data: Optional data to pass to the new scene
            transition: Whether to use transition animation
        """
        # Pause current scene if exists
        if self._scene_stack:
            current_scene = self._scene_stack[-1]
            current_scene.pause()
            logger.debug(f"Paused scene: {current_scene.__class__.__name__}")

        # Create and enter new scene
        new_scene = scene_class(scene_manager=self)
        new_scene.on_enter(data)
        self._scene_stack.append(new_scene)

        logger.info(f"Pushed scene: {scene_class.__name__} (stack size: {len(self._scene_stack)})")

        # Start transition if requested
        if transition:
            self._start_transition()

    def pop_scene(
        self,
        data: Optional[Dict[str, Any]] = None,
        transition: bool = True
    ) -> None:
        """
        Pop the current scene from the stack.

        The previous scene (if any) is resumed.

        Args:
            data: Optional data to pass back to the previous scene
            transition: Whether to use transition animation
        """
        if not self._scene_stack:
            logger.warning("Cannot pop scene: stack is empty")
            return

        # Exit current scene
        current_scene = self._scene_stack.pop()
        current_scene.on_exit()
        logger.info(f"Popped scene: {current_scene.__class__.__name__} (stack size: {len(self._scene_stack)})")

        # Resume previous scene if exists
        if self._scene_stack:
            previous_scene = self._scene_stack[-1]
            previous_scene.resume(data)
            logger.debug(f"Resumed scene: {previous_scene.__class__.__name__}")

        # Start transition if requested
        if transition:
            self._start_transition()

    def replace_scene(
        self,
        scene_class: Type[SceneBase],
        data: Optional[Dict[str, Any]] = None,
        transition: bool = True
    ) -> None:
        """
        Replace the current scene with a new scene.

        The current scene is exited and removed from the stack.

        Args:
            scene_class: The scene class to instantiate and replace with
            data: Optional data to pass to the new scene
            transition: Whether to use transition animation
        """
        # Exit current scene if exists
        if self._scene_stack:
            current_scene = self._scene_stack.pop()
            current_scene.on_exit()
            logger.debug(f"Removed scene: {current_scene.__class__.__name__}")

        # Create and enter new scene
        new_scene = scene_class(scene_manager=self)
        new_scene.on_enter(data)
        self._scene_stack.append(new_scene)

        logger.info(f"Replaced with scene: {scene_class.__name__} (stack size: {len(self._scene_stack)})")

        # Start transition if requested
        if transition:
            self._start_transition()

    def clear_stack(self) -> None:
        """
        Clear all scenes from the stack.

        All scenes are properly exited.
        """
        while self._scene_stack:
            scene = self._scene_stack.pop()
            scene.on_exit()
            logger.debug(f"Cleared scene: {scene.__class__.__name__}")

        logger.info("Scene stack cleared")

    def update(self, delta_ms: float) -> None:
        """
        Update the current scene and handle transitions.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        # Update transition
        if self._transition_active:
            self._update_transition(delta_ms)

        # Update current scene
        if self._scene_stack:
            current_scene = self._scene_stack[-1]
            current_scene.update(delta_ms)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the current scene with transition effects.

        Args:
            surface: Pygame surface to draw on
        """
        if not self._scene_stack:
            return

        # Draw current scene
        current_scene = self._scene_stack[-1]
        current_scene.draw(surface)

        # Draw transition overlay
        if self._transition_active and self._transition_surface:
            self._draw_transition(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Events are passed to the current scene.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        if self._scene_stack:
            current_scene = self._scene_stack[-1]
            return current_scene.handle_event(event)
        return False

    def get_current_scene(self) -> Optional[SceneBase]:
        """
        Get the current active scene.

        Returns:
            SceneBase: The current scene, or None if stack is empty
        """
        return self._scene_stack[-1] if self._scene_stack else None

    def get_stack_size(self) -> int:
        """
        Get the number of scenes in the stack.

        Returns:
            int: Number of scenes
        """
        return len(self._scene_stack)

    def is_empty(self) -> bool:
        """
        Check if the scene stack is empty.

        Returns:
            bool: True if empty, False otherwise
        """
        return len(self._scene_stack) == 0

    def set_transition_duration(self, duration_ms: float) -> None:
        """
        Set the transition duration.

        Args:
            duration_ms: Duration in milliseconds
        """
        self._transition_duration = max(0, duration_ms)
        logger.debug(f"Transition duration set to {duration_ms}ms")

    def set_transition_type(self, transition_type: str) -> None:
        """
        Set the transition type.

        Args:
            transition_type: Transition type ('fade', 'none')
        """
        self._transition_type = transition_type
        logger.debug(f"Transition type set to {transition_type}")

    def _start_transition(self) -> None:
        """Start a scene transition."""
        if self._transition_type == 'none' or self._transition_duration <= 0:
            return

        self._transition_active = True
        self._transition_progress = 0.0
        logger.debug("Transition started")

    def _update_transition(self, delta_ms: float) -> None:
        """
        Update transition progress.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        if not self._transition_active:
            return

        # Update progress
        self._transition_progress += delta_ms / self._transition_duration
        self._transition_progress = min(1.0, self._transition_progress)

        # End transition when complete
        if self._transition_progress >= 1.0:
            self._transition_active = False
            self._transition_progress = 0.0
            logger.debug("Transition completed")

    def _draw_transition(self, surface: pygame.Surface) -> None:
        """
        Draw transition effect.

        Args:
            surface: Pygame surface to draw on
        """
        if self._transition_type == 'fade':
            # Create fade overlay if needed
            if not self._transition_surface:
                self._transition_surface = pygame.Surface(surface.get_size())
                self._transition_surface.fill((0, 0, 0))

            # Calculate alpha based on progress (fade in from black)
            # Progress 0.0 -> alpha 255 (fully black)
            # Progress 1.0 -> alpha 0 (fully transparent)
            alpha = int(255 * (1.0 - self._transition_progress))
            self._transition_surface.set_alpha(alpha)

            # Draw overlay
            surface.blit(self._transition_surface, (0, 0))

    def __repr__(self) -> str:
        """String representation of the scene manager."""
        scene_names = [scene.__class__.__name__ for scene in self._scene_stack]
        return f"SceneManager(stack={scene_names})"
