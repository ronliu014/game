"""
Audio Module

This module provides audio functionality for the game including
sound effects, background music, and centralized audio management.

Classes:
    AudioManager: Centralized audio management
    SoundPlayer: Sound effect playback
    BGMController: Background music control

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

from src.audio.audio_manager import AudioManager
from src.audio.sound_player import SoundPlayer
from src.audio.bgm_controller import BGMController

__all__ = [
    "AudioManager",
    "SoundPlayer",
    "BGMController",
]
