"""
Progress Data Structures

Defines data classes for tracking game progress.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


@dataclass
class LevelProgress:
    """
    Progress data for a single level.

    Attributes:
        level_id (int): Unique level identifier
        completed (bool): Whether the level has been completed
        stars (int): Star rating (0-3)
        best_time (float): Best completion time in seconds
        best_moves (int): Fewest moves to complete
        unlocked (bool): Whether the level is unlocked
        attempts (int): Number of times attempted
        last_played (Optional[str]): ISO format timestamp of last play

    Example:
        >>> progress = LevelProgress(level_id=1, unlocked=True)
        >>> progress.complete(stars=3, time=45.5, moves=12)
        >>> progress.is_completed()
        True
    """

    level_id: int
    completed: bool = False
    stars: int = 0
    best_time: float = float('inf')
    best_moves: int = float('inf')
    unlocked: bool = False
    attempts: int = 0
    last_played: Optional[str] = None

    def __post_init__(self):
        """Validate data after initialization."""
        if self.level_id < 1:
            raise ValueError(f"Invalid level_id: {self.level_id}")
        if not 0 <= self.stars <= 3:
            raise ValueError(f"Invalid stars: {self.stars}")
        if self.best_time < 0:
            raise ValueError(f"Invalid best_time: {self.best_time}")
        if self.best_moves < 0:
            raise ValueError(f"Invalid best_moves: {self.best_moves}")

    def complete(self, stars: int, time: float, moves: int) -> bool:
        """
        Mark level as completed and update best scores.

        Args:
            stars: Star rating (0-3)
            time: Completion time in seconds
            moves: Number of moves used

        Returns:
            bool: True if this is a new best score, False otherwise
        """
        if not 0 <= stars <= 3:
            raise ValueError(f"Invalid stars: {stars}")

        self.completed = True
        self.attempts += 1
        self.last_played = datetime.now().isoformat()

        # Check if this is a new best
        is_new_best = False

        # Update best time
        if time < self.best_time:
            self.best_time = time
            is_new_best = True
            logger.info(f"New best time for level {self.level_id}: {time:.2f}s")

        # Update best moves
        if moves < self.best_moves:
            self.best_moves = moves
            is_new_best = True
            logger.info(f"New best moves for level {self.level_id}: {moves}")

        # Update stars (keep the highest)
        if stars > self.stars:
            self.stars = stars
            is_new_best = True
            logger.info(f"New star rating for level {self.level_id}: {stars}")

        return is_new_best

    def unlock(self) -> None:
        """Unlock this level."""
        if not self.unlocked:
            self.unlocked = True
            logger.info(f"Level {self.level_id} unlocked")

    def is_completed(self) -> bool:
        """Check if level is completed."""
        return self.completed

    def is_unlocked(self) -> bool:
        """Check if level is unlocked."""
        return self.unlocked

    def get_stars(self) -> int:
        """Get star rating."""
        return self.stars

    def get_best_time(self) -> float:
        """Get best completion time."""
        return self.best_time if self.best_time != float('inf') else 0.0

    def get_best_moves(self) -> int:
        """Get best move count."""
        return self.best_moves if self.best_moves != float('inf') else 0

    def increment_attempts(self) -> None:
        """Increment attempt counter."""
        self.attempts += 1
        self.last_played = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dict: Dictionary representation
        """
        data = asdict(self)
        # Convert inf to None for JSON serialization
        if data['best_time'] == float('inf'):
            data['best_time'] = None
        if data['best_moves'] == float('inf'):
            data['best_moves'] = None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LevelProgress':
        """
        Create from dictionary.

        Args:
            data: Dictionary with level progress data

        Returns:
            LevelProgress: New instance
        """
        # Convert None back to inf
        if data.get('best_time') is None:
            data['best_time'] = float('inf')
        if data.get('best_moves') is None:
            data['best_moves'] = float('inf')

        return cls(**data)

    def __repr__(self) -> str:
        """String representation."""
        status = "✓" if self.completed else "✗"
        stars_str = "★" * self.stars + "☆" * (3 - self.stars)
        return f"Level {self.level_id} {status} {stars_str} (Time: {self.get_best_time():.1f}s, Moves: {self.get_best_moves()})"


@dataclass
class GameProgress:
    """
    Overall game progress data.

    Attributes:
        levels (Dict[int, LevelProgress]): Progress for each level
        current_level (int): Current level player is on
        total_stars (int): Total stars earned
        total_playtime (float): Total playtime in seconds
        last_played (Optional[str]): ISO format timestamp of last play
        version (str): Save data version
        created_at (str): ISO format timestamp of creation

    Example:
        >>> progress = GameProgress()
        >>> progress.unlock_level(1)
        >>> progress.complete_level(1, stars=3, time=45.5, moves=12)
        >>> progress.get_total_stars()
        3
    """

    levels: Dict[int, LevelProgress] = field(default_factory=dict)
    current_level: int = 1
    total_stars: int = 0
    total_playtime: float = 0.0
    last_played: Optional[str] = None
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        """Initialize with level 1 unlocked if no levels exist."""
        if not self.levels:
            self.unlock_level(1)

    def get_level_progress(self, level_id: int) -> Optional[LevelProgress]:
        """
        Get progress for a specific level.

        Args:
            level_id: Level identifier

        Returns:
            Optional[LevelProgress]: Level progress or None if not found
        """
        return self.levels.get(level_id)

    def unlock_level(self, level_id: int) -> None:
        """
        Unlock a level.

        Args:
            level_id: Level identifier
        """
        if level_id not in self.levels:
            self.levels[level_id] = LevelProgress(level_id=level_id, unlocked=True)
        else:
            self.levels[level_id].unlock()

        logger.info(f"Level {level_id} unlocked")

    def complete_level(self, level_id: int, stars: int, time: float, moves: int) -> bool:
        """
        Mark a level as completed.

        Args:
            level_id: Level identifier
            stars: Star rating (0-3)
            time: Completion time in seconds
            moves: Number of moves used

        Returns:
            bool: True if this is a new best score
        """
        if level_id not in self.levels:
            self.levels[level_id] = LevelProgress(level_id=level_id, unlocked=True)

        # Complete the level
        is_new_best = self.levels[level_id].complete(stars, time, moves)

        # Update total stars
        self._recalculate_total_stars()

        # Update last played
        self.last_played = datetime.now().isoformat()

        # Unlock next level
        next_level = level_id + 1
        if next_level not in self.levels or not self.levels[next_level].is_unlocked():
            self.unlock_level(next_level)

        # Update current level if needed
        if level_id >= self.current_level:
            self.current_level = next_level

        logger.info(f"Level {level_id} completed: {stars} stars, {time:.2f}s, {moves} moves")

        return is_new_best

    def is_level_unlocked(self, level_id: int) -> bool:
        """
        Check if a level is unlocked.

        Args:
            level_id: Level identifier

        Returns:
            bool: True if unlocked, False otherwise
        """
        if level_id not in self.levels:
            return False
        return self.levels[level_id].is_unlocked()

    def is_level_completed(self, level_id: int) -> bool:
        """
        Check if a level is completed.

        Args:
            level_id: Level identifier

        Returns:
            bool: True if completed, False otherwise
        """
        if level_id not in self.levels:
            return False
        return self.levels[level_id].is_completed()

    def get_total_stars(self) -> int:
        """
        Get total stars earned.

        Returns:
            int: Total stars
        """
        return self.total_stars

    def get_completed_levels_count(self) -> int:
        """
        Get number of completed levels.

        Returns:
            int: Number of completed levels
        """
        return sum(1 for level in self.levels.values() if level.is_completed())

    def get_unlocked_levels_count(self) -> int:
        """
        Get number of unlocked levels.

        Returns:
            int: Number of unlocked levels
        """
        return sum(1 for level in self.levels.values() if level.is_unlocked())

    def get_current_level(self) -> int:
        """
        Get current level.

        Returns:
            int: Current level number
        """
        return self.current_level

    def add_playtime(self, seconds: float) -> None:
        """
        Add playtime.

        Args:
            seconds: Playtime to add in seconds
        """
        self.total_playtime += seconds

    def _recalculate_total_stars(self) -> None:
        """Recalculate total stars from all levels."""
        self.total_stars = sum(level.get_stars() for level in self.levels.values())

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dict: Dictionary representation
        """
        return {
            'levels': {str(level_id): level.to_dict() for level_id, level in self.levels.items()},
            'current_level': self.current_level,
            'total_stars': self.total_stars,
            'total_playtime': self.total_playtime,
            'last_played': self.last_played,
            'version': self.version,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameProgress':
        """
        Create from dictionary.

        Args:
            data: Dictionary with game progress data

        Returns:
            GameProgress: New instance
        """
        # Convert level dict back to LevelProgress objects
        levels = {}
        for level_id_str, level_data in data.get('levels', {}).items():
            level_id = int(level_id_str)
            levels[level_id] = LevelProgress.from_dict(level_data)

        return cls(
            levels=levels,
            current_level=data.get('current_level', 1),
            total_stars=data.get('total_stars', 0),
            total_playtime=data.get('total_playtime', 0.0),
            last_played=data.get('last_played'),
            version=data.get('version', '1.0.0'),
            created_at=data.get('created_at', datetime.now().isoformat())
        )

    def to_json(self) -> str:
        """
        Convert to JSON string.

        Returns:
            str: JSON representation
        """
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'GameProgress':
        """
        Create from JSON string.

        Args:
            json_str: JSON string

        Returns:
            GameProgress: New instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        """String representation."""
        completed = self.get_completed_levels_count()
        unlocked = self.get_unlocked_levels_count()
        return f"GameProgress(Levels: {completed}/{unlocked}, Stars: {self.total_stars}, Current: {self.current_level})"
