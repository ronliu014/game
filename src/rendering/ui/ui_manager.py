"""
UI Manager Module

This module provides the UIManager class for managing all UI components
in the game.

Classes:
    UIManager: Central manager for all UI components

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import List, Optional
import pygame

from src.rendering.ui.ui_component import UIComponent

# Configure logger
logger = logging.getLogger(__name__)


class UIManager:
    """
    Central manager for all UI components.

    Manages drawing and event handling for all registered UI components.

    Attributes:
        _components: List of registered UI components

    Example:
        >>> ui_manager = UIManager()
        >>> button = Button(100, 100, 200, 50, "Click Me")
        >>> ui_manager.add_component(button)
        >>> ui_manager.draw(screen)
        >>> ui_manager.handle_event(event)
    """

    def __init__(self) -> None:
        """Initialize the UI manager."""
        self._components: List[UIComponent] = []
        logger.info("UIManager initialized")

    def add_component(self, component: UIComponent) -> None:
        """
        Add a UI component to the manager.

        Args:
            component: UI component to add

        Example:
            >>> button = Button(100, 100, 200, 50, "Click")
            >>> ui_manager.add_component(button)
        """
        self._components.append(component)
        logger.debug(f"Component added: {type(component).__name__}")

    def remove_component(self, component: UIComponent) -> bool:
        """
        Remove a UI component from the manager.

        Args:
            component: UI component to remove

        Returns:
            True if component was removed, False if not found

        Example:
            >>> ui_manager.remove_component(button)
            True
        """
        if component in self._components:
            self._components.remove(component)
            logger.debug(f"Component removed: {type(component).__name__}")
            return True
        return False

    def clear_components(self) -> None:
        """
        Remove all UI components.

        Example:
            >>> ui_manager.clear_components()
        """
        count = len(self._components)
        self._components.clear()
        logger.info(f"All components cleared: {count} components removed")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw all visible UI components.

        Args:
            surface: Pygame surface to draw on

        Example:
            >>> ui_manager.draw(screen)
        """
        for component in self._components:
            if component.is_visible():
                component.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle a pygame event and pass it to components.

        Args:
            event: Pygame event to handle

        Returns:
            True if any component handled the event, False otherwise

        Example:
            >>> for event in pygame.event.get():
            ...     if ui_manager.handle_event(event):
            ...         continue  # Event was handled
        """
        # Pass event to components in reverse order (top to bottom)
        for component in reversed(self._components):
            if component.is_enabled() and component.handle_event(event):
                return True
        return False

    def get_components(self) -> List[UIComponent]:
        """
        Get all registered UI components.

        Returns:
            List of UI components

        Example:
            >>> components = ui_manager.get_components()
            >>> print(f"Manager has {len(components)} components")
        """
        return self._components.copy()

    def get_component_count(self) -> int:
        """
        Get the number of registered components.

        Returns:
            Number of components

        Example:
            >>> count = ui_manager.get_component_count()
        """
        return len(self._components)

    def show_all(self) -> None:
        """
        Show all UI components.

        Example:
            >>> ui_manager.show_all()
        """
        for component in self._components:
            component.show()
        logger.debug("All components shown")

    def hide_all(self) -> None:
        """
        Hide all UI components.

        Example:
            >>> ui_manager.hide_all()
        """
        for component in self._components:
            component.hide()
        logger.debug("All components hidden")

    def enable_all(self) -> None:
        """
        Enable all UI components.

        Example:
            >>> ui_manager.enable_all()
        """
        for component in self._components:
            component.enable()
        logger.debug("All components enabled")

    def disable_all(self) -> None:
        """
        Disable all UI components.

        Example:
            >>> ui_manager.disable_all()
        """
        for component in self._components:
            component.disable()
        logger.debug("All components disabled")
