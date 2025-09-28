# Neodoo18Framework - PowerShell Launcher
# This file launches the Python CLI for Windows PowerShell users

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonCMDs = @("python", "python3", "py")
$PythonFound = $false

foreach ($cmd in $PythonCMDs) {
    try {
        & $cmd --version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $PythonCmd = $cmd
            $PythonFound = $true
            break
        }
    }
    catch {
        continue
    }
}

if (-not $PythonFound) {
    Write-Host "Error: Python not found in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and ensure it's in your PATH" -ForegroundColor Yellow
    Write-Host "Or try running directly: python framework\cli\neodoo.py" -ForegroundColor Cyan
    Read-Host "Press Enter to continue"
    exit 1
}

# Execute the Python CLI
& $PythonCmd "$ScriptDir\framework\cli\neodoo.py" $args