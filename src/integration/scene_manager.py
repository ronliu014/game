"""
Scene Manager

Manages game scenes and scene transitions.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from typing import Optional, Dict, Any
from enum import Enum
from src.utils.logger import GameLogger


class SceneType(Enum):
    """
    Scene types.

    Attributes:
        MENU: Main menu scene
        GAME: Game playing scene
        VICTORY: Victory scene
        PAUSE: Pause scene
    """
    MENU = "menu"
    GAME = "game"
    VICTORY = "victory"
    PAUSE = "pause"


class Scene:
    """
    Base class for all game scenes.

    Attributes:
        scene_type (SceneType): Type of this scene
        _active (bool): Whether scene is active
        _logger (GameLogger): Logger instance
    """

    def __init__(self, scene_type: SceneType):
        """
        Initialize the scene.

        Args:
            scene_type: Type of this scene
        """
        self.scene_type: SceneType = scene_type
        self._active: bool = False
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def enter(self, **kwargs: Any) -> None:
        """
        Called when entering this scene.

        Args:
            **kwargs: Scene-specific parameters
        """
        self._active = True
        self._logger.info(f"Entering scene: {self.scene_type.value}")

    def exit(self) -> None:
        """Called when exiting this scene."""
        self._active = False
        self._logger.info(f"Exiting scene: {self.scene_type.value}")

    def update(self, delta_ms: float) -> None:
        """
        Update scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    def draw(self, renderer) -> None:
        """
        Draw the scene.

        Args:
            renderer: Renderer instance
        """
        pass

    def handle_event(self, event) -> None:
        """
        Handle pygame event.

        Args:
            event: Pygame event
        """
        pass

    def is_active(self) -> bool:
        """
        Check if scene is active.

        Returns:
            bool: True if active, False otherwise
        """
        return self._active


class SceneManager:
    """
    Scene manager for handling scene transitions.

    Manages scene stack and transitions between scenes.

    Attributes:
        _scenes (Dict[SceneType, Scene]): Registered scenes
        _scene_stack (list[Scene]): Scene stack
        _logger (GameLogger): Logger instance
    """

    def __init__(self):
        """Initialize the scene manager."""
        self._scenes: Dict[SceneType, Scene] = {}
        self._scene_stack: list[Scene] = []
        self._logger: GameLogger = GameLogger.get_logger(__name__)

    def register_scene(self, scene_type: SceneType, scene: Scene) -> None:
        """
        Register a scene.

        Args:
            scene_type: Type of scene
            scene: Scene instance
        """
        self._scenes[scene_type] = scene
        self._logger.debug(f"Registered scene: {scene_type.value}")

    def push_scene(self, scene_type: SceneType, **kwargs: Any) -> bool:
        """
        Push a scene onto the stack.

        Args:
            scene_type: Type of scene to push
            **kwargs: Scene-specific parameters

        Returns:
            bool: True if successful, False otherwise
        """
        if scene_type not in self._scenes:
            self._logger.error(f"Scene not registered: {scene_type.value}")
            return False

        # Pause current scene if exists
        if self._scene_stack:
            current_scene = self._scene_stack[-1]
            current_scene.exit()

        # Push new scene
        scene = self._scenes[scene_type]
        self._scene_stack.append(scene)
        scene.enter(**kwargs)

        self._logger.info(f"Pushed scene: {scene_type.value}")
        return True

    def pop_scene(self) -> Optional[Scene]:
        """
        Pop the current scene from the stack.

        Returns:
            Optional[Scene]: Popped scene, or None if stack is empty
        """
        if not self._scene_stack:
            self._logger.warning("Cannot pop scene: stack is empty")
            return None

        # Exit current scene
        scene = self._scene_stack.pop()
        scene.exit()

        # Resume previous scene if exists
        if self._scene_stack:
            previous_scene = self._scene_stack[-1]
            previous_scene.enter()

        self._logger.info(f"Popped scene: {scene.scene_type.value}")
        return scene

    def change_scene(self, scene_type: SceneType, **kwargs: Any) -> bool:
        """
        Change to a different scene (replace current scene).

        Args:
            scene_type: Type of scene to change to
            **kwargs: Scene-specific parameters

        Returns:
            bool: True if successful, False otherwise
        """
        if scene_type not in self._scenes:
            self._logger.error(f"Scene not registered: {scene_type.value}")
            return False

        # Exit current scene if exists
        if self._scene_stack:
            current_scene = self._scene_stack.pop()
            current_scene.exit()

        # Push new scene
        scene = self._scenes[scene_type]
        self._scene_stack.append(scene)
        scene.enter(**kwargs)

        self._logger.info(f"Changed to scene: {scene_type.value}")
        return True

    def get_current_scene(self) -> Optional[Scene]:
        """
        Get the current active scene.

        Returns:
            Optional[Scene]: Current scene, or None if stack is empty
        """
        if not self._scene_stack:
            return None
        return self._scene_stack[-1]

    def clear_scenes(self) -> None:
        """Clear all scenes from the stack."""
        while self._scene_stack:
            scene = self._scene_stack.pop()
            scene.exit()

        self._logger.info("All scenes cleared")

    def get_scene_count(self) -> int:
        """
        Get the number of scenes in the stack.

        Returns:
            int: Number of scenes
        """
        return len(self._scene_stack)

    def update(self, delta_ms: float) -> None:
        """
        Update the current scene.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        current_scene = self.get_current_scene()
        if current_scene:
            current_scene.update(delta_ms)

    def draw(self, renderer) -> None:
        """
        Draw the current scene.

        Args:
            renderer: Renderer instance
        """
        current_scene = self.get_current_scene()
        if current_scene:
            current_scene.draw(renderer)

    def handle_event(self, event) -> None:
        """
        Handle pygame event for current scene.

        Args:
            event: Pygame event
        """
        current_scene = self.get_current_scene()
        if current_scene:
            current_scene.handle_event(event)
