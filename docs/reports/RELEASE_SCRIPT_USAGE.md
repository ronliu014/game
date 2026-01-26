# 发行打包脚本使用说明

## 两种方式

### 方式1：使用 PowerShell 脚本（推荐）

```powershell
.\create_release.ps1
```

**优点：**
- 彩色输出，更易读
- 更好的错误处理
- 显示详细进度

### 方式2：使用 CMD 批处理

在 CMD（不是PowerShell）中运行：

```cmd
create_release.bat
```

**注意：** 必须在 CMD 中运行，不要在 PowerShell 中运行 .bat 文件！

## 如果遇到问题

### 问题1：PowerShell 执行策略限制

如果提示"无法加载，因为在此系统上禁止运行脚本"：

```powershell
# 临时允许执行脚本
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 然后运行脚本
.\create_release.ps1
```

### 问题2：在 PowerShell 中运行 .bat 文件

**错误做法：**
```powershell
.\create_release.bat  # ❌ 会出现编码问题
```

**正确做法：**
```powershell
cmd /c create_release.bat  # ✅ 通过 cmd 运行
```

或者直接使用 PowerShell 脚本：
```powershell
.\create_release.ps1  # ✅ 推荐
```

## 输出结果

脚本会创建：

```
release/
├── CircuitRepairGame-v1.0.1-win64/     # 发行目录
│   ├── CircuitRepairGame.exe
│   ├── _internal/
│   ├── README.txt
│   ├── LICENSE.txt
│   └── CHANGELOG.txt
├── CircuitRepairGame-v1.0.1-win64.zip  # 发行包
└── CircuitRepairGame-v1.0.1-win64.zip.sha256  # 校验和
```

## 手动打包（如果脚本失败）

如果脚本无法运行，可以手动打包：

1. 复制 `dist/CircuitRepairGame/` 到 `release/CircuitRepairGame-v1.0.1-win64/`
2. 复制 `README_USER.txt` 到发行目录并重命名为 `README.txt`
3. 复制 `LICENSE` 和 `CHANGELOG.md` 到发行目录
4. 右键点击发行目录 → 发送到 → 压缩(zipped)文件夹
5. 重命名为 `CircuitRepairGame-v1.0.1-win64.zip`

## 验证打包

```bash
python tools/scripts/verify_package.py release/CircuitRepairGame-v1.0.1-win64
```

## 生成校验和（手动）

```cmd
certutil -hashfile release\CircuitRepairGame-v1.0.1-win64.zip SHA256
```
