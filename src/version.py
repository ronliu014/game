"""
Version Information for Circuit Repair Game
电路修复游戏版本信息

This module contains version and metadata information for the game.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Application metadata
APP_NAME = "Circuit Repair Game"
APP_NAME_CN = "电路修复游戏"
APP_AUTHOR = "Circuit Repair Game Team"
APP_LICENSE = "MIT"
APP_COPYRIGHT = "Copyright (c) 2026 Circuit Repair Game Team"
APP_DESCRIPTION = "A puzzle game about connecting circuits"
APP_DESCRIPTION_CN = "一款基于 Pygame 的益智解谜游戏"

# Build information
BUILD_DATE = "2026-01-24"
BUILD_TYPE = "Release"

# Repository information
REPO_URL = "https://github.com/your-username/circuit-repair-game"
ISSUES_URL = "https://github.com/your-username/circuit-repair-game/issues"
DOCS_URL = "https://github.com/your-username/circuit-repair-game/wiki"


def get_version_string() -> str:
    """
    Get the full version string.
    
    Returns:
        str: Version string (e.g., "1.0.0")
    """
    return __version__


def get_version_info() -> tuple:
    """
    Get the version information as a tuple.
    
    Returns:
        tuple: Version tuple (e.g., (1, 0, 0))
    """
    return __version_info__


def get_full_version_string() -> str:
    """
    Get the full version string with build information.
    
    Returns:
        str: Full version string (e.g., "1.0.0 (Release, 2026-01-24)")
    """
    return f"{__version__} ({BUILD_TYPE}, {BUILD_DATE})"


def get_app_info() -> dict:
    """
    Get all application information as a dictionary.
    
    Returns:
        dict: Application information
    """
    return {
        "name": APP_NAME,
        "name_cn": APP_NAME_CN,
        "version": __version__,
        "version_info": __version_info__,
        "author": APP_AUTHOR,
        "license": APP_LICENSE,
        "copyright": APP_COPYRIGHT,
        "description": APP_DESCRIPTION,
        "description_cn": APP_DESCRIPTION_CN,
        "build_date": BUILD_DATE,
        "build_type": BUILD_TYPE,
        "repo_url": REPO_URL,
        "issues_url": ISSUES_URL,
        "docs_url": DOCS_URL,
    }


def print_version_info():
    """Print version information to console."""
    print(f"{APP_NAME} ({APP_NAME_CN})")
    print(f"Version: {get_full_version_string()}")
    print(f"Author: {APP_AUTHOR}")
    print(f"License: {APP_LICENSE}")
    print(f"Repository: {REPO_URL}")


if __name__ == "__main__":
    print_version_info()
