@echo off
echo Restarting Niche Compass Backend Server...
echo.

echo Step 1: Stopping current server...
taskkill /f /im python.exe 2>nul
echo Server stopped.

echo.
echo Step 2: Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo Step 3: Starting new server...
cd /d "C:\Users\spice\OneDrive\Documents\Project Saya\niche-compass-monorepo\backend"
echo Current directory: %CD%
echo Starting Flask server...
python run.py

pause
