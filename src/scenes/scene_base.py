"""
Scene Base Class

Provides the abstract base class for all game scenes.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import pygame
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class SceneBase(ABC):
    """
    Abstract base class for all game scenes.

    Defines the lifecycle methods and common functionality for scenes.

    Lifecycle:
        1. __init__() - Scene construction
        2. on_enter(data) - Called when scene becomes active
        3. update(delta_ms) - Called every frame while active
        4. draw(surface) - Called every frame to render
        5. handle_event(event) - Called for each pygame event
        6. on_exit() - Called when scene is being replaced/removed

    Attributes:
        scene_manager: Reference to the scene manager
        is_active (bool): Whether the scene is currently active
        transition_data (Dict): Data passed from previous scene

    Example:
        >>> class MyScene(SceneBase):
        ...     def on_enter(self, data=None):
        ...         print("Scene entered")
        ...     def update(self, delta_ms):
        ...         pass
        ...     def draw(self, surface):
        ...         surface.fill((0, 0, 0))
        ...     def handle_event(self, event):
        ...         return False
    """

    def __init__(self, scene_manager=None):
        """
        Initialize the scene.

        Args:
            scene_manager: Reference to the scene manager
        """
        self.scene_manager = scene_manager
        self.is_active = False
        self.transition_data: Dict[str, Any] = {}
        logger.debug(f"{self.__class__.__name__} created")

    def on_enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when the scene becomes active.

        Use this to initialize scene-specific resources, load data,
        and set up the initial state.

        Args:
            data: Optional data passed from the previous scene
        """
        self.is_active = True
        self.transition_data = data or {}
        logger.info(f"{self.__class__.__name__} entered with data: {data}")

    def on_exit(self) -> None:
        """
        Called when the scene is being replaced or removed.

        Use this to clean up resources, save state, and prepare
        for the next scene.
        """
        self.is_active = False
        logger.info(f"{self.__class__.__name__} exited")

    @abstractmethod
    def update(self, delta_ms: float) -> None:
        """
        Update scene logic.

        Called every frame while the scene is active.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the scene.

        Called every frame to render the scene.

        Args:
            surface: Pygame surface to draw on
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        pass

    def get_transition_data(self, key: str, default: Any = None) -> Any:
        """
        Get data from the transition data dictionary.

        Args:
            key: Data key
            default: Default value if key not found

        Returns:
            The value associated with the key, or default
        """
        return self.transition_data.get(key, default)

    def set_transition_data(self, key: str, value: Any) -> None:
        """
        Set data in the transition data dictionary.

        Args:
            key: Data key
            value: Data value
        """
        self.transition_data[key] = value

    def request_scene_change(
        self,
        scene_class,
        data: Optional[Dict[str, Any]] = None,
        replace: bool = True
    ) -> None:
        """
        Request a scene change through the scene manager.

        Args:
            scene_class: The scene class to switch to
            data: Optional data to pass to the new scene
            replace: If True, replace current scene; if False, push on stack
        """
        if self.scene_manager:
            if replace:
                self.scene_manager.replace_scene(scene_class, data)
            else:
                self.scene_manager.push_scene(scene_class, data)
        else:
            logger.error("Cannot change scene: no scene manager reference")

    def request_scene_pop(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Request to pop the current scene from the stack.

        Args:
            data: Optional data to pass back to the previous scene
        """
        if self.scene_manager:
            self.scene_manager.pop_scene(data)
        else:
            logger.error("Cannot pop scene: no scene manager reference")

    def pause(self) -> None:
        """
        Pause the scene.

        Called when another scene is pushed on top of this one.
        Override to implement pause behavior.
        """
        logger.debug(f"{self.__class__.__name__} paused")

    def resume(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Resume the scene.

        Called when a scene on top of this one is popped.
        Override to implement resume behavior.

        Args:
            data: Optional data passed back from the popped scene
        """
        if data:
            self.transition_data.update(data)
        logger.debug(f"{self.__class__.__name__} resumed with data: {data}")
