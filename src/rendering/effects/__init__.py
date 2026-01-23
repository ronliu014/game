"""
Effects Module

This module provides visual effects for the game including
particle systems, glow effects, fireworks, and smoke.

Classes:
    ParticleSystem: Particle effect system
    Particle: Individual particle
    GlowEffect: Glow effect for highlighting
    FireworksEffect: Fireworks celebration effect
    SmokeEffect: Smoke effect for failure scenes

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from src.rendering.effects.particle_system import ParticleSystem, Particle
from src.rendering.effects.glow_effect import GlowEffect
from src.rendering.effects.fireworks_effect import FireworksEffect
from src.rendering.effects.smoke_effect import SmokeEffect

__all__ = [
    "ParticleSystem",
    "Particle",
    "GlowEffect",
    "FireworksEffect",
    "SmokeEffect",
]
