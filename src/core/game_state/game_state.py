"""
Game State Enum

Defines all possible game states.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from enum import Enum


class GameState(Enum):
    """
    Game state enumeration.

    Defines all possible states the game can be in.

    States:
        INIT: Initial state when game starts
        LOADING: Loading level data
        PLAYING: Active gameplay
        VICTORY: Level completed successfully
        PAUSED: Game paused
        EXITING: Game is shutting down

    Example:
        >>> state = GameState.INIT
        >>> print(state.value)
        'init'
    """

    INIT = "init"
    LOADING = "loading"
    PLAYING = "playing"
    VICTORY = "victory"
    PAUSED = "paused"
    EXITING = "exiting"

    def __str__(self) -> str:
        """Return string representation of state"""
        return self.value

    def __repr__(self) -> str:
        """Return detailed representation of state"""
        return f"GameState.{self.name}"
