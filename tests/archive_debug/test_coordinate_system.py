"""
测试坐标系理解

假设1：我的理解
- (x, y) = (row, col)
- x向下增加，y向右增加
- SOUTH = (1, 0) = row+1

假设2：用户可能的理解
- (x, y) = (col, row)
- x向右增加，y向下增加
- EAST = (1, 0) = col+1

路径：(0,0) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (3,3)
"""

print("="*80)
print("坐标系分析")
print("="*80)

path = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3)]

print("\n假设1：(x,y) = (row, col)，x向下，y向右")
print("-"*80)
for i in range(len(path)-1):
    curr = path[i]
    next_pos = path[i+1]
    dx = next_pos[0] - curr[0]
    dy = next_pos[1] - curr[1]

    if dx == 1 and dy == 0:
        direction = "向下(SOUTH)"
    elif dx == 0 and dy == 1:
        direction = "向右(EAST)"
    elif dx == -1 and dy == 0:
        direction = "向上(NORTH)"
    elif dx == 0 and dy == -1:
        direction = "向左(WEST)"
    else:
        direction = "未知"

    print(f"{curr} → {next_pos}: dx={dx}, dy={dy} → {direction}")

print("\n假设2：(x,y) = (col, row)，x向右，y向下")
print("-"*80)
print("如果用户理解为(x,y)=(col,row)，那么路径应该重新解释：")
for i in range(len(path)-1):
    curr = path[i]
    next_pos = path[i+1]
    # 重新解释：第一个数是col，第二个数是row
    curr_reinterpreted = (curr[1], curr[0])  # (col, row)
    next_reinterpreted = (next_pos[1], next_pos[0])

    dx = next_reinterpreted[0] - curr_reinterpreted[0]  # col变化
    dy = next_reinterpreted[1] - curr_reinterpreted[1]  # row变化

    if dx == 1 and dy == 0:
        direction = "向右(EAST)"
    elif dx == 0 and dy == 1:
        direction = "向下(SOUTH)"
    elif dx == -1 and dy == 0:
        direction = "向左(WEST)"
    elif dx == 0 and dy == -1:
        direction = "向上(NORTH)"
    else:
        direction = "未知"

    print(f"{curr}(col={curr[0]},row={curr[1]}) → {next_pos}(col={next_pos[0]},row={next_pos[1]}): "
          f"dx={dx}, dy={dy} → {direction}")

print("\n" + "="*80)
print("元素2分析")
print("="*80)

print("\n假设1：(x,y)=(row,col)")
print("  路径：(1,0) → (2,0) → (2,1)")
print("  (1,0)→(2,0): 向下(SOUTH)")
print("  (2,0)→(2,1): 向右(EAST)")
print("  描述：从竖直向下转向水平向右")
print("  entry=SOUTH, exit=EAST → 90度")

print("\n假设2：(x,y)=(col,row)")
print("  路径：(1,0) → (2,0) → (2,1)")
print("  重新解释：col=1,row=0 → col=2,row=0 → col=2,row=1")
print("  (col=1,row=0)→(col=2,row=0): 向右(EAST)")
print("  (col=2,row=0)→(col=2,row=1): 向下(SOUTH)")
print("  描述：从水平向右转向竖直向下")
print("  entry=EAST, exit=SOUTH → 90度")

print("\n用户描述：'从水平向下转'，期望180度")
print("这个描述更接近假设2的理解！")

print("\n" + "="*80)
print("重新计算：如果坐标理解为(col,row)")
print("="*80)

from enum import Enum

class PathDirection(Enum):
    NORTH = (0, -1)  # row-1, 向上
    EAST = (1, 0)    # col+1, 向右
    SOUTH = (0, 1)   # row+1, 向下
    WEST = (-1, 0)   # col-1, 向左

def get_direction_colrow(from_pos, to_pos):
    """假设pos=(col,row)"""
    # 第一个是col，第二个是row
    dcol = to_pos[0] - from_pos[0]
    drow = to_pos[1] - from_pos[1]

    for direction in PathDirection:
        if direction.value == (dcol, drow):
            return direction
    return None

print("\n元素2：(1,0) → (2,0) → (2,1)")
print("  解释为：(col=1,row=0) → (col=2,row=0) → (col=2,row=1)")
entry = get_direction_colrow((1,0), (2,0))
exit_dir = get_direction_colrow((2,0), (2,1))
print(f"  entry={entry.name if entry else 'None'}, exit={exit_dir.name if exit_dir else 'None'}")

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

if entry and exit_dir:
    rotation = corner_map.get((entry, exit_dir), -1)
    print(f"  计算结果：{rotation}度")
    print(f"  用户期望：180度")
    print(f"  匹配：{'YES' if rotation == 180 else 'NO'}")

print("\n元素5：(2,2) → (2,3) → (3,3)")
print("  解释为：(col=2,row=2) → (col=2,row=3) → (col=3,row=3)")
entry = get_direction_colrow((2,2), (2,3))
exit_dir = get_direction_colrow((2,3), (3,3))
print(f"  entry={entry.name if entry else 'None'}, exit={exit_dir.name if exit_dir else 'None'}")

if entry and exit_dir:
    rotation = corner_map.get((entry, exit_dir), -1)
    print(f"  计算结果：{rotation}度")
    print(f"  用户期望：0度")
    print(f"  匹配：{'YES' if rotation == 0 else 'NO'}")
