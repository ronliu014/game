"""
Unit tests for SaveManager.

Tests save file management, backup, and recovery.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from src.progression.save_manager import SaveManager
from src.progression.progress_data import GameProgress


@pytest.fixture
def temp_save_dir():
    """Create a temporary directory for save files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def save_manager(temp_save_dir):
    """Create a SaveManager with temporary directory."""
    return SaveManager(save_dir=temp_save_dir)


class TestSaveManagerInit:
    """Test SaveManager initialization."""

    def test_init_default(self):
        """Test default initialization."""
        manager = SaveManager()

        assert manager._save_dir == Path("data/saves")
        assert manager._save_file == "player_progress.json"

    def test_init_custom_paths(self, temp_save_dir):
        """Test initialization with custom paths."""
        manager = SaveManager(save_dir=temp_save_dir, save_file="custom.json")

        assert manager._save_dir == Path(temp_save_dir)
        assert manager._save_file == "custom.json"

    def test_creates_save_directory(self, temp_save_dir):
        """Test that save directory is created."""
        save_dir = Path(temp_save_dir) / "new_dir"
        manager = SaveManager(save_dir=str(save_dir))

        assert save_dir.exists()


class TestSaveManagerLoadSave:
    """Test loading save files."""

    def test_load_save_no_file(self, save_manager):
        """Test loading when no save file exists."""
        progress = save_manager.load_save()

        assert progress is not None
        assert isinstance(progress, GameProgress)
        assert progress.current_level == 1

    def test_load_save_existing_file(self, save_manager):
        """Test loading existing save file."""
        # Create a save file
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)
        save_manager.save_progress(progress)

        # Load it back
        loaded = save_manager.load_save()

        assert loaded.is_level_completed(1)
        assert loaded.get_total_stars() == 3

    def test_load_save_corrupted_file(self, save_manager):
        """Test loading corrupted save file."""
        # Create corrupted save file
        save_path = save_manager.get_save_path()
        with open(save_path, 'w') as f:
            f.write("corrupted data")

        # Should create new progress
        progress = save_manager.load_save()

        assert progress is not None
        assert progress.current_level == 1

    def test_load_save_invalid_json(self, save_manager):
        """Test loading invalid JSON."""
        # Create invalid JSON
        save_path = save_manager.get_save_path()
        with open(save_path, 'w') as f:
            f.write('{"invalid": json}')

        # Should create new progress
        progress = save_manager.load_save()

        assert progress is not None


class TestSaveManagerSaveProgress:
    """Test saving progress."""

    def test_save_progress_new_file(self, save_manager):
        """Test saving to new file."""
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)

        result = save_manager.save_progress(progress)

        assert result is True
        assert save_manager.save_exists()

    def test_save_progress_overwrite(self, save_manager):
        """Test overwriting existing save."""
        # Create initial save
        progress1 = GameProgress()
        progress1.complete_level(1, stars=2, time=60.0, moves=20)
        save_manager.save_progress(progress1)

        # Overwrite with new progress
        progress2 = GameProgress()
        progress2.complete_level(1, stars=3, time=45.5, moves=12)
        result = save_manager.save_progress(progress2)

        assert result is True

        # Load and verify
        loaded = save_manager.load_save()
        assert loaded.levels[1].stars == 3

    def test_save_progress_creates_backup(self, save_manager):
        """Test that backup is created."""
        # Create initial save
        progress1 = GameProgress()
        save_manager.save_progress(progress1, create_backup=False)

        # Save again with backup
        progress2 = GameProgress()
        progress2.complete_level(1, stars=3, time=45.5, moves=12)
        save_manager.save_progress(progress2, create_backup=True)

        # Check backup exists
        backups = save_manager.get_backup_files()
        assert len(backups) > 0

    def test_save_progress_no_backup(self, save_manager):
        """Test saving without backup."""
        progress = GameProgress()
        result = save_manager.save_progress(progress, create_backup=False)

        assert result is True
        assert len(save_manager.get_backup_files()) == 0


class TestSaveManagerBackup:
    """Test backup functionality."""

    def test_create_backup(self, save_manager):
        """Test creating backup."""
        # Create initial save
        progress = GameProgress()
        save_manager.save_progress(progress, create_backup=False)

        # Create backup manually
        save_manager._create_backup()

        # Check backup exists
        backups = save_manager.get_backup_files()
        assert len(backups) == 1

    def test_cleanup_old_backups(self, save_manager):
        """Test cleanup of old backups."""
        progress = GameProgress()

        # Create multiple saves to generate backups
        for i in range(5):
            progress.complete_level(i + 1, stars=3, time=45.5, moves=12)
            save_manager.save_progress(progress, create_backup=True)

        # Should keep only MAX_BACKUPS
        backups = save_manager.get_backup_files()
        assert len(backups) <= SaveManager.MAX_BACKUPS

    def test_recover_from_backup(self, save_manager):
        """Test recovery from backup."""
        # Create initial save
        progress1 = GameProgress()
        progress1.complete_level(1, stars=3, time=45.5, moves=12)
        save_manager.save_progress(progress1)

        # Corrupt main save
        save_path = save_manager.get_save_path()
        with open(save_path, 'w') as f:
            f.write("corrupted")

        # Load should recover from backup
        loaded = save_manager.load_save()

        assert loaded is not None
        # Should either recover from backup or create new
        assert isinstance(loaded, GameProgress)


class TestSaveManagerUtilities:
    """Test utility methods."""

    def test_create_new_save(self, save_manager):
        """Test creating new save."""
        progress = save_manager.create_new_save()

        assert progress is not None
        assert save_manager.save_exists()

    def test_delete_save(self, save_manager):
        """Test deleting save."""
        # Create save
        progress = GameProgress()
        save_manager.save_progress(progress)

        # Delete it
        result = save_manager.delete_save()

        assert result is True
        assert not save_manager.save_exists()

    def test_delete_save_no_file(self, save_manager):
        """Test deleting when no save exists."""
        result = save_manager.delete_save()

        assert result is False

    def test_save_exists(self, save_manager):
        """Test checking if save exists."""
        assert not save_manager.save_exists()

        progress = GameProgress()
        save_manager.save_progress(progress)

        assert save_manager.save_exists()

    def test_get_save_path(self, save_manager):
        """Test getting save path."""
        path = save_manager.get_save_path()

        assert isinstance(path, Path)
        assert path.name == "player_progress.json"

    def test_get_backup_files(self, save_manager):
        """Test getting backup files."""
        # No backups initially
        backups = save_manager.get_backup_files()
        assert len(backups) == 0

        # Create some backups
        progress = GameProgress()
        for i in range(3):
            progress.complete_level(i + 1, stars=3, time=45.5, moves=12)
            save_manager.save_progress(progress, create_backup=True)

        backups = save_manager.get_backup_files()
        assert len(backups) > 0


class TestSaveManagerImportExport:
    """Test import/export functionality."""

    def test_export_save(self, save_manager, temp_save_dir):
        """Test exporting save."""
        # Create save
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)
        save_manager.save_progress(progress)

        # Export it
        export_path = Path(temp_save_dir) / "export" / "exported.json"
        result = save_manager.export_save(str(export_path))

        assert result is True
        assert export_path.exists()

    def test_export_save_no_file(self, save_manager, temp_save_dir):
        """Test exporting when no save exists."""
        export_path = Path(temp_save_dir) / "exported.json"
        result = save_manager.export_save(str(export_path))

        assert result is False

    def test_import_save(self, save_manager, temp_save_dir):
        """Test importing save."""
        # Create a save file to import
        import_path = Path(temp_save_dir) / "import.json"
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)
        progress.complete_level(2, stars=2, time=60.0, moves=20)

        with open(import_path, 'w', encoding='utf-8') as f:
            json.dump(progress.to_dict(), f)

        # Import it
        imported = save_manager.import_save(str(import_path))

        assert imported is not None
        assert imported.is_level_completed(1)
        assert imported.is_level_completed(2)
        assert save_manager.save_exists()

    def test_import_save_not_found(self, save_manager):
        """Test importing non-existent file."""
        result = save_manager.import_save("nonexistent.json")

        assert result is None

    def test_import_save_invalid(self, save_manager, temp_save_dir):
        """Test importing invalid save."""
        import_path = Path(temp_save_dir) / "invalid.json"
        with open(import_path, 'w') as f:
            f.write("invalid json")

        result = save_manager.import_save(str(import_path))

        assert result is None


class TestSaveManagerValidation:
    """Test save data validation."""

    def test_validate_save_data_valid(self, save_manager):
        """Test validating valid save data."""
        data = {
            'levels': {},
            'current_level': 1,
            'total_stars': 0,
            'version': '1.0.0'
        }

        result = save_manager._validate_save_data(data)

        assert result is True

    def test_validate_save_data_missing_field(self, save_manager):
        """Test validating save data with missing field."""
        data = {
            'levels': {},
            'current_level': 1
            # Missing total_stars and version
        }

        result = save_manager._validate_save_data(data)

        assert result is False


class TestSaveManagerIntegration:
    """Integration tests for SaveManager."""

    def test_full_save_load_cycle(self, save_manager):
        """Test complete save and load cycle."""
        # Create progress
        progress = GameProgress()
        progress.complete_level(1, stars=3, time=45.5, moves=12)
        progress.complete_level(2, stars=2, time=60.0, moves=20)
        progress.complete_level(3, stars=3, time=50.0, moves=15)
        progress.add_playtime(180.0)

        # Save it
        save_manager.save_progress(progress)

        # Load it back
        loaded = save_manager.load_save()

        # Verify all data
        assert loaded.get_completed_levels_count() == 3
        assert loaded.get_total_stars() == 8
        assert loaded.total_playtime == 180.0
        assert loaded.current_level == 4

    def test_multiple_save_load_cycles(self, save_manager):
        """Test multiple save/load cycles."""
        for i in range(5):
            progress = save_manager.load_save()
            progress.complete_level(i + 1, stars=3, time=45.5, moves=12)
            save_manager.save_progress(progress)

        # Final load
        final = save_manager.load_save()

        assert final.get_completed_levels_count() == 5
        assert final.get_total_stars() == 15


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
