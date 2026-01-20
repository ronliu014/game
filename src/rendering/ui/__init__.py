"""
UI Module

This module provides UI components for the game including buttons, panels,
HUD, and UI management.

Classes:
    UIComponent: Base class for all UI components
    Button: Interactive button component
    HUD: Heads-up display component
    Panel: Container panel for grouping components
    UIManager: Central manager for UI components

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from src.rendering.ui.ui_component import UIComponent
from src.rendering.ui.button import Button
from src.rendering.ui.hud import HUD
from src.rendering.ui.panel import Panel
from src.rendering.ui.ui_manager import UIManager

__all__ = [
    "UIComponent",
    "Button",
    "HUD",
    "Panel",
    "UIManager",
]
