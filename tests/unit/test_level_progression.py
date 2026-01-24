"""
Unit tests for LevelProgressionManager.

Tests level progression, unlocking, and management.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

import pytest
import tempfile
import shutil
from src.progression.level_progression import LevelProgressionManager
from src.progression.save_manager import SaveManager


@pytest.fixture
def temp_save_dir():
    """Create a temporary directory for save files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def progression_manager(temp_save_dir):
    """Create a LevelProgressionManager with temporary save."""
    save_manager = SaveManager(save_dir=temp_save_dir)
    return LevelProgressionManager(save_manager=save_manager)


class TestLevelProgressionManagerInit:
    """Test LevelProgressionManager initialization."""

    def test_init_default(self):
        """Test default initialization."""
        manager = LevelProgressionManager()

        assert manager is not None
        assert manager.get_progress() is not None

    def test_init_with_save_manager(self, temp_save_dir):
        """Test initialization with custom save manager."""
        save_manager = SaveManager(save_dir=temp_save_dir)
        manager = LevelProgressionManager(save_manager=save_manager)

        assert manager is not None


class TestLevelProgressionManagerCompletion:
    """Test level completion."""

    def test_complete_level_first_time(self, progression_manager):
        """Test completing a level for the first time."""
        result = progression_manager.complete_level(1, stars=3, time=45.5, moves=12)

        assert result['is_new_best'] is True
        assert 2 in result['unlocked_levels']
        assert result['total_stars'] == 3
        assert result['next_level'] == 2
        assert result['completed_count'] == 1

    def test_complete_level_better_score(self, progression_manager):
        """Test completing with better score."""
        progression_manager.complete_level(1, stars=2, time=60.0, moves=20)
        result = progression_manager.complete_level(1, stars=3, time=45.5, moves=12)

        assert result['is_new_best'] is True
        assert result['total_stars'] == 3

    def test_complete_level_worse_score(self, progression_manager):
        """Test completing with worse score."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        result = progression_manager.complete_level(1, stars=2, time=60.0, moves=20)

        assert result['is_new_best'] is False
        assert result['total_stars'] == 3

    def test_complete_level_auto_save(self, progression_manager):
        """Test that completion auto-saves."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12, auto_save=True)

        # Reload and verify
        progression_manager.reload_progress()
        assert progression_manager.is_level_completed(1)

    def test_complete_level_no_auto_save(self, progression_manager):
        """Test completion without auto-save."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12, auto_save=False)

        # Reload - should not be saved
        progression_manager.reload_progress()
        assert not progression_manager.is_level_completed(1)


class TestLevelProgressionManagerUnlocking:
    """Test level unlocking."""

    def test_is_level_unlocked_initial(self, progression_manager):
        """Test initial unlock state."""
        assert progression_manager.is_level_unlocked(1)
        assert not progression_manager.is_level_unlocked(2)

    def test_unlock_level_manual(self, progression_manager):
        """Test manual level unlock."""
        result = progression_manager.unlock_level(2)

        assert result is True
        assert progression_manager.is_level_unlocked(2)

    def test_unlock_level_already_unlocked(self, progression_manager):
        """Test unlocking already unlocked level."""
        result = progression_manager.unlock_level(1)

        assert result is False

    def test_unlock_level_auto_save(self, progression_manager):
        """Test that unlock auto-saves."""
        progression_manager.unlock_level(2, auto_save=True)

        # Reload and verify
        progression_manager.reload_progress()
        assert progression_manager.is_level_unlocked(2)

    def test_auto_unlock_on_completion(self, progression_manager):
        """Test that completing a level unlocks the next."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)

        assert progression_manager.is_level_unlocked(2)


class TestLevelProgressionManagerQueries:
    """Test query methods."""

    def test_is_level_completed(self, progression_manager):
        """Test checking if level is completed."""
        assert not progression_manager.is_level_completed(1)

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.is_level_completed(1)

    def test_get_level_progress(self, progression_manager):
        """Test getting level progress."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)

        level_progress = progression_manager.get_level_progress(1)

        assert level_progress is not None
        assert level_progress.level_id == 1
        assert level_progress.stars == 3

    def test_get_level_stars(self, progression_manager):
        """Test getting level stars."""
        assert progression_manager.get_level_stars(1) == 0

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.get_level_stars(1) == 3

    def test_get_level_best_time(self, progression_manager):
        """Test getting best time."""
        assert progression_manager.get_level_best_time(1) == 0.0

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.get_level_best_time(1) == 45.5

    def test_get_level_best_moves(self, progression_manager):
        """Test getting best moves."""
        assert progression_manager.get_level_best_moves(1) == 0

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.get_level_best_moves(1) == 12

    def test_get_unlocked_levels(self, progression_manager):
        """Test getting unlocked levels."""
        unlocked = progression_manager.get_unlocked_levels()

        assert 1 in unlocked
        assert 2 not in unlocked

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        unlocked = progression_manager.get_unlocked_levels()

        assert 2 in unlocked

    def test_get_completed_levels(self, progression_manager):
        """Test getting completed levels."""
        completed = progression_manager.get_completed_levels()
        assert len(completed) == 0

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        completed = progression_manager.get_completed_levels()

        assert 1 in completed

    def test_get_total_stars(self, progression_manager):
        """Test getting total stars."""
        assert progression_manager.get_total_stars() == 0

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.get_total_stars() == 3

        progression_manager.complete_level(2, stars=2, time=60.0, moves=20)
        assert progression_manager.get_total_stars() == 5

    def test_get_current_level(self, progression_manager):
        """Test getting current level."""
        assert progression_manager.get_current_level() == 1

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.get_current_level() == 2

    def test_get_completion_percentage(self, progression_manager):
        """Test getting completion percentage."""
        assert progression_manager.get_completion_percentage() == 0.0

        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        assert progression_manager.get_completion_percentage() == 50.0  # 1/2 unlocked levels


class TestLevelProgressionManagerReset:
    """Test reset functionality."""

    def test_reset_level(self, progression_manager):
        """Test resetting a level."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)

        result = progression_manager.reset_level(1)

        assert result is True
        assert not progression_manager.is_level_completed(1)
        assert progression_manager.is_level_unlocked(1)

    def test_reset_level_not_exists(self, progression_manager):
        """Test resetting non-existent level."""
        result = progression_manager.reset_level(999)

        assert result is False

    def test_reset_all_progress(self, progression_manager):
        """Test resetting all progress."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        progression_manager.complete_level(2, stars=2, time=60.0, moves=20)

        progression_manager.reset_all_progress()

        assert progression_manager.get_total_stars() == 0
        assert progression_manager.get_current_level() == 1
        assert not progression_manager.is_level_completed(1)


class TestLevelProgressionManagerSave:
    """Test save/load functionality."""

    def test_save_progress(self, progression_manager):
        """Test saving progress."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12, auto_save=False)

        result = progression_manager.save_progress()

        assert result is True

    def test_reload_progress(self, progression_manager):
        """Test reloading progress."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        progression_manager.save_progress()

        # Modify in memory
        progression_manager.complete_level(2, stars=2, time=60.0, moves=20, auto_save=False)

        # Reload
        progression_manager.reload_progress()

        # Should only have level 1 completed
        assert progression_manager.is_level_completed(1)
        assert not progression_manager.is_level_completed(2)


class TestLevelProgressionManagerPlaytime:
    """Test playtime tracking."""

    def test_add_playtime(self, progression_manager):
        """Test adding playtime."""
        progression_manager.add_playtime(60.0)

        stats = progression_manager.get_statistics()
        assert stats['total_playtime'] == 60.0

    def test_add_playtime_auto_save(self, progression_manager):
        """Test adding playtime with auto-save."""
        progression_manager.add_playtime(60.0, auto_save=True)

        progression_manager.reload_progress()
        stats = progression_manager.get_statistics()
        assert stats['total_playtime'] == 60.0


class TestLevelProgressionManagerStatistics:
    """Test statistics."""

    def test_get_statistics_initial(self, progression_manager):
        """Test getting initial statistics."""
        stats = progression_manager.get_statistics()

        assert stats['total_levels'] == 1
        assert stats['completed_levels'] == 0
        assert stats['unlocked_levels'] == 1
        assert stats['total_stars'] == 0
        assert stats['max_stars'] == 3
        assert stats['completion_percentage'] == 0.0
        assert stats['current_level'] == 1

    def test_get_statistics_after_completion(self, progression_manager):
        """Test statistics after completing levels."""
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        progression_manager.complete_level(2, stars=2, time=60.0, moves=20)

        stats = progression_manager.get_statistics()

        assert stats['completed_levels'] == 2
        assert stats['total_stars'] == 5
        assert stats['completion_percentage'] == 66.66666666666666  # 2/3


class TestLevelProgressionManagerIntegration:
    """Integration tests."""

    def test_full_progression_flow(self, progression_manager):
        """Test complete progression flow."""
        # Complete multiple levels
        for i in range(1, 4):
            result = progression_manager.complete_level(i, stars=3, time=45.5, moves=12)
            assert result['is_new_best']
            assert result['next_level'] == i + 1

        # Verify final state
        assert progression_manager.get_total_stars() == 9
        assert progression_manager.get_current_level() == 4
        assert len(progression_manager.get_completed_levels()) == 3

    def test_persistence_across_sessions(self, progression_manager):
        """Test that progress persists across sessions."""
        # Complete levels
        progression_manager.complete_level(1, stars=3, time=45.5, moves=12)
        progression_manager.complete_level(2, stars=2, time=60.0, moves=20)

        # Create new manager with same save
        new_manager = LevelProgressionManager(save_manager=progression_manager._save_manager)

        # Verify progress loaded
        assert new_manager.get_total_stars() == 5
        assert new_manager.is_level_completed(1)
        assert new_manager.is_level_completed(2)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
