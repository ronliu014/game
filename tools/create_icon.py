"""
Icon Generator for Circuit Repair Game
电路修复游戏图标生成器

This script generates a simple application icon for the game.
For production, replace with a professionally designed icon.

Usage:
    python tools/create_icon.py
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(output_path: str = "assets/icon.ico", size: int = 256):
    """
    Create a simple application icon.
    
    Args:
        output_path: Path to save the icon file
        size: Icon size in pixels (will generate multiple sizes)
    """
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Steampunk color palette (copper/brass tones)
    copper = (184, 115, 51)      # #B87333
    brass = (205, 127, 50)       # #CD7F32
    dark_copper = (139, 69, 19)  # #8B4513
    
    # Draw background circle (copper)
    margin = size // 10
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=copper,
        outline=dark_copper,
        width=size // 40
    )
    
    # Draw circuit pattern (simplified)
    center = size // 2
    line_width = size // 20
    
    # Horizontal line
    draw.line(
        [(margin * 2, center), (size - margin * 2, center)],
        fill=brass,
        width=line_width
    )
    
    # Vertical line
    draw.line(
        [(center, margin * 2), (center, size - margin * 2)],
        fill=brass,
        width=line_width
    )
    
    # Draw power source (red circle on left)
    power_size = size // 6
    draw.ellipse(
        [margin * 2 - power_size // 2, center - power_size // 2,
         margin * 2 + power_size // 2, center + power_size // 2],
        fill=(220, 50, 50),
        outline=(180, 30, 30),
        width=size // 80
    )
    
    # Draw terminal (green circle on right)
    draw.ellipse(
        [size - margin * 2 - power_size // 2, center - power_size // 2,
         size - margin * 2 + power_size // 2, center + power_size // 2],
        fill=(50, 220, 50),
        outline=(30, 180, 30),
        width=size // 80
    )
    
    # Draw corner pieces (top and bottom)
    corner_size = size // 8
    
    # Top corner
    draw.arc(
        [center - corner_size, margin * 2 - corner_size,
         center + corner_size, margin * 2 + corner_size],
        start=180,
        end=270,
        fill=brass,
        width=line_width
    )
    
    # Bottom corner
    draw.arc(
        [center - corner_size, size - margin * 2 - corner_size,
         center + corner_size, size - margin * 2 + corner_size],
        start=0,
        end=90,
        fill=brass,
        width=line_width
    )
    
    # Save as ICO with multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save as ICO
    img.save(output_path, format='ICO', sizes=icon_sizes)
    print(f"✅ Icon created: {output_path}")
    
    # Also save as PNG for reference
    png_path = output_path.replace('.ico', '.png')
    img.save(png_path, format='PNG')
    print(f"✅ PNG version created: {png_path}")


def main():
    """Main entry point."""
    print("=" * 50)
    print("Circuit Repair Game - Icon Generator")
    print("电路修复游戏 - 图标生成器")
    print("=" * 50)
    print()
    
    try:
        create_icon()
        print()
        print("✅ Icon generation completed successfully!")
        print()
        print("Note: This is a simple placeholder icon.")
        print("For production, consider using a professionally designed icon.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
