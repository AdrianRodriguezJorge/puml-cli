@echo off
setlocal enabledelayedexpansion

REM Verify if Python is installed
py --version >nul 2>&1
if %errorlevel% equ 0 (
    py install.py %*
    goto end
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    python install.py %*
    goto end
)

echo [ERROR] Python was not found on this system. Please install Python 3.x and add it to your PATH.
pause

:end
