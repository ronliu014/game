"""
测试修复后的旋转逻辑

路径：(0,0) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (3,3)
"""

from enum import Enum

class PathDirection(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

def get_direction(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]

    for direction in PathDirection:
        if direction.value == (dx, dy):
            return direction
    return None

def get_opposite(direction):
    opposites = {
        PathDirection.NORTH: PathDirection.SOUTH,
        PathDirection.SOUTH: PathDirection.NORTH,
        PathDirection.EAST: PathDirection.WEST,
        PathDirection.WEST: PathDirection.EAST
    }
    return opposites[direction]

def get_corner_rotation_fixed(entry_dir, exit_dir):
    """修复后的逻辑"""
    conn_entry = get_opposite(entry_dir)
    conn_exit = get_opposite(exit_dir)

    corner_map = {
        (PathDirection.NORTH, PathDirection.EAST): 0,
        (PathDirection.EAST, PathDirection.NORTH): 0,
        (PathDirection.EAST, PathDirection.SOUTH): 90,
        (PathDirection.SOUTH, PathDirection.EAST): 90,
        (PathDirection.SOUTH, PathDirection.WEST): 180,
        (PathDirection.WEST, PathDirection.SOUTH): 180,
        (PathDirection.WEST, PathDirection.NORTH): 270,
        (PathDirection.NORTH, PathDirection.WEST): 270
    }

    return corner_map.get((conn_entry, conn_exit), -1)

# 测试路径
path = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3)]

print("="*80)
print("测试修复后的旋转逻辑")
print("="*80)

# 元素2
print("\n【元素2】位置 (2,0)")
print("路径段：(1,0) -> (2,0) -> (2,1)")
entry_dir = get_direction((1,0), (2,0))
exit_dir = get_direction((2,0), (2,1))
print(f"电流移动方向：{entry_dir.name} -> {exit_dir.name}")

conn_entry = get_opposite(entry_dir)
conn_exit = get_opposite(exit_dir)
print(f"Tile连接点：{conn_entry.name} 和 {conn_exit.name}")

rotation = get_corner_rotation_fixed(entry_dir, exit_dir)
print(f"计算结果：{rotation}度")
print(f"用户期望：180度")
print(f"匹配：{'YES' if rotation == 180 else 'NO'}")

# 元素5
print("\n【元素5】位置 (2,3)")
print("路径段：(2,2) -> (2,3) -> (3,3)")
entry_dir = get_direction((2,2), (2,3))
exit_dir = get_direction((2,3), (3,3))
print(f"电流移动方向：{entry_dir.name} -> {exit_dir.name}")

conn_entry = get_opposite(entry_dir)
conn_exit = get_opposite(exit_dir)
print(f"Tile连接点：{conn_entry.name} 和 {conn_exit.name}")

rotation = get_corner_rotation_fixed(entry_dir, exit_dir)
print(f"计算结果：{rotation}度")
print(f"用户期望：0度")
print(f"匹配：{'YES' if rotation == 0 else 'NO'}")

print("\n" + "="*80)
print("分析所有中间元素")
print("="*80)

for i in range(1, len(path) - 1):
    pos = path[i]
    prev_pos = path[i-1]
    next_pos = path[i+1]

    entry_dir = get_direction(prev_pos, pos)
    exit_dir = get_direction(pos, next_pos)

    print(f"\n元素{i}：位置{pos}")
    print(f"  电流：{entry_dir.name} -> {exit_dir.name}")

    if entry_dir == exit_dir or get_opposite(entry_dir) == exit_dir:
        print(f"  类型：直线")
    else:
        conn_entry = get_opposite(entry_dir)
        conn_exit = get_opposite(exit_dir)
        rotation = get_corner_rotation_fixed(entry_dir, exit_dir)
        print(f"  连接：{conn_entry.name} <-> {conn_exit.name}")
        print(f"  旋转：{rotation}度")
