"""
数学工具函数模块

提供游戏中常用的数学计算函数，包括角度转换、向量运算、插值等。

遵循《开发规范》(docs/specifications/05_开发规范.md)
"""

import math
from typing import Tuple


def normalize_angle(angle: float) -> float:
    """
    将角度标准化到 [0, 360) 范围

    Args:
        angle: 输入角度（度）

    Returns:
        float: 标准化后的角度 [0, 360)

    Example:
        >>> normalize_angle(450)
        90.0
        >>> normalize_angle(-90)
        270.0
    """
    return angle % 360


def degrees_to_radians(degrees: float) -> float:
    """
    将角度转换为弧度

    Args:
        degrees: 角度值

    Returns:
        float: 弧度值

    Example:
        >>> degrees_to_radians(180)
        3.141592653589793
    """
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """
    将弧度转换为角度

    Args:
        radians: 弧度值

    Returns:
        float: 角度值

    Example:
        >>> radians_to_degrees(math.pi)
        180.0
    """
    return math.degrees(radians)


def rotate_point(
    x: float,
    y: float,
    angle: float,
    origin_x: float = 0,
    origin_y: float = 0
) -> Tuple[float, float]:
    """
    围绕指定原点旋转点

    Args:
        x: 点的x坐标
        y: 点的y坐标
        angle: 旋转角度（度，顺时针）
        origin_x: 旋转中心x坐标
        origin_y: 旋转中心y坐标

    Returns:
        Tuple[float, float]: 旋转后的坐标 (new_x, new_y)

    Example:
        >>> rotate_point(1, 0, 90)
        (0.0, 1.0)
    """
    # 转换为弧度
    rad = degrees_to_radians(angle)

    # 平移到原点
    translated_x = x - origin_x
    translated_y = y - origin_y

    # 旋转
    cos_angle = math.cos(rad)
    sin_angle = math.sin(rad)
    rotated_x = translated_x * cos_angle - translated_y * sin_angle
    rotated_y = translated_x * sin_angle + translated_y * cos_angle

    # 平移回原位置
    new_x = rotated_x + origin_x
    new_y = rotated_y + origin_y

    return (new_x, new_y)


def lerp(start: float, end: float, t: float) -> float:
    """
    线性插值

    Args:
        start: 起始值
        end: 结束值
        t: 插值参数 [0, 1]

    Returns:
        float: 插值结果

    Example:
        >>> lerp(0, 100, 0.5)
        50.0
        >>> lerp(0, 100, 0.25)
        25.0
    """
    return start + (end - start) * t


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    将值限制在指定范围内

    Args:
        value: 输入值
        min_value: 最小值
        max_value: 最大值

    Returns:
        float: 限制后的值

    Example:
        >>> clamp(150, 0, 100)
        100
        >>> clamp(-10, 0, 100)
        0
        >>> clamp(50, 0, 100)
        50
    """
    return max(min_value, min(value, max_value))


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    计算两点之间的欧几里得距离

    Args:
        x1: 第一个点的x坐标
        y1: 第一个点的y坐标
        x2: 第二个点的x坐标
        y2: 第二个点的y坐标

    Returns:
        float: 两点之间的距离

    Example:
        >>> distance(0, 0, 3, 4)
        5.0
    """
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def ease_in_out(t: float) -> float:
    """
    缓动函数：ease-in-out

    Args:
        t: 时间参数 [0, 1]

    Returns:
        float: 缓动后的值 [0, 1]

    Example:
        >>> ease_in_out(0.5)
        0.5
        >>> ease_in_out(0.25) < 0.25
        True
    """
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - 2 * (1 - t) * (1 - t)


def ease_in(t: float) -> float:
    """
    缓动函数：ease-in

    Args:
        t: 时间参数 [0, 1]

    Returns:
        float: 缓动后的值 [0, 1]

    Example:
        >>> ease_in(0.5)
        0.25
    """
    return t * t


def ease_out(t: float) -> float:
    """
    缓动函数：ease-out

    Args:
        t: 时间参数 [0, 1]

    Returns:
        float: 缓动后的值 [0, 1]

    Example:
        >>> ease_out(0.5)
        0.75
    """
    return 1 - (1 - t) * (1 - t)


def vector_add(
    v1: Tuple[float, float],
    v2: Tuple[float, float]
) -> Tuple[float, float]:
    """
    向量加法

    Args:
        v1: 第一个向量 (x, y)
        v2: 第二个向量 (x, y)

    Returns:
        Tuple[float, float]: 结果向量

    Example:
        >>> vector_add((1, 2), (3, 4))
        (4, 6)
    """
    return (v1[0] + v2[0], v1[1] + v2[1])


def vector_subtract(
    v1: Tuple[float, float],
    v2: Tuple[float, float]
) -> Tuple[float, float]:
    """
    向量减法

    Args:
        v1: 第一个向量 (x, y)
        v2: 第二个向量 (x, y)

    Returns:
        Tuple[float, float]: 结果向量

    Example:
        >>> vector_subtract((5, 7), (2, 3))
        (3, 4)
    """
    return (v1[0] - v2[0], v1[1] - v2[1])


def vector_scale(v: Tuple[float, float], scalar: float) -> Tuple[float, float]:
    """
    向量缩放

    Args:
        v: 向量 (x, y)
        scalar: 缩放因子

    Returns:
        Tuple[float, float]: 缩放后的向量

    Example:
        >>> vector_scale((3, 4), 2)
        (6, 8)
    """
    return (v[0] * scalar, v[1] * scalar)


def vector_length(v: Tuple[float, float]) -> float:
    """
    计算向量长度（模）

    Args:
        v: 向量 (x, y)

    Returns:
        float: 向量长度

    Example:
        >>> vector_length((3, 4))
        5.0
    """
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def vector_normalize(v: Tuple[float, float]) -> Tuple[float, float]:
    """
    向量归一化（单位化）

    Args:
        v: 向量 (x, y)

    Returns:
        Tuple[float, float]: 归一化后的向量

    Raises:
        ValueError: 零向量无法归一化

    Example:
        >>> vector_normalize((3, 4))
        (0.6, 0.8)
    """
    length = vector_length(v)
    if length == 0:
        raise ValueError("Cannot normalize zero vector")
    return (v[0] / length, v[1] / length)


def is_point_in_rect(
    px: float,
    py: float,
    rect_x: float,
    rect_y: float,
    rect_width: float,
    rect_height: float
) -> bool:
    """
    检查点是否在矩形内

    Args:
        px: 点的x坐标
        py: 点的y坐标
        rect_x: 矩形左上角x坐标
        rect_y: 矩形左上角y坐标
        rect_width: 矩形宽度
        rect_height: 矩形高度

    Returns:
        bool: 点是否在矩形内

    Example:
        >>> is_point_in_rect(5, 5, 0, 0, 10, 10)
        True
        >>> is_point_in_rect(15, 5, 0, 0, 10, 10)
        False
    """
    return (rect_x <= px <= rect_x + rect_width and
            rect_y <= py <= rect_y + rect_height)
