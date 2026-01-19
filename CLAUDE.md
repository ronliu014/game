# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python Environment

This project uses the conda environment Game, with the path: D:\anaconda3\envs\Game.

Before executing any Python commands, you must run the following command first:

```plaintext
conda activate Game
```

Do not use the system's default Python interpreter.

## Project Overview

This is a circuit board repair puzzle game (修复电路板) - a standalone mini-game that can be invoked by other systems. Players rotate circuit pieces on a grid to connect a power source to a terminal endpoint.

## Current State

**Current Phase**: Stage 0 - Environment Setup & Technical Planning

The project has completed comprehensive planning and documentation:
- ✅ Complete project specification system established
- ✅ Directory structure standards defined
- ✅ Development and documentation standards created
- ⏳ Technical stack selection in progress
- ⏳ Code implementation not yet started

### 📚 Documentation Index

**完整文档导航**: [docs/INDEX.md](docs/INDEX.md) ⭐ **必读** - 所有文档的索引和快速查找指南

#### 规范文档 (Specifications)
所有规范文档位于 `docs/specifications/`，**强制遵守**：

| 序号 | 文档名称 | 用途 | 优先级 |
|------|---------|------|--------|
| 00 | [项目规划总纲](docs/specifications/00_项目规划总纲.md) | 项目整体规划与指导原则 | ⭐⭐⭐ |
| 01 | [技术方案文档](docs/specifications/01_技术方案文档.md) | 技术选型与架构设计 | ⭐⭐ |
| 02 | [目录结构规范](docs/specifications/02_目录结构规范.md) | 文件组织与命名规则 | ⭐⭐⭐ |
| 03 | [文档编写规范](docs/specifications/03_文档编写规范.md) | 文档格式与模板标准 | ⭐⭐⭐ |
| 04 | [日志系统规范](docs/specifications/04_日志系统规范.md) | 日志记录标准与实现 | ⭐⭐⭐ |
| 05 | [开发规范](docs/specifications/05_开发规范.md) | 代码风格与开发流程 | ⭐⭐⭐ |
| 06 | [项目实施路线图](docs/specifications/06_项目实施路线图.md) | 开发计划与里程碑 | ⭐⭐ |

#### 设计文档 (Design)
游戏设计和系统设计文档位于 `docs/design/`：

| 文档名称 | 用途 | 状态 |
|---------|------|------|
| [派对游戏 - 修复电路板](docs/design/派对游戏%20-%20修复电路板_设计文档.md) | 游戏核心玩法与系统设计 | ✅ 完成 |
| UI设计规范 | UI/UX设计标准 | ⏳ 待创建 |
| API接口文档 | 外部集成接口 | ⏳ 待创建 |

#### 资源文档 (Assets)
设计稿和可视化资源位于 `docs/assets/`：

- **UI设计稿**: [docs/assets/image/](docs/assets/image/) (12张界面设计图)

### 新成员必读顺序

1. **[文档索引](docs/INDEX.md)** - 了解文档结构
2. **[项目规划总纲](docs/specifications/00_项目规划总纲.md)** - 了解项目全貌
3. **[开发规范](docs/specifications/05_开发规范.md)** - 掌握开发标准
4. **[目录结构规范](docs/specifications/02_目录结构规范.md)** - 熟悉项目结构
5. **[游戏设计文档](docs/design/派对游戏%20-%20修复电路板_设计文档.md)** - 理解游戏设计

## Game Design Key Points

### Core Mechanics
- Grid-based puzzle: NxN board with circuit pieces (power source, terminal, straight lines, corner pieces)
- Player clicks black tiles to rotate circuit pieces 90° clockwise
- Victory condition: Complete electrical path from power source to terminal
- Industrial steampunk aesthetic with copper/brass elements

### Level Design System
Levels are defined by:
1. Grid size (e.g., 4x4)
2. Correct circuit layout with rotation angles
3. Intentionally rotated pieces (shown as black/clickable tiles)

### Visual & Audio Requirements
- **Visual Effects**: Electrical current animation along connected paths, terminal glow-up on completion, celebratory particle effects
- **Audio**: Gear rotation clicks, electrical hum on connection, victory fanfare
- **BGM**: Reduce to 20% when game UI is active

### Integration Requirements
- Must be callable as standalone module from external systems
- Support level selection (single or multiple levels)
- No progress persistence required on exit

## Development Guidelines

### MANDATORY: Follow All Standards
**All code implementation MUST strictly adhere to the project specifications:**

1. **Code Style**: Follow [Development Standards](docs/05_开发规范.md)
   - PEP 8 compliance
   - Type annotations required
   - Unit test coverage ≥80%
   - All public APIs must have docstrings

2. **File Organization**: Follow [Directory Structure Standards](docs/02_目录结构规范.md)
   - Organize by function, not file type
   - Use standardized naming conventions
   - Maximum 4 directory levels

3. **Logging**: Follow [Logging System Standards](docs/04_日志系统规范.md)
   - Use structured logging format
   - Log all critical operations
   - Performance logging required
   - No sensitive information in logs

4. **Documentation**: Follow [Documentation Standards](docs/03_文档编写规范.md)
   - Update docs with code changes
   - Use standardized templates
   - Include code examples

### Architecture Principles (from specifications)
- **Separation of Concerns**: Core logic (`src/core/`) must be independent of rendering
- **Data-Driven Design**: Level configurations in JSON format under `data/levels/`
- **Modular Integration**: Clear API boundary in `src/integration/`
- **Performance First**: Meet all performance targets (60 FPS, <2s startup, <500ms level load)

### Critical Implementation Requirements
- **Connectivity Algorithm**: BFS-based path finding from power source to terminal (O(N²) complexity)
- **Rotation System**: 90° clockwise rotation, 0/90/180/270 states
- **Win Condition**: Complete path validation before victory sequence
- **State Management**: Proper game state machine implementation

### Level Data Format
See [Implementation Roadmap](docs/06_项目实施路线图.md) Section 4.2.3 for detailed JSON schema.

## Standard Directory Structure

**MUST follow this structure** (see [Directory Structure Standards](docs/02_目录结构规范.md) for complete details):

```
circuit-repair-game/
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── core/              # Game logic (no rendering dependencies)
│   │   ├── grid/          # Grid system
│   │   ├── circuit/       # Connectivity algorithms
│   │   ├── level/         # Level management
│   │   └── game_state/    # State machine
│   ├── rendering/         # Rendering layer
│   │   ├── animation/     # Animation system
│   │   ├── effects/       # Visual effects
│   │   └── ui/            # UI components
│   ├── audio/             # Audio system
│   ├── input/             # Input handling
│   ├── integration/       # External API
│   ├── config/            # Configuration
│   └── utils/             # Utilities (logger, etc.)
├── assets/                # Game resources
│   ├── sprites/           # Images
│   ├── audio/             # Sound files
│   └── fonts/             # Fonts
├── data/                  # Data files
│   ├── levels/            # Level JSON files
│   └── config/            # Configuration JSON
├── tests/                 # Test code
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
└── tools/                 # Development tools
```

## Technology Stack

**Recommended**: Python + Pygame (see [Implementation Roadmap](docs/06_项目实施路线图.md) Section 2.2.1)

**Rationale**:
- Matches existing conda environment (Game)
- Fast development cycle
- Easy external integration
- Sufficient 2D performance
- Rich ecosystem

**Alternative options**: Pyglet, Unity, Godot (requires separate evaluation)

## Next Steps

Before starting implementation:
1. ✅ Review all specification documents
2. ⏳ Finalize technology stack decision
3. ⏳ Set up development environment (conda, dependencies)
4. ⏳ Create project directory structure
5. ⏳ Initialize Git repository
6. ⏳ Begin Stage 1: Core Framework Development

See [Implementation Roadmap](docs/06_项目实施路线图.md) for detailed development plan (8-12 weeks).
