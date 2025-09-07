@echo off
echo Starting Frontend Development Server...
echo ======================================

cd template-react-vite-app

echo Installing dependencies if needed...
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Starting Vite development server...
npm run dev

pause

