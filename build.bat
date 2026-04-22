@echo off
setlocal enabledelayedexpansion

set "APP_NAME=ReqPrompt"
set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "VENV_DIR=%ROOT_DIR%\venv"

cd /d "%ROOT_DIR%"

echo === %APP_NAME% - Build ===

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instalalo desde https://python.org
    exit /b 1
)

if not exist "%VENV_DIR%" (
    echo ^> Entorno virtual no encontrado. Ejecutando setup inicial...
    call "%ROOT_DIR%\setup.bat"
    if errorlevel 1 exit /b 1
)

echo ^> Activando entorno virtual...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 exit /b 1

echo ^> Instalando dependencias de compilacion...
python -m pip install --upgrade pip -q
if errorlevel 1 exit /b 1
python -m pip install pyinstaller -q
if errorlevel 1 exit /b 1

echo ^> Limpiando artefactos previos...
if exist "%ROOT_DIR%\build" rmdir /s /q "%ROOT_DIR%\build"
if exist "%ROOT_DIR%\dist" rmdir /s /q "%ROOT_DIR%\dist"

echo ^> Compilando aplicacion...
python -m PyInstaller --noconfirm --clean "%ROOT_DIR%\ReqPrompt.spec"
if errorlevel 1 exit /b 1

echo.
echo Compilacion completada.
echo.
if exist "%ROOT_DIR%\dist\%APP_NAME%.exe" (
    echo Salida: %ROOT_DIR%\dist\%APP_NAME%.exe
) else (
    echo Salida: %ROOT_DIR%\dist\%APP_NAME%
)

endlocal
