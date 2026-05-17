@echo off
echo ==============================
echo Starting FastAPI backend
echo ==============================

REM Activate venv
call venv\Scripts\activate.bat

REM Start server
uvicorn backend.main:app --reload

pause