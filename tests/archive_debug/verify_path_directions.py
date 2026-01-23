"""
调试脚本：验证关卡生成的方向和旋转角度

路径：(0,0) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (3,3)
"""

# 定义方向
class PathDirection:
    NORTH = (-1, 0)  # 向上
    EAST = (0, 1)    # 向右
    SOUTH = (1, 0)   # 向下
    WEST = (0, -1)   # 向左

def get_direction(from_pos, to_pos):
    """获取从from_pos到to_pos的方向"""
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]

    if dx == -1 and dy == 0:
        return "NORTH"
    elif dx == 0 and dy == 1:
        return "EAST"
    elif dx == 1 and dy == 0:
        return "SOUTH"
    elif dx == 0 and dy == -1:
        return "WEST"
    else:
        return f"INVALID ({dx}, {dy})"

# 路径
path = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3)]

print("="*60)
print("路径分析")
print("="*60)

for i in range(1, len(path) - 1):
    prev_pos = path[i-1]
    curr_pos = path[i]
    next_pos = path[i+1]

    entry_dir = get_direction(prev_pos, curr_pos)
    exit_dir = get_direction(curr_pos, next_pos)

    print(f"\n元素{i}: 位置 {curr_pos}")
    print(f"  从 {prev_pos} 进入 → 方向: {entry_dir}")
    print(f"  到 {next_pos} 离开 → 方向: {exit_dir}")

    # 判断类型
    if entry_dir == exit_dir:
        tile_type = "直线（相同方向）"
    elif (entry_dir == "NORTH" and exit_dir == "SOUTH") or \
         (entry_dir == "SOUTH" and exit_dir == "NORTH") or \
         (entry_dir == "EAST" and exit_dir == "WEST") or \
         (entry_dir == "WEST" and exit_dir == "EAST"):
        tile_type = "直线（相反方向）"
    else:
        tile_type = "直角"

        # 确定旋转角度
        corner_map = {
            ("NORTH", "EAST"): 0,
            ("EAST", "NORTH"): 0,
            ("EAST", "SOUTH"): 90,
            ("SOUTH", "EAST"): 90,
            ("SOUTH", "WEST"): 180,
            ("WEST", "SOUTH"): 180,
            ("WEST", "NORTH"): 270,
            ("NORTH", "WEST"): 270
        }
        rotation = corner_map.get((entry_dir, exit_dir), "未知")
        print(f"  类型: {tile_type} → 旋转角度: {rotation}°")
        continue

    print(f"  类型: {tile_type}")
    if "EAST" in entry_dir or "WEST" in entry_dir or "EAST" in exit_dir or "WEST" in exit_dir:
        print(f"  → 水平直线 (0° 或 180°)")
    else:
        print(f"  → 竖直直线 (90° 或 270°)")

print("\n" + "="*60)
print("预期结果对比")
print("="*60)

expected = {
    1: ("直线", "0° 或 180°", "水平"),
    2: ("直角", "180°", "从水平向下转"),
    3: ("直线", "90° 或 270°", "竖直"),
    4: ("直线", "90° 或 270°", "竖直"),
    5: ("直角", "0°", "从竖直向右转")
}

for i, (tile_type, rotation, desc) in expected.items():
    print(f"\n元素{i}: {desc}")
    print(f"  预期: {tile_type} {rotation}")
