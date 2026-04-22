@echo off
REM ─── run.bat — Windows ────────────────────────────────────────────────────
if not exist venv (
    echo Primero ejecuta: setup.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python main.py
