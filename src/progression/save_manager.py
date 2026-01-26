"""
Save Manager

Manages loading and saving game progress to disk.

Author: Circuit Repair Game Team
Date: 2026-01-24
"""

import os
import json
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime
from src.progression.progress_data import GameProgress
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class SaveManager:
    """
    Manages game save files.

    Handles loading, saving, and backing up game progress data.

    Features:
        - JSON-based save files
        - Automatic backup creation
        - Error recovery
        - Save file validation

    Example:
        >>> manager = SaveManager()
        >>> progress = manager.load_save()
        >>> progress.complete_level(1, stars=3, time=45.5, moves=12)
        >>> manager.save_progress(progress)
    """

    DEFAULT_SAVE_DIR = "data/saves"
    DEFAULT_SAVE_FILE = "player_progress.json"
    BACKUP_SUFFIX = ".backup"
    MAX_BACKUPS = 3

    def __init__(self, save_dir: Optional[str] = None, save_file: Optional[str] = None):
        """
        Initialize the save manager.

        Args:
            save_dir: Directory for save files (default: data/saves)
            save_file: Save file name (default: player_progress.json)
        """
        self._save_dir = Path(save_dir or self.DEFAULT_SAVE_DIR)
        self._save_file = save_file or self.DEFAULT_SAVE_FILE
        self._save_path = self._save_dir / self._save_file

        # Create save directory if it doesn't exist
        self._ensure_save_directory()

        logger.debug(f"SaveManager initialized: {self._save_path}")

    def _ensure_save_directory(self) -> None:
        """Create save directory if it doesn't exist."""
        try:
            self._save_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Save directory ensured: {self._save_dir}")
        except Exception as e:
            logger.error(f"Failed to create save directory: {e}")
            raise

    def load_save(self) -> GameProgress:
        """
        Load game progress from save file.

        Returns:
            GameProgress: Loaded progress or new progress if file doesn't exist

        Raises:
            Exception: If save file is corrupted and backup recovery fails
        """
        # Try to load from main save file
        if self._save_path.exists():
            try:
                progress = self._load_from_file(self._save_path)
                logger.info(f"Save loaded successfully: {self._save_path}")
                return progress
            except Exception as e:
                logger.error(f"Failed to load save file: {e}")

                # Try to recover from backup
                backup_progress = self._try_recover_from_backup()
                if backup_progress:
                    logger.info("Recovered progress from backup")
                    return backup_progress

                logger.warning("Creating new save file")

        # Create new progress if no save exists
        logger.info("Creating new game progress")
        return GameProgress()

    def _load_from_file(self, file_path: Path) -> GameProgress:
        """
        Load progress from a specific file.

        Args:
            file_path: Path to save file

        Returns:
            GameProgress: Loaded progress

        Raises:
            Exception: If file cannot be loaded or parsed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate save data
            if not self._validate_save_data(data):
                raise ValueError("Invalid save data format")

            progress = GameProgress.from_dict(data)
            logger.debug(f"Loaded progress from {file_path}")
            return progress

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading save file: {e}")
            raise

    def _validate_save_data(self, data: dict) -> bool:
        """
        Validate save data structure.

        Args:
            data: Save data dictionary

        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['levels', 'current_level', 'total_stars', 'version']

        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False

        return True

    def save_progress(self, progress: GameProgress, create_backup: bool = True) -> bool:
        """
        Save game progress to disk.

        Args:
            progress: Game progress to save
            create_backup: Whether to create a backup before saving

        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Create backup if requested and save exists
            if create_backup and self._save_path.exists():
                self._create_backup()

            # Save to file
            self._save_to_file(progress, self._save_path)

            logger.info(f"Progress saved successfully: {self._save_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
            return False

    def _save_to_file(self, progress: GameProgress, file_path: Path) -> None:
        """
        Save progress to a specific file.

        Args:
            progress: Game progress to save
            file_path: Path to save file

        Raises:
            Exception: If file cannot be written
        """
        try:
            # Convert to dictionary
            data = progress.to_dict()

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.debug(f"Saved progress to {file_path}")

        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            raise

    def _create_backup(self) -> None:
        """Create a backup of the current save file."""
        try:
            if not self._save_path.exists():
                return

            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{self._save_file}.{timestamp}{self.BACKUP_SUFFIX}"
            backup_path = self._save_dir / backup_name

            # Copy save file to backup
            shutil.copy2(self._save_path, backup_path)

            logger.debug(f"Backup created: {backup_path}")

            # Clean up old backups
            self._cleanup_old_backups()

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")

    def _cleanup_old_backups(self) -> None:
        """Remove old backup files, keeping only the most recent ones."""
        try:
            # Find all backup files
            backup_files = sorted(
                self._save_dir.glob(f"{self._save_file}.*{self.BACKUP_SUFFIX}"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            # Remove old backups
            for backup_file in backup_files[self.MAX_BACKUPS:]:
                backup_file.unlink()
                logger.debug(f"Removed old backup: {backup_file}")

        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")

    def _try_recover_from_backup(self) -> Optional[GameProgress]:
        """
        Try to recover progress from backup files.

        Returns:
            Optional[GameProgress]: Recovered progress or None if recovery fails
        """
        try:
            # Find all backup files
            backup_files = sorted(
                self._save_dir.glob(f"{self._save_file}.*{self.BACKUP_SUFFIX}"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            # Try to load from each backup
            for backup_file in backup_files:
                try:
                    progress = self._load_from_file(backup_file)
                    logger.info(f"Recovered from backup: {backup_file}")
                    return progress
                except Exception as e:
                    logger.warning(f"Failed to load backup {backup_file}: {e}")
                    continue

            return None

        except Exception as e:
            logger.error(f"Error during backup recovery: {e}")
            return None

    def create_new_save(self) -> GameProgress:
        """
        Create a new save file with default progress.

        Returns:
            GameProgress: New game progress
        """
        progress = GameProgress()
        self.save_progress(progress, create_backup=False)
        logger.info("New save file created")
        return progress

    def delete_save(self) -> bool:
        """
        Delete the current save file.

        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            if self._save_path.exists():
                self._save_path.unlink()
                logger.info(f"Save file deleted: {self._save_path}")
                return True
            else:
                logger.warning("No save file to delete")
                return False

        except Exception as e:
            logger.error(f"Failed to delete save file: {e}")
            return False

    def save_exists(self) -> bool:
        """
        Check if a save file exists.

        Returns:
            bool: True if save file exists, False otherwise
        """
        return self._save_path.exists()

    def get_save_path(self) -> Path:
        """
        Get the path to the save file.

        Returns:
            Path: Save file path
        """
        return self._save_path

    def get_backup_files(self) -> list:
        """
        Get list of backup files.

        Returns:
            list: List of backup file paths
        """
        try:
            backup_files = sorted(
                self._save_dir.glob(f"{self._save_file}.*{self.BACKUP_SUFFIX}"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            return list(backup_files)

        except Exception as e:
            logger.error(f"Failed to get backup files: {e}")
            return []

    def export_save(self, export_path: str) -> bool:
        """
        Export save file to a different location.

        Args:
            export_path: Path to export to

        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            if not self._save_path.exists():
                logger.error("No save file to export")
                return False

            export_path = Path(export_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(self._save_path, export_path)
            logger.info(f"Save exported to: {export_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export save: {e}")
            return False

    def import_save(self, import_path: str) -> Optional[GameProgress]:
        """
        Import save file from a different location.

        Args:
            import_path: Path to import from

        Returns:
            Optional[GameProgress]: Imported progress or None if import fails
        """
        try:
            import_path = Path(import_path)

            if not import_path.exists():
                logger.error(f"Import file not found: {import_path}")
                return None

            # Load and validate imported save
            progress = self._load_from_file(import_path)

            # Save to current location
            self.save_progress(progress, create_backup=True)

            logger.info(f"Save imported from: {import_path}")
            return progress

        except Exception as e:
            logger.error(f"Failed to import save: {e}")
            return None

    def __repr__(self) -> str:
        """String representation."""
        exists = "exists" if self.save_exists() else "not found"
        return f"SaveManager(path={self._save_path}, {exists})"
