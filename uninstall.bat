@echo off
setlocal enabledelayedexpansion

REM Verify if Python is installed
py --version >nul 2>&1
if %errorlevel% equ 0 (
    py uninstall.py %*
    goto end
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    python uninstall.py %*
    goto end
)

echo [ERROR] Python was not found on this system. Cannot run uninstaller.
pause

:end
