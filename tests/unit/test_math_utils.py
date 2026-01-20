"""
数学工具函数单元测试

测试math_utils模块的所有数学函数。
"""

import unittest
import math
from src.utils.math_utils import (
    normalize_angle,
    degrees_to_radians,
    radians_to_degrees,
    rotate_point,
    lerp,
    clamp,
    distance,
    ease_in_out,
    ease_in,
    ease_out,
    vector_add,
    vector_subtract,
    vector_scale,
    vector_length,
    vector_normalize,
    is_point_in_rect
)


class TestAngleFunctions(unittest.TestCase):
    """测试角度相关函数"""

    def test_normalize_angle(self):
        """测试角度标准化"""
        self.assertEqual(normalize_angle(0), 0)
        self.assertEqual(normalize_angle(360), 0)
        self.assertEqual(normalize_angle(450), 90)
        self.assertEqual(normalize_angle(-90), 270)
        self.assertEqual(normalize_angle(-360), 0)

    def test_degrees_to_radians(self):
        """测试角度转弧度"""
        self.assertAlmostEqual(degrees_to_radians(0), 0)
        self.assertAlmostEqual(degrees_to_radians(180), math.pi)
        self.assertAlmostEqual(degrees_to_radians(90), math.pi / 2)
        self.assertAlmostEqual(degrees_to_radians(360), 2 * math.pi)

    def test_radians_to_degrees(self):
        """测试弧度转角度"""
        self.assertAlmostEqual(radians_to_degrees(0), 0)
        self.assertAlmostEqual(radians_to_degrees(math.pi), 180)
        self.assertAlmostEqual(radians_to_degrees(math.pi / 2), 90)
        self.assertAlmostEqual(radians_to_degrees(2 * math.pi), 360)

    def test_rotate_point(self):
        """测试点旋转"""
        # 旋转90度
        x, y = rotate_point(1, 0, 90)
        self.assertAlmostEqual(x, 0, places=5)
        self.assertAlmostEqual(y, 1, places=5)

        # 旋转180度
        x, y = rotate_point(1, 0, 180)
        self.assertAlmostEqual(x, -1, places=5)
        self.assertAlmostEqual(y, 0, places=5)

        # 围绕非原点旋转
        x, y = rotate_point(2, 1, 90, origin_x=1, origin_y=1)
        self.assertAlmostEqual(x, 1, places=5)
        self.assertAlmostEqual(y, 2, places=5)


class TestInterpolationFunctions(unittest.TestCase):
    """测试插值函数"""

    def test_lerp(self):
        """测试线性插值"""
        self.assertEqual(lerp(0, 100, 0), 0)
        self.assertEqual(lerp(0, 100, 1), 100)
        self.assertEqual(lerp(0, 100, 0.5), 50)
        self.assertEqual(lerp(0, 100, 0.25), 25)
        self.assertEqual(lerp(10, 20, 0.5), 15)

    def test_clamp(self):
        """测试值限制"""
        self.assertEqual(clamp(50, 0, 100), 50)
        self.assertEqual(clamp(150, 0, 100), 100)
        self.assertEqual(clamp(-10, 0, 100), 0)
        self.assertEqual(clamp(0, 0, 100), 0)
        self.assertEqual(clamp(100, 0, 100), 100)


class TestDistanceFunction(unittest.TestCase):
    """测试距离计算"""

    def test_distance(self):
        """测试欧几里得距离"""
        self.assertEqual(distance(0, 0, 0, 0), 0)
        self.assertEqual(distance(0, 0, 3, 4), 5)
        self.assertEqual(distance(1, 1, 4, 5), 5)
        self.assertAlmostEqual(distance(0, 0, 1, 1), math.sqrt(2))


class TestEasingFunctions(unittest.TestCase):
    """测试缓动函数"""

    def test_ease_in_out(self):
        """测试ease-in-out"""
        self.assertEqual(ease_in_out(0), 0)
        self.assertEqual(ease_in_out(1), 1)
        self.assertEqual(ease_in_out(0.5), 0.5)
        # 前半段应该小于线性
        self.assertLess(ease_in_out(0.25), 0.25)
        # 后半段应该大于线性
        self.assertGreater(ease_in_out(0.75), 0.75)

    def test_ease_in(self):
        """测试ease-in"""
        self.assertEqual(ease_in(0), 0)
        self.assertEqual(ease_in(1), 1)
        self.assertEqual(ease_in(0.5), 0.25)

    def test_ease_out(self):
        """测试ease-out"""
        self.assertEqual(ease_out(0), 0)
        self.assertEqual(ease_out(1), 1)
        self.assertEqual(ease_out(0.5), 0.75)


class TestVectorFunctions(unittest.TestCase):
    """测试向量运算"""

    def test_vector_add(self):
        """测试向量加法"""
        self.assertEqual(vector_add((1, 2), (3, 4)), (4, 6))
        self.assertEqual(vector_add((0, 0), (5, 5)), (5, 5))
        self.assertEqual(vector_add((-1, -2), (1, 2)), (0, 0))

    def test_vector_subtract(self):
        """测试向量减法"""
        self.assertEqual(vector_subtract((5, 7), (2, 3)), (3, 4))
        self.assertEqual(vector_subtract((5, 5), (5, 5)), (0, 0))
        self.assertEqual(vector_subtract((0, 0), (1, 1)), (-1, -1))

    def test_vector_scale(self):
        """测试向量缩放"""
        self.assertEqual(vector_scale((3, 4), 2), (6, 8))
        self.assertEqual(vector_scale((3, 4), 0), (0, 0))
        self.assertEqual(vector_scale((3, 4), -1), (-3, -4))

    def test_vector_length(self):
        """测试向量长度"""
        self.assertEqual(vector_length((0, 0)), 0)
        self.assertEqual(vector_length((3, 4)), 5)
        self.assertAlmostEqual(vector_length((1, 1)), math.sqrt(2))

    def test_vector_normalize(self):
        """测试向量归一化"""
        # 标准向量
        x, y = vector_normalize((3, 4))
        self.assertAlmostEqual(x, 0.6)
        self.assertAlmostEqual(y, 0.8)
        self.assertAlmostEqual(vector_length((x, y)), 1.0)

        # 零向量应该抛出异常
        with self.assertRaises(ValueError):
            vector_normalize((0, 0))


class TestGeometryFunctions(unittest.TestCase):
    """测试几何函数"""

    def test_is_point_in_rect(self):
        """测试点是否在矩形内"""
        # 点在矩形内
        self.assertTrue(is_point_in_rect(5, 5, 0, 0, 10, 10))
        # 点在边界上
        self.assertTrue(is_point_in_rect(0, 0, 0, 0, 10, 10))
        self.assertTrue(is_point_in_rect(10, 10, 0, 0, 10, 10))
        # 点在矩形外
        self.assertFalse(is_point_in_rect(15, 5, 0, 0, 10, 10))
        self.assertFalse(is_point_in_rect(-1, 5, 0, 0, 10, 10))


if __name__ == '__main__':
    unittest.main()
