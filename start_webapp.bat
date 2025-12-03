@echo off
echo.
echo ===============================================
echo   MiniLang Compiler Web Application
echo   Authors: Shozab Mehdi, Taha Sharif
echo   Course: CS-4031 - Compiler Construction
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install streamlit pandas >nul 2>&1

REM Run the app
echo.
echo Starting MiniLang Compiler Web App...
echo The app will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py

pause