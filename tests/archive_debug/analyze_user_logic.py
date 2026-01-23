"""
按照用户的逻辑重新分析

用户的理解：
- cur_grid.y == last_grid.y：当前和前一个在同一列（y相同）→ 竖直方向
- cur_grid.x == last_grid.x：当前和下一个在同一行（x相同）→ 水平方向

路径：(0,0) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (3,3)
"""

path = [(0,0), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3)]

print("="*80)
print("按照用户逻辑分析路径")
print("="*80)
print("\n关键理解：")
print("- (x, y) 中，x 是行号，y 是列号")
print("- 同一列（y相同）→ 竖直方向")
print("- 同一行（x相同）→ 水平方向")
print()

for i in range(1, len(path) - 1):
    last_grid = path[i-1]
    cur_grid = path[i]
    next_grid = path[i+1]

    print(f"\n元素{i}：位置 {cur_grid}")
    print(f"  路径段：{last_grid} → {cur_grid} → {next_grid}")

    # 分析进入方向
    if cur_grid[1] == last_grid[1]:  # y相同，同一列
        print(f"  进入：cur.y({cur_grid[1]}) == last.y({last_grid[1]}) → 竖直方向")
        if cur_grid[0] > last_grid[0]:
            entry_desc = "从上方进入（向下）"
        else:
            entry_desc = "从下方进入（向上）"
    elif cur_grid[0] == last_grid[0]:  # x相同，同一行
        print(f"  进入：cur.x({cur_grid[0]}) == last.x({last_grid[0]}) → 水平方向")
        if cur_grid[1] > last_grid[1]:
            entry_desc = "从左方进入（向右）"
        else:
            entry_desc = "从右方进入（向左）"
    else:
        entry_desc = "未知"

    # 分析离开方向
    if cur_grid[1] == next_grid[1]:  # y相同，同一列
        print(f"  离开：cur.y({cur_grid[1]}) == next.y({next_grid[1]}) → 竖直方向")
        if next_grid[0] > cur_grid[0]:
            exit_desc = "向下离开"
        else:
            exit_desc = "向上离开"
    elif cur_grid[0] == next_grid[0]:  # x相同，同一行
        print(f"  离开：cur.x({cur_grid[0]}) == next.x({next_grid[0]}) → 水平方向")
        if next_grid[1] > cur_grid[1]:
            exit_desc = "向右离开"
        else:
            exit_desc = "向左离开"
    else:
        exit_desc = "未知"

    print(f"  {entry_desc} + {exit_desc}")

    # 判断类型
    entry_vertical = (cur_grid[1] == last_grid[1])
    exit_vertical = (cur_grid[1] == next_grid[1])
    entry_horizontal = (cur_grid[0] == last_grid[0])
    exit_horizontal = (cur_grid[0] == next_grid[0])

    if (entry_vertical and exit_vertical) or (entry_horizontal and exit_horizontal):
        print(f"  类型：直线")
        if entry_vertical:
            print(f"  → 竖直直线，应该是 90° 或 270°")
        else:
            print(f"  → 水平直线，应该是 0° 或 180°")
    else:
        print(f"  类型：拐角")

        # 用户的期望
        if i == 1:
            print(f"  用户期望：90° (竖直直线)")
        elif i == 2:
            print(f"  用户期望：180° (拐角)")
        elif i == 5:
            print(f"  用户期望：0° (拐角)")

print("\n" + "="*80)
print("关键发现")
print("="*80)
print("""
元素1 (1,0)：
  - 进入：竖直（从上方）
  - 离开：竖直（向下）
  - 类型：竖直直线
  - 应该：90° 或 270°
  - 但 level_001.json 中是：90° ✓

元素2 (2,0)：
  - 进入：竖直（从上方）
  - 离开：水平（向右）
  - 类型：拐角（从竖直转向水平）
  - 用户期望：180°

元素5 (2,3)：
  - 进入：水平（从左方）
  - 离开：竖直（向下）
  - 类型：拐角（从水平转向竖直）
  - 用户期望：0°

现在的问题是：
1. 直线tile的0度是水平还是竖直？
2. 拐角tile的旋转定义是什么？

让我检查 level_001.json 中的实际配置...
""")

# 读取 level_001.json
import json
with open('E:/projects/my_app/game/data/levels/level_001.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n" + "="*80)
print("level_001.json 中的实际配置")
print("="*80)

tiles = data['solution']['tiles']
for i in range(1, len(path) - 1):
    pos = path[i]
    tile = next((t for t in tiles if t['x'] == pos[0] and t['y'] == pos[1]), None)
    if tile:
        print(f"\n元素{i} ({pos[0]},{pos[1]}):")
        print(f"  类型：{tile['type']}")
        print(f"  旋转：{tile['rotation']}°")
        if 'accepted_rotations' in tile:
            print(f"  可接受：{tile['accepted_rotations']}")
