"""
Difficulty Configuration Module

Defines difficulty levels and their parameters for level generation.

Classes:
    DifficultyLevel: Enum for difficulty levels
    DifficultyConfig: Configuration for each difficulty level

Author: Circuit Repair Game Team
Date: 2026-01-22
"""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple


class DifficultyLevel(Enum):
    """
    Difficulty levels for the game.

    Attributes:
        EASY: Simple puzzles with fewer movable elements
        NORMAL: Medium complexity puzzles
        HARD: Challenging puzzles with more elements
        HELL: Extremely difficult puzzles
    """
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    HELL = "hell"


@dataclass
class DifficultyConfig:
    """
    Configuration parameters for a difficulty level.

    Attributes:
        min_movable_tiles: Minimum number of movable tiles (excluding power source and terminal)
        max_movable_tiles: Maximum number of movable tiles
        scramble_ratio: Minimum ratio of tiles that need manual rotation (0.0-1.0)
        min_corners: Minimum number of corner tiles in the path
        max_corners: Maximum number of corner tiles in the path
        grid_size_range: Tuple of (min_size, max_size) for grid dimensions

    Example:
        >>> config = DifficultyConfig.get_config(DifficultyLevel.EASY)
        >>> print(config.min_movable_tiles)
        3
    """
    min_movable_tiles: int
    max_movable_tiles: int
    scramble_ratio: float
    min_corners: int
    max_corners: int
    grid_size_range: Tuple[int, int]

    @staticmethod
    def get_config(level: DifficultyLevel) -> 'DifficultyConfig':
        """
        Get configuration for a specific difficulty level.

        Args:
            level: The difficulty level

        Returns:
            DifficultyConfig for the specified level

        Example:
            >>> config = DifficultyConfig.get_config(DifficultyLevel.NORMAL)
            >>> print(config.scramble_ratio)
            0.8
        """
        configs = {
            DifficultyLevel.EASY: DifficultyConfig(
                min_movable_tiles=3,
                max_movable_tiles=8,
                scramble_ratio=0.7,  # 70% need manual rotation
                min_corners=1,
                max_corners=6,
                grid_size_range=(4, 5)
            ),
            DifficultyLevel.NORMAL: DifficultyConfig(
                min_movable_tiles=4,
                max_movable_tiles=10,
                scramble_ratio=0.8,  # 80% need manual rotation
                min_corners=2,
                max_corners=8,
                grid_size_range=(5, 6)
            ),
            DifficultyLevel.HARD: DifficultyConfig(
                min_movable_tiles=5,
                max_movable_tiles=12,
                scramble_ratio=0.9,  # 90% need manual rotation
                min_corners=3,
                max_corners=10,
                grid_size_range=(6, 7)
            ),
            DifficultyLevel.HELL: DifficultyConfig(
                min_movable_tiles=6,
                max_movable_tiles=15,
                scramble_ratio=1.0,  # 100% need manual rotation
                min_corners=4,
                max_corners=12,
                grid_size_range=(7, 8)
            )
        }
        return configs[level]

    def validate_path(self, movable_count: int, corner_count: int) -> bool:
        """
        Validate if a path meets the difficulty requirements.

        Args:
            movable_count: Number of movable tiles in the path
            corner_count: Number of corner tiles in the path

        Returns:
            True if the path meets requirements, False otherwise

        Example:
            >>> config = DifficultyConfig.get_config(DifficultyLevel.EASY)
            >>> config.validate_path(movable_count=4, corner_count=2)
            True
        """
        if movable_count < self.min_movable_tiles:
            return False
        if movable_count > self.max_movable_tiles:
            return False
        if corner_count < self.min_corners:
            return False
        if corner_count > self.max_corners:
            return False
        return True
