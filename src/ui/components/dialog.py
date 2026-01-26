"""
Dialog Component

Provides a modal dialog box for displaying messages and getting user confirmation.

Author: Circuit Repair Game Team
Date: 2026-01-26
"""

from typing import Optional, Callable, Tuple
import pygame
from src.ui.components.ui_component import UIComponent
from src.ui.components.panel import Panel
from src.ui.components.label import Label
from src.ui.components.button import Button
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class Dialog(UIComponent):
    """
    Modal dialog component for displaying messages.

    Features:
    - Semi-transparent overlay background
    - Centered dialog panel
    - Title and message text
    - OK button to close
    - Optional callback on close

    Example:
        >>> def on_close():
        ...     print("Dialog closed")
        >>> dialog = Dialog(
        ...     screen_width=800,
        ...     screen_height=600,
        ...     title="提示",
        ...     message="关卡未解锁",
        ...     on_close=on_close
        ... )
        >>> dialog.draw(screen)
    """

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        title: str,
        message: str,
        on_close: Optional[Callable] = None,
        dialog_width: int = 400,
        dialog_height: int = 200
    ):
        """
        Initialize the dialog.

        Args:
            screen_width: Screen width
            screen_height: Screen height
            title: Dialog title
            message: Dialog message
            on_close: Optional callback when dialog is closed
            dialog_width: Width of dialog panel
            dialog_height: Height of dialog panel
        """
        super().__init__(0, 0, screen_width, screen_height)

        self._screen_width = screen_width
        self._screen_height = screen_height
        self._title = title
        self._message = message
        self._on_close = on_close
        self._dialog_width = dialog_width
        self._dialog_height = dialog_height

        # Calculate dialog position (centered)
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2

        # Create overlay (semi-transparent background)
        self._overlay = Panel(
            x=0, y=0,
            width=screen_width,
            height=screen_height,
            background_color=(0, 0, 0),
            border_width=0
        )
        self._overlay.set_alpha(180)  # Semi-transparent

        # Create dialog panel
        self._dialog_panel = Panel(
            x=dialog_x,
            y=dialog_y,
            width=dialog_width,
            height=dialog_height,
            background_color=(40, 40, 50),
            border_color=(100, 100, 120),
            border_width=3
        )

        # Create title label
        self._title_label = Label(
            x=dialog_x + 20,
            y=dialog_y + 20,
            width=dialog_width - 40,
            height=40,
            text=title,
            font_size=28,
            text_color=(255, 255, 255),
            alignment=Label.ALIGN_CENTER
        )

        # Create message label
        self._message_label = Label(
            x=dialog_x + 20,
            y=dialog_y + 70,
            width=dialog_width - 40,
            height=60,
            text=message,
            font_size=20,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_CENTER
        )

        # Create OK button
        button_width = 120
        button_height = 40
        button_x = dialog_x + (dialog_width - button_width) // 2
        button_y = dialog_y + dialog_height - button_height - 20

        self._ok_button = Button(
            x=button_x,
            y=button_y,
            width=button_width,
            height=button_height,
            label="确定 (OK)",
            on_click=self._handle_close
        )

        logger.debug(f"Dialog created: '{title}'")

    def _handle_close(self):
        """Handle dialog close."""
        logger.debug(f"Dialog closed: '{self._title}'")
        self.visible = False
        if self._on_close:
            self._on_close()

    def show(self):
        """Show the dialog."""
        self.visible = True
        logger.debug(f"Dialog shown: '{self._title}'")

    def hide(self):
        """Hide the dialog."""
        self.visible = False
        logger.debug(f"Dialog hidden: '{self._title}'")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the dialog.

        Args:
            surface: Pygame surface to draw on
        """
        if not self.visible:
            return

        # Draw overlay
        self._overlay.draw(surface)

        # Draw dialog panel
        self._dialog_panel.draw(surface)

        # Draw title
        self._title_label.draw(surface)

        # Draw message
        self._message_label.draw(surface)

        # Draw OK button
        self._ok_button.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        if not self.visible:
            return False

        # Handle OK button
        if self._ok_button.handle_event(event):
            return True

        # Handle ESC key to close
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._handle_close()
                return True

        # Consume all events when dialog is visible (modal behavior)
        return True

    def update(self, dt: float):
        """
        Update dialog logic.

        Args:
            dt: Delta time in seconds
        """
        if not self.visible:
            return

        self._ok_button.update(dt)

    def set_message(self, message: str):
        """
        Update the dialog message.

        Args:
            message: New message text
        """
        self._message = message
        self._message_label.set_text(message)
        logger.debug(f"Dialog message updated: '{message}'")

    def set_title(self, title: str):
        """
        Update the dialog title.

        Args:
            title: New title text
        """
        self._title = title
        self._title_label.set_text(title)
        logger.debug(f"Dialog title updated: '{title}'")
