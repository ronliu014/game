"""
Loading Scene

Provides a loading screen with progress indication.

Author: Circuit Repair Game Team
Date: 2026-01-23
"""

from typing import Optional, Dict, Any, List, Callable
import pygame
from src.scenes.scene_base import SceneBase
from src.ui.components.panel import Panel
from src.ui.components.label import Label
from src.ui.components.progress_bar import ProgressBar
from src.ui.layouts.layout_manager import LayoutManager
from src.ui.resource_preloader import ResourcePreloader
from src.utils.logger import GameLogger

logger = GameLogger.get_logger(__name__)


class LoadingScene(SceneBase):
    """
    Loading scene with progress bar.

    Displays loading progress while resources are being loaded.

    Features:
        - Loading message
        - Progress bar with percentage
        - Asynchronous resource loading
        - Automatic transition when complete

    Example:
        >>> scene = LoadingScene(scene_manager)
        >>> scene.on_enter(data={
        ...     'next_scene': GameplayScene,
        ...     'resources': ['image1', 'sound1']
        ... })
    """

    def __init__(self, scene_manager=None):
        """
        Initialize the loading scene.

        Args:
            scene_manager: Reference to the scene manager
        """
        super().__init__(scene_manager)

        # Screen dimensions
        self._screen_width = 800
        self._screen_height = 600

        # UI components
        self._background_panel: Optional[Panel] = None
        self._title_label: Optional[Label] = None
        self._status_label: Optional[Label] = None
        self._progress_bar: Optional[ProgressBar] = None

        # Layout manager
        self._layout: Optional[LayoutManager] = None

        # Loading state
        self._resource_preloader: Optional[ResourcePreloader] = None
        self._loading_complete = False
        self._loading_started = False
        self._next_scene_class = None
        self._next_scene_data: Dict[str, Any] = {}
        self._loading_tasks: List[Callable] = []
        self._current_task_index = 0
        self._min_display_time = 1000.0  # Minimum time to show loading screen (ms)
        self._elapsed_time = 0.0

        logger.debug("LoadingScene initialized")

    def on_enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called when the scene becomes active.

        Args:
            data: Optional data containing:
                - next_scene: Scene class to transition to after loading
                - next_scene_data: Data to pass to next scene
                - resources: List of resources to load
                - loading_tasks: List of custom loading tasks
                - min_display_time: Minimum time to display loading screen (ms)
        """
        super().on_enter(data)

        # Get screen dimensions
        self._screen_width = self.get_transition_data('screen_width', 800)
        self._screen_height = self.get_transition_data('screen_height', 600)

        # Get loading configuration
        self._next_scene_class = self.get_transition_data('next_scene')
        self._next_scene_data = self.get_transition_data('next_scene_data', {})
        self._loading_tasks = self.get_transition_data('loading_tasks', [])
        self._min_display_time = self.get_transition_data('min_display_time', 1000.0)

        # Initialize layout manager
        self._layout = LayoutManager(self._screen_width, self._screen_height)

        # Create UI components
        self._create_ui()

        # Initialize resource preloader
        self._resource_preloader = ResourcePreloader()
        resources = self.get_transition_data('resources', [])
        for resource in resources:
            # Assume resources are dictionaries with 'type', 'name', 'path'
            if isinstance(resource, dict):
                res_type = resource.get('type', 'image')
                res_name = resource.get('name')
                res_path = resource.get('path')

                if res_type == 'image':
                    self._resource_preloader.add_image(res_name, res_path)
                elif res_type == 'sound':
                    self._resource_preloader.add_sound(res_name, res_path)
                elif res_type == 'music':
                    self._resource_preloader.add_music(res_name, res_path)
                elif res_type == 'font':
                    size = resource.get('size', 20)
                    self._resource_preloader.add_font(res_name, res_path, size)

        logger.info("LoadingScene entered")

    def on_exit(self) -> None:
        """Called when the scene is being replaced or removed."""
        super().on_exit()
        logger.info("LoadingScene exited")

    def update(self, delta_ms: float) -> None:
        """
        Update scene logic.

        Args:
            delta_ms: Time elapsed since last update in milliseconds
        """
        self._elapsed_time += delta_ms

        # Start loading on first update
        if not self._loading_started:
            self._start_loading()
            self._loading_started = True

        # Update progress bar animation
        if self._progress_bar:
            self._progress_bar.update(delta_ms)

        # Check if loading is complete and minimum display time has elapsed
        if self._loading_complete and self._elapsed_time >= self._min_display_time:
            self._transition_to_next_scene()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the scene.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw background
        if self._background_panel:
            self._background_panel.draw(surface)

        # Draw title
        if self._title_label:
            self._title_label.draw(surface)

        # Draw status
        if self._status_label:
            self._status_label.draw(surface)

        # Draw progress bar
        if self._progress_bar:
            self._progress_bar.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.

        Args:
            event: Pygame event to handle

        Returns:
            bool: True if the event was handled, False otherwise
        """
        # Loading scene doesn't handle events (non-interactive)
        return False

    def _create_ui(self) -> None:
        """Create UI components."""
        # Create background
        self._background_panel = Panel(
            0, 0,
            self._screen_width,
            self._screen_height,
            background_color=(20, 20, 30),
            alpha=255
        )

        # Create title label
        self._title_label = Label(
            0, 0,
            self._screen_width,
            80,
            "加载中...",
            font_size=36,
            text_color=(200, 200, 200),
            alignment=Label.ALIGN_CENTER
        )
        self._layout.center_component(
            self._title_label,
            horizontal=True,
            vertical=False,
            offset_y=-100
        )

        # Create status label
        self._status_label = Label(
            0, 0,
            self._screen_width,
            40,
            "正在加载资源...",
            font_size=20,
            text_color=(150, 150, 150),
            alignment=Label.ALIGN_CENTER
        )
        self._layout.center_component(
            self._status_label,
            horizontal=True,
            vertical=False,
            offset_y=-20
        )

        # Create progress bar
        self._progress_bar = ProgressBar(
            0, 0,
            400, 30,
            bar_color=(100, 200, 100),
            background_color=(50, 50, 50),
            border_color=(150, 150, 150),
            border_width=2,
            show_percentage=True,
            animation_speed=0.5  # Slower animation for smooth effect
        )
        self._layout.center_component(
            self._progress_bar,
            horizontal=True,
            vertical=True,
            offset_y=50
        )

    def _start_loading(self) -> None:
        """Start the loading process."""
        logger.info("Starting loading process")

        # Load resources if any
        if self._resource_preloader and self._resource_preloader.get_total_count() > 0:
            self._resource_preloader.load_all(progress_callback=self._on_loading_progress)
        else:
            # No resources to load, just execute tasks
            self._execute_loading_tasks()

    def _execute_loading_tasks(self) -> None:
        """Execute custom loading tasks."""
        if not self._loading_tasks:
            self._loading_complete = True
            return

        try:
            for i, task in enumerate(self._loading_tasks):
                # Update progress
                progress = (i + 1) / len(self._loading_tasks)
                self._on_loading_progress(progress)

                # Execute task
                if callable(task):
                    task()

            self._loading_complete = True
            logger.info("All loading tasks completed")

        except Exception as e:
            logger.error(f"Error during loading: {e}")
            self._loading_complete = True

    def _on_loading_progress(self, progress: float) -> None:
        """
        Handle loading progress update.

        Args:
            progress: Progress value (0.0 to 1.0)
        """
        if self._progress_bar:
            self._progress_bar.set_progress(progress)

        # Update status text
        if self._status_label:
            percentage = int(progress * 100)
            self._status_label.set_text(f"正在加载资源... {percentage}%")

        # Check if loading is complete
        if progress >= 1.0:
            if not self._loading_tasks:
                self._loading_complete = True
                if self._status_label:
                    self._status_label.set_text("加载完成！")
                logger.info("Resource loading completed")
            else:
                # Execute additional loading tasks
                self._execute_loading_tasks()

    def _transition_to_next_scene(self) -> None:
        """Transition to the next scene."""
        if self._next_scene_class:
            logger.info(f"Transitioning to {self._next_scene_class.__name__}")

            # Pass loaded resources to next scene
            if self._resource_preloader:
                self._next_scene_data['resource_preloader'] = self._resource_preloader

            # Transition to next scene
            self.request_scene_change(
                self._next_scene_class,
                data=self._next_scene_data,
                replace=True
            )
        else:
            logger.warning("No next scene specified, staying on loading screen")

    def set_status_text(self, text: str) -> None:
        """
        Set the status text.

        Args:
            text: Status text to display
        """
        if self._status_label:
            self._status_label.set_text(text)

    def get_resource_preloader(self) -> Optional[ResourcePreloader]:
        """
        Get the resource preloader.

        Returns:
            ResourcePreloader: The resource preloader instance
        """
        return self._resource_preloader
