"""
Level Progression Manager

Manages level unlocking, progression, and completion tracking.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

from typing import Optional, List, Dict, Any
from src.progression.progress_data import GameProgress, LevelProgress
from src.progression.save_manager import SaveManager
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class LevelProgressionManager:
    """
    Manages level progression and unlocking.

    Handles:
        - Level unlocking based on completion
        - Progress tracking
        - Best score management
        - Save/load integration

    Example:
        >>> manager = LevelProgressionManager()
        >>> manager.complete_level(1, stars=3, time=45.5, moves=12)
        >>> manager.is_level_unlocked(2)
        True
    """

    def __init__(self, save_manager: Optional[SaveManager] = None):
        """
        Initialize the progression manager.

        Args:
            save_manager: SaveManager instance (creates new if None)
        """
        self._save_manager = save_manager or SaveManager()
        self._progress: GameProgress = self._save_manager.load_save()

        logger.info(f"LevelProgressionManager initialized: {self._progress}")

    def get_progress(self) -> GameProgress:
        """
        Get current game progress.

        Returns:
            GameProgress: Current progress
        """
        return self._progress

    def complete_level(
        self,
        level_id: int,
        stars: int,
        time: float,
        moves: int,
        auto_save: bool = True
    ) -> Dict[str, Any]:
        """
        Complete a level and update progress.

        Args:
            level_id: Level identifier
            stars: Star rating (0-3)
            time: Completion time in seconds
            moves: Number of moves used
            auto_save: Whether to auto-save progress

        Returns:
            Dict: Completion result with keys:
                - is_new_best (bool): Whether this is a new best score
                - unlocked_levels (List[int]): Newly unlocked level IDs
                - total_stars (int): Total stars earned
                - next_level (int): Next level to play
        """
        # Complete the level
        is_new_best = self._progress.complete_level(level_id, stars, time, moves)

        # Get newly unlocked levels
        unlocked_levels = [level_id + 1] if self._progress.is_level_unlocked(level_id + 1) else []

        # Prepare result
        result = {
            'is_new_best': is_new_best,
            'unlocked_levels': unlocked_levels,
            'total_stars': self._progress.get_total_stars(),
            'next_level': self._progress.get_current_level(),
            'completed_count': self._progress.get_completed_levels_count()
        }

        # Auto-save if requested
        if auto_save:
            self.save_progress()

        logger.info(f"Level {level_id} completed: {result}")

        return result

    def is_level_unlocked(self, level_id: int) -> bool:
        """
        Check if a level is unlocked.

        Args:
            level_id: Level identifier

        Returns:
            bool: True if unlocked, False otherwise
        """
        return self._progress.is_level_unlocked(level_id)

    def is_level_completed(self, level_id: int) -> bool:
        """
        Check if a level is completed.

        Args:
            level_id: Level identifier

        Returns:
            bool: True if completed, False otherwise
        """
        return self._progress.is_level_completed(level_id)

    def get_level_progress(self, level_id: int) -> Optional[LevelProgress]:
        """
        Get progress for a specific level.

        Args:
            level_id: Level identifier

        Returns:
            Optional[LevelProgress]: Level progress or None
        """
        return self._progress.get_level_progress(level_id)

    def get_level_stars(self, level_id: int) -> int:
        """
        Get star rating for a level.

        Args:
            level_id: Level identifier

        Returns:
            int: Star rating (0-3)
        """
        level_progress = self._progress.get_level_progress(level_id)
        return level_progress.get_stars() if level_progress else 0

    def get_level_best_time(self, level_id: int) -> float:
        """
        Get best time for a level.

        Args:
            level_id: Level identifier

        Returns:
            float: Best time in seconds (0.0 if not completed)
        """
        level_progress = self._progress.get_level_progress(level_id)
        return level_progress.get_best_time() if level_progress else 0.0

    def get_level_best_moves(self, level_id: int) -> int:
        """
        Get best move count for a level.

        Args:
            level_id: Level identifier

        Returns:
            int: Best move count (0 if not completed)
        """
        level_progress = self._progress.get_level_progress(level_id)
        return level_progress.get_best_moves() if level_progress else 0

    def get_unlocked_levels(self) -> List[int]:
        """
        Get list of unlocked level IDs.

        Returns:
            List[int]: List of unlocked level IDs
        """
        return [
            level_id
            for level_id, level_progress in self._progress.levels.items()
            if level_progress.is_unlocked()
        ]

    def get_completed_levels(self) -> List[int]:
        """
        Get list of completed level IDs.

        Returns:
            List[int]: List of completed level IDs
        """
        return [
            level_id
            for level_id, level_progress in self._progress.levels.items()
            if level_progress.is_completed()
        ]

    def get_total_stars(self) -> int:
        """
        Get total stars earned.

        Returns:
            int: Total stars
        """
        return self._progress.get_total_stars()

    def get_current_level(self) -> int:
        """
        Get current level (next level to play).

        Returns:
            int: Current level number
        """
        return self._progress.get_current_level()

    def get_completion_percentage(self) -> float:
        """
        Get overall completion percentage.

        Returns:
            float: Completion percentage (0.0-100.0)
        """
        completed = self._progress.get_completed_levels_count()
        unlocked = self._progress.get_unlocked_levels_count()

        if unlocked == 0:
            return 0.0

        return (completed / unlocked) * 100.0

    def unlock_level(self, level_id: int, auto_save: bool = True) -> bool:
        """
        Manually unlock a level.

        Args:
            level_id: Level identifier
            auto_save: Whether to auto-save progress

        Returns:
            bool: True if level was unlocked, False if already unlocked
        """
        was_unlocked = self._progress.is_level_unlocked(level_id)

        if not was_unlocked:
            self._progress.unlock_level(level_id)

            if auto_save:
                self.save_progress()

            logger.info(f"Level {level_id} manually unlocked")
            return True

        return False

    def reset_level(self, level_id: int, auto_save: bool = True) -> bool:
        """
        Reset a level's progress.

        Args:
            level_id: Level identifier
            auto_save: Whether to auto-save progress

        Returns:
            bool: True if reset successful, False otherwise
        """
        if level_id in self._progress.levels:
            # Create new progress for this level
            self._progress.levels[level_id] = LevelProgress(
                level_id=level_id,
                unlocked=True
            )

            # Recalculate total stars
            self._progress._recalculate_total_stars()

            if auto_save:
                self.save_progress()

            logger.info(f"Level {level_id} reset")
            return True

        return False

    def reset_all_progress(self, auto_save: bool = True) -> None:
        """
        Reset all progress (start new game).

        Args:
            auto_save: Whether to auto-save progress
        """
        self._progress = GameProgress()

        if auto_save:
            self.save_progress()

        logger.info("All progress reset")

    def save_progress(self) -> bool:
        """
        Save current progress to disk.

        Returns:
            bool: True if save successful, False otherwise
        """
        result = self._save_manager.save_progress(self._progress)

        if result:
            logger.info("Progress saved successfully")
        else:
            logger.error("Failed to save progress")

        return result

    def reload_progress(self) -> None:
        """Reload progress from disk."""
        self._progress = self._save_manager.load_save()
        logger.info("Progress reloaded from disk")

    def add_playtime(self, seconds: float, auto_save: bool = False) -> None:
        """
        Add playtime to total.

        Args:
            seconds: Playtime to add in seconds
            auto_save: Whether to auto-save progress
        """
        self._progress.add_playtime(seconds)

        if auto_save:
            self.save_progress()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall game statistics.

        Returns:
            Dict: Statistics including:
                - total_levels: Total number of levels
                - completed_levels: Number of completed levels
                - unlocked_levels: Number of unlocked levels
                - total_stars: Total stars earned
                - max_stars: Maximum possible stars
                - completion_percentage: Completion percentage
                - total_playtime: Total playtime in seconds
                - current_level: Current level number
        """
        unlocked_count = self._progress.get_unlocked_levels_count()
        completed_count = self._progress.get_completed_levels_count()

        return {
            'total_levels': unlocked_count,
            'completed_levels': completed_count,
            'unlocked_levels': unlocked_count,
            'total_stars': self._progress.get_total_stars(),
            'max_stars': unlocked_count * 3,
            'completion_percentage': self.get_completion_percentage(),
            'total_playtime': self._progress.total_playtime,
            'current_level': self._progress.get_current_level()
        }

    def __repr__(self) -> str:
        """String representation."""
        stats = self.get_statistics()
        return (
            f"LevelProgressionManager("
            f"Levels: {stats['completed_levels']}/{stats['total_levels']}, "
            f"Stars: {stats['total_stars']}/{stats['max_stars']}, "
            f"Current: {stats['current_level']})"
        )
