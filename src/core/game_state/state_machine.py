"""
State Machine Module

This module provides the StateMachine class for managing game state transitions.

Classes:
    StateMachine: Manages game state and validates state transitions

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from typing import Dict, Set, Optional, Callable
import logging

from src.core.game_state.game_state import GameState

# Configure logger
logger = logging.getLogger(__name__)


class StateMachine:
    """
    Game state machine.

    Manages game state transitions with validation and logging.
    Ensures only valid state transitions are allowed.

    Attributes:
        _current_state: Current game state
        _previous_state: Previous game state
        _valid_transitions: Dictionary mapping states to valid next states
        _state_callbacks: Dictionary mapping states to callback functions

    Example:
        >>> machine = StateMachine()
        >>> machine.get_current_state()
        <GameState.INIT: 'init'>
        >>> machine.transition_to(GameState.LOADING)
        True
        >>> machine.get_current_state()
        <GameState.LOADING: 'loading'>
    """

    def __init__(self) -> None:
        """
        Initialize state machine.

        Starts in INIT state with no previous state.
        """
        self._current_state: GameState = GameState.INIT
        self._previous_state: Optional[GameState] = None
        self._state_callbacks: Dict[GameState, Callable[[], None]] = {}

        # Define valid state transitions
        self._valid_transitions: Dict[GameState, Set[GameState]] = {
            GameState.INIT: {GameState.LOADING, GameState.EXITING},
            GameState.LOADING: {GameState.PLAYING, GameState.INIT, GameState.EXITING},
            GameState.PLAYING: {GameState.VICTORY, GameState.PAUSED, GameState.LOADING, GameState.EXITING},
            GameState.VICTORY: {GameState.LOADING, GameState.INIT, GameState.EXITING},
            GameState.PAUSED: {GameState.PLAYING, GameState.INIT, GameState.EXITING},
            GameState.EXITING: set()  # Terminal state, no transitions allowed
        }

        logger.info("StateMachine initialized in INIT state")

    def transition_to(self, new_state: GameState) -> bool:
        """
        Transition to a new state.

        Validates the transition before changing state.
        Logs all state changes.

        Args:
            new_state: Target state to transition to

        Returns:
            True if transition successful, False if invalid

        Example:
            >>> machine = StateMachine()
            >>> machine.transition_to(GameState.LOADING)
            True
            >>> machine.transition_to(GameState.VICTORY)  # Invalid from LOADING
            False
        """
        if not isinstance(new_state, GameState):
            logger.error(f"Invalid state type: {type(new_state)}")
            return False

        # Check if transition is valid
        if not self._is_valid_transition(new_state):
            logger.warning(
                f"Invalid state transition: {self._current_state.value} -> {new_state.value}"
            )
            return False

        # Perform transition
        self._previous_state = self._current_state
        self._current_state = new_state

        logger.info(
            f"State transition: {self._previous_state.value} -> {self._current_state.value}"
        )

        # Execute callback if registered
        if new_state in self._state_callbacks:
            try:
                self._state_callbacks[new_state]()
                logger.debug(f"Executed callback for state: {new_state.value}")
            except Exception as e:
                logger.error(f"Error executing callback for state {new_state.value}: {e}")

        return True

    def _is_valid_transition(self, new_state: GameState) -> bool:
        """
        Check if transition to new state is valid.

        Args:
            new_state: Target state

        Returns:
            True if transition is valid, False otherwise
        """
        valid_next_states = self._valid_transitions.get(self._current_state, set())
        return new_state in valid_next_states

    def get_current_state(self) -> GameState:
        """
        Get current game state.

        Returns:
            Current GameState

        Example:
            >>> machine = StateMachine()
            >>> machine.get_current_state()
            <GameState.INIT: 'init'>
        """
        return self._current_state

    def get_previous_state(self) -> Optional[GameState]:
        """
        Get previous game state.

        Returns:
            Previous GameState, or None if no previous state

        Example:
            >>> machine = StateMachine()
            >>> machine.get_previous_state()
            None
            >>> machine.transition_to(GameState.LOADING)
            >>> machine.get_previous_state()
            <GameState.INIT: 'init'>
        """
        return self._previous_state

    def is_in_state(self, state: GameState) -> bool:
        """
        Check if currently in specified state.

        Args:
            state: State to check

        Returns:
            True if in specified state, False otherwise

        Example:
            >>> machine = StateMachine()
            >>> machine.is_in_state(GameState.INIT)
            True
            >>> machine.is_in_state(GameState.PLAYING)
            False
        """
        return self._current_state == state

    def can_transition_to(self, state: GameState) -> bool:
        """
        Check if transition to state is valid.

        Args:
            state: Target state

        Returns:
            True if transition is valid, False otherwise

        Example:
            >>> machine = StateMachine()
            >>> machine.can_transition_to(GameState.LOADING)
            True
            >>> machine.can_transition_to(GameState.VICTORY)
            False
        """
        return self._is_valid_transition(state)

    def register_callback(self, state: GameState, callback: Callable[[], None]) -> None:
        """
        Register a callback function for a state.

        The callback will be executed when transitioning to the state.

        Args:
            state: State to register callback for
            callback: Function to call when entering state

        Example:
            >>> def on_victory():
            ...     print("Level completed!")
            >>> machine = StateMachine()
            >>> machine.register_callback(GameState.VICTORY, on_victory)
        """
        if not isinstance(state, GameState):
            logger.error(f"Invalid state type: {type(state)}")
            return

        if not callable(callback):
            logger.error(f"Callback is not callable: {callback}")
            return

        self._state_callbacks[state] = callback
        logger.debug(f"Registered callback for state: {state.value}")

    def unregister_callback(self, state: GameState) -> None:
        """
        Unregister callback for a state.

        Args:
            state: State to unregister callback for

        Example:
            >>> machine = StateMachine()
            >>> machine.unregister_callback(GameState.VICTORY)
        """
        if state in self._state_callbacks:
            del self._state_callbacks[state]
            logger.debug(f"Unregistered callback for state: {state.value}")

    def reset(self) -> None:
        """
        Reset state machine to initial state.

        Clears previous state and returns to INIT.

        Example:
            >>> machine = StateMachine()
            >>> machine.transition_to(GameState.LOADING)
            >>> machine.reset()
            >>> machine.get_current_state()
            <GameState.INIT: 'init'>
        """
        self._previous_state = self._current_state
        self._current_state = GameState.INIT

        logger.info(f"State machine reset to INIT (from {self._previous_state.value})")

    def get_valid_transitions(self) -> Set[GameState]:
        """
        Get all valid transitions from current state.

        Returns:
            Set of valid next states

        Example:
            >>> machine = StateMachine()
            >>> valid = machine.get_valid_transitions()
            >>> GameState.LOADING in valid
            True
        """
        return self._valid_transitions.get(self._current_state, set()).copy()
