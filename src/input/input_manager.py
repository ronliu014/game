"""
Input Manager Module

This module provides the InputManager class for handling user input including
mouse and keyboard events.

Classes:
    InputManager: Central manager for input handling

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import logging
from typing import Tuple, Optional, Set
import pygame

# Configure logger
logger = logging.getLogger(__name__)


class InputManager:
    """
    Central manager for handling user input.

    Tracks mouse position, button states, and keyboard states.

    Attributes:
        _mouse_pos: Current mouse position (x, y)
        _mouse_buttons: Set of currently pressed mouse buttons
        _keys_pressed: Set of currently pressed keys
        _mouse_motion: Mouse motion delta (dx, dy)

    Example:
        >>> input_mgr = InputManager()
        >>> input_mgr.update(events)
        >>> if input_mgr.is_mouse_button_pressed(1):
        ...     x, y = input_mgr.get_mouse_position()
        ...     print(f"Left click at ({x}, {y})")
    """

    def __init__(self) -> None:
        """Initialize the InputManager."""
        self._mouse_pos: Tuple[int, int] = (0, 0)
        self._mouse_buttons: Set[int] = set()
        self._keys_pressed: Set[int] = set()
        self._mouse_motion: Tuple[int, int] = (0, 0)

        logger.info("InputManager initialized")

    def update(self, events: list) -> None:
        """
        Update input state from pygame events.

        Args:
            events: List of pygame events

        Example:
            >>> events = pygame.event.get()
            >>> input_mgr.update(events)
        """
        # Reset motion
        self._mouse_motion = (0, 0)

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self._mouse_pos = event.pos
                self._mouse_motion = event.rel

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons.add(event.button)
                self._mouse_pos = event.pos
                logger.debug(f"Mouse button {event.button} pressed at {event.pos}")

            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons.discard(event.button)
                self._mouse_pos = event.pos
                logger.debug(f"Mouse button {event.button} released at {event.pos}")

            elif event.type == pygame.KEYDOWN:
                self._keys_pressed.add(event.key)
                logger.debug(f"Key {pygame.key.name(event.key)} pressed")

            elif event.type == pygame.KEYUP:
                self._keys_pressed.discard(event.key)
                logger.debug(f"Key {pygame.key.name(event.key)} released")

    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get the current mouse position.

        Returns:
            (x, y) tuple of mouse position

        Example:
            >>> x, y = input_mgr.get_mouse_position()
        """
        return self._mouse_pos

    def get_mouse_motion(self) -> Tuple[int, int]:
        """
        Get the mouse motion delta since last update.

        Returns:
            (dx, dy) tuple of mouse motion

        Example:
            >>> dx, dy = input_mgr.get_mouse_motion()
        """
        return self._mouse_motion

    def is_mouse_button_pressed(self, button: int) -> bool:
        """
        Check if a mouse button is currently pressed.

        Args:
            button: Mouse button number (1=left, 2=middle, 3=right)

        Returns:
            True if button is pressed, False otherwise

        Example:
            >>> if input_mgr.is_mouse_button_pressed(1):
            ...     print("Left mouse button is pressed")
        """
        return button in self._mouse_buttons

    def is_key_pressed(self, key: int) -> bool:
        """
        Check if a keyboard key is currently pressed.

        Args:
            key: Pygame key constant (e.g., pygame.K_SPACE)

        Returns:
            True if key is pressed, False otherwise

        Example:
            >>> if input_mgr.is_key_pressed(pygame.K_SPACE):
            ...     print("Space key is pressed")
        """
        return key in self._keys_pressed

    def get_pressed_keys(self) -> Set[int]:
        """
        Get all currently pressed keys.

        Returns:
            Set of pressed key codes

        Example:
            >>> keys = input_mgr.get_pressed_keys()
            >>> print(f"{len(keys)} keys pressed")
        """
        return self._keys_pressed.copy()

    def get_pressed_mouse_buttons(self) -> Set[int]:
        """
        Get all currently pressed mouse buttons.

        Returns:
            Set of pressed mouse button numbers

        Example:
            >>> buttons = input_mgr.get_pressed_mouse_buttons()
        """
        return self._mouse_buttons.copy()

    def clear(self) -> None:
        """
        Clear all input state.

        Example:
            >>> input_mgr.clear()
        """
        self._mouse_buttons.clear()
        self._keys_pressed.clear()
        self._mouse_motion = (0, 0)
        logger.debug("Input state cleared")
