@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 v2\install.py
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python 3.11+ is required. Install Python and run this installer again.
    exit /b 1
  )
  python v2\install.py
)
if errorlevel 1 exit /b %errorlevel%
echo.
echo SHDA installation and verification completed.
