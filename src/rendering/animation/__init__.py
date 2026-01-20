"""
Animation Module

This module provides animation functionality for the game including
rotation animations, current flow effects, and animation management.

Classes:
    Animator: Base class for all animations
    RotationAnimation: Tile rotation animation with easing
    CurrentFlowAnimation: Electrical current flow animation

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from src.rendering.animation.animator import Animator
from src.rendering.animation.rotation_animation import RotationAnimation
from src.rendering.animation.current_flow_animation import CurrentFlowAnimation

__all__ = [
    "Animator",
    "RotationAnimation",
    "CurrentFlowAnimation",
]
