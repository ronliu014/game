"""
Asset Generator Script

Generates placeholder assets for the circuit repair game.
Creates simple colored sprites for tiles, UI elements, and other game assets.

Usage:
    python tools/scripts/generate_placeholder_assets.py

Author: Circuit Repair Game Team
Date: 2026-01-21
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_directory(path: str):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def create_tile_sprite(tile_type: str, size: int = 128) -> Image.Image:
    """
    Create a placeholder tile sprite.

    Args:
        tile_type: Type of tile (power_source, terminal, straight, corner, empty)
        size: Size of the sprite in pixels

    Returns:
        PIL Image object
    """
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define colors for different tile types
    colors = {
        'power_source': (255, 215, 0, 255),    # Gold
        'terminal': (0, 191, 255, 255),        # Deep Sky Blue
        'straight': (184, 115, 51, 255),       # Copper
        'corner': (205, 127, 50, 255),         # Bronze
        'empty': (50, 50, 50, 255)             # Dark Gray
    }

    color = colors.get(tile_type, (255, 0, 255, 255))  # Magenta for unknown

    # Draw tile background
    margin = 4
    draw.rectangle(
        [margin, margin, size - margin, size - margin],
        fill=color,
        outline=(255, 255, 255, 255),
        width=2
    )

    # Draw circuit pattern based on type
    center = size // 2
    line_width = 8

    if tile_type == 'power_source':
        # Draw a star/burst pattern
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            x1 = center + int(20 * math.cos(rad))
            y1 = center + int(20 * math.sin(rad))
            x2 = center + int(40 * math.cos(rad))
            y2 = center + int(40 * math.sin(rad))
            draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 255), width=3)

    elif tile_type == 'terminal':
        # Draw a target/circle pattern
        for radius in [15, 25, 35]:
            draw.ellipse(
                [center - radius, center - radius, center + radius, center + radius],
                outline=(255, 255, 255, 255),
                width=2
            )

    elif tile_type == 'straight':
        # Draw a straight line (horizontal)
        draw.line(
            [margin + 10, center, size - margin - 10, center],
            fill=(255, 255, 255, 255),
            width=line_width
        )

    elif tile_type == 'corner':
        # Draw an L-shape (corner)
        draw.line(
            [center, margin + 10, center, center],
            fill=(255, 255, 255, 255),
            width=line_width
        )
        draw.line(
            [center, center, size - margin - 10, center],
            fill=(255, 255, 255, 255),
            width=line_width
        )

    return img


def create_button_sprite(state: str, size: tuple = (200, 60)) -> Image.Image:
    """
    Create a placeholder button sprite.

    Args:
        state: Button state (normal, hover, pressed)
        size: Size of the button (width, height)

    Returns:
        PIL Image object
    """
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define colors for different states
    colors = {
        'normal': (100, 100, 100, 255),
        'hover': (150, 150, 150, 255),
        'pressed': (80, 80, 80, 255)
    }

    color = colors.get(state, (100, 100, 100, 255))

    # Draw button
    draw.rounded_rectangle(
        [0, 0, size[0], size[1]],
        radius=10,
        fill=color,
        outline=(255, 255, 255, 255),
        width=2
    )

    return img


def generate_all_assets():
    """Generate all placeholder assets."""
    print("Generating placeholder assets...")

    # Create directories
    create_directory('assets/sprites/tiles')
    create_directory('assets/sprites/ui')
    create_directory('assets/sprites/effects')

    # Generate tile sprites
    tile_types = ['power_source', 'terminal', 'straight', 'corner', 'empty']
    for tile_type in tile_types:
        print(f"  Creating tile: {tile_type}")
        img = create_tile_sprite(tile_type)
        img.save(f'assets/sprites/tiles/tile_{tile_type}.png')

    # Generate button sprites
    button_states = ['normal', 'hover', 'pressed']
    for state in button_states:
        print(f"  Creating button: {state}")
        img = create_button_sprite(state)
        img.save(f'assets/sprites/ui/button_{state}.png')

    # Create a simple particle sprite
    print("  Creating particle sprite")
    particle = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(particle)
    draw.ellipse([0, 0, 16, 16], fill=(255, 255, 255, 255))
    particle.save('assets/sprites/effects/particle.png')

    print("\n✅ All placeholder assets generated successfully!")
    print("\nGenerated files:")
    print("  - assets/sprites/tiles/tile_*.png (5 files)")
    print("  - assets/sprites/ui/button_*.png (3 files)")
    print("  - assets/sprites/effects/particle.png")
    print("\nYou can now run the game with: python src/main.py")


if __name__ == "__main__":
    try:
        generate_all_assets()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have Pillow installed: pip install Pillow")
