@echo off
rem Neodoo18Framework - Windows Batch Launcher
rem This file launches the Python CLI for Windows users

set SCRIPT_DIR=%~dp0
set PYTHON_CMD=python

rem Try different Python commands
where python >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :run
)

where python3 >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    goto :run
)

where py >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    goto :run
)

echo Error: Python not found in PATH
echo Please install Python 3.8+ and ensure it's in your PATH
echo Or try running directly: python framework\cli\neodoo.py
pause
exit /b 1

:run
"%PYTHON_CMD%" "%SCRIPT_DIR%framework\cli\neodoo.py" %*