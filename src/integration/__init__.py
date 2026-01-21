"""
Integration Module

This module provides integration components for the game including
game loop, scene management, game controller, and external API.

Classes:
    GameAPI: External API for game integration
    GameController: Coordinates all game modules
    GameLoop: Main game loop
    SceneManager: Scene management and transitions
    Scene: Base scene class
    SceneType: Scene type enumeration

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from src.integration.game_api import GameAPI
from src.integration.game_controller import GameController
from src.integration.game_loop import GameLoop
from src.integration.scene_manager import SceneManager, Scene, SceneType

__all__ = [
    "GameAPI",
    "GameController",
    "GameLoop",
    "SceneManager",
    "Scene",
    "SceneType",
]
