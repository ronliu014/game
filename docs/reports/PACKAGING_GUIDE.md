# 电路修复游戏 - 发行说明

## 📦 打包说明

本游戏使用 PyInstaller 打包，生成的是**完全独立的可执行程序**。

### ✅ 目标机器要求

**无需安装任何依赖！**

- ❌ 不需要安装 Python
- ❌ 不需要安装 pygame
- ❌ 不需要运行 `pip install`
- ❌ 不需要任何其他依赖库

**系统要求：**
- Windows 7 或更高版本
- 64位操作系统
- 约 50MB 磁盘空间

### 📋 打包内容

```
CircuitRepairGame/
├── CircuitRepairGame.exe (4.7 MB)  # 主程序
└── _internal/ (45 MB)               # 所有依赖和资源
    ├── Python 解释器 (内嵌)
    ├── 15 个 .pyd 文件 (Python扩展)
    ├── 65 个 .dll 文件 (系统库)
    ├── assets/ (游戏资源)
    │   ├── sprites/ (48个图片文件)
    │   ├── audio/ (音频文件)
    │   └── fonts/ (字体文件)
    └── data/ (配置和关卡)
        ├── config/ (4个配置文件)
        └── levels/ (7个关卡文件)
```

**总大小：约 48.7 MB**

### 🚀 发行方式

#### 方式1：ZIP压缩包（推荐）✅

1. 将整个 `dist/CircuitRepairGame/` 目录打包成 ZIP
2. 命名格式：`CircuitRepairGame-v1.0.1-win64.zip`
3. 用户解压后直接运行 `CircuitRepairGame.exe`

**优点：**
- 启动速度快
- 文件结构清晰
- 便于更新资源

**打包命令：**
```bash
cd dist
zip -r CircuitRepairGame-v1.0.1-win64.zip CircuitRepairGame/
```

或在 Windows 上：
```batch
cd dist
powershell Compress-Archive -Path CircuitRepairGame -DestinationPath CircuitRepairGame-v1.0.1-win64.zip
```

#### 方式2：单文件EXE（可选）

如果需要单文件发行，修改 `circuit_repair_game.spec`：
- 注释掉 COLLECT 部分（第147-156行）
- 取消注释单文件 EXE 部分（第160-183行）
- 重新运行 `pyinstaller circuit_repair_game.spec`

**注意：** 单文件模式启动较慢，不推荐。

### 📝 用户安装说明

创建一个 `README.txt` 放在 ZIP 包中：

```
电路修复游戏 v1.0.1
Circuit Repair Game v1.0.1

=== 安装说明 ===

1. 解压此 ZIP 文件到任意目录
2. 双击运行 CircuitRepairGame.exe
3. 开始游戏！

=== 系统要求 ===

- Windows 7 或更高版本
- 64位操作系统
- 约 50MB 磁盘空间

=== 无需安装 ===

本游戏是独立程序，无需安装 Python 或任何依赖库。
解压后即可直接运行。

=== 卸载 ===

直接删除整个游戏目录即可。

=== 技术支持 ===

如有问题，请访问：https://github.com/ronliu014/game

=== 版本信息 ===

版本：v1.0.1
发布日期：2026-01-26
```

### 🧪 验证打包完整性

运行验证脚本：
```bash
python tools/scripts/verify_package.py dist/CircuitRepairGame
```

### 🔒 数字签名（可选）

为了避免 Windows SmartScreen 警告，建议对 EXE 进行数字签名：

1. 购买代码签名证书
2. 使用 `signtool` 签名：
   ```batch
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com CircuitRepairGame.exe
   ```

### 📊 打包统计

- **主程序大小：** 4.7 MB
- **依赖和资源：** 44 MB
- **总大小：** 48.7 MB
- **Python扩展：** 15 个 .pyd 文件
- **系统库：** 65 个 .dll 文件
- **游戏资源：** 48 个图片文件
- **配置文件：** 4 个 JSON 文件
- **关卡文件：** 7 个 JSON 文件

### ✅ 发行检查清单

打包前检查：
- [ ] 所有功能测试通过
- [ ] 资源文件完整
- [ ] 配置文件正确
- [ ] 版本号更新

打包后检查：
- [ ] 运行验证脚本
- [ ] 在干净的机器上测试（无Python环境）
- [ ] 检查文件大小合理
- [ ] 创建 ZIP 压缩包
- [ ] 编写发行说明

发行：
- [ ] 上传到 GitHub Releases
- [ ] 创建 tag
- [ ] 更新 CHANGELOG.md
- [ ] 通知用户

### 🎯 常见问题

**Q: 用户需要安装 Python 吗？**
A: 不需要！程序已经包含了 Python 解释器。

**Q: 用户需要运行 pip install 吗？**
A: 不需要！所有依赖库都已打包。

**Q: 为什么有 _internal 目录？**
A: 这是 PyInstaller 的标准结构，包含所有依赖和资源。

**Q: 可以只发布 .exe 文件吗？**
A: 不可以！必须包含 _internal 目录，否则程序无法运行。

**Q: 如何减小文件大小？**
A: 已经通过 spec 文件排除了不必要的库（numpy, matplotlib等）。

**Q: Windows Defender 报毒怎么办？**
A: 这是误报。可以通过数字签名解决，或者提交样本给微软。

### 📚 相关文档

- [构建脚本](../../build.bat)
- [PyInstaller配置](../../circuit_repair_game.spec)
- [项目README](../../README.md)
- [变更日志](../../CHANGELOG.md)
