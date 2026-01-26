"""
Unit tests for progress data structures.

Tests LevelProgress and GameProgress classes.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

import pytest
import json
from datetime import datetime
from src.progression.progress_data import LevelProgress, GameProgress


class TestLevelProgress:
    """Test LevelProgress class."""

    def test_init_default(self):
        """Test default initialization."""
        progress = LevelProgress(level_id=1)

        assert progress.level_id == 1
        assert not progress.completed
        assert progress.stars == 0
        assert progress.best_time == float('inf')
        assert progress.best_moves == float('inf')
        assert not progress.unlocked
        assert progress.attempts == 0
        assert progress.last_played is None

    def test_init_with_values(self):
        """Test initialization with custom values."""
        progress = LevelProgress(
            level_id=5,
            completed=True,
            stars=3,
            best_time=45.5,
            best_moves=12,
            unlocked=True,
            attempts=3
        )

        assert progress.level_id == 5
        assert progress.completed
        assert progress.stars == 3
        assert progress.best_time == 45.5
        assert progress.best_moves == 12
        assert progress.unlocked
        assert progress.attempts == 3

    def test_init_invalid_level_id(self):
        """Test initialization with invalid level_id."""
        with pytest.raises(ValueError):
            LevelProgress(level_id=0)

        with pytest.raises(ValueError):
            LevelProgress(level_id=-1)

    def test_init_invalid_stars(self):
        """Test initialization with invalid stars."""
        with pytest.raises(ValueError):
            LevelProgress(level_id=1, stars=-1)

        with pytest.raises(ValueError):
            LevelProgress(level_id=1, stars=4)

    def test_complete_first_time(self):
        """Test completing level for the first time."""
        progress = LevelProgress(level_id=1, unlocked=True)

        is_new_best = progress.complete(stars=3, time=45.5, moves=12)

        assert is_new_best
        assert progress.completed
        assert progress.stars == 3
        assert progress.best_time == 45.5
        assert progress.best_moves == 12
        assert progress.attempts == 1
        assert progress.last_played is not None

    def test_complete_with_better_score(self):
        """Test completing with better score."""
        progress = LevelProgress(level_id=1, unlocked=True)
        progress.complete(stars=2, time=60.0, moves=20)

        is_new_best = progress.complete(stars=3, time=45.5, moves=12)

        assert is_new_best
        assert progress.stars == 3
        assert progress.best_time == 45.5
        assert progress.best_moves == 12
        assert progress.attempts == 2

    def test_complete_with_worse_score(self):
        """Test completing with worse score."""
        progress = LevelProgress(level_id=1, unlocked=True)
        progress.complete(stars=3, time=45.5, moves=12)

        is_new_best = progress.complete(stars=2, time=60.0, moves=20)

        assert not is_new_best
        assert progress.stars == 3  # Keep best stars
        assert progress.best_time == 45.5  # Keep best time
        assert progress.best_moves == 12  # Keep best moves
        assert progress.attempts == 2

    def test_unlock(self):
        """Test unlocking level."""
        progress = LevelProgress(level_id=1)

        assert not progress.is_unlocked()

        progress.unlock()

        assert progress.is_unlocked()

    def test_unlock_already_unlocked(self):
        """Test unlocking already unlocked level."""
        progress = LevelProgress(level_id=1, unlocked=True)

        progress.unlock()

        assert progress.is_unlocked()

    def test_increment_attempts(self):
        """Test incrementing attempts."""
        progress = LevelProgress(level_id=1)

        progress.increment_attempts()

        assert progress.attempts == 1
        assert progress.last_played is not None

    def test_to_dict(self):
        """Test converting to dictionary."""
        progress = LevelProgress(
            level_id=1,
            completed=True,
            stars=3,
            best_time=45.5,
            best_moves=12,
            unlocked=True,
            attempts=2
        )

        data = progress.to_dict()

        assert data['level_id'] == 1
        assert data['completed'] is True
        assert data['stars'] == 3
        assert data['best_time'] == 45.5
        assert data['best_moves'] == 12
        assert data['unlocked'] is True
        assert data['attempts'] == 2

    def test_to_dict_with_inf(self):
        """Test converting to dict with inf values."""
        progress = LevelProgress(level_id=1)

        data = progress.to_dict()

        assert data['best_time'] is None
        assert data['best_moves'] is None

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            'level_id': 1,
            'completed': True,
            'stars': 3,
            'best_time': 45.5,
            'best_moves': 12,
            'unlocked': True,
            'attempts': 2,
            'last_played': '2026-01-24T10:00:00'
        }

        progress = LevelProgress.from_dict(data)

        assert progress.level_id == 1
        assert progress.completed
        assert progress.stars == 3
        assert progress.best_time == 45.5
        assert progress.best_moves == 12
        assert progress.unlocked
        assert progress.attempts == 2

    def test_from_dict_with_none(self):
        """Test creating from dict with None values."""
        data = {
            'level_id': 1,
            'completed': False,
            'stars': 0,
            'best_time': None,
            'best_moves': None,
            'unlocked': False,
            'attempts': 0,
            'last_played': None
        }

        progress = LevelProgress.from_dict(data)

        assert progress.best_time == float('inf')
        assert progress.best_moves == float('inf')


class TestGameProgress:
    """Test GameProgress class."""

    def test_init_default(self):
        """Test default initialization."""
        progress = GameProgress()

        assert progress.current_level == 1
        assert progress.total_stars == 0
        assert progress.total_playtime == 0.0
        assert progress.version == "1.0.0"
        assert progress.created_at is not None
        # Level 1 should be auto-unlocked
        assert 1 in progress.levels
        assert progress.levels[1].is_unlocked()

    def test_unlock_level(self):
        """Test unlocking a level."""
        progress = GameProgress()

        progress.unlock_level(2)

        assert progress.is_level_unlocked(2)
        assert 2 in progress.levels

    def test_complete_level_first_time(self):
        """Test completing a level for the first time."""
        progress = GameProgress()

        is_new_best = progress.complete_level(1, stars=3, time=45.5, moves=12)

        assert is_new_best
        assert progress.is_level_completed(1)
        assert progress.get_total_stars() == 3
        assert progress.is_level_unlocked(2)  # Next level unlocked
        assert progress.current_level == 2

    def test_complete_level_updates_stars(self):
        """Test that completing level updates total stars."""
        progress = GameProgress()

        progress.complete_level(1, stars=2, time=60.0, moves=20)
        assert progress.get_total_stars() == 2

        progress.complete_level(1, stars=3, time=45.5, moves=12)
        assert progress.get_total_stars() == 3

    def test_complete_multiple_levels(self):
        """Test completing multiple levels."""
        progress = GameProgress()

        progress.complete_level(1, stars=3, time=45.5, moves=12)
        progress.complete_level(2, stars=2, time=60.0, moves=20)
        progress.complete_level(3, stars=3, time=50.0, moves=15)

        assert progress.get_completed_levels_count() == 3
        assert progress.get_total_stars() == 8
        assert progress.current_level == 4

    def test_is_level_unlocked(self):
        """Test checking if level is unlocked."""
        progress = GameProgress()

        assert progress.is_level_unlocked(1)
        assert not progress.is_level_unlocked(2)

        progress.unlock_level(2)
        assert progress.is_level_unlocked(2)

    def test_is_level_completed(self):
        """Test checking if level is completed."""
        progress = GameProgress()

        assert not progress.is_level_completed(1)

        progress.complete_level(1, stars=3, time=45.5, moves=12)
        assert progress.is_level_completed(1)

    def test_get_level_progress(self):
        """Test getting level progress."""
        progress = GameProgress()

        level_progress = progress.get_level_progress(1)

        assert level_progress is not None
        assert level_progress.level_id == 1

    def test_get_level_progress_not_found(self):
        """Test getting progress for non-existent level."""
        progress = GameProgress()

        level_progress = progress.get_level_progress(999)

        assert level_progress is None

    def test_get_completed_levels_count(self):
        """Test getting completed levels count."""
        progress = GameProgress()

        assert progress.get_completed_levels_count() == 0

        progress.complete_level(1, stars=3, time=45.5, moves=12)
        assert progress.get_completed_levels_count() == 1

        progress.complete_level(2, stars=2, time=60.0, moves=20)
        assert progress.get_completed_levels_count() == 2

    def test_get_unlocked_levels_count(self):
        """Test getting unlocked levels count."""
        progress = GameProgress()

        assert progress.get_unlocked_levels_count() == 1  # Level 1 auto-unlocked

        progress.unlock_level(2)
        assert progress.get_unlocked_levels_count() == 2

    def test_add_playtime(self):
        """Test adding playtime."""
        progress = GameProgress()

        progress.add_playtime(60.0)
        assert progress.total_playtime == 60.0

        progress.add_playtime(30.5)
        assert progress.total_playtime == 90.5

    def test_to_dict(self):
        """Test converting to dictionary."""
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)

        data = progress.to_dict()

        assert 'levels' in data
        assert '1' in data['levels']
        assert data['current_level'] == 2
        assert data['total_stars'] == 3
        assert data['version'] == '1.0.0'

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {
            'levels': {
                '1': {
                    'level_id': 1,
                    'completed': True,
                    'stars': 3,
                    'best_time': 45.5,
                    'best_moves': 12,
                    'unlocked': True,
                    'attempts': 1,
                    'last_played': '2026-01-24T10:00:00'
                }
            },
            'current_level': 2,
            'total_stars': 3,
            'total_playtime': 60.0,
            'last_played': '2026-01-24T10:00:00',
            'version': '1.0.0',
            'created_at': '2026-01-24T09:00:00'
        }

        progress = GameProgress.from_dict(data)

        assert progress.current_level == 2
        assert progress.total_stars == 3
        assert progress.total_playtime == 60.0
        assert 1 in progress.levels
        assert progress.levels[1].is_completed()

    def test_to_json_and_from_json(self):
        """Test JSON serialization and deserialization."""
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)
        progress.complete_level(2, stars=2, time=60.0, moves=20)

        # Serialize to JSON
        json_str = progress.to_json()

        # Deserialize from JSON
        restored = GameProgress.from_json(json_str)

        assert restored.current_level == progress.current_level
        assert restored.total_stars == progress.total_stars
        assert restored.get_completed_levels_count() == progress.get_completed_levels_count()

    def test_auto_unlock_next_level(self):
        """Test that completing a level auto-unlocks the next."""
        progress = GameProgress()

        assert progress.is_level_unlocked(1)
        assert not progress.is_level_unlocked(2)

        progress.complete_level(1, stars=3, time=45.5, moves=12)

        assert progress.is_level_unlocked(2)

    def test_current_level_progression(self):
        """Test current level progression."""
        progress = GameProgress()

        assert progress.current_level == 1

        progress.complete_level(1, stars=3, time=45.5, moves=12)
        assert progress.current_level == 2

        progress.complete_level(2, stars=2, time=60.0, moves=20)
        assert progress.current_level == 3

    def test_replay_level_doesnt_change_current(self):
        """Test that replaying a level doesn't change current level."""
        progress = GameProgress()

        progress.complete_level(1, stars=3, time=45.5, moves=12)
        progress.complete_level(2, stars=2, time=60.0, moves=20)

        assert progress.current_level == 3

        # Replay level 1
        progress.complete_level(1, stars=3, time=40.0, moves=10)

        assert progress.current_level == 3  # Should not change


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
