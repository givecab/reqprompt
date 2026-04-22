@echo off
REM ─── setup.bat — Windows ──────────────────────────────────────────────────
echo === ReqPrompt - Setup ===

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instalalo desde https://python.org
    pause
    exit /b 1
)

echo Creando entorno virtual...
python -m venv venv

echo Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo.
echo Setup completo.
echo Para iniciar: run.bat
pause
