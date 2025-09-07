@echo off
echo ========================================
echo    Advanced Writing Tracker Server
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found! Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python server.py

pause
