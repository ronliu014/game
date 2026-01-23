"""
验证修复后的旋转逻辑

路径：(0,0) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (3,3)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.level.level_generator_v2 import LevelGeneratorV2, PathDirection
from src.core.level.difficulty_config import DifficultyLevel

# 创建生成器
generator = LevelGeneratorV2(
    grid_size=4,
    difficulty=DifficultyLevel.EASY
)

# 测试路径
path = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3)]

print("="*80)
print("验证修复后的旋转逻辑")
print("="*80)

# 手动计算每个元素的旋转
for i in range(1, len(path) - 1):
    pos = path[i]
    prev_pos = path[i-1]
    next_pos = path[i+1]

    # 计算移动方向
    move_in = generator._get_direction(prev_pos, pos)
    move_out = generator._get_direction(pos, next_pos)

    # 转换为连接点方向
    entry_dir = generator._get_opposite_direction(move_in)
    exit_dir = generator._get_opposite_direction(move_out)

    print(f"\n元素{i}：位置{pos}")
    print(f"  电流移动：{move_in.name} → {move_out.name}")
    print(f"  Tile连接：{entry_dir.name} ↔ {exit_dir.name}")

    # 判断类型
    if entry_dir == exit_dir or generator._is_opposite(entry_dir, exit_dir):
        print(f"  类型：直线")
    else:
        rotation = generator._get_corner_rotation(entry_dir, exit_dir)
        print(f"  类型：拐角，旋转 {rotation}度")

        # 验证关键元素
        if i == 2:
            expected = 0
            status = "✓" if rotation == expected else "✗"
            print(f"  期望：{expected}度 {status}")
        elif i == 5:
            expected = 0
            status = "✓" if rotation == expected else "✗"
            print(f"  期望：{expected}度 {status}")

print("\n" + "="*80)
print("生成完整关卡测试")
print("="*80)

try:
    level_data = generator.generate()
    print(f"✓ 关卡生成成功")
    print(f"  网格大小：{level_data['grid_size']}")
    print(f"  路径长度：{len(level_data.get('path', []))}")

    # 检查元素2和元素5的旋转
    tiles = level_data['solution']['tiles']
    for tile in tiles:
        if tile['x'] == 2 and tile['y'] == 0 and tile['type'] == 'corner':
            print(f"\n元素2 (2,0)：")
            print(f"  类型：{tile['type']}")
            print(f"  旋转：{tile['rotation']}度")
            print(f"  期望：0度")
            print(f"  状态：{'✓ 正确' if tile['rotation'] == 0 else '✗ 错误'}")

        if tile['x'] == 2 and tile['y'] == 3 and tile['type'] == 'corner':
            print(f"\n元素5 (2,3)：")
            print(f"  类型：{tile['type']}")
            print(f"  旋转：{tile['rotation']}度")
            print(f"  期望：0度")
            print(f"  状态：{'✓ 正确' if tile['rotation'] == 0 else '✗ 错误'}")

except Exception as e:
    print(f"✗ 生成失败：{e}")
    import traceback
    traceback.print_exc()
