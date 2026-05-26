@echo off
setlocal

cd /d "%~dp0"
title CaloriesCounter Bot

echo Starting CaloriesCounter bot...
echo.

python -m app.main
set "exit_code=%errorlevel%"

if not "%exit_code%"=="0" (
    echo.
    echo Bot stopped with exit code %exit_code%.
    pause
)

endlocal
