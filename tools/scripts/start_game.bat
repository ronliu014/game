@echo off
REM Circuit Repair Game Launcher
REM Quick launcher for the game

echo ========================================
echo   Circuit Repair Game
echo ========================================
echo.

REM Activate conda environment
call conda activate Game

REM Run the game
python src/main.py %*

pause
