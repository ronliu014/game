"""
Star Rating System

Calculates star rating based on game performance.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Dict, Any
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class StarRating:
    """
    Star rating calculator for level completion.

    Calculates 1-3 stars based on:
    - Time taken (compared to time limit)
    - Number of moves (compared to optimal moves)

    Example:
        >>> rating = StarRating()
        >>> stars = rating.calculate_stars(
        ...     time_taken=30.0,
        ...     time_limit=60.0,
        ...     moves=10,
        ...     optimal_moves=8
        ... )
        >>> print(stars)  # 3
    """

    # Star thresholds (percentage of optimal performance)
    STAR_3_TIME_THRESHOLD = 0.5    # Use ≤50% of time limit
    STAR_2_TIME_THRESHOLD = 0.75   # Use ≤75% of time limit
    STAR_3_MOVES_THRESHOLD = 1.25  # Use ≤125% of optimal moves
    STAR_2_MOVES_THRESHOLD = 1.5   # Use ≤150% of optimal moves

    def __init__(self):
        """Initialize the star rating calculator."""
        logger.debug("StarRating initialized")

    def calculate_stars(
        self,
        time_taken: float,
        time_limit: float,
        moves: int,
        optimal_moves: int
    ) -> int:
        """
        Calculate star rating based on performance.

        Args:
            time_taken: Time taken to complete level (seconds)
            time_limit: Time limit for the level (seconds)
            moves: Number of moves made
            optimal_moves: Optimal number of moves for the level

        Returns:
            int: Star rating (1-3)
        """
        # Calculate time performance (0.0 to 1.0, lower is better)
        time_ratio = time_taken / time_limit if time_limit > 0 else 1.0

        # Calculate moves performance (1.0 is optimal, higher is worse)
        moves_ratio = moves / optimal_moves if optimal_moves > 0 else 1.0

        # Determine stars based on both metrics
        stars = self._calculate_stars_from_metrics(time_ratio, moves_ratio)

        logger.info(
            f"Star rating calculated: {stars} stars "
            f"(time: {time_ratio:.2%}, moves: {moves_ratio:.2f}x)"
        )

        return stars

    def _calculate_stars_from_metrics(
        self,
        time_ratio: float,
        moves_ratio: float
    ) -> int:
        """
        Calculate stars from performance metrics.

        Args:
            time_ratio: Time used / time limit (0.0 to 1.0)
            moves_ratio: Moves used / optimal moves (≥1.0)

        Returns:
            int: Star rating (1-3)
        """
        # 3 stars: Excellent performance on both metrics
        if (time_ratio <= self.STAR_3_TIME_THRESHOLD and
            moves_ratio <= self.STAR_3_MOVES_THRESHOLD):
            return 3

        # 2 stars: Good performance on both metrics
        if (time_ratio <= self.STAR_2_TIME_THRESHOLD and
            moves_ratio <= self.STAR_2_MOVES_THRESHOLD):
            return 2

        # 1 star: Completed the level
        return 1

    def get_star_requirements(
        self,
        time_limit: float,
        optimal_moves: int
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get the requirements for each star rating.

        Args:
            time_limit: Time limit for the level (seconds)
            optimal_moves: Optimal number of moves

        Returns:
            Dict containing requirements for each star level
        """
        return {
            '3_stars': {
                'max_time': time_limit * self.STAR_3_TIME_THRESHOLD,
                'max_moves': int(optimal_moves * self.STAR_3_MOVES_THRESHOLD),
                'description': '优秀'
            },
            '2_stars': {
                'max_time': time_limit * self.STAR_2_TIME_THRESHOLD,
                'max_moves': int(optimal_moves * self.STAR_2_MOVES_THRESHOLD),
                'description': '良好'
            },
            '1_star': {
                'max_time': time_limit,
                'max_moves': float('inf'),
                'description': '完成'
            }
        }

    def format_star_display(self, stars: int) -> str:
        """
        Format star rating for display.

        Args:
            stars: Number of stars (1-3)

        Returns:
            str: Formatted star display (e.g., "★★★")
        """
        filled_star = "★"
        empty_star = "☆"
        return filled_star * stars + empty_star * (3 - stars)

    def get_star_color(self, stars: int) -> tuple:
        """
        Get the color for star display.

        Args:
            stars: Number of stars (1-3)

        Returns:
            tuple: RGB color tuple
        """
        colors = {
            1: (205, 127, 50),   # Bronze
            2: (192, 192, 192),  # Silver
            3: (255, 215, 0)     # Gold
        }
        return colors.get(stars, (200, 200, 200))
