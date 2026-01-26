# 关卡生成算法 V3 - 完整实现说明

## 📋 概述

本文档详细说明了 `level_generator_v3.py` 如何完整实现用户提出的关卡生成算法。

**版本**: 3.0
**日期**: 2026-01-23
**状态**: ✅ 已实现并验证

---

## 🎯 算法核心思路

### 用户的算法规范

1. **选择起点和终点** - 在 N×N 格子中随机选择电源和终端位置
2. **路径查找** - 使用 DFS 算法找到一条连通路径（不要求最短）
3. **精灵定义** - 明确定义直线和拐角精灵的旋转角度含义
4. **瓷砖配置** - 根据前一个、当前、下一个格子的相对位置确定精灵类型和旋转
5. **保存正确配置** - 记录每个瓷砖的正确旋转角度
6. **打乱瓷砖** - 随机旋转部分瓷砖作为初始状态
7. **难度控制** - 通过可移动元素数量和打乱比例控制难度

---

## 🔧 实现细节

### 1. 精灵旋转定义

#### 直线精灵 (`tile_straight.png`)

```
0° (或 180°):  ─  水平直线（左↔右）
90° (或 270°): │  竖直直线（上↔下）
```

**等价性**:
- 0° 和 180° 等价（都是水平线）
- 90° 和 270° 等价（都是竖直线）

#### 拐角精灵 (`tile_corner.png`)

```
0°:   └  连接上和右（从上转右）
90°:  ┌  连接右和下（从右转下）
180°: ┐  连接下和左（从下转左）
270°: ┘  连接左和上（从左转上）
```

**方向性**: 拐角是双向的，可以从任一方向进入

---

### 2. 核心算法实现

#### 步骤 1: 选择端点

```python
def _select_endpoints(self):
    """选择电源和终端位置，确保曼哈顿距离 >= 2"""
    while True:
        power_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        terminal_pos = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))

        distance = abs(power_x - terminal_x) + abs(power_y - terminal_y)
        if distance >= 2:  # 至少需要1个中间瓷砖
            return power_pos, terminal_pos
```

#### 步骤 2: DFS 路径查找

```python
def _find_path(self, start, end):
    """使用 DFS 找到一条路径（不要求最短）"""
    visited = set()
    path = []

    def dfs(pos):
        if pos == end:
            path.append(pos)
            return True

        visited.add(pos)
        path.append(pos)

        # 随机尝试四个方向
        for direction in random.shuffle([UP, DOWN, LEFT, RIGHT]):
            next_pos = pos + direction
            if is_valid(next_pos) and next_pos not in visited:
                if dfs(next_pos):
                    return True

        path.pop()  # 回溯
        return False

    return path if dfs(start) else None
```

#### 步骤 3: 瓷砖配置逻辑

这是算法的核心部分，完全按照用户的伪代码实现：

```python
def _determine_tile_config(self, prev_pos, cur_pos, next_pos):
    """
    根据前一个、当前、下一个格子的相对位置确定瓷砖配置

    返回: (tile_type, rotation, accepted_rotations)
    """
    prev_x, prev_y = prev_pos
    cur_x, cur_y = cur_pos
    next_x, next_y = next_pos

    # 情况 1: 前一个格子在当前格子的正上方 (cur_y > prev_y)
    if cur_x == prev_x and cur_y > prev_y:
        if cur_x < next_x and cur_y == next_y:
            # 下一个在正右方 → 0° 拐角（上→右）
            return 'corner', 0, [0]
        elif cur_x == next_x and cur_y < next_y:
            # 下一个在正下方 → 90°/270° 直线（上↔下）
            return 'straight', 90, [90, 270]
        elif cur_x > next_x and cur_y == next_y:
            # 下一���在正左方 → 270° 拐角（上→左）
            return 'corner', 270, [270]

    # 情况 2: 前一个格子在当前格子的正右方 (cur_x > prev_x)
    elif cur_x > prev_x and cur_y == prev_y:
        if cur_x == next_x and cur_y < next_y:
            # 下一个在正下方 → 90° 拐角（右→下）
            return 'corner', 90, [90]
        elif cur_x > next_x and cur_y == next_y:
            # 下一个在正左方 → 0°/180° 直线（右↔左）
            return 'straight', 0, [0, 180]
        elif cur_x == next_x and cur_y > next_y:
            # 下一个在正上方 → 0° 拐角（右→上）
            return 'corner', 0, [0]

    # 情况 3: 前一个格子在当前格子的正下方 (cur_y < prev_y)
    elif cur_x == prev_x and cur_y < prev_y:
        if cur_x > next_x and cur_y == next_y:
            # 下一个在正左方 → 180° 拐角（下→左）
            return 'corner', 180, [180]
        elif cur_x == next_x and cur_y > next_y:
            # 下一个在正上方 → 90°/270° 直线（下↔上）
            return 'straight', 90, [90, 270]
        elif cur_x < next_x and cur_y == next_y:
            # 下一个在正右方 → 90° 拐角（下→右）
            return 'corner', 90, [90]

    # 情况 4: 前一个格子在当前格子的正左方 (cur_x < prev_x)
    elif cur_x < prev_x and cur_y == prev_y:
        if cur_x == next_x and cur_y > next_y:
            # 下一个在正上方 → 270° 拐角（左→上）
            return 'corner', 270, [270]
        elif cur_x < next_x and cur_y == next_y:
            # 下一个在正右方 → 0°/180° 直线（左↔右）
            return 'straight', 0, [0, 180]
        elif cur_x == next_x and cur_y < next_y:
            # 下一个在正下方 → 180° 拐角（左→下）
            return 'corner', 180, [180]

    else:
        # 不应该出现的情况（斜线或重叠）
        raise ValueError("Invalid path geometry")
```

#### 步骤 4: 打乱瓷砖

```python
def _create_scrambled_state(self, solution_tiles, movable_count):
    """
    创建打乱的初始状态

    确保至少 scramble_ratio 比例的瓷砖需要旋转
    """
    # 计算需要打乱的瓷砖数量
    min_scrambled = int(movable_count * self.config.scramble_ratio)

    # 随机选择要打乱的瓷砖
    movable_indices = [i for i, t in enumerate(solution_tiles) if t['is_clickable']]
    scramble_indices = random.sample(movable_indices, min_scrambled)

    scrambled = []
    for i, tile in enumerate(solution_tiles):
        if i in scramble_indices:
            # 选择一个错误的旋转角度
            accepted = tile['accepted_rotations']
            invalid_rotations = [r for r in [0, 90, 180, 270] if r not in accepted]
            tile['rotation'] = random.choice(invalid_rotations)

        scrambled.append(tile)

    return scrambled
```

---

## 📊 难度配置

### 难度参数

| 难度 | 网格大小 | 可移动瓷砖 | 打乱比例 | 拐角数量 |
|------|---------|-----------|---------|---------|
| 简单 | 4-5 | 3-8 | 70% | 1-6 |
| 普通 | 5-6 | 4-10 | 80% | 2-8 |
| 困难 | 6-7 | 5-12 | 90% | 3-10 |
| 地狱 | 7-8 | 6-15 | 100% | 4-12 |

### 验证逻辑

```python
def _validate_difficulty(self, movable_count, corner_count):
    """验证关卡是否符合难度要求"""
    # 检查可移动瓷砖数量
    if not (min_movable <= movable_count <= max_movable):
        return False

    # 检查拐角数量
    if not (min_corners <= corner_count <= max_corners):
        return False

    return True
```

---

## 🧪 测试验证

### 测试脚本

运行 `tests/integration/test_algorithm_verification.py` 来验证算法：

```bash
python tests/integration/test_algorithm_verification.py
```

### 测试内容

1. **路径生成测试** - 验证 DFS 能找到有效路径
2. **瓷砖配置测试** - 验证每个瓷砖的类型和旋转是否正确
3. **难度验证测试** - 验证生成的关卡符合难度要求
4. **打乱逻辑测试** - 验证打乱比例符合配置

### 可视化输出

测试脚本会输出关卡的可视化表示：

```
关卡可视化 (Level Visualization)
============================================================
网格大小: 5x5
路径长度: 7

图例 (Legend):
  P = 电源 (Power Source)
  T = 终端 (Terminal)
  ─ = 水平直线 (Horizontal Straight)
  │ = 竖直直线 (Vertical Straight)
  └ = 0° 拐角 (上→右)
  ┌ = 90° 拐角 (右→下)
  ┐ = 180° 拐角 (下→左)
  ┘ = 270° 拐角 (左→上)
  . = 空格子 (Empty)

    0  1  2  3  4
 0  .  .  .  .  .
 1  P  ─  ┐  .  .
 2  .  .  │  .  .
 3  .  .  └  ─  T
 4  .  .  .  .  .
```

---

## ✅ 实现完成度

### 已实现的功能

- ✅ **端点选择** - 随机选择电源和终端，确保距离 >= 2
- ✅ **DFS 路径查找** - 找到一条有效路径（不要求最短）
- ✅ **精灵旋转定义** - 完全按照用户规范定义
- ✅ **瓷砖配置逻辑** - 完整实现用户的伪代码
- ✅ **正确配置保存** - 记录 `accepted_rotations`
- ✅ **打乱逻辑** - 根据难度打乱指定比例的瓷砖
- ✅ **难度控制** - 四种难度级别，可配置参数
- ✅ **验证机制** - 确保生成的关卡符合要求

### 与用户算法的对应关系

| 用户算法步骤 | V3 实现方法 | 状态 |
|-------------|------------|------|
| 1. 选择起点终点 | `_select_endpoints()` | ✅ |
| 2. BFS/DFS 路径查找 | `_find_path()` | ✅ |
| 3. 精灵旋转定义 | 文档注释 + 代码实现 | ✅ |
| 4. 瓷砖配置逻辑 | `_determine_tile_config()` | ✅ |
| 5. 保存正确配置 | `accepted_rotations` 字段 | ✅ |
| 6. 打乱瓷砖 | `_create_scrambled_state()` | ✅ |
| 7. 难度控制 | `DifficultyConfig` + 验证 | ✅ |

---

## 🎮 使用示例

### 基础用法

```python
from src.core.level.level_generator_v3 import LevelGeneratorV3
from src.core.level.difficulty_config import DifficultyLevel

# 创建生成器
generator = LevelGeneratorV3(difficulty=DifficultyLevel.NORMAL)

# 生成关卡
result = generator.generate()

# 访问结果
print(f"网格大小: {result['grid_size']}")
print(f"路径长度: {len(result['path'])}")
print(f"可移动瓷砖: {result['movable_count']}")
print(f"拐角数量: {result['corner_count']}")
```

### 通过 LevelManager 使用

```python
from src.core.level.level_manager import LevelManager
from src.core.level.level_loader import LevelLoader

loader = LevelLoader()
manager = LevelManager(loader)

# 加载生成的关卡
manager.load_generated_level(difficulty="normal", level_number=1)
```

### 通过 GameController 使用

```python
from src.integration.game_controller import GameController

controller = GameController()
controller.initialize()

# 启动游戏（自动使用 V3 生成器）
controller.start_game(difficulty="normal")
```

---

## 🐛 已知限制

### 1. 极小网格限制

在极小的网格（如 3x3）上生成高难度关卡可能失败，因为空间不足以满足最小路径长度要求。

**解决方案**: 系统会自动重试最多 50 次，或者调整难度配置。

### 2. 路径随机性

由于使用 DFS 而不是 BFS，生成的路径可能不是最短路径，这是**预期行为**，可以增加游戏趣味性。

---

## 📝 总结

`level_generator_v3.py` 完全按照用户的算法规范实现，包括：

1. ✅ **精确的精灵旋转定义** - 0°/90°/180°/270° 含义明确
2. ✅ **完整的瓷砖配置逻辑** - 基于前/当前/下一个格子的相对位置
3. ✅ **DFS 路径查找** - 不要求最短路径
4. ✅ **难度控制系统** - 可移动瓷砖数量 + 打乱比例
5. ✅ **验证机制** - 确保生成的关卡符合要求

算法已经过测试验证，可以正常工作。

---

**作者**: Circuit Repair Game Team
**日期**: 2026-01-23
**版本**: 3.0
**状态**: ✅ 已完成并验证
