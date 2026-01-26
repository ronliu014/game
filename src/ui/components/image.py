"""
Image Component

Provides an image display UI component with transformation support.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Tuple
import pygame
from src.ui.components.ui_component import UIComponent
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class Image(UIComponent):
    """
    Image component for displaying images.

    Supports scaling, rotation, and transparency.

    Attributes:
        image (pygame.Surface): Original image surface
        scale (float): Scale factor
        rotation (float): Rotation angle in degrees
        alpha (int): Transparency (0-255)

    Example:
        >>> image = Image(100, 100, 200, 200, image_surface)
        >>> image.set_scale(1.5)
        >>> image.set_rotation(45)
        >>> image.draw(screen)
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        image: Optional[pygame.Surface] = None,
        scale: float = 1.0,
        rotation: float = 0.0,
        alpha: int = 255,
        maintain_aspect_ratio: bool = True
    ):
        """
        Initialize the image component.

        Args:
            x: X position
            y: Y position
            width: Display width
            height: Display height
            image: Image surface to display
            scale: Scale factor (1.0 = original size)
            rotation: Rotation angle in degrees (clockwise)
            alpha: Transparency (0=transparent, 255=opaque)
            maintain_aspect_ratio: Whether to maintain aspect ratio when scaling
        """
        super().__init__(x, y, width, height)
        self._original_image = image
        self._scale = scale
        self._rotation = rotation
        self._alpha = alpha
        self._maintain_aspect_ratio = maintain_aspect_ratio

        # Transformed image cache
        self._transformed_image: Optional[pygame.Surface] = None
        self._needs_update = True

        if image:
            self._update_transformed_image()

        logger.debug(f"Image created at ({x}, {y}) with size ({width}, {height})")

    def _update_transformed_image(self) -> None:
        """Update the transformed image based on current transformations."""
        if not self._original_image:
            self._transformed_image = None
            return

        # Start with original image
        image = self._original_image.copy()

        # Apply scaling
        if self._maintain_aspect_ratio:
            # Calculate scale to fit within width/height while maintaining aspect ratio
            original_width, original_height = image.get_size()
            width_ratio = self.width / original_width
            height_ratio = self.height / original_height
            scale_ratio = min(width_ratio, height_ratio) * self._scale

            new_width = int(original_width * scale_ratio)
            new_height = int(original_height * scale_ratio)
        else:
            # Scale to exact width/height
            new_width = int(self.width * self._scale)
            new_height = int(self.height * self._scale)

        if new_width > 0 and new_height > 0:
            image = pygame.transform.scale(image, (new_width, new_height))

        # Apply rotation
        if self._rotation != 0:
            image = pygame.transform.rotate(image, self._rotation)

        # Apply alpha
        if self._alpha < 255:
            image.set_alpha(self._alpha)

        self._transformed_image = image
        self._needs_update = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the image on the given surface.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible or not self._transformed_image:
            return

        # Update transformation if needed
        if self._needs_update:
            self._update_transformed_image()

        # Calculate position to center the image
        image_rect = self._transformed_image.get_rect()
        image_rect.center = (self.x + self.width // 2, self.y + self.height // 2)

        # Draw the image
        surface.blit(self._transformed_image, image_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event (images don't handle events by default).

        Args:
            event: Pygame event to handle

        Returns:
            bool: False (images don't handle events)
        """
        return False

    def set_image(self, image: pygame.Surface) -> None:
        """
        Set the image to display.

        Args:
            image: Image surface
        """
        self._original_image = image
        self._needs_update = True
        logger.debug("Image updated")

    def get_image(self) -> Optional[pygame.Surface]:
        """
        Get the original image surface.

        Returns:
            pygame.Surface: Original image surface
        """
        return self._original_image

    def set_scale(self, scale: float) -> None:
        """
        Set the scale factor.

        Args:
            scale: Scale factor (1.0 = original size)
        """
        self._scale = max(0.1, scale)  # Minimum scale of 0.1
        self._needs_update = True
        logger.debug(f"Image scale set to {self._scale}")

    def get_scale(self) -> float:
        """
        Get the current scale factor.

        Returns:
            float: Current scale factor
        """
        return self._scale

    def set_rotation(self, rotation: float) -> None:
        """
        Set the rotation angle.

        Args:
            rotation: Rotation angle in degrees (clockwise)
        """
        self._rotation = rotation % 360  # Normalize to 0-360
        self._needs_update = True
        logger.debug(f"Image rotation set to {self._rotation}°")

    def get_rotation(self) -> float:
        """
        Get the current rotation angle.

        Returns:
            float: Current rotation angle in degrees
        """
        return self._rotation

    def set_alpha(self, alpha: int) -> None:
        """
        Set the transparency.

        Args:
            alpha: Transparency (0=transparent, 255=opaque)
        """
        self._alpha = max(0, min(255, alpha))
        self._needs_update = True
        logger.debug(f"Image alpha set to {self._alpha}")

    def get_alpha(self) -> int:
        """
        Get the current transparency.

        Returns:
            int: Current alpha value
        """
        return self._alpha

    def set_maintain_aspect_ratio(self, maintain: bool) -> None:
        """
        Set whether to maintain aspect ratio when scaling.

        Args:
            maintain: True to maintain aspect ratio, False to stretch
        """
        self._maintain_aspect_ratio = maintain
        self._needs_update = True

    def load_from_file(self, file_path: str) -> bool:
        """
        Load image from file.

        Args:
            file_path: Path to image file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            image = pygame.image.load(file_path)
            self.set_image(image)
            logger.info(f"Image loaded from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load image from {file_path}: {e}")
            return False
