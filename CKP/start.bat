@echo off
echo ========================================
echo     Full Stack Application Launcher
echo     Backend (FastAPI) + Frontend (React)
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo Python OK!

echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)
echo Node.js OK!

echo Checking npm installation...
npm --version
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    pause
    exit /b 1
)
echo npm OK!

echo.
echo ========================================
echo Starting Servers...
echo ========================================

echo Starting Backend Server...
echo Opening backend in new window...
start "Backend - FastAPI" cmd /k "cd /d %CD%\backend && echo ===== BACKEND SERVER ===== && echo Starting FastAPI on http://localhost:8000 && echo Press Ctrl+C to stop && echo. && python main.py"

echo Waiting 2 seconds for backend...
ping -n 3 127.0.0.1 >nul

echo Starting Frontend Server...
echo Opening frontend in new window...  
start "Frontend - React" cmd /k "cd /d %CD%\template-react-vite-app && echo ===== FRONTEND SERVER ===== && echo Starting React dev server && echo This will open browser automatically && echo Press Ctrl+C to stop && echo. && npm run dev"

echo.
echo ===== BOTH SERVERS STARTED =====
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Check the 2 new command windows that opened!
echo Close this window is safe now.

echo.
echo ========================================
echo     Both servers are starting!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173 (default Vite port)
echo API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo You can close this launcher window now.
echo To stop servers, close their respective windows or press Ctrl+C in them.
echo ========================================
echo.
echo Press any key to close this launcher...
pause >nul
