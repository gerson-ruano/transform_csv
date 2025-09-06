@echo off
title Empaquetando Aplicación
echo ===============================
echo    EMPAQUETADOR PYINSTALLER
echo ===============================
echo.

REM Navegar a la carpeta donde está este script
cd /d "%~dp0"

REM Verificar que estamos en la carpeta correcta
echo Carpeta actual: %CD%
echo.
pip install pyinstaller
REM Ejecutar PyInstaller correctamente
pyinstaller --onefile --clean --name="ProcesadorCSV" main.py

echo.
echo ✅ Ejecutable creado en: dist\ProcesadorCSV.exe
echo.
pause