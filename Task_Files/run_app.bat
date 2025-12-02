@echo off
REM ScoreSight - Launch Script
REM This script starts the Streamlit application

echo ========================================
echo   ScoreSight - EPL Prediction Hub
echo ========================================
echo.

REM Check if in correct directory
REM Check if in correct directory
if not exist "Final_Project\Frontend_Code\main.py" (
    echo ERROR: Please run this script from the ScoreSight root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Starting Streamlit application...
echo.
echo The app will open automatically in your browser
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit
cd Final_Project\Frontend_Code
streamlit run main.py

pause
