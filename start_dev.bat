@echo off
REM ========================================
REM 电路板修复游戏 - 开发环境启动脚本
REM ========================================

echo ========================================
echo 电路板修复游戏 - 开发环境启动
echo ========================================
echo.

REM 激活conda环境
echo [1/3] 激活conda环境...
call conda activate Game
if errorlevel 1 (
    echo ✗ 激活conda环境失败
    echo 请确保已安装Anaconda/Miniconda
    pause
    exit /b 1
)
echo ✓ conda环境已激活
echo.

REM 检查Python版本
echo [2/3] 检查Python环境...
python --version
echo.

REM 进入项目目录
echo [3/3] 进入项目目录...
cd /d E:\projects\my_app\game
echo ✓ 当前目录: %CD%
echo.

echo ========================================
echo 环境已就绪，可以开始开发！
echo ========================================
echo.
echo 常用命令:
echo   - 验证环境: python tools/scripts/verify_environment.py
echo   - 运行游戏: python main.py
echo   - 运行测试: pytest
echo   - 代码格式化: black src/
echo   - 代码检查: pylint src/
echo.
echo ========================================

REM 保持窗口打开
cmd /k
