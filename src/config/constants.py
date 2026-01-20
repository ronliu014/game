"""
游戏常量定义

定义游戏中使用的所有常量，包括窗口设置、颜色、尺寸等。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

from enum import Enum
from typing import Tuple


# ============================================================================
# 窗口设置
# ============================================================================

WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
WINDOW_TITLE: str = "电路板修复游戏 - Circuit Repair Game"
FPS: int = 60


# ============================================================================
# 网格设置
# ============================================================================

GRID_SIZE_MIN: int = 3
GRID_SIZE_MAX: int = 8
GRID_SIZE_DEFAULT: int = 4

TILE_SIZE: int = 128  # 瓦片尺寸（像素）
TILE_PADDING: int = 4  # 瓦片间距（像素）


# ============================================================================
# 颜色定义（RGB格式）
# ============================================================================

# 蒸汽朋克主题色（铜/黄铜色调）
COLOR_COPPER: Tuple[int, int, int] = (184, 115, 51)  # #B87333
COLOR_BRASS: Tuple[int, int, int] = (205, 127, 50)   # #CD7F32
COLOR_BRONZE: Tuple[int, int, int] = (139, 69, 19)   # #8B4513

# 基础颜色
COLOR_WHITE: Tuple[int, int, int] = (255, 255, 255)
COLOR_BLACK: Tuple[int, int, int] = (0, 0, 0)
COLOR_GRAY: Tuple[int, int, int] = (128, 128, 128)
COLOR_DARK_GRAY: Tuple[int, int, int] = (64, 64, 64)
COLOR_LIGHT_GRAY: Tuple[int, int, int] = (192, 192, 192)

# 游戏状态颜色
COLOR_POWER_ON: Tuple[int, int, int] = (255, 215, 0)    # 金色（通电）
COLOR_POWER_OFF: Tuple[int, int, int] = (100, 100, 100)  # 灰色（断电）
COLOR_CLICKABLE: Tuple[int, int, int] = (50, 50, 50)     # 深灰（可点击）
COLOR_TERMINAL_GLOW: Tuple[int, int, int] = (0, 255, 255)  # 青色（终端发光）

# UI颜色
COLOR_BUTTON_NORMAL: Tuple[int, int, int] = (100, 100, 100)
COLOR_BUTTON_HOVER: Tuple[int, int, int] = (150, 150, 150)
COLOR_BUTTON_PRESSED: Tuple[int, int, int] = (80, 80, 80)
COLOR_TEXT: Tuple[int, int, int] = (255, 255, 255)
COLOR_BACKGROUND: Tuple[int, int, int] = (30, 30, 30)


# ============================================================================
# 动画设置
# ============================================================================

ROTATION_DURATION_MS: int = 300  # 旋转动画时长（毫秒）
GLOW_DURATION_MS: int = 500      # 发光动画时长（毫秒）
PARTICLE_LIFETIME_MS: int = 1000  # 粒子生命周期（毫秒）

# 缓动函数类型
class EasingType(Enum):
    """缓动函数类型"""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"


# ============================================================================
# 音频设置
# ============================================================================

AUDIO_VOLUME_DEFAULT: float = 0.7  # 默认音量（0.0-1.0）
AUDIO_BGM_VOLUME: float = 0.2      # BGM音量（游戏UI激活时）
AUDIO_SFX_VOLUME: float = 1.0      # 音效音量

# 音频文件路径
AUDIO_PATH_CLICK: str = "assets/audio/sfx/click.wav"
AUDIO_PATH_ROTATE: str = "assets/audio/sfx/rotate.wav"
AUDIO_PATH_CONNECT: str = "assets/audio/sfx/connect.wav"
AUDIO_PATH_VICTORY: str = "assets/audio/sfx/victory.wav"
AUDIO_PATH_BGM: str = "assets/audio/bgm/game_theme.ogg"


# ============================================================================
# 资源路径
# ============================================================================

# 精灵图路径
SPRITE_PATH_POWER_SOURCE: str = "assets/sprites/tiles/power_source.png"
SPRITE_PATH_TERMINAL_OFF: str = "assets/sprites/tiles/terminal_off.png"
SPRITE_PATH_TERMINAL_ON: str = "assets/sprites/tiles/terminal_on.png"
SPRITE_PATH_LINE: str = "assets/sprites/tiles/line.png"
SPRITE_PATH_CORNER: str = "assets/sprites/tiles/corner.png"
SPRITE_PATH_TILE_BG: str = "assets/sprites/tiles/tile_bg.png"

# UI元素路径
SPRITE_PATH_BUTTON_EXIT: str = "assets/sprites/ui/btn_exit.png"
SPRITE_PATH_VICTORY_BANNER: str = "assets/sprites/ui/victory_banner.png"

# 特效路径
SPRITE_PATH_GLOW: str = "assets/sprites/effects/glow.png"

# 字体路径
FONT_PATH_DEFAULT: str = "assets/fonts/default.ttf"


# ============================================================================
# 游戏逻辑常量
# ============================================================================

# 旋转角度
ROTATION_ANGLES: Tuple[int, ...] = (0, 90, 180, 270)
ROTATION_STEP: int = 90  # 每次旋转的角度

# 方向定义
class Direction(Enum):
    """方向枚举"""
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


# 方向向量（用于坐标计算）
DIRECTION_VECTORS: dict = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}


# ============================================================================
# 性能设置
# ============================================================================

# 性能目标
TARGET_FPS: int = 60
TARGET_STARTUP_TIME_MS: int = 2000  # 启动时间目标（毫秒）
TARGET_LEVEL_LOAD_TIME_MS: int = 500  # 关卡加载时间目标（毫秒）
TARGET_MEMORY_MB: int = 100  # 内存占用目标（MB）

# 性能监控
PERFORMANCE_LOG_INTERVAL_MS: int = 1000  # 性能日志记录间隔（毫秒）


# ============================================================================
# 调试设置
# ============================================================================

DEBUG_MODE: bool = False  # 调试模式开关
DEBUG_SHOW_FPS: bool = True  # 显示FPS
DEBUG_SHOW_GRID: bool = False  # 显示网格线
DEBUG_SHOW_HITBOX: bool = False  # 显示碰撞框


# ============================================================================
# 版本信息
# ============================================================================

VERSION: str = "0.1.0-alpha"
VERSION_MAJOR: int = 0
VERSION_MINOR: int = 1
VERSION_PATCH: int = 0
VERSION_STAGE: str = "alpha"
