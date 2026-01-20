"""
Rendering Module

This module provides rendering functionality for the game, including
sprite management, rendering pipeline, and visual effects.

Classes:
    Renderer: Main rendering engine
    SpriteManager: Sprite loading and caching

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from src.rendering.renderer import Renderer
from src.rendering.sprite_manager import SpriteManager

__all__ = [
    "Renderer",
    "SpriteManager",
]
